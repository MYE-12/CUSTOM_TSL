// Copyright (c) 2021, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order Data', {
	onload_post_render:function(frm){
		if(frm.doc.material_list[0].item_code){
                                var item = $(".static-area.ellipsis")[6].outerText
                                var item = item.split(":")[0]
                                $(".static-area.ellipsis")[6].outerText = item;
                                frm.refresh_field("material_list")
                }
	},
	delivery:function(frm){
		if(frm.doc.delivery){
		frm.set_value("status",'CT-Customer Testing');
		frm.refresh_field('status')
		}
	},
	onload(frm){
		if(!frappe.user.has_role("Administrator") && !frappe.user.has_role("Lab Coordinator" ) && !frappe.user.has_role("Procurement" ) && !frappe.user.has_role("Admin")){
			frm.set_df_property("technician","read_only",1)
			frm.set_df_property("status","read_only",1)
			frm.set_df_property("advance_payment_amount","hidden",1)
		}
		if(!frappe.user.has_role("Lab Coordinator")){
			frm.set_df_property("mistaken_ner","hidden",1)
			
		}

		
	},
	refresh: function(frm) {
		
		// if(frm.doc.docstatus === 1) {
		// 	frm.add_custom_button(__("Part Sheet"), function(){
		// 		frappe.call({
		// 			method: "tsl.tsl.doctype.work_order_data.work_order_data.create_part_sheet",
		// 			args: {
		// 				"work_order": frm.doc.name
		// 			},
		// 			callback: function(r) {
		// 				if(r.message) {
		// 					var doc = frappe.model.sync(r.message);
		// 					frappe.set_route("Form", doc[0].doctype, doc[0].name);
		// 				}
		// 			}
		// 		});
		// 	},__('Create'));
		// }
		if(frm.doc.material_list[0].item_code){
                		var item = $(".static-area.ellipsis")[6].outerText
        			var item = item.split(":")[0]
       		 		$(".static-area.ellipsis")[6].outerText = item;
        			frm.refresh_field("material_list")
	        }

		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Evaluation Report"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_evaluation_report",
					args: {
						"doc_no": frm.doc.name
					},
					callback: function(r) {
						if(r.message) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
						}
					}
				});
			},__('Create'));
		}
		  if(frm.doc.docstatus == 1) {
            // if(!frappe.user.has_role("Technician")){
				frm.add_custom_button(__("Initial Evaluation"), function(){
					frappe.call({
							method: "tsl.tsl.doctype.work_order_data.work_order_data.create_test_evaluation_report",
							args: {
									"doc_no": frm.doc.name
							},
							callback: function(r) {
									if(r.message) {
											var doc = frappe.model.sync(r.message);
											frappe.set_route("Form", doc[0].doctype, doc[0].name);
									}
							}
					});
			},__('Create'));
			// }
                }
		if(frm.doc.docstatus == 1) {
		if(!frappe.user.has_role("Technician") || frappe.user.has_role("Administrator")){
			frm.add_custom_button(__("Internal Quotation"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_quotation",
					args: {
						"wod": frm.doc.name
					},
					callback: function(r) {

						if(r.message) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
							
						}
					}

				});

			},__('Create'));
}
		}
		if(frm.doc.docstatus == 1) {
		if (!frappe.user.has_role ("Admin") && ! frappe.user.has_role ("Technician")){
			frm.add_custom_button(__("Stock Transfer"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_stock_entry",
					args: {
						"wod": frm.doc.name
					},
					callback: function(r) {
						if(r.message) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
							
						}
					}
				});
			},__('Create'));
}
		}

		if(frm.doc.docstatus == 1) {
		// if(! frappe.user.has_role("Technician")){
			if(frm.doc.company != "TSL COMPANY - KSA") {
				frm.add_custom_button(__("Sales Invoice"), function(){
					frappe.call({
						method: "tsl.tsl.doctype.work_order_data.work_order_data.create_sal_inv",
						args: {
							"wod": frm.doc.name
						},
						callback: function(r) {
							console.log(r.message)
							if(r.message) {
								// $.each(r.message,function(i,v){
								// 	console.log(v.name)
								// })
								var doc = frappe.model.sync(r.message);
								frappe.set_route("Form", doc[0].doctype, doc[0].name);
								
								
							}
						}
					});
				},__('Create'));
			}
			
		// }
}

if(frm.doc.docstatus == 1) {
	// if(! frappe.user.has_role("Technician")){
		if(frm.doc.company != "TSL COMPANY - KSA") {
			frm.add_custom_button(__("Invoice Request"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_sal_inv",
					args: {
						"wod": frm.doc.name
					},
					callback: function(r) {
						console.log(r.message)
						if(r.message) {
							// $.each(r.message,function(i,v){
							// 	console.log(v.name)
							// })
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
							
							
						}
					}
				});
			},__('Create'));
		}
		
	// }
}
		if(frm.doc.docstatus === 1) {
		if(! frappe.user.has_role("Technician") || frappe.user.has_role("Administrator")){
			frm.add_custom_button(__("Delivery Note"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_dn",
					args: {
						"wod": frm.doc.name
					},
					callback: function(r) {
						if(r.message) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
							
							
						}
					}
				});
			},__('Create'));
		}
}
		if(frm.doc.docstatus == 1 && (frm.doc.status == "RNR-Return Not Repaired" || frm.doc.status == "RNRC-Return Not Repaired Client" ||frm.doc.status == "RNF-Return No Fault" ||frm.doc.status == "RNA-Return Not Approved"|| frm.doc.status == "RNP-Return No Parts" || frm.doc.status == "C-Comparison")){
			frm.add_custom_button(__("Supply Order Form"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_sof",
					args: {
						"wod": frm.doc.name
					},
					callback: function(r) {
						if(r.message) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
						}
					}
				});
			},__('Create'));
			frm.add_custom_button(__("Return Note"), function(){
                                frappe.call({
                                        method: "tsl.tsl.doctype.work_order_data.work_order_data.create_rn",
                                        args: {
                                                "wod": frm.doc.name
                                        },
                                        callback: function(r) {
                                                if(r.message) {
                                                        var doc = frappe.model.sync(r.message);
                                                        frappe.set_route("Form", doc[0].doctype, doc[0].name);
                                                }
                                        }
                                });
                        },__('Create'));
		}
		if(frm.doc.docstatus == 1 && (frm.doc.status == "RSC-Repaired and Shipped Client")) {
			frm.add_custom_button(__("Payment Entry"), function(){
				frappe.call({
					method: "tsl.tsl.doctype.work_order_data.work_order_data.create_paymet_entry",
					args: {
						"wod": frm.doc.name
					},
					callback: function(r) {
						if(r.message) {
							console.log(r.message)
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
						}
					}
				});
			},__('Create'));
		}
		if(frm.doc.attach_image && frm.doc.docstatus == 1){
			cur_frm.set_df_property("image", "options","<img src="+frm.doc.attach_image+">");
			cur_frm.refresh_fields();
			// // if(frm.doc.material_list.length > 0){
			// 	frappe.call({
			// 		method: "tsl.tsl.doctype.work_order_data.work_order_data.get_item_image",
			// 		args: {
			// 			"erf_no":frm.doc.equipment_recieved_form,
			// 			"item":frm.doc.material_list[0].item_code
			// 		},
			// 		callback: function(r) {
			// 			if(r.message) {
			// 				console.log(r.message)
			// 				cur_frm.set_df_property("image", "options","<img src="+r.message+">");
			// 				cur_frm.refresh_fields();
			// 			}
			// 		}
			// 	});
			// }
		}
		
	},
	// check_for_extra_partsheets:function(frm){
	// 	if(frm.doc.docstatus === 1) {
	// 		frappe.call({
	// 			method: "tsl.tsl.doctype.work_order_data.work_order_data.create_extra_ps",
	// 			args: {
	// 				"doc":frm.doc.name
	// 			},
	// 			callback: function(r) {
	// 				if(r.message) {
	// 					if(r.message.length >0){
	// 						console.log(r.message)
	// 						cur_frm.clear_table("extra_part_sheets");
	// 						for(var i=0;i<r.message.length;i++){
	// 							var childTable = cur_frm.add_child("extra_part_sheets");
	// 							childTable.part_sheet_name = r.message[i]["name"],
	// 							childTable.technician = r.message[i]["technician"],
	// 							cur_frm.refresh_fields("extra_part_sheets");

	// 					    }
	// 						cur_frm.doc.docstatus = 1;
	// 					    cur_frm.refresh_fields();
	// 					}
	// 					else{
	// 						frappe.msgprint("No Extra Part Sheets for this Work Order");
	// 					}
						
	// 				}
					
	// 			}
	// 		})
	// 	}

	// },
	material_list_on_form_rendered:function(frm){
	    console.log("add")
	     if(frm.doc.material_list[0].item_code){
		console.log("call")
		$(`[data-name=${frm.doc.material_list[0].item_code}]`).text(frm.doc.material_list[0].item_code)
	     }
	},
	branch:function(frm){
		var d = {
			"Dammam - TSL-SA":"WOD-D.YY.-",
			"Riyadh - TSL-SA":"WOD-R.YY.-",
			"Jeddah - TSL-SA":"WOD-J.YY.-",
			"Kuwait - TSL":"WOD-K.YY.-"
		};
		if(frm.doc.branch){
			frm.set_value("naming_series",d[frm.doc.branch]);
		}
	},

	setup:function(frm){
		frm.fields_dict['material_list'].grid.get_field('item_code').get_query = function(frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			var d = {};
			if(child.model_no){
				d['model'] = child.model_no;
	
			}
			if(child.mfg){
				d['mfg'] = child.mfg;
			}
			if(child.type){
				d['type'] = child.type;
			}
			d['item_group'] = "Equipments";
			return{
				filters: d
			}
			
		}
		// frm.fields_dict['material_list'].grid.get_field('serial_no').get_query = function(frm, cdt, cdn) {
		// 	var row = locals[cdt][cdn];
		// 	var l =[];
		// 	if(row.item_code){
		// 		frappe.call({
		// 		method :"tsl.tsl.doctype.part_sheet.part_sheet.get_serial_no",
		// 		args :{
		// 			"item" :row.item_code,
					
		// 		},
		// 		callback :function(r){
		// 			if(r.message){
		// 				console.log(r.message)
						
		// 				for(var i=0;i<r.message.length;i++){
		// 					l.push(r.message[i]);
		// 				}
						
		// 			console.log(l)
	
		// 			}
					
		// 			}
					
				
	
		// 	})
		// 	return {
		// 		filters: [
		// 			["Serial No","name","in",l]
		// 		]
		// 	};
		// 	}
			
		// }
	 }
		
	
});
frappe.ui.form.on('Work Order Data', {
	setup: function(frm) {
		frm.set_query("branch", function() {
			return {
				filters: [
					["Branch","company", "=", frm.doc.company],
				
					
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
frappe.ui.form.on('Material List', {
	item_code: function(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		var l = [];
		if(row.item_code){
			frappe.call({
			method :"tsl.tsl.doctype.part_sheet.part_sheet.get_serial_no",
			args :{
				"item" :row.item_code,
				
			},
			callback :function(r){
				if(r.message){
					for(var i=0;i<r.message.length;i++){
						l.push(r.message[i]);
					}
					
					
				}
				
				
				}
			
			

		})
		
		}
		frm.set_query("serial_no","material_list", function(frm, cdt, cdn) {
			return {
				filters: {
					'name': ["in",l]
					
				}
			};
		});
		frm.refresh_field("material_list");
		
	},
	
});
