from gettext import find
import frappe
from frappe.utils import datetime,now,today

def before_save(self,method):
    customer = []
    print("\n\n\n..........")
    print(self.email_id,self.mobile_no)
    if self.email_id_or_address:
        self.append("email_ids",{
            "email_id":self.email_id_or_address,
            "is_primary":1
        })
    if self.mobile_or_phone_number:
        self.append("phone_nos",{
            "phone":self.mobile_or_phone_number,
            "is_primary_phone":1,
            "is_primary_mobile_no":1
        }
        )
    self.email_id = self.email_id_or_address
    self.mobile_no = self.mobile_or_phone_number
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