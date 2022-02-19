from pydoc import doc
import frappe
import json

def on_submit(self,method):
    ps = self.part_sheet
    doc = frappe.get_doc("Part Sheet",ps)
    for i in self.get("items"):
        for j in doc.get("items"):
            if j.part == i.item_code:
                print("if true.....")
                j.price_ea = i.rate
                j.total = i.rate * j.qty
                doc.total_amount += j.total
    doc.save(ignore_permissions=True)
