frappe.ui.form.on('Quotation', {
//	margin_rate:function(frm){
//		if(frm.doc.margin_rate){
//			var additional = frm.doc.margin_rate - frm.doc.overall_discount_amount
//			frm.doc.discount_amount = additional*-1
//			frm.doc.grand_total = frm.doc.grand_total + (frm.doc.discount_amount)
//		}
//	},
	onload_post_render:function(frm){
		if(frm.doc.docstatus == 0){
			frm.set_query("branch", function() {
                return {
                        filters: [
                                ["Warehouse","company", "=", frm.doc.company],
                                ["Warehouse","is_branch","=",1]
                        ]
                };
        });
        frm.fields_dict['items'].grid.get_field('item_code').get_query = function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var d = {};
			if(child.model){
				d['model'] = child.model;
			}
			if(child.manufacturer){
				d['mfg'] = child.manufacturer;
			}
			if(child.type){
				d['type'] = child.type;
			}
                        if(child.category){
				d['category_'] = child.category;
			}
                        if(child.sub_category){
				d['sub_category'] = child.sub_category;
			}
			return{
				filters: d
			}
		};

		}
		if(frm.doc.quotation_type == "Customer Quotation - Repair" && frm.doc.docstatus == 0){
			for(var i=0;i<frm.doc.quotation_history.length;i++){
				if(frm.doc.quotation_history[i].quotation_type == "Internal Quotation - Repair" && frm.doc.quotation_history[i].status == "Approved By Management" ){
					var doc_name = frm.doc.quotation_history[i].quotation_name
					break;
				}
			}
			if(doc_name){
				frappe.call({
					method: "tsl.custom_py.quotation.final_price_validate",
					args: {
						"source": doc_name,
					},
					callback: function(r) {
						if(r.message) {
							for(var i=0;i<frm.doc.items.length;i++){
								frm.doc.items[i].rate = r.message
								frm.doc.items[i].amount = frm.doc.items[i].qty*r.message
							}
							frm.refresh_field("items");

						}
					}
				});

			}


		}
		// if(frm.doc.quotation_type == "Internal Quotation - Supply" && frm.doc.docstatus == 0){
		// 	var d ={};
		// 	for(var i=0;i<frm.doc.items.length;i++){
		// 		if(frm.doc.items[i].supplier_quotation && frm.doc.items[i].item_code){
		// 		 d[frm.doc.items[i].item_code] = frm.doc.items[i].supplier_quotation
		// 		}
		// 	}
		// 	frappe.call({
		// 		method: "tsl.custom_py.quotation.get_itemwise_price",
		// 		args: {
		// 			"data":frm.doc.items
		// 		},
		// 		callback: function(r) {
		// 			if(r.message) {
		// 				for(var i=0;i<frm.doc.items.length;i++){
		// 					frm.doc.items[i].rate = r.message[i][0]
		// 					frm.doc.items[i].amount = r.message[i][1]
		// 					// frm.refresh_fields()
		// 				}
		// 				frm.refresh_fields();
		// 			}
					
		// 		}
		// 	});
			
			
			
		// }
        
    
        },
	default_discount_percentage(frm){
		if(frm.doc.is_multiple_quotation){
			var disc_val = (frm.doc.actual_price/100)*frm.doc.default_discount_percentage
			var disc = Math.ceil(frm.doc.actual_price - disc_val).toFixed(2)
			frm.set_value("after_discount_cost",disc)
			frm.set_value("default_discount_value",Math.floor(disc_val)).toFixed(2)
		}
		if(frm.doc.default_discount_percentage){
		var disc_val = (frm.doc.unit_rate_price/100)*frm.doc.default_discount_percentage
		var disc = Math.ceil(frm.doc.unit_rate_price - disc_val).toFixed(2)
		frm.set_value("after_discount_cost",disc)
		frm.set_value("default_discount_value",Math.floor(disc_val)).toFixed(2)
		
		}
		
		// else{
		// 	frm.set_value("after_discount_cost",'')
		// 	frm.set_value("default_discount_value",'')
		// }
		if(frm.doc.default_discount_percentage){
			frm.set_value("after_discount_cost",frm.doc.final_approved_price)

		}

	},
	final_approved_price(frm){
		if(frm.doc.final_approved_price){
			var add_val = (frm.doc.final_approved_price/100)*5
			var add_v = Math.ceil(add_val).toFixed(2)
			var ds = parseInt(add_v )+ frm.doc.final_approved_price
			frm.set_value("unit_rate_price",ds)
			

		}
		else{
			frm.set_value("unit_rate_price","")

		}
	},
	validate(frm){
		// cur_frm.clear_table('technician_hours_spent')

		if(frm.doc.is_multiple_quotation){
			$.each(frm.doc.items, function(i,v){
				if(v.margin_amount <= 0){
					frappe.throw({
						title: __('<b style = color:green>Alert</b>'),
						indicator: 'green',
						message: __('<center><b style=color:red>Note : Please Give the Suggested Price for each Work Order Line Item !!</b></center>')
					});

					// frappe.msgprint("Please Give the Suggested Price for each Work Order Line Item")
				}
			})
		}
		if(frm.doc.quotation_type != "Internal Quotation - Repair"){
			frm.set_value("letter_head",'TSL New')
			frappe.msgprint("Letter Head Placed Successufully")
		}
		else{
			frm.set_value("letter_head",'')

		}
	
		frm.refresh_field('technician_hours_spent')
		var amt = 0
		var sup_amt = 0
		$.each(frm.doc.item_price_details,function(i,v){
			if (v.item_source =="TSL Inventory"){
				amt += v.amount	
			} 
			else{
				sup_amt += v.amount
			}
		})
		if(frm.doc.item_price_details){
			cur_frm.clear_table("parts_price_list_");
			var child = cur_frm.add_child("parts_price_list_");
			var spc = frm.doc.shipping_cost
			child.tsl_inventory = Math.ceil(amt).toFixed(2),
			child.supplier = Math.ceil(sup_amt).toFixed(2),
			child.total_material_cost = Math.ceil(sup_amt + amt + spc).toFixed(2) || 0,
			cur_frm.refresh_fields("parts_price_list_");
		
		}
	},
    refresh:function(frm){
		// frm.add_custom_button(__('Customer Quotation'), function(){
			
		// 	frappe.call({
		// 		method: "tsl.custom_py.quotation.create_cust_qtn",
		// 		args: {
		// 			"source": frm.doc.name,
		// 			"type":"Customer Quotation - Repair"
		// 		},
		// 		callback: function(r) {
		// 			if(r.message) {
		// 				var doc = frappe.model.sync(r.message);
		// 				frappe.set_route("Form", doc[0].doctype, doc[0].name);


		// 			}
		// 		}
		// 	});


		// 			}, ('Create'))
		if(frm.doc.quotation_type == "Internal Quotation - Repair"){
		frm.add_custom_button(__('Customer Quotation'), function(){
				// let diff = frm.doc.final_approved_price - frm.doc.rounded_total
				// let inc_rate = diff / frm.doc.total_qty
				// $.each(frm.doc.items,function(i,v){
				// 	var mar = v.margin_amount
				// })
				// frappe.db.get_value('Quotation', frm.doc.items, 'margin_amount', (v) => {
				// 	var mar = v
					
				// });
                frappe.call({
					method: "tsl.custom_py.quotation.get_quotation_history",
					args: {
						"source": frm.doc.name,
						// "rate":inc_rate,
						"type":"Customer Quotation - Repair"
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
	if((frm.doc.quotation_type === "Internal Quotation - Repair" || frm.doc.quotation_type === "Internal Quotation - Supply") && !frm.doc.__islocal){

            frm.add_custom_button(__('Similar Unit Quoted Before'), function () {
				frappe.call({
					method: "tsl.custom_py.quotation.get_similar_unit_details",
					args: {
						"name":frm.doc.name
					},
					callback: function(r) {

					}
				});

            }, __("View"));
    }
	if(frm.doc.docstatus == 1 && frm.doc.workflow_state == "Approved By Customer"){
		frm.add_custom_button(__('Sales Invoice'), function(){

			frappe.call({
				method: "tsl.custom_py.quotation.create_sal_inv",
				args: {
					"source": frm.doc.name,
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
	if(frm.doc.docstatus == 1 && frm.doc.workflow_state == "Approved By Customer" && frm.doc.is_advance_pay == 1){
			frm.add_custom_button(__('Advance Payment'), function(){

				frappe.call({
					method: "tsl.custom_py.quotation.advance_pay",
					args: {
						"source": frm.doc.name,
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

		
	if(frm.doc.quotation_type === "Internal Quotation - Supply" && frm.doc.docstatus===1){
		frm.add_custom_button(__('Customer Quotation'), function(){
				
                frappe.call({
					method: "tsl.custom_py.quotation.get_quotation_history",
					args: {
						"source": frm.doc.name,
						"rate":null,
						"type":"Customer Quotation - Supply"
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
	
	if((frm.doc.quotation_type === "Customer Quotation - Repair" || frm.doc.quotation_type === "Revised Quotation - Repair") && frm.doc.workflow_state==="Rejected by Customer" ){ 
                frm.add_custom_button(__('Revised Quotation'), function(){
					frappe.call({
						method: "tsl.custom_py.quotation.get_quotation_history",
						args: {
							"source": frm.doc.name,
							"rate":null,
							
							"type":"Revised Quotation - Repair"
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
		if((frm.doc.quotation_type === "Customer Quotation - Supply" || frm.doc.quotation_type === "Revised Quotation - Supply") && frm.doc.workflow_state==="Rejected by Customer" ){ 
			frm.add_custom_button(__('Revised Quotation'), function(){
				frappe.call({
					method: "tsl.custom_py.quotation.get_quotation_history",
					args: {
						"source": frm.doc.name,
						"rate":null,
						
						"type":"Revised Quotation - Supply"
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
		if(frm.doc.quotation_type ==="Internal Quotation - Repair" && frm.doc.workflow_state==="Rejected"){
			frm.add_custom_button(__('Internal Quotation'), function(){
				// let diff = frm.doc.final_approved_price - frm.doc.rounded_total
				// let inc_rate = diff / frm.doc.total_qty
				frappe.call({
					method: "tsl.custom_py.quotation.get_quotation_history",
					args: {
						"source": frm.doc.name,
						"rate":null,
						
						"type":"Internal Quotation - Repair"
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
		if(frm.doc.quotation_type ==="Internal Quotation - Supply" && frm.doc.workflow_state==="Rejected"){
			frm.add_custom_button(__('Internal Quotation'), function(){
				// let diff = frm.doc.final_approved_price - frm.doc.rounded_total
				// let inc_rate = diff / frm.doc.total_qty
				frappe.call({
					method: "tsl.custom_py.quotation.get_quotation_history",
					args: {
						"source": frm.doc.name,
						"rate":null,
						"type":"Internal Quotation - Supply"
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
        if (frm.doc.docstatus===0 && frm.doc.quotation_type == "Internal Quotation - Repair") {
				frm.add_custom_button(__('Work Order Data'),
				function() {
					var from_date = frappe.datetime.add_months(frappe.datetime.get_today(), -1)
                			var to_date = frappe.datetime.get_today()
					new frappe.ui.form.MultiSelectDialog({
						doctype: "Work Order Data",
						target: frm,
						setters: {
							customer:frm.doc.party_name,
							wod_component:null
						},
						
						add_filters_group: 1,
						// get_query() {
						// 	return {
						// 		filters: { is_quotation_created: 0, docstatus:1,branch :frm.doc.branch_name, posting_date:["between",[from_date,to_date]]}
						// 	}
						// },
						action(selections) {
							frappe.call({
								method: "tsl.custom_py.quotation.get_wod_items",
								args: {
									"wod": selections
								},
								callback: function(r) {
									if(r.message) {
										cur_frm.doc.sales_rep = r.message[0]["sales_rep"];
										var tot_amt = 0;
										var tot_qty=0;
										for(var i=0;i<r.message.length;i++){
											var childTable = cur_frm.add_child("items");
											childTable.item_code = r.message[i]["item"],
											childTable.item_name = r.message[i]["item_name"],
											childTable.wod_no = r.message[i]["wod"],
											childTable.model_no = r.message[i]["model_no"],
											childTable.manufacturer = r.message[i]["manufacturer"],
											childTable.serial_no = r.message[i]["serial_no"],
											childTable.description = r.message[i]["description"],
											childTable.type = r.message[i]['type'],
											childTable.qty = r.message[i]["qty"]
											// childTable.rate = r.message[i]["total_amt"]
											// if(r.message[i]["total_amt"]){
											// 	var amt = r.message[i]["qty"] * r.message[i]["total_amt"];
											// 	childTable.amount = amt		
											// }										
											tot_qty += r.message[i]["qty"];
											cur_frm.refresh_fields("items");
										}
										frm.doc.total = tot_amt;
										frm.doc.total_qty = tot_qty;
										frm.doc.grand_total = tot_amt+frm.doc.total_taxes_and_charges;
										frm.doc.rounded_total = frm.doc.grand_total;
										// frm.doc.actual_price = frm.doc.rounded_total;
										// if(frm.doc.technician_hours_spent.length > 0 && frm.doc.technician_hours_spent[0].total_price){
										// 	frm.doc.actual_price = frm.doc.rounded_total + frm.doc.technician_hours_spent[0].total_price;
										// }
										// frm.doc.final_approved_price = frm.doc.actual_price;
										cur_frm.refresh_fields();

									}
								}
							});
							cur_dialog.hide();
						}

					});
				}, __("Get Items From"), "btn-default");
		}
		if (frm.doc.docstatus===0 && frm.doc.quotation_type == "Customer Quotation - Repair") {
			frm.add_custom_button(__('Approved Internal'),
			function() {
				var from_date = frappe.datetime.add_months(frappe.datetime.get_today(), -1)
						var to_date = frappe.datetime.get_today()
				new frappe.ui.form.MultiSelectDialog({
					doctype: "Quotation",
					target: frm,
					setters: {
						party_name:frm.doc.party_name,
						workflow_state:'Approved By Management'
					},
					
					add_filters_group: 1,
					// get_query() {
					// 	return {
					// 		filters: { is_quotation_created: 0, docstatus:0,branch :frm.doc.branch_name, posting_date:["between",[from_date,to_date]]}
					// 	}
					// },
					action(selections) {
						frappe.call({
							method: "tsl.custom_py.quotation.get_qtn_items",
							args: {
								"qtn": selections
							},
							callback: function(r) {
								if(r.message) {
									cur_frm.doc.sales_rep = r.message[0]["sales_rep"];
									var tot_amt = 0;
									var tot_qty=0;
									var sa=0
									var ur=0
									var urv=0
									$.each(r.message,function(i,s){
										var childTable = cur_frm.add_child("items");
										childTable.item_code = s.item,
										childTable.item_name = s.item_name,
										childTable.wod_no = s.wod_no
										childTable.model_no = s.model_no,
										childTable.manufacturer =s.manufacturer,
										childTable.serial_no = s.serial_no,
										childTable.description = s.description,
										childTable.type = s.type,
										childTable.qty = s.qty,
										childTable.margin_amount = s.margin_amount,
										childTable.margin_amount_value = s.margin_amount_value,
										childTable.unit_price = s.unit_price,							
										tot_qty += s.qty,
										cur_frm.refresh_fields("items");
										sa += s.margin_amount;	
										ur += s.unit_price;
										urv += s.margin_amount_value;
										console.log(sa)
									})
									// for(var i=0;i<r.message.length;i++){
									// 	var childTable = cur_frm.add_child("items");
									// 	childTable.item_code = r.message[i]["item"],
									// 	childTable.item_name = r.message[i]["item_name"],
									// 	childTable.wod_no = r.message[i]["wod_no"],
									// 	childTable.model_no = r.message[i]["model_no"],
									// 	childTable.manufacturer = r.message[i]["manufacturer"],
									// 	childTable.serial_no = r.message[i]["serial_no"],
									// 	childTable.description = r.message[i]["description"],
									// 	childTable.type = r.message[i]['type'],
									// 	childTable.qty = r.message[i]["qty"]
									// 	childTable.margin_amount = r.message[i]["margin_amount"]
									// 	childTable.margin_amount_value = r.message[i]["margin_amount_value"]
									// 	childTable.unit_price = r.message[i]["unit_price"]									
									// 	tot_qty += r.message[i]["qty"];
									// 	cur_frm.refresh_fields("items");
									// 	frm.doc.actual_price += r.message[i]["margin_amount"];

									// }
									frm.doc.after_discount_cost = sa;
									frm.doc.unit_rate_price = ur;
									frm.doc.default_discount_value = urv;
									// frm.doc.grand_total = tot_amt+frm.doc.total_taxes_and_charges;
									// frm.doc.rounded_total = frm.doc.grand_total;
									cur_frm.refresh_fields();

								}
							}
						});
						cur_dialog.hide();
					}

				});
			}, __("Get Items From"), "btn-default");
	}
		if (frm.doc.docstatus===0 && frm.doc.quotation_type == "Internal Quotation - Supply") {
			frm.add_custom_button(__('Supply Order Data'),
				function() {
					new frappe.ui.form.MultiSelectDialog({
						doctype: "Supply Order Data",
						target: frm,
						setters: {
							customer:frm.doc.party_name,
						},
						add_filters_group: 1,
						get_query() {
							return {
								filters: {is_quotation_created:0 ,docstatus:1 , branch :frm.doc.branch_name }
							}
						},
						action(selections) {
							frappe.call({
								method: "tsl.custom_py.quotation.get_sqtn_items",
								args: {
									"sod": selections
								},
								callback: function(r) {
									if(r.message) {
										
										cur_frm.clear_table("items");
										var tot_amt = 0;
										var tot_qty=0;
										for(var i=0;i<r.message.length;i++){
											
											var childTable = cur_frm.add_child("items");
											childTable.item_code = r.message[i]["item_code"],
											childTable.item_name = r.message[i]["item_name"],
											childTable.supply_order_data = r.message[i]["sod"],
											childTable.supplier_quotation = r.message[i]['sqtn'],
											childTable.model_no = r.message[i]["model_no"],
											childTable.serial_no = r.message[i]["serial_no"],
											childTable.description = r.message[i]["item_name"],
											childTable.uom = r.message[i]['uom'],
											childTable.stock_uom = r.message[i]['stock_uom'],
											childTable.conversion_factor = r.message[i]['conversion_factor'],
											childTable.type = r.message[i]['type'],
											childTable.qty = r.message[i]["qty"],
											childTable.rate = r.message[i]["rate"]
											childTable.amount = r.message[i]['amount'],
											tot_amt += r.message[i]['amount'];
											tot_qty += r.message[i]["qty"];
											cur_frm.refresh_fields("items");
										}
										frm.doc.total = tot_amt;
										frm.doc.total_qty = tot_qty;
										frm.doc.grand_total = tot_amt+frm.doc.total_taxes_and_charges;
										// frm.doc.rounded_total = frm.doc.grand_total;
										// frm.doc.actual_price = frm.doc.rounded_total;
										// if(frm.doc.technician_hours_spent.length > 0 && frm.doc.technician_hours_spent[0].value){
										// 	frm.doc.actual_price = frm.doc.rounded_total +(frm.doc.technician_hours_spent[0].value*frm.doc.technician_hours_spent[0].total_hours_spent);
										// }
										
										// frm.doc.final_approved_price = (frm.doc.actual_price*(302.8/100))+frm.doc.actual_price;
										cur_frm.refresh_fields();

									}
								}
							});
							cur_dialog.hide();
						}

					});
				}, __("Get Items From"), "btn-default");
		}
		if(frm.doc.docstatus === 0 && frm.doc.quotation_type){
			frm.trigger("branch_name")
			

		}

		// if(frm.doc.edit_final_approved_price){ 
		// 	frm.set_df_property("final_approved_price", "read_only", 0)
		// }
		// else{ 
		// 	frm.set_df_property("final_approved_price", "read_only", 1)
		// }
		if(frm.doc.quotation_type != "Internal Quotation - Repair" && frm.doc.workflow_state == "Approved By Customer" && !frm.doc.type_of_approval){
			
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
						label: "Attach",
						fieldname: "attach",
						fieldtype: "Attach",
						
						
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
					frm.set_value("approval_date",data.approval_date);
					d.hide();
					
				},
				primary_action_label: __('Submit')
			});
			d.show();
			
	  }

    },
	is_advance_pay:function(frm){
		frm.save_or_update();
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
				"Internal Quotation - Repair":{"Kuwait - TSL":"REP-QTN-INT-K.YY.-","Dammam - TSL-SA":"REP-QTN-INT-D.YY.-","Riyadh - TSL-SA":"REP-QTN-INT-R.YY.-","Jeddah - TSL-SA":"REP-QTN-INT-J.YY.-"},
				"Customer Quotation - Repair":{"Kuwait - TSL":"REP-QTN-CUS-K.YY.-","Dammam - TSL-SA":"REP-QTN-CUS-D.YY.-","Riyadh - TSL-SA":"REP-QTN-CUS-R.YY.-","Jeddah - TSL-SA":"REP-QTN-CUS-J.YY.-"},
				"Revised Quotation - Repair":{"Kuwait - TSL":"REP-QTN-REV-K.YY.-","Dammam - TSL-SA":"REP-QTN-REV-D.YY.-","Riyadh - TSL-SA":"REP-QTN-REV-R.YY.-","Jeddah - TSL-SA":"REP-QTN-REV-J.YY.-"},
				"Internal Quotation - Supply":{"Kuwait - TSL":"SUP-QTN-INT-K.YY.-","Dammam - TSL-SA":"SUP-QTN-INT-D.YY.-","Riyadh - TSL-SA":"SUP-QTN-INT-R.YY.-","Jeddah - TSL-SA":"SUP-QTN-INT-J.YY.-"},
				"Customer Quotation - Supply":{"Kuwait - TSL":"SUP-QTN-CUS-K.YY.-","Dammam - TSL-SA":"SUP-QTN-CUS-D.YY.-","Riyadh - TSL-SA":"SUP-QTN-CUS-R.YY.-","Jeddah - TSL-SA":"SUP-QTN-CUS-J.YY.-"},
				"Revised Quotation - Supply":{"Kuwait - TSL":"SUP-QTN-REV-K.YY.-","Dammam - TSL-SA":"SUP-QTN-REV-D.YY.-","Riyadh - TSL-SA":"SUP-QTN-REV-R.YY.-","Jeddah - TSL-SA":"SUP-QTN-REV-J.YY.-"},
				"Site Visit Quotation":{"Kuwait - TSL":"SV-QTN-K.YY.-","Dammam - TSL-SA":"SV-QTN-D.YY.-","Riyadh - TSL-SA":"SV-QTN-R.YY.-","Jeddah - TSL-SA":"SV-QTN-J.YY.-"},
				}
				frm.set_value("naming_series",d[frm.doc.quotation_type][frm.doc.branch_name])
		

		}
	},
	quotation_type:function(frm){
		frm.trigger("branch_name");
	},
	is_internal_quotation:function(frm){
		if(frm.doc.is_internal_quotation){
			frm.doc.quotation_type = "Internal Quotation - Repair"
			cur_frm.set_df_property("quotation_type","read_only",1)

		}
		else{
			cur_frm.set_df_property("quotation_type","read_only",0)
		}
		
	},
	overall_discount_amount:function(frm){
//		if(frm.doc.overall_discount_amount){
//			frm.doc.discount_amount = frm.doc.overall_discount_amount
//			if(frm.doc.margin_rate){
//				frm.doc.discount_amount = frm.doc.discount_amount - frm.doc.margin_rate
//			}
//			var total = frm.doc.total-(frm.doc.discount_amount)
//			frm.doc.grand_total = total
//			if(frm.doc.technician_hours_spent.length > 0 ){
//				total += frm.doc.technician_hours_spent[0].total_price
//			} 
//			frm.doc.actual_price = total
		if(in_list(["Internal Quotation - Repair","Revised Quotation - Repair"],frm.doc.quotation_type)){
			// frm.doc.final_approved_price = frm.doc.actual_price;
			// frm.doc.final_approved_price = frm.doc.final_approved_price - frm.doc.overall_discount_amount
			// frm.doc.final_approved_price = frm.doc.margin_rate
			frm.refresh_fields()
		}
		else if(in_list(["Customer Quotation - Repair"],frm.doc.quotation_type)){ 
			// frm.doc.discount_amount = frm.doc.overall_discount_amount
			// frm.doc.grand_total = frm.doc.total

			frm.doc.after_discount_cost = frm.doc.after_discount_cost - frm.doc.overall_discount_amount
			frm.refresh_fields()
                }
//		}
	},
	margin_rate:function(frm){
		frm.trigger("overall_discount_amount")
	},
	discount_percent:function(frm){
		if(in_list(["Internal Quotation - Repair","Revised Quotation - Repair"],frm.doc.quotation_type)){
			frm.doc.overall_discount_amount = (frm.doc.actual_price * frm.doc.discount_percent)/100
			frm.trigger("overall_discount_amount")
		}
		else if(in_list(["Customer Quotation - Repair"],frm.doc.quotation_type)){
			frm.doc.overall_discount_amount = (frm.doc.after_discount_cost * frm.doc.discount_percent)/100
			frm.trigger("overall_discount_amount")
		}
	}

});



frappe.ui.form.on("Quotation Item",{ 
	
	   qty : function(frm,cdt,cdn){
			var item = locals[cdt][cdn];
			if(item.qty){
				item.amount = item.qty * item.rate;
				item.final_approved_price = item.amount;
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
				frm.doc.actual_price = frm.doc.rounded_total;
				if(frm.doc.technician_hours_spent.length > 0 && frm.doc.technician_hours_spent[0].value){
//					frm.doc.actual_price = frm.doc.rounded_total +(frm.doc.technician_hours_spent[0].value *frm.doc.technician_hours_spent[0].total_hours_spent);

				}
				var act = frm.doc.actual_price
				frm.set_value("final_approved_price",act);
				cur_frm.refresh_fields();

				
			}
		   
	   },
	   margin_amount:function(frm,cdt,cdn){
		var item = locals[cdt][cdn];
		var margin_amount = item.margin_amount

		var disc_per = 5
		var disc_val = (margin_amount/100)*disc_per
		frappe.model.set_value(cdt, cdn, "margin_amount_value",disc_val);
		var dic_val = item.margin_amount_value + margin_amount
		frappe.model.set_value(cdt, cdn, "unit_price",dic_val);

		// item.margin_amount_value = disc_val
		
	   },
	   rate:function(frm,cdt,cdn){
		   frm.script_manager.trigger("qty",cdt,cdn);
	   }
		
	});
frappe.ui.form.on("Technician Hours Spent",{ 
	value:function(frm,cdt,cdn){
		var item = locals[cdt][cdn];
		if(item.value && item.total_hours_spent){
			item.total_price = item.value * item.total_hours_spent;
			var tot_amt =  item.value * item.total_hours_spent;
			// for(var i=0 ;i< frm.doc.technician_hours_spent.length;i++){
			// 	tot_amt += (frm.doc.technician_hours_spent[i]["value"] * frm.doc.technician_hours_spent[i]["total_hours_spent"]);
			// }
			
			frm.doc.actual_price = tot_amt +frm.doc.rounded_total;
			frm.doc.final_approved_price = frm.doc.actual_price;
			cur_frm.refresh_fields();

		
	}
	},
	total_hours_spent:function(frm,cdt,cdn){
		frm.script_manager.trigger("value",cdt,cdn);
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
			frm.set_query("department", function() {
				return {
					filters: [
						["Cost Center","company", "=", frm.doc.company],
						
					]
				}
			});
		}
	});
	// frappe.ui.form.on('Sales Invoice', {
	// 	setup: function(frm) {
	// 		frm.set_query("branch", function() {
	// 			return {
	// 				filters: [
	// 					["Warehouse","company", "=", frm.doc.company],
	// 					["Warehouse","is_branch","=",1]
						
	// 				]
	// 			};
	// 		});
	// 		frm.fields_dict['items'].grid.get_field('item_code').get_query = function(frm, cdt, cdn) {
	// 		var child = locals[cdt][cdn];
	// 		return{
	// 			filters: {
	// 				'model': child.model,
	// 				'manufacturer':child.manufacturer,
	// 				'type':child.type,
	// 				'serial_no':child.serial_number
	// 			}
	// 		};
	// 	};
	// 	}
	// });
