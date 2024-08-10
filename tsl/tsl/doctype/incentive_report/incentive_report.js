// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Incentive Report', {
	// refresh: function(frm) {

	// }
	get_data:function (frm){
		if (frm.doc.from_date && frm.doc.to_date){
			frm.call('get_work_orders').then(r=>{
				if(r.message){
			
					frm.fields_dict.html.$wrapper.html(r.message);
		
				}
		
									
				})
		}
	},

	view(frm){
		frm.trigger("get_data");
	},

	

	
	download:function(frm){
		
		var print_format ="Incentive Report";
			var f_name = "Incentive Report"
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Incentive Report")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
	
	
},
});
