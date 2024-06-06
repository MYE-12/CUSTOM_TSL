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
	}
})