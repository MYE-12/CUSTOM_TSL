# Copyright (c) 2013, Tsl and contributors
# For license information, please see license.txt

from locale import currency
import frappe

# from pkgutil import get_data
from webbrowser import get
import frappe
from frappe.utils import fmt_money

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
	data = []
	data.append({"description":"","qty":"","buy_source":""})
	suppliers = frappe.db.sql('''select supplier,name,currency from `tabSupplier Quotation` where supply_order_data = %s''',filters.get('sod_no'),as_dict=1)
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
					i[j['supplier'].lower().replace(" ","_")] = fmt_money(k.rate,currency = j["currency"])
					i[j['supplier'].lower().replace(" ","_")+"1"] = fmt_money(k.amount,currency = j["currency"])
				else:
					i[j['supplier'].lower().replace(" ","_")] = fmt_money(0,currency = j["currency"])
					i[j['supplier'].lower().replace(" ","_")+"1"] = fmt_money(0,currency = j["currency"])

		data.append(i)
	d = {}
	for i in suppliers:
		doc = frappe.get_doc("Supplier Quotation",i['name'])
		d['description'] = "Supplier Total"
		d[i['supplier'].lower().replace(" ","_")] = fmt_money(doc.total,currency = i["currency"])
	data.append(d)
	ec = [{"description":"Supplier Quotation No"},{"description":"Freight Charges"},{"description":"Custom Clearance"},{"description":"Payment Commission"},{"description":"Max Freight Duration"},{"description":"Max Custom Duration"}]
	for i in ec:
		for j in suppliers:
			doc = frappe.get_doc("Supplier Quotation",j['name'])
			if i["description"] == "Supplier Quotation No":
				i[j['supplier'].lower().replace(" ","_")] = frappe.utils.get_link_to_form("Supplier Quotation",doc.name)
			if i["description"] == "Freight Charges":
				i[j['supplier'].lower().replace(" ","_")] =fmt_money(doc.freight_charges,currency = j["currency"])
			elif i["description"] == "Custom Clearance":
				i[j['supplier'].lower().replace(" ","_")] =fmt_money(doc.custom_clearance,currency = j["currency"])
			elif i["description"] == "Payment Commission":
				i[j['supplier'].lower().replace(" ","_")] =fmt_money(doc.payment_commission,currency = j["currency"])
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
		sum += float(doc.freight_charges)+float(doc.custom_clearance)+float(doc.payment_commission)
		gt[i['supplier'].lower().replace(" ","_")] = fmt_money(sum,currency = i["currency"])
	data.append(gt)

	return data

