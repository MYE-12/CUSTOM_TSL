// Copyright (c) 2022, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Create Work Order', {
	refresh:function(frm){
		frm.disable_save()
		frm.set_value("branch",frappe.user_defaults.warehouse)
		frm.add_custom_button(__("Create Work Order"), function(){
			frappe.call({
				'method': 'tsl.tsl.doctype.equipment_received_form.equipment_received_form.create_workorder_data',
				'freeze':true,
				'args':{
				'order_no':cur_frm.doc
				},
				'callback':function(res){
					if(res.message){
						cur_frm.reload_doc();

					}
				}


			})
		});
	},

	branch:function(frm){
		if(frm.doc.company && frm.doc.branch){
			var d = {
				"Kuwait - TSL":"Repair - Kuwait - TSL",
				"Dammam - TSL-SA":"Repair - Dammam - TSL-SA",
				"Jeddah - TSL-SA":"Repair - Jeddah - TSL-SA",
				"Riyadh - TSL-SA":"Repair - Riyadh - TSL-SA"
			}
			frm.set_value("repair_warehouse",d[frm.doc.branch]);
			var d = {
				"Dammam - TSL-SA":"ERF-D.YY.-",
				"Riyadh - TSL-SA":"ERF-R.YY.-",
				"Jeddah - TSL-SA":"ERF-J.YY.-",
				"Kuwait - TSL":"ERF-K.YY.-"
			};
			if(frm.doc.branch){
				frm.set_value("naming_series",d[frm.doc.branch]);
			}

		}


	},
	company:function(frm){
		frm.trigger("branch")
	},
	customer:function(frm){
		if(!frm.doc.customer){
				return
		}
		frappe.call({
				method:'tsl.tsl.doctype.equipment_received_form.equipment_received_form.get_contacts',
				args: {
						"customer": frm.doc.customer,
				},
				callback(r) {
						if(r.message) {
								frm.set_query("incharge", function() {
										return {
												"filters": {
														"name":["in", r.message[0]]
												}
										};
								});
								if(r.message[0]){
									frm.set_value("incharge",r.message[0][0])
								}
								console.log("sale")
								console.log(r.message[1])
								console.log(r.message[2])
								if(r.message[1]){
									frm.set_query("sales_person", function() {
										return {
												"filters": {
														"name":["in", r.message[1]]
												}
										};
									});
								}
								
								if(r.message[2]){
									frm.set_value("sales_person",r.message[2])
								}
								else{
									frm.set_value("sales_person","");
									frm.set_value("sales_person_name","");
								}


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
},
work_order_data:function(frm){
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
						childTable.item_code = r.message[i]['item_code'],
						childTable.item_name = r.message[i]["item_name"],
						childTable.manufacturer = r.message[i]["mfg"]
						childTable.model = r.message[i]["model_no"],
						childTable.serial_no = r.message[i]["serial_no"]
						if(r.message[i]['serial_no']){
							childTable.has_serial_no = 1;
						}
						childTable.type = r.message[i]["type"],
						childTable.qty = r.message[i]["qty"],
						frm.doc.sales_person = r.message[i]["sales_rep"],
						frm.doc.customer = r.message[i]["customer"],
						frm.trigger("customer");
						frm.doc.address = r.message[i]["address"],
						frm.trigger("address");
						frm.doc.incharge = r.message[i]["incharge"],
						frm.trigger("incharge");
						frm.doc.branch = r.message[i]["branch"]
						cur_frm.refresh_fields();
					}
				}
			}
		});

	}
},
setup:function(frm){
	frm.fields_dict['received_equipment'].grid.get_field('item_code').get_query = function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var d = {};
		if(child.model){
			d['model'] = child.model;

		}
		if(child.manufacturer){
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

	frm.fields_dict['received_equipment'].grid.get_field('repair_warehouse').get_query = function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];

		return {
			filters: [
					["Warehouse","company", "=", cur_frm.doc.company],
					["Warehouse","is_repair","=",1],

			]
		};

		}







}
});
frappe.ui.form.on("Create Work Order", {
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

frappe.ui.form.on('Create Work Order', {
	setup: function(frm) {
		frm.set_query("branch", function() {
			return {
				filters: [
					["Warehouse","company", "=", frm.doc.company],
					["Warehouse","is_branch","=",1]

				]
			}

		});
		frm.set_query("repair_warehouse", function() {
			return {
				filters: [
					["Warehouse","company", "=", frm.doc.company],
					["Warehouse","is_repair","=",1]

				]
			}

		});
	}
});