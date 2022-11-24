frappe.ui.form.on('Purchase Order', {
	onload_post_render:function(frm){
        frm.set_query("branch", function() {
                return {
                        filters: [
                                ["Branch","company", "=", frm.doc.company],
                                ["Branch","is_branch","=",1]
                                
                        ]
                };
        });
        frm.fields_dict['items'].grid.get_field('item_code').get_query = function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		return{
			filters: {
				'model': child.model,
				'manufacturer':child.mfg,
				'type':child.type,
				'serial_no':child.serial_no,
				'financial_code':child.part_number,
				'category_':child.category,
				'sub_category':child.sub_category
			}
		};
	};
    
        },
    refresh:function(frm){
		if(frm.doc.workflow_state === "Rejected" && frm.doc.docstatus===0){
		frm.add_custom_button(__('Revised Purchase Order'), function(){
				frappe.call({
					method: "tsl.get_revised_po",
					args: {
						"source": frm.doc.name,
					},
					callback: function(r) {
						if(r.message) {
							var doc = frappe.model.sync(r.message);
							// doc[0].similar_items_quoted_before = [];
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
							
						}
					}
				});
        }, ('Create'))
	}
   }
});