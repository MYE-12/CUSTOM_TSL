# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class IncentiveReport(Document):
	@frappe.whitelist()
	def get_work_orders(self):
		data= ""
		data += '<table class="table table-bordered">'

		data += '<tr>'
		data += '<td colspan = 1 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
		data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>RS</b><center></td>'
		data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>NER</b><center></td>'
		data += '<td colspan = 1 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
		data += '</tr>'	
		

		data += '<tr>' 
		data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center>RANGE<center></td>'
		data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center>1 - 320<center></td>'
		data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center>320 - 640<center></td>'
		data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center>640 - 1200<center></td>'
		data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center>1200 ><center></td>'
		data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center><center></td>'
		data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center>1 - 320<center></td>'
		data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center>320 - 640<center></td>'
		data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center>640 - 1200<center></td>'
		data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center>1200 ><center></td>'
		data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center><center></td>'
		data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;"><center><center></td>'
		data += '</tr>'	 


		data += '<tr>'
		data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>TECHNICIAN</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>A</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>B</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>C</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>D</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>TOTAL</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>A</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>B</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>C</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>D</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>TOTAL</b><center></td>'
		data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>SUB TOTAL</b><center></td>'
		data += '</tr>'	

		
		sp = frappe.get_all("Employee",{"designation": ["in", ["TECHNICIAN",'SENIOR TECHNICIAN']],"company":self.company},["*"])
		# wd = frappe.get_all("Work Order Data",{"status":"RSI-Repaired and Shipped Invoiced","posting_date": ["between", (self.from_date,self.to_date)]},["*"])
		for i in sp:
			data += '<tr>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(i.employee_name)
			wd = frappe.get_all("Work Order Data",{"technician":i.user_id,"invoice_no": ["!=", ""],"status_cap": ["=",""]},["*"])
			

			count_a = 0
			count_b = 0
			count_c = 0
			count_d = 0
			frappe.errprint(i.employee_name)
			for j in wd:
				sales = frappe.db.sql(""" select `tabSales Invoice`.posting_date,`tabSales Invoice Item`.amount  from `tabSales Invoice`
				left join `tabSales Invoice Item` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
				where `tabSales Invoice Item`.wod_no = '%s' or `tabSales Invoice Item`.work_order_data = '%s' and `tabSales Invoice`.status IN ('Paid', 'Overdue','Unpaid') """ %(j.name,j.name),as_dict = 1)
				if sales:
					from_date = datetime.strptime(str(self.from_date), "%Y-%m-%d").date()
					to_date = datetime.strptime(str(self.to_date), "%Y-%m-%d").date()
					if sales[0]["posting_date"] >= from_date and sales[0]["posting_date"] <= to_date:
						if sales[0]["amount"] > 0 and sales[0]["amount"] < 320:
							count_a = count_a + 1
							frappe.errprint(j.name)
							frappe.errprint(sales[0]["amount"])
						elif sales[0]["amount"] >= 320 and sales[0]["amount"] < 640:
							count_b = count_b + 2
							frappe.errprint(j.name)
							frappe.errprint(sales[0]["amount"])
						elif sales[0]["amount"] >=640 and sales[0]["amount"] < 1200:
							count_c = count_c + 3
							frappe.errprint(j.name)
							frappe.errprint(sales[0]["amount"])
						elif sales[0]["amount"] >= 1200:
							count_d = count_d + 4
							frappe.errprint(j.name)
							frappe.errprint(sales[0]["amount"])

			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_a)
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_b)
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_c)
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_d)
			t_cnt = count_a + count_b + count_c + count_d
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(t_cnt)
			
			
			
			ner = frappe.get_all("Work Order Data",{"technician":i.user_id,"invoice_no": ["!=", ""],"status_cap_date": ["between", (self.from_date,self.to_date)]},["*"])
			ner_count_a = 0
			ner_count_b = 0
			ner_count_c = 0
			ner_count_d = 0
			
			for k in ner:
				sales = frappe.db.sql(""" select `tabSales Invoice`.name,`tabSales Invoice Item`.amount  from `tabSales Invoice`
				left join `tabSales Invoice Item` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
				where `tabSales Invoice`.posting_date between '%s' and '%s' and `tabSales Invoice Item`.wod_no = '%s' or `tabSales Invoice Item`.work_order_data = '%s' and `tabSales Invoice`.status IN ('Paid', 'Overdue','Unpaid') """ %(self.from_date,self.to_date,j.name,j.name),as_dict = 1)
				if sales:
					if sales[0]["amount"] > 0 and sales[0]["amount"] < 320:
						ner_count_a = ner_count_a + 1
					if sales[0]["amount"] >= 320 and sales[0]["amount"] < 640:
						ner_count_b = ner_count_b + 2
					if sales[0]["amount"] >=640 and sales[0]["amount"] <1200:
						ner_count_c = ner_count_c + 3
					if sales[0]["amount"] >= 1200:
						ner_count_d = ner_count_d + 4
			
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_a)
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_b)
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_c)
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_d)
			ner_t_cnt = ner_count_a + ner_count_b + ner_count_c + ner_count_d
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_t_cnt)
			
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(t_cnt - ner_t_cnt)
			
			data += '</tr>'	
		data += '</table>'

		return data

