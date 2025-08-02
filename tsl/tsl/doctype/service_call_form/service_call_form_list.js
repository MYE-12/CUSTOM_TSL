frappe.listview_settings['Service Call Form'] = {
	add_fields: ["status","name"],
	refresh:function(){
		//console.log("DSS")
		//if(frappe.user.has_role("Technician") && frappe.session.user !="Administrator" ){
		//console.log("HTD")
		//listview.page.fields_dict.status.value = "NE-Need Evaluation"
		//listview.page.fields_dict.status.refresh()
		//}
		// cur_list.page.clear_primary_action()
     	},
	

	get_indicator: function (doc) {
		if (doc.status === "Service Enquiry") {
			return [__("Service Enquiry"), "yellow", "status,=,Service Enquiry"];

		} else if (doc.status === "Internally Quoted") {
			return [__("Internally Quoted"), "orange", "status,=,Internally Quoted"];
                  
		} else if (doc.status === "Quoted") {
			return [__("Quoted"), "yellow", "status,=,Quoted"];
            }
        else if (doc.status === "Rejected") {
                    return [__("Rejected"), "green", "status,=,Rejected"];
        }
        else if (doc.status === "Invoiced") {
            return [__("Invoiced"), "green", "status,=,Invoiced"];
    	}
		else if (doc.status === "Approved") {
            return [__("Approved"), "green", "status,=,Approved"];
    	}

		else if (doc.status === "Not Succeed") {
            return [__("Not Succeed"), "red", "status,=,Not Succeed"];
    	}

		else if (doc.status === "Cancelled") {
            return [__("Cancelled"), "red", "status,=,Cancelled"];
    	}
		
            
          
          
      },
};
