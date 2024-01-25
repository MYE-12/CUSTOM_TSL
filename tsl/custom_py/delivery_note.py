import frappe

def on_submit(self,method):
	# pass
   for i in self.get("items"):
      if i.wod_no:
         dn_rsi = frappe.db.sql("""select status_cap,invoice_no from `tabWork Order Data` where name =%s"""%(i.wod),as_dict=1)
         frappe.errprint(dn_rsi)

         frappe.db.set_value("Work Order Data",i.wod_no,"dn_no",self.name)
         frappe.db.set_value("Work Order Data",i.wod_no,"dn_date",self.posting_date)
         frappe.db.set_value("Work Order Data",i.wod_no,"delivery",self.posting_date)
         doc = frappe.get_doc("Work Order Data",i.wod_no)
      #   doc.status = 'CT-Customer Testing'
         doc.status = 'RSC-Repaired and Shipped Client'
         
         doc.save(ignore_permissions = True)
#        if i.supply_order_data:
#            doc = frappe.get_doc("Supply Order Data",i.supply_order_data)
#            doc.status = "Delivered and Invoiced"
#            doc.save(ignore_permissions = True)


@frappe.whitelist()
def wo_status_count():
    wo_status = frappe.db.sql("""select status from `tabWork Order Data` status""")
    for wo in wo_status:
      print(wo_status)
