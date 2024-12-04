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
		_("Work Order") + ":Link/Work Order Data:140",
		_("Evaluation Report") + ":Link/Evaluation Report:140",
		_("Quotation") + ":Link/Quotation:140",
		_("Currency") + ":Data:50",
		_("Quoted Amount") + ":Data:150",
		_("Amount of Parts") + ":Data:150",
		_("Labour Cost") + ":Data:150",
		_("Difference") + ":Data:150",
		_("Profit %") + ":Data:80",
	
		
	]	
	return columns

def get_data(filters):
	data = []
	wd = frappe.db.sql(""" select `tabQuotation Item`.wod_no ,
	`tabQuotation`.name as q,
	`tabQuotation`.is_multiple_quotation as imq,
	`tabQuotation`.after_discount_cost as adc,
	`tabQuotation`.currency as c,
	`tabQuotation Item`.margin_amount  as ma
	from `tabQuotation` 
	left join `tabQuotation Item` on `tabQuotation Item`.parent = `tabQuotation`.name 
	where `tabQuotation`.workflow_state = "Approved By Customer" and `tabQuotation`.company = "TSL COMPANY - Kuwait" """ ,as_dict=True)
	for i in wd:
		ev = frappe.db.exists("Evaluation Report",{"work_order_data":i.wod_no})
		if ev:
			q_amt = 0
			if i.imq == 1:
				q_amt = i.ma
			if i.imq == 0:
				q_amt = i.adc
				
			tec_amt = frappe.db.sql(""" select DISTINCT `tabTechnician Hours Spent`.work_order_data ,`tabTechnician Hours Spent`.total_price from `tabQuotation` 
			left join `tabTechnician Hours Spent` on `tabTechnician Hours Spent`.parent = `tabQuotation`.name
			where `tabQuotation`.workflow_state = "Approved By Management" and `tabTechnician Hours Spent`.work_order_data = '%s' """ %(i.wod_no) ,as_dict=True)
			# frappe.errprint(tec_amt)
			t_amt = 0
			if tec_amt:
				t_amt = tec_amt[0]["total_price"]
				
			# else:
			# 	tec_amt[0]["total_price"] = 0
			# 	frappe.errprint(tec_amt[0]["total_price"])

			e = frappe.db.sql(""" select sum(`tabPart Sheet Item`.total) as amt from `tabEvaluation Report` 
			left join `tabPart Sheet Item` on `tabPart Sheet Item`.parent = `tabEvaluation Report`.name
			where `tabEvaluation Report`.name = '%s'  """ %(ev) ,as_dict=True)
			if not e[0]["amt"]:
				e[0]["amt"] = 0
			t_exp = e[0]["amt"] + t_amt
	
			if t_exp >= 1 and q_amt > 0:
				exp = e[0]["amt"] + t_amt
				pp = ((q_amt - exp)/q_amt)
				pp = round(pp,2)
			else:
				pp = "-"

			if q_amt >= 1 and e[0]["amt"] >=1 and t_amt >= 1:
				row = [i.wod_no,ev,i.q,i.c,q_amt,round(e[0]["amt"]),t_amt,round(q_amt - (e[0]["amt"]+t_amt)),pp]
				data.append(row) 
	# w = frappe.get_all("Work Order Data",["*"])
	# for i in w:
	# 	if i.status_cap:
	# 		if i.status == "WP-Waiting Parts" or i.status == "C-Comparison" or i.status == "TR-Technician Repair" or i.status == "UTR-Under Technician Repair" or i.status == "AP-Available Parts" or i.status == "NER-Need Evaluation Return":
	
	
	return data
