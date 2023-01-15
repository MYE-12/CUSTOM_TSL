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
		if self.status:
			if self.status == "Working":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "W-Working"
			elif self.status == "Spare Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "SP-Searching Parts"
			elif self.status == "Extra Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "EP-Extra Parts"
			elif self.status == "Comparison":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "C-Comparison"
			elif self.status == "Return Not Repaired":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNR-Return Not Repaired"
			elif self.status == "Return No Fault":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNF-Return No Fault"
			doc.save(ignore_permissions = True)
		if self.if_parts_required:
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			if self.parts_availability == "Yes":
				doc.status = "AP-Available Parts"
			else:
				doc.status = "SP-Searching Parts"
			doc.save(ignore_permissions=True)

	def before_save(self):
		print("save")
		if not frappe.db.get_value("Work Order Data",self.work_order_data,"technician"):
			frappe.db.set_value("Work Order Data",self.work_order_data,"technician",frappe.session.user)
			frappe.db.set_value("Work Order Data",self.work_order_data,"status","UE-Under Evaluation")
		add = 0
		self.total_amount = 0
		for i in self.items:
			total = 0
			if i.total:
				total = i.total
			add += total
		self.total_amount = add
		doc = frappe.get_doc("Work Order Data",self.work_order_data)
		if not doc.technician:
			doc.status = "UE-Under Evaluation"
		doc.save(ignore_permissions = True)
		if self.if_parts_required:
			f=0
			for i in self.get("items"):
				print("1n")
				if not i.part_sheet_no:
					print("2")
					i.part_sheet_no = 1
				if i.parts_availability == "No":
					print("3")
					f=1
			if f:
				self.parts_availability = "No"
			else:
				self.parts_availability = "Yes"

	def on_update_after_submit(self):
		add = total = 0
		self.total_amount = 0
		for i in self.items:
			total = 0
			if i.total:
				total = i.total
			add += total
		self.total_amount = add

		if self.status:
			if self.status == "Working":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "W-Working"
			elif self.status == "Spare Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "SP-Searching Parts"
			elif self.status == "Extra Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "EP-Extra Parts"
			elif self.status == "Comparison":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "C-Comparison"
			elif self.status == "Return Not Repaired":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNR-Return Not Repaired"
			elif self.status == "Return No Fault":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNF-Return No Fault"
			doc.save(ignore_permissions = True)
		if self.if_parts_required:
			self.part_no = 0
			f=0
			for i in self.get("items"):
				if not i.part_sheet_no:
					i.part_sheet_no = int(self.part_no)+1
					frappe.db.set_value("Part Sheet Item",{"parent":self.name,"name":i.name},"part_sheet_no",int(self.part_no)+1)
				else:
					self.part_no = i.part_sheet_no
					
				if i.parts_availability == "No":
					f=1
				
			if f:
				self.parts_availability = "No"
			else:
				self.parts_availability = "Yes"
			if self.parts_availability == "Yes" and self.work_order_data:
				frappe.db.sql("""update `tabWork Order Data` set status = "AP-Available Parts" where name = %s""",self.work_order_data)
			for i in self.items:
				i.is_not_edit = 1
				frappe.db.set_value("Part Sheet Item",{"parent":self.name,"name":i.name},"is_not_edit",1)
	def before_submit(self):
		for i in self.items:
			i.is_not_edit = 1
		if self.if_parts_required:
			wod = frappe.get_doc("Work Order Data",self.work_order_data)
			extra_ps = frappe.db.sql('''select name,attn from `tabEvaluation Report` where work_order_data = %s and docstatus = 1 and creation <= %s''',(self.work_order_data,self.creation),as_dict=1)
			if extra_ps:
				wod.append("extra_part_sheets",{
					"part_sheet_name":self.name,
					"technician":self.attn,
				})
				wod.save(ignore_permissions = True)

		
