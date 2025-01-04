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

		// {
		// 	"fieldname": "company",
		// 	"label": __("Company"),
		// 	"fieldtype": "Link",
		// 	"width": "100",
		// 	"options": "Company",

			
		// },

		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Warehouse",
			"default": null, // Placeholder for default value
            "get_query": function() {
                // Optional: Define a custom query for the warehouse field if needed
                return {
                    filters: {
                        company: frappe.defaults.get_user_default("company")
                    }
                };
            }
			
				
			
		},

		
	],

	onload: function(report) {
        // Fetch the user's default company
        const user_company = frappe.defaults.get_user_default("company");

        // Determine the default warehouse based on the user's company
        let default_warehouse = null;
        if(user_company === 'TSL COMPANY - UAE') {
            default_warehouse = 'Dubai - TSL-UAE';
        } 
		else if (user_company === 'TSL COMPANY - Kuwait') {
            default_warehouse = 'Kuwait - TSL';
        }

        // Set the default value for the warehouse filter
        if (default_warehouse) {
            report.set_filter_value('warehouse', default_warehouse);
        }
    }


};

// function get_default_warehouse() {
// 	var com = ""
// 	frappe.db.get_value('Employee', {'user_id':frappe.session.user},['company'], (r) => {
	
		
// 	frappe.db.get_value('Warehouse', {'is_branch':1,'company':r.compnay},['name'], (s) => {

	
// 	com = s.name
// 	console.log(com)
	
// 	});
// 	return com;
// 	});
	
	

// }
