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
		tickets = (exp_years // 2) * 1
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
		tickets = (exp_years // 2) * 1
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
def create_leave_allocation(name):
	from datetime import datetime
	current_year = datetime.now().year
	last_date_of_year = datetime(current_year, 12, 31)
	doc = frappe.get_doc("Employee",name)
	leave_type = [{'type':"Sick Leave 25%",'days':frappe.db.get_value("Leave Allocation Table",{"company": doc.company},"sick_leave_25") or 0},
				{'type':"Sick Leave 50%",'days':frappe.db.get_value("Leave Allocation Table",{"company": doc.company},"sick_leave_50") or 0},
			   	{'type':"Sick Leave 75%",'days':frappe.db.get_value("Leave Allocation Table",{"company": doc.company},"sick_leave_75") or 0},
			   	{'type':"Sick Leave 100%",'days':frappe.db.get_value("Leave Allocation Table",{"company": doc.company},"sick_leave_100") or 0}]
	
	if doc.religion == "Islam":
		leave_type.append({'type':"Hajj Leave",'days':frappe.db.get_value("Leave Allocation Table",{"company": doc.company},"hajj_leave") or 0})
	if doc.gender == "Female":
		leave_type.append({'type':"Maternity Leave",'days':frappe.db.get_value("Leave Allocation Table",{"company": doc.company},"maternity_leave") or 0})
	for i in leave_type:
		alc = frappe.db.exists("Leave Allocation",{"employee":doc.employee,"leave_type":i['type'],"to_date":last_date_of_year})
		if not alc:
			if i['days'] >0:
				al = frappe.new_doc("Leave Allocation")
				al.employee = doc.employee
				al.leave_type = i['type']
				al.from_date = doc.date_of_joining
				al.to_date = last_date_of_year
				al.new_leaves_allocated = i['days']
				al.total_leaves_allocated = i['days']
				al.save(ignore_permissions =True)
				al.submit()
				frappe.msgprint("Leave Allocation <b>"+al.name+"</b> created for Employee - <b>"+doc.employee+"</b> for type - <b>"+i['type']+"</b>" )
		else:
			frappe.msgprint("Leave Allocation <b>"+alc+"</b> already there for Employee - <b>"+doc.employee+"</b> for type - <b>"+i['type']+"</b>")

@frappe.whitelist()
def civil_id_expiry():
	from frappe.utils import formatdate
	doc = frappe.db.get_list("Employee",{'status':"Active"},['civil_id_expiry_date','civil_id_no','name','employee_name','company','location'])
	forty_five = '<table border = 1px><tr>'
	forty_five += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Employee")
	forty_five += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Employee Name")
	forty_five += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Company")
	forty_five += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Location")
	forty_five += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Civil ID No.")
	forty_five += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Civil ID Expiry Date")
	forty_five += '<td style = "font-size:6px;font-weight:bold">%s</td></tr>'%("Days")
	send = 0
	for i in doc:
		if i.civil_id_expiry_date and i.civil_id_no:
			current_date = now_datetime()
			expiry_date = getdate(i.civil_id_expiry_date)
			days = date_diff(expiry_date,current_date)
			if days and days >=31 and days <= 45:
				forty_five += '<tr><td style = "font-size:6px"><a href = "https://erp.tsl-me.com/app/employee/%s">%s</a></td>'%(i.name,i.name)
				forty_five += '<td style = "font-size:6px">%s</td>'%(i.employee_name)
				forty_five += '<td style = "font-size:6px">%s</td>'%(i.company)
				forty_five += '<td style = "font-size:6px">%s</td>'%(i.location or '')
				forty_five += '<td style = "font-size:6px">%s</td>'%(i.civil_id_no)
				forty_five += '<td style = "font-size:6px">%s</td>'%(formatdate(i.civil_id_expiry_date, "dd-MM-yyyy"))
				forty_five += '<td style = "font-size:6px">%s</td></tr>'%(days)
				send+=1
	forty_five += "</table>"
	msg = '''Dear Mam/Sir,<br>Civil ID is expiring within 45 days for the below listed employees.<br>'''
	if send > 0:
		frappe.sendmail(
			recipients="j.sha.14601@gmail.com",
			# recipients="hr@tsl-me.com",
			subject=('Civil ID is Expiring within 45 days !!!'),
			message=msg+forty_five
		)
	thirty = '<table border = 1px><tr>'
	thirty += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Employee")
	thirty += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Employee Name")
	thirty += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Company")
	thirty += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Location")
	thirty += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Civil ID No.")
	thirty += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Civil ID Expiry Date")
	thirty += '<td style = "font-size:6px;font-weight:bold">%s</td></tr>'%("Days")
	send = 0
	for i in doc:
		if i.civil_id_expiry_date and i.civil_id_no:
			current_date = now_datetime()
			expiry_date = getdate(i.civil_id_expiry_date)
			days = date_diff(expiry_date,current_date)
			if days and days >=16 and days <= 30:
				thirty += '<tr><td style = "font-size:6px"><a href = "https://erp.tsl-me.com/app/employee/%s">%s</a></td>'%(i.name,i.name)
				thirty += '<td style = "font-size:6px">%s</td>'%(i.employee_name)
				thirty += '<td style = "font-size:6px">%s</td>'%(i.company)
				thirty += '<td style = "font-size:6px">%s</td>'%(i.location or '')
				thirty += '<td style = "font-size:6px">%s</td>'%(i.civil_id_no)
				thirty += '<td style = "font-size:6px">%s</td>'%(formatdate(i.civil_id_expiry_date, "dd-MM-yyyy"))
				thirty += '<td style = "font-size:6px">%s</td></tr>'%(days)
				send+=1
	thirty += "</table>"
	msg = '''Dear Mam/Sir,<br>Civil ID is expiring within 30 days for the below listed employees.<br>'''
	if send > 0:
		frappe.sendmail(
			recipients="j.sha.14601@gmail.com",
			# recipients="hr@tsl-me.com",
			subject=('Civil ID is Expiring within 30 days !!!'),
			message=msg+thirty
		)

	fifteen = '<table border = 1px><tr>'
	fifteen += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Employee")
	fifteen += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Employee Name")
	fifteen += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Company")
	fifteen += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Location")
	fifteen += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Civil ID No.")
	fifteen += '<td style = "font-size:6px;font-weight:bold">%s</td>'%("Civil ID Expiry Date")
	fifteen += '<td style = "font-size:6px;font-weight:bold">%s</td></tr>'%("Days")
	send = 0
	for i in doc:
		if i.civil_id_expiry_date and i.civil_id_no:
			current_date = now_datetime()
			expiry_date = getdate(i.civil_id_expiry_date)
			days = date_diff(expiry_date,current_date)
			if days and days >=1 and days <= 15:
				fifteen += '<tr><td style = "font-size:6px"><a href = "https://erp.tsl-me.com/app/employee/%s">%s</a></td>'%(i.name,i.name)
				fifteen += '<td style = "font-size:6px">%s</td>'%(i.employee_name)
				fifteen += '<td style = "font-size:6px">%s</td>'%(i.company)
				fifteen += '<td style = "font-size:6px">%s</td>'%(i.location or '')
				fifteen += '<td style = "font-size:6px">%s</td>'%(i.civil_id_no)
				fifteen += '<td style = "font-size:6px">%s</td>'%(formatdate(i.civil_id_expiry_date, "dd-MM-yyyy"))
				fifteen += '<td style = "font-size:6px">%s</td></tr>'%(days)
				send += 1
	fifteen += "</table>"
	msg = '''Dear Mam/Sir,<br>Civil ID is expiring within 15 days for the below listed employees.<br>'''
	if send > 0:
		frappe.sendmail(
			recipients="j.sha.14601@gmail.com",
			# recipients="hr@tsl-me.com",
			subject=('Civil ID is Expiring within 15 days !!!'),
			message=msg+fifteen
		)
		
@frappe.whitelist()
def employee_series(cyrix_employee):
	last_number = frappe.db.get_value("HR Settings","HR Settings",["last_number_in_series","custom_last_number"],as_dict = 1)
	if cyrix_employee == '0':
		next_in_series = int(last_number.last_number_in_series)+1
		next_in_series = check_for_employee(next_in_series)
		return str(next_in_series)
	if cyrix_employee == '1':
		next_in_series = int(last_number.custom_last_number)+1
		next_in_series = check_for_employee(next_in_series)
		return str(next_in_series)

def check_for_employee(name):
	# Loop until a unique employee number is found
	while frappe.db.exists("Employee", str(name)):
		name += 1
	return name

def update_last_employee_number(doc,method):
	if doc.cyrix_employee_ == 0:
		frappe.db.set_value("HR Settings","HR Settings","last_number_in_series",doc.name)

	if doc.cyrix_employee_ == 1:
		frappe.db.set_value("HR Settings","HR Settings","custom_last_number",doc.name)


def rename_user():
	frappe.rename_doc("User","maari@tsl-me.com", "marimithran2018@gmail.com")