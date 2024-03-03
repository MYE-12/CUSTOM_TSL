// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Dashboard', {
	// refresh: function(frm) {

	// }

	download:function(frm){
			if(frm.doc.reports == "Statement of Customer" && frm.doc.customer){
				var print_format ="Account Receivable";
				var f_name = "Account Receivable"
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Report Dashboard")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}

			if(frm.doc.reports == "Statement of Customer"){
				frappe.msgprint("Please Select Customer")
			}

			if(frm.doc.reports == "Sales Person Summary"){
				var print_format ="Sales Person Summary";
				var f_name = "Sales Person Summary";
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Report Dashboard")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			
		
		}
	
});
