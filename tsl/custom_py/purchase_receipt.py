from pydoc import doc
import frappe

def before_save(self,method):
    for i in self.items:
        if i.item_code and frappe.db.get_value("Item",i.item_code,"has_serial_no"):
            serial_nos = frappe.db.get_list("Serial No",{"item_code":i.item_code},"name")
            if len(serial_nos)>1:
                frappe.throw("Choose Serial No for this Item {0}".format(i.item_code))
            i.serial_no = serial_nos[0]["name"]

def on_submit(self,method):
    if self.part_sheet:
        doc = frappe.get_doc("Evaluation Report",self.part_sheet)
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
    if self.supply_order_data:
        wod = frappe.get_doc("Supply Order Data",self.supply_order_data)
        wod.status = "Received"
        for i in self.get('items'):
            for j in wod.get('in_stock'):
                if i.item_code == j.part:
                    j.parts_availability = "Yes"
            for j in wod.get("material_list"):
                if i.item_code == j.item_code:
                    j.parts_availability = "Yes"
        wod.save(ignore_permissions = True)
