# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta

def execute(filters=None):
	columns=get_columns(filters)
	data = get_data(filters) 
	return columns, data

def get_columns(filters):

	columns = [
		_("Service Call Form") + ":Link/Service Call Form:160",
		_("Quotation") + ":Link/Quotation:160",
		_("Date") + ":Date:120",
		_("Site Visit Date") + ":Date:110",
		_("Status") + ":Data:150",
		_("Customer") + ":Data:150",
		_("Sales Man") + ":Data:150",
		_("Technician") + ":Data:150",
		_("Branch") + ":Data:110",
		_("Amount") + ":Data:125",
		_("Currency") + ":Data:100",
	
	
	
		
	]	
	return columns

def get_data(filters):
	data = []
	sc = frappe.get_all("Service Call Form",{"company":filters.company},["*"])
	for i in sc:
		q = frappe.db.exists("Quotation",{"service_call_form":i.name,"workflow_state":"Approved By Customer"})
		if q:		
			qu = frappe.get_value("Quotation",{"name":q},["after_discount_cost"])
			qdate= frappe.get_value("Quotation",{"name":q},["transaction_date"])
			s = frappe.get_value("User",{"name":i.salesman_name},["username"])
			t = frappe.get_value("User",{"name":i.technician_name},["username"])
			row = [i.name,q,qdate,i.sch_date,i.status,i.customer,s,t,i.branch,qu,"KWD"]
			data.append(row) 
	
	return data

	





