// Copyright (c) 2025, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on("Lab Report Summary", {
	get_data:function (frm){
        frappe.show_alert({
            message: "Please Wait,Data processing takes time around 5 minutes",
            indicator: 'blue'
        }, 50);  // 5 seconds

        frm.call('get_data').then(r=>{
            if(r.message){
                frm.fields_dict.html.$wrapper.html(r.message);

            }

                                
            })

    },

    get_data1:function (frm){
        frappe.show_alert({
            message: "Data processing",
            indicator: 'blue'
        }, 50);  // 5 seconds

        frm.call('get_data1').then(r=>{
            if(r.message){
                frm.fields_dict.html.$wrapper.html(r.message);

            }

                                
            })

    },

    view(frm){
        frm.trigger("get_data");
    },

    view1(frm){
        frm.trigger("get_data1");
    },

    download:function(frm){
		var print_format ="Lab Report Summary";
		var f_name = "Lab Report Summary"
		window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
			+ "doctype=" + encodeURIComponent("Lab Report Summary")
			+ "&name=" + encodeURIComponent(f_name)
			+ "&trigger_print=1"
			+ "&format=" + print_format
			+ "&no_letterhead=0"
		));
	

	
	
	},


});
