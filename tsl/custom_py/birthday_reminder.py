import frappe
import calendar
from frappe.utils import (
	add_days,
	add_months,
	cint,
	date_diff,
	flt,
	get_first_day,
	get_last_day,
	get_link_to_form,
	getdate,
	rounded,
	today,
)
from frappe.core.doctype.communication.email import make
from datetime import datetime

def send_birthday_reminder():
	today_date = today()
	today_month_day = getdate(today_date).strftime("%m-%d")
	is_leap_year = calendar.isleap(datetime.now().year)
	branch_and_mail_id = [
		{"name": "Jeddah - TSL-SA", "sender":"info-jed@tsl-me.com" ,"recipient": "admin@tsl-me.com" ,"cc":"admin-sa1@tsl-me.com"},
		{"name": "Dammam - TSL-SA", "sender":"info-dmm@tsl-me.com" ,"recipient": "admin@tsl-me.com" ,"cc":"admin-sa1@tsl-me.com"},
		{"name": "Dubai - TSL", "sender":"info@tsl-me.com" ,"recipient": "info-uae@tsl-me.com" ,"cc":None},
		{"name": "Riyadh - TSL- KSA", "sender":"info-sa@tsl-me.com" ,"recipient": "admin@tsl-me.com" ,"cc":"admin-sa1@tsl-me.com"},
		{"name": "Kuwait - TSL", "sender":"info@tsl-me.com" ,"recipient": "admin1@tsl-me.com" ,"cc":"info@tsl-me.com"}
	]
	
	for branch in branch_and_mail_id:
		today_birthdays = []
		upcoming_birthdays = []
		all_today_birthdays = []
		all_upcoming_birthdays = []
		employees = frappe.get_all("Employee", 
			filters={
				"status": "Active", 
				"branch": branch["name"],
				"user_id": ["not in", ["admin1@tsl-me.com", "info-uae@tsl-me.com"]]
			},
			fields=['name', 'date_of_birth', 'employee_name','user_id']
		)
		for employee_doc in employees:
			birthday = getdate(employee_doc.date_of_birth)
			birthday_month_day = birthday.strftime("%m-%d")
			if not is_leap_year and birthday_month_day == "02-29":
				birthday_month_day = "02-28"
			if today_month_day == birthday_month_day:
				today_birthdays.append((branch["name"], employee_doc.employee_name, employee_doc.date_of_birth))
			elif today_month_day == add_days(birthday, -2).strftime("%m-%d"):
				upcoming_birthdays.append((branch["name"], employee_doc.employee_name, employee_doc.date_of_birth))
		
		all_today_birthdays.extend(today_birthdays)
		all_upcoming_birthdays.extend(upcoming_birthdays)
		print(all_today_birthdays)
		print(all_upcoming_birthdays)
	
		if all_today_birthdays or all_upcoming_birthdays:
			subject = "Birthday Reminder for the Day"
			message = """
			<html>
			<body>
			<p>Dear Team,</p>
			"""
			
			if all_today_birthdays:
				message += "<h3>Today's Birthdays:</h3>"
				message += "<table border='1' cellpadding='5' cellspacing='0'><tr><th>Name</th><th>Branch</th><th>Date of Birth</th></tr>"
				for branch_name, name, dob in all_today_birthdays:
					message += f"<tr><td>{name}</td><td>{branch_name}</td><td>{dob.strftime('%d-%m-%Y')}</td></tr>"
				message += "</table><br>"
			
			if all_upcoming_birthdays:
				message += "<h3>Upcoming Birthdays (In 2 Days):</h3>"
				message += "<table border='1' cellpadding='5' cellspacing='0'><tr><th>Name</th><th>Branch</th><th>Date of Birth</th></tr>"
				for branch_name, name, dob in all_upcoming_birthdays:
					message += f"<tr><td>{name}</td><td>{branch_name}</td><td>{dob.strftime('%d-%m-%Y')}</td></tr>"
				message += "</table><br>"
			
			make(
				sender = branch['sender'],
				recipients=branch['recipient'],
				# recipients= "j.sha.14601@gmail.com",
				subject=subject,
				content=message,
				send_email=1,
				cc=branch["cc"]
				# cc= "shajith@tsl-me.com"
			)


def send_birthday_reminder_hr():
	today_date = today()
	today_month_day = getdate(today_date).strftime("%m-%d")
	is_leap_year = calendar.isleap(datetime.now().year)
	branch_and_mail_id = [
		{"name": "Dubai - TSL", "sender":"info-uae@tsl-me.com" ,"recipient": "ehab@tsl-me.com"},
		{"name": "Kuwait - TSL", "sender":"info@tsl-me.com" ,"recipient": "info@tsl-me.com"}
	]
	
	for branch in branch_and_mail_id:
		today_birthdays = []
		upcoming_birthdays = []
		all_today_birthdays = []
		all_upcoming_birthdays = []
		employees = frappe.get_all("Employee", 
			filters={
				"status": "Active", 
				"branch": branch["name"],
				"user_id": ["in", ["admin1@tsl-me.com", "info-uae@tsl-me.com"]]
			},
			fields=['name', 'date_of_birth', 'employee_name','user_id']
		)
		for employee_doc in employees:
			birthday = getdate(employee_doc.date_of_birth)
			birthday_month_day = birthday.strftime("%m-%d")
			if not is_leap_year and birthday_month_day == "02-29":
				birthday_month_day = "02-28"
			if today_month_day == birthday_month_day:
				today_birthdays.append((branch["name"], employee_doc.employee_name, employee_doc.date_of_birth))
			elif today_month_day == add_days(birthday, -2).strftime("%m-%d"):
				upcoming_birthdays.append((branch["name"], employee_doc.employee_name, employee_doc.date_of_birth))
			
		all_today_birthdays.extend(today_birthdays)
		all_upcoming_birthdays.extend(upcoming_birthdays)
	
		if all_today_birthdays or all_upcoming_birthdays:
			subject = "Birthday Reminder for the Day"
			message = """
			<html>
			<body>
			<p>Dear Team,</p>
			"""
			
			if all_today_birthdays:
				message += "<h3>Today's Birthdays:</h3>"
				message += "<table border='1' cellpadding='5' cellspacing='0'><tr><th>Name</th><th>Branch</th><th>Date of Birth</th></tr>"
				for branch_name, name, dob in all_today_birthdays:
					message += f"<tr><td>{name}</td><td>{branch_name}</td><td>{dob.strftime('%d-%m-%Y')}</td></tr>"
				message += "</table><br>"
			
			if all_upcoming_birthdays:
				message += "<h3>Upcoming Birthdays (In 2 Days):</h3>"
				message += "<table border='1' cellpadding='5' cellspacing='0'><tr><th>Name</th><th>Branch</th><th>Date of Birth</th></tr>"
				for branch_name, name, dob in all_upcoming_birthdays:
					message += f"<tr><td>{name}</td><td>{branch_name}</td><td>{dob.strftime('%d-%m-%Y')}</td></tr>"
				message += "</table><br>"

			make(
				sender = branch['sender'],
				recipients=branch['recipient'],
				subject=subject,
				content=message,
				send_email=1,
			)


def schedule_birthday_reminder():
	job = frappe.db.exists('Scheduled Job Type', 'birthday_reminder.send_birthday_reminder_hr')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'tsl.custom_py.birthday_reminder.send_birthday_reminder_hr',
			"frequency" : 'Daily',
		})
		sjt.save(ignore_permissions=True)
	job = frappe.db.exists('Scheduled Job Type', 'birthday_reminder.send_birthday_reminder')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'tsl.custom_py.birthday_reminder.send_birthday_reminder',
			"frequency" : 'Daily',
		})
		sjt.save(ignore_permissions=True)