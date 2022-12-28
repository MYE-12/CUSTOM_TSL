# Copyright (c) 2022, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CreateWorkOrder(Document):
	def before_submit(self):
		if not self.branch:
			frappe.throw("Assign a branch to Submit")
		for i in self.get('received_equipment'):
			if not i.item_code:
				frappe.throw("Item code should be filled in Row-{0}".format(i.idx))
		for i in self.get('received_equipment'):
			if i.item_code:
				new_doc = frappe.new_doc("Stock Entry")
				new_doc.stock_entry_type = "Material Receipt"
				new_doc.company = self.company
				new_doc.branch = self.branch
				new_doc.equipment_received_form = self.name
				new_doc.to_warehouse = i.repair_warehouse
				new_doc.append("items",{
					't_warehouse': i.repair_warehouse,
					'item_code':i.item_code,
					'item_name':i.item_name,
					'description':i.item_name,
					'serial_no':i.serial_no,
					'qty':i.qty,
					'uom':frappe.db.get_value("Item",i.item_code,'stock_uom'),
					'conversion_factor':1,
					'allow_zero_valuation_rate':1
				})
				new_doc.save(ignore_permissions = True)
				if new_doc.name:
					new_doc.submit()

	def on_cancel(self):
		if frappe.db.get_list("Stock Entry",{'equipment_received_form':self.name},"name",as_list = 1):
			for i in frappe.db.get_list("Stock Entry",{'equipment_received_form':self.name},"name",as_list = 1):
				doc = frappe.get_doc("Stock Entry",i[0])
				if doc.docstatus == 1:
					doc.cancel()
		


			
	def after_save(self):
		return
		if self.repair_warehouse:
			for i in self.get("received_equipment"):
				i.repair_warehouse = self.repair_warehouse
		for i in self.get('received_equipment'):
			if i.model and i.manufacturer and i.type and i.serial_no:
				for sod in frappe.db.sql('''select parent from `tabMaterial List` where model_no = %s and mfg = %s and type = %s and serial_no = %s and parenttype = "Supply Order Data" ''',(i.model,i.manufacturer,i.type,i.serial_no),as_dict=1):
					prev_quoted = frappe.db.sql('''select q.party_name as customer,q.name as name,qi.rate as price from `tabQuotation Item` as qi inner join `tabQuotation` as q on qi.parent = q.name where qi.supply_order_data = %s and (q.quotation_type = "Customer Quotation - Supply" or q.quotation_type = "Revised Quotation - Supply") and q.workflow_state = "Approved By Customer" ''',sod['parent'],as_dict = 1)
					self.append("previously_quoted",{
						"customer":prev_quoted[0]['customer'],
						"model":i.model,
						"mfg":i.manufacturer,
						"type":i.type,
						"quoted_price":prev_quoted[0]['price'],
						"quotation_no":prev_quoted[0]['name']
					})
				
		for i in self.get('received_equipment'):
			if not i.item_code:
				item = frappe.db.get_value("Item",{"model":i.model,"mfg":i.manufacturer,"type":i.type,"item_name":i.item_name},"name")
				if item and i.serial_no in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
					i.item_code = item
				elif item and i.serial_no not in [i[0] for i in frappe.db.get_list("Serial No",{"item_code":item},as_list=1)]:
					i.item_code = item
				else:
					new_doc = frappe.new_doc('Item')
					new_doc.naming_series = '.####'
					new_doc.item_name = i.item_name
					new_doc.item_group = "Equipments"
					new_doc.description = i.item_name
					new_doc.model = i.model
					new_doc.is_stock_item = 1
					new_doc.mfg = i.manufacturer
					new_doc.type = i.type
					if i.has_serial_no:
						new_doc.has_serial_no = 1
					new_doc.save(ignore_permissions = True)
					if new_doc.name:
						i.item_code = new_doc.name
						print(new_doc.name)
						# if i.has_serial_no and i.serial_no:
						# 	sn_doc = frappe.new_doc("Serial No")
						# 	sn_doc.serial_no = i.serial_no
						# 	sn_doc.item_code = i.item_code
						# 	sn_doc.warehouse = i.repair_warehouse
						# 	sn_doc.save(ignore_permissions = True)
