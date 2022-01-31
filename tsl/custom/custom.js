frappe.ui.form.on('Quotation', {

	
    refresh:function(frm){
		
		if(frm.doc.quotation_type === "Internal Quotation" && frm.doc.docstatus===1){
		frm.add_custom_button(__('Customer Quotation'), function(){
				let diff = frm.doc.final_approved_price - frm.doc.rounded_total
				let inc_rate = diff / frm.doc.total_qty
                frappe.call({
					method: "tsl.custom_py.quotation.get_quotation_history",
					args: {
						"source": frm.doc.name,
						
						"rate":inc_rate,
						"type":"Customer Quotation"
					},
					callback: function(r) {
						if(r.message) {
							var doc = frappe.model.sync(r.message);
							// doc[0].similar_items_quoted_before = [];
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
							
						}
					}
				});
				
				
                               
                        }, ('Create'))
	}
	if(frm.doc.docstatus === 0 && frm.doc.party_name){
		frm.refresh_field("customer_name");

	}
	if((frm.doc.quotation_type === "Customer Quotation" || frm.doc.quotation_type === "Revised Quotation") && frm.doc.workflow_state==="Rejected by Customer" ){ 
                frm.add_custom_button(__('Revised Quotation'), function(){
					frappe.call({
						method: "tsl.custom_py.quotation.get_quotation_history",
						args: {
							"source": frm.doc.name,
							"rate":null,
							
							"type":"Revised Quotation"
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
		if(frm.doc.quotation_type ==="Internal Quotation" && frm.doc.workflow_state==="Rejected"){
			frm.add_custom_button(__('Internal Quotation'), function(){
				let diff = frm.doc.final_approved_price - frm.doc.rounded_total
				let inc_rate = diff / frm.doc.total_qty
				frappe.call({
					method: "tsl.custom_py.quotation.get_quotation_history",
					args: {
						"source": frm.doc.name,
						"rate":inc_rate,
						
						"type":"Internal Quotation"
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
		// if(frm.doc.docstatus===0 && frm.doc.actual_price && frm.doc.workflow_state=="Waiting For Approval"){
		// 	var act = (frm.doc.actual_price*(302.8/100))+ frm.doc.actual_price
		// 	frm.set_value("final_approved_price",act);
		//  	frm.refresh_fields();

		// }
        if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Work Order Data'),
				function() {
					new frappe.ui.form.MultiSelectDialog({
						doctype: "Work Order Data",
						target: frm,
						setters: {
							customer:frm.doc.customer_name,
						},
						add_filters_group: 1,
						// date_field: "transaction_date",
						get_query() {
							return {
								filters: { is_quotation_created: 0, docstatus:1,branch :frm.doc.branch_name }
							}
						},
						action(selections) {
							frappe.call({
								method: "tsl.custom_py.quotation.get_wod_items",
								args: {
									"wod": selections
								},
								callback: function(r) {
									if(r.message) {
										cur_frm.clear_table("items");
										cur_frm.doc.sales_rep = r.message[0]["sales_rep"];
										var tot_amt = 0;
										var tot_qty=0;
										for(var i=0;i<r.message.length;i++){
											
											var childTable = cur_frm.add_child("items");
											childTable.item_code = r.message[i]["item"],
											childTable.item_name = r.message[i]["item_name"],
											childTable.wod_no = r.message[i]["wod"],
											childTable.model_no = r.message[i]["model_no"],
											childTable.serial_no = r.message[i]["serial_no"],
											childTable.description = r.message[i]["type"],
											childTable.qty = r.message[i]["qty"],
											childTable.rate = r.message[i]["total_amt"]
											var amt = r.message[i]["qty"] * r.message[i]["total_amt"];
											childTable.amount = amt,
											childTable.final_approved_price = (amt*(302.8/100))+amt,
											tot_amt += amt;
											tot_qty += r.message[i]["qty"];
											cur_frm.refresh_fields("items");
										}
										frm.doc.total = tot_amt;
										frm.doc.total_qty = tot_qty;
										frm.doc.grand_total = tot_amt+frm.doc.total_taxes_and_charges;
										frm.doc.rounded_total = frm.doc.grand_total;
										if(frm.doc.technician_hours_spent){
											frm.doc.actual_price = frm.doc.rounded_total +frm.doc.technician_hours_spent[0].value;

										}
										else{
											frm.doc.actual_price = frm.doc.rounded_total;
										}
										frm.doc.final_approved_price = (frm.doc.actual_price*(302.8/100))+frm.doc.actual_price;
										cur_frm.refresh_fields();

									}
								}
							});
							cur_dialog.hide();
						}

					});
				}, __("Get Items From"), "btn-default");
		}
		// if(frm.doc.party_name && frm.doc.docstatus===0 ){
        //     frm.doc.customer_name = frm.doc.party_name
		// 	frm.refresh_fields()
        // }
		if(frm.doc.docstatus === 0 && frm.doc.quotation_type){
			frm.trigger("branch_name")
			

		}

		// if(frm.doc.quotation_type && frm.doc.docstatus===0 ){
        //     frm.trigger("quotation_type");
        // }
		if(frm.doc.edit_final_approved_price){ 
			frm.set_df_property("final_approved_price", "read_only", 0)
		}
		else{ 
			frm.set_df_property("final_approved_price", "read_only", 1)
		}
		if(frm.doc.quotation_type != "Internal Quotation" && frm.doc.workflow_state == "Approved By Customer" && !frm.doc.type_of_approval){
			
			var d = new frappe.ui.Dialog({
				
				fields: [
					{
						label: 'Type Of Approval',
						fieldname: 'type_of_approval',
						fieldtype: 'Select',
						options:["Email","Phone Call","PO","Others"],
						change: () => {
							let template_type = d.get_value('type_of_approval');
	
							if (template_type === "Others") {
								d.set_df_property('specify', 'hidden',0);
								d.set_df_property('po_no', 'hidden',1);
								d.set_df_property('po_date', 'hidden',1);
							} 
							if (template_type === "PO") {
								d.set_df_property('po_no', 'hidden',0);
								d.set_df_property('po_date', 'hidden',0);
								d.set_df_property('specify', 'hidden',1);
							}
							if (template_type === "Email") {
								d.set_df_property('specify', 'hidden',1);
								d.set_df_property('po_no', 'hidden',1);
								d.set_df_property('po_date', 'hidden',1);
							}
							if (template_type === "Phone Call") {
								d.set_df_property('specify', 'hidden',1);
								d.set_df_property('po_no', 'hidden',1);
								d.set_df_property('po_date', 'hidden',1);
							}   
							
						}
					},
					{
						label: "Specify",
						fieldname: "specify",
						fieldtype: "Data",
						hidden:1,
						
					},
					{
						label: "PO No",
						fieldname: "po_no",
						fieldtype: "Data",
						hidden:1,
						
					},
					{
						label: "PO Date",
						fieldname: "po_date",
						fieldtype: "Date",
						hidden:1,
						
					},
					{
						label: "Approval Date",
						fieldname: "approval_date",
						fieldtype: "Date",
						
						
					},
				],
				primary_action: function() {
					var data = d.get_values();
					frm.set_value("type_of_approval",data.type_of_approval)
					
					
					if(data.type_of_approval == "Others"){
						frm.set_value("specify",data.specify)
					}
					if(data.type_of_approval == "PO"){
						frm.set_value("purchase_order_no",data.po_no);
						frm.set_value("purchase_order_date", data.po_date);
					}
					
					// cur_frm.refresh_fields();
					frm.set_value("approval_date",data.approval_date)
					d.hide();
					
				},
				primary_action_label: __('Submit')
			});
			d.show();
			
	  }

    },
    edit_final_approved_price:function(frm){
        if(frm.doc.edit_final_approved_price){
            frm.set_df_property("final_approved_price", "read_only", 0)
        }
        else{
            frm.set_df_property("final_approved_price", "read_only", 1)
        }
    },
	approval_date:function(frm){
		frm.save_or_update();
	},
	branch_name:function(frm){
		if(frm.doc.quotation_type && frm.doc.branch_name){
			var d = {
				"Internal Quotation":{"Kuwait - TSL":"QTN-INT-K.YY.-","Dammam - TSL-SA":"QTN-INT-D.YY.-","Riyadh - TSL-SA":"QTN-INT-R.YY.-","Jeddah - TSL-SA":"QTN-INT-J.YY.-"},
				"Customer Quotation":{"Kuwait - TSL":"QTN-CUS-K.YY.-","Dammam - TSL-SA":"QTN-CUS-D.YY.-","Riyadh - TSL-SA":"QTN-CUS-R.YY.-","Jeddah - TSL-SA":"QTN-CUS-J.YY.-"},
				"Revised Quotation":{"Kuwait - TSL":"QTN-REV-K.YY.-","Dammam - TSL-SA":"QTN-REV-D.YY.-","Riyadh - TSL-SA":"QTN-REV-R.YY.-","Jeddah - TSL-SA":"QTN-REV-J.YY.-"}
					
				}
				frm.set_value("naming_series",d[frm.doc.quotation_type][frm.doc.branch_name])
		

		}
	},
	quotation_type:function(frm){
		frm.trigger("branch_name");
	},
	is_internal_quotation:function(frm){
		frm.doc.quotation_type = "Internal Quotation"
		cur_frm.set_df_property("quotation_type","read_only",1)
	}
			
});



frappe.ui.form.on("Quotation Item",{ 
	
	   qty : function(frm,cdt,cdn){
			var item = locals[cdt][cdn];
			if(item.qty){
				item.amount = item.qty * item.rate;
				item.final_approved_price = (item.amount *(302.8/100))+item.amount;
				var tot_amt = 0;
				var tot_qty=0;
				for(var i=0 ;i< frm.doc.items.length;i++){
					tot_amt += frm.doc.items[i]["amount"];
					tot_qty += frm.doc.items[i]["qty"];

				}
				frm.doc.total = tot_amt;
				frm.doc.total_qty = tot_qty;
				frm.doc.grand_total = tot_amt+frm.doc.total_taxes_and_charges;
				frm.doc.rounded_total = frm.doc.grand_total;
				if(frm.doc.technician_hours_spent){
					frm.doc.actual_price = frm.doc.rounded_total +frm.doc.technician_hours_spent[0].value;

				}
				else{
					frm.doc.actual_price = frm.doc.rounded_total;
				}
				var act = (frm.doc.actual_price*(302.8/100))+ frm.doc.actual_price
				frm.set_value("final_approved_price",act);
				cur_frm.refresh_fields();

				
			}
		   
	   },
	   rate:function(frm,cdt,cdn){
		   frm.script_manager.trigger("qty",cdt,cdn);
	   }
		
	});
frappe.ui.form.on("Technician Hours Spent",{ 
	value:function(frm,cdt,cdn){
		var item = locals[cdt][cdn];
		if(item.value){
			var tot_amt = 0;
			for(var i=0 ;i< frm.doc.technician_hours_spent.length;i++){
				tot_amt += frm.doc.technician_hours_spent[i]["value"];
			}
			frm.doc.actual_price = tot_amt +frm.doc.rounded_total;
			frm.doc.final_approved_price = (frm.doc.actual_price*(302.8/100))+frm.doc.actual_price;
			cur_frm.refresh_fields();

		
	}

	}
	

});
frappe.ui.form.on('Quotation', {
		setup: function(frm) {
			frm.set_query("branch_name", function() {
				return {
					filters: [
						["Warehouse","company", "=", frm.doc.company],
						["Warehouse","is_branch","=",1]
						
					]
				}
			});
		}
	});
