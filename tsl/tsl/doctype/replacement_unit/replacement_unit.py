# Copyright (c) 2025, Tsl and contributors
# For license information, please see license.txt

from codecs import ignore_errors
from hashlib import new
from pydoc import doc
from types import new_class
import frappe
import json
from frappe.model.document import Document
from frappe.utils import getdate,today
from datetime import datetime,date
from frappe.utils.data import (
	add_days,
	add_months,
	add_to_date,
	date_diff,
	flt,
	get_date_str,
	nowdate,
)


class ReplacementUnit(Document):
	def on_update_after_submit(self):
		if self.status != self.status_duration_details[-1].status:
			ldate = self.status_duration_details[-1].date
			
			now = datetime.now()
			
			time_date = str(ldate).split(".")[0]
			format_data = "%Y-%m-%d %H:%M:%S"
			date = datetime.strptime(time_date, format_data)
			duration = now - date
			duration_in_s = duration.total_seconds()
			minutes = divmod(duration_in_s, 60)[0]/60
			data = str(minutes).split(".")[0]+"hrs "+str(minutes).split(".")[1][:2]+"min"

			frappe.db.set_value("Status Duration Details",self.status_duration_details[-1].name,"duration",data)
			self.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})

			doc = frappe.get_doc("Work Order Data",self.name)

			doc.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
			doc.save(ignore_permissions=True)

	def before_submit(self):
		self.status = "Inquiry"
		now = datetime.now()
		self.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
	
		if self.status != self.status_duration_details[-1].status:
			ldate = self.status_duration_details[-1].date
			now = datetime.now()
			time_date = str(ldate).split(".")[0]
			format_data = "%Y-%m-%d %H:%M:%S"
			date = datetime.strptime(time_date, format_data)
			duration = now - date
			duration_in_s = duration.total_seconds()
			minutes = divmod(duration_in_s, 60)[0]/60
			data = str(minutes).split(".")[0]+"hrs "+str(minutes).split(".")[1][:2]+"min"
			self.status_duration_details[-1].duration = data
			# doc = frappe.get_doc("Work Order Data",self.name)
			self.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})


@frappe.whitelist()
def create_rfq(docname):
	doc = frappe.get_doc("Replacement Unit",docname)
	new_doc = frappe.new_doc("Request for Quotation")
	new_doc.company = doc.company
	new_doc.branch = doc.branch
	new_doc.schedule_date = today()
	new_doc.custom_replacement_unit = docname
	new_doc.department = doc.department
	new_doc.items=[]
	if doc.company == "TSL COMPANY - KSA":
		new_doc.naming_series = "RFQ-SA-.YY.-"
	warehouse = new_doc.branch
	if new_doc.branch == "Dammam - TSL-SA":
		warehouse = "Dammam - TSL - KSA"
	if new_doc.branch == "Jeddah - TSL-SA":
		warehouse = "Jeddah - TSL - KSA"
	if new_doc.branch == "Riyadh - TSL- KSA":
		warehouse = "Riyadh - TSL - KSA"
		
	for i in doc.get("material_list"):
		new_doc.append("items",{
			"item_code":i.item_code,
			'model':i.model_no,
			"uom":"Nos",
			"stock_uom":"Nos",
			"conversion_factor":1,
			"stock_qty":1,
			"qty":1,
			"work_order_data":docname,
			# "schedule_date":add_to_date(new_doc.transaction_date,days = 2),
			"schedule_date":today(),
			"warehouse":warehouse,
			"branch":new_doc.branch,
			"department":doc.department        
		})
	return new_doc