# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EquipmentReceivedForm(Document):
	pass



@frappe.whitelist()
def create_workorder_data(order_no):
	l=[]
	doc = frappe.get_doc("Equipment Received Form",order_no)
	for i in doc.get("received_equipment"):
		wod = frappe.db.sql("""select wo.name as name from `tabWork Order Data` as wo join `tabMaterial List` as ml on wo.name=ml.parent where wo.equipment_recieved_form=%s and wo.docstatus!=2 and ml.item=%s and ml.quantity=%s""",(order_no,i.item, i.qty))
		if wod:
			frappe.msgprint("""Work Order Data already exists for this Equipment: {0}""".format(i.item))
			continue

		new_doc = frappe.new_doc("Work Order Data")
		new_doc.customer = doc.customer
		new_doc.received_date = doc.received_date
		new_doc.sales_rep = doc.incharge
		new_doc.equipment_recieved_form = doc.name
		new_doc.append("material_list",{
			"item":i.item,
			"item_name": i.item_name,
			"mfg":i.manufacturer,
			"serial_no":i.serial_no,
			"quantity":i.qty,
			"uom": i.uom,
			"item_image":i.image
		})
		new_doc.save(ignore_permissions = True)
		l.append(new_doc.name)
	if l:
		link = []
		for i in l:
			link.append(""" <a href='/app/work-order-data/{0}'>{0}</a> """.format(i))
		frappe.msgprint("Work Order created: "+', '.join(link))
		return True
	return False
