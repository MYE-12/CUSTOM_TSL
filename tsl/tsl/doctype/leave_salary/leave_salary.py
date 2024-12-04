# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveSalary(Document):
	pass

@frappe.whitelist()
def check_for_active_loans(name):
	status = "Not Exists"
	if frappe.db.exists("Loan",{'applicant_name':name,'status':("not in",["Closed"])}):
		status = "Exists"
	return status
