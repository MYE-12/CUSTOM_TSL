# Copyright (c) 2022, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_qtn(source):
	doc = frappe.get_doc("Service Call Form",source)
	new_doc = frappe.new_doc("Quotation")
	new_doc.naming_series = "SV-QTN-.YY.-"
	new_doc.company = doc.company
	new_doc.party_name = doc.customer,
	new_doc.party_name = new_doc.party_name[0]
	new_doc.customer_name = doc.customer_name
	new_doc.customer_address = frappe.db.get_value("Customer",doc.customer,"customer_primary_address")
	new_doc.address_display = frappe.db.get_value("Customer",doc.customer,"primary_address")
	new_doc.quotation_type = "Site Visit Quotation"
	new_doc.sales_rep = doc.salesman_name
	new_doc.scheduled_date = doc.sch_date
	new_doc.scheduled_time = doc.sch_time
	new_doc.scheduled_day = doc.day 
	new_doc.technician_name = doc.technician_name
	new_doc.branch_name = doc.branch
	new_doc.append("items",{
		"item_code":"Service Item",
		"item_name":"Service Item",
		"description":"Service Item",
		"qty":1,
		"uom":"Nos",
		"stock_uom":"Nos",
		"conversion_factor":1,
		"stock_qty":1,
		"discount_amount":150
	})
	return new_doc
	

	
		

class ServiceCallForm(Document):
	pass
