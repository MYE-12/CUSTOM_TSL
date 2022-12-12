# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

import json
from pydoc import doc
from re import X
#from typing_extensions import Self
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
				frappe.throw("Item code should be filled in Row-{0}".format(i.idx))
		for i in self.get('received_equipment'):
			if i.item_code:
				new_doc = frappe.new_doc("Stock Entry")
				new_doc.stock_entry_type = "Material Receipt"
				new_doc.company = self.company
				new_doc.branch = self.branch
				new_doc.equipment_received_form = self.name
				new_doc.to_warehouse = i.repair_warehouse
				new_doc.append("items",{
					't_warehouse': i.repair_warehouse,
					'item_code':i.item_code,
					'item_name':i.item_name,
					'description':i.item_name,
					'serial_no':i.serial_no,
					'qty':i.qty,
					'uom':frappe.db.get_value("Item",i.item_code,'stock_uom'),
					'conversion_factor':1,
					'allow_zero_valuation_rate':1
				})
				new_doc.save(ignore_permissions = True)
				if new_doc.name:
					new_doc.submit()

	def on_cancel(self):
		if frappe.db.get_list("Stock Entry",{'equipment_received_form':self.name},"name",as_list = 1):
			for i in frappe.db.get_list("Stock Entry",{'equipment_received_form':self.name},"name",as_list = 1):
				doc = frappe.get_doc("Stock Entry",i[0])
				if doc.docstatus == 1:
					doc.cancel()

	def before_save(self):
		if self.repair_warehouse:
			for i in self.get("received_equipment"):
				i.repair_warehouse = self.repair_warehouse
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
		for i in self.get('received_equipment'):
			if not i.item_code:
				item = frappe.db.get_value("Item",{"model":i.model,"mfg":i.manufacturer,"type":i.type,"item_name":i.item_name},"name")
				if item and i.serial_no in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
					i.item_code = item
				elif item and i.serial_no not in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
					i.item_code = item
				else:
					new_doc = frappe.new_doc('Item')
					new_doc.naming_series = '.####'
					new_doc.item_name = i.item_name
					new_doc.item_group = "Equipments"
					new_doc.description = i.item_name
					new_doc.model = i.model
					new_doc.is_stock_item = 1
					new_doc.mfg = i.manufacturer
					new_doc.type = i.type
					if i.has_serial_no:
						new_doc.has_serial_no = 1
					new_doc.save(ignore_permissions = True)
					if new_doc.name:
						i.item_code = new_doc.name

@frappe.whitelist()
def get_contacts(customer):
	doc = frappe.get_doc("Customer",customer)
	l=[]
	sp = []
	default_sp = ""
	for i in doc.get("contact_details"):
		l.append(i.name1)
	for i in doc.get("sales_person_details"):
		sp.append(i.sales_person)
		if i.is_default:
			default_sp = i.sales_person
	return [l,sp,default_sp]

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
def create_workorder_data(order_no):
	l=[]
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
			"Kuwait - TSL":"Repair - Kuwait - TSL",
			"Dammam - TSL-SA":"Repair - Dammam - TSL-SA",
			"Jeddah - TSL-SA":"Repair - Jeddah - TSL-SA",
			"Riyadh - TSL-SA":"Repair - Riyadh - TSL-SA"
		}
		doc.repair_warehouse = d[doc.branch]

	for i in doc.get("received_equipment"):
		if not 'item_code' in i:
			item = frappe.db.get_value("Item",{"model":i['model'],"mfg":i['manufacturer'],"type":i['type'],"item_name":i['item_name']},"name")
			if item and i['serial_no'] in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
				i['item_code'] = item
			elif item and i['serial_no'] not in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
				i['item_code'] = item
			else:
				new_doc = frappe.new_doc('Item')
				new_doc.naming_series = '.####'
				new_doc.item_name = i['item_name']
				new_doc.item_group = "Equipments"
				new_doc.description = i['item_name']
				new_doc.model = i['model']
				new_doc.is_stock_item = 1
				new_doc.mfg = i['manufacturer']
				new_doc.type = i['type']
				if 'has_serial_no' in i and i['has_serial_no']:
					new_doc.has_serial_no = 1
				new_doc.save(ignore_permissions = True)
				if new_doc.name:
					i['item_code'] = new_doc.name
					if 'has_serial_no' in i and i['has_serial_no'] and i['serial_no']:
						frappe.defaults.set_user_default("warehouse", None)
						sn_doc = frappe.new_doc("Serial No")
						sn_doc.serial_no = i['serial_no']
						sn_doc.item_code = i['item_code']
						sn_doc.save(ignore_permissions = True)
						if sn_doc.name:
							sn_no = sn_doc.name
		d = {
			"Dammam - TSL-SA":"WOD-D.YY.-",
			"Riyadh - TSL-SA":"WOD-R.YY.-",
			"Jeddah - TSL-SA":"WOD-J.YY.-",
			"Kuwait - TSL":"WOD-K.YY.-"
		}
		if frappe.db.get_value("Item",i['item_code'],"has_serial_no") and not i['has_serial_no']:
			frappe.throw("Item {0} in Row -{1} has serial number ".format(i['item_code'],i['idx']))
		
		new_doc = frappe.new_doc("Work Order Data")
		if doc.work_order_data:
			link0 = []
			warr = frappe.db.get_value("Work Order Data",doc.work_order_data,["delivery","warranty"],as_dict = 1)
			print(warr)
			if warr['delivery'] and warr['warranty']:
				date = frappe.utils.add_to_date(warr['delivery'], days=int(warr['warranty']))
				print(date,type(date))
				frappe.db.set_value("Work Order Data",doc.work_order_data,"expiry_date",date)
				frappe.db.set_value("Work Order Data",doc.work_order_data,"returned_date",doc.received_date)
				if (datetime.strptime(doc.received_date, '%Y-%m-%d').date()) <= date:
					frappe.db.set_value("Work Order Data",doc.work_order_data,"status","NER-Need Evaluation Return")
					if not doc.name == "Create Work Order":
						frappe.db.set_value("Work Order Data",doc.work_order_data,"equipment_recieved_form",doc.name)
					link0.append(""" <a href='/app/work-order-data/{0}'>{0}</a> """.format(doc.work_order_data))
					frappe.msgprint("Work Order Updated: "+', '.join(link0))
					return True
				else:
					frappe.throw("Warranty Expired for the Work Order Data - "+str(doc.work_order_data))
			else:
				frappe.throw("No Warranty Period or Delivery Date is Mentioned In work order")
		cc = ""
		if i["no_power"]:
				cc+="No Power,\n"
		if i["no_output"]:
			cc+="No Output,\n"
		if i["no_display"]:
			cc+="No Display,\n"
		if i["no_communication"]:
			cc+="No Communication,\n"
		if i["supply_voltage"]:
			cc+="Supply Voltage,\n"
		if i["touchkeypad_not_working"]:
			cc+="Touch keypad Not Working,\n"
		if i["no_backlight"]:
			cc+="No BackLight,\n"
		if i["error_code"]:
			cc+="Error Code,\n"
		if i["short_circuit"]:
			cc+="Short Circuit,\n"
		if i["overloadovercurrent"]:
			cc+="Overload/Over Current,\n"
		if i["other"]:
			cc+=i["specify"]
		new_doc.complaints = cc
		new_doc.wod_component = i["item_code"] if "item_code" in i else ""
		new_doc.customer = doc.customer
		new_doc.received_date = doc.received_date
		new_doc.sales_rep = doc.sales_person
		new_doc.branch = doc.branch
		new_doc.department = frappe.db.get_value("Cost Center",{"company":doc.company,"is_repair":1})
		new_doc.repair_warehouse = doc.repair_warehouse
		new_doc.address = doc.address
		new_doc.incharge = doc.incharge
		new_doc.naming_series = d[new_doc.branch]
		new_doc.attach_image = (i['attach_image']).replace(" ","%20") if 'attach_image' in i and i['attach_image'] else ""

		# serial_no=""
		# if i['has_serial_no'] and i['serial_no']:
		# 	serial_no = i['serial_no']
		# 	sn_doc = frappe.new_doc("Serial No")
		# 	sn_doc.serial_no = i['serial_no']
		# 	sn_doc.item_code = i['item_code']
		# 	sn_doc.warehouse = ""
		# 	sn_doc.status = "Inactive"
		# 	sn_doc.save(ignore_permissions = True)

		new_doc.append("material_list",{
			"item_code": i['item_code'],
			"item_name":i['item_name'],
			"type":i['type'],
			"model_no":i['model'],
			"mfg":i['manufacturer'],
			"serial_no":sn_no,
			"quantity":i['qty'],
		})

		new_doc.save(ignore_permissions = True)
		if new_doc.name and "attach_image" in i:
			frappe.db.sql('''update `tabFile` set attached_to_name = %s where file_url = %s ''',(new_doc.name,i["attach_image"]))
		new_doc.submit()
		l.append(new_doc.name)
	if l:
		
		frappe.delete_doc("Create Work Order","Create Work Order")
		for j in doc.get('received_equipment'):
			if j['item_code']:
				se_doc = frappe.new_doc("Stock Entry")
				se_doc.stock_entry_type = "Material Receipt"
				se_doc.company = doc.company
				se_doc.branch = doc.branch
				se_doc.to_warehouse = doc.repair_warehouse
				se_doc.append("items",{
					't_warehouse': doc.repair_warehouse,
					'item_code':j['item_code'],
					'item_name':j['item_name'],
					'description':j['item_name'],
					'serial_no':sn_no,
					'qty':j['qty'],
					'uom':frappe.db.get_value("Item",j['item_code'],'stock_uom') or "Nos",
					'conversion_factor':1,
					'allow_zero_valuation_rate':1
				})
				se_doc.save(ignore_permissions = True)
				if se_doc.name:
					# se_doc.submit()
					pass
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
			"item_code": i.item_code,
			"type": i.type,
			"mfg":i.mfg,
			"model_no": i.model_no,
			"serial_no": i.serial_no,
			"qty": i.quantity,
			"sales_rep":doc.sales_rep,
			"customer":doc.customer,
			"incharge":doc.incharge,
			"address" : doc.address,
			"branch":doc.branch

		}))
	return l