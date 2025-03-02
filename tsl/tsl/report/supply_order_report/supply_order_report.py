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
		# _("Posting Date") + ":Date:150",
		_("Work Order") + ":Link/Work Order Data:140",
		_("Posting Date") + ":Date:150",
		# _("Old WOD") + ":Data:150",
		_("Sales Person") + ":Data:150",
		# _("Company") + ":Data:150",
		_("Branch") + ":Data:150",
		_("Type") + ":Data:150",
		_("Mfg") + ":Data:150",
		_("Model") + ":Data:150",
		_("Description") + ":Data:150",
		_("Serial No") + ":Data:150",
		_("Quantity") + ":Data:150",
		_("Customer") + ":Data:150",
		_("Customer_ref") + ":Data:150",
		# _("Contact Person") + ":Data:150",
		# _("Contact Email") + ":Data:150",
		# _("Contact Number") + ":Data:150",
		_("Technician") + ":Data:150",
		# _("Quoted Price") + ":Currency:150",
		# # _("Old Quoted Amount") + ":Data:150",
		# # _("Old VAT") + ":Data:100",
		# # _("Old Total Amount") + ":Data:100",
		_("Quoted Date") + ":Date:150",
		# # _("Po No") + ":Data:150",
		_("Payment Ref") + ":Link/Payment Entry:140",
		_("Payment Date") + ":Date:150",
		_("Delivery Note") +  ":Link/Delivery Note:140",
		_("Delivery Date") + ":Date:150",
		_("Invoice No") +  ":Link/Sales Invoice:140",
		_("Invoice Date") + ":Date:150",
		# _("Return Date") + ":Date:150",
		# _("Approval Date") + ":Date:150",
		_("Quoted Amount") + ":currency:120",
		_("Total Amount") + ":currency:120",
		# # _("VAT%") + ":float:120",
		# # _("VAT Amount%") + ":float:130",
		# # _("Total Amount") + ":float:130",
		# _("Quotation") + ":Link/Quotation:140",
		# _("NER") + ":Data:120",
		# _("NER Date") + ":Date:120",
		_("Status") + ":Data:170",
		
	]	
	return columns


def get_data(filters):
	data = []
	wr = []
	if filters.from_date:
		w = frappe.get_all("Supply Order Data",{"posting_date":["between",(filters.from_date,filters.to_date)]},["*"])
		wr = w
	if filters.to_date:
		w = frappe.get_all("Supply Order Data",{"posting_date":["between",(filters.from_date,filters.to_date)]},["*"])
		wr = w
	if filters.company:
		w = frappe.get_all("Supply Order Data",{"company":filters.company,"posting_date":["between",(filters.from_date,filters.to_date)]},["*"])
		wr = w
	if filters.from_date and filters.to_date:
		w = frappe.get_all("Supply Order Data",{"posting_date":["between",(filters.from_date,filters.to_date)]},["*"])
		wr = w
	if filters.from_date and filters.to_date and filters.company:
		w = frappe.get_all("Supply Order Data",{"company":filters.company,"posting_date":["between",(filters.from_date,filters.to_date)]},["*"])
		wr = w
	for i in wr:
		it = frappe.db.sql(''' select type,mfg,model_no,serial_no,quantity,description from `tabSupply Order Table` where parent = %s ''' ,i.name,as_dict=1)
		
		modd = ""
		typ = ""
		mf = ""
		s_n = ""
		des = ""
		qty = ""
		if it:
			mod = frappe.db.get_value("Item Model",it[0]["model_no"],"model")
			modd = mod
			typ = it[0]["type"]
			mf = it[0]["mfg"]
			des = it[0]["description"]
			qty = it[0]["quantity"]
			s_n = it[0]["serial_no"]
		q_amt = frappe.db.sql(''' select `tabQuotation`.taxes_and_charges as tax,`tabQuotation`.company as com,`tabQuotation Item`.amount as amt,`tabQuotation Item`.margin_amount as m_am,`tabQuotation`.purchase_order_no as po_no,`tabQuotation Item`.supply_order_data as sod,`tabQuotation Item`.qty as qty,`tabQuotation Item`.item_code as ic,`tabQuotation`.name as q_name,`tabQuotation`.default_discount_percentage as dis,`tabQuotation`.approval_date as a_date,`tabQuotation`.is_multiple_quotation as is_m,`tabQuotation`.after_discount_cost as adc,`tabQuotation`.Workflow_state,`tabQuotation Item`.unit_price as up,`tabQuotation Item`.margin_amount as ma from `tabQuotation` 
		left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
		where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer") and `tabQuotation Item`.supply_order_data = %s ''',i.name,as_dict=1)
		
		
		ap_date = ''
		qu_name = ''
		vat_amt = 0
		q_m = 0
		if q_amt:
			if q_amt[0]["com"] == "TSL COMPANY - KSA":
				q_m = q_amt[0]["amt"]
				if q_amt[0]["tax"]:
					vat_amt = (q_amt[0]["amt"] * 15)/100
					
				
		row = [i.name,
		i.posting_date,
		i.sales_rep,
		# i.company,
		i.branch,
		typ,
		mf,
		modd,
		des,
		s_n,
		qty,
		i.customer,
		i.customer_reference_number,
		i.technician,
		# i.quoted_price,
		i.quoted_date,
		# "",
		i.payment_entry_reference,
		i.payment_date,
		i.dn_no,
		i.dn_date,
		i.invoice_no,
		i.invoice_date,
		# "",
		# "",
		# "",
		round(q_m),
		# vat_amt,
		round(q_m)+vat_amt,
		# "",
		i.status
		]
		data.append(row)
		
	return data

