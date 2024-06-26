# Copyright (c) 2023, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WarrantyForm(Document):
	pass

@frappe.whitelist()

def get_dn(wod):
	delivery_note = frappe.db.sql("""select `tabDelivery Note Item`.wod_no as wo,`tabDelivery Note`.warranty_end_date,`tabDelivery Note`.posting_date as date,`tabDelivery Note`.name as dn from `tabDelivery Note`
		left join `tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
		where `tabDelivery Note Item`.wod_no = '%s' and status != 'Cancelled' """ % (wod), as_dict=True)

	return delivery_note
