// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order Data', {
	refresh: function(frm) {
		if(frm.doc.docstatus==1){
			cur_frm.add_custom_button("Work Order Report", function(frm){
				frappe.set_route("query-report", "Work Order Status");
			});
		}
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
							console.log(r.message)
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
						}
					}
				});
			});
		}
	},
	check_for_extra_partsheets:function(frm){
		if(frm.doc.docstatus == 1) {
			frappe.call({
				method: "tsl.tsl.doctype.work_order_data.work_order_data.create_extra_ps",
				args: {
					"doc":frm.doc.name
				},
				callback: function(r) {
					console.log("extra_ps............")
					if(r.message) {
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
				}
			})
		}

	}
	
		
	
});
