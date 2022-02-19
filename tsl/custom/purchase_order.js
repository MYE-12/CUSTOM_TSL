frappe.ui.form.on('Purchase Order', {
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