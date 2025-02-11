# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff,nowdate

class OfficialDocument(Document):
	pass
@frappe.whitelist()
def trigger_mail_notification():
	doc = frappe.get_doc("Official Document","Official Document")
	message = ''
	for i in doc.document_list:
		if i.expiry_date:
			expiry_days = date_diff(i.expiry_date,nowdate())
			if expiry_days == 45:
				message = i.document_name_in_english + " is expiring in 45 days"
			if expiry_days == 30:
				message = i.document_name_in_english + " is expiring in 30 days"
			if expiry_days == 15:
				message = i.document_name_in_english + " is expiring in 15 days"		
			if expiry_days == 3:
				message = i.document_name_in_english + " is expiring in 3 days"
	if message:
		frappe.sendmail(
			recipients="yousuf@tsl-me.com",
			# recipients="hr@tsl-me.com",
			subject=('Document is Expiring !!!'),
			message=message
		)