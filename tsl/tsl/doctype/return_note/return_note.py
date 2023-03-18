# Copyright (c) 2023, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReturnNote(Document):
	def on_submit(self):
		doc = frappe.get_doc("Work Order Data",self.work_order_data)
		se_doc = frappe.new_doc("Stock Entry")
		se_doc.stock_entry_type = "Material Issue"
		se_doc.company = doc.company
		se_doc.branch = doc.branch
		se_doc.from_warehouse = doc.repair_warehouse
		se_doc.work_order_data = doc.name
		for i in doc.material_list:
			se_doc.append("items",{
				's_warehouse': doc.repair_warehouse,
				'item_code':i.item_code,
				'item_name':i.item_name,
				'description':i.item_name,
				'serial_no':i.serial_no,
				'qty':i.quantity,
				'uom':frappe.db.get_value("Item",i.item_code,'stock_uom') or "Nos",
				'branch':doc.branch,
				'cost_center':doc.department,
				'work_order_data':doc.name,
				'conversion_factor':1,
				'allow_zero_valuation_rate':1
			})
		se_doc.save(ignore_permissions = True)
		se_doc.submit()
