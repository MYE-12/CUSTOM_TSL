# Copyright (c) 2022, Tsl and contributors
# For license information, please see license.txt

from unicodedata import category
import frappe
#from typing_extensions import Self
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
def create_sal_inv(sod):
	doc = frappe.get_doc("Supply Order Data",sod)
	new_doc = frappe.new_doc("Sales Invoice")
	new_doc.company = doc.company
	new_doc.customer = doc.customer
	new_doc.branch = doc.branch
	new_doc.department = doc.department
	new_doc.supply_order_data = sod
	new_doc.currency = frappe.db.get_value("Company",doc.company,"default_currency")
	new_doc.cost_center = doc.department
	
	d = {}
	d['Kuwait - TSL'] = "Kuwait Repair - TSL"
	d['Dammam - TSL-SA'] = 'Repair - Dammam - TSL-SA'
	d['Jeddah - TSL-SA'] = 'Repair - Jeddah - TSL-SA'
	d['Riyadh - TSL-SA'] = 'Repair - Riyadh - TSL-SA'
	
	for i in doc.get("material_list"):
		qi_details = frappe.db.sql('''select q.valid_till as valid_till,q.discount_amount as discount,q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where qi.item_code = %s and q.workflow_state = "Approved By Customer" and qi.supply_order_data = %s and q.docstatus = 1 order by q.modified desc limit 1''',(i.item_code,sod),as_dict=1)
		r = 0
		amt = 0
		qty = i.quantity
		if qi_details:
			r = qi_details[0]['rate']
			amt = qi_details[0]['amount']
			qty = qi_details[0]['qty']
			new_doc.due_date = qi_details[0]['valid_till']
			new_doc.discount_amount = qi_details[0]['discount']
		new_doc.append("items",{
			"item_name":i.item_name,
			"item_code":i.item_code,
			"manufacturer":i.mfg,
			"model":i.model_no,
			"rate":r,
			"amount":amt, 
			"type":i.type,
			"serial_number":i.serial_no,
			"description":i.item_name,
			"qty":qty,
			"supply_order_data":sod,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"cost_center":doc.department,
			"income_account":"",
			"warehouse":doc.branch,
			"branch":doc.branch

		})
	for i in doc.get('in_stock'):
		qi_details = frappe.db.sql('''select q.valid_till as valid_till,q.discount_amount as discount,q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where qi.item_code = %s and q.workflow_state = "Approved By Customer" and q.docstatus = 1 and qi.supply_order_data = %s order by q.modified desc limit 1''',(i.part,sod),as_dict=1)
		r = 0
		amt = 0
		qty = i.qty
		if qi_details:
			r = qi_details[0]['rate']
			amt = qi_details[0]['amount']
			qty = qi_details[0]['qty']
			new_doc.due_date = qi_details[0]['valid_till']
			new_doc.overall_discount_amount = qi_details[0]['discount']
		new_doc.append("items",{
			"item_name":i.part_name,
			"item_code":i.part,
			"manufacturer":i.manufacturer,
			"model":i.model,
			"rate":r,
			"amount":amt, 
			"type":i.type,
			"serial_number":i.serial_no,
			"description":i.part_name,
			"qty":qty,
			"supply_order_data":sod,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"cost_center":doc.department,
			"income_account":"",
			"warehouse":doc.branch,
			"branch":doc.branch

		})

	return new_doc

@frappe.whitelist()
def create_dn(sod):
	doc = frappe.get_doc("Supply Order Data",sod)
	new_doc = frappe.new_doc("Delivery Note")
	new_doc.company = doc.company
	new_doc.customer = doc.customer
	new_doc.branch = doc.branch
	new_doc.department = doc.department
	new_doc.cost_center = doc.department
	new_doc.supply_order_data = doc.name
	new_doc.currency = frappe.db.get_value("Company",doc.company,"default_currency")
	
	
	for i in doc.get("material_list"):
		qi_details = frappe.db.sql('''select q.valid_till as valid_till,q.discount_amount as discount,q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where qi.item_code = %s and q.workflow_state = "Approved By Customer" and qi.supply_order_data = %s and q.docstatus = 1 order by q.modified desc limit 1''',(i.item_code,sod),as_dict=1)
		r = 0
		amt = 0
		qty = i.quantity
		if qi_details:
			r = qi_details[0]['rate']
			amt = qi_details[0]['amount']
			qty = qi_details[0]['qty']
			new_doc.due_date = qi_details[0]['valid_till']
			new_doc.discount_amount = qi_details[0]['discount']
		new_doc.append("items",{
			"item_name":i.item_name,
			"item_code":i.item_code,
			"manufacturer":i.mfg,
			"model":i.model_no,
			"rate":r,
			"amount":amt, 
			"type":i.type,
			"serial_number":i.serial_no,
			"description":i.item_name,
			"qty":qty,
			"supply_order_data":sod,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"cost_center":doc.department,
			"income_account":"",
			"warehouse":doc.branch,
			"branch":doc.branch

		})
	for i in doc.get('in_stock'):
		qi_details = frappe.db.sql('''select q.valid_till as valid_till,q.discount_amount as discount,q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where qi.item_code = %s and q.workflow_state = "Approved By Customer" and q.docstatus = 1 and qi.supply_order_data = %s order by q.modified desc limit 1''',(i.part,sod),as_dict=1)
		r = 0
		amt = 0
		qty = i.qty
		if qi_details:
			r = qi_details[0]['rate']
			amt = qi_details[0]['amount']
			qty = qi_details[0]['qty']
			new_doc.due_date = qi_details[0]['valid_till']
			new_doc.overall_discount_amount = qi_details[0]['discount']
		new_doc.append("items",{
			"item_name":i.part_name,
			"item_code":i.part,
			"manufacturer":i.manufacturer,
			"model":i.model,
			"rate":r,
			"amount":amt, 
			"type":i.type,
			"serial_number":i.serial_no,
			"description":i.part_name,
			"qty":qty,
			"supply_order_data":sod,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"cost_center":doc.department,
			"income_account":"",
			"warehouse":doc.branch,
			"branch":doc.branch

		})

	return new_doc

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
	for i in doc.get("in_stock"):
		if i.parts_availability == "No":
			new_doc.append("items",{
				"item_code":i.part,
				"item_name":i.part_name,
				"description":i.part_name,
				"type":i.type,
				"model":i.model,
				"mfg":i.manufacturer,
				"serial_no":i.serial_no,
				"category":i.category,
				"sub_category":i.sub_category,
				"uom":"Nos",
				"stock_uom":"Nos",
				"conversion_factor":1,
				"schedule_date":sched_date,
				"stock_qty":1,
				"warehouse":doc.branch,
				"qty":i.qty,
				"item_group":"Components",
				"supply_order_data":doc.name,
				"branch":doc.branch,
				"department":doc.department
			})
	for i in doc.get("material_list"):
		new_doc.append("items",{
			"item_code":i.item_code,
			"item_name":i.item_name,
			"description":i.item_name,
			"type":i.type,
			"model":i.model_no,
			"mfg":i.mfg,
			"serial_no":i.serial_no,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"schedule_date":sched_date,
			"stock_qty":1,
			"warehouse":doc.branch,
			"qty":i.quantity,
			"supply_order_data":doc.name,
			"branch":doc.branch,
			"department":doc.department,
			"item_group":"Equipments"
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
	new_doc.department = doc.department
	new_doc.currency = frappe.db.get_value("Company",doc.company,"default_currency")
	new_doc.quotation_type = "Internal Quotation - Supply"
	new_doc.sales_rep = doc.sales_rep
	new_doc.ignore_pricing_rule = 1
	# for i in doc.get("in_stock"):
	# 	new_doc.append("items",{
	# 		"supply_order_data":sod,
	# 		"item_code":i.part,
	# 		"item_name":i.part_name,
	# 		"description":i.part_name,
	# 		'model_no':i.model,
	# 		"type":i.type,
	# 		"manufacturer":i.manufacturer,
	# 		"serial_no":i.serial_no,
	# 		"qty":i.qty,
	# 		"schedule_date":add_to_date(nowdate(),3),
	# 		"price_list_rate":i.price_ea,
	# 		"rate":i.price_ea,
	# 		"amount":i.total,
	# 		"uom":"Nos",
	# 		"stock_uom":"Nos"
	# 	})
	# tot = 0
	# extra_charges = frappe.db.sql('''select name,freight_charges,custom_clearance,payment_commission,max_freight_duration,max_custom_duration from `tabSupplier Quotation` where supply_order_data = %s and workflow_state = "Approved" and docstatus = 1''',sod,as_dict = 1)
	# if extra_charges:
	# 	new_doc.supplier_quotation = extra_charges[0]['name']
	# 	new_doc.freight_charges = extra_charges[0]['freight_charges']
	# 	tot += float(extra_charges[0]['freight_charges'])
	# 	new_doc.custom_clearance = extra_charges[0]['custom_clearance']
	# 	tot += float(extra_charges[0]['custom_clearance'])
	# 	new_doc.payment_commission = extra_charges[0]['payment_commission']
	# 	tot += float(extra_charges[0]['payment_commission'])
	# 	new_doc.max_freight_duration = extra_charges[0]['max_freight_duration']
	# 	new_doc.max_custom_duration = extra_charges[0]['max_custom_duration']
	# 	new_doc.discount_amount = tot * -1
	return new_doc
@frappe.whitelist()
def make_payment(sod,invoice):
	new_doc = frappe.new_doc("Payment Entry")
	doc = frappe.get_doc("Supply Order Data",sod)
	new_doc.payment_type = "Receive"
	new_doc.company = doc.company
	new_doc.branch = doc.branch
	new_doc.cost_center = doc.department
	new_doc.supply_order_data = sod
	new_doc.paid_from = frappe.db.get_value("Account",{"account_type":["in",["Receivable"]],"is_group":0,"company":doc.company})
	new_doc.paid_from_account_currency = frappe.db.get_value("Company",doc.company,"default_currency")
	new_doc.party_type = "Customer"
	new_doc.party = doc.customer
	new_doc.party_name = doc.customer_name
	new_doc.cost_center = doc.department
	new_doc.append("references",
	{
		"reference_doctype":"Sales Invoice",
		"reference_name":invoice,
		"total_amount":frappe.db.get_value("Sales Invoice",invoice,"grand_total"),
		"outstanding_amount":frappe.db.get_value("Sales Invoice",invoice,"outstanding_amount"),
		"allocated_amount":frappe.db.get_value("Sales Invoice",invoice,"grand_total")
	})
	return new_doc

class SupplyOrderData(Document):
	def on_update_after_submit(self):
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
	
	def before_save(self):
		self.previously_quoted =[]
		for i in self.get('in_stock'):
			if i.part:
				i.parts_availability = 'No'
				invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
				if frappe.db.get_value("Bin",{"item_code":i.part,"warehouse":["in",invent],'actual_qty':['>=',i.qty]},"name"):
					if frappe.db.get_value('Bin',{'item_code':i.part,'actual_qty':['>=',i.qty]}):
						i.parts_availability = 'Yes'
						i.price_ea = frappe.db.get_value('Bin',{'item_code':i.part},'valuation_rate')
						i.total = i.qty * i.price_ea
				suqb = frappe.db.sql('''select q.party_name as customer,qi.parent as quotation_no,qi.wod_no as work_order_data,qi.supply_order_data as supply_order_data ,qi.rate as quoted_price,qi.item_code as sku,qi.model_no as model,qi.type as type,qi.manufacturer as mfg from `tabQuotation` as q inner join `tabQuotation Item` as qi on qi.parent=q.name where qi.item_code = %s and q.workflow_state = "Approved By Customer" and q.docstatus = 1 ''',i.part,as_dict =1 )
				if suqb:
					for j in suqb:
						self.append("previously_quoted",j)
		for i in self.get("material_list"):
			if i.item_code:
				suqb = frappe.db.sql('''select q.party_name as customer,qi.parent as quotation_no,qi.wod_no as work_order_data,qi.supply_order_data as supply_order_data ,qi.rate as quoted_price,qi.item_code as sku,qi.model_no as model,qi.type as type,qi.manufacturer as mfg from `tabQuotation` as q inner join `tabQuotation Item` as qi on qi.parent=q.name where qi.item_code = %s and q.workflow_state = "Approved By Customer" and q.docstatus = 1 ''',i.item_code,as_dict =1 )
				if suqb:
					for j in suqb:
						self.append("previously_quoted",j)
		
