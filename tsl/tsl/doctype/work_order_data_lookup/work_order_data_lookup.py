# Copyright (c) 2023, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WorkOrderDataLookup(Document):
	pass
@frappe.whitelist()
def get_wod_for_tool(doc):
	wod_data = frappe.get_doc("Work Order Data",doc)
	initial_eval = frappe.db.exists("Initial Evaluation",{'work_order_data':doc})
	if initial_eval:
		eval = frappe.get_doc('Initial Evaluation',initial_eval)	
		return wod_data,eval