# Copyright (c) 2013, Tsl and contributors
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
		_("Posting Date") + ":Date:150",
		_("Work Order") + ":Link/Work Order Data:140",
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
		_("Old Quoted Amount") + ":Data:150",
		_("Quoted Date") + ":Date:150",
		_("Po No") + ":Data:150",
		_("Payment Ref") + ":Link/Payment Entry:140",
		_("Payment Date") + ":Date:150",
		_("Delivery Note") +  ":Link/Delivery Note:140",
		_("Delivery Date") + ":Date:150",
		_("Invoice No") +  ":Link/Sales Invoice:140",
		_("Invoice Date") + ":Date:150",
		_("Return Date") + ":Date:150",
		_("Approval Date") + ":Date:150",
		_("Quoted Amount") + ":currency:120",
		_("Quotation") + ":Link/Quotation:140",
		_("NER") + ":Data:120",
		_("NER Date") + ":Date:120",
		_("Status") + ":Data:170",
		
	]	
	return columns

def get_data(filters):
	data = []
	if filters.from_date:
		w = frappe.get_all("Work Order Data",{"posting_date":["between",(filters.from_date,filters.to_date)]},["*"])

	if filters.to_date:
		w = frappe.get_all("Work Order Data",{"posting_date":["between",(filters.from_date,filters.to_date)]},["*"])

	if filters.company:
		w = frappe.get_all("Work Order Data",{"company":filters.company,"posting_date":["between",(filters.from_date,filters.to_date)]},["*"])
	
	if filters.from_date and filters.to_date:
		w = frappe.get_all("Work Order Data",{"posting_date":["between",(filters.from_date,filters.to_date)]},["*"])

	for i in w:
		# pay_ref= frappe.get_value("Work Order Data",{"name":i.name},["payment_entry_reference"])
		# pdate = frappe.get_value("Work Order Data",{"name":i.name},["payment_date"])
		# dn_no = frappe.get_value("Work Order Data",{"name":i.name},["dn_no"])
		# dn_date = frappe.get_value("Work Order Data",{"name":i.name},["dn_date"])
		# iv_no = frappe.get_value("Work Order Data",{"name":i.name},["invoice_no"])
		# iv_date = frappe.get_value("Work Order Data",{"name":i.name},["invoice_date"])
		# r_date = frappe.get_value("Work Order Data",{"name":i.name},["returned_date"])

		it = frappe.db.sql('''select type,mfg,model_no,serial_no,quantity,item_name from `tabMaterial List` where parent = %s ''',i.name,as_dict=1)
		
		mod = frappe.db.get_value("Item Model",it[0]["model_no"],"model")

		q_amt = frappe.db.sql(''' select `tabQuotation`.purchase_order_no as po_no,`tabQuotation`.name as q_name,`tabQuotation`.default_discount_percentage as dis,`tabQuotation`.approval_date as a_date,`tabQuotation`.is_multiple_quotation as is_m,`tabQuotation`.after_discount_cost as adc,`tabQuotation`.Workflow_state,`tabQuotation Item`.unit_price as up,`tabQuotation Item`.margin_amount as ma from `tabQuotation` 
		left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
		where  `tabQuotation`.Workflow_state in ("Approved By Customer") and `tabQuotation Item`.wod_no = %s ''',i.name,as_dict=1)
		# frappe.errprint(q_amt)
		q_m = 0
		ap_date = ''
		qu_name = ''
		po = ''
		if q_amt:
			ap_date = q_amt[0]["a_date"]
			qu_name =  q_amt[0]["q_name"]
			po =  q_amt[0]["po_no"]
			if q_amt[0]["is_m"] == 1:
				per = (q_amt[0]["up"] * q_amt[0]["dis"])/100
				q_m = q_amt[0]["up"] - per

			if q_amt[0]["is_m"] == 0:
				q_m = q_amt[0]["adc"]

		else:
			q_amt_2 = frappe.db.sql(''' select `tabQuotation`.purchase_order_no as po_no,`tabQuotation`.name as q_name,`tabQuotation`.default_discount_percentage as dis,`tabQuotation`.approval_date as a_date,`tabQuotation`.is_multiple_quotation as is_m,`tabQuotation`.after_discount_cost as adc,`tabQuotation`.Workflow_state,`tabQuotation Item`.unit_price as up,`tabQuotation Item`.margin_amount as ma from `tabQuotation` 
			left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
			where  `tabQuotation`.Workflow_state in ("Quoted to Customer") and `tabQuotation Item`.wod_no = %s ''',i.name,as_dict=1)

			if q_amt_2:
				ap_date = q_amt_2[0]["a_date"]
				qu_name =  q_amt_2[0]["q_name"]
				po =  q_amt_2[0]["po_no"]
				if q_amt_2[0]["is_m"] == 1:
					per = (q_amt_2[0]["up"] * q_amt_2[0]["dis"])/100
					q_m = q_amt_2[0]["up"] - per

				if q_amt_2[0]["is_m"] == 0:
					q_m = q_amt_2[0]["adc"]



		contact = frappe.db.sql('''select name1,email_id,phone_number from `tabContact Details` where parent = %s and parenttype="Customer" ''',i.customer,as_dict=1)
		frappe.errprint(contact)
		cont = ''
		email = ''
		mobile = ''
		if contact:
			cont = contact[0]['name1'] 
			email = contact[0]['email_id']
			mobile = contact[0]['phone_number']

		row = [i.posting_date,
		i.name,
		i.old_wo_no,
		i.sales_rep,
		i.company,
		i.branch,
		it[0]["type"],
		it[0]["mfg"],
		mod,
		it[0]["item_name"],
		it[0]["serial_no"],
		it[0]["quantity"],
		i.customer,
		i.customer_reference_number,
		cont,
		email,
		mobile,
		i.technician,
		i.quoted_price,
		i.old_wo_q_amount,
		i.quoted_date,
		po,
		i.payment_reference_number,
		i.payment_date,
		i.dn_no,
		i.dn_date,
		i.invoice_no,
		i.invoice_date,
		i.returned_date,
		ap_date,
		q_m,
		qu_name,
		i.status_cap,
		i.status_cap_date,
		i.status]
		data.append(row) 
	return data

	
# from pkgutil import get_data
# import frappe
# from datetime import datetime,date

# def execute(filters=None):
# 	data = []
# 	if filters.from_date and filters.to_date:
# 		data = get_data(filters)
# 	columns = get_columns(filters)
# 	return columns, data


# def get_columns(filters):
# 	columns = [
# 	{
# 		"fieldname":"posting_date",
# 		"label": "Date",
# 		"fieldtype": "Date",
# 		"width":100
# 	},
# 	{
# 		"fieldname":"wod_no",
# 		"label": "WOD",
# 		"fieldtype": "Link",
# 		"options" : "Work Order Data"
# 	},

# 	{
# 		"fieldname":"old_wo_no",
# 		"label": "Old Wo No",
# 		"fieldtype": "Data",
		
# 	},

# 	{
# 		"fieldname":"sales_rep",
# 		"label": "Sales Name",
# 		"fieldtype": "Link",
# 		"options" : "User"
# 	},
	
# 	{
# 		"fieldname":"company",
# 		"label": "Company Name",
# 		"fieldtype": "Link",
# 		"options" : "Company"
# 	},
# 	# {
# 	# 	"fieldname":"city",
# 	# 	"label": "City",
# 	# 	"fieldtype": "Data",
# 	# },

# 	# {
# 	# 	"fieldname":"branch_name",
# 	# 	"label": "Branch/Plant Name",
# 	# 	"fieldtype": "Data",
# 	# },

# 	{
# 		"fieldname":"type",
# 		"label": "Description",
# 		"fieldtype": "Data",
# 	},
# 	{
# 		"fieldname":"mfg",
# 		"label": "Mfg",
# 		"fieldtype": "Data",
# 		"width":100
# 	},
# 	{
# 		"fieldname":"model_no",
# 		"label": "Model",
# 		"fieldtype": "Data",
# 		"width":150

# 	},
# 	{
# 		"fieldname":"serial_no",
# 		"label": "Serial No",
# 		"fieldtype": "Data",
# 		"width":150

# 	},
# 	# {
# 	# 	"fieldname":"quantity",
# 	# 	"label": "Qty",
# 	# 	"fieldtype": "Float",
# 	# 	"width":100
# 	# },

# 	{
# 		"fieldname":"technician",
# 		"label": "Technician",
# 		"fieldtype": "Link",
# 		"options" : "User",
# 		"width":150
# 	},

# 	{
# 		"fieldname":"customer",
# 		"label": "Customer",
# 		"fieldtype": "Link",
# 		"options" : "Customer",
# 		"width":200
# 	},

# 	{
# 		"fieldname":"customer_ref",
# 		"label": "Customer Ref",
# 		"fieldtype": "Data",
# 		"width":150
# 	},
	
# 	{
# 		"fieldname":"quoted_price",
# 		"label": "Quoted Price",
# 		"fieldtype": "Currency",
# 	},


# 	{
# 		"fieldname":"old_wo_q_amount",
# 		"label": "Old Quoted Amount",
# 		"fieldtype": "Currency",
		
# 	},

# 	{
# 		"fieldname":"quoted_date",
# 		"label": "Old Quoted Date",
# 		"fieldtype": "Date",
		
# 	},
# 	# {
# 	# 	"fieldname":"price_after_dis",
# 	# 	"label": "Price After Discount",
# 	# 	"fieldtype": "Currency",
# 	# },
# 	# {
# 	# 	"fieldname":"tax",
# 	# 	"label": "Tax(VAT)",
# 	# 	"fieldtype": "Currency",
# 	# },
# 	# {
# 	# 	"fieldname":"gross",
# 	# 	"label": "Gross",
# 	# 	"fieldtype": "Currency",
# 	# },
# 	# {
# 	# 	"fieldname":"pc1",
# 	# 	"label": "1-Payments/Credits",
# 	# 	"fieldtype": "Currency",
# 	# },
# 	# {
# 	# 	"fieldname":"pc2",
# 	# 	"label": "2-Payments/Credits",
# 	# 	"fieldtype": "Currency",
# 	# },
# 	# {
# 	# 	"fieldname":"due_balance",
# 	# 	"label": "Due Balance",
# 	# 	"fieldtype": "Currency",
# 	# },
# 	# {
# 	# 	"fieldname":"comisssion",
# 	# 	"label": "Comission(4%)",
# 	# 	"fieldtype": "Currency",
# 	# },
	
# 	{
# 		"fieldname":"status",
# 		"label": "Status",
# 		"fieldtype": "Data",
# 		"width":220
# 	},
# 	{
# 		"fieldname":"quoted_date",
# 		"label": "Quoted Date",
# 		"fieldtype": "Date",
# 	},
# 	{
# 		"fieldname":"approved_date",
# 		"label": "Approved Date",
# 		"fieldtype": "Date",
# 	},
# 	# {
# 	# 	"fieldname":"return_date",
# 	# 	"label": "Unit Returned Date to Customer",
# 	# 	"fieldtype": "Date",
# 	# },
# 	# {
# 	# 	"fieldname":"shipped_date",
# 	# 	"label": "Shipped Date",
# 	# 	"fieldtype": "Date",
# 	# },
# 	{
# 		"fieldname":"returned_date",
# 		"label": "Returned Date",
# 		"fieldtype": "Date",
# 		"width":100

		
# 	},

# 	{
# 		"fieldname":"dn_no",
# 		"label": "DN No",
# 		"fieldtype": "Link",
# 		"options":"Delivery Note",
# 		"width":150

# 	},

# 	{
# 		"fieldname":"dn_date",
# 		"label": "DN Date",
# 		"fieldtype": "Date",
# 		"width":150

# 	},
# 	{
# 		"fieldname":"expiry_date",
# 		"label": "NER Date(Under warranty)",
# 		"fieldtype": "Date",
# 	},
# 	{
# 		"fieldname":"paid_date",
# 		"label": "Paid Date",
# 		"fieldtype": "Date",
# 		"width":100

# 	},

# 	{
# 		"fieldname":"payment_entry",
# 		"label": "Payment Reference",
# 		"fieldtype": "Link",
# 		"options": "Payment Entry",
# 		"width":150

# 	},

# 	{
# 		"fieldname":"invoice_date",
# 		"label": "Invoice Date",
# 		"fieldtype": "Date",
# 		"width":100

# 	},
# 	{
# 		"fieldname":"invoice_no",
# 		"label": "Invoice No",
# 		"fieldtype": "Link",
# 		"options":"Sales Invoice",
# 		"width":150

# 	},

# 	{
# 		"fieldname":"po",
# 		"label": "PO Number",
# 		"fieldtype": "Data",
# 		"width":150

# 	},
# 	# {
# 	# 	"fieldname":"rv_no",
# 	# 	"label": "R.V. No",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"payment_condition",
# 	# 	"label": "Payment Condition",
# 	# 	"fieldtype": "Data",
# 	# },
	
# 	# {
# 	# 	"fieldname":"remarks",
# 	# 	"label": "Remarks",
# 	# 	"fieldtype": "Data",
# 	# 	"width":150
# 	# },
# 	# {
# 	# 	"fieldname":"pr_no",
# 	# 	"label": "Customer Reference Number",
# 	# 	"fieldtype": "Data",
# 	# 	"width":200
# 	# },
# 	{
# 		"fieldname":"po_no",
# 		"label": "PO No",
# 		"fieldtype": "Link",
# 		"options": "Purchase Order",
# 		"width":100

# 	},

	
# 	# {
# 	# 	"fieldname":"customer_vat_no",
# 	# 	"label": "Customer VAT No",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"vat_status",
# 	# 	"label": "VAT Status",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"unit_location",
# 	# 	"label": "Unit Location",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"q_unit_status",
# 	# 	"label": "Q-Unit Status",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"contact_person_name",
# 	# 	"label": "Contact Person Name",
# 	# 	"fieldtype": "Link",
# 	# 	"options":"Contact"
# 	# },
# 	{
# 		"fieldname":"email_id",
# 		"label": "Conatct Email ID",
# 		"fieldtype": "Data",
# 	},
# 	{
# 		"fieldname":"contact_no",
# 		"label": "Contact No",
# 		"fieldtype": "Data",
# 	},
# 	{
# 		"fieldname":"department",
# 		"label": "Department",
# 		"fieldtype": "Link",
# 		"options":"Cost Center"
# 	},
	

# 	]
# 	return columns
	
		
# def get_data(filters):
# 	# work_order_entries = frappe.db.sql('''select name as wod_no,sales_rep,posting_date,remarks from `tabWork Order Data` where posting_date >= %s and posting_date <= %s''',(filters.from_date,filters.to_date),as_dict=1)
# 	data = []
# 	f = ""
# 	if filters.get('company'):
# 		f += "and company = '{0}' ".format(filters.get('company'))
# 	work_order_entries = frappe.db.sql('''select  payment_entry_reference as payment_entry,payment_date as paid_date,name as wod_no,sales_rep,posting_date,remarks,expiry_date,customer,technician,status,department,returned_date,branch as branch_name,dn_no,dn_date,invoice_no,invoice_date,purchase_order_no as po_no  from `tabWork Order Data` where posting_date>=%s and posting_date <= %s {0}'''.format(f),(filters.from_date,filters.to_date),as_dict=1)
# 	for i in work_order_entries:
# 		pdate = frappe.get_value("Work Order Data",{"name":i["wod_no"]},["payment_date"])
# 		i["paid_date"] = pdate

# 		cr = frappe.get_value("Work Order Data",{"name":i["wod_no"]},["customer_reference_number"])
# 		i["customer_ref"] = cr

# 		dndate = frappe.get_value("Work Order Data",{"name":i["wod_no"]},["dn_date"])
# 		i["dn_date"] = dndate


# 		old_wo_no = frappe.get_value("Work Order Data",{"name":i["wod_no"]},["old_wo_no"])
# 		i["old_wo_no"] = old_wo_no

# 		q_date = frappe.get_value("Work Order Data",{"name":i["wod_no"]},["quoted_date"])
# 		i["quoted_date"] = q_date

# 		old_q_amount = frappe.get_value("Work Order Data",{"name":i["wod_no"]},["old_wo_q_amount"])
# 		i["old_wo_q_amount"] = old_q_amount
		
# 		payment_ref= frappe.get_value("Work Order Data",{"name":i["wod_no"]},["payment_entry_reference"])
# 		i["payment_entry"] = payment_ref

# 		doc = frappe.get_doc("Work Order Data",i["wod_no"])
# 		if doc.status == "NER-Need Evaluation Return":
# 			i['ner_date'] = doc.returned_date
# 		# i["sales_rep"] = frappe.db.get_value("User",i.sales_rep,"full_name")
# 		i["company"] = frappe.defaults.get_user_default("Company")
# 		i["city"] = frappe.db.get_value("Address",frappe.db.get_value("Customer",i.customer,"customer_primary_address"),"city")
# 		for j in frappe.db.sql('''select type,mfg,model_no,serial_no,quantity from `tabMaterial List` where parent = %s''',i.wod_no,as_dict=1):
# 			mod = frappe.db.get_value("Item Model",j["model_no"],"model")
# 			i["type"] = j["type"] 
# 			i["mfg"] = j["mfg"]
# 			i["model_no"] = mod
# 			i["serial_no"] = j["serial_no"]
# 			# i["quantity"] = j["quantity"]
# 		for j in frappe.db.sql('''select margin_amount,rate,amount,parent,q_unit_status from `tabQuotation Item` where wod_no = %s and parenttype = "Quotation"  ''',i.wod_no,as_dict=1):
# 			i["pr_no"] = frappe.db.get_value("Quotation",j['parent'],"customer_reference_number")
# 			is_multi = frappe.db.get_value("Quotation",j['parent'],["is_multiple_quotation","after_discount_cost"])
# 			Quo_status = frappe.db.exists("Quotation",{"name":j['parent'],"workflow_state":"Approved By Customer"})
# 			if Quo_status:
# 				if is_multi[0] == 1:
# 					i["quoted_price"] = j["margin_amount"]
# 				else:
# 					# frappe.errprint(is_multi[-1])
# 					i["quoted_price"] = is_multi[-1]
# 				i["price_after_dis"] = j["amount"]
# 				i["gross"] = j["amount"]
# 				i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
				
# 				po= frappe.db.get_value("Quotation",j['parent'],"purchase_order_no")
# 				i["po"] = po
# 				crn= frappe.db.get_value("Quotation",j['parent'],"customer_reference_number")
# 				# i["customer_ref"] = crn
		
# 				sales_rep=  frappe.get_value("Work Order Data",i["wod_no"],"sales_rep")
# 				if sales_rep:
# 					i["sales_rep"] = sales_rep
# 				else:
# 					i["sales_rep"] = frappe.get_value("Quotation",j["parent"],"sales_rep")
			
# 			else:
# 				Q_status = frappe.db.exists("Quotation",{"name":j['parent'],"workflow_state":"Quoted to Customer"})
# 				if Q_status:
# 					if is_multi[0] == 1:
# 						i["quoted_price"] = j["margin_amount"]
# 					else:
# 						# frappe.errprint(is_multi[-1])
# 						i["quoted_price"] = is_multi[-1]
# 					i["price_after_dis"] = j["amount"]
# 					i["gross"] = j["amount"]
# 					i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
# 					i["q_unit_status"] = j["q_unit_status"]
# 					po= frappe.db.get_value("Quotation",j['parent'],"purchase_order_no")
# 					i["po"] = po
# 					crn= frappe.db.get_value("Quotation",j['parent'],"customer_reference_number")
# 					# i["customer_ref"] = crn
# 					sales_rep=  frappe.get_value("Work Order Data",i["wod_no"],"sales_rep")
# 					if sales_rep:
# 						i["sales_rep"] = sales_rep
# 					else:
# 						i["sales_rep"] = frappe.get_value("Quotation",j["parent"],"sales_rep")
				
# 				elif not Q_status:
# 					rq_status = frappe.db.exists("Quotation",{"name":j['parent'],"workflow_state":"Rejected by Customer"})
# 					if rq_status:
# 						if is_multi[0] == 1:
# 							i["quoted_price"] = j["margin_amount"]
# 						else:
# 							# frappe.errprint(is_multi[-1])
# 							i["quoted_price"] = is_multi[-1]
# 						i["price_after_dis"] = j["amount"]
# 						i["gross"] = j["amount"]
# 						i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
# 						po= frappe.db.get_value("Quotation",j['parent'],"purchase_order_no")
# 						i["po"] = po
# 						crn= frappe.db.get_value("Quotation",j['parent'],"customer_reference_number")
# 						# i["customer_ref"] = crn
				
# 						sales_rep=  frappe.get_value("Work Order Data",i["wod_no"],"sales_rep")
# 						if sales_rep:
# 							i["sales_rep"] = sales_rep
# 						else:
# 							i["sales_rep"] = frappe.get_value("Quotation",j["parent"],"sales_rep")

# 					elif not rq_status:
# 						rq_status = frappe.db.exists("Quotation",{"name":j['parent'],"workflow_state":"Rejected"})
# 						if rq_status:
# 							if is_multi[0] == 1:
# 								i["quoted_price"] = j["margin_amount"]
# 							else:
# 								# frappe.errprint(is_multi[-1])
# 								i["quoted_price"] = is_multi[-1]
# 							i["price_after_dis"] = j["amount"]
# 							i["gross"] = j["amount"]
# 							i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
# 							po= frappe.db.get_value("Quotation",j['parent'],"purchase_order_no")
# 							i["po"] = po
# 							crn= frappe.db.get_value("Quotation",j['parent'],"customer_reference_number")
# 							# i["customer_ref"] = crn
					
# 							sales_rep=  frappe.get_value("Work Order Data",i["wod_no"],"sales_rep")
# 							if sales_rep:
# 								i["sales_rep"] = sales_rep
# 							else:
# 								i["sales_rep"] = frappe.get_value("Quotation",j["parent"],"sales_rep")

				
# 					else:
# 						Q_status_rev = frappe.db.exists("Quotation",{"name":j['parent'],"workflow_state":"Approved By Management","quotation_type":"Revised Quotation - Repair"})
# 						if Q_status_rev:
# 							if is_multi[0] == 1:
# 								i["quoted_price"] = j["margin_amount"]
# 							else:
# 								# frappe.errprint(is_multi[-1])
# 								i["quoted_price"] = is_multi[-1]
# 							i["price_after_dis"] = j["amount"]
# 							i["gross"] = j["amount"]
# 							i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
# 							i["q_unit_status"] = j["q_unit_status"]
# 							po= frappe.db.get_value("Quotation",j['parent'],"purchase_order_no")
# 							i["po"] = po
# 							crn= frappe.db.get_value("Quotation",j['parent'],"customer_reference_number")
# 							# i["customer_ref"] = crn
# 							sales_rep=  frappe.get_value("Work Order Data",i["wod_no"],"sales_rep")
# 							if sales_rep:
# 								i["sales_rep"] = sales_rep
# 							else:
# 								i["sales_rep"] = frappe.get_value("Quotation",j["parent"],"sales_rep")



				
# 		if frappe.db.get_value("Status Duration Details",{"parent":i.wod_no,"status":"Q-Quoted","parenttype": "Work Order Data"},"date"):
# 			i["quoted_date"] = frappe.db.get_value("Status Duration Details",{"parent":i.wod_no,"status":"Q-Quoted","parenttype": "Work Order Data"},"date").date()
		

# 		contact = frappe.db.sql('''select name1,email_id,phone_number from `tabContact Details` where parent = %s and parenttype="Customer" ''',i.customer,as_dict=1)
# 		if contact:
# 			i["contact_person_name"] = contact[0]['name1']
# 			i["email_id"] = contact[0]['email_id']
# 			i["contact_no"] = contact[0]['phone_number']
# 		data.append(i)

# 	return data
	