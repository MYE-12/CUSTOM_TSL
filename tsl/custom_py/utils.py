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
#from frappe.permissions import has_role
# @frappe.whitelist()
# def currency():

# 	url = "https://api.exchangerate.host/USD"
# 	payload = {}
# 	headers = {}
# 	response = requests.request("GET", url, headers=headers, data=payload)
# 	data = response.json()
# 	print((data['rates']['KWD']))

@frappe.whitelist()
def send_sales_reminder(): # Reflects in Sales Track
    
    sales_person = ["maaz@tsl-me.com","vazeem@tsl-me.com"]
    sales_report = frappe.db.sql("""select date,sales_user from `tabSales Track` where date = CURDATE()""",as_dict=1)

    if sales_report == []:
        frappe.sendmail(
                        recipients= sales_person,
                       cc = ["yousuf@tsl-me.com"],
                        subject="Daily Sales Report Reminder",
                        message = """Dear Team,<br><br>Kindly fill the Daily Report by EOD<br><br>Thanks & Regards,<br><br>
                        <b>​TSL Company</b><br>
                        Bldg: 1473, Unit: 13, Street: 24, Block: 1, Al Rai Industrial Area, Kuwait.<br>
                        Tel: +965 24741313 | Fax: +965 24741311 | <br>
                        Email: info@tsl-me.com | Web: www.tsl-me.com"""
                        )
    for sr in sales_report:
        print(sr.sales_person)
        if sales_person[0] not in sr.sales_user:
            print(sales_person[0])
            frappe.sendmail(
                    recipients= [sales_person[0]],
                    cc = ["yousuf@tsl-me.com"],
                    subject="Daily Sales Report Reminder",
                    message = """Dear Team,<br><br>Kindly fill the Daily Report by EOD<br><br>Thanks & Regards,<br><br>
                            <b>​TSL Company</b><br>
                            Bldg: 1473, Unit: 13, Street: 24, Block: 1, Al Rai Industrial Area, Kuwait.<br>
                            Tel: +965 24741313 | Fax: +965 24741311 | <br>
                            Email: info@tsl-me.com | Web: www.tsl-me.com"""
                            )
        if sales_person[1] not in sr.sales_user:
            print(sales_person[1])
            frappe.sendmail(
                recipients= sales_person[1],
                cc = ["yousuf@tsl-me.com"],
                            subject="Daily Sales Report Reminder",
                            message = """Dear Team,<br><br>Kindly fill the Daily Report by EOD<br><br>Thanks & Regards,<br><br>
                            <b>​TSL Company</b><br>
                            Bldg: 1473, Unit: 13, Street: 24, Block: 1, Al Rai Industrial Area, Kuwait.<br>
                            Tel: +965 24741313 | Fax: +965 24741311 | <br>
                            Email: info@tsl-me.com | Web: www.tsl-me.com"""
                            )

@frappe.whitelist()
def create_rfq_int(ps): # Request For Quotation
    doc = frappe.get_doc("Initial Evaluation",ps)
    new_doc = frappe.new_doc("Request for Quotation")
    new_doc.company = doc.company
    new_doc.branch = frappe.db.get_value("Work Order Data",doc.work_order_data,"branch")
    new_doc.initial_evaluation = ps
    new_doc.work_order_data = doc.work_order_data
    new_doc.department = frappe.db.get_value("Work Order Data",doc.work_order_data,"department")
    new_doc.items=[]
    psn = doc.items[-1].part_sheet_no
    for i in doc.get("items"):
        invent = [i[0] for i in frappe.db.get_list("Warehouse",{"company":doc.company,"is_branch":1},"name",as_list=1)]
        actual = frappe.db.get_value("Bin",{"item_code":i.part,"warehouse":["in",invent]},"actual_qty")
        needed = i.qty - (actual or 0)
        if needed > 0:
            qty = needed
        if i.parts_availability == "No" and psn == i.part_sheet_no:
            new_doc.append("items",{
                "item_code":i.part,
                "item_name":i.part_name,
                "description":i.part_name,
                'model':i.model,
                "category":i.category,
                "sub_category":i.sub_category,
                "mfg":i.manufacturer,
                'serial_no':i.serial_no,
                "uom":"Nos",
                "stock_uom":"Nos",
                "conversion_factor":1,
                "stock_qty":1,
                "qty":qty or 0,
                "schedule_date":add_to_date(new_doc.transaction_date,days = 2),
                "warehouse":new_doc.branch,
                "branch":new_doc.branch,
                "work_order_data":doc.work_order_data,
                "department":frappe.db.get_value("Work Order Data",doc.work_order_data,"department")
            })
    return new_doc

@frappe.whitelist() # Stock against the Parts requested in initial Evaluation
def getstock_detail(item_details,company):
    item_details = json.loads(item_details)
    data = ''
    data += '<h4><center><b>STOCK DETAILS</b></center></h4>'
    data += '<h6><B>Note:</h6>'
    data += '<table style = font-size:12px width=100% ><tr><td>REPAIR KUWAIT - <b>TSL</b></td><td>RIYADH MAIN -<b>TSL SA</b></td><td>JEDDAH -<b>TSL SA</b></td><td>DAMMAM- <b>TSL SA</b></tr>'
    data += '</table>'
    for j in item_details:
        country = frappe.get_value("Company",{"name":company},["country"])
        warehouse_stock = frappe.db.sql("""
        select sum(b.actual_qty) as qty from `tabBin` b join `tabWarehouse` wh on wh.name = b.warehouse join `tabCompany` c on c.name = wh.company where c.country = '%s' and b.item_code = '%s'
        """ % (country,j["sku"]),as_dict=True)[0]
        if not warehouse_stock["qty"]:
            warehouse_stock["qty"] = 0		
        new_po = frappe.db.sql("""select sum(`tabPurchase Order Item`.qty) as qty,sum(`tabPurchase Order Item`.received_qty) as d_qty from `tabPurchase Order` 
        left join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
        where `tabPurchase Order Item`.item_code = '%s' and `tabPurchase Order`.docstatus = 1 """ % (j["sku"]), as_dict=True)[0]
        if not new_po['qty']:
            new_po['qty'] = 0
        if not new_po['d_qty']:
            new_po['d_qty'] = 0
        in_transit = new_po['qty'] - new_po['d_qty']
        total = warehouse_stock["qty"] + in_transit
        
        stocks = frappe.db.sql("""select actual_qty,warehouse,stock_uom,stock_value from tabBin
        where item_code = '%s' """%(j["sku"]),as_dict=True)
        frappe.errprint(stocks)
        
        pos = frappe.db.sql("""select `tabPurchase Order Item`.item_code as item_code,`tabPurchase Order Item`.item_name as item_name,`tabPurchase Order`.supplier as supplier,sum(`tabPurchase Order Item`.qty) as qty,`tabPurchase Order Item`.rate as rate,`tabPurchase Order`.transaction_date as date,`tabPurchase Order`.name as po from `tabPurchase Order`
        left join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
        where `tabPurchase Order Item`.item_code = '%s' and `tabPurchase Order`.docstatus != 2 order by rate asc limit 1""" % (j["sku"]), as_dict=True)
        
        new_so = frappe.db.sql("""select sum(`tabSales Order Item`.qty) as qty,sum(`tabSales Order Item`.delivered_qty) as d_qty from `tabSales Order`
        left join `tabSales Order Item` on `tabSales Order`.name = `tabSales Order Item`.parent
        where `tabSales Order Item`.item_code = '%s' and `tabSales Order`.docstatus = 1  """ % (j["sku"]), as_dict=True)[0]
        
        if not new_so['qty']:
            new_so['qty'] = 0
        if not new_so['d_qty']:
            new_so['d_qty'] = 0
        del_total = new_so['qty'] - new_so['d_qty']
            
        i = 0
        
        for po in pos:
            if pos:
                data += '<table class="table table-bordered">'
                data += '<tr>'
                data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>SKU</b><center></td>'
                data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>PART NUMBER</b><center></td>'
                data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>STOCK - ( KW )</b><center></td>'
                data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>STOCK - ( RIYADH-SA )</b><center></td>'
                data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>STOCK - ( JEDDAH-SA )</b><center></td>'
                data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>STOCK - ( DAMMAM-SA )</b><center></td>'
                data += '</tr>'
                data +='<tr>'
                data += '<td style="text-align:center" colspan=1>%s</td>'%(j["sku"])
                
                data += '<td style="text-align:center" colspan=1>%s</td>'%(frappe.db.get_value("Item Model",j["model"],['model']))
                for stock in stocks:
                    if stock.actual_qty > 0:
                        data += '<td style="text-align:center;" colspan=1>%s</td>'%(stock.actual_qty)
                    
                data += '</tr>'
            i += 1
        data += '</table>'
                
    return data
# def create_hooks():
#     job = frappe.db.exists('Scheduled Job Type', 'stock_reminder')
#     if not job:
#         sjt = frappe.new_doc("Scheduled Job Type")  
#         sjt.update({
#             "method" : 'tsl.custom_py.utils.enque_qty',
#             "frequency" : 'Cron',
#             "cron_format" : '30 16 * * *'
#         })
#         sjt.save(ignore_permissions=True)

# def enque_qty():
# 	frappe.enqueue(
# 					item_qty, queue="long", enqueue_after_commit=True
# 				)


@frappe.whitelist() # Low Balance Email Trigger
def item_qty():
    item = frappe.db.sql("""select name,model,category,sub_category,qty from `tabItem` where qty < 5 """,as_dict=1)
    ir = 0
    data= ""
    data += '<table class="table table-bordered">'
    data += '<tr>'
    data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>SKU</b><center></td>'
    data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>PART NUMBER</b><center></td>'
    data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>CATEGORY</b><center></td>'
    data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>SUB - CATEGORY</b><center></td>'
    data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>QTY</b><center></td>'
    data += '</tr>'


    for i in item:
        
        data +='<tr>'
        data += '<td style="text-align:center" colspan=1>%s</td>'%(i.name)
        data += '<td style="text-align:center" colspan=1>%s</td>'%(i.model)
        data += '<td style="text-align:center" colspan=1>%s</td>'%(i.category)
        data += '<td style="text-align:center" colspan=1>%s</td>'%(i.sub_category)
        data += '<td style="text-align:center;" colspan=1>%s</td>'%(i.qty)
        data += '</tr>'
        
    data += '</table>'
        # print(message)
    print(data)

    frappe.sendmail(
    recipients='yousuf@tsl-me.com',
    sender="info@tsl-me.com",
    subject="Low Stock",
    message=data
    
            
    )

@frappe.whitelist()
def amount(amount,currency):
    url = "https://api.exchangerate-api.com/v4/latest/%s"%(currency)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    
    rate_kw = data['rates']['KWD']
    conv_rate = float(amount) / 0.31
    return conv_rate
    

@frappe.whitelist()
def get_work_orders(data):
    data = json.loads(data)
    wods = []
    for i in data:
        wo = frappe.db.sql(""" select DISTINCT `tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
        left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
        where `tabSales Invoice`.name = '%s' """ %(i["reference_name"]),as_dict =1)
        for j in wo:
            if j["wo"]:
                wods.append(j["wo"])
            else:
                wods.append(j["w"])

    return wods


@frappe.whitelist()
def get_work_orders_purchase(data):
    data = json.loads(data)
    wods = []
    combined_data = []
    # sods = []
    for i in data:
        if i["reference_doctype"] == "Purchase Invoice":
            pi = frappe.db.sql(""" select DISTINCT `tabPurchase Invoice`.name as p,`tabPurchase Invoice Item`.work_order_data as wo,`tabPurchase Invoice Item`.supply_order_data as so from `tabPurchase Invoice` 
            left join `tabPurchase Invoice Item` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent 
            where `tabPurchase Invoice`.name = '%s' """ %(i["reference_name"]),as_dict =1)
            for j in pi:
                frappe.errprint(i["reference_name"])
                combined_dict = {
                "doc_name":i["doc_name"],
                "reference_name": i["reference_name"],
                "work_order_data": j["wo"],
                "supply_order_data": j["so"]
            }
                combined_data.append(combined_dict)
    
    aggregated_data = {}

    for entry in combined_data:
        doc_name = entry['doc_name']
        ref_name = entry['reference_name']
        wo = entry['work_order_data']
        so = entry['supply_order_data']
        
        if ref_name not in aggregated_data:
            aggregated_data[ref_name] = {
                'work_order_data': set(),  # Use a set to avoid duplicates
                'supply_order_data': set()
            }
        
        if wo:
            aggregated_data[ref_name]['work_order_data'].add(wo)
        if so:
            aggregated_data[ref_name]['supply_order_data'].add(so)

    # Convert sets to lists for final output
    final_data = []
    for ref_name, values in aggregated_data.items():
        final_data.append({
        'reference_name': ref_name,
        'doc_name': doc_name,
        'work_order_data': ','.join(values['work_order_data']),
        'supply_order_data': ','.join(values['supply_order_data'])
    })

                
    frappe.errprint(final_data)
    
    return final_data


@frappe.whitelist()
def set_payment(data,pe,date):
    data = json.loads(data)
    for i in data:
        frappe.db.set_value("Work Order Data",i["work_order_data"],"payment_date",date)
        frappe.db.set_value("Work Order Data",i["work_order_data"],"payment_entry_reference",pe)
        wd = frappe.get_doc("Work Order Data",i["work_order_data"])
        wd.status = "P-Paid"
        ldate = wd.status_duration_details[-1].date
        now = datetime.now()
        time_date = str(ldate).split(".")[0]
        format_data = "%Y-%m-%d %H:%M:%S"
        date = datetime.strptime(time_date, format_data)
        duration = now - date
        duration_in_s = duration.total_seconds()
        minutes = divmod(duration_in_s, 60)[0]/60
        data = str(minutes).split(".")[0]+"hrs "+str(minutes).split(".")[1][:2]+"min"
        frappe.db.set_value("Status Duration Details",wd.status_duration_details[-1].name,"duration",data)
        wd.append("status_duration_details",{
            "status":wd.status,
            "date":now,
        })
        doc = frappe.get_doc("Work Order Data",wd.name)
        doc.append("status_duration_details",{
            "status":wd.status,
            "date":now,
        })
        wd.save(ignore_permissions = 1)
        
        
        
@frappe.whitelist()
def get_receivable(customer):	

    data = ''
    data += '<table class="table table-bordered">'
    data += '<tr>'
    data += '<td align = center style="border-color:#000000;font-size: 11px;width:15%"><b>Date</b></td>'
    data += '<td align = center style="border-color:#000000;font-size: 11px;width:25%"><b>Invoice No</b></td>'
    data += '<td align = center style="border-color:#000000;font-size: 11px;width:25%;"><b>Ref(WOD)</b></td>'
    data += '<td align = center style="border-color:#000000;font-size: 11px;width:25%;"><b>Ref(PO)</b></td>'
    data += '<td align = center style="border-color:#000000;font-size: 11px;width:15%;"><b>Invoiced</b></td>'
    data += '<td align = center style="border-color:#000000;font-size: 11px;width:10%;"><b>Paid</b></td>'
    data += '<td align = center style="border-color:#000000;font-size: 11px;width:15%;"><b>Outstanding</b></td>'
    data += '</tr>'
    si = frappe.get_all("Sales Invoice",{"status":"Overdue","customer":customer},["*"])
    os = 0
    for i in si:
        os = os + i.outstanding_amount
        wo = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.po_no as po_no,`tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.previous_wod_no as pwo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
        left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
        where `tabSales Invoice`.name = '%s' """ %(i.name),as_dict =1)
        wods = []

        for j in wo:
            if j["wo"]:
                original_string = str(j["wo"])
                substring = original_string[8:] 
                wods.append(substring)
                
            elif j["w"]:
                original_string = str(j["w"])
                substring = original_string[8:] 
                wods.append(substring)
            
            elif j["pwo"]:
                wods.append(j["pwo"])

            # else:
            # 	wods.append('')

        po_no = frappe.get_value("Sales Invoice",{"name":i.name},["po_no"])
        # if [po_no]:
        # 	wods.append(po_no)
        
        # Input date string
        input_date_string = str(i.due_date)

        # Convert string to datetime object
        input_date = datetime.strptime(input_date_string, "%Y-%m-%d")

        # Format the date in the desired format
        formatted_due_date = input_date.strftime("%d-%m-%Y")
        wod = str(wods).strip('[]')
        wod = wod.replace("'", '')
        if wod == None:
            wod = ''
        data += '<tr>'
        data += '<td style="border-color:#000000;font-size: 10px;">%s</td>'%(formatted_due_date)
        data += '<td align = center style="border-color:#000000;font-size: 10px;font-weight: bold;"><a href="https://erp.tsl-me.com/api/method/frappe.utils.print_format.download_pdf?doctype=Sales Invoice&name=%s&format=Sales Invoice TSL&no_letterhead=0&letterhead=TSL New&settings={}&_lang=en">%s</a></td>'%(i.name,i.name)
        data += '<td style="border-color:#000000;font-size: 10px;">%s</td>'%(wod)
        data += '<td style="border-color:#000000;font-size: 10px;">%s</td>'%(po_no)
        gt = "{:,.3f}".format(i.grand_total)
        p = i.grand_total-i.outstanding_amount
        paid = "{:,.3f}".format(p)
        outs= "{:,.3f}".format(i.outstanding_amount)
        data += '<td align = center style="border-color:#000000;font-size: 10px;">%s</td>'%(gt)
        data += '<td align = center style="border-color:#000000;font-size: 10px;">%s</td>'%("")
        data += '<td align = center style="border-color:#000000;font-size: 10px;">%s</td>'%(outs)
        data += '</tr>'
        wods = []
    data += '<tr>'
    frmtd_num = "{:,.3f}".format(os)
    data += '<td align = right colspan = 6 style="border-color:#000000;"><b>Balance Due</b></td>'
    data += '<td align = center colspan = 2 style="border-color:#000000;"><b>%s</b></td>'%(frmtd_num)
    data += '</tr>'
    data += '</table>'

    data += '<p><p>'


    return data

@frappe.whitelist()
def get_wod():
    data = ''
    data += '<div class="table-container">'
    data += '<table class="table table-bordered" width: 100%;>'
    data += '<tr>'
    data += '<td colspan = 3 style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="150"></td>'
    data += '<td colspan = 3 style="border-color:#000000;"><h2><center><b>TSL Company</b></center></h2></td>'
    data += '<td colspan = 3 style="border-color:#000000;"><center><img src = "/files/kuwait flag.jpg" width ="100"></center></td>'
    
    data += '</tr>'

    data += '<tr>'
    data += '<td colspan = 9 style="border-color:#000000;"><b>RSC & Quoted Summary</b></td>'
        
    data += '</tr>'

    data += '<tr>'
    data += '<td colspan = 1 style="border-color:#000000;"><center><b></b></center></td>'
    data += '<td colspan = 2 style="border-color:#000000;"><center><b>Total Amount(RSI)</b></center></td>'
    data += '<td colspan = 2 style="border-color:#000000;"><center><b>Total Amount(RSC)</b></center></td>'
    data += '<td colspan = 2 style="border-color:#000000;"><center><b>Total Amount(RS)</b></center></td>'
    data += '<td colspan = 2 style="border-color:#000000;"><center><b>Total Amount(Quoted)</b></center></td>'
    
    data += '</tr>'
    wo = frappe.db.sql(""" select DISTINCT sales_rep from `tabWork Order Data` """,as_dict =1)
    data += '<tr>'
    data += '<td style="border-color:#000000;width:10%"><center><b>Salesman</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;"><center><b>WO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;"><center><b>SO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;"><center><b>WO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;"><center><b>SO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;"><center><b>WO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;"><center><b>SO(in KD)</b></center></td>'
    data += '<td style="border-color:#000000;width:10%;"><center><b>WO(in KD)</b></center></td>'  
    data += '<td style="border-color:#000000;width:10%;"><center><b>SO(in KD)</b></center></td>'	
    data += '</tr>'
    current_date_time = datetime.now()

    # Extract and print the current date
    current_date = current_date_time.date()
    # Week_start = add_days(current_date,-6)
    Week_start = "2023-09-23"

    total_rsi = 0
    total_rsc = 0
    total_rs = 0
    total_quotation = 0
    for i in wo:
        if not i["sales_rep"] == None:
            if not i["sales_rep"] == '':
                wds = frappe.get_all("Work Order Data",{"sales_rep":i["sales_rep"],"status":"RSI-Repaired and Shipped Invoiced","posting_date": ["between", (Week_start,current_date)]})
                 # RSI
                squot = 0
                for j in wds:
                    rsi_q = frappe.db.sql(''' select `tabQuotation`.after_discount_cost, `tabQuotation`.Workflow_state,`tabQuotation Item`.margin_amount from `tabQuotation` 
                    left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    where `tabQuotation`.Workflow_state = "Approved By Customer"  and `tabQuotation Item`.wod_no = %s  and `tabQuotation`.is_multiple_quotation = 0 ''',j.name,as_dict=1)
                    
                    for k in rsi_q:
                        squot = squot + k["after_discount_cost"]
            

                mquot = 0
                for j in wds:
                    rsi_mq = frappe.db.sql(''' select `tabQuotation`.after_discount_cost, `tabQuotation`.Workflow_state,`tabQuotation Item`.margin_amount from `tabQuotation` 
                    left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    where `tabQuotation`.Workflow_state = "Approved By Customer"  and `tabQuotation Item`.wod_no = %s  and `tabQuotation`.is_multiple_quotation = 1 ''',j.name,as_dict=1)
                    
                    for k in rsi_mq:
                        mquot = mquot + k["margin_amount"]
            
                rsi_total = squot + mquot

                # RSC	
                
                wds_rsc = frappe.get_all("Work Order Data",{"sales_rep":i["sales_rep"],"status":"RSC-Repaired and Shipped Client","posting_date": ["between", (Week_start,current_date)]})
                
                rsc_squot = 0
                for j in wds_rsc:
                    rsc_q = frappe.db.sql(''' select `tabQuotation`.after_discount_cost, `tabQuotation`.Workflow_state,`tabQuotation Item`.margin_amount from `tabQuotation` 
                    left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    where `tabQuotation`.Workflow_state = "Approved By Customer"  and `tabQuotation Item`.wod_no = %s  and `tabQuotation`.is_multiple_quotation = 0 ''',j.name,as_dict=1)
                    
                    for k in rsc_q:
                        rsc_squot = rsc_squot + k["after_discount_cost"]
            

                rsc_mquot = 0
                for j in wds_rsc:
                    rsc_mq = frappe.db.sql(''' select `tabQuotation`.after_discount_cost, `tabQuotation`.Workflow_state,`tabQuotation Item`.margin_amount from `tabQuotation` 
                    left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    where `tabQuotation`.Workflow_state = "Approved By Customer"  and `tabQuotation Item`.wod_no = %s  and `tabQuotation`.is_multiple_quotation = 1 ''',j.name,as_dict=1)
                    
                    for k in rsc_mq:
                        rsc_mquot = rsc_mquot + k["margin_amount"]

                #RS				
                wds_rs = frappe.get_all("Work Order Data",{"sales_rep":i["sales_rep"],"status":"RS-Repaired and Shipped","posting_date": ["between", (Week_start,current_date)]})
                
                rs_squot = 0
                for j in wds_rs:
                    rs_q = frappe.db.sql(''' select `tabQuotation`.after_discount_cost, `tabQuotation`.Workflow_state,`tabQuotation Item`.margin_amount from `tabQuotation` 
                    left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    where `tabQuotation`.Workflow_state = "Approved By Customer"  and `tabQuotation Item`.wod_no = %s  and `tabQuotation`.is_multiple_quotation = 0 ''',j.name,as_dict=1)
                    
                    for k in rs_q:
                        rs_squot = rs_squot + k["after_discount_cost"]
            

                rs_mquot = 0
                for j in wds_rs:
                    rs_mq = frappe.db.sql(''' select `tabQuotation`.after_discount_cost, `tabQuotation`.Workflow_state,`tabQuotation Item`.margin_amount from `tabQuotation` 
                    left join `tabQuotation Item` on  `tabQuotation`.name = `tabQuotation Item`.parent
                    where `tabQuotation`.Workflow_state = "Approved By Customer"  and `tabQuotation Item`.wod_no = %s  and `tabQuotation`.is_multiple_quotation = 1 ''',j.name,as_dict=1)
                    
                    for k in rs_mq:
                        rs_mquot = rs_mquot + k["margin_amount"]
            
                rsi_total = squot + mquot
                rsc_total = rsc_squot + rsc_mquot
                rs_total = rs_squot + rs_mquot

                total_rsi = total_rsi + rsi_total
                total_rsc = total_rsc + rsc_total
                total_rs = total_rs + rs_total 

                total_q = frappe.db.sql(''' select sum(after_discount_cost) as t from `tabQuotation` 
                where Workflow_state = "Approved By Customer"  and sales_rep = %s ''',i["sales_rep"],as_dict=1)
                print(total_q[0]["t"])
                if total_q[0]["t"] == None:
                    total_q[0]["t"] = 0

                total_quotation = total_quotation + total_q[0]["t"] 

                data += '<tr>'
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %(i["sales_rep"])
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %(rsi_total)
                data += '<td style="border-color:#000000;"><center><b></b></center></td>'
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %(rsc_total)
                data += '<td style="border-color:#000000;"><center><b></b></center></td>'
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>'%(rs_total)
                data += '<td style="border-color:#000000;"><center><b></b></center></td>'
                data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>'%(total_q[0]["t"])
                data += '<td style="border-color:#000000;"><center><b></b></center></td>'	
                data += '</tr>'
    data += '<tr>'
    data += '<td style="border-color:#000000;"><center><b>Total</b></center></td>'
    data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %(total_rsi)
    data += '<td style="border-color:#000000;"><center><b></b></center></td>'
    data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>' %(total_rsc)
    data += '<td style="border-color:#000000;"><center><b></b></center></td>'
    data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>'%(total_rs)
    data += '<td style="border-color:#000000;"><center><b></b></center></td>'
    data += '<td style="border-color:#000000;"><center><b>%s</b></center></td>'%(total_quotation )
    data += '<td style="border-color:#000000;"><center><b></b></center></td>' 
    data += '</tr>'

    data += '</table>'
    data += '</div>'
    
    return data


@frappe.whitelist()
def get_wrk_ord(from_date,to_date,customer,work_order_data,sales_person,report):
    if report == "RSI-Repaired and Shipped Invoiced":
        data= ""
        data += '<table class="table table-bordered">'

        data += '<tr>'
        data += '<td colspan = 3 style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="150"></td>'
        data += '<td colspan = 4 style="border-color:#000000;"><h1><center><b>Sales Summary Report</b></center></h1></td>'
        
        data += '</tr>'


        data += '<tr>'
        data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">S.No</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Date</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Work Order</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Sales Person</td>'
        data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Sales Invoice</td>'
        data += '<td style="border-color:#000000;width:35%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Customer</td>'
        data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Amount</td>'
        data += '</tr>'
        
        if customer:
            si = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.due_date, `tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
            left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
            where `tabSales Invoice`.status = "Overdue" and `tabSales Invoice`.due_date between '%s' and '%s' and `tabSales Invoice`.customer = '%s' """ %(from_date,to_date,customer),as_dict =1)
        
        elif sales_person:
            si = frappe.db.sql(""" select DISTINCT  `tabSales Invoice`.due_date,`tabSales Team`.sales_person,`tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
            left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
            right join `tabSales Team` on `tabSales Invoice`.name = `tabSales Team`.parent
            where `tabSales Invoice`.status = "Overdue" and `tabSales Team`.sales_person = '%s' and `tabSales Invoice`.due_date between '%s' and '%s' ORDER BY `tabSales Invoice`.due_date ASC """ %(sales_person,from_date,to_date),as_dict =1)

        elif work_order_data:
            si = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.due_date,`tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
            left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
            where `tabSales Invoice`.status = "Overdue" and `tabSales Invoice`.due_date between '%s' and '%s' and `tabSales Invoice Item`.work_order_data = '%s' """ %(from_date,to_date,work_order_data),as_dict =1)
            if not si:
                si = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.due_date,`tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
                left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                where `tabSales Invoice`.due_date between '%s' and '%s' and `tabSales Invoice Item`.wod_no = '%s' """ %(from_date,to_date,work_order_data),as_dict =1)


        else:
            si = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.due_date, `tabSales Invoice Item`.work_order_data as wo,`tabSales Invoice Item`.wod_no as w from `tabSales Invoice` 
            left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
            where `tabSales Invoice`.status = "Overdue" and `tabSales Invoice`.due_date between '%s' and '%s' """ %(from_date,to_date),as_dict =1)


            
        wod_list = []
        for j in si:
            if j["wo"]:
                wod_list.append(j["wo"])
            else:
                wod_list.append(j["w"])
                
        sn = 0
        total_amt = 0
        for i in wod_list:
            st = frappe.get_value("Work Order Data",{"name":i},["Status"])
            
            if i:
                sid_1 = frappe.db.sql(""" select `tabSales Invoice`.due_date from `tabSales Invoice` 
                left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                where `tabSales Invoice Item`.work_order_data = '%s' """ %(i),as_dict =1)

                sid_2 = frappe.db.sql(""" select `tabSales Invoice`.due_date from `tabSales Invoice` 
                left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                where `tabSales Invoice Item`.wod_no = '%s' """ %(i),as_dict =1)
            

                sales_rep_1 = frappe.db.sql(""" select `tabSales Team`.sales_person from `tabSales Invoice` 
                left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                right join `tabSales Team` on `tabSales Invoice`.name = `tabSales Team`.parent
                where `tabSales Invoice Item`.work_order_data = '%s' """ %(i),as_dict =1)
                    
                sales_rep_2 = frappe.db.sql(""" select `tabSales Team`.sales_person from `tabSales Invoice` 
                left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                right join `tabSales Team` on `tabSales Invoice`.name = `tabSales Team`.parent
                where `tabSales Invoice Item`.wod_no = '%s' """ %(i),as_dict =1)
                    
                cust = frappe.get_value("Work Order Data",{"name":i},["customer"])
            
                if sid_1:
                    input_date_string = str(sid_1[0]["due_date"])
                else:
                    input_date_string = str(sid_2[0]["due_date"])

                if input_date_string:
                    input_date = datetime.strptime(input_date_string, "%Y-%m-%d")

                
                formatted_date = input_date.strftime("%d-%m-%Y")
                
                
                wo = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.name, `tabSales Invoice Item`.amount as amount from `tabSales Invoice` 
                left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                where `tabSales Invoice Item`.work_order_data = '%s' """ %(i),as_dict =1)
                amt = 0
                n = []
                if wo:
                    amt = wo[0]["amount"]
                    n.append(wo[0]["name"])
                    n = str(n).strip('[]')
                    n = n.replace("'", '')
                    
                
                else:
                    wos = frappe.db.sql(""" select DISTINCT `tabSales Invoice`.name,`tabSales Invoice Item`.amount as amount from `tabSales Invoice` 
                    left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                    where `tabSales Invoice Item`.wod_no = '%s' """ %(i),as_dict =1)
                    amt = wos[0]["amount"]
                    n.append(wos[0]["name"])
                    n = str(n).strip('[]')
                    n = n.replace("'", '')
                
                
                total_amt = total_amt + amt
                sn = sn + 1
                data += '<tr>'
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sn)
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date)
                    
                
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/work-order-data/%s"target="_blank">%s</a><center></td>'%(i,i)
                if sales_rep_1:
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sales_rep_1[0]["sales_person"] or "-" )
                elif sales_rep_2:
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sales_rep_2[0]["sales_person"] or "-" )
                else:
                    data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%("-" )

                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/sales-invoice/%s"target="_blank">%s</a><center></td>'%(n,n)
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(cust)
                data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>' %(format(amt, ".2f"))
            
        data += '<tr>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Total</td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">%s</td>'%(format(total_amt, ".2f"))
        data += '</tr>'
        data += '</table>'
    
    if report == "RSC-Repaired and Shipped Client":
        data= ""
        data += '<table class="table table-bordered">'

        data += '<tr>'
        data += '<td colspan = 3 style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="150"></td>'
        data += '<td colspan = 5 style="border-color:#000000;"><h1><center><b>Sales Summary Report</b></center></h1></td>'
        
        data += '</tr>'

        data += '</tr>'
        data += '<tr>'
        data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">S.No</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Date</td>'
        data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Work Order</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Sales Person</td>'
        data += '<td style="border-color:#000000;width:30%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Customer</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Delivery Note</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Delivery Date</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Amount</td>'
        data += '</tr>'
        
        if customer:
            wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (from_date,to_date)],"status":"RSC-Repaired and Shipped Client","customer":customer},["*"])

        elif sales_person:
            wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (from_date,to_date)],"status":"RSC-Repaired and Shipped Client","sales_rep":sales_person},["*"])

        elif work_order_data:
            wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (from_date,to_date)],"status":"RSC-Repaired and Shipped Client","name":work_order_data},["*"])

        else:
            wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (from_date,to_date)],"status":"RSC-Repaired and Shipped Client"},["*"])
        
        sn = 0
        total_rsc = 0
        for i in wd:
            amount = 0
            amt = frappe.db.sql(""" select `tabQuotation`.after_discount_cost as cost  from `tabQuotation` 
            left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
            where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Customer' """ %(i.name),as_dict =1)
            if amt:
                amount = amt[0]["cost"]
            else:
                am = frappe.db.sql(""" select `tabQuotation`.after_discount_cost as cos  from `tabQuotation` 
                left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
                where `tabQuotation Item`.wod_no = '%s' and `tabQuotation`.workflow_state = 'Approved By Management' """ %(i.name),as_dict =1)
                if am:
                    amount = am[0]["cos"]
                    
            sn = sn+1

            input_date_string_1 = str(i.posting_date)
            input_date_string_2 = str(i.dn_date)

            input_date_1 = datetime.strptime(input_date_string_1, "%Y-%m-%d")
            if i.dn_date:
                input_date_2 = datetime.strptime(input_date_string_2, "%Y-%m-%d")


            formatted_date_1 = input_date_1.strftime("%d-%m-%Y")
            if input_date_2:
                formatted_date_2 = input_date_2.strftime("%d-%m-%Y")
            
                
            data += '<tr>'
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sn)
                
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date_1)
            
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/work-order-data/%s"target="_blank">%s</a><center></td>'%(i.name,i.name)
                
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.sales_rep)

            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.customer)
                
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/delivery-note/%s"target="_blank">%s</a><center></td>'%(i.dn_no,i.dn_no)					

            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date_2)

            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(format(amount, ".2f"))
            total_rsc = total_rsc + amount
            
        data += '<tr>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"></td>'
        data += '<td align = center style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;">Total</td>'
        data += '<td align = center style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;font-weight:bold;">%s</td>'%(format(total_rsc, ".2f"))
        data += '</tr>'

    if report == "Q-Quoted":
        data= ""
        data += '<table class="table table-bordered">'
        
        data += '<tr>'
        data += '<td colspan = 3 style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="150"></td>'
        data += '<td colspan = 4 style="border-color:#000000;"><h1><center><b>Sales Summary Report</b></center></h1></td>'
        
        data += '</tr>'
        
        data += '<tr>'
        data += '<td style="border-color:#000000;width:5%;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">S.No</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Date</td>'
        data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Work Order</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Sales Person</td>'
        data += '<td style="border-color:#000000;width:15%;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Quotation</td>'
        data += '<td style="border-color:#000000;width:35%;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Customer</td>'
        data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Amount</td>'
        data += '</tr>'
        
        if customer:
            wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (from_date,to_date)],"status":"Q-Quoted","customer":customer},["*"])

        elif sales_person:
            wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (from_date,to_date)],"status":"Q-Quoted","sales_rep":sales_person},["*"])

        elif work_order_data:
            wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (from_date,to_date)],"status":"Q-Quoted","name":work_order_data},["*"])

        else:
            wd = frappe.get_all("Work Order Data",{"posting_date": ["between", (from_date,to_date)],"status":"Q-Quoted"},["*"])
        
        sn = 0
        total_amt = 0
        for i in wd:
            sn = sn+1
            ada  = si = frappe.db.sql(""" select DISTINCT `tabQuotation`.is_multiple_quotation as multi,`tabQuotation`.name as qname,`tabQuotation Item`.margin_amount as ma,`tabQuotation`.after_discount_cost as adc from `tabQuotation` 
            left join `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent 
            where `tabQuotation Item`.wod_no = '%s' """ %(i.name),as_dict =1)
            amt = 0
            if ada:
                if ada[0]["multi"] == 1:
                    amt = ada[0]["ma"]
                else:
                    amt = ada[0]["adc"]

            total_amt = total_amt + amt

            
            input_date_string = str(i.posting_date)

            input_date = datetime.strptime(input_date_string, "%Y-%m-%d")

            formatted_date = input_date.strftime("%d-%m-%Y")
                

            data += '<tr>'
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(sn)
                
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(formatted_date)
            
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/work-order-data/%s"target="_blank">%s</a><center></td>'%(i.name,i.name)
                
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.sales_rep)

            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><a href="https://erp.tsl-me.com/app/quotation/%s"target="_blank">%s</a><center></td>'%(ada[0]["qname"],ada[0]["qname"])					

            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(i.customer)
                
        
            data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center>%s<center></td>'%(amt)
    
        data += '<tr>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;"></td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">Total</td>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#4169E1;color:white;text-align:center;font-weight:bold;">%s</td>' %(total_amt)
        data += '</tr>'

    
    return data


@frappe.whitelist()
def change_shipping_cost(currency,sq):
    ship_cost = frappe.get_value("Supplier Quotation",{"supply_order_data":sq,"workflow_state":"Approved By Management"},["Shipping_cost"])
    base_total = frappe.get_value("Supplier Quotation",{"supply_order_data":sq,"workflow_state":"Approved By Management"},["base_total"])
    supplier = frappe.get_value("Supplier Quotation",{"supply_order_data":sq},["supplier"])
    cur = frappe.get_value("Supplier",{"name":supplier},["default_currency"])
    if not cur:
        frappe.throw("Please select default currency for the supplier %s " %(supplier))
    exr = get_exchange_rate(cur,currency)
    cost = ship_cost * exr
    return cost,base_total,supplier

@frappe.whitelist()
def crt_wo(import_file):
    from datetime import datetime
    filepath = get_file(import_file)
    data = read_csv_content(filepath[1])
    count = 0
    a_date = ''
    p_date = ''
    d_date = ''
    Pd_date = ''

    for i in data[1:]:
        count = count + 1
        print(count)
        wo = frappe.new_doc("Work Order Data")
        cus = frappe.db.exists("Customer",{"name": i[3]})
        if not cus:
            c = frappe.new_doc("Customer")
            c.customer_name = i[3]
            c.territory = "Kuwait"
            c.customer_type = "Company"
            c.company_group = "Kuwait"
            c.save(ignore_permissions = 1)
            
        sp = frappe.db.exists("Sales Person",{"name": i[1]})
        if not sp:
            s = frappe.new_doc("Sales Person")
            s.sales_person_name= i[1]
            s.parent_sales_person = "Sales Team"
            s.save(ignore_permissions =1)
        
        # Input date string
        if i[2]:
            date_ad = str(i[2])
            day, month, year = date_ad.split("/")
            if month == "Jan":
                month = "1"
            if month == "Feb":
                month = "2"
            if month == "Mar":
                month = "3"
            if month == "Apr":
                month = "4"
            if month == "May":
                month = "5"
            if month == "Jun":
                month = "6"
            if month == "Jul":
                month = "7"
            if month == "Aug":
                month = "8"
            if month == "Sep":
                month = "9"
            if month == "Oct":
                month = "10"
            if month == "Nov":
                month = "11"
            if month == "Dec":
                month = "12"
            
            if year == "17":
                year = "2017" 
            if year == "18":
                year = "2018" 
            if year == "19":
                year = "2019" 
            if year == "20":
                year = "2020" 
            if year == "21":
                year = "2021" 
            if year == "22":
                year = "2022" 
            if year == "23":
                year = "2023" 
            if year == "24":
                year = "2024" 


            result = "-".join([year,month,day])
            p_date = result
        else:
            p_date = ''
        
        

        if i[7]:
            date_ad = str(i[7])
            day, month, year = date_ad.split("/")
            if month == "Jan":
                month = "1"
            if month == "Feb":
                month = "2"
            if month == "Mar":
                month = "3"
            if month == "Apr":
                month = "4"
            if month == "May":
                month = "5"
            if month == "Jun":
                month = "6"
            if month == "Jul":
                month = "7"
            if month == "Aug":
                month = "8"
            if month == "Sep":
                month = "9"
            if month == "Oct":
                month = "10"
            if month == "Nov":
                month = "11"
            if month == "Dec":
                month = "12"
            
            if year == "17":
                year = "2017" 
            if year == "18":
                year = "2018" 
            if year == "19":
                year = "2019" 
            if year == "20":
                year = "2020" 
            if year == "21":
                year = "2021" 
            if year == "22":
                year = "2022" 
            if year == "23":
                year = "2023" 
            if year == "24":
                year = "2024" 


            result = "-".join([year,month,day])
            a_date = result
        else:
            a_date = ''
        
            

        if i[8]:
            date_ad = str(i[8])
            day, month, year = date_ad.split("/")
            if month == "Jan":
                month = "1"
            if month == "Feb":
                month = "2"
            if month == "Mar":
                month = "3"
            if month == "Apr":
                month = "4"
            if month == "May":
                month = "5"
            if month == "Jun":
                month = "6"
            if month == "Jul":
                month = "7"
            if month == "Aug":
                month = "8"
            if month == "Sep":
                month = "9"
            if month == "Oct":
                month = "10"
            if month == "Nov":
                month = "11"
            if month == "Dec":
                month = "12"
            
            if year == "17":
                year = "2017" 
            if year == "18":
                year = "2018" 
            if year == "19":
                year = "2019" 
            if year == "20":
                year = "2020" 
            if year == "21":
                year = "2021" 
            if year == "22":
                year = "2022" 
            if year == "23":
                year = "2023" 
            if year == "24":
                year = "2024" 


            result = "-".join([year,month,day])
            d_date = result
        else:
            d_date = ''
        
        

        if i[9]:
            date_ad = str(i[9])
            day, month, year = date_ad.split("/")
            if month == "Jan":
                month = "1"
            if month == "Feb":
                month = "2"
            if month == "Mar":
                month = "3"
            if month == "Apr":
                month = "4"
            if month == "May":
                month = "5"
            if month == "Jun":
                month = "6"
            if month == "Jul":
                month = "7"
            if month == "Aug":
                month = "8"
            if month == "Sep":
                month = "9"
            if month == "Oct":
                month = "10"
            if month == "Nov":
                month = "11"
            if month == "Dec":
                month = "12"
            
            if year == "17":
                year = "2017" 
            if year == "18":
                year = "2018" 
            if year == "19":
                year = "2019" 
            if year == "20":
                year = "2020" 
            if year == "21":
                year = "2021" 
            if year == "22":
                year = "2022" 
            if year == "23":
                year = "2023" 
            if year == "24":
                year = "2024" 


            result = "-".join([year,month,day])
            pd_date = result
        else:
            pd_date = ''
        
        print(i[0])
        print(p_date)
        print(a_date)
        print(d_date)
        print(pd_date)
            
        
        if i[6] == "P" or i[6] == "p":
            i[6] = 'P-Paid'
        if i[6] == "RNRC":
            i[6] = 'RNRC-Return Not Repaired Client'
        if i[6] == "A":
            i[6] = 'A-Approved'
        if i[6] == "C":
            i[6] = 'C-Comparison'
        if i[6] == "CC":
            i[6] = 'CC-Comparison Client'
        if i[6] == "EP" or i[6] == "ED":
            i[6] = 'EP-Extra Parts'
        if i[6] == "NE":
            i[6] = 'NE-Need Evaluation'
        if i[6] == "NER":
            i[6] = 'NER-Need Evaluation Return'
        if i[6] == "Q":
            i[6] = 'Q-Quoted'
        if i[6] == "RNA":
            i[6] = 'RNA-Return Not Approved'
        if i[6] == "RNAC":
            i[6] = 'RNAC-Return Not Approved Client'
        if i[6] == "RNF":
            i[6] = 'RNF-Return No Fault'
        if i[6] == "RNFC":
            i[6] = 'RNFC-Return No Fault Client'
        if i[6] == "RNP":
            i[6] = 'RNP-Return No Parts'
        if i[6] == "RNPC":
            i[6] = 'RNPC-Return No Parts Client'
        if i[6] == "RNR":
            i[6] = 'RNR-Return Not Repaired'
        if i[6] == "RNRC":
            i[6] = 'RNRC-Return Not Repaired Client'
        if i[6] == "RS":
            i[6] = 'RS-Repaired and Shipped'
        if i[6] == "RSC":
            i[6] = 'RSC-Repaired and Shipped Client'
        if i[6] == "RSI":
            i[6] = 'RSI-Repaired and Shipped Invoiced'
        if i[6] == "SP":
            i[6] = 'SP-Searching Parts'
        if i[6] == "TR":
            i[6] ='TR-Technician Repair'
        if i[6] == "UE":
            i[6] = 'UE-Under Evaluation'
        if i[6] == "UTR":
            i[6] = 'UTR-Under Technician Repair'
        if i[6] == "W":
            i[6] = "W-Working"
        if i[6] == "WP":
            i[6] = 'WP-Waiting Parts'

        wo.naming_series = "WOD-KO.YY.-"
        wo.customer = i[3]
        wo.old_wo_no = i[0]
        wo.status = i[6]
        wo.sales_rep = i[1]
        wo.posting_date = p_date
        wo.old_wo_q_amount = i[5]
        wo.quoted_date = a_date
        wo.payment_date = pd_date
        wo.delivery = d_date
        wo.no_power = 1
        wo.append("material_list", {
                
            'item_code': "001300",
            'model_no': "Old",
            "mfg":"Old mfg",
            "type": "Old",
            "item_name":"001300",
            "quantity" :1
                
        })
        wo.save(ignore_permissions = 1)

@frappe.whitelist()
def dlt_wo():
    wo = frappe.db.sql(""" delete from `tabWork Order Data` where old_wo_no IS NOT NULL """)

@frappe.whitelist()
def update_wo():
    wo = frappe.db.sql(""" UPDATE `tabWork Order Data` SET docstatus = 1 WHERE old_wo_no IS NOT NULL; """)


@frappe.whitelist()
def set_alert_urgent():
    w = frappe.get_all("Work Order Data",["*"])
    tody = datetime.now().date()
    data = ""
    data += '<p>Hi</p>'
    data += '<p>Kindly find the below Work orders are pending for 2 days.Please take necessary action to click Work order</p>'
    count = 0
    for i in w:
        if not i.old_wo_no and i.priority_status == "Urgent":
            qu = frappe.db.sql(""" select `tabQuotation`.name  from `tabQuotation` left join 
            `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
            where `tabQuotation`.workflow_state  != "Rejected by Customer" and `tabQuotation Item`.wod_no = '%s' """ %(i.name) ,as_dict=1)
            if not qu:
                d = add_days(i.posting_date,2)
                if d <= tody:
                    if not i.status == "RNA-Return Not Approved" and not i.status == "RNF-Return No Fault":
                        count = count + 1
                        data += '<p><a href="https://erp.tsl-me.com/app/work-order-data/%s">%s-%s</a></p>' % (i.name,i.name,i.status)
                    # data += '<table class="table table-bordered">'
                    # data += '<tr>'
                    # data += '<td colspan = "2" style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;b"><center><b>Work Orders</b><center></td>'
                    # data += '</tr>'

                    # data += '<tr>'
                    # data += '<td colspan = "2" style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;b"><center><b>%s</b><center></td>' %(i.name)
                    # data += '</tr>'
                    # data += '</table>'

    
    # message = """{}""".format(data)
    
    if count > 0:
        frappe.sendmail(recipients=["omar@tsl-me.com"],
                        sender="Notification from TSL <info@tsl-me.com>",
                        subject="Work Orders - Pending",
                        message=data)

@frappe.whitelist()
def set_alert_normal():
    w = frappe.get_all("Work Order Data",["*"])
    tody = datetime.now().date()
    data = ""
    data += '<p>Hi</p>'
    data += '<p>Kindly find the below Work orders are pending for 6 days.Please take necessary action to click Work order</p>'
    count = 0
    for i in w:	
        if not i.old_wo_no and i.priority_status == "Normal":
            qu = frappe.db.sql(""" select `tabQuotation`.name  from `tabQuotation` left join 
            `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent
            where `tabQuotation`.workflow_state  != "Rejected by Customer" and `tabQuotation Item`.wod_no = '%s' """ %(i.name) ,as_dict=1)
            if not qu:
                d = add_days(i.posting_date,6)
                if d <= tody:
                    if not i.status == "RNA-Return Not Approved" and not i.status == "RNF-Return No Fault":
                        count = count + 1
                        data += '<p><a href="https://erp.tsl-me.com/app/work-order-data/%s">%s</a></p>' % (i.name,i.name)

                    # data += '<table class="table table-bordered">'
                    # data += '<tr>'
                    # data += '<td colspan = "2" style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;b"><center><b>Work Orders</b><center></td>'
                    # data += '</tr>'

                    # data += '<tr>'
                    # data += '<td colspan = "2" style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;b"><center><b>%s</b><center></td>' %(i.name)
                    # data += '</tr>'
                    # data += '</table>'

    
    # message = """{}""".format(data)
    # print(message)
    if count > 0:
        frappe.sendmail(recipients=["omar@tsl-me.com"],
                        sender="Notification from TSL <info@tsl-me.com>",
                        subject="Work Orders - Pending",
                        message=data)


@frappe.whitelist()
def send_mail_to_customer(q,type,email):
    if type == "Customer Quotation - Repair":
        if email:
            frappe.sendmail(recipients=[email],
            sender="Notification from TSL <info@tsl-me.com>",
            subject="Quotation from TSL",
            message=""" 
            <p>Dear Mr / Mrs</p><br>
            <p>Please find the attached quotation for the repair.
            We are waiting for your approval for further processing.</p>
            """,
            attachments=get_attachments(q,"Quotation")
            )
            frappe.msgprint("Mail Successfully Sent to Customer")
            
    if type == "Customer Quotation - Supply":
        if email:
            frappe.sendmail(recipients=[email],
            sender="Notification from TSL <info@tsl-me.com>",
            subject="Quotation from TSL",
            message=""" 
            <p>Dear Mr / Mrs</p><br>
            <p>Please find the attached quotation for the supply.
            We are waiting for your approval for further processing.</p>
            """,
            attachments=get_attach(q,"Quotation")
            )
            frappe.msgprint("Mail Successfully Sent to Customer")
        


def get_attachments(name,doctype):
    attachments = frappe.attach_print(doctype, name,file_name=doctype, print_format="Quotation TSL")
    return [attachments]

def get_attach(name,doctype):
    attachments = frappe.attach_print(doctype, name,file_name=doctype, print_format="Supply Quotation")
    return [attachments]

@frappe.whitelist()
def customer_notification():
    si = frappe.get_all("Sales Invoice",["*"])
    tody = datetime.now().date()
    for i in si:
        d = add_days(i.posting_date,6)
        if tody == d and i.send_later:
            email = frappe.get_value("Customer",{"name":i.customer},["email_id"])
            if email:
                frappe.sendmail(recipients=["karthiksrinivasan1996.ks@gmail.com"],
                sender="Notification from TSL <info@tsl-me.com>",
                subject="Quotatio from TSL - ",
                message=""" 
                <p>Dear Mr / ms</p><br>
                Please find the attached Invoice and delivery copy as requested.
                Kindly issue the payment as soon as possible.</p>
                """,
                attachments=get_attachments(i.name,"Sales Invoice")
                )



@frappe.whitelist()
def cron_job_allocation():
    job = frappe.db.exists('Scheduled Job Type', 'urgent_work_order')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")  
        sjt.update({
            "method" : 'tsl.custom_py.utils.set_alert_normal',
            "frequency" : 'Daily',
            "cron_format" : '0 8 * * *'
        })
        sjt.save(ignore_permissions=True)

@frappe.whitelist()
def crt_item(import_file):
    from datetime import datetime
    filepath = get_file(import_file)
    data = read_csv_content(filepath[1])
    c = 0
    for i in data:
        s = frappe.db.exists("Item",{"name":i[1],"published_in_website":0})
        if s:
            frappe.db.set_value("Item",i[1],"published_in_website",1)
            c = c +1
            print(c)
    
@frappe.whitelist()
def update_ner(wod):
    frappe.errprint(wod)
    # frappe.db.set_value("Work Order Data",wod,"status_cap","")
    # ev = frappe.get_doc("Evaluation Report",{"work_order_data":wod})
    # ev.ner_field = ""
    # ev.save(ignore_permissions =1)

@frappe.whitelist()
def update_item(model,item):
    i = frappe.db.exists("Item",item)
    if i:
        it = frappe.get_doc("Item",item)
        it.model = model
        it.save(ignore_permissions = 1)
        frappe.msgprint("Model Number Updated")

@frappe.whitelist()
def salary_register(month_name,company,cyrix_employee):
    from datetime import timedelta
    current_year = datetime.now().year
    month_number = datetime.strptime(month_name, '%B').month
    
    first_date = datetime(current_year, month_number, 1)
    if month_number == 12:
        last_date = datetime(current_year, month_number, 31)
    else:
        next_month = datetime(current_year, month_number + 1, 1)
        last_date = next_month - timedelta(days=1)
    if company == "TSL COMPANY - Kuwait":
        filters = {'from_date': first_date.date(), 'to_date': last_date.date(), 'currency': 'KWD', 'company': company, 'docstatus': 'Draft'}
    if company == "TSL COMPANY - KSA":
        filters = {'from_date': first_date.date(), 'to_date': last_date.date(), 'currency': 'SAR', 'company': company, 'docstatus': 'Draft'}
    if company == "TSL COMPANY - UAE":
        filters = {'from_date': first_date.date(), 'to_date': last_date.date(), 'currency': 'AED', 'company': company, 'docstatus': 'Draft'}
    from hrms.payroll.report.salary_register.salary_register import execute
    result = execute(filters)
    headers = result[0]
    records = result[1]
    skip_columns = ['total_loan_repayment','company','salary_slip_id', 'branch', 'date_of_joining', 'start_date', 'end_date','currency','data_of_joining']
    int_columns = ['leave_without_pay', 'payment_days']
    currency_columns = [header['fieldname'] for header in headers if header.get('fieldtype') == 'Currency']
    filtered_headers = []
    for header in headers:
        if header['fieldname'] in skip_columns:
            continue
        # if header['fieldname'] == 'total_loan_repayment':
        #     header['label'] = 'Loan'
        if header['fieldname'] == 'loan':
            header['label'] = 'Loan Deduction'
        filtered_headers.append(header)
    totals = {fieldname: 0.0 for fieldname in currency_columns}

    # Generate HTML table headers
    data = '<table border="1" width="100%"><tr><td style="text-align:right;font-size:6px;font-weight:bold">Sl.No.</td>'
    data += ''.join(f'<td style="font-size:7px;font-weight:bold">{header["label"]}</td>' for header in filtered_headers)
    data += '</tr>'

    # Generate HTML table rows
    sl_no = 1
    for record in records:
        cyrix = frappe.db.get_value("Employee",record.get('employee'),'cyrix_employee_')
        if cyrix == cyrix_employee:
            data += '<tr>'
            data += f'<td style="font-size:6px">{sl_no}</td>'

            for header in filtered_headers:
                fieldname = header['fieldname']
                fieldtype = header.get('fieldtype', '')
                cell_value = record.get(fieldname, 0)  # Default to 0 if None
                
                # Update totals for currency columns
                if fieldname in currency_columns:
                    totals[fieldname] += float(cell_value) if isinstance(cell_value, (float, int)) else 0
                
                # Format cell value
                if fieldtype == 'Currency':
                    cell_value = "{:,.3f}".format(cell_value) if isinstance(cell_value, (float, int)) else "0.000"
                elif isinstance(cell_value, float):
                    # cell_value = f"{cell_value:.3f}"
                    cell_value = "{:,.3f}".format(cell_value) 
                data += f'<td style="font-size:6px">{cell_value or ""}</td>'
            data += '</tr>'
            sl_no += 1

    # Generate totals row for currency columns
    data += '<tr>'

    # Determine the number of non-currency columns before the first currency column
    first_currency_index = next((i for i, header in enumerate(filtered_headers) if header['fieldname'] in currency_columns), len(filtered_headers))
    non_currency_colspan = first_currency_index + 1

    # Add merged cell for 'Total' title
    if non_currency_colspan > 0:
        data += f'<td style="font-size:6px;font-weight:bold;text-align:center" colspan="{non_currency_colspan}">Total</td>'

    # Add empty cells for any columns between the merged 'Total' cell and the first currency column
    for i in range(non_currency_colspan, first_currency_index):
        data += '<td></td>'

    # Add total values for currency columns and empty cells for non-currency columns after 'Total'
    for i, header in enumerate(filtered_headers[first_currency_index:], start=first_currency_index):
        fieldname = header['fieldname']
        if fieldname in currency_columns:
            total_value = "{:,.3f}".format(totals[fieldname])
        else:
            total_value = ''
        data += f'<td style="font-size:6px;font-weight:bold">{total_value}</td>'
    data += '</tr>'

    data += '</table>'

    return data


@frappe.whitelist()
def update_wd():
    s = frappe.db.sql(""" UPDATE `tabWork Order Data` SET tech_id = 5 WHERE technician = "sami@tsl-me.com" """)
    

@frappe.whitelist()
def get_sales(from_date,to_date,company):
    data= ""
    data += '<table class="table table-bordered">'

    data += '<tr>'
    data += '<td colspan = 3 style="border-color:#000000;"><img src = "/files/TSL Logo.png" align="left" width ="200"></td>'
    data += '<td colspan = 9 style="border-color:#000000;"><h1><center><b>Incentive Report</b></center></h1></td>'
    
    data += '<tr>'
    data += '<td colspan = 1 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
    data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">RS</b><center></td>'
    data += '<td colspan = 5 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">NER</b><center></td>'
    data += '<td colspan = 1 style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b></b><center></td>'
    data += '</tr>'	
    

    data += '<tr>' 
    data += '<td style="border-color:#000000;width:10%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:14px;">RANGE<center></td>'
    data += '<td style="border-color:#000000;width:5%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:10px;">1 - 320<center></td>'
    data += '<td style="border-color:#000000;width:5%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:10px;">320 - 640<center></td>'
    data += '<td style="border-color:#000000;width:5%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:10px;">640 - 1200<center></td>'
    data += '<td style="border-color:#000000;width:5%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:10px;">1200 ><center></td>'
    data += '<td style="border-color:#000000;width:10%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:12px;">TOTAL(RS)<center></td>'
    data += '<td style="border-color:#000000;width:5%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:10px;">1 - 320<center></td>'
    data += '<td style="border-color:#000000;width:5%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:10px;">320 - 640<center></td>'
    data += '<td style="border-color:#000000;width:5%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:10px;">640 - 1200<center></td>'
    data += '<td style="border-color:#000000;width:5%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:10px;">1200 ><center></td>'
    data += '<td style="border-color:#000000;width:10%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:12px;">TOTAL(NER)<center></td>'
    data += '<td style="border-color:#000000;width:10%;padding:1px;background-color:#3333ff;color:white;font-weight:bold;"><center style="color:white;font-size:14px;">SUB TOTAL<center></td>'
    data += '</tr>'	 


    data += '<tr>'
    data += '<td style="border-color:#000000;width:10%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">TECHNICIAN</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">A</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">B</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">C</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">D</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">A+B+C+D</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">A</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">B</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">C</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">D</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">A+B+C+D</b><center></td>'
    data += '<td style="border-color:#000000;width:7%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b style="color:white;">(NER-RS)</b><center></td>'
    data += '</tr>'	

    
    sp = frappe.get_all("Employee",{"designation": ["in", ["TECHNICIAN",'SENIOR TECHNICIAN']],"company":company},["*"])
    # wd = frappe.get_all("Work Order Data",{"status":"RSI-Repaired and Shipped Invoiced","posting_date": ["between", (self.from_date,self.to_date)]},["*"])
    for i in sp:
        data += '<tr>'
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(i.employee_name)
        wd = frappe.get_all("Work Order Data",{"technician":i.user_id,"invoice_no": ["!=", ""],"status_cap": ["=",""]},["*"])
        

        count_a = 0
        count_b = 0
        count_c = 0
        count_d = 0
        frappe.errprint(i.employee_name)
        for j in wd:
            sales = frappe.db.sql(""" select `tabSales Invoice`.posting_date,`tabSales Invoice Item`.amount  from `tabSales Invoice`
            left join `tabSales Invoice Item` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
            where `tabSales Invoice Item`.wod_no = '%s' or `tabSales Invoice Item`.work_order_data = '%s' and `tabSales Invoice`.status IN ('Paid', 'Overdue','Unpaid') """ %(j.name,j.name),as_dict = 1)
            if sales:
                frm_date = datetime.strptime(str(from_date), "%Y-%m-%d").date()
                t_date = datetime.strptime(str(to_date), "%Y-%m-%d").date()
                if sales[0]["posting_date"] >= frm_date and sales[0]["posting_date"] <= t_date:
                    if sales[0]["amount"] > 0 and sales[0]["amount"] < 320:
                        count_a = count_a + 1
                        
                    elif sales[0]["amount"] >= 320 and sales[0]["amount"] < 640:
                        count_b = count_b + 2
                        
                    elif sales[0]["amount"] >=640 and sales[0]["amount"] < 1200:
                        count_c = count_c + 3
                        
                    elif sales[0]["amount"] >= 1200:
                        count_d = count_d + 4
                        

        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_a)
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_b)
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_c)
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(count_d)
        t_cnt = count_a + count_b + count_c + count_d
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(t_cnt)
        
        
        
        ner = frappe.get_all("Work Order Data",{"technician":i.user_id,"invoice_no": ["!=", ""],"status_cap_date": ["between", (from_date,to_date)]},["*"])
        ner_count_a = 0
        ner_count_b = 0
        ner_count_c = 0
        ner_count_d = 0
        
        for k in ner:
            sales = frappe.db.sql(""" select `tabSales Invoice`.name,`tabSales Invoice Item`.amount  from `tabSales Invoice`
            left join `tabSales Invoice Item` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
            where `tabSales Invoice`.posting_date between '%s' and '%s' and `tabSales Invoice Item`.wod_no = '%s' or `tabSales Invoice Item`.work_order_data = '%s' and `tabSales Invoice`.status IN ('Paid', 'Overdue','Unpaid') """ %(from_date,to_date,j.name,j.name),as_dict = 1)
            if sales:
                if sales[0]["amount"] > 0 and sales[0]["amount"] < 320:
                    ner_count_a = ner_count_a + 1
                if sales[0]["amount"] >= 320 and sales[0]["amount"] < 640:
                    ner_count_b = ner_count_b + 2
                if sales[0]["amount"] >=640 and sales[0]["amount"] <1200:
                    ner_count_c = ner_count_c + 3
                if sales[0]["amount"] >= 1200:
                    ner_count_d = ner_count_d + 4
        
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_a)
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_b)
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_c)
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_count_d)
        ner_t_cnt = ner_count_a + ner_count_b + ner_count_c + ner_count_d
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(ner_t_cnt)
        
        data += '<td style="border-color:#000000;padding:1px;font-size:14px;font-size:12px;"><center><b>%s</b><center></td>' %(t_cnt - ner_t_cnt)
        
        data += '</tr>'	
    data += '</table>'

    return data



from datetime import datetime, timedelta, date
@frappe.whitelist()
def get_leave_application(leave_application):
    from hrms.hr.doctype.leave_application.leave_application import get_leave_details
    leave_app = frappe.db.sql(""" select * from `tabLeave Application` where name = '%s' """%(leave_application),as_dict=1)
    if leave_app:
        for lap in leave_app:
            remaining_leaves = 0
            val = get_leave_details(lap.employee,today())
            if val['leave_allocation'].get("Annual Leave", {}).get("remaining_leaves"):
                remaining_leaves = (val['leave_allocation'].get("Annual Leave", {}).get("remaining_leaves"))
            from_date = lap.from_date
            first_of_month = from_date.replace(day=1)
            before_day = from_date - timedelta(days=1)
            to_date = lap.to_date
            worked_days = date_diff(from_date,first_of_month)
            leave_days = date_diff(to_date,from_date) +1
            return first_of_month,before_day,from_date,to_date,worked_days,leave_days,remaining_leaves

import openpyxl
from openpyxl import Workbook
from six import BytesIO, string_types
from openpyxl.styles import Font, Alignment, Border, Side
@frappe.whitelist()
def salary_register_excel():
    args = frappe.local.form_dict
    filename = "Salary Summary"
    test = build_xlsx_response(filename)

def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
    args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name, 0)
    month_name = args.month_name
    company = args.company
    cyrix_employee = args.cyrix_employee
    from datetime import timedelta
    frappe.log_error(title = 'value',message = args)
    frappe.log_error(title = 'type',message = type(month_name))
    current_year = datetime.now().year
    month_number = datetime.strptime(month_name, '%B').month    
    first_date = datetime(current_year, month_number, 1)
    if month_number == 12:
        last_date = datetime(current_year, month_number, 31)
    else:
        next_month = datetime(current_year, month_number + 1, 1)
        last_date = next_month - timedelta(days=1)
    if company == "TSL COMPANY - Kuwait":
        filters = {'from_date': first_date.date(), 'to_date': last_date.date(), 'currency': 'KWD', 'company': company, 'docstatus': 'Draft'}
    if company == "TSL COMPANY - KSA":
        filters = {'from_date': first_date.date(), 'to_date': last_date.date(), 'currency': 'SAR', 'company': company, 'docstatus': 'Draft'}
    if company == "TSL COMPANY - UAE":
        filters = {'from_date': first_date.date(), 'to_date': last_date.date(), 'currency': 'AED', 'company': company, 'docstatus': 'Draft'}
    from hrms.payroll.report.salary_register.salary_register import execute
    result = execute(filters)
    headers = result[0]
    records = result[1]
    skip_columns = ['total_loan_repayment','company','salary_slip_id', 'branch', 'date_of_joining', 'start_date', 'end_date','currency','data_of_joining']
    int_columns = ['leave_without_pay', 'payment_days']
    currency_columns = [header['fieldname'] for header in headers if header.get('fieldtype') == 'Currency']
    filtered_headers = []
    for header in headers:
        if header['fieldname'] in skip_columns:
            continue
        if header['fieldname'] == 'loan':
            header['label'] = 'Loan Deduction'
        filtered_headers.append(header)
    totals = {fieldname: 0.0 for fieldname in currency_columns}
    ws.append(["SALARY SUMMARY"])
    ws.append([""])
    ws.append([company])

    title = ["Sl.No."]
    for header in filtered_headers:
        title.append(header["label"])
    ws.append(title)
    cl_no = len(filtered_headers)+1
    for header in ws.iter_rows(min_row=1 , max_row=4, min_col=1, max_col=cl_no):
        for cell in header:
            cell.font = Font(bold=True)
    sl_no = 1
    for record in records:
        columns = [sl_no]
        cyrix = frappe.db.get_value("Employee",record.get('employee'),'cyrix_employee_')
        if cyrix == int(cyrix_employee):
            for header in filtered_headers:
                fieldname = header['fieldname']
                fieldtype = header.get('fieldtype', '')
                cell_value = record.get(fieldname, 0)  # Default to 0 if None
                if fieldname in currency_columns:
                    totals[fieldname] += float(cell_value) if isinstance(cell_value, (float, int)) else 0
                if fieldtype == 'Currency':
                    cell_value = "{:,.3f}".format(cell_value) if isinstance(cell_value, (float, int)) else "0.000"
                elif isinstance(cell_value, float):
                    cell_value = "{:,.3f}".format(cell_value)
                columns.append(cell_value)
            ws.append(columns)
            sl_no += 1
    total_row = []
    first_currency_index = next((i for i, header in enumerate(filtered_headers) if header['fieldname'] in currency_columns), len(filtered_headers))
    non_currency_colspan = first_currency_index + 1
    total_row.append("Total")
    if non_currency_colspan > 0:
        for _ in range(non_currency_colspan-1):
            total_row.append("")
    for i in range(non_currency_colspan, first_currency_index):
        data += '<td></td>'
        total_row.append("")
    for i, header in enumerate(filtered_headers[first_currency_index:], start=first_currency_index):
        fieldname = header['fieldname']
        if fieldname in currency_columns:
            total_value = "{:,.3f}".format(totals[fieldname])
        else:
            total_value = ''
        total_row.append(total_value)
    ws.append(total_row)
    align_center = Alignment(horizontal='center',vertical='center')
    ws.merge_cells(start_row=sl_no+4, start_column=1, end_row=sl_no+4, end_column=non_currency_colspan )
    ws.merge_cells(start_row=1, start_column=1, end_row=2, end_column=cl_no )
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=cl_no )

    for header in ws.iter_rows(min_row=sl_no+4 , max_row=sl_no+4, min_col=1, max_col=non_currency_colspan):
        for cell in header:
            cell.font = Font(bold=True)
    border_thin = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin'))
    header_range = ws['A1':ws.cell(row=sl_no+4, column=cl_no).coordinate]
    for row in header_range:
        for cell in row:
            cell.border = border_thin
            cell.alignment = align_center
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file

def build_xlsx_response(filename):
    xlsx_file = make_xlsx(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'


@frappe.whitelist()
def get_pi(posting_date,name,party_name,amount_in,total_allocated_amount,currency_paid,cost_center,references ):
    data = ""
    data+= '<table class="table table-bordered" style="border:1px solid black;" >'
    data+= '<tr><td colspan = 8><center><b style = "color:blue;font-size:15px">TSL COMPANY</b></center></td></tr>'
    data+= '<tr><td colspan = 8><center><b style = "color:red";>PAYMENT TRANSFER APPROVAL FORM</b></center></td></tr>'
    data+= '<tr><td>Date</td><td>%s</td></tr>' %(posting_date)
    data+='<tr><td>REF NO</td><td>%s</td></tr>' %(name)
    data+='<tr>  <td>Supplier Name</td><td>%s</td></tr>' %(party_name)
    data+='<tr> <td>Amount</td><td>%s</td></tr>' %(amount_in or total_allocated_amount)
    data+='<tr><td>Currency</td><td>%s</td></tr>' %(currency_paid)
    data+='<tr><td>Department</td><td>%s</td></tr>' %(cost_center)
    for i in references:
        pat = frappe.get_value("Purchase Invoice",{"name":i.reference_name},["supplier_invoice_attach"])
        pi = frappe.db.sql(""" select DISTINCT `tabPurchase Invoice`.name as p,`tabPurchase Invoice Item`.work_order_data as wo,`tabPurchase Invoice Item`.supply_order_data as so from `tabPurchase Invoice` 
        left join `tabPurchase Invoice Item` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent 
        where `tabPurchase Invoice`.name = '%s' """ %(i.reference_name),as_dict =1)
        data+='<tr><td>Attached With Supporting Document</td><td><b>%s</b>/ <a href="%s"><u><b style = "color:red">Supplier Invoice Link</b></u></a></td><br>'%(i.reference_name,pat)
        for j in pi:
            if j["wo"] or j["so"]:
                data+='<tr><td></td><td><a href="https://erp.tsl-me.com/app/work-order-data/%s">%s</a></td></tr>' %(j["wo"] or j["so"],j["wo"] or j["so"])
    data+= "</table>"
    return data

@frappe.whitelist()
def get_q(name):
    qu = frappe.db.sql(""" select `tabQuotation Item`.wod_no,`tabQuotation`.name as q  from `tabQuotation` left join 
    `tabQuotation Item` on `tabQuotation`.name = `tabQuotation Item`.parent where `tabQuotation`.name = '%s' """ %(name) ,as_dict=1)
    count = 0
    for i in qu:
        if i['wod_no']:
            ev = frappe.db.exists("Evaluation Report",{"work_order_data":i['wod_no']})
            if not ev:
                count = count + 1
    
    if count > 0:     
        data = ""
        data+= '<table class="table table-bordered" style="border:1px solid black;" >'
        data+= '<tr><td colspan = 8><center><b style = "color:blue;font-size:15px">TSL COMPANY</b></center></td></tr>'
        data+= '<tr><td colspan = 8><center><b style = "color:red";>PAYMENT TRANSFER APPROVAL FORM</b></center></td></tr>'
        data+= "</table>"
        return "Yes"
