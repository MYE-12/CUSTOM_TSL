import frappe,json

def on_submit(self,method):
    if self.supply_order_data and len(self.references)>0 and self.payment_type == 'Receive':
        doc = frappe.get_doc("Supply Order Data",self.supply_order_data)
        doc.status = "Paid"
        doc.save(ignore_permissions = True)
    if self.work_order_data and len(self.references)>0 and self.payment_type == 'Receive':
        doc = frappe.get_doc("Work Order Data",self.work_order_data)
        doc.status = "P-Paid"
        doc.save(ignore_permissions = True)
    
    # if not self.work_order_data and len(self.references)>0 and self.payment_type == 'Receive' and len(self.work_orders)>0:
    #     for i in self.work_orders:
    #         doc = frappe.get_doc("Work Order Data",i.work_order_data)
    #         doc.status = "P-Paid"
    #         doc.save(ignore_permissions = True)
    


    if self.work_order_data and self.payment_type == 'Receive':
        frappe.db.sql('''update `tabWork Order Data` set payment_entry_reference = %s,advance_payment_amount=%s,advance_paid_date=%s where name = %s''',(self.name,self.paid_amount,self.posting_date,self.work_order_data))
    if self.supply_order_data and self.payment_type == 'Receive':
        frappe.db.sql('''update `tabSupply Order Data` set payment_entry_reference = %s,advance_payment_amount=%s,advance_paid_date=%s where name = %s''',(self.name,self.paid_amount,self.posting_date,self.supply_order_data))

