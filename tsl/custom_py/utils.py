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
def send_sales_reminder():
	# fri = ["06-01-2023,13-01-2023,20-01-2023,27-01-2023,03-02-2023,10-02-2023,17-02-2023,24-02-2023,03-03-2023,10-03-2023,17-03-2023,24-03-2023,31-03-2023,07-04-2023,14-04-2023,21-04-2023,28-04-2023,05-05-2023,12-05-2023,19-05-2023,26-05-2023,02-06-2023,09-06-2023,16-06-2023,23-06-2023,30-06-2023,07-07-2023,14-07-2023,21-07-2023,28-07-2023,04-08-2023,11-08-2023,18-08-2023,25-08-2023,01-09-2023,08-09-2023,15-09-2023,22-09-2023,29-09-2023,06-10-2023,13-10-2023,20-10-2023,27-10-2023,03-11-2023,10-11-2023,17-11-2023,24-11-2023,01-12-2023,08-12-2023,15-12-2023,22-12-2023,29-12-2023"]
	
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
def create_rfq_int(ps):
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

@frappe.whitelist()
def getstock_detail(item_details,company):
	item_details = json.loads(item_details)
	data = ''
	data += '<h4><center><b>STOCK DETAILS</b></center></h4>'
	data += '<h6><B>Note:</h6>'
	data += '<table style = font-size:12px width=100% ><tr><td>REPAIR KUWAIT - <b>TSL</b></td><td>RIYADH MAIN -<b>TSL SA</b></td><td>JEDDAH -<b>TSL SA</b></td><td>DAMMAM- <b>TSL SA</b></tr>'
	# data += '<tr><td>Electra Najma Showroom Warehouse - <b> ENS</b></td><td>Marazeem Warehouse - <b>MSS</b></td><td>Barwa Showroom  - <b>EBS</b></td><td>Electra Electrical Warehouse - <b>EDE</b></td><td>Electra Engineering Warehouse - <b>EED</b></td></tr>'
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
				data += '<td style="text-align:center" colspan=1>%s</td>'%(j["model"])
				for stock in stocks:
					if stock.actual_qty > 0:
						data += '<td style="text-align:center;" colspan=1>%s</td>'%(stock.actual_qty)
					
				data += '</tr>'
			i += 1
		data += '</table>'
				
	return data
# def create_hooks():
#     job = frappe.db.exists('Scheduled Job Type', 'send_sales_reminder')
#     if not job:
#         sjt = frappe.new_doc("Scheduled Job Type")  
#         sjt.update({
#             "method" : 'tsl.custom_py.utils.send_sales_reminder',
#             "frequency" : 'Cron',
#             "cron_format" : '30 16 * * *'
#         })
#         sjt.save(ignore_permissions=True)
#def previous_day_mail():
#	yesterday = add_days(today(), -1)
#	sales_report = frappe.db.sql("""select date,sales_user from `tabSales Track` where date ='%s'"""%(yesterday),as_dict=1)
#	#print(sales_report)
	#print(yesterday)
#	sales_person = ["maaz@tsl-me.com","omar@tsl-me.com","vazeem@tsl-me.com"]


#	if sales_report == []:
		#print("1")
#		frappe.sendmail(
#                        recipients= sales_person,
					   # cc = ["yousuf@tsl-me.com"],
#                        subject="Previous day  Sales Report Reminder",
#                        message = "Pending on Pervious day Report.Kindly fill ASAP"
#                        )
#	for sr in sales_report:
#		if  sales_person[0]not in sr.sales_user:
	#		print(sales_person[0])
#			print(sr.sales_user)
#			frappe.sendmail(
#                                        recipients= [sales_person[0]],
										#cc = ["yousuf@tsl-me.com"],
#                                        subject="Previous day  Sales Report Reminder",
#                                        message ="Pending on Pervious day Report.Kindly fill ASAP"
#                                )
#		if sales_person[1] not in sr.sales_user:
	#		print(sales_person[1])
#			frappe.sendmail(
#                                recipients= sales_person[1],
								#cc = ["yousuf@tsl-me.com"],
#                                subject="Previous day Sales Report Reminder",
#                                message = "Pending on Previous day Report.Kindly fill ASAP"
#                                )
#		if sales_person[2] not in sr.sales_user:
	#		print(sales_person[2])
#			frappe.sendmail(
#                                        recipients= [sales_person[2]],
 #                                       cc = ["yousuf@tsl-me.com"],
#                                        subject="Previous day Sales Report Reminder",
#                                        message = "Pending on Pervious day Report.Kindly fill ASAP"
#                                )


# @frappe.whitelist()
# def item_qty():
# 	item = frappe.db.sql("""select name,model,category,sub_category,qty from `tabItem`""",as_dict=1)
# 	ir = 0
# 	data= ""

# 	for i in item:
		
			
# 		data += '<table class="table table-bordered">'
# 		data += '<tr>'
# 		data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>SKU</b><center></td>'
# 		data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>PART NUMBER</b><center></td>'
# 		data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>CATEGORY</b><center></td>'
# 		data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>SUB - CATEGORY</b><center></td>'
# 		data += '<td style="width:07%;padding:1px;font-size:14px;font-size:12px;background-color:#3333ff;color:white;"><center><b>QTY</b><center></td>'
		
# 		data += '</tr>'
# 		data +='<tr>'
# 		data += '<td style="text-align:center" colspan=1>%s</td>'%(i.name)
# 		data += '<td style="text-align:center" colspan=1>%s</td>'%(i.model)
# 		data += '<td style="text-align:center" colspan=1>%s</td>'%(i.category)
# 		data += '<td style="text-align:center" colspan=1>%s</td>'%(i.sub_category)
# 		if i.qty < 10:
# 			data += '<td style="text-align:center;" colspan=1>%s</td>'%(i.qty)
# 			ir += 1
# 		data += '</tr>'
		
# 		data += '</table>'
# 		# print(message)
# 		# print(data)

# 		frappe.sendmail(
# 		recipients='yousuf@tsl-me.com',
# 		sender="info@tsl-me.com",
# 		subject="Low Stock",
# 		message=data
			
# 	)