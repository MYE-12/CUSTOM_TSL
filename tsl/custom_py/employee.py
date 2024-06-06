import frappe
from frappe.utils import date_diff, getdate, now_datetime

@frappe.whitelist()
def update_ticket_count():
	list = frappe.db.get_list("Employee")
	for i in list:
		doc = frappe.get_doc("Employee",i.name)
		current_date = now_datetime()
		join_date = getdate(doc.date_of_joining)
		days = date_diff(current_date, join_date)
		exp_years = current_date.year - join_date.year
		if (current_date.month, current_date.day) < (join_date.month, join_date.day):
			exp_years -= 1
		tickets = (exp_years // 2) * 2
		total_tickets = tickets
		frappe.db.set_value("Employee",i.name,'total_tickets',total_tickets,update_modified=False)
		leaves = frappe.db.sql(""" select sum(ticket_used) as tickets_used from `tabLeave Application` where employee = '%s' and docstatus = 1 """%(i.name),as_dict=True)[0]
		if leaves['tickets_used']:
			used_tickets = leaves['tickets_used']
		else:
			used_tickets = 0
		frappe.db.set_value("Employee",i.name,'used_tickets',used_tickets,update_modified=False)
		tickets_available = total_tickets - used_tickets
		frappe.db.set_value("Employee",i.name,'no_of_tickets',tickets_available,update_modified=False)

@frappe.whitelist()
def update_used_tickets_in_employee(doc,method):
	list = frappe.db.get_list("Employee")
	for i in list:
		doc = frappe.get_doc("Employee",i.name)
		current_date = now_datetime()
		join_date = getdate(doc.date_of_joining)
		days = date_diff(current_date, join_date)
		exp_years = current_date.year - join_date.year
		if (current_date.month, current_date.day) < (join_date.month, join_date.day):
			exp_years -= 1
		tickets = (exp_years // 2) * 2
		total_tickets = tickets
		frappe.db.set_value("Employee",i.name,'total_tickets',total_tickets,update_modified=False)
		leaves = frappe.db.sql(""" select sum(ticket_used) as tickets_used from `tabLeave Application` where employee = '%s' and docstatus = 1 """%(i.name),as_dict=True)[0]
		if leaves['tickets_used']:
			used_tickets = leaves['tickets_used']
		else:
			used_tickets = 0
		frappe.db.set_value("Employee",i.name,'used_tickets',used_tickets,update_modified=False)
		tickets_available = total_tickets - used_tickets
		frappe.db.set_value("Employee",i.name,'no_of_tickets',tickets_available,update_modified=False)