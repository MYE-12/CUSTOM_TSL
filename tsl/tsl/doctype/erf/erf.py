# Copyright (c) 2025, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ERF(Document):
	pass


	
@frappe.whitelist()
def create_work_order_from_erf(source_name, target_doc=None):
	from frappe.model.mapper import get_mapped_doc

	doc = get_mapped_doc(
		"ERF",
		source_name,
		{
			"ERF": {"doctype": "Create Work Order Kuwait"},
			"Received Equipment ERF": {
				"doctype": "Received Equipment",
			},
		},
		target_doc
	)

	return doc
