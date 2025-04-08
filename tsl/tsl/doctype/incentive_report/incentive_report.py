# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from erpnext.setup.utils import get_exchange_rate

class IncentiveReport(Document):
	@frappe.whitelist()
	def get_work_orders(self):
		data= ""
		data += '<table class="table table-bordered">'

		# data += '<tr>'
		# data += '<td colspan = 1 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b></b><center></td>'
		# data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>RS</b><center></td>'
		# data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>NER</b><center></td>'
		# data += '<td colspan = 1 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b></b><center></td>'
		# data += '</tr>'	
		

		# data += '<tr>' 
		# data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center>RANGE<center></td>'
		# data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center>1 - 320<center></td>'
		# data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center>320 - 640<center></td>'
		# data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center>640 - 1200<center></td>'
		# data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center>1200 ><center></td>'
		# data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center><center></td>'
		# data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center>1 - 320<center></td>'
		# data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center>320 - 640<center></td>'
		# data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center>640 - 1200<center></td>'
		# data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center>1200 ><center></td>'
		# data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center><center></td>'
		# data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;font-weight:bold;"><center><center></td>'
		# data += '</tr>'	 


		data += '<tr>'
		data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>TECHNICIAN</b><center></td>'

		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>Total RS WO Count</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>Total RS Amount</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>Total Material Cost</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>NET Amount</b><center></td>'

		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>NER COUNT</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>NER % Against RS</b><center></td>'
		
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>NER DEDUCTION AMT</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>NER DEDUCTION COMMISSION</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>AMT AFTER DEDUCTION</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>COMMISSION</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>AFTER DEDUCTION COMMISSION</b><center></td>'
		# data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>TOTAL</b><center></td>'
		# data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>SUB TOTAL</b><center></td>'
		data += '</tr>'	

		
		sp = frappe.get_all("Employee",{"designation": ["in", ["Technician",'Senior Technician',"Automation Technician"]],"company":self.company,"status":"Active"},["*"])
		# wd = frappe.get_all("Work Order Data",{"status":"RSI-Repaired and Shipped Invoiced","posting_date": ["between", (self.from_date,self.to_date)]},["*"])
		for i in sp:
			data += '<tr>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(i.employee_name)
			wd = frappe.get_all("Work Order Data",{"technician":i.user_id,"invoice_no": ["!=", ""],"status_cap": ["=",""]},["*"])

			rs = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped"  and `tabWork Order Data`.status_cap IS NULL
				and `tabWork Order Data`.technician = "%s" and DATE(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(i.user_id,self.from_date,self.to_date) ,as_dict=1)

			ner = frappe.db.sql("""
			SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS ct 
			FROM `tabWork Order Data`
			LEFT JOIN `tabStatus Duration Details` 
				ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			WHERE `tabStatus Duration Details`.status = "NER-Need Evaluation Return" 
			AND `tabWork Order Data`.technician = %s 
			AND DATE(`tabStatus Duration Details`.date)BETWEEN %s AND %s
			""", (i.user_id, self.from_date, self.to_date), as_dict=1)

			
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(rs[0]["ct"])
			
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner[0]["ct"])

		
			count_a = 0
			count_b = 0
			count_c = 0
			count_d = 0

			wd = frappe.db.sql(""" select DISTINCT `tabWork Order Data` .name as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.status_cap IS NULL
			and `tabWork Order Data`.technician = "%s" and DATE(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(i.user_id,self.from_date,self.to_date) ,as_dict=1)
			

			wds = frappe.db.sql(""" select DISTINCT `tabWork Order Data` .name as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped"
			and `tabWork Order Data`.technician = "%s" and DATE(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(i.user_id,self.from_date,self.to_date) ,as_dict=1)
			
			q_m = 0
			m_cost = 0
			s_total = 0
			inv_total = 0
			total_shipping_cost = 0
			for j in wds:
				ev = frappe.db.sql(""" select  `tabPart Sheet Item`.total as t from `tabEvaluation Report` 
				left join `tabPart Sheet Item` on `tabEvaluation Report`.name = `tabPart Sheet Item`.parent
				where  `tabEvaluation Report`.work_order_data = '%s' """ %(j.ct) ,as_dict=1)
				if ev:
					for e in ev:
						if e["t"]:
							inv_total = inv_total + e["t"]
				
				s_amt = frappe.get_all("Supplier Quotation",{"work_order_data":j.ct,"workflow_state":"Approved By Management"},["*"])
				s_amt= frappe.db.sql(''' select base_total as b_am,shipping_cost as ship from `tabSupplier Quotation` 
				where Workflow_state in ("Approved By Management") and
				work_order_data = '%s' ''' %(j.ct) ,as_dict=1)
				if s_amt:
					for s in s_amt:
						# s_total = s_total + s.base_total
						s_cur = frappe.get_value("Supplier",{"name":s.supplier},["default_currency"])
						exr = get_exchange_rate(s_cur,"KWD")
						if s.shipping_cost:
							s_total = s_total + (s.shipping_cost * exr)
					# s_total = s_total + s_amt[0]["b_am"]

			

			for j in wd:
				# q_m = 0
				
				# s_amt = frappe.get_all("Supplier Quotation",{"work_order_data":j.ct,"workflow_state":"Approved By Management"},["*"])
				# s_amt= frappe.db.sql(''' select base_total as b_am,shipping_cost as ship from `tabSupplier Quotation` 
				# where Workflow_state in ("Approved By Management") and
				# work_order_data = '%s' ''' %(j.ct) ,as_dict=1)
				# if s_amt:
					
				# 	for s in s_amt:
				# 		s_total = s_total + s.base_total
				# 		s_cur = frappe.get_value("Supplier",{"name":s.supplier},["default_currency"])
				# 		exr = get_exchange_rate(s_cur,"KWD")
						
				# 		if s.shipping_cost:
				# 			s_total = s_total + (s.shipping_cost * exr)
				# 	# s_total = s_total + s_amt[0]["b_am"]
				# else:
				# 	ev = frappe.db.sql(""" select  `tabPart Sheet Item`.total as t from `tabEvaluation Report` 
				# 	left join `tabPart Sheet Item` on `tabEvaluation Report`.name = `tabPart Sheet Item`.parent
				# 	where  `tabEvaluation Report`.work_order_data = '%s' """ %(j.ct) ,as_dict=1)
				# 	if ev:
				# 		for e in ev:
				# 			if e["t"]:
								
				# 				inv_total = inv_total + e["t"]

				# mt = frappe.db.sql(""" select  `tabItem Price Details`.amount as t,`tabItem Price Details`.supplier_quotation as sq from `tabQuotation` 
				# 	left join `tabItem Price Details` on `tabQuotation`.name = `tabItem Price Details`.parent
				# 	where  `tabItem Price Details`.work_order_data = '%s' and `tabQuotation`.workflow_state = "Approved By Customer" """ %(j.ct) ,as_dict=1)
				
				# if mt:
				# 	for i in mt:
				# 		
				# 		
				# 		m_cost = m_cost + i["t"]
				# 		if i["sq"]:
				# 			supplier = frappe.get_value("Supplier Quotation",{"name":i["sq"]},["supplier"])
				# 			supplier_cur = frappe.get_value("Supplier",{"name":supplier},["default_currency"])
				# 			shipping_cost = frappe.get_value("Supplier Quotation",{"name":i["sq"]},["shipping_cost"])
				# 			exr = get_exchange_rate(supplier_cur,"KWD")
				# 			if shipping_cost:
				# 				shipping_cost = shipping_cost * exr
				# 				total_shipping_cost = total_shipping_cost + shipping_cost
				# else:
				

				q_amt= frappe.db.sql(''' select `tabQuotation`.name as q_name,
				`tabQuotation`.default_discount_percentage as dis,
				`tabQuotation`.is_multiple_quotation as is_m,
				`tabQuotation`.after_discount_cost as adc,
				`tabQuotation`.Workflow_state,
				`tabQuotation Item`.unit_price as up,
				`tabQuotation Item`.margin_amount as mar,
				`tabQuotation Item`.margin_amount as ma from `tabQuotation` 
				left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
				where `tabQuotation`.Workflow_state in ("Approved By Customer") and
				`tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")
				and `tabQuotation Item`.wod_no = '%s' ''' %(j.ct) ,as_dict=1)

				if q_amt:
					
					for k in q_amt:
						if k.is_m == 1:
							
							per = (k.up * k.dis)/100
							amt = k.up - per
							
							q_m = q_m + amt


						else:
							amt = k.adc
						
							q_m = q_m + amt

			
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(f"{round(q_m):,}")
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(f"{round(s_total + inv_total):,}")
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(f"{round(q_m - (round(s_total + inv_total))):,}") 
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner[0]["ct"])
			
			
			if rs[0]["ct"] == 0:
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s%s</b><center></td>' %(rs[0]["ct"],"%")
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s%s</b><center></td>' %(round((ner[0]["ct"]/rs[0]["ct"])*100),"%")
			
			if rs[0]["ct"] == 0:
				nar = 0
			else:
				nar = round((ner[0]["ct"]/rs[0]["ct"])*100)


			to_rs = round(q_m,2)
			ner_deduct = (nar * to_rs)/100
			net_amount =  round((q_m - round(s_total + inv_total)),2)
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(f"{round(ner_deduct):,}")
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(f"{round(ner_deduct*2/100):,}")
			aad = round(net_amount - ner_deduct,2)
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(f"{round(aad):,}")
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(f"{round(aad*2/100):,}") 
			ner_d_com =  round(ner_deduct*2/100)
			aad_d_com = round(aad*2/100)		
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(f"{aad_d_com-ner_d_com:,}") 

			
			# 	sales = frappe.db.sql(""" select `tabSales Invoice`.posting_date,`tabSales Invoice Item`.amount  from `tabSales Invoice`
			# 	left join `tabSales Invoice Item` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
			# 	where `tabSales Invoice Item`.wod_no = '%s' or `tabSales Invoice Item`.work_order_data = '%s' and `tabSales Invoice`.status IN ('Paid', 'Overdue','Unpaid') """ %(j.name,j.name),as_dict = 1)
			# 	if sales:
			# 		from_date = datetime.strptime(str(self.from_date), "%Y-%m-%d").date()
			# 		to_date = datetime.strptime(str(self.to_date), "%Y-%m-%d").date()
			# 		if sales[0]["posting_date"] >= from_date and sales[0]["posting_date"] <= to_date:
			# 			if sales[0]["amount"] > 0 and sales[0]["amount"] < 320:
			# 				count_a = count_a + 1
							
			# 			elif sales[0]["amount"] >= 320 and sales[0]["amount"] < 640:
			# 				count_b = count_b + 2
							
			# 			elif sales[0]["amount"] >=640 and sales[0]["amount"] < 1200:
			# 				count_c = count_c + 3
							
			# 			elif sales[0]["amount"] >= 1200:
			# 				count_d = count_d + 4
							

			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_a)
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_b)
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_c)
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_d)
			# t_cnt = count_a + count_b + count_c + count_d
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(t_cnt)
			
			
			
			# ner = frappe.get_all("Work Order Data",{"technician":i.user_id,"status_cap_date": ["between", (self.from_date,self.to_date)]},["*"])
			# ner_count_a = 0
			# ner_count_b = 0
			# ner_count_c = 0
			# ner_count_d = 0
			
			# for k in ner:
			# 	sales = frappe.db.sql(""" select `tabSales Invoice`.name,`tabSales Invoice Item`.amount  from `tabSales Invoice`
			# 	left join `tabSales Invoice Item` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
			# 	where `tabSales Invoice Item`.wod_no = '%s' or `tabSales Invoice Item`.work_order_data = '%s' and `tabSales Invoice`.status IN ('Paid', 'Overdue','Unpaid') """ %(j.name,j.name),as_dict = 1)
			# 	if sales:
			# 		if sales[0]["amount"] > 0 and sales[0]["amount"] < 320:
			# 			ner_count_a = ner_count_a + 1
			# 		if sales[0]["amount"] >= 320 and sales[0]["amount"] < 640:
			# 			ner_count_b = ner_count_b + 2
			# 		if sales[0]["amount"] >=640 and sales[0]["amount"] <1200:
			# 			ner_count_c = ner_count_c + 3
			# 		if sales[0]["amount"] >= 1200:
			# 			ner_count_d = ner_count_d + 4
			
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_a)
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_b)
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_c)
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_d)
			# ner_t_cnt = ner_count_a + ner_count_b + ner_count_c + ner_count_d
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_t_cnt)
			
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(t_cnt - ner_t_cnt)
			
			data += '</tr>'	
		data += '</table>'

		return data

