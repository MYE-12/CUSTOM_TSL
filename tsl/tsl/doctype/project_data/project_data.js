// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Data', {
	refresh: function(frm) {
		if(frm.doc.status == "A-Approved"){
			frm.add_custom_button(__('Create'), function(){
					
				
				frm.call('crt_wo').then(r=>{
					if(r.message){
						console.log(r.message)
			
					}
			
										
					})
	
	
							})
			}

			if(frm.doc.status != "A-Approved"){
				frm.add_custom_button(__('Create Quotation'), function(){	
					frm.call('crt_quote').then(r=>{
						if(r.message){
							console.log(r.message)
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);

				
						}
				
											
						})
		
		
								})

				
							
		}

		if(frm.doc.status != "Parts Priced"){
			frm.add_custom_button(__('Request for Quotation'), function(){	
				frm.call('rfq').then(r=>{
					if(r.message){
						console.log(r.message)
						var doc = frappe.model.sync(r.message);
						frappe.set_route("Form", doc[0].doctype, doc[0].name);
	
			
					}
			
										
					})
	
							})
		}

	
	}
});
