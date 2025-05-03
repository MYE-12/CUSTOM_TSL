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
			"description":i.description,
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
def create_sal_inv_tender(sod):
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
		qi_details = frappe.db.sql('''select q.grand_total,q.valid_till as valid_till,q.discount_amount as discount,q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where qi.item_code = %s and q.workflow_state = "Awarded" and qi.supply_order_data = %s and q.docstatus = 1 order by q.modified desc limit 1''',(i.item_code,sod),as_dict=1)
		r = 0
		amt = 0
		qty = i.quantity
		if qi_details:
			
			r = qi_details[0]['rate']
			frappe.errprint(r)
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
		qi_details = frappe.db.sql('''select q.grand_total,q.valid_till as valid_till,q.discount_amount as discount,q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where qi.item_code = %s and q.workflow_state = "Awarded" and q.docstatus = 1 and qi.supply_order_data = %s order by q.modified desc limit 1''',(i.part,sod),as_dict=1)
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
	new_doc.purchase_order_no = doc.po_number
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
			"description":i.description,
			"qty":qty,
			"supply_order_data":sod,
			# "uom":"Nos",
			# "stock_uom":"Nos",
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
	if doc.company == "TSL COMPANY - KSA":
		new_doc.naming_series = "RFQ-SA-.YY.-"
	warehouse = new_doc.branch
	if new_doc.branch == "Dammam - TSL-SA":
		warehouse = "Dammam - TSL - KSA"
	if new_doc.branch == "Jeddah - TSL-SA":
		warehouse = "Jeddah - TSL - KSA"
	if new_doc.branch == "Riyadh - TSL- KSA":
		warehouse = "Riyadh - TSL - KSA"
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
				"warehouse":warehouse,
				"qty":i.qty,
				"item_group":"Components",
				"supply_order_data":doc.name,
				"branch":doc.branch,
				"department":doc.department
			})
	for i in doc.get("material_list"):
		new_doc.append("items",{
			"item_code":i.item_code,
			# "model":i.item_name,
			"item_name":i.item_name,
			"description":i.description,
			"type":i.type,
			"model":i.model_no,
			"mfg":i.mfg,
			"serial_no":i.serial_no,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"schedule_date":sched_date,
			"stock_qty":1,
			"warehouse":warehouse,
			"qty":i.quantity,
			"supply_order_data":doc.name,
			"branch":doc.branch,
			"department":doc.department,
			"item_group":"Equipments"
		})
	return new_doc


@frappe.whitelist()
def create_sq(sod):
	doc = frappe.get_doc("Supply Order Data",sod)
	new_doc= frappe.new_doc("Supplier Quotation")
	new_doc.company = doc.company
	new_doc.branch = doc.branch
	new_doc.supply_order_data = sod
	new_doc.department = doc.department
	new_doc.st = doc.st or 0
	new_doc.items=[]
	for i in doc.get("material_list"):
		new_doc.append("items",{
			"item_code":i.item_code,
			# "model":i.item_name,
			"item_name":i.item_name,
			"description":i.description,
			"type":i.type,
			"model":i.model_no,
			"mfg":i.mfg,
			"serial_no":i.serial_no,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			# "schedule_date":sched_date,
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
	new_doc.plant = doc.plant
	new_doc.party_name = doc.customer
	new_doc.purchase_order_no = doc.po_number
	new_doc.supplier_name = doc.supplier_name
	new_doc.supply_tender_no = doc.name
	new_doc.customer_reference_number = doc.customer_reference_number
	# new_doc.party_name = new_doc.party_name
	new_doc.customer_name = frappe.db.get_value("Customer",doc.customer,"customer_name")
	pay_term = ""
	if frappe.db.get_value("Customer",doc.customer,"advance"):
		pay_term = "Advance"
	elif frappe.db.get_value("Customer",doc.customer,"cash_on_delivery"):
		pay_term = "Cash on Delivery"
	elif frappe.db.get_value("Customer",doc.customer,"credit"):
		pay_term = "Credit"
	new_doc.payment_term = pay_term	
	new_doc.customer_address = frappe.db.get_value("Customer",doc.customer,"customer_primary_address") or doc.address
	new_doc.address_display = frappe.db.get_value("Customer",doc.customer,"primary_address")
	new_doc.branch_name = doc.branch
	new_doc.department = doc.department
	new_doc.currency = frappe.db.get_value("Company",doc.company,"default_currency")
	if doc.department == "Supply Tender - TSL":
		new_doc.quotation_type = "Quotation - Supply Tender"
		new_doc.custom_department = "Supply Tender - TSL"
		new_doc.naming_series = "ST-Q-.YY.-"
	# else:
	# 	if doc.st == 1:
	# 		new_doc.quotation_type = "Customer Quotation - Supply"
	# 		new_doc.st = doc.st
	else:
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
		if self.material_list:
			for i in self.material_list:
				item = frappe.get_doc("Item",i.item_code)
				item.set("online_price_table", [])
				for j in self.price_list:
					item.append("online_price_table",{
					"item_code":j.item_code,
					"price_type":j.price_type,
					"price":j.price,
					"website":j.website,
					"comments":j.comments
					

					})
				item.save(ignore_permissions = 1)
				# item.online_price = i.online_price

				# item.save(ignore_permissions = 1)

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
					self.previously_quoted = []
					for j in suqb:
						self.append("previously_quoted",j)
		if not self.project:
			for i in self.get("material_list"):
				if i.item_code:
					suqb = frappe.db.sql('''select q.party_name as customer,qi.parent as quotation_no,qi.wod_no as work_order_data,qi.supply_order_data as supply_order_data ,qi.rate as quoted_price,qi.item_code as sku,qi.model_no as model,qi.type as type,qi.manufacturer as mfg from `tabQuotation` as q inner join `tabQuotation Item` as qi on qi.parent=q.name where qi.item_code = %s and q.workflow_state = "Approved By Customer" and q.docstatus = 1 ''',i.item_code,as_dict =1 )
					if suqb:
						for j in suqb:
							self.append("previously_quoted",j)
		

@frappe.whitelist()
def supply_order_mail(name):
	supply_order = frappe.get_doc('Supply Order Data',name)
	if supply_order.branch == "Jeddah - TSL-SA":
		msg1 = """Dear Purchaser, <br> <br>Please find the Supply Order Create (<a href="https://erp.tsl-me.com/app/supply-order-data/%s">%s</a>) need price for further proceeding.<br> 
				<br><br> Thanks & Regards"""%(supply_order.name,supply_order.name)

		msg2 = """<div><style>.sh-src a{text-decoration:none!important;}</style></div> <br> <table cellpadding="0" cellspacing="0" border="0" class="sh-src" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td align="center" style="padding: 0px 18px 0px 0px; vertical-align: top;">
			<table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 13px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/file/5r1rjllxn0zdme" alt="" title="Profile Picture" width="100" height="100" class="" style="display: block; border: 0px; max-width: 100px;"></p></td></tr></table> <table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://tsl-me.com/" target="_blank"><img src="https://signaturehound.com/api/v1/file/137twgllxltmdmv" alt="" title="Logo" width="150" height="50" style="display: block; border: 0px; max-width: 150px;"></a></p></td></tr></table></td> <td width="5" style="padding: 1px 0px 0px;"></td> <td style="padding: 0px 1px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 10px 0px; border-bottom: 2px solid rgb(0,92,163); font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap;"><p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; font-weight: 700; color: rgb(0,92,163); white-space: nowrap; margin: 1px;">Ajai
			</p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">Admin &amp; Customer Support</p> <!----> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">
				TSL Group | KSA - Jeddah</p> <!----></td></tr> <tr><td style="padding: 10px 1px 10px 0px; border-bottom: 2px solid rgb(0,92,163);"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/email/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; margin: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="mailto:info-jed@tsl-me.com" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">info-jed@tsl-me.com</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/mobile/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; margin: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="tel:+966558803522" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">+966 55 880 3522</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/map/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; margin: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://www.google.com/maps/dir/21.3180818,39.227158/TSL+Industrial+Electronics+for+Repairing+%26+Supply+-+Jeddah,+80th+street%D8%8C+Al-Qarinia+District%D8%8C+Jeddah+22535,+Saudi+Arabia%E2%80%AD/@21.3172514,39.1901511,13z/data=!3m1!4b1!4m9!4m8!1m1!4e1!1m5" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">80th Street, Al-Qrainia, Jeddah, Saudi Arabia.</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/website/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; margin: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,162) !important; font-weight: 700; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://tsl-me.com/" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,163); font-weight: 700; text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,163); font-weight: 700; text-decoration: none !important;">tsl-me.com</span></a></p></td></tr></table></td></tr> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.linkedin.com/company/tsl-me/mycompany/" target="_blank"><img src="https://signaturehound.com/api/v1/png/linkedin/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://x.com/tsl_mecompany?s=11&amp;t=Zxza0-9Q_18nsDCddfTQPw" target="_blank"><img src="https://signaturehound.com/api/v1/png/x/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.instagram.com/tslcom/?igshid=MzRlODBiNWFlZA%3D%3D" target="_blank"><img src="https://signaturehound.com/api/v1/png/instagram/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.facebook.com/people/TSL-Industrial-Electronics-Services/61550277093129/" target="_blank"><img src="https://signaturehound.com/api/v1/png/facebook/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.youtube.com/@TSLELECTRONICSSERVICES" target="_blank"><img src="https://signaturehound.com/api/v1/png/youtube/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td>
				</tr></table></td></tr></table></td></tr></table></td></tr> <!----> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: 0px; border-collapse: collapse;"><tr><td style="padding: 15px 1px 0px 0px; font-family: Arial, sans-serif; font-size: 10px; line-height: 12px; color: rgb(136,136,136);"><p style="font-family: Arial, sans-serif; font-size: 10px; line-height: 12px; color: rgb(136,136,136); margin: 1px;">The content of this email is confidential and intended for the recipient specified in message only. It is strictly forbidden to share any part of this message with any third party, without a written consent of the sender. If you received this message by mistake, please reply to this message and follow with its deletion, so that we can ensure such a mistake does not occur in the future.</p></td></tr></table></td></tr> """
				
		# technician = supply_order.technician
		frappe.sendmail(
				recipients="purchase-sa@tsl-me.com",
				sender="info-jed@tsl-me.com",
				subject= "New Supply Order Created Needed Price",
				message=msg1+msg2,
				attachments=get_attachments(supply_order.name,"Supply Order Data")
		)
		frappe.msgprint("Mail Sent on Parts Request")
	else:
		if supply_order.branch == "Dammam - TSL-SA":

			msg1 = """Dear Purchaser, <br> <br>Please find the Supply Order Create (<a href="https://erp.tsl-me.com/app/supply-order-data/%s">%s</a>) need price for further proceeding.<br> 
				<br><br> Thanks & Regards"""%(supply_order.name,supply_order.name)

			msg2 = """<div><style>.sh-src a{text-decoration:none!important;}</style></div> <br> <table cellpadding="0" cellspacing="0" border="0" class="sh-src" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td align="center" style="padding: 0px 23px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 16px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/file/17u3rllxlu3i3d" alt="" title="Profile Picture" width="84" height="84" class="" style="display: block; border: 0px; max-width: 84px;"></p></td></tr></table> <table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><p style="margin: 1px;"><a href="http://tsl-me.com" target="_blank"><img src="https://signaturehound.com/api/v1/file/137twgllxlu01oi" alt="" title="Logo" width="129" height="47" style="display: block; border: 0px; max-width: 129px;"></a></p></td></tr></table></td> <td width="5" style="padding: 1px 0px 0px;"></td> <td style="padding: 0px 1px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 13px 0px; border-bottom: 2px solid rgb(0,123,255); font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap;"><p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; font-weight: 700; color: rgb(0,0,0); white-space: nowrap; margin: 1px;">Muhammad Umar
			</p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">Customer Support Executive</p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">
				Dammam Branch </p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">
				Technical Solutions Company for Maintenance</p> <!----></td></tr> <tr><td style="padding: 13px 1px 13px 0px; border-bottom: 2px solid rgb(0,123,255);"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/email/default/007bff.png" alt="" width="18" height="18" style="display: block; border: 0px; margin: 0px; width: 18px; height: 18px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="mailto:info-dmm@tsl-me.com" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">info-dmm@tsl-me.com</span></a></p></td></tr>  <tr><td valign="top" style="padding: 1px 5px 1px 0px; vertical-align: top;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/map/default/007bff.png" alt="" width="18" height="18" style="display: block; border: 0px; margin: 0px; width: 18px; height: 18px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://maps.app.goo.gl/VqaMGCLVvnGnotrX7?g_st=iw" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">2nd industry، no 38، 166st X 23st Factory, Dammam 32275,<br> Saudi Arabia</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/website/default/007bff.png" alt="" width="18" height="18" style="display: block; border: 0px; margin: 0px; width: 18px; height: 18px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(0,123,254) !important; font-weight: 700; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;">
				<a href="http://tsl-me.com" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(0,123,255); font-weight: 700; text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(0,123,255); font-weight: 700; text-decoration: none !important;">tsl-me.com</span></a></p></td></tr></table></td></tr> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td width="30" style="font-size: 0px; line-height: 0px; padding: 16px 1px 0px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/facebook/default/007bff.png" alt="" width="30" height="30" style="display: block; border: 0px; margin: 0px; width: 30px; height: 30px;"></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="30" style="font-size: 0px; line-height: 0px; padding: 16px 1px 0px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/linkedin/default/007bff.png" alt="" width="30" height="30" style="display: block; border: 0px; margin: 0px; width: 30px; height: 30px;"></p></td> <td width="3" style="padding: 0px 0px 1px;"></td></tr></table></td></tr></table></td></tr></table></td></tr> <!----> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: 0px; border-collapse: collapse;"><tr><td style="padding: 20px 1px 0px 0px; font-family: Arial, sans-serif; font-size: 10px; line-height: 13px; color: rgb(136,136,136);"><p style="font-family: Arial, sans-serif; font-size: 10px; line-height: 13px; color: rgb(136,136,136); margin: 1px;">The content of this email is confidential and intended for the recipient specified in message only. It is strictly forbidden to share any part of this message with any third party, without a written consent of the sender. If you received this message by mistake, please reply to this message and follow with its deletion, so that we can ensure such a mistake does not occur in the future.</p></td></tr></table></td></tr> <!----> <!----></table>"""
			frappe.sendmail(
					recipients="purchase-sa@tsl-me.com",
					sender="info-dmm@tsl-me.com",
					subject= "New Supply Order Created Needed Price",
					message= msg1+msg2,
					attachments=get_attachments(supply_order.name,"Supply Order Data")

					)

def get_attachments(name,doctype):
	attachments = frappe.attach_print(doctype, name,file_name=doctype, print_format="Supply Order Mail")
	return [attachments]

