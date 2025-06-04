# Copyright (c) 2023, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WorkOrderDataLookup(Document):
	pass
@frappe.whitelist()
def get_wod_for_tool(doc):
    wod_data = frappe.get_doc("Work Order Data", doc)
    
    # Initialize the result structure
    result = {
        "material_list": wod_data.material_list,
        "items": []
    }

    # Check if Initial Evaluation exists
    initial_eval_name = frappe.db.exists("Initial Evaluation", {'work_order_data': doc})
    if initial_eval_name:
        eval_doc = frappe.get_doc("Initial Evaluation", initial_eval_name)
        result["items"] = eval_doc.items  # Assuming it has a child table named 'items'
    else:
        final_eval = frappe.db.exists("Evaluation Report", {'work_order_data': doc})
        if final_eval:
            eval_doc = frappe.get_doc("Evaluation Report", final_eval)
            result["items"] = eval_doc.items

    return result