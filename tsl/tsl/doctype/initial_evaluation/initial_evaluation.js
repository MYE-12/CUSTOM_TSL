// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Initial Evaluation', {
	// refresh: function(frm) {

	// },
	/*on_update_before_submit:function(frm){
		console.log("opn_update")
	   if(frm.doc.status){
		var sts = ""
		if(frm.doc.status == "Spare Parts"){
			sts = "SP-Searching Parts"
		}
		else if(frm.doc.status == "Extra Parts"){
			sts = "EP-Extra Parts"
		}
		else if(frm.doc.status == "Working"){ 
					sts = "W-Working" 
				}
		else if(frm.doc.status == "Comparison"){ 
					sts = "C-Comparison"
				}
		else if(frm.doc.status == "Return Not Repaired"){ 
					sts = "RNR-Return Not Repaired"
				}
		else if(frm.doc.status == "Return No Fault"){ 
					sts = "RNF-Return No Fault"
				}

		if(!sts){
			if(frm.doc.parts_availability == "Yes"){
				sts = "AP-Available Parts"
			}
			else if(frm.doc.parts_availability == "No"){
				sts = "SP-Searching Parts"
			}
		}
		console.log(sts)
		frappe.call({
						method :"tsl.tsl.doctype.evaluation_report.evaluation_report.set_wod_status",
						args :{
								"wod":frm.doc.work_order_data,
								"sts":sts,
						},
						async : false
		})

		  }
	},*/
	items_on_form_rendered: function (frm, cdt, cdn) {
		let grid_row = cur_frm.open_grid_row();
		if (grid_row.grid_form.fields_dict.is_not_edit.doc.is_not_edit) {
			$(".btn.btn-danger.btn-sm.pull-right.grid-delete-row").hide()
			cur_frm.refresh_fields()
		}
		else {
			$(".btn.btn-danger.btn-sm.pull-right.grid-delete-row").show()
			cur_frm.refresh_fields()
		}
	},

	work_order_data: function (frm) {
		if (frm.doc.work_order_data) {
			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "Work Order Data",
					name: frm.doc.work_order_data
				},
				callback: function (data) {
					if (data.message) {
						var doc = data.message
						frm.doc.customer = doc.customer
						frm.doc.attn = doc.sales_rep
						frm.no_output = doc.no_output
						frm.doc.no_power = doc.no_power
						frm.doc.no_display = doc.no_display
						frm.doc.no_communication = doc.no_communication
						frm.doc.no_backlight = doc.no_backlight
						frm.doc.supply_voltage = doc.supply_voltage
						frm.doc.error_code = doc.error_code
						frm.doc.touch_keypad_not_working = doc.touch_keypad_not_working
						frm.doc.short_circuit = doc.short_circuit
						frm.doc.overload_overcurrent = doc.overload_overcurrent
						frm.doc.others = doc.others
						frm.doc.specify = doc.specify
						frm.refresh_fields();
						for (var i = 0; i < doc.material_list.length; i++) {
							frm.clear_table("evaluation_details")
							var childTable = cur_frm.add_child("evaluation_details");
							childTable.item = doc.material_list[i].item_code
							childTable.model = doc.material_list[i].model_no
							childTable.manufacturer = doc.material_list[i].mfg
							childTable.type = doc.material_list[i].type
							childTable.serial_no = doc.material_list[i].serial_no
							childTable.description = doc.material_list[i].item_name
							cur_frm.refresh_field("evaluation_details")
						}
					}
				}
			});
		}
	},
	refresh: function (frm) {
	if(frm.doc.docstatus == 1){
		frm.add_custom_button(__("Evaluation Report"), function () {
			frappe.call({
				method: "tsl.tsl.doctype.work_order_data.work_order_data.create_initial_eval",
				args: {
					"doc_no": frm.doc.name
				},
				callback: function (r) {
					if (r.message) {
						var doc = frappe.model.sync(r.message);
						frappe.set_route("Form", doc[0].doctype, doc[0].name);
					}
				}
			});
		}, __('Create'));
	}
		if(frappe.user.has_role("Procurement")){
			frm.add_custom_button(__("Release Parts"), function () {
				frappe.call({
					method: "tsl.tsl.doctype.initial_evaluation.initial_evaluation.create_material_issue_from_ini_eval",
					args:{
						'name':frm.doc.name
					},
					callback: function (r) {
						if (r.message) {
							frappe.msgprint("Material Released")
							// frappe.set_route("Form", "Stock Entry", "new-stock-entry-1");
						}
					}
				});
			}, __('Create'));
		}
		

		// if(frm.doc.work_order_data){
			
		// frappe.call({
		// 		method: "tsl.tsl.doctype.evaluation_report.evaluation_report.get_item_image",
		// 		args: {
		// 			"wod_no":frm.doc.work_order_data,
		// 		},
		// 		callback: function(r) {
		// 			console.log(r)
		// 			if(r.message) {
		// 				cur_frm.set_df_property("item_photo", "options","<img src="+r.message+"></img>");
		// 				cur_frm.refresh_fields();
		// 			}
		// 		}
		// 	});

		// }
		// if(frm.doc.docstatus == 1){
		// 	$(".btn.btn-xs.btn-danger.grid-remove-rows").hide()
		// 	cur_frm.refresh_fields()
		// }
		if (!frm.doc.if_parts_required) {
			set_field_options("status", ["Installed and Completed", "Customer Testing", "Working", "Comparison", "Return Not Repaired", "Return No Fault"])
		}
		if (frm.doc.if_parts_required && frm.doc.items.length > 0) {
			if (frm.doc.items[frm.doc.items.length - 1].part_sheet_no > 1) {
				set_field_options("status", ["Installed and Completed", "Customer Testing", "Working", "Extra Parts", "Comparison", "Return Not Repaired", "Return No Fault"])
			}
			else if (frm.doc.items[(frm.doc.items.length) - 1].part_sheet_no == 1) {
				set_field_options("status", ["Installed and Completed", "Customer Testing", "Working", "Spare Parts", "Comparison", "Return Not Repaired", "Return No Fault"])
			}
		}
		if (frm.doc.attach_image) {
			cur_frm.set_df_property("item_photo", "options", "<img src=" + frm.doc.attach_image + "></img>");
			cur_frm.refresh_fields();
		}
		if (in_list(frappe.user_roles, "Technician")) {
			var df = frappe.meta.get_docfield("Testing Part Sheet", "price_ea", cur_frm.doc.name);
			df.read_only = 1;
			cur_frm.refresh_fields();
		}
		else if (in_list(frappe.user_roles, "Purchase User")) {
			var df = frappe.meta.get_docfield("Testing Part Sheet", "part", cur_frm.doc.name);
			df.read_only = 1;
			var df = frappe.meta.get_docfield("Testing Part Sheet", "part_name", cur_frm.doc.name);
			df.read_only = 1;
			var df = frappe.meta.get_docfield("Testing Part Sheet", "type", cur_frm.doc.name);
			df.read_only = 1;
			var df = frappe.meta.get_docfield("Testing Part Sheet", "qty", cur_frm.doc.name);
			df.read_only = 1;
			cur_frm.refresh_fields();
		}
		else {
			var df = frappe.meta.get_docfield("Testing Part Sheet", "price_ea", cur_frm.doc.name);
			df.read_only = 1;
			var df = frappe.meta.get_docfield("Testing Part Sheet", "part", cur_frm.doc.name);
			//df.read_only = 1;
			var df = frappe.meta.get_docfield("Testing Part Sheet", "part_name", cur_frm.doc.name);
			df.read_only = 1;
			var df = frappe.meta.get_docfield("Testing Part Sheet", "type", cur_frm.doc.name);
			df.read_only = 1;
			var df = frappe.meta.get_docfield("Testing Part Sheet", "qty", cur_frm.doc.name);
			df.read_only = 1;
			cur_frm.refresh_fields();

		}
		frm.fields_dict['items'].grid.get_field('part').get_query = function (frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			var d = {};
			if (child.model_no) {
				d['model'] = child.model;
			}
			if (child.mfg) {
				d['mfg'] = child.manufacturer;
			}
			if (child.type) {
				d['type'] = child.type;
			}
			d['item_group'] = "Equipments";
			return {
				filters: d,
				// cur_frm.set_value("part", d)

			}
		}
		frm.fields_dict['items'].grid.get_field('part').get_query = function (frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			var d = {};
			d['item_group'] = "Components";
			
			// frappe.call({
			// 	method:"tsl.custom_py.utils.get_item_warehouse",
				
			// 	callback: function(r) {
			// 		console.log(r.message[1].default_warehouse)
			// 		var dw = (r.message[1].default_warehouse)
			// 	}
			// })
			// frappe.db.get_value('Bin', child.part, 'warehouse', (values) => {
			// 	d['warehouse'] = values.warehouse;
			// })
			if (child.model) {
				d['model'] = child.model;
			}
			if (child.category) {
				d['category_'] = child.category;
			}
			if (child.sub_category) {
				d['sub_category'] = child.sub_category;
			}
			
			
			return {
				filters: d
			}
		}
		if (frm.doc.parts_availability == "No") {
			if (!frappe.user.has_role("Technician") || frappe.user.has_role("Administrator")) {
				frm.add_custom_button(__("Request for Quotation"), function () {
					frappe.call({
						method: "tsl.custom_py.utils.create_rfq_int",
						args: {
							"ps": frm.doc.name
						},
						callback: function (r) {
							if (r.message) {
								var doc = frappe.model.sync(r.message);
								frappe.set_route("Form", doc[0].doctype, doc[0].name);
							}
						}
					});
				}, __('Create'));
			}
		}
	},
	// if_parts_required:function(frm){
	// 	if(frm.doc.if_parts_required){
	// 		set_field_options("status", ["Installed and Completed","Customer Testing","Working","Spare Parts","Comparison","Return Not Repaired","Return No Fault"])
	//                 frm.set_value("status","Spare Parts")
	// 		frm.refresh_fields()
	//         	if(frm.doc.items[frm.doc.items.length-1].part_sheet_no > 1 ){
	//                 	set_field_options("status", ["Installed and Completed","Customer Testing","Working","Extra Parts","Comparison","Return Not Repaired","Return No Fault"])
	//         	}
	//         	else if(frm.doc.items[(frm.doc.items.length)-1].part_sheet_no == 1 ){
	//                 	set_field_options("status", ["Installed and Completed","Customer Testing","Working","Spare Parts","Comparison","Return Not Repaired","Return No Fault"])
	//         	}
	// 	}
	// 	else{
	// 		set_field_options("status", ["Installed and Completed","Customer Testing","Working","Comparison","Return Not Repaired","Return No Fault"])
	// 	}
	// },
	// validate(frm){
	// 	console.log('hi')
	// 	if(frappe.session.user==="Mohamed Yousuf Ebrahim"){
	// 	frappe.show_alert({
	// 		message:__('Hi, you have a new message'),
	// 		indicator:'blue'
	// 	}, 90)
	// }},
	setup: function (frm) {
		frm.fields_dict['items'].grid.get_field('sub_category').get_query = function (frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
					'category': child.category,
				}
			}
		}
		frm.fields_dict['items'].grid.get_field('part').get_query = function (frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			var d = {};
			d['item_group'] = "Components";
			frappe.call({
				method:"tsl.custom_py.utils.get_item_warehouse",
				callback: function(r) {
				}
			})
			if (child.model) {
				d['model'] = child.model;

			}
			if (child.category) {
				d['category_'] = child.category;
			}
			if (child.sub_category) {
				d['sub_category'] = child.sub_category;
			}
			return {
				filters: d
			}
		}
		frm.set_query("department", function () {
			return {
				filters: [
					["Cost Center", "company", "=", frm.doc.company],

				]
			}
		});
		//frm.set_query("category","items",function(doc,cdt,cdn){
		//var d = locals[cdt][cdn];
		//return{
		//filters:{
		//	modelpart:d.model
		//}
		//}
		//});
		frm.set_query("part_description", "items", function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					model_part: d.model
				}
			}
		});
		frm.set_query("model", "items", function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			if (d.part_description) {
				return {
					filters: {
						description: d.part_description
					}
				}
			}
		});


	}
});
frappe.ui.form.on('Testing Part Sheet', {
	refresh: function (frm, cdt, cdn) {
		if (frm.doc.parts_availability) {
			var last_no = frm.doc.items[frm.doc.items.length - 1].part_sheet_no
			for (var i = 0; i < frm.doc.items.length; i++) {
				if (frm.doc.items[i].part_sheet_no != last_no) {
					var df = frappe.meta.get_docfield("Testing Part Sheet", "qty", cdn);
					df.read_only = 1;
					frm.refresh_fields();
				}
			}
		}
	},
	// validate:function(frm,cdt,cdn){
	// 	console.log("OUK")
	// 	cur_frm.refresh_field("part")
	// },

	//	before_items_remove:function(frm,cdt,cdn){
	//		var item = locals[cdt][cdn];
	//	if(item.is_not_edit && item.__checked){
	//			item.__checked = 1
	//			cur_frm.refresh_fields()
	//			frappe.throw("Cannot Delete old Part Sheets")
	//		}
	// for(var i=0;i<frm.doc.items.length;i++){

	// 	if(frm.doc.items[i].is_not_edit && cur_frm.doc.items[1].__checked){

	// 		frappe.throw("Cannot Delete old Part Sheets")
	// 	}

	// }
	//	},

	part: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		if (row.part && row.qty) {
			frappe.call({
				method: "tsl.tsl.doctype.part_sheet.part_sheet.get_valuation_rate",
				args: {
					"item": row.part,
					"qty": row.qty,
					"warehouse": frappe.user_defaults.company
				},
				callback: function (r) {
					frappe.model.set_value(cdt, cdn, "price_ea", r.message[0]);
					frappe.model.set_value(cdt, cdn, "parts_availability", r.message[1]);
					row.total = row.qty * r.message[0];
					let tot_amount = 0
					for (let i in frm.doc.items) {
						tot_amount += frm.doc.items[i].total

					}

					frm.set_value("total_amount", tot_amount)
					frm.refresh_fields();
				}
			})
		}
		frm.refresh();
	},
	qty: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		if (row.qty && row.part) {
			frm.script_manager.trigger('part', cdt, cdn)
		}
	},
	used_qty: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		let tot_qty = 0
		if (row.used_qty && row.part) {
			for (let i in frm.doc.items) {
				tot_qty += frm.doc.items[i].used_qty
			}
			frm.set_value("total_qty", tot_qty)
		}
	},
	price_ea: function (frm, cdt, cdn) {
		frm.script_manager.trigger("qty", cdt, cdn);

	},

});
