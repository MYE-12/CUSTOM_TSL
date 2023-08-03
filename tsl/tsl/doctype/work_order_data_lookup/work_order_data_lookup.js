// Copyright (c) 2023, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order Data Lookup', {
	refresh: function(frm) {
		frm.disable_save()
	},
	work_order(frm){
		if(frm.doc.work_order){
			frappe.call({
				method: "tsl.tsl.doctype.work_order_data_lookup.work_order_data_lookup.get_wod_for_tool", //dotted path to server method
				args:{
					doc:frm.doc.work_order
				},
				callback: function(r) {
					if(r.message){
						
					console.log(r.message.material_list[0].item_code)
					var c = frm.add_child("material_list");
						c.item_code = r.message.material_list[0].item_code;
						c.model_no = r.message.material_list[0].model_no;
						c.mfg = r.message.material_list[0].mfg;
						c.type = r.message.material_list[0].type;
						c.item_name = r.message.material_list[0].item_name;
						c.qty = r.message.material_list[0].qty;
					frm.refresh_field("material_list");
						
						// cur_frm.clear_table("material_list")

				}
			}
			});
		}
	}
});
