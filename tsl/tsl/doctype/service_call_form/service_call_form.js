// Copyright (c) 2022, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Call Form', {
	refresh: function(frm) {
		if(frm.doc.docstatus===1){
			frm.add_custom_button(__('Internal Quotation'), function(){
					frappe.call({
						method: "tsl.tsl.doctype.service_call_form.service_call_form.create_qtn",
						args: {
							"source":frm.doc.name
						},
						callback: function(r) {
							if(r.message) {
								var doc = frappe.model.sync(r.message);
								frappe.set_route("Form", doc[0].doctype, doc[0].name);
								
							}
						}
					});
									   
			}, ('Create'))

		}
		if(frm.doc.docstatus===1){
			frm.add_custom_button(__('Sales Invoice'), function(){
					frappe.call({
						method: "tsl.tsl.doctype.service_call_form.service_call_form.create_sal_inv",
						args: {
							"source":frm.doc.name
						},
						callback: function(r) {
							if(r.message) {
								var doc = frappe.model.sync(r.message);
								frappe.set_route("Form", doc[0].doctype, doc[0].name);
								
							}
						}
					});
					
					
								   
			}, ('Create'))
			
		}

	},
	related_doc:function(frm){
		if(frm.doc.related_doc){
			var data= frm.doc.related_doc
			var doc_type = frm.doc.document_type
			var customer = frappe.db.get_value(doc_type,{"name":data},"customer",(r) =>{
				if(r.customer){
					frm.set_value("customer",r.customer);
				}
				else{
					frm.set_value("customer","");	
				}
			})
			var branch = frappe.db.get_value(doc_type,{"name":data},"branch",(r) =>{
				if (r.branch){
					frm.set_value("branch",r.branch);	
				}
				else{
					frm.set_value("branch","");	
				}
			})
			var department = frappe.db.get_value(doc_type,{"name":data},"department",(r) =>{
				if(r.department){
					frm.set_value("department",r.department);	
				}
				else{
					frm.set_value("department","");	
				}
			})
			var sales_rep = frappe.db.get_value(doc_type,{"name":data},"sales_rep",(r) =>{
				if(r.sales_rep){
					frm.set_value("salesman_name",r.sales_rep);	
				}
				else{
					frm.set_value("salesman_name","");	
				}
			})
			var technician = frappe.db.get_value(doc_type,{"name":data},"technician",(r) =>{
				if(r.technician){
					frm.set_value("technician_name",r.technician);	
				}
				else{
					frm.set_value("technician_name","");	
				}
			})
			}
	},
	sch_date:function(frm){

		var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
		var now = new Date(frm.doc.sch_date);
		var day = days[ now.getDay() ];
		frm.set_value("day",day);
	}
});
frappe.ui.form.on('Service Call Form', {
	setup: function(frm) {
		// frm.set_query("branch", function() {
		// 	return {
		// 		filters: [
		// 			["Warehouse","company", "=", frm.doc.company],
		// 			["Warehouse","is_branch","=",1]
					
		// 		]
		// 	}
		// });
	}
});
