# Copyright (c) 2013, Tsl and contributors
# For license information, please see license.txt

# import frappe

# from pkgutil import get_data
from webbrowser import get
import frappe

def execute(filters=None):
	if filters.get("sod_no"):
		columns = get_columns(filters)
		data = get_data(filters)
		return columns, data

def get_columns(filters):
	columns = [
		{
			"fieldname":"description",
			"label": "Material Description",
			"fieldtype": "Data",
		},
		{
			"fieldname":"qty",
			"label": "Qty",
			"fieldtype": "Float",
		},
		{
			"fieldname":"buy_source",
			"label": "Planned Actual Buying Source",
			"fieldtype": "Data",
		},
	]
	suppliers = frappe.db.sql('''select supplier from `tabSupplier Quotation` where supply_order_data = %s''',filters.get('sod_no'),as_list=1)
	print("\n\n\n\n")
	print(suppliers)
	for i in suppliers:
		s = i[0].lower().replace(" ","_")
		columns.append({
			"fieldname":s,
			"label": i[0],
			"fieldtype": "Data",
			
			"width":170
		})
		columns.append({
			"fieldname":s+"1",
			"label": i[0],
			"fieldtype": "Data",
			
			"width":170
		})
	return columns

def get_data(filters):
	print("\n\n\nget_data\n")
	data = []
	data.append({"description":"","qty":"","buy_source":""})
	suppliers = frappe.db.sql('''select supplier,name from `tabSupplier Quotation` where supply_order_data = %s''',filters.get('sod_no'),as_dict=1)
	for i in suppliers:
		s = i['supplier'].lower().replace(" ","_")
		data[0][s] = "Unit Price"
		data[0][s+"1"] = "Total Price"
	item = []
	for i in suppliers:
		doc = frappe.get_doc("Supplier Quotation",i['name'])
		for j in doc.get("items"):
			if {"description":j.item_name,"qty":j.qty} not in item:
				item.append({"description":j.item_name,"qty":j.qty})
	for i in item:
		for j in suppliers:
			doc = frappe.get_doc("Supplier Quotation",j['name'])
			for k in doc.get("items"):
				if i["description"] == k.item_name:
					i[j['supplier'].lower().replace(" ","_")] = str(k.rate) 
					i[j['supplier'].lower().replace(" ","_")+"1"] = str(k.amount)
		data.append(i)
	d = {}
	for i in suppliers:
		doc = frappe.get_doc("Supplier Quotation",i['name'])
		d['description'] = "Supplier Total"
		d[i['supplier'].lower().replace(" ","_")] = str(doc.total)
	data.append(d)
	ec = [{"description":"Supplier Quotation No"},{"description":"Freight Charges"},{"description":"Custom Clearance"},{"description":"Payment Commission"},{"description":"Max Freight Duration"},{"description":"Max Custom Duration"}]
	for i in ec:
		for j in suppliers:
			doc = frappe.get_doc("Supplier Quotation",j['name'])
			if i["description"] == "Supplier Quotation No":
				i[j['supplier'].lower().replace(" ","_")] = doc.name
			for k in doc.get("extra_charges"):
				if i['description'] == k.type:
					i[j['supplier'].lower().replace(" ","_")] =str(k.amount)
				elif i["description"] == "Max Freight Duration":
					i[j['supplier'].lower().replace(" ","_")] = doc.max_freight_duration
				elif i["description"] == "Max Custom Duration":
					i[j['supplier'].lower().replace(" ","_")] = doc.max_custom_duration
				
		data.append(i)
	data.append({})
	gt = {}
	for i in suppliers:
		doc = frappe.get_doc("Supplier Quotation",i['name'])
		gt['description'] = "Grand Total"
		sum = 0
		sum += doc.total
		for j in doc.get("extra_charges"):
			sum += float(j.amount)
		gt[i['supplier'].lower().replace(" ","_")] = str(sum)
	data.append(gt)

	return data

