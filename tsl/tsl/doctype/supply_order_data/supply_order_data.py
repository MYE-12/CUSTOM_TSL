# Copyright (c) 2022, Tsl and contributors
# For license information, please see license.txt

import frappe
from typing_extensions import Self
from frappe.model.document import Document
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
def create_rfq(sod):
	doc = frappe.get_doc("Supply Order Data",sod)
	new_doc = frappe.new_doc("Request for Quotation")
	new_doc.company = doc.company
	new_doc.branch = doc.branch
	new_doc.supply_order_data = sod
	new_doc.department = doc.department
	new_doc.items=[]
	sched_date = add_to_date(nowdate(),3)
	print(sched_date)
	for i in doc.get("in_stock"):
		if i.parts_availability == "No":
			new_doc.append("items",{
				"item_code":i.part,
				"item_name":i.part_name,
				"description":i.type,
				"uom":"Nos",
				"stock_uom":"Nos",
				"conversion_factor":1,
				"schedule_date":sched_date,
				"stock_qty":1,
				"warehouse":"All Warehouses - TSL",
				"qty":i.qty
			})
	for i in doc.get("material_list"):
		new_doc.append("items",{
				"item_code":"Service Item",
				"item_name":i.item_name,
				"description":"Type: "+str(i.type)+", Model: "+str(i.model_no)+" , Serial No: "+str(i.serial_no),
				"uom":"Nos",
				"stock_uom":"Nos",
				"schedule_date":sched_date,
				"conversion_factor":1,
				"warehouse":"All Warehouses - TSL",
				"stock_qty":1,
				"qty":i.quantity
			})
	return new_doc

@frappe.whitelist()
def create_quotation(sod):
	doc = frappe.get_doc("Supply Order Data",sod)
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
	new_doc.quotation_type = "Internal Quotation - Supply"
	new_doc.sales_rep = doc.sales_rep
	new_doc.ignore_pricing_rule = 1
	for i in doc.get("in_stock"):
		new_doc.append("items",{
			"supply_order_data":sod,
			"item_code":i.part,
			"item_name":i.part_name,
			"description":i.type,
			"qty":i.qty,
			"schedule_date":add_to_date(nowdate,3),
			"price_list_rate":i.price_ea,
			"rate":i.price_ea,
			"amount":i.total,
			"uom":"Nos",
			"stock_uom":"Nos"
		})
	for i in doc.get("material_list"):
		new_doc.append("items",{
			"supply_order_data":sod,
			"item_code":"Service Item",
			"item_name":i.item_name,
			"model_no":i.model_no,
			"serial_no":i.serial_no,
			"description":i.type,
			"qty":i.quantity,
			"schedule_date":add_to_date(nowdate,3),
			"price_list_rate":i.price,
			"rate":i.price,
			"amount":i.amount,
			"uom":"Nos",
			"stock_uom":"Nos"
		})
	tot = 0
	extra_charges = frappe.db.sql('''select name,freight_charges,custom_clearance,payment_commission,max_freight_duration,max_custom_duration from `tabSupplier Quotation` where supply_order_data = %s and workflow_state = "Approved" and docstatus = 1''',sod,as_dict = 1)
	if extra_charges:
		new_doc.supplier_quotation = extra_charges[0]['name']
		new_doc.freight_charges = extra_charges[0]['freight_charges']
		tot += float(extra_charges[0]['freight_charges'])
		new_doc.custom_clearance = extra_charges[0]['custom_clearance']
		tot += float(extra_charges[0]['custom_clearance'])
		new_doc.payment_commission = extra_charges[0]['payment_commission']
		tot += float(extra_charges[0]['payment_commission'])
		new_doc.max_freight_duration = extra_charges[0]['max_freight_duration']
		new_doc.max_custom_duration = extra_charges[0]['max_custom_duration']
		new_doc.discount_amount = tot * -1
	return new_doc


class SupplyOrderData(Document):
	def on_update_after_submit(self):
		print("\n\n\n\n\nduring submit")
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
			doc = frappe.get_doc("Supply Order Data",self.name)
			doc.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
			doc.save(ignore_permissions=True)

	def before_submit(self):
		if not self.branch:
				frappe.throw("Assign a Branch to Submit")
		if not self.department:
			frappe.throw("Set Department to Submit")
		now = datetime.now()
		self.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
	
