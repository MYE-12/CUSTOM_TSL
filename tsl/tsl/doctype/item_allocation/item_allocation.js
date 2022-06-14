// Copyright (c) 2022, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Allocation', {
	// refresh(frm) {
	// 	frm.fields_dict["items"].grid.add_custom_button(__('Hello'), 
	// 		function() {
	// 			frappe.msgprint(__("Hello"));
    //     });
    //     frm.fields_dict["items"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');

	// },
	refresh(frm) {
		if (frm.doc.docstatus === 0){
			
			frm.fields_dict.items.grid.add_custom_button(__("Create Quotation"), () => {
				let selected_children = frm.fields_dict.items.grid.get_selected_children();
				var l=[];
				selected_children.forEach(doc => {
					doc.__checked = 0;			
					// let row = frm.add_child("items", doc);
					
					l.push(doc)
					
				});	
				if(selected_children){
					console.log(l)
					frappe.call({
						method: "tsl.tsl.doctype.item_allocation.item_allocation.create_qtn",
						args: {
							"doc": l,
							"sod":frm.doc.supply_order_data
						},
						callback: function(r) {
							if(r.message) {
								var doc = frappe.model.sync(r.message);
								frappe.set_route("Form", doc[0].doctype, doc[0].name);
								
							}
						}
					});
					
				}
			});
		frm.fields_dict.items.grid.custom_buttons["Create Quotation"].removeClass('btn-default').addClass('btn-primary');
		}
	}
	
});
