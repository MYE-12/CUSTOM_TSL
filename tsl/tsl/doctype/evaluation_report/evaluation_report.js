// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Evaluation Report', {
	// refresh: function(frm) {

	// }
	refresh:function(frm){
		if(frm.doc.work_order_data){
			frappe.call({
				method: "tsl.tsl.doctype.evaluation_report.evaluation_report.get_item_image",
				args: {
					"wod_no":frm.doc.work_order_data,
				},
				callback: function(r) {
					if(r.message) {
						cur_frm.set_df_property("item_photo", "options","<img src="+r.message+"></img>");
						cur_frm.refresh_fields();
					}
				}
			});

		}
		
	}
});
