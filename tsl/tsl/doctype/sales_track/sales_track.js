// Copyright (c) 2023, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Track', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			frm.set_value("date",frappe.datetime.get_today())
			// frm.set_value("sales_user",frappe.session.user)
		}
		// if(frm.doc.sales_user){
		// 	frappe.db.get_value('User', frm.doc.sales_user, 'full_name', (values) => {
		// 		frm.set_value("sales_person", values.full_name);
		// 	});
		// }
	}
});
