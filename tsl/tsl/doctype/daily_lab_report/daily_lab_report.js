// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Lab Report', {
	// refresh: function(frm) {

	// }

	onload(frm){
		frm.trigger("get_data");
	},


	get_data:function (frm){
		
	frm.call('get_work_orders').then(r=>{
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
