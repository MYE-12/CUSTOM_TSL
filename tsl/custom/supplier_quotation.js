frappe.ui.form.on("Supplier Quotation", {
    refresh:function(frm){
        if(frm.doc.supply_order_data ){
        frm.add_custom_button(__('Price Comparison Sheet'), function () {
            if(frm.doc.supply_order_data){
                frappe.set_route('query-report', 'Price Comparison Sheet', { sod_no: frm.doc.supply_order_data });

            }
        }, __("View"));
        }
        if(frm.doc.supply_order_data){
            if(frm.doc.workflow_state == "Approved" && frm.doc.docstatus == 1){
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
        else if(frm.doc.work_order_data){
            if(frm.doc.workflow_state == "Approved" && frm.doc.docstatus == 1){
                frappe.call({
                    method: "tsl.custom_py.supplier_quotation.reject_other_sq",
                    args: {
                            "sq": cur_frm.doc.name,
                            "wod":frm.doc.work_order_data
                            
                    },
                   
                    callback: function(r) {
                            if(r.message) {
                            }
                    }
            });
            }
        }
        
        // if(frm.doc.docstatus ==  0 && frm.doc.workflow_state == "Waiting For Approval" && frm.doc.supply_order_data){
        //     frm.add_custom_button(__('Item Allocation'), function () {
        //         frappe.call({
		// 			method: "tsl.custom_py.supplier_quotation.item_allocate_to_supplier",
		// 			args: {
		// 				"sod": frm.doc.supply_order_data
		// 			},
		// 			callback: function(r) {
		// 				if(r.message) {
		// 					var doc = frappe.model.sync(r.message);
		// 					frappe.set_route("Form", doc[0].doctype, doc[0].name);
							
		// 				}
		// 			}
		// 		});
        //     }, __("Create"));
        // }
        
    
    },
    
    
});