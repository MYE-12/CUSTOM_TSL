// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order Data', {
	refresh: function(frm) {
		
		if(frm.doc.docstatus === 1) {
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
		if(frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Create Evaluation Report"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_evaluation_report",
					args: {
						"doc_no": frm.doc.name
					},
					callback: function(r) {
						if(r.message) {
							console.log(r.message)
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
						}
					}
				});
			});
		}
		if(!frm.doc.image){
			if(frm.doc.equipment_recieved_form){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.get_item_image",
					args: {
						"erf_no":frm.doc.equipment_recieved_form,
					},
					callback: function(r) {
						if(r.message) {
							cur_frm.set_df_property("image", "options","<img src="+r.message+"></img>");
							cur_frm.refresh_fields();
						}
					}
				});
			}
		}
		
	},
	check_for_extra_partsheets:function(frm){
		if(frm.doc.docstatus === 1) {
			frappe.call({
				method: "tsl.tsl.doctype.work_order_data.work_order_data.create_extra_ps",
				args: {
					"doc":frm.doc.name
				},
				callback: function(r) {
					if(r.message) {
						if(r.message.length >0){
							console.log(r.message)
							cur_frm.clear_table("extra_part_sheets");
							for(var i=0;i<r.message.length;i++){
								var childTable = cur_frm.add_child("extra_part_sheets");
								childTable.part_sheet_name = r.message[i]["name"],
								childTable.technician = r.message[i]["technician"],
								cur_frm.refresh_fields("extra_part_sheets");

						    }
							cur_frm.doc.docstatus = 1;
						    cur_frm.refresh_fields();
						}
						else{
							frappe.msgprint("No Extra Part Sheets for this Work Order");
						}
						
					}
					
				}
			})
		}

	},
	branch:function(frm){
		var d = {
			"Dammam - TS":"WOD-D.YY.-",
			"Riyadh - TS":"WOD-R.YY.-",
			"Jenda - TS":"WOD-J.YY.-"
		};
		if(frm.doc.branch){
			frm.set_value("naming_series",d[frm.doc.branch]);
		}
	},
	
		
	
});
frappe.ui.form.on('Work Order Data', {
	setup: function(frm) {
		frm.set_query("branch", function() {
			return {
				filters: [
					["Warehouse","company", "=", frm.doc.company],
					
				]
			}
		});
	}
});
