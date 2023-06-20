// Copyright (c) 2023, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Initial Evaluation', {
	refresh: function(frm) {
	// if(frm.doc.docstatus === 1) {
                        frm.add_custom_button(__("Evaluation Report"), function(){
                                frappe.call({
                                        method: "tsl.tsl.doctype.work_order_data.work_order_data.create_initial_eval",
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
		  frm.fields_dict['evaluation_details'].grid.get_field('item').get_query = function(frm, cdt, cdn) {
                                var child = locals[cdt][cdn];
                                var d = {};
                                if(child.model_no){
                                        d['model'] = child.model;
                                }
                                if(child.mfg){
                                        d['mfg'] = child.manufacturer;
                                }
                                if(child.type){
                                        d['type'] = child.type;
                                }
                                d['item_group'] = "Equipments";
                                return{
                                        filters: d
                                }
                        }
		       frm.fields_dict['items'].grid.get_field('part').get_query = function(frm, cdt, cdn) {
                                        var child = locals[cdt][cdn];
                                                var d = {};
                                                d['item_group'] = "Components";
                                                if(child.model){
                                                        d['model'] = child.model;
                                                }
                                                if(child.category){
                                                        d['category_'] = child.category;
                                                }
                                                if(child.sub_category){
                                                        d['sub_category'] = child.sub_category;
                                                }
                                                console.log(d)
                                                return{
                                                        filters: d
                                                }
                        }
		 if( frm.doc.parts_availability == "No"){
                        frm.add_custom_button(__("Request for Quotation"), function(){
                                frappe.call({
                                        method: "tsl.tsl.doctype.part_sheet.part_sheet.create_rfq",
                                        args: {
                                                "ps": frm.doc.name
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
	//}
})  
frappe.ui.form.on('Testing Part Sheet', {
        refresh:function(frm,cdt,cdn){
                if(frm.doc.parts_availability){
                        var last_no = frm.doc.items[frm.doc.items.length-1].part_sheet_no
                        for(var i=0;i<frm.doc.items.length;i++){
                                if(frm.doc.items[i].part_sheet_no != last_no){
                                        var df = frappe.meta.get_docfield("Testing Part Sheet","qty", cdn);
                                        df.read_only = 1;
                                        frm.refresh_fields();
                                }
                        }
                }
        },

	part: function(frm, cdt, cdn){
                let row = locals[cdt][cdn]
                if(row.part && row.qty){
                frappe.call({
                        method :"tsl.tsl.doctype.part_sheet.part_sheet.get_valuation_rate",
                        args :{
                                "item" :row.part,
                                "qty":row.qty,
                                "warehouse":frm.doc.company
                        },
                        callback :function(r){
                                console.log(r)
                                frappe.model.set_value(cdt, cdn, "price_ea", r.message[0]);
                                frappe.model.set_value(cdt, cdn, "parts_availability", r.message[1]);
                                row.total = row.qty * r.message[0];
                                let tot_qty = 0
                                let tot_amount = 0
                                for(let i in frm.doc.items){
                                        tot_qty += frm.doc.items[i].qty
                                        tot_amount += frm.doc.items[i].total
                                }
                                frm.set_value("total_qty", tot_qty)
                                frm.set_value("total_amount", tot_amount)
                                                frm.refresh_fields();
                                }
                })
                }
                frm.refresh();
        },
	qty:function(frm, cdt, cdn){
                var row = locals[cdt][cdn]
                if(row.qty && row.part){
//                      frappe.call({
//                      method :"tsl.tsl.doctype.part_sheet.part_sheet.get_availabilty",
//                      args :{
//                              "qty" : row.qty,
//                              "item" :row.part,
//                              "warehouse":frappe.user_defaults.company
//                      },
//                      callback :function(r){
//                              if(r.message){
//                                      frappe.model.set_value(cdt, cdn, "parts_availability",r.message);
//                                      frm.refresh_fields();
//                              }
//                              row.total = row.qty * row.price_ea
//                              let tot_qty = 0
//                              let tot_amount = 0
//                              for(let i in frm.doc.items){
//                                      tot_qty += frm.doc.items[i].qty
//                                      tot_amount += frm.doc.items[i].total
//                              }
//                              frm.set_value("total_qty", tot_qty)
//                              frm.set_value("total_amount", tot_amount)
//                              frm.refresh();
//                      }
//              })
                frm.script_manager.trigger('part',cdt,cdn)
           }
        },
        price_ea:function(frm,cdt,cdn){
                frm.script_manager.trigger("qty",cdt,cdn);

        },
})
