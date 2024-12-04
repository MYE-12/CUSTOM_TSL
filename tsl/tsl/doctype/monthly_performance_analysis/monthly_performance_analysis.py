# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document

class MonthlyPerformanceAnalysis(Document):

	@frappe.whitelist()
	def get_work_orders(self):
		data = ""
		data += '<table class="table table-bordered">'

		data += '<tr>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>WO Parts</b><center></td>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Ave Days</b><center></td>'
		data += '</tr>'

		wd = frappe.get_all("Work Order Data",{"posting_date": ["between", ("2024-04-01","2024-05-07")]},["name"])
		total = 0
		t_days = 0
		for i in wd:
			rfq = frappe.get_value("Request for Quotation",{"work_order_data":i.name},["transaction_date"])

			q = frappe.db.sql(""" select `tabQuotation`.transaction_date  from `tabQuotation` left join 
				`tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
				where  `tabQuotation Item`.wod_no = '%s' """ %(i.name) ,as_dict=1)
			if q and rfq:
				total = total + 1
				date1 = datetime.strptime(str(q[0]["transaction_date"]),"%Y-%m-%d").date()
				
				date2 = datetime.strptime(str(rfq), "%Y-%m-%d").date()
				
				difference = date1 - date2

				days_between = difference.days
				t_days = t_days + days_between
		# frappe.errprint(t_days)		
		# frappe.errprint(total)
		data += '<tr>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b>From Req to Quote Date</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>'  %(t_days/total)
		data += '</tr>'
		
		total2 = 0
		t2_days = 0
		for i in wd:
			qu = frappe.db.sql(""" select `tabQuotation`.approval_date  from `tabQuotation` left join 
			`tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
			where `tabQuotation`.workflow_state = "Approved By Customer" and `tabQuotation Item`.wod_no = '%s' and   `tabQuotation`.quotation_type = "Customer Quotation - Repair" """ %(i.name) ,as_dict=1)
			
			pr = frappe.db.sql(""" select `tabPurchase Receipt`.posting_date  from `tabPurchase Receipt` left join 
			`tabPurchase Receipt Item` on `tabPurchase Receipt`.name = `tabPurchase Receipt Item`.parent
			where `tabPurchase Receipt Item`.work_order_data = '%s' """ %(i.name) ,as_dict=1)
			
			if qu and pr:
			
				total2 = total2 + 1
				date1 = datetime.strptime(str(pr[0]["posting_date"]),"%Y-%m-%d").date()
				# frappe.errprint(qu[0]["approval_date"])

				date2 = datetime.strptime(str(qu[0]["approval_date"]),"%Y-%m-%d").date()
				difference = date1 - date2

				days_between = difference.days
				t2_days = t2_days + days_between
		# frappe.errprint(t2_days)		
		# frappe.errprint(total2)

		data += '<tr>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b>From Approval to Receive Date</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(t2_days/total2)

		data += '</tr>'
		
		data += '<tr>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b>Quoted %</b><center></td>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b>Not Found %</b><center></td>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b>Quoted Only</b><center></td>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b>Ordered</b><center></td>'
		data += '<td style="border-color:#000000;width:50%;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'
		data += '</tr>'
		

		data += '</table>'
		return data

