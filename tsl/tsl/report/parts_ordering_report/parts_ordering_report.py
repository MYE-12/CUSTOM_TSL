# Copyright (c) 2025, Tsl and contributors
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
		_("Work Order") + ":Link/Work Order Data:150",
		_("Status") + ":Data:200",
		# _("Customer") + ":Data:200",
		_("Sales Person") + ":Data:150",
		_("Technician") + ":Data:150",
		_("Evaluation Report") + ":Link/Evaluation Report:150",
		_("Part") + ":Data:160",
		_("Model") + ":Data:120",
		_("Qty") + ":Data:100",
		_("Parts Availability") + ":Data:100",
		# _("Received Date") + ":Date:150",
		# _("Repaired Date") + ":Date:150",
		# _("Delivery Date") + ":Date:150",
		# _("Status") + ":Data:150",
		# _("Evaluation Report Status") + ":Data:200",
		# _("Model Name") + ":Data:150",
		# _("Technical Remarks") + ":Data:150",
		
	]	
	return columns


def get_data(filters):
	data = []

	if filters.branch:
		wo = frappe.db.sql(""" select DISTINCT `tabWork Order Data`.name as w,
		`tabWork Order Data`.status as st,`tabWork Order Data`.sales_rep as sl,
		`tabWork Order Data`.technician as tech
		from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "A-Approved"
		and `tabWork Order Data`.company = "%s" and `tabWork Order Data`.branch = "%s" """ %(filters.company,filters.branch) ,as_dict=1)
	if not filters.branch:
		wo = frappe.db.sql(""" select DISTINCT `tabWork Order Data`.name as w,
		`tabWork Order Data`.status as st,`tabWork Order Data`.sales_rep as sl,
		`tabWork Order Data`.technician as tech
		from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "A-Approved"
		and `tabWork Order Data`.company = "%s" """ %(filters.company) ,as_dict=1)


	for i in wo:
		eval = ""
		technician = frappe.get_value("Employee",{"user_id":i["tech"]},["employee_name"])
		ev = frappe.get_value("Evaluation Report",{"work_order_data":i["w"]},["name"])
		if ev:
			eval = ev
			part = frappe.db.sql(""" select `tabPart Sheet Item`.part as sku,
			`tabPart Sheet Item`.model as md,`tabPart Sheet Item`.qty as qty,
			`tabPart Sheet Item`.parts_availability as pa
			from `tabEvaluation Report` 
			left join `tabPart Sheet Item` on `tabEvaluation Report`.name = `tabPart Sheet Item`.parent
			where  `tabEvaluation Report`.work_order_data = "%s" """ %(i["w"]) ,as_dict=1)
			sku = ""
			model = ""
			qty = ""
			pa = ""
			if part:
				for k in part:
					if k["sku"]:
						sku = k["sku"]
					
					if k["md"]:
						model = k["md"]
						item_md = frappe.get_value("Item Model",{"name":k["md"]},["model"])
						if item_md:
							model = item_md
					if k["qty"]:
						qty = k["qty"]

					if k["pa"]:
						pa = k["pa"]
					
					
					data.append([i["w"],i["st"],i["sl"],technician,eval,sku,model,qty,pa])
						
			data.append(["","","","","","","","",""])

			
		
	return data