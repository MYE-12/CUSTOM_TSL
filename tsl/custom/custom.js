frappe.ui.form.on('Quotation', {
    onload:function(frm){
        if(frm.doc.quotation_type == "Internal Quotation" && frm.doc.docstatus==1){
		frm.add_custom_button(__('Customer Quotation'), function(){
                                var new_doc = frappe.model.copy_doc(frm.doc);
                                new_doc.quotation_type = "Customer Quotation"
                                frappe.set_route('Form', 'Quotation', new_doc.name);
                        }, ('Create'))
	}
	if(frm.doc.quotation_type == "Customer Quotation" && frm.doc.workflow_state=="Rejected by Customer"){ 
                frm.add_custom_button(__('Revised Quotation'), function(){
                                var new_doc = frappe.model.copy_doc(frm.doc);
                                new_doc.quotation_type = "Revised Quotation"
                                frappe.set_route('Form', 'Quotation', new_doc.name);
                        }, ('Create'))
        }
    },
	refresh:function(frm){
        if (frm.doc.docstatus==0) {
			frm.add_custom_button(__('Work Order Data'),
				function() {
					new frappe.ui.form.MultiSelectDialog({
						doctype: "Work Order Data",
						target: frm,
						setters: {
							customer:frm.doc.customer_name ,
						},
						add_filters_group: 1,
						// date_field: "transaction_date",
						get_query() {
							return {
								filters: { is_quotation_created: 0, docstatus:1 }
							}
						},
						action(selections) {
							frappe.call({
								method: "tsl.custom_py.quotation.get_wod_items",
								args: {
									"wod": selections
								},
								callback: function(r) {
									if(r.message) {
										console.log(r.message)
										cur_frm.clear_table("items");
										cur_frm.doc.sales_rep = r.message[0]["sales_rep"];
										var tot_amt = 0;
										var tot_qty=0;
										for(var i=0;i<r.message.length;i++){
											var childTable = cur_frm.add_child("items");
											childTable.item_code = r.message[i]["item"],
											childTable.item_name = r.message[i]["item_name"],
											childTable.wod_no = r.message[i]["wod"],
											childTable.model_no = r.message[i]["model_no"],
											childTable.serial_no = r.message[i]["serial_no"],
											childTable.description = r.message[i]["type"],
											childTable.uom  = r.message[i]["uom"],
											childTable.qty = r.message[i]["qty"],
											childTable.rate = r.message[i]["total_amt"]
											var amt = r.message[i]["qty"] * r.message[i]["total_amt"];
											childTable.amount = amt,
											childTable.final_approved_price = (amt*(302.9/100))+amt,
											tot_amt += amt;
											tot_qty += r.message[i]["qty"];

											cur_frm.refresh_fields("items");
										

										}
										frm.doc.total = tot_amt;
										frm.doc.total_qty = tot_qty;
										frm.doc.grand_total = tot_amt+frm.doc.total_taxes_and_charges;
										frm.doc.final_approved_price = (frm.doc.grand_total*(302.8/100))+frm.doc.grand_total;
										cur_frm.refresh_fields();

									}
								}
							});
							cur_dialog.hide();
						}

					});
				}, __("Get Items From"), "btn-default");
		}
		    },
			
});

frappe.ui.form.on("Quotation Item",{ 
	
	   qty : function(frm,cdt,cdn){
			var item = locals[cdt][cdn];
			if(item.qty){
				item.amount = item.qty * item.rate;
				item.final_approved_price = (item.amount *(302.8/100))+item.amount;
				var tot_amt = 0;
				var tot_qty=0;
				for(var i=0 ;i< frm.doc.items.length;i++){
					tot_amt += frm.doc.items[i]["amount"];
					tot_qty += frm.doc.items[i]["qty"];

				}
				frm.doc.total = tot_amt;
				frm.doc.total_qty = tot_qty;
				frm.doc.grand_total = tot_amt+frm.doc.total_taxes_and_charges;
				frm.doc.final_approved_price = (frm.doc.grand_total*(302.8/100))+frm.doc.grand_total;
				cur_frm.refresh_fields();

				
			}
		   
	   }
		
	});

