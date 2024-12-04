// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('WO Approval', {
	
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
