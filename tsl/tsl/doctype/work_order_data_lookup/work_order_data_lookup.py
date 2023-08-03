# Copyright (c) 2023, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WorkOrderDataLookup(Document):
	pass
@frappe.whitelist()
def get_wod_for_tool(doc):
	wod_data = frappe.get_doc("Work Order Data",doc)
	return wod_data