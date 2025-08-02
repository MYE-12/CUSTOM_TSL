// Copyright (c) 2025, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Replacement Unit', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1){
			frm.add_custom_button(__("Request for Quotation"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.replacement_unit.replacement_unit.create_rfq",
					args: {
						"docname": frm.doc.name
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
});
