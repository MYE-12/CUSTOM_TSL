import frappe

def on_submit(self,method):
	if self.work_order_data:
		frappe.db.set_value("Work Order Data",self.work_order_data,"invoice_no",self.name)
		frappe.db.set_value("Work Order Data",self.work_order_data,"invoice_date",self.posting_date)

def before_save(self,method):
	if self.taxes:
		igst = cgst = sgst = 0
		for i in self.taxes:
			if "IGST" in i.account_head:
				igst = i.rate
			if "SGST" in i.account_head:
				sgst = i.rate
			if "CGST" in i.account_head:
				cgst = i.rate
		for i in self.items:
			if i.net_amount:
				self.igst = round((i.net_amount * float(igst))/100)
				self.cgst = round((i.net_amount * float(cgst))/100)
				self.sgst = round((i.net_amount * float(sgst))/100)
			

