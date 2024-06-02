# Copyright (c) 2013, Tsl and contributors
# For license information, please see license.txt

import frappe
def execute(filters=None):
	data = []
	if filters.from_date and filters.to_date :
		data = get_data(filters)
	columns = get_columns(filters)
	return columns, data

def get_columns(filters):
	columns = [
		
	{
		"fieldname":"name",
		"label": "SOD",
		"fieldtype": "Link",
		"options" : "Supply Order Data",
		"width":150
	},
	# {
	# 	"fieldname":"wod_no",
	# 	"label": "WOD",
	# 	"fieldtype": "Link",
	# 	"options" : "Work Order Data"
	# },
	# {
	# 	"fieldname":"city",
	# 	"label": "City",
	# 	"fieldtype": "Data",
	# },
	{
		"fieldname":"sales_rep",
		"label": "Sales Name",
		"fieldtype": "Link",
		"options" : "User"
	},
	{
		"fieldname":"received_date",
		"label": "Received Date",
		"fieldtype": "Date",
		"width":100
	},

	{
		"fieldname":"customer_name",
		"label": "Customer Name",
		"fieldtype": "Link",
		"options" : "Customer",
		"width":250
	},
	# {
	# 	"fieldname":"branch_name",
	# 	"label": "Branch/Plant Name",
	# 	"fieldtype": "Data",
	# },
	# {
	# 	"fieldname":"company",
	# 	"label": "Company Name",
	# 	"fieldtype": "Link",
	# 	"options" : "Company"
	# },
	
	{
		"fieldname":"mfg",
		"label": "Mfg",
		"fieldtype": "Data",
		"width":100
	},
	{
		"fieldname":"model_no",
		"label": "Model No",
		"fieldtype": "Data",
		"width":100
	},

	{
		"fieldname":"type",
		"label": "Type",
		"fieldtype": "Data",
		"width":100
	},

	# {
	# 	"fieldname":"serial_no",
	# 	"label": "Serial No",
	# 	"fieldtype": "Data",
	# },
	
	# {
	# 	"fieldname":"quantity",
	# 	"label": "Qty",
	# 	"fieldtype": "Float",
	# 	"width":100
	# },
	{
		"fieldname":"quoted_price",
		"label": "Quoted Price",
		"fieldtype": "Currency",
		"width":100
	},
	{
		"fieldname":"status",
		"label": "Status",
		"fieldtype": "Data",
		"width":150
	},

	{
		"fieldname":"approval_date",
		"label": "Approval Date",
		"fieldtype": "Date",
		"width":100
	},
	# {
	# 	"fieldname":"price_after_dis",
	# 	"label": "Price After Discount",
	# 	"fieldtype": "Currency",
	# },
	# {
	# 	"fieldname":"tax",
	# 	"label": "Tax(VAT)",
	# 	"fieldtype": "Currency",
	# },
	# {
	# 	"fieldname":"gross",
	# 	"label": "Gross",
	# 	"fieldtype": "Currency",
	# },
	# {
	# 	"fieldname":"pc1",
	# 	"label": "1-Payments/Credits",
	# 	"fieldtype": "Currency",
	# },
	# {
	# 	"fieldname":"pc2",
	# 	"label": "2-Payments/Credits",
	# 	"fieldtype": "Currency",
	# },
	# {
	# 	"fieldname":"due_balance",
	# 	"label": "Due Balance",
	# 	"fieldtype": "Currency",
	# },
	# {
	# 	"fieldname":"status",
	# 	"label": "Status",
	# 	"fieldtype": "Data",
	# 	"width" : 200
	# },
	# {
	# 	"fieldname":"quoted_date",
	# 	"label": "Quoted Date",
	# 	"fieldtype": "Date",
	# },
	# {
	# 	"fieldname":"approved_date",
	# 	"label": "Approved Date",
	# 	"fieldtype": "Date",
	# },
	# {
	# 	"fieldname":"return_date",
	# 	"label": "Unit Returned Date to Customer",
	# 	"fieldtype": "Date",
	# },
	{
		"fieldname":"dn_date",
		"label": "Shipped Date",
		"fieldtype": "Date",
		"width":100
	},
	# {
	# 	"fieldname":"dn_no",
	# 	"label": "DN No",
	# 	"fieldtype": "Data",
	# },
	# {
	# 	"fieldname":"ner_date",
	# 	"label": "NER Date(Under warranty)",
	# 	"fieldtype": "Date",
	# },
	{
		"fieldname":"paid_date",
		"label": "Paid Date",
		"fieldtype": "Date",
	},
	# {
	# 	"fieldname":"rv_no",
	# 	"label": "R.V. No",
	# 	"fieldtype": "Data",
	# },
	# {
	# 	"fieldname":"supply_type",
	# 	"label": "Supply Type",
	# 	"fieldtype": "Select",
	# 	"options":["","Used","New"]
	# },
	# {
	# 	"fieldname":"payment_condition",
	# 	"label": "Payment Condition",
	# 	"fieldtype": "Data",
	# },
	{
		"fieldname":"remarks",
		"label": "Remarks",
		"fieldtype": "Data",
		"width":150
	},
	# {
	# 	"fieldname":"invoice_date",
	# 	"label": "Invoice Date",
	# 	"fieldtype": "Date",
	# },
	# {
	# 	"fieldname":"invoice_no",
	# 	"label": "Invoice No",
	# 	"fieldtype": "Data",
	# },
	# {
	# 	"fieldname":"customer_vat_no",
	# 	"label": "Customer VAT No",
	# 	"fieldtype": "Data",
	# },
	# {
	# 	"fieldname":"unit_location",
	# 	"label": "Unit Location",
	# 	"fieldtype": "Data",
	# },

	

	]
	return columns

def get_data(filters):
	data = []
	
	if filters.company:

		supply_order_entries = frappe.db.sql(""" select 
		so.name,
		so.status,						  
		so.posting_date,
		so.customer,
		so.wod_no,
		so.sales_rep,
		so.received_date,
		so.remarks,
		so.customer_name,
		so.status,
		so.department,
		so.company,
		so.branch as branch_name,
		ps.type as type,
		ps.mfg as mfg,
		ps.model_no as model_no
		from `tabSupply Order Data` as so

		left join `tabSupply Order Table` as ps on ps.parent = so.name 
		where so.posting_date  between '%s' and '%s' and so.company = '%s' """ %(filters.from_date,filters.to_date,filters.company),as_dict=1)
		# + frappe.db.sql('''select so.name,so.customer,so.wod_no,so.sales_rep,so.received_date,so.remarks,so.customer_name,so.status,so.department,so.company,so.branch as branch_name,ml.type as type,ml.mfg as mfg,ml.model_no as model_no,ml.serial_no as serial_no,ml.quantity as quantity from `tabSupply Order Data` as so inner join `tabMaterial List` as ml on ml.parent = so.name where so.creation >= %s and so.posting_date <= %s order by so.posting_date desc''',(filters.from_date,filters.to_date),as_dict=1)
	else:
		supply_order_entries = frappe.db.sql(""" select 
		so.name,
		so.status,						  
		so.posting_date,
		so.customer,
		so.wod_no,
		so.sales_rep,
		so.received_date,
		so.remarks,
		so.customer_name,
		so.status,
		so.department,
		so.company,
		so.branch as branch_name,
		ps.type as type,
		ps.mfg as mfg,
		ps.model_no as model_no
		from `tabSupply Order Data` as so

		left join `tabSupply Order Table` as ps on ps.parent = so.name 
		where so.posting_date  between '%s' and '%s'  """ %(filters.from_date,filters.to_date),as_dict=1)
		
	for i in supply_order_entries:
		for j in frappe.db.sql('''select margin_amount,rate,amount,parent,q_unit_status from `tabQuotation Item` where supply_order_data = %s and parenttype = "Quotation"  ''',i["name"],as_dict=1):
			ap_date= frappe.db.get_value("Quotation",j['parent'],["approval_date"])
			i["approval_date"] = ap_date
			dn = frappe.db.sql(''' select posting_date from `tabDelivery Note` left join 
			`tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
			where `tabDelivery Note Item`.supply_order_data = %s ''',i["name"],as_dict=1)
			if dn:
				i["dn_date"] = dn[0]["posting_date"]
			else:
				i["dn_date"] = ''
			
			cq = frappe.db.sql(''' select approval_date from `tabQuotation` left join 
			`tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
			where `tabQuotation Item`.supply_order_data = %s ''',i["name"],as_dict=1)
			if cq:
				i["approval_date"] = cq[0]["approval_date"]
			else:
				i["approval_date"] = ''

			is_multi = frappe.db.get_value("Quotation",j['parent'],["is_multiple_quotation","after_discount_cost"])
			Quo_status = frappe.db.exists("Quotation",{"name":j['parent'],"workflow_state":"Approved By Customer"})
			if Quo_status:
				if is_multi[0] == 1:
					i["quoted_price"] = j["margin_amount"]
				else:
					
					i["quoted_price"] = is_multi[-1]
				i["price_after_dis"] = j["amount"]
				i["gross"] = j["amount"]
				i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
				po= frappe.db.get_value("Quotation",j['parent'],"purchase_order_no")
				i["po"] = po
				im = frappe.get_value("Item Model",{"name":i["model_no"]},["model"])
	
				i["model_no"] = im
				
				
			else:
				Q_status = frappe.db.exists("Quotation",{"name":j['parent'],"workflow_state":"Quoted to Customer"})
				if Q_status:
					if is_multi[0] == 1:
						i["quoted_price"] = j["margin_amount"]
					else:
					
						i["quoted_price"] = is_multi[-1]
	
	# 	i["city"] = frappe.db.get_value("Address",frappe.db.get_value("Customer",i.customer,"customer_primary_address"),"city")
	# 	i["sales_rep"] = frappe.db.get_value("User",i.sales_rep,"full_name")
	# 	for j in frappe.db.sql('''select rate,amount,parent from `tabQuotation Item` where supply_order_data = %s and description = %s and parenttype = "Quotation" ''',(i.name,i.type),as_dict=1):
	# 		i["pr_no"] = frappe.db.get_value("Quotation",j['parent'],"customer_reference_number")
	# 		if frappe.db.get_value("Quotation",j['parent'],"workflow_state") == "Approved By Customer":
	# 			i["quoted_price"] = j["rate"]
	# 			i["price_after_dis"] = j["rate"]
	# 			i["gross"] = j["amount"]
	# 			i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
	# 			i["quoted_date"] = frappe.db.get_value("Quotation",j['parent'],"transaction_date")
	# 	contact = frappe.db.sql('''select name1,email_id,phone_number from `tabContact Details` where parent = %s and parenttype="Customer" ''',i.customer,as_dict=1)
	# 	if contact:
	# 		i["contact_person_name"] = contact[0]['name1']
	# 		i["email_id"] = contact[0]['email_id']
	# 		i["contact_no"] = contact[0]['phone_number']
		data.append(i)

	return data
	
