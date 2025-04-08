// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Application Form', {
	return_date(frm){
		if(frm.doc.to_date < frm.doc.return_date){
			frappe.msgprint("Return Date should not be greater than the leave end date")
			frappe.validated = false
		}
	},
	lop_days(frm){
		if (frm.doc.lop_start_date && frm.doc.lop_end_date && 
			frm.doc.employee && frm.doc.leave_type){
			frappe.call({
				method:"tsl.tsl.doctype.leave_application_form.leave_application_form.validate_balance_leaves_lop",
				args:{
					company:frm.doc.company,
					from_date: frm.doc.lop_start_date,
					to_date: frm.doc.lop_end_date,
					employee: frm.doc.employee,
					leave_type: frm.doc.leave_type
				},
				callback(r){
					if(r){
						frm.set_value("lop_days",r.message)	
						if(frm.doc.lop_days > 15 && frm.doc.is_special_permission == 0){
							frappe.msgprint("Unpaid Days should not be greater than 15 days")
							frappe.validated = false
						}
						frm.set_value("no_of_days",frm.doc.leave_days + r.message)						
					}
				}
			})
		}
		else{
			frm.set_value("lop_days",0)	
			frm.set_value("no_of_days",frm.doc.leave_days + frm.doc.lop_days)	
		}
	},
	leave_days(frm){
		if (frm.doc.leave_start_date && frm.doc.leave_end_date && 
			frm.doc.employee && frm.doc.leave_type){
			frappe.call({
				method:"tsl.tsl.doctype.leave_application_form.leave_application_form.validate_balance_leaves",
				args:{
					company:frm.doc.company,
					from_date: frm.doc.leave_start_date,
					to_date: frm.doc.leave_end_date,
					employee: frm.doc.employee,
					leave_type: frm.doc.leave_type
				},
				callback(k){
					if(k){
						frm.set_value("leave_days",k.message)	
						frm.set_value("no_of_days",frm.doc.lop_days + k.message)	
					}
				}
			})	
		}
		else{
			frm.set_value("leave_days",0)	
			frm.set_value("no_of_days",frm.doc.lop_days+frm.doc.leave_days)
		}
	},
	lop_start_date(frm){
		frappe.run_serially([
			() => frm.trigger("date_calc"),
			() => frm.trigger("lop_days"),
			() => frm.trigger("leave_days"),
			() => {
				if(frm.doc.lop_start_date && (frm.doc.lop_start_date < frm.doc.from_date || frm.doc.lop_start_date > frm.doc.to_date)){
					frappe.msgprint(__('Please enter a date between {0} and {1}.', [frm.doc.from_date, frm.doc.to_date]));
					frm.set_value('lop_start_date', null);
				}
				if(frm.doc.lop_end_date < frm.doc.lop_start_date){
					frappe.msgprint(__('LOP Start Date should be lesser than LOP End Date'));
					frm.set_value('lop_start_date', null);
				}
			},
		])		
	},
	lop_end_date(frm){
		frappe.run_serially([
			() => {
				if(frm.doc.lop_end_date && (frm.doc.lop_end_date < frm.doc.from_date || frm.doc.lop_end_date > frm.doc.to_date)){
					frappe.msgprint(__('Please enter a date between {0} and {1}.', [frm.doc.from_date, frm.doc.to_date]));
					frm.set_value('lop_end_date', null);
				}
				if(frm.doc.lop_end_date < frm.doc.lop_start_date){
					frappe.msgprint(__('LOP End Date should be greater than LOP Start Date'));
					frm.set_value('lop_end_date', null);
				}
			},	
			() => frm.trigger("lop_days"),
			() => frm.trigger("leave_days"),
		])		
	},
	date_calc(frm){
		frappe.run_serially([
			() => {
				if(frm.doc.lop_start_date){
					if(frm.doc.lop_start_date == frm.doc.from_date){
						if(frm.doc.leave_end_date){
							frm.set_value("leave_end_date",null)
						}
						if(frm.doc.leave_start_date){
							frm.set_value("leave_start_date",null)
						}
					}
					else{
						frm.set_value("leave_start_date",frm.doc.from_date)
						frm.set_value("leave_end_date",frappe.datetime.add_days(frm.doc.lop_start_date,-1))
					}
				}
				else{
					frm.set_value("leave_start_date",frm.doc.from_date)
					frm.set_value("leave_end_date",frm.doc.to_date)
				}
			},
			() => frm.trigger("lop_days"),
			() => frm.trigger("leave_days"),
		])
	},
	to_date(frm){
	    frm.trigger("employee")
		if(frm.doc.to_date != frm.doc.lop_end_date){
			frm.set_value("lop_start_date",null)
			frm.set_value("lop_end_date",null)
		}
		if(frm.doc.to_date && frm.doc.to_date < frm.doc.from_date){
			frappe.msgprint(__("To Date should be greater than From Date"))
			frm.set_value("from_date",null)
			frm.set_value("to_date",null)
		}
		frappe.run_serially([
			() => {
				if (frm.doc.from_date && frm.doc.to_date && 
					frm.doc.employee && frm.doc.leave_type){
					frappe.call({
						method:"tsl.tsl.doctype.leave_application_form.leave_application_form.validate_balance_leaves",
						args:{
							company:frm.doc.company,
							from_date: frm.doc.from_date,
							to_date: frm.doc.to_date,
							employee: frm.doc.employee,
							leave_type: frm.doc.leave_type
						},
						callback(k){
							if(k){
								frm.set_value("total_leave_days",k.message)
								if(k.message < frm.doc.leave_balance){
									frm.set_value("lop_start_date",null)
									frm.set_value("lop_end_date",null)
								}
								if(k.message > frm.doc.leave_balance){
									frappe.msgprint("Kindly fill the Unpaid Start and End Date")
								}
								if(frm.doc.leave_balance + 13 <k.message && frm.doc.is_special_permission == 0){
									frappe.msgprint("Unpaid Days exceed the permissible limit - <b>"+15+"</b>")
									frm.set_value("to_date",null)
									frm.set_value("lop_start_date",null)
									frm.set_value("lop_end_date",null)
								}
							}
						}
					})	
				}
			},
			() => {
				if(frm.doc.employee && frm.doc.from_date && frm.doc.to_date && frm.doc.leave_type && frm.doc.leave_balance){
					frappe.call({
						method:"tsl.tsl.doctype.leave_application_form.leave_application_form.list_leave_dates",
						args:{
							'employee':frm.doc.employee, 
							'from_date':frm.doc.from_date, 
							'to_date':frm.doc.to_date,
							'leave_type':frm.doc.leave_type,
							'company':frm.doc.company,
							'leave_balance':frm.doc.leave_balance
						},
						callback(r){
							frm.fields_dict.lop_start_date.datepicker.update({
								minDate: new Date(r.message[1]),
								maxDate: new Date(frm.doc.to_date),
							});
							frm.fields_dict.lop_end_date.datepicker.update({
								minDate: new Date(r.message[1]),
								maxDate: new Date(frm.doc.to_date),
							});
						}
					})
				}
			},
			
			() => {
				if (frm.doc.leave_start_date && frm.doc.leave_end_date && 
					frm.doc.employee && frm.doc.leave_type){
					frappe.call({
						method:"tsl.tsl.doctype.leave_application_form.leave_application_form.validate_balance_leaves",
						args:{
							company:frm.doc.company,
							from_date: frm.doc.leave_start_date,
							to_date: frm.doc.leave_end_date,
							employee: frm.doc.employee,
							leave_type: frm.doc.leave_type
						},
						callback(k){
							if(k){
								frm.set_value("leave_days",k.message)	
							}
						}
					})	
				}
			},
			() => frm.trigger("date_calc"),
			() => frm.trigger("lop_days"),
			() => frm.trigger("leave_days"),
		])
	},
	from_date(frm){
	    frm.trigger("employee")
		if(frm.doc.to_date && frm.doc.to_date < frm.doc.from_date){
			frappe.msgprint(__("To Date should be greater than From Date"))
			frm.set_value("from_date",null)
			frm.set_value("to_date",null)
		}
		frappe.run_serially([
			() => frm.set_value("leave_start_date",frm.doc.from_date),
			() => frm.trigger("leave_days"),
			() => frm.trigger("to_date"),
			() => frm.trigger("date_calc"),
			() => frm.trigger("lop_days"),
		])
		
	},
	leave_type(frm){
	    frm.trigger("employee")
		frm.trigger("to_date")
	},
	employee(frm){
		if (frm.doc.employee) {
			frappe.call({
				method:"tsl.tsl.doctype.leave_application_form.leave_application_form.return_last_rejoined_date",
				args:{
					employee:frm.doc.employee
				},
				callback(r){
					if(r.message){
						frm.set_value("last_rejoined_date",r.message)
					}
				}
			})
			
			if(frm.doc.user_id){
				frappe.call({
					method:"tsl.tsl.doctype.leave_application_form.leave_application_form.get_roles",
					args:{
						user_id:frm.doc.user_id
					},
					callback(r){
						if(r){
							if(r.message == true){
								frm.set_value('approver',1)
							}
							if(r.message == false){
								frm.set_value('approver',0)
							}
						}
					}
				})
			}
			else{
				frm.set_value('approver',0)
				frappe.msgprint("User ID not set for this employee")
			}
			
			let today = new Date().toISOString().split('T')[0];
            frappe.call({
				method: "hrms.hr.doctype.leave_application.leave_application.get_leave_details",
				async: false,
				args: {
					employee: frm.doc.employee,
					date: today,
				},
				callback: function (r) {
					// for (const [key, value] of Object.entries(r.message["leave_allocation"])) {
					// 	if (key == frm.doc.leave_type && frm.doc.docstatus == 0){
					// 		if(value['remaining_leaves'] != frm.doc.leave_balance){
					// 			frm.set_value("leave_balance",value['remaining_leaves'])
					// 		}
					// 	}
					// }
					let leave_details = r.message["leave_allocation"];
					let lwps = r.message["lwps"];
					frm.get_field("balance").$wrapper.html(renderLeaveDetailsTable(leave_details,frm))
					
					let allowed_leave_types = Object.keys(leave_details);
					allowed_leave_types = allowed_leave_types.concat(lwps);
					frm.set_query("leave_type", function () {
						return {
							filters: [["leave_type_name", "in", allowed_leave_types]],
						};
					});
				},
			});
        }
	},
	refresh(frm) {
		if(frm.doc.employee && frm.doc.from_date && frm.doc.to_date && frm.doc.leave_type && frm.doc.leave_balance){
			frappe.call({
				method:"tsl.tsl.doctype.leave_application_form.leave_application_form.list_leave_dates",
				args:{
					'employee':frm.doc.employee, 
					'from_date':frm.doc.from_date, 
					'to_date':frm.doc.to_date,
					'leave_type':frm.doc.leave_type,
					'company':frm.doc.company,
					'leave_balance':frm.doc.leave_balance
				},
				callback(r){
					frm.fields_dict.lop_start_date.datepicker.update({
						minDate: new Date(r.message[1]),
						maxDate: new Date(frm.doc.to_date),
					});
					frm.fields_dict.lop_end_date.datepicker.update({
						minDate: new Date(r.message[1]),
						maxDate: new Date(frm.doc.to_date),
					});
				}
			})
		}
		
	    frm.trigger("employee")
		if(!frm.doc.__islocal){
			frm.add_custom_button(__("Print"), function () {
				var f_name = frm.doc.name;
				var print_format = "Leave Application";
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Leave Application Form")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}); 
		}
		
		if (frm.doc.leave_type == 'Annual Leave') {
			frm.add_custom_button(__('Leave Salary'), function () {
				frappe.db.get_value('Leave Salary', { 'employee': frm.doc.employee }, 'name')
				.then(r => {
					if (r.message && Object.entries(r.message).length === 0) {
						frappe.route_options = { 'employee': frm.doc.employee, 'employee_name': frm.doc.employee_name ,'leave_application':frm.doc.name};
						frappe.set_route('Form', 'Leave Salary', 'new-leave-salary-1');
					}
					else {
						frappe.set_route('Form', 'Leave Salary', r.message.name);
					}
				});
			});
			frm.add_custom_button(__('Employee Clearance'), function () {
				frappe.db.get_value('Employee Clearance', { 'emp_no': frm.doc.employee }, 'emp_no')
					.then(r => {
						if (r.message && Object.entries(r.message).length === 0) {
							frappe.route_options = { 'emp_no': frm.doc.employee, 'employee_name': frm.doc.employee_name,'leave_application':frm.doc.name};
							frappe.set_route('Form', 'Employee Clearance', 'new-employee-clearance-1');
						}
						else {
							frappe.set_route('Form', 'Employee Clearance', r.message.name);
						}
					});
			});
		}
	},
	validate: function(frm) {
		if(["Annual Leave"].includes(frm.doc.leave_type) && frm.doc.from_date){
			let today = new Date().toISOString().split('T')[0];
			frappe.call({
				method: "tsl.custom_py.leave_allocation.calculate_projected_leaves",
				async: false,
				args: {
					employee: frm.doc.employee,
					current_date: today,
					leave_start_date: frm.doc.from_date
				},
				callback(k){
					if(k){
						if(k.message > 0){
							frm.set_value("leave_projection",1)
						}
						else{
							frm.set_value("leave_projection",0)
						}
					}
				}
			})
		}
		frappe.run_serially([
			() => frm.set_value("no_of_days",frm.doc.lop_days + frm.doc.leave_days),
			() => frm.trigger("return_date"),
			() => frm.trigger("leave_days"),
			() => frm.trigger("lop_days"),
			() => frm.trigger("lop_end_date"),
			() => frm.trigger("lop_start_date"),
 		])	
	},
	ticket_used(frm) {
	    if(frm.doc.ticket_used && frm.doc.no_of_tickets < frm.doc.ticket_used){
	        frappe.msgprint("Available Tickets <b>"+frm.doc.no_of_tickets+"</b> is lesser than - <b>"+ frm.doc.ticket_used+"</b>")
	        frappe.validated = false
	    }
	},
	before_workflow_action: async (frm) => {
		if(frm.doc.workflow_state == "Draft"){
			let promise = new Promise((resolve, reject) => {
				if (frm.selected_workflow_action == "Send to Department Head" && frm.doc.leave_approver) {
					// Department Head
					frm.call({
						method: 'trigger_mail',
						args: {
							"name": frm.doc.name,
							"leave_approver": frm.doc.leave_approver,
						},
					})
				}
				resolve();
			});
			await promise.catch(() => frappe.throw());
		}
		let promise = new Promise((resolve, reject) => {
			if(frm.doc.company == "TSL COMPANY - KSA"){
				var hr_mail = "admin@tsl-me.com" 
			}
			else{
				var hr_mail = "hr@tsl-me.com"
			}
			if (frm.selected_workflow_action == "Send to CEO") {
				// CEO Approval
				frm.call({
					method: 'trigger_mail',
					args: {
						"name": frm.doc.name,
						"workflow_state": "Under CEO",
						"email": "alkouh@tsl-me.com",
						"hr_mail": hr_mail
					},
				})
			}
			resolve();
		});
		await promise.catch(() => frappe.throw());
		
		
		let w_flow = new Promise((resolve, reject) => {
			if (frm.selected_workflow_action == "Send to HR") {
				// HR Approval
				frm.call({
					method: 'trigger_mail_to_hr',
					args: {
						"name": frm.doc.name,
						"workflow_state": "Under HR",
						"company": frm.doc.company
					},
				})
			}
			resolve();
		});
		await w_flow.catch(() => frappe.throw());
		
	},
})

function renderLeaveDetailsTable(data,frm) {
    if (jQuery.isEmptyObject(data)) {
        return `<p style="margin-top: 20px;text-align:center;font-size:14px">${__("No leaves have been allocated.")}</p>`;
    }


    let tableHTML = `<table class="table table-bordered" style = "border: 1px solid black"><thead><tr><th style="width: 16%;border: 1px solid black">${__("Leave Type")}</th><th style="width: 16%;border: 1px solid black" class="text-right">${__("Available Leaves")}</th><th style="width: 16%;border: 1px solid black" class="text-right">${__("Used Leaves")}</th>`;
	if(["Annual Leave"].includes(frm.doc.leave_type) && frm.doc.from_date){
		tableHTML += `<th style="width: 16%;border: 1px solid black" class="text-right">${__("Future Projected Leaves")}</th>`;
	}
	tableHTML += `<th style="border: 1px solid black;width: 16%" class="text-right">${__("Total Available Leaves")}</th>`
	tableHTML += `</tr></thead><tbody>`;

    for (const [key, value] of Object.entries(data)) {
        let color = parseInt(value["remaining_leaves"]) > 0 ? "green" : "red";
        tableHTML += `
            <tr>
                <td style = "border: 1px solid black">${key}</td>
                <td style = "border: 1px solid black" class="text-right" ${color}">${value["total_leaves"]}</td>`
		if(["Annual Leave"].includes(frm.doc.leave_type) && frm.doc.from_date){
			let today = new Date().toISOString().split('T')[0];
			frappe.call({
				method: "tsl.custom_py.leave_allocation.calculate_projected_leaves",
				async: false,
				args: {
					employee: frm.doc.employee,
					current_date: today,
					leave_start_date: frm.doc.from_date
				},
				callback(k){
					if(k){
						if(k.message > 0){
							frm.set_value("leave_projection",1)
						}
						else{
							frm.set_value("leave_projection",0)
						}
						if(key == frm.doc.leave_type){
							tableHTML +=`
								<td style = "border: 1px solid black" class="text-right">${value["leaves_taken"]}</td>
								<td style = "border: 1px solid black" class="text-right">${k.message}</td>
								<td style = "border: 1px solid black" class="text-right" style="color: ${color}">${parseInt((k.message + value["remaining_leaves"]),10)}</td>`;
								if(parseInt((k.message + value["remaining_leaves"]),10) != frm.doc.leave_balance){
									frm.set_value("leave_balance",parseInt((k.message + value["remaining_leaves"]),10))		
								}	
						}
						else{
							tableHTML +=`
							<td style = "border: 1px solid black" class="text-right">${value["leaves_taken"]}</td>
							<td style = "border: 1px solid black" class="text-right">0</td>
							<td style = "border: 1px solid black" class="text-right" style="color: ${color}">${parseInt((value["remaining_leaves"]),10)}</td>`;
						}
					}
				}
			})
		}
		else{
			if((key == frm.doc.leave_type) && (parseInt((value["remaining_leaves"]),10) != frm.doc.leave_balance)){
				frm.set_value("leave_balance",parseInt((value["remaining_leaves"]),10))		
			}
			let color = parseInt(value["remaining_leaves"]) > 0 ? "green" : "red";
			tableHTML += `
                <td style = "border: 1px solid black" class="text-right" >${value["leaves_taken"]}</td><td class="text-right" style="border: 1px solid black;color:${color}">${parseInt((value["remaining_leaves"]),10)}</td>`
		}
        tableHTML += `</tr>`;

    }

    tableHTML += `
            </tbody>
        </table>
    `;
    return tableHTML;
}
