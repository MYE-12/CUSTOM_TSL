// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Appraisal', {
	refresh: function(frm) {
		if(!frm.doc.__islocal){
			frm.add_custom_button(__("Print"), function () {
				var f_name = frm.doc.name;
				var print_format = "Employee Appraisal";
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Employee Appraisal")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}); 
		}
	}
});
// frappe.ui.form.on('Appraisal Table', {
// 	teamwork: function(frm, cdt, cdn) {
// 		let row = locals[cdt][cdn]
// 		var total = (row.teamwork + row.attendance + row.quality + row.skils + row.communication) * 5
// 		frm.set_value("overall",total.toFixed(2))
// 	},
// 	attendance: function(frm, cdt, cdn) {
// 		frm.trigger("teamwork", cdt, cdn);
// 	},
// 	quality: function(frm, cdt, cdn) {
// 		frm.trigger("teamwork", cdt, cdn);
// 	},
// 	skils: function(frm, cdt, cdn) {
// 		frm.trigger("teamwork", cdt, cdn);
// 	},
// 	communication: function(frm, cdt, cdn) {
// 		frm.trigger("teamwork", cdt, cdn);
// 	},
// });