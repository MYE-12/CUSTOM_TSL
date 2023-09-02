// Copyright (c) 2023, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Warranty Lookup', {
	refresh: function(frm) {
	
		var date = frappe.datetime.get_today()
		console.log(date)
		frm.set_value("date",date)
	},
	work_order_data(frm){
		if(frm.doc.work_order_data){
			frappe.call({
				method: "tsl.tsl.doctype.warranty_form.warranty_form.get_dn",
				args: {
					'wod': frm.doc.work_order_data,
					
				},
				callback:function(r){
					
					$.each(r.message,function(i,v){
						console.log(v)
						if(frm.doc.date <= v.warranty_end_date){
							frappe.msgprint({
								title: __('<b style = color:green>Warranty Cover</b>'),
								indicator: 'green',
								message: (__("<center><b style=color:green>Note :This Work Order Date is Under Warranty DN -No</b>-{0}</center>",[v.dn]))
							});
							frm.set_value("warranty_status","Under Warranty")

						}
						else{
							console.log('ui')
							frappe.msgprint({
								title: __('<b style = color:green>Warranty Cover</b>'),
								indicator: 'green',
								message: __('<center><b style=color:green>Note :This Work Order Date is Not Under Warranty !!</b></center>')
							});
							frm.set_value("warranty_status","Warranty Expired")

						}

					})
					
				}
			});
		}
	}
});
