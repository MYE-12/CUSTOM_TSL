from gettext import find
import frappe
from frappe.utils import datetime,now,today

def before_save(self,method):
    customer = []
    supplier= []
    if self.email_id_or_address:
        self.email_ids = []
        self.append("email_ids",{
            "email_id":self.email_id_or_address,
            "is_primary":1
        })
    if self.mobile_or_phone_number:
        self.phone_nos = []
        self.append("phone_nos",{
            "phone":self.mobile_or_phone_number,
            "is_primary_phone":1,
            "is_primary_mobile_no":1
        }
        )
   # self.email_id = self.email_id_or_address
   # self.mobile_no = self.mobile_or_phone_number
    for i in self.links:
        if i.link_doctype == "Customer":
            customer.append(i.link_name)
        elif i.link_doctype == "Supplier":
            supplier.append(i.link_name)
    if len(customer):
        for i in customer:
            if self.name in find_idx("Customer",i)[1]:
                continue
            doc = frappe.new_doc("Contact Details")
            doc.parenttype = "Customer"
            doc.parentfield = "contact_details"
            doc.parent = i
            doc.idx = find_idx("Customer",i)[0]+1
            doc.name1 = self.name
            doc.designation = self.designation
            doc.phone_number = self.phone
            doc.email_id = self.email_id_or_address
            doc.location  = self.location
            doc.save()
    if len(supplier):
        for i in supplier:
            if self.name in find_idx("Supplier",i)[1]:
                continue
            doc = frappe.new_doc("Contact Details")
            doc.parenttype = "Supplier"
            doc.parentfield = "contact_details"
            doc.parent = i
            doc.idx = find_idx("Supplier",i)[0]+1
            doc.name1 = self.name
            doc.designation = self.designation
            doc.phone_number = self.phone
            doc.email_id = self.email_id
            doc.location  = self.location
            doc.save()
    
def find_idx(doctype ,customer):
    doc = frappe.get_doc(doctype,customer)
    length = 0
    names = []
    for i in doc.contact_details:
        names.append(i.name1)
    if doc.contact_details:
        length = doc.contact_details[-1].idx
    return [length,names]
    # if self.links:
    #     for i in self.links:
    #         if i.link_doctype == "Customer":
    #             cus_self = frappe.get_doc("Customer",i.link_name)
    #             cus_self.contact_details = []
    #             cus_self.append("contact_details",{
    #                 "name1":self.name,
    #                 "designation":self.designation,
    #                 "phone_number":self.phone,
    #                 "email_id":self.email_id,
    #                 "location":self.location
    #             })
    #             cus_self.insert()
