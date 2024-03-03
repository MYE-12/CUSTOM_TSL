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
		_("Total Cost(Before Quote)") + ":Float:150",
		_("Cost After Quoted ") + ":Float:150",
		# _("Sales Person") + ":Data:200",
		# _("Project Type") + ":Data:200",
		# _("Company") + ":Data:1200",
		
	]	
	return columns

def get_data(filters):
	data = []
	if filters.work_order_data:
		wd = frappe.get_all("Work Order Data",{"name":filters.work_order_data ,"docstatus":1,"posting_date": ["between", [filters.from_date,filters.to_date]]},["*"])
	else:
		wd = frappe.get_all("Work Order Data",{"docstatus":1,"posting_date": ["between", [filters.from_date,filters.to_date]]},["*"])
	for i in wd:
		er = frappe.get_value("Evaluation Report",{"work_order_data":i.name})
		q = frappe.db.sql(""" select `tabQuotation`.grand_total,`tabQuotation`.is_multiple_quotation from `tabQuotation` left join 
		`tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
		where `tabQuotation Item`.wod_no = %s and `tabQuotation`.workflow_state = 'Approved By Management' LIMIT 1 
		""",i.name,as_dict =1)
		
		ev = frappe.db.sql(""" select sum(`tabPart Sheet Item`.total) as price from `tabEvaluation Report` left join 
		`tabPart Sheet Item` on `tabEvaluation Report`.name = `tabPart Sheet Item`.parent
		where `tabEvaluation Report`.name = %s and `tabPart Sheet Item`.part_sheet_no > 1 
		""",er,as_dict =1)
	
		qu = 0
		if q:	
			if q[0]["is_multiple_quotation"] == 1:
				evm = frappe.db.sql(""" select sum(`tabPart Sheet Item`.total) as price ,`tabEvaluation Report`.evaluation_time,`tabEvaluation Report`.estimated_repair_time from `tabEvaluation Report` left join 
				`tabPart Sheet Item` on `tabEvaluation Report`.name = `tabPart Sheet Item`.parent and `tabPart Sheet Item`.part_sheet_no < 2
				where `tabEvaluation Report`.name = %s 
				""",er,as_dict =1)
			
				if not evm[0]["price"]:
					evm[0]["price"] = 0
				if evm[0]["evaluation_time"]:
					et = evm[0]["evaluation_time"]/3600
					r_et = round(et,1)
				if evm[0]["estimated_repair_time"]:
					ert = evm[0]["estimated_repair_time"]/3600
					r_etr = round(ert,1)
				total_time = r_et + r_etr
				cost_of_time = total_time * 20
				total_cost = cost_of_time + evm[0]["price"]
				qu = total_cost
			else:
				qu = q[0]["grand_total"]
			row = [i.name,er,qu or 0,ev[0]["price"] or 0]
			data.append(row)
	return data

	





