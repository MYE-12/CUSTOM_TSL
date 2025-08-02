frappe.ready(() => {
    // Exclude Administrator
    if (frappe.session.user === "Administrator") return;

    // Avoid duplicate prompts
    if (sessionStorage.getItem("password_check_done") === "1") return;

    frappe.call({
        method: "frappe.client.get_value",
        args: {
            doctype: "User",
            filters: { name: frappe.session.user },
            fieldname: ["last_password_reset_date", "creation"]
        },
        callback: function(res) {
            if (!res.message) return;

            let pwd_date = res.message.last_password_reset_date || res.message.creation;
            let days = frappe.datetime.get_diff(frappe.datetime.nowdate(), pwd_date);

            if (days > 90) {
                sessionStorage.setItem("password_check_done", "1");

                frappe.msgprint({
                    title: __("Security Alert"),
                    message: __("Your password is older than 90 days. Please change it now."),
                    indicator: "red",
                    primary_action: {
                        label: __("Change Password"),
                        action() {
                            window.location.href = "/update-password";
                        }
                    }
                });
            }
        }
    });
});
