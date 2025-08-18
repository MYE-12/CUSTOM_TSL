# Copyright (c) 2025, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from frappe.utils.background_jobs import enqueue
import calendar

class LabReportSummary(Document):
    @frappe.whitelist()
    def get_data(self):
        data= ""
        data += """
        <style>
            /* Overall Report Container */
            .report-container {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px auto;
                padding: 20px;
                max-width: 1200px;
                background-color: #f8f9fa;
                border-radius: 18px;
                box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
            }

            /* Report Header */
            .report-header {
                background: linear-gradient(135deg, #1565c0, #0d47a1);
                color: white;
                padding: 35px;
                text-align: center;
                font-size: 4.2em;
                font-weight: 800;
                border-radius: 15px;
                margin-bottom: 35px;
                box-shadow: 0 6px 25px rgba(0, 0, 0, 0.25);
                letter-spacing: 1px;
            }

            /* Summary Cards */
            .summary-card {
                background-color: #ffffff;
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
                padding: 28px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .summary-card:hover {
                transform: translateY(-6px);
                box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
            }

            /* Table Styling */
            .summary-card table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 18px;
            }
            
            .summary-card th, .summary-card td {
                padding: 16px;
                text-align: center;
                border-bottom: 1px solid #e9ecef;
                border-right: 1px solid #e9ecef;
                font-size: 1em;
                color: #343a40;
            }

            .summary-card th:first-child, .summary-card td:first-child {
                border-left: 1px solid #e9ecef;
            }
            
            .summary-card th {
                background: linear-gradient(90deg, #3949ab, #5c6bc0);
                color: #ffffff;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                font-size: 1.1em;
            }

            .summary-card tr:nth-child(even) {
                background-color: #f5f7fa;
            }

            .summary-card tr:hover {
                background-color: #e3f2fd;
                transition: background-color 0.25s ease;
            }

            /* Metric Cards for KPIs */
            .metric-card-container {
                display: flex;
                justify-content: space-around;
                gap: 22px;
                margin-bottom: 35px;
            }

            .metric-card {
                flex: 1;
                background: #ffffff;
                border-radius: 14px;
                padding: 25px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border-bottom: 6px solid #1565c0;
            }

            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            }

            .metric-card-label {
                font-size: 1.1em;
                color: #6c757d;
                margin-bottom: 12px;
                text-transform: uppercase;
                font-weight: 600;
            }

            .metric-card-value {
                font-size: 2.8em;
                font-weight: bold;
                color: #0d47a1;
            }

            /* Status Badges */
            .status-badge {
                display: inline-block;
                padding: 8px 18px;
                border-radius: 25px;
                color: white;
                font-size: 0.9em;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
            }
            
            .status-ne { background-color: #fb8c00; } 
            .status-ner { background-color: #e53935; }
            .status-rs { background-color: #43a047; }
            .status-tr { background-color: #1e88e5; }
            .status-nr { background-color: #546e7a; }
            .status-rnf { background-color: #ff7043; }
            .status-rnr { background-color: #c62828; }
            .status-default { background-color: #9e9e9e; }

            /* Progress Bar */
            .progress-container {
                width: 85%;
                background-color: #e9ecef;
                border-radius: 12px;
                margin: 12px auto;
            }

            .progress-bar {
                height: 18px;
                border-radius: 12px;
                color: white;
                padding-right: 5px;
                line-height: 18px;
                text-align: right;
                transition: width 0.5s ease-in-out;
            }

            .progress-green { background-color: #43a047; }
            .progress-blue { background-color: #1e88e5; }
            .progress-orange { background-color: #fb8c00; }

            /* Status Dots */
            .status-dot {
                height: 12px;
                width: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 6px;
                vertical-align: middle;
            }

            .dot-green { background-color: #43a047; }
            .dot-red { background-color: #e53935; }
            .dot-orange { background-color: #fb8c00; }
        </style>

        """
        data += '<div class="report-container">'
        data += '<div class="report-header">Lab Report</div>'
        data += '<div class="summary-card">'
        # data += '<div class="table-container">'
        # data += '<h3><b><center>WORK ORDER<center><b><h3>'
        data += '<table class="table table-bordered">'
        # data += '<tr>'
        # data += '<td style="width:30%;border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="180"></td>'
        # if self.company == "TSL COMPANY - Kuwait":  
        #     data += '<td style="width:70%;border-color:#000000;color:#055c9d;"><h3><center><b style="color:#055c9d;">TSL Company<br>Branch - Kuwait</b></center></h3></td>' 
        # data += '</tr>'

        # data += '<tr>'


        # data += '<td colspan = 4 style="border-color:#000000;color:#055c9d;"><h3><center><b style="color:#055c9d;">Lab Report</b></center></h3></td>' 
        # data += '</tr>'
        data += '</table>'


        data += '<table class="table table-bordered">'
        data += '<tr>'

        data += '<td colspan = 6 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;font-size:12px;">Overall Summary</b></center></td>' 


        data += '</tr>'      

        data += '<tr>'

        data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;"></b></center></td>'   
        data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Metrics</b></center></td>' 
        data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Status / Metrics</b></center></td>' 
        # data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Current Week</b></center></td>' 
        # data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Current Month</b></center></td>' 
        data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">2025 Cumulative</b></center></td>' 
       
        data += '</tr>'
        
        today = date.today()

        # Sunday as the start of the week
        
        s_week = today - timedelta(days=6)
        e_week = today


        s_month = date(today.year, today.month, 1)

        # last day of current month
        last_day = calendar.monthrange(today.year, today.month)[1]
        e_month = date(today.year, today.month, last_day)
        
        # First day of current year
        first_day = date(today.year, 1, 1)

        # Last day of current year
        last_day = date(today.year, 12, 31)

        # Format for SQL
        s_year = first_day.strftime("%Y-%m-%d")
        e_year = last_day.strftime("%Y-%m-%d")

        if self.period == "Yearly":
            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Input</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">WO Received</td>' 
            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NE</td>' 
           
            wo_count_yearly = frappe.db.count("Work Order Data",{"company":self.company,"posting_date": ["between", [s_year,e_year]]})

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(wo_count_yearly) 
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. WO per Technician</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            
            tech_count = frappe.db.sql("""
            SELECT COUNT(DISTINCT technician) as ct
            FROM `tabWork Order Data`
            WHERE company = '%s' 
            AND technician IS NOT NULL 
            """ %(self.company),as_dict=1)

        
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(wo_count_yearly/tech_count[0]['ct']) 
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Returned WO</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">-</td>' 

            ner_wo_count_yearly = frappe.db.count("Work Order Data",{"company":self.company,"status_cap_date": ["between", [s_year,e_year]],"status":"NER-Need Evaluation Return"})
            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_wo_count_yearly)
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Output</td>' 
            

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Completed WO</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>'

           
            rs_yearly = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_year,e_year) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(rs_yearly[0]["ct"])
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Completed NER</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NER</td>' 


                     
            ner_yearly = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s'
            and `tabWork Order Data`.status_cap = "NER-Need Evaluation Return" 
            and  date(`tabStatus Duration Details`.date) > `tabWork Order Data`.status_cap_date """ %(self.company,s_year,e_year) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>'  %(ner_yearly[0]["ct"]) 
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Pending WO</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">RS</td>' 

            # tr_count_weekly = frappe.db.count("Work Order Data",{"status":"TR-Technician Repair","company":self.company,"posting_date": ["between", [s_week,e_week]]})
                        
            tr_count_yearly  = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "TR-Technician Repair" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_year,e_year) ,as_dict=1)
        
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(tr_count_yearly[0]["wd"])

            data += '</tr>'

            
            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Not Repairable WO</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">RNR/RNF</td>'
            # not_repaired_count_weekly = frappe.db.count("Work Order Data",{"status": ["in", ["RNR-Return Not Repaired","RNF-Return No Fault"]],"company":self.company,"posting_date": ["between", [s_week,e_week]]})

           
            not_repaired_count_yearly  = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where `tabStatus Duration Details`.status IN ("RNF-Return No Fault","RNR-Return Not Repaired") and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_year,e_year) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>'  %(not_repaired_count_yearly[0]["ct"]) 
            data += '</tr>'




            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Waiting Time</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NE Time</td>'
            
           
            wo_list_time_yr = frappe.get_all("Evaluation Report",{"company":self.company,"date": ["between", [s_year,e_year]]},["work_order_data"])
            wo_list_time_yr_count = frappe.db.count("Evaluation Report",{"company":self.company,"date": ["between", [s_year,e_year]]},["work_order_data"])
            total_hrs_ne_y = 0
            for i in  wo_list_time_yr:
            
                ne = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "NE-Need Evaluation"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.work_order_data),as_dict=1)

                ue = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.work_order_data),as_dict=1)
                if ne and ue:
                    hr = ue[0]['date'] - ne[0]['date']
                    hours = hr.total_seconds() / 3600
                    total_hrs_ne_y = total_hrs_ne_y + round(hours,2)

            ne_time_ratio_yr = (total_hrs_ne_y/wo_list_time_yr_count)/24
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(total_hrs_ne_y,2))
            
            data += '</tr>'

            # data += '<tr>'
            # data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            # data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg.Response time</td>' 
            # data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NER Time</td>' 
            
            # total_hrs_ner = 0
            # for i in  wo_list_time:
            
            #     ne = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
            #     left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            #     where  `tabStatus Duration Details`.status = "NE-Need Evaluation"
            #     and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.name),as_dict=1)

            #     ue = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
            #     left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            #     where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
            #     and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.name),as_dict=1)
            #     if ne and ue:
            #         hr = ue[0]['date'] - ne[0]['date']
            #         hours = hr.total_seconds() / 3600
            #         total_hrs_ner = total_hrs_ner + round(hours,2)


            # ner_time_ratio = (total_hrs_ner/wo_count_weekly)/24

            # # data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            # # data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            # data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            # data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">TR Time</td>' 

            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '</tr>'


            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Processing Time</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. Evaluation Time</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">UE Time</td>' 

            

            total_eval_time_year = frappe.db.sql("""
            SELECT SUM(er.evaluation_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s
            """, (s_year,e_year), as_dict=1)
            
            hours = total_eval_time_year[0]['total_time'] / 3600
            eval_time_year = hours/24

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(eval_time_year,2)) 
            
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. Repair Time</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">UTR Time</td>' 
                       
            total_rep_time_year = frappe.db.sql("""
            SELECT SUM(er.estimated_repair_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s
            """, (s_year,e_year), as_dict=1)
            
            hours = total_rep_time_year[0]['total_time'] / 3600
            rep_time_year = hours/24

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>'  %(round(rep_time_year,2)) 
            data += '</tr>'


            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. RS Value</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">-</td>' 

           
          
            rs_y = frappe.db.sql(""" select DISTINCT `tabWork Order Data`.name as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_year,e_year) ,as_dict=1)
            

            qy = 0
            for i in rs_y:
                qamt_ovrl3 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if qamt_ovrl3:             
                    if qamt_ovrl3[0]["is_m"] == 1:
                        per = (qamt_ovrl3[0]["up"] * qamt_ovrl3[0]["dis"])/100
                        q_amt = qamt_ovrl3[0]["up"] - per
                        qy = qy + q_amt

                    else:
                        q_amt = qamt_ovrl3[0]["adc"]

                        qy = qy + q_amt

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(f"{round(qy,2):,.2f}")
            data += '</tr>'
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Value Metrics</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. NER Value</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">-</td>' 
            
           

            ner_rs_y = frappe.db.sql(""" select DISTINCT `tabWork Order Data`.name as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "NER-Need Evaluation Return" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_year,e_year) ,as_dict=1)
            

            ner_qy = 0
            for i in ner_rs_y:
                qamt_ovrl3 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if qamt_ovrl3:             
                    if qamt_ovrl3[0]["is_m"] == 1:
                        per = (qamt_ovrl3[0]["up"] * qamt_ovrl3[0]["dis"])/100
                        q_amt = qamt_ovrl3[0]["up"] - per
                        ner_qy  = ner_qy  + q_amt

                    else:
                        q_amt = qamt_ovrl3[0]["adc"]

                        ner_qy  = ner_qy  + q_amt

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(f"{round(ner_qy,2):,.2f}")

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">No. of Pre-Evaluation Quotes</td>' 

            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">-</td>' 
           
            pre_wods_y = frappe.db.sql(''' select 
            count(DISTINCT `tabQuotation Item`.wod_no) as cnt
            from `tabQuotation` 
            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
            LEFT JOIN `tabWork Order Data` wod ON `tabQuotation Item`.wod_no = wod.name
            where `tabQuotation`.Workflow_state in ("Approved By Management") and
            `tabQuotation`.quotation_type in ("Internal Quotation - Repair") 
            and `tabQuotation`.transaction_date between '%s' and '%s' and `tabQuotation`.company = '%s' and  `tabQuotation`.pre_evaluation = 1 ''' %(s_year,e_year,self.company),as_dict=1)

            
            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(pre_wods_y[0]["cnt"])
            data += '</tr>'                
            data += '</table>'
            data += '</div>'
            data += '</div>'
            data += '</div>'

            return data

        else:
            data += '<table class="table table-bordered">'
            data += '<tr>'

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;"></b></center></td>'   
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Metrics</b></center></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Status / Metrics</b></center></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Current Week</b></center></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Current Month</b></center></td>' 
          
        
            data += '</tr>'
            
            today = date.today()

            # Sunday as the start of the week
            
            s_week = today - timedelta(days=6)
            e_week = today


            s_month = date(today.year, today.month, 1)

            # last day of current month
            last_day = calendar.monthrange(today.year, today.month)[1]
            e_month = date(today.year, today.month, last_day)
            
            # First day of current year
            first_day = date(today.year, 1, 1)

            # Last day of current year
            last_day = date(today.year, 12, 31)

            # Format for SQL
            s_year = first_day.strftime("%Y-%m-%d")
            e_year = last_day.strftime("%Y-%m-%d")
            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Input</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">WO Received</td>' 
            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NE</td>' 

            wo_count_weekly = frappe.db.count("Work Order Data",{"company":self.company,"posting_date": ["between", [s_week,e_week]]})

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(wo_count_weekly)
            
            wo_count_monthly = frappe.db.count("Work Order Data",{"company":self.company,"posting_date": ["between", [s_month,e_month]]})

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(wo_count_monthly) 
            
          
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. WO per Technician</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            
            tech_count = frappe.db.sql("""
            SELECT COUNT(DISTINCT technician) as ct
            FROM `tabWork Order Data`
            WHERE company = '%s' 
            AND technician IS NOT NULL 
            """ %(self.company),as_dict=1)

        

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(wo_count_weekly/tech_count[0]['ct']) 
            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(wo_count_monthly/tech_count[0]['ct']) 
           
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Returned WO</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">-</td>' 

            ner_wo_count_weekly = frappe.db.count("Work Order Data",{"company":self.company,"status_cap_date": ["between", [s_week,e_week]],"status":"NER-Need Evaluation Return"})

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>'%(ner_wo_count_weekly) 
            
            ner_wo_count_monthly = frappe.db.count("Work Order Data",{"company":self.company,"status_cap_date": ["between", [s_month,e_month]],"status":"NER-Need Evaluation Return"})

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_wo_count_monthly)

            
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Output</td>' 
            

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Completed WO</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>'

            rs = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_week,e_week) ,as_dict=1)


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(rs[0]['ct']) 

            rs_monthly = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_month,e_month) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(rs_monthly[0]["ct"])

            
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Completed NER</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NER</td>' 


            ner = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s'
            and `tabWork Order Data`.status_cap = "NER-Need Evaluation Return" 
            and  date(`tabStatus Duration Details`.date) > `tabWork Order Data`.status_cap_date """ %(self.company,s_week,e_week) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner[0]['ct']) 
        
            ner_monthly = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s'
            and `tabWork Order Data`.status_cap = "NER-Need Evaluation Return" 
            and  date(`tabStatus Duration Details`.date) > `tabWork Order Data`.status_cap_date """ %(self.company,s_month,e_month) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_monthly[0]["ct"]) 
            
          
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Pending WO</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">RS</td>' 

            # tr_count_weekly = frappe.db.count("Work Order Data",{"status":"TR-Technician Repair","company":self.company,"posting_date": ["between", [s_week,e_week]]})
            
            tr_count_weekly  = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "TR-Technician Repair" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_week,e_week) ,as_dict=1)
        
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(tr_count_weekly[0]["wd"])

            tr_count_monthly  = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "TR-Technician Repair" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_month,e_month) ,as_dict=1)
        
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(tr_count_monthly[0]["wd"])
            
            data += '</tr>'

            
            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Not Repairable WO</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">RNR/RNF</td>'
            # not_repaired_count_weekly = frappe.db.count("Work Order Data",{"status": ["in", ["RNR-Return Not Repaired","RNF-Return No Fault"]],"company":self.company,"posting_date": ["between", [s_week,e_week]]})

            not_repaired_count_weekly  = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where `tabStatus Duration Details`.status IN ("RNF-Return No Fault","RNR-Return Not Repaired") and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_week,e_week) ,as_dict=1)


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(not_repaired_count_weekly[0]["ct"]) 
            
            not_repaired_count_monthly  = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where `tabStatus Duration Details`.status IN ("RNF-Return No Fault","RNR-Return Not Repaired") and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_month,e_month) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(not_repaired_count_monthly[0]["ct"]) 

            data += '</tr>'




            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Waiting Time</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NE Time</td>'
            
            wo_list_time = frappe.get_all("Evaluation Report",{"company":self.company,"date": ["between", [s_week,e_week]]},["work_order_data"])
            wo_list_time_count_w = frappe.db.count("Evaluation Report",{"company":self.company,"date": ["between", [s_week,e_week]]},["work_order_data"])
            total_hrs_ne = 0
            for i in  wo_list_time:
            
                ne = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "NE-Need Evaluation"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1 """ %(i.work_order_data),as_dict=1)

                ue = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.work_order_data),as_dict=1)
                if ne and ue:
                    hr = ue[0]['date'] - ne[0]['date']
                    hours = hr.total_seconds() / 3600
                    total_hrs_ne = total_hrs_ne + round(hours,2)

            ne_time_ratio = (total_hrs_ne/wo_list_time_count_w)/24

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(ne_time_ratio,2))

            wo_list_time_month = frappe.get_all("Evaluation Report",{"company":self.company,"date": ["between", [s_month,e_month]]},["work_order_data"])
            wo_list_time_month_count = frappe.db.count("Evaluation Report",{"company":self.company,"date": ["between", [s_month,e_month]]},["work_order_data"])
            total_hrs_ne_m = 0
            for i in  wo_list_time_month:
            
                ne = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "NE-Need Evaluation"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.work_order_data),as_dict=1)

                ue = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.work_order_data),as_dict=1)
                if ne and ue:
                    hr = ue[0]['date'] - ne[0]['date']
                    hours = hr.total_seconds() / 3600
                    total_hrs_ne_m = total_hrs_ne_m + round(hours,2)

            ne_time_ratio_m = (total_hrs_ne_m/wo_list_time_month_count)/24
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(ne_time_ratio_m,2))

           
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg.Response time</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NER Time</td>' 
            
            total_hrs_ner = 0
            for i in  wo_list_time:
            
                ner = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "NER-Need Evaluation Return"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.name),as_dict=1)

                ue = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date desc LIMIT 1""" %(i.name),as_dict=1)
                if ne and ue:
                    hr = ue[0]['date'] - ner[0]['date']
                    hours = hr.total_seconds() / 3600
                    total_hrs_ner = total_hrs_ner + round(hours,2)

            ner_time_ratio = (total_hrs_ner/wo_count_weekly)/24

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_time_ratio)

            total_hrs_ner_m = 0
            for i in  wo_list_time:
            
                ner = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "NER-Need Evaluation Return"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.name),as_dict=1)

                ue = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "UE-Under Evaluation"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date desc LIMIT 1""" %(i.name),as_dict=1)
                if ne and ue:
                    hr = ue[0]['date'] - ner[0]['date']
                    hours = hr.total_seconds() / 3600
                    total_hrs_ner_m = total_hrs_ner_m + round(hours,2)

            ner_time_ratio_m = (total_hrs_ner_m/wo_list_time_count_w)/24

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_time_ratio_m)
            
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">TR Time</td>' 

            total_hrs_tr = 0
            for i in  wo_list_time:
                tr = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "TR-Technician Repair"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.name),as_dict=1)

                utr = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "UTR-Under Technician Repair"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.name),as_dict=1)
                if tr and utr:
                    hr = utr[0]['date'] - tr[0]['date']
                    hours = hr.total_seconds() / 3600
                    total_hrs_tr = total_hrs_tr+ round(hours,2)

            tr_time_ratio = (total_hrs_tr/wo_count_weekly)/24

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(tr_time_ratio,2)) 

            total_hrs_tr_m = 0
            for i in  wo_list_time_month:
                tr = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "TR-Technician Repair"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.name),as_dict=1)

                utr = frappe.db.sql(""" select `tabStatus Duration Details`.date  from `tabWork Order Data` 
                left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
                where  `tabStatus Duration Details`.status = "UTR-Under Technician Repair"
                and `tabWork Order Data`.name = '%s' ORDER BY `tabStatus Duration Details`.date ASC LIMIT 1""" %(i.name),as_dict=1)
                if tr and utr:
                    hr = utr[0]['date'] - tr[0]['date']
                    hours = hr.total_seconds() / 3600
                    total_hrs_tr_m = total_hrs_tr_m + round(hours,2)

            tr_time_ratio_m = (total_hrs_tr_m/wo_count_monthly)/24

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(tr_time_ratio_m,2))
            
            data += '</tr>'


            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Processing Time</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. Evaluation Time</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">UE Time</td>' 

            total_eval_time = frappe.db.sql("""
            SELECT SUM(er.evaluation_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s
            """, (s_week,e_week), as_dict=1)
            
            hours = total_eval_time[0]['total_time'] / 3600
            eval_time = hours/24

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(eval_time,2)) 

            total_eval_time_month = frappe.db.sql("""
            SELECT SUM(er.evaluation_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s
            """, (s_month,e_month), as_dict=1)
            
            hours = total_eval_time_month[0]['total_time'] / 3600
            eval_time_month = hours/24


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>'  %(round(eval_time_month,2)) 

            
           
            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. Repair Time</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">UTR Time</td>' 

            total_rep_time = frappe.db.sql("""
            SELECT SUM(er.estimated_repair_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s
            """, (s_week,e_week), as_dict=1)
            
            hours = total_rep_time[0]['total_time'] / 3600
            rep_time = hours/24
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(rep_time,2)) 

            total_rep_time_month = frappe.db.sql("""
            SELECT SUM(er.estimated_repair_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s
            """, (s_month,e_month), as_dict=1)
            
            hours = total_rep_time_month[0]['total_time'] / 3600
            rep_time_month = hours/24


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(rep_time_month,2)) 
            
          
            data += '</tr>'


            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. RS Value</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">-</td>' 

            rs_w = frappe.db.sql(""" select DISTINCT `tabWork Order Data`.name as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_week,e_week) ,as_dict=1)
        
            qw = 0
            for i in rs_w:
                qamt_ovrl = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if qamt_ovrl:
                                    
                    if qamt_ovrl[0]["is_m"] == 1:
                        per = (qamt_ovrl[0]["up"] * qamt_ovrl[0]["dis"])/100
                        q_amt = qamt_ovrl[0]["up"] - per
                        qw = qw + q_amt

                    else:
                        q_amt = qamt_ovrl[0]["adc"]

                        qw = qw + q_amt

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(f"{round(qw,2):,.2f}") 

            rs_m = frappe.db.sql(""" select DISTINCT `tabWork Order Data`.name as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_month,e_month) ,as_dict=1)
            
            qmm = 0
            for i in rs_m:
                qamt_ovrl2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if qamt_ovrl2:
                                    
                    if qamt_ovrl2[0]["is_m"] == 1:
                        per = (qamt_ovrl2[0]["up"] * qamt_ovrl2[0]["dis"])/100
                        q_amt = qamt_ovrl2[0]["up"] - per
                        qmm= qmm + q_amt

                    else:
                        q_amt = qamt_ovrl2[0]["adc"]

                        qmm= qmm + q_amt


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(f"{round(qmm,2):,.2f}")

            data += '</tr>'

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Value Metrics</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. NER Value</td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">-</td>' 
            
            rs_w_ner = frappe.db.sql(""" select DISTINCT `tabWork Order Data`.name as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "NER-Need Evaluation Return" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_week,e_week) ,as_dict=1)
        
            ner_qw = 0
            for i in rs_w_ner:
                qamt_ovrl = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if qamt_ovrl:
                                    
                    if qamt_ovrl[0]["is_m"] == 1:
                        per = (qamt_ovrl[0]["up"] * qamt_ovrl[0]["dis"])/100
                        q_amt = qamt_ovrl[0]["up"] - per
                        ner_qw = ner_qw + q_amt

                    else:
                        q_amt = qamt_ovrl[0]["adc"]

                        ner_qw = ner_qw + q_amt

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(f"{round(ner_qw,2):,.2f}") 

            ner_rs_m = frappe.db.sql(""" select DISTINCT `tabWork Order Data`.name as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "NER-Need Evaluation Return" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_month,e_month) ,as_dict=1)
            
            ner_q2 = 0
            for i in ner_rs_m:
                qamt_ovrl2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if qamt_ovrl2:
                                    
                    if qamt_ovrl2[0]["is_m"] == 1:
                        per = (qamt_ovrl2[0]["up"] * qamt_ovrl2[0]["dis"])/100
                        q_amt = qamt_ovrl2[0]["up"] - per
                        ner_q2 = ner_q2 + q_amt

                    else:
                        q_amt = qamt_ovrl2[0]["adc"]

                        ner_q2 = ner_q2 + q_amt


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(f"{round(ner_q2,2):,.2f}")

            ner_rs_y = frappe.db.sql(""" select DISTINCT `tabWork Order Data`.name as wd from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "NER-Need Evaluation Return" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' """ %(self.company,s_year,e_year) ,as_dict=1)
            

            
            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center"></td>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">No. of Pre-Evaluation Quotes</td>' 

            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">-</td>' 
            
            pre_wods_w = frappe.db.sql(''' select 
            count(DISTINCT `tabQuotation Item`.wod_no) as cnt
            from `tabQuotation` 
            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
            LEFT JOIN `tabWork Order Data` wod ON `tabQuotation Item`.wod_no = wod.name
            where `tabQuotation`.Workflow_state in ("Approved By Management") and
            `tabQuotation`.quotation_type in ("Internal Quotation - Repair") 
            and `tabQuotation`.transaction_date between '%s' and '%s' and `tabQuotation`.company = '%s' and  `tabQuotation`.pre_evaluation = 1 ''' %(s_week,e_week,self.company),as_dict=1)

            pre_wods_m = frappe.db.sql(''' select 
            count(DISTINCT `tabQuotation Item`.wod_no) as cnt
            from `tabQuotation` 
            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
            LEFT JOIN `tabWork Order Data` wod ON `tabQuotation Item`.wod_no = wod.name
            where `tabQuotation`.Workflow_state in ("Approved By Management") and
            `tabQuotation`.quotation_type in ("Internal Quotation - Repair") 
            and `tabQuotation`.transaction_date between '%s' and '%s' and `tabQuotation`.company = '%s' and  `tabQuotation`.pre_evaluation = 1 ''' %(s_month,e_month,self.company),as_dict=1)


            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(pre_wods_w[0]["cnt"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(pre_wods_m[0]["cnt"])
            # data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(pre_wods_y[0]["cnt"])
            data += '</tr>'                
            data += '</table>'
            data += '</div>'
            data += '</div>'
            data += '</div>'

            return data


    @frappe.whitelist()
    def get_data1(self):
        data = ''
        data += """
        <style>
            /* Overall Report Container */
            .report-container {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px auto;
                padding: 20px;
                max-width: 1200px;
                background-color: #f8f9fa;
                border-radius: 18px;
                box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
            }

            /* Report Header */
            .report-header {
                background: linear-gradient(135deg, #1565c0, #0d47a1);
                color: white;
                padding: 35px;
                text-align: center;
                font-size: 4.2em;
                font-weight: 800;
                border-radius: 15px;
                margin-bottom: 35px;
                box-shadow: 0 6px 25px rgba(0, 0, 0, 0.25);
                letter-spacing: 1px;
            }

            /* Summary Cards */
            .summary-card {
                background-color: #ffffff;
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
                padding: 28px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .summary-card:hover {
                transform: translateY(-6px);
                box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
            }

            /* Table Styling */
            .summary-card table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 18px;
            }
            
            .summary-card th, .summary-card td {
                padding: 16px;
                text-align: center;
                border-bottom: 1px solid #e9ecef;
                border-right: 1px solid #e9ecef;
                font-size: 1em;
                color: #343a40;
            }

            .summary-card th:first-child, .summary-card td:first-child {
                border-left: 1px solid #e9ecef;
            }
            
            .summary-card th {
                background: linear-gradient(90deg, #3949ab, #5c6bc0);
                color: #ffffff;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                font-size: 1.1em;
            }

            .summary-card tr:nth-child(even) {
                background-color: #f5f7fa;
            }

            .summary-card tr:hover {
                background-color: #e3f2fd;
                transition: background-color 0.25s ease;
            }

            /* Metric Cards for KPIs */
            .metric-card-container {
                display: flex;
                justify-content: space-around;
                gap: 22px;
                margin-bottom: 35px;
            }

            .metric-card {
                flex: 1;
                background: #ffffff;
                border-radius: 14px;
                padding: 25px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border-bottom: 6px solid #1565c0;
            }

            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            }

            .metric-card-label {
                font-size: 1.1em;
                color: #6c757d;
                margin-bottom: 12px;
                text-transform: uppercase;
                font-weight: 600;
            }

            .metric-card-value {
                font-size: 2.8em;
                font-weight: bold;
                color: #0d47a1;
            }

            /* Status Badges */
            .status-badge {
                display: inline-block;
                padding: 8px 18px;
                border-radius: 25px;
                color: white;
                font-size: 0.9em;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
            }
            
            .status-ne { background-color: #fb8c00; } 
            .status-ner { background-color: #e53935; }
            .status-rs { background-color: #43a047; }
            .status-tr { background-color: #1e88e5; }
            .status-nr { background-color: #546e7a; }
            .status-rnf { background-color: #ff7043; }
            .status-rnr { background-color: #c62828; }
            .status-default { background-color: #9e9e9e; }

            /* Progress Bar */
            .progress-container {
                width: 85%;
                background-color: #e9ecef;
                border-radius: 12px;
                margin: 12px auto;
            }

            .progress-bar {
                height: 18px;
                border-radius: 12px;
                color: white;
                padding-right: 5px;
                line-height: 18px;
                text-align: right;
                transition: width 0.5s ease-in-out;
            }

            .progress-green { background-color: #43a047; }
            .progress-blue { background-color: #1e88e5; }
            .progress-orange { background-color: #fb8c00; }

            /* Status Dots */
            .status-dot {
                height: 12px;
                width: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 6px;
                vertical-align: middle;
            }

            .dot-green { background-color: #43a047; }
            .dot-red { background-color: #e53935; }
            .dot-orange { background-color: #fb8c00; }
        </style>

        """

        data += '<div class="report-container">'
        data += '<div class="report-header">Technician Summary</div>'
        data += '<div class="summary-card">'
        data += '<table class="table table-bordered">'
        data += '<tr>'

        data += '<td colspan = 6 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Technician-wise Summary</b></center></td>' 


        data += '</tr>'      

        data += '<tr>'

        data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Technician</b></center></td>'   
        
        data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Status / Metrics</b></center></td>' 
        data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Current Week</b></center></td>' 
        data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">Current Month</b></center></td>' 
        data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;"><center><b style="color:#055c9d;">2025 Cumulative</b></center></td>' 
        data += '</tr>'
        today = date.today()

        # Sunday as the start of the week
        s_week = today - timedelta(days=(today.weekday() + 1) % 7)
        e_week = s_week + timedelta(days=6)

        s_month = date(today.year, today.month, 1)

        # last day of current month
        last_day = calendar.monthrange(today.year, today.month)[1]
        e_month = date(today.year, today.month, last_day)
        
        # First day of current year
        first_day = date(today.year, 1, 1)

        # Last day of current year
        last_day = date(today.year, 12, 31)

        # Format for SQL
        s_year = first_day.strftime("%Y-%m-%d")
        e_year = last_day.strftime("%Y-%m-%d")

        technicians = frappe.db.sql("""
        SELECT DISTINCT technician as tec
        FROM `tabWork Order Data`
        WHERE company = '%s' 
        AND technician IS NOT NULL 
        """ %(self.company),as_dict=1)

        for i in technicians:
            
            tech_name = frappe.get_value('Employee',{"user_id":i["tec"],"status":"Active"},["employee_name"])
            data += '<tr>'
            data += '<td rowspan = 9 colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center;padding-top:180px;font-weight:bold;">%s</td>' %(tech_name or i["tec"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NE</td>' 

            wo_count_w_tech = frappe.db.count("Work Order Data",{"technician":i["tec"],"company":self.company,"posting_date": ["between", [s_week,e_week]]})

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(wo_count_w_tech)

            wo_count_m_tech = frappe.db.count("Work Order Data",{"technician":i["tec"],"company":self.company,"posting_date": ["between", [s_month,e_month]]})

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(wo_count_m_tech)

            wo_count_y_tech = frappe.db.count("Work Order Data",{"technician":i["tec"],"company":self.company,"posting_date": ["between", [s_year,s_year]]})

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(wo_count_y_tech)
            data += '</tr>'   

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg.UE Time</td>' 

            tech_e_time_week = 0

            total_eval_time_week_tech = frappe.db.sql("""
            SELECT SUM(er.evaluation_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s and wod.technician = %s
            """, (s_week,e_week,i["tec"]), as_dict=1)

            if total_eval_time_week_tech:
                if total_eval_time_week_tech [0]['total_time']:
                    hours = total_eval_time_week_tech [0]['total_time'] / 3600
                    tech_e_time_week = hours/24


            
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(tech_e_time_week,2))

            tech_e_time_month = 0
            total_eval_time_month_tech = frappe.db.sql("""
            SELECT SUM(er.evaluation_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s and wod.technician = %s
            """, (s_month,e_month,i["tec"]), as_dict=1)

            if total_eval_time_month_tech:
                if total_eval_time_month_tech[0]['total_time']:
                    hours = total_eval_time_month_tech[0]['total_time'] / 3600
                    tech_e_time_month = hours/24


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(tech_e_time_month,2))

            tech_e_time_year = 0
            total_eval_time_year_tech = frappe.db.sql("""
            SELECT SUM(er.evaluation_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s and wod.technician = %s
            """, (s_year,e_year,i["tec"]), as_dict=1)

            if total_eval_time_year_tech:
                if total_eval_time_year_tech[0]['total_time']:
                    hours = total_eval_time_year_tech[0]['total_time'] / 3600
                    tech_e_time_year = hours/24

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(tech_e_time_year,2))
            data += '</tr>'   

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">NER</td>' 
            
            ner_tech_w = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "NER-Need Evaluation Return" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' and `tabWork Order Data`.technician = '%s' """ %(self.company,s_week,e_week,i["tec"]) ,as_dict=1)

            ner_tech_m = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "NER-Need Evaluation Return" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' and `tabWork Order Data`.technician = '%s' """ %(self.company,s_month,e_month,i["tec"]) ,as_dict=1)

            ner_tech_y = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "NER-Need Evaluation Return" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' and `tabWork Order Data`.technician = '%s' """ %(self.company,s_year,e_year,i["tec"]) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_tech_w[0]["ct"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_tech_m[0]["ct"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_tech_y[0]["ct"])
            data += '</tr>'   

            data += '</tr>'   

            
            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg.NER Value</td>' 


            wods_ner = frappe.db.sql(''' select 
            DISTINCT `tabQuotation Item`.wod_no AS wd,`tabQuotation Item`.margin_amount as ma
            from `tabQuotation` 
            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
            LEFT JOIN `tabWork Order Data` wod ON `tabQuotation Item`.wod_no = wod.name
            where `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") and
            `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
            and `tabQuotation`.transaction_date between '%s' and '%s' 
            and `tabQuotation`.company = '%s'
            and wod.technician = '%s' and wod.status_cap = "NER-Need Evaluation Return" ''' %(s_week,e_week,self.company,i["tec"]),as_dict=1)

            wods_m_ner = frappe.db.sql(''' select 
            DISTINCT `tabQuotation Item`.wod_no AS wd,`tabQuotation Item`.margin_amount as ma
            from `tabQuotation` 
            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
            LEFT JOIN `tabWork Order Data` wod ON `tabQuotation Item`.wod_no = wod.name
            where `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") and
            `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
            and `tabQuotation`.transaction_date between '%s' and '%s' 
            and `tabQuotation`.company = '%s' 
            and wod.technician = '%s' and wod.status_cap = "NER-Need Evaluation Return" ''' %(s_month,e_month,self.company,i["tec"]),as_dict=1)

            wods_y_ner = frappe.db.sql(''' select 
            DISTINCT `tabQuotation Item`.wod_no AS wd,`tabQuotation Item`.margin_amount as ma
            from `tabQuotation` 
            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
            LEFT JOIN `tabWork Order Data` wod ON `tabQuotation Item`.wod_no = wod.name
            where `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") and
            `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
            and `tabQuotation`.transaction_date between '%s' 
            and '%s' and `tabQuotation`.company = '%s' 
            and wod.technician = '%s' and wod.status_cap = "NER-Need Evaluation Return" ''' %(s_year,e_year,self.company,i["tec"]),as_dict=1)

            q_w_ner = 0
            for i in wods_ner:
                q_amt_ner = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if q_amt_ner:               
                    if q_amt_ner[0]["is_m"] == 1:
                        per = (q_amt_ner[0]["up"] * q_amt_ner[0]["dis"])/100
                        q_amt = q_amt_ner[0]["up"] - per
                        q_w_ner =  q_w_ner + q_amt

                    else:
                        q_amt = q_amt_ner[0]["adc"]

                        q_w_ner =  q_w_ner + q_amt
                        

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(q_w_ner)

            q_m_ner = 0
            for i in wods_m_ner:
                q_amt_ner2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if q_amt_ner2:               
                    if q_amt_ner2[0]["is_m"] == 1:
                        per = (q_amt_ner2[0]["up"] * q_amt_ner2[0]["dis"])/100
                        q_amt = q_amt_ner2[0]["up"] - per
                        q_m_ner =  q_m_ner + q_amt

                    else:
                        q_amt = q_amt_ner2[0]["adc"]

                        q_m_ner =  q_m_ner + q_amt
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(q_m_ner)

            q_y_ner = 0
            for i in wods_m_ner:
                q_amt_ner3 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if q_amt_ner3:               
                    if q_amt_ner3[0]["is_m"] == 1:
                        per = (q_amt_ner3[0]["up"] * q_amt_ner3[0]["dis"])/100
                        q_amt = q_amt_ner3[0]["up"] - per
                        q_y_ner =  q_y_ner + q_amt

                    else:
                        q_amt = q_amt_ner3[0]["adc"]

                        q_y_ner =  q_y_ner + q_amt
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(q_y_ner)
            data += '</tr>'   


            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">RS</td>' 

            rs_tech_w = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' and `tabWork Order Data`.technician = '%s' """ %(self.company,s_week,e_week,i["tec"]) ,as_dict=1)

            rs_tech_m = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' and `tabWork Order Data`.technician = '%s' """ %(self.company,s_month,e_month,i["tec"]) ,as_dict=1)

            rs_tech_y = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  `tabStatus Duration Details`.status = "RS-Repaired and Shipped" and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' and `tabWork Order Data`.technician = '%s' """ %(self.company,s_year,e_year,i["tec"]) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(rs_tech_w[0]["ct"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(rs_tech_m[0]["ct"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(rs_tech_y[0]["ct"])
            data += '</tr>'   

            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">RS1</td>' 

            
            ner_rs_tech_w = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where 
            `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' 
            and `tabStatus Duration Details`.status = "RS-Repaired and Shipped"
            and  date(`tabStatus Duration Details`.date) > `tabWork Order Data`.status_cap_date
            and `tabWork Order Data`.technician = '%s' and `tabWork Order Data`.status_cap = "NER-Need Evaluation Return" 
            ORDER BY `tabStatus Duration Details`.date desc LIMIT 1 """ %(self.company,s_week,e_week,i["tec"]) ,as_dict=1)

            ner_rs_tech_m = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where 
            `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' 
            and  date(`tabStatus Duration Details`.date) > `tabWork Order Data`.status_cap_date
            and `tabStatus Duration Details`.status = "RS-Repaired and Shipped"
            and `tabWork Order Data`.technician = '%s' and `tabWork Order Data`.status_cap = "NER-Need Evaluation Return"
            ORDER BY `tabStatus Duration Details`.date desc LIMIT 1 """ %(self.company,s_month,e_month,i["tec"]) ,as_dict=1)

            ner_rs_tech_y = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where  
            `tabStatus Duration Details`.status = "RS-Repaired and Shipped"
            and `tabWork Order Data`.company = '%s'
            and date(`tabStatus Duration Details`.date) between '%s' and '%s' 
            and  date(`tabStatus Duration Details`.date) > `tabWork Order Data`.status_cap_date
            and `tabWork Order Data`.technician = '%s' 
            ORDER BY `tabStatus Duration Details`.date desc LIMIT 1""" %(self.company,s_year,e_year,i["tec"]) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_rs_tech_w[0]["ct"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_rs_tech_m[0]["ct"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(ner_rs_tech_y[0]["ct"])
            data += '</tr>'   


            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">RNR/RNF</td>' 

            not_repaired_count_weekly_t = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where `tabStatus Duration Details`.status IN ("RNF-Return No Fault","RNR-Return Not Repaired") and `tabWork Order Data`.company = '%s'
            and `tabWork Order Data`.posting_date between '%s' and '%s' and `tabWork Order Data`.technician = '%s' """ %(self.company,s_week,e_week,i["tec"]) ,as_dict=1)


            not_repaired_count_monthy_t  = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where `tabStatus Duration Details`.status IN ("RNF-Return No Fault","RNR-Return Not Repaired") and `tabWork Order Data`.company = '%s'
            and `tabWork Order Data`.posting_date between '%s' and '%s' and `tabWork Order Data`.technician = '%s' """ %(self.company,s_month,e_month,i["tec"]) ,as_dict=1)


            not_repaired_count_yearly_t  = frappe.db.sql(""" select count(DISTINCT `tabWork Order Data`.name) as ct from `tabWork Order Data` 
            left join `tabStatus Duration Details` on `tabWork Order Data`.name = `tabStatus Duration Details`.parent
            where `tabStatus Duration Details`.status IN ("RNF-Return No Fault","RNR-Return Not Repaired") and `tabWork Order Data`.company = '%s'
            and `tabWork Order Data`.posting_date between '%s' and '%s' and `tabWork Order Data`.technician = '%s' """ %(self.company,s_year,e_year,i["tec"]) ,as_dict=1)

            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(not_repaired_count_weekly_t[0]["ct"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(not_repaired_count_monthy_t[0]["ct"])
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(not_repaired_count_yearly_t[0]["ct"])
            data += '</tr>'   

            data += '<tr>' 
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg.UTR Time</td>' 

            rep_time_week_t = 0
            total_rep_time_weekly_tech_t = frappe.db.sql("""
            SELECT SUM(er.estimated_repair_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s and wod.technician = %s
            """, (s_week,e_week,i["tec"]), as_dict=1)

            if total_rep_time_weekly_tech_t:    
                if not total_rep_time_weekly_tech_t[0]['total_time']:
                    total_rep_time_weekly_tech_t[0]['total_time'] = 0
                if total_rep_time_weekly_tech_t[0]['total_time'] > 0:
                    hours = total_rep_time_weekly_tech_t[0]['total_time'] / 3600
                    rep_time_week_t = hours/24

            
            rep_time_month_t = 0
            total_rep_time_month_t = frappe.db.sql("""
            SELECT SUM(er.estimated_repair_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s and wod.technician = %s
            """, (s_month,e_month,i["tec"]), as_dict=1)
            if total_rep_time_month_t:
                if not total_rep_time_month_t[0]['total_time']:
                    total_rep_time_month_t[0]['total_time'] = 0
                if total_rep_time_month_t[0]['total_time'] > 0:
                    hours = total_rep_time_month_t[0]['total_time'] / 3600
                    rep_time_month_t = hours/24

            rep_time_year_t = 0
            total_rep_time_yearly_t = frappe.db.sql("""
            SELECT SUM(er.estimated_repair_time) AS total_time
            FROM `tabEvaluation Report` er
            INNER JOIN `tabWork Order Data` wod
            ON er.work_order_data = wod.name
            WHERE er.date BETWEEN %s AND %s and wod.technician = %s
            """, (s_year,e_year,i["tec"]), as_dict=1)
            if total_rep_time_yearly_t:
                if total_rep_time_month_t[0]['total_time']:
                    if total_rep_time_yearly_t[0]['total_time'] > 0:
                        hours = total_rep_time_yearly_t[0]['total_time'] / 3600
                        rep_time_year_t = hours/24
        
       
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(rep_time_week_t,2))
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(rep_time_month_t,2))
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(round(rep_time_year_t,2))
            data += '</tr>'   


            data += '<tr>'
            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">Avg. RS Value</td>' 
           
            wods = frappe.db.sql(''' select 
            DISTINCT `tabQuotation Item`.wod_no AS wd,`tabQuotation Item`.margin_amount as ma
            from `tabQuotation` 
            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
            LEFT JOIN `tabWork Order Data` wod ON `tabQuotation Item`.wod_no = wod.name
            where `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") and
            `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
            and `tabQuotation`.transaction_date between '%s' and '%s' and `tabQuotation`.company = '%s' and wod.technician = '%s' ''' %(s_week,e_week,self.company,i["tec"]),as_dict=1)

            wods_m = frappe.db.sql(''' select 
            DISTINCT `tabQuotation Item`.wod_no AS wd,`tabQuotation Item`.margin_amount as ma
            from `tabQuotation` 
            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
            LEFT JOIN `tabWork Order Data` wod ON `tabQuotation Item`.wod_no = wod.name
            where `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") and
            `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
            and `tabQuotation`.transaction_date between '%s' and '%s' and `tabQuotation`.company = '%s' and wod.technician = '%s' ''' %(s_month,e_month,self.company,i["tec"]),as_dict=1)

            wods_y = frappe.db.sql(''' select 
            DISTINCT `tabQuotation Item`.wod_no AS wd,`tabQuotation Item`.margin_amount as ma
            from `tabQuotation` 
            left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
            LEFT JOIN `tabWork Order Data` wod ON `tabQuotation Item`.wod_no = wod.name
            where `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") and
            `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair") 
            and `tabQuotation`.transaction_date between '%s' and '%s' and `tabQuotation`.company = '%s' and wod.technician = '%s' ''' %(s_year,e_year,self.company,i["tec"]),as_dict=1)

            q_m = 0
            for i in wods:
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
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if q_amt:
                                    
                    if q_amt[0]["is_m"] == 1:
                        per = (q_amt[0]["up"] * q_amt[0]["dis"])/100
                        q_amt = q_amt[0]["up"] - per
                        q_m = q_m + q_amt

                    else:
                        q_amt = q_amt[0]["adc"]

                        q_m = q_m + q_amt


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(f"{round(q_m,2):,.2f}")
            
           
            qm2= 0
            for i in wods_m:
                q_amt2 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if q_amt2:
                                    
                    if q_amt2[0]["is_m"] == 1:
                        per = (q_amt2[0]["up"] * q_amt2[0]["dis"])/100
                        q_amt = q_amt2[0]["up"] - per
                        qm2 = qm2 + q_amt

                    else:
                        q_amt = q_amt2[0]["adc"]
                        qm2 = qm2 + q_amt


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(f"{round(qm2,2):,.2f}")

            qm3= 0
            for i in wods_y:
                q_amt3 = frappe.db.sql(''' select `tabQuotation`.name as q_name,
                `tabQuotation`.default_discount_percentage as dis,
                `tabQuotation`.approval_date as a_date,
                `tabQuotation`.is_multiple_quotation as is_m,
                `tabQuotation`.after_discount_cost as adc,
                `tabQuotation Item`.unit_price as up,
                `tabQuotation Item`.margin_amount as ma 
                from `tabQuotation` 
                left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                where  `tabQuotation`.Workflow_state in ("Approved By Customer","Quoted to Customer","Rejected by Customer") 
                and `tabQuotation Item`.wod_no = '%s' and
                `tabQuotation`.quotation_type in ("Customer Quotation - Repair","Revised Quotation - Repair")  
                ''' %(i["wd"],),as_dict=1)
                if q_amt3:
                                    
                    if q_amt3[0]["is_m"] == 1:
                        per = (q_amt3[0]["up"] * q_amt3[0]["dis"])/100
                        q_amt = q_amt3[0]["up"] - per
                        qm3 = qm3 + q_amt

                    else:
                        q_amt = q_amt3[0]["adc"]
                        qm3 = qm3 + q_amt


            data += '<td colspan = 1 style="border-color:#000000;color:#055c9d;text-align:center">%s</td>' %(f"{round(qm3,2):,.2f}")
            data += '</tr>'       

        data += '</table>'
        data += '</div>'
        data += '</div>'
        data += '</div>'
        

        return data



