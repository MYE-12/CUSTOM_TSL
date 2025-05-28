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
		_("Work Order") + ":Link/Work Order Data:150",
		_("Purchase Order") + ":Link/Purchase Order:150",
		_("Purchase Invoice") + ":Link/Purchase Invoice:150",
		_("Tracking ID") + ":Data:150",
		_("Customer") + ":Data:200",
		_("Sales Person") + ":Data:150",
		_("Received Date") + ":Date:150",
		_("Repaired Date") + ":Date:150",
		_("Delivery Date") + ":Date:150",
		_("Status") + ":Data:150",
		_("Evaluation Report Status") + ":Data:200",
		_("Model Name") + ":Data:150",
		_("Technical Remarks") + ":Data:150",
		
	]	
	return columns


def get_data(filters):
	data = []
	if filters.work_order_data:
		evr = frappe.get_all("Evaluation Report",{"work_order_data":filters.work_order_data ,"docstatus":1,"date": ["between", [filters.from_date,filters.to_date]]},["*"])
	
	elif filters.branch:
		evr = frappe.get_all("Evaluation Report",{"branch":filters.branch ,"docstatus":1,"date": ["between", [filters.from_date,filters.to_date]]},["*"])
	
	else:
		evr = frappe.get_all("Evaluation Report",{"docstatus":1,"date": ["between", [filters.from_date,filters.to_date]]},["*"])

	for i in evr:
		rec_date = frappe.get_value("Work Order Data",{"name":i.work_order_data},["posting_date"])
		wods= frappe.get_value("Work Order Data",{"name":i.work_order_data},["name"])
		cus = frappe.get_value("Work Order Data",{"name":i.work_order_data},["customer"])
		dn_date = frappe.get_value("Work Order Data",{"name":i.work_order_data},["dn_date"])
		w_status= frappe.get_value("Work Order Data",{"name":i.work_order_data},["status"])
		sales= frappe.get_value("Work Order Data",{"name":i.work_order_data},["sales_rep"])


		psi = frappe.db.sql(""" select `tabEvaluation Report`.comment as com,`tabEvaluation Report`.test_result as ts,`tabPart Sheet Item`.model  from `tabEvaluation Report` 
		left join `tabPart Sheet Item` on `tabEvaluation Report`.name = `tabPart Sheet Item`.parent
		where `tabEvaluation Report`.name = %s 
		""",i.name,as_dict=1)
		
		if psi:
			for j in psi:
				im = frappe.get_value("Item Model",{"name":j["model"]},["model"])

				po = ""
				p_order = frappe.db.sql(""" select `tabPurchase Order`.name as po from `tabPurchase Order` 
				left join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent 
				where `tabPurchase Order Item`.work_order_data = '%s' """ %(wods),as_dict =1)
				if p_order:
					po = p_order[0]["po"]
			
				pi = ""
				tr_id = ""
						
				p_inv = frappe.db.sql(""" select `tabPurchase Invoice`.tracking_id as td,`tabPurchase Invoice`.name as pi from `tabPurchase Invoice` 
				left join `tabPurchase Invoice Item` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent 
				where `tabPurchase Invoice Item`.work_order_data = '%s' """ %(wods),as_dict =1)
				if p_inv:
					pi = p_inv[0]["pi"]
					tr_id = p_inv[0]["td"]

								
				row = [wods,po,pi,tr_id,cus,sales,rec_date,i.date,dn_date or "-",w_status,i.status,im,j["com"] or j["ts"]]
				data.append(row)
			data.append(["","","","","","","","","","","","",""])		
	return data

	





