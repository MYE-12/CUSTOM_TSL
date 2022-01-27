# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from tsl.tsl.doctype.work_order_data.work_order_data import get_item_image as img

@frappe.whitelist()
def get_item_image(wod_no):
	erf_no = frappe.db.get_value("Work Order Data",wod_no,"equipment_recieved_form")
	image = img(erf_no)
	return image

class EvaluationReport(Document):
	pass
