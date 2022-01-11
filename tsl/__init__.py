
__version__ = '0.0.1'
import frappe

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


