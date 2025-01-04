// Copyright (c) 2024, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Rejoining Form', {
	actual_rejoining_date(frm) {
		frappe.call({
		    method:"tsl.tsl.doctype.leave_rejoining_form.leave_rejoining_form.get_number_of_leave_days",
		    args:{
		        employee:frm.doc.emp_no,
		        
		        to_date:frm.doc.actual_rejoining_date || '',
		        from_date:frm.doc.rejoining_date ||''
		    },
		    callback(r){
		        if(r.message>0){
		            frm.set_value("late_days",r.message -1)
		        }
		        else{
		            frm.set_value("late_days",0)
		        }
		    }
		})
	},
	refresh(frm){
		if(frm.doc.emp_no){
			let today = new Date().toISOString().split('T')[0];
			frappe.call({
				method: "hrms.hr.doctype.leave_application.leave_application.get_leave_details",
				async: false,
				args: {
					employee: frm.doc.emp_no,
					date: today,
				},
				callback: function (r) {
					let leave_details = r.message["leave_allocation"];
					let lwps = r.message["lwps"];
					frm.get_field("leave_balance").$wrapper.html(renderLeaveDetailsTable(leave_details))
					
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
	}
})



function renderLeaveDetailsTable(data) {
    if (jQuery.isEmptyObject(data)) {
        return `<p style="margin-top: 30px;">${__("No leaves have been allocated.")}</p>`;
    }

    let tableHTML = `
        <table class="table table-bordered small">
            <thead>
                <tr>
                    <th style="width: 16%">${__("Leave Type")}</th>
                    <th style="width: 16%" class="text-right">${__("Total Allocated Leaves")}</th>
                    <th style="width: 16%" class="text-right">${__("Expired Leaves")}</th>
                    <th style="width: 16%" class="text-right">${__("Used Leaves")}</th>
                    <th style="width: 16%" class="text-right">${__("Leaves Pending Approval")}</th>
                    <th style="width: 16%" class="text-right">${__("Available Leaves")}</th>
                </tr>
            </thead>
            <tbody>
    `;

    for (const [key, value] of Object.entries(data)) {
        let color = parseInt(value["remaining_leaves"]) > 0 ? "green" : "red";
        tableHTML += `
            <tr>
                <td>${key}</td>
                <td class="text-right">${value["total_leaves"]}</td>
                <td class="text-right">${value["expired_leaves"]}</td>
                <td class="text-right">${value["leaves_taken"]}</td>
                <td class="text-right">${value["leaves_pending_approval"]}</td>
                <td class="text-right" style="color: ${color}">${value["remaining_leaves"]}</td>
            </tr>
        `;
    }

    tableHTML += `
            </tbody>
        </table>
    `;
    return tableHTML;
}