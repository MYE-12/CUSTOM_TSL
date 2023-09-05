import frappe,json

def on_update_after_submit(self,method):
	pass

def on_submit(self,method):
	if self.work_order_data:
		doc = frappe.get_doc("Work Order Data",self.work_order_data)
		doc.status = 'RSC-Repaired and Shipped Client'
		doc.save(ignore_permissions = True)
		frappe.db.set_value("Work Order Data",self.work_order_data,"invoice_no",self.name)
		frappe.db.set_value("Work Order Data",self.work_order_data,"invoice_date",self.posting_date)
	if self.supply_order_data:
		frappe.db.set_value("Supply Order Data",self.supply_order_data,"invoice_no",self.name)
		frappe.db.set_value("Supply Order Data",self.supply_order_data,"invoice_date",self.posting_date)

def before_save(self,method):
	if self.taxes:
		igst = cgst = sgst = 0
		for i in self.taxes:
			if "IGST" in i.account_head:
				igst = i.rate
			if "SGST" in i.account_head:
				sgst = i.rate
			if "CGST" in i.account_head:
				cgst = i.rate
		for i in self.items:
			if i.net_amount:
				self.igst = round((i.net_amount * float(igst))/100)
				self.cgst = round((i.net_amount * float(cgst))/100)
				self.sgst = round((i.net_amount * float(sgst))/100)
	if self.work_order_data:
		if not frappe.db.get_value("Delivery Note",{"work_order_data":self.work_order_data}):
			frappe.msgprint("No Delivery Note is created against this Work Order")

@frappe.whitelist()
def get_wod_items_from_quotation(wod):
	wod = json.loads(wod)
	l=[]
	for k in list(wod):
		tot = frappe.db.sql('''select sum(total_amount) as total_amount  from `tabEvaluation Report` where work_order_data = %s and docstatus=1 group by work_order_data''',k,as_dict=1)
		# if not tot:
		# 	link = []
		# 	link.append(""" <a href='/app/work-order-data/{0}'>{0}</a> """.format(k))
		# 	frappe.throw("No Part Sheet created for this Work Order"+"-".join(link))
		# 	continue
		doc = frappe.get_doc("Work Order Data",k)
		branch = doc.branch
		if not tot:
			tot = 0
		else:
			tot = tot[0]['total_amount']
		for i in doc.get("material_list"):
			rate = 0
			price_details = frappe.db.sql('''select qi.rate as rate,qi.amount as amount  from `tabQuotation` as q join `tabQuotation Item` as qi on qi.parent = q.name where q.party_name = %s and workflow_state = "Approved By Customer"
							and qi.item_code = %s and q.docstatus = 1''',(doc.customer,i.item_code),as_dict=1)
			# frappe.errprint(price_details[-1])
			
			if len(price_details) and 'rate' in price_details[-0]:
				rate = price_details[-1]['rate']
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
				"total_amt": rate,
				"work_order_data":doc.name,
				"cost_center":doc.department,
				"branch":branch,
				"income_account":"6001002 - Revenue from Service - TSL"

			}))
	return l
