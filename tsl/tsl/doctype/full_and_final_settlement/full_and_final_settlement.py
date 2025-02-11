# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
import calendar
class FullandFinalSettlement(Document):
	pass

@frappe.whitelist()
def get_reg_form(employee):
    if frappe.db.exists('Resignation Form', {'employee': employee}):
        name_reg = frappe.db.sql(   
            """select name,hods_relieving_date,actual_relieving_date from `tabResignation Form` where employee = %s """ % (employee), as_dict=True)[0]
        current_date = name_reg.actual_relieving_date
        first_day_of_month = current_date.replace(day=1)
        return name_reg.name, first_day_of_month, name_reg.actual_relieving_date
    else:
        termination_date = frappe.get_value('Employee', {'name': employee}, ['termination_date'])
        current_date = termination_date
        first_day_of_month = current_date.replace(day=1)
        return None,first_day_of_month, termination_date



@frappe.whitelist()
def get_current_month_date(employee):
    ff = frappe.get_value('Resignation Form', {'employee': employee}, ['actual_relieving_date']) or frappe.get_value('Employee', {'name': employee}, ['termination_date'])
    now = ff
    days = calendar.monthrange(now.year, now.month)[1]
    return days