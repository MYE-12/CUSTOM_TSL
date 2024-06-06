frappe.ui.form.on('Leave Application', {
	ticket_used(frm) {
	    if(frm.doc.ticket_used && frm.doc.no_of_tickets < frm.doc.ticket_used){
	        frappe.msgprint("Available Tickets <b>"+frm.doc.no_of_tickets+"</b> is lesser than - <b>"+ frm.doc.ticket_used+"</b>")
	        frappe.validated = false
	    }
	},
	validate(frm){
	    frm.trigger("ticket_used")
	}
})