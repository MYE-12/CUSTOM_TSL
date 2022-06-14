# Copyright (c) 2013, Tsl and contributors
# For license information, please see license.txt

from pkgutil import get_data
import frappe
from datetime import datetime,date

def execute(filters=None):
	data = []
	if filters.from_date and filters.to_date and filters.company:
		data = get_data(filters)
	columns = get_columns(filters)
	return columns, data


def get_columns(filters):
	columns = [
	{
		"fieldname":"wod_no",
		"label": "WOD",
		"fieldtype": "Link",
		"options" : "Work Order Data"
	},
	{
		"fieldname":"sales_rep",
		"label": "Sales Name",
		"fieldtype": "Link",
		"options" : "User"
	},
	{
		"fieldname":"posting_date",
		"label": "Date",
		"fieldtype": "Date",
		"width":100
	},
	{
		"fieldname":"company",
		"label": "Company Name",
		"fieldtype": "Link",
		"options" : "Company"
	},
	{
		"fieldname":"city",
		"label": "City",
		"fieldtype": "Data",
	},
	{
		"fieldname":"branch_name",
		"label": "Branch/Plant Name",
		"fieldtype": "Data",
	},
	{
		"fieldname":"type",
		"label": "Description",
		"fieldtype": "Data",
	},
	{
		"fieldname":"mfg",
		"label": "Mfg",
		"fieldtype": "Data",
		"width":100
	},
	{
		"fieldname":"model_no",
		"label": "Model",
		"fieldtype": "Data",
	},
	{
		"fieldname":"serial_no",
		"label": "Serial No",
		"fieldtype": "Data",
	},
	{
		"fieldname":"technician",
		"label": "Technician",
		"fieldtype": "Link",
		"options" : "User",
		"width":150
	},
	{
		"fieldname":"quantity",
		"label": "Qty",
		"fieldtype": "Float",
		"width":100
	},
	{
		"fieldname":"quoted_price",
		"label": "Quoted Price",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"price_after_dis",
		"label": "Price After Discount",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"tax",
		"label": "Tax(VAT)",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"gross",
		"label": "Gross",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"pc1",
		"label": "1-Payments/Credits",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"pc2",
		"label": "2-Payments/Credits",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"due_balance",
		"label": "Due Balance",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"comisssion",
		"label": "Comission(4%)",
		"fieldtype": "Currency",
	},
	
	{
		"fieldname":"status",
		"label": "Status",
		"fieldtype": "Data",
	},
	{
		"fieldname":"quoted_date",
		"label": "Quoted Date",
		"fieldtype": "Date",
	},
	{
		"fieldname":"approved_date",
		"label": "Approved Date",
		"fieldtype": "Date",
	},
	{
		"fieldname":"return_date",
		"label": "Unit Returned Date to Customer",
		"fieldtype": "Date",
	},
	{
		"fieldname":"shipped_date",
		"label": "Shipped Date",
		"fieldtype": "Date",
	},
	{
		"fieldname":"dn_no",
		"label": "DN No",
		"fieldtype": "Link",
		"options":"Delivery Note"
	},
	{
		"fieldname":"ner_date",
		"label": "NER Date(Under warranty)",
		"fieldtype": "Date",
	},
	{
		"fieldname":"paid_date",
		"label": "Paid Date",
		"fieldtype": "Date",
	},
	{
		"fieldname":"invoice_date",
		"label": "Invoice Date",
		"fieldtype": "Date",
	},
	{
		"fieldname":"invoice_no",
		"label": "Invoice No",
		"fieldtype": "Link",
		"options":"Sales Invoice"
	},
	{
		"fieldname":"rv_no",
		"label": "R.V. No",
		"fieldtype": "Data",
	},
	{
		"fieldname":"payment_condition",
		"label": "Payment Condition",
		"fieldtype": "Data",
	},
	
	{
		"fieldname":"remarks",
		"label": "Remarks",
		"fieldtype": "Data",
		"width":150
	},
	{
		"fieldname":"pr_no",
		"label": "Customer Reference Number",
		"fieldtype": "Data",
		"width":200
	},
	{
		"fieldname":"po_no",
		"label": "PO No",
		"fieldtype": "Link",
		"options": "Purchase Order"
	},
	{
		"fieldname":"customer_vat_no",
		"label": "Customer VAT No",
		"fieldtype": "Data",
	},
	{
		"fieldname":"vat_status",
		"label": "VAT Status",
		"fieldtype": "Data",
	},
	{
		"fieldname":"unit_location",
		"label": "Unit Location",
		"fieldtype": "Data",
	},
	{
		"fieldname":"q_unit_status",
		"label": "Q-Unit Status",
		"fieldtype": "Data",
	},
	{
		"fieldname":"contact_person_name",
		"label": "Contact Person Name",
		"fieldtype": "Link",
		"options":"Contact"
	},
	{
		"fieldname":"email_id",
		"label": "Email ID",
		"fieldtype": "Data",
	},
	{
		"fieldname":"contact_no",
		"label": "Contact No",
		"fieldtype": "Data",
	},
	{
		"fieldname":"department",
		"label": "Department",
		"fieldtype": "Link",
		"options":"Cost Center"
	},
	

	]
	return columns
	
		
def get_data(filters):
	# work_order_entries = frappe.db.sql('''select name as wod_no,sales_rep,posting_date,remarks from `tabWork Order Data` where posting_date >= %s and posting_date <= %s''',(filters.from_date,filters.to_date),as_dict=1)
	data = []
	work_order_entries = frappe.db.sql('''select name as wod_no,sales_rep,posting_date,remarks,customer,technician,status,department,branch as branch_name,dn_no,invoice_no,invoice_date,purchase_order_no as po_no  from `tabWork Order Data` where posting_date>=%s and posting_date <= %s''',(filters.from_date,filters.to_date),as_dict=1)
	for i in work_order_entries:
		doc = frappe.get_doc("Work Order Data",i["wod_no"])
		if doc.status == "NER-Need Evaluation Return":
			i['ner_date'] = doc.returned_date
		i["sales_rep"] = frappe.db.get_value("User",i.sales_rep,"full_name")
		i["company"] = frappe.defaults.get_user_default("Company")
		i["city"] = frappe.db.get_value("Address",frappe.db.get_value("Customer",i.customer,"customer_primary_address"),"city")
		for j in frappe.db.sql('''select type,mfg,model_no,serial_no,quantity from `tabMaterial List` where parent = %s''',i.wod_no,as_dict=1):
			i["type"] = j["type"] 
			i["mfg"] = j["mfg"]
			i["model_no"] = j["model_no"]
			i["serial_no"] = j["serial_no"]
			i["quantity"] = j["quantity"]
		for j in frappe.db.sql('''select rate,amount,parent,q_unit_status from `tabQuotation Item` where wod_no = %s and parenttype = "Quotation"  ''',i.wod_no,as_dict=1):
			i["pr_no"] = frappe.db.get_value("Quotation",j['parent'],"customer_reference_number")
			if frappe.db.get_value("Quotation",j['parent'],"workflow_state") == "Approved By Customer":
				i["quoted_price"] = j["amount"]
				i["price_after_dis"] = j["amount"]
				i["gross"] = j["amount"]
				i["approved_date"] = frappe.db.get_value("Quotation",j['parent'],"approval_date")
				i["q_unit_status"] = j["q_unit_status"]
		if frappe.db.get_value("Status Duration Details",{"parent":i.wod_no,"status":"Q-Quoted","parenttype": "Work Order Data"},"date"):
			i["quoted_date"] = frappe.db.get_value("Status Duration Details",{"parent":i.wod_no,"status":"Q-Quoted","parenttype": "Work Order Data"},"date").date()
		

		contact = frappe.db.sql('''select name1,email_id,phone_number from `tabContact Details` where parent = %s and parenttype="Customer" ''',i.customer,as_dict=1)
		if contact:
			i["contact_person_name"] = contact[0]['name1']
			i["email_id"] = contact[0]['email_id']
			i["contact_no"] = contact[0]['phone_number']
		data.append(i)

	return data
	