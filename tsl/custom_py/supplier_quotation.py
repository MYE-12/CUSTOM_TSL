from pydoc import doc
import frappe
import json

def on_submit(self,method):
    if self.part_sheet:
        doc = frappe.get_doc("Part Sheet",self.part_sheet)
        for i in self.get("items"):
            for j in doc.get("items"):
                if j.part == i.item_code:
                    print("if true.....")
                    j.price_ea = i.rate
                    j.total = i.rate * j.qty
        doc.save(ignore_permissions=True)

    if self.supply_order_data:
        doc = frappe.get_doc("Supply Order Data",self.supply_order_data)
        for i in self.get("items"):
            for j in doc.get("in_stock"):
                if j.part == i.item_code:
                    j.price_ea = i.rate
                    j.total = i.rate * j.qty
            for j in doc.get("material_list"):
                if j.item_name == i.item_name:
                    j.price = i.rate
                    j.amount = float(i.rate) * float(j.quantity)
        doc.save(ignore_permissions=True)

