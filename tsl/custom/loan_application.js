
frappe.ui.form.on('Loan Application', {
    // refresh(frm){
    //     frappe.db.get_value("Loan", {"loan_application": frm.doc.name, "docstatus": 1}, "name", (r) => {
    //         if (Object.keys(r).length === 0) {
    //             frm.add_custom_button(__('Loan Data'), function() {
    //                 frm.trigger('create_loan');
    //             },__('Create'))
    //         } else {
    //             frm.set_df_property('status', 'read_only', 1);
    //         }
    //     });
    // },
    create_loan: function(frm) {
		if (frm.doc.status != "Approved") {
			frappe.throw(__("Cannot create loan until application is approved"));
		}

		frappe.model.open_mapped_doc({
			method: 'tsl.custom_py.loan_application.create_loan',
			frm: frm
		});
	},
})