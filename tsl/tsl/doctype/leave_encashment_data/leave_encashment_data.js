// Copyright (c) 2025, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Encashment Data', {
	encashing_days : function(frm){
		frm.trigger("calculate_encashable_amount")
	},
	leave_type: function(frm) {
		frappe.call({
			method:"hrms.hr.doctype.leave_application.leave_application.get_leave_balance_on",
			args:{
				employee:frm.doc.employee || '',
				leave_type:frm.doc.leave_type || '',
				date:frappe.datetime.now_date()
			},
			callback(k){
				if(k){
					frm.set_value("leave_balance",k.message)					
					frappe.db.get_value("Leave Type", {"name": frm.doc.leave_type}, "encashment_threshold_days", (r) => {
						if(r.encashment_threshold_days){
							if(r.encashment_threshold_days > k.message){
								var encashable = r.encashment_threshold_days - k.message
							}
							else{
								var encashable = k.message - r.encashment_threshold_days
							}
						}
						else{
							var encashable = k.message
						}
						// frm.trigger("calculate_encashable_amount")
						frm.set_value("encashable_days",encashable)
					});
				}
			}
		})
	},
	calculate_encashable_amount:function(frm){
		if(frm.doc.employee){
			frappe.call({
				method:"tsl.tsl.doctype.leave_encashment_data.leave_encashment_data.per_day_salary",
				args:{
					employee:frm.doc.employee,
				},
				callback(r){
					if(r){
						var encashable_amount  = frm.doc.encashing_days * r.message
						frm.set_value("encashment_amount",encashable_amount)
					}
				}
			})
		}
	}
});
