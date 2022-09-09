from gettext import find
import frappe
from frappe.utils import datetime,now,today

def on_save(self,method):
    customer = []
    for i in self.links:
        if i.link_doctype == "Customer":
            customer.append(i.link_name)
    for i in customer:
        doc = frappe.new_doc("Contact Details")
        doc.parenttype = "Customer"
        doc.parentfield = "contact_details"
        doc.parent = i
        doc.idx = find_idx(i)+1
        doc.name1 = self.name
        doc.designation = self.designation
        doc.phone_number = self.phone
        doc.email_id = self.email_id
        doc.location  = self.location
        doc.save()
    
def find_idx(customer):
    doc = frappe.get_doc("Customer",customer)
    length = 0
    if doc.contact_details:
        length = doc.contact_details[-1].idx
    return length
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