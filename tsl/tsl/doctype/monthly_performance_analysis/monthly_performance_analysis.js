// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Performance Analysis', {
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
});
