
import frappe

def on_update(self, method):
	if self.workflow_state not in ["Rejected", "Rejected by Customer", "Approved", "Approved By Customer", "Cancelled"]:
		if self.quotation_type == "Internal Quotation":
			self.workflow_state = "Waiting For Approval"
		else:
			frappe.db.set_value(self.doctype, self.name, "workflow_state", "Quoted to Customer")
