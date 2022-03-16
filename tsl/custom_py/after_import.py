import frappe

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
