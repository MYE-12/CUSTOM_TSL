// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Appraisal', {
	set_series(frm){
		if(frm.doc.__islocal){
			frm.call("set_series")
			.then(r=>{
				frm.set_value("naming_series",r.message)
			})
		}
	},
	appraisal_calculation:function(frm){
		if(frm.doc.appraisal){
			$.each(frm.doc.appraisal,function(i,row){
				row.score = parseInt(row.teamwork) + parseInt(row.attendance) + parseInt(row.quality) + parseInt(row.skils)
			})
			frm.refresh_field("appraisal")
		}
	},
	posting_date(frm){
		frm.trigger("set_series")
	},
	validate(frm){
		frm.trigger("set_series")
		frm.trigger("appraisal_calculation")
	},
	get_employees: function(frm){
		frm.call("fetch_employee_details")
		.then(r=>{
			frm.refresh_field("appraisal")
			frm.save()
		})
	},
	refresh: function(frm) {
		frm.trigger("set_series")
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