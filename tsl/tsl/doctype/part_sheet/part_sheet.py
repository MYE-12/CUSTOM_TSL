# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

from hashlib import new
from pydoc import doc
import frappe
from frappe.model.document import Document

@frappe.whitelist()
def check_userrole(user,wod):
	if len(frappe.db.sql(""" select role from `tabHas Role` where parent = \'{0}\' and role in ("Technician","Purchase User") """.format(user),as_dict=1)) == 2:
		return 2
	if frappe.db.sql(""" select role from `tabHas Role` where parent = \'{0}\' and role = "Technician" """.format(user),as_dict=1):
		
		return "Technician"
	if frappe.db.sql(""" select role from `tabHas Role` where parent = \'{0}\' and role = "Purchase User" """.format(user),as_dict=1):
		return "Purchase User"
	return "No Role"

@frappe.whitelist()
def get_valuation_rate(item,qty):
	sts = "No"
	if frappe.db.get_value("Bin",{"item_code":item}):
		price = frappe.db.get_value("Item",{"item_code":item},"valuation_rate") or frappe.db.get_value("Item Price",{"item_code":item,"buying":1},"price_list_rate")
		if float(frappe.db.get_value("Bin",{"item_code":item},"actual_qty")) >= float(qty):		
			sts = "Yes"
		return [price,sts]
	return[0,sts]

	
@frappe.whitelist()
def get_availabilty(qty,item):
	actual = frappe.db.get_value("Bin",{"item_code":item},"actual_qty")
	if actual:
		if float(actual) >= float(qty):
			return "Yes"
	return "No"

@frappe.whitelist()
def create_rfq(ps):
	doc = frappe.get_doc("Part Sheet",ps)
	new_doc = frappe.new_doc("Request for Quotation")
	new_doc.company = doc.company
	new_doc.branch = frappe.db.get_value("Work Order Data",doc.work_order_data,"branch")
	print("\n\n\n")
	print(frappe.db.get_value("Work Order Data",doc.work_order_data,"branch"))
	new_doc.part_sheet = ps
	new_doc.work_order_data = doc.work_order_data
	new_doc.department = frappe.db.get_value("Work Order Data",doc.work_order_data,"department")
	new_doc.items=[]
	for i in doc.get("items"):
		if i.parts_availability == "No":
			new_doc.append("items",{
				"item_code":i.part,
				"item_name":i.part_name,
				"description":i.type,
				"uom":"Nos",
				"stock_uom":"Nos",
				"conversion_factor":1,
				"stock_qty":1,
				"qty":i.qty
			})
	return new_doc

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
