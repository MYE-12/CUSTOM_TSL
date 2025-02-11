// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Resignation Form', {
	refresh(frm) {
	    frm.add_custom_button(__('F & F Statement'), function() {
	        frappe.db.get_value('Full and Final Settlement',{'employee': frm.doc.employee },'name')
				.then(r => {
				if(r.message && Object.entries(r.message).length === 0){
					frappe.route_options = { 'employee':frm.doc.employee,'employee_name': frm.doc.employee_name}
					frappe.set_route('Form','Full and Final Settlement','new-full-and-final-settlement-1')
					
				}
				else{
				frappe.set_route('Form','Full and Final Settlement',r.message.name)
				}
			})			
		}); 
	},
	validate(frm){
	    if(frm.doc.employee_name){
	        frm.set_value('session_user',frappe.session.user)
      }
	            
	},
	onload(frm){
	    if(frm.doc.workflow_state == 'Pending for HOD'){
			frm.set_value('hods_relieving_date',frappe.datetime.get_today())
		}
		if(frm.doc.workflow_state == 'Pending for HR'){
			frm.set_value('approved_relieving_date',frappe.datetime.get_today())
		}
	}
		
})