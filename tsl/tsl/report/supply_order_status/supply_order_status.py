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
		_("Supply Order Data") + ":Link/Supply Order Data:140",
		_("Received Date") + ":Date:150",
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
		_("Technician") + ":Data:150",
		_("Quoted Price") + ":Currency:150",
		_("Quoted Date") + ":Date:150",
		_("Po No") + ":Data:140",
		_("Payment Ref") + ":Link/Payment Entry:140",
		_("Payment Date") + ":Date:150",
		_("Delivery Note") +  ":Link/Delivery Note:140",
		_("Delivery Date") + ":Date:150",
		_("Invoice No") +  ":Link/Sales Invoice:140",
		_("Invoice Date") + ":Date:150",
		_("Approval Date") + ":Date:150",
		_("SKU") + ":Data:120",
		_("Qty") + ":Data:90",
		_("Quoted Amount") + ":currency:120",
		_("VAT Amount") + ":currency:120",
		_("Total Amount") + ":currency:120",
		_("Quotation") + ":Link/Quotation:180",
		_("Status") + ":Data:150",
		
	]	
	return columns

def get_data(filters):
	data = []
	if filters.from_date:
		w = frappe.get_all("Supply Order Data",{"company":filters.company,"posting_date":["between",(filters.from_date,filters.to_date)],"docstatus":1},["*"])

	if filters.to_date:
		w = frappe.get_all("Supply Order Data",{"company":filters.company,"posting_date":["between",(filters.from_date,filters.to_date)],"docstatus":1},["*"])

	if filters.company:
		w = frappe.get_all("Supply Order Data",{"company":filters.company,"posting_date":["between",(filters.from_date,filters.to_date)],"docstatus":1},["*"])
	
	if filters.from_date and filters.to_date:
		w = frappe.get_all("Supply Order Data",{"company":filters.company,"posting_date":["between",(filters.from_date,filters.to_date)],"docstatus":1},["*"])

	if filters.from_date and filters.to_date and filters.company:
		w = frappe.get_all("Supply Order Data",{"company":filters.company,"posting_date":["between",(filters.from_date,filters.to_date)],"docstatus":1},["*"])


	for i in w:
		it = frappe.db.sql(''' select type,mfg,model_no,serial_no,quantity,description from `tabSupply Order Table` where parent = %s ''' ,i.name,as_dict=1)
		
		mod = frappe.db.get_value("Item Model",it[0]["model_no"],"model")
		
		q_amt = frappe.db.sql(''' select `tabQuotation`.taxes_and_charges as tax,`tabQuotation`.company as com,`tabQuotation Item`.amount as amt,`tabQuotation Item`.margin_amount as m_am,`tabQuotation`.purchase_order_no as po_no,`tabQuotation Item`.supply_order_data as sod,`tabQuotation Item`.qty as qty,`tabQuotation Item`.item_code as ic,`tabQuotation`.name as q_name,`tabQuotation`.default_discount_percentage as dis,`tabQuotation`.approval_date as a_date,`tabQuotation`.is_multiple_quotation as is_m,`tabQuotation`.after_discount_cost as adc,`tabQuotation`.Workflow_state,`tabQuotation Item`.unit_price as up,`tabQuotation Item`.margin_amount as ma from `tabQuotation` 
		left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
		where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer") and `tabQuotation Item`.supply_order_data = %s ''',i.name,as_dict=1)
		
		
		ap_date = ''
		qu_name = ''
		vat_amt = ''
		q_m = 0
		if q_amt:
			for k in q_amt:
				if k.m_am:
					if q_amt[0]["com"] == "TSL COMPANY - Kuwait":
						per = (k.up * k.dis)/100
						q_m = k.up - per
						q_m = q_m * k.qty
					
					if q_amt[0]["com"] == "TSL COMPANY - UAE":
						# per = (k.up * k.dis)/100
						# q_m = k.up - per
						frappe.errprint(i.name)
						frappe.errprint(q_amt)
						frappe.errprint(q_amt[0]["amt"])
						q_m = k.amt
						if q_amt[0]["tax"]:
							vat_amt = (k.amt * 5)/100
					

				if not k.m_am:
					if q_amt[0]["com"] == "TSL COMPANY - Kuwait":
						q_m = k.adc
					if q_amt[0]["com"] == "TSL COMPANY - UAE":
						q_m = k.adc
						if q_amt[0]["tax"]:
							vat_amt = (k.adc * 5)/100
					

				row = [k.sod,
		   		i.posting_date,
			
				i.sales_rep,
				i.company,
				i.branch,
				it[0]["type"],
				it[0]["mfg"],
				mod,
				it[0]["description"],
				it[0]["serial_no"],
				it[0]["quantity"],
				i.customer,
				i.customer_reference_number,
				i.technician,
				i.quoted_price,
				i.quoted_date,
				k.po_no,
				i.payment_entry_reference,
				i.payment_date,
				i.dn_no,
				i.dn_date,
				i.invoice_no,
				i.invoice_date,
				k.a_date,
				k.ic,
				k.qty,
				round(q_m,2),
				vat_amt,
				round(q_m,2)+vat_amt,
				k.q_name,
				i.status
				]
				data.append(row)
		else:
			row = [i.name,
			i.posting_date,
			i.sales_rep,
			i.company,
			i.branch,
			it[0]["type"],
			it[0]["mfg"],
			mod,
			it[0]["description"],
			it[0]["serial_no"],
			it[0]["quantity"],
			i.customer,
			i.customer_reference_number,
			i.technician,
			i.quoted_price,
			i.quoted_date,
			"",
			i.payment_entry_reference,
			i.payment_date,
			i.dn_no,
			i.dn_date,
			i.invoice_no,
			i.invoice_date,
			"",
			"",
			"",
			"",
			"",
			"",
			"",
			i.status
			]
			data.append(row)

				# ap_date = q_amt[0]["a_date"]
				# qu_name =  q_amt[0]["q_name"]
				# if q_amt[0]["is_m"] == 1:
				# 	per = (q_amt[0]["up"] * q_amt[0]["dis"])/100
				# 	q_m = q_amt[0]["up"] - per

				# if q_amt[0]["is_m"] == 0:
				# 	q_m = q_amt[0]["adc"]

		# else:
		# 	q_amt_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,`tabQuotation`.default_discount_percentage as dis,`tabQuotation`.approval_date as a_date,`tabQuotation`.is_multiple_quotation as is_m,`tabQuotation`.after_discount_cost as adc,`tabQuotation`.Workflow_state,`tabQuotation Item`.unit_price as up,`tabQuotation Item`.margin_amount as ma from `tabQuotation` 
		# 	left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
		# 	where  `tabQuotation`.Workflow_state in ("Quoted to Customer") and `tabQuotation Item`.supply_order_data = %s ''',i.name,as_dict=1)

		# 	if q_amt_2:
		# 		ap_date = q_amt_2[0]["a_date"]
		# 		qu_name =  q_amt_2[0]["q_name"]
		# 		if q_amt_2[0]["is_m"] == 1:
		# 			per = (q_amt_2[0]["up"] * q_amt_2[0]["dis"])/100
		# 			q_m = q_amt_2[0]["up"] - per

		# 		if q_amt_2[0]["is_m"] == 0:
		# 			q_m = q_amt_2[0]["adc"]



		 
	return data



# import frappe
# def execute(filters=None):
# 	data = []
# 	if filters.from_date and filters.to_date :
# 		data = get_data(filters)
# 	columns = get_columns(filters)
# 	return columns, data

# def get_columns(filters):
# 	columns = [
		
# 	{
# 		"fieldname":"name",
# 		"label": "SOD",
# 		"fieldtype": "Link",
# 		"options" : "Supply Order Data",
# 		"width":150
# 	},
# 	# {
# 	# 	"fieldname":"wod_no",
# 	# 	"label": "WOD",
# 	# 	"fieldtype": "Link",
# 	# 	"options" : "Work Order Data"
# 	# },
# 	# {
# 	# 	"fieldname":"city",
# 	# 	"label": "City",
# 	# 	"fieldtype": "Data",
# 	# },
# 	{
# 		"fieldname":"sales_rep",
# 		"label": "Sales Name",
# 		"fieldtype": "Link",
# 		"options" : "User"
# 	},
# 	{
# 		"fieldname":"received_date",
# 		"label": "Received Date",
# 		"fieldtype": "Date",
# 		"width":100
# 	},

# 	{
# 		"fieldname":"customer_name",
# 		"label": "Customer Name",
# 		"fieldtype": "Link",
# 		"options" : "Customer",
# 		"width":250
# 	},
# 	# {
# 	# 	"fieldname":"branch_name",
# 	# 	"label": "Branch/Plant Name",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"company",
# 	# 	"label": "Company Name",
# 	# 	"fieldtype": "Link",
# 	# 	"options" : "Company"
# 	# },
	
# 	{
# 		"fieldname":"mfg",
# 		"label": "Mfg",
# 		"fieldtype": "Data",
# 		"width":100
# 	},
# 	{
# 		"fieldname":"model_no",
# 		"label": "Model No",
# 		"fieldtype": "Data",
# 		"width":100
# 	},

# 	{
# 		"fieldname":"type",
# 		"label": "Type",
# 		"fieldtype": "Data",
# 		"width":100
# 	},

# 	# {
# 	# 	"fieldname":"serial_no",
# 	# 	"label": "Serial No",
# 	# 	"fieldtype": "Data",
# 	# },
	
# 	# {
# 	# 	"fieldname":"quantity",
# 	# 	"label": "Qty",
# 	# 	"fieldtype": "Float",
# 	# 	"width":100
# 	# },
# 	{
# 		"fieldname":"quoted_price",
# 		"label": "Quoted Price",
# 		"fieldtype": "Currency",
# 		"width":100
# 	},
# 	{
# 		"fieldname":"status",
# 		"label": "Status",
# 		"fieldtype": "Data",
# 		"width":150
# 	},

# 	{
# 		"fieldname":"approval_date",
# 		"label": "Approval Date",
# 		"fieldtype": "Date",
# 		"width":100
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
# 	# 	"fieldname":"status",
# 	# 	"label": "Status",
# 	# 	"fieldtype": "Data",
# 	# 	"width" : 200
# 	# },
# 	# {
# 	# 	"fieldname":"quoted_date",
# 	# 	"label": "Quoted Date",
# 	# 	"fieldtype": "Date",
# 	# },
# 	# {
# 	# 	"fieldname":"approved_date",
# 	# 	"label": "Approved Date",
# 	# 	"fieldtype": "Date",
# 	# },
# 	# {
# 	# 	"fieldname":"return_date",
# 	# 	"label": "Unit Returned Date to Customer",
# 	# 	"fieldtype": "Date",
# 	# },
# 	{
# 		"fieldname":"dn_date",
# 		"label": "Shipped Date",
# 		"fieldtype": "Date",
# 		"width":100
# 	},
# 	# {
# 	# 	"fieldname":"dn_no",
# 	# 	"label": "DN No",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"ner_date",
# 	# 	"label": "NER Date(Under warranty)",
# 	# 	"fieldtype": "Date",
# 	# },
# 	{
# 		"fieldname":"paid_date",
# 		"label": "Paid Date",
# 		"fieldtype": "Date",
# 	},
# 	# {
# 	# 	"fieldname":"rv_no",
# 	# 	"label": "R.V. No",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"supply_type",
# 	# 	"label": "Supply Type",
# 	# 	"fieldtype": "Select",
# 	# 	"options":["","Used","New"]
# 	# },
# 	# {
# 	# 	"fieldname":"payment_condition",
# 	# 	"label": "Payment Condition",
# 	# 	"fieldtype": "Data",
# 	# },
# 	{
# 		"fieldname":"remarks",
# 		"label": "Remarks",
# 		"fieldtype": "Data",
# 		"width":150
# 	},
# 	# {
# 	# 	"fieldname":"invoice_date",
# 	# 	"label": "Invoice Date",
# 	# 	"fieldtype": "Date",
# 	# },
# 	# {
# 	# 	"fieldname":"invoice_no",
# 	# 	"label": "Invoice No",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"customer_vat_no",
# 	# 	"label": "Customer VAT No",
# 	# 	"fieldtype": "Data",
# 	# },
# 	# {
# 	# 	"fieldname":"unit_location",
# 	# 	"label": "Unit Location",
# 	# 	"fieldtype": "Data",
# 	# },

	

# 	]
# 	return columns

# def get_data(filters):
# 	data = []
	
# 	if filters.company:

# 		supply_order_entries = frappe.db.sql(""" select 
# 		so.name,
# 		so.status,						  
# 		so.posting_date,
# 		so.customer,
# 		so.wod_no,
# 		so.sales_rep,
# 		so.received_date,
# 		so.remarks,
# 		so.customer_name,
# 		so.status,
# 		so.department,
# 		so.company,
# 		so.branch as branch_name,
# 		ps.type as type,
# 		ps.mfg as mfg,
# 		ps.model_no as model_no
# 		from `tabSupply Order Data` as so

# 		left join `tabSupply Order Table` as ps on ps.parent = so.name 
# 		where so.posting_date  between '%s' and '%s' and so.company = '%s' """ %(filters.from_date,filters.to_date,filters.company),as_dict=1)
# 		# + frappe.db.sql('''select so.name,so.customer,so.wod_no,so.sales_rep,so.received_date,so.remarks,so.customer_name,so.status,so.department,so.company,so.branch as branch_name,ml.type as type,ml.mfg as mfg,ml.model_no as model_no,ml.serial_no as serial_no,ml.quantity as quantity from `tabSupply Order Data` as so inner join `tabMaterial List` as ml on ml.parent = so.name where so.creation >= %s and so.posting_date <= %s order by so.posting_date desc''',(filters.from_date,filters.to_date),as_dict=1)
# 	else:
# 		supply_order_entries = frappe.db.sql(""" select 
# 		so.name,
# 		so.status,						  
# 		so.posting_date,
# 		so.customer,
# 		so.wod_no,
# 		so.sales_rep,
# 		so.received_date,
# 		so.remarks,
# 		so.customer_name,
# 		so.status,
# 		so.department,
# 		so.company,
# 		so.branch as branch_name,
# 		ps.type as type,
# 		ps.mfg as mfg,
# 		ps.model_no as model_no
# 		from `tabSupply Order Data` as so

# 		left join `tabSupply Order Table` as ps on ps.parent = so.name 
# 		where so.posting_date  between '%s' and '%s'  """ %(filters.from_date,filters.to_date),as_dict=1)
		
# 	for i in supply_order_entries:
# 		for j in frappe.db.sql('''select margin_amount,rate,amount,parent,q_unit_status from `tabQuotation Item` where supply_order_data = %s and parenttype = "Quotation"  ''',i["name"],as_dict=1):
# 			ap_date= frappe.db.get_value("Quotation",j['parent'],["approval_date"])
# 			i["approval_date"] = ap_date
# 			dn = frappe.db.sql(''' select posting_date from `tabDelivery Note` left join 
# 			`tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
# 			where `tabDelivery Note Item`.supply_order_data = %s ''',i["name"],as_dict=1)
# 			if dn:
# 				i["dn_date"] = dn[0]["posting_date"]
# 			else:
# 				i["dn_date"] = ''
			
# 			cq = frappe.db.sql(''' select approval_date from `tabQuotation` left join 
# 			`tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
# 			where `tabQuotation Item`.supply_order_data = %s ''',i["name"],as_dict=1)
# 			if cq:
# 				i["approval_date"] = cq[0]["approval_date"]
# 			else:
# 				i["approval_date"] = ''

# 			is_multi = frappe.db.get_value("Quotation",j['parent'],["is_multiple_quotation","after_discount_cost"])
# 			Quo_status = frappe.db.exists("Quotation",{"name":j['parent'],"workflow_state":"Approved By Customer"})
# 			if Quo_status:
# 				if is_multi[0] == 1:
# 					i["quoted_price"] = j["margin_amount"]
# 				else:
					
# 					i["quoted_price"] = is_multi[-1]
# 				i["price_after_dis"] = j["amount"]
# 				i["gross"] = j["amount"]
# 				i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
# 				po= frappe.db.get_value("Quotation",j['parent'],"purchase_order_no")
# 				i["po"] = po
# 				im = frappe.get_value("Item Model",{"name":i["model_no"]},["model"])
	
# 				i["model_no"] = im
				
				
# 			else:
# 				Q_status = frappe.db.exists("Quotation",{"name":j['parent'],"workflow_state":"Quoted to Customer"})
# 				if Q_status:
# 					if is_multi[0] == 1:
# 						i["quoted_price"] = j["margin_amount"]
# 					else:
					
# 						i["quoted_price"] = is_multi[-1]
	
# 	# 	i["city"] = frappe.db.get_value("Address",frappe.db.get_value("Customer",i.customer,"customer_primary_address"),"city")
# 	# 	i["sales_rep"] = frappe.db.get_value("User",i.sales_rep,"full_name")
# 	# 	for j in frappe.db.sql('''select rate,amount,parent from `tabQuotation Item` where supply_order_data = %s and description = %s and parenttype = "Quotation" ''',(i.name,i.type),as_dict=1):
# 	# 		i["pr_no"] = frappe.db.get_value("Quotation",j['parent'],"customer_reference_number")
# 	# 		if frappe.db.get_value("Quotation",j['parent'],"workflow_state") == "Approved By Customer":
# 	# 			i["quoted_price"] = j["rate"]
# 	# 			i["price_after_dis"] = j["rate"]
# 	# 			i["gross"] = j["amount"]
# 	# 			i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
# 	# 			i["quoted_date"] = frappe.db.get_value("Quotation",j['parent'],"transaction_date")
# 	# 	contact = frappe.db.sql('''select name1,email_id,phone_number from `tabContact Details` where parent = %s and parenttype="Customer" ''',i.customer,as_dict=1)
# 	# 	if contact:
# 	# 		i["contact_person_name"] = contact[0]['name1']
# 	# 		i["email_id"] = contact[0]['email_id']
# 	# 		i["contact_no"] = contact[0]['phone_number']
# 		data.append(i)

# 	return data
	
