from codecs import ignore_errors
from pydoc import doc
import frappe

def on_submit(self,method):
    if self.work_order_data:
        for i in self.get("items"):
            doc = frappe.get_doc("Item",i.item_code)
            l = []
            if len(doc.supplier_price_details) < 3:
                if not len(doc.supplier_price_details)==0:
                    for j in doc.get("supplier_price_details"):
                        l.append({"supplier_name":j.supplier_name,"price":j.price})
                    doc.supplier_price_details = []
                doc.append("supplier_price_details",{
                    "supplier_name":self.supplier,
                    "price":i.rate
                })
                if l:
                    for j in l:
                        doc.append("supplier_price_details",j)
            else:
                print("\n\n\nelse.....")
                for j in doc.get("supplier_price_details"):
                    l.append({"supplier_name":j.supplier_name,"price":j.price})
                doc.supplier_price_details = []
                l.pop(-1)
                doc.append("supplier_price_details",{
                    "supplier_name":self.supplier,
                    "price":i.rate
                })
                for j in l:
                    doc.append("supplier_price_details",j)
            doc.save(ignore_permissions = True)
        wod = frappe.get_doc("Work Order Data",self.work_order_data)
        wod.status = "WP-Waiting Parts"
        wod.save(ignore_permissions = True)