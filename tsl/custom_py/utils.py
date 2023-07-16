import frappe
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

#from frappe.permissions import has_role

@frappe.whitelist()
def send_sales_reminder():
	# fri = ["06-01-2023,13-01-2023,20-01-2023,27-01-2023,03-02-2023,10-02-2023,17-02-2023,24-02-2023,03-03-2023,10-03-2023,17-03-2023,24-03-2023,31-03-2023,07-04-2023,14-04-2023,21-04-2023,28-04-2023,05-05-2023,12-05-2023,19-05-2023,26-05-2023,02-06-2023,09-06-2023,16-06-2023,23-06-2023,30-06-2023,07-07-2023,14-07-2023,21-07-2023,28-07-2023,04-08-2023,11-08-2023,18-08-2023,25-08-2023,01-09-2023,08-09-2023,15-09-2023,22-09-2023,29-09-2023,06-10-2023,13-10-2023,20-10-2023,27-10-2023,03-11-2023,10-11-2023,17-11-2023,24-11-2023,01-12-2023,08-12-2023,15-12-2023,22-12-2023,29-12-2023"]
	
	sales_person = ["maaz@tsl-me.com","vazeem@tsl-me.com"]	
	sales_report = frappe.db.sql("""select date,sales_user from `tabSales Track` where date = CURDATE()""",as_dict=1)

	if sales_report == []:
		frappe.sendmail(
                        recipients= sales_person,
                       # cc = ["yousuf@tsl-me.com"],
                        subject="Daily Sales Report Reminder",
                        message = "Kindly fill the Daily Report by EOD"
                        )
	for sr in sales_report:
		print(sr.sales_person)
		if sales_person[0] not in sr.sales_user:
			print(sales_person[0])
			frappe.sendmail(
					recipients= [sales_person[0]],
					cc = ["yousuf@tsl-me.com"],
					subject="Daily Sales Report Reminder",
					message = "Kindly fill the Daily Report by EOD"
				)
		if sales_person[1] not in sr.sales_user:
			print(sales_person[1])
			frappe.sendmail(
				recipients= sales_person[1],
				cc = ["yousuf@tsl-me.com"],
	                        subject="Daily Sales Report Reminder",
	                        message = "Kindly fill the Daily Report by EOD"
		                )

# 		if sales_person[2] not in sr.sales_user:
#                         print(sales_person[2])
#                         frappe.sendmail(
#                                         recipients= [sales_person[2]],
#  #                                       cc = ["yousuf@tsl-me.com"],
#                                         subject="Daily Sales Report Reminder",
#                                         message = "Kindly fill the Daily Report by EOD"
#                                 )

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
				"qty":i.qty,
				"schedule_date":add_to_date(new_doc.transaction_date,days = 2),
				"warehouse":new_doc.branch,
				"branch":new_doc.branch,
				"work_order_data":doc.work_order_data,
				"department":frappe.db.get_value("Work Order Data",doc.work_order_data,"department")
			})
	return new_doc


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
