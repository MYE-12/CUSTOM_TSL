// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lab Report"] = {
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

		{
			"fieldname": "work_order_data",
			"label": __("Work Order"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Work Order Data",

			
		},


		{
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Branch",

			
		},


		// {
		// 	"fieldname": "tracking_id",
		// 	"label": __("Tracking ID"),
		// 	"fieldtype": "Data",
		// 	"width": "80",
			

			
		// },


		
		// {
		// 	"fieldname": "status",
		// 	"label": __("Status"),
		// 	"fieldtype": "Select",
		// 	"options": "A-Approved\nAP-Available Parts\nC-Comparison\nCT-Customer Testing\nCC-Comparison Client\nEP-Extra Parts\nIQ-Internally Quoted\nNE-Need Evaluation\nNER-Need Evaluation Return\nNEA-Need Evaluation Approved\nP-Paid\nQ-Quoted\nRNA-Return Not Approved\nRNAC-Return Not Approved Client\nRNF-Return No Fault\nRNFC-Return No Fault Client\nRNP-Return No Parts\nRNPC-Return No Parts Client\nRNR-Return Not Repaired\nRNRC-Return Not Repaired Client\nRS-Repaired and Shipped\nRSC-Repaired and Shipped Client\nRSI-Repaired and Shipped Invoiced\nSP-Searching Parts\nTR-Technician Repair\nUE-Under Evaluation\nUTR-Under Technician Repair\nW-Working\nWP-Waiting Parts\nParts Priced\nPending Internal Approval\nRSI-Repaired and Shipped Invoiced\nNEA-Need Evaluation Approved",
		// 	"default": "Submitted",
		// 	"width": "100"
		// }



		






	]
};

