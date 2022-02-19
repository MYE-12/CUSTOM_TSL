
from pydoc import doc
import frappe
import json
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def get_wod_items(wod):
	wod = json.loads(wod)
	l=[]
	for k in list(wod):
		tot = frappe.db.sql('''select sum(total_amount) as total_amount  from `tabPart Sheet` where work_order_data = %s and docstatus=1 ''',k,as_dict=1)[0]["total_amount"]
		# q_sts = frappe.db.get_value("Evaluation Report",{"work_order_data":k},"test_result")
		if not tot:
			link = []
			link.append(""" <a href='/app/work-order-data/{0}'>{0}</a> """.format(k))
			frappe.throw("No Part Sheet created for this Work Order"+"-".join(link))
			continue
		doc = frappe.get_doc("Work Order Data",k)
		branch = doc.branch
		rate = frappe.db.get_value("Part Sheet", {"work_order_data":k, "docstatus":1}, "total_amount")
		if not rate:
			rate = 0
		for i in doc.get("material_list"):
			l.append(frappe._dict({
				"item" :"Service Item",
				"item_name" : i.item_name,
				"wod": k,
				"type": i.type,
				"model_no": i.model_no,
				"serial_no": i.serial_no,
				"qty": i.quantity,
				"sales_rep":doc.sales_rep,
				"rate": rate,
				"total_amt":float(tot)/float(i.quantity),
				"branch":branch,
				# "q_unit_status":q_sts

			}))
			
	return l

def before_save(self,method):
	self.item_price_details=[]
	self.similar_items_quoted_before=[]
	for i in self.get("items"):
		part_sheet = frappe.db.sql('''select name from `tabPart Sheet` where work_order_data = %s and docstatus = 1 order by creation desc''',i.wod_no,as_dict=1)
		for j in part_sheet:
			doc = frappe.get_doc("Part Sheet",j['name'])
			for k in doc.get("items"):
				if frappe.db.get_value("Item",k.part,"last_quoted_price") >= 0 and frappe.db.get_value("Item",k.part,"last_quoted_client"):
					self.append("similar_items_quoted_before",{
						"item":k.part_name,
						"client":frappe.db.get_value("Item",k.part,"last_quoted_client"),
						"price":frappe.db.get_value("Item",k.part,"last_quoted_price")
					})

				if frappe.db.get_value("Bin",{"item_code":k.part},"actual_qty"):
					price = frappe.db.get_value("Item",{"item_code":k.part},"valuation_rate")
					source = "TSL Inventory"
					if k.parts_availability == "No":
						source = "Supplier"
				else:
					price = k.price_ea
					source = "Supplier"
				
				self.append("item_price_details",{
					"item":k.part_name,
					"item_source":source,
					"price":price

				})
	
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

def on_update(self, method):
	# if self.quotation_type == "Site Visit Quotation":
	# 	print("\n\n\n\ntrue")
	# 	self.workflow_state = "Pending Approval"

	if self.workflow_state not in ["Rejected", "Rejected by Customer", "Approved", "Approved By Customer", "Cancelled","Pending Approval"]:
		if self.quotation_type == "Internal Quotation":
			self.workflow_state = "Waiting For Approval"
		
		else:
			frappe.db.set_value(self.doctype, self.name, "workflow_state", "Quoted to Customer")
	if self.quotation_type == "Internal Quotation":
		for i in self.get("items"):
			if i.wod_no:
				doc = frappe.get_doc("Work Order Data",i.wod_no)
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved":
					doc.status = "IQ-Internally Quoted"	
				doc.save(ignore_permissions=True)
	if not self.quotation_type == "Internal Quotation":
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

def before_submit(self,method):
	l = []
	if self.quotation_type == "Internal Quotation":
		for i in self.get("items"):
			if i.wod_no:
				frappe.db.set_value("Work Order Data",i.wod_no,"is_quotation_created",1)
		if self.item_price_details:
			for i in self.get("item_price_details"):
				frappe.db.set_value("Item",{"item_name":i.item},"last_quoted_price",i.price)
				frappe.db.set_value("Item",{"item_name":i.item},"last_quoted_client",self.party_name)





def validate(self, method):
	if not self.edit_final_approved_price and self.quotation_type=="Internal Quotation":
		self.final_approved_price = self.actual_price*302.8/100+self.actual_price
	l = []
	if self.quotation_type == "Internal Quotation":
		for i in self.get("items"):
			if i.item_name:
				item = frappe.db.sql('''select parent,item_name,rate from `tabQuotation Item` where parenttype = "Quotation" and item_name = %s and docstatus = 1 order by creation desc''',i.item_name,as_dict=1)
				for j in item:
					if frappe.db.get_value("Quotation",j['parent'],"quotation_type") == "Internal Quotation":
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
		
