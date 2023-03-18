import frappe

def on_submit(self,method):
    for i in self.get("items"):
        if i.work_order_data:
            frappe.db.set_value("Work Order Data",i.work_order_data,"dn_no",self.name)
            frappe.db.set_value("Work Order Data",i.work_order_data,"dn_date",self.posting_date)
            doc = frappe.get_doc("Work Order Data",i.work_order_data)
            doc.status = 'RS-Repaired and Shipped'
            doc.save(ignore_permissions = True)
        if i.supply_order_data:
            doc = frappe.get_doc("Supply Order Data",i.supply_order_data)
            doc.status = "Delivered and Invoiced"
            doc.save(ignore_permissions = True)

