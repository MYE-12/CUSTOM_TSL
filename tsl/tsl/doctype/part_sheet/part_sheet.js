// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt
frappe.ui.form.on('Part Sheet', {
	refresh: function(frm) {
		frappe.call({
			method: "tsl.tsl.doctype.part_sheet.part_sheet.check_userrole",
			args: {
				"user":frappe.session.user
			},
			callback: function(r) {
				if(r.message) {
					console.log(r.message)
					if(r.message == "Technician"){
						var df = frappe.meta.get_docfield("Part Sheet Item","price_ea", cur_frm.doc.name);
						df.read_only = 1;
						cur_frm.refresh_fields();
					}
					else if(r.message == "Purchase User"){
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
					else if(r.message=="No Role"){
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
				}
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
				"doc" : cur_frm.doc,
				"item" :row.part,
				
			},
			callback :function(r){
				if(r.message){
					console.log(r.message)
					frappe.model.set_value(cdt, cdn, "price_ea", r.message);
					frm.refresh_fields();

				}
			}
	
		})
	
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
					console.log(r.message)
					frappe.model.set_value(cdt, cdn, "parts_availability",r.message);
					frm.refresh_fields();
					
				}
			}
	
		})
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
