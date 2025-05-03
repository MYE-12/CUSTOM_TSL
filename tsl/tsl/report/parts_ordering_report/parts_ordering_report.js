// Copyright (c) 2025, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Parts Ordering Report"] = {
	"filters": [

		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Select",
			"width": "80",
			"options": "TSL COMPANY - KSA\n",
			"reqd" : 1
		},


		{
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Select",
			"width": "80",
			"options": "Jeddah - TSL-SA\nRiyadh - TSL- KSA\nDammam - TSL-SA"
		}

	]
};
