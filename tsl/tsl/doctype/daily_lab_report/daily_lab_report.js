// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Lab Report', {
	refresh: function(frm) {
		if(frappe.session.user != "Administrator" && frappe.session.user != "mohammed.d@tsl-me.com" ){
	        frm.set_df_property('company', 'read_only', 1);
	
	    }
	},

	download:function(frm){
		if (frm.doc.company == "TSL COMPANY - Kuwait"){
		var print_format ="Daily Lab Report";
		var f_name = "Daily Lab Report"
		window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
			+ "doctype=" + encodeURIComponent("Daily Lab Report")
			+ "&name=" + encodeURIComponent(f_name)
			+ "&trigger_print=1"
			+ "&format=" + print_format
			+ "&no_letterhead=0"
		));
	}

	if (frm.doc.company == "TSL COMPANY - UAE"){
		var print_format ="Daily Lab Report UAE";
		var f_name = "Daily Lab Report UAE"
		window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
			+ "doctype=" + encodeURIComponent("Daily Lab Report")
			+ "&name=" + encodeURIComponent(f_name)
			+ "&trigger_print=1"
			+ "&format=" + print_format
			+ "&no_letterhead=0"
		));
	}
	
	},

	onload(frm){
		// console.log(frappe.session.user)
		frm.set_value("company","")
		if (frappe.session.user == "labcoordinator@tsl-me.com"){
			frm.set_value("company","TSL COMPANY - Kuwait")
			// frm.doc.save()

		}

		if (frappe.session.user == "lab-uae@tsl-me.com" || frappe.session.user == "purchase-uae@tsl-me.com"){
			frm.set_value("company","TSL COMPANY - UAE")
			// frm.doc.save()
		}

		frm.trigger("get_data");
	},

	company(frm){
		if(frm.doc.company){
		frm.trigger("get_data");
		}
	},


	get_data:function (frm){
		
	frm.call('work_orders').then(r=>{
		if(r.message){
	
			frm.fields_dict.html.$wrapper.html(r.message);

		}

							
		})
		
	},

	date(frm){
		if(frm.doc.date){
			frm.call('work_orders').then(r=>{
				if(r.message){
					
					frm.fields_dict.html.$wrapper.html(r.message);
		
				}
		
									
				})
		}

		if(!frm.doc.date){
			frm.call('get_work_orders').then(r=>{
				if(r.message){
					
					frm.fields_dict.html.$wrapper.html(r.message);
		
				}
		
									
				})
		}
		
	}
});
