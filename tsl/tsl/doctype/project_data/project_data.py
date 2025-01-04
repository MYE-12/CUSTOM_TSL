# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProjectData(Document):
	@frappe.whitelist()
	def crt_wo(self):
		for i in self.items:
			if i.order_type == "Repair":
				for j in range(i.qty):
					frappe.errprint("Iter")
					s = frappe.new_doc("Work Order Data",)
					s.customer = self.customer
					s.sales_rep = self.sales_person
					s.company = self.company
					s.priority_status = "Normal"
					s.naming_series = "WOD-DU-P-.YY.-"
					s.project = self.name
					s.append("material_list",{
						"item_code":i.sku,
						"model":i.model,
						"description":i.description,
						"type":i.type,
						"mfg":i.mfg,
						"qty":i.qty,
						"order_type":i.order_type,
						})
					s.save(ignore_permissions = 1)
				
			if i.order_type == "Supply":
				s = frappe.new_doc("Supply Order Data",)
				s.customer = self.customer
				s.sales_rep = self.sales_person
				s.company = self.company
				s.priority_status = "Not Urgent"
				s.naming_series = "SOD-DU-P-.YY.-"
				s.project = self.name
				s.append("material_list",{
					"item_code":i.sku,
					"model_no":i.model,
					"description":i.description,
					"type":i.type,
					"mfg":i.mfg,
					"qty":i.qty,
					"item_name":i.description,
					"unit":"Nos",
					"order_type":i.order_type,
					})
				s.save(ignore_permissions = 1)
		
		frappe.msgprint("Documents Created for the Project")
		

	@frappe.whitelist()
	def crt_quote(self):
		new_doc= frappe.new_doc("Quotation")
		new_doc.company = self.company
		new_doc.party_name = self.customer
		# new_doc.sales_rep = doc.sales_rep
		if self.company == "TSL COMPANY - UAE":
			new_doc.selling_price_list = "Standard Selling - UAE"
		new_doc.currency = frappe.db.get_value("Company",self.company,"default_currency")
		new_doc.customer_name = frappe.db.get_value("Customer",self.customer,"customer_name")
		pay_term = ""
		if frappe.db.get_value("Customer",self.customer,"advance"):
			pay_term = "Advance"
		elif frappe.db.get_value("Customer",self.customer,"cash_on_delivery"):
			pay_term = "Cash on Delivery"
		elif frappe.db.get_value("Customer",self.customer,"credit"):
			pay_term = "Credit"
		# new_doc.payment_term = pay_term	
		# new_doc.customer_address = frappe.db.get_value("Customer",self.customer,"customer_primary_address") or self.address
		# new_doc.address_display = frappe.db.get_value("Customer",self.customer,"primary_address")
		# new_doc.contact_person = doc.incharge
		new_doc.naming_series = "PRO-QTN-INT-DU-.YY.-"
		sales = frappe.get_value("Sales Person",self.sales_person,"user")
		if sales:
			new_doc.sales_rep = sales
		new_doc.branch_name = self.branch
		new_doc.project = self.name
		new_doc.quotation_type = "Internal Quotation - Project"
		for i in self.items:
		
			new_doc.append("items",{
				"item_code":i.sku,
				"item_name":i.description,
				"description":i.description,
				"uom":'Nos',
				"qty":i.qty,
				"model_no":i.model,
				"mfg":i.mfg,
				"project":self.name,
			})
			
		
		
		return new_doc
