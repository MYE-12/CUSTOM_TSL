# Copyright (c) 2025, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta
from frappe.utils.background_jobs import enqueue
import calendar

class WOApprovalTest(Document):
    @frappe.whitelist()
    def get_q(self):
        current_month = datetime.now().month

        # Get the list of month names (January to December)
        months = list(calendar.month_name)[1:]  # Skipping the empty string at index 0

        # Calculate the last 5 months including the current one



        last_six_months = []
        for i in range(11, -1, -1):  # 5 months before and including the current month
            month_index = (current_month - i - 1) % 12  # Handle wrap-around
            last_six_months.append(months[month_index])

        data = ""
        data += '<table class="table table-bordered">'
        data += '<tr>'
        data += '<td style="width:30%;border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="200"></td>'
        data += '<td style="width:30%;border-color:#000000;font-size:35px;color:#055c9d;"><center><b>TSL Company</b></center></td>'
        if self.company == "TSL COMPANY - Kuwait":  
            data += '<td style="width:30%;border-color:#000000;"><center><img src = "/files/kuwait flag.jpg" width ="120"></center></td>'
        if self.company == "TSL COMPANY - UAE":  
            data += '<td style="width:30%;border-color:#000000;"><center><img src = "/files/Flag_of_the_United_Arab_Emirates.svg.jpg" width ="120"></center></td>'

        data += '</tr>'
        data += '</table>'

        data += '<table class="table table-bordered">'

        data += '<tr>'
        data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>WO Approval Percentage by Amount</b><center></td>'
        data += '</tr>'

    
        sp = frappe.get_all("Sales Person",{"company":self.company},["*"])
        for i in sp:
            if i.name == "Ahmad" or i.name == "Vazeem" or i.name == "Maaz" or i.name == "Nidhin" or i.name == "EHAB" or i.name == "Yousef" or i.name == "Mohannad" or i.name == "Karoline":              
            # if i.name == "Vazeem":         
                sl = frappe.get_value("Sales Person",{"name":i.name},["user"])
                data += '<tr>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>Sales</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>Month</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>Total Quoted Amount(in KD)</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b>Approved Amount(in KD)</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b> % of Approved Amount</b><center></td>'
                data += '</tr>'
                tmt = 0
                tmt_2 = 0
                total_q1 = 0
                total_q2 = 0
                # for m in last_six_months:
                for index, m in enumerate(last_six_months):
                    
                    month_name = m
                    
                    # Get the month number from the month name
                    month_number = datetime.strptime(month_name, "%B").month
                    # current_date = datetime.now()
                    year = 2024
                    if month_number == 1 or month_number == 2 or month_number == 3 or month_number == 4:
                        year = 2025
                   
                    # First date of the month
                    first_day = datetime(year, month_number, 1)

                    # Last date of the month
                    last_day = datetime(year, month_number, calendar.monthrange(year, month_number)[1])
                    
                    data += '<tr>'

                    
                    if index == 5:
                        data += '<td style="border-bottom:hidden;border-color:#000000;padding:1px;font-size:12px;font-weight:bold"><center>%s<center></td>' %(sl)
                    else:
                        data += '<td style="border-bottom:hidden;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("")
                    
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;font-weight:bold"><center>%s<center></td>' %(m)

                    from_date = first_day.date()
                    to_date = last_day.date()
                    
                    wod = frappe.db.sql(''' select 
                    DISTINCT `tabQuotation Item`.wod_no AS wd
                    from `tabQuotation` 
                    left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    where `tabQuotation`.sales_rep = '%s' and                   
                    `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") and
                    `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
                    and transaction_date between '%s' and '%s' ''' %(sl,from_date,to_date),as_dict=1)
                   
                    q_m = 0
                    q_m_2 = 0
                    if wod:
                        for i in wod:
                            
                            q_amt = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                            `tabQuotation`.default_discount_percentage as dis,
                            `tabQuotation`.approval_date as a_date,
                            `tabQuotation`.is_multiple_quotation as is_m,
                            `tabQuotation`.after_discount_cost as adc,
                            `tabQuotation Item`.unit_price as up,
                            `tabQuotation Item`.margin_amount as ma 
                            from `tabQuotation` 
                            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                            where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                            and `tabQuotation`.sales_rep = '%s' and `tabQuotation Item`.wod_no = '%s' and
                            `tabQuotation`.quotation_type in ("Customer Quotation - Repair")  and transaction_date between '%s' and '%s'
                            ''' %(sl,i["wd"],from_date,to_date),as_dict=1)

                            if q_amt:
                                
                                if q_amt[0]["is_m"] == 1:
                                    per = (q_amt[0]["up"] * q_amt[0]["dis"])/100
                                    q_amt = q_amt[0]["up"] - per
                                    q_m = q_m + q_amt

                                else:
                                    q_amt = q_amt[0]["adc"]
            
                                    q_m = q_m + q_amt

                            
                            rev = frappe.db.sql(''' select 
                            DISTINCT `tabQuotation Item`.wod_no AS wd
                            from `tabQuotation` 
                            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                            where `tabQuotation`.sales_rep = '%s' and                   
                            `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") and
                            `tabQuotation`.quotation_type in ("Customer Quotation - Repair") and `tabQuotation Item`.wod_no = '%s'
                            and transaction_date between '%s' and '%s' ''' %(sl,i["wd"],from_date,to_date),as_dict=1)
                   
                            frappe.errprint(rev)
                            if rev:
                                q_amt_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                                `tabQuotation`.default_discount_percentage as dis,
                                `tabQuotation`.approval_date as a_date,
                                `tabQuotation`.is_multiple_quotation as is_m,
                                `tabQuotation`.after_discount_cost as adc,
                                `tabQuotation Item`.unit_price as up,
                                `tabQuotation Item`.margin_amount as ma 
                                
                                from `tabQuotation` 
                                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                                where  `tabQuotation`.Workflow_state in ("Approved By Customer") 
                                and `tabQuotation`.sales_rep = '%s' and `tabQuotation Item`.wod_no = '%s' and
                                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
                                and transaction_date between '%s' and '%s'
                                ''' %(sl,i["wd"],from_date,to_date),as_dict=1)

                                if q_amt_2:
                                    if q_amt_2[0]["is_m"] == 1:
                                        per = (q_amt_2[0]["up"] * q_amt_2[0]["dis"])/100
                                        q_amt = q_amt_2[0]["up"] - per
                                        q_m_2 = q_m_2 + q_amt

                                    else:
                                        q_amt = q_amt_2[0]["adc"]
                                        q_m_2 = q_m_2 + q_amt
                                
                                

                                

                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'% (f"{round(q_m):,}" or 0)
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' % (f"{round(q_m_2):,}" or 0)
                    if not q_m or not q_m_2:
                        data += '<td style="font-weight:bold;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("0")
                    else:
                        data += '<td style="font-weight:bold;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s%s<center></td>' %(round((q_m_2/q_m)*100),"%")

                    total_q1 = total_q1 + round(q_m)
                    total_q2 = total_q2 + round(q_m_2)
                
                data += '</tr>'

               
                data += '<tr>'
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'% ("")
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s<center></td>' % ("Total")
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s<center></td>'% (f"{round(total_q1):,}" or 0)
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s<center></td>' % (f"{round(total_q2):,}" or 0)
                if total_q1 == 0:
                    data += '<td style="background-color:red;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(0,"%")
                else:
                    if round((total_q2/total_q1)*100) < 60:
                        data += '<td style="background-color:red;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%")
                    if round((total_q2/total_q1)*100) > 60 and round((total_q2/total_q1)*100) < 80:
                        data += '<td style="background-color:yellow;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%")
                    if round((total_q2/total_q1)*100) >=80:
                         data += '<td style="background-color:green;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%") 
                
                
                data += '</tr>'
                data += '<tr>'
                data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>-</b><center></td>'
                data += '</tr>'

        data += '</table>'

        return data

    
