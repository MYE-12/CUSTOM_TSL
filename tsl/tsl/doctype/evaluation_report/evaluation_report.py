
# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

from pydoc import doc
import frappe
from frappe.model.document import Document
# from tsl.tsl.doctype.work_order_data.work_order_data import get_item_image as img
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
			if i.part and i.parts_availability == "No":
				bin = frappe.db.sql('''select name from `tabBin` where item_code = '{0}' and warehouse in ('{1}') and (actual_qty) >={2} '''.format(i.part,"','".join(invent),i.qty),as_dict =1)
				sts = "Yes"
				if len(bin) and 'name' in bin[0]:
					price = frappe.db.get_value("Bin",{"item_code":i.part},"valuation_rate") or frappe.db.get_value("Item Price",{"item_code":i.part,"buying":1},"price_list_rate")
					i.price_ea = price
					i.parts_availability = sts
					frappe.db.sql('''update `tabPart Sheet Item` set parts_availability = '{0}' ,price_ea = {1} where name ='{2}' '''.format(sts,price,i.name))
				if i.parts_availability == sts:
					frappe.db.sql('''update `tabWork Order Data` set status = 'AP-Available Parts' where name ='{0}' '''.format(self.work_order_data))
				# else:
				#     frappe.db.sql('''update `tabWork Order Data` set status = 'WP-Waiting Parts' where name ='{0}' '''.format(self.work_order_data))
		
					# frappe.db.set_value("Bin",{'item_code':i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value("Bin",{'item_code':i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))

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
			# elif self.status == "Spare Parts":
			# 	doc = frappe.get_doc("Work Order Data",self.work_order_data)
			# 	doc.status = "Parts Priced"
			elif self.status == "Spare Parts" and self.parts_availability == "Yes":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "AP-Available Parts"
			# elif self.status == "Spare Parts" and self.parts_availability == "No":
			# 	doc.status = "SP-Searching Parts"
			
			elif self.status == "Return Not Repaired":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNR-Return Not Repaired"
			elif self.status == "Return No Fault":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNF-Return No Fault"
			elif self.status in ["Installed and Completed/Repaired","Customer Testing"]:
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RS-Repaired and Shipped"
			elif  self.status == "Customer Testing":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "CT-Customer Testing"
			# else:
			# 	doc = frappe.get_doc("Work Order Data",self.work_order_data)
			# 	doc.status = "AP-Available Parts"
				doc.save(ignore_permissions=True)
	def on_submit(self):
		if self.status == "Extra Parts" and self.parts_availability != "Yes":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "EP-Extra Parts"
			doc.save(ignore_permissions = True)

		if self.status == "Spare Parts" and self.parts_availability == "Yes":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "AP-Available Parts"
			doc.save(ignore_permissions = True)

		if self.status == "RNP-Return No Parts":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RNP-Return No Parts"
			doc.save(ignore_permissions = True)

		elif self.status == "Comparison":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "C-Comparison"
			doc.save(ignore_permissions = True)

		elif self.status == "Return Not Repaired":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RNR-Return Not Repaired"
			doc.save(ignore_permissions = True)

		elif self.status == "Return No Fault":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RNF-Return No Fault"
			doc.save(ignore_permissions = True)

		elif self.status == "Installed and Completed/Repaired":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RS-Repaired and Shipped"
			doc.save(ignore_permissions = True)

		elif self.status == "Customer Testing":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "CT-Customer Testing"
			doc.save(ignore_permissions = True)

		elif self.status == "Working":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "W-Working"
			doc.save(ignore_permissions = True)
		# if parts Required Check box is checked
		if self.if_parts_required:
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			# if parts avaliability field is yes
			if self.parts_availability == "Yes":
				doc.status = "AP-Available Parts"
			if self.parts_availability == "No":
				sq = frappe.db.sql("""select work_order_data from `tabSupplier Quotation` where work_order_data = '%s' and docstatus = 1 """%(self.work_order_data))
				
				if sq:

					doc.status = "Parts Priced"
					self.status = "Supplier Quoted"
				# if sq:
				# 	self.status = "Supplier Quoted"
				else:
					doc.status = "SP-Searching Parts"
			doc.save(ignore_permissions=True)
		if self.status:
			if self.status == "Working":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "W-Working"
			elif self.status == "Spare Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				sq = frappe.db.sql("""select work_order_data from `tabSupplier Quotation` where work_order_data = '%s' and docstatus = 1 """%(self.work_order_data))
				if sq:

					doc.status = "Parts Priced"
				else:
					doc.status = "SP-Searching Parts"

		if self.status == "Comparison":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "C-Comparison"
			doc.save(ignore_permissions = True)
		elif self.status == "Return Not Repaired":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RNR-Return Not Repaired"
			doc.save(ignore_permissions = True)

		elif self.status == "Return No Fault":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RNF-Return No Fault"
			doc.save(ignore_permissions = True)

		elif self.status in ["Installed and Completed/Repaired","Customer Testing"]:
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RS-Repaired and Shipped"
			doc.save(ignore_permissions = True)

		elif  self.status == "Customer Testing":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "CT-Customer Testing"
			doc.save(ignore_permissions = True)

		elif  self.status == "Spare Parts":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "SP-Searching Parts"
			doc.save(ignore_permissions = True)

		elif  self.status == "Spare Parts" and self.parts_availability == "Yes":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "AP-Available Parts"
			doc.save(ignore_permissions = True)

		if self.status == "Extra Parts" and self.parts_availability != "Yes":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "EP-Extra Parts"
			doc.save(ignore_permissions = True)

		if self.status == "Spare Parts" and self.parts_availability == "Yes":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "AP-Available Parts"
			doc.save(ignore_permissions = True)

		if self.status == "RNP-Return No Parts":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RNP-Return No Parts"
			doc.save(ignore_permissions = True)

		elif self.status == "Comparison":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "C-Comparison"
			doc.save(ignore_permissions = True)

		elif self.status == "Return Not Repaired":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RNR-Return Not Repaired"
			doc.save(ignore_permissions = True)

		elif self.status == "Return No Fault":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RNF-Return No Fault"
			doc.save(ignore_permissions = True)

		elif self.status == "Installed and Completed/Repaired":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "RS-Repaired and Shipped"
			doc.save(ignore_permissions = True)

		elif self.status == "Customer Testing":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "CT-Customer Testing"
			doc.save(ignore_permissions = True)

		elif self.status == "Working":
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			doc.status = "W-Working"
			doc.save(ignore_permissions = True)
		
		
		invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
#			for i in self.items:
#				if i.part and i.parts_availability == "Yes":
#					frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))




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
		if self.status in ("Return No Fault","Return Not Repaired","Comparison"):
			pass
		else:
			if not self.evaluation_time or not self.estimated_repair_time:
				frappe.msgprint("Note: Evaluation Time and Estimated Repair Time is not given.")
		for pm in self.get("items"):
			model = pm.model
			part_no = pm.part
			category = pm.category
			sub_cat = pm.sub_category
			package = pm.part_description
			# ptof = frappe.db.exists ("Item",{'name':pm.part,'model':model,'category':category,'sub_category':sub_cat})
			if not part_no:
				item_doc = frappe.new_doc("Item")
				#item_doc.naming_series = "CO.#####"
				item_doc.naming_series = "P.######"
				item_doc.model = model
				item_doc.category_ = category
				item_doc.sub_category = sub_cat
				# item_doc.package = package
				item_doc.item_group = "Components"
				if frappe.session.user == "purchase@tsl-me.com" :
					item_doc.save(ignore_permissions = True)
	def on_update_after_submit(self):
		add = total = 0
		self.total_amount = 0
		for i in self.items:
			if i.part and get_valuation_rate(i.part,self.company,i.qty)[1] == "Yes" and not i.from_scrap:
				price_sts = get_valuation_rate(i.part,self.company,i.qty)
				i.price_ea = price_sts[0] if len(price_sts) else 0
				# i.total = i.price_ea*i.qty
				i.parts_availability = price_sts[1] if len(price_sts) else "No"
				# frappe.db.sql('''update `tabPart Sheet Item` set price_ea = %s,total = %s,parts_availability = %s where name = %s''',(i.price_ea,(i.price_ea*i.qty),i.parts_availability,i.name))
			#add += (i.price_ea * i.qty)
		#self.total_amount = add
		# frappe.db.sql('''update `tabEvaluation Report` set total_amount = %s where name = %s ''',(add,self.name))
		if self.status == "Working":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "W-Working"
		if self.status:
			sq = frappe.db.sql("""select (`tabSupplier Quotation Item`.work_order_data) as wod ,`tabSupplier Quotation`.name as sq 
					  from `tabSupplier Quotation` left join `tabSupplier Quotation Item` on `tabSupplier Quotation`.name = `tabSupplier Quotation Item`.parent  
					  where `tabSupplier Quotation`.docstatus = 1 """,as_dict=1)
			
			for s in sq:
				
				if s.wod:
					if self.status == "Spare Parts":
						doc = frappe.get_doc("Work Order Data",s.wod)
						doc.status = "Parts Priced"
			doc = frappe.get_doc("Work Order Data",self.work_order_data)
			wod_status = []
			qtn = frappe.db.sql("""select `tabQuotation Item`.wod_no as wod ,`tabQuotation`.name as qtn
					from `tabQuotation` left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent  
						where `tabQuotation`.workflow_state = 'Approved By Management' and `tabQuotation Item`.wod_no = '%s' """ %(self.work_order_data),as_dict=1)
			
			qtn_1 = frappe.db.sql("""select `tabQuotation Item`.wod_no as wod ,`tabQuotation`.name as qtn
					from `tabQuotation` left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent  
						where `tabQuotation`.workflow_state = 'Approved By Customer' and `tabQuotation Item`.wod_no = '%s' """ %(self.work_order_data),as_dict=1)
			if qtn:
				wod_status = qtn
			else:
				wod_status = qtn_1
			
			for qt in  wod_status:
				if self.status == "Working":
					if qt.wod == self.work_order_data:
						frappe.errprint("yes")
						doc = frappe.get_doc("Work Order Data",qt.wod)
						doc.status = "RS-Repaired and Shipped"
				

					else:
						doc.status = "W-Working"
		
				if self.status == "Spare Parts" and self.parts_availability == "Yes":
					if qt.wod == self.work_order_data:
						doc = frappe.get_doc("Work Order Data",qt.wod)
						doc.status = "A-Approved"

					else:
						doc.status = "AP-Available Parts"
			else:
				sq = frappe.db.sql("""select work_order_data from `tabSupplier Quotation` where work_order_data = '%s' and docstatus = 1 """%(self.work_order_data))
				if sq:
					doc.status == "Parts Priced"
				elif self.status == "Spare Parts":
					doc.status = "SP-Searching Parts"
			
			if self.status == "Extra Parts" and self.parts_availability != "Yes":

				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "EP-Extra Parts"
			
			if self.status == "Spare Parts" and self.parts_availability == "Yes":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "AP-Available Parts"



			if self.status == "RNP-Return No Parts":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNP-Return No Parts"
			elif self.status == "Comparison":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "C-Comparison"
			elif self.status == "Return Not Repaired":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNR-Return Not Repaired"
			elif self.status == "Return No Fault":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNF-Return No Fault"
			elif self.status == "Installed and Completed/Repaired":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RS-Repaired and Shipped"
			elif  self.status == "Customer Testing":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "CT-Customer Testing"
			elif  self.status == "Working":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "W-Working"
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
			if len(self.items)>0 and self.items[-1].part_sheet_no and self.docstatus ==1:
					if str(self.items[-1].part_sheet_no) > str(1) and self.status in ["Spare Parts","Extra Parts","Comparison","Internal Extra Parts"] and self.ner_field == "NER-Need Evaluation Return":
						frappe.db.sql('''update `tabEvaluation Report` set status = %s where name = %s ''',("Extra Parts",self.name))
					if str(self.items[-1].part_sheet_no) > str(1) and self.status in ["Spare Parts","Comparison","Internal Extra Parts","Working"] and  self.ner_field != "NER-Need Evaluation Return":
						frappe.db.sql('''update `tabEvaluation Report` set status = %s where name = %s ''',("Internal Extra Parts",self.name))

			if f:
				sq = frappe.db.sql("""select work_order_data from `tabSupplier Quotation` where work_order_data = '%s' and docstatus = 1 """%(self.work_order_data))

				frappe.db.sql('''update `tabEvaluation Report` set parts_availability = "No" where name = %s ''',(self.name))
				if self.parts_availability == "No" and sq:
					doc = frappe.get_doc("Work Order Data",self.work_order_data)

					doc.status = "Parts Priced"
				# else:
				# 	# doc = frappe.get_doc("Work Order Data",self.work_order_data)

				# 	# self.parts_availability == "No"
				
				# 	doc.status = "SP-Searching Parts"
				# doc.save(ignore_permissions=True)
				#	scrap = frappe.db.sql('''select * from `tabPart Sheet Item` where name = %s ''', (self.name),as_dict=1)
			else:
				# if self.parts_availability == "Yes"  and i.parts_availability == 'No':
				# 	frappe.db.sql('''update `tabEvaluation Report` set parts_availability = "No" where name = %s ''',(self.name))
				# else:
				# 	frappe.db.sql('''update `tabEvaluation Report` set parts_availability = "Yes" where name = %s ''',(self.name))

				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				if self.status == "Installed and Completed/Repaired":
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
				# else:
				# 	doc.status = "AP-Available Parts"
				doc.save(ignore_permissions=True)
			invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]
			for i in self.items:
				if i.part and i.parts_availability == "Yes" and not i.is_not_edit:
					frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))
			for i in self.items:
				i.is_not_edit = 1
				frappe.db.sql('''update `tabPart Sheet Item` set is_not_edit = 1 where name = %s''',(i.name))
			if self.items:
				lpn = self.items[-1].part_sheet_no
			for i in self.items:
				if i.part_sheet_no != lpn:
					frappe.db.sql('''update `tabPart Sheet Item` set is_read_only = 1 where name = %s''',(i.name))
			for pm in self.get("items"):
				model = pm.model
				part_no = pm.part
				category = pm.category
				sub_cat = pm.sub_category
				package = pm.part_description
				# ptof = frappe.db.exists ("Item",{'name':pm.part,'model':model,'category':category,'sub_category':sub_cat})
				if  not part_no:
					item_doc = frappe.new_doc("Item")
					item_doc.naming_series = 'P.######'
					item_doc.model = model
					mod = frappe.db.get_value("Item Model",model,"model")
					item_doc.model_num = mod
					item_doc.category_ = category
					scn = frappe.db.get_value("Sub Category",sub_cat,"sub_category")
					item_doc.sub_category = sub_cat
					item_doc.sub_category_name = scn
					item_doc.package = package
					item_doc.item_group = "Components"
					if frappe.session.user == "purchase@tsl-me.com" :
						item_doc.save(ignore_permissions = True)
		
	# def before_submit(self):
	#     frappe.errprint("jiy")
	#     invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":self.company,"is_branch":1},"name",as_list=1)]	
	#     for i in self.items:
	#         if i.part and i.parts_availability == "Yes" and not i.from_scrap:
	#             frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",(frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")+i.qty))

	#     for i in self.items:
	#         i.is_not_edit = 1
	#         frappe.db.set_value("Part Sheet Item",{"parent":self.name,"name":i.name},"is_not_edit",1)
	#     if self.if_parts_required:
	#         wod = frappe.get_doc("Work Order Data",self.work_order_data)
	#         extra_ps = frappe.db.sql('''select name,attn from `tabEvaluation Report` where work_order_data = %s and docstatus = 1 and creation <= %s''',(self.work_order_data,self.creation),as_dict=1)
	#         if extra_ps:
	#             wod.append("extra_part_sheets",{
	#                 "part_sheet_name":self.name,
	#                 "technician":self.technician,
	#             })
	#             wod.save(ignore_permissions = True)

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

	# new_doc.to_warehouse = "Kuwait - TSL"
	ini= frappe.get_doc('Evaluation Report',name)
	for i in ini.items:
		if i.released != 1:
			new_doc.append("items",{
				's_warehouse':"Kuwait - TSL",
				'item_code':i.part,
				'qty':i.qty,
				'uom':frappe.db.get_value("Item",i.part,'stock_uom'),
				# 'conversion_factor':1,
				# 'allow_zero_valuation_rate':1
			})
		frappe.msgprint("Parts Released and Material Issue is Created")

	new_doc.save(ignore_permissions = True)
	new_doc.submit()

#	def onload(self):
#		self.append("technician_details",{
#			'user':frappe.session.user
#		})
#		self.save(ignore_permissions = True)
