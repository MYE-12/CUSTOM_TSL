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
		"before_submit":[
			"tsl.custom_py.quotation.before_submit"
		],
		"validate":[
			"tsl.custom_py.quotation.validate"
		],
		"before_save":[
			"tsl.custom_py.quotation.before_save"
		]
	},
	"Supplier Quotation":{
		"on_submit":[
			"tsl.custom_py.supplier_quotation.on_submit"
		]

	},
	"Purchase Order":{
		"on_submit":[
			"tsl.custom_py.purchase_order.on_submit"
		]
	},
	"Purchase Receipt":{
		"on_submit":[
			"tsl.custom_py.purchase_receipt.on_submit"
		]
	},
	"Delivery Note":{
		"on_submit":[
			"tsl.custom_py.delivery_note.on_submit"
		]
	},
	"Contact":{
		"before_save":[
			"tsl.custom_py.contact.before_save"
		]
	},
	"Sales Invoice":{
		"on_submit":[
			"tsl.custom_py.sales_invoice.on_submit"
		]
	},
	"Stock Entry":{
		"on_submit":[
			"tsl.custom_py.stock_entry.on_submit"
		]
	},
	
		
	
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
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
	"erpnext.stock.doctype.landed_cost_voucher.landed_cost_voucher.get_items_from_purchase_receipts": "tsl.custom_py.after_import.get_items_from_purchase_receipts"
}
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

