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
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Invoice Date</b><center></td>'
			data += '<td style="border-color:#000000;width:40%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Customer</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Amount</b><center></td>'
			data += '</tr>'

			filters = [
			"sdd.status = 'RSI-Repaired and Shipped Invoiced' ",
			"wod.posting_date BETWEEN %s AND %s",
			]
			params = [self.from_date, self.to_date]

			for field, value in [
				("customer", self.customer),
				("sales_rep", self.sales_person or self.sales),
				("work_order_data", self.work_order_data),
				("company", self.company)
			]:
				if value:
					filters.append(f"wod.{field} = %s")
					params.append(value)
					break

			query = f"""
				SELECT DISTINCT wod.name AS name,
				wod.posting_date,
				wod.sales_rep,
				wod.customer,
				wod.invoice_date,
				wod.invoice_no
				FROM `tabWork Order Data` wod
				LEFT JOIN `tabStatus Duration Details` sdd ON wod.name = sdd.parent
				WHERE {' AND '.join(filters)}
			"""

			wd = frappe.db.sql(query, tuple(params), as_dict=True)

					
			sn = 0
			total_rsi = 0
			for i in wd:
				amount = 0
				if self.company == "TSL COMPANY - Kuwait":
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
				else:
					amt = frappe.db.sql(""" select `tabQuotation Item`.net_amount as cost  from `tabQuotation` 
					left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
					where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Customer' """ %(i.name),as_dict =1)
					if amt:
						amount = amt[0]["cost"]
					else:
						am = frappe.db.sql(""" select `tabQuotation Item`.net_amount as cos from `tabQuotation` 
						left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
						where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Management' """ %(i.name),as_dict =1)
						if am:
							amount = am[0]["cos"]
					
				

				sn = sn+1

				input_date_string_1 = str(i.posting_date)
				input_date_1 = datetime.strptime(input_date_string_1, "%Y-%m-%d")
				formatted_date_1 = input_date_1.strftime("%d-%m-%Y")

				input_date_string_2 = str(i.invoice_date)
				input_date_2 = datetime.strptime(input_date_string_2, "%Y-%m-%d")
				formatted_date_2 = input_date_2.strftime("%d-%m-%Y")
				

				total_rsi = total_rsi + amount
				sn = sn + 1
				data += '<tr>'
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sn)
				
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date_1)
				
				
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/work-order-data/%s"target="_blank">%s</a><center></td>'%(i.name,i.name)
				
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.sales_rep or "-" )
				
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/sales-invoice/%s"target="_blank">%s</a><center></td>'%(i.invoice_no,i.invoice_no)
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date_2)
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.customer)			
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(format(amount, ".2f"))
				
			data += '<tr>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Total</b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>%s</b><center></td>'%(format(total_rsi, ".2f"))
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
			filters = [
			"sdd.status = 'RSC-Repaired and Shipped Client' ",
			"wod.posting_date BETWEEN %s AND %s",
			]
			params = [self.from_date, self.to_date]
			
			for field, value in [
				("customer", self.customer),
				("sales_rep", self.sales_person or self.sales),
				("work_order_data", self.work_order_data),
				("company", self.company)
			]:
				if value:
					filters.append(f"wod.{field} = %s")
					params.append(value)
					break

			query = f"""
				SELECT DISTINCT wod.name AS name,
				wod.posting_date,
				wod.sales_rep,
				wod.customer,
				wod.dn_date,
				wod.dn_no
				FROM `tabWork Order Data` wod
				LEFT JOIN `tabStatus Duration Details` sdd ON wod.name = sdd.parent
				WHERE {' AND '.join(filters)}
			"""

			wd = frappe.db.sql(query, tuple(params), as_dict=True)

						
			sn = 0
			total_rsc = 0
			for i in wd:
				amount = 0
				if self.company == "TSL COMPANY - Kuwait":
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
				else:
					amt = frappe.db.sql(""" select `tabQuotation Item`.net_amount as cost  from `tabQuotation` 
					left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
					where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Customer' """ %(i.name),as_dict =1)
					if amt:
						amount = amt[0]["cost"]
					else:
						am = frappe.db.sql(""" select `tabQuotation Item`.net_amount as cos  from `tabQuotation` 
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

		
		#RS
		if self.report == "RS-Repaired and Shipped":
			data= ""
			data += '<table class="table table-bordered">'
			data += '<tr>'
			data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>S.No</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Date</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Work Order</b><center></td>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Sales Person</b><center></td>'
			data += '<td style="border-color:#000000;width:30%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Customer</b><center></td>'
			# data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Amount</b><center></td>'
			
			data += '</tr>'
			filters = [
			"wod.status = 'RS-Repaired and Shipped' ",
			"wod.posting_date BETWEEN %s AND %s",
			]
			params = [self.from_date, self.to_date]
			
			for field, value in [
				("customer", self.customer),
				("sales_rep", self.sales_person or self.sales),
				("work_order_data", self.work_order_data),
				("company", self.company)
			]:
				if value:
					filters.append(f"wod.{field} = %s")
					params.append(value)
					break

			query = f"""
				SELECT wod.name AS name,
				wod.posting_date,
				wod.sales_rep,
				wod.customer,
				wod.dn_date,
				wod.dn_no
				FROM `tabWork Order Data` wod
				
				WHERE {' AND '.join(filters)}
			"""

			wd = frappe.db.sql(query, tuple(params), as_dict=True)

						
			sn = 0
			total_rsc = 0
			for i in wd:
				amount = 0
				if self.company == "TSL COMPANY - Kuwait":
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
				else:
					amt = frappe.db.sql(""" select `tabQuotation Item`.net_amount as cost  from `tabQuotation` 
					left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
					where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Customer' """ %(i.name),as_dict =1)
					if amt:
						amount = amt[0]["cost"]
					else:
						am = frappe.db.sql(""" select `tabQuotation Item`.net_amount as cos  from `tabQuotation` 
						left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
						where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Management' """ %(i.name),as_dict =1)
						if am:
							amount = am[0]["cos"]
					
				

				sn = sn+1

				input_date_string_1 = str(i.posting_date)
				

				input_date_1 = datetime.strptime(input_date_string_1, "%Y-%m-%d")
				

				formatted_date_1 = input_date_1.strftime("%d-%m-%Y")
				
					
				data += '<tr>'
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sn)
					
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date_1)
				
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/work-order-data/%s"target="_blank">%s</a><center></td>'%(i.name,i.name)
					
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.sales_rep)

				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.customer)
					
				
				# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(format(amount, ".2f"))
				total_rsc = total_rsc + amount
			
			# data += '<tr>'
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Total</b><center></td>'
			# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>%s</b><center></td>'%(format(total_rsc, ".2f"))
			# data += '</tr>'

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
			
			filters = [
			"sdd.status = 'A-Approved' ",
			"wod.posting_date BETWEEN %s AND %s",
			]
			params = [self.from_date, self.to_date]
			
			for field, value in [
				("customer", self.customer),
				("sales_rep", self.sales_person or self.sales),
				("work_order_data", self.work_order_data),
				("company", self.company)
			]:
				if value:
					filters.append(f"wod.{field} = %s")
					params.append(value)
					break

			query = f"""
				SELECT DISTINCT wod.name AS name,
				wod.posting_date,
				wod.sales_rep,
				wod.customer
				FROM `tabWork Order Data` wod
				LEFT JOIN `tabStatus Duration Details` sdd ON wod.name = sdd.parent
				WHERE {' AND '.join(filters)}
			"""

			wd = frappe.db.sql(query, tuple(params), as_dict=True)

		
						
			sn = 0
			total_amt = 0
			for i in wd:
				sn = sn+1
				amount = 0
				name = ""
				if self.company == "TSL COMPANY - Kuwait":
					amt = frappe.db.sql(""" select `tabQuotation`.name as n,`tabQuotation`.after_discount_cost as cost  from `tabQuotation` 
					left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
					where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Customer' """ %(i.name),as_dict =1)
					if amt:
						amount = amt[0]["cost"]
						name = amt[0]["n"]
					else:
						am = frappe.db.sql(""" select `tabQuotation`.name as n,`tabQuotation`.after_discount_cost as cos  from `tabQuotation` 
						left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
						where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Management' """ %(i.name),as_dict =1)
						if am:
							amount = am[0]["cos"]
							name = am[0]["n"]
				else:
					amt = frappe.db.sql(""" select `tabQuotation`.name as n,`tabQuotation Item`.net_amount as cost  from `tabQuotation` 
					left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
					where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Customer' """ %(i.name),as_dict =1)
					if amt:
						amount = amt[0]["cost"]
						name = amt[0]["n"]
					else:
						am = frappe.db.sql(""" select `tabQuotation`.name as n,`tabQuotation Item`.net_amount as cos  from `tabQuotation` 
						left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
						where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Management' """ %(i.name),as_dict =1)
						if am:
							amount = am[0]["cos"]
							name = am[0]["n"]


				total_amt = total_amt + amount

				
				input_date_string = str(i.posting_date)

				input_date = datetime.strptime(input_date_string, "%Y-%m-%d")

				formatted_date = input_date.strftime("%d-%m-%Y")
					

				data += '<tr>'
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sn)
					
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date)
				
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/work-order-data/%s"target="_blank">%s</a><center></td>'%(i.name,i.name)
					
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.sales_rep)

				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/quotation/%s"target="_blank">%s</a><center></td>'%(name,name)					

				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.customer)
					
			
				data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(amount)
		
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
	
	

	
