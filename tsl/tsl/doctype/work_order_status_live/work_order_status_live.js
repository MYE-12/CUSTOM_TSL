// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order Status Live', {
	refresh: function(frm) {
		frm.disable_save()
		frappe.call({
			method:'tsl.tsl.doctype.work_order_status_live.work_order_status_live.wod',
			args:{
			},
			callback(r){
				
				if(r.message){
					frm.fields_dict.html.$wrapper.empty().append(frappe.render_template('wod_details',r.message))
					
					
				}
			}
			
		})

	}
});
