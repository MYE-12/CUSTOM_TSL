// Copyright (c) 2023, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Return Note', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			frm.set_value("conversion_rate","1")
			frm.set_value("plc_conversion_rate","1")
			
			frm.set_value("plc_conversion_rate","1")
		}
		frm.add_custom_button(__('Work Order Data'),
		function() {
			var from_date = frappe.datetime.add_months(frappe.datetime.get_today(), -1)
					var to_date = frappe.datetime.get_today()
			new frappe.ui.form.MultiSelectDialog({
				doctype: "Work Order Data",
				target: frm,
				setters: {
					customer:frm.doc.customer,
					wod_component:null
				},
				
				add_filters_group: 1,
				get_query() {
					return {
						filters: { status:["in",["RNA-Return Not Approved","RNR-Return Not Repaired","RNP-Return No Parts","RNF-Return No Fault","C-Comparison"]],branch :frm.doc.branch_name}
					}
				},
				action(selections) {
					frappe.call({
						method: "tsl.tsl.doctype.return_note.return_note.get_wod_items",
						args: {
							"wod": selections
						},
						callback: function(r) {
							if(r.message) {
								console.log(r.message)
								cur_frm.doc.sales_rep = r.message[0]["sales_rep"];
								var tot_amt = 0;
								var tot_qty=0;
								for(var i=0;i<r.message.length;i++){
									var childTable = cur_frm.add_child("items");
									childTable.item_code = r.message[i]["item_code"],
									childTable.item_name = r.message[i]["item_name"],
									childTable.wod_no = r.message[i]["wod_no"],
									childTable.model = r.message[i]["model"],
									childTable.manufacturer = r.message[i]["manufacturer"],
									childTable.serial_number = r.message[i]["serial_number"],
									childTable.description = r.message[i]["description"],
									childTable.type = r.message[i]['type'],
									childTable.rate = r.message[i]["rate"]
									childTable.uom = r.message[i]["uom"]
									childTable.conversion_factor = r.message[i]["conversion_factor"]
									childTable.income_account = r.message[i]["income_account"]
									childTable.qty = r.message[i]["qty"]
									childTable.amount = r.message[i]["amount"]
									childTable.base_rate = r.message[i]["amount"]
									childTable.base_amount = r.message[i]["amount"]								
									tot_qty += r.message[i]["qty"];
									cur_frm.refresh_fields("items");
								}
								frm.doc.total = tot_amt;
								// frm.doc.total_qty = tot_qty;
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
	},
	validate:function(frm){
		frm.set_value("grand_total","1")
		frm.set_value("base_grand_total","1")
		frm.set_value("base_total","1")
		frm.set_value("base_net_total","1")
	}
});
