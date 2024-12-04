frappe.ui.form.on('Request for Quotation', {
        setup: function (frm) {
        	frappe.db.get_value('Company', {'name':frm.doc.company}, ['country'], (r) => {
                        console.log(r)
		   frm.set_query("supplier", "suppliers", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
		
			return {
				filters: [
					['Supplier', 'country', '=', r.country]
				]
			};
		});
    	});
		

	},

    onload_post_render:function(frm){

        // if(frm.doc.items && frm.doc.supply_order_data){
        //         $.each(frm.doc.items, function(i,d) {
        //         frappe.db.get_value('Warehouse', {'company':frm.doc.company,"is_repair":0}, ['name'], (r) => {
        //                 d.warehouse = r.name
                                                        
        //             });
                       
        //                 });
        //         }
                        
                if(frm.doc.items && frm.doc.work_order_data){
                        $.each(frm.doc.items, function(i,d) {
                        frappe.db.get_value('Warehouse', {'company':frm.doc.company,"is_branch":1}, ['name'], (r) => {
                        d.warehouse = r.name
                                                        
                            });
                        });
        
                        // frappe.db.get_value('Department', {'company':frm.doc.company,"is_repair":1}, ['name'], (r) => {
                        //         frm.set_value("department",r.name)
                                                                
                        // });
                }

                if(frm.doc.items && frm.doc.supply_order_data){
                        $.each(frm.doc.items, function(i,d) {
                        frappe.db.get_value('Warehouse', {'company':frm.doc.company,"is_branch":1}, ['name'], (r) => {
                        d.warehouse = r.name
                                                        
                            });
                        });
        
                        // frappe.db.get_value('Department', {'company':frm.doc.company,"is_repair":1}, ['name'], (r) => {
                        //         frm.set_value("department",r.name)
                                                                
                        // });
                }
                
        frm.set_query("branch", function() {
                return {
                        filters: [
                                ["Branch","company", "=", frm.doc.company],
                                
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
    
        },
    refresh:function(frm){

        if(frm.doc.supply_order_data){
                frm.set_df_property('work_order_data', 'hidden',1)
            }
            if(frm.doc.work_order_data){
                frm.set_df_property('supply_order_data', 'hidden',1)
            }


        if (frm.doc.docstatus === 1) {
		frm.add_custom_button(__('Multiple Supplier Quotation'),
			function(){ 
                        frappe.call({
                                method: "tsl.custom_py.supplier_quotation.make_supplier_quotation_from_rfq",
                                args: {
                                        "source_name": cur_frm.doc.name
                                        
                                },
                                freeze :true,
                                freeze_message :"Processing...",
                               
                                callback: function(r) {
                                        if(r.message) {
                                        }
                                }
                        });
                        }, __("Create"));
                }
        
        if(frm.doc.docstatus == 0 && frm.doc.__islocal){
                
                frm.add_custom_button(__('Work Order Data'),
                function() {
        new frappe.ui.form.MultiSelectDialog({
                doctype: "Work Order Data",
                target: frm,
                setters: {
                        customer:null,
                        wod_component:null,
                },
                
                add_filters_group: 1,
                get_query() {
                        return {
                                filters: { is_quotation_created: 0, docstatus:1,branch :frm.doc.branch_name }
                        }
                },
                action(selections) {
                        frappe.call({
                        method: "tsl.custom_py.after_import.get_items_from_ps",
                        args: {
                                "wod": selections
                        },
                        callback: function(r) {
                                if(r.message) {
                                        cur_frm.clear_table("items");
                                        // for(var i=0;i<r.message.length;i++){
                                                console.log(r)
                                                $.each(r.message, function(i,v){
                                                        console.log(v.qty)
                                                        var item_child = cur_frm.add_child("items");
                                                        item_child.item_code = v.part,
                                                        item_child.item_name = v.part_name,
                                                        item_child.mfg = v.manufacturer,
                                                        item_child.model = v.model,
                                                        item_child.category = v.category,
                                                        item_child.sub_category = v.sub_category,
                                                        item_child.serial_no = v.serial_no,
                                                        item_child.description = v.part_name,
                                                        item_child.qty = v.qty,
                                                        item_child.uom = "Nos",
                                                        item_child.warehouse = frm.doc.branch,
                                                        item_child.branch =  frm.doc.branch,
                                                        item_child.work_order_data =  v.wod,
                                                        item_child.conversion_factor =1,
                                                        item_child.department = frm.doc.department,
                                                        item_child.initial_evaluation = v.parent
                                                        cur_frm.refresh_fields("items");
                                                })
                                                // if(r.message[i]["parts_availabilty == "No"){
                                                       
                                                // }
                                        // }
                                                
                                                     
                                                
                                 }
                                }
                        });
                        cur_dialog.hide();
                }

                        });
                }, __("Get Items From"), "btn-default");
        }

        if(frm.doc.docstatus == 0 && frm.doc.__islocal){
                
                frm.add_custom_button(__('Supply Order Data'),
                function() {
        new frappe.ui.form.MultiSelectDialog({
                doctype: "Supply Order Data",
                target: frm,
                setters: {
                        customer:null,
                        
                },
                
                add_filters_group: 1,
                get_query() {
                        return {
                                filters: { is_quotation_created: 0, docstatus:1,branch :frm.doc.branch_name }
                        }
                },
                action(selections) {
                        frappe.call({
                        method: "tsl.custom_py.after_import.get_items_from_sod",
                        args: {
                                "sod": selections
                        },
                        callback: function(r) {
                                if(r.message) {
                                        var item_code ,item_name,model,mfg,category,sub_category,qty,description;
                                        console.log(r.message)
                                        cur_frm.clear_table("items");
                                        for(var i=0;i<r.message.length;i++){
                                                if("part" in r.message[i]){
                                                        item_code = r.message[i]['part']
                                                        item_name = r.message[i]['part_name']
                                                        model = r.message[i]['model']
                                                        mfg = r.message[i]['manufacturer']
                                                        category = r.message[i]['category']
                                                        sub_category= r.message[i]['sub_category']
                                                        qty = r.message[i]['qty']
                                                        description = r.message[i]['part_name']+"<br>Item Group: Components "
                                                        
                                                }
                                                else{
                                                        item_code = r.message[i]["item_code"]
                                                        item_name = r.message[i]['item_name']
                                                        model = r.message[i]['model_no']
                                                        mfg = r.message[i]['mfg']
                                                        qty = r.message[i]['quantity']
                                                        description = r.message[i]['item_name']+"<br>Item Group: Equipments "
                                                        
                                                }
                                                        var childTable = cur_frm.add_child("items");
                                                        childTable.item_code = item_code,
                                                        childTable.item_name = item_name,
                                                        childTable.mfg =mfg,
                                                        childTable.model = model,
                                                        childTable.category = category,
                                                        childTable.sub_category = sub_category,
                                                        childTable.serial_no = r.message[i]["serial_no"],
                                                        childTable.description = description,
                                                        childTable.type=r.message[i]['type']
                                                        childTable.qty = qty,
                                                        childTable.uom = "Nos",
                                                        childTable.warehouse = frm.doc.branch,
                                                        childTable.branch =  frm.doc.branch,
                                                        childTable.supply_order_data =  r.message[i]['sod'],
                                                        childTable.conversion_factor =1,
                                                        childTable.department =r.message[i]['dept'],
                                                        frm.doc.supply_order_data = r.message[i]['sod']
                                                        frm.doc.department = r.message[i]['dept']
                                                        cur_frm.refresh_fields("items");
                                                }  
                                                                                              
                                                     
                                                
                                 }
                                }
                        });
                        cur_dialog.hide();
                }

                        });
                }, __("Get Items From"), "btn-default");
        }
        }
});
