// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipment Received Form', {
	refresh: function(frm) {
		
		if(frm.doc.docstatus == 1){
			frm.add_custom_button(__("Create Work Order Data"), function(frm){
				frappe.call({
					'method': 'tsl.tsl.doctype.equipment_received_form.equipment_received_form.create_workorder_data',
					'args':{
					'order_no':cur_frm.doc.name
					},
					'callback':function(res){
						if(res.message){
//							frappe.msgprint("Work order data created")
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
				method:'tsl.tsl.doctype.equipment_received_form.equipment_received_form.get_contacts',
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
}
});
frappe.ui.form.on("Equipment Received Form", {
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
frappe.ui.form.on('Equipment Received Form', {
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
