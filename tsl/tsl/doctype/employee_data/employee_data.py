# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from tsl.custom_py.employee import employee_series

class EmployeeData(Document):
	def on_submit(self):
		exists = frappe.db.exists("Employee",{'first_name':self.first_name,'gender':self.gender,'company':self.company,'date_of_birth':self.date_of_birth,'date_of_joining':self.date_of_joining})
		if not exists:
			emp = frappe.new_doc("Employee")
			fields = [field.fieldname for field in frappe.get_meta(self.doctype).fields if field.fieldtype not in ['HTML','Button','Tab Break','Section Break','Column Break']]
			for field in fields:
				if field not in ["amended_from"]:
					setattr(emp, field, getattr(self, field))
			emp.employee_number = employee_series()
			frappe.msgprint("Please fill the Salary Details")
			emp.save(ignore_permissions=True)