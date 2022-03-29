# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

from pydoc import doc
from re import X
#from typing_extensions import Self
import frappe
from frappe.model.document import Document
# from tsl.tsl.custom_py.quotation import before_submit

class EquipmentReceivedForm(Document):
	def before_submit(self):
		if not self.branch:
			frappe.throw("Assign a branch to Submit")
			
	def before_save(self):
		for i in self.get('received_equipment'):
			if i.model and i.manufacturer and i.type and i.serial_no:
				for sod in frappe.db.sql('''select parent from `tabMaterial List` where model_no = %s and mfg = %s and type = %s and serial_no = %s and parenttype = "Supply Order Data" ''',(i.model,i.manufacturer,i.type,i.serial_no),as_dict=1):
					prev_quoted = frappe.db.sql('''select q.party_name as customer,q.name as name,qi.rate as price from `tabQuotation Item` as qi inner join `tabQuotation` as q on qi.parent = q.name where qi.supply_order_data = %s and (q.quotation_type = "Customer Quotation - Supply" or q.quotation_type = "Revised Quotation - Supply") and q.workflow_state = "Approved By Customer" ''',sod['parent'],as_dict = 1)
					self.append("previously_quoted",{
						"customer":prev_quoted[0]['customer'],
						"model":i.model,
						"mfg":i.manufacturer,
						"type":i.type,
						"quoted_price":prev_quoted[0]['price'],
						"quotation_no":prev_quoted[0]['name']
					})

	

@frappe.whitelist()
def get_contacts(customer):
	doc = frappe.get_doc("Customer",customer)
	l=[]
	for i in doc.get("contact_details"):
		l.append(i.name1)
	return l

@frappe.whitelist()
def get_sku(model,mfg):
	sku = frappe.db.sql('''select sku from `tabRecieved Equipment` where model = %s and manufacturer = %s and docstatus = 1 and parenttype = "Equipment Received Form" ''',(model,mfg),as_dict = 1)
	if sku:
		return sku[0]['sku']
	else:
		import random
		x = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))
		return x


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
			link0 = []
			warr = frappe.db.get_value("Work Order Data",doc.work_order_data,["delivery","warranty"])
			date = frappe.utils.add_to_date(warr[0], days=int(warr[1]))
			print(doc.received_date)
			frappe.db.set_value("Work Order Data",doc.work_order_data,"expiry_date",date)
			frappe.db.set_value("Work Order Data",doc.work_order_data,"returned_date",doc.received_date)
			if doc.received_date <= date:
				frappe.db.set_value("Work Order Data",doc.work_order_data,"status","NER-Need Evaluation Return")
				frappe.db.set_value("Work Order Data",doc.work_order_data,"equipment_recieved_form",doc.name)
				link0.append(""" <a href='/app/work-order-data/{0}'>{0}</a> """.format(doc.work_order_data))
				frappe.msgprint("Work Order Updated: "+', '.join(link0))
				return True
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
	od = frappe.db.get_value("Equipment Received Form",doc.equipment_recieved_form,["incharge","address"])
	for i in doc.get("material_list"):
		l.append(frappe._dict({
			"item_name" : i.item_name,
			"type": i.type,
			"mfg":i.mfg,
			"model_no": i.model_no,
			"serial_no": i.serial_no,
			"qty": i.quantity,
			"sales_rep":doc.sales_rep,
			"customer":doc.customer,
			"incharge":od[0] or None,
			"address" : od[1] or None,
			"branch":doc.branch
			
		}))
	return l