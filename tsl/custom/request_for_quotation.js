frappe.ui.form.on('Request for Quotation', {
    
	onload_post_render:function(frm){
        frm.fields_dict['items'].grid.get_field('warehouse').get_query = function(doc){
                return{
                        filters:[
                                {"company": frm.doc.company}
                        ]
                }
        }
    
   }
});
