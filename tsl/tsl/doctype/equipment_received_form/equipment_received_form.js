// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipment Received Form', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1){
			frm.add_custom_button(__("Create Work Order Data"), function(frm){
				frappe.call({
					'method': 'tsl.tsl.doctype.equipment_received_form.equipment_received_form.create_workorder_data',
					'args':{
					'order_no':cur_frm.doc.name
					},
					'callback':function(res){
						if(res.message){
//							frappe.msgprint("Work order data created")
						}
					}
					})

			})
		}

	}
});
