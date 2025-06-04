import frappe

def create_customer_details(doc,method):
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
