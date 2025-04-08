from pydoc import doc
from re import L
import frappe
import json
from frappe.model.mapper import get_mapped_doc
# import pandas as pd
from frappe import get_print
from datetime import datetime
import requests
from erpnext.setup.utils import get_exchange_rate
from frappe.utils import (
	add_days,
	add_months,
	cint,
	date_diff,
	flt,
	get_first_day,
	get_last_day,
	get_link_to_form,
	getdate,
	rounded,
	today,
)


@frappe.whitelist()
def on_submit(doc,method):
	if doc.project:
		if doc.quotation_type == "Internal Quotation - Project":
			p = frappe.get_doc("Project Data",doc.project)
			p.status = "IQ-Internally Quoted"
			p.save()
		if doc.quotation_type == "Customer Quotation - Project":
			p = frappe.get_doc("Project Data",doc.project)
			p.status = "A-Approved"
			p.save()
	# d = datetime.now().date()
	# if doc.quotation_type in ["Customer Quotation - Repair","Customer Quotation - Supply","Revised Quotation - Repair","Revised Quotation - Supply"]:
	# 	doc.approval_date = d
	# 	frappe.db.set_value("Quotation",doc.name,"approval_date",d)
		# for i in doc.items:
		# 	if i.wod_no:
		# 		frappe.db.set_value("Work Order Data",i.wod_no,"quotation_approved_date",d)
		# 	if i.supply_order_data:
		# 		frappe.db.set_value("Supply Order Data",i.supply_order_data,"quotation_approved_date",d)
		

	if doc.service_call_form:
		frappe.errprint("sv")
		if doc. quotation_type == "Site Visit Quotation - Internal":
			sc = frappe.get_doc("Service Call Form",doc.service_call_form)
			sc.status = "Internally Quoted"
			sc.save(ignore_permissions = 1)
		if doc. quotation_type == "Site Visit Quotation - Customer":
			frappe.errprint("sv")
			sc = frappe.get_doc("Service Call Form",doc.service_call_form)
			sc.status = "Approved"
			sc.save(ignore_permissions = 1)
		
	if doc.quotation_type == "Customer Quotation - Repair" or doc.quotation_type == "Revised Quotation - Repair":
		if doc.items:
			for i in doc.items:
				if i.wod_no:
					wd = frappe.get_doc("Work Order Data",i.wod_no)
					wd.quoted = 1
					wd.save(ignore_permissions =1)
			
@frappe.whitelist()
def on_update_after_submit(doc,method):
	d = datetime.now().date()
	if doc.quotation_type in ["Customer Quotation - Repair","Customer Quotation - Supply","Revised Quotation - Repair","Revised Quotation - Supply"]:
		doc.approval_date = d
		frappe.db.set_value("Quotation",doc.name,"approval_date",d)
		
		for i in doc.items:
			if i.wod_no:
				frappe.db.set_value("Work Order Data",i.wod_no,"quotation_approved_date",d)
			if i.supply_order_data:
				frappe.db.set_value("Supply Order Data",i.supply_order_data,"quotation_approved_date",d)
		
		

@frappe.whitelist()
def get_wod_items(wod):
	wod = json.loads(wod)
	l=[]
	for k in list(wod):
		tot = 0
		tot = frappe.db.sql('''select sum(total_amount) as total_amount  from `tabEvaluation Report` where work_order_data = %s and docstatus=0 group by work_order_data''',k,as_dict=1)
		doc = frappe.get_doc("Work Order Data",k)
		branch = doc.branch
		if len(tot) and 'total_amount' in tot[0]:
			tot = tot[0]['total_amount']
		else:
			tot = 0
		for i in doc.get("material_list"):
			l.append(frappe._dict({
				"item" :i.item_code,
				"item_name" : i.item_name0,
				"description":i.item_name,
				"wod": k,
				"type": i.type,
				"model_no": i.model_no,
				"manufacturer": i.mfg,
				"serial_no": i.serial_no,
				"qty": i.quantity,
				"sales_rep":doc.sales_rep,
				"total_amt":float(tot)/float(i.quantity),
				"branch":branch,

			}))
	return l
# Approved Quotation Multiselect
@frappe.whitelist()
def get_qtn_items(qtn):
	qtn = json.loads(qtn)
	l=[]
	for k in list(qtn):
		tot = 0
		totd = 0
		tot = frappe.db.sql('''select sum(total_amount) as total_amount  from `tabEvaluation Report` where work_order_data = %s and docstatus=0 group by work_order_data''',k,as_dict=1)
		doc = frappe.get_doc("Quotation",k)
		totd += doc.default_discount_value

		if len(tot) and 'total_amount' in tot[0]:
			tot = tot[0]['total_amount']
		else:
			tot = 0
		for i in doc.get("items"):
			l.append(frappe._dict({
				"item" :i.item_code,
				"item_name" : i.item_name,
				"description":i.item_name,
				"wod_no": i.wod_no,
				"type": i.type,
				"model_no": i.model_no,
				"manufacturer": i.manufacturer,
				"serial_no": i.serial_no,
				"qty": i.qty,
				"margin_amount": i.margin_amount or doc.after_discount_cost,
				"margin_amount_value": i.margin_amount_value or totd,
				"unit_price": i.unit_price or doc.unit_rate_price,
				# "sales_rep":doc.sales_rep,
				# "total_amt":float(tot)/float(i.quantity),
				# "branch":branch,

			}))
	return l
@frappe.whitelist()
def get_sqtn_items(sod):
	sod = json.loads(sod)
	l=[]
	for k in list(sod):
		l += frappe.db.sql('''select si.sr_no as sr_no,si.item_code as item_code,si.mfg as manufacturer,si.supplier_quotation as sqtn,si.model_no as model_no,si.type as type,si.serial_no as serial_no,si.model_no as item_name,si.description as description,"Nos" as uom,"Nos" as stock_uom,1 as conversion_factor,si.quantity as qty,si.price as rate,si.amount as amount,s.name as sod from `tabSupply Order Table` as si inner join `tabSupply Order Data` as s on si.parent = s.name where s.docstatus = 1 and s.name = %s order by si.idx  ''',k,as_dict =1)
		
		l += frappe.db.sql('''select si.part as item_code,si.manufacturer as manufacturer,si.supplier_quotation as sqtn,si.model as model_no,si.type as type,si.serial_no as serial_no,si.part_name as item_name,"Nos" as uom,"Nos" as stock_uom,1 as conversion_factor,si.qty as qty,si.price_ea as rate,si.total as amount,s.name as sod from `tabPart Sheet Item Supply` as si inner join `tabSupply Order Data` as s on si.parent = s.name where s.docstatus = 1 and s.name = %s order by si.idx ''',k,as_dict =1)
	
	return l


@frappe.whitelist()
def get_online_price(ite):
	item = json.loads(ite)
	l=[]
	for i in item:
		l += frappe.db.sql('''select k.website,k.comments,k.item_code,k.price_type,k.price from `tabItem` as t inner join `tabOnline Price List` as k on k.parent = t.name where t.name = %s ''',i["item_code"],as_dict =1)
	
				
	return l


@frappe.whitelist()
def get_similar_unit_details(name):
	doc = frappe.get_doc("Quotation",name)
	l=[]
	if doc.quotation_type == 'Internal Quotation - Supply':
		for i in doc.get("items"):
			l.append(i.supply_order_data)
		l = list(set(l))
		for j in l:
			sod = frappe.get_doc("Supply Order Data",j)
			for i in sod.get('material_list'):
				if i.model_no and i.mfg and i.type and i.serial_no:
					for wod in frappe.db.sql('''select parent from `tabMaterial List` where model_no = %s and mfg = %s and type = %s and serial_no = %s and parenttype = "Work Order Data" ''',(i.model_no,i.mfg,i.type,i.serial_no),as_dict=1):
						prev_quoted = frappe.db.sql('''select q.party_name as customer,q.name as name,qi.rate as price from `tabQuotation Item` as qi inner join `tabQuotation` as q on qi.parent = q.name where qi.wod_no = %s and (q.quotation_type = "Customer Quotation - Repair" or q.quotation_type = "Revised Quotation - Repair") and q.workflow_state = "Approved By Customer" ''',wod['parent'],as_dict = 1)
						doc.append("similar_unit_details",{
							"customer":prev_quoted[0]['customer'],
							"model":i.model_no,
							"mfg":i.mfg,
							"type":i.type,
							"quoted_price":prev_quoted[0]['price'],
							"quotation_no":prev_quoted[0]['name']
						})
					doc.save(ignore_permissions =True)
	if doc.quotation_type == 'Internal Quotation - Repair':
		for i in doc.get("items"):
			l.append(i.wod_no)
		for j in l:
			wod = frappe.get_doc("Work Order Data",j)
			for i in wod.get('material_list'):
				if i.model_no and i.mfg and i.type and i.serial_no:
					for sod in frappe.db.sql('''select parent from `tabMaterial List` where model_no = %s and mfg = %s and type = %s and serial_no = %s and parenttype = "Supply Order Data" ''',(i.model_no,i.mfg,i.type,i.serial_no),as_dict=1)[:4]:
						prev_quoted = frappe.db.sql('''select q.party_name as customer,q.name as name,qi.rate as price from `tabQuotation Item` as qi inner join `tabQuotation` as q on qi.parent = q.name where qi.supply_order_data = %s and (q.quotation_type = "Customer Quotation - Supply" or q.quotation_type = "Revised Quotation - Supply") and q.workflow_state = "Approved By Customer" ''',sod['parent'],as_dict = 1)
						doc.append("similar_unit_details",{
							"customer":prev_quoted[0]['customer'],
							"model":i.model_no,
							"mfg":i.mfg,
							"type":i.type,
							"quoted_price":prev_quoted[0]['price'],
							"quotation_no":prev_quoted[0]['name']
						})
					doc.save(ignore_permissions =True)
	
# @frappe.whitelist()		
# def get_itemwise_price(data):
# 	data = json.loads(data)
# 	l =[]
# 	for i in data:
# 		p = frappe.db.get_value("Supplier Wise Item",{"sku":i['item_code'],"supplier_quotation":i['supplier_quotation']},['price','amount'])
# 		l.append(p)
# 		i["rate"] = p[0]
# 		i["price_list_rate"] = p[0]
# 		i["amount"] = p[1]

# 	return l
@frappe.whitelist()
def sum_amount(doc,method):
	if not doc.company == "TSL COMPANY - UAE" and not doc.company == "TSL COMPANY - KSA" :
		for sm in doc.items:
			pi = frappe.db.sql("""select sum(amount)as amount,work_order_data from `tabItem Price Details` where parent = '%s' and docstatus = 0 group by work_order_data = '%s'"""%(doc.name,sm.wod_no),as_dict=1)
			ths = frappe.db.sql("""select sum(total_price) as price,work_order_data from `tabTechnician Hours Spent` where parent = '%s' and docstatus = 0 group by work_order_data = '%s'"""%(doc.name,sm.wod_no),as_dict=1)	
			for p in pi:
				if p.work_order_data:
					for th in ths:
						if th.work_order_data:
							if p.work_order_data == th.work_order_data:
								th = th.price
								pt= p.amount
								tot_a = th + pt
								sm.rate = tot_a
							else:
								sm.rate = p.amount


def show_details(self,method):
	if self.is_multiple_quotation == 1:
		tot = 0
		up=0
		for i in self.get("items"):
			tot += i.unit_price * i.qty
			if self.quotation_type == "Revised Quotation - Repair":
				up += i.margin_amount *i.qty
			else:
				up += i.margin_amount * i.qty
			actual_percentage = (tot/100)*5
			price = up - actual_percentage
		

		self.final_approved_price = up
		if self.company == "TSL COMPANY - UAE":
			self.unit_rate_price = round(tot,2)
		else:
			self.unit_rate_price = round(tot)
		if not self.default_discount_value:
			if self.company == "TSL COMPANY - UAE":
				self.default_discount_value = round(actual_percentage,2)
			else:
				self.default_discount_value = round(actual_percentage)
	if self.is_multiple_quotation == 0 and self.quotation_type == "Internal Quotation - Supply":
		up=0
		for i in self.get("items"):
			
			up = up + i.margin_amount
			
	
		# self.final_approved_price = up

	if self.quotation_type == "Internal Quotation - Repair":
		self.item_price_details=[]
		self.similar_items_quoted_before=[]
		self.technician_hours_spent =[]
		tc = self.technician_hours_spent
		parts_priced = self.parts_price_list_
		
		
		for i in self.get("items"):
			total_qtn_rate = 0
			part_sheet = frappe.db.sql('''select name from `tabEvaluation Report` where work_order_data = %s and docstatus = 1 order by creation desc''',i.wod_no,as_dict=1)
			for j in  part_sheet:
				doc = frappe.get_doc("Evaluation Report",j['name']) 
				total = 0
				if doc.evaluation_time and doc.estimated_repair_time:
					total = round(((doc.evaluation_time/3600) + (doc.estimated_repair_time/3600)),2)
					exr = get_exchange_rate("KWD","AED")
					if self.company == "TSL COMPANY - UAE":
					
						self.append("technician_hours_spent",{
							"total_hours_spent":total,
							"value":20 * exr,
							"total_price":total*(20 * exr),
							"work_order_data":doc.work_order_data
						})
					elif self.company == "TSL COMPANY - KSA":
						self.append("technician_hours_spent",{
							"total_hours_spent":total,
							"value":300,
							"total_price":total*300,
							"work_order_data":doc.work_order_data
						})
					else:
						self.append("technician_hours_spent",{
							"total_hours_spent":total,
							"value":20,
							"total_price":total*20,
							"work_order_data":doc.work_order_data
						})


		for i in self.get("items"):
			
			eval =frappe.db.exists("Evaluation Report",{"work_order_data":i.wod_no})
			if eval:
				doc = frappe.get_doc("Evaluation Report",{"name":eval}) 
				if doc:
					for k in doc.get("items"):
						
						total_qtn_rate += k.total
						if self.company == "TSL COMPANY - Kuwait" and k.parts_availability == "No":
							
							source = "Supplier"
							price = k.price_ea
							sq_no = frappe.db.sql('''select sq.name as sq, sum(sq.shipping_cost) as spc, sq.currency as currency from `tabSupplier Quotation` as sq inner join `tabSupplier Quotation Item` as sqi on sqi.parent = sq.name 
														where sq.docstatus = 1 and sq.work_order_data = %s and sqi.item_code = %s and sq.workflow_state = "Approved By Management" 
									order by sq.modified desc limit 1''',(doc.work_order_data,k.part),as_dict=1)	
							
							
							
							for sq in sq_no:
								price = k.price_ea
								self.append("item_price_details",{
								"item":k.part,
								"item_source":source,
								"model":k.model,
								"price":price,
								"amount":k.total,
								"supplier_quotation":sq["sq"],
								"work_order_data":doc.work_order_data

							})
								url = "https://api.exchangerate-api.com/v4/latest/%s"%(sq.currency)

								payload = {}
								headers = {}

								response = requests.request("GET", url, headers=headers, data=payload)
								data = response.json()
								frappe.errprint(data)
								rates_kw = data['rates']['KWD']
								conv_rate = sq.spc * rates_kw
								self.shipping_cost = conv_rate

								
							if len(sq_no):
								sq_no = sq_no[0]["sq"]
							else:
								sq_no =  ""
							
						elif self.company == "TSL COMPANY - UAE" and k.parts_availability == "No":
							sq_no = frappe.db.sql('''select sq.name as sq, sum(sq.shipping_cost) as spc, sq.currency as currency from `tabSupplier Quotation` as sq inner join `tabSupplier Quotation Item` as sqi on sqi.parent = sq.name 
							where sq.docstatus = 1 and sq.work_order_data = %s and sqi.item_code = %s and sq.workflow_state = "Approved By Management" 
							order by sq.modified desc limit 1''',(doc.work_order_data,k.part),as_dict=1)	
							# if sq_no:
							# 	frappe.db.set_value("Supplier Quotation",sq_no,"quotation",self.name)
							
							for sq in sq_no:
								if sq.spc:	
									url = "https://api.exchangerate-api.com/v4/latest/%s"%(sq.currency)

									payload = {}
									headers = {}

									response = requests.request("GET", url, headers=headers, data=payload)
									data = response.json()
									rates_kw = data['rates']['AED']
									conv_rate = sq.spc * rates_kw
									self.shipping_cost = conv_rate
							if len(sq_no):
								sq_no = sq_no[0]["sq"]
							else:
								sq_no =  ""
							

							exr = get_exchange_rate(self.currency,"AED")
							source = "Supplier"
							
							price = k.price_ea
							self.append("item_price_details",{
							"item":k.part,
							"item_source":source,
							"model":k.model,
							"price":price * exr,
							"amount":k.total * exr,
							"supplier_quotation":sq_no,
							"work_order_data":doc.work_order_data

							})
						
						elif self.company == "TSL COMPANY - KSA" and k.parts_availability == "No":
							sq_no = frappe.db.sql('''select sq.name as sq, sum(sq.shipping_cost) as spc, sq.currency as currency from `tabSupplier Quotation` as sq inner join `tabSupplier Quotation Item` as sqi on sqi.parent = sq.name 
														where sq.docstatus = 1 and sq.work_order_data = %s and sqi.item_code = %s and sq.workflow_state = "Approved By Management" 
									order by sq.modified desc limit 1''',(doc.work_order_data,k.part),as_dict=1)	
							# if sq_no:
							# 	frappe.db.set_value("Supplier Quotation",sq_no,"quotation",self.name)
							
							for sq in sq_no:
								if sq.spc:	
									url = "https://api.exchangerate-api.com/v4/latest/%s"%(sq.currency)

									payload = {}
									headers = {}

									response = requests.request("GET", url, headers=headers, data=payload)
									data = response.json()
									rates_kw = data['rates']['SAR']
									conv_rate = sq.spc * rates_kw
									self.shipping_cost = conv_rate
							if len(sq_no):
								sq_no = sq_no[0]["sq"]
							else:
								sq_no =  ""
							

							exr = get_exchange_rate(self.currency,"SAR")
							source = "Supplier"
							
							price = k.price_ea
							self.append("item_price_details",{
							"item":k.part,
							"item_source":source,
							"model":k.model,
							"price":price * exr,
							"amount":k.total * exr,
							"supplier_quotation":sq_no,
							"work_order_data":doc.work_order_data

							})
						else:
							price = k.price_ea
							source = "TSL Inventory"
							sq_no = ""
							self.append("item_price_details",{
							"item":k.part,
							"item_source":source,
							"model":k.model,
							"price":price,
							"amount":k.total,
							# "supplier_quotation":sq_no,
							"work_order_data":doc.work_order_data

							})
						
			labour_value = 0
			for t in tc:
				labour_value += t.total_price
			if parts_priced:
				for pp in parts_priced:
					cost = float(pp.total_material_cost)
		
			
				if not self.is_multiple_quotation and self.technician_hours_spent:
						self.actual_cost = round(labour_value + cost)
				else:
					

					self.actual_cost = round(labour_value + cost)
					
				if self.after_discount_cost:
					self.in_words1 = frappe.utils.money_in_words(self.after_discount_cost) or "Zero"

	if self.quotation_type == "Internal Quotation - Supply":
		l = []
		fc = cc = pc = additional =0
		mfd = "0"
		mcd = "0"
		for i in self.get('items'):
			if i.supplier_quotation:
				l.append(i.supplier_quotation)
		l = list(set(l))
		for i in l:
			doc = frappe.get_doc("Supplier Quotation",i)
			fc += doc.freight_charges
			cc += doc.custom_clearance
			pc += doc.payment_commission
			mfd = doc.max_freight_duration if doc.max_freight_duration and int(doc.max_freight_duration) > int(mfd) else mfd
			mcd = doc.max_custom_duration if doc.max_custom_duration and int(doc.max_custom_duration) > int(mcd) else mcd
			doc.save(ignore_permissions = True)
		self.freight_charges = fc
		self.custom_clearance = cc
		self.payment_commission = pc
		self.max_freight_duration = mfd
		self.max_custom_duration = mcd
		additional = (self.freight_charges + self.custom_clearance + self.payment_commission )
		if not self.margin_rate:
			self.margin_rate = 0
		discount_amount = (additional + self.margin_rate)*-1
		self.discount_amount = discount_amount or 0
		self.grand_total -= self.discount_amount
		self.rounded_total = self.grand_total

	for i in self.get("items"):
		if i.item_code:
			suqb = frappe.db.sql('''select q.party_name as customer,qi.parent as quotation_no,qi.wod_no as work_order_data,qi.supply_order_data as supply_order_data ,qi.rate as quoted_price,qi.margin_amount as margin_quoted_price
			,qi.item_code as sku,qi.model_no as model,qi.type as type,qi.manufacturer as mfg ,q.after_discount_cost as adc from `tabQuotation` as q inner join `tabQuotation Item` as qi
			on qi.parent=q.name where qi.item_code = %s and q.workflow_state = "Approved By Customer" and q.docstatus = 1 and q.name != %s and q.company = %s ''',(i.item_code,self.name,self.company),as_dict =1 )
			
			if suqb:
				self.previously_quoted_unit = []
			
				for j in suqb[:1]:
					if j.work_order_data:
						w_doc = frappe.get_doc("Work Order Data",j.work_order_data)
					
						self.append("previously_quoted_unit",{
						"customer":j.customer,
						"sku":j.sku,
						"model":j.model,
						"type":j.type,
						"mfg":j.mfg,
						"quoted_price":j.margin_quoted_price or j.adc,
						"quotation_no":j.quotation_no,
						"work_order_data":j.work_order_data or "" ,
						"wo_status":w_doc.status
})
@frappe.whitelist()
def create_cust_qtn(type,source):
	doc = frappe.get_doc('Quotation',source)
	target_doc = frappe.new_doc('Quotation')
	target_doc.party_name = doc.party_name
	target_doc.branch_name = doc.branch_name
	target_doc.internal_quotation = source
	target_doc.quotation_type = "Customer Quotation - Repair"
	
	target_doc.quotation_type = type
	if type == "Customer Quotation - Repair":
		target_doc.overall_discount_amount = 0
		target_doc.margin_rate = 0
		target_doc.discount_amount = 0
	target_doc.append("quotation_history",{
		"quotation_type":doc.quotation_type,
		"status":doc.workflow_state,
		"quotation_name":doc.name,
	})
	for i in doc.items:
		target_doc.append("items",{
			"item_code":i.item_code,
			'rate':i.margin_amount or i.rate, 
			'uom':1,
			'description':i.description,
			'item_name':i.item_name,
			'wod_no':i.wod_no,
			'qty':i.qty,
		})

	return target_doc


@frappe.whitelist()
def get_quotation_tender(source,type = None):
	target_doc = frappe.new_doc("Quotation")
	doc = frappe.get_doc("Quotation",source)
	if not doc.is_multiple_quotation:
		for i in doc.items:
			rate = i.margin_amount

	def postprocess(source, target_doc):
		target_doc.quotation_type = type
		target_doc.naming_series = "ST-Q-R-.YY.-"
		target_doc.workflow_state = "Quoted to Customer"
		if type == "Customer Quotation - Repair":
			target_doc.overall_discount_amount = 0
			target_doc.margin_rate = 0
			target_doc.discount_amount = 0
		target_doc.append("quotation_history",{
			"quotation_type":"Site Visit Quotation - Customer",
			"quotation_name":doc.name,
		})

	doclist = get_mapped_doc("Quotation",source , {
		"Quotation": {
			"doctype": "Quotation",
			
		},
		"Quotation Item": {
			"doctype": "Quotation Item",
			
		},
	}, target_doc, postprocess)

	return doclist

	
@frappe.whitelist()
def get_quotation(source,type = None):
	target_doc = frappe.new_doc("Quotation")
	doc = frappe.get_doc("Quotation",source)
	if not doc.is_multiple_quotation:
		for i in doc.items:
			rate = i.margin_amount

	def postprocess(source, target_doc):
		target_doc.quotation_type = type
		if doc.company == "TSL COMPANY - Kuwait":
			target_doc.naming_series = "SV-QTN-CUS-K.YY.-"

		if doc.company == "TSL COMPANY - UAE":
			target_doc.naming_series = "SV-QTN-CUS-DU.YY.-"
		
		if doc.company == "TSL COMPANY - KSA":
			if doc.branch_name == "Riyadh - TSL- KSA":
				target_doc.naming_series = "SV-QTN-CUS-R.YY.-"
		
		if doc.company == "TSL COMPANY - KSA":
			if doc.branch_name == "Jeddah - TSL-SA":
				target_doc.naming_series = "SV-QTN-CUS-J.YY.-"
		
		if doc.company == "TSL COMPANY - KSA":
			if doc.branch_name == "Dammam - TSL-SA":
				target_doc.naming_series = "SV-QTN-CUS-D.YY.-"
		

		target_doc.workflow_state = "Quoted to Customer"
		if type == "Customer Quotation - Repair":
			target_doc.overall_discount_amount = 0
			target_doc.margin_rate = 0
			target_doc.discount_amount = 0
		target_doc.append("quotation_history",{
			"quotation_type":"Site Visit Quotation - Customer",
			"quotation_name":doc.name,
		})

	doclist = get_mapped_doc("Quotation",source , {
		"Quotation": {
			"doctype": "Quotation",
			
		},
		"Quotation Item": {
			"doctype": "Quotation Item",
			
		},
	}, target_doc, postprocess)

	return doclist

@frappe.whitelist()
def get_quote(source,type = None):
	target_doc = frappe.new_doc("Quotation")
	doc = frappe.get_doc("Quotation",source)
	
	def postprocess(source, target_doc):
		target_doc.quotation_type = type
		if type == "Customer Quotation - Repair":
			target_doc.overall_discount_amount = 0
			target_doc.margin_rate = 0
			target_doc.discount_amount = 0
			# target_doc.taxes_and_charges = "UAE VAT 5% - TSL-UAE"
		target_doc.append("quotation_history",{
			"quotation_type":doc.quotation_type,
			"status":doc.workflow_state,
			"quotation_name":doc.name,
		})


	doclist = get_mapped_doc("Quotation",source , {
		"Quotation": {
			"doctype": "Quotation",
			
		},
		"Quotation Item": {
			"doctype": "Quotation Item",
			
		},
	}, target_doc, postprocess)
	
	
		# if not doc.quotation_type == "Internal Quotation - Supply":
	for ic in doclist.get('items'):
		ic.rate = ic.margin_amount
					
	return doclist
	
	# target_doc = frappe.new_doc("Quotation")
	# doc = frappe.get_doc("Quotation",source)
	# if not doc.is_multiple_quotation:
	# 	for i in doc.items:
	# 		rate = i.margin_amount

	# def postprocess(source, target_doc):
	# 	target_doc.quotation_type = type
	# 	if type == "Customer Quotation - Repair":
	# 		target_doc.overall_discount_amount = 0
	# 		target_doc.margin_rate = 0
	# 		target_doc.discount_amount = 0
	# 		# target_doc.taxes_and_charges = "UAE VAT 5% - TSL-UAE"
	# 	target_doc.append("quotation_history",{
	# 		"quotation_type":doc.quotation_type,
	# 		"status":doc.workflow_state,
	# 		"quotation_name":doc.name,
	# 	})

	# doclist = get_mapped_doc("Quotation",source , {
	# 	"Quotation": {
	# 		"doctype": "Quotation",
			
	# 	},
	# 	"Quotation Item": {
	# 		"doctype": "Quotation Item",
			
	# 	},
	# }, target_doc, postprocess)
	
	# if not doc.quotation_type == "Internal Quotation - Supply":
	# 	for ic in doclist.get('items'):
	# 		if not ic.margin_amount:
	# 			disc = (doclist.after_discount_cost * doclist.default_discount_percentage)/100
	# 			unit_disc = disc
	# 			ic.rate = doc.after_discount_cost+disc
				
	# 		if not doc.is_multiple_quotation and ic.item_code:
	# 			if doc.company == "TSL COMPANY - UAE":
	# 				ic.rate = round(doc.after_discount_cost)
	# 			else:
	# 				ic.rate = round(doc.after_discount_cost,2)
			
	# 		if doc.is_multiple_quotation and ic.item_code:
	# 			ic.rate = ic.margin_amount
	# 			ic.item_price = ic.margin_amount
				
	# else:
	# 	for ic in doclist.get('items'):
			
	# 		if not ic.margin_amount:
	# 			disc = (doclist.after_discount_cost * doclist.default_discount_percentage)/100
	# 			unit_disc = disc
				
	# 			ic.rate = ic.rate
			
	# 		if ic.item_code:
	# 			ic.rate = ic.margin_amount
			
					
				
	# return doclist

@frappe.whitelist()
def get_quote_ksa(source,type = None):
	target_doc = frappe.new_doc("Quotation")
	doc = frappe.get_doc("Quotation",source)
	if not doc.is_multiple_quotation:
		for i in doc.items:
			rate = i.margin_amount

	def postprocess(source, target_doc):
		target_doc.quotation_type = type
		if type == "Customer Quotation - Repair":
			target_doc.overall_discount_amount = 0
			target_doc.margin_rate = 0
			target_doc.discount_amount = 0
			# target_doc.taxes_and_charges = "UAE VAT 5% - TSL-UAE"
		target_doc.append("quotation_history",{
			"quotation_type":doc.quotation_type,
			"status":doc.workflow_state,
			"quotation_name":doc.name,
		})


	doclist = get_mapped_doc("Quotation",source , {
		"Quotation": {
			"doctype": "Quotation",
			
		},
		"Quotation Item": {
			"doctype": "Quotation Item",
			
		},
	}, target_doc, postprocess)
	
	
	# if not doc.quotation_type == "Internal Quotation - Supply":
	if type  == "Revised Quotation - Supply" or type  == "Revised Quotation - Repair":
		for ic in doclist.get('items'):
			ic.rate = ic.unit_price
	else:
		for ic in doclist.get('items'):
			ic.rate = ic.margin_amount
	# for i in doc.items:
		
		
					
				
	return doclist
	# doc = frappe.get_doc("Quotation",source)
	# target_doc = frappe.new_doc("Quotation")
	# target_doc.is_multiple_quotation = doc.is_multiple_quotation
	# target_doc.quotation_type = type
	# target_doc.naming_series = doc.naming_series
	# target_doc.party_name = doc.party_name
	# if type == "Customer Quotation - Repair":
	# 	target_doc.overall_discount_amount = 0
	# 	target_doc.margin_rate = 0
	# 	target_doc.discount_amount = 0
	# target_doc.append("quotation_history",{
	# 	"quotation_type":doc.quotation_type,
	# 	"status":doc.workflow_state,
	# 	"quotation_name":doc.name,
	# })

	# for i in doc.get("items"):
	# 	target_doc.append("items",{
	# 	"item_code":i.item_code,
	# 	"item_name":i.item_name,
	# 	"margin_amount":i.margin_amount,
	# 	"rate":i.rate,
	# 	"description":i.description,
	# 	"uom":i.uom,
	# 	"qty":i.qty,
	# 	"wod_no":i.wod_no

	# })
	# # target_doc.taxes_and_charges = doc.taxes_and_charges

	# # for i in doc.get("taxes"):
	# # 	target_doc.append("taxes",{
	# # 	"charge_type":i.charge_type,
	# # 	"account_head":i.account_head

	# # })
	# target_doc.save(ignore_permissions = 1)
	
	# return target_doc
	# # target_doc = get_mapped_doc("Quotation",source , {
	# # 	# "Quotation": {
	# # 	# 	"doctype": "Quotation",
			
	# # 	# },
	# # 	"Quotation Item": {
	# # 		"doctype": "Quotation Item",
			
	# # 	},
	# # }, target_doc, postprocess)
	
	# # if not doc.quotation_type == "Internal Quotation - Supply":
	# # 	for ic in doclist.get('items'):
	# # 		
	# # 		if not ic.margin_amount:
	# # 			disc = (doclist.after_discount_cost * doclist.default_discount_percentage)/100
	# # 			unit_disc = disc

	# # 			ic.rate = doc.after_discount_cost+disc
			
	# # 		if not doc.is_multiple_quotation and ic.item_code:
	# # 			ic.rate = round(doc.unit_rate_price)
		
	# # else:
	# # 	for ic in doclist.get('items'):
	# # 		if not ic.margin_amount:
	# # 			disc = (doclist.after_discount_cost * doclist.default_discount_percentage)/100
	# # 			unit_disc = disc

	# # 			ic.rate = ic.rate
			
	# # 		if ic.item_code:
	# # 			ic.rate = ic.rate
			


@frappe.whitelist()
def get_quote_pro(source,type = None):
	target_doc = frappe.new_doc("Quotation")
	doc = frappe.get_doc("Quotation",source)
	
	def postprocess(source, target_doc):
		target_doc.quotation_type = type
		if type == "Customer Quotation - Project":
			target_doc.naming_series = "PCQ-DU.YY.-"
			target_doc.overall_discount_amount = 0
			target_doc.margin_rate = 0
			target_doc.discount_amount = 0
			# target_doc.taxes_and_charges = "UAE VAT 5% - TSL-UAE"
		target_doc.append("quotation_history",{
			"quotation_type":doc.quotation_type,
			"status":doc.workflow_state,
			"quotation_name":doc.name,
		})

	doclist = get_mapped_doc("Quotation",source , {
		"Quotation": {
			"doctype": "Quotation",
			
		},
		"Quotation Item": {
			"doctype": "Quotation Item",
			
		},
	}, target_doc, postprocess)
	
	
	return doclist


@frappe.whitelist()
def get_quotation_history(source,type = None):
	target_doc = frappe.new_doc("Quotation")
	doc = frappe.get_doc("Quotation",source)
	if not doc.is_multiple_quotation:
		for i in doc.items:
			rate = i.margin_amount
	
	def postprocess(source, target_doc):
		target_doc.quotation_type = type
		if type == "Customer Quotation - Repair":
			target_doc.overall_discount_amount = 0
			target_doc.margin_rate = 0
			target_doc.discount_amount = 0
		target_doc.append("quotation_history",{
			"quotation_type":doc.quotation_type,
			"status":doc.workflow_state,
			"quotation_name":doc.name,
		})

	doclist = get_mapped_doc("Quotation",source , {
		"Quotation": {
			"doctype": "Quotation",
			
		},
		"Quotation Item": {
			"doctype": "Quotation Item",
			
		},
	}, target_doc, postprocess)


	if doc.company == "TSL COMPANY - Kuwait":
		if not doc.quotation_type == "Internal Quotation - Supply":
			for ic in doclist.get('items'):
				if not ic.margin_amount:
					disc = (doclist.after_discount_cost * doclist.default_discount_percentage)/100
					unit_disc = disc

					ic.rate = doc.after_discount_cost+disc
				
				if not doc.is_multiple_quotation and ic.item_code:
					ic.rate = round(doc.unit_rate_price)
			
		else:
			for ic in doclist.get('items'):
				if not ic.margin_amount:
					disc = (doclist.after_discount_cost * doclist.default_discount_percentage)/100
					unit_disc = disc
					ic.rate = doc.after_discount_cost
					# ic.rate = ic.rate
				
				if ic.item_code:
					ic.rate = ic.rate

	if doc.company == "TSL COMPANY - UAE" or doc.company == "TSL COMPANY - KSA":

		# if not doc.quotation_type == "Internal Quotation - Supply":
		if type  == "Revised Quotation - Supply" or type  == "Revised Quotation - Repair":
			for ic in doclist.get('items'):
				ic.rate = ic.unit_price
		else:
			for ic in doclist.get('items'):
				ic.rate = ic.margin_amount
			# if not doc.is_multiple_quotation:
			# 	if type  == "Revised Quotation - Supply" or type  == "Revised Quotation - Repair":
			# 		disc = (doclist.after_discount_cost * doclist.default_discount_percentage)/100
			# 		unit_disc = disc

			# 		ic.rate = doc.unit_rate_price
			# 		ic.item_price =  doc.unit_rate_price
			# 		ic.price_list_rate = doc.unit_rate_price
			# 	else:
			# 		disc = (doclist.after_discount_cost * doclist.default_discount_percentage)/100
			# 		ic.rate = doc.after_discount_cost
			# 		ic.item_price = doc.after_discount_cost
				
			# if doc.is_multiple_quotation:
			# 	if type  == "Revised Quotation - Supply" or type  == "Revised Quotation - Repair":
			# 		ic.rate = ic.unit_price
			# 		ic.item_price = ic.unit_price
			# 		ic.price_list_rate = ic.unit_price
			# 	else:
			# 		ic.rate = ic.margin_amount
			# 		ic.item_price = ic.margin_amount

					
			
		# if doc.company == "TSL COMPANY - KSA":
		# 	for ic in doclist.get('items'):
		
		# 		if not ic.margin_amount:
		# 			disc = (doclist.after_discount_cost * doclist.default_discount_percentage)/100
		# 			unit_disc = disc
		# 			ic.rate = doc.after_discount_cost
		# 			ic.item_price = doc.after_discount_cost
		# 			# ic.rate = ic.rate
				
		# 		else:
		# 			ic.rate = ic.margin_amount
		# 			ic.item_price = ic.margin_amount

		
	# for i in doc.items:
	# 	rate = i.margin_amount
	# 	if rate:
	# 		for i in range(len(doclist.items)):
	# 			doclist.items[i].rate = (rate)
	# 			doclist.after_discount_cost = doc.actual_price
					
				
	return doclist


@frappe.whitelist()
def create_sal_inv(source):
	target_doc = frappe.new_doc("Sales Invoice")
	doc = frappe.get_doc("Quotation",source)
	target_doc.purchase_order_no = doc.purchase_order_no 
	target_doc.project_data = doc.project
	target_doc.cost_center = doc.department
	doclist = get_mapped_doc("Quotation",source , {
		"Quotation": {
			"doctype": "Sales Invoice",
			"field_map": {
				"name": "quotation",
				"party_name":"customer",
				"branch_name":"branch",
				
			},
			
		},
		"Quotation Item": {
			"doctype": "Sales Invoice Item",
			
		},

	}, target_doc)
	if doc.company == "TSL COMPANY - Kuwait":
		for mg in doc.get('items'):	
			for i in doclist.get('items'):		
				doclist.department = frappe.db.get_value("Work Order Data",i.wod_no,"department")
				if mg.item_code == i.item_code and doc.is_multiple_quotation:
					
					i.item_code = mg.item_code
					i.rate= mg.margin_amount
					i.model= mg.model_no
					i.manufacturer= mg.manufacturer
				if mg.item_code == i.item_code and not doc.is_multiple_quotation:
					
					i.rate= doc.after_discount_cost

	elif doc.company == "TSL COMPANY - UAE":
		for mg in doc.get('items'):	
			for i in doclist.get('items'):		
				doclist.department = frappe.db.get_value("Work Order Data",i.wod_no,"department")
				if mg.item_code == i.item_code and doc.is_multiple_quotation:
					
					i.item_code = mg.item_code
					if doc.disc:
						i.rate= mg.rate
					else:
						i.rate= mg.margin_amount
					i.model= mg.model_no
					i.manufacturer= mg.manufacturer
					i.project_data = mg.project
				# else:
				# 	i.rate= doc.after_discount_cost

	return doclist

@frappe.whitelist()
def create_inv_req(source,user):
	new_doc = frappe.new_doc("Invoice Request")
	doc = frappe.get_doc("Quotation",source)
	new_doc.requested_by = user


	if doc.quotation_type == "Customer Quotation - Repair" or doc.quotation_type == "Revised Quotation - Repair":
		new_doc.request_for = "Work Order"

		new_doc.append("invoice_list",{
		"quotation":doc.name,
		})

		wd = frappe.db.sql(""" select  `tabQuotation Item`.wod_no from `tabQuotation` 
			left join `tabQuotation Item` on `tabQuotation Item`.parent = `tabQuotation`.name
			where `tabQuotation`.name = '%s' """ %(doc.name),as_dict = 1)
		for i in wd:
			frappe.errprint(i["wod_no"])
			new_doc.append("invoice_list",{
			"wod_sod":i["wod_no"],
		})

	if doc.quotation_type == "Customer Quotation - Supply" or doc.quotation_type == "Revised Quotation - Supply":
		new_doc.request_for = "Supply Order"
		new_doc.append("sod_quotation",{
		"quotation":doc.name,
		})

		sd = frappe.db.sql(""" select  `tabQuotation Item`.supply_order_data from `tabQuotation` 
			left join `tabQuotation Item` on `tabQuotation Item`.parent = `tabQuotation`.name
			where `tabQuotation`.name = '%s' """ %(doc.name),as_dict = 1)
	
		
		for i in sd:
			new_doc.append("sod_quotation",{
			"supply_order_data":i["supply_order_data"],
		})
	
		
			
	return new_doc
	
	

	

@frappe.whitelist()
def create_sal_inv_pro(source):
	doc = frappe.get_doc("Quotation",source)
	new_doc= frappe.new_doc("Quotation")
	new_doc.company = doc.company
	new_doc.party_name = doc.customer
	new_doc.project = ""
	# new_doc.sales_rep = doc.sales_rep
	if doc.company == "TSL COMPANY - UAE":
		new_doc.selling_price_list = "Standard Selling - UAE"
	new_doc.currency = frappe.db.get_value("Company",doc.company,"default_currency")
	new_doc.customer_name = frappe.db.get_value("Customer",doc.customer,"customer_name")
	new_doc.branch = doc.branch
	new_doc.project_data = doc.project
	
	# for i in doc.items:
		# new_doc.append("items",{
		# 	"item_code":i.sku,
		# 	"model":i.model_no,
		# 	"item_name":i.description,
		# 	"description":i.description,
		# 	"uom":'Nos',
		# 	"qty":i.qty,
		# 	"model_no":i.model,
		# 	"mfg":i.mfg,
		# 	"project_data":i.project,
		# })
		
	return new_doc


@frappe.whitelist()
def advance_pay(source):
	new_doc = frappe.new_doc("Payment Entry")
	doc = frappe.get_doc("Quotation",source)
	new_doc.payment_type = "Receive"
	new_doc.company = doc.company
	new_doc.branch = doc.branch_name
	new_doc.cost_center = doc.department
	for i in doc.items:
		new_doc.work_order_data = i.wod_no
		new_doc.supply_order_data = i.supply_order_data
	new_doc.paid_from = frappe.db.get_value("Account",{"account_type":["in",["Receivable"]],"is_group":0,"company":doc.company})
	new_doc.paid_from_account_currency = frappe.db.get_value("Company",doc.company,"default_currency")
	new_doc.party_type = "Customer"
	new_doc.party = doc.party_name
	new_doc.party_name = doc.customer_name
	new_doc.cost_center = doc.department
	return new_doc


@frappe.whitelist()
def final_price_validate(source):
	doc = frappe.get_doc("Quotation",source)
	return round(doc.after_discount_cost / doc.total_qty,2) or 0

@frappe.whitelist()
def final_price_validate_si(wod):
	qi_details = frappe.db.sql('''select q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where q.workflow_state = "Approved By Customer" and qi.wod_no = %s order by q.creation desc''',wod,as_dict=1)
	return qi_details

def update_cq(self, method):
	if self.quotation_type == "Customer Quotation - Repair" or self.quotation_type == "Customer Quotation - Supply" or self.quotation_type == "Revised Quotation - Repair" or self.quotation_type == "Revised Quotation - Supply"  or self.quotation_type == "Site Visit Quotation - Customer" or self.quotation_type == "Customer Quotation - Project":
		frappe.db.set_value(self.doctype, self.name, "workflow_state", "Quoted to Customer")
	if self.quotation_type == "Internal Quotation - Repair" or self.quotation_type == "Internal Quotation - Supply" or self.quotation_type == "Site Visit Quotation - Internal" or self.quotation_type == "Internal Quotation - Project":
			frappe.db.set_value(self.doctype, self.name, "workflow_state", "Waiting For Approval")
	
	if self.quotation_type == "Internal Quotation - Project" and self.project:
		p = frappe.get_doc("Project Data",self.project)
		p.status = "Pending Internal Approval"
		p.save()

	if self.quotation_type == "Customer Quotation - Project" and self.project:
		p = frappe.get_doc("Project Data",self.project)
		p.status = "Q-Quoted"
		p.save()
		
	# if self.items:
	# 	for i in self.items:
	# 		item = frappe.get_doc("Item",i.item_code)
	# 		for j in item.online_price_table:
	# 			frappe.errprint(j.item_code)
	# 			frappe.errprint(j.price)
	# 			self.append("price_list",{
	# 				"item_code":j.item_code,
	# 				"price_type":j.price_type,
	# 				"price":j.price,
	# 				"website":j.website,
	# 				"comments":j.comments
					

	# 				})
				# item.save(ignore_permissions = 1)


	# if self.quotation_type == "Quotation - Supply Tender":
	# 	s = self.name.replace("Q-", "")
	# 	frappe.db.set_value(self.doctype, self.name, "qtn_no",s)
	# if self.quotation_type == "Revised Quotation - Supply Tender":
	# 	s = self.name.replace("Q-", "")
	# 	frappe.db.set_value(self.doctype, self.name, "qtn_no",s)


# def get_pre_eval(self, method):
# 	if self.quotation_type == "Internal Quotation - Repair":
# 		if self.items:
# 			for i in self.items:
# 				if i.wod_no:
# 					ev = frappe.db.exists("Evaluation Report",{"work_order_data":i.wod_no})
# 					if not ev:
# 						pr  = frappe.get_doc("Quotation",self.name)
# 						pr.pre_evaluation = 1
# 						pr.save(ignore_permissions =1)


def on_update(self, method):
	# if self.workflow_state not in ["Rejected", "Rejected by Customer", "Approved","Approved By Management", "Approved By Customer", "Cancelled"]:
	# 	if self.quotation_type == "Internal Quotation - Repair" or self.quotation_type == "Internal Quotation - Supply":
	# 		frappe.db.set_value(self.doctype, self.name, "workflow_state", "Waiting For Approval")

		# else:
		# 	frappe.db.set_value(self.doctype, self.name, "workflow_state", "Quoted to Customer")
	# if self.quotation_type == "Customer Quotation - Repair" or self.quotation_type == "Revised Quotation - Repair":
	# 	if self.items:
	# 		for i in self.items:
	# 			wd = frappe.get_doc("Work Order Data",i.wod_no)
	# 			wd.quoted = 1
	# 			wd.save(ignore_permissions =1)
			

	if self.quotation_type == "Site Visit Quotation - Customer":
			sc = frappe.get_doc("Service Call Form",self.service_call_form)
			sc.status = "Quoted"
			sc.save(ignore_permissions = 1)

	if self.quotation_type == "Internal Quotation - Repair":
		for i in self.get("items"):
			if i.wod_no:
				doc = frappe.get_doc("Work Order Data",i.wod_no)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Management":
					doc.status = "IQ-Internally Quoted"
				else:
					doc.status = "Pending Internal Approval"

				doc.save(ignore_permissions=True)
	if self.quotation_type == "Internal Quotation - Supply":
		for i in self.get("items"):
			if i.supply_order_data:
				doc = frappe.get_doc("Supply Order Data",i.supply_order_data)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Management":
					doc.status = "Internal Quotation"	
				doc.save(ignore_permissions=True)
	if not self.quotation_type == "Internal Quotation - Repair":
		for i in self.get("items"):
			if i.wod_no:
				doc = frappe.get_doc("Work Order Data",i.wod_no)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Quoted to Customer":
					doc.status = "Q-Quoted"
					doc.is_quotation_created = 1
					doc.save(ignore_permissions=True)


				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Customer" and self.pre_evaluation == 0:
					doc.status = "A-Approved"
					doc.save(ignore_permissions=True)

				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Customer" and self.pre_evaluation == 1:
					doc.status = "NEA-Need Evaluation Approved"
					doc.save(ignore_permissions=True)


					# doc.save(ignore_permissions=True)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Rejected by Customer":
					# frappe.db.set_value("Work Order Data",i.wod_no,"is_quotation_created",0)
					doc.status =  "RNA-Return Not Approved"
					doc.save(ignore_permissions=True)
	if not self.quotation_type == "Internal Quotation - Supply":
		for i in self.get("items"):
			if i.supply_order_data:
				doc = frappe.get_doc("Supply Order Data",i.supply_order_data)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Quoted to Customer":
					doc.status = "Quoted"
					doc.save(ignore_permissions=True)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Customer":
					doc.status = "Approved"
					doc.save(ignore_permissions=True)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Rejected by Customer":
					# frappe.db.set_value("Work Order Data",i.wod_no,"is_quotation_created",0)
					doc.status =  "Not Approved"
					doc.save(ignore_permissions=True)

def before_submit(self,method):
	if self.supplier_quotation:
		frappe.db.set_value("Supplier Quotation",self.supplier_quotation,"quotation",self.name)
	if self.quotation_type == "Internal Quotation - Repair":
		for i in self.get("items"):
			if i.wod_no:
				frappe.db.set_value("Work Order Data",i.wod_no,"is_quotation_created",1)
		# if self.item_price_details:
		# 	for i in self.get("item_price_details"):
		# 		frappe.db.set_value("Item",{"item_name":i.item},"last_quoted_price",i.price)
		# 		frappe.db.set_value("Item",{"item_name":i.item},"last_quoted_client",self.party_name)
	if self.quotation_type == "Internal Quotation - Supply":
		d = {}
		for i in self.get('items'):
			if i.supplier_quotation:
				d[i.supplier_quotation] = []
		for i in self.get('items'):
			if i.supplier_quotation and i.item_code:
				if i.item_code not in d[i.supplier_quotation]:
					d[i.supplier_quotation].append(i.item_code)
		
		for k,v in d.items():
			to_add = []
			doc = frappe.get_doc("Supplier Quotation",k)
			for i in doc.get("items"):
				if i.item_code in v:
					to_add.append(i)
			doc.items = []
			for i in to_add:
				doc.append("items",i)
			doc.quotation = self.name
			doc.save(ignore_permissions= True)
			doc.submit()

		


	
				
#def validate(self, method):
#	items = self.get("items")
#	for item in items:
#		if item.wod_no:
#			eval_report = frappe.db.sql("""select * from `tabEvaluation Report` where work_order_data = '%s'"""%(item.wod_no),as_dict =1)
#			for eval in eval_report:
#				eval_time = eval.evaluation_time or 0
#				spent_time = eval.estimated_repair_time or 0
#				total_time = str(datetime.timedelta(seconds = eval_time + spent_time))
#				total_hrs = total_time.split(":")[0]
#				self.append("technician_hours_spent",{
#							"total_hours_spent":total_hrs,
#							"value":20,
#							"total_price":20*int(total_hrs),
#							"comments": eval.status
#						})
#		tech = self.technician_hours_spent
#		for t in tech:
#			self.actual_price += t.total_price
    			
#	if not self.edit_final_approved_price and self.quotation_type=="Internal Quotation - Repair":
#		self.overall_discount_amount = (self.final_approved_price * self.discount_percent)/100
#		self.final_approved_price -= self.overall_discount_amount
#		self.final_approved_price += self.margin_rate
#	l = []
#	if self.quotation_type == "Internal Quotation - Repair":
#		for i in self.get("items"):
#			if i.item_name:
#				item = frappe.db.sql('''select parent,item_name,rate from `tabQuotation Item` where parenttype = "Quotation" and item_name = %s and docstatus = 1 order by creation desc''',i.item_name,as_dict=1)
#				for j in item:
#					if frappe.db.get_value("Quotation",j['parent'],"quotation_type") == "Internal Quotation - Repair":
#						l.append({
#							"item":j['item_name'],
#							"client":frappe.db.get_value("Quotation",j['parent'],"party_name"),
#							"price":j['rate'],
#
#						})
#		self.similar_items_quoted_before = []
#		for i in range(len(l)):
#			if i==3:
#				break
#			self.append("similar_items_quoted_before",l[i])

def send_qtn_reminder_mail():
	q = frappe.get_all("Quotation",{"workflow_state":"Quoted to Customer", "transaction_date": [">","2024-03-01"]},["*"])
	data = []
	data_2 = []
	for i in q:
		if i.quotation_type ==  "Customer Quotation - Repair":
			qu = frappe.db.sql(""" select `tabQuotation Item`.wod_no as wo from `tabQuotation` 
					left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
					where `tabQuotation`.name = "%s" """ %(i.name) ,as_dict=1)
			
			wod = frappe.db.exists("Work Order Data",{"status":"Q-Quoted","name":qu[0]["wo"]})
			if wod:
				if qu[0]["wo"] not in data:
					data.append(i.name)
		if i.quotation_type ==  "Customer Quotation - Supply":
			qu = frappe.db.sql(""" select `tabQuotation Item`.supply_order_data as so from `tabQuotation` 
					left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
					where `tabQuotation`.name = "%s" """ %(i.name) ,as_dict=1)
			
			wod = frappe.db.exists("Supply Order Data",{"status":"Quoted","name":qu[0]["so"]})
			if wod:
				if qu[0]["so"] not in data_2:
					data_2.append(i.name)

	for s in data:
		cus = frappe.get_value("Quotation",{"name":s},["party_name"])
		original_string = s
		mod = original_string.replace("REP-", "").replace("CUS-", "")
	

		if cus:
			email = frappe.get_value("Customer",{"name":cus},["email_id"])
			if email:
				print(email)
				msg = """Dear Sir,<br><br>
				I hope this message ﬁnds you well.<br><br>
				I am writing to follow up on the quotation we sent earlier Ref.No : [%s]. We
				wanted to ensure you received the quotation and to see if you have any questions or require
				further information.<br><br>
				If you need any adjustments to the quotation or have any concerns, please let us know, and we be glad to assist.<br><br>
				Thank you once again for considering TSL COMPANY.<br><br>
				Best regards,<br>"""%(mod)
				
				msg1="""<div><style>.sh-src a{text-decoration:none!important;}</style></div> <br> <table cellpadding="0" cellspacing="0" border="0" class="sh-src" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td align="center" style="padding: 0px 18px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 13px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/file/5r1rjllxn18j0p" alt="" title="Profile Picture" width="100" height="100" class="" style="display: block; border: 0px; max-width: 100px;"></p></td></tr></table> <table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://tsl-me.com/" target="_blank"><img src="https://signaturehound.com/api/v1/file/3lwizllxn10tyt" alt="" title="Logo" width="150" height="50" style="display: block; border: 0px; max-width: 150px;"></a></p></td></tr></table></td> <td width="5" style="padding: 1px 0px 0px;"></td> <td style="padding: 0px 1px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 10px 0px; border-bottom: 2px solid rgb(0,92,163); font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap;"><p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; font-weight: 700; color: rgb(0,92,163); white-space: nowrap; margin: 1px;">Mohammed K Daddy</p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">Customer Support Officer</p> <!----> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">TSL Group | Kuwait</p></td></tr> <tr><td style="padding: 10px 1px 10px 0px; border-bottom: 2px solid rgb(0,92,163);"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/email/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="mailto:info@tsl-me.com" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">info@tsl-me.com</span></a>
				</p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/direct/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="tel:+96524741313" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">+965 24741313</span></a></p></td></tr><tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/fax/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="tel:+96524741311" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">+965 24741311</span></a></p></td></tr> <tr><td valign="top" style="padding: 1px 5px 1px 0px; vertical-align: top;"><p style="margin: 1px;">
				<img src="https://signaturehound.com/api/v1/png/map/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://www.google.com/maps/place/TSL+For+Industrial+Electronics+Repairing+%26+Supply+-+Kuwait/@29.3082683,47.9352691,18z/data=!4m6!3m5!1s0x3fcf9a9068440231:0x7321607de759fdc1!8m2!3d29.3082309!4d47.9365244!16s%2Fg%2F11c0rlsd_t?entry=ttu" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">Bldg: 1473, Unit: 13, Street: 24, Block: 1,<br>Al Rai Industrial Area, Kuwait</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/website/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,162) !important; font-weight: 700; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://tsl-me.com/" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,163); font-weight: 700; text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,163); font-weight: 700; text-decoration: none !important;">tsl-me.com</span></a></p></td></tr></table></td></tr> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.linkedin.com/company/tsl-me/mycompany/" target="_blank"><img src="https://signaturehound.com/api/v1/png/linkedin/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;">
				<a href="https://x.com/tsl_mecompany?s=11&amp;t=Zxza0-9Q_18nsDCddfTQPw" target="_blank"><img src="https://signaturehound.com/api/v1/png/x/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.instagram.com/tslcom/?igshid=MzRlODBiNWFlZA%3D%3D" target="_blank"><img src="https://signaturehound.com/api/v1/png/instagram/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.facebook.com/people/TSL-Industrial-Electronics-Services/61550277093129/" target="_blank"><img src="https://signaturehound.com/api/v1/png/facebook/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.youtube.com/@TSLELECTRONICSSERVICES" target="_blank"><img src="https://signaturehound.com/api/v1/png/youtube/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td></tr></table></td></tr></table></td></tr></table></td></tr> <!----> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: 0px; border-collapse: collapse;"><tr><td style="padding: 15px 1px 0px 0px; font-family: Arial, sans-serif; font-size: 10px; line-height: 12px; color: rgb(136,136,136);"><p style="font-family: Arial, sans-serif; font-size: 10px; line-height: 12px; color: rgb(136,136,136); margin: 1px;">The content of this email is confidential and intended for the recipient specified in message only. It is strictly forbidden to share any part of this message with any third party, without a written consent of the sender. If you received this message by mistake, please reply to this message and follow with its deletion, so that we can ensure such a mistake does not occur in the future.</p></td></tr></table></td></tr> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td valign="middle" style="padding: 15px 4px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"></p></td> <td style="font-family: Arial, sans-serif; color: rgb(136,136,135) !important; font-weight: 700; font-size: 10px; line-height: 15px; padding: 15px 0px 1px; vertical-align: middle;"><p style="margin: 1px;"</p></td></tr></table></td></tr> <!----></table>"""
				
				frappe.sendmail(
				recipients=["yousuf@tsl-me.com"],
				sender= "Notification from TSL <info@tsl-me.com>",
				subject = "Quotation"+" "+str(mod),
				message = msg+msg1,
				attachments=get_attachments(s,"Quotation")
				)

	for s in data_2:
		
		cus = frappe.get_value("Quotation",{"name":s},["party_name"])
		original_string = s
		mod = original_string.replace("SUP-", "").replace("CUS-", "")
		
		if cus:
			email = frappe.get_value("Customer",{"name":cus},["email_id"])
			if email:
				msg = """Dear Sir,<br><br>
				I hope this message ﬁnds you well.<br><br>
				I am writing to follow up on the quotation we sent earlier Ref.No : [%s]. We
				wanted to ensure you received the quotation and to see if you have any questions or require
				further information.<br><br>
				If you need any adjustments to the quotation or have any concerns, please let us know, and we be glad to assist.<br><br>
				Thank you once again for considering TSL COMPANY.<br><br>
				Best regards,<br>"""%(mod)
				
				msg1="""<div><style>.sh-src a{text-decoration:none!important;}</style></div> <br> <table cellpadding="0" cellspacing="0" border="0" class="sh-src" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td align="center" style="padding: 0px 18px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 13px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/file/5r1rjllxn18j0p" alt="" title="Profile Picture" width="100" height="100" class="" style="display: block; border: 0px; max-width: 100px;"></p></td></tr></table> <table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://tsl-me.com/" target="_blank"><img src="https://signaturehound.com/api/v1/file/3lwizllxn10tyt" alt="" title="Logo" width="150" height="50" style="display: block; border: 0px; max-width: 150px;"></a></p></td></tr></table></td> <td width="5" style="padding: 1px 0px 0px;"></td> <td style="padding: 0px 1px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 10px 0px; border-bottom: 2px solid rgb(0,92,163); font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap;"><p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; font-weight: 700; color: rgb(0,92,163); white-space: nowrap; margin: 1px;">Mohammed K Daddy</p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">Customer Support Officer</p> <!----> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">TSL Group | Kuwait</p></td></tr> <tr><td style="padding: 10px 1px 10px 0px; border-bottom: 2px solid rgb(0,92,163);"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/email/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="mailto:info@tsl-me.com" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">info@tsl-me.com</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/direct/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="tel:+96524741313" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">+965 24741313</span></a></p></td></tr><tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/fax/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="tel:+96524741311" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">+965 24741311</span></a></p></td></tr> <tr><td valign="top" style="padding: 1px 5px 1px 0px; vertical-align: top;"><p style="margin: 1px;">
				<img src="https://signaturehound.com/api/v1/png/map/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://www.google.com/maps/place/TSL+For+Industrial+Electronics+Repairing+%26+Supply+-+Kuwait/@29.3082683,47.9352691,18z/data=!4m6!3m5!1s0x3fcf9a9068440231:0x7321607de759fdc1!8m2!3d29.3082309!4d47.9365244!16s%2Fg%2F11c0rlsd_t?entry=ttu" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">Bldg: 1473, Unit: 13, Street: 24, Block: 1,<br>Al Rai Industrial Area, Kuwait</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/website/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,162) !important; font-weight: 700; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://tsl-me.com/" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,163); font-weight: 700; text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,163); font-weight: 700; text-decoration: none !important;">tsl-me.com</span></a></p></td></tr></table></td></tr> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.linkedin.com/company/tsl-me/mycompany/" target="_blank"><img src="https://signaturehound.com/api/v1/png/linkedin/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;">
				<a href="https://x.com/tsl_mecompany?s=11&amp;t=Zxza0-9Q_18nsDCddfTQPw" target="_blank"><img src="https://signaturehound.com/api/v1/png/x/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.instagram.com/tslcom/?igshid=MzRlODBiNWFlZA%3D%3D" target="_blank"><img src="https://signaturehound.com/api/v1/png/instagram/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.facebook.com/people/TSL-Industrial-Electronics-Services/61550277093129/" target="_blank"><img src="https://signaturehound.com/api/v1/png/facebook/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.youtube.com/@TSLELECTRONICSSERVICES" target="_blank"><img src="https://signaturehound.com/api/v1/png/youtube/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td></tr></table></td></tr></table></td></tr></table></td></tr> <!----> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: 0px; border-collapse: collapse;"><tr><td style="padding: 15px 1px 0px 0px; font-family: Arial, sans-serif; font-size: 10px; line-height: 12px; color: rgb(136,136,136);"><p style="font-family: Arial, sans-serif; font-size: 10px; line-height: 12px; color: rgb(136,136,136); margin: 1px;">The content of this email is confidential and intended for the recipient specified in message only. It is strictly forbidden to share any part of this message with any third party, without a written consent of the sender. If you received this message by mistake, please reply to this message and follow with its deletion, so that we can ensure such a mistake does not occur in the future.</p></td></tr></table></td></tr> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td valign="middle" style="padding: 15px 4px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"></p></td> <td style="font-family: Arial, sans-serif; color: rgb(136,136,135) !important; font-weight: 700; font-size: 10px; line-height: 15px; padding: 15px 0px 1px; vertical-align: middle;"><p style="margin: 1px;"</p></td></tr></table></td></tr> <!----></table>"""
				
				frappe.sendmail(
				recipients=["yousuf@tsl-me.com"],
				sender= "Notification from TSL <info@tsl-me.com>",
				subject = "Quotation"+" "+str(mod),
				message = msg+msg1,
				attachments= get_attachments_supply(s,"Quotation")
				)
	# for i in frappe.db.sql('''select  q.name as name,c.email_id as email_id,q.branch_name as branch,q.is_email_sent as ecount,q.party_name as customer_name from `tabQuotation` as q join `tabCustomer` as c on c.name = q.party_name where q.docstatus = 0 and 
	# 			q.workflow_state = 'Quoted to Customer' ''',as_dict=1):
	# 	receiver = []
	# 	receiver.append(i['email_id'])
	# 	sender = frappe.db.get_value("Email Account",{"branch":i['branch']},"email_id")
	# 	doctype = "Quotation"
	# 	name = i['name']
		# msg = '''Dear Mr./Ms. %s,{Dear Sir,}<br>We would like to remind you about the Quotation (WO/ Quotation Ref.: %s) sent earlier.<br>Kindly advise in order to proceed with
		# 	work or we will return the unit in your facility.<br><br>Your quick response will be highly appreciated.'''%(i['customer_name'],i['name'])
	# 	if not i['ecount']:
	# 		msg = '''Dear Mr./Ms. %s,{Dear Sir,}<br>We would like to remind you about the Quotation (WO/ Quotation Ref.: %s) sent earlier. We have<br>attached the quotation
	# 			for your reference.<br><br>We look forward to your approval of the work.'''%(i['customer_name'],i['name'])

	# 	if len(receiver):
	# 		try:
	# 			frappe.sendmail(
	# 				recipients = receiver,
	# 				sender = sender,
	# 				subject = str(doctype)+" "+str(name),
	# 				message = msg,
	# 				attachments=get_attachments(name,doctype)
	# 			)
	# 			print("Email sent")
	# 			frappe.db.set_value("Quotation",name,"is_email_sent",1)
	# 		except frappe.OutgoingEmailError as e:
	# 			print(str(e))

def get_attachments(name,doctype):
	attachments = frappe.attach_print(doctype, name,file_name=doctype, print_format="Quotation TSL")
	return [attachments]

def get_attachments_supply(name,doctype):
	attachments = frappe.attach_print(doctype, name,file_name=doctype, print_format="Supply Quotation")
	return [attachments]


# @frappe.whitelist()
# def create_wallet_balance():
# 	import requests
# 	url = "https://apimaqadhe.ribox.me/rest/all/V1/walletsystem/wallet/list"
# 	payload={}
# 	headers = {
# 	}
# 	response = requests.request("GET", url, headers=headers, data=payload)
# 	resp = json.loads(response.text)
# 	l = []
# 	for i in resp["walletList"]:
# 		if not frappe.db.get_value("Wallet Balances",{"customer_name":i["customer_name"],"customer_mail":i["customer_mail"],"customer_id":i["customer_id"]}):
# 			print("no wallet balance")
# 			i["doctype"] = "Wallet Balances"
# 			customer = frappe.db.get_value("Customer",{"customer_name":i["customer_name"],"email_id":i["customer_mail"]})
# 			if customer:
# 				if not frappe.db.get_value("Customer",customer,"customer_id"):
# 							frappe.db.set_value("Customer",customer,"customer_id",i["customer_id"])
# 			else:
# 				customer = create_customer(i)
# 			i["customer"] = customer
# 			doc = frappe.get_doc(i)
# 			doc.insert(ignore_permissions = True)
# 			if doc.name:
# 				l.append("created = "+doc.name)
# 		else:
# 			wallet = frappe.db.sql('''select name from `tabWallet Balances` where customer_name = %s and customer_id = %s
# 			and customer_mail = %s and updated_at < %s ''',(i["customer_name"],i["customer_id"],i["customer_mail"],i["updated_at"]),as_dict=1)
# 			wallet = wallet[0]["name"] if wallet else None
# 			if wallet:
# 				doc = frappe.get_doc("Wallet Balances",wallet)
# 				doc.total_amount = i["total_amount"]
# 				doc.remaining_amount = i["remaining_amount"]
# 				doc.used_amount = i["used_amount"]
# 				doc.updated_at = i["updated_at"]
# 				doc.save(ignore_permissions = True)
# 				if doc.name:
# 					l.append("updated = "+doc.name)


# 	return l

# def create_customer(order_doc):
# 	doc = frappe.get_doc(dict(
# 		doctype = "Customer",
# 		customer_name = order_doc['customer_name'],
# 		email_id = order_doc['customer_mail'],
# 		customer_id = order_doc['customer_id'],
# 		customer_group = frappe.db.get_value("Wallet Settings","Wallet Settings","customer_group"),
# 		territory = frappe.db.get_value("Wallet Settings","Wallet Settings","territory")
# 	)).insert(ignore_permissions = True)
# 	return doc.name

# @frappe.whitelist()
# def get_wallet_transactions():
# 	emails = frappe.db.sql('''select distinct(customer_mail) from `tabWallet Balances` ''',as_list=1)
# 	emails= [i[0] for i in emails]
# 	l=[]
# 	print(emails)
# 	for i in emails:
# 		l.append(i)
# 		url = "https://apimaqadhe.ribox.me/rest/all/V1/walletsystem/transaction/"+str(i)
# 		payload={}
# 		headers = {}
# 		response = requests.request("GET", url, headers=headers, data=payload)
# 		resp = json.loads(response.text)
# 		if resp["transactionList"] == "No Data Found!":
# 			continue
# 		for j in resp["transactionList"]:
# 			cwb = frappe.db.sql('''select name from `tabConnector Wallet Transactions`  where customer_mail = %s
# 				and transaction_at = %s ''',(j["customer_mail"],j["transaction_at"]),as_dict=1)
# 			if not cwb:
# 				j["doctype"] = "Connector Wallet Transactions"
# 				j["api_status"] = j["status"]
# 				del j["status"]
# 				j["retry_limit"] = 5
# 				doc = frappe.get_doc(j)
# 				doc.insert(ignore_permissions = True)
# 				l.append(doc.name)
# 				l.append("         ")
# 	return l
	
# @frappe.whitelist()
# def create_jv_for_transactions(tsn_id = None):
# 	filter = ""
# 	if tsn_id:
# 		filter  += "and name = '{0}' ".format(tsn_id)
# 	cwb = frappe.db.sql('''select sender_type,mode_of_payment,amount,customer_id,name,retry_limit,is_sync,transaction_note from `tabConnector Wallet Transactions` where is_sync = 0
# 			and status = "Pending" and action = "credit" and retry_limit > 0 {0} order by creation asc limit 10'''.format(filter),as_dict =1)
# 	pay_mode = frappe.db.get_value("Wallet Settings","Wallet Settings","default_mode_of_payment")
# 	for i in cwb:
# 		if i["is_sync"]:
# 				continue
# 		frappe.db.set_value("Connector Wallet Transactions",i["name"],"retry_limit",int(i["retry_limit"])-1)
# 		mod_account = ""
# 		if i["sender_type"] == "Recharge wallet":
# 			mod_account = frappe.db.get_value("Mode of Payment Account",{"parent":pay_mode},"default_account")
# 		elif i["sender_type"] == "Admin credit" or i["sender_type"] == "Admin debit":
# 			mod_account = frappe.db.get_value("Wallet Settings","Wallet Settings","adjustment_account")
# 		else:
# 			continue
# 		doc = frappe.new_doc("Journal Entry")
# 		doc.posting_date = frappe.utils.today()
# 		db_amt = 0
# 		cr_amt = 0
# 		db_amt = i["amount"]
# 		if i["sender_type"] == "Admin debit":
# 			db_amt = 0
# 			cr_amt = i["amount"]
# 		doc.append("accounts",{
# 			"account":mod_account,
# 			"debit_in_account_currency":db_amt,
# 			"credit_in_account_currency":cr_amt
# 		})
# 		customer_account = frappe.db.get_value("Wallet Settings","Wallet Settings","account")
# 		customer = frappe.db.get_value("Customer",{"customer_id":i["customer_id"]})
# 		ref_doc = i["transaction_note"]
# 		doc.append("accounts",{
# 			"account":customer_account,
# 			"party_type":"Customer",
# 			"party":customer,
# 			"credit_in_account_currency":db_amt,
# 			"debit_in_account_currency":cr_amt,
# 			"user_remark":ref_doc
# 		})
# 		doc.save(ignore_permissions = True)
# 		if doc.name:
# 			frappe.db.set_value("Connector Wallet Transactions",i["name"],"reference_id",doc.name)
# 			if frappe.db.get_value("Wallet Settings","Wallet Settings","submit_journal_entry"):
# 				print("submit")
# 				try:
# 					doc.submit()
# 				except Exception as e:
# 					frappe.log_error(frappe.get_traceback())
# 					continue
# 			frappe.db.set_value("Connector Wallet Transactions",i["name"],"is_sync",1)
# 			frappe.db.set_value("Connector Wallet Transactions",i["name"],"status","Synced")
# 			link = "<a href='/desk#Form/Journal%20Entry/{0}'>{0}</a>".format(doc.name)
# 			frappe.msgprint("Transaction synced against {0}".format(link) )
# 	return 0
