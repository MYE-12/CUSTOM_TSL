# Copyright (c) 2023, Tsl and contributors
# For license information, please see license.txt
from pydoc import doc
import frappe
from frappe.model.document import Document
# from tsl.tsl.doctype.work_order_data.work_order_data import get_item_image as img
from tsl.tsl.doctype.part_sheet.part_sheet import get_valuation_rate
from frappe.model.document import Document

class InitialEvaluation(Document):
	@frappe.whitelist()
	def update_availability_status(self):
		invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
		for i in self.items:
			if i.part and i.parts_availability == "No" :
				bin = frappe.db.sql('''select name from `tabBin` where item_code = '{0}' and warehouse in ('{1}') and (actual_qty) >={2} '''.format(i.part,"','".join(invent),i.qty),as_dict =1)
				frappe.errprint(bin)
				if len(bin) and 'name' in bin[0]:
					sts = "Yes"
					price = frappe.db.get_value("Bin",{"item_code":i.part},"valuation_rate") or frappe.db.get_value("Item Price",{"item_code":i.part,"buying":1},"price_list_rate")
					i.price_ea = price
					i.parts_availability = sts

					frappe.db.sql('''update `tabTesting Part Sheet` set parts_availability = '{0}' ,price_ea = {1} where name ='{2}' '''.format(sts,price,i.name))
					frappe.db.set_value("Bin",{'item_code':i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value("Bin",{'item_code':i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))

		f = 0
		for i in self.items:
			if i.parts_availability == "No" and not i.from_scrap:
				f = 1
		if f:
			self.parts_availability = "No"
			frappe.db.sql('''update `tabInitial Evaluation` set parts_availability = "No" where name = %s ''',(self.name))
		else:
			self.parts_availability = "Yes"
			frappe.db.sql('''update `tabInitial Evaluation` set parts_availability = "Yes" where name = %s ''',(self.name))

	def validate(self):
		add = 0
		self.total_amount = 0
		for i in self.items:
			if i.part and not i.from_scrap:
#				price_sts = get_valuation_rate(i.part,i.qty,frappe.defaults.get_defaults().company)
#				i.price_ea = price_sts[0] if len(price_sts) else 0
#				i.parts_availability = price_sts[1] if len(price_sts) else "No"
				total = 0
			if i.total:
				total = i.total
				add += total
		self.total_amount = add
		doc = frappe.get_doc("Work Order Data",self.work_order_data)
		doc.status = "UE-Under Evaluation"
		if self.status_repair == "Comprasion":
			doc.status = "C-Comparison"

		doc.save(ignore_permissions = True)
		if self.if_parts_required:
			f=0
			for i in self.get("items"):
				if not i.part_sheet_no:
					i.part_sheet_no = 1
				if i.parts_availability == "No" and not i.from_scrap:
					f=1
			if f:
				self.parts_availability = "No"
				doc = frappe.get_doc("Work Order Data",self.work_order_data)

				if self.status_repair == "Comprasion":
					doc.status = "C-Comparison"
				else:
					doc.status = "SP-Searching Parts"
			else:
				self.parts_availability = "Yes"
				doc.status = "AP-Available Parts"
		if not self.evaluation_time or not self.estimated_repair_time:
			frappe.msgprint("Note: Evaluation Time and Estimated Repair Time is not given.")

		for pm in self.get("items"):
			model = pm.model
			part_no = pm.part
			category = pm.category
			sub_cat = pm.sub_category
			# ptof = frappe.db.exists ("Item",{'name':pm.part,'model':model,'category':category,'sub_category':sub_cat})
			if not part_no:		
				item_doc = frappe.new_doc("Item")
				item_doc.naming_series = "P.######"
				item_doc.model = model
				item_doc.category_ = category
				item_doc.sub_category = sub_cat
				item_doc.item_group = "Components"
				if frappe.session.user == "purchase@tsl-me.com":
					item_doc.save(ignore_permissions = True)
		if self.if_parts_required:
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			if self.parts_availability == "Yes":
				doc.status = "AP-Available Parts"
			if self.parts_availability != "Yes":
				sq = frappe.db.sql("""select work_order_data from `tabSupplier Quotation` where work_order_data = '%s' and docstatus = 1 """%(self.work_order_data))
				if sq:
					doc.status = "Parts Priced"
				if self.status_repair == "Comprasion":
					doc.status = "C-Comparison"
				else:
					doc.status = "SP-Searching Parts"
			
			doc.save(ignore_permissions=True)
	def on_update_after_submit(self):
		add = total = 0
		self.total_amount = 0
		for i in self.items:
			if i.part and get_valuation_rate(i.part,self.company,i.qty)[1] == "Yes" and not i.from_scrap:
				price_sts = get_valuation_rate(i.part,i.qty,self.company)
				i.price_ea = price_sts[0] if len(price_sts) else 0
				i.total = i.price_ea*i.qty
				i.parts_availability = price_sts[1] if len(price_sts) else "No"
				frappe.db.sql('''update `tabTesting Part Sheet` set price_ea = %s,total = %s,parts_availability = %s where name = %s''',(i.price_ea,(i.price_ea*i.qty),i.parts_availability,i.name))
			#add += (i.price_ea * i.qty)
		#self.total_amount = add
		frappe.db.sql('''update `tabInitial Evaluation` set total_amount = %s where name = %s ''',(add,self.name))
		if self.if_parts_required:
			self.part_no = 0
			f=0
			for i in self.get("items"):
				if not i.part_sheet_no:
					i.part_sheet_no = int(self.part_no)+1
					frappe.db.sql('''update `tabTesting Part Sheet` set part_sheet_no = %s where name = %s''',((int(self.part_no)+1),i.name))
				else:
					self.part_no = i.part_sheet_no
				if i.parts_availability == "No" and not i.from_scrap:
					f=1
			if len(self.items)>0 and self.items[-1].part_sheet_no:
				if str(self.items[-1].part_sheet_no) > str(1) and self.status in ["Spare Parts","Extra Parts",""]:
					frappe.db.sql('''update `tabInitial Evaluation` set status = %s where name = %s ''',("Extra Parts",self.name))
			if f:
				frappe.db.sql('''update `tabInitial Evaluation` set parts_availability = "No" where name = %s ''',(self.name))
				self.parts_availability == "No"
				# doc = frappe.get_doc("Work Order Data",self.work_order_data)
				# doc.status = "SP-Searching Parts"
				# doc.save(ignore_permissions=True)
				#	scrap = frappe.db.sql('''select * from `tabTesting Part Sheet` where name = %s ''', (self.name),as_dict=1)
				#	frappe.errprint(scrap)
			else:
				self.parts_availability = "Yes"
				frappe.db.sql('''update `tabInitial Evaluation` set parts_availability = "Yes" where name = %s ''',(self.name))
				
			invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
			for i in self.items:
				if i.part and i.parts_availability == "Yes" and not i.is_not_edit:
					frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))
			for i in self.items:
				i.is_not_edit = 1
				frappe.db.sql('''update `tabTesting Part Sheet` set is_not_edit = 1 where name = %s''',(i.name))
			lpn = self.items[-1].part_sheet_no
			for i in self.items:
				if i.part_sheet_no != lpn:
					frappe.db.sql('''update `tabTesting Part Sheet` set is_read_only = 1 where name = %s''',(i.name))
			for pm in self.get("items"):
				model = pm.model
				part_no = pm.part
				category = pm.category
				sub_cat = pm.sub_category
				# ptof = frappe.db.exists ("Item",{'name':pm.part,'model':model,'category':category,'sub_category':sub_cat})
				if  not part_no:
					frappe.errprint('ijt')
					item_doc = frappe.new_doc("Item")
					item_doc.naming_series = 'P.######'
					item_doc.model = model
					item_doc.category_ = category
					item_doc.sub_category = sub_cat
					item_doc.item_group = "Components"
					item_doc.save(ignore_permissions = True)
		
	def before_submit(self):
		invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]	
		for parts in self.items:
			update_part = parts.qty - (parts.used_qty or 0)
			
			if update_part >0 :
				item_name = frappe.get_value("Item",parts.part,"description")
				for i in self.get('items'):
					if i.part:
						new_doc = frappe.new_doc("Stock Entry")
						new_doc.stock_entry_type = "Material Receipt"
						new_doc.company = self.company
						new_doc.to_warehouse = "Kuwait - TSL"
						new_doc.append("items",{
							't_warehouse':"Kuwait - TSL",
							'item_code':i.part,
							'item_name':item_name,
							'description':item_name,
							'qty':update_part,
							'uom':frappe.db.get_value("Item",i.part,'stock_uom'),
							'conversion_factor':1,
							'allow_zero_valuation_rate':1
						})
						if self.parts_returned != 1:
							frappe.throw("<b style=color:red>Please Mention the Used Parts and Return the Unused Parts to Submit this Document</b> ")
						else:
							new_doc.save(ignore_permissions=True)
						if new_doc.name:
							new_doc.submit()
				if i.part and i.parts_availability == "Yes" and i.used_qty > 0:
					frappe.errprint("Status")
					new_doc = frappe.new_doc("Stock Entry")
					new_doc.stock_entry_type = "Material Issue"
					new_doc.company = self.company
					new_doc.to_warehouse = "Kuwait - TSL"

					# new_doc.to_warehouse = "Kuwait - TSL"
					new_doc.append("items",{
						's_warehouse':"Kuwait - TSL",
						'item_code':i.part,
						'qty':i.used_qty,
						'uom':frappe.db.get_value("Item",i.part,'stock_uom'),
						'conversion_factor':1,
						'allow_zero_valuation_rate':1
					})
					new_doc.save(ignore_permissions = True)
					new_doc.submit()
		for i in self.items:
			if i.part and i.parts_availability == "Yes" and not i.from_scrap:
				frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))

		for i in self.items:
			i.is_not_edit = 1
			frappe.db.set_value("Testing Part Sheet",{"parent":self.name,"name":i.name},"is_not_edit",1)
		if self.if_parts_required:
			wod = frappe.get_doc("Work Order Data",self.work_order_data)
			extra_ps = frappe.db.sql('''select name,attn from `tabInitial Evaluation` where work_order_data = %s and docstatus = 1 and creation <= %s''',(self.work_order_data,self.creation),as_dict=1)
			if extra_ps:
				wod.append("extra_part_sheets",{
					"part_sheet_name":self.name,
					"attn":self.attn,
				})
				wod.save(ignore_permissions = True)

	def on_cancel(self):
		invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
		for i in self.items:
			if i.part and i.parts_availability == "Yes" and not i.from_scrap:
				frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")-i.qty))

@frappe.whitelist()
def create_material_issue_from_ini_eval(name):
	new_doc = frappe.new_doc("Stock Entry")
	new_doc.stock_entry_type = "Material Issue"
	# new_doc.company = self.company
	new_doc.to_warehouse = "Kuwait - TSL"

	new_doc.to_warehouse = "Kuwait - TSL"
	ini= frappe.get_doc('Initial Evaluation',name)
	for i in ini.items:
		frappe.errprint(i)
		new_doc.append("items",{
			's_warehouse':"Kuwait - TSL",
			'item_code':i.part,
			'qty':i.qty,
			'uom':frappe.db.get_value("Item",i.part,'stock_uom'),
			# 'conversion_factor':1,
			# 'allow_zero_valuation_rate':1
		})
	new_doc.save(ignore_permissions = True)
	# new_doc.submit()
