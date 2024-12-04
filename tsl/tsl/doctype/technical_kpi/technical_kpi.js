// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Technical KPI', {
	// refresh: function(frm) {

	// }

	get_data:function (frm){
		frm.call('get_data').then(r=>{
			if(r.message){
		
				frm.fields_dict.html.$wrapper.html(r.message);
	
			}
	
								
			})
	},


	from_date(frm){
		frm.trigger("get_data");
	},

	to_date(frm){
		frm.trigger("get_data");
	},


	onload(frm){
		frm.trigger("get_data");
	},

});
