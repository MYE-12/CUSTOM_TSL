# Copyright (c) 2013, Tsl and contributors
# For license information, please see license.txt

from pkgutil import get_data
import frappe

def execute(filters=None):
	data = []
	if filters.from_date and filters.to_date and filters.company:
		data = get_data(filters)
	columns = get_columns(filters)
	return columns, data


def get_columns(filters):
	columns = [
	{
		"fieldname":"wod_no",
		"label": "WOD",
		"fieldtype": "Link",
		"options" : "Work Order Data"
	},
	{
		"fieldname":"sales_rep",
		"label": "Sales Name",
		"fieldtype": "Link",
		"options" : "User"
	},
	{
		"fieldname":"posting_date",
		"label": "Date",
		"fieldtype": "Date",
	},
	{
		"fieldname":"company",
		"label": "Company Name",
		"fieldtype": "Link",
		"options" : "Company"
	},
	{
		"fieldname":"city",
		"label": "City",
		"fieldtype": "Data",
	},
	{
		"fieldname":"branch_name",
		"label": "Branch/Plant Name",
		"fieldtype": "Data",
	},
	{
		"fieldname":"type",
		"label": "Description",
		"fieldtype": "Data",
	},
	{
		"fieldname":"mfg",
		"label": "Mfg",
		"fieldtype": "Data",
	},
	{
		"fieldname":"model_no",
		"label": "Model",
		"fieldtype": "Data",
	},
	{
		"fieldname":"serial_no",
		"label": "Serial No",
		"fieldtype": "Data",
	},
	{
		"fieldname":"technician",
		"label": "Technician",
		"fieldtype": "Link",
		"options" : "User"
	},
	{
		"fieldname":"quantity",
		"label": "Qty",
		"fieldtype": "Float",
	},
	{
		"fieldname":"quoted_price",
		"label": "Quoted Price",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"price_after_dis",
		"label": "Price After Discount",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"tax",
		"label": "Tax(VAT)",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"Gross",
		"label": "grand_total",
		"fieldtype": "Currency",
	},
	{
		"fieldname":"status",
		"label": "Status",
		"fieldtype": "Data",
	},
	{
		"fieldname":"remarks",
		"label": "Remarks",
		"fieldtype": "Data",
	},
	]
	return columns
	
		
def get_data(filters):
	# work_order_entries = frappe.db.sql('''select name as wod_no,sales_rep,posting_date,remarks from `tabWork Order Data` where posting_date >= %s and posting_date <= %s''',(filters.from_date,filters.to_date),as_dict=1)
	data = []
	work_order_entries = frappe.db.sql('''select name as wod_no,sales_rep,posting_date,remarks from `tabWork Order Data`''',as_dict=1)
	print(work_order_entries)
	for i in work_order_entries:
		print(i.wod_no)
		
		data.append(i)

	return data
	