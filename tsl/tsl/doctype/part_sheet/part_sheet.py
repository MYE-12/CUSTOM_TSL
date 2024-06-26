# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

from hashlib import new
from pydoc import doc
import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date

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
def get_valuation_rate(item,warehouse,qty):
	price = 0
	sts = "No"
	invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":warehouse,"is_branch":1},"name",as_list=1)]

	#if frappe.db.get_value("Bin",{"item_code":item,"warehouse":["in",invent],"actual_qty":[">=",qty]}):
	bin = frappe.db.sql("""select name from `tabBin` where item_code = '{0}'  and warehouse in ('{1}') and (actual_qty) >= {2}""".format(item,"','".join(invent),qty),as_dict =1)

	if len(bin) and 'name' in bin[0]:
		price = frappe.db.get_value("Bin",{"item_code":item},"valuation_rate") or frappe.db.get_value("Item Price",{"item_code":item,"buying":1},"price_list_rate")
		sts = "Yes"
	return[price,sts]

@frappe.whitelist()
def get_availabilty(item,qty,warehouse):
	invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":warehouse,"is_branch":1},"name",as_list=1)]
	actual = frappe.db.get_value("Bin",{"item_code":item,"warehouse":["in",invent]},"actual_qty")
	if actual:
		if float(actual) >= float(qty):
			return "Yes"
	return "No"
@frappe.whitelist()
def get_serial_no(item):
	return [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]

@frappe.whitelist()
def create_rfq(ps):
	doc = frappe.get_doc("Evaluation Report",ps)
	new_doc = frappe.new_doc("Request for Quotation")
	new_doc.company = doc.company
	new_doc.branch = frappe.db.get_value("Work Order Data",doc.work_order_data,"branch")
	new_doc.part_sheet = ps
	new_doc.work_order_data = doc.work_order_data
	new_doc.department = frappe.db.get_value("Work Order Data",doc.work_order_data,"department")
	new_doc.items=[]
	psn = doc.items[-1].part_sheet_no
	for i in doc.get("items"):
		if i.parts_availability == "No" and psn == i.part_sheet_no:
			new_doc.append("items",{
				"item_code":i.part,
				"item_name":i.part_name,
				"description":i.part_name,
				'model':i.model,
				"category":i.category,
				"sub_category":i.sub_category,
				"mfg":i.manufacturer,
				'serial_no':i.serial_no,
				"uom":"Nos",
				"stock_uom":"Nos",
				"conversion_factor":1,
				"stock_qty":1,
				"qty":i.qty,
				"schedule_date":add_to_date(new_doc.transaction_date,days = 2),
				"warehouse":new_doc.branch,
				"branch":new_doc.branch,
				"work_order_data":doc.work_order_data,
				"department":frappe.db.get_value("Work Order Data",doc.work_order_data,"department")
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
