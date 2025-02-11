# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
import datetime

class EmployeeAppraisal(Document):
	def on_submit(self):
		for app in self.appraisal:
			if app.get("employee"):
				emp = frappe.get_doc("Employee",app.get("employee"))
				emp.append("employee_appraisal_history",{
					"appraisal":self.name,
					"teamwork":app.get("teamwork"),
					"attendance":app.get("attendance"),
					"quality":app.get("quality"),
					"skils":app.get("skils"),
					"score":app.get("score")
				})
				emp.save()
	
	def on_cancel(self):
		employee_list = frappe.db.get_all("Employee Appraisal History",{'parenttype':"Employee",'appraisal':self.name},'name')
		if employee_list:
			for emp in employee_list:
				frappe.delete_doc_if_exists("Employee Appraisal History", emp.name)



	@frappe.whitelist()
	def fetch_employee_details(self):
		session_employee = frappe.db.get_value("Employee",{"user_id":frappe.session.user,"status":"Active"},'name')
		if session_employee:
			self.set("appraisal", [])
			self.set("appraisal_history", [])
			current_date = datetime.datetime.strptime(self.posting_date, '%Y-%m-%d')
			current_year = current_date.year
			current_month = current_date.month
			current_quarter = (current_month - 1) // 3 + 1
			quarter_months = {
				1: [1, 2, 3],   
				2: [4, 5, 6],   
				3: [7, 8, 9],
				4: [10, 11, 12]
			}
			emp_list = frappe.db.get_all("Employee", {'company': self.company,'reports_to':session_employee}, ['name','employee_name', 'department', 'date_of_joining'])
			eligible_employees = []
			for emp in emp_list:
				emp_doc = frappe.get_doc("Employee",emp.name)
				for app_ in emp_doc.employee_appraisal_history:
					self.append("appraisal_history",{					
						'employee_name': emp.employee_name,
						'document_no': app_.get("appraisal"),
						"teamwork":app_.get("teamwork"),
						"attendance":app_.get("attendance"),
						"quality":app_.get("quality"),
						"skils":app_.get("skils"),
						"score":app_.get("score")
					})
				joining_date = getdate(emp['date_of_joining'])
				if joining_date.year == current_year:
					if joining_date.month in quarter_months[current_quarter]:
						continue
				eligible_employees.append(emp)
			for emp_ in eligible_employees:
				self.append("appraisal", {
					'employee': emp_.name,
					'department': emp_.department,
					'teamwork': 0,
					'attendance': 0,
					'quality': 0,
					'skils': 0,
				})
			
			self.save()
		else:
			frappe.msgprint("Not an Employee")

	@frappe.whitelist()
	def set_series(self):
		current_date = datetime.datetime.strptime(self.posting_date, '%Y-%m-%d')
		current_year = current_date.year
		current_month = current_date.month
		current_quarter = (current_month - 1) // 3 + 1
		quarter_label = f"Q{current_quarter}"
		series = f"EMP-APP-{quarter_label}-{str(current_year)[-2:]}-.#####"
		return series