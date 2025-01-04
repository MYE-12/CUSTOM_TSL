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
        wod.purchase_order_no = self.name
        wod.status = "WP-Waiting Parts"
        wod.save(ignore_permissions = True)
    if self.supply_order_data:
        sod = frappe.get_doc("Supply Order Data",self.supply_order_data)
        sod.status = "Ordered"
        sod.save(ignore_permissions = True)

        
def on_update(self,method):
    if self.work_order_data:
        if self.status == "Completed":
            p = frappe.get_all("Purchase Order",{"work_order_data":self.work_order_data},["*"])
            if p:
                count = 0
                c = 0
                for k in p:
                    count = count + 1
                    if k.status == "Completed":
                        c = c + 1

                if count == c:
                    
                    wod = frappe.get_doc("Work Order Data",self.work_order_data)
                    wod.status = "TR-Technician Repair"
                    wod.save(ignore_permissions = True)

                
                    frappe.errprint("yess")
            