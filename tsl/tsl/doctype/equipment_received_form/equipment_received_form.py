# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

from pydoc import doc
#from typing_extensions import Self
import frappe
from frappe.model.document import Document
# from tsl.tsl.custom_py.quotation import before_submit

class EquipmentReceivedForm(Document):
	def before_submit(self):
		if not self.branch:
			frappe.throw("Assign a branch to Submit")

	

@frappe.whitelist()
def get_contacts(customer):
	doc = frappe.get_doc("Customer",customer)
	l=[]
	for i in doc.get("contact_details"):
		l.append(i.name1)
	return l



@frappe.whitelist()
def create_workorder_data(order_no):
	l=[]
	doc = frappe.get_doc("Equipment Received Form",order_no)
	for i in doc.get("received_equipment"):
		wod = frappe.db.sql("""select wo.name as name from `tabWork Order Data` as wo join `tabMaterial List` as ml on wo.name=ml.parent where wo.equipment_recieved_form=%s and wo.docstatus!=2 and ml.item_name=%s and ml.quantity=%s""",(order_no,i.item_name, i.qty))
		if wod:
			frappe.msgprint("""Work Order Data already exists for this Equipment: {0}""".format(i.item_name))
			continue
		d = {
			"Dammam - TSL-SA":"WOD-D.YY.-",
			"Riyadh - TSL-SA":"WOD-R.YY.-",
			"Jeddah - TSL-SA":"WOD-J.YY.-",
			"Kuwait - TSL":"WOD-K.YY.-"
		}

		new_doc = frappe.new_doc("Work Order Data")
		if doc.work_order_data:
			warr = frappe.db.get_value("Work Order Data",doc.work_order_data,["delivery","warranty"])
			print(warr)
			date = frappe.utils.add_to_date(warr[0], days=int(warr[1]))
			print(date)
			print(doc.received_date)
			if doc.received_date <= date:
				new_doc.status = "NER-Need Evaluation Return"
			else:
				frappe.throw("Warranty Expired for the Work Order Data - "+str(doc.work_order_data))
		new_doc.customer = doc.customer
		new_doc.received_date = doc.received_date
		new_doc.sales_rep = doc.sales_person
		new_doc.branch = doc.branch
		new_doc.naming_series = d[new_doc.branch]
		new_doc.equipment_recieved_form = doc.name
		new_doc.append("material_list",{
			"item_name": i.item_name,
			"type":i.type,
			"model_no":i.model,
			"mfg":i.manufacturer,
			"serial_no":i.serial_no,
			"quantity":i.qty,
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

@frappe.whitelist()
def get_wod_details(wod):
	l = []
	doc = frappe.get_doc("Work Order Data",wod)
	for i in doc.get("material_list"):
		l.append(frappe._dict({
			"item_name" : i.item_name,
			"type": i.type,
			"mfg":i.mfg,
			"model_no": i.model_no,
			"serial_no": i.serial_no,
			"qty": i.quantity,
			"sales_rep":doc.sales_rep,
			
		}))
	return l