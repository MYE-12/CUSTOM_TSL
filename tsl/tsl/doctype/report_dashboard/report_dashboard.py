# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReportDashboard(Document):
	@frappe.whitelist()
	def get_wod(self):
		return "Yesss"
