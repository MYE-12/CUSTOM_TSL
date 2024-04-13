frappe.listview_settings['Supply Order Data'] = {
	add_fields: ["status","name"],
	get_indicator: function (doc) {
	if (doc.status === "Inquiry") {
		return [__("Inquiry"), "blue", "status,=,Inquiry"];

	}
      else if (doc.status === "Searching Items") {
		return [__("Searching Items"), "yellow", "status,=,Searching Items"];

	} else if (doc.status === "Not Found") {
		return [__("Not Found"), "red", "status,=,Not Found"];
	}
       else if (doc.status === "Internal Quotation") {
		return [__("Internal Quotation"), "orange", "status,=,Internal Quotation"];
        }
        
        else if (doc.status === "Quoted") {
			return [__("Quoted"), "green", "status,=,Quoted"];
        }
        else if (doc.status === "Approved") {
			return [__("Approved"), "green", "status,=,Approved"];
        }
        else if (doc.status === "Not Approved") {
			return [__("Not Approved"), "red", "status,=,Not Approved"];
        }
        else if (doc.status === "Ordered") {
			return [__("Ordered"), "cyan", "status,=,Ordered"];
        }
        else if (doc.status === "Shipped") {
			return [__("Shipped"), "pink", "status,=,Shipped"];
        }
        else if (doc.status === "Received") {
			return [__("Received"), "yellow", "status,=,Received"];
        }
        else if (doc.status === "Paid") {
			return [__("Paid"), "green", "status,=,Paid"];
        }
        else if (doc.status === "Delivered and Invoiced") {
			return [__("Delivered and Invoiced"), "cyan", "status,=,Delivered and Invoiced"];
        }
        else if (doc.status === "Parts Priced") {
              return [__("Parts Priced"), "green", "status,=,Parts Priced"];
 }
        


        // else if(doc.docstatus==0){
        //     return [__("Inquiry"), "blue", "status,=,Inquiry"];
        // }
 },
	
};
