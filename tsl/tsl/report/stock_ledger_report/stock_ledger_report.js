// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Ledger Report"] = {
	"filters": [

		{
			"fieldname": "item",
			"label": __("Item"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Item",

			
		},

		{
			"fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Item Group",

			
		},

		
	]
};
