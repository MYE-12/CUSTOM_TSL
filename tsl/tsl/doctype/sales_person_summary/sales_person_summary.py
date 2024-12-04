# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta
from frappe.utils.background_jobs import enqueue
import calendar

class SalesPersonSummary(Document):
    @frappe.whitelist()
    def get_q(self):
        current_month = datetime.now().month

        # Get the list of month names (January to December)
        months = list(calendar.month_name)[1:]  # Skipping the empty string at index 0

        # Calculate the last 5 months including the current one



        last_six_months = []
        for i in range(5, -1, -1):  # 5 months before and including the current month
            month_index = (current_month - i - 1) % 12  # Handle wrap-around
            last_six_months.append(months[month_index])





        # frappe.errprint(last_six_months)
        # months = list(calendar.month_name)[3:]

        # frappe.errprint(months)
        # # Get the current month as an integer (1 for January, 12 for December)
        # current_month = datetime.now().month
        # frappe.errprint(current_month)
        # # Filter months that come before and include the current month
        # months_before_and_including_current = months[]
        # frappe.errprint(months_before_and_including_current)
        data= ""
        data += '<table class="table table-bordered">'

        data += '<tr>'
        data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>WO Approval Percentage by Amount</b><center></td>'
        data += '</tr>'

    
        sp = frappe.get_all("Sales Person",{"company":self.company},["*"])
        for i in sp:
            if i.name == "Ahmad" or i.name == "Maaz" or i.name == "Vazeem" or i.name == "Abdullah":
                sl = frappe.get_value("Sales Person",{"name":i.name},["user"])
                data += '<tr>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Sales</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Month</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Total Quoted Amount</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>Approved Amount</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b> % of Approved Amount</b><center></td>'
                data += '</tr>'
                tmt = 0
                tmt_2 = 0
                for m in last_six_months:
                    month_name = m
                    year = 2024

                    # Get the month number from the month name
                    month_number = datetime.strptime(month_name, "%B").month

                    # First date of the month
                    first_day = datetime(year, month_number, 1)

                    # Last date of the month
                    last_day = datetime(year, month_number, calendar.monthrange(year, month_number)[1])
                    
                    data += '<tr>'
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(i.name)
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(m)

                    from_date = first_day.date()
                    to_date = last_day.date()

                   
                    # q_m = 0
                    # if q_amt:
                    #     ap_date = q_amt[0]["a_date"]
                    #     qu_name =  q_amt[0]["q_name"]
                    #     po =  q_amt[0]["po_no"]
                    #     if q_amt[0]["is_m"] == 1:
                    #         per = (q_amt[0]["up"] * q_amt[0]["dis"])/100
                    #         q_m = q_amt[0]["up"] - per

                    #     if q_amt[0]["is_m"] == 0:
                    #         q_m = q_amt[0]["adc"]

                    # else:
                    #     q_amt_2 = frappe.db.sql(''' select `tabQuotation`.purchase_order_no as po_no,`tabQuotation`.name as q_name,`tabQuotation`.default_discount_percentage as dis,`tabQuotation`.approval_date as a_date,`tabQuotation`.is_multiple_quotation as is_m,`tabQuotation`.after_discount_cost as adc,`tabQuotation`.Workflow_state,`tabQuotation Item`.unit_price as up,`tabQuotation Item`.margin_amount as ma from `tabQuotation` 
                    #     left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    #     where  `tabQuotation`.Workflow_state in ("Quoted to Customer") and `tabQuotation Item`.wod_no = %s ''',i.name,as_dict=1)

                    #     if q_amt_2:
                    #         ap_date = q_amt_2[0]["a_date"]
                    #         qu_name =  q_amt_2[0]["q_name"]
                    #         po =  q_amt_2[0]["po_no"]
                    #         if q_amt_2[0]["is_m"] == 1:
                    #             per = (q_amt_2[0]["up"] * q_amt_2[0]["dis"])/100
                    #             q_m = q_amt_2[0]["up"] - per

                    #         if q_amt_2[0]["is_m"] == 0:
                    #             q_m = q_amt_2[0]["adc"]

                    tmt = 0
                    tmt_2 = 0
                   
                    qu = frappe.db.sql(""" select sum(`tabQuotation`.final_approved_price) as f_amt from `tabQuotation`
                    where `tabQuotation`.sales_rep = "%s" and `tabQuotation`.workflow_state in ("Approved By Customer","Quoted to Customer") and `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") and transaction_date between '%s' and '%s' """ %(sl,from_date,to_date) ,as_dict=1)
                   
                    if qu:
                        tmt = qu[0]["f_amt"]
                        # frappe.errprint(qu)
                       
                    qu2 = frappe.db.sql(""" select sum(`tabQuotation`.after_discount_cost) as d_amt from `tabQuotation`
                    where `tabQuotation`.sales_rep = "%s" and `tabQuotation`.workflow_state in ("Approved By Customer") and `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") and transaction_date between '%s' and '%s' """ %(sl,from_date,to_date) ,as_dict=1)
                   
                    if qu2:
                        tmt_2 = qu2[0]["d_amt"]
                        # frappe.errprint(qu2)
                     
                    
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(tmt or 0)
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(tmt_2 or 0)
                    if not tmt or not tmt_2:
                        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("0")
                    else:
                        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(round((tmt_2/tmt)*100,2))
                    

                    data += '</tr>'
            
                data += '<tr>'
                data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>-</b><center></td>'
                data += '</tr>'

        data += '</table>'

        return data

    