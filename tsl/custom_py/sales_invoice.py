import frappe

def on_submit(self,method):
    if self.work_order_data:
        frappe.db.set_value("Work Order Data",self.work_order_data,"invoice_no",self.name)
        frappe.db.set_value("Work Order Data",self.work_order_data,"invoice_date",self.posting_date)