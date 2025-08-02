# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.core.doctype.communication.email import make

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

	
		if self.table_wknj:
			for i in self.table_wknj:
				if i.sales_invoice:
					cus = frappe.get_value("Sales Invoice",i.sales_invoice,"customer")
					msg = '''Dear Finance,<br><br> Sales Invoice <b>%s</b> has been Requested for cancellation .<br>Customer Name : <b>%s</b>.<br><br>Please take action on cancellation. <br>Reason : <b>%s</b><br><a href="https://erp.tsl-me.com/app/invoice-cancellation/%s" target="_blank">Click Here</a>'''%(i.sales_invoice,cus,self.reason_for_cancellation,self.name)
				
					if self.workflow_state == "Initiate Cancellation":
						if self.branch == "Riyadh - TSL- KSA":

							make(sender = info,
								recipients=["finance-sa1@tsl-me.com"],
								subject="Invoice Cancellation - %s"%(i.sales_invoice),
								content=msg,
								cc=[ "finance@tsl-me.com","alhassan@tsl-me.com",self.sales_email],
								send_email=1,
								)
						elif self.branch == "Jeddah - TSL-SA":
							make(sender = info,
								recipients=["finance-sa1@tsl-me.com"],
								subject="Invoice Cancellation - %s"%(i.sales_invoice),
								content=msg,
								cc=[ "finance@tsl-me.com","omar.m@tsl-me.com",self.sales_email],
								send_email=1,
								)
						elif self.branch == "Dammam - TSL-SA":
							make(sender = info,
								recipients=["finance-sa1@tsl-me.com"],
								subject="Invoice Cancellation - %s"%(i.sales_invoice),
								content=msg,
								cc=[ "finance@tsl-me.com","abdelrahman@tsl-me.com",self.sales_email],
								send_email=1,
								)
						else:
							make(sender = info,
								recipients=["finance2@tsl-me.com"],
								subject="Invoice Cancellation - %s"%(i.sales_invoice),
								content=msg,
								cc=[ "finance-kw@tsl-me.com","omar@tsl-me.com",self.sales_email],

								send_email=1,
								)
				

	def on_submit(self):
		frappe.db.set_value("Invoice Cancellation",self.name,"submitted_by",frappe.session.user)

	
		