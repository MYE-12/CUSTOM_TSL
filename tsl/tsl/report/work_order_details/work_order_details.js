// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Work Order Details"] = {
	"filters": [

		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			default: frappe.datetime.add_months(frappe.datetime.month_start(), -1),

			
			
	
		},
		
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
			
		},

	]
};
