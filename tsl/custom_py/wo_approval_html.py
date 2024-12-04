import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta
from frappe.utils.background_jobs import enqueue
import calendar

@frappe.whitelist()
def get_data(company):
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


    sp = frappe.get_all("Sales Person",{"company":company},["*"])
    for i in sp:
        if i.name == "Ahmad":              
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

                w = frappe.db.sql(""" select name from `tabWork Order Data` where sales_rep = '%s' and company = '%s' and old_wo_no IS NULL """ %(i.name,company),as_dict =1)
                # w = frappe.get_all("Work Order Data",{"sales_rep":i.name,"company":self.company,"old_wo_no":["is","not set"]},["*"])
                q_m = 0
                q_m_2 = 0

                for j in w:
                    q_amt = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                    `tabQuotation`.default_discount_percentage as dis,
                    `tabQuotation`.approval_date as a_date,
                    `tabQuotation`.is_multiple_quotation as is_m,
                    `tabQuotation`.after_discount_cost as adc,
                    `tabQuotation Item`.unit_price as up,
                    `tabQuotation Item`.margin_amount as ma 
                    from `tabQuotation` 
                    left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer") and 
                    `tabQuotation Item`.wod_no = '%s' and 
                    `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
                    and transaction_date between '%s' and '%s' ''' %(j.name,from_date,to_date),as_dict=1)

                    if q_amt:
                        # frappe.errprint(i.name)
                        if q_amt[0]["is_m"] == 1:
                            per = (q_amt[0]["up"] * q_amt[0]["dis"])/100
                            q_amt = q_amt[0]["up"] - per
                            q_m = q_m + q_amt

                        else:
                            q_amt = q_amt[0]["adc"]
                            q_m = q_m + q_amt
                            

                    
                    q_amt_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                    `tabQuotation`.default_discount_percentage as dis,
                    `tabQuotation`.approval_date as a_date,
                    `tabQuotation`.is_multiple_quotation as is_m,
                    `tabQuotation`.after_discount_cost as adc,
                    `tabQuotation`.Workflow_state,
                    `tabQuotation Item`.unit_price as up,
                    `tabQuotation Item`.margin_amount as ma from `tabQuotation` 
                    left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    where `tabQuotation`.Workflow_state in ("Approved By Customer") and
                    `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")
                    and `tabQuotation Item`.wod_no = '%s' 
                    and approval_date between '%s' and '%s' ''' %(j.name,from_date,to_date) ,as_dict=1)

                    if q_amt_2:
                        if q_amt_2[0]["is_m"] == 1:
                            per = (q_amt_2[0]["up"] * q_amt_2[0]["dis"])/100
                            q_amt_2 = q_amt_2[0]["up"] - per
                            q_m_2 = q_m_2 + q_amt_2

                        else:
                            q_amt_2 = q_amt_2[0]["adc"]
                            q_m_2 = q_m_2 + q_amt_2

                
                    
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(round(q_m )or 0)
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(round(q_m_2,2) or 0)
                if not q_m or not q_m_2:
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %("0")
                else:
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(round((q_m_2/q_m)*100,2))
                    


                data += '</tr>'
        
            data += '<tr>'
            data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>-</b><center></td>'
            data += '</tr>'

    data += '</table>'

    return data

