// Copyright (c) 2022, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Supply Order Form', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1){
			frm.add_custom_button(__("Create Supply Order Data"), function(frm){
				frappe.call({
					'method': 'tsl.tsl.doctype.supply_order_form.supply_order_form.create_supply_order_data',
					'args':{
					'order_no':cur_frm.doc.name
					},
					'callback':function(res){
						if(res.message){
						}
					}
					})

			})
		}
		if(frm.doc.received_equipment){
			let options = []
			for(let i in frm.doc.received_equipment){
				if(!options.includes(frm.doc.received_equipment[i].item)){
					options.push(frm.doc.received_equipment[i].item)
				}
			}
			frm.fields_dict['images'].grid.get_field('item').get_query = function(doc){
				return{
					filters:{
						"name": ["in", options]
					}
				}
			}
		}

	},
	customer:function(frm){
		if(!frm.doc.customer){
				return
		}
		frappe.call({
				method:'tsl.tsl.doctype.supply_order_form.supply_order_form.get_contacts',
				args: {
						"customer": frm.doc.customer,
				},
				callback(r) {
						if(r.message) {
								frm.set_query("incharge", function() {
										return {
												"filters": {
														"name":["in", r.message]
												}
										};
								});
						}
				}
		});
	},
	address:function(frm){
		if (frm.doc.address) {
			frappe.call({
				method: 'frappe.contacts.doctype.address.address.get_address_display',
				args: {
					"address_dict": frm.doc.address
				},
				callback: function(r) {
					frm.set_df_property("customer_address","options", "Customer  Address <br><br>"+r.message+"<br>");
					frm.refresh_fields();
				}
			});
		}
	},work_order_data:function(frm){
		if(frm.doc.work_order_data){
			frappe.call({
				method:'tsl.tsl.doctype.equipment_received_form.equipment_received_form.get_wod_details',
				args: {
						"wod": frm.doc.work_order_data,
				},
				callback(r) {
					if(r.message) {
						cur_frm.clear_table("received_equipment")
						for(var i=0;i<r.message.length;i++){
							var childTable = cur_frm.add_child("received_equipment");
							childTable.item_name = r.message[i]["item_name"],
							childTable.manufacturer = r.message[i]["mfg"]
							childTable.model = r.message[i]["model_no"],
							childTable.serial_no = r.message[i]["serial_no"],
							childTable.type = r.message[i]["type"],
							frm.doc.sales_person = r.message[i]["sales_rep"],
							childTable.qty = r.message[i]["qty"],
							cur_frm.refresh_fields("received_equipment");
						}
					}
				}
			});
	
		}
	},
	setup:function(frm){
		frm.fields_dict['equipments_in_stock'].grid.get_field('part').get_query = function(frm, cdt, cdn) {
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
					if(child.manufacturer){
						d['mfg'] = child.manufacturer;
					}
					if(child.type){
						d['type'] = child.type;
					}
					d['item_group'] = "Components";
					return{
						filters: d
					}
			
		},
		frm.fields_dict['equipments_in_stock'].grid.get_field('sub_category').get_query = function(frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			return{
				filters: {
					
					'category':child.category
				}
			}
		}
	}
	});
frappe.ui.form.on("Supply Order Form", {
	setup: function(frm) {
		frm.set_query("address", function() {
			return {
				filters: [
					["Dynamic Link","parenttype", "=", "Address"],
					["Dynamic Link","link_name","=",frm.doc.customer],
					["Dynamic Link","link_doctype","=","Customer"]
					
				]
			}
		});
		
	}
});
frappe.ui.form.on('Recieved Equipment Image', {
	images_add:function(frm){
		if(frm.doc.received_equipment){
			let options = []
			for(let i in frm.doc.received_equipment){
				if(!options.includes(frm.doc.received_equipment[i].item)){
					options.push(frm.doc.received_equipment[i].item)
				}
			}
			frm.fields_dict['images'].grid.get_field('item').get_query = function(doc){
				return{
					filters:{
						"name": ["in", options]
						}
				}
			}
		}
	}
});
frappe.ui.form.on('Supply Order Form', {
	setup: function(frm) {
		frm.set_query("branch", function() {
			return {
				filters: [
					["Warehouse","company", "=", frm.doc.company],
					["Warehouse","is_branch","=",1]
					
				]
			}
		});
	}
});
frappe.ui.form.on('Supply Data Item', {
	
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
				row.total = row.qty * row.price_ea
				}
		})
		}
		frm.refresh();
	},
	qty:function(frm, cdt, cdn){
		let row = locals[cdt][cdn]
		if(row.qty){
			frappe.call({
			method :"tsl.tsl.doctype.part_sheet.part_sheet.get_availabilty",
			args :{
				"qty" : row.qty,
				"item" :row.part,
				
			},
			callback :function(r){
				if(r.message){
					frappe.model.set_value(cdt, cdn, "parts_availability",r.message);
					row.total = row.qty * row.price_ea
					frm.refresh_fields();
					
				}
			}
	
		})
	   }
	},
	price_ea:function(frm,cdt,cdn){
		frm.script_manager.trigger("qty",cdt,cdn);

	},
	
});

