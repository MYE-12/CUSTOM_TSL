
# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

from pydoc import doc
import frappe
from frappe.model.document import Document
from tsl.tsl.doctype.work_order_data.work_order_data import get_item_image as img
from tsl.tsl.doctype.part_sheet.part_sheet import get_valuation_rate
# @frappe.whitelist()
# def get_item_image(wod_no):
# 	erf_no = frappe.db.get_value("Work Order Data",wod_no,"equipment_recieved_form")
# 	image = img(erf_no)
# 	return image

class EvaluationReport(Document):
	@frappe.whitelist()
	def update_availability_status(self):
		invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
		for i in self.items:
			if i.part and i.parts_availability == "No" and not i.from_scarp:
				bin = frappe.db.sql('''select name from `tabBin` where item_code = {0} and warehouse in ('{1}') and (actual_qty-evaluation_qty) >={2} '''.format(i.part,"','".join(invent),i.qty),as_dict =1)
				if len(bin) and 'name' in bin[0]:
					sts = "Yes"
					price = frappe.db.get_value("Bin",{"item_code":i.part},"valuation_rate") or frappe.db.get_value("Item Price",{"item_code":i.part,"buying":1},"price_list_rate")
					i.price_ea = price
					i.parts_availability = sts
					frappe.db.sql('''update `tabPart Sheet Item` set parts_availability = '{0}' ,price_ea = {1} where name ='{2}' '''.format(sts,price,i.name))
					frappe.db.set_value("Bin",{'item_code':i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value("Bin",{'item_code':i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))

		f = 0
		for i in self.items:
			if i.parts_availability == "No" and not i.from_scrap:
				f = 1
		if f:
			self.parts_availability = "No"
			frappe.db.sql('''update `tabEvaluation Report` set parts_availability = "No" where name = %s ''',(self.name))
		else:
			self.parts_availability = "Yes"
			frappe.db.sql('''update `tabEvaluation Report` set parts_availability = "Yes" where name = %s ''',(self.name))
			if self.status == "Working":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "W-Working"
			elif self.status == "Comparison":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "C-Comparison"
			elif self.status == "Return Not Repaired":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNR-Return Not Repaired"
			elif self.status == "Return No Fault":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNF-Return No Fault"
			elif self.status in ["Installed and Completed","Customer Testing"]:
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RS-Repaired and Shipped"
			elif  self.status == "Customer Testing":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "CT-Customer Testing"
			else:
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "AP-Available Parts"
			doc.save()
	def on_submit(self):
		if self.status:
			if self.status == "Working":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "W-Working"
			elif self.status == "Spare Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "SP-Searching Parts"
			elif self.status == "Extra Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "EP-Extra Parts"
			elif self.status == "Comparison":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "C-Comparison"
			elif self.status == "Return Not Repaired":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNR-Return Not Repaired"
			elif self.status == "Return No Fault":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNF-Return No Fault"
			elif self.status in ["Installed and Completed","Customer Testing"]:
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RS-Repaired and Shipped"
			elif  self.status == "Customer Testing":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "CT-Customer Testing"
			doc.save(ignore_permissions = True)
		if self.if_parts_required:
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			if self.parts_availability == "Yes":
				doc.status = "AP-Available Parts"
			else:
				doc.status = "SP-Searching Parts"
			doc.save(ignore_permissions=True)
			invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
#			for i in self.items:
#				if i.part and i.parts_availability == "Yes":
#					frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))




	def validate(self):
		add = 0
		self.total_amount = 0
		for i in self.items:
			if i.part and not i.from_scrap:
				price_sts = get_valuation_rate(i.part,i.qty,frappe.defaults.get_defaults().company)
				i.price_ea = price_sts[0] if len(price_sts) else 0
				i.parts_availability = price_sts[1] if len(price_sts) else "No"
				total = 0
			if i.total:
				total = i.total
				add += total
		self.total_amount = add
		doc = frappe.get_doc("Work Order Data",self.work_order_data)
		doc.status = "UE-Under Evaluation"
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
			else:
				self.parts_availability = "Yes"
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
				item_doc.model = model
				item_doc.category_ = category
				item_doc.sub_category = sub_cat
				item_doc.item_group = "Components"
				item_doc.save(ignore_permissions = True)
	def on_update_after_submit(self):
		add = total = 0
		self.total_amount = 0
		for i in self.items:
			if i.part and get_valuation_rate(i.part,i.qty,self.company)[1] == "Yes" and not i.from_scrap:
				price_sts = get_valuation_rate(i.part,i.qty,self.company)
				i.price_ea = price_sts[0] if len(price_sts) else 0
				i.total = i.price_ea*i.qty
				i.parts_availability = price_sts[1] if len(price_sts) else "No"
				frappe.db.sql('''update `tabPart Sheet Item` set price_ea = %s,total = %s,parts_availability = %s where name = %s''',(i.price_ea,(i.price_ea*i.qty),i.parts_availability,i.name))
			#add += (i.price_ea * i.qty)
		#self.total_amount = add
		frappe.db.sql('''update `tabEvaluation Report` set total_amount = %s where name = %s ''',(add,self.name))
		if self.status:
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			if self.status == "Working":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "W-Working"
			elif self.status == "Spare Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "SP-Searching Parts"
			elif self.status == "Extra Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "EP-Extra Parts"
			elif self.status == "Comparison":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "C-Comparison"
			elif self.status == "Return Not Repaired":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNR-Return Not Repaired"
			elif self.status == "Return No Fault":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNF-Return No Fault"
			elif self.status == "Installed and Completed":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RS-Repaired and Shipped"
			elif  self.status == "Customer Testing":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "CT-Customer Testing"
			doc.save(ignore_permissions = True)
		if self.if_parts_required:
			self.part_no = 0
			f=0
			for i in self.get("items"):
				if not i.part_sheet_no:
					i.part_sheet_no = int(self.part_no)+1
					frappe.db.sql('''update `tabPart Sheet Item` set part_sheet_no = %s where name = %s''',((int(self.part_no)+1),i.name))
				else:
					self.part_no = i.part_sheet_no
				if i.parts_availability == "No" and not i.from_scrap:
					f=1
			if len(self.items)>0 and self.items[-1].part_sheet_no:
				if str(self.items[-1].part_sheet_no) > str(1) and self.status in ["Spare Parts","Extra Parts",""]:
					frappe.db.sql('''update `tabEvaluation Report` set status = %s where name = %s ''',("Extra Parts",self.name))
			if f:
				frappe.db.sql('''update `tabEvaluation Report` set parts_availability = "No" where name = %s ''',(self.name))
				self.parts_availability == "No"
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "SP-Searching Parts"
				doc.save(ignore_permissions=True)
				#	scrap = frappe.db.sql('''select * from `tabPart Sheet Item` where name = %s ''', (self.name),as_dict=1)
				#	frappe.errprint(scrap)
			else:
				self.parts_availability = "Yes"
				frappe.db.sql('''update `tabEvaluation Report` set parts_availability = "Yes" where name = %s ''',(self.name))
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				if self.status == "Installed and Completed":
					doc.status = "RS-Repaired and Shipped"
				elif self.status == "Customer Testing":
					doc.status == "CT-Customer Testing"
				elif self.status == "Working":
					doc.status = "W-Working"
				elif self.status == "Comparison":
					doc.status = "C-Comparison"
				elif self.status == "Return Not Repaired":
					doc.status = "RNR-Return Not Repaired"
				elif self.status == "Return No Fault":
					doc.status = "RNF-Return No Fault"
				else:
					doc.status = "AP-Available Parts"
				doc.save(ignore_permissions=True)
			invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
			for i in self.items:
				if i.part and i.parts_availability == "Yes" and not i.is_not_edit:
					frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))
			for i in self.items:
				i.is_not_edit = 1
				frappe.db.sql('''update `tabPart Sheet Item` set is_not_edit = 1 where name = %s''',(i.name))
			lpn = self.items[-1].part_sheet_no
			for i in self.items:
				if i.part_sheet_no != lpn:
					frappe.db.sql('''update `tabPart Sheet Item` set is_read_only = 1 where name = %s''',(i.name))
			for pm in self.get("items"):
				model = pm.model
				part_no = pm.part
				category = pm.category
				sub_cat = pm.sub_category
				# ptof = frappe.db.exists ("Item",{'name':pm.part,'model':model,'category':category,'sub_category':sub_cat})
				if  not part_no:
					item_doc = frappe.new_doc("Item")
					item_doc.model = model
					item_doc.category_ = category
					item_doc.sub_category = sub_cat
					item_doc.item_group = "Components"
					item_doc.save(ignore_permissions = True)
		
	def before_submit(self):
		invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]	
		for i in self.items:
			if i.part and i.parts_availability == "Yes" and not i.from_scrap:
				frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))

		for i in self.items:
			i.is_not_edit = 1
			frappe.db.set_value("Part Sheet Item",{"parent":self.name,"name":i.name},"is_not_edit",1)
		if self.if_parts_required:
			wod = frappe.get_doc("Work Order Data",self.work_order_data)
			extra_ps = frappe.db.sql('''select name,attn from `tabEvaluation Report` where work_order_data = %s and docstatus = 1 and creation <= %s''',(self.work_order_data,self.creation),as_dict=1)
			if extra_ps:
				wod.append("extra_part_sheets",{
					"part_sheet_name":self.name,
					"technician":self.attn,
				})
				wod.save(ignore_permissions = True)

	def on_cancel(self):
		invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
		for i in self.items:
			if i.part and i.parts_availability == "Yes" and not i.from_scrap:
				frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")-i.qty))


#	def onload(self):
#		self.append("technician_details",{
#			'user':frappe.session.user
#		})
#		self.save(ignore_permissions = True)
