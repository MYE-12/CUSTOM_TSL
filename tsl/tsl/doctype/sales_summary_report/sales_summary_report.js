// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Summary Report', {
	// refresh: function(frm) {

	// }


	download:function(frm){
		
			var print_format ="Sales Summary";
				var f_name = "Sales Summary Report"
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Sales Summary Report")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
		
		
	},

	get_data:function (frm){
		if (frm.doc.report){
			frm.call('get_work_orders').then(r=>{
				if(r.message){
			
					frm.fields_dict.html.$wrapper.html(r.message);
		
				}
		
									
				})
		}
	},

	report(frm){
		if(frm.doc.report == "RS-Repaired and Shipped"){
			
				let today = frappe.datetime.get_today();
			// 	console.log(today)
			
				frm.set_value("from_date",today)
				frm.set_value("to_date",today)
			}
		frm.trigger("get_data");
	},

	onload(frm){
		if (frappe.user.has_role("Sales user")) {
            frm.set_df_property('sales_person', 'hidden', 1);
        }
		
		if (frappe.user.has_role("Sales Manager")) {
            frm.set_df_property('sales','hidden', 1);
        }
		
		if(!frappe.session.user == "Administrator"){
			console.log(frappe.session.user)
			frappe.db.get_value('Sales Person', {'custom_user':frappe.session.user}, ['name','company'], (r) => {
      	    
				if(r){
					frm.set_value("sales",r.name)
					frm.set_value("company",r.company)
				}
			   
				
	  });
		}
		frm.trigger("get_data");
	},

	from_date(frm){
		frm.trigger("get_data");
	},

	to_date(frm){
		frm.trigger("get_data");
	},

	company(frm){
		frm.trigger("get_data");
	},

	work_order_data(frm){
		frm.trigger("get_data");
	},

	customer(frm){
		frm.trigger("get_data");
	},

	// report(frm) {
	// 	if(frm.doc.report){
	// 	frm.call('get_work_orders').then(r=>{
	// 	if(r.message){
	
	// 		frm.fields_dict.html.$wrapper.html(r.message);

	// 	}

							
	// 	})
	// 	}
	// 	else{
	// 		frm.fields_dict.html.$wrapper.html('');

	// 	}
		
		
	// },

	customer(frm){
		if(frm.doc.customer){
			frm.trigger("get_data");
			}

			else{
			
				frm.trigger("get_data");
			}
	},

	work_order_data(frm){
		if(frm.doc.work_order_data){
			frm.trigger("get_data");
			}

			else{
			
				frm.trigger("get_data");
			}
	},
	
	sales_person(frm){
		if(frm.doc.sales_person){
			frm.trigger("get_data");
			}

		else{
			
			frm.trigger("get_data");
		}
	}
});
