// Copyright (c) 2025, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('WO Approval Test', {
	// refresh: function(frm) {

	// }

	refresh: function(frm) {
		if(frappe.session.user != "Administrator"){
	        frm.set_df_property('company', 'read_only', 1);
	
	    }
	},
	
	get_data:function (frm){
		frappe.show_alert({
			message: "Data processing",
			indicator: 'blue'
		}, 50);  // 5 seconds

		frm.call('get_q').then(r=>{
			if(r.message){
				frm.fields_dict.html.$wrapper.html(r.message);
	
			}
	
								
			})

},

		view(frm){
			frm.trigger("get_data");
		},

		onload(frm){
		frm.set_value("company","")
		if (frappe.session.user == "info@tsl-me.com"){
			frm.set_value("company","TSL COMPANY - Kuwait")
			

		}

		if (frappe.session.user == "info-uae@tsl-me.com"){
			frm.set_value("company","TSL COMPANY - UAE")
			
		}
		},

		download:function(frm){
			var print_format ="WO Approval";
			var f_name = "WO Approval"
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("WO Approval")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		
		},

});
