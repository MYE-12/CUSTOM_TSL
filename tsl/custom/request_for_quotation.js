frappe.ui.form.on('Request for Quotation', {
    
    onload_post_render:function(frm){
        frm.set_query("branch", function() {
                return {
                        filters: [
                                ["Warehouse","company", "=", frm.doc.company],
                                ["Warehouse","is_branch","=",1]
                                
                        ]
                };
        });
        frm.fields_dict['items'].grid.get_field('item_code').get_query = function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		return{
			filters: {
				'model': child.model,
				'manufacturer':child.manufacturer,
				'type':child.type,
				'serial_no':child.serial_number,
                                'financial_code':child.part_number,
                                'category_':child.category,
                                'sub_category':child.sub_category
			}
		};
	};
    
        },
    refresh:function(frm){
        if (frm.doc.docstatus === 1) {
		frm.add_custom_button(__('Multiple Supplier Quotation'),
			function(){ 
                        frappe.call({
                                method: "tsl.custom_py.supplier_quotation.make_supplier_quotation_from_rfq",
                                args: {
                                        "source_name": cur_frm.doc.name
                                        
                                },
                               
                                callback: function(r) {
                                        if(r.message) {
                                        }
                                }
                        });
                        }, __("Create"));
                }

        }
});
