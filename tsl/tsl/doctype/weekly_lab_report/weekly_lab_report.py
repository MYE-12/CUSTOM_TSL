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

class WeeklyLabReport(Document):
	@frappe.whitelist()
	def get_data(self):
		d = datetime.now().date()
		ogdate = datetime.strptime(str(d),"%Y-%m-%d")

		# Format the date as a string in the desired format
		formatted_date = ogdate.strftime("%d-%m-%Y")
		
		from_date = add_days(d,-7)
		br = ""
		if self.company == "TSL COMPANY - Kuwait":
			br = "Kuwait"
		if self.company == "TSL COMPANY - UAE":
			br = "UAE"
			

		data= ""
		data += '<div class="table-container">'
		data += '<table class="table table-bordered">'
		data += '<tr>'
		data += '<td colspan = 1 align = center style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="250"></td>'
		data += '<td colspan = 2 style="border-color:#000000;"><h2><center><b style="color:#055c9d;">TSL Company <br> Branch - %s</b></center></h2></td>' %(br)
		data += '<td colspan = 1 style="border-color:#000000;"><center><img src = "/files/kuwait flag.jpg" width ="150"></center></td>'
		
		data += '<tr>'
		data += '<td colspan = 4 style="border-color:#000000;padding:1px;font-size:20px;background-color:#0e86d4;color:white;"><b>%s</b></td>' %(formatted_date)
		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#0e86d4;color:white;width:25%;"><center><b>Status</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#0e86d4;color:white;width:25%;"><center><b>WOD Count</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#0e86d4;color:white;width:25%;"><center><b>More than a Week</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#0e86d4;color:white;width:25%;"><center><b>Remarks</b><center></td>'

		data += '</tr>'

		ne_1 =  frappe.db.count("Work Order Data",{"status":"NE-Need Evaluation","company":self.company,"old_wo_no":["is","not set"]})
		ner_1 =  frappe.db.count("Work Order Data",{"status":"NER-Need Evaluation Return","company":self.company,"old_wo_no":["is","not set"]})
		ue_1 =  frappe.db.count("Work Order Data",{"status":"UE-Under Evaluation","company":self.company,"old_wo_no":["is","not set"]})
		utr_1 =  frappe.db.count("Work Order Data",{"status":"UTR-Under Technician Repair","company":self.company,"old_wo_no":["is","not set"]})
		tr_1 =  frappe.db.count("Work Order Data",{"status":"TR-Technician Repair","company":self.company,"old_wo_no":["is","not set"]})
		sp_1 =  frappe.db.count("Work Order Data",{"status":"SP-Searching Parts","company":self.company,"old_wo_no":["is","not set"]})
		wp_1 =  frappe.db.count("Work Order Data",{"status":"WP-Waiting Parts","company":self.company,"old_wo_no":["is","not set"]})

		# ne = frappe.db.sql(""" select count(`tabWork Order Data` .name) as wd from `tabWork Order Data` 
		# where  `tabWork Order Data`.posting_date < '%s' and `tabWork Order Data`.status = "NE-Need Evaluation" and `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL """ %(from_date,self.company) ,as_dict=1)

		ne = frappe.db.sql("""
		SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS wd
		FROM `tabWork Order Data`
		LEFT JOIN `tabStatus Duration Details` ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		WHERE `tabStatus Duration Details`.status = "NE-Need Evaluation"
		AND `tabWork Order Data`.status = "NE-Need Evaluation"
		AND `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL
		AND DATE(`tabStatus Duration Details`.date) < '%s'
		""" % (self.company,from_date), as_dict=1)


		# ner = frappe.db.sql(""" select count(`tabWork Order Data` .name) as wd from `tabWork Order Data` 
		# where  `tabWork Order Data`.status_cap_date < '%s' and `tabWork Order Data`.status = "NER-Need Evaluation Return" and `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL """ %(from_date,self.company) ,as_dict=1)
		
		ner = frappe.db.sql("""
		SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS wd
		FROM `tabWork Order Data`
		LEFT JOIN `tabStatus Duration Details` ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		WHERE `tabStatus Duration Details`.status = "NER-Need Evaluation Return"
		AND `tabWork Order Data`.status = "NER-Need Evaluation Return"
		AND `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL
		and DATE(`tabStatus Duration Details`.date) BETWEEN '%s' AND '%s';
		""" % (self.company,from_date,d), as_dict=1)

		
		# ner_2 = frappe.db.sql("""
		# SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS wd
		# FROM `tabWork Order Data`
		# LEFT JOIN `tabStatus Duration Details` ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		# WHERE `tabStatus Duration Details`.status = "NER-Need Evaluation Return"
		# AND `tabWork Order Data`.status = "NER-Need Evaluation Return"
		# AND `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL
		# AND DATE(`tabStatus Duration Details`.date) BETWEEN '%s' AND '%s';
		# """ % (self.company,from_date,d), as_dict=1)

		

		# ue = frappe.db.sql(""" select count(`tabWork Order Data` .name) as wd from `tabWork Order Data` 
		# where  `tabWork Order Data`.posting_date < '%s' and `tabWork Order Data`.status = "UE-Under Evaluation" and `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL """ %(from_date,self.company) ,as_dict=1)
		
		ue = frappe.db.sql("""
		SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS wd
		FROM `tabWork Order Data`
		LEFT JOIN `tabStatus Duration Details` ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		WHERE `tabStatus Duration Details`.status = 'UE-Under Evaluation'
		AND `tabWork Order Data`.status = 'UE-Under Evaluation'
		AND `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL
		AND DATE(`tabStatus Duration Details`.date) < '%s'
		""" % (self.company,from_date), as_dict=1)
		# frappe.errprint(frodate)

		utr = frappe.db.sql("""
		SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS wd
		FROM `tabWork Order Data`
		LEFT JOIN `tabStatus Duration Details` ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		WHERE `tabStatus Duration Details`.status = "UTR-Under Technician Repair"
		AND `tabWork Order Data`.status = "UTR-Under Technician Repair"
		AND `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL
		AND DATE(`tabStatus Duration Details`.date) < '%s' AND DATE(`tabStatus Duration Details`.date) > '%s' 
		""" % (self.company,from_date,from_date), as_dict=1)

		# utr = frappe.db.sql(""" select count(`tabWork Order Data` .name) as wd from `tabWork Order Data` 
		# where  `tabWork Order Data`.posting_date < '%s' and `tabWork Order Data`.status = "UTR-Under Technician Repair" and `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL """ %(from_date,self.company) ,as_dict=1)
		
		tr = frappe.db.sql("""
		SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS wd
		FROM `tabWork Order Data`
		LEFT JOIN `tabStatus Duration Details` ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		WHERE `tabStatus Duration Details`.status = "TR-Technician Repair"
		AND `tabWork Order Data`.status = "TR-Technician Repair"
		AND `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL
		AND DATE(`tabStatus Duration Details`.date) < '%s'
		""" % (self.company,from_date), as_dict=1)

		# tr = frappe.db.sql(""" select count(`tabWork Order Data` .name) as wd from `tabWork Order Data` 
		# where  `tabWork Order Data`.posting_date < '%s' and `tabWork Order Data`.status = "TR-Technician Repair" and `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL """ %(from_date,self.company) ,as_dict=1)
		
		sp = frappe.db.sql("""
		SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS wd
		FROM `tabWork Order Data`
		LEFT JOIN `tabStatus Duration Details` ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		WHERE `tabStatus Duration Details`.status = "SP-Searching Parts"
		AND `tabWork Order Data`.status = "SP-Searching Parts"
		AND `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL
		AND DATE(`tabStatus Duration Details`.date) < '%s'
		""" % (self.company,from_date), as_dict=1)

		# sp = frappe.db.sql(""" select count(`tabWork Order Data` .name) as wd from `tabWork Order Data` 
		# where  `tabWork Order Data`.posting_date < '%s' and `tabWork Order Data`.status = "SP-Searching Parts" and `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL  """ %(from_date,self.company) ,as_dict=1)
		
		# wp = frappe.db.sql(""" select count(`tabWork Order Data` .name) as wd from `tabWork Order Data` 
		# where  `tabWork Order Data`.posting_date < '%s' and `tabWork Order Data`.status = "WP-Waiting Parts" and `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL """ %(from_date,self.company) ,as_dict=1)
		
		wp = frappe.db.sql("""
		SELECT COUNT(DISTINCT `tabWork Order Data`.name) AS wd
		FROM `tabWork Order Data`
		LEFT JOIN `tabStatus Duration Details` ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		WHERE `tabStatus Duration Details`.status = "WP-Waiting Parts"
		AND `tabWork Order Data`.status = "WP-Waiting Parts"
		AND `tabWork Order Data`.company = '%s' and`tabWork Order Data`.old_wo_no IS NULL
		AND DATE(`tabStatus Duration Details`.date) < '%s'
		""" % (self.company,from_date), as_dict=1)

		ner_3 = ner_1-ner[0]["wd"]

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b>NE</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(ne_1)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(ne[0]["wd"])
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b></b><center></td>'
		data += '</tr>'

		
		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b>NER</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(ner_1)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(ner_3)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b></b><center></td>'
		data += '</tr>'
		
		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b>UE</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(ue_1)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(ue[0]["wd"])
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b></b><center></td>'

		data += '</tr>'
			
		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b>UTR</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(utr_1)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(utr[0]["wd"])
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b></b><center></td>'

		data += '</tr>'

		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b>TR</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(tr_1)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(tr[0]["wd"])
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b></b><center></td>'

		data += '</tr>'
			
		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b>SP</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(sp_1)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(sp[0]["wd"])
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b></b><center></td>'

		data += '</tr>'
		
		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b>WP</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(wp_1)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;"><center><b>%s</b><center></td>' %(wp[0]["wd"])
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;"><center><b></b><center></td>'

		data += '</tr>'
		
		data += '<tr>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;width:25%;background-color:#0e86d4;color:white;"><center><b>Total</b><center></td>'
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#0e86d4;color:white;"><center><b>%s</b><center></td>' %(ne_1 + ner_1 + ue_1 + utr_1 + sp_1 + tr_1 + wp_1)
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#0e86d4;color:white;"><center><b>%s</b><center></td>' %(ne[0]["wd"] + ner_3 + ue[0]["wd"] + utr[0]["wd"] + tr[0]["wd"] + sp[0]["wd"] + wp[0]["wd"])
		data += '<td style="border-color:#000000;padding:1px;font-size:16px;background-color:#0e86d4;color:white;width:25%;"><center><b></b><center></td>'

		data += '</tr>'
		data += '</table>'



		data += '</div>'
		return data

