# Copyright (c) 2022, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def create_supply_order_data(order_no):
	if frappe.db.get_value("Supply Order Data",{"supply_order_form":order_no}):
		frappe.throw("""Supply Order Data already exists for this Form: {0}""".format(order_no))
	l=[]
	doc = frappe.get_doc("Supply Order Form",order_no)
	# for i in doc.get("received_equipment"):
	# wod = frappe.db.sql("""select wo.name as name from `tabSupply Order Data` as wo join `tabMaterial List` as ml on wo.name=ml.parent where wo.supply_order_form=%s and wo.docstatus!=2 and ml.item_name=%s and ml.quantity=%s""",(order_no,i.item_name, i.qty))
	# if wod:
	# 	frappe.msgprint("""Work Order Data already exists for this Equipment: {0}""".format(i.item_name))
		# continue
	d = {
		"Dammam - TSL-SA":"SOD-D.YY.-",
		"Riyadh - TSL-SA":"SOD-R.YY.-",
		"Jeddah - TSL-SA":"SOD-J.YY.-",
		"Kuwait - TSL":"SOD-K.YY.-"
	}

	new_doc = frappe.new_doc("Supply Order Data")
	# if doc.work_order_data:
	# 	warr = frappe.db.get_value("Work Order Data",doc.work_order_data,["delivery","warranty"])
	# 	date = frappe.utils.add_to_date(warr[0], days=int(warr[1]))
	# 	if doc.received_date <= date:
	# 		new_doc.status = "NER-Need Evaluation Return"
	# 	else:
	# 		frappe.throw("Warranty Expired for the Work Order Data - "+str(doc.work_order_data))
	new_doc.customer = doc.customer
	new_doc.received_date = doc.received_date
	new_doc.sales_rep = doc.sales_person
	new_doc.branch = doc.branch
	new_doc.naming_series = d[new_doc.branch]
	new_doc.supply_order_form = doc.name
	for i in doc.get("equipments_in_stock"):
		new_doc.append("in_stock",{
			"part":i.part,
			'item_name':i.item_name,
			'part_number':i.part_number,
			'category':i.category,
			'sub_category':i.sub_category,
			"part_name":i.part_name,
			"type":i.type,
			"model_no":i.model,
			"mfg":i.manufacturer,
			"serial_no":i.serial_no,
			"qty":i.qty,
			"price_ea":i.price_ea,
			"total":i.total,
			"parts_availability":i.parts_availability,
			
		})
	new_doc.save(ignore_permissions = True)
	l.append(new_doc.name)
	if l:
		link = []
		for i in l:
			link.append(""" <a href='/app/supply-order-data/{0}'>{0}</a> """.format(i))
		frappe.msgprint("Supply Order created: "+', '.join(link))
		return True
	return False

@frappe.whitelist()
def get_contacts(customer):
	doc = frappe.get_doc("Customer",customer)
	l=[]
	for i in doc.get("contact_details"):
		l.append(i.name1)
	return l

class SupplyOrderForm(Document):
	def before_save(self):
		for i in self.get('equipments_in_stock'):
			if i.model and i.manufacturer and i.type and i.serial_no:
				for wod in frappe.db.sql('''select parent from `tabMaterial List` where model_no = %s and mfg = %s and type = %s and serial_no = %s''',(i.model,i.manufacturer,i.type,i.serial_no),as_dict=1):
					prev_quoted = frappe.db.sql('''select q.party_name as customer,q.name as name,qi.rate as price from `tabQuotation Item` as qi inner join `tabQuotation` as q on qi.parent = q.name where qi.wod_no = %s and (q.quotation_type = "Customer Quotation - Repair" or q.quotation_type = "Revised Quotation - Repair") and q.workflow_state = "Approved By Customer" ''',wod['parent'],as_dict = 1)
					self.append("previously_quoted",{
						"customer":prev_quoted[0]['customer'],
						"model":i.model,
						"mfg":i.manufacturer,
						"type":i.type,
						"quoted_price":prev_quoted[0]['price'],
						"quotation_no":prev_quoted[0]['name']
					})

		for i in self.get('equipments_in_stock'):
			if not i.part:
				new_doc = frappe.new_doc('Item')
				new_doc.naming_series = '.####'
				new_doc.item_name = i.part_name
				new_doc.description = i.part_name
				new_doc.item_group = "All Item Groups"
				new_doc.category_ = i.category
				new_doc.sub_category = i.sub_category
				new_doc.qty = i.qty
				new_doc.model = i.model
				new_doc.is_stock_item = 1
				new_doc.mfg = i.manufacturer
				new_doc.serial_no = i.serial_no
				new_doc.save(ignore_permissions = True)
				if new_doc.name:
					i.part = new_doc.name

	def before_submit(self):
		if not self.branch:
			frappe.throw("Assign a branch to Submit")
	
