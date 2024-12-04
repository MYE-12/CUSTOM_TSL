# Copyright (c) 2013, Tsl and contributors
# For license information, please see license.txt

from locale import currency
import frappe

# from pkgutil import get_data
from webbrowser import get
import frappe
from frappe.utils import fmt_money

def execute(filters=None):
	columns,data = [],[]
	if filters.get("sod_no") or filters.get("wod_no"):
		columns = get_columns(filters)
		data = get_data(filters)
	return columns, data

def get_columns(filters=None):
	columns = [
		{
			"fieldname":"description",
			"label": frappe.bold("Material Description"),
			"fieldtype": "Data",
		},
		{
			"fieldname":"qty",
			"label": frappe.bold("Qty"),
			"fieldtype": "Float",
		},
		# {
		# 	"fieldname":"buy_source",
		# 	"label": frappe.bold("Planned Actual Buying Source"),
		# 	"fieldtype": "Data",
		# },
	]
	if filters.get("sod_no"):
		suppliers = frappe.db.sql('''select supplier from `tabSupplier Quotation` where supply_order_data = %s and docstatus != 2''',filters.get('sod_no'),as_list=1)
	elif filters.get("wod_no"):
		suppliers = frappe.db.sql('''select supplier from `tabSupplier Quotation` where work_order_data = %s and docstatus != 2''',filters.get('wod_no'),as_list=1)
	for i in suppliers:
		s = i[0].lower().replace(" ","_")
		columns.append({
			"fieldname":s,
			"label":"<b>Supplier</b>"+":"+frappe.bold(i[0]),
			"fieldtype": "Data",
			"width":170
		})
		columns.append({
			"fieldname":s+"1",
			"label": "",
			"fieldtype": "Data",
			"width":170
		})
	return columns

def get_data(filters=None):
	data = []
	# data.append({"description":"","qty":"","buy_source":""})
	data.append({"description":"","qty":""})
	if filters.get("sod_no"):
		suppliers = frappe.db.sql('''select quotation,supplier,name,currency from `tabSupplier Quotation` where supply_order_data = %s and docstatus != 2''',filters.get('sod_no'),as_dict=1)
	elif filters.get("wod_no"):
		suppliers = frappe.db.sql('''select quotation,supplier,name,currency from `tabSupplier Quotation` where work_order_data = %s and docstatus != 2''',filters.get('wod_no'),as_dict=1)
	for i in suppliers:
		s = i['supplier'].lower().replace(" ","_")
		data[0][s] = frappe.bold("Unit Price")
		data[0][s+"1"] = frappe.bold("Total Price")
	item = []
	for i in suppliers:
		doc = frappe.get_doc("Supplier Quotation",i['name'])
		for j in doc.get("items"):
			if {"item_code":j.item_code,"description":j.item_name,"qty":j.qty} not in item:
				item.append({"item_code":j.item_code,"description":j.item_name,"qty":j.qty})
	for i in item:
		print(i)
		for j in suppliers:
			print(j)
			doc = frappe.get_doc("Supplier Quotation",j['name'])
			for k in doc.get("items"):
				if i["item_code"] == k.item_code:
					print(k.item_code)
					print(k.rate,k.amount)

					i[j['supplier'].lower().replace(" ","_")] = fmt_money(k.rate,currency = j["currency"])
					i[j['supplier'].lower().replace(" ","_")+"1"] = fmt_money(k.amount,currency = j["currency"])
				# else:
				# 	i[j['supplier'].lower().replace(" ","_")] = fmt_money(0,currency = j["currency"])
				# 	i[j['supplier'].lower().replace(" ","_")+"1"] = fmt_money(0,currency = j["currency"])
		data.append(i)
	d = {}
	for i in suppliers:
		doc = frappe.get_doc("Supplier Quotation",i['name'])
		d['description'] = frappe.bold("Supplier Total")
		d[i['supplier'].lower().replace(" ","_")] = fmt_money(doc.total,currency = i["currency"])
	data.append(d)
	ec = [{"description":frappe.bold("Supplier Quotation No")},{"description":frappe.bold("Freight Charges")},{"description":frappe.bold("Custom Clearance")},{"description":frappe.bold("Payment Commission")},{"description":frappe.bold("Max Freight Duration")},{"description":frappe.bold("Max Custom Duration")}]
	for i in ec:
		for j in suppliers:
			doc = frappe.get_doc("Supplier Quotation",j['name'])
			if i["description"] == frappe.bold("Supplier Quotation No"):
				i[j['supplier'].lower().replace(" ","_")] = frappe.bold(frappe.utils.get_link_to_form("Supplier Quotation",doc.name))
			if i["description"] == frappe.bold("Freight Charges"):
				i[j['supplier'].lower().replace(" ","_")] =fmt_money(doc.freight_charges,currency = j["currency"])
			elif i["description"] == frappe.bold("Custom Clearance"):
				i[j['supplier'].lower().replace(" ","_")] =fmt_money(doc.custom_clearance,currency = j["currency"])
			elif i["description"] == frappe.bold("Payment Commission"):
				i[j['supplier'].lower().replace(" ","_")] =fmt_money(doc.payment_commission,currency = j["currency"])
			elif i["description"] == frappe.bold("Max Freight Duration"):
				i[j['supplier'].lower().replace(" ","_")] = doc.max_freight_duration
			elif i["description"] == frappe.bold("Max Custom Duration"):
				i[j['supplier'].lower().replace(" ","_")] = doc.max_custom_duration
		data.append(i)
	data.append({})
	gt = {}
	for i in suppliers:
		doc = frappe.get_doc("Supplier Quotation",i['name'])
		gt['description'] = frappe.bold("Grand Total")
		sum = 0
		sum += doc.total
		sum += float(doc.freight_charges)+float(doc.custom_clearance)+float(doc.payment_commission)
		gt[i['supplier'].lower().replace(" ","_")] = frappe.bold(fmt_money(sum,currency = i["currency"]))
	data.append(gt)
	# frappe.errprint(data)
	return data

