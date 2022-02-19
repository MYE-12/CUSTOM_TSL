from pydoc import doc
import frappe

def on_submit(self,method):
    doc = frappe.get_doc("Part Sheet",self.part_sheet)
    for i in self.get("items"):
        for j in doc.get("items"):
            if  i.item_code == j.part:
                j.parts_availability = "Yes"
    f = 0
    for i in doc.get("items"):
        if i.parts_availability == "No":
            f = 1
    if f==0:
        doc.parts_availability = "Yes"
    doc.save(ignore_permissions = True)
    wod = frappe.get_doc("Work Order Data",self.work_order_data)
    wod.status = "TR-Technician Repair"
    wod.save(ignore_permissions = True)
