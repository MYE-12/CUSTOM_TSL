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
		_("SKU") + ":Link/Item:100",
		_("Model") + ":Data:100",
		_("Description") + ":Data:100",
		_("Item Group") + ":Data:100",
		_("Category") + ":Data:100",
		_("Sub category") + ":Data:100",
		_("Package") + ":Data:100",
		_("Avail Qty") + ":Data:100",
		_("Bin") + ":Data:100",
		
	]	
	return columns

def get_data(filters):
	data = []
	if filters.item:
		items = frappe.get_all("Item",{"name":filters.item},["*"])
	elif filters.item_group:
		items = frappe.get_all("Item",{"item_group":filters.item_group},["*"])

	elif filters.item_group and filters.item:
		items = frappe.get_all("Item",{"item_group":filters.item_group,"name":filters.item},["*"])
		
	else:
		items = frappe.get_all("Item",["*"])

	for i in items:
		
		stock = frappe.db.sql(""" select sum(actual_qty) as qty from `tabBin` where item_code = '%s'
        """ % (i.name),as_dict=True)[0]
		if not stock["qty"]:
			stock["qty"] = 0
		sc = frappe.get_value("Sub Category",{"name":i.sub_category},["sub_category"])
		row = [i.name,i.model_num,i.description,i.item_group,i.category_,sc,i.package,stock["qty"],i.bin]
		data.append(row)
	return data

	

		




