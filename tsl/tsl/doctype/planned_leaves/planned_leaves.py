# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

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

from hrms.hr.doctype.leave_application.leave_application import get_number_of_leave_days,get_leave_details
from frappe.utils.dateutils import get_from_date_from_timespan, get_period_ending
from frappe.utils import add_to_date, formatdate, get_link_to_form, getdate, nowdate

class PlannedLeaves(Document):
	def on_submit(self):
		if self.lop_start_date:
			lop = frappe.new_doc("Leave Application")
			lop.employee = self.employee
			lop.no_of_tickets = self.no_of_tickets
			lop.from_date = self.lop_start_date
			lop.to_date = self.lop_end_date
			lop.description = self.description
			lop.leave_type = "Leave Without Pay"
			lop.posting_date = self.posting_date
			lop.status = "Approved"
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
		l_ap.status = "Approved"
		l_ap.follow_via_email = 0

		l_ap.save(ignore_permissions =1)
		l_ap.submit()

@frappe.whitelist()
def create_planned_leaves():
	current_time = datetime.today().date()
	doc = frappe.db.sql(""" select name from `tabPlanned Leaves` where from_date = '%s' """%(current_time),as_dict = 1)
	if doc:
		for k in doc:
			pl = frappe.get_doc("Planned Leaves", k.name)
			pl.submit()


# @frappe.whitelist()
# def cron_job_allocation():
# 	sjt = frappe.new_doc("Scheduled Job Type")  
# 	sjt.update({
# 		"method" : 'tsl.tsl.doctype.planned_leaves.planned_leaves.create_planned_leaves',
# 		"frequency" : 'Daily',
# 	})
# 	sjt.save(ignore_permissions=True)