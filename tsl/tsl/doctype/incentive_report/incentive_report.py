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

		
		sp = frappe.get_all("Employee",{"designation": ["in", ["Technician",'Senior Technician',"Automation Technician"]],"company":self.company,"status":"Active","branch":self.branch,},["*"])
		# wd = frappe.get_all("Work Order Data",{"status":"RSI-Repaired and Shipped Invoiced","posting_date": ["between", (self.from_date,self.to_date)]},["*"])
		
		for i in sp:
			data += '<tr>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(i.employee_name)
			wd = frappe.get_all("Work Order Data",{"technician":i.user_id,"invoice_no": ["!=", ""],"status_cap": ["=",""]},["*"])

			rs = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" 
				and `tabWork Order Data`.technician = "%s" and DATE(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(i.user_id,self.from_date,self.to_date) ,as_dict=1)

			
			rss = frappe.db.sql(""" select DISTINCT `tabWork Order Data` .name as ct , DATE(`tabStatus Duration Details`.date) as d from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" 
				and `tabWork Order Data`.technician = "%s" and DATE(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(i.user_id,self.from_date,self.to_date) ,as_dict=1)
			
			q_m = 0
			m_cost = 0
			s_total = 0
			inv_total = 0
			total_shipping_cost = 0

			rs_count = 0

			seen = set()
			unique_rss = []
			for s in rss:
				r = frappe.db.sql(""" select DISTINCT `tabWork Order Data` .name as ct , DATE(`tabStatus Duration Details`.date) as d from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" 
				and `tabWork Order Data`.name = "%s" and DATE(`tabStatus Duration Details`.date) < '%s' LIMIT 1 """ %(s['ct'],self.from_date) ,as_dict=1)
				
				if not r:
					if s['ct'] not in seen:
					# if i.user_id == "sampath@tsl-me.com":
					# 	frappe.errprint(s['ct'])
						seen.add(s['ct'])
						unique_rss.append(s['ct'])
						rs_count = rs_count + 1

			if self.company == "TSL COMPANY - Kuwait":
				for j in unique_rss:
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
					and `tabQuotation Item`.wod_no = '%s' ''' %(j) ,as_dict=1)

					if q_amt:
						
						for k in q_amt:
							if k.is_m == 1:
								
								per = (k.up * k.dis)/100
								amt = k.up - per
								if i.user_id == "sami@tsl-me.com":
									frappe.errprint(j)
									frappe.errprint(amt)
								q_m = q_m + amt
								


							else:
								amt = k.adc
								if i.user_id == "sami@tsl-me.com":
									frappe.errprint(j)
									frappe.errprint(amt)
									
								q_m = q_m + amt
								

			
			if self.company == "TSL COMPANY - KSA" or self.company == "TSL COMPANY - UAE":
				for j in unique_rss:
					q_amt= frappe.db.sql(''' select `tabQuotation`.name as q_name,
					`tabQuotation`.default_discount_percentage as dis,
					`tabQuotation`.is_multiple_quotation as is_m,
					`tabQuotation`.after_discount_cost as adc,
					`tabQuotation`.Workflow_state,
					`tabQuotation`.grand_total as gt,
					`tabQuotation Item`.unit_price as up,
					`tabQuotation Item`.margin_amount as mar,
					`tabQuotation Item`.margin_amount as ma from `tabQuotation` 
					left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
					where `tabQuotation`.Workflow_state in ("Approved By Customer") and
					`tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")
					and `tabQuotation Item`.wod_no = '%s' ''' %(j) ,as_dict=1)

					if q_amt:
						q_m = q_m + q_amt[0]["gt"]


			wd = frappe.db.sql(""" select DISTINCT `tabWork Order Data` .name as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.status_cap IS NULL
			and `tabWork Order Data`.technician = "%s" and DATE(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(i.user_id,self.from_date,self.to_date) ,as_dict=1)
			

			wds = frappe.db.sql(""" select DISTINCT `tabWork Order Data` .name as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped"
			and `tabWork Order Data`.technician = "%s" and DATE(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(i.user_id,self.from_date,self.to_date) ,as_dict=1)
			
			
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


			


							

			ner = frappe.db.sql("""
			SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS ct 
			FROM `tabWork Order Data`
			LEFT JOIN `tabStatus Duration Details` 
				ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			WHERE `tabStatus Duration Details`.status = "NER-Need Evaluation Return" 
			AND `tabWork Order Data`.technician = %s 
			AND DATE(`tabStatus Duration Details`.date)BETWEEN %s AND %s
			""", (i.user_id, self.from_date, self.to_date), as_dict=1)

			
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(rs_count)
			
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner[0]["ct"])

		
			count_a = 0
			count_b = 0
			count_c = 0
			count_d = 0

			
			
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

			
			data += '</tr>'	
		data += '</table>'

		return data

