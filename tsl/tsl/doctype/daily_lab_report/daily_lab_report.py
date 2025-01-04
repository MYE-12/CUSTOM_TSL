# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import (
	add_days,
	add_months,
	cint,
	date_diff,
	flt,
	get_first_day,
	get_last_day,
	get_link_to_form,
	getdate,
	rounded,
	today,
)

class DailyLabReport(Document):
	@frappe.whitelist()
	def work_orders(self):
		if self.company == "TSL COMPANY - Kuwait":
			d = datetime.now().date()
			ogdate = datetime.strptime(str(d),"%Y-%m-%d")
			ogdate_2 = datetime.strptime(str(self.date),"%Y-%m-%d")

			# Format the date as a string in the desired format
			formatted_date = ogdate.strftime("%d-%m-%Y")
			formatted_date_2 = ogdate_2.strftime("%d-%m-%Y")
			
			# date = d.strftime("%Y-%m-%d")
			# original_date = datetime.strptime(str(d), "%Y-%m-%d")
			original_date = self.date


			# Format datetime object to new date string format
			# date = datetime.strptime(str(original_date), "%Y-%m-%d")

			data = ""
			data += '<table class="table table-bordered">'
			data += '<tr>'
			data += '<td colspan = "7" align = "center" style="border-color:#000000;padding:1px;font-size:20px;background-color:#808080;color:white;"><b>Date :%s</b></td>' %(formatted_date_2)
			data += '</tr>'
			data += '<tr>'
			data += '<td colspan = 2 style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="150"></td>'
			data += '<td colspan = 3 style="border-color:#000000;"><h2><center><b>TSL Company</b></center></h2></td>'
			data += '<td colspan = 2 style="border-color:#000000;"><center><img src = "/files/kuwait flag.jpg" width ="100"></center></td>'
			
			data += '</tr>'
			data += '<tr>'
			# data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;"><center><b></b><center></td>'
			data += '<td colspan = "2" style="border-color:#000000;padding:1px;font-size:18px;font-size:16px;background-color:#3333ff;color:white;"><center><b>Status</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:18px;font-size:16px;background-color:#FFA500;color:white;"><center><b>Sampat</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:18px;font-size:16px;background-color:#FFC000;color:white;"><center><b>Mari</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:18px;font-size:16px;background-color:#008000;color:white;"><center><b>ED</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:18px;font-size:16px;background-color:#0047AB;color:white;"><center><b>Aakib</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:18px;font-size:16px;background-color:#4682B4;color:white;"><center><b>Total</b><center></td>'
			data += '</tr>'

			tech = ["sampath@tsl-me.com","maari@tsl-me.com","eduardo@tsl-me.com","aakib@tsl-me.com"]
			total_ne_s = 0
			total_ne_m = 0
			total_ne_e = 0
			total_ne_a = 0

			lp_total_ne_s = 0
			lp_total_ne_m = 0
			lp_total_ne_e = 0
			lp_total_ne_a = 0

			total_ner_s = 0
			total_ner_m = 0
			total_ner_e = 0
			total_ner_a = 0

			ue_s = 0
			ue_m = 0
			ue_e = 0
			ue_a = 0

			utr_s = 0
			utr_m = 0
			utr_e = 0
			utr_a = 0

			rs_s = 0
			rs_m = 0
			rs_e = 0
			rs_a = 0

			w_s = 0
			w_m = 0
			w_e = 0
			w_a = 0

			rnr_s = 0
			rnr_m = 0
			rnr_e = 0
			rnr_a = 0

			rnf_s = 0
			rnf_m = 0
			rnf_e = 0
			rnf_a = 0

			com_s = 0
			com_m = 0
			com_e = 0
			com_a = 0

			# for t in tech:
			# 	ne = frappe.get_all("Work Order Data",{"technician":t},["*"])
			# 	for i in ne:
			# 		ev = frappe.db.exists("Evaluation Report",{"work_order_data":i.name,"date":original_date,"technician":t})
			# 		if ev:
			# 			# techni = frappe.get_value("Evaluation Report",{"name":ev},["technician"])
			# 			if t == "sampath@tsl-me.com":
			# 				total_ne_s = total_ne_s + 1
			# 			if t == "maari@tsl-me.com":
			# 				total_ne_m = total_ne_m + 1
			# 			if t == "eduardo@tsl-me.com":
			# 				total_ne_e = total_ne_e + 1
			# 			if t == "aakib@tsl-me.com":
			# 				total_ne_a = total_ne_a + 1
						
			
				# ne = frappe.get_all("Work Order Data",{"posting_date":original_date,"technician":t},["*"])
				# for i in ne:
				# 	sd = frappe.get_doc("Work Order Data",i.name)
				# 	for j in sd.status_duration_details:
				# 		timestamp = str(j.date) 
				# 		date_portion = timestamp[:10]
				# 		j.date= date_portion
				# 		if "NE-Need Evaluation"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) :
				# 			total_ne_s = total_ne_s + 1
				# 		if "NE-Need Evaluation"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date):
				# 			total_ne_m = total_ne_m + 1
				# 		if "NE-Need Evaluation"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
				# 			total_ne_e = total_ne_e + 1
				# 		if "NE-Need Evaluation"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
				# 			total_ne_a = total_ne_a + 1
						
				# 		if "NER-Need Evaluation Return"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
				# 			total_ner_s = total_ner_s + 1
				# 		if "NER-Need Evaluation Return"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
				# 			total_ner_m = total_ner_m + 1
				# 		if "NER-Need Evaluation Return"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
				# 			total_ner_e = total_ner_e + 1
				# 		if "NER-Need Evaluation Return"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
				# 			total_ner_a = total_ner_a + 1
						
						
			
			# total_ne_s = frappe.db.count("Work Order Data",{"technician":"sampath@tsl-me.com","status":"NE-Need Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			# total_ne_m = frappe.db.count("Work Order Data",{"technician":"maari@tsl-me.com","status":"NE-Need Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			# total_ne_e = frappe.db.count("Work Order Data",{"technician":"eduardo@tsl-me.com","status":"NE-Need Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			# total_ne_a = frappe.db.count("Work Order Data",{"technician":"aakib@tsl-me.com","status":"NE-Need Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			
			for t in tech:
				emp = frappe.get_value("Employee",{"user_id":t})
				if emp:
					lp = frappe.db.sql(
						"""
						SELECT employee
						FROM `tabLeave Application Form` 
						WHERE employee = %s
						AND %s BETWEEN from_date AND to_date and docstatus = 1
						""",
						(emp,self.date),
						as_dict=True
					)
					if lp:
						if t == "sampath@tsl-me.com":
							lp_total_ne_s = "L"
						if t == "maari@tsl-me.com":
							lp_total_ne_m = "L"
						if t == "eduardo@tsl-me.com":
							lp_total_ne_e = "L"
						if t == "aakib@tsl-me.com":
							lp_total_ne_a = "L"
				
				ne = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
						left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
						where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
						and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date),as_dict=1)
					
				if t == "sampath@tsl-me.com":
					total_ne_s = ne[0]["ct"]
				if t == "maari@tsl-me.com":
					total_ne_m = ne[0]["ct"]
				if t == "eduardo@tsl-me.com":
					total_ne_e = ne[0]["ct"]
				if t == "aakib@tsl-me.com":
					total_ne_a = ne[0]["ct"]

			total_ner_s = frappe.db.count("Work Order Data",{"technician":"sampath@tsl-me.com","status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			total_ner_m = frappe.db.count("Work Order Data",{"technician":"maari@tsl-me.com","status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			total_ner_e = frappe.db.count("Work Order Data",{"technician":"eduardo@tsl-me.com","status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			total_ner_a = frappe.db.count("Work Order Data",{"technician":"aakib@tsl-me.com","status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			
			
			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>UE</b><center></td>'
			
			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				total_ne_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ne_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				total_ne_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ne_m or 0)
			
			if lp_total_ne_e == "L":
				total_ne_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ne_e or 0)
			
			if lp_total_ne_a == "L":
				total_ne_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(total_ne_a or 0)

			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ne_s + total_ne_m + total_ne_e + total_ne_a)
			
			data += '</tr>'

			
			

			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>Started Work</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>NER</b><center></td>'

			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				total_ner_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ner_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				total_ner_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ner_m or 0)
			
			if lp_total_ne_e == "L":
				total_ner_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ner_e or 0)
			
			if lp_total_ne_a == "L":
				total_ner_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(total_ner_a or 0)




			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ner_s + total_ner_m + total_ner_e + total_ner_a)
			data += '</tr>'

			data += '<tr>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>Total</b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ne_s + total_ner_s)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ne_m + total_ner_m)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ne_e + total_ner_e)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ne_a + total_ner_a)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %((total_ne_s + total_ne_m + total_ne_e + total_ne_a)+(total_ner_s + total_ner_m + total_ner_e + total_ner_a))
			data += '</tr>'


			data += '</table>'



			data += '<table class="table table-bordered">'
			
			data += '<tr>'
			data += '<td colspan = "2" style="border-left:hidden;border-top:hidden;border-color:#000000;padding:1px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '</tr>'

			total_ue_s = frappe.db.count("Work Order Data",{"technician":"sampath@tsl-me.com","status":"UE-Under Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			total_ue_m = frappe.db.count("Work Order Data",{"technician":"maari@tsl-me.com","status":"UE-Under Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			total_ue_e = frappe.db.count("Work Order Data",{"technician":"eduardo@tsl-me.com","status":"UE-Under Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			total_ue_a = frappe.db.count("Work Order Data",{"technician":"aakib@tsl-me.com","status":"UE-Under Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			
			total_utr_s = frappe.db.count("Work Order Data",{"technician":"sampath@tsl-me.com","status":"UTR-Under Technician Repair","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			total_utr_m = frappe.db.count("Work Order Data",{"technician":"maari@tsl-me.com","status":"UTR-Under Technician Repair","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			total_utr_e = frappe.db.count("Work Order Data",{"technician":"eduardo@tsl-me.com","status":"UTR-Under Technician Repair","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
			total_utr_a = frappe.db.count("Work Order Data",{"technician":"aakib@tsl-me.com","status":"UTR-Under Technician Repair","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})

			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>UE</b><center></td>' 
			
			for t in technician:
				
				ue = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
					left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
					where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
					and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t.user_id,original_date) ,as_dict=1)
				
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ue[0]["ct"] or 0)


			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>End of the Work</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>UTR</b><center></td>'
			
			for t in technician:

				utr = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
					left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
					where  `tabStatus Duration Details`.status = "UTR-Under Technician Repair"
					and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t.user_id,original_date),as_dict=1)
				
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(utr[0]["ct"] or 0)

				

			
			
			
			
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ue_s + total_ue_m + total_ue_e + total_ue_a)
			data += '</tr>'

			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>End of the Work</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>UTR</b><center></td>'
			
			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				total_utr_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_utr_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				total_utr_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_utr_m or 0)
			
			if lp_total_ne_e == "L":
				total_utr_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_utr_e or 0)
			
			if lp_total_ne_a == "L":
				total_utr_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(total_utr_a or 0)


			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_utr_s +total_utr_m + total_utr_e + total_utr_a)
			data += '</tr>'

			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>Site Visit</b><center></td>'
			
			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				total_utr_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(0 or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				total_utr_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(0 or 0)
			
			if lp_total_ne_e == "L":
				total_utr_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(0 or 0)
			
			if lp_total_ne_a == "L":
				total_utr_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(0 or 0)

				
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;"><center><b>0	</b><center></td>'
			
			data += '</tr>'

			data += '<tr>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>Total</b><center></td>'
			

			data += '<td style="border-color:#000000;;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ue_s + total_utr_s)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ue_m + total_utr_m)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ue_e + total_utr_e)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ue_a + total_utr_a)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %((total_ue_s + total_ue_m + total_ue_e + total_ue_a)+(total_utr_s +  total_utr_m + total_utr_e + total_utr_a))
			data += '</tr>'

			data += '</table>'

			data += '<table class="table table-bordered">'
			
			data += '<tr>'
			data += '<td colspan = "2" style="border-left:hidden;border-top:hidden;border-color:#000000;padding:1px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '</tr>'

			for t in tech:
				s = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
					left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
					where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped"
					and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
				
				if t == "sampath@tsl-me.com":
					rs_s = s[0]["ct"]
				if t == "maari@tsl-me.com":
					rs_m = s[0]["ct"]
				if t == "eduardo@tsl-me.com":
					rs_e = s[0]["ct"]
				if t == "aakib@tsl-me.com":
					rs_a = s[0]["ct"]

				w = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
					left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
					where  `tabStatus Duration Details`.status = "W-Working" 
					and `tabWork Order Data`.technician = "%s" 
					and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
				
				r = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
					left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
					where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" 
					and `tabWork Order Data`.technician = "%s" 
					and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
				
				# if t == "sampath@tsl-me.com":
				# 	# if not r:
				# 	w_s = w[0]["ct"]
				# if t == "maari@tsl-me.com":
				# 	# if not r:
				# 	w_m = w[0]["ct"]
				# if t == "eduardo@tsl-me.com":
				# 	# if not r:
				# 	w_e = w[0]["ct"]
				# if t == "aakib@tsl-me.com":
				# 	# if not r:
				# 	w_a = w[0]["ct"]

				rnr = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
					left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
					where  `tabStatus Duration Details`.status = "RNR-Return Not Repaired"
							and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
				
				if t == "sampath@tsl-me.com":
					rnr_s = rnr[0]["ct"]
				if t == "maari@tsl-me.com":
					rnr_m = rnr[0]["ct"]
				if t == "eduardo@tsl-me.com":
					rnr_e = rnr[0]["ct"]
				if t == "aakib@tsl-me.com":
					rnr_a = rnr[0]["ct"]

				rnf = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
					left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
					where  `tabStatus Duration Details`.status = "RNF-Return No Fault"
					and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
				
				if t == "sampath@tsl-me.com":
					rnf_s = rnf[0]["ct"]
				if t == "maari@tsl-me.com":
					rnf_m = rnf[0]["ct"]
				if t == "eduardo@tsl-me.com":
					rnf_e = rnf[0]["ct"]
				if t == "aakib@tsl-me.com":
					rnf_a = rnf[0]["ct"]

				com = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
					left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
					where  `tabStatus Duration Details`.status = "C-Comparison"
							and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
				
				if t == "sampath@tsl-me.com":
					com_s = com[0]["ct"]
				if t == "maari@tsl-me.com":
					com_m = com[0]["ct"]
				if t == "eduardo@tsl-me.com":
					com_e = com[0]["ct"]
				if t == "aakib@tsl-me.com":
					com_a = com[0]["ct"]


				# ne = frappe.get_all("Work Order Data",{"technician":t},["*"])
				# for i in ne:
				# 	sd = frappe.get_doc("Work Order Data",i.name)
				# 	for j in sd.status_duration_details:
					
				# 		timestamp = str(j.date) 
				# 		date_portion = timestamp[:10]
						
				# 		j.date= date_portion
						
				# 		if "RS-Repaired and Shipped"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
				# 			rs_s = rs_s + 1
				# 		if "RS-Repaired and Shipped"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
				# 			rs_m = rs_m + 1
				# 		if "RS-Repaired and Shipped"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
				# 			rs_e = rs_e + 1
				# 		if "RS-Repaired and Shipped"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
				# 			rs_a = rs_a + 1

				# 		s = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
				# 			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				# 			where  `tabStatus Duration Details`.status = "W-Working" 
				# 			and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date LIKE "%s" """ %("sampath@tsl-me.com",original_date) ,as_dict=1)
				# 		
				# 		if "W-Working"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
				# 			w_s = w_s + 1
							
				# 		if "W-Working"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
				# 			w_m = w_m + 1
							
				# 		if "W-Working"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
				# 			w_e = w_e + 1
				# 		if "W-Working"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
				# 			w_a = w_a + 1

				# 		if "RNR-Return Not Repaired"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
				# 			rnr_s = rnr_s + 1
				# 		if "RNR-Return Not Repaired"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
				# 			rnr_m = rnr_m + 1
				# 		if "RNR-Return Not Repaired"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
				# 			rnr_e = rnr_e + 1
				# 		if "RNR-Return Not Repaired"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
				# 			rnr_a = rnr_a + 1
						
				# 		if "RNF-Return No Fault"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
				# 			rnf_s = rnf_s + 1
				# 		if "RNF-Return No Fault"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
				# 			rnf_m = rnf_m + 1
				# 		if "RNF-Return No Fault"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
				# 			rnf_e = rnf_e + 1
				# 		if "RNF-Return No Fault"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
				# 			rnf_a = rnf_a + 1

				# 		if "C-Comparison"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
				# 			com_s = com_s + 1
				# 		if "C-Comparison"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
				# 			com_m = com_m + 1
				# 		if "C-Comparison"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
				# 			com_e = com_e + 1
				# 		if "C-Comparison"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
				# 			com_a = com_a + 1
						
						
						
			
			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>RS</b><center></td>'
			
			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				rs_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rs_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				rs_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rs_m or 0)
			
			if lp_total_ne_e == "L":
				rs_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rs_e or 0)
			
			if lp_total_ne_a == "L":
				rs_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(rs_a or 0)

				
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rs_s + rs_m + rs_e + rs_a)
			data += '</tr>'

			ev_s = 0
			ev_m = 0
			ev_e = 0
			ev_a = 0

			# for t in tech:
			# 	ne = frappe.get_all("Work Order Data",{"date":original_date,"technician":t},["*"])
			# 	for i in ne:
			# 		ev = frappe.db.exists("Evaluation Report",{"work_order_data":i.name})
			# 		if ev:
			# 			techni = frappe.get_value("Evaluation Report",{"name":ev},["technician"])
			# 			if techni == "sampath@tsl-me.com":
			# 				ev_s = ev_s + 1
			# 			if techni == "maari@tsl-me.com":
			# 				ev_m = ev_m + 1
			# 			if techni == "eduardo@tsl-me.com":
			# 				ev_e = ev_e + 1
			# 			if techni == "aakib@tsl-me.com":
			# 				ev_a = ev_a + 1
			ev_s = frappe.db.count("Evaluation Report",{"date":original_date,"technician":"sampath@tsl-me.com"})
			ev_m = frappe.db.count("Evaluation Report",{"date":original_date,"technician":"maari@tsl-me.com"})
			ev_e = frappe.db.count("Evaluation Report",{"date":original_date,"technician":"eduardo@tsl-me.com"})
			ev_a = frappe.db.count("Evaluation Report",{"date":original_date,"technician":"aakib@tsl-me.com"})
						
			

			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b>PS</b><center></td>'
			
			
			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				ev_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ev_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				ev_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ev_m or 0)
			
			if lp_total_ne_e == "L":
				ev_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ev_e or 0)
			
			if lp_total_ne_a == "L":
				ev_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(ev_a or 0)

			
			
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ev_s + ev_m + ev_e + ev_a)
			data += '</tr>'

			
			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>W</b><center></td>'
			
			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				w_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(w_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				w_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(w_m or 0)
			
			if lp_total_ne_e == "L":
				w_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(w_e or 0)
			
			if lp_total_ne_a == "L":
				w_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(w_a or 0)

		
			
			
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(w_s + w_m + w_e + w_a)
			data += '</tr>'

			
			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b>Out - Flow</b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>RNR</b><center></td>'


			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				rnr_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnr_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				rnr_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnr_m or 0)
		
			if lp_total_ne_e == "L":
				rnr_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnr_e or 0)
			
			if lp_total_ne_a == "L":
				rnr_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(rnr_a or 0)

		
		

			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnr_s + rnr_m + rnr_e + rnr_a)
			data += '</tr>'

			# rnf_s = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"sampath@tsl-me.com","status":"RNF-Return No Fault"})
			# rnf_m = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"maari@tsl-me.com","status":"RNF-Return No Fault"})
			# rnf_e = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"eduardo@tsl-me.com","status":"RNF-Return No Fault"})
			# rnf_a = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"aakib@tsl-me.com","status":"RNF-Return No Fault"})


			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>RNF</b><center></td>'

			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				rnf_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnf_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				rnf_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnf_m or 0)
		
			if lp_total_ne_e == "L":
				rnf_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnf_e or 0)
			
			if lp_total_ne_a == "L":
				rnf_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(rnf_a or 0)



			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnf_a + rnf_s + rnf_e + rnf_m) 
			data += '</tr>'

			# com_s = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"sampath@tsl-me.com","status":"C-Comparison"})
			# com_m = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"maari@tsl-me.com","status":"C-Comparison"})
			# com_e = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"eduardo@tsl-me.com","status":"C-Comparison"})
			# com_a = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"aakib@tsl-me.com","status":"C-Comparison"})


			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>COMP</b><center></td>'

			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				com_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(com_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				com_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(com_m or 0)
		
			if lp_total_ne_e == "L":
				com_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(com_e or 0)
			
			if lp_total_ne_a == "L":
				com_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(com_a or 0)


			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(com_s + com_m + com_e + com_a)
			data += '</tr>'

			total_out_s = (rs_s or 0) + (ev_s or 0) + (w_s or 0) + (rnr_s or 0) + (rnf_s or 0) + (com_s or 0)
			total_out_m = (rs_m or 0) + (ev_m or 0) + (w_m or 0) + (rnr_m or 0) + (rnf_m or 0) + (com_m or 0)
			total_out_e = (rs_e or 0) + (ev_e or 0) + (w_e or 0) + (rnr_e or 0) + (rnf_e or 0) + (com_e or 0)
			total_out_a = (rs_a or 0) + (ev_a or 0) + (w_a or 0) + (rnr_a or 0) + (rnf_a or 0) + (com_a or 0)

			sum_total_out = (rs_s + rs_m + rs_e + rs_a) + (ev_s + ev_m + ev_e + ev_a) + (w_s + w_m + w_e + w_a) + (rnr_s + rnr_m + rnr_e + rnr_a) + (rnf_a + rnf_s + rnf_e + rnf_m)

			data += '<tr>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b>Total</b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_out_s or 0)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_out_m or 0)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_out_e or 0)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_out_a or 0)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(sum_total_out or 0)
			data += '</tr>'

			data += '</table>'


			data += '<table class="table table-bordered">'

			data += '<tr>'
			data += '<td colspan = "2" style="border-left:hidden;border-top:hidden;border-color:#000000;padding:1px;font-size:15px;font-size:15px;color:white;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
			data += '</tr>'
			p_total_ne_s = 0
			p_total_ne_m = 0
			p_total_ne_e = 0
			p_total_ne_a = 0

			p_total_ner_s = 0
			p_total_ner_m = 0
			p_total_ner_e = 0
			p_total_ner_a = 0
			dat = add_days(today(), -1)
			

			p_total_ne_s = frappe.db.count("Work Order Data",{"technician":"sampath@tsl-me.com","status":"NE-Need Evaluation","posting_date": ["BETWEEN", ["2016-01-01", dat]]})
			p_total_ne_m = frappe.db.count("Work Order Data",{"technician":"maari@tsl-me.com","status":"NE-Need Evaluation","posting_date": ["BETWEEN", ["2016-01-01", dat]]})
			p_total_ne_e = frappe.db.count("Work Order Data",{"technician":"eduardo@tsl-me.com","status":"NE-Need Evaluation","posting_date": ["BETWEEN", ["2016-01-01",dat]]})
			p_total_ne_a = frappe.db.count("Work Order Data",{"technician":"aakib@tsl-me.com","status":"NE-Need Evaluation","posting_date": ["BETWEEN", ["2016-01-01",dat]]})


			p_total_ner_s = frappe.db.count("Work Order Data",{"technician":"sampath@tsl-me.com","status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01", dat]]})
			p_total_ner_m = frappe.db.count("Work Order Data",{"technician":"maari@tsl-me.com","status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01", dat]]})
			p_total_ner_e = frappe.db.count("Work Order Data",{"technician":"eduardo@tsl-me.com","status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01",dat]]})
			p_total_ner_a = frappe.db.count("Work Order Data",{"technician":"aakib@tsl-me.com","status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01",dat]]})
			
			
			nes = total_ne_s- p_total_ne_s
			
			nem = total_ne_m - p_total_ne_m
			nee = total_ne_e - p_total_ne_e
		
			nea = total_ne_a - p_total_ne_a		
						
			ners = total_ner_s- p_total_ner_s
			
			nerm = total_ner_m - p_total_ner_m
			nere = total_ner_e - p_total_ner_e
		
			nera = total_ner_a - p_total_ner_a		
						

			
			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b>NE</b><center></td>'

			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				p_total_ne_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(p_total_ne_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				p_total_ne_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(p_total_ne_m or 0)
			
			if lp_total_ne_e == "L":
				p_total_ne_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(p_total_ne_e or 0)
			
			if lp_total_ne_a == "L":
				p_total_ne_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(p_total_ne_a or 0)
		
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(p_total_ne_s + p_total_ne_m + p_total_ne_e + p_total_ne_a)
			data += '</tr>'

			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b>Pending Works</b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>NER</b><center></td>'

			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				p_total_ner_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(p_total_ner_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				p_total_ner_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(p_total_ner_m or 0)
			
			if lp_total_ne_e == "L":
				p_total_ner_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(p_total_ner_e or 0)
			
			if lp_total_ne_a == "L":
				p_total_ner_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(p_total_ner_a or 0)
		
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(p_total_ner_s + p_total_ner_m + p_total_ner_e + p_total_ner_a)
			data += '</tr>'

					
			tr_s = frappe.db.count("Work Order Data",{"technician":"sampath@tsl-me.com","status":"TR-Technician Repair"})
			tr_m = frappe.db.count("Work Order Data",{"technician":"maari@tsl-me.com","status":"TR-Technician Repair"})
			tr_e = frappe.db.count("Work Order Data",{"technician":"eduardo@tsl-me.com","status":"TR-Technician Repair"})
			tr_a = frappe.db.count("Work Order Data",{"technician":"aakib@tsl-me.com","status":"TR-Technician Repair"})

			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>TR</b><center></td>'
			
			if lp_total_ne_s == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
				tr_s = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(tr_s or 0)

			if lp_total_ne_m == "L":
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
				tr_m = 0
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(tr_m or 0)
			
			if lp_total_ne_e == "L":
				tr_e = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(tr_e or 0)
			
			if lp_total_ne_a == "L":
				tr_a = 0
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
			else:
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(tr_a or 0)


			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(tr_s + tr_m + tr_e + tr_a)
			data += '</tr>'

			# t_p_s = nes + ners + tr_s
			# t_p_m = nem + nerm + tr_m
			# t_p_e = nee + nere + tr_e
			# t_p_a = nea + nera + tr_a
	
			data += '<tr>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>Total</b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>'  %(p_total_ne_s + p_total_ner_s + tr_s)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>'  %(p_total_ne_m + p_total_ner_m + tr_m)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>'  %(p_total_ne_e + p_total_ner_e + tr_e)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>'  %(p_total_ne_a + p_total_ner_a + tr_a)
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>'  %((p_total_ne_s + p_total_ne_m + p_total_ne_e + p_total_ne_a)+(p_total_ner_s + p_total_ner_m + p_total_ner_e + p_total_ner_a)+(tr_s + tr_m + tr_e + tr_a))
			data += '</tr>'

			data += '</table>'
			return data
		
		if self.company == "TSL COMPANY - UAE":
			d = datetime.now().date()
			ogdate = datetime.strptime(str(d),"%Y-%m-%d")
			ogdate_2 = datetime.strptime(str(self.date),"%Y-%m-%d")

			# Format the date as a string in the desired format
			formatted_date = ogdate.strftime("%d-%m-%Y")
			formatted_date_2 = ogdate_2.strftime("%d-%m-%Y")
			
			# date = d.strftime("%Y-%m-%d")
			# original_date = datetime.strptime(str(d), "%Y-%m-%d")
			original_date = self.date


			# Format datetime object to new date string format
			# date = datetime.strptime(str(original_date), "%Y-%m-%d")
			# total_ne = 0

			data = ""
			data += '<table class="table table-bordered">'
			data += '<tr>'
			data += '<td colspan = "7" align = "center" style="border-color:#000000;padding:1px;font-size:20px;background-color:#808080;color:white;"><b>Date :%s</b></td>' %(formatted_date_2)
			data += '</tr>'
			data += '<tr>'
			data += '<td colspan = 2 style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="150"></td>'
			data += '<td colspan = 3 style="border-color:#000000;"><h2><center><b>TSL Company</b></center></h2></td>'
			data += '<td colspan = 2 style="border-color:#000000;"><center><img src = "/files/kuwait flag.jpg" width ="100"></center></td>'
			tech = frappe.get_all("Employee",{"company":self.company,"status": "Active","designation":["in",["Technician","Senior Technician"]]},["first_name"])

			data += '</tr>'
			data += '<tr>'
			# data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;"><center><b></b><center></td>'
			data += '<td colspan = "2" style="border-color:#000000;padding:1px;font-size:18px;font-size:16px;background-color:#3333ff;color:white;"><center><b>Status</b><center></td>'
			for i in tech:
				data += '<td style="border-color:#000000;padding:1px;font-size:18px;font-size:16px;background-color:#FFA500;color:white;"><center><b>%s</b><center></td>' %(i.first_name)
			# data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:18px;font-size:16px;background-color:#FFC000;color:white;"><center><b>Mari</b><center></td>'
			# data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:18px;font-size:16px;background-color:#008000;color:white;"><center><b>ED</b><center></td>'
			# data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:18px;font-size:16px;background-color:#0047AB;color:white;"><center><b>Aakib</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:18px;font-size:16px;background-color:#4682B4;color:white;"><center><b>Total</b><center></td>'
			data += '</tr>'

			technician = frappe.get_all("Employee",{"company":self.company,"status": "Active","designation":["in",["Technician","Senior Technician"]]},["user_id"])

			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>UE</b><center></td>'
			total_ne = 0
			for t in technician:
				# emp = frappe.get_value("Employee",{"user_id":t})
				# if emp:
				# 	lp = frappe.db.sql(
				# 		"""
				# 		SELECT employee
				# 		FROM `tabLeave Application Form` 
				# 		WHERE employee = %s
				# 		AND %s BETWEEN from_date AND to_date and docstatus = 1
				# 		""",
				# 		(emp,self.date),
				# 		as_dict=True
				# 	)
				# 	if lp:
				# 		if t == "sampath@tsl-me.com":
				# 			lp_total_ne_s = "L"
				# 		if t == "maari@tsl-me.com":
				# 			lp_total_ne_m = "L"
				# 		if t == "eduardo@tsl-me.com":
				# 			lp_total_ne_e = "L"
				# 		if t == "aakib@tsl-me.com":
				# 			lp_total_ne_a = "L"
				
				ne = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
						left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
						where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
						and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t.user_id,original_date),as_dict=1)
				total_ne = total_ne + ne[0]["ct"]
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ne[0]["ct"] or 0)

			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ne or 0)

				
			data += '</tr>'

			data += '<tr>'
			data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>Started Work</b><center></td>'
			data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>NER</b><center></td>'
			
			total_ner = 0
			for t in technician:
				ner = frappe.db.count("Work Order Data",{"technician":t.user_id,"status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ner or 0)

			total_ner = total_ne + ner

			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ner or 0)

			data += '<tr>'
			data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>Total</b><center></td>'
			
			sum_ne_ner = 0

			for t in technician:
				ne = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
				and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t.user_id,original_date),as_dict=1)
				ner = frappe.db.count("Work Order Data",{"technician":t.user_id,"status":"NER-Need Evaluation Return","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
				
				sum_ne_ner = (sum_ne_ner + ner+ne[0]["ct"])
				data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(ner + ne[0]["ct"])
			
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(sum_ne_ner or 0)

			data += '</tr>'

			data += '</table>'

		data += '<table class="table table-bordered">'
			
		data += '<tr>'
		data += '<td colspan = "2" style="border-left:hidden;border-top:hidden;border-color:#000000;padding:1px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '</tr>'

		total_ue_s = frappe.db.count("Work Order Data",{"technician":"sampath@tsl-me.com","status":"UE-Under Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
		total_ue_m = frappe.db.count("Work Order Data",{"technician":"maari@tsl-me.com","status":"UE-Under Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
		total_ue_e = frappe.db.count("Work Order Data",{"technician":"eduardo@tsl-me.com","status":"UE-Under Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
		total_ue_a = frappe.db.count("Work Order Data",{"technician":"aakib@tsl-me.com","status":"UE-Under Evaluation","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
		
		total_utr_s = frappe.db.count("Work Order Data",{"technician":"sampath@tsl-me.com","status":"UTR-Under Technician Repair","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
		total_utr_m = frappe.db.count("Work Order Data",{"technician":"maari@tsl-me.com","status":"UTR-Under Technician Repair","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
		total_utr_e = frappe.db.count("Work Order Data",{"technician":"eduardo@tsl-me.com","status":"UTR-Under Technician Repair","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})
		total_utr_a = frappe.db.count("Work Order Data",{"technician":"aakib@tsl-me.com","status":"UTR-Under Technician Repair","posting_date": ["BETWEEN", ["2016-01-01",self.date]]})

		for t in tech:
			ue = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
				and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
			
			if t == "sampath@tsl-me.com":
				ue_s = ue[0]["ct"]
			if t == "maari@tsl-me.com":
				ue_m = ue[0]["ct"]
			if t == "eduardo@tsl-me.com":
				ue_e = ue[0]["ct"]
			if t == "aakib@tsl-me.com":
				ue_a = ue[0]["ct"]

			utr = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "UTR-Under Technician Repair"
				and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date),as_dict=1)
			
			if t == "sampath@tsl-me.com":
				utr_s = utr[0]["ct"]
			if t == "maari@tsl-me.com":
				utr_m = utr[0]["ct"]
			if t == "eduardo@tsl-me.com":
				utr_e = utr[0]["ct"]
			if t == "aakib@tsl-me.com":
				utr_a = utr[0]["ct"]
			# ne = frappe.get_all("Work Order Data",{"technician":t},["*"])
			# for i in ne:
			# 	sd = frappe.get_doc("Work Order Data",i.name)
			# 	for j in sd.status_duration_details:
				
			# 		timestamp = str(j.date) 
			# 		date_portion = timestamp[:10]
					
			# 		j.date= date_portion
					
			# 		if "UE-Under Evaluation" == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
			# 			ue_s = ue_s + 1
			# 		if "UE-Under Evaluation" == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
			# 			ue_m = ue_m + 1
					
			# 		if "UE-Under Evaluation" == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
			# 			ue_e = ue_e + 1
			# 		if "UE-Under Evaluation" == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
			# 			ue_a = ue_a + 1
						
			# 		if "UTR-Under Technician Repair" == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
			# 			utr_s = utr_s + 1
			# 		if "UTR-Under Technician Repair" == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
			# 			utr_m = utr_m + 1
					
			# 		if "UTR-Under Technician Repair" == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
			# 			utr_e = utr_e + 1
			# 		if "UTR-Under Technician Repair" == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
			# 			utr_a = utr_a + 1
						

		data += '<tr>'
		data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>UE</b><center></td>' 
		
		
		if lp_total_ne_s == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
			total_ue_s = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ue_s or 0)

		if lp_total_ne_m == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
			total_ue_m = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ue_m or 0)
		
		if lp_total_ne_e == "L":
			total_ue_e = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ue_e or 0)
		
		if lp_total_ne_a == "L":
			total_ue_a = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(total_ue_a or 0)

		
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_ue_s + total_ue_m + total_ue_e + total_ue_a)
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>End of the Work</b><center></td>'
		data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>UTR</b><center></td>'
		
		if lp_total_ne_s == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
			total_utr_s = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_utr_s or 0)

		if lp_total_ne_m == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
			total_utr_m = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_utr_m or 0)
		
		if lp_total_ne_e == "L":
			total_utr_e = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_utr_e or 0)
		
		if lp_total_ne_a == "L":
			total_utr_a = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(total_utr_a or 0)


		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(total_utr_s +total_utr_m + total_utr_e + total_utr_a)
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>Site Visit</b><center></td>'
		
		if lp_total_ne_s == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
			total_utr_s = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(0 or 0)

		if lp_total_ne_m == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
			total_utr_m = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(0 or 0)
		
		if lp_total_ne_e == "L":
			total_utr_e = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(0 or 0)
		
		if lp_total_ne_a == "L":
			total_utr_a = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(0 or 0)

			
		data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;"><center><b>0	</b><center></td>'
		
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>Total</b><center></td>'
		

		data += '<td style="border-color:#000000;;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ue_s + total_utr_s)
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ue_m + total_utr_m)
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ue_e + total_utr_e)
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_ue_a + total_utr_a)
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %((total_ue_s + total_ue_m + total_ue_e + total_ue_a)+(total_utr_s +  total_utr_m + total_utr_e + total_utr_a))
		data += '</tr>'

		data += '</table>'

		data += '<table class="table table-bordered">'
		
		data += '<tr>'
		data += '<td colspan = "2" style="border-left:hidden;border-top:hidden;border-color:#000000;padding:1px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '<td style="border-right:hidden;border-top:hidden;border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;color:white;"><center><b></b><center></td>'
		data += '</tr>'

		for t in tech:
			s = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped"
				and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
			
			if t == "sampath@tsl-me.com":
				rs_s = s[0]["ct"]
			if t == "maari@tsl-me.com":
				rs_m = s[0]["ct"]
			if t == "eduardo@tsl-me.com":
				rs_e = s[0]["ct"]
			if t == "aakib@tsl-me.com":
				rs_a = s[0]["ct"]

			w = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "W-Working" 
				and `tabWork Order Data`.technician = "%s" 
				and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
			
			r = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" 
				and `tabWork Order Data`.technician = "%s" 
				and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
			
			# if t == "sampath@tsl-me.com":
			# 	# if not r:
			# 	w_s = w[0]["ct"]
			# if t == "maari@tsl-me.com":
			# 	# if not r:
			# 	w_m = w[0]["ct"]
			# if t == "eduardo@tsl-me.com":
			# 	# if not r:
			# 	w_e = w[0]["ct"]
			# if t == "aakib@tsl-me.com":
			# 	# if not r:
			# 	w_a = w[0]["ct"]

			rnr = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "RNR-Return Not Repaired"
						and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
			
			if t == "sampath@tsl-me.com":
				rnr_s = rnr[0]["ct"]
			if t == "maari@tsl-me.com":
				rnr_m = rnr[0]["ct"]
			if t == "eduardo@tsl-me.com":
				rnr_e = rnr[0]["ct"]
			if t == "aakib@tsl-me.com":
				rnr_a = rnr[0]["ct"]

			rnf = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "RNF-Return No Fault"
				and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
			
			if t == "sampath@tsl-me.com":
				rnf_s = rnf[0]["ct"]
			if t == "maari@tsl-me.com":
				rnf_m = rnf[0]["ct"]
			if t == "eduardo@tsl-me.com":
				rnf_e = rnf[0]["ct"]
			if t == "aakib@tsl-me.com":
				rnf_a = rnf[0]["ct"]

			com = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
				left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
				where  `tabStatus Duration Details`.status = "C-Comparison"
						and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date  LIKE "%s%%" """ %(t,original_date) ,as_dict=1)
			
			if t == "sampath@tsl-me.com":
				com_s = com[0]["ct"]
			if t == "maari@tsl-me.com":
				com_m = com[0]["ct"]
			if t == "eduardo@tsl-me.com":
				com_e = com[0]["ct"]
			if t == "aakib@tsl-me.com":
				com_a = com[0]["ct"]


			# ne = frappe.get_all("Work Order Data",{"technician":t},["*"])
			# for i in ne:
			# 	sd = frappe.get_doc("Work Order Data",i.name)
			# 	for j in sd.status_duration_details:
				
			# 		timestamp = str(j.date) 
			# 		date_portion = timestamp[:10]
					
			# 		j.date= date_portion
					
			# 		if "RS-Repaired and Shipped"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
			# 			rs_s = rs_s + 1
			# 		if "RS-Repaired and Shipped"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
			# 			rs_m = rs_m + 1
			# 		if "RS-Repaired and Shipped"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
			# 			rs_e = rs_e + 1
			# 		if "RS-Repaired and Shipped"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
			# 			rs_a = rs_a + 1

			# 		s = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data` .name) as ct from `tabWork Order Data` 
			# 			left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
			# 			where  `tabStatus Duration Details`.status = "W-Working" 
			# 			and `tabWork Order Data`.technician = "%s" and `tabStatus Duration Details`.date LIKE "%s" """ %("sampath@tsl-me.com",original_date) ,as_dict=1)
			# 		
			# 		if "W-Working"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
			# 			w_s = w_s + 1
						
			# 		if "W-Working"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
			# 			w_m = w_m + 1
						
			# 		if "W-Working"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
			# 			w_e = w_e + 1
			# 		if "W-Working"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
			# 			w_a = w_a + 1

			# 		if "RNR-Return Not Repaired"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
			# 			rnr_s = rnr_s + 1
			# 		if "RNR-Return Not Repaired"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
			# 			rnr_m = rnr_m + 1
			# 		if "RNR-Return Not Repaired"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
			# 			rnr_e = rnr_e + 1
			# 		if "RNR-Return Not Repaired"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
			# 			rnr_a = rnr_a + 1
					
			# 		if "RNF-Return No Fault"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
			# 			rnf_s = rnf_s + 1
			# 		if "RNF-Return No Fault"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
			# 			rnf_m = rnf_m + 1
			# 		if "RNF-Return No Fault"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
			# 			rnf_e = rnf_e + 1
			# 		if "RNF-Return No Fault"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
			# 			rnf_a = rnf_a + 1

			# 		if "C-Comparison"  == j.status and i.technician == "sampath@tsl-me.com" and str(j.date) == original_date:
			# 			com_s = com_s + 1
			# 		if "C-Comparison"  == j.status and i.technician == "maari@tsl-me.com" and str(j.date) == original_date:
			# 			com_m = com_m + 1
			# 		if "C-Comparison"  == j.status and i.technician == "eduardo@tsl-me.com" and str(j.date) == original_date:
			# 			com_e = com_e + 1
			# 		if "C-Comparison"  == j.status and i.technician == "aakib@tsl-me.com" and str(j.date) == original_date:
			# 			com_a = com_a + 1
					
					
					
		
		data += '<tr>'
		data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>RS</b><center></td>'
		
		if lp_total_ne_s == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
			rs_s = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rs_s or 0)

		if lp_total_ne_m == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
			rs_m = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rs_m or 0)
		
		if lp_total_ne_e == "L":
			rs_e = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rs_e or 0)
		
		if lp_total_ne_a == "L":
			rs_a = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(rs_a or 0)

			
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rs_s + rs_m + rs_e + rs_a)
		data += '</tr>'

		ev_s = 0
		ev_m = 0
		ev_e = 0
		ev_a = 0

		# for t in tech:
		# 	ne = frappe.get_all("Work Order Data",{"date":original_date,"technician":t},["*"])
		# 	for i in ne:
		# 		ev = frappe.db.exists("Evaluation Report",{"work_order_data":i.name})
		# 		if ev:
		# 			techni = frappe.get_value("Evaluation Report",{"name":ev},["technician"])
		# 			if techni == "sampath@tsl-me.com":
		# 				ev_s = ev_s + 1
		# 			if techni == "maari@tsl-me.com":
		# 				ev_m = ev_m + 1
		# 			if techni == "eduardo@tsl-me.com":
		# 				ev_e = ev_e + 1
		# 			if techni == "aakib@tsl-me.com":
		# 				ev_a = ev_a + 1
		ev_s = frappe.db.count("Evaluation Report",{"date":original_date,"technician":"sampath@tsl-me.com"})
		ev_m = frappe.db.count("Evaluation Report",{"date":original_date,"technician":"maari@tsl-me.com"})
		ev_e = frappe.db.count("Evaluation Report",{"date":original_date,"technician":"eduardo@tsl-me.com"})
		ev_a = frappe.db.count("Evaluation Report",{"date":original_date,"technician":"aakib@tsl-me.com"})
					
		

		data += '<tr>'
		data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b>PS</b><center></td>'
		
		
		if lp_total_ne_s == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
			ev_s = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ev_s or 0)

		if lp_total_ne_m == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
			ev_m = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ev_m or 0)
		
		if lp_total_ne_e == "L":
			ev_e = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ev_e or 0)
		
		if lp_total_ne_a == "L":
			ev_a = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(ev_a or 0)

		
		
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(ev_s + ev_m + ev_e + ev_a)
		data += '</tr>'

		
		data += '<tr>'
		data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>W</b><center></td>'
		
		if lp_total_ne_s == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
			w_s = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(w_s or 0)

		if lp_total_ne_m == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
			w_m = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(w_m or 0)
		
		if lp_total_ne_e == "L":
			w_e = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(w_e or 0)
		
		if lp_total_ne_a == "L":
			w_a = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(w_a or 0)

	
		
		
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(w_s + w_m + w_e + w_a)
		data += '</tr>'

		
		data += '<tr>'
		data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b>Out - Flow</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>RNR</b><center></td>'


		if lp_total_ne_s == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
			rnr_s = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnr_s or 0)

		if lp_total_ne_m == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
			rnr_m = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnr_m or 0)
	
		if lp_total_ne_e == "L":
			rnr_e = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnr_e or 0)
		
		if lp_total_ne_a == "L":
			rnr_a = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(rnr_a or 0)

	
	

		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnr_s + rnr_m + rnr_e + rnr_a)
		data += '</tr>'

		# rnf_s = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"sampath@tsl-me.com","status":"RNF-Return No Fault"})
		# rnf_m = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"maari@tsl-me.com","status":"RNF-Return No Fault"})
		# rnf_e = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"eduardo@tsl-me.com","status":"RNF-Return No Fault"})
		# rnf_a = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"aakib@tsl-me.com","status":"RNF-Return No Fault"})


		data += '<tr>'
		data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>RNF</b><center></td>'

		if lp_total_ne_s == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
			rnf_s = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnf_s or 0)

		if lp_total_ne_m == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
			rnf_m = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnf_m or 0)
	
		if lp_total_ne_e == "L":
			rnf_e = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnf_e or 0)
		
		if lp_total_ne_a == "L":
			rnf_a = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(rnf_a or 0)



		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(rnf_a + rnf_s + rnf_e + rnf_m) 
		data += '</tr>'

		# com_s = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"sampath@tsl-me.com","status":"C-Comparison"})
		# com_m = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"maari@tsl-me.com","status":"C-Comparison"})
		# com_e = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"eduardo@tsl-me.com","status":"C-Comparison"})
		# com_a = frappe.db.count("Work Order Data",{"posting_date":original_date,"technician":"aakib@tsl-me.com","status":"C-Comparison"})


		data += '<tr>'
		data += '<td style="border-bottom:hidden;border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>COMP</b><center></td>'

		if lp_total_ne_s == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_s or 0)
			com_s = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(com_s or 0)

		if lp_total_ne_m == "L":
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_m or 0)
			com_m = 0
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(com_m or 0)
	
		if lp_total_ne_e == "L":
			com_e = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(lp_total_ne_e or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(com_e or 0)
		
		if lp_total_ne_a == "L":
			com_a = 0
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(lp_total_ne_a or 0)
		else:
			data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>'%(com_a or 0)


		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;"><center><b>%s</b><center></td>' %(com_s + com_m + com_e + com_a)
		data += '</tr>'

		total_out_s = (rs_s or 0) + (ev_s or 0) + (w_s or 0) + (rnr_s or 0) + (rnf_s or 0) + (com_s or 0)
		total_out_m = (rs_m or 0) + (ev_m or 0) + (w_m or 0) + (rnr_m or 0) + (rnf_m or 0) + (com_m or 0)
		total_out_e = (rs_e or 0) + (ev_e or 0) + (w_e or 0) + (rnr_e or 0) + (rnf_e or 0) + (com_e or 0)
		total_out_a = (rs_a or 0) + (ev_a or 0) + (w_a or 0) + (rnr_a or 0) + (rnf_a or 0) + (com_a or 0)

		sum_total_out = (rs_s + rs_m + rs_e + rs_a) + (ev_s + ev_m + ev_e + ev_a) + (w_s + w_m + w_e + w_a) + (rnr_s + rnr_m + rnr_e + rnr_a) + (rnf_a + rnf_s + rnf_e + rnf_m)

		data += '<tr>'
		data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b></b><center></td>'
		data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:15px;background-color:#A7C7E7;"><center><b>Total</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_out_s or 0)
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_out_m or 0)
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_out_e or 0)
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(total_out_a or 0)
		data += '<td style="border-color:#000000;padding:1px;font-size:15px;font-size:15px;background-color:#A7C7E7;"><center><b>%s</b><center></td>' %(sum_total_out or 0)
		data += '</tr>'

		data += '</table>'

		return data