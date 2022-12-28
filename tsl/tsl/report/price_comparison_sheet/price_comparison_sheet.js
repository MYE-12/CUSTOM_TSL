// Copyright (c) 2016, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Price Comparison Sheet"] = {
	"filters": [
		{
			"fieldname":"sod_no",
			"label": __("SOD No"),
			"fieldtype": "Link",
			"options":"Supply Order Data",
			"width": "80",
			on_change: () => {
				var sod = frappe.query_report.get_filter_value('sod_no');
				if (sod) {
					frappe.db.get_value('Supply Order Data', sod, ["customer", "sales_rep"], function(value) {
						frappe.query_report.set_filter_value('client_name', value["customer"]);
						frappe.query_report.set_filter_value('sales_rep', value["sales_rep"]);
					});
				} else {
					frappe.query_report.set_filter_value('client name', "");
					frappe.query_report.set_filter_value('sales_rep', "");
				}
			}
		},
		{
			"fieldname":"wod_no",
			"label": __("WOD No"),
			"fieldtype": "Link",
			"options":"Work Order Data",
			"width": "80",
			on_change: () => {
				var sod = frappe.query_report.get_filter_value('wod_no');
				if (sod) {
					frappe.db.get_value('Work Order Data', sod, ["customer", "sales_rep"], function(value) {
						frappe.query_report.set_filter_value('client_name', value["customer"]);
						frappe.query_report.set_filter_value('sales_rep', value["sales_rep"]);
					});
				} else {
					frappe.query_report.set_filter_value('client name', "");
					frappe.query_report.set_filter_value('sales_rep', "");
				}
			}
		},
		{
			"fieldname":"client_name",
			"label": __("Client Name"),
			"fieldtype": "Link",
			"options":"Customer",
			"width": "80",
			
		},
		{
			"fieldname":"sales_rep",
			"label": __("Sales Rep"),
			"fieldtype": "Link",
			"options": "User",
			"width": "80",
		}

	],
};
