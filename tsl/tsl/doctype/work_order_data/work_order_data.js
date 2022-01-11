// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order Data', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Create Part Sheet"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_part_sheet",
					args: {
						"work_order": frm.doc.name
					},
					callback: function(r) {
						if(r.message) {
							
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
						}
					}
				});
			});
		}
		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Create Evaluation Report"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_evaluation_report",
					args: {
						"doc_no": frm.doc.name
					},
					callback: function(r) {
						if(r.message) {
							
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
						}
					}
				});
			});
		}
		
	},
	onload_post_render(frm){
		for(var i=0;i<frm.doc.material_list.length;i++){
			var image = frm.doc.material_list[i]["item_image"];
			cur_frm.set_df_property("image", "options","<img src="+image+"></img>");
			cur_frm.refresh_fields();
			
		}
	},
	
		
	
	
});
