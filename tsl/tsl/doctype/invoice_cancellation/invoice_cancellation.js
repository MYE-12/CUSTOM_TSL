// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice Cancellation', {
	refresh: function(frm) {
		frm.set_query('invoice_no', 'cancellation_list', function(doc, cdt, cdn) {
			return {
				filters:[
					['company', '=', doc.company],
					['is_return', '=', 0]
				]
			};
		});
	}
});
