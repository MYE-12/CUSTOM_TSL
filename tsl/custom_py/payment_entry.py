import frappe,json

def on_submit(self,method):
    if self.supply_order_data and len(self.references)>0:
        doc = frappe.get_doc("Supply Order Data",self.supply_order_data)
        doc.status = "Paid"
        doc.save(ignore_permissions = True)