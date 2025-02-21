// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Dashboard', {

	onload(frm){
		
		frm.set_value("company","")
		if(frm.doc.reports == "Sales Person Summary"){
		if (frappe.session.user == "info@tsl-me.com"){
			frm.set_value("company","TSL COMPANY - Kuwait")
			// frm.doc.save()

		}

		if (frappe.session.user == "info-uae@tsl-me.com"){
			frm.set_value("company","TSL COMPANY - UAE")
			// frm.doc.save()
		}
	}

		frm.trigger("get_data");

	},

	reports(frm){

		if (frappe.session.user == "info@tsl-me.com"){
			frm.set_value("company","")
			if(frm.doc.reports == "Sales Person Summary"){
				frm.set_value("company","TSL COMPANY - Kuwait")
			}
		}
		
		if (frappe.session.user == "info-uae@tsl-me.com"){
			frm.set_value("company","")
			if(frm.doc.reports == "Sales Person Summary"){
				frm.set_value("company","TSL COMPANY - UAE")
			}
		}
		

		frm.trigger("get_data");

	},


	// refresh: function(frm) {
       
        
    //     // Check if the user has a specific role
    //     if (frappe.user.has_role("HR Manager")) {
    //         // Set options only for users with the specified role
    //         frm.set_df_property("reports", "options", ["Salary Summary"]);
    //     }
	// 	else if (frappe.user.has_role("Admin")) {
    //         // Set options only for users with the specified role
    //         frm.set_df_property("reports", "options", ["Statement of Customer"]);
    //     }
		

	// 	 else {
    //         // Set limited options for other users
    //         frm.set_df_property("reports", "options", ["Salary Summary","Statement of Customer"]);
    //     }
    // },
	download_excel(frm){
		if(frm.doc.reports == "Salary Summary"){
				
			var path = "tsl.custom_py.utils.salary_register_excel"
			var args = 'month_name=%(month_name)s&company=%(company)s&cyrix_employee=%(cyrix_employee)s'
				
		}

		if (path) {
			
			window.location.href = repl(frappe.request.url +'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				month_name: frm.doc.month,
				company : frm.doc.company,
				cyrix_employee : frm.doc.cyrix_employee,	
			
			});
		}
	},
	
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

			if(frm.doc.reports == "Salary Summary"){
				if(frm.doc.company){
					var print_format ="Salary Summary";
					var f_name = "Salary Summary";
					window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
						+ "doctype=" + encodeURIComponent("Report Dashboard")
						+ "&name=" + encodeURIComponent(f_name)
						+ "&trigger_print=1"
						+ "&format=" + print_format
						+ "&no_letterhead=0"
					));
				}
				else{
					frappe.throw("Please select Company")
				}			
			}


			if(frm.doc.reports == "Work Order Data Time Log"){
				
			var path = "tsl.tsl.doctype.report_dashboard.work_order_data_time_log.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
				
			}

			if (path) {
				
				window.location.href = repl(frappe.request.url +'?cmd=%(cmd)s&%(args)s', {
					cmd: path,
					args: args,
					date: frm.doc.date,
					from_date : frm.doc.from_date,
					to_date : frm.doc.to_date,	
				
				});
			}
			
		
		}
	
});
