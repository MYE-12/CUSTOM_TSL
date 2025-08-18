
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
			if i.part:
				
				bin = frappe.db.sql('''select name from `tabBin` where item_code = '{0}' and warehouse in ('{1}') and (actual_qty) >={2} '''.format(i.part,"','".join(invent),i.qty),as_dict =1)
				sts = "Yes"
				if len(bin) and 'name' in bin[0]:
					# price = frappe.db.get_value("Bin",{"item_code":i.part},"valuation_rate") or frappe.db.get_value("Item Price",{"item_code":i.part,"buying":1},"price_list_rate")
					bn = frappe.db.get_value("Bin",{"item_code":i.part},"valuation_rate")
					price = 0
					if bn:
						price = bn
						
					else:
						ip = frappe.db.get_value("Item Price",{"item_code":i.part,"buying":1},"price_list_rate")
						if ip:
							price = ip
							# frappe.errprint(price)
					
					
					i.price_ea = price
					i.total = i.price_ea * i.qty
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
				doc.save(ignore_permissions=True)
			elif self.status == "Comparison":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "C-Comparison"
				doc.save(ignore_permissions=True)
			# elif self.status == "Spare Parts":
			# 	doc = frappe.get_doc("Work Order Data",self.work_order_data)
			# 	doc.status = "Parts Priced"
			elif self.status == "Spare Parts" and self.parts_availability == "Yes":
			
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "AP-Available Parts"
				doc.save(ignore_permissions=True)
			# elif self.status == "Spare Parts" and self.parts_availability == "No":
			# 	doc = frappe.get_doc("Work Order Data",self.work_order_data)
			# 	doc.status = "SP-Searching Parts"
			# 	doc.save(ignore_permissions=True)
			
			elif self.status == "Return Not Repaired":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNR-Return Not Repaired"
				doc.save(ignore_permissions=True)
			elif self.status == "Return No Fault":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RNF-Return No Fault"
				doc.save(ignore_permissions=True)
			elif self.status in ["Installed and Completed/Repaired","Customer Testing"]:
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "RS-Repaired and Shipped"
				doc.save(ignore_permissions=True)
			elif  self.status == "Customer Testing":
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				doc.status = "CT-Customer Testing"
			# else:
			# 	doc = frappe.get_doc("Work Order Data",self.work_order_data)
			# 	doc.status = "AP-Available Parts"
				doc.save(ignore_permissions=True)
				
	def on_submit(self):
		# if self.status == "Extra Parts" and self.parts_availability != "Yes":
		# 	doc = frappe.get_doc("Work Order Data",self.work_order_data)
		# 	doc.status = "EP-Extra Parts"
		# 	doc.save(ignore_permissions = True)

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
			if self.parts_availability == "Yes" and self.status != "Working":
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
				frappe.throw("Note: Evaluation Time and Estimated Repair Time is not given.")
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
				if frappe.session.user == "purchase@tsl-me.com" or frappe.session.user == "purchase-sa1@tsl-me.com":
					item_doc.save(ignore_permissions = True)

	def on_update_after_submit(self):
		
		if not self.evaluation_time or not self.estimated_repair_time:
			if not self.status == "Comparison":
				frappe.throw("Note: Evaluation Time and Estimated Repair Time is not given.")
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
			
			if  self.status in ["Extra Parts","Working"]:
				doc = frappe.get_doc("Work Order Data",self.work_order_data)
				if self.status == "Extra Prts":
					doc.status = "EP-Extra Parts"
				else:
					doc.status = "W-Working"
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
		
				
									
				if int(self.items[-1].part_sheet_no) > int(1) and self.status in ["Extra Parts","Working",""] and self.ner_field == "NER-Need Evaluation Return":
					frappe.db.sql('''update `tabEvaluation Report` set status = %s where name = %s ''',("Extra Parts",self.name))

					if self.status == "Extra Parts":
						wd = frappe.get_doc("Work Order Data",self.work_order_data)
						wd.status = "EP-Extra Parts"
						wd.save(ignore_permissions = 1)

					else:
						if self.status == "Working":
							wd = frappe.get_doc("Work Order Data",self.work_order_data)
							wd.status = "W-Working"
							wd.save(ignore_permissions = 1)


				if int(self.items[-1].part_sheet_no) > int(1) and self.status in ["Spare Parts","Comparison","Extra Parts","Internal Extra Parts"]  and not self.ner_field == "NER-Need Evaluation Return":
					
					self.status = "Internal Extra Parts"
					frappe.db.sql('''update `tabEvaluation Report` set status = %s where name = %s ''',("Internal Extra Parts",self.name))
					if self.document_active_status == "Yes":
						wd = frappe.get_doc("Work Order Data",self.work_order_data)
						wd.status = "IP-Internal Extra Parts"
						wd.save(ignore_permissions = 1)

					# if self.status == "Extra Parts":
					# 	self.status = "Extra Parts"
					# 	# frappe.db.sql('''update `tabEvaluation Report` set status = %s where name = %s ''',("Extra Parts",self.name))
					# 	if self.document_active_status == "Yes":
					# 		wd = frappe.get_doc("Work Order Data",self.work_order_data)
					# 		wd.status = "EP-Extra Parts"
					# 		wd.save(ignore_permissions = 1)

				if str(self.items[-1].part_sheet_no) > str(1) and  self.status in["Working"] and not self.ner_field == "NER-Need Evaluation Return":
					if self.status == "Working":
						self.status = "Working"
						# frappe.db.sql('''update `tabEvaluation Report` set status = %s where name = %s ''',("Working",self.name))
						wd = frappe.get_doc("Work Order Data",self.work_order_data)
						wd.status = "W-Working"
						wd.save(ignore_permissions = 1)
					
				if str(self.items[-1].part_sheet_no) > str(1) and self.status in ["Spare Parts","Comparison","Internal Extra Parts","Working"] and  not self.ner_field == "NER-Need Evaluation Return" and self.parts_availability == "Yes":
				
					frappe.db.sql('''update `tabEvaluation Report` set status = %s where name = %s ''',("Working",self.name))

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
				if i.part and i.parts_availability == "Yes":
					ev_qty = 0
					ev = frappe.db.get_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty")
					if ev:
						ev_qty = ev
					frappe.db.set_value('Bin',{"item_code":i.part,"warehouse":["in",invent]},"evaluation_qty",ev_qty+i.qty)
			# for i in self.items:
			# 	i.is_not_edit = 1
			# 	frappe.db.sql('''update `tabPart Sheet Item` set is_not_edit = 1 where name = %s''',(i.name))
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
				des = pm.part_name
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
					item_doc.description = des
					item_doc.item_group = "Components"
					if frappe.session.user == "purchase@tsl-me.com" or frappe.session.user == "purchase-sa1@tsl-me.com" :
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
	# new_doc.to_warehouse = "Kuwait - TSL"
	ini= frappe.get_doc('Evaluation Report',name)
	
	if ini.company == "TSL COMPANY - Kuwait":
		new_doc = frappe.new_doc("Stock Entry")
		new_doc.stock_entry_type = "Material Issue"
		# new_doc.company = self.company
		new_doc.to_warehouse = "Kuwait - TSL"
		for i in ini.items:
			if not i.released == 1 and i.parts_availability == "Yes":
				new_doc.append("items",{
					's_warehouse':"Kuwait - TSL",
					'item_code':i.part,
					'qty':i.qty,
					'uom':frappe.db.get_value("Item",i.part,'stock_uom'),
					'work_order_data':ini.work_order_data,

					# 'conversion_factor':1,
					# 'allow_zero_valuation_rate':1
				})

		new_doc.save(ignore_permissions = True)
		new_doc.submit()

		frappe.msgprint("Parts Released and Material Issue is Created")
		
	if ini.company == "TSL COMPANY - UAE":
		new_doc = frappe.new_doc("Stock Entry")
		new_doc.company = "TSL COMPANY - UAE"
		new_doc.stock_entry_type = "Material Issue"
		new_doc.from_warehouse = "Dubai - TSL-UAE"
		
		for i in ini.items:
			if i.released == 0 and i.parts_availability == "Yes":
				
				new_doc.append("items",{
					's_warehouse':"Dubai - TSL-UAE",
					'item_code':i.part,
					'qty':i.qty,
					'uom':frappe.db.get_value("Item",i.part,'stock_uom'),
					'cost_center':"Main - TSL-UAE",
					'work_order_data':ini.work_order_data,
					'conversion_factor':1,
					# 'allow_zero_valuation_rate':1
				})
		new_doc.save(ignore_permissions = True)
		new_doc.submit()

		frappe.msgprint("Parts Released and Material Issue is Created")

	if ini.company == "TSL COMPANY - KSA":
		new_doc = frappe.new_doc("Stock Entry")
		new_doc.company = "TSL COMPANY - KSA"
		new_doc.stock_entry_type = "Material Issue"
		
		war = ""
		cc = ""
		if ini.branch == "Riyadh - TSL- KSA":
			war = "Riyadh - TSL - KSA"
			cc = "Riyadh-Repair - TSL - KSA"
		if ini.branch == "Jeddah - TSL-SA":
			war = "Jeddah - TSL - KSA"
			cc = "Jeddah-Repair - TSL - KSA"
		if ini.branch == "Dammam - TSL-SA":
			war = "Dammam - TSL - KSA"
			cc = "Dammam-Repair - TSL - KSA"
		new_doc.from_warehouse = war

		for i in ini.items:
			
			if i.released == 0 and i.parts_availability == "Yes" and  i.from_scrap != 1:
				uom = frappe.db.get_value("Item",i.part,'stock_uom')
				serial_no = frappe.db.get_value("Serial No",{"item_code":i.part},"name")
				new_doc.append("items",{
					's_warehouse':war,
					'item_code':i.part,
					'qty':i.qty,
					'serial_no':serial_no or "",
					'uom':uom,
					'stock_uom':uom,
					'cost_center':cc,
					'work_order_data':ini.work_order_data,
					'conversion_factor':1,
					'allow_zero_valuation_rate':1
				})
		new_doc.save(ignore_permissions = True)
		new_doc.submit()
		# return new_doc.name
		frappe.msgprint("Parts Released and Material Issue is Created")


@frappe.whitelist()
def parts_request(name):
	parts= frappe.get_doc('Evaluation Report',name)

	for pa in parts.items:
		if parts.if_parts_required:
			technician = frappe.db.get_value("User",{"name":parts.technician},"full_name")

			if parts.branch == "Jeddah - TSL-SA":
				msg1 = """Dear Purchaser, <br> <br>Please find the Evaluation Report for the Technician (%s) need price for further proceeding.<br> 
						<br><br>"""%(technician)

				msg2 = """<div><style>.sh-src a{text-decoration:none!important;}</style></div> <br> <table cellpadding="0" cellspacing="0" border="0" class="sh-src" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td align="center" style="padding: 0px 18px 0px 0px; vertical-align: top;">
					<table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 13px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/file/5r1rjllxn0zdme" alt="" title="Profile Picture" width="100" height="100" class="" style="display: block; border: 0px; max-width: 100px;"></p></td></tr></table> <table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://tsl-me.com/" target="_blank"><img src="https://signaturehound.com/api/v1/file/137twgllxltmdmv" alt="" title="Logo" width="150" height="50" style="display: block; border: 0px; max-width: 150px;"></a></p></td></tr></table></td> <td width="5" style="padding: 1px 0px 0px;"></td> <td style="padding: 0px 1px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 10px 0px; border-bottom: 2px solid rgb(0,92,163); font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap;"><p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; font-weight: 700; color: rgb(0,92,163); white-space: nowrap; margin: 1px;">Ajai
                    </p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">Admin &amp; Customer Support</p> <!----> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">
                      TSL Group | KSA - Jeddah</p> <!----></td></tr> <tr><td style="padding: 10px 1px 10px 0px; border-bottom: 2px solid rgb(0,92,163);"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/email/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; margin: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="mailto:info-jed@tsl-me.com" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">info-jed@tsl-me.com</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/mobile/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; margin: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="tel:+966558803522" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">+966 55 880 3522</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/map/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; margin: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://www.google.com/maps/dir/21.3180818,39.227158/TSL+Industrial+Electronics+for+Repairing+%26+Supply+-+Jeddah,+80th+street%D8%8C+Al-Qarinia+District%D8%8C+Jeddah+22535,+Saudi+Arabia%E2%80%AD/@21.3172514,39.1901511,13z/data=!3m1!4b1!4m9!4m8!1m1!4e1!1m5" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">80th Street, Al-Qrainia, Jeddah, Saudi Arabia.</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/website/round-outlined/0088cc.png" alt="" width="22" height="22" style="display: block; border: 0px; margin: 0px; width: 22px; height: 22px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,162) !important; font-weight: 700; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://tsl-me.com/" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,163); font-weight: 700; text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 15px; white-space: nowrap; color: rgb(0,92,163); font-weight: 700; text-decoration: none !important;">tsl-me.com</span></a></p></td></tr></table></td></tr> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.linkedin.com/company/tsl-me/mycompany/" target="_blank"><img src="https://signaturehound.com/api/v1/png/linkedin/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://x.com/tsl_mecompany?s=11&amp;t=Zxza0-9Q_18nsDCddfTQPw" target="_blank"><img src="https://signaturehound.com/api/v1/png/x/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.instagram.com/tslcom/?igshid=MzRlODBiNWFlZA%3D%3D" target="_blank"><img src="https://signaturehound.com/api/v1/png/instagram/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.facebook.com/people/TSL-Industrial-Electronics-Services/61550277093129/" target="_blank"><img src="https://signaturehound.com/api/v1/png/facebook/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="27" style="font-size: 0px; line-height: 0px; padding: 13px 1px 0px 0px;"><p style="margin: 1px;"><a href="https://www.youtube.com/@TSLELECTRONICSSERVICES" target="_blank"><img src="https://signaturehound.com/api/v1/png/youtube/round/0088cc.png" alt="" width="27" height="27" style="display: block; border: 0px; margin: 0px; width: 27px; height: 27px;"></a></p></td> <td width="3" style="padding: 0px 0px 1px;"></td>
					  </tr></table></td></tr></table></td></tr></table></td></tr> <!----> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: 0px; border-collapse: collapse;"><tr><td style="padding: 15px 1px 0px 0px; font-family: Arial, sans-serif; font-size: 10px; line-height: 12px; color: rgb(136,136,136);"><p style="font-family: Arial, sans-serif; font-size: 10px; line-height: 12px; color: rgb(136,136,136); margin: 1px;">The content of this email is confidential and intended for the recipient specified in message only. It is strictly forbidden to share any part of this message with any third party, without a written consent of the sender. If you received this message by mistake, please reply to this message and follow with its deletion, so that we can ensure such a mistake does not occur in the future.</p></td></tr></table></td></tr> """
						
				# technician = parts.technician
				frappe.sendmail(
						recipients="purchase-sa1@tsl-me.com",
						sender="info-jed@tsl-me.com",
						subject= "New Part Request",
						message=msg1+msg2,
						attachments=get_attachments(parts.name,"Evaluation Report")
				)
				frappe.msgprint("Mail Sent on Parts Request")
			else:
				if parts.branch == "Dammam - TSL-SA":

					msg1 = """Dear Purchaser, <br> <br>Please find the Evaluation Report for the Technician (%s) need price for further proceeding.<br> 
						<br><br>"""%(technician)

					msg2 = """<div><style>.sh-src a{text-decoration:none!important;}</style></div> <br> <table cellpadding="0" cellspacing="0" border="0" class="sh-src" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td align="center" style="padding: 0px 23px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 16px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/file/17u3rllxlu3i3d" alt="" title="Profile Picture" width="84" height="84" class="" style="display: block; border: 0px; max-width: 84px;"></p></td></tr></table> <table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 0px 0px;"><p style="margin: 1px;"><a href="http://tsl-me.com" target="_blank"><img src="https://signaturehound.com/api/v1/file/137twgllxlu01oi" alt="" title="Logo" width="129" height="47" style="display: block; border: 0px; max-width: 129px;"></a></p></td></tr></table></td> <td width="5" style="padding: 1px 0px 0px;"></td> <td style="padding: 0px 1px 0px 0px; vertical-align: top;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td style="padding: 0px 1px 13px 0px; border-bottom: 2px solid rgb(0,123,255); font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap;"><p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; font-weight: 700; color: rgb(0,0,0); white-space: nowrap; margin: 1px;">Muhammad Umar
                    </p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">Customer Support Executive</p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">
                      Dammam Branch </p> <p style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); margin: 1px;">
                      Technical Solutions Company for Maintenance</p> <!----></td></tr> <tr><td style="padding: 13px 1px 13px 0px; border-bottom: 2px solid rgb(0,123,255);"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/email/default/007bff.png" alt="" width="18" height="18" style="display: block; border: 0px; margin: 0px; width: 18px; height: 18px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="mailto:info-dmm@tsl-me.com" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">info-dmm@tsl-me.com</span></a></p></td></tr>  <tr><td valign="top" style="padding: 1px 5px 1px 0px; vertical-align: top;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/map/default/007bff.png" alt="" width="18" height="18" style="display: block; border: 0px; margin: 0px; width: 18px; height: 18px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,135) !important; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><a href="https://maps.app.goo.gl/VqaMGCLVvnGnotrX7?g_st=iw" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(136,136,136); text-decoration: none !important;">2nd industry، no 38، 166st X 23st Factory, Dammam 32275,<br> Saudi Arabia</span></a></p></td></tr> <tr><td valign="middle" style="padding: 1px 5px 1px 0px; vertical-align: middle;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/website/default/007bff.png" alt="" width="18" height="18" style="display: block; border: 0px; margin: 0px; width: 18px; height: 18px;"></p></td> <td style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(0,123,254) !important; font-weight: 700; padding: 1px 0px; vertical-align: middle;"><p style="margin: 1px;">
					  <a href="http://tsl-me.com" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(0,123,255); font-weight: 700; text-decoration: none !important;"><span style="font-family: Arial, sans-serif; font-size: 13px; line-height: 16px; white-space: nowrap; color: rgb(0,123,255); font-weight: 700; text-decoration: none !important;">tsl-me.com</span></a></p></td></tr></table></td></tr> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="margin: 0px; border-collapse: collapse;"><tr><td width="30" style="font-size: 0px; line-height: 0px; padding: 16px 1px 0px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/facebook/default/007bff.png" alt="" width="30" height="30" style="display: block; border: 0px; margin: 0px; width: 30px; height: 30px;"></p></td> <td width="3" style="padding: 0px 0px 1px;"></td><td width="30" style="font-size: 0px; line-height: 0px; padding: 16px 1px 0px 0px;"><p style="margin: 1px;"><img src="https://signaturehound.com/api/v1/png/linkedin/default/007bff.png" alt="" width="30" height="30" style="display: block; border: 0px; margin: 0px; width: 30px; height: 30px;"></p></td> <td width="3" style="padding: 0px 0px 1px;"></td></tr></table></td></tr></table></td></tr></table></td></tr> <!----> <tr><td style="padding: 0px 1px 0px 0px;"><table cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: 0px; border-collapse: collapse;"><tr><td style="padding: 20px 1px 0px 0px; font-family: Arial, sans-serif; font-size: 10px; line-height: 13px; color: rgb(136,136,136);"><p style="font-family: Arial, sans-serif; font-size: 10px; line-height: 13px; color: rgb(136,136,136); margin: 1px;">The content of this email is confidential and intended for the recipient specified in message only. It is strictly forbidden to share any part of this message with any third party, without a written consent of the sender. If you received this message by mistake, please reply to this message and follow with its deletion, so that we can ensure such a mistake does not occur in the future.</p></td></tr></table></td></tr> <!----> <!----></table>"""
					frappe.sendmail(
							recipients="purchase-sa1@tsl-me.com",
							sender="info-dmm@tsl-me.com",
							subject= "New Part Request",
							message= msg1+msg2,
							attachments=get_attachments(parts.name,"Evaluation Report")

							)
					frappe.msgprint("Mail Sent on Parts Request")

def get_attachments(name,doctype):
	attachments = frappe.attach_print(doctype, name,file_name=doctype, print_format="Part Sheet")
	return [attachments]