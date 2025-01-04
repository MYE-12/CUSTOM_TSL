# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveSalary(Document):
	def after_insert(self):
		if self.leave_application:
			frappe.db.set_value("Leave Application Form",self.leave_application,"leave_salary_reference",self.name,update_modified = False)


@frappe.whitelist()
def check_for_active_loans(name):
	status = "Not Exists"
	if frappe.db.exists("Loan",{'applicant_name':name,'status':("not in",["Closed"])}):
		status = "Exists"
	return status
