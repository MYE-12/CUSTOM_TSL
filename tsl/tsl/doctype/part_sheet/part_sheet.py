# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def check_userrole(user):
	if len(frappe.db.sql(""" select role from `tabHas Role` where parent = \'{0}\' and role in ("Technician","Purchase User") """.format(user),as_dict=1)) == 2:
		return 2
	if frappe.db.sql(""" select role from `tabHas Role` where parent = \'{0}\' and role = "Technician" """.format(user),as_dict=1):
		return "Technician"
	if frappe.db.sql(""" select role from `tabHas Role` where parent = \'{0}\' and role = "Purchase User" """.format(user),as_dict=1):
		return "Purchase User"
	return "No Role"

@frappe.whitelist()
def get_valuation_rate(doc,item):
	price = frappe.db.get_value("Bin",{"item_code":item},"valuation_rate")
	sts = "Yes"
	if not frappe.db.get_value("Bin",{"item_code":item},"name"):
		sts = "No"
	return [price,sts]

	
@frappe.whitelist()
def get_availabilty(qty,item):
	actual = frappe.db.get_value("Bin",{"item_code":item},"actual_qty")
	if actual:
		if float(actual) >= float(qty):
			return "Yes"
	return "No"


class PartSheet(Document):
	def on_submit(self):
		doc = frappe.get_doc("Work Order Data",self.work_order_data)
		if self.parts_availability == "Yes":
			doc.status = "AP-Available Parts"
		else:
			doc.status = "SP-Searching Parts"
		doc.save(ignore_permissions=True)

	def before_save(self):
		f=0
		for i in self.get("items"):
			if i.parts_availability == "No":
				f=1
		if f==1:
			self.parts_availability = "No"
		else:
			self.parts_availability = "Yes"
