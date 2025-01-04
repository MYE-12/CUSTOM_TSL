frappe.ui.form.on('Employee', {
        date_of_joining(frm) {
                var join_date = new Date(frm.doc.date_of_joining);
                var difference = Date.now() - join_date.getTime();
                var diff_date = new Date(difference);
                var exp_years = Math.abs(diff_date.getUTCFullYear() - 1970);
                var tickets = Math.floor(exp_years / 2) * 2;
                frm.set_value("total_tickets", tickets);
                var tickets_available = tickets - frm.doc.used_tickets
                frm.set_value('no_of_tickets',tickets_available)
	},
        refresh(frm){
                frm.trigger("company")
        },
       
        company(frm){
                if(frm.doc.__islocal){
                        frappe.call({
                                method:"tsl.custom_py.employee.employee_series",
                                callback(r){
                                        if(r.message){
                                                frm.set_value("employee_number",r.message)
                                        }
                                }
                        })
                }
        },
        create_fnf(frm){
                frappe.db.get_value('Full and Final Settlement',{'employee': frm.doc.name },'name')
                        .then(r => {
                        if(r.message && Object.entries(r.message).length === 0){
                                frappe.route_options = { 
                                        'employee':frm.doc.employee,
                                        'employee_name': frm.doc.employee_name,
                                        'type': "Termination",
                                }
                                frappe.set_route('Form','Full and Final Settlement','new-full-and-final-settlement-1')
                        }
                        else{
                                frappe.set_route('Form','Full and Final Settlement',r.message.name)
                        }
                })
        }
})