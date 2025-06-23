# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class InvoiceRequest(Document):
    @frappe.whitelist()
    def get_work_orders(qu):
        # data= ""
        # data += '<table class="table table-bordered">'
        # data += '<tr>'
        # data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Linked Work Orders</b><center></td>'
        # data += '</tr>'	

        # wd = frappe.db.sql(""" select  `tabQuotation Item`.wod_no from `tabQuotation` 
        # 	left join `tabQuotation Item` on `tabQuotation Item`.parent = `tabQuotation`.name
        # 	where `tabQuotation`.name = '%s' """ %(self.quotation),as_dict = 1)
        frappe.errprint(qu)
        # for i in wd:
        # 	data += '<tr>'
        # 	data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(i["wod_no"])
        # 	data += '</tr>'	
        # data += '</table>'
        # return wd
    
    def on_update(self):
        info = ""
    
        if self.branch == "Riyadh - TSL- KSA":
            info = "info-sa@tsl-me.com"
        
        if self.branch == "Dammam - TSL-SA":
            info = "info-dmm@tsl-me.com"
        
        if self.branch == "Jeddah - TSL-SA":
            info = "info-jed@tsl-me.com"

        if self.branch == "Kuwait - TSL":
            info = "info@tsl-me.com"


        if not self.email_sent:
            if self.invoice_list:
                for i in self.invoice_list:
                    if i.quotation:
                        cus = frappe.get_value("Quotation",i.quotation,"party_name")
                        msg = '''Dear Finance,<br><br> Quotation <b>%s</b> has been approved.<br>Customer Name : <b>%s</b>.<br><br>Please take action to make invoice. <br><br><a href="https://erp.tsl-me.com/app/invoice-request/%s" target="_blank">Click Here</a>'''%(i.quotation,cus,self.name)
                    
                        if self.workflow_state == "Pending with Finance":
                            if self.branch != "Kuwait - TSL":
                            
                                frappe.sendmail(
                                    sender= info,
                                    recipients=['finance-sa1@tsl-me.com',"finance@tsl-me.com"],
                                    subject = "Invoice Request - %s"%(i.quotation),
                                    message = msg,
                                
                                    )
                                # frappe.db.set_value("Invoice Request",self.name,"email_sent",1)
                                self.email_sent = 1
                            else:
                                frappe.sendmail(
                                    sender= info,
                                    recipients=['finance2@tsl-me.com',"finance-kw@tsl-me.com"],
                                    subject = "Invoice Request - %s"%(i.quotation),
                                    message = msg,
                                
                                    )
                                # frappe.db.set_value("Invoice Request",self.name,"email_sent",1)
                                self.email_sent = 1
                                
            if self.sod_quotation:
                for i in self.sod_quotation:
                    if i.quotation:
                        cus = frappe.get_value("Quotation",i.quotation,"party_name")
                        msg = '''Dear Finance,<br><br> Quotation <b>%s</b> has been approved.<br>Customer Name : <b>%s</b>.<br><br>Please take action to make invoice. <br><br><a href="https://erp.tsl-me.com/app/invoice-request/%s" target="_blank">Click Here</a>'''%(i.quotation,cus,self.name)
                    
                        if self.workflow_state == "Pending with Finance":
                            if self.branch != "Kuwait - TSL":
                            
                                frappe.sendmail(
                                    sender= info,
                                    recipients=['finance-sa1@tsl-me.com',"finance@tsl-me.com"],
                                    cc = ["karthiksrinivasan1996.ks@gmail.com","yousuf@tsl-me.com"],
                                    subject = "Invoice Request - %s"%(i.quotation),
                                    message = msg,
                                
                                    )
                                # frappe.db.set_value("Invoice Request",self.name,"email_sent",1)
                                self.email_sent = 1
                            else:
                                frappe.sendmail(
                                    sender= info,
                                    recipients=['finance2@tsl-me.com',"finance-kw@tsl-me.com"],
                                    cc = ["karthiksrinivasan1996.ks@gmail.com","yousuf@tsl-me.com"],
                                    subject = "Invoice Request - %s"%(i.quotation),
                                    message = msg,
                                
                                    )
                                # frappe.db.set_value("Invoice Request",self.name,"email_sent",1)
                                self.email_sent = 1

            
    def on_submit(self):
        frappe.db.set_value("Invoice Request",self.name,"submitted_by",frappe.session.user)
        if self.workflow_state == "Invoice Created":
            
            # self.submitted_by = frappe.session.user
            frappe.db.set_value("Invoice Request",self.name,"submitted_by",frappe.session.user)
            if self.invoice_list:
                for i in self.invoice_list:
                    if i.quotation:
                        cus = frappe.get_value("Quotation",i.quotation,"party_name")
                        # msg = '''Dear Info,<br> Against the Quotation invoice has been created.Please find the invoice in Attach Invoice Field <br><a href="https://erp.tsl-me.com/app/invoice-request/%s" target="_blank">Click Here</a>'''%(self.name)
                        msg = """Dear Info,<br><br>
                                    I hope this email finds you well.<br><br>
                                    The Invoice has been created as per your request for the Quotation - %s.<br><br>
                                    Please find the attached Invoice for your reference.<a href="https://erp.tsl-me.com/app/invoice-request/%s" target="_blank">Click Here</a>"""%(i.quotation,self.name)
                        frappe.sendmail(
                            sender= self.submitted_by,
                            recipients=["yousuf@tsl-me.com",self.requested_by],
                            subject = "Invoice Created for - %s"%(i.quotation),
                            message = msg,
                        
                            )
    