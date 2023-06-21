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
#from frappe.permissions import has_role

@frappe.whitelist()
def send_sales_reminder():
	sales_person = ["maaz@tsl-me.com","omar@tsl-me.com","vazeem@tsl-me.com"]	
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

		if sales_person[2] not in sr.sales_user:
                        print(sales_person[2])
                        frappe.sendmail(
                                        recipients= [sales_person[2]],
 #                                       cc = ["yousuf@tsl-me.com"],
                                        subject="Daily Sales Report Reminder",
                                        message = "Kindly fill the Daily Report by EOD"
                                )


def create_hooks():
    job = frappe.db.exists('Scheduled Job Type', 'send_sales_reminder')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")  
        sjt.update({
            "method" : 'tsl.custom_py.utils.send_sales_reminder',
            "frequency" : 'Cron',
            "cron_format" : '30 16 * * *'
        })
        sjt.save(ignore_permissions=True)
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
