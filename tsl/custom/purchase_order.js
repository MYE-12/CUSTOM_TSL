frappe.ui.form.on('Purchase Order', {
	onload_post_render:function(frm){
		var end_date = frappe.datetime.add_days(frm.doc.transaction_date, 15);
		cur_frm.set_value("schedule_date", end_date);
        // frm.set_query("branch", function() {
        //         return {
        //                 filters: [
        //                         ["Warehouse","company", "=", frm.doc.company],
        //                         // ["Warehouse","is_branch","=",1]
                                
        //                 ]
        //         };
        // });
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
	if (frm.doc.docstatus===0 && frm.doc.quotation_type == "Internal Quotation - Repair") {
		frm.add_custom_button(__('Evaluation Report'),
		function() {
			var from_date = frappe.datetime.add_months(frappe.datetime.get_today(), -1)
					var to_date = frappe.datetime.get_today()
			new frappe.ui.form.MultiSelectDialog({
				doctype: "Evaluation Report",
				target: frm,
				setters: {
					// customer:frm.doc.party_name,
					wod_component:null
				},
				
				add_filters_group: 1,
				// get_query() {
				// 	return {
				// 		filters: { is_quotation_created: 0, docstatus:1,branch :frm.doc.branch_name, posting_date:["between",[from_date,to_date]]}
				// 	}
				// },
				action(selections) {
					frappe.call({
						method: "tsl.custom_py.quotation.get_wod_items",
						args: {
							"wod": selections
						},
						callback: function(r) {
							if(r.message) {
								cur_frm.doc.sales_rep = r.message[0]["sales_rep"];
								var tot_amt = 0;
								var tot_qty=0;
								var wo_no_txt = r.message[0]["wod"]
								var wo = wo_no_txt.split("-")

								for(var i=0;i<r.message.length;i++){
									var childTable = cur_frm.add_child("items");
									childTable.item_code = r.message[i]["item"],
									childTable.item_name = r.message[i]["item_name"],
									childTable.wod_no = r.message[i]["wod"],
									childTable.model_no = r.message[i]["model_no"],
									childTable.wo_no = wo[2],
									childTable.manufacturer = r.message[i]["manufacturer"],
									childTable.serial_no = r.message[i]["serial_no"],
									childTable.description = r.message[i]["description"],
									childTable.type = r.message[i]['type'],
									childTable.qty = r.message[i]["qty"]										
									tot_qty += r.message[i]["qty"];
									cur_frm.refresh_fields("items");
								}
								frm.doc.total = tot_amt;
								frm.doc.total_qty = tot_qty;
								frm.doc.grand_total = tot_amt+frm.doc.total_taxes_and_charges;
								frm.doc.rounded_total = frm.doc.grand_total;
								cur_frm.refresh_fields();

							}
						}
					});
					cur_dialog.hide();
				}

			});
		}, __("Get Items From"), "btn-default");
}
   }
});
