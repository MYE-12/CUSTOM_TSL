import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta
from frappe.utils.background_jobs import enqueue
import calendar

@frappe.whitelist()
def get_sales(company):
    d = datetime.now().date()
    ogdate = datetime.strptime(str(d),"%Y-%m-%d")

    # Format the date as a string in the desired format
    formatted_date = ogdate.strftime("%d-%m-%Y")

    current_month = datetime.now().month

    # Get the list of month names (January to December)
    months = list(calendar.month_name)[1:]  # Skipping the empty string at index 0

    # Calculate the last 5 months including the current one



    last_six_months = []
    for i in range(11, -1, -1):  # 5 months before and including the current month
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
    # if company == "TSL COMPANY - Kuwait":
    #     branch = "Kuwait" 
    # if company == "TSL COMPANY - UAE":
    #     branch = "UAE" 
    data= ""
    data += '<table class="table table-bordered">'

    data += '<tr>'
    data += '<td style="width:30%;border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="220"></td>'
    if company == "TSL COMPANY - Kuwait":  
        data += '<td style="width:30%;border-color:#000000;color:#055c9d;"><h1><center><b style="color:#055c9d;">TSL Company<br>Branch - Kuwait</b></center></h1></td>' 
    if company == "TSL COMPANY - UAE":  
        data += '<td style="width:40%;border-color:#000000;color:#055c9d;"><h1><center><b style="color:#055c9d;">TSL Company<br>Branch - UAE</b></center></h1></td>' 
    if company == "TSL COMPANY - Kuwait": 
        data += '<td style="width:30%;border-color:#000000;"><center><img src = "/files/kuwait flag.jpg" width ="120"></center></td>'
    if company == "TSL COMPANY - UAE":  
        data += '<td style="width:30%;border-color:#000000;"><center><img src = "/files/Flag_of_the_United_Arab_Emirates.svg.jpg" width ="120"></center></td>'
    data += '</tr>'
    data += '</table>'
    # data += '<p align = right>%s</p>' %(formatted_date)
    data += '<table class="table table-bordered">'
    data += '<tr>'
    data += '<td colspan = 5 align = right style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><b style="color:white;">Generation Date:%s</b></td>' %(formatted_date)
    data += '</tr>'
    data += '<tr>'
    data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">WO Approval Percentage by Amount</b><center></td>'
    data += '</tr>'


    sp = frappe.get_all("Sales Person",{"company":company},["*"])
    for i in sp:
        if i.name == "Ahmad" or i.name == "Vazeem" or i.name == "Maaz" or i.name == "Nidhin" or i.name == "EHAB" or i.name == "Yousef" or i.name == "Mohannad" or i.name == "Karoline":                         
        # if i.name == "Ahmad":         
            sl = frappe.get_value("Sales Person",{"name":i.name},["user"])
            if company == "TSL COMPANY - Kuwait":
                data += '<tr>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Sales</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Month</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Total Quoted Amt(in KD)</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Approved Amt(in KD)</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;"> % of Approved Amount</b><center></td>'
                data += '</tr>'
            if company == "TSL COMPANY - UAE":
                data += '<tr>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Sales</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Month</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Total Quoted Amt(in AED)</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Approved Amt(in AED)</b><center></td>'
                data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;"> % of Approved Amount</b><center></td>'
                data += '</tr>'
            tmt = 0
            tmt_2 = 0
            total_q1 = 0
            total_q2 = 0
            
            # for m in last_six_months:
            for index, m in enumerate(last_six_months):
               # frappe.errprint(index)
                month_name = m
                
                # Get the month number from the month name
                month_number = datetime.strptime(month_name, "%B").month
                # current_date = datetime.now()
                year = 2024
                if month_number == 1 or month_number == 2 or month_number == 3:
                    year = 2025
                
                # First date of the month
                first_day = datetime(year, month_number, 1)

                # Last date of the month
                last_day = datetime(year, month_number, calendar.monthrange(year, month_number)[1])
                
                data += '<tr>'
                if index == 6:
                    data += '<td style="border-bottom:hidden;border-color:#000000;padding:1px;font-size:12px;font-weight:bold"><center>%s<center></td>' %(i.name)
                else:
                    data += '<td style="border-bottom:hidden;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("")

                # data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(i.name)
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(m)

                from_date = first_day.date()
                to_date = last_day.date()

                # w = frappe.db.sql(""" select name from `tabWork Order Data` where sales_rep = '%s' and company = '%s' and old_wo_no IS NULL """ %(i.name,self.company),as_dict =1)
                # w = frappe.get_all("Work Order Data",{"sales_rep":i.name,"company":self.company,"old_wo_no":["is","not set"]},["*"])
                
                q_m = 0
                q_m_2 = 0
                # for j in w:
                q_amt = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer") 
                and `tabQuotation`.sales_rep = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
                and transaction_date between '%s' and '%s' ''' %(sl,from_date,to_date),as_dict=1)

                if q_amt:
                    for k in q_amt:
                        if k.is_m == 1:
                            
                            per = (k.up * k.dis)/100
                            q_amt = k.up - per
                            # q_amt = k.ma
                            q_m = q_m + q_amt

                        else:
                            q_amt = k.adc
                    
                            q_m = q_m + q_amt
                            
                    
                q_amt_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.wod_no as wod,                      
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation`.Workflow_state,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as mar,
                `tabQuotation Item`.margin_amount as ma from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where `tabQuotation`.Workflow_state in ("Approved By Customer") and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")
                and `tabQuotation`.sales_rep = '%s'
                and transaction_date between '%s' and '%s' ''' %(sl,from_date,to_date) ,as_dict=1)

                if q_amt_2:
                    for k in q_amt_2:
                        if k.is_m == 1:
                            # c_wo = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                            # `tabQuotation`.transaction as t_date
                            # from `tabQuotation` 
                            # left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                            # where  `tabQuotation`.Workflow_state in ("Approv"Quoted to Customer") 
                            # and `tabQuotation`.sales_rep = '%s' and tabQuotation Item`.wod_no = '%s' 
                            # `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
                            # and transaction_date between '%s' and '%s' ''' %(k.wod,sl,from_date,to_date),as_dict=1)
                            # frappe.errprint(k.q_name)
                            per = (k.up * k.dis)/100
                            q_amt_2 = k.up - per
                            # q_amt_2 = k.mar
                    
                            
                            q_m_2 = q_m_2 + q_amt_2


                        else:
                            # frappe.errprint(k.q_name)
                            q_amt_2 = k.adc
                    
                            q_m_2 = q_m_2 + q_amt_2

                
                if company == "TSL COMPANY - Kuwait":
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'% (f"{round(q_m):,}" or 0)
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' % (f"{round(q_m_2):,}" or 0)
                    if not q_m or not q_m_2:
                        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("0")
                    else:
                        # if round((q_m_2/q_m)*100) < 60:
                        #     data += '<td style="font-weight:bold;background-color:red;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s%s<center></td>' %(round((q_m_2/q_m)*100),"%")
                        # if round((q_m_2/q_m)*100) >= 60 and round((q_m_2/q_m)*100) < 80:
                        #     frappe.errprint(round((q_m_2/q_m)*100))
                        #     data += '<td style="font-weight:bold;background-color:yellow;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s%s<center></td>' %(round((q_m_2/q_m)*100),"%")
                        # if round((q_m_2/q_m)*100) >=80:
                        #     data += '<td style="font-weight:bold;background-color:green;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s%s<center></td>' %(round((q_m_2/q_m)*100),"%")

                        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s%s<center></td>' %(round((q_m_2/q_m)*100),"%")
                        
                    total_q1 = total_q1 + round(q_m)
                    total_q2 = total_q2 + round(q_m_2)
                
                if company == "TSL COMPANY - UAE":
                    if q_m > 0:
                        q_m = round(q_m)
                    if q_m_2 > 0:
                        q_m_2 = round(q_m_2)

                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'% (f"{q_m:,}" or 0)
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' % (f"{q_m_2:,}" or 0)
                    if not q_m or not q_m_2:
                        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("0")
                    else:
                        x = (q_m_2/q_m)*100
                        # if x < 60:
                        #     data += '<td style="font-weight:bold;background-color:red;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s%s<center></td>' %(round(x),"%")
                        # if x > 60 and x < 80:
                        #     data += '<td style="font-weight:bold;background-color:yellow;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s%s<center></td>' %(round(x),"%")
                        # if x >=80:
                        #     data += '<td style="font-weight:bold;background-color:green;border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s%s<center></td>' %(round(x),"%")

                        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s%s<center></td>' %(round(x),"%")
                        
                    total_q1 = total_q1 + round(q_m)
                    total_q2 = total_q2 + round(q_m_2)
                
            data += '</tr>'
            
            if company == "TSL COMPANY - Kuwait":
                
                data += '<tr>'
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'% ("")
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s<center></td>' % ("Total")
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s<center></td>'% (f"{round(total_q1):,}" or 0)
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s<center></td>' % (f"{round(total_q2):,}" or 0)

                if round((total_q2/total_q1)*100) < 60:
                    data += '<td style="background-color:red;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%")
                if round((total_q2/total_q1)*100) > 60 and round((total_q2/total_q1)*100) < 80:
                    data += '<td style="background-color:yellow;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%")
                if round((total_q2/total_q1)*100) >=80:
                        data += '<td style="background-color:green;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%") 

              
                # data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%")
                data += '</tr>'

            if company == "TSL COMPANY - UAE":
                data += '<tr>'
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'% ("")
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s<center></td>' % ("Total")
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s<center></td>'% (f"{total_q1:,}" or 0)
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s<center></td>' % (f"{total_q2:,}" or 0)
                if total_q1 == 0:
                    data += '<td style="background-color:red;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %((0),"%")
                else:
                    if round((total_q2/total_q1)*100) < 60:
                        data += '<td style="background-color:red;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%")
                    if round((total_q2/total_q1)*100) > 60 and round((total_q2/total_q1)*100) < 80:
                        data += '<td style="background-color:yellow;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%")
                    if round((total_q2/total_q1)*100) >=80:
                         data += '<td style="background-color:green;border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>' %(round((total_q2/total_q1)*100),"%") 

              
                    # data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:13px;font-weight:bold;"><center>%s%s<center></td>'  %(round((total_q2/total_q1)*100),"%")
                data += '</tr>'

        
            data += '<tr>'
            data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>-</b><center></td>'
            data += '</tr>'
    data += '</table>'
    return data

    
    # data= ""
    # data += '<table class="table table-bordered">'

    # data += '<tr>'
    # data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">WO Approval Percentage by Amount</b><center></td>'
    # data += '</tr>'


    # sp = frappe.get_all("Sales Person",{"company":company},["*"])
    # for i in sp:
    #     if i.name == "Ahmad" or i.name == "Maaz" or i.name == "Vazeem" or i.name == "Abdullah":
    #         sl = frappe.get_value("Sales Person",{"name":i.name},["user"])
    #         data += '<tr>'
    #         data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Sales</b><center></td>'
    #         data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Month</b><center></td>'
    #         data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Total Quoted Amount</b><center></td>'
    #         data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;">Approved Amount</b><center></td>'
    #         data += '<td style="width:20%;border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#0e86d4;color:white;"><center><b style="color:white;"> % of Approved Amount</b><center></td>'
    #         data += '</tr>'
    #         tmt = 0
    #         tmt_2 = 0
    #         for m in last_six_months:
    #             month_name = m
    #             year = 2024

    #             # Get the month number from the month name
    #             month_number = datetime.strptime(month_name, "%B").month

    #             # First date of the month
    #             first_day = datetime(year, month_number, 1)

    #             # Last date of the month
    #             last_day = datetime(year, month_number, calendar.monthrange(year, month_number)[1])
                
    #             data += '<tr>'
    #             data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(i.name)
    #             data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(m)

    #             from_date = first_day.date()
    #             to_date = last_day.date()

                
                
    #             tmt = 0
    #             tmt_2 = 0
                
    #             qu = frappe.db.sql(""" select sum(`tabQuotation`.final_approved_price) as f_amt from `tabQuotation`
    #             where `tabQuotation`.sales_rep = "%s" and `tabQuotation`.workflow_state in ("Approved By Customer","Quoted to Customer") and `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") and transaction_date between '%s' and '%s' """ %(sl,from_date,to_date) ,as_dict=1)
                
    #             if qu:
    #                 tmt = qu[0]["f_amt"]
    #                 frappe.errprint(qu)
                    
    #             qu2 = frappe.db.sql(""" select sum(`tabQuotation`.after_discount_cost) as d_amt from `tabQuotation`
    #             where `tabQuotation`.sales_rep = "%s" and `tabQuotation`.workflow_state in ("Approved By Customer") and `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") and transaction_date between '%s' and '%s' """ %(sl,from_date,to_date) ,as_dict=1)
                
    #             if qu2:
    #                 tmt_2 = qu2[0]["d_amt"]
    #                 frappe.errprint(qu2)
                    
                
    #             data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("{:,.2f}".format(tmt or 0))
    #             data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("{:,.2f}".format(tmt_2 or 0))
    #             if not tmt or not tmt_2:
    #                 data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("0.00")
    #             else:
    #                 data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(round((tmt_2/tmt)*100,2))
                

    #             data += '</tr>'
        
    #         data += '<tr>'
    #         data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>-</b><center></td>'
    #         data += '</tr>'

    # data += '</table>'

    # return data

