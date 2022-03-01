frappe.ui.form.on("Supplier Quotation", {
    refresh:function(frm){
        if(frm.doc.supply_order_data){
            frm.add_custom_button(__('Price Comparison Sheet'), function () {
                frappe.set_route('query-report', 'Price Comparison Sheet', { sod_no: frm.doc.supply_order_data });
            }, __("View"));
        }
        if(frm.doc.workflow_state == "Approved" && frm.doc.supply_order_data && frm.doc.docstatus == 1){
            frappe.call({
                method: "tsl.custom_py.supplier_quotation.reject_other_sq",
                args: {
                        "sq": cur_frm.doc.name,
                        "sod":frm.doc.supply_order_data
                        
                },
               
                callback: function(r) {
                        if(r.message) {
                        }
                }
        });
        }
        
    
    }
    
});