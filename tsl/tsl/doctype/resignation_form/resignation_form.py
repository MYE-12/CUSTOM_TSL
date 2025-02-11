# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class ResignationForm(Document):
	def on_submit(self):
		frappe.db.set_value("Employee",self.employee,'relieving_date',self.actual_relieving_date)

	def on_cancel(self):
		frappe.db.set_value("Employee",self.employee,'relieving_date','')

def update_employee_status():
	today_date = frappe.flags.current_date or getdate()

	emp_list = frappe.db.get_all("Employee", {'status': "Active"}, ["name", "relieving_date", "termination_date"])

	for emp in emp_list:
		relieving_date, termination_date = emp['relieving_date'], emp['termination_date']
		
		if termination_date and termination_date <= today_date:
			frappe.db.set_value("Employee", emp['name'], 'status', "Suspended")

		elif relieving_date and relieving_date <= today_date:
			frappe.db.set_value("Employee", emp['name'], 'status', "Left")


@frappe.whitelist()
def schedule_update_employee_status():
	job = frappe.db.exists('Scheduled Job Type', 'resignation_form.update_employee_status')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'tsl.tsl.doctype.resignation_form.resignation_form.update_employee_status',
			"frequency" : 'Daily',
		})
		sjt.save(ignore_permissions=True)