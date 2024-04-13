# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class PurchaseReport(Document):
	@frappe.whitelist()
	def get_data(self):
		data= ""
		data += '<div class="table-container">'
		data += '<h3><b><center>WO<center><b><h3>'
		data += '<table class="table table-bordered">'
		
		ordered = frappe.db.count("Work Order Data",{"status":"Q-Quoted","posting_date": ["between", [self.date, self.date]]})
		quot = frappe.db.count("Work Order Data",{"status":"Parts Priced","posting_date": ["between", [self.date, self.date]]})
		rec =  frappe.db.count("Work Order Data",{"status":"TR-Technician Repair","posting_date": ["between", [self.date, self.date]]})
		app =  frappe.db.count("Work Order Data",{"status":"A-Approved","posting_date": ["between", [self.date, self.date]]})
		not_qt =  frappe.db.count("Work Order Data",{"status":"SP-Searching Parts","posting_date": ["between", [self.date, self.date]]})
		wp =  frappe.db.count("Work Order Data",{"status":"WP-Waiting Parts","posting_date": ["between", ["2023-07-23", self.date]]})
		np =  frappe.db.count("Work Order Data",{"status":"RNP-Return No Parts","posting_date": ["between", [self.date, self.date]]})


		s_quoted = frappe.db.count("Supply Order Data",{"status":"Quoted","posting_date": ["between", [self.date, self.date]]})
		s_ordered = frappe.db.count("Supply Order Data",{"status":"Ordered","posting_date": ["between", [self.date, self.date]]})
		s_received = frappe.db.count("Supply Order Data",{"status":"Received","posting_date": ["between", [self.date, self.date]]})
		s_approved = frappe.db.count("Supply Order Data",{"status":"Approved","posting_date": ["between", [self.date, self.date]]})
		s_not_quoted = frappe.db.count("Supply Order Data",{"status":"Inquiry","posting_date": ["between", [self.date, self.date]]})
		s_not_found = frappe.db.count("Supply Order Data",{"status":"Inquiry","posting_date": ["between", [self.date, self.date]]})
		waiting_so = frappe.db.count("Supply Order Data",{"status":"ordered","posting_date": ["between", ["2023-07-23", self.date]]})


		# quot = frappe.db.count("Supply Order Data",{"status":"Parts Priced","posting_date": ["between", [self.date, self.date]]})
		# rec =  frappe.db.count("Supply Order Data",{"status":"TR-Technician Repair","posting_date": ["between", [self.date, self.date]]})
		# app =  frappe.db.count("Supply Order Data",{"status":"A-Approved","posting_date": ["between", [self.date, self.date]]})
		# not_qt =  frappe.db.count("Supply Order Data",{"status":"SP-Searching Parts","posting_date": ["between", [self.date, self.date]]})
		# wp =  frappe.db.count("Supply Order Data",{"status":"WP-Waiting Parts","returned_date": ["between", [self.date, self.date]]})
		# np =  frappe.db.count("Supply Order Data",{"status":"RNP-Return No Parts","posting_date": ["between", [self.date, self.date]]})

		data += '<tr>'
		data += '<td colspan = 4 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Achievments</b><center></td>'
		data += '<td colspan = 4 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Status</b><center></td>'
		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Current Status</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Count</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Status</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Count</b><center></td>'

		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Not Found</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(np)
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Approved</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(app)

		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Ordered</b><center></td>' 
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>'%(ordered)
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Not Quoted</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(not_qt)

		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Quoted</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(quot)
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Waiting PS</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(wp)

		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Received</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(rec)
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'

		data += '</tr>'
		data += '</table>'

		data += '<h3><b><center>SO<center><b><h3>'
		data += '<table class="table table-bordered">'
		data += '<tr>'
		data += '<td colspan = 4 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Achievments</b><center></td>'
		data += '<td colspan = 4 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Status</b><center></td>'
		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Current Status</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Count</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Status</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Count</b><center></td>'

		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Not Found</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(s_not_found)
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Approved</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(s_approved)

		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Ordered</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(s_ordered)
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Not Quoted</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>'  %(s_not_quoted)

		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Quoted</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(s_quoted)
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>Waiting SO</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(waiting_so)

		data += '</tr>'

		data += '<tr>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;color:white;"><center><b>Received</b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(s_received)
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'
		data += '<td colspan = 2 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b></b><center></td>'

		data += '</tr>'
		data += '</table>'
		data += '</div>'
		return data
