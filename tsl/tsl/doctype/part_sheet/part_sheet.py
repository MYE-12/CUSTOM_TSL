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
	def on_submit(self):
		if self.parts_availability == "Yes":
			frappe.db.set_value("Work Order Data",{"name":self.work_order_data},"status","AP-Available Parts")
		else:
			frappe.db.set_value("Work Order Data",{"name":self.work_order_data},"status","SP-Searching Parts")

	def before_save(self):
		f=0
		for i in self.get("items"):
			if i.parts_availability == "No":
				f=1
		if f==1:
			self.parts_availability = "No"
		else:
			self.parts_availability = "Yes"
