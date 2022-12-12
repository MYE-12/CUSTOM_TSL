// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Evaluation Report', {
	// refresh: function(frm) {

	// }
	refresh:function(frm){
		// if(frm.doc.work_order_data){
		// 	frappe.call({
		// 		method: "tsl.tsl.doctype.evaluation_report.evaluation_report.get_item_image",
		// 		args: {
		// 			"wod_no":frm.doc.work_order_data,
		// 		},
		// 		callback: function(r) {
		// 			if(r.message) {
		// 				cur_frm.set_df_property("item_photo", "options","<img src="+r.message+"></img>");
		// 				cur_frm.refresh_fields();
		// 			}
		// 		}
		// 	});

		// }
		if(frm.doc.attach_image){
			cur_frm.set_df_property("item_photo", "options","<img src="+frm.doc.attach_image+"></img>");
			cur_frm.refresh_fields();
		}
		if(frm.doc.docstatus == 0){
			if(in_list(frappe.user_roles,"Technician")){
				var df = frappe.meta.get_docfield("Part Sheet Item","price_ea", cur_frm.doc.name);
				df.read_only = 1;
				cur_frm.refresh_fields();
			}
			else if(in_list(frappe.user_roles,"Purchase User")){
				var df = frappe.meta.get_docfield("Part Sheet Item","part", cur_frm.doc.name);
				df.read_only = 1;
				var df = frappe.meta.get_docfield("Part Sheet Item","part_name", cur_frm.doc.name);
				df.read_only = 1;
				var df = frappe.meta.get_docfield("Part Sheet Item","type", cur_frm.doc.name);
				df.read_only = 1;
				var df = frappe.meta.get_docfield("Part Sheet Item","qty", cur_frm.doc.name);
				df.read_only = 1;
				cur_frm.refresh_fields();
			}
			else {
				var df = frappe.meta.get_docfield("Part Sheet Item","price_ea", cur_frm.doc.name);
				df.read_only = 1;
				var df = frappe.meta.get_docfield("Part Sheet Item","part", cur_frm.doc.name);
				df.read_only = 1;
				var df = frappe.meta.get_docfield("Part Sheet Item","part_name", cur_frm.doc.name);
				df.read_only = 1;
				var df = frappe.meta.get_docfield("Part Sheet Item","type", cur_frm.doc.name);
				df.read_only = 1;
				var df = frappe.meta.get_docfield("Part Sheet Item","qty", cur_frm.doc.name);
				df.read_only = 1;
				cur_frm.refresh_fields();

			}
			frm.fields_dict['evaluation_details'].grid.get_field('item').get_query = function(frm, cdt, cdn) {
				var child = locals[cdt][cdn];
				var d = {};
				if(child.model_no){
					d['model'] = child.model;
		
				}
				if(child.mfg){
					d['mfg'] = child.manufacturer;
				}
				if(child.type){
					d['type'] = child.type;
				}
				d['item_group'] = "Equipments";
				return{
					filters: d
				}
				
			}
				frm.fields_dict['items'].grid.get_field('part').get_query = function(frm, cdt, cdn) {
					var child = locals[cdt][cdn];
						var d = {};
						if(child.model){
							d['model'] = child.model;
	
						}
						if(child.category){
							d['category_'] = child.category;
						}
						if(child.sub_category){
							d['sub_category'] = child.sub_category;
						}
						d['item_group'] = "Components";
						return{
							filters: d
						}
			}
			
		}
		if(frm.doc.docstatus == 1 && frm.doc.parts_availability == "No"){
			frm.add_custom_button(__("Request for Quotation"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.part_sheet.part_sheet.create_rfq",
					args: {
						"ps": frm.doc.name
					},
					callback: function(r) {
						if(r.message) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
						}
					}
				});
			},__('Create'));
		}
		
	},
	setup:function(frm){
		
		frm.fields_dict['items'].grid.get_field('sub_category').get_query = function(frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			return{
				filters: {
					'category':child.category,
					
				}
			}
		}
		frm.set_query("department", function() {
			return {
				filters: [
					["Cost Center","company", "=", frm.doc.company],
					
				]
			}
		});

	}

});
frappe.ui.form.on('Part Sheet Item', {
	part: function(frm, cdt, cdn){
		let row = locals[cdt][cdn]
		if(row.part){
			frappe.call({
			method :"tsl.tsl.doctype.part_sheet.part_sheet.get_valuation_rate",
			args :{
				"item" :row.part,
				"qty":row.qty
				
			},
			callback :function(r){
				frappe.model.set_value(cdt, cdn, "price_ea", r.message[0]);
				frappe.model.set_value(cdt, cdn, "parts_availability", r.message[1]);
				row.total = row.qty * r.message[0];
				let tot_qty = 0
				let tot_amount = 0
				for(let i in frm.doc.items){
					tot_qty += frm.doc.items[i].qty
					tot_amount += frm.doc.items[i].total
				}
				frm.set_value("total_qty", tot_qty)
				frm.set_value("total_amount", tot_amount)
						frm.refresh_fields();
				}
		})
		}
		frm.refresh();
	},
	qty:function(frm, cdt, cdn){
		let row = locals[cdt][cdn]
		if(row.qty && row.part){
			frappe.call({
			method :"tsl.tsl.doctype.part_sheet.part_sheet.get_availabilty",
			args :{
				"qty" : row.qty,
				"item" :row.part,
				
			},
			callback :function(r){
				if(r.message){
					frappe.model.set_value(cdt, cdn, "parts_availability",r.message);
					frm.refresh_fields();
					
				}
				row.total = row.qty * row.price_ea
				let tot_qty = 0
				let tot_amount = 0
				for(let i in frm.doc.items){
					tot_qty += frm.doc.items[i].qty
					tot_amount += frm.doc.items[i].total
				}
				frm.set_value("total_qty", tot_qty)
				frm.set_value("total_amount", tot_amount)
				frm.refresh();
			}
	
		})
	   }
		
	},
	price_ea:function(frm,cdt,cdn){
		frm.script_manager.trigger("qty",cdt,cdn);

	},
	
});