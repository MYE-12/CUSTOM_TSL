	
from pydoc import doc
from re import L
import frappe
import json
from frappe.model.mapper import get_mapped_doc
from frappe import get_print
import datetime
@frappe.whitelist()
def get_wod_items(wod):
	wod = json.loads(wod)
	l=[]
	for k in list(wod):
		tot = 0
		tot = frappe.db.sql('''select sum(total_amount) as total_amount  from `tabEvaluation Report` where work_order_data = %s and docstatus=1 group by work_order_data''',k,as_dict=1)
		frappe.errprint(tot)
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
		l += frappe.db.sql('''select si.item_code as item_code,si.mfg as manufacturer,si.supplier_quotation as sqtn,si.model_no as model_no,si.type as type,si.serial_no as serial_no,si.item_name as item_name,"Nos" as uom,"Nos" as stock_uom,1 as conversion_factor,si.quantity as qty,si.price as rate,si.amount as amount,s.name as sod from `tabSupply Order Table` as si inner join `tabSupply Order Data` as s on si.parent = s.name where s.docstatus = 1 and s.name = %s order by s.modified''',k,as_dict =1)
		l += frappe.db.sql('''select si.part as item_code,si.manufacturer as manufacturer,si.supplier_quotation as sqtn,si.model as model_no,si.type as type,si.serial_no as serial_no,si.part_name as item_name,"Nos" as uom,"Nos" as stock_uom,1 as conversion_factor,si.qty as qty,si.price_ea as rate,si.total as amount,s.name as sod from `tabPart Sheet Item Supply` as si inner join `tabSupply Order Data` as s on si.parent = s.name where s.docstatus = 1 and s.name = %s order by s.modified''',k,as_dict =1)
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
		tc = self.technician_hours_spent
		for t in tc:
			labour_value = t.total_price
		for i in self.get("items"):
			total_qtn_rate = 0
			part_sheet = frappe.db.sql('''select name from `tabEvaluation Report` where work_order_data = %s and docstatus = 1 order by creation desc''',i.wod_no,as_dict=1)
			part_sheet_ini = frappe.db.sql('''select name from `tabInitial Evaluation` where work_order_data = %s and docstatus = 0 order by creation desc''',i.wod_no,as_dict=1)
			# frappe.errprint(part_sheet_ini)
			for j in  part_sheet_ini:
				# frappe.errprint(j)
				doc = frappe.get_doc("Initial Evaluation",j['name']) 
				for k in doc.get("items"):
					frappe.errprint(k)
					total_qtn_rate += k.total
					# frappe.errprint(total_qtn_rate)
#					if frappe.db.get_value("Item",k.part,"last_quoted_price") >= 0 and frappe.db.get_value("Item",k.part,"last_quoted_client"):
#						self.append("similar_items_quoted_before",{
#							"item":k.part_name,
#							"client":frappe.db.get_value("Item",k.part,"last_quoted_client"),
#							"price":frappe.db.get_value("Item",k.part,"last_quoted_price")
#						})
					if k.parts_availability == "No":
						source = "Supplier"
						price = k.price_ea
						sq_no = frappe.db.sql('''select sq.name as sq from `tabSupplier Quotation` as sq inner join `tabSupplier Quotation Item` as sqi on sqi.parent = sq.name 
                                        			where sq.docstatus = 1 and sq.work_order_data = %s and sqi.item_code = %s and sq.workflow_state = "Approved By Management" 
								order by sq.modified desc limit 1''',(doc.work_order_data,k.part),as_dict=1)
						frappe.errprint(sq_no)
						if len(sq_no):
							sq_no = sq_no[0]["sq"]
						else:
							sq_no =  ""
					else:
						price = k.price_ea
						frappe.errprint(pr)
						source = "TSL Inventory"
						sq_no = ""
					self.append("item_price_details",{
						"item":k.part,
						"item_source":source,
						"model":k.model,
						"amount":k.total,
						"supplier_quotation":sq_no

					})
					if sq_no:
						frappe.db.set_value("Supplier Quotation",sq_no,"quotation",self.name)

			for j in  part_sheet:
				# frappe.errprint(j)
				doc = frappe.get_doc("Evaluation Report",j['name']) 
				for k in doc.get("items"):
					total_qtn_rate += k.total
					# frappe.errprint(total_qtn_rate)
#					if frappe.db.get_value("Item",k.part,"last_quoted_price") >= 0 and frappe.db.get_value("Item",k.part,"last_quoted_client"):
#						self.append("similar_items_quoted_before",{
#							"item":k.part_name,
#							"client":frappe.db.get_value("Item",k.part,"last_quoted_client"),
#							"price":frappe.db.get_value("Item",k.part,"last_quoted_price")
#						})
					if k.parts_availability == "No":
						source = "Supplier"
						price = k.price_ea
						sq_no = frappe.db.sql('''select sq.name as sq from `tabSupplier Quotation` as sq inner join `tabSupplier Quotation Item` as sqi on sqi.parent = sq.name 
                                        			where sq.docstatus = 1 and sq.work_order_data = %s and sqi.item_code = %s and sq.workflow_state = "Approved By Management" 
								order by sq.modified desc limit 1''',(doc.work_order_data,k.part),as_dict=1)
						if len(sq_no):
							sq_no = sq_no[0]["sq"]
						else:
							sq_no =  ""
					else:
						price = k.price_ea
						source = "TSL Inventory"
						sq_no = ""
					self.append("item_price_details",{
						"item":k.part,
						"item_source":source,
						"model":k.model,
						"supplier_quotation":sq_no

					})
					if sq_no:
						frappe.db.set_value("Supplier Quotation",sq_no,"quotation",self.name)
			i.amount = total_qtn_rate /i.qty + labour_value
			i.rate = total_qtn_rate/i.qty + labour_value
			self.actual_price = i.rate
		if self.final_approved_price:
			self.in_words1 = frappe.utils.money_in_words(self.final_approved_price) or "Zero"
	
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
			suqb = frappe.db.sql('''select q.party_name as customer,qi.parent as quotation_no,qi.wod_no as work_order_data,qi.supply_order_data as supply_order_data ,qi.rate as quoted_price
				,qi.item_code as sku,qi.model_no as model,qi.type as type,qi.manufacturer as mfg from `tabQuotation` as q inner join `tabQuotation Item` as qi
				on qi.parent=q.name where qi.item_code = %s and q.workflow_state = "Approved By Customer" and q.docstatus = 1 and q.name != %s''',(i.item_code,self.name),as_dict =1 )
			if suqb:
				# frappe.errprint(suqb)
				self.previously_quoted_unit = []
				for j in suqb:
					# frappe.errprint(j)
					if j.work_order_data:
						w_doc = frappe.get_doc("Work Order Data",j.work_order_data)
					
						self.append("previously_quoted_unit",{
						"customer":j.customer,
						"sku":j.sku,
						"model":j.model,
						"type":j.type,
						"quoted_price":j.quoted_price,
						"quotation_no":j.quotation_no,
						"work_order_data":j.work_order_data or "" ,
						"wo_status":w_doc.status
})


	
@frappe.whitelist()
def get_quotation_history(source,rate = None,type = None):
	target_doc = frappe.new_doc("Quotation")
	doc = frappe.get_doc("Quotation",source)

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
	return round(doc.final_approved_price / doc.total_qty,2) or 0

@frappe.whitelist()
def final_price_validate_si(wod):
	qi_details = frappe.db.sql('''select q.name,qi.qty as qty,qi.rate as rate,qi.amount as amount from `tabQuotation Item` as qi inner join `tabQuotation` as q on q.name = qi.parent where q.workflow_state = "Approved By Customer" and qi.wod_no = %s order by q.creation desc''',wod,as_dict=1)
	return qi_details

def on_update(self, method):
	if self.workflow_state not in ["Rejected", "Rejected by Customer", "Approved","Approved By Management", "Approved By Customer", "Cancelled"]:
		if self.quotation_type == "Internal Quotation - Repair" or self.quotation_type == "Internal Quotation - Supply":
			frappe.db.set_value(self.doctype, self.name, "workflow_state", "Waiting For Approval")

		else:
			frappe.db.set_value(self.doctype, self.name, "workflow_state", "Quoted to Customer")
	if self.quotation_type == "Internal Quotation - Repair":
		for i in self.get("items"):
			if i.wod_no:
				doc = frappe.get_doc("Work Order Data",i.wod_no)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Management":
					doc.status = "IQ-Internally Quoted"	
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
	for i in frappe.db.sql('''select  q.name as name,c.email_id as email_id,q.branch_name as branch,q.is_email_sent as ecount,q.party_name as customer_name from `tabQuotation` as q join `tabCustomer` as c on c.name = q.party_name where q.docstatus = 0 and 
				q.workflow_state = 'Quoted to Customer' ''',as_dict=1):
		receiver = []
		receiver.append(i['email_id'])
		sender = frappe.db.get_value("Email Account",{"branch":i['branch']},"email_id")
		doctype = "Quotation"
		name = i['name']
		msg = '''Dear Mr./Ms. %s,{Dear Sir,}<br>We would like to remind you about the Quotation (WO/ Quotation Ref.: %s) sent earlier.<br>Kindly advise in order to proceed with
			work or we will return the unit in your facility.<br><br>Your quick response will be highly appreciated.'''%(i['customer_name'],i['name'])
		if not i['ecount']:
			msg = '''Dear Mr./Ms. %s,{Dear Sir,}<br>We would like to remind you about the Quotation (WO/ Quotation Ref.: %s) sent earlier. We have<br>attached the quotation
				for your reference.<br><br>We look forward to your approval of the work.'''%(i['customer_name'],i['name'])

		if len(receiver):
			try:
				frappe.sendmail(
					recipients = receiver,
					sender = sender,
					subject = str(doctype)+" "+str(name),
					message = msg,
					attachments=get_attachments(name,doctype)
				)
				print("Email sent")
				frappe.db.set_value("Quotation",name,"is_email_sent",1)
			except frappe.OutgoingEmailError as e:
				print(str(e))

def get_attachments(name,doctype):
	attachments = frappe.attach_print(doctype, name,file_name=doctype, print_format="Quotation TSL")
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
