import frappe

def on_submit(self,method):
    for i in self.get("items"):
        frappe.db.set_value("Work Order Data",i.wod_no,"dn_no",self.name)
        frappe.db.set_value("Work Order Data",i.wod_no,"dn_date",self.posting_date)