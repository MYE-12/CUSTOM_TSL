import frappe,datetime,json

def on_submit(self,method):
    if self.supply_order_data:
        doc  = frappe.get_doc("Supply Order Data",self.supply_order_data)
        doc.status = "Searching Items"
        doc.save(ignore_permissions = True)