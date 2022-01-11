frappe.ui.form.on('Quotation', {
    refresh:function(frm){
        console.log("called.....................")
        if (frm.doc.docstatus==0) {
			frm.add_custom_button(__('Work Order Data'),
				function() {
                    console.log("button works.............")
					erpnext.utils.map_current_doc({
						method: "tsl.__init__.get_work_order_data",
						source_doctype: "Work Order Data",
						target: frm,
						setters: [
							{
								label: "Customer",
								fieldname: "customer_name",
								fieldtype: "Link",
								options: me.frm.doc.quotation_to,
								default: me.frm.doc.party_name || undefined
							},
							
						],
						
					})
				}, __("Get Items From"), "btn-default");
		}
    },
});