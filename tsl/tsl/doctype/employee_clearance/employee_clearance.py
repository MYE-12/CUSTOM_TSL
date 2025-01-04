# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeClearance(Document):
	def after_insert(self):
		if self.leave_application:
			frappe.db.set_value("Leave Application Form",self.leave_application,"employee_clearance",self.name,update_modified = False)

