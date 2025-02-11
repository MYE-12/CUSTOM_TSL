// Copyright (c) 2025, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Work Order Transition Analysis"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Company",

			
		},

		{
            "fieldname": "year",
            "label": __("Year"),
            "fieldtype": "Select",
            "width": "80",
            "options": [
                "",
                "2022",
                "2023",
                "2024",
                "2025"
            ],
            "default": new Date().getFullYear().toString() 
        }

	]
};
