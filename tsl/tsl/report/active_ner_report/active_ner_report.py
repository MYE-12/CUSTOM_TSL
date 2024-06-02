# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta

def execute(filters=None):
	columns=get_columns(filters)
	data = get_data(filters) 
	return columns, data

def get_columns(filters):

	columns = [
		_("Work Order") + ":Link/Work Order Data:140",
		_("NER") + ":Data:150",
		_("Status") + ":Data:150",
	
		
	]	
	return columns

def get_data(filters):
	data = []
	w = frappe.get_all("Work Order Data",["*"])
	for i in w:
		if i.status_cap:
			if i.status == "WP-Waiting Parts" or i.status == "C-Comparison" or i.status == "TR-Technician Repair" or i.status == "UTR-Under Technician Repair" or i.status == "AP-Available Parts" or i.status == "NER-Need Evaluation Return":
				row = [i.name,"NER-Need Evaluation Return",i.status]
				data.append(row) 
	return data

	





