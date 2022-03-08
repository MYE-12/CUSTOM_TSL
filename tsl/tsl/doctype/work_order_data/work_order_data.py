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
def get_item_image(erf_no):
	image = frappe.db.sql('''select image from `tabRecieved Equipment Image` where parent = %s order by idx limit 1''',erf_no,as_dict=1)
	if image:
		return image[0]['image']

@frappe.whitelist()
def create_quotation(wod):
	doc = frappe.get_doc("Work Order Data",wod)
	new_doc= frappe.new_doc("Quotation")
	new_doc.company = doc.company
	new_doc.party_name = doc.customer,
	new_doc.party_name = new_doc.party_name[0]
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
	new_doc.sales_rep = doc.sales_rep
	if frappe.db.get_value("Evaluation Report",{"work_order_data":wod},"status"):
		comm = frappe.db.get_value("Evaluation Report",{"work_order_data":wod},"status") 
		if comm == "Others":
			comm = frappe.db.get_value("Evaluation Report",{"work_order_data":wod},"specify")
		new_doc.append("technician_hours_spent",{
			"comments": comm
		})
	return new_doc

@frappe.whitelist()
def create_part_sheet(work_order):
	doc = frappe.get_doc("Work Order Data",work_order)
	new_doc= frappe.new_doc("Part Sheet")
	new_doc.company = doc.company
	new_doc.work_order_data = doc.name
	new_doc.customer = doc.customer
	new_doc.customer_name = doc.customer_name
	new_doc.technician = doc.technician
	new_doc.item = doc.material_list[0].item_name
	new_doc.manufacturer = doc.material_list[0].mfg
	new_doc.model = doc.material_list[0].model_no
	return new_doc

@frappe.whitelist()
def create_evaluation_report(doc_no):
	doc = frappe.get_doc("Work Order Data",doc_no)
	new_doc = frappe.new_doc("Evaluation Report")
	new_doc.company = doc.company
	new_doc.customer = doc.customer
	new_doc.attn = doc.technician
	new_doc.work_order_data = doc.name
	erf_doc = frappe.get_doc("Equipment Received Form",doc.equipment_recieved_form)
	cc =""
	for erf in erf_doc.received_equipment:
		if erf.no_power:
			cc+="No Power,"
		if erf.no_output:
			cc+="No Output,"
		if erf.no_display:
			cc+="No Display,"
		if erf.no_communication:
			cc+="No Communication,"
		if erf.supply_voltage:
			cc+="Supply Voltage,"
		if erf.touchkeypad_not_working:
			cc+="Touch keypad Not Working,"
		if erf.no_backlight:
			cc+="No BackLight,"
		if erf.error_code:
			cc+="Error Code,"
		if erf.short_circuit:
			cc+="Short Circuit,"
		if erf.overloadovercurrent:
			cc+="Overload/Over Current,"
		if erf.other:
			cc+=erf.specify
	new_doc.customer_complaint = cc
	for i in doc.get("material_list"):
		new_doc.append("evaluation_details",{
			"item":i.item_name,
			"description":i.type,
			"manufacturer":i.mfg,
			"model":i.model_no,
			"serial_no":i.serial_no

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
	ps_list = frappe.db.get_list("Part Sheet",{"work_order_data":wod,"parts_availability":"Yes"})
	for i in ps_list:
		ps_doc = frappe.get_doc("Part Sheet",i["name"])
		for j in ps_doc.get("items"):
			new_doc.append("items",{
				"item_code":j.part,
				"item_name":j.part_name,
				"qty":j.qty,
				"uom":"Nos",
				"transfer_qty":j.qty,
				"stock_uom":"Nos",
				"conversion_factor":1,
				"basic_rate":frappe.db.get_value("Bin",{"item_code":j.part},"valuation_rate") or j.price_ea,
				"basic_amount":float(j.qty) * (float(frappe.db.get_value("Bin",{"item_code":j.part},"valuation_rate") or j.price_ea))
			})
	add = 0
	for i in new_doc.get("items"):
		i.basic_amount = i.qty * i.basic_rate
		add += float(i.basic_amount)
	new_doc.total_outgoing_value = add
	new_doc.value_difference = (float(new_doc.total_incoming_value) if new_doc.total_incoming_value  else  0) - new_doc.total_outgoing_value

	return new_doc

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
	for i in doc.get("material_list"):
		qi_details = frappe.db.sql('''select q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where q.workflow_state = "Approved By Customer" and qi.wod_no = %s order by q.creation desc''',wod,as_dict=1)
		new_doc.append("items",{
			"item_name":i.item_name,
			"item_code":"Service Item",
			"manufacturer":i.mfg,
			"model":i.model_no,
			"rate":qi_details[0]['rate'],
			"amount":qi_details[0]['amount'],
			"serial_number":i.serial_no,
			"description":i.type,
			"qty":i.quantity,
			"wod_no":wod,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"cost_center":doc.department

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
	for i in doc.get("material_list"):
		qi_details = frappe.db.sql('''select q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where q.workflow_state = "Approved By Customer" and qi.wod_no = %s order by q.creation desc''',wod,as_dict=1)
		new_doc.append("items",{
			"item_name":i.item_name,
			"item_code":"Service Item",
			"manufacturer":i.mfg,
			"model":i.model_no,
			"serial_number":i.serial_no,
			"description":i.type,
			"qty":i.quantity,
			"rate":qi_details[0]['rate'],
			"amount":qi_details[0]['amount'],
			"wod_no":wod,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"cost_center":doc.department

		})
	return new_doc


@frappe.whitelist()
def create_extra_ps(doc):
	l=[]
	extra_ps = frappe.db.sql('''select name,technician from `tabPart Sheet` where work_order_data = %s order by creation''',doc,as_dict=1)
	for i in range(1,len(extra_ps)):
		l.append(extra_ps[i])
	return l

@frappe.whitelist()
def create_status_duration(wod):
	doc = frappe.get_doc("Work Order Data",wod)
	return(doc.status_duration_details[len(doc.status_duration_details-1)])
	

	
class WorkOrderData(Document):
	def before_save(self):
		print("\n\n\nbef save......")
		# d = {
		# 	"Dammam - TSL-SA":"WOD-D.YY.-",
		# 	"Riyadh - TSL-SA":"WOD-R.YY.-",
		# 	"Jeddah - TSL-SA":"WOD-J.YY.-",
		# 	"Kuwait - TSL":"WOD-K.YY.-"
		# }
		# if self.branch:
		# 	self.naming_series = d[self.branch]
			# frappe.db.set_value("Work Order Data",self.name,"naming_series",d[self.branch])
		now = datetime.now()
		if not self.status_duration_details or self.status != self.status_duration_details[-1].status:
			print("\n\n\n\nbef save if.......")
			self.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
			
	def on_update_after_submit(self):
		print("\n\n\n\n\nduring submit")
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

			# frappe.db.set_value("Status Duration Details",self.status_duration_details[-2].name,"duration",data)
			doc.save(ignore_permissions=True)
		
	def before_submit(self):
		if not self.branch:
			frappe.throw("Assign a Branch to Submit")
		if not self.technician:
			frappe.throw("Assign a Technician to Submit")
		if not self.department:
			frappe.throw("Set Department to Submit")
		self.status = "UE-Under Evaluation"
		
		# current_time = now.strftime("%H:%M:%S")
		# self.status_duration_details =[]
		if self.status != self.status_duration_details[-1].status:
			print("\n\n\nif passes.")
			ldate = self.status_duration_details[-1].date
			now = datetime.now()
			time_date = str(ldate).split(".")[0]
			format_data = "%Y-%m-%d %H:%M:%S"
			date = datetime.strptime(time_date, format_data)
			duration = now - date
			duration_in_s = duration.total_seconds()
			minutes = divmod(duration_in_s, 60)[0]/60
			data = str(minutes).split(".")[0]+"hrs "+str(minutes).split(".")[1][:2]+"min"
			print(data)
			self.status_duration_details[-1].duration = data
			# doc = frappe.get_doc("Work Order Data",self.name)
			self.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
			# doc.save(ignore_permissions=True)
		

	

