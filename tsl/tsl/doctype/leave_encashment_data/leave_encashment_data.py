# Copyright (c) 2025, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
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
from datetime import datetime

class LeaveEncashmentData(Document):
	def on_submit(self):
		additional_salary = frappe.new_doc("Additional Salary")
		additional_salary.company = frappe.get_value("Employee", self.employee, "company")
		additional_salary.employee = self.employee
		additional_salary.currency = self.currency
		earning_component = frappe.get_value("Leave Type", self.leave_type, "earning_component")
		if not earning_component:
			frappe.throw(_("Please set Earning Component for Leave type: {0}.").format(self.leave_type))
		additional_salary.salary_component = earning_component

		encashment = datetime.strptime(str(self.encashment_date), "%Y-%m-%d")

		# Calculate the first date of the next month
		if encashment.month == 12:
			first_day_next_month = datetime(encashment.year + 1, 1, 1)
		else:
			first_day_next_month = datetime(encashment.year, encashment.month + 1, 1)

		# Set payroll_date to the first date of the next month
		additional_salary.payroll_date = first_day_next_month
		additional_salary.amount = self.encashment_amount
		additional_salary.ref_doctype = self.doctype
		additional_salary.ref_docname = self.name
		additional_salary.submit()

@frappe.whitelist()
def per_day_salary(employee):
	basic = frappe.db.get_value("Employee",employee,'ctc')
	company = frappe.db.get_value("Employee",employee,'company')
	working_days = frappe.db.get_value("Company Wise Payroll Days",{"company": company},"total_working_days")
	if basic and basic > 0:
		perday = basic / working_days
	else:
		perday = 0
	return perday