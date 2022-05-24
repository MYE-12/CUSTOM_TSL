import frappe

def on_submit(self,method):
    for i in self.get('items'):
        frappe.db.sql('''update `tabPart Sheet Item` as pi inner join  `tabEvaluation Report` as er on pi.parent = er.name set pi.parts_availability = "Yes" where er.work_order_data = %s and er.docstatus = 1 and pi.part = %s and pi.qty <= %s''',(self.work_order_data,i.item_code,float(i.qty)))
    frappe.db.commit()