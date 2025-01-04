// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Create Project', {

	customer(frm){
		frm.call('get_contact').then(r=>{
			if(r.message){
				console.log(r.message[0])
				frm.set_value("customer_representative",r.message[0])
			}					
			})
	},

	refresh: function(frm) {
		frm.fields_dict['items'].grid.get_field('sku').get_query = function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];  // Get the current row in child table
            return {
                filters: {
                    'model': row.model // Filter by item_group
                }
            };
        };

		frm.set_query('sales_person', function(doc, cdt, cdn) {
            return {
                filters: {
                    'company': frm.doc.company  // Filter sales person by company
                }
            };
        });

		frm.set_query('customer', function(doc, cdt, cdn) {
            return {
                filters: {
                    'territory': "DUBAI"  // Filter sales person by company
                }
            };
        });
	},

	setup: function (frm) {
		frm.set_query("branch", function () {
			return {
				filters: [
					["Branch", "company", "=", frm.doc.company]

				]
			}

		});
	}
});
