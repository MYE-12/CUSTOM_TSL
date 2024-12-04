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
def update_leave_allocation():
    employees = frappe.get_all("Employee",{"status":"Active"},["*"])
    current_date = datetime.now().date()
    first = get_first_day(current_date)
    last = get_last_day(current_date)
    total_days = date_diff(last,first) + 1
    per_day = 2.5/total_days
    current_year = getdate().year
    first_date_of_year = f"{current_year}-01-01"
    for emp in employees:
        if frappe.db.exists("Leave Allocation",{'employee':emp.employee,'leave_type':"Annual Leave"}):
            la = frappe.get_doc("Leave Allocation",{'employee':emp.employee,'leave_type':"Annual Leave"},["*"])
            la.new_leaves_allocated = la.new_leaves_allocated + per_day
            la.save(ignore_permissions=True)
            la.submit()   
        else:
            la = frappe.new_doc("Leave Allocation")
            la.employee = emp.name
            la.leave_type = "Annual Leave"
            la.new_leaves_allocated = per_day
            la.from_date = first_date_of_year
            la.to_date = "2100-12-31"
            la.save(ignore_permissions=True)
            la.submit()

def cron_job_allocation():
	job = frappe.db.exists('Scheduled Job Type', 'tsl.custom_py.leave_allocation.update_leave_allocation')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'tsl.custom_py.leave_allocation.update_leave_allocation',
			"frequency" : 'Daily'
		})
		sjt.save(ignore_permissions=True)


from datetime import datetime, timedelta
@frappe.whitelist()
def calculate_projected_leaves(current_date, leave_start_date):
    current_date = datetime.strptime(current_date,"%Y-%m-%d")
    leave_start_date = datetime.strptime(leave_start_date,"%Y-%m-%d")
    if leave_start_date <= current_date:
        return 0.0  # No projection needed for past or today
    monthly_leave_allocation = 2.5
    projected_leaves = 0.0
    days_until_leave = (leave_start_date - current_date).days
    
    for day in range(days_until_leave):
        projection_date = current_date + timedelta(days=day)
        
        if projection_date.month == 2:
            days_in_month = 29 if (projection_date.year % 4 == 0 and (projection_date.year % 100 != 0 or projection_date.year % 400 == 0)) else 28
        else:
            from calendar import monthrange
            days_in_month = monthrange(projection_date.year, projection_date.month)[1]

        if days_in_month > 0:
            projected_leaves += (monthly_leave_allocation / days_in_month)
        else:
            projected_leaves += 0  # Just in case, although days_in_month should never be 0

    return round(projected_leaves,3)