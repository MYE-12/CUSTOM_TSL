
import frappe

def on_update(self, method):
	if self.workflow_state not in ["Rejected", "Rejected by Customer", "Approved", "Approved By Customer", "Cancelled"]:
		if self.quotation_type == "Internal Quotation":
			self.workflow_state = "Waiting For Approval"
		else:
			frappe.db.set_value(self.doctype, self.name, "workflow_state", "Quoted to Customer")

	if not self.quotation_type == "Internal Quotation":
		for i in self.items:
			if i.prevdoc_doctype == "Work Order Data" and i.prevdoc_docname:
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Quoted to Customer":
					frappe.db.set_value("Work Order Data", i.prevdoc_docname, "status", "Q-Quoted")
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Approved By Customer":
					frappe.db.set_value("Work Order Data", i.prevdoc_docname, "status", "A-Approved")
				if frappe.db.get_value(self.doctype, self.name, "workflow_state") == "Rejected by Customer":
					frappe.db.set_value("Work Order Data", i.prevdoc_docname, "status", "RNA-Return Not Approved")
