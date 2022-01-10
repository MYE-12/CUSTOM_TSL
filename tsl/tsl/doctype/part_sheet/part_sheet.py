# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def check_userrole(user):
	print("\n\n\ncheck calledd.......................\n\n\n")
	if len(frappe.db.sql(""" select role from `tabHas Role` where parent = \'{0}\' and role in ("Technician","Purchase User") """.format(user),as_dict=1)) == 2:
		return 2
	if frappe.db.sql(""" select role from `tabHas Role` where parent = \'{0}\' and role = "Technician" """.format(user),as_dict=1):
		return "Technician"
	if frappe.db.sql(""" select role from `tabHas Role` where parent = \'{0}\' and role = "Purchase User" """.format(user),as_dict=1):
		return "Purchase User"
	return "No Role"

class PartSheet(Document):
	pass
