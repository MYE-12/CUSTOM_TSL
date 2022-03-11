from pydoc import doc
import frappe
from erpnext.accounts.party import get_party_account_currency, get_party_details
from erpnext.stock.doctype.material_request.material_request import set_missing_values
from frappe.model.mapper import get_mapped_doc
import json

@frappe.whitelist()
def reject_other_sq(sq,sod):
    frappe.db.sql('''update `tabSupplier Quotation` set workflow_state = "Rejected" where supply_order_data = %s and docstatus = 0 and workflow_state = "Waiting For Approval" ''',sod)
    frappe.db.commit()
    return True
    
@frappe.whitelist()
def make_supplier_quotation_from_rfq(source_name, target_doc=None, for_supplier=None):
    doc = frappe.get_doc("Request for Quotation",source_name)
    l = []
    for i in doc.get("suppliers"):
        def postprocess(source, target_doc):
            if i.supplier:
                target_doc.supplier = i.supplier
                args = get_party_details(i.supplier, party_type="Supplier", ignore_permissions=True)
                target_doc.currency = args.currency or get_party_account_currency('Supplier', i.supplier, source.company)
                target_doc.buying_price_list = args.buying_price_list or frappe.db.get_value('Buying Settings', None, 'buying_price_list')
            set_missing_values(source, target_doc)

        doclist = get_mapped_doc("Request for Quotation", source_name, {
            "Request for Quotation": {
                "doctype": "Supplier Quotation",
                "validation": {
                    "docstatus": ["=", 1]
                }
            },
            "Request for Quotation Item": {
                "doctype": "Supplier Quotation Item",
                "field_map": {
                    "name": "request_for_quotation_item",
                    "parent": "request_for_quotation"
                },
            }
        }, target_doc, postprocess)
        doclist.save()
        l.append(doclist.name)
    if l:
        link = []
        for i in l:
            link.append(""" <a href='/app/supplier-quotation/{0}'>{0}</a> """.format(i))
        frappe.msgprint("Supplier Quotation created for each Supplier: "+', '.join(link))
        return True

def on_submit(self,method):
    if self.part_sheet:
        add = 0
        doc = frappe.get_doc("Evaluation Report",self.part_sheet)
        for i in self.get("items"):
            for j in doc.get("items"):
                if j.part == i.item_code:
                    j.price_ea = i.rate
                    j.total = i.rate * j.qty
                    add += float(j.total)
        doc.total_amount += add
        doc.save(ignore_permissions=True)

    if self.supply_order_data:
        doc = frappe.get_doc("Supply Order Data",self.supply_order_data)
        for i in self.get("items"):
            for j in doc.get("in_stock"):
                if j.part == i.item_code:
                    j.price_ea = i.rate
                    j.total = i.rate * j.qty
            for j in doc.get("material_list"):
                if j.item_name == i.item_name:
                    j.price = i.rate
                    j.amount = float(i.rate) * float(j.quantity)
        doc.save(ignore_permissions=True)

