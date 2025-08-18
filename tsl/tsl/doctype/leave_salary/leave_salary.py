# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveSalary(Document):
	def on_submit(self):
		if self.is_leaves_encashed and self.encashment_days:
			self.create_leave_encashment()
		
	def on_cancel(self):
		if self.leave_encashment:
			doc = frappe.get_doc("Leave Encashment Data",self.leave_encashment)
			if doc.docstatus == 1:
				ad_sal = frappe.get_doc("Additional Salary",{'ref_docname':doc.name})
				if ad_sal.docstatus ==1:
					ad_sal.cancel()
				doc.cancel()

	def after_insert(self):
		if self.leave_application:
			frappe.db.set_value("Leave Application Form",self.leave_application,"leave_salary_reference",self.name,update_modified = False)

	def on_trash(self):
		frappe.db.set_value("Leave Application Form",self.leave_application,"leave_salary_reference",'',update_modified = False)

	def create_leave_encashment(self):
		doc = frappe.new_doc("Leave Encashment Data")
		doc.company = self.company
		doc.employee = self.employee
		doc.currency = self.currency
		doc.encashment_days = self.encashment_days
		doc.leave_type = "Annual Leave"
		doc.save(ignore_permissions = True)
		doc.submit()
		self.leave_encashment = doc.name
		frappe.db.set_value("Leave Salary",self.name,"leave_encashment",doc.name,update_modified = False)

@frappe.whitelist()
def check_for_active_loans(name):
	status = "Not Exists"
	if frappe.db.exists("Loan",{'applicant_name':name,'status':("not in",["Closed"])}):
		status = "Exists"
	return status



@frappe.whitelist()
def check_balance_leaves(employee):
	actual_leave_balance = 0
	from frappe.utils import getdate
	today = getdate()
	from hrms.hr.doctype.leave_application.leave_application import get_leave_details
	val = get_leave_details(employee, today)

	# Check if 'Annual Leave' allocation exists
	if 'Annual Leave' in val['leave_allocation']:
		annual_leave_balance = val['leave_allocation']['Annual Leave']['remaining_leaves']
		
		# Check if there are any draft Planned Leaves
		if frappe.db.exists("Planned Leaves", {'employee': employee, 'docstatus': 0}):
			planned_leave_balance = frappe.db.get_value("Planned Leaves", 
													{'employee': employee, 'docstatus': 0}, 
													'leave_days') or 0
			# Subtract the planned leave balance from the annual leave balance
			actual_leave_balance = annual_leave_balance - planned_leave_balance
		else:
			# If no planned leaves are found, just use the annual leave balance
			actual_leave_balance = annual_leave_balance
	else:
		actual_leave_balance = 0

	return actual_leave_balance