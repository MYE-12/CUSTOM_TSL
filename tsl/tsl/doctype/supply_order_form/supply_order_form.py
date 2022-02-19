# Copyright (c) 2022, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def get_contacts(customer):
	doc = frappe.get_doc("Customer",customer)
	l=[]
	for i in doc.get("contact_details"):
		l.append(i.name1)
	return l

class SupplyOrderForm(Document):
	def before_submit(self):
		if not self.branch:
			frappe.throw("Assign a branch to Submit")
	
