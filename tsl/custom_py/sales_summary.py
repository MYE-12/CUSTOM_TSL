import frappe
import json
from frappe.utils import (
    add_days,
    add_months,
    cint,
    date_diff,
    flt,
    get_first_day,
    get_last_day,
    get_link_to_form,
    getdate,
    rounded,
    today,
)
from frappe.utils.file_manager import save_file
from frappe.utils.file_manager import get_file
from frappe.utils import add_to_date
import requests
from datetime import datetime
from erpnext.setup.utils import get_exchange_rate
from frappe.utils.csvutils import read_csv_content


@frappe.whitelist()
def get_wod(from_date,to_date,company):
    d = datetime.now().date()
    ogdate = datetime.strptime(str(d),"%Y-%m-%d")

    # Format the date as a string in the desired format
    formatted_date = ogdate.strftime("%d-%m-%Y")

    data = ''
    data += '<div class="table-container">'
    data += '<table class="table table-bordered" width: 100%;>'
    data += '<tr>'
    data += '<td colspan = 3 style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="300"></td>'
    data += '<td colspan = 3 style="border-color:#000000;"><h2><center><b>TSL Company<br>Branch - Kuwait</b></center></h2></td>'
    data += '<td colspan = 3 style="border-color:#000000;"><center><img src = "/files/kuwait flag.jpg" width ="100"></center></td>'
    
    data += '</tr>'

    data += '<tr>'
    data += '<td colspan = 4 style="border-color:#000000;"><b>RSI,RSC & Quoted Summary</b></td>'
    data += '<td colspan = 5 align = right style="border-left:hidden;border-color:#000000;"><b>Generation Date : %s</b></td>' %(formatted_date)
       
    data += '</tr>'

    data += '<tr>'
    data += '<td colspan = 1 style="border-color:#000000;background-color:#0e86d4;"><center><b></b></center></td>'
    data += '<td colspan = 2 style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">Total Amount(RSI)</b></center></td>'
    data += '<td colspan = 2 style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">Total Amount(RSC)</b></center></td>'
    data += '<td colspan = 2 style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">Total Amount(RS)</b></center></td>'
    data += '<td colspan = 2 style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">Total Amount(Quoted)</b></center></td>'
    
    data += '</tr>'
    wo = frappe.db.sql(""" select DISTINCT sales_rep from `tabWork Order Data` where company = '%s' """ %(company) ,as_dict =1)
    data += '<tr>'
    data += '<td style="border-color:#000000;width:10%;background-color:#0e86d4;color:white;"><center><b style="color:white;">Salesman</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;background-color:#0e86d4;color:white;"><center><b style="color:white;">WO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;background-color:#0e86d4;color:white;"><center><b style="color:white;">SO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;background-color:#0e86d4;color:white;"><center><b style="color:white;">WO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;background-color:#0e86d4;color:white;"><center><b style="color:white;">SO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;background-color:#0e86d4;color:white;"><center><b style="color:white;">WO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;background-color:#0e86d4;color:white;"><center><b style="color:white;">SO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;background-color:#0e86d4;color:white;"><center><b style="color:white;">WO(in KD)</b></center></td>'  
    data += '<td style="border-color:#000000;width:10%;background-color:#0e86d4;color:white;"><center><b style="color:white;">SO(in KD)</b></center></td>'	
    data += '</tr>'
    current_date_time = datetime.now()

    # Extract and print the current date
    current_date = to_date
    # Week_start = add_days(current_date,-6)
    Week_start = from_date

    total_rsi = 0
    total_rsc = 0
    total_rs = 0
    total_quot = 0

    s_invoiced = 0
    s_delivered = 0
    s_received = 0
    sup_quoted_sod = 0
    
    for i in wo:
        if not i["sales_rep"] == None:
            if not i["sales_rep"] == 'Sales Team' and not i["sales_rep"] == 'Walkin' and not i["sales_rep"] == 'OMAR' and not i["sales_rep"] == '' and not i["sales_rep"] == 'Mazz':   
                gt = 0
                sales = frappe.get_value("Sales Person",i["sales_rep"],["user","name"])
                
                #RSI - wd
                gr = frappe.get_all("Sales Invoice",{"department":"Repair - TSL","status": ["in", ["Unpaid","Overdue","Partly Paid"]],"sales_rep":sales[0]},["*"])
                for i in gr:
                    gt = gt + i.outstanding_amount
                
                #Invcd - sod

                st = 0
                sr = frappe.get_all("Sales Invoice",{"department":"Supply - TSL","status": ["in", ["Unpaid","Overdue","Partly Paid"]],"sales_rep":sales[0]},["*"])
                for i in sr:
                    st = st + i.outstanding_amount

                #RSC - wd
                wds_rsc = frappe.get_all("Work Order Data",{"sales_rep":sales[1],"status":"RSC-Repaired and Shipped Client","posting_date": ["between", (Week_start,current_date)]},["*"])
                q_m = 0
                q_m_2 = 0
                for j in wds_rsc:
                    frappe.errprint(j.name)
                    q_amt = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma 
                        from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where  `tabQuotation`.Workflow_state in ("Approved By Customer") and 
                        `tabQuotation Item`.wod_no = '%s' and 
                        `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date),as_dict=1)

                    if q_amt:
                        # frappe.errprint(i.name)
                        if q_amt[0]["is_m"] == 1:
                            per = (q_amt[0]["up"] * q_amt[0]["dis"])/100
                            q_amt = q_amt[0]["up"] - per
                            q_m = q_m + q_amt

                        else:
                            q_amt = q_amt[0]["adc"]
                            q_m = q_m + q_amt
                            
                    else:
                        
                        q_amt_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation`.Workflow_state,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where `tabQuotation`.Workflow_state in ("Quoted to Customer") and
                        `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")
                        and `tabQuotation Item`.wod_no = '%s' 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date) ,as_dict=1)

                        if q_amt_2:
                            if q_amt_2[0]["is_m"] == 1:
                                per = (q_amt_2[0]["up"] * q_amt_2[0]["dis"])/100
                                q_amt_2 = q_amt_2[0]["up"] - per
                                q_m_2 = q_m_2 + q_amt_2

                            else:
                                q_amt_2 = q_amt_2[0]["adc"]
                                q_m_2 = q_m_2 + q_amt_2

                #RSC-old
                rsc_old = 0
                for i in wds_rsc:
                    rsc_old = rsc_old + i.old_wo_q_amount
            
                rsc_total = q_m + q_m_2 + rsc_old

                   
                #Delivered
                sup_in = frappe.get_all("Supply Order Data",{"sales_rep":sales[1],"status":"Delivered","posting_date": ["between", (Week_start,current_date)]})
                sp_del =0
                sp_del_2 =0
                for j in sup_in:
                    sup_qamt_del = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma 
                        from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where  `tabQuotation`.Workflow_state in ("Approved By Customer") and 
                        `tabQuotation Item`.supply_order_data = '%s' and 
                        `tabQuotation`.quotation_type in ("Customer Quotation - Supply","Revised Quotation - Supply") 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date),as_dict=1)

                    if sup_qamt_del:
                        # frappe.errprint(i.name)
                        if sup_qamt_del[0]["is_m"] == 1:
                            per = (sup_qamt_del[0]["up"] * sup_qamt_del[0]["dis"])/100
                            q_amt = sup_qamt_del[0]["up"] - per
                            sp_del = sp_del + q_amt

                        else:
                            q_amt = sup_qamt_del[0]["adc"]
                            sp_del = sp_del + q_amt
                            
                    else:
                        
                        sup_qamt_del_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation`.Workflow_state,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where `tabQuotation`.Workflow_state in ("Quoted to Customer") and
                        `tabQuotation`.quotation_type in ("Customer Quotation - Supply","Revised Quotation - Supply")
                        and `tabQuotation Item`.supply_order_data = '%s' 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date) ,as_dict=1)

                        if sup_qamt_del_2:
                            if sup_qamt_del_2[0]["is_m"] == 1:
                                per = (sup_qamt_del_2[0]["up"] * sup_qamt_del_2[0]["dis"])/100
                                q_amt_2 = sup_qamt_del_2[0]["up"] - per
                                sp_del_2 = sp_del_2 + q_amt_2

                            else:
                                q_amt_2 = sup_qamt_del_2[0]["adc"]
                                sp_del_2 = sp_del_2 + q_amt_2
     
                
            
                s_del_total = sp_del + sp_del_2

                #RS				
                wds_rs = frappe.get_all("Work Order Data",{"sales_rep":sales[1],"status":"RS-Repaired and Shipped","posting_date": ["between", (Week_start,current_date)]},["*"])
                
                rs_am = 0
                rs_am_2 = 0
                for j in wds_rs:
                    rs_qamt = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma 
                        from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where  `tabQuotation`.Workflow_state in ("Approved By Customer") and 
                        `tabQuotation Item`.wod_no = '%s' and 
                        `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date),as_dict=1)

                    if rs_qamt:
                        # frappe.errprint(i.name)
                        if rs_qamt[0]["is_m"] == 1:
                            per = (rs_qamt[0]["up"] * rs_qamt[0]["dis"])/100
                            q_amt = rs_qamt[0]["up"] - per
                            rs_am = rs_am + q_amt

                        else:
                            q_amt = rs_qamt[0]["adc"]
                            rs_am = rs_am + q_amt
                            
                    else:
                        
                        rs_qamt_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation`.Workflow_state,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where `tabQuotation`.Workflow_state in ("Quoted to Customer") and
                        `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")
                        and `tabQuotation Item`.wod_no = '%s' 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date) ,as_dict=1)

                        if rs_qamt_2:
                            if rs_qamt_2[0]["is_m"] == 1:
                                per = (rs_qamt_2[0]["up"] * rs_qamt_2[0]["dis"])/100
                                q_amt_2 = rs_qamt_2[0]["up"] - per
                                rs_am_2 = rs_am_2 + q_amt_2

                            else:
                                q_amt_2 = rs_qamt_2[0]["adc"]
                                rs_am_2= rs_am_2 + q_amt_2
     
                        
                #rs-old
                rs_old = 0
                for i in wds_rs:
                    rs_old = rs_old + i.old_wo_q_amount
              
                rs_total = rs_am + rs_am_2 + rs_old



                #Received
                sup_rec = frappe.get_all("Supply Order Data",{"sales_rep":sales[1],"status":"Received","posting_date": ["between", (Week_start,current_date)]})

                sp_rec =0
                sp_rec_2 =0
                for j in sup_rec:
                    sup_qamt_rec = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.qty as qty,
                        `tabQuotation Item`.margin_amount as ma 
                        from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where  `tabQuotation`.Workflow_state in ("Approved By Customer") and 
                        `tabQuotation Item`.supply_order_data = '%s' and 
                        `tabQuotation`.quotation_type in ("Customer Quotation - Supply","Revised Quotation - Supply") 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date),as_dict=1)

                    if sup_qamt_rec:
                        # frappe.errprint(i.name)
                        if sup_qamt_rec[0]["is_m"] == 1:
                            per = (sup_qamt_rec[0]["up"] * sup_qamt_rec[0]["dis"])/100
                            q_amt = (sup_qamt_rec[0]["up"] - per) * sup_qamt_rec[0]["qty"]
                            sp_rec = sp_rec + q_amt

                        else:
                            q_amt = sup_qamt_rec[0]["adc"]
                            sp_rec = sp_rec + q_amt
                            
                    else:
                        sup_qamt_rec_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation`.Workflow_state,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where `tabQuotation`.Workflow_state in ("Quoted to Customer") and
                        `tabQuotation`.quotation_type in ("Customer Quotation - Supply","Revised Quotation - Supply")
                        and `tabQuotation Item`.supply_order_data = '%s' 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date) ,as_dict=1)

                        if sup_qamt_rec_2:
                            if sup_qamt_rec_2[0]["is_m"] == 1:
                                per = (sup_qamt_rec_2[0]["up"] * sup_qamt_rec_2[0]["dis"])/100
                                q_amt_2 = (sup_qamt_rec_2[0]["up"] - per) * sup_qamt_rec_2[0]["qty"]
                                sp_rec = sp_rec + q_amt_2

                            else:
                                q_amt_2 = sup_qamt_rec_2[0]["adc"]
                                sp_rec_2 = sp_rec_2 + q_amt_2
     
                
            
                
                s_rec_total =sp_rec + sp_rec_2

                #q-quoted-wd
                
                wds_quot = frappe.get_all("Work Order Data",{"sales_rep":sales[1],"status":"Q-Quoted","posting_date": ["between", (Week_start,current_date)]},["*"])
                quot_am = 0
                quot_am_2 = 0
                for j in wds_quot:
                    
                    q_amt_q = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma 
                        from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where  `tabQuotation`.Workflow_state in ("Approved By Customer") and 
                        `tabQuotation Item`.wod_no = '%s' and 
                        `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date),as_dict=1)

                    if q_amt_q:
                        # frappe.errprint(i.name)
                        if q_amt_q[0]["is_m"] == 1:
                            per = (q_amt_q[0]["up"] * q_amt_q[0]["dis"])/100
                            t_q_amt = q_amt_q[0]["up"] - per
                            quot_am = quot_am + t_q_amt

                        else:
                            t_q_amt = q_amt_q[0]["adc"]
                            quot_am = quot_am + t_q_amt
                            
                    else:
                        q_amt_q_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation`.Workflow_state,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where `tabQuotation`.Workflow_state in ("Quoted to Customer") and
                        `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")
                        and `tabQuotation Item`.wod_no = '%s' 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date) ,as_dict=1)

                        if q_amt_q_2:
                            if q_amt_q_2[0]["is_m"] == 1:
                                per = (q_amt_q_2[0]["up"] * q_amt_q_2[0]["dis"])/100
                                t_q_amt = q_amt_q_2[0]["up"] - per
                                quot_am_2 = quot_am_2 + t_q_amt

                            else:
                                t_q_amt = q_amt_q_2[0]["adc"]
                                quot_am_2 = quot_am_2 + t_q_amt

                

                #quoted-old
                q_old = 0
                for i in wds_quot:
                    q_old = q_old + i.old_wo_q_amount
             
                wd_total_quot =   quot_am + quot_am_2 + q_old


                #Quoted-sod
                sup_quoted= frappe.get_all("Supply Order Data",{"sales_rep":sales[1],"status":"Quoted","posting_date": ["between", (Week_start,current_date)]})

                sp_qted =0
                sp_qted_2 =0
                for j in sup_quoted:
                    sup_qamt_qted = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.qty as qty,
                        `tabQuotation Item`.margin_amount as ma 
                        from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where  `tabQuotation`.Workflow_state in ("Approved By Customer") and 
                        `tabQuotation Item`.supply_order_data = '%s' and 
                        `tabQuotation`.quotation_type in ("Customer Quotation - Supply","Revised Quotation - Supply") 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date),as_dict=1)

                    if sup_qamt_qted:
                        if sup_qamt_qted[0]["is_m"] == 1:
                            for k in sup_qamt_qted:
                                per = (k.up * k.dis)/100
                                q_amt = (k.up - per) * k.qty
                                sp_qted = sp_qted + q_amt

                        else:
                            q_amt = sup_qamt_qted[0]["adc"]
                            sp_qted = sp_qted + q_amt
                            
                    else:
                        
                        sup_qamt_qted_2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                        `tabQuotation`.default_discount_percentage as dis,
                        `tabQuotation`.approval_date as a_date,
                        `tabQuotation`.is_multiple_quotation as is_m,
                        `tabQuotation`.after_discount_cost as adc,
                        `tabQuotation`.Workflow_state,
                        `tabQuotation Item`.qty as qty,
                        `tabQuotation Item`.unit_price as up,
                        `tabQuotation Item`.margin_amount as ma from `tabQuotation` 
                        left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                        where `tabQuotation`.Workflow_state in ("Quoted to Customer") and
                        `tabQuotation`.quotation_type in ("Customer Quotation - Supply","Revised Quotation - Supply")
                        and `tabQuotation Item`.supply_order_data = '%s' 
                        and transaction_date between '%s' and '%s' ''' %(j.name,Week_start,current_date) ,as_dict=1)

                        if sup_qamt_qted_2:
                            if sup_qamt_qted_2[0]["is_m"] == 1:
                                for k in sup_qamt_qted_2:
                                    per = (k.up * k.dis)/100
                                    q_amt_2 = (k.up - per)  * k.qty
                                    sp_qted_2 = sp_qted_2 + q_amt_2

                            else:
                                q_amt_2 = sup_qamt_qted_2[0]["adc"]
                                sp_qted_2 = sp_qted_2 + q_amt_2
     
                
            
                
                sup_quoted_total = sp_qted + sp_qted_2


                data += '<tr>'
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %(sales[1])
                gt = round(gt)
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %("{:,.2f}".format(gt))
                st =round(st)
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %("{:,.2f}".format(st))
                # total_rsc = total_rsc + rsc_total
                rsc_total = round(rsc_total)
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %("{:,.2f}".format(rsc_total))
                s_del_total = round(s_del_total)
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %("{:,.2f}".format(s_del_total))
                rs_total = round(rs_total)
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %("{:,.2f}".format(rs_total))
                s_rec_total = round(s_rec_total)
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %("{:,.2f}".format(s_rec_total)) 
                wd_total_quot = round(wd_total_quot)
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %("{:,.2f}".format(wd_total_quot))
                sup_quoted_total = round(sup_quoted_total)
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>'	 %("{:,.2f}".format(sup_quoted_total))
                # data += '</tr>'


                total_rsi = total_rsi + gt
                total_rsc = total_rsc + rsc_total
                total_rs = total_rs + rs_total 
                total_quot = total_quot + wd_total_quot

                s_invoiced = s_invoiced + st
                s_delivered = s_delivered + s_del_total
                s_received = s_received + s_rec_total
                sup_quoted_sod = sup_quoted_sod + sup_quoted_total

    total_rsi = round(total_rsi)
    s_invoiced = round(s_invoiced)
    total_rsc = round(total_rsc)
    s_delivered = round(s_delivered)
    total_rs = round(total_rs)
    s_received = round(s_received)
    total_quot = round(total_quot)
    sup_quoted_sod = round(sup_quoted_sod)
    data += '<tr>'
    data += '<td style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">Total</b></center></td>'
    data += '<td style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">%s</b></center></td>' %("{:,.2f}".format(total_rsi)) 
    data += '<td style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">%s</b></center></td>'  %("{:,.2f}".format(s_invoiced))
    data += '<td style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">%s</b></center></td>'  %("{:,.2f}".format(total_rsc))
    data += '<td style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">%s</b></center></td>'  %("{:,.2f}".format(s_delivered))
    data += '<td style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">%s</b></center></td>'  %("{:,.2f}".format(total_rs))
    data += '<td style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">%s</b></center></td>' %("{:,.2f}".format(s_received))
    data += '<td style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">%s</b></center></td>' %("{:,.2f}".format(total_quot)) 
    data += '<td style="border-color:#000000;background-color:#0e86d4;color:white;"><center><b style="color:white;">%s</b></center></td>' %("{:,.2f}".format(sup_quoted_sod))
    data += '</tr>'

    data += '</table>'
    data += '</div>'
    
    return data
