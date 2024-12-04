// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Lab Report', {
	// refresh: function(frm) {

	// }

	download:function(frm){
		
		var print_format ="Daily Lab Report";
		var f_name = "Daily Lab Report"
		window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
			+ "doctype=" + encodeURIComponent("Daily Lab Report")
			+ "&name=" + encodeURIComponent(f_name)
			+ "&trigger_print=1"
			+ "&format=" + print_format
			+ "&no_letterhead=0"
		));
	
	},

	onload(frm){
		frm.trigger("get_data");
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
