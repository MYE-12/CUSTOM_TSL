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
					console.log(r.message)

					frm.clear_table("material_list");
					var c = frm.add_child("material_list");
						c.item_code = r.message[0].material_list[0].item_code;
						c.model_no = r.message[0].material_list[0].model_no;
						c.mfg = r.message[0].material_list[0].mfg;
						c.type = r.message[0].material_list[0].type;
						c.item_name = r.message[0].material_list[0].item_name;
						c.qty = r.message[0].material_list[0].qty;
					
					if(r.message[1].items){
					frm.clear_table("items");
						
						$.each(r.message[1].items, function(i, d) {
							console.log(d)
							var l = frm.add_child("items")
							l.part = d.part;
							l.model = d.model;
							l.category = d.category;
							l.sub_category = d.sub_category;
							l.qty = d.qty;
							l.used_qty = d.used_qty;
							l.parts_availability = d.parts_availability;
							l.bin_no = d.bin_no;
							l.from_scrap = d.from_scrap;
							l.part_description = d.part_description;
							

						});
					}
				
				}
				frm.refresh_field("material_list");
				frm.refresh_field("items");

			}
			});
		}
		
	},
	onload: function(frm) {
		frm.set_query('work_order', function() {
			return {
				filters: {
					'branch': frm.doc.branch
				}
			};
		});
	}
});
