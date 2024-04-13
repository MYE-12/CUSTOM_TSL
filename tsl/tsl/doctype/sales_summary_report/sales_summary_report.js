// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Summary Report', {
	// refresh: function(frm) {

	// }
	download:function(frm){
		
			var print_format ="Sales Summary";
				var f_name = "Sales Summary Report"
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Sales Summary Report")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
		
		
	},

	get_data:function (frm){
		if (frm.doc.report){
			frm.call('get_work_orders').then(r=>{
				if(r.message){
			
					frm.fields_dict.html.$wrapper.html(r.message);
		
				}
		
									
				})
		}
	},

	report(frm){
		frm.trigger("get_data");
	},

	onload(frm){
		frm.trigger("get_data");
	},

	// report(frm) {
	// 	if(frm.doc.report){
	// 	frm.call('get_work_orders').then(r=>{
	// 	if(r.message){
	
	// 		frm.fields_dict.html.$wrapper.html(r.message);

	// 	}

							
	// 	})
	// 	}
	// 	else{
	// 		frm.fields_dict.html.$wrapper.html('');

	// 	}
		
		
	// },

	customer(frm){
		if(frm.doc.customer){
			frm.trigger("get_data");
			}

			else{
			
				frm.trigger("get_data");
			}
	},

	work_order_data(frm){
		if(frm.doc.work_order_data){
			frm.trigger("get_data");
			}

			else{
			
				frm.trigger("get_data");
			}
	},
	
	sales_person(frm){
		if(frm.doc.sales_person){
			frm.trigger("get_data");
			}

		else{
			
			frm.trigger("get_data");
		}
	}
});
