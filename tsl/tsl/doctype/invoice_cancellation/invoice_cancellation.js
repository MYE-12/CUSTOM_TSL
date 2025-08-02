// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice Cancellation', {
	refresh: function(frm) {
		frm.set_query('work_order_data', 'table_wknj', function(doc, cdt, cdn) {
			return {
				filters:[
					['company', '=', doc.company],
					['branch', '=', doc.branch],
					['sales_rep', '=', doc.sales_person],
					['status', '!=', "C-Cancelled"],
					['invoice_no', 'is', 'set']
				]
			};
		});


		frm.set_query('invoice_no', 'cancellation_list', function(doc, cdt, cdn) {
			return {
				filters:[
					['company', '=', doc.company],
					['branch', '=', doc.branch],
					['custom_sales_person', '=', doc.sales_person],
					// ['status', '!=', "Cancelled"],
					['is_return', '!=', "1"],
					
				]
			};
		});
	}

	
});


// frappe.ui.form.on('Cancellation Table', {
	
// 	quotation(frm, cdt, cdn) {
// 		var child = locals[cdt][cdn]
// 		if (child.work_order_data) {
		    
// 		    frm.call({
// 				method: 'tsl.custom_py.utils.invoice_cancellation_inv',
// 				args: {
// 					qu:child.work_order_data,
// 				}
// 			}).then(r => {
// 				if (r.message) {
// 					// frm.clear_table('invoice_list');
// 					$.each(r.message, function(i,d) {
// 						console.log(d)
// 						let child = frm.add_child('able_wknj');
// 						child.wod_sod = d.wod_no;
					

// 					});
// 					frm.refresh_field('able_wknj');		
// 				}
// 			});
// 		}
	
// 	},
// })

