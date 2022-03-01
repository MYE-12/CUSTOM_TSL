frappe.ui.form.on('Request for Quotation', {
    
    onload_post_render:function(frm){
        frm.fields_dict['items'].grid.get_field('warehouse').get_query = function(doc){
                return{
                        filters:[
                                {"company": frm.doc.company}
                        ]
                }
        }
    
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
