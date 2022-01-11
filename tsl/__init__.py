
__version__ = '0.0.1'
import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_workorder_data(order_no):
	l=[]
	if frappe.db.exists("Work Order Data",{"reference_doctype":order_no}):
		frappe.throw("Order Already Created")
	doc = frappe.get_doc("Equipment Received Form",order_no)
	for i in doc.get("received_equipment"):
		new_doc = frappe.new_doc("Work Order Data")
		new_doc.customer = doc.customer
		new_doc.quoted_date = doc.date
		new_doc.sales_rep = doc.incharge
		new_doc.equipment_recieved_form = doc.name
		new_doc.append("material_list",{
			"item":i.item,
			"mfg":i.manufacturer,
			"serial_no":i.serial_no,
			"quantity":i.qty
		})
		new_doc.save(ignore_permissions = True)
		l.append(new_doc.name)
	if l:
		return True
	return False

<<<<<<< HEAD
@frappe.whitelist()
def get_work_order_data(source_name, target_doc=None):
	print("\n\n\n\nget work called\n\n\n\n")
	doclist = get_mapped_doc("Work Order Data", source_name, {
		"Work Order Data": {
			"doctype": "Quotation",
			"field_map": {
				
				"name": "enq_no",
			}
		},
		"Material List": {
			"doctype": "Quotation Item",
			"field_map": {
				"parent": "prevdoc_docname",
				"parenttype": "prevdoc_doctype",
				"item":"item_code",
				"type":"description",
				"quantity":"qty",
			},
			"add_if_empty": True
		}
	}, target_doc)

	return doclist
	
=======

>>>>>>> 9f605024606e7edd18cec1d274876f8ec2ba9b89
