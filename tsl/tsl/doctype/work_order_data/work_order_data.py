# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def create_part_sheet(work_order):
	doc = frappe.get_doc("Work Order Data",work_order)
	new_doc= frappe.new_doc("Part Sheet")
	new_doc.work_order_data = doc.name
	new_doc.customer = doc.customer
	new_doc.customer_name = doc.customer_name
	new_doc.technician = doc.technician
	new_doc.item = doc.material_list[0].item
	new_doc.manufacturer = doc.material_list[0].mfg
	new_doc.model = doc.material_list[0].model_no
	return new_doc

	


class WorkOrderData(Document):
	def before_submit(self):
		if not self.technician:
			frappe.throw("Assign a Technician to submit")
