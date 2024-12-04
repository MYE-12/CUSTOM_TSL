// Copyright (c) 2022, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Supply Order Data', {
	onload(frm){
		if(frappe.session.user != "info@tsl-me.com" && frappe.session.user != "Administrator"){
			
			var df = frappe.meta.get_docfield("Supply Order Table", "model_no", frm.doc.name);
			df.read_only = 1;

			var df = frappe.meta.get_docfield("Supply Order Table", "mfg", frm.doc.name);
			df.read_only = 1;
			
			var df = frappe.meta.get_docfield("Supply Order Table", "type", frm.doc.name);
			df.read_only = 1;

			var df = frappe.meta.get_docfield("Supply Order Table", "item_name", frm.doc.name);
			df.read_only = 1;
			
		}
	},

	refresh: function(frm) {
		if(frm.doc.docstatus == 1){
			frm.add_custom_button(__("Request for Quotation"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.supply_order_data.supply_order_data.create_rfq",
					args: {
						"sod": frm.doc.name
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
		if(frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Quotation"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.supply_order_data.supply_order_data.create_quotation",
					args: {
						"sod": frm.doc.name
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
		if(frm.doc.docstatus === 1) {
		if(frm.doc.department == "Supply - TSL"){
		frm.add_custom_button(__("Sales Invoice"), function(){
			frappe.call({
				method: "tsl.tsl.doctype.supply_order_data.supply_order_data.create_sal_inv_tender",
				args: {
					"sod": frm.doc.name
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
		
		}

		if(frm.doc.docstatus === 1) {
			if(frm.doc.department == "Supply Tender - TSL"){
			frm.add_custom_button(__("Sales Invoice"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.supply_order_data.supply_order_data.create_sal_inv_tender",
					args: {
						"sod": frm.doc.name
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
			
			}


		if(frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Delivery Note"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.supply_order_data.supply_order_data.create_dn",
					args: {
						"sod": frm.doc.name
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
		if(frm.doc.docstatus == 1){
			if(frm.doc.invoice_no){
				frm.add_custom_button(__("Make Payment"), function(){
					frappe.call({
						method: "tsl.tsl.doctype.supply_order_data.supply_order_data.make_payment",
						args: {
							"sod": frm.doc.name,
							"invoice":frm.doc.invoice_no
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
			
		}

	},
	setup:function(frm){
		frm.fields_dict['in_stock'].grid.get_field('part').get_query = function(frm, cdt, cdn) {
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
			
		}
	
	
	

	},
	branch:function(frm){
		var d = {
			"Dammam - TSL-SA":"SOD-D.YY.-",
			"Riyadh - TSL-SA":"SOD-R.YY.-",
			"Jeddah - TSL-SA":"SOD-J.YY.-",
			"Kuwait - TSL":"SOD-K.YY.-"
		};
		if(frm.doc.branch){
			frm.set_value("naming_series",d[frm.doc.branch]);
		}
	},
});
frappe.ui.form.on('Supply Order Data', {
	setup: function(frm) {
		frm.set_query("branch", function() {
			return {
				filters: [
					["Warehouse","company", "=", frm.doc.company],
					["Warehouse","is_branch","=",1]
					
				]
			}
		});
		frm.set_query("department", function() {
			return {
				filters: [
					["Cost Center","company", "=", frm.doc.company],
					
				]
			}
		});
	}

});


