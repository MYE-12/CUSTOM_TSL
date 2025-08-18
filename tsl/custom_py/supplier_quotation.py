from pydoc import doc
import frappe
from erpnext.accounts.party import get_party_account_currency, get_party_details
from erpnext.stock.doctype.material_request.material_request import set_missing_values
from frappe.model.mapper import get_mapped_doc
import json
import requests
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
    # if frappe.db.get_value("Supplier Quotation",{"work_order_data":doc.work_order_data}):
    #     frappe.throw("Supplier Quotations already created for this RFQ")
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


def validate(self,method):
    for i in self.items:
        if i.work_order_data:
            doc = frappe.db.sql("""select name,status,work_order_data from `tabEvaluation Report` where work_order_data = '%s' and docstatus != 2 and status not in ('Return Not Repaired', 'RNP-Return no Parts', 'Return No Fault')"""%(i.work_order_data),as_dict=1)
        
            for d in doc:
                ev = frappe.get_doc("Evaluation Report",d.name)
                if d.status != "Comparison":
                    ev.status = "Supplier Quoted"
                    ev.save()
    
    # if self.company == "TSL COMPANY - Kuwait" or self.company == "TSL COMPANY - KSA":
    #     if self.work_order_data:
    #         ev = frappe.db.sql(""" select `tabPart Sheet Item`.part as p, `tabPart Sheet Item`.parts_availability as pa from `tabEvaluation Report` left join
    #         `tabPart Sheet Item` on  `tabEvaluation Report`.name =  `tabPart Sheet Item`.parent 
    #         where `tabEvaluation Report`.work_order_data = '%s' """%(self.work_order_data),as_dict=1)
    #         ev_list = []
    #         for e in ev:
    #             if e['pa'] == "No":
    #                 ev_list.append(e['p'])

    #         count = 0

    #         sq = frappe.get_all("Supplier Quotation",{"work_order_data":self.work_order_data,"workflow_state":"Approved by Management"})
    #         if sq:
                
    #             for d in sq:
    #                 sup = frappe.db.sql(""" select `tabSupplier Quotation Item`.item_code as ic from `tabSupplier Quotation` left join
    #                 `tabSupplier Quotation Item` on  `tabSupplier Quotation`.name =  `tabSupplier Quotation Item`.parent 
    #                 where `tabSupplier Quotation`.name = '%s' """%(d["name"]),as_dict=1)
    #                 for k in sup:
    #                     if k["ic"] in ev_list:
    #                         count = count + 1

    #         for j in self.items:
    #             if j.item_code in ev_list:
    #                 count = count + 1
                        
    #         # if count == len(ev_list):
    #         #     frappe.errprint("yessss")
    #         #     ev = frappe.get_doc("Work Order Data",self.work_order_data)
    #         #     ev.status = "Parts Priced"
    #         #     ev.save(ignore_permissions =1)

    #             # doc = frappe.db.sql("""select name from `tabWork Order Data` where name = '%s' """%(self.work_order_data),as_dict=1)
    #             # for d in doc:
               
    
        

def on_submit(self,method):
    if self.get("custom_replacement_unit"):
        frappe.db.set_value("Replacement Unit",self.get("custom_replacement_unit"),"status", "Parts Priced", update_modified = False)
    
    if self.project_data:
        pd = frappe.get_doc("Project Data",self.project_data)
        pd.status = "Parts Priced"
        pd.save()

    if not self.department == "Supply Tender - TSL":
        for i in self.items:
            if self.company == "TSL COMPANY - UAE" or self.company == "TSL COMPANY - Kuwait" or self.company == "TSL COMPANY - KSA":
                if i.work_order_data and not self.get("custom_replacement_unit"):
                    doc = frappe.db.sql("""select name from `tabWork Order Data` where name = '%s' """%(i.work_order_data),as_dict=1)
                    for d in doc:
                        ev = frappe.get_doc("Work Order Data",d.name)
                        
                        ev.status = "Parts Priced"
                        ev.save(ignore_permissions =1)
            
            
            if i.supply_order_data or self.supply_order_data:
                doc = frappe.db.sql("""select name from `tabSupply Order Data` where name = '%s' """%(i.supply_order_data or self.supply_order_data),as_dict=1)
                for d in doc:
                    ev = frappe.get_doc("Supply Order Data",d.name)
                    ev.status = "Parts Priced"
                    ev.save(ignore_permissions =1)
            


        if (self.part_sheet and self.initial_evaluation):
            items = self.get("items")
            for it in items:
                ie = frappe.get_doc("Initial Evaluation",it.initial_evaluation)
                for i in self.get('items'):
                    url = "https://api.exchangerate.host/%s"%(self.currency)
                    payload = {}
                    headers = {}
                    response = requests.request("GET", url, headers=headers, data=payload)
                    data = response.json()
                    rate_kw = data['rates']['KWD']
                    conv_rate = i.rate * rate_kw
                    for j in ie.get("items"):
                        if j.part == i.item_code:
                            j.price_ea = conv_rate
                            j.total = conv_rate * j.qty
                add = 0
                for i in ie.items:
                    add += j.total
                ie.total_amount = add

                ie.save(ignore_permissions=True)


        if self.work_order_data:
            evl = frappe.get_value("Evaluation Report",{"Work_order_data":self.work_order_data})
            frappe.errprint(evl)
            if evl:
                doc = frappe.get_doc("Evaluation Report",evl)
                for i in self.get("items"):
                    # url = "https://api.exchangerate.host/%s"%(self.currency)
                    url = "https://api.exchangerate-api.com/v4/latest/%s"%(self.currency)

                    payload = {}
                    headers = {}
                    response = requests.request("GET", url, headers=headers, data=payload)
                    data = response.json()
                    com_cur = frappe.get_value("Company",self.company,"default_currency")
                    rate_kw = data['rates'][com_cur]
                    conv_rate = i.rate * rate_kw
                    for j in doc.get("items"):
                        if j.part == i.item_code:
                            j.price_ea = conv_rate
                            j.total = conv_rate * j.qty
                add = 0
                for i in doc.items:
                    add += j.total
                doc.total_amount = add

                doc.save(ignore_permissions=True)
        if not self.work_order_data and not self.supply_order_data:
            for i in self.get("items"):
                wod = i.work_order_data

                evl = frappe.get_value("Evaluation Report",{"Work_order_data":wod})

                doc = frappe.get_doc("Evaluation Report",evl)
                url = "https://api.exchangerate-api.com/v4/latest/%s"%(self.currency)

                payload = {}
                headers = {}
                response = requests.request("GET", url, headers=headers, data=payload)
                data = response.json()
                com_cur = frappe.get_value("Company",self.company,"default_currency")
                rate_kw = data['rates'][com_cur]
                conv_rate = i.rate * rate_kw
                for j in doc.get("items"):
                    if j.part == i.item_code:
                        j.price_ea = conv_rate
                        j.total = conv_rate * j.qty
                add = 0
                for i in doc.items:
                    add += j.total
                doc.total_amount = add

                doc.save(ignore_permissions=True)

            for i in self.get("items"):
                if self.custom_replacement_unit:
                    doc = frappe.get_doc("Work Order Data",wod)
                    url = "https://api.exchangerate-api.com/v4/latest/%s"%(self.currency)

                    payload = {}
                    headers = {}
                    response = requests.request("GET", url, headers=headers, data=payload)
                    data = response.json()
                    com_cur = frappe.get_value("Company",self.company,"default_currency")
                    rate_kw = data['rates'][com_cur]
                    conv_rate = i.rate * rate_kw
                    for j in doc.get("material_list"):
                        if j.item_code == i.item_code:
                            j.price = float(conv_rate)
                            j.amount = float(conv_rate) * float(j.quantity)
                    doc.save(ignore_permissions=True)
                    
        elif self.initial_evaluation:
            doc = frappe.get_doc("Initial Evaluation",self.initial_evaluation)
            
            for i in self.get("items"):
                url = "https://api.exchangerate-api.com/v4/latest/%s"%(self.currency)
                payload = {}
                headers = {}
                response = requests.request("GET", url, headers=headers, data=payload)
                data = response.json()
                frappe.errprint(data)
                rate_kw = data['rates']['KWD']
                conv_rate = i.rate * rate_kw
                for j in doc.get("items"):
                    if j.part == i.item_code:
                        j.price_ea = conv_rate
                        j.total = conv_rate * j.qty
            add = 0
            for i in doc.items:
                add += j.total
            doc.total_amount = add

            doc.save(ignore_permissions=True)

    #Supplier quotation supply order rate conversion

        if self.supply_order_data and self.company == "TSL COMPANY - UAE":
            doc = frappe.get_doc("Supply Order Data",self.supply_order_data)
            for i in self.get('items'):
                for j in doc.get("in_stock"):
                    if i.item_code == j.part:
                        j.price_ea = i.rate
                        j.total = i.rate * j.qty
                        j.supplier_quotation = self.name
                for j in doc.get('material_list'):
                    if j.item_code == i.item_code:
                        # rate_kw = data['rates']['KWD']
                        # conv_rate = i.rate * rate_kw
                        j.price = i.rate     
                        j.amount = i.rate * float(j.quantity)
                        j.supplier_quotation = self.name
            doc.save(ignore_permissions=True)
        
        if self.supply_order_data and self.company == "TSL COMPANY - Kuwait":
            doc = frappe.get_doc("Supply Order Data",self.supply_order_data)
            for i in self.get('items'):
                for j in doc.get("in_stock"):
                    if i.item_code == j.part:
                        j.price_ea = i.rate
                        j.total = i.rate * j.qty
                        j.supplier_quotation = self.name
                for j in doc.get('material_list'):
                    if j.item_code == i.item_code:
                        url = "https://api.exchangerate-api.com/v4/latest/%s"%(self.currency)
                        payload = {}
                        headers = {}
                        response = requests.request("GET", url, headers=headers, data=payload)
                        data = response.json()
                    
                        rate_kw = data['rates']['KWD']
                        conv_rate = i.rate * rate_kw
                        j.price = conv_rate      
                        j.amount = conv_rate * float(j.quantity)
                        j.supplier_quotation = self.name
            doc.save(ignore_permissions=True)


