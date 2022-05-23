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
                var d = {};
			if(child.model){
				d['model'] = child.model;
	
			}
			if(child.manufacturer){
				d['mfg'] = child.manufacturer;
			}
			if(child.type){
				d['type'] = child.type;
			}
                        if(child.category){
				d['category_'] = child.category;
			}
                        if(child.sub_category){
				d['sub_category'] = child.sub_category;
			}
			return{
				filters: d
			}
		
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
