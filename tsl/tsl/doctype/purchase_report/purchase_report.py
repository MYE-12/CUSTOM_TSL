# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date
from frappe.utils import (
    add_days,
    add_months,
    cint,
)

class PurchaseReport(Document):
	@frappe.whitelist()
	def get_data(self):
		data= ""
		data += '<div class="table-container">'
		# data += '<h3><b><center>WORK ORDER<center><b><h3>'
		data += '<table class="table table-bordered">'
		data += '<tr>'
		data += '<td colspan = 1 style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="150"></td>'
		data += '<td colspan = 2 style="border-color:#000000;color:#055c9d;"><h2><center><b>TSL Company</b></center></h2></td>'
		if self.company == "TSL COMPANY - Kuwait":  
			data += '<td colspan = 1 style="border-color:#000000;"><center><img src = "/files/kuwait flag.jpg" width ="100"></center></td>'
		if self.company == "TSL COMPANY - UAE":  
			data += '<td colspan = 1 style="border-color:#000000;"><center><img src = "/files/Flag_of_the_United_Arab_Emirates.svg.jpg" width ="100"></center></td>'
		data += '<tr>'
		data += '<td colspan = 4 style="border-color:#000000;padding:1px;font-size:20px;background-color:#00BFFF;color:white;"><center><b>WORK ORDER</b><center></td>'
		data += '</tr>'

		day = add_days(self.date,-1)
		
		# rnp = frappe.db.count("Work Order Data",{"status":"RNP-Return No Parts","posting_date": ["between", ["2015-07-23", self.date]]})

		rnp = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "RNP-Return No Parts" and `tabWork Order Data`.company = '%s'
		and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(self.company,self.date) ,as_dict=1)
		
		# ordered =  frappe.db.count("Work Order Data",{"status":"WP-Waiting Parts","posting_date": ["between", [self.date,self.date]]})
		ordered = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as wp from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "WP-Waiting Parts" and `tabWork Order Data`.company = '%s'
		and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(self.company,self.date) ,as_dict=1)
		
		# ordered = frappe.db.count("Work Order Data",{"status":"Q-Quoted","posting_date": ["between", [self.date, self.date]]})
		quot = frappe.db.count("Work Order Data",{"status":"Parts Priced","posting_date": ["between", [self.date, self.date]]})
		rec =  frappe.db.count("Work Order Data",{"status":"TR-Technician Repair","posting_date": ["between", [self.date, self.date]]})
		# app =  frappe.db.count("Work Order Data",{"status":"A-Approved","posting_date": ["between", ["2015-07-23", self.date]]})

		not_qt =  frappe.db.count("Work Order Data",{"company":self.company,"old_wo_no":["is","not set"],"status":"SP-Searching Parts","posting_date": ["between", ["2015-07-23", self.date]]})

		wp =  frappe.db.count("Work Order Data",{"company":self.company,"status":"WP-Waiting Parts","posting_date": ["between", ["2015-07-23", self.date]]})
		np =  frappe.db.count("Work Order Data",{"company":self.company,"status":"RNP-Return No Parts","posting_date": ["between", [self.date, self.date]]})


		s_quoted = frappe.db.count("Supply Order Data",{"status":"Quoted","posting_date": ["between", [self.date, self.date]]})
		s_ordered = frappe.db.count("Supply Order Data",{"status":"Ordered","posting_date": ["between", [self.date, self.date]]})
		# s_received = frappe.db.count("Supply Order Data",{"status":"Received","posting_date": ["between", [self.date, self.date]]})
		s_approved = frappe.db.count("Supply Order Data",{"status":"Approved","posting_date": ["between", [self.date, self.date]]})
		s_not_quoted = frappe.db.count("Supply Order Data",{"department":"Supply - TSL","docstatus":1,"company":self.company,"status":"Inquiry","posting_date": ["between", ["2015-07-23", self.date]]})

		s_not_found = frappe.db.count("Supply Order Data",{"department":"Supply - TSL","company":self.company,"status":"Not Found","posting_date": ["between", ["2015-07-23", self.date]]})

		waiting_so = frappe.db.count("Supply Order Data",{"department":"Supply - TSL","company":self.company,"status":"ordered","posting_date": ["between", ["2015-07-23", day]]})


		po = frappe.db.sql(""" select count(`tabPurchase Order Item`.work_order_data) as p from `tabPurchase Order`
			left join `tabPurchase Order Item` on `tabPurchase Order Item`.parent = `tabPurchase Order`.name
			where `tabPurchase Order`.transaction_date = '%s' and `tabPurchase Order`.docstatus != 2 and `tabPurchase Order`.per_received = %s and  `tabPurchase Order`.company = '%s' """ %("2024-09-14",0,self.company),as_dict =1)

		prw = frappe.db.sql(""" select count(`tabPurchase Receipt Item`.work_order_data) as pr from `tabPurchase Receipt`
			left join `tabPurchase Receipt Item` on `tabPurchase Receipt Item`.parent = `tabPurchase Receipt`.name
			where `tabPurchase Receipt`.posting_date = '%s' and `tabPurchase Receipt`.docstatus != 2  and `tabPurchase Receipt`.company = '%s' """ %(self.date,self.company),as_dict =1)

		# qc = frappe.db.sql(""" select count(`tabQuotation Item`.wod_no) as q from `tabQuotation`
		# 	left join `tabQuotation Item` on `tabQuotation Item`.parent = `tabQuotation`.name
		# 	where `tabQuotation`.transaction_date = '%s' and `tabQuotation`.workflow_state = "Approved By Customer" and  `tabQuotation`.company = "TSL COMPANY - Kuwait" """ %(self.date),as_dict =1)

		qc = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as q from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabWork Order Data`.status = "A-Approved" and `tabWork Order Data`.company = '%s'
		and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(self.company,self.date) ,as_dict=1)
			
		pre_eval =  frappe.get_all("Work Order Data",{"status":"A-Approved","company":self.company,"old_wo_no":["is","not set"],"posting_date": ["between", ["2015-07-23", self.date]]})

		pre_wod_count = 0
		for i in pre_eval:
			
			eval_rep = frappe.db.exists("Evaluation Report",{"work_order_data":i.name})
			if not eval_rep:
				pre_q = frappe.db.sql(""" select `tabQuotation`.name from `tabQuotation`
				left join `tabQuotation Item` on `tabQuotation Item`.parent = `tabQuotation`.name
				where `tabQuotation`.workflow_state = "Approved By Customer" and `tabQuotation Item`.wod_no = "%s" """ %(i.name),as_dict =1)
				if pre_q:
					pre_wod_count = pre_wod_count + 1
		


		pwod = 0
		if po:	
			pwod = po[0]["p"]

		prwod = 0
		if prw:	
			prwod = prw[0]["pr"]
		

		qcw = 0
		if qc:	
			qcw = qc[0]["q"]
		
		sq = frappe.db.count("Supplier Quotation",{"transaction_date":self.date,"work_order_data": ["is", "set"],"company":self.company})
		
		

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:16px;background-color:#00BFFF;color:white;"><center><b>Achievments</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:16px;background-color:#00BFFF;color:white;"><center><b>Status</b><center></td>'
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#004792;color:white;width:25%;"><center><b>Current Status</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#004792;color:white;width:25%;"><center><b>Count</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#004792;color:white;width:25%;"><center><b>Status</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#004792;color:white;width:25%;"><center><b>Count</b><center></td>'

		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Not Found</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(rnp[0]["ct"])
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Approved</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(qcw)

		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Ordered</b><center></td>' 
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>'%(ordered[0]["wp"] or 0)
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Pre-Approved</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(pre_wod_count)

		
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Quoted</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(sq)
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Not Quoted</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(not_qt)

		
		data += '</tr>'

		prwod = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "TR-Technician Repair" and `tabWork Order Data`.company = '%s'
		and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(self.company,self.date) ,as_dict=1)
			

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Received</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(prwod[0]["ct"] or 0)
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Waiting PS</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(wp)

		data += '</tr>'
		data += '</table>'




		# data += '<h3><b><center>SUPPLY ORDER<center><b><h3>'
		data += '<table class="table table-bordered">'
		data += '<tr>'
		data += '<td colspan = 4 style="border-color:#000000;padding:1px;font-size:20px;background-color:#00BFFF;color:white;"><center><b>SUPPLY ORDER</b><center></td>'
		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:16px;background-color:#00BFFF;color:white;"><center><b>Achievments</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:16px;background-color:#00BFFF;color:white;"><center><b>Status</b><center></td>'
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#004792;color:white;width:25%;"><center><b>Current Status</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#004792;color:white;width:25%;"><center><b>Count</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#004792;color:white;width:25%;"><center><b>Status</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#004792;color:white;width:25%;"><center><b>Count</b><center></td>'

		data += '</tr>'


		spo = frappe.db.sql(""" select count(`tabPurchase Order Item`.supply_order_data) as p from `tabPurchase Order`
			left join `tabPurchase Order Item` on `tabPurchase Order Item`.parent = `tabPurchase Order`.name
			where `tabPurchase Order`.transaction_date = '%s' and `tabPurchase Order`.docstatus != 2 and `tabPurchase Order`.per_received = %s
			and `tabPurchase Order`.company = '%s' and `tabPurchase Order`.cost_center != 'Supply Tender - TSL' """ %(self.date,0,self.company),as_dict =1)

		frappe.errprint(spo)
		spwod = 0
		if spo:	
			spwod = spo[0]["p"]
		
		# sqs = frappe.db.count("Supplier Quotation",{"transaction_date":self.date,"supply_order_data": ["is", "set"],"company":"TSL COMPANY - Kuwait"})

		sqs = frappe.db.sql(""" select count(DISTINCT `tabSupply Order Data`.name) as ct from `tabSupply Order Data` 
		left join `tabStatus Duration Details` on `tabSupply Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "Parts Priced" and `tabSupply Order Data`.company = '%s'
		and `tabStatus Duration Details`.date  LIKE "%s%%" and `tabSupply Order Data`.department != 'Supply Tender - TSL' """ %(self.company,self.date) ,as_dict=1)
		

		# sqc = frappe.db.sql(""" select count(`tabQuotation Item`.supply_order_data) as qs from `tabQuotation`
		# 	left join `tabQuotation Item` on `tabQuotation Item`.parent = `tabQuotation`.name
		# 	where `tabQuotation`.transaction_date = '%s' and `tabQuotation`.workflow_state = "Approved By Customer" and  `tabQuotation`.company = "TSL COMPANY - Kuwait" """ %(self.date),as_dict =1)

		# sqcount = 0
		# if sqc:	
		# 	sqcount = sqc[0]["qs"]

		sqc = frappe.db.sql(""" select count(DISTINCT `tabSupply Order Data`.name) as ct from `tabSupply Order Data` 
		left join `tabStatus Duration Details` on `tabSupply Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabSupply Order Data`.status = "Approved" and `tabSupply Order Data`.company = '%s' and `tabSupply Order Data`.department != 'Supply Tender - TSL'
		 """ %(self.company) ,as_dict=1)
		

		s_not_found = frappe.db.sql(""" select count(DISTINCT `tabSupply Order Data`.name) as ct from `tabSupply Order Data` 
		left join `tabStatus Duration Details` on `tabSupply Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "Not Found" and `tabSupply Order Data`.company = '%s' and `tabSupply Order Data`.department != 'Supply Tender - TSL'
		and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(self.company,self.date) ,as_dict=1)
		

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Not Found</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(s_not_found[0]["ct"] or 0)
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Approved</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(sqc[0]["ct"])

		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#A7C7E7;"><center><b>Ordered</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(spwod)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#A7C7E7;"><center><b>Not Quoted</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>'  %(s_not_quoted)

		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#A7C7E7;"><center><b>Quoted</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(sqs[0]["ct"] or 0)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#A7C7E7;"><center><b>Waiting SO</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(waiting_so)

		data += '</tr>'

		s_received = frappe.db.sql(""" select count(DISTINCT `tabSupply Order Data`.name) as ct from `tabSupply Order Data` 
		left join `tabStatus Duration Details` on `tabSupply Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "Received" and `tabSupply Order Data`.company = '%s' and `tabSupply Order Data`.department != 'Supply Tender - TSL'
		and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(self.company,self.date) ,as_dict=1)
		

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b>Received</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b>%s</b><center></td>' %(s_received[0]["ct"] or 0)
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;"><center><b></b><center></td>'

		data += '</tr>'
		
		data += '</table>'


	
		data += '</div>'
		return data
