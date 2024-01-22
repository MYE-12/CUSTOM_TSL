// Copyright (c) 2023, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Work Order Count"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1
		},	
	],
	// onload: function (report) {
	// 	var to_date = frappe.query_report.get_filter('to_date');
	// 	to_date.refresh();
	// 	to_date.set_input(frappe.datetime.add_days(frappe.datetime.month_start(),30))
	// 	var from_date = frappe.query_report.get_filter('from_date');
	// 	from_date.refresh();
	// 	var d = frappe.datetime.add_months(frappe.datetime.month_start())
	// 	from_date.set_input(frappe.datetime.add_days(d))
	// },
};
