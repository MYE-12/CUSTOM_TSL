// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Gratuity"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"options": "Today",
		}	
	]
};
