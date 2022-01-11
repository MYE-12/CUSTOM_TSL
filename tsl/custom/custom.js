frappe.ui.form.on('Quotation', {
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
								filters: { is_quotation_created: 0 }
							}
						},
						action(selections) {
							console.log(selections);
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
										for(var i=0;i<r.message.length;i++){
											var childTable = cur_frm.add_child("items");
											childTable.item_code = r.message[i]["item"],
											childTable.item_name = r.message[i]["item_name"],
											childTable.wod_no = r.message[i]["wod"],
											childTable.model_no = r.message[i]["model_no"],
											childTable.serial_no = r.message[i]["serial_no"],
											childTable.description = r.message[i]["type"],
											childTable.qty = r.message[i]["qty"],
											cur_frm.refresh_fields("items");

										}
										
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