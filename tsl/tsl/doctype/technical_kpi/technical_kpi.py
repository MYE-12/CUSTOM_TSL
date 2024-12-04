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

class TechnicalKPI(Document):
	@frappe.whitelist()
	def get_data(self):
		data= ""
		data += '<div class="table-container">'
		# data += '<h3><b><center>WORK ORDER<center><b><h3>'
		data += '<table class="table table-bordered">'

		data += '<tr>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Status</b><center></td>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Output</b><center></td>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Percentage%</b><center></td>'

		data += '</tr>'

		ftfr =  frappe.db.count("Work Order Data",{"status_cap_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})
		# rs =  frappe.db.count("Work Order Data",{"status":"RS-Repaired and Shipped","posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})
		rs = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" 
		and company = "TSL COMPANY - Kuwait" and `tabWork Order Data`.posting_date between '%s' and '%s' """ %(self.from_date,self.to_date) ,as_dict=1)

		r = 0
		if rs:
			r = rs[0]["ct"]

		
		
		data += '<tr>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>FTFR</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(ftfr/r,2))
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(ftfr/r,2) * 100)

		data += '</tr>'

		# rnr =  frappe.db.count("Work Order Data",{"status":"RNR-Return Not Repaired","posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})
		rnr = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "RNR-Return Not Repaired" 
		and company = "TSL COMPANY - Kuwait" and `tabWork Order Data`.posting_date between '%s' and '%s' """ %(self.from_date,self.to_date) ,as_dict=1)

		rr = 0
		if rnr:
			rr = rnr[0]["ct"]
		wod =  frappe.db.count("Work Order Data",{"posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})

		data += '<tr>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>RNR</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(rr/wod,2))
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(rr/wod,2) * 100)

		data += '</tr>'

		# rnf =  frappe.db.count("Work Order Data",{"status":"RNF-Return No Fault","posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})
		
		rnf = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
		left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		where  `tabStatus Duration Details`.status = "RNF-Return No Fault" 
		and company = "TSL COMPANY - Kuwait" and `tabWork Order Data`.posting_date between '%s' and '%s' """ %(self.from_date,self.to_date) ,as_dict=1)

		rf = 0
		if rnf:
			rf = rnf[0]["ct"]
		
		data += '<tr>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>RNF</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(rf/wod,2))
		data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(rf/wod,2) * 100)

		data += '</tr>'

		data += '</table">'
		data += '</div>'




	

		t = ["sampath@tsl-me.com","maari@tsl-me.com","eduardo@tsl-me.com","aakib@tsl-me.com"]
	
		
		data += '<div class="table-container">'
			
		data += '<table class="table table-bordered">'

		data += '<tr>'
		data += '<td colspan = "5" style="border-color:#000000;padding:1px;font-size:14px;font-size:16px;background-color:#3333ff;color:white;"><center><b>For Technician</b><center></td>'
		data += '</tr>'
		data += '<tr>'

		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Status</b><center></td>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Sampath</b><center></td>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Maari</b><center></td>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Ed</b><center></td>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Aakib</b><center></td>'
		# data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Percentage%</b><center></td>'

		data += '</tr>'

		

		
		data += '<tr>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>FTFR</b><center></td>'
		total_ftfr = 0
		for i in t:
			
			ftfr =  frappe.db.count("Work Order Data",{"status_cap_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait","technician":i})
			# rs =  frappe.db.count("Work Order Data",{"status":"RS-Repaired and Shipped","posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})
			rs = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.technician = '%s'
			and company = "TSL COMPANY - Kuwait" and `tabWork Order Data`.posting_date between '%s' and '%s' """ %(i,self.from_date,self.to_date) ,as_dict=1)

			r = 0
			if rs:
				r = rs[0]["ct"]
			
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(ftfr/r,2))
			total_ftfr = total_ftfr + ftfr/r
		# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %("")
		# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(ftfr/r,2) * 100)
		data += '</tr>'

		

		data += '<tr>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>RNR</b><center></td>'
		total_rnr = 0
		for i in t:
			wod =  frappe.db.count("Work Order Data",{"posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait","technician":i})
			# rnr =  frappe.db.count("Work Order Data",{"status":"RNR-Return Not Repaired","posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})
			rnr = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RNR-Return Not Repaired" and `tabWork Order Data`.technician = '%s'
			and company = "TSL COMPANY - Kuwait" and `tabWork Order Data`.posting_date between '%s' and '%s' """ %(i,self.from_date,self.to_date) ,as_dict=1)
			rr = 0
			if rnr:
				rr = rnr[0]["ct"]
			
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(rr/wod,2))
			total_rnr = total_rnr + rr/wod
		# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %("")
		# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(rr/wod,2) * 100)
		data += '</tr>'

	
		# rnf =  frappe.db.count("Work Order Data",{"status":"RNF-Return No Fault","posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})
		

		data += '<tr>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>RNF</b><center></td>'
		total_rnf = 0
		for i in t:
			wod =  frappe.db.count("Work Order Data",{"posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait","technician":i})

			rnf = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RNF-Return No Fault" and `tabWork Order Data`.technician = '%s'
			and company = "TSL COMPANY - Kuwait" and `tabWork Order Data`.posting_date between '%s' and '%s' """ %(i,self.from_date,self.to_date) ,as_dict=1)

			rf = 0
			if rnf:
				rf = rnf[0]["ct"]
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(rf/wod,2))
			total_rnf = total_rnf + rf/wod
		# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(round(rf/wod,2) * 100)
		


		data += '</tr>'

		data += '<tr>'
		data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Percentage %</b><center></td>'
		
		total_per = 0
		for i in t:
			# frappe.errprint(i)
			ftfr =  frappe.db.count("Work Order Data",{"status_cap_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait","technician":i})
			# rs =  frappe.db.count("Work Order Data",{"status":"RS-Repaired and Shipped","posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})
			rs = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.technician = '%s'
			and company = "TSL COMPANY - Kuwait" and `tabWork Order Data`.posting_date between '%s' and '%s' """ %(i,self.from_date,self.to_date) ,as_dict=1)

			r = 0
			if rs:
				r = rs[0]["ct"]
			t_ftr = ftfr/r
			
			

			wod =  frappe.db.count("Work Order Data",{"posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait","technician":i})
			# rnr =  frappe.db.count("Work Order Data",{"status":"RNR-Return Not Repaired","posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait"})
			rnr = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RNR-Return Not Repaired" and `tabWork Order Data`.technician = '%s'
			and company = "TSL COMPANY - Kuwait" and `tabWork Order Data`.posting_date between '%s' and '%s' """ %(i,self.from_date,self.to_date) ,as_dict=1)
			rr = 0
			if rnr:
				rr = rnr[0]["ct"]
			
		
			t_rnr =  rr/wod
			


			wod =  frappe.db.count("Work Order Data",{"posting_date": ["between", [self.from_date, self.to_date]],"company":"TSL COMPANY - Kuwait","technician":i})

			rnf = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			where  `tabStatus Duration Details`.status = "RNF-Return No Fault" and `tabWork Order Data`.technician = '%s'
			and company = "TSL COMPANY - Kuwait" and `tabWork Order Data`.posting_date between '%s' and '%s' """ %(i,self.from_date,self.to_date) ,as_dict=1)

			rf = 0
			if rnf:
				rf = rnf[0]["ct"]
			
			t_rnf = rf/wod
			
			total_per = total_per + t_ftr + t_rnr + t_rnf
			# frappe.errprint(total_per)
			data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s%s</b><center></td>' %(round(total_per,2),"%")
			total_per = 0


		# data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %("total")
		
		# data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'
		# data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'
		# data += '<td style="width:15%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'



		data += '</tr>'

		

		data += '</table">'
		data += '</div>'
	
		return data
