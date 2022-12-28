from pydoc import doc
import frappe
from erpnext.accounts.party import get_party_account_currency, get_party_details
from erpnext.stock.doctype.material_request.material_request import set_missing_values
from frappe.model.mapper import get_mapped_doc
import json

@frappe.whitelist()
def reject_other_sq(sq,sod = None,wod = None):
    if sod:
        frappe.db.sql('''update `tabSupplier Quotation` set workflow_state = "Rejected" where supply_order_data = %s and docstatus = 0 and workflow_state = "Waiting For Approval" ''',sod)
        frappe.db.commit()
        return True
    if wod:
        frappe.db.sql('''update `tabSupplier Quotation` set workflow_state = "Rejected" where work_order_data = %s and docstatus = 0 and workflow_state = "Waiting For Approval" ''',wod)
        frappe.db.commit()
        return True

@frappe.whitelist()
def item_allocate_to_supplier(sod):
    order = ""
    new_doc = frappe.new_doc("Item Allocation")
    new_doc.order_by = "Supplier"
    if new_doc.order_by == "Supplier":
        order += "order by s.creation desc"
    elif new_doc.order_by == "Item":
        order += "order by si.item_name"
    sqtn = frappe.db.sql('''select s.supplier as supplier_name,s.name as supplier_quotation,si.item_code as sku,si.item_name as item_name,si.rate as price,si.qty as qty,si.amount as amount from `tabSupplier Quotation` as s inner join `tabSupplier Quotation Item` as si on si.parent = s.name where s.supply_order_data = %s and s.docstatus = 0 and s.workflow_state = "Waiting For Approval" {0}'''.format(order),sod,as_dict= 1)
    new_doc.supply_order_data = sod
    for i in sqtn:
        new_doc.append("items",i)
    new_doc.save(ignore_permissions = True)
    return new_doc

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
                    "parent": "request_for_quotation",
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
        doc = frappe.get_doc("Evaluation Report",self.part_sheet)
        for i in self.get("items"):
            for j in doc.get("items"):
                if j.part == i.item_code:
                    j.price_ea = i.rate
                    j.total = i.rate * j.qty
        add = 0
        for i in doc.items:
            add += j.total
        doc.total_amount = add

        doc.save(ignore_permissions=True)
