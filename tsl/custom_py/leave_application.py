import frappe
from frappe.model.mapper import get_mapped_doc
import datetime
from frappe.utils import (
	add_days,
	today,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_fullname,
	get_link_to_form,
	getdate,now_datetime,
	nowdate,
	get_first_day,
	get_last_day
)
from datetime import datetime


@frappe.whitelist()
def create_leave_rejoining():
	leave_applications = frappe.db.get_all("Leave Application Form",{"docstatus":1}, ['*'])
	today_date = datetime.today().date() 

	for leave in leave_applications:
		leave_end_date = leave.leave_end_date
		lop_end_date = leave.lop_end_date

		# Check if leave has ended today
		if (leave_end_date and not lop_end_date and leave_end_date == today_date) or (lop_end_date and lop_end_date == today_date):
			# Check if rejoining form already exists
			if not frappe.db.exists("Leave Rejoining Form", {'leave_application': leave.name, "emp_no": leave.employee}):
				try:
					rejoin = frappe.new_doc("Leave Rejoining Form")
					rejoin.emp_no = leave.employee
					rejoin.leave_application = leave.name
					rejoin.from_date = leave.from_date
					rejoin.to_date = leave.to_date
					rejoin.rejoining_date = add_days(today_date, 1) 
					rejoin.save()
				except Exception as e:
					print(f"Error creating rejoining form for {leave.employee}: {e}")
	

@frappe.whitelist()
def schedule_create_leave_rejoining():
	job = frappe.db.exists('Scheduled Job Type', 'leave_application.create_leave_rejoining')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'tsl.custom_py.leave_application.create_leave_rejoining',
			"frequency" : 'Daily'
		})
		sjt.save(ignore_permissions=True)
