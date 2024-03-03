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
from frappe.utils import add_to_date
import requests
from datetime import datetime
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
def get_wod(data):
	data = json.loads(data)
	wods = []
	for i in data:
		wo = frappe.db.sql(""" select DISTINCT `tabSales Invoice Item`.work_order_data as wo from `tabSales Invoice` 
		left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
		where `tabSales Invoice`.name = '%s' """ %(i["reference_name"]),as_dict =1)
		for j in wo:
			
			wods.append(j["wo"])

	return wods

@frappe.whitelist()
def set_payment(data,pe,date):
	data = json.loads(data)
	for i in data:
		frappe.db.set_value("Work Order Data",i["work_order_data"],"payment_date",date)
		frappe.db.set_value("Work Order Data",i["work_order_data"],"payment_entry_reference",pe)
		
@frappe.whitelist()
def get_receivable(customer):	
	data = ''
	data += '<table class="table table-bordered">'
	data += '<tr>'
	data += '<td style="border-color:#000000;width:15%"><b>Date</b></td>'
	data += '<td style="border-color:#000000;width:15%"><b>Activity</b></td>'
	data += '<td style="border-color:#000000;width:30%;"><b>Reference(WOD/PO)</b></td>'
	data += '<td style="border-color:#000000;width:15%;"><b>Invoiced</b></td>'
	data += '<td style="border-color:#000000;width:10%;"><b>Paid</b></td>'
	data += '<td style="border-color:#000000;width:15%;"><b>Outstanding</b></td>'
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
		if [po_no]:
			wods.append(po_no)
		
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
		data += '<td style="border-color:#000000;">%s</td>'%(formatted_due_date)
		data += '<td style="border-color:#000000;"><a href="https://erp.tsl-me.com/app/sales-invoice/%s">%s</a></td>'%(i.name,i.name)
		data += '<td style="border-color:#000000;">%s</td>'%(wod)
		data += '<td style="border-color:#000000;">%s</td>'%(i.grand_total)
		data += '<td style="border-color:#000000;">%s</td>'%(i.grand_total-i.outstanding_amount)
		data += '<td style="border-color:#000000;">%s</td>'%(i.outstanding_amount)
		data += '</tr>'
		wods = []
	data += '<tr>'
	data += '<td colspan = 6 style="border-color:#000000;"><b>Balance Due : %s</b></td>'%(os)
	data += '</tr>'
	data += '</table>'

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
	Week_start = "2024-01-01"

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