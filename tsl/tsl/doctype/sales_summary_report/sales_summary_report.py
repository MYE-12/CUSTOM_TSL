# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class SalesSummaryReport(Document):

	@frappe.whitelist()
	def get_work_orders(self):
		# RSI
		if self.report == "RSI-Repaired and Shipped Invoiced":
			data= ""
			data += '<table class="table table-bordered">'
			data += '<tr>'
			data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>S.No</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Date</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Work Order</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Sales Person</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Sales Invoice</b><center></td>'
			data += '<td style="border-color:#000000;width:40%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Customer</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Amount</b><center></td>'
			data += '</tr>'
			
			if self.customer:
				si = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.posting_date,`tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
				left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
				where `tabSales Invoice`.status = "Overdue" and `tabSales Invoice`.posting_date between '%s' and '%s' and `tabSales Invoice`.customer = '%s' ORDER BY `tabSales Invoice`.posting_date ASC """ %(self.from_date,self.to_date,self.customer),as_dict =1)
			
			elif self.sales_person:
				si = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.posting_date, `tabSales Team`.sales_person,`tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
				left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
				right join `tabSales Team` on `tabSales Invoice`.name = `tabSales Team`.parent
				where `tabSales Invoice`.status = "Overdue" and `tabSales Team`.sales_person = '%s' and `tabSales Invoice`.posting_date between '%s' and '%s' ORDER BY `tabSales Invoice`.posting_date ASC """ %(self.sales_person,self.from_date,self.to_date),as_dict =1)

			elif self.work_order_data:
				si = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.posting_date,`tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
				left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
				where `tabSales Invoice`.posting_date between '%s' and '%s' and `tabSales Invoice Item`.work_order_data = '%s' ORDER BY `tabSales Invoice`.posting_date ASC """ %(self.from_date,self.to_date,self.work_order_data),as_dict =1)
				if not si:
					si = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.posting_date,`tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
					left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
					where `tabSales Invoice`.status = "Overdue" and  `tabSales Invoice`.posting_date between '%s' and '%s' and `tabSales Invoice Item`.wod_no = '%s' ORDER BY `tabSales Invoice`.posting_date ASC """ %(self.from_date,self.to_date,self.work_order_data),as_dict =1)

			else:
				si = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.posting_date,`tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
				left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
				where `tabSales Invoice`.status = "Overdue" and  `tabSales Invoice`.posting_date between '%s' and '%s' ORDER BY `tabSales Invoice`.posting_date ASC """ %(self.from_date,self.to_date),as_dict =1)


		
			wod_list = []
			for j in si:
				if j["wo"]:
					wod_list.append(j["wo"])
				
				else:
					wod_list.append(j["w"])
					

			sn = 0
			total_amt = 0
			for i in wod_list:
				
				st = frappe.get_value("Work Order Data",{"name":i},["Status"])
				
				if i:
					sid_1 = frappe.db.sql(""" select `tabSales Invoice`.posting_date from `tabSales Invoice` 
					left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
					where `tabSales Invoice Item`.work_order_data = '%s' """ %(i),as_dict =1)

					sid_2 = frappe.db.sql(""" select `tabSales Invoice`.posting_date from `tabSales Invoice` 
					left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
					where `tabSales Invoice Item`.wod_no = '%s' """ %(i),as_dict =1)
			

				
					customer = frappe.get_value("Work Order Data",{"name":i},["customer"])
				

					sales_rep_1 = frappe.db.sql(""" select `tabSales Team`.sales_person from `tabSales Invoice` 
					left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
					right join `tabSales Team` on `tabSales Invoice`.name = `tabSales Team`.parent
					where `tabSales Invoice Item`.work_order_data = '%s' """ %(i),as_dict =1)
					
					sales_rep_2 = frappe.db.sql(""" select `tabSales Team`.sales_person from `tabSales Invoice` 
					left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
					right join `tabSales Team` on `tabSales Invoice`.name = `tabSales Team`.parent
					where `tabSales Invoice Item`.wod_no = '%s' """ %(i),as_dict =1)
					

					if sid_1:
						input_date_string = str(sid_1[0]["posting_date"])
					else:
						input_date_string = str(sid_2[0]["posting_date"])

					if input_date_string:
						input_date = datetime.strptime(input_date_string, "%Y-%m-%d")

				
					formatted_date = input_date.strftime("%d-%m-%Y")
					
					wo = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.name, `tabSales Invoice Item`.amount as amount from `tabSales Invoice` 
					left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
					where `tabSales Invoice Item`.work_order_data = '%s' """ %(i),as_dict =1)
					amt = 0
					n = []
					if wo:
						amt = wo[0]["amount"]
						n.append(wo[0]["name"])
						n = str(n).strip('[]')
						n = n.replace("'", '')
						
					
					else:
						wos = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.name,`tabSales Invoice Item`.amount as amount from `tabSales Invoice` 
						left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
						where `tabSales Invoice Item`.wod_no = '%s' """ %(i),as_dict =1)
						amt = wos[0]["amount"]
						n.append(wos[0]["name"])
						n = str(n).strip('[]')
						n = n.replace("'", '')
					
					
					total_amt = total_amt + amt
					sn = sn + 1
					data += '<tr>'
					data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sn)
					
					data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date)
					
					
					data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/work-order-data/%s"target="_blank">%s</a><center></td>'%(i,i)
					if sales_rep_1:
						data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sales_rep_1[0]["sales_person"] or "-" )
					elif sales_rep_2:
						data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sales_rep_2[0]["sales_person"] or "-" )
					else:
						data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%("-" )

					
						
					
					data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/sales-invoice/%s"target="_blank">%s</a><center></td>'%(n,n)
					data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(customer)
					data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(format(amt, ".2f"))
				
			data += '<tr>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Total</b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>%s</b><center></td>'%(format(total_amt, ".2f"))
			data += '</tr>'
			data += '</table>'
		


		#RSC
		if self.report == "RSC-Repaired and Shipped Client":
			data= ""
			data += '<table class="table table-bordered">'
			data += '<tr>'
			data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>S.No</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Date</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Work Order</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Sales Person</b><center></td>'
			data += '<td style="border-color:#000000;width:30%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Customer</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Delivery Note</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Delivery Date</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Amount</b><center></td>'
			
			data += '</tr>'
			
			if self.customer:
				wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (self.from_date,self.to_date)],"status":"RSC-Repaired and Shipped Client","customer":self.customer},["*"])

			elif self.sales_person:
				wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (self.from_date,self.to_date)],"status":"RSC-Repaired and Shipped Client","sales_rep":self.sales_person},["*"])

			elif self.work_order_data:
				wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (self.from_date,self.to_date)],"status":"RSC-Repaired and Shipped Client","name":self.work_order_data},["*"])

			else:
				wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (self.from_date,self.to_date)],"status":"RSC-Repaired and Shipped Client"},["*"])
			
			sn = 0
			total_rsc = 0
			for i in wd:
				amount = 0
				amt = frappe.db.sql(""" select `tabQuotation`.after_discount_cost as cost  from `tabQuotation` 
				left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
				where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Customer' """ %(i.name),as_dict =1)
				if amt:
					amount = amt[0]["cost"]
				else:
					am = frappe.db.sql(""" select `tabQuotation`.after_discount_cost as cos  from `tabQuotation` 
					left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
					where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Management' """ %(i.name),as_dict =1)
					if am:
						amount = am[0]["cos"]
					
				

				sn = sn+1

				input_date_string_1 = str(i.posting_date)
				input_date_string_2 = str(i.dn_date)

				input_date_1 = datetime.strptime(input_date_string_1, "%Y-%m-%d")
				if i.dn_date:
					input_date_2 = datetime.strptime(input_date_string_2, "%Y-%m-%d")


				formatted_date_1 = input_date_1.strftime("%d-%m-%Y")
				if input_date_2:
					formatted_date_2 = input_date_2.strftime("%d-%m-%Y")
				
					
				data += '<tr>'
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sn)
					
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date_1)
				
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/work-order-data/%s"target="_blank">%s</a><center></td>'%(i.name,i.name)
					
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.sales_rep)

				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.customer)
					
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/delivery-note/%s"target="_blank">%s</a><center></td>'%(i.dn_no,i.dn_no)					

				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date_2 or '')

				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(format(amount, ".2f"))
				total_rsc = total_rsc + amount
			
			data += '<tr>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Total</b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>%s</b><center></td>'%(format(total_rsc, ".2f"))
			data += '</tr>'

					
		#Q-Quoted
		if self.report == "Q-Quoted":
			data= ""
			data += '<table class="table table-bordered">'
			data += '<tr>'
			data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>S.No</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Date</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Work Order</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Sales Person</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Quotation</b><center></td>'
			data += '<td style="border-color:#000000;width:35%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Customer</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Amount</b><center></td>'
			data += '</tr>'
			
			if self.customer:
				wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (self.from_date,self.to_date)],"status":"Q-Quoted","customer":self.customer},["*"])

			elif self.sales_person:
				wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (self.from_date,self.to_date)],"status":"Q-Quoted","sales_rep":self.sales_person},["*"])

			elif self.work_order_data:
				wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (self.from_date,self.to_date)],"status":"Q-Quoted","name":self.work_order_data},["*"])

			else:
				wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (self.from_date,self.to_date)],"status":"Q-Quoted"},["*"])
			
			sn = 0
			total_amt = 0
			for i in wd:
				sn = sn+1
				ada  = si = frappe.db.sql(""" select DISTINCT `tabQuotation`.is_multiple_quotation as multi,`tabQuotation`.name as qname,`tabQuotation Item`.margin_amount as ma,`tabQuotation`.after_discount_cost as adc from `tabQuotation` 
				left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
				where `tabQuotation Item`.wod_no = '%s' """ %(i.name),as_dict =1)
				amt = 0
				if ada:
					if ada[0]["multi"] == 1:
						amt = ada[0]["ma"]
					else:
						amt = ada[0]["adc"]

				total_amt = total_amt + amt

				
				input_date_string = str(i.posting_date)

				input_date = datetime.strptime(input_date_string, "%Y-%m-%d")

				formatted_date = input_date.strftime("%d-%m-%Y")
					

				data += '<tr>'
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sn)
					
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date)
				
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/work-order-data/%s"target="_blank">%s</a><center></td>'%(i.name,i.name)
					
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.sales_rep)

				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/quotation/%s"target="_blank">%s</a><center></td>'%(ada[0]["qname"],ada[0]["qname"])					

				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.customer)
					
			
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(amt)
		
			data += '<tr>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Total</b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>%s</b><center></td>' %(total_amt)
			data += '</tr>'

		return data
	
	

	
