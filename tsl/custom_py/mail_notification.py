import frappe

@frappe.whitelist()
def purchase_msg_to_info(com,branch,ev,sender):
    frappe.errprint(branch)
    frappe.errprint(com)
    info = ""
    if com == "TSL COMPANY - KSA":
        if branch == "Riyadh - TSL- KSA":
            info = "lab-sa@tsl-me.com"
        
        if branch == "Dammam - TSL-SA":
            info = "lab-dmm@tsl-me.com"
        
        if branch == "Jeddah - TSL-SA":
            info = "info-jed@tsl-me.com"

    frappe.sendmail(recipients=[info],
			sender = sender,
			subject="Part sheet Comments",
			message=""" <b>Dear Lab Coordinator,</b><br>
            Kindly find the comment for the Evaluation report  <b>%s</b> . Please take action to  <a href="https://erp.tsl-me.com/app/evaluation-report/%s"target="_blank">click here.</a>
		   
			""" %(ev,ev)
			)
    frappe.msgprint("Message sent Successfully")
            

    