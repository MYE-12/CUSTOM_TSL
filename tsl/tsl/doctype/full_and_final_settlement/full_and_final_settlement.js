// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Full and Final Settlement', {
    check_for_total_working_days : function(frm){
        if(frm.doc.company == "TSL COMPANY - Kuwait" && frm.doc.no_of_days_worked > frm.doc.total_working_days){
            frm.set_value("no_of_days_worked",frm.doc.total_working_days)
        }
    },
    get_leave_balance: function (frm) {
		frappe.call({
			method: "hrms.hr.doctype.leave_application.leave_application.get_leave_balance_on",
			args: {
				employee: frm.doc.employee,
				date: frm.doc.last_day_of_work || '',
				to_date: frm.doc.last_day_of_work || '',
				leave_type: "Annual Leave",
				consider_all_leaves_in_the_allocation_period: 1,
			},
			callback: function (r) {
				if (!r.exc && r.message) {
					frm.set_value("leave_balance", r.message);
					frappe.call({
					    method:"tsl.custom_py.utils.calculate_leave_payment_amount",
					    args:{
					        "company": frm.doc.company,
					        "total_working_days": frm.doc.total_working_days,
					        "basic":frm.doc.ctc,
					        "leave_balance":r.message
					    },
					    callback(k){
					        if(k.message ){
              	                frm.set_value("leave_payment_amount",k.message)
					        }
					    }
					})
                
				} else {
					frm.set_value("leave_balance", "0");
				}
			},
		});
	},
	
    type(frm){
        frm.trigger("gratuity_calculation")  
    },
    gratuity_calculation(frm){
        if(frm.doc.employee){
            frappe.call({
                method:"tsl.custom_py.utils.gratuity_amount",
                args:{
                    employee:frm.doc.employee,
					date:frm.doc.last_day_of_work
                },
                callback(r){
                    if(r){
                        if(frm.doc.type == "Resignation"){
                            frm.set_value("gratuity_amount",r.message.resignation_amount)
                            frm.set_value("gratuity_days",r.message.resignation_days)
                        }
                        
                        if(frm.doc.type == "Termination"){
                            frm.set_value("gratuity_amount",r.message.termination_amount)
                            frm.set_value("gratuity_days",r.message.termination_days)
                        }
                    }
                }
            })
        }
    },
    refresh(frm) {
        frm.trigger("get_leave_balance")
        if (frm.doc.workflow_state == "Approved") {
            frm.add_custom_button(__("Print F & F"), function () {

                var f_name = frm.doc.name
                var print_format = "Full and Final Settlement";
                window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
                    + "doctype=" + encodeURIComponent("Full and Final Settlement")
                    + "&name=" + encodeURIComponent(f_name)
                    + "&trigger_print=1"
                    + "&format=" + print_format
                    + "&no_letterhead=0"
                ))
            });
        }
    },
    net_pay(frm){
        var leave_pay = (frm.doc.leave_payment_amount)
        var gra_amount = (frm.doc.gratuity_amount)
        var leave_grat = (parseFloat(leave_pay) + parseFloat(gra_amount)) + (parseFloat(frm.doc.additions))- (frm.doc.loan_other_deduction)
        frm.set_value('leave_gratuity_total', leave_grat)
        var net_pay = leave_grat + frm.doc.total_salary
        frm.set_value('net_pay', net_pay)
    },
    validate(frm) {
        var date1 = new Date(frm.doc.date_of_joining);
        var date2 = new Date(frm.doc.pay_end_date);
        var diffTime = Math.abs(date2 - date1);
        var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
        frm.set_value('employment_duration',diffDays +1)
        frm.set_value('total_worked',diffDays +1)
        frm.trigger("gratuity_calculation")
        frm.trigger("encashed_leaves")
        frm.trigger("net_pay")
        frm.trigger("check_for_total_working_days")
    },
    leaves_calculation(frm){
        var earned_basic = ((frm.doc.basic_salary / frm.doc.total_working_days) * (frm.doc.no_of_days_worked- frm.doc.absent_days))
        if (earned_basic) {
            frm.set_value('earned_basic', earned_basic.toFixed(2))
        }
        
        var earned_food_allowance = ((frm.doc.food_allowance/frm.doc.total_working_days)*(frm.doc.no_of_days_worked - frm.doc.absent_days))
        if (earned_food_allowance) {
            frm.set_value('earned_food_allowance', earned_food_allowance.toFixed(2))
        }
        
        var earned_mobile_allowance = ((frm.doc.mobile_allowance/frm.doc.total_working_days)*(frm.doc.no_of_days_worked - frm.doc.absent_days))
        if (earned_mobile_allowance) {
            frm.set_value('earned_mobile_allowance', earned_mobile_allowance.toFixed(2))
        }
        
        var earned_car_allowance = ((frm.doc.car_allowance/frm.doc.total_working_days)*(frm.doc.no_of_days_worked - frm.doc.absent_days))
        if (earned_car_allowance) {
            frm.set_value('earned_car_allowance', earned_car_allowance.toFixed(2))
        }
        
        var earned_hra = ((frm.doc.hra/frm.doc.total_working_days)*(frm.doc.no_of_days_worked - frm.doc.absent_days))
        if (earned_hra) {
            frm.set_value('earned_hra', earned_hra.toFixed(2))
        }
        
        var earned_other_allowance = ((frm.doc.other_allowances/frm.doc.total_working_days)*(frm.doc.no_of_days_worked - frm.doc.absent_days))
        if (earned_other_allowance) {
            frm.set_value('earned_other_allowance', earned_other_allowance.toFixed(2))
        }
        
        var gosi = ((frm.doc.gosi_deduction/frm.doc.total_working_days)*(frm.doc.no_of_days_worked - frm.doc.absent_days))
        if (gosi) {
            frm.set_value('gosi', gosi.toFixed(2))
        }
        
        
        var transportation = ((frm.doc.transportation_pay/frm.doc.total_working_days)*(frm.doc.no_of_days_worked - frm.doc.absent_days))
        if (transportation) {
            frm.set_value('transportation', earned_food_allowance.toFixed(2))
        }
        
        
        var tott = (parseFloat(frm.doc.earned_basic)+parseFloat(frm.doc.earned_food_allowance)+
                    parseFloat(frm.doc.earned_mobile_allowance)+parseFloat(frm.doc.earned_car_allowance)+
                    parseFloat(frm.doc.earned_hra)+parseFloat(frm.doc.earned_other_allowance)+
                    parseFloat(frm.doc.amount)+parseFloat(frm.doc.transportation) - parseFloat(frm.doc.gosi))
        frm.set_value('total_salary',tott)
    },
    onload(frm){
		frappe.run_serially([
			()=>{
				if(frm.doc.type == "Termination"){
					frappe.db.get_value(
						"Employee",
						frm.doc.employee,
						"termination_date",
						(r) => {
							frm.set_value("last_day_of_work", r.termination_date)
						}
					);
				}
				else{
					frappe.db.get_value(
						"Resignation Form",
						frm.doc.employee,
						"actual_relieving_date",
						(r) => {
							frm.set_value("last_day_of_work", r.actual_relieving_date)
						}
					);
				}
			},
			// () => frm.trigger("employee"),  
			() => frm.trigger("gratuity_calculation"),
			() => frm.trigger("get_leave_balance"),
			() => frm.trigger("check_for_total_working_days")
		])
    },
    employee(frm) {
        if(frm.doc.employee && frm.doc.company){
            frappe.call({
                method: "tsl.tsl.doctype.full_and_final_settlement.full_and_final_settlement.get_reg_form",
                args: {
                    'employee': frm.doc.employee
                },
                callback: function (d) {
                    if (d.message) {
                        frm.set_value('resignation_form', d.message[0])
                        frm.set_value('pay_start_date', d.message[1])
                        frm.set_value('pay_end_date', d.message[2])
                		frappe.call({
                		    method:"tsl.tsl.doctype.leave_application_form.leave_application_form.get_number_of_leave_days",
                		    args:{
                            	company:frm.doc.company,
                            	employee: frm.doc.employee,
                            	leave_type: "Annual Leave",
                		        to_date:frm.doc.pay_end_date || '',
                		        from_date:frm.doc.pay_start_date ||''
                		    },
                		    callback(r){
                		        if(r.message>0){
                		            frm.set_value("no_of_days_worked",r.message)
                		        }
                		        else{
                		            frm.set_value("no_of_days_worked",0)
                		        }
                		    }
                		})
                    }
                }
            })
                   
            frappe.call({
                method: "tsl.tsl.doctype.full_and_final_settlement.full_and_final_settlement.get_current_month_date",
                args: {
                    'employee': frm.doc.employee,
                },
                callback: function (d) {
                    if (d.message) {
                        if(frm.doc.company == "TSL COMPANY - Kuwait"){
                            frm.set_value('total_working_days', 26)
                        }
                        else{
                            frm.set_value('total_working_days', d.message)
                        }
                    }
                }
            })
        }
    },
    absent_days(frm){
        frm.trigger("leaves_calculation")
        frm.trigger("encashed_leaves")
        frm.trigger("net_pay")
    },
    amount(frm){
        frm.trigger("leaves_calculation")
        frm.trigger("encashed_leaves")
    },
    encashed_leaves(frm) {
        var cal = ((frm.doc.basic_salary / frm.doc.total_working_days) * frm.doc.encashed_leaves)
        frm.set_value('leave_pay', cal.toFixed(2))
        frm.trigger("leaves_calculation")
        frm.trigger("net_pay")
    },
    additions(frm){
        frm.trigger("encashed_leaves")
    },
    loan_other_deduction(frm){
        frm.trigger("encashed_leaves")
    },
})
