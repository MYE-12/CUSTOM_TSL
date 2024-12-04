// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Report', {
	// refresh: function(frm) {

	// }

	download:function(frm){
		
		var print_format ="Purchase Report";
		var f_name = "Purchase Report"
		window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
			+ "doctype=" + encodeURIComponent("Purchase Report")
			+ "&name=" + encodeURIComponent(f_name)
			+ "&trigger_print=1"
			+ "&format=" + print_format
			+ "&no_letterhead=0"
		));
	
	},

	get_data:function (frm){
		frm.call('get_data').then(r=>{
			if(r.message){
		
				frm.fields_dict.html.$wrapper.html(r.message);
	
			}
	
								
			})
	},

	

	date(frm){
		frm.trigger("get_data");
	},

	
	
	onload(frm){
		frm.trigger("get_data");
	},


});
