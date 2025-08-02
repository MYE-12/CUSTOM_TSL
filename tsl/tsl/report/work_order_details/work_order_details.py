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
		_("Work Order") + ":Link/Work Order Data:200",
		_("Evaluation Report") + ":Link/Evaluation Report:200",
		_("Total Cost") + ":Float:150",
		_("Cost After Quoted ") + ":Float:150",
		# _("Sales Person") + ":Data:200",
		# _("Project Type") + ":Data:200",
		# _("Company") + ":Data:1200",
		
	]	
	return columns

def get_data(filters):
	data = []
	wd = frappe.get_all("Work Order Data",{"docstatus":1,"posting_date": ["between", [filters.from_date,filters.to_date]]},["*"])
	for i in wd:
		er = frappe.get_value("Evaluation Report",{"work_order_data":i.name})
		q = frappe.db.sql(""" select `tabQuotation`.grand_total,`tabQuotation`.is_multiple_quotation from `tabQuotation` left join 
		`tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
		where `tabQuotation Item`.wod_no = %s and `tabQuotation`.workflow_state = 'Approved By Management' LIMIT 1 
		""",i.name,as_dict =1)
		# if q[0]["is_multiple_quotation"] == 1:
		# 	frappe.errprint("yes")
		# else:
			# frappe.errprint("No")
		ev = frappe.db.sql(""" select sum(`tabPart Sheet Item`.price_ea) as price from `tabEvaluation Report` left join 
		`tabPart Sheet Item` on `tabEvaluation Report`.name = `tabPart Sheet Item`.parent
		where `tabEvaluation Report`.name = %s and `tabPart Sheet Item`.part_sheet_no > 1 
		""",er,as_dict =1)
			# frappe.errprint(ev[0]["price"])
		if q:	
			row = [i.name,er,q[0]["grand_total"] or 0,ev[0]["price"] or 0]
			data.append(row)
	return data
	# p = frappe.get_all("Project",["*"])
	# conditions = build_conditions(filters)
	# frappe.errprint(conditions)
	# if filters.from_date and filters.to_date and filters.type:
	# 	sql_query = f""" SELECT * FROM  `tabProject` WHERE `tabProject`.check = 1 {conditions} """
	# 	p = frappe.db.sql(sql_query, as_dict=True)
	# 	for i in p:
	# 		row = [i.name,i.expected_start_date,i.expected_end_date,i.customer,i.sales_person,i.project_type,i.company]
	# 		data.append(row)
		
	# 	return data
	

def build_conditions(filters):
	conditions = ""
		
	if filters.get("from_date"):
		conditions += f" AND expected_end_date >= '{filters['from_date']}'"

	if filters.get("to_date"):
		conditions += f" AND expected_end_date <= '{filters['to_date']}'"

	
	return conditions




