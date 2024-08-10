# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class InvoiceRequest(Document):
	@frappe.whitelist()
	def get_work_orders(self):
		data= ""
		data += '<table class="table table-bordered">'
		data += '<tr>'
		data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Linked Work Orders</b><center></td>'
		data += '</tr>'	
		wd = frappe.db.sql(""" select  `tabQuotation Item`.wod_no from `tabQuotation` 
			left join `tabQuotation Item` on `tabQuotation Item`.parent = `tabQuotation`.name
			where `tabQuotation`.name = '%s' """ %(self.quotation),as_dict = 1)
		for i in wd:
			data += '<tr>'
			data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(i["wod_no"])
			data += '</tr>'	
		data += '</table>'
		return data
	
	def on_update(self):
		if self.workflow_state == "Pending with Finance":
			msg = '''Dear Sir,<br> Quotation %s has been approved by the customer.Please take action to make invoice <br><a href="https://erp.tsl-me.com/app/invoice-request/%s" target="_blank">Click Here</a>'''%(self.quotation,self.name)

			frappe.sendmail(
				recipients=["karthiksrinivasan1996.ks@gmail.com","yousuf@tsl-me.com"],
				sender= "Notification from TSL <info@tsl-me.com>",
				subject = "Invoice Request",
				message = msg,
			
				)
