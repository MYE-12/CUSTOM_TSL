# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

from codecs import ignore_errors
from hashlib import new
from pydoc import doc
from types import new_class
import frappe
import json
from frappe.model.document import Document
from frappe.utils import getdate,today
from datetime import datetime,date
from frappe.utils.data import (
	add_days,
	add_months,
	add_to_date,
	date_diff,
	flt,
	get_date_str,
	nowdate,
)


@frappe.whitelist()
def get_item_image(erf_no,item):
	image = frappe.db.sql('''select attach_image as image from `tabRecieved Equipment` where parent = %s and item_code = %s and docstatus = 1 ''',(erf_no,item),as_dict=1)
	if image[0]['image']:
		img = image[0]['image'].replace(" ","%20")
		return img

@frappe.whitelist()
def create_quotation(wod):
	doc = frappe.get_doc("Work Order Data",wod)
	new_doc= frappe.new_doc("Quotation")
	new_doc.company = doc.company
	new_doc.party_name = doc.customer
	# new_doc.party_name = new_doc.party_name[0]
	new_doc.department = doc.department
	new_doc.currency = frappe.db.get_value("Company",doc.company,"default_currency")
	new_doc.customer_name = frappe.db.get_value("Customer",doc.customer,"customer_name")
	pay_term = ""
	if frappe.db.get_value("Customer",doc.customer,"advance"):
		pay_term = "Advance"
	elif frappe.db.get_value("Customer",doc.customer,"cash_on_delivery"):
		pay_term = "Cash on Delivery"
	elif frappe.db.get_value("Customer",doc.customer,"credit"):
		pay_term = "Credit"
	new_doc.payment_term = pay_term	
	new_doc.customer_address = frappe.db.get_value("Customer",doc.customer,"customer_primary_address")
	new_doc.address_display = frappe.db.get_value("Customer",doc.customer,"primary_address")
	new_doc.branch_name = doc.branch
	new_doc.quotation_type = "Internal Quotation - Repair"
	if doc.branch:
		d = {
			"Internal Quotation - Repair":{"Kuwait - TSL":"REP-QTN-INT-K.YY.-","Dammam - TSL-SA":"REP-QTN-INT-D.YY.-","Riyadh - TSL-SA":"REP-QTN-INT-R.YY.-","Jeddah - TSL-SA":"REP-QTN-INT-J.YY.-"},
			"Customer Quotation - Repair":{"Kuwait - TSL":"REP-QTN-CUS-K.YY.-","Dammam - TSL-SA":"REP-QTN-CUS-D.YY.-","Riyadh - TSL-SA":"REP-QTN-CUS-R.YY.-","Jeddah - TSL-SA":"REP-QTN-CUS-J.YY.-"},
			"Revised Quotation - Repair":{"Kuwait - TSL":"REP-QTN-REV-K.YY.-","Dammam - TSL-SA":"REP-QTN-REV-D.YY.-","Riyadh - TSL-SA":"REP-QTN-REV-R.YY.-","Jeddah - TSL-SA":"REP-QTN-REV-J.YY.-"},
			"Internal Quotation - Supply":{"Kuwait - TSL":"SUP-QTN-INT-K.YY.-","Dammam - TSL-SA":"SUP-QTN-INT-D.YY.-","Riyadh - TSL-SA":"SUP-QTN-INT-R.YY.-","Jeddah - TSL-SA":"SUP-QTN-INT-J.YY.-"},
			"Customer Quotation - Supply":{"Kuwait - TSL":"SUP-QTN-CUS-K.YY.-","Dammam - TSL-SA":"SUP-QTN-CUS-D.YY.-","Riyadh - TSL-SA":"SUP-QTN-CUS-R.YY.-","Jeddah - TSL-SA":"SUP-QTN-CUS-J.YY.-"},
			"Revised Quotation - Supply":{"Kuwait - TSL":"SUP-QTN-REV-K.YY.-","Dammam - TSL-SA":"SUP-QTN-REV-D.YY.-","Riyadh - TSL-SA":"SUP-QTN-REV-R.YY.-","Jeddah - TSL-SA":"SUP-QTN-REV-J.YY.-"},
			"Site Visit Quotation":{"Kuwait - TSL":"SV-QTN-K.YY.-","Dammam - TSL-SA":"SV-QTN-D.YY.-","Riyadh - TSL-SA":"SV-QTN-R.YY.-","Jeddah - TSL-SA":"SV-QTN-J.YY.-"},
			}
		new_doc.naming_series = d[new_doc.quotation_type][doc.branch]
	
	new_doc.sales_rep = doc.sales_rep
	
	ths = frappe.db.sql('''select status,hours_spent,ratehour from `tabEvaluation Report` where docstatus = 1 and work_order_data = %s order by creation desc limit 1''',wod,as_dict =1)
	if ths:
		total = 0
		if ths[0]["status"] == "Others":
			ths[0]["status"] = frappe.db.get_value("Evaluation Report",{"work_order_data":wod},"specify")
		total = float(ths[0]["hours_spent"]) * float(ths[0]["ratehour"])
		new_doc.append("technician_hours_spent",{
			"comments": ths[0]["status"],
			"total_hours_spent":ths[0]["hours_spent"],
			"value":ths[0]["ratehour"],
			"total_price":total
		})
	return new_doc


@frappe.whitelist()
def create_evaluation_report(doc_no):
	doc = frappe.get_doc("Work Order Data",doc_no)
	new_doc = frappe.new_doc("Evaluation Report")
	new_doc.company = doc.company
	new_doc.customer = doc.customer
	new_doc.attn = doc.sales_rep
	new_doc.work_order_data = doc.name
	new_doc.attach_image = doc.attach_image
	
	if doc.no_power:
		frappe.errprint("no power")
		new_doc.no_power = 1
	if doc.no_output:
		new_doc.no_output = 1
	if doc.no_display:
		new_doc.no_display = 1
	if doc.no_communication:
		new_doc.no_communication = 1
	if doc.supply_voltage:
		new_doc.supply_voltage =1
	if doc.touch_keypad_not_working:
		new_doc.touch_keypad_not_working =1
	if doc.no_backlight:
		new_doc.no_backlight = 1
	if doc.error_code:
		new_doc.error_code =1 
	if doc.short_circuit:
		new_doc.short_circuit = 1
	if doc.overload_overcurrent:
		new_doc.overload_overcurrent = 1
	if doc.others:
		new_doc.others = 1
		new_doc.specify = doc.specify
	new_doc.customer_complaint = doc.complaints
	for i in doc.get("material_list"):
		new_doc.append("evaluation_details",{
			"item":i.item_code,
			"description":i.item_name,
			"manufacturer":i.mfg,
			"model":i.model_no,
			"serial_no":i.serial_no,
			"type":i.type

		})
	new_doc.item_photo = doc.image
	return new_doc

@frappe.whitelist()
def create_stock_entry(wod):
	doc = frappe.get_doc("Work Order Data",wod)
	new_doc = frappe.new_doc("Stock Entry")
	new_doc.work_order_data = doc.name
	new_doc.branch = doc.branch
	new_doc.department = doc.department
	new_doc.stock_entry_type = "Material Transfer"
	ps_list = frappe.db.get_list("Evaluation Report",{"work_order_data":wod,"parts_availability":"Yes"})
	if ps_list:
		for i in ps_list:
			ps_doc = frappe.get_doc("Evaluation Report",i["name"])
			for j in ps_doc.get("items"):
				s_warehouse = ""
				source_bin = frappe.db.sql('''select warehouse from `tabBin` where item_code = %s and actual_qty > 0 order by creation desc limit 1''' ,j.part,as_dict = 1)
				if source_bin:
					for war in source_bin:
						if frappe.db.get_value("Warehouse",{"name":war['warehouse'],"company":doc.company}):
							s_warehouse = war['warehouse']
							break
				new_doc.append("items",{
					"item_code":j.part,
					"item_name":j.part_name,
					"s_warehouse": s_warehouse,
					"t_warehouse":doc.repair_warehouse,
					"qty":j.qty,
					"uom":"Nos",
					"allow_zero_valuation_rate":1,
					"transfer_qty":j.qty,
					"stock_uom":"Nos",
					"conversion_factor":1,
					"basic_rate":frappe.db.get_value("Bin",{"item_code":j.part,"actual_qty":[">","0"]},"valuation_rate") or j.price_ea,
					"basic_amount":float(j.qty) * (float(frappe.db.get_value("Bin",{"item_code":j.part},"valuation_rate") or j.price_ea))
				}
				)
		return new_doc
	else:
		
		for j in doc.get("material_list"):
<<<<<<< HEAD
			new_doc.append("items",{
					"item_code":j.item_code,
					"item_name":j.item_name0 or j.item_name,
					"s_warehouse":frappe.db.sql('''select warehouse from `tabBin` where item_code = %s and actual_qty > 0 order by creation desc limit 1''' ,j.item_code,as_dict = 1)[0]['warehouse'] or "",
					"qty":j.quantity,
					"uom":"Nos",
					"transfer_qty":j.quantity,
					"allow_zero_valuation_rate":1,
					"stock_uom":"Nos",
					"conversion_factor":1,
					"basic_rate":frappe.db.get_value("Bin",{"item_code":j.item_code,"actual_qty":[">","0"]},"valuation_rate") or j.price,
					"basic_amount":float(j.quantity) * (float(frappe.db.get_value("Bin",{"item_code":j.item_code,"actual_qty":[">","0"]},"valuation_rate") or j.price))
				}
				)
	# add = 0
	# for i in new_doc.get("items"):
	# 	i.basic_amount = i.qty * i.basic_rate
	# 	add += float(i.basic_amount)
	# new_doc.total_outgoing_value = add
	# new_doc.value_difference = (float(new_doc.total_incoming_value) if new_doc.total_incoming_value  else  0) - new_doc.total_outgoing_value
=======
			source_warehouse = frappe.db.sql('''select warehouse from `tabBin` where item_code = %s and actual_qty > 0 order by creation desc limit 1''' ,j.item_code,as_dict = 1)
			if len(source_warehouse) and 'warehouse' in source_warehouse[0] :
				if not doc.repair_warehouse == source_warehouse[0]['warehouse']:
					source_warehouse = source_warehouse[0]['warehouse']
					new_doc.append("items",{
							"item_code":j.item_code,
							"item_name":j.item_name0 or j.item_name,
							"s_warehouse":source_warehouse ,
							"qty":j.quantity,
							"uom":"Nos",
							"transfer_qty":j.quantity,
							"allow_zero_valuation_rate":1,
							"stock_uom":"Nos",
							"conversion_factor":1,
							"basic_rate":frappe.db.get_value("Bin",{"item_code":j.item_code,"actual_qty":[">","0"]},"valuation_rate") or j.price,
							"basic_amount":float(j.quantity) * (float(frappe.db.get_value("Bin",{"item_code":j.item_code,"actual_qty":[">","0"]},"valuation_rate") or j.price))
						}
						)
		if len(new_doc.items) > 1:
			return new_doc
		frappe.throw("No Spare parts available for this Work Order")
				
>>>>>>> 1a48180aece979c78eef4fc50f1af5c9e1201c56


@frappe.whitelist()
def create_sof(wod):
	doc = frappe.get_doc("Work Order Data",wod)
	new_doc = frappe.new_doc("Supply Order Form")
	new_doc.company = doc.company
	new_doc.customer = doc.customer
	new_doc.branch = doc.branch
	new_doc.address = frappe.db.get_value("Equipment Received Form",doc.equipment_recieved_form,"address")
	new_doc.incharge = frappe.db.get_value("Equipment Received Form",doc.equipment_recieved_form,"incharge")
	new_doc.sales_person = doc.sales_rep
	new_doc.work_order_data = wod
	for i in doc.get("material_list"):
		new_doc.append("received_equipment",{
			"item_name":i.item_name,
			"type":i.type,
			"manufacturer":i.mfg,
			"model":i.model_no,
			"serial_no":i.serial_no,
			"qty":i.quantity

		})
	return new_doc

@frappe.whitelist()
def create_sal_inv(wod):
	doc = frappe.get_doc("Work Order Data",wod)
	new_doc = frappe.new_doc("Sales Invoice")
	new_doc.company = doc.company
	new_doc.customer = doc.customer
	new_doc.branch = doc.branch
	new_doc.department = doc.department
	new_doc.customer_address = frappe.db.get_value("Equipment Received Form",doc.equipment_recieved_form,"address")
	new_doc.contact_person = frappe.db.get_value("Equipment Received Form",doc.equipment_recieved_form,"incharge")
	new_doc.work_order_data = wod
	d = {}
	d['Kuwait - TSL'] = "Kuwait Repair - TSL"
	d['Dammam - TSL-SA'] = 'Repair - Dammam - TSL-SA'
	d['Jeddah - TSL-SA'] = 'Repair - Jeddah - TSL-SA'
	d['Riyadh - TSL-SA'] = 'Repair - Riyadh - TSL-SA'
	for i in doc.get("material_list"):
		qi_details = frappe.db.sql('''select q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where q.workflow_state = "Approved By Customer" and qi.wod_no = %s order by q.creation desc''',wod,as_dict=1)
		r = 0
		amt = 0
		if qi_details:
			r = qi_details[0]['rate']
			amt = qi_details[0]['amount']
		new_doc.append("items",{
			"item_name":i.item_name0,
			"item_code":i.item_code,
			"manufacturer":i.mfg,
			"model":i.model_no,
			"rate":r,
			"amount":amt, 
			"type":i.type,
			"serial_number":i.serial_no,
			"description":i.item_name,
			"qty":i.quantity,
			"work_order_data":wod, 
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"cost_center":doc.department,
			"income_account":"6001002 - Revenue from Service - TSL",
			"warehouse":d[doc.branch]

		})
	return new_doc

@frappe.whitelist()
def create_dn(wod):
	doc = frappe.get_doc("Work Order Data",wod)
	new_doc = frappe.new_doc("Delivery Note")
	new_doc.company = doc.company
	new_doc.customer = doc.customer
	new_doc.branch = doc.branch
	new_doc.department = doc.department
	new_doc.customer_address = frappe.db.get_value("Equipment Received Form",doc.equipment_recieved_form,"address")
	new_doc.contact_person = frappe.db.get_value("Equipment Received Form",doc.equipment_recieved_form,"incharge")
	new_doc.work_order_data = wod
	d = {}
	d['Kuwait - TSL'] = "Repair - Kuwait - TSL"
	d['Dammam - TS'] = 'Repair - Dammam - TSL-SA'
	d['Jeddah - TS'] = 'Repair - Jeddah - TSL-SA'
	d['Riyadh - TS'] = 'Repair - Riyadh - TSL-SA'
	for i in doc.get("material_list"):
		qi_details = frappe.db.sql('''select q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where q.workflow_state = "Approved By Customer" and qi.wod_no = %s order by q.creation desc''',wod,as_dict=1)
		r = 0
		amt = 0
		if qi_details:
			r = qi_details[0]['rate']
			amt = qi_details[0]['amount']
		new_doc.append("items",{
			"item_name":i.item_name0,
			"item_code":i.item_code,
			"manufacturer":i.mfg,
			"model":i.model_no,
			"serial_number":i.serial_no,
			"description":i.item_name,
			'type':i.type,
			"qty":i.quantity,
			"rate":r,
			"amount":amt,
			"work_order_data":wod,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"cost_center":doc.department,
			"warehouse":d[doc.branch]

		})
	return new_doc


@frappe.whitelist()
def create_extra_ps(doc):
	l=[]
	extra_ps = frappe.db.sql('''select name,technician from `tabEvaluation Report` where work_order_data = %s order by creation''',doc,as_dict=1)
	for i in range(1,len(extra_ps)):
		l.append(extra_ps[i])
	return l

@frappe.whitelist()
def create_status_duration(wod):
	doc = frappe.get_doc("Work Order Data",wod)
	return(doc.status_duration_details[len(doc.status_duration_details-1)])
	

	
class WorkOrderData(Document):
	def before_save(self):
		pass
		# now = datetime.now()
		# if not self.status_duration_details or self.status != self.status_duration_details[-1].status:
		# 	self.append("status_duration_details",{
		# 		"status":self.status,
		# 		"date":now,
		# 	})
			
	def on_update_after_submit(self):
		if self.technician and self.status == "NE-Need Evaluation":
			self.status = "UE-Under Evaluation"
		if self.warranty and self.delivery:
			date = frappe.utils.add_to_date(self.delivery, days=int(self.warranty))
			frappe.db.set_value(self.doctype,self.name,"expiry_date",date)
		if self.status != self.status_duration_details[-1].status:
			ldate = self.status_duration_details[-1].date
			now = datetime.now()
			time_date = str(ldate).split(".")[0]
			format_data = "%Y-%m-%d %H:%M:%S"
			date = datetime.strptime(time_date, format_data)
			duration = now - date
			duration_in_s = duration.total_seconds()
			minutes = divmod(duration_in_s, 60)[0]/60
			data = str(minutes).split(".")[0]+"hrs "+str(minutes).split(".")[1][:2]+"min"
			frappe.db.set_value("Status Duration Details",self.status_duration_details[-1].name,"duration",data)
			doc = frappe.get_doc("Work Order Data",self.name)
			doc.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
			# doc.save(ignore_permissions=True)
		
	def before_submit(self):

		self.status = "NE-Need Evaluation"
		now = datetime.now()
		self.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
		# if not self.branch:
		# 	frappe.throw("Assign a Branch to Submit")
		# if not self.technician:
		# 	frappe.throw("Assign a Technician to Submit")
		# if not self.department:
		# 	frappe.throw("Set Department to Submit")
		# self.status = "UE-Under Evaluation"
		
		# current_time = now.strftime("%H:%M:%S")
		# self.status_duration_details =[]
		
		if self.status != self.status_duration_details[-1].status:
			ldate = self.status_duration_details[-1].date
			now = datetime.now()
			time_date = str(ldate).split(".")[0]
			format_data = "%Y-%m-%d %H:%M:%S"
			date = datetime.strptime(time_date, format_data)
			duration = now - date
			duration_in_s = duration.total_seconds()
			minutes = divmod(duration_in_s, 60)[0]/60
			data = str(minutes).split(".")[0]+"hrs "+str(minutes).split(".")[1][:2]+"min"
			self.status_duration_details[-1].duration = data
			# doc = frappe.get_doc("Work Order Data",self.name)
			self.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
			# doc.save(ignore_permissions=True)
		

	

