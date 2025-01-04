// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Data', {
	refresh: function(frm) {
		// if(frm.doc.quotation_type == "Site Visit Quotation - Internal"){
			frm.add_custom_button(__('Create'), function(){
					
				
				frm.call('crt_wo').then(r=>{
					if(r.message){
						console.log(r.message)
			
					}
			
										
					})
	
	
							})

				frm.add_custom_button(__('Create Quotation'), function(){	
					frm.call('crt_quote').then(r=>{
						if(r.message){
							console.log(r.message)
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);

				
						}
				
											
						})
		
		
								})

							
		// }
	}
});
