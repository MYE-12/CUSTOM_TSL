
import frappe
import json

@frappe.whitelist()
def get_wod_items(wod):
	wod = json.loads(wod)
	l=[]
	for k in list(wod):
		d = {}
		doc = frappe.get_doc("Work Order Data",k)
		for i in doc.get("material_list"):
			l.append(frappe._dict({
				"item" :i.item,
				"item_name" : i.item_name,
				"wod": k,
				"type": i.type,
				"model_no": i.model_no,
				"serial_no": i.serial_no,
				"qty": i.quantity,
				"sales_rep":doc.sales_rep

			}))
	return l

def on_update(self, method):
	if self.workflow_state not in ["Rejected", "Rejected by Customer", "Approved", "Approved By Customer", "Cancelled"]:
		if self.quotation_type == "Internal Quotation":
			self.workflow_state = "Waiting For Approval"
		else:
			frappe.db.set_value(self.doctype, self.name, "workflow_state", "Quoted to Customer")

	if not self.quotation_type == "Internal Quotation":
		for i in self.items:
			if i.prevdoc_doctype == "Work Order Data" and i.wod_no:
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Quoted to Customer":
					frappe.db.set_value("Work Order Data", i.wod_no, "status", "Q-Quoted")
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Customer":
					frappe.db.set_value("Work Order Data", i.wod_no, "status", "A-Approved")
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Rejected by Customer":
					frappe.db.set_value("Work Order Data", i.wod_no, "status", "RNA-Return Not Approved")

def before_submit(self,method):
	for i in self.get("items"):
		if i.wod_no:
			frappe.db.set_value("Work Order Data",i.wod_no,"is_quotation_created",1)


