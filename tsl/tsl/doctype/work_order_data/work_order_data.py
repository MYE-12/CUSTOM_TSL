# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def get_item_image(erf_no):
	image = frappe.db.sql('''select image from `tabRecieved Equipment Image` where parent = %s order by idx limit 1''',erf_no,as_dict=1)
	return image[0]['image']


@frappe.whitelist()
def create_part_sheet(work_order):
	doc = frappe.get_doc("Work Order Data",work_order)
	new_doc= frappe.new_doc("Part Sheet")
	new_doc.work_order_data = doc.name
	new_doc.customer = doc.customer
	new_doc.customer_name = doc.customer_name
	new_doc.technician = doc.technician
	new_doc.item = doc.material_list[0].item_name
	new_doc.manufacturer = doc.material_list[0].mfg
	new_doc.model = doc.material_list[0].model_no
	return new_doc

@frappe.whitelist()
def create_evaluation_report(doc_no):
	doc = frappe.get_doc("Work Order Data",doc_no)
	new_doc = frappe.new_doc("Evaluation Report")
	new_doc.customer = doc.customer
	new_doc.attn = doc.technician
	new_doc.work_order_data = doc.name
	for i in doc.get("material_list"):
		new_doc.append("evaluation_details",{
			"item":i.item_name,
			"description":i.type,
			"manufacturer":i.mfg,
			"model":i.model_no,
			"serial_no":i.serial_no

		})
	new_doc.item_photo = doc.image
	return new_doc

@frappe.whitelist()
def create_extra_ps(doc):
	l=[]
	extra_ps = frappe.db.sql('''select name,technician from `tabPart Sheet` where work_order_data = %s order by creation''',doc,as_dict=1)
	for i in range(1,len(extra_ps)):
		l.append(extra_ps[i])
	return l

	
class WorkOrderData(Document):
	def before_submit(self):
		if not self.technician:
			frappe.throw("Assign a Technician to Submit")
		if not self.department:
			frappe.throw("Set Department to Submit")