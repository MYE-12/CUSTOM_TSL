// Copyright (c) 2016, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Supply Order Status"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			// "default": frappe.datetime.get_today(),
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"width": "80",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		}

	],
};
