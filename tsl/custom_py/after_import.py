import frappe,json
from frappe.desk.form.utils import get_pdf_link


@frappe.whitelist()
def get_items_from_ps(wod):
    wod = json.loads(wod)
    l = []
    for i in list(wod):
        er =  frappe.db.sql('''select name from `tabEvaluation Report` where docstatus = 1 and work_order_data = %s and parts_availability = "No" ''',i,as_dict=1)
        ie =  frappe.db.sql('''select name from `tabInitial Evaluation` where docstatus = 0 and work_order_data = %s and parts_availability = "No" ''',i,as_dict=1)
      
        for j in er:
            doc = frappe.get_doc("Evaluation Report",j['name'])
            for k in doc.items:
                if k.parts_availability == "No":
                    d = frappe._dict((k.as_dict()))
                    d["wod"] = i
                    d["part_sheet"] = j["name"]
                    l.append(d)
                    frappe.errprint(l)
        for j in ie:
            doc = frappe.get_doc("Initial Evaluation",j['name'])
            for k in doc.items:
                if k.parts_availability == "No":
                    d = frappe._dict((k.as_dict()))
                    d["wod"] = i
                    d["part_sheet"] = j["name"]
                    l.append(d)
    return l

@frappe.whitelist()
def get_items_from_sod(sod):
    sod = json.loads(sod)
    l=[]
    for i in list(sod):
        doc = frappe.get_doc("Supply Order Data",i)
        for j in doc.in_stock:
            if j.parts_availability == "No":
                d = frappe._dict(j.as_dict())
                d['sod'] = i
                d['dept'] = doc.department
                l.append(d)
        for j in doc.material_list:
            d = frappe._dict(j.as_dict())
            d['sod'] = i
            d['dept'] = doc.department
            l.append(d)
    return l
        
def create_after_import():
    for i in ['cr_copy','vat_certificate','bank_details','address']:
        l = frappe.db.sql('''select name,{0} from `tabCustomer` where {0} is not null '''.format(i),as_dict = 1)
        for j in l:
            if not frappe.db.sql('''select name from `tabFile` where attached_to_doctype = "Customer" and attached_to_field = %s and attached_to_name = %s and file_url = %s ''',(i,j['name'],j[i])):
                doc = frappe.new_doc("File")
                doc.file_name = j[i].split('/')[-1]
                doc.file_url = j[i]
                doc.attached_to_doctype = 'Customer'
                doc.attached_to_name = j['name']
                doc.attached_to_field = i
                doc.save(ignore_permissions = True)

from frappe.www.printview import get_rendered_template
from frappe.utils.pdf import get_pdf

@frappe.whitelist()
def send_mail(branch,name,doctype,msg):
    receivers = []
    sender = frappe.db.get_value("Email Account",{"branch":branch},"email_id")
    doc = frappe.get_doc(doctype,name)
    receivers = ["frankel9675@gmail.com"]
   # for i in doc.get('suppliers'):
    #    if i.email_id:
     #       receivers.append(i.email_id)
    msg = "<br><br><br>To View Quotation<a href='https://tsl.ribox.me{0}'>Click Here</a>".format(get_pdf_link(doctype,name,"Quotation TSL",0))
    if receivers:
        try:
            frappe.sendmail(
                recipients = receivers,
                sender = sender,
                subject = str(doctype)+" "+str(name),
                message = msg,
                attachments= get_attachments(name , doctype),
                print_letterhead = 1,
                unsubscribe_params = "https://tsl.ribox.me"+get_pdf_link(doctype,name,"Quotation TSL",0),
                add_unsubscribe_link = 1
            )
            frappe.msgprint("Email sent")
        except frappe.OutgoingEmailError as e:
            frappe.msgprint(str(e))

import os,pdfkit
def create_pdf(name, str_html):
        path = os.getcwd()+frappe.utils.get_site_base_path()[1:]+"/public/files/"+name+".pdf"
        pdfkit.from_string(str_html, path)
        return path

def get_attachments(name,doctype):
    attachments = frappe.attach_print(doctype, name,file_name=doctype, print_format="Quotation TSL",print_letterhead = True)
#    attachments = get_pdf_link(doctype,name,"Quotation TSL",0)
    return [attachments]

@frappe.whitelist()
def get_items_from_purchase_receipts(self):
    self.set("items", [])
    for pr in self.get("purchase_receipts"):
        if pr.receipt_document_type and pr.receipt_document:
            pr_items = frappe.db.sql("""select pr_item.item_code, pr_item.description,
                pr_item.qty, pr_item.base_rate, pr_item.base_amount, pr_item.name,
                pr_item.cost_center, pr_item.is_fixed_asset
                from `tab{doctype} Item` pr_item where parent = %s
                and exists(select name from tabItem
                    where name = pr_item.item_code and (is_stock_item = 1 or is_fixed_asset=1))
                """.format(doctype=pr.receipt_document_type), pr.receipt_document, as_dict=True)

            for d in pr_items:
                item = self.append("items")
                item.item_code = d.item_code
                item.description = d.description
                item.qty = d.qty
                item.rate = d.base_rate
                item.cost_center = d.cost_center or \
                    erpnext.get_default_cost_center(self.company)
                item.amount = d.base_amount
                item.receipt_document_type = pr.receipt_document_type
                item.receipt_document = pr.receipt_document
                item.purchase_receipt_item = d.name
                item.is_fixed_asset = d.is_fixed_asset
