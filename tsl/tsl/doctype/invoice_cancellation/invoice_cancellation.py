# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InvoiceCancellation(Document):
	@frappe.whitelist()
	def on_update(self):
		info = ""
		if self.branch == "Riyadh - TSL- KSA":
			info = "info-sa@tsl-me.com"
		if self.branch == "Dammam - TSL-SA":
			info = "info-dmm@tsl-me.com"
		if self.branch == "Jeddah - TSL-SA":
			info = "info-jed@tsl-me.com"
		if self.branch == "Kuwait - TSL":
			info = "info@tsl-me.com"		
		# if not self.email_sent:
		# 	if self.invoice_list:
		# 		for i in self.invoice_list:
		# 			if i.invoice_no:
		# 				cus = frappe.get_value("Quotation",i.invoice_no,"party_name")
		# 				msg = '''Dear Finance,<br><br> Quotation <b>%s</b> has been approved.<br>Customer Name : <b>%s</b>.<br><br>Please take action to make invoice. <br><br><a href="https://erp.tsl-me.com/app/invoice-request/%s" target="_blank">Click Here</a>'''%(i.invoice_no,cus,self.name)
                    
		# 				if self.workflow_state == "Pending with Finance":
		# 					if self.branch != "Kuwait - TSL":
							
		# 						frappe.sendmail(
		# 							sender= info,
		# 							recipients=['finance-sa1@tsl-me.com',"finance@tsl-me.com"],
		# 							cc = ["karthiksrinivasan1996.ks@gmail.com","yousuf@tsl-me.com"],
		# 							subject = "Invoice Request - %s"%(i.invoice_no),
		# 							message = msg,
								
		# 							)
		# 						# frappe.db.set_value("Invoice Request",self.name,"email_sent",1)
		# 						self.email_sent = 1
		# 					else:
		# 						frappe.sendmail(
		# 							sender= info,
		# 							recipients=['finance2@tsl-me.com',"finance-kw@tsl-me.com"],
		# 							cc = ["karthiksrinivasan1996.ks@gmail.com","yousuf@tsl-me.com"],
		# 							subject = "Invoice Request - %s"%(i.invoice_no),
		# 							message = msg,
								
		# 							)
		# 						# frappe.db.set_value("Invoice Request",self.name,"email_sent",1)
		# 						self.email_sent = 1

	def on_submit(self):
		frappe.db.set_value("Invoice Cancellation",self.name,"submitted_by",frappe.session.user)

	
		