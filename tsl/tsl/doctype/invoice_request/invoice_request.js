// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice Request', {
	// refresh: function(frm) {

	// }
	 
	// onload(frm){
	// 	if(frm.doc.quotation){
	// 		frm.trigger("get_data");
	// 	}
	// },

	onload: function(frm) {
        // Set the query for the child table field
        frm.fields_dict['invoice_list'].grid.get_field('quotation').get_query = function(doc, cdt, cdn) {
            // Custom filter logic
            return {
                filters: {
                    'quotation_type': ['in', ['Customer Quotation - Repair','Revised Quotation - Repair']],
					'workflow_state': ['in', ['Approved By Customer']],
                    
                }
            };
        };


		frm.fields_dict['sod_quotation'].grid.get_field('quotation').get_query = function(doc, cdt, cdn) {
            // Custom filter logic
            return {
                filters: {
                    'quotation_type': ['in', ['Customer Quotation - Supply','Revised Quotation - supply']],
                    'workflow_state': ['in', ['Approved By Customer']],
                }
            };
        };
    },


	get_data:function (frm){

			frm.call('get_work_orders').then(r=>{
				if(r.message){
			
					frm.fields_dict.html.$wrapper.html(r.message);
		
				}
		
									
				})
		
	},

	go_to(frm){
		frappe.set_route('Form','Quotation', frm.doc.quotation);

	},

	quotation(frm){
		frm.trigger("get_data");
	}
});


frappe.ui.form.on('Invoice Creation', {
	
	quotation(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (child.quotation) {
		    
		    frm.call({
				method: 'tsl.custom_py.utils.invoice_request',
				args: {
					qu:child.quotation,
				}
			}).then(r => {
				if (r.message) {
					// frm.clear_table('invoice_list');
					$.each(r.message, function(i,d) {
						console.log(d)
						let child = frm.add_child('invoice_list');
						child.wod_sod = d.wod_no;
					

					});
					frm.refresh_field('invoice_list');		
				}
			});
		}
	
	},
})

frappe.ui.form.on('SOD IV Creation', {
	quotation(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if (child.quotation) {
		    
		    frm.call({
				method: 'tsl.custom_py.utils.invoice_request_2',
				args: {
					qu:child.quotation,
				}
			}).then(r => {
				if (r.message) {
					// frm.clear_table('invoice_list');
					$.each(r.message, function(i,d) {
						console.log(d)
						let child = frm.add_child('sod_quotation');
						child.supply_order_data = d.supply_order_data;
					

					});
					frm.refresh_field('sod_quotation');		
				}
			});
		}
	
	},
})
