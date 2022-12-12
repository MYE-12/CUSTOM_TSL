
from pydoc import doc
from re import L
import frappe
import json
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def get_wod_items(wod):
	wod = json.loads(wod)
	l=[]
	for k in list(wod):
		tot = frappe.db.sql('''select sum(total_amount) as total_amount  from `tabEvaluation Report` where work_order_data = %s and docstatus=1 ''',k,as_dict=1)[0]["total_amount"]
		# if not tot:
		# 	link = []
		# 	link.append(""" <a href='/app/work-order-data/{0}'>{0}</a> """.format(k))
		# 	frappe.throw("No Part Sheet created for this Work Order"+"-".join(link))
		# 	continue
		doc = frappe.get_doc("Work Order Data",k)
		branch = doc.branch
		if not tot:
			tot = 0
		for i in doc.get("material_list"):
			l.append(frappe._dict({
				"item" :i.item_code,
				"item_name" : i.item_name0,
				"description":i.item_name,
				"wod": k,
				"type": i.type,
				"model_no": i.model_no,
				"serial_no": i.serial_no,
				"qty": i.quantity,
				"sales_rep":doc.sales_rep,
				"total_amt":float(tot)/float(i.quantity),
				"branch":branch,

			}))
			
	return l

@frappe.whitelist()
def get_sqtn_items(sod):
	sod = json.loads(sod)
	l=[]
	for k in list(sod):
		l += frappe.db.sql('''select si.item_code,si.mfg,si.model,si.type,si.serial_no,si.item_name,si.uom,si.stock_uom,si.conversion_factor,si.qty,si.rate,si.amount,s.name as sqtn,s.supply_order_data as sod from `tabSupplier Quotation` as s inner join `tabSupplier Quotation Item` as si on si.parent = s.name where s.docstatus = 0 and s.supply_order_data = %s and s.workflow_state = 'Waiting For Approval' order by s.creation''',k,as_dict =1)
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
					for sod in frappe.db.sql('''select parent from `tabMaterial List` where model_no = %s and mfg = %s and type = %s and serial_no = %s and parenttype = "Supply Order Data" ''',(i.model_no,i.mfg,i.type,i.serial_no),as_dict=1):
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

def before_save(self,method):
	if self.quotation_type == "Internal Quotation - Repair":
		self.item_price_details=[]
		self.similar_items_quoted_before=[]
		for i in self.get("items"):
			part_sheet = frappe.db.sql('''select name from `tabEvaluation Report` where work_order_data = %s and docstatus = 1 order by creation desc''',i.wod_no,as_dict=1)
			for j in part_sheet:
				doc = frappe.get_doc("Evaluation Report",j['name'])
				for k in doc.get("items"):
					if frappe.db.get_value("Item",k.part,"last_quoted_price") >= 0 and frappe.db.get_value("Item",k.part,"last_quoted_client"):
						self.append("similar_items_quoted_before",{
							"item":k.part_name,
							"client":frappe.db.get_value("Item",k.part,"last_quoted_client"),
							"price":frappe.db.get_value("Item",k.part,"last_quoted_price")
						})

					if frappe.db.get_value("Bin",{"item_code":k.part},"actual_qty"):
						price = frappe.db.get_value("Item",{"item_code":k.part},"valuation_rate") or frappe.db.get_value("Bin",{"item_code":k.part},"valuation_rate")
						source = "TSL Inventory"
						if k.parts_availability == "No":
							source = "Supplier"
					else:
						price = k.price_ea
						source = "Supplier"
					sq_no = frappe.db.sql('''select sq.name as sq from `tabSupplier Quotation` as sq inner join `tabSupplier Quotation Item` as sqi 
					where sq.work_order_data = %s and sqi.item_code = %s and sq.workflow_state = "Approved" order by sq.transaction_date desc limit 1''',(doc.work_order_data,k.part),as_dict=1)
					if sq_no:
						sq_no = sq_no[0]["sq"]
						self.append("item_price_details",{
							"item":k.part,
							"item_source":source,
							"price":price,
							"supplier_quotation":sq_no

						})
						frappe.db.set_value("Supplier Quotation",sq_no,"quotation",self.name)
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




	
@frappe.whitelist()
def get_quotation_history(source,rate = None,type = None):
	target_doc = frappe.new_doc("Quotation")
	doc = frappe.get_doc("Quotation",source)

	def postprocess(source, target_doc):
		target_doc.quotation_type = type
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
	if rate:
		for i in range(len(doclist.items)):
			doclist.items[i].rate += float(rate)
	return doclist

@frappe.whitelist()
def create_sal_inv(source):
	target_doc = frappe.new_doc("Sales Invoice")
	doc = frappe.get_doc("Quotation",source)
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
	for i in doclist.get('items'):
		doclist.department = frappe.db.get_value("Work Order Data",i.wod_no,"department")
	return doclist

@frappe.whitelist()
def final_price_validate(source):
	doc = frappe.get_doc("Quotation",source)
	return round(doc.final_approved_price / doc.total_qty,2)

@frappe.whitelist()
def final_price_validate_si(wod):
	qi_details = frappe.db.sql('''select q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where q.workflow_state = "Approved By Customer" and qi.wod_no = %s order by q.creation desc''',wod,as_dict=1)
	return qi_details

def on_update(self, method):
	if self.workflow_state not in ["Rejected", "Rejected by Customer", "Approved", "Approved By Customer", "Cancelled"]:
		if self.quotation_type == "Internal Quotation - Repair" or self.quotation_type == "Internal Quotation - Supply":
			frappe.db.set_value(self.doctype, self.name, "workflow_state", "Waiting For Approval")

		else:
			frappe.db.set_value(self.doctype, self.name, "workflow_state", "Quoted to Customer")
	if self.quotation_type == "Internal Quotation - Repair":
		for i in self.get("items"):
			if i.wod_no:
				doc = frappe.get_doc("Work Order Data",i.wod_no)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved":
					doc.status = "IQ-Internally Quoted"	
				doc.save(ignore_permissions=True)
	if self.quotation_type == "Internal Quotation - Supply":
		for i in self.get("items"):
			if i.supply_order_data:
				doc = frappe.get_doc("Supply Order Data",i.supply_order_data)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved":
					doc.status = "IQ-Internally Quoted"	
				doc.save(ignore_permissions=True)
	if not self.quotation_type == "Internal Quotation - Repair":
		for i in self.get("items"):
			if i.wod_no:
				doc = frappe.get_doc("Work Order Data",i.wod_no)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Quoted to Customer":
					doc.status = "Q-Quoted"
					doc.save(ignore_permissions=True)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Customer":
					doc.status = "A-Approved"
					doc.save(ignore_permissions=True)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Rejected by Customer":
					# frappe.db.set_value("Work Order Data",i.wod_no,"is_quotation_created",0)
					doc.status =  "RNA-Return Not Approved"
					doc.save(ignore_permissions=True)
	if not self.quotation_type == "Internal Quotation - Supply":
		for i in self.get("items"):
			if i.supply_order_data:
				doc = frappe.get_doc("Supply Order Data",i.supply_order_data)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Quoted to Customer":
					doc.status = "Q-Quoted"
					doc.save(ignore_permissions=True)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Customer":
					doc.status = "A-Approved"
					doc.save(ignore_permissions=True)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Rejected by Customer":
					# frappe.db.set_value("Work Order Data",i.wod_no,"is_quotation_created",0)
					doc.status =  "RNA-Return Not Approved"
					doc.save(ignore_permissions=True)

def before_submit(self,method):
	if self.supplier_quotation:
		frappe.db.set_value("Supplier Quotation",self.supplier_quotation,"quotation",self.name)
	if self.quotation_type == "Internal Quotation - Repair":
		for i in self.get("items"):
			if i.wod_no:
				frappe.db.set_value("Work Order Data",i.wod_no,"is_quotation_created",1)
		if self.item_price_details:
			for i in self.get("item_price_details"):
				frappe.db.set_value("Item",{"item_name":i.item},"last_quoted_price",i.price)
				frappe.db.set_value("Item",{"item_name":i.item},"last_quoted_client",self.party_name)
	if self.quotation_type == "Internal Quotation - Supply":
		d = {}
		for i in self.get('items'):
			if i.supplier_quotation:
				d[i.supplier_quotation] = []
		for i in self.get('items'):
			if i.supplier_quotation and i.item_code:
				if i.item_code not in d[i.supplier_quotation]:
					d[i.supplier_quotation].append(i.item_code)
		print(d)
		
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

		


	
				
def validate(self, method):
	if not self.edit_final_approved_price and self.quotation_type=="Internal Quotation - Repair":
		self.final_approved_price = self.actual_price*302.8/100+self.actual_price
	l = []
	if self.quotation_type == "Internal Quotation - Repair":
		for i in self.get("items"):
			if i.item_name:
				item = frappe.db.sql('''select parent,item_name,rate from `tabQuotation Item` where parenttype = "Quotation" and item_name = %s and docstatus = 1 order by creation desc''',i.item_name,as_dict=1)
				for j in item:
					if frappe.db.get_value("Quotation",j['parent'],"quotation_type") == "Internal Quotation - Repair":
						l.append({
							"item":j['item_name'],
							"client":frappe.db.get_value("Quotation",j['parent'],"party_name"),
							"price":j['rate'],

						})
		self.similar_items_quoted_before = []
		for i in range(len(l)):
			if i==3:
				break
			self.append("similar_items_quoted_before",l[i])
		
