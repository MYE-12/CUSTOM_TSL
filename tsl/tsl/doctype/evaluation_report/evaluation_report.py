# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
@frappe.whitelist()
def get_item_image(wod_no):
	image = frappe.db.get_value("Material List",{"parent":wod_no},"item_image")
	return image

class EvaluationReport(Document):
	pass
