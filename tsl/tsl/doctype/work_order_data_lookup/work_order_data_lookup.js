frappe.ui.form.on('Work Order Data Lookup', {
	refresh: function(frm) {
		frm.disable_save(); // Prevent saving from UI
	},

	work_order(frm) {
		if (frm.doc.work_order) {
			frappe.call({
				method: "tsl.tsl.doctype.work_order_data_lookup.work_order_data_lookup.get_wod_for_tool",
				args: {
					doc: frm.doc.work_order
				},
				callback: function(r) {
					if (r.message) {
						let material = r.message.material_list;
						let items = r.message.items;

						frm.clear_table("material_list");
						if (Array.isArray(material) && material.length > 0) {
							let c = frm.add_child("material_list");
							c.item_code = material[0].item_code;
							c.model_no = material[0].model_no;
							c.mfg = material[0].mfg;
							c.type = material[0].type;
							c.item_name = material[0].item_name;
							c.qty = material[0].qty;
						}

						frm.clear_table("items");
						if (Array.isArray(items)) {
							items.forEach(function(d) {
								let l = frm.add_child("items");
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

						frm.refresh_field("material_list");
						frm.refresh_field("items");
					}
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
