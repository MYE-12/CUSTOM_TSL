# Copyright (c) 2022, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from tsl.tsl.doctype.supply_order_data.supply_order_data import create_quotation
from frappe.utils import json
from frappe.utils.data import (
	add_days,
	add_months,
	add_to_date,
	date_diff,
	flt,
	get_date_str,
	nowdate,
)


class ItemAllocation(Document):
	@frappe.whitelist()
	def item_allocate_to_supplier(self):
		self.items =[]
		order = ""
		if self.order_by == "Supplier":
			order += "order by s.creation desc"
		elif self.order_by == "Item":
			order += "order by si.item_name"
		sqtn = frappe.db.sql('''select s.supplier as supplier_name,s.name as supplier_quotation,si.item_code as sku,si.item_name as item_name,si.rate as price,si.qty as qty,si.amount as amount from `tabSupplier Quotation` as s inner join `tabSupplier Quotation Item` as si on si.parent = s.name where s.supply_order_data = %s and s.docstatus = 0 and s.workflow_state = "Waiting For Approval" {0}'''.format(order),self.supply_order_data,as_dict= 1)
		for i in sqtn:
			self.append("items",i)
		self.save()
		self.reload()

@frappe.whitelist()
def create_qtn(doc,sod):
	new_doc = create_quotation(sod)
	new_doc.items = []
	doc = json.loads(doc)
	for i in doc:
		new_doc.append("items",{
			"supply_order_data":sod,
			"item_code":i['sku'],
			"item_name":i['item_name'],
			"description":i['item_name'],
			"qty":i['qty'],
			"schedule_date":add_to_date(nowdate(),3),
			"price_list_rate":i['price'],
			"rate":i['price'],
			"amount":i['amount'],
			"supplier_quotation":i['supplier_quotation'],
			"uom":"Nos",
			"stock_uom":"Nos"
		})
	return new_doc
	
		
		
