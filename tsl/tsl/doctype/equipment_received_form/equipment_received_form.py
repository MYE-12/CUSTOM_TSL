# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

import json
import time
from pydoc import doc
from re import X
# from typing_extensions import Self
import frappe
from frappe.model.document import Document
from datetime import datetime
# from tsl.tsl.custom_py.quotation import before_submit


class EquipmentReceivedForm(Document):
    def before_submit(self):
        if not self.branch:
            frappe.throw("Assign a branch to Submit")
        for i in self.get('received_equipment'):
            if not i.item_code:
                frappe.throw(
                    "Item code should be filled in Row-{0}".format(i.idx))
        for i in self.get('received_equipment'):
            if i.item_code:
                new_doc = frappe.new_doc("Stock Entry")
                new_doc.stock_entry_type = "Material Receipt"
                new_doc.company = self.company
                new_doc.branch = self.branch
                new_doc.equipment_received_form = self.name
                new_doc.to_warehouse = i.repair_warehouse
                new_doc.append("items", {
                    't_warehouse': i.repair_warehouse,
                    'item_code': i.item_code,
                    'item_name': i.item_name,
                    'description': i.item_name,
                    'serial_no': i.serial_no,
                    'qty': i.qty,
                    'uom': frappe.db.get_value("Item", i.item_code, 'stock_uom'),
                    'conversion_factor': 1,
                    'allow_zero_valuation_rate': 1
                })
                new_doc.save(ignore_permissions=True)
                if new_doc.name:
                    new_doc.submit()

    def on_cancel(self):
        if frappe.db.get_list("Stock Entry", {'equipment_received_form': self.name}, "name", as_list=1):
            for i in frappe.db.get_list("Stock Entry", {'equipment_received_form': self.name}, "name", as_list=1):
                doc = frappe.get_doc("Stock Entry", i[0])
                if doc.docstatus == 1:
                    doc.cancel()

    def before_save(self):
        if self.repair_warehouse:
            for i in self.get("received_equipment"):
                i.repair_warehouse = self.repair_warehouse
        for i in self.get('received_equipment'):
            if i.model and i.manufacturer and i.type and i.serial_no:
                for sod in frappe.db.sql('''select parent from `tabMaterial List` where model_no = %s and mfg = %s and type = %s and serial_no = %s and parenttype = "Supply Order Data" ''', (i.model, i.manufacturer, i.type, i.serial_no), as_dict=1):
                    prev_quoted = frappe.db.sql(
                        '''select q.party_name as customer,q.name as name,qi.rate as price from `tabQuotation Item` as qi inner join `tabQuotation` as q on qi.parent = q.name where qi.supply_order_data = %s and (q.quotation_type = "Customer Quotation - Supply" or q.quotation_type = "Revised Quotation - Supply") and q.workflow_state = "Approved By Customer" ''', sod['parent'], as_dict=1)
                    self.append("previously_quoted", {
                        "customer": prev_quoted[0]['customer'],
                        "model": i.model,
                        "mfg": i.manufacturer,
                        "type": i.type,
                        "quoted_price": prev_quoted[0]['price'],
                        "quotation_no": prev_quoted[0]['name']
                    })
        for i in self.get('received_equipment'):
            if not i.item_code:
                item = frappe.db.get_value(
                    "Item", {"model": i.model, "mfg": i.manufacturer, "type": i.type}, "name")
                if item and i.serial_no in [i[0] for i in frappe.db.get_list("Serial No", {"item_code": item}, as_list=1)]:
                    i.item_code = item
                elif item and i.serial_no not in [i[0] for i in frappe.db.get_list("Serial No", {"item_code": item}, as_list=1)]:
                    i.item_code = item
                else:
                    if 'item_name' not in i:
                        i['item_name'] = i['item_code']
                    new_doc = frappe.new_doc('Item')
                    new_doc.naming_series = '.######'
                    new_doc.item_name = i.item_name
                    new_doc.item_group = "Equipments"
                    new_doc.description = i.item_name
                    new_doc.model = i.model
                    new_doc.is_stock_item = 1
                    new_doc.mfg = i.manufacturer
                    new_doc.type = i.type
                    if i.has_serial_no:
                        new_doc.has_serial_no = 1
                    new_doc.save(ignore_permissions=True)
                    if new_doc.name:
                        i.item_code = new_doc.name


@frappe.whitelist()
def get_contacts(customer):
    doc = frappe.get_doc("Customer", customer)
    l = []
    sp = []
    default_sp = ""
    for i in doc.get("contact_details"):
        l.append(i.name1)
    for i in doc.get("sales_person_details"):
        sp.append(i.sales_person)
        if i.is_default:
            default_sp = i.sales_person
    return [l, sp, default_sp]

# @frappe.whitelist()
# def get_sku(model,mfg,type,serial_no):
# 	sku = frappe.db.sql('''select sku from `tabRecieved Equipment` where model = %s and manufacturer = %s and type = %s and serial_no = %s and docstatus = 1 and parenttype = "Equipment Received Form" ''',(model,mfg,type,serial_no),as_dict = 1)
# 	if sku:
# 		return sku[0]['sku']
# 	else:
# 		import random
# 		x = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))
# 		return x


@frappe.whitelist()
def create_workorder_data(order_no, f):
    l = []
    sn_no = ""
    doc = frappe._dict(json.loads(order_no))
    if not doc.branch:
        frappe.throw("Please Specify Branch Name")
    if not doc.customer:
        frappe.throw("Please Mention the Customer Name")
    if not doc.incharge:
        frappe.throw("Please Mention the Customer Representative")
    if not doc.repair_warehouse:
        d = {
            "Kuwait - TSL": "Repair - Kuwait - TSL",
            "Dammam - TSL-SA": "Dammam - TSL-SA",
            "Jeddah - TSL-SA": "Jeddah - TSL-SA",
            "Riyadh - TSL-SA": "Riyadh - TSL-SA"
        }
        doc.repair_warehouse = d[doc.branch]
    if doc.address:
        if not frappe.db.get_value("Dynamic Link", {"parent": doc.address, "link_doctype": "Customer"}, "link_name"):
            addr = frappe.get_doc("Address", doc.address)
            addr.append("links", {
                "link_doctype": "Customer",
                "link_name": doc.customer
            })
            addr.save(ignore_permissions=True)
    if doc.incharge:
        if not frappe.db.get_value("Dynamic Link", {"parent": doc.incharge, "link_doctype": "Customer", "parenttype": "Contact"}, "link_name"):
            addr = frappe.get_doc("Contact", doc.incharge)
            addr.append("links", {
                "link_doctype": "Customer",
                "link_name": doc.customer
            })
            addr.save(ignore_permissions=True)
            frappe.errprint("ji")
    if int(f) == 0:
        for i in doc.get("received_equipment"):
            if i["no_power"]:
                f = 1
            if i["no_output"]:
                f = 1
            if i["no_display"]:
                f = 1
            if i["no_communication"]:
                f = 1
            if i["supply_voltage"]:
                f = 1
            if i["touchkeypad_not_working"]:
                f = 1
            if i["no_backlight"]:
                f = 1
            if i["error_code"]:
                f = 1
            if i["short_circuit"]:
                f = 1
            if i["overloadovercurrent"]:
                f = 1
            if i["other"]:
                f = 1
                
            if int(f) == 0:
                return "Confirm"
            
    for i in doc.get("received_equipment"):
        if not 'item_code' in i:
            item = frappe.db.get_value("Item", {"model": i['model'], "mfg": i['manufacturer'], "type": i['type']}, "name")
            frappe.errprint(item)

            if item and 'serial_no' in i and i['serial_no'] in [i[0] for i in frappe.db.get_list("Serial No", {"item_code": item}, as_list=1)]:
                i['item_code'] = item
            elif item and 'serial_no' in i and i['serial_no'] not in [i[0] for i in frappe.db.get_list("Serial No", {"item_code": item}, as_list=1)]:
                i['item_code'] = item
                frappe.defaults.set_user_default("warehouse", None)
                sn_doc = frappe.new_doc("Serial No")
                sn_doc.serial_no = i['serial_no']
                sn_doc.item_code = i['item_code']
                sn_doc.save(ignore_permissions=True)
                if sn_doc.name:
                    sn_no = sn_doc.name
            elif item:
                i['item_code'] = item
                i['item_name'] = frappe.db.get_value("Item", item, "item_name")
            else:
                if not 'item_name' in i:
                    i['item_name'] = ""
                new_doc = frappe.new_doc('Item')
                new_doc.naming_series = '.######'
                new_doc.item_name = i['item_name']
                new_doc.item_group = "Equipments"
                new_doc.description = i['item_name']
                new_doc.model = i['model']
                new_doc.is_stock_item = 1
                new_doc.mfg = i['manufacturer']
                new_doc.type = i['type']
                if 'has_serial_no' in i and i['has_serial_no']:
                    new_doc.has_serial_no = 1
                new_doc.save(ignore_permissions=True)
                if new_doc.name:
                    i['item_code'] = new_doc.name
                    if 'has_serial_no' in i and i['has_serial_no'] and i['serial_no']:
                        frappe.defaults.set_user_default("warehouse", None)
                        sn_doc = frappe.new_doc("Serial No")
                        sn_doc.serial_no = i['serial_no']
                        sn_doc.item_code = i['item_code']
                        sn_doc.save(ignore_permissions=True)
                        if sn_doc.name:
                            sn_no = sn_doc.name
        # else:
        #     if i['item_code'] and 'serial_no' in i and i['serial_no'] not in [i[0] for i in frappe.db.get_list("Serial No", {"item_code": i['item_code']}, as_list=1)]:
        #         frappe.errprint("hiu")
        #         frappe.defaults.set_user_default("warehouse", None)
        #         sn_doc = frappe.new_doc("Serial No")
        #         sn_doc.serial_no = i['serial_no'] or ''
        #         sn_doc.item_code = i['item_code']
        #         sn_doc.save(ignore_permissions=True)
        #         if sn_doc.name:
        #             sn_no = sn_doc.name

        d = {
            "Dammam - TSL-SA": "WOD-D.YY.-",
            "Riyadh - TSL-SA": "WOD-R.YY.-",
            "Jeddah - TSL-SA": "WOD-J.YY.-",
            "Kuwait - TSL": "WOD-K.YY.-"
        }
        if frappe.db.get_value("Item", i['item_code'], "has_serial_no") and not i['has_serial_no']:
            frappe.throw(
                "Item {0} in Row -{1} has serial number ".format(i['item_code'], i['idx']))

        new_doc = frappe.new_doc("Work Order Data")
        if doc.work_order_data:
            link0 = []
            warr = frappe.db.get_value("Work Order Data", doc.work_order_data, ["delivery", "warranty"], as_dict=1)
            print(warr)
            if warr['delivery'] and warr['warranty']:
                date = frappe.utils.add_to_date(warr['delivery'], months=int(warr['warranty']))
                print(date, type(date))
                frappe.db.set_value("Work Order Data",doc.work_order_data, "expiry_date", date)
                frappe.db.set_value("Work Order Data", doc.work_order_data, "returned_date", doc.received_date)
                eval = frappe.db.exists("Evaluation Report",{"work_order_data":doc.work_order_data})

                if (datetime.strptime(doc.received_date, '%Y-%m-%d').date()) <= date:
                    frappe.errprint("ji")
                    if eval:
                        frappe.errprint(eval)
                        # frappe.db.set_value("Evaluation Report", eval, "ner_field", "NER-Need Evaluation Return")
                        
                    frappe.db.set_value("Work Order Data", doc.work_order_data, "status", "NER-Need Evaluation Return")
                    frappe.db.set_value("Work Order Data", doc.work_order_data, "status_cap", "NER-Need Evaluation Return")
                    if not doc.name == "Create Work Order":
                        frappe.db.set_value("Work Order Data", doc.work_order_data, "equipment_recieved_form", doc.name)
                    link0.append(
                        """ <a href='/app/work-order-data/{0}'>{0}</a> """.format(doc.work_order_data))
                    frappe.msgprint("Work Order Updated: "+', '.join(link0))
                    return True
                else:
                    frappe.throw("Warranty Expired for the Work Order Data - "+str(doc.work_order_data))
            else:
                frappe.throw("No Warranty Period or Delivery Date is Mentioned In work order")
        if i["no_power"]:
            new_doc.no_power = 1
        if i["no_output"]:
            new_doc.no_output = 1
        if i["no_display"]:
            new_doc.no_display = 1
        if i["no_communication"]:
            new_doc.no_communication = 1
        if i["supply_voltage"]:
            new_doc.supply_voltage = 1
        if i["touchkeypad_not_working"]:
            new_doc.touch_keypad_not_working = 1
        if i["no_backlight"]:
            new_doc.no_backlight = 1
        if i["error_code"]:
            new_doc.error_code = 1
        if i["short_circuit"]:
            new_doc.short_circuit = 1
        if i["overloadovercurrent"]:
            new_doc.overload_overcurrent = 1
        if i["other"]:
            new_doc.others = 1
            new_doc.specify = i["specify"]
        
        new_doc.wod_component = i["item_code"] if "item_code" in i else ""
        new_doc.customer = doc.customer
        new_doc.received_date = doc.received_date
        new_doc.sales_rep = doc.sales_person or ''
        new_doc.branch = doc.branch
        new_doc.department = frappe.db.get_value(
            "Cost Center", {"company": doc.company, "is_repair": 1})
        new_doc.repair_warehouse = doc.repair_warehouse
        new_doc.address = doc.address
        new_doc.incharge = doc.incharge
        new_doc.priority_status = doc.sts
        new_doc.naming_series = d[new_doc.branch]
        new_doc.attach_image = (i['attach_image'])
        new_doc.image = (i['attach_image']).replace(
            " ", "%20")
        # serial_no=""
        # if i['has_serial_no'] and i['serial_no']:
        # 	serial_no = i['serial_no']
        # 	sn_doc = frappe.new_doc("Serial No")
        # 	sn_doc.serial_no = i['serial_no']
        # 	sn_doc.item_code = i['item_code']
        # 	sn_doc.warehouse = ""
        # 	sn_doc.status = "Inactive"
        # 	sn_doc.save(ignore_permissions = True)
        if "type" in i:
            item_type = i['type']
        new_doc.append("material_list", {
            "item_code": i['item_code'],
            "item_name": i['item_name'],
            "type": item_type,
            "model_no": i['model'],
            "mfg": i['manufacturer'],
            "serial_no": sn_no,
            "quantity": i['qty'],
        })
        # new_doc.append("price_table",{
        #     "price_type":i["price_type_section"],
        #     "new_price":i["price"],
        #     "websitelink":"Tese",
        # })
        new_doc.save(ignore_permissions=True)
        if new_doc.name and "attach_image" in i:
            frappe.db.sql('''update `tabFile` set attached_to_name = %s where file_url = %s ''',(new_doc.name,i["attach_image"]))
        new_doc.submit()
        if i['item_code']:
            se_doc = frappe.new_doc("Stock Entry")
            se_doc.stock_entry_type = "Material Receipt"
            se_doc.company = doc.company
            se_doc.branch = doc.branch
            se_doc.to_warehouse = doc.repair_warehouse
            se_doc.work_order_data = new_doc.name
            se_doc.append("items", {
                't_warehouse': doc.repair_warehouse,
                'item_code': i['item_code'],
                'item_name': i['item_name'],
                'description': i['item_name'],
                'serial_no': sn_no or "",
                'qty': i['qty'],
                'uom': frappe.db.get_value("Item", i['item_code'], 'stock_uom') or "Nos",
                'branch': doc.branch,
                'cost_center': frappe.db.get_value("Cost Center", {"company": doc.company, "is_repair": 1}) or "",
                'work_order_data': new_doc.name,
                'conversion_factor': 1,
                'allow_zero_valuation_rate': 1
            })
            se_doc.save(ignore_permissions=True)
            if se_doc.name:
                se_doc.submit()
                try:
                    se_doc.submit()
                except Exception as e:
                    frappe.log_error(frappe.get_traceback())
                pass
        l.append(new_doc.name)
    if l:
        frappe.delete_doc("Create Work Order", "Create Work Order")
        link = []
        for i in l:
            link.append(
                """ <a href='/app/work-order-data/{0}'>{0}</a> """.format(i))
        frappe.msgprint("Work Order created: "+', '.join(link))
        return True
    return False


@frappe.whitelist()
def complaint_issue(args):
    args = json.loads(args)
    if args['list']:
        create_workorder_data(args['order_no'], 1)


@frappe.whitelist()
def get_wod_details(wod):
    l = []
    frappe.errprint("o")
    doc = frappe.get_doc("Work Order Data", wod)
    for i in doc.get("material_list"):
        l.append(frappe._dict({
            "item_name": i.item_name,
            "item_code": i.item_code,
            "type": i.type,
            "mfg": i.mfg,
            "model_no": i.model_no,
            "serial_no": i.serial_no,
            "qty": i.quantity,
            "sales_rep": doc.sales_rep,
            "customer": doc.customer,
            "incharge": doc.incharge,
            "address": doc.address,
            "branch": doc.branch

        }))
    return l
