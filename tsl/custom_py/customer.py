import frappe

def create_customer_details(doc,method):
#    contacts = frappe.db.sql('''select c.name as name,c.phone as phone,c.mobile_no as mobile_no,c.email_id as email,c.designation as desig,c.address as location from `tabContact` as c inner join `tabDynamic Link` as dl on dl.parent = c.name where dl.link_doctype = "Customer" and dl.link_name = %s and dl.parenttype = "Contact" ''',self.name,as_dict=1)
 #   print(contacts)
  #  if contacts:
#        self.contact_details = []
#        for i in contacts:
 #           self.append("contact_details",{
 #               "name1":i['name'],
 #               "designation":i['desig'],
 #               "phone_number":i['phone'] if i['phone'] else i['mobile_no'],
 #               "email_id":i['email'],
 #               "location":i['location'],
 #           })

	if doc.email_id:
		customer = frappe.get_doc('Customer',{'email_id':doc.email_id})
		if customer:
			customer.append("contact_details",{
                "name1":doc.name,
                "designation":doc.designation,
                "phone_number":doc.phone if doc.phone else doc.mobile_no,
                "email_id":doc.email_id,
                "location":doc.location,
            })
		frappe.db.commit()
		customer.save(ignore_permissions=True)
