# Copyright (c) 2025, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta
from erpnext.setup.utils import get_exchange_rate




def execute(filters=None):
	columns=get_columns(filters)
	data = get_data(filters) 
	return columns, data

def get_columns(filters):

	columns = [
		# _("Posting Date") + ":Date:150",
		_("Work Order") + ":Link/Work Order Data:140",
		_("Posting Date") + ":Date:150",
		_("Old WOD") + ":Data:150",
		_("Sales Person") + ":Data:150",
		_("Company") + ":Data:150",
		_("Branch") + ":Data:150",
		_("Type") + ":Data:150",
		_("Mfg") + ":Data:150",
		_("Model") + ":Data:150",
		_("Description") + ":Data:150",
		_("Serial No") + ":Data:150",
		_("Quantity") + ":Data:150",
		_("Customer") + ":Data:150",
		_("Customer_ref") + ":Data:150",
		_("Contact Person") + ":Data:150",
		_("Contact Email") + ":Data:150",
		_("Contact Number") + ":Data:150",
		_("Technician") + ":Data:150",
		_("Quoted Price") + ":Currency:150",
		# _("Old Quoted Amount") + ":Data:150",
		# _("Old VAT") + ":Data:100",
		# _("Old Total Amount") + ":Data:100",
		_("Quoted Date") + ":Date:150",
		# _("Po No") + ":Data:150",
		_("Payment Ref") + ":Link/Payment Entry:140",
		_("Payment Date") + ":Date:150",
		_("Delivery Note") +  ":Link/Delivery Note:140",
		_("Delivery Date") + ":Date:150",
		_("Invoice No") +  ":Link/Sales Invoice:140",
		_("Invoice Date") + ":Date:150",
		_("Return Date") + ":Date:150",
		_("Approval Date") + ":Date:150",
		_("RS Date") + ":Date:150",
		_("Quoted Amount") + ":currency:120",
		_("Cost") + ":currency:120",
		# _("Total Amount") + ":currency:120",
		# _("VAT%") + ":float:120",
		_("VAT Amount%") + ":float:130",
		_("Total Amount") + ":float:130",
		_("Quotation") + ":Link/Quotation:140",
		_("NER") + ":Data:120",
		_("NER Date") + ":Date:120",
		_("Status") + ":Data:170",
		
	]	
	return columns


def get_data(filters):
	data = []
	wr = []
	
	branch = frappe.get_value("Employee",{"user_id":frappe.session.user},["branch"])
	
	if filters.from_date:
		w = frappe.get_all("Work Order Data",{"branch":branch,"company":"TSL COMPANY - KSA","posting_date":["between",(filters.from_date,filters.to_date)]},["*"])
		wr = w
	if filters.to_date:
		w = frappe.get_all("Work Order Data",{"branch":branch,"company":"TSL COMPANY - KSA","posting_date":["between",(filters.from_date,filters.to_date)]},["*"])
		wr = w
	if filters.from_date and filters.to_date:
		w = frappe.get_all("Work Order Data",{"branch":branch,"company":"TSL COMPANY - KSA","posting_date":["between",(filters.from_date,filters.to_date)]},["*"])
		wr = w
	
	
	for i in wr:

		rs_date = ""
		rs = frappe.db.sql(""" select DATE(`tabStatus Duration Details`.date) AS date from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped"
		and `tabWork Order Data`.name = "%s" ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1 """ %(i.name) ,as_dict=1)
		
		if rs:
			frappe.errprint(rs[0]["date"])
			rs_date = rs[0]["date"]
		
		it = frappe.db.sql('''select type,mfg,model_no,serial_no,quantity,item_name from `tabMaterial List` where parent = %s ''',i.name,as_dict=1)
		mod = frappe.db.get_value("Item Model",it[0]["model_no"],"model")

		contact = frappe.db.sql('''select name1,email_id,phone_number from `tabContact Details` where parent = %s and parenttype="Customer" ''',i.customer,as_dict=1)
		
		cont = ''
		email = ''
		mobile = ''
		if contact:
			cont = contact[0]['name1'] 
			email = contact[0]['email_id']
			mobile = contact[0]['phone_number']

		s_total = 0
		inv_total = 0
		
		ev = frappe.db.sql(""" select  `tabPart Sheet Item`.total as t from `tabEvaluation Report` 
		left join `tabPart Sheet Item` on `tabEvaluation Report`.name = `tabPart Sheet Item`.parent
		where  `tabEvaluation Report`.work_order_data = '%s' """ %(i.name) ,as_dict=1)
		if ev:
			for e in ev:
				if e["t"]:
					inv_total = inv_total + e["t"]
		
			
		s_amt= frappe.db.sql(''' select base_total as b_am,shipping_cost as ship from `tabSupplier Quotation` 
		where Workflow_state in ("Approved By Management") and
		work_order_data = '%s' ''' %(i.name) ,as_dict=1)
		if s_amt:
			for s in s_amt:
				# s_total = s_total + s.base_total
				s_cur = frappe.get_value("Supplier",{"name":s.supplier},["default_currency"])
				exr = get_exchange_rate(s_cur,"KWD")
				if s.shipping_cost:
					s_total = s_total + (s.shipping_cost * exr)

		q_amt = frappe.db.sql(''' select `tabQuotation`.company as com,`tabQuotation`.taxes_and_charges as tax,
		`tabQuotation`.purchase_order_no as po_no,
		`tabQuotation`.name as q_name,`tabQuotation`.default_discount_percentage as dis,
		`tabQuotation`.approval_date as a_date,
		`tabQuotation`.transaction_date as qd,
		`tabQuotation`.is_multiple_quotation as is_m,
		`tabQuotation`.after_discount_cost as adc,`tabQuotation`.Workflow_state,
		`tabQuotation Item`.unit_price as up,`tabQuotation Item`.margin_amount as ma,
		`tabQuotation Item`.net_amount as amount
		 from `tabQuotation` 
		left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
		where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer") and `tabQuotation Item`.wod_no = %s ''',i.name,as_dict=1)
		
		q_m = 0
		ap_date = ''
		qu_name = ''
		quoted_date = ''
		po = ''
		vat = 0
		vat_amt = 0
		if q_amt:
			quoted_date = q_amt[0]["qd"]
			ap_date = q_amt[0]["a_date"]
			qu_name =  q_amt[0]["q_name"]
			po =  q_amt[0]["po_no"]
			q_m = q_amt[0]["amount"]
			if q_amt[0]["tax"]:
				vat_amt = (q_amt[0]["amount"] * 15) / 100
				

			
		row = [i.name,i.posting_date,i.old_wo_no,i.sales_rep,i.company,i.branch,
		it[0]["type"],it[0]["mfg"],mod,it[0]["item_name"],it[0]["serial_no"],it[0]["quantity"],
		i.customer,
		i.cus,
		cont,
		email,
		mobile,
		i.technician,
		i.quoted_price,
		# i.old_wo_q_amount,
		# i.old_wo_vat,
		# i.old_wo_total_amt,
		quoted_date,
		i.payment_reference_number,
		i.payment_date,
		i.dn_no,
		i.dn_date or i.delivery,
		i.invoice_no,
		i.invoice_date,
		i.returned_date,
		ap_date,
		rs_date,
		q_m,
		s_total + inv_total,
		vat_amt,
		round((q_m + vat_amt),2),
		qu_name,
		i.status_cap,
		i.status_cap_date,
		i.status
		]
		data.append(row)  
	return data

