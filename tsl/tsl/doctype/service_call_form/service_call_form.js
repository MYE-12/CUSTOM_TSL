// Copyright (c) 2022, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Call Form', {
	refresh: function(frm) {
		if(frm.doc.docstatus===1){
			frm.add_custom_button(__('Internal Quotation'), function(){
					frappe.call({
						method: "tsl.tsl.doctype.service_call_form.service_call_form.create_qtn",
						args: {
							"source":frm.doc.name
						},
						callback: function(r) {
							if(r.message) {
								var doc = frappe.model.sync(r.message);
								// doc[0].similar_items_quoted_before = [];
								frappe.set_route("Form", doc[0].doctype, doc[0].name);
								
							}
						}
					});
					
					
								   
							}, ('Create'))
		}

	}
});
frappe.ui.form.on('Service Call Form', {
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