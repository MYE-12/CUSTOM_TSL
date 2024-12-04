from . import __version__ as app_version
from tsl import tsl

app_name = "tsl"
app_title = "Tsl"
app_publisher = "Tsl"
app_description = "Tsl"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "Tsl"
app_license = "MIT"


jinja = {
	"methods": [
		"tsl.custom_py.utils.get_receivable",
        "tsl.custom_py.sales_summary.get_wod",
        # "tsl.custom_py.wo_approval_html.get_data",
        "tsl.custom_py.utils.salary_register",
        "tsl.custom_py.utils.get_wrk_ord",
        "tsl.custom_py.utils.get_sales",
        "tsl.custom_py.utils.get_pi",
        "tsl.custom_py.utils.get_q",
		"tsl.custom_py.utils.get_mc",
        "tsl.custom_py.utils.purchase_report",
        "tsl.custom_py.utils.daily_lab_report",
        "tsl.custom_py.utils.weekly_lab_report",
        "tsl.custom_py.sales_person_html.get_sales",
        # "tsl.tsl.doctype.sales_summary_reprt.sales_summary_report.get_work_orders"
	]
}
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tsl/css/tsl.css"
# app_include_js = "/assets/tsl/js/tsl.js"

# include js, css files in header of web template
# web_include_css = "/assets/tsl/css/tsl.css"
# web_include_js = "/assets/tsl/js/tsl.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tsl/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Quotation" : ["custom/custom.js"],
	"Employee" : ["custom/employee.js"],
	"Leave Application" : ["custom/leave_application.js"],
	"Loan Application" : ["custom/loan_application.js"],
	"Request for Quotation" : ["custom/request_for_quotation.js"],
	"Purchase Order":["custom/purchase_order.js"],
	"Supplier Quotation":["custom/supplier_quotation.js"]
	

}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "tsl.install.before_install"
# after_install = "tsl.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tsl.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Quotation":{
		"on_update": [
			"tsl.custom_py.quotation.on_update"   
		],

		"after_insert": [
			"tsl.custom_py.quotation.update_cq",
			"tsl.custom_py.quotation.get_pre_eval"
            
            
		],
		"before_submit":[
			"tsl.custom_py.quotation.before_submit"
		],
		"validate":[
			"tsl.custom_py.quotation.sum_amount",
            "tsl.custom_py.quotation.show_details"
            
		],

		"on_submit":[
			"tsl.custom_py.quotation.on_submit"
		],
		# "after_save":[
			
		# ]
	},
	"Supplier Quotation":{
		"on_submit":[
			"tsl.custom_py.supplier_quotation.on_submit"
		],
        "validate":[
			"tsl.custom_py.supplier_quotation.validate"

		],

	},
	"Purchase Order":{
		"on_submit":[
			"tsl.custom_py.purchase_order.on_submit"
		]
	},
	"Purchase Receipt":{
		"on_submit":[
			"tsl.custom_py.purchase_receipt.on_submit"
		],

		"validate":[
			"tsl.custom_py.purchase_receipt.check_item",

		],
        
		"before_save":[
			"tsl.custom_py.purchase_receipt.before_save"
		]
	},
	"Delivery Note":{
		"on_submit":[
			"tsl.custom_py.delivery_note.on_submit"
		],

		"on_update_after_submit":[
			"tsl.custom_py.delivery_note.on_update_after_submit"
		],
	},
	"Contact":{
		"before_save":[
			"tsl.custom_py.contact.before_save"
		]
	},
	 #"Contact":{
          #      "after_insert":[
           #             "tsl.custom_py.customer.create_customer_details"
           #     ]
      #  },
	"Sales Invoice":{
		"on_submit":[
			"tsl.custom_py.sales_invoice.on_submit",
            "tsl.custom_py.sales_invoice.send_mail"
            
		],
		"on_update_after_submit":[
			"tsl.custom_py.sales_invoice.on_update_after_submit"
		],
		"before_save":[
			"tsl.custom_py.sales_invoice.before_save"
		]
	},
	"Stock Entry":{
		"on_submit":[
			"tsl.custom_py.stock_entry.on_submit"
		]
	},
	"Request for Quotation":{
		"on_submit":[
			"tsl.custom_py.request_for_quotation.on_submit"
		]
	},
	"Payment Entry":{
		"on_submit":[
			"tsl.custom_py.payment_entry.on_submit"
		]
	},
	"Leave Application": {
		"on_submit": [
			"tsl.custom_py.employee.update_used_tickets_in_employee"
		]
	},
    "Loan Application": {
		# "on_submit": "tsl.custom_py.loan_application_tsl.update_loan_amount",
		# "on_cancel": "tsl.custom_py.loan_application_tsl.update_loan_amount"
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"tsl.tsl.doctype.official_document.official_document.trigger_mail_notification",
		"tsl.custom_py.employee.update_ticket_count"
	],
	"weekly": [
		"tsl.custom_py.quotation.send_qtn_reminder_mail"
	],
    "cron": {
		"30 19 * * *": [
			"tsl.custom_py.utils.send_sales_reminder",
		]
	},
}
# 	"all": [
# 		"tsl.tasks.all"
# 	],
# 	"daily": [
# 		"tsl.tasks.daily"
# 	],
# 	"hourly": [
# 		"tsl.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tsl.tasks.weekly"
# 	]
# 	"monthly": [
# 		"tsl.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "tsl.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.stock.doctype.landed_cost_voucher.landed_cost_voucher.get_items_from_purchase_receipts": "tsl.custom_py.after_import.get_items_from_purchase_receipts",
}

from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry as fed
from tsl.custom_py import utils as nfed

fed.fill_employee_details = nfed.fill_employee_details

#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tsl.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"tsl.auth.validate"
# ]

fixtures = ["Property Setter"]
