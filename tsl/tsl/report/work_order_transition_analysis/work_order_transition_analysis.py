# Copyright (c) 2025, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta
from datetime import date



def execute(filters=None):
	columns=get_columns(filters)
	data = get_data(filters) 
	return columns, data

def get_columns(filters):

	columns = [
        _("Work Order Data") + ":Link/Work Order Data:150",
        _("Received Date") + ":Data:130",
		_("Quoted Amount") + ":Data:130",
        _("RS Date") + ":Data:130",
        _("RSC Date") + ":Data:130",
		_("Delivery Note") + ":Data:130",
		_("Return Issued") + ":Check:130",
        _("RSI Date") + ":Data:130",
		_("Sales Invoice") + ":Data:130",
		_("SI Status") + ":Data:130",
        _("Day Difference(RSC & RSI)") + ":Data:120:Center:B",
    ]
	
	return columns

def get_data(filters):
	data = []

	# Extract year from filters
	
	if filters.year:
		year = int(filters.year)  # Ensure the year is an integer

		# Calculate the first and last dates of the year
		first_date = date(year, 1, 1)  # January 1st of the year
		last_date = date(year, 12, 31)  # December 31st of the year

		# Log the first and last date for debugging
		# frappe.errprint(f"Year: {year}, First Date: {first_date}, Last Date: {last_date}")

		# Fetch data from "Work Order Data" within the date range and company filter
		w = frappe.get_all(
			"Work Order Data",
			filters={
				"posting_date": ["between", [first_date, last_date]],
				"company": filters.company
			},
			fields=["*"]
		)
	
	else:
		w = frappe.get_all(
			"Work Order Data",
			filters={
				"old_wo_no":["is","not set"],
				"company": filters.company
			},
			fields=["*"]
		)
		
	# Process and add work order data to the result
	
	for i in w:
		rs = frappe.db.sql("""
		SELECT `tabStatus Duration Details`.date AS d
		FROM `tabWork Order Data`
		LEFT JOIN `tabStatus Duration Details`
		ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		WHERE `tabStatus Duration Details`.status = "RS-Repaired and Shipped"
		AND `tabWork Order Data`.name = %s
		ORDER BY `tabStatus Duration Details`.date DESC
		LIMIT 1
		""", (i.name,), as_dict=1)
		
		rs_d = ""

		# rsc = frappe.db.sql("""
		# SELECT `tabStatus Duration Details`.date AS d
		# FROM `tabWork Order Data`
		# LEFT JOIN `tabStatus Duration Details`
		# ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		# WHERE `tabStatus Duration Details`.status = "RSC-Repaired and Shipped Client"
		# AND `tabWork Order Data`.name = %s
		# ORDER BY `tabStatus Duration Details`.date DESC
		
		# """, (i.name,), as_dict=1)
		dn = frappe.get_value("Work Order Data",{"name":i.name},["dn_no"])

		rsc = frappe.get_value("Work Order Data",{"name":i.name},["dn_date"])
		rsc_d = ""
		if rsc:
			rsc_d = rsc
		check_re = 0
		re = frappe.db.exists("Return Note",{"work_order_data":i.name})
		if re:
			check_re = 1
		# rsi = frappe.db.sql("""
		# SELECT `tabStatus Duration Details`.date AS d
		# FROM `tabWork Order Data`
		# LEFT JOIN `tabStatus Duration Details`
		# ON `tabWork Order Data`.name = `tabStatus Duration Details`.parent
		# WHERE `tabStatus Duration Details`.status = "RSI-Repaired and Shipped Invoiced"
		# AND `tabWork Order Data`.name = %s
		# ORDER BY `tabStatus Duration Details`.date DESC
		
		# """, (i.name,), as_dict=1)
		si = frappe.get_value("Work Order Data",{"name":i.name},["invoice_no"])
		rsi = frappe.get_value("Work Order Data",{"name":i.name},["invoice_date"])
		rsi_d = ""
		if rsi:
			# if i.name == "WOD-K25-13808":
			# 	frappe.errprint(rsi)
			rsi_d = rsi
		
		ss = ""
		if si:
			sales = frappe.get_value("Sales Invoice",{"name":si},["status"])
			ss = sales
		if rs:
			rs_d = rs[0]["d"].date()

		dd = ""
		if rsc and rsi:
			# Convert date strings to datetime objects
			date_str1 = str(rsc_d)
			date_str2 = str(rsi_d)
			date1 = datetime.strptime(date_str1, "%Y-%m-%d")
			date2 = datetime.strptime(date_str2, "%Y-%m-%d")

			# Calculate the difference
			difference = date2 - date1

			# Extract the number of days directly from the timedelta object
			dd = difference.days  # This gives the difference in days as an integer

			# If needed, you can print or log the difference
			# frappe.errprint(dd)  #
		elif rsc and not rsi:	
			dd = "Not Invoiced"
		elif not rsc and rsi:	
			dd = "Not Delivered"
				# frappe.errprint(days)
		
			# frappe.errprint(dd)
			
		# rs_d_bold = f"<b>{rs_d}</b>" 
		# rsc_d_bold = f"<b>{rsc_d}</b>" 
		# rsi_d_bold = f"<b>{rsi_d}</b>"
		# dd_bold = f"<b>{dd}</b>" 

		# rsd = str(rs_d_bold)
		# rscd = str(rsc_d_bold)
		# rsid = str(rsi_d_bold)

		# # Convert string to datetime object
		# date_obj1 = datetime.strptime(rsd, "%Y-%m-%d")
		# date_obj2 = datetime.strptime(rscd, "%Y-%m-%d")
		# date_obj3 = datetime.strptime(rsid, "%Y-%m-%d")

		# # Convert datetime object to desired format
		# formatted_date1 = date_obj1.strftime("%d-%m-%Y")
		# formatted_date2 = date_obj2.strftime("%d-%m-%Y")
		# formatted_date3 = date_obj3.strftime("%d-%m-%Y")
		q_m = 0
		q_amt = frappe.db.sql(''' select `tabQuotation`.name as q_name,
		`tabQuotation`.default_discount_percentage as dis,
		`tabQuotation`.approval_date as a_date,
		`tabQuotation`.is_multiple_quotation as is_m,
		`tabQuotation`.after_discount_cost as adc,
		`tabQuotation Item`.unit_price as up,
		`tabQuotation Item`.margin_amount as ma 
		from `tabQuotation` 
		left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
		where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer") 
		and `tabQuotation Item`.wod_no = '%s' ''' %(i.name),as_dict=1)
		
		if q_amt:
			frappe.errprint(i.name)
			frappe.errprint(q_amt)
			for k in q_amt:
				if k.is_m == 1:
					
			# 		# per = (k.up * k.dis)/100
			# 		# q_amt = k.up - per
			# 		# # q_amt = k.ma
					q_m = k.ma

				else:
					# frappe.errprint(k.adc)
					q_m = k.adc

		row = [i.name,i.posting_date,q_m,rs_d,rsc_d,dn,check_re,rsi_d,si,ss,dd]
		data.append(row)
	return data

