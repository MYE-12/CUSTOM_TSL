    # Copyright (c) 2023, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class ReturnNote(Document):
    def on_submit(self):
        for wo in self.items:
            doc = frappe.get_doc("Work Order Data",wo.wod_no)
            if doc.status == "RNP-Return No Parts":
                frappe.db.sql('''update `tabWork Order Data` set status = %s where name = %s ''',("RNPC-Return No Parts Client",wo.wod_no))
            elif doc.status == "RNA-Return Not Approved":
                frappe.db.sql('''update `tabWork Order Data` set status = %s where name = %s ''',("RNAC-Return Not Approved Client",wo.wod_no))
            elif doc.status == "RNR-Return Not Repaired":
                frappe.db.sql('''update `tabWork Order Data` set status = %s where name = %s ''',("RNRC-Return Not Repaired Client",wo.wod_no))
            elif doc.status == "RNF-Return No Fault":
                frappe.db.sql('''update `tabWork Order Data` set status = %s where name = %s ''',("RNFC-Return No Fault Client",wo.wod_no))
            elif doc.status == "C-Comparison":
                frappe.db.sql('''update `tabWork Order Data` set status = %s where name = %s ''',("CC-Comparison Client",wo.wod_no))
            
            se_doc = frappe.new_doc("Stock Entry")
            se_doc.stock_entry_type = "Material Issue"
            se_doc.company = doc.company
            se_doc.branch = doc.branch
            se_doc.from_warehouse = doc.repair_warehouse
            se_doc.work_order_data = doc.name
            for i in doc.material_list:
                se_doc.append("items",{
                    's_warehouse': doc.repair_warehouse,
                    'item_code':i.item_code,
                    'item_name':i.item_name,
                    'description':i.item_name,
                    'serial_no':i.serial_no,
                    'qty':i.quantity,
                    'uom':frappe.db.get_value("Item",i.item_code,'stock_uom') or "Nos",
                    'branch':doc.branch,
                    'cost_center':doc.department,
                    'work_order_data':doc.name,
                    'conversion_factor':1,
                    'allow_zero_valuation_rate':1
                })
            se_doc.save(ignore_permissions = True)
            se_doc.submit()
    def on_cancel(self):
        for wo in self.items:
            doc = frappe.get_doc("Work Order Data",wo.wod_no)
            frappe.db.sql('''update `tabWork Order Data` set status = %s where name = %s ''',("NE-Need Evaluation",wo.wod_no))
            se_doc = frappe.new_doc("Stock Entry")
            se_doc.stock_entry_type = "Material Receipt"
            se_doc.company = doc.company
            se_doc.branch = doc.branch
            se_doc.from_warehouse = doc.repair_warehouse
            se_doc.work_order_data = doc.name
            for i in doc.material_list:
                se_doc.append("items",{
                    's_warehouse': doc.repair_warehouse,
                    't_warehouse': doc.repair_warehouse,
                    'item_code':i.item_code,
                    'item_name':i.item_name,
                    'description':i.item_name,
                    'serial_no':i.serial_no,
                    'qty':i.quantity,
                    'uom':frappe.db.get_value("Item",i.item_code,'stock_uom') or "Nos",
                    'branch':doc.branch,
                    'cost_center':doc.department,
                    'work_order_data':doc.name,
                    'conversion_factor':1,
                    'allow_zero_valuation_rate':1
                })
            se_doc.save(ignore_permissions = True)
            se_doc.submit()
     
     
@frappe.whitelist()
def get_wod_items(wod):
    wod = json.loads(wod)
    l=[]
    for k in list(wod):
        doc = frappe.get_doc("Work Order Data",k)
        branch = doc.branch
        for i in doc.material_list:
            l.append(frappe._dict({
                "item_name":i.item_name,
                "item_code":i.item_code,
                "manufacturer":i.mfg,
                "model":i.model_no,
                "type":i.type,
                "serial_number":i.serial_no,
                "serial_no":i.serial_no,
                "description":i.item_name,
                "qty":i.quantity,
                "wod_no":doc.name, 
                "uom":"Nos",
                "stock_uom":"Nos",
                "conversion_factor":1,
                "cost_center":doc.department,
                "rate":1,
                "amount":1,
                "income_account":"4101002 - Revenue from Service - TSL",
                "warehouse":branch

            }))
    return l