// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Part Sheet', {
	refresh: function(frm) {
		// var df = frappe.meta.get_docfield("Employer Project Details","company_name", cur_frm.doc.name);
		// df.options = ["Tech M", "Wipro", "TCS"];
	}
});

frappe.ui.form.on('Part Sheet Item', {
	price_ea:function(frm, cdt, cdn){
		let row = locals[cdt][cdn]
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