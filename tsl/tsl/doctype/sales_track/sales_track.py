# Copyright (c) 2023, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalesTrack(Document):
	pass

	# # @frappe.whitelist()
	# def onload(self):
	# 	frappe.errprint("hii")
	# 	user = self.sales_user
	# 	user_name = frappe.db.get_value('User',user,'full_name')
	# 	# frappe.db.set_value(self.sales_person,user_name)

