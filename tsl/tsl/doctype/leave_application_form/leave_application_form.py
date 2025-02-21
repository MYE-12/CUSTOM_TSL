# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

from frappe import _
from frappe.query_builder.functions import Max, Min, Sum
from frappe.utils import (
	add_days,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_fullname,
	get_link_to_form,
	getdate,
	nowdate,
)

from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import daterange
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee

from hrms.hr.doctype.leave_block_list.leave_block_list import get_applicable_block_dates
from hrms.hr.doctype.leave_ledger_entry.leave_ledger_entry import create_leave_ledger_entry
from hrms.hr.utils import (
	get_holiday_dates_for_employee,
	get_leave_period,
	set_employee_name,
	share_doc_with_approver,
	validate_active_employee,
)

from hrms.hr.doctype.leave_application.leave_application import get_leave_details
from frappe.utils.dateutils import get_from_date_from_timespan, get_period_ending
from frappe.utils import add_to_date, formatdate, get_link_to_form, getdate, nowdate

class LeaveApplicationForm(Document):
	def validate(self):
		self.travel_days = date_diff(self.to_date, self.from_date) + 1
		self.validate_applicable_after()
	
	def validate_applicable_after(self):
		if self.leave_type:
			leave_type = frappe.get_doc("Leave Type", self.leave_type)
			if leave_type.applicable_after > 0:
				date_of_joining = frappe.db.get_value("Employee", self.employee, "date_of_joining")
				leave_days = get_approved_leaves_for_period(
					self.employee, False, date_of_joining, self.from_date
				)
				number_of_days = date_diff(getdate(self.from_date), date_of_joining)
				if number_of_days >= 0:
					holidays = 0
					if not frappe.db.get_value("Leave Type", self.leave_type, "include_holiday"):
						holidays = get_holidays_no(self.employee, date_of_joining, self.from_date)
					number_of_days = number_of_days - leave_days - holidays
					if number_of_days < leave_type.applicable_after:
						frappe.throw(
							_("{0} applicable after {1} working days").format(
								self.leave_type, leave_type.applicable_after
							)
						)

	def trigger_mail_on_submission(self):
		parent_doc = frappe.get_doc("Leave Application Form", self.name)
		args = parent_doc.as_dict()

		email_template = frappe.get_doc("Email Template", "Leave Application Approved")
		subject = frappe.render_template(email_template.subject, args)
		message = frappe.render_template(email_template.response, args)
		if self.user_id:
			try:
				frappe.sendmail(
					recipients=self.user_id,
					sender= self.user_id,
					subject = subject,
					message = message,
				)
				frappe.msgprint(_("Email sent to {0}").format(self.user_id))
			except frappe.OutgoingEmailError:
				pass
		else:
			try:
				frappe.sendmail(
					recipients=self.user_id,
					sender= "info@tsl-me.com",
					subject = subject,
					message = message,
				)
				frappe.msgprint(_("Email sent to {0}").format(self.user_id))
			except frappe.OutgoingEmailError:
				pass
		
	def on_trash(self):
		exists = frappe.db.exists("Planned Leaves",{"reference":self.name})
		frappe.delete_doc("Planned Leaves", exists, force=1)

	def on_submit(self):
		if self.workflow_state == "Approved":
			self.trigger_mail_on_submission()
		if self.leave_projection == 1:
			pl = frappe.new_doc("Planned Leaves")
			fields = [field.fieldname for field in frappe.get_meta(self.doctype).fields 
					if field.fieldtype not in ['HTML', 'Button', 'Tab Break', 'Section Break', 'Column Break']
					and field.fieldname not in ["amended_from"]]
			for field in fields:
				setattr(pl, field, getattr(self, field))
			pl.reference = self.name
			pl.save(ignore_permissions=1)


		else:
			if self.leave_type != "Leave Without Pay":
				if self.lop_start_date:
					lop = frappe.new_doc("Leave Application")
					lop.employee = self.employee
					lop.no_of_tickets = self.no_of_tickets
					lop.from_date = self.lop_start_date
					lop.to_date = self.lop_end_date
					lop.description = self.description
					lop.leave_type = "Leave Without Pay"
					lop.posting_date = self.posting_date
					if self.workflow_state == "Approved":
						lop.status = "Approved"
					else:
						lop.status = "Rejected"

					lop.follow_via_email = 0
					lop.save(ignore_permissions=1)
					lop.submit()

				l_ap = frappe.new_doc("Leave Application")
				l_ap.employee = self.employee
				l_ap.no_of_tickets = self.no_of_tickets
				l_ap.from_date = self.leave_start_date
				l_ap.to_date = self.leave_end_date
				l_ap.description = self.description
				l_ap.no_of_tickets = self.no_of_tickets
				l_ap.ticket_used = self.ticket_used
				l_ap.leave_type = self.leave_type
				l_ap.posting_date = self.posting_date
				if self.workflow_state == "Approved":
					l_ap.status = "Approved"
				else:
					l_ap.status = "Rejected"

				l_ap.follow_via_email = 0
				l_ap.save(ignore_permissions =1)
				l_ap.submit()
			else:
				l_ap = frappe.new_doc("Leave Application")
				l_ap.employee = self.employee
				l_ap.no_of_tickets = self.no_of_tickets
				l_ap.from_date = self.from_date
				l_ap.to_date = self.to_date
				l_ap.description = self.description
				l_ap.no_of_tickets = self.no_of_tickets
				l_ap.ticket_used = self.ticket_used
				l_ap.leave_type = self.leave_type
				l_ap.posting_date = self.posting_date
				if self.workflow_state == "Approved":
					l_ap.status = "Approved"
				else:
					l_ap.status = "Rejected"

				l_ap.follow_via_email = 0
				l_ap.save(ignore_permissions =1)
				l_ap.submit()



	
@frappe.whitelist()
def get_dates_from_timegrain(from_date, to_date, timegrain, holidays,company):
	days = months = years = 0
	if "Daily" == timegrain:
		days = 1
	dates = [get_period_ending(from_date, timegrain)]
	while getdate(dates[-1]) < getdate(to_date):
		date = get_period_ending(add_to_date(dates[-1], years=years, months=months, days=days), timegrain)
		dates.append(date)
	if company == "TSL COMPANY - Kuwait":
		dates = [date for date in dates if date not in holidays]
	else:
		dates = [date for date in dates]
	return dates

def get_holidays(employee, from_date, to_date, holiday_list=None):
	"""Get holidays between two dates for the given employee."""
	if not holiday_list:
		holiday_list = get_holiday_list_for_employee(employee)
	holidays = frappe.db.sql(
		"""select distinct holiday_date from `tabHoliday` h1, `tabHoliday List` h2
		where h1.parent = h2.name and h1.holiday_date between %s and %s
		and h2.name = %s order by h1.holiday_date """,
		(from_date, to_date, holiday_list), as_dict=1
	)
	return [holiday['holiday_date'] for holiday in holidays]

@frappe.whitelist()
def get_roles(user_id):
	if "Leave Approver" in frappe.get_roles(user_id):
		return True
	else:
		return False

@frappe.whitelist()
def trigger_mail(name,workflow_state = None,email = None,leave_approver = None,hr_mail = None):
	if leave_approver:
		parent_doc = frappe.get_doc("Leave Application Form", name)
		args = parent_doc.as_dict()

		email_template = frappe.get_doc("Email Template", "Leave Approval Notification")
		subject = frappe.render_template(email_template.subject, args)
		message = frappe.render_template(email_template.response, args)
		# frappe.errprint("working")
		try:
			frappe.sendmail(
				recipients=leave_approver,
				sender= "yousuf@tsl-me.com",
				subject = subject,
				message = message,
			)
			frappe.msgprint(_("Email sent to {0}").format(leave_approver))
		except frappe.OutgoingEmailError:
			pass
	else:
		parent_doc = frappe.get_doc("Leave Application Form", name)
		args = parent_doc.as_dict()

		email_template = frappe.get_doc("Email Template", "Leave Approval Notification")
		subject = frappe.render_template(email_template.subject, args)
		message = frappe.render_template(email_template.response, args)
		try:
			frappe.sendmail(
				recipients=email,
				cc = hr_mail,
				sender= "yousuf@tsl-me.com",
				subject = subject,
				message = message,
			)
			frappe.msgprint(_("Email sent to {0}").format(email))
		except frappe.OutgoingEmailError:
			pass
			
@frappe.whitelist()
def trigger_mail_to_hr(name,workflow_state = None,company = None,leave_approver = None):
	if company == "TSL COMPANY - KSA":
		email= ['admin@tsl-me.com','hr@tsl-me.com','yousuf@tsl-me.com']
	else:
		email= ['hr@tsl-me.com','yousuf@tsl-me.com']
	parent_doc = frappe.get_doc("Leave Application Form", name)
	args = parent_doc.as_dict()

	email_template = frappe.get_doc("Email Template", "Leave Approval Notification")
	subject = frappe.render_template(email_template.subject, args)
	message = frappe.render_template(email_template.response, args)
	try:
		frappe.sendmail(
			recipients=email,
			sender= "yousuf@tsl-me.com",
			subject = subject,
			message = message,
		)
		frappe.msgprint(_("Email sent to {0}").format(email))
	except frappe.OutgoingEmailError:
		pass

@frappe.whitelist()
def validate_balance_leaves(company,from_date,to_date,employee,leave_type,half_day = None,half_day_date = None):
	holiday_list = frappe.db.get_value("Employee",employee,'holiday_list') or None
	total_leave_days = get_number_of_leave_days(
		company,
		employee,
		leave_type,
		from_date,
		to_date,
		half_day,
		half_day_date,
		holiday_list
	)
	return total_leave_days


@frappe.whitelist()
def validate_balance_leaves_lop(company,from_date,to_date,employee,leave_type,half_day = None,half_day_date = None):
	holiday_list = frappe.db.get_value("Employee",employee,'holiday_list') or None
	total_leave_days = get_number_of_leave_days_lop(
		company,
		employee,
		leave_type,
		from_date,
		to_date,
		half_day,
		half_day_date,
		holiday_list
	)
	return total_leave_days


@frappe.whitelist()
def get_number_of_leave_days(
	company:str,
	employee: str,
	leave_type: str,
	from_date: datetime.date,
	to_date: datetime.date,
	half_day: int | str | None = None,
	half_day_date: datetime.date | str | None = None,
	holiday_list: str | None = None,
) -> float:
	"""Returns number of leave days between 2 dates after considering half day and holidays
	(Based on the include_holiday setting in Leave Type)"""
	number_of_days = 0
	if cint(half_day) == 1:
		if getdate(from_date) == getdate(to_date):
			number_of_days = 0.5
		elif half_day_date and getdate(from_date) <= getdate(half_day_date) <= getdate(to_date):
			number_of_days = date_diff(to_date, from_date) + 0.5
		else:
			number_of_days = date_diff(to_date, from_date) + 1
	else:
		number_of_days = date_diff(to_date, from_date) + 1
	number_of_days = flt(number_of_days) - flt(
		get_holidays_no(employee, from_date, to_date, holiday_list=holiday_list, company=company)
	)
	return number_of_days

@frappe.whitelist()
def get_number_of_leave_days_lop(
	company:str,
	employee: str,
	leave_type: str,
	from_date: datetime.date,
	to_date: datetime.date,
	half_day: int | str | None = None,
	half_day_date: datetime.date | str | None = None,
	holiday_list: str | None = None,
) -> float:
	"""Returns number of leave days between 2 dates after considering half day and holidays
	(Based on the include_holiday setting in Leave Type)"""
	number_of_days = 0
	if cint(half_day) == 1:
		if getdate(from_date) == getdate(to_date):
			number_of_days = 0.5
		elif half_day_date and getdate(from_date) <= getdate(half_day_date) <= getdate(to_date):
			number_of_days = date_diff(to_date, from_date) + 0.5
		else:
			number_of_days = date_diff(to_date, from_date) + 1
	else:
		number_of_days = date_diff(to_date, from_date) + 1
	return number_of_days

def get_holidays_no(employee, from_date, to_date, holiday_list=None, company = None):
	"""get holidays between two dates for the given employee"""
	if not holiday_list:
		holiday_list = get_holiday_list_for_employee(employee)
	if company == "TSL COMPANY - Kuwait":
		holidays = frappe.db.sql(
			"""select count(distinct holiday_date) from `tabHoliday` h1, `tabHoliday List` h2
			where h1.parent = h2.name and h1.holiday_date between %s and %s
			and h2.name = %s and h1.weekly_off = 1 """,
			(from_date, to_date, holiday_list),
		)[0][0]
	else:
		holidays = frappe.db.sql(
			"""select count(distinct holiday_date) from `tabHoliday` h1, `tabHoliday List` h2
			where h1.parent = h2.name and h1.holiday_date between %s and %s
			and h2.name = %s and h1.weekly_off = 0 """,
			(from_date, to_date, holiday_list),
		)[0][0]

	return holidays


@frappe.whitelist()
def list_leave_dates(employee, from_date, to_date,leave_type,leave_balance,company):
	holidays = get_holidays(employee, from_date, to_date)
	dates = get_dates_from_timegrain(from_date, to_date, "Daily", holidays,company)
	frappe.log_error("holidays",holidays)
	frappe.log_error("dates",dates)
	if len(dates) > int(leave_balance):
		if frappe.db.exists("Leave Allocation",{"from_date": ["<=", from_date],"employee":employee,"leave_type":leave_type,"docstatus":1}):
			leave_days = int(leave_balance) or 0
			leave_start_date = dates[0]
			leave_end_date = dates[leave_days]
			return leave_start_date ,leave_end_date
	

@frappe.whitelist()
def trigger_mail_on_lap_form():
	current_date = nowdate()
	leaves = frappe.db.get_all("Leave Application Form",{'from_date':current_date,"leave_type":"Annual Leave"},['*'])
	for self in leaves:
		parent_doc = frappe.get_doc("Leave Application Form", self.name)
		args = parent_doc.as_dict()
		email_template = frappe.get_doc("Email Template", "Employee Travelling Today")
		subject = frappe.render_template(email_template.subject, args)
		message = frappe.render_template(email_template.response, args)
		try:
			frappe.sendmail(
				recipients="alkouh@tsl-me.com",
				sender= "info@tsl-me.com",
				subject = subject,
				message = message,
			)
		except frappe.OutgoingEmailError:
			pass

def schedule_trigger_mail_on_lap_form():
	job = frappe.db.exists('Scheduled Job Type', 'leave_application_form.trigger_mail_on_lap_form')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'tsl.tsl.doctype.leave_application_form.leave_application_form.trigger_mail_on_lap_form',
			"frequency" : 'Daily'
		})
		sjt.save(ignore_permissions=True)

def get_approved_leaves_for_period(employee, leave_type, from_date, to_date):
	LeaveApplication = frappe.qb.DocType("Leave Application Form")
	query = (
		frappe.qb.from_(LeaveApplication)
		.select(
			LeaveApplication.employee,
			LeaveApplication.leave_type,
			LeaveApplication.from_date,
			LeaveApplication.to_date,
			LeaveApplication.total_leave_days,
		)
		.where(
			(LeaveApplication.employee == employee)
			& (LeaveApplication.docstatus == 1)
			& (LeaveApplication.status == "Approved")
			& (
				(LeaveApplication.from_date.between(from_date, to_date))
				| (LeaveApplication.to_date.between(from_date, to_date))
				| ((LeaveApplication.from_date < from_date) & (LeaveApplication.to_date > to_date))
			)
		)
	)

	if leave_type:
		query = query.where(LeaveApplication.leave_type == leave_type)

	leave_applications = query.run(as_dict=True)

	leave_days = 0
	for leave_app in leave_applications:
		if leave_app.from_date >= getdate(from_date) and leave_app.to_date <= getdate(to_date):
			leave_days += leave_app.total_leave_days
		else:
			if leave_app.from_date < getdate(from_date):
				leave_app.from_date = from_date
			if leave_app.to_date > getdate(to_date):
				leave_app.to_date = to_date

			leave_days += get_number_of_leave_days(
				employee, leave_type, leave_app.from_date, leave_app.to_date
			)

	return leave_days
