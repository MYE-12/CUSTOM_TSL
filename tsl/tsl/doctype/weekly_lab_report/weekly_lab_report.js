// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Weekly Lab Report', {
	// refresh: function(frm) {

	// }
	onload(frm){
		// frm.set_value("company","")
		// if (frappe.session.user == "labcoordinator@tsl-me.com"){
		// 	frm.set_value("company","TSL COMPANY - Kuwait")
		// 	// frm.doc.save()

		// }

		// if (frappe.session.user == "lab-uae@tsl-me.com" || frappe.session.user == "purchase-uae@tsl-me.com"){
		// 	frm.set_value("company","TSL COMPANY - UAE")
		// 	// frm.doc.save()
		// }
		frm.trigger("get_data");

	},

	company(frm){
		frm.trigger("get_data");
	},

	get_data:function (frm){
		frm.call('get_data').then(r=>{
			if(r.message){
		
				frm.fields_dict.html.$wrapper.html(r.message);
	
			}
	
								
			})
	},

	download_pdf:function(frm){
		var print_format ="Weekly Lab Report";
		var f_name = "Weekly Lab Report"
		window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
			+ "doctype=" + encodeURIComponent("Weekly Lab Report")
			+ "&name=" + encodeURIComponent(f_name)
			+ "&trigger_print=1"
			+ "&format=" + print_format
			+ "&no_letterhead=0"
		));
	
	},

});
