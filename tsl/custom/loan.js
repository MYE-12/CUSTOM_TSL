frappe.ui.form.on('Loan', {
    refresh(frm){
        if(frm.doc.docstatus == 1){
            frm.add_custom_button(__('Pause'), function() {
                let dialog = new frappe.ui.Dialog({
                    title: 'Pause Loan Accrual',
                    fields: [
                        {
                            fieldtype: 'Date',
                            fieldname: 'from_date',
                            label: 'From Date',
                            reqd: 1,
                            onchange(){
                                frappe.call({
                                    method:"erpnext.loan_management.doctype.loan.loan.check_from_date",
                                    args:{
                                        name:frm.doc.name,
                                        date:dialog.get_value('from_date')
                                    }
                                })
                            }
                        },
                        {
                            fieldtype: 'Date',
                            fieldname: 'to_date',
                            label: 'To Date',
                            reqd: 1
                        },
                        {
                            label: 'Date',
                            fieldname:'date',
                            fieldtype:'Date',
                            default: frappe.datetime.now_date(),
                            hidden:1
                        },
                        {
                            label: 'Remarks',
                            fieldname:'remarks',
                            reqd:1,
                            fieldtype:'Small Text',
                        },
                    ],
                    primary_action_label: 'Pause',
                    primary_action: function() {
                        let data = dialog.get_values();
                        if (data) {
    
                            let newRemark = {
                                pause_from:data.from_date,
                                pause_upto:data.to_date,
                                posting_date:data.date,
                                remarks:data.remarks, 
                            };
                            frappe.call({
                                method:"erpnext.loan_management.doctype.loan.loan.shift_payment_dates_for_pause",
                                args:{
                                    self:frm.doc.name,
                                    from_date:data.from_date,
                                    to_date:data.to_date,
                                    loan_pause_details: newRemark
                                },
                                callback(r){
                                    dialog.hide();
                                    // window.location.reload()
                                }
                            })
    
                        }
                    }
                });
                dialog.show();
            });
        }
    },
});
