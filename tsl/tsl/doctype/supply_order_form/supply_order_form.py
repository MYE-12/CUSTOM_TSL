# Copyright (c) 2022, Tsl and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document
from datetime import datetime

@frappe.whitelist()
def create_supply_order_data(order_no):
	l=[]
	d = {
			"Dammam - TSL-SA":"SOD-D.YY.-",
			"Riyadh - TSL-SA":"SOD-R.YY.-",
			"Jeddah - TSL-SA":"SOD-J.YY.-",
			"Kuwait - TSL":"SOD-K.YY.-"
		}
	sn_no = ""
	doc = frappe._dict(json.loads(order_no))
	if not doc.branch:
		frappe.throw("Please Specify Branch Name")
	if not doc.customer:
		frappe.throw("Please Mention the Customer Name")
	if not doc.incharge:
		frappe.throw("Please Mention the Customer Representative")
	# if not doc.repair_warehouse:
	# 	rw = {
	# 		"Kuwait - TSL":"Repair - Kuwait - TSL",
	# 		"Dammam - TSL-SA":"Repair - Dammam - TSL-SA",
	# 		"Jeddah - TSL-SA":"Repair - Jeddah - TSL-SA",
	# 		"Riyadh - TSL-SA":"Repair - Riyadh - TSL-SA"
	# 	}
	# 	doc.repair_warehouse = rw[doc.branch]
	new_doc = frappe.new_doc("Supply Order Data")
	new_doc.customer = doc.customer
	new_doc.customer_name = doc.customer_name
	new_doc.received_date = doc.received_date
	new_doc.sales_rep = doc.sales_person
	new_doc.tender_issue_date = doc.client_rfq_date
	new_doc.branch = doc.branch
	new_doc.customer_reference_number = doc.customer_reference_number
	# new_doc.department = frappe.db.get_value("Cost Center",{"company":doc.company,"is_supply":1})
	new_doc.department = doc.department
	new_doc.repair_warehouse = doc.repair_warehouse
	new_doc.address = doc.address
	new_doc.incharge = doc.incharge
	if doc.department == "Supply Tender - TSL":
		new_doc.naming_series ="ST-K.YY.-"
	elif doc.company == "TSL COMPANY - UAE":
		new_doc.naming_series ="SOD-DU.YY.-"
	else:
		new_doc.naming_series = d[new_doc.branch]
	if not doc.department == "Supply Tender - TSL":
		if len(doc.get('received_equipment')):
			for i in doc.get("received_equipment"):
				if not 'item_name' in i or not 'manufacturer' in i or not 'model' in i or not 'type' in i:
					frappe.throw("Model, Manufacturer , Type and Item Name are Mandatory")
				if not 'item_code' in i:
					item = frappe.db.get_value("Item",{"model":i['model'],"mfg":i['manufacturer'],"type":i['type'],"item_name":i['item_name']},"name")
					if item:
						if i['serial_no'] in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
							i['item_code'] = item
						elif i['serial_no'] not in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
							i['item_code'] = item
							sn_no = ""
							sn_doc = frappe.new_doc("Serial No")
							sn_doc.serial_no = i['serial_no']
							sn_doc.item_code = i['item_code']
							sn_doc.save(ignore_permissions = True)
							if sn_doc.name:
								sn_no = sn_doc.name
					else:
						i_doc = frappe.new_doc('Item')
						i_doc.naming_series = '.######'
						i_doc.item_name = i['item_name']
						i_doc.item_group = "Equipments"
						i_doc.description = i['item_name']
						i_doc.model = i['model']
						i_doc.is_stock_item = 1
						i_doc.mfg = i['manufacturer']
						i_doc.type = i['type']
						if 'has_serial_no' in i and i['has_serial_no']:
							i_doc.has_serial_no = 1
						i_doc.save(ignore_permissions = True)
						
						if i_doc.name:
							i['item_code'] = i_doc.name
							if 'has_serial_no' in i and i['has_serial_no'] and i['serial_no']:
								sn_no = ""
								sn_doc = frappe.new_doc("Serial No")
								sn_doc.serial_no = i['serial_no']
								sn_doc.item_code = i['item_code']
								sn_doc.save(ignore_permissions = True)
								if sn_doc.name:
									sn_no = sn_doc.name
				# else:
				# 	if frappe.db.get_value("Item",i['item_code'],"has_serial_no") and not i['has_serial_no']:
				# 		frappe.throw("Item {0} in Row -{1} has serial number ".format(i['item_code'],i['idx']))
				new_doc.append("material_list",{
					"item_code": i['item_code'],
					"description":i['item_name'],
					"type":i['type'],
					"model_no":i['model'],
					"mfg":i['manufacturer'],
					"serial_no":sn_no,
					"quantity":i['qty'],
				})
	else:
		for i in doc.get("received_equipment"):
			
			if not 'item_code' in i:
				item = frappe.db.get_value("Item",{"model":i['model']},"name")
				if not item:
					frappe.errprint("ji")
					i_doc = frappe.new_doc('Item')
					i_doc.naming_series = '.######'
					i_doc.description = i['description']
					i_doc.item_number = i['item_number']
					i_doc.model_no = i['model']
					if i['item_group']:
						i_doc.item_group = i['item_group']
					else:
						i_doc.item_group = "Equipments"
					i_doc.model = i['model']
					i_doc.is_stock_item = 0
					if 'has_serial_no' in i and i['has_serial_no']:
						i_doc.has_serial_no = 1
					i_doc.save(ignore_permissions = True)
					if i_doc.name:
						i['item_code'] = i_doc.name
						if 'has_serial_no' in i and i['has_serial_no'] and i['serial_no']:
							sn_no = ""
							sn_doc = frappe.new_doc("Serial No")
							sn_doc.serial_no = i['serial_no']
							sn_doc.item_code = i['item_code']
							sn_doc.save(ignore_permissions = True)
							if sn_doc.name:
								sn_no = sn_doc.name
				
			new_doc.append("material_list",{
				"item_code": i['item_code'],
				"model_no": i['model'],
				"mfg": i['manufracturer'],
				"description":i['description'],
				"item_name":i['model'],	
				"unit":i['uom'],
				"item_group": i['item_group'],
				"item_number":i['item_number'],
				"quantity":i['qty'],
			})
			
	for i in doc.get("equipments_in_stock"):
		category = i['category'] if "category" in i else ""
		sub_category = i['sub_category'] if 'sub_category' in i else ""
		if not 'part_name' in i or not 'manufacturer' in i or not 'model' in i:
			frappe.throw("Model, Manufacturer , Type and Item Name are Mandatory in Row {0}".format(i['idx']))
		if not 'part' in i:
			item = frappe.db.get_value("Item",{"model":i['model'],"mfg":i['manufacturer'],"type":i['type'],"item_name":i['part_name']},"name")
			if item:
				if 'has_serial_no' in i and 'serial_no' in i:
					if i['serial_no'] in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
						i['part'] = item
					elif i['serial_no'] not in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
						frappe.defaults.set_user_default("warehouse", None)
						sn_doc = frappe.new_doc("Serial No")
						sn_doc.serial_no = i['serial_no']
						sn_doc.item_code = i['part']
						sn_doc.save(ignore_permissions = True)
						if sn_doc.name:
							sn_no = sn_doc.name
						i['part'] = item
				i['part'] = item
			else:
				
				i_doc = frappe.new_doc('Item')
				i_doc.naming_series = '.####'
				i_doc.item_name = i['part_name']
				i_doc.category_ =category
				i_doc.sub_category = sub_category
				i_doc.item_group = "Components"
				i_doc.description = i['part_name']
				i_doc.model = i['model']
				i_doc.is_stock_item = 1
				i_doc.mfg = i['manufacturer']
				i_doc.type = i['type']
				if 'has_serial_no' in i and i['has_serial_no']:
					i_doc.has_serial_no = 1
				i_doc.save(ignore_permissions = True)
				if i_doc.name:
					i['part'] = i_doc.name
					if 'has_serial_no' in i and i['has_serial_no'] and i['serial_no']:
						frappe.defaults.set_user_default("warehouse", None)
						sn_doc = frappe.new_doc("Serial No")
						sn_doc.serial_no = i['serial_no']
						sn_doc.item_code = i['part']
						sn_doc.save(ignore_permissions = True)
						if sn_doc.name:
							sn_no = sn_doc.name
		else:
			if frappe.db.get_value("Item",i['part'],"has_serial_no") and not i['has_serial_no']:
				frappe.throw("Item {0} in Row -{1} has serial number ".format(i['part'],i['idx']))
		
		new_doc.append("in_stock",{
			"part":i['part'],
			"model":i['model'],
			"manufacturer":i['manufacturer'],
			"type": i['type'],
			"serial_no":sn_no,
			"category":category,
			"sub_category":sub_category ,
			"part_name": i['part_name']
		}
		)
	new_doc.save(ignore_permissions = True)
	new_doc.submit()
	l.append(new_doc.name)
	if l:
		frappe.delete_doc("Create Supply Order","Create Supply Order")
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
				new_doc.item_group = "Components"
				new_doc.category_ = i.category
				new_doc.sub_category = i.sub_category
				if i.has_serial_no:
					new_doc.has_serial_no = 1
				new_doc.qty = i.qty
				new_doc.type = i.type
				new_doc.model = i.model
				new_doc.mfg = i.manufacturer
				new_doc.serial_no = i.serial_no
				new_doc.save(ignore_permissions = True)
				if new_doc.name:
					i.part = new_doc.name

	def before_submit(self):
		if not self.branch:
			frappe.throw("Assign a branch to Submit")
		for i in self.get('equipments_in_stock'):
			if i.part and i.has_serial_no and i.serial_no:
				if frappe.db.get_value('Item',i.part,"has_serial_no"):
					new_doc = frappe.new_doc('Serial No')
					new_doc.serial_no = i.serial_no
					new_doc.item_code = i.part
					new_doc.save(ignore_permissions = True)
					if new_doc.name:
						i.serial_no = new_doc.name
		
	
