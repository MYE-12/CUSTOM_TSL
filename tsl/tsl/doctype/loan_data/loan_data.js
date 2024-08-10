// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Loan Data', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Repayment Schedule', {
	deduct(frm,cdt,cdn) {
		var child = locals[cdt][cdn]
		frappe.call({
			method:"tsl.tsl.doctype.loan_data.loan_data.create_additional_salary",
			args:{
				'name':child.name,
				'is_deducted':child.is_deducted,
				'employee':frm.doc.applicant,
				'company':frm.doc.company,
				'payment_date':child.payment_date,
				'total_payment':child.total_payment
			},
		})
	}
})