# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff,today,cstr
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date,timedelta
from frappe.utils import date_diff, add_months,today,add_days,add_years,nowdate,flt


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = calculate_gratuity(filters)
	return columns, data

def get_columns(filters):
	return [
		{
			"fieldname": "employee_id",
			"label": _("Employee ID"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120
		},
		{
			"fieldname": "employee_name",
			"label": _("Employee Name"),
			"fieldtype": "Data",
			"width": 230
		},
		{
			"fieldname": "date_of_joining",
			"label": _("Date of Joining"),
			"fieldtype": "Date",
			"width": 130
		},
		{
			"fieldname": "years_of_service",
			"label": _("Years of Service"),
			"fieldtype": "Data",
			"width": 250
		},
		{
			"fieldname": "company",
			"label": _("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"width": 210,
		},
		{
			"fieldname": "currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"width": 120,
			"hidden":1
		},
		{
			"fieldname": "ctc",
			"label": _("CTC"),
			"fieldtype": "Currency",
			"options": 'currency',
			"width": 150
		},
		{
			"fieldname": "gratuity_amount",
			"label": _("Gratuity Amount"),
			"fieldtype": "Currency",
			"options": 'currency',
			"width": 150
		}
	]



def calculate_gratuity(filters):
	row = []
	data = []
	if filters.get("employee") and filters.get("company"):
		employees = frappe.get_all('Employee',{'status':'Active','employee':filters.employee,'company':filters.company},["*"])
	elif filters.get("employee") and not filters.get("company"):
		employees = frappe.get_all('Employee',{'status':'Active','employee':filters.employee},["*"])
	elif not filters.get("employee") and filters.get("company"):
		employees = frappe.get_all('Employee',{'status':'Active','company':filters.company},["*"])
	else:
		employees = frappe.get_all('Employee',{'status':'Active'},["*"])
		
	for emp in employees:
		from datetime import datetime
		from dateutil import relativedelta
		date_2 = datetime.now()
		diff = relativedelta.relativedelta(date_2, emp.date_of_joining)
		yos = cstr(diff.years) + ' years, ' + cstr(diff.months) +' months and ' + cstr(diff.days) + ' days'
		exp_years = diff.years
		exp_month = diff.months
		exp_days = diff.days
		total_days = (exp_years * 365) + (exp_month * 30) + exp_days
		currency = frappe.db.get_value("Company",emp.company,'default_currency')
		if emp.company == "TSL COMPANY - Kuwait":
			if(exp_years >= 3 and exp_years < 5):	
				per = (emp.ctc*7.5/30)
				for_years = per * exp_years
				for_days_months = ((exp_month/12)+ (exp_days/365)) * per
				gratuity = for_years + for_days_months
				row = [emp.name,emp.employee_name,emp.date_of_joining,yos,emp.company,currency,emp.ctc,for_years]
				data.append(row)
			
			elif(exp_years >= 5 and exp_years < 10):
				per = (emp.ctc * 20 / 30)
				first_five_years = ((emp.ctc*15)/30)*5
				additional_years = exp_years - 5
				gratuity_additional_years = per * additional_years
				for_days_months = ((exp_month/12)+ (exp_days/365)) * per
				gratuity = first_five_years +gratuity_additional_years+ for_days_months
				row = [emp.name,emp.employee_name,emp.date_of_joining,yos,emp.company,currency,emp.ctc,gratuity]
				data.append(row)

			elif(exp_years >= 10):
				years = emp.ctc * exp_years
				for_days_months = ((exp_month/12)+ (exp_days/365)) * emp.ctc
				gratuity = years + for_days_months
				row = [emp.name,emp.employee_name,emp.date_of_joining,yos,emp.company,currency,emp.ctc,gratuity]
				data.append(row)
			
			else:
				row = [emp.name,emp.employee_name,emp.date_of_joining,yos,emp.company,currency,emp.ctc,0]
				data.append(row)

		elif emp.company == "TSL COMPANY - UAE":
			per_day = emp.ctc / 30
			if exp_years > 0:
				if exp_years < 5:
					years = 21 * per_day * exp_years
					gratuity = (((exp_month/12)+ (exp_days/365)) * per_day * 21) + years
				else:
					gratuity = (21 * per_day * 5) + (30 * per_day * (exp_years - 5)) + ((exp_month/12)+ (exp_days/365)) * per_day * 30
				row = [emp.name,emp.employee_name,emp.date_of_joining,yos,emp.company,currency,emp.ctc,gratuity]
			else:
				row = [emp.name,emp.employee_name,emp.date_of_joining,yos,emp.company,currency,emp.ctc,0]
			data.append(row)


		else:
			row = [emp.name,emp.employee_name,emp.date_of_joining,yos,emp.company,currency,emp.ctc,0]
			data.append(row)

	return data