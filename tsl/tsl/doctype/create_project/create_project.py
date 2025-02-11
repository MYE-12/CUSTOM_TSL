# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CreateProject(Document):
	@frappe.whitelist()
	def crt_pro(self):
		if not self.customer:
			frappe.throw("Please mention Customer")
		if not self.branch:
			frappe.throw("Please mention branch")
		if not self.sales_person:
			frappe.throw("Please mention Sales person")

		if not self.project:
			frappe.throw("Please mention Project Name")

		if not self.items:
			frappe.throw("Please fill Project Details Table")

		for i in self.items:
			md = frappe.get_value("Item Model",i.model,["model"])
			item = frappe.db.exists("Item",{"model":i.model,"type":i.type,"mfg":i.mfg})
			if not item:
				s = frappe.new_doc("Item")
				s.model = i.model
				s.item_name = i.description
				s.description = i.description
				s.type = i.type
				s.mfg = i.mfg
				s.item_group = "Equipments"
				s.stock_uom = "Nos"
				s.save()
				
				
				

		s = frappe.new_doc("Project Data")
		s.customer = self.customer
		s.project = self.project
		s.company = self.company
		s.status = "Initiated"
		s.customer_representative = self.customer_representative
		s.mobile = self.mobile
		s.branch = self.branch
		s.sales_person = self.sales_person
		if self.items:
			for i in self.items:

				it = frappe.db.exists("Item",{"model":i.model,"type":i.type,"mfg":i.mfg})
				if it:
					s.append("items",{
						"sku":it,
						"model":i.model,
						"description":i.description,
						"type":i.type,
						"mfg":i.mfg,
						"qty":i.qty,
						"order_type":i.order_type,
						"automation":i.automation
						})
		s.save()
		s.submit()
		frappe.msgprint("Project is created: <a href='/app/project-data/{0}'>{0}</a>".format(s.name,s.name))
		
			
	@frappe.whitelist()
	def get_contact(self):
		doc = frappe.get_doc("Customer", self.customer)
		l = []
		for i in doc.get("contact_details"):
			l.append(i.name1)
		return l
		
			