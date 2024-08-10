import frappe

def on_update_after_submit(self,method):
   for i in self.items:
      if i.supply_order_data:
         frappe.db.set_value("Supply Order Data",i.supply_order_data,"dn_no",self.name)
         frappe.db.set_value("Supply Order Data",i.supply_order_data,"dn_date",self.posting_date)

   

def on_submit(self,method):
   for i in self.get("items"):
      wod = i.work_order_data or i.wod_no
      
      if wod:
         dn_rsi = frappe.db.sql("""select status_cap,invoice_no,payment_entry_reference from `tabWork Order Data` where name = '%s' """%(wod),as_dict=1)
         for dn in dn_rsi:
            # if there is invoice_no status will be RSI
            if dn.invoice_no and not dn.status_cap:
               frappe.db.set_value("Work Order Data",wod,"dn_no",self.name)
               frappe.db.set_value("Work Order Data",wod,"dn_date",self.posting_date)
               frappe.db.set_value("Work Order Data",wod,"delivery",self.posting_date)
               frappe.db.set_value("Work Order Data",wod,"status","RSI-Repaired and Shipped Invoiced")
               
           
            #if there is invoice and NER status will be RSI
               
            elif dn.status_cap and dn.invoice_no:
               frappe.db.set_value("Work Order Data",wod,"dn_no",self.name)
               frappe.db.set_value("Work Order Data",wod,"dn_date",self.posting_date)
               frappe.db.set_value("Work Order Data",wod,"delivery",self.posting_date)
               frappe.db.set_value("Work Order Data",wod,"status","RSI-Repaired and Shipped Invoiced")
            
            elif dn.status_cap and dn.payment_entry_reference:
               wd = frappe.get_doc("Work Order Data",wod)
               wd.status = "P-Paid"
               wd.save(ignore_permissions = 1)
             
            # if none no NER or INVOICE it will be RSC
            else:
               wd = frappe.get_doc("Work Order Data",wod)
               if not wd.status_cap == "NER-Need Evaluation Return":
                  wd.status = "RSC-Repaired and Shipped Client"
                  # wd.dn_no = self.name
                  # wd.dn_date = self.posting_date
                  # wd.delivery = self.posting_date
                  wd.save(ignore_permissions = 1)
                  frappe.db.set_value("Work Order Data",wod,"dn_no",self.name)
                  frappe.db.set_value("Work Order Data",wod,"dn_date",self.posting_date)
                  frappe.db.set_value("Work Order Data",wod,"delivery",self.posting_date)
           
      if i.supply_order_data:
         doc = frappe.get_doc("Supply Order Data",i.supply_order_data)
         doc.status = 'Invoiced'
         doc.save(ignore_permissions = True)
         frappe.db.set_value("Supply Order Data",i.supply_order_data,"dn_no",self.name)
         frappe.db.set_value("Supply Order Data",i.supply_order_data,"dn_date",self.posting_date)

   

@frappe.whitelist()
def wo_status_count():
    wo_status = frappe.db.sql("""select status from `tabWork Order Data` status""")
    for wo in wo_status:
      print(wo_status)
