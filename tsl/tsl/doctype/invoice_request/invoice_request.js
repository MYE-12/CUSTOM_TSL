// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice Request', {
	// refresh: function(frm) {

	// }
	 
	onload(frm){
		if(frm.doc.quotation){
			frm.trigger("get_data");
		}
	},

	get_data:function (frm){

			frm.call('get_work_orders').then(r=>{
				if(r.message){
			
					frm.fields_dict.html.$wrapper.html(r.message);
		
				}
		
									
				})
		
	},

	go_to(frm){
		frappe.set_route('Form','Quotation', frm.doc.quotation);

	},

	quotation(frm){
		frm.trigger("get_data");
	}
});
