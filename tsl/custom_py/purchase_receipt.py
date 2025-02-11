from pydoc import doc
import frappe

def before_save(self,method):
    for i in self.items:
        if i.item_code and frappe.db.get_value("Item",i.item_code,"has_serial_no"):
            serial_nos = frappe.db.get_list("Serial No",{"item_code":i.item_code},"name")
            # if len(serial_nos)>1:
            #     frappe.throw("Choose Serial No for this Item {0}".format(i.item_code))
            # i.serial_no = serial_nos[0]["name"]

def on_submit(self,method):
    if self.items:
        for k in self.items:
            if k.work_order_data:
                ev = frappe.get_value("Evaluation Report",{"work_order_data":k.work_order_data},["name"])
                if ev:
                    doc = frappe.get_doc("Evaluation Report",ev)
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


    # if self.part_sheet:
    #     doc = frappe.get_doc("Evaluation Report",self.part_sheet)
    #     for i in self.get("items"):
    #         for j in doc.get("items"):
    #             if  i.item_code == j.part:
    #                 j.parts_availability = "Yes"
    #     f = 0
    #     for i in doc.get("items"):
    #         if i.parts_availability == "No":
    #             f = 1
    #     if f==0:
    #         doc.parts_availability = "Yes"
    #     doc.save(ignore_permissions = True)

    for i in self.get("items"):
        if i.work_order_data:
            count = 0
            ct = 0
            # frappe.errprint(i.work_order_data)
            e = frappe.db.exists("Evaluation Report",{"work_order_data":i.work_order_data})
            if e:
                ev= frappe.get_doc("Evaluation Report",e)
                
                for k in ev.items:
                    count = count + 1
                    if k.parts_availability == "Yes":
                        ct = ct + 1
                        
            if count == ct:
                wod = frappe.get_doc("Work Order Data",i.work_order_data)
                wod.status = "TR-Technician Repair"
                wod.save(ignore_permissions = True)

                wod = frappe.get_doc("Evaluation Report",{"work_order_data":i.work_order_data})
                wod.received = 1
                wod.save(ignore_permissions = True)


    # for i in self.get("items"):
    #     if i.work_order_data:
    #         wod = frappe.get_doc("Work Order Data",i.work_order_data)
    #         wod.status = "TR-Technician Repair"
    #         wod.save(ignore_permissions = True)

    #         wod = frappe.get_doc("Evaluation Report",{"work_order_data":i.work_order_data})
    #         wod.received = 1
    #         wod.save(ignore_permissions = True)

    for i in self.get("items"): 
        if i.supply_order_data:
            wod = frappe.get_doc("Supply Order Data",i.supply_order_data)
            wod.status = "Received"
            wod.save(ignore_permissions = True)

        # for i in self.get('items'):
        #     for j in wod.get('in_stock'):
        #         if i.item_code == j.part:
        #             j.parts_availability = "Yes"
        #     for j in wod.get("material_list"):
        #         if i.item_code == j.item_code:
        #             j.parts_availability = "Yes"
        # wod.save(ignore_permissions = True)


def check_item(self,method):
    for i in self.items:
        if i.serial_no:
            # frappe.errprint(i.item_code)
            item = frappe.get_value("Item",{"name":i.item_code},["has_serial_no"])
            if item == 0:   
                frappe.db.set_value("Item",i.item_code,"has_serial_no",1)

