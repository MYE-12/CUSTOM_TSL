# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

from pydoc import doc
import frappe
from frappe.model.document import Document
from tsl.tsl.doctype.work_order_data.work_order_data import get_item_image as img

# @frappe.whitelist()
# def get_item_image(wod_no):
# 	erf_no = frappe.db.get_value("Work Order Data",wod_no,"equipment_recieved_form")
# 	image = img(erf_no)
# 	return image

class EvaluationReport(Document):
	def on_submit(self):
		if self.if_parts_required:
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			if self.parts_availability == "Yes":
				doc.status = "AP-Available Parts"
			else:
				doc.status = "SP-Searching Parts"
			doc.save(ignore_permissions=True)

	def before_save(self):
		if self.if_parts_required:
			f=0
			for i in self.get("items"):
				if i.parts_availability == "No":
					f=1
			if f:
				self.parts_availability = "No"
			else:
				self.parts_availability = "Yes"

	def on_update_after_submit(self):
		print("OUAS")
		if self.if_parts_required:
			f=0
			for i in self.get("items"):
				if i.parts_availability == "No":
					f=1
			if f:
				self.parts_availability = "No"
			else:
				self.parts_availability = "Yes"
		if self.parts_availability == "Yes" and self.work_order_data:

			frappe.db.sql("""update `tabWork Order Data` set status = "AP-Available Parts" where name = %s""",self.work_order_data)
			

	def before_submit(self):
		if self.if_parts_required:
			wod = frappe.get_doc("Work Order Data",self.work_order_data)
			extra_ps = frappe.db.sql('''select name,attn from `tabEvaluation Report` where work_order_data = %s and docstatus = 1 and creation <= %s''',(self.work_order_data,self.creation),as_dict=1)
			if extra_ps:
				wod.append("extra_part_sheets",{
					"part_sheet_name":self.name,
					"technician":self.attn,
				})
				wod.save(ignore_permissions = True)

		
