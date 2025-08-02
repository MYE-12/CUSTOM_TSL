// Copyright (c) 2025, Tsl and contributors
// For license information, please see license.txt

frappe.ui.form.on("ERF", {
	refresh(frm){
		if(!frm.doc.__islocal){
			frm.add_custom_button(__("Print"), function () {
				var f_name = frm.doc.name;
				var print_format = "ERF";
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("ERF")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}); 

			frm.add_custom_button(__("Create Work Order"), function () {		
				frappe.call({
					method: 'tsl.tsl.doctype.erf.erf.create_work_order_from_erf',
					args: {
						source_name: frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
                        let erf = r.message;

                        frappe.set_route('Form', 'Create Work Order Kuwait');

                        const interval = setInterval(() => {
                            if (cur_frm && cur_frm.doc.doctype === 'Create Work Order Kuwait') {
                                clearInterval(interval);

                                cur_frm.set_value('customer', erf.customer);
                                cur_frm.set_value('email', erf.email);
                                cur_frm.set_value('mobile', erf.mobile);
                                cur_frm.set_value('incharge', erf.incharge);
                                cur_frm.set_value('incharge_name', erf.incharge_name);
                                cur_frm.set_value('incharge_phone_no', erf.incharge_phone_no);
                                cur_frm.set_value('company', erf.company);
                                cur_frm.set_value('branch', erf.branch);
                                cur_frm.set_value('plant', erf.plant);
                                cur_frm.set_value('customer_reference_number', erf.customer_reference_number);
                                cur_frm.set_value('address', erf.address);
                                cur_frm.set_value('received_date', erf.received_date);
                                cur_frm.set_value('repair_warehouse', erf.repair_warehouse);
                                cur_frm.set_value('sales_person', erf.sales_person);
                                cur_frm.set_value('sts', erf.sts);

                                cur_frm.clear_table('received_equipment');
                                erf.received_equipment.forEach(row => {
                                    let new_row = cur_frm.add_child('received_equipment', {
                                        manufacturer: row.manufacturer,
                                        model: row.model,
                                        no_power: row.no_power,
                                        no_display: row.no_display,
                                        no_output: row.no_output,
                                        no_communication: row.no_communication,
                                        no_backlight: row.no_backlight,
                                        touchkeypad_not_working: row.touchkeypad_not_working,
                                        short_circuit: row.short_circuit,
                                        overloadovercurrent: row.overloadovercurrent,
                                        supply_voltage: row.supply_voltage,
                                        other: row.other,
                                    });
                                });

                                cur_frm.refresh_field('received_equipment');
                            }
                        }, 200);
                    }
					}
				});
			}); 
		}		
	},
	setup: function (frm) {
		frm.set_query("address", function () {
			return {
				filters: [
					["Dynamic Link", "parenttype", "=", "Address"],
					["Dynamic Link", "link_name", "=", frm.doc.customer],
					["Dynamic Link", "link_doctype", "=", "Customer"]

				]
			}
		});
		frm.set_query("branch", function () {
			return {
				filters: [
					["Branch", "company", "=", frm.doc.company]

				]
			}

		});
		frm.set_query("repair_warehouse", function () {
			return {
				filters: [
					["Warehouse", "company", "=", frm.doc.company],
				]
			}

		});
		var d = {
			"Kuwait - TSL": "Repair - Kuwait - TSL",
			"Dammam - TSL-SA": "Dammam - Repair - TSL - KSA",
			"Jeddah - TSL-SA": "Jeddah - Repair - TSL - KSA",
			"Riyadh - TSL- KSA": "Riyadh - Repair - TSL - KSA",
			"Dubai - TSL": "Dubai - Repair - TSL-UAE"
		}
		frm.set_value("repair_warehouse", d[frm.doc.branch]);
	},
	branch: function (frm) {
		if (frm.doc.company && frm.doc.branch) {
			var d = {
				"Kuwait - TSL": "ERF-K.YY.-",
				"Dammam - TSL-SA": "ERF-D.YY.-",
				"Jeddah - TSL-SA": "ERF-J.YY.-",
				"Riyadh - TSL- KSA": "ERF-R.YY.-",
				"Dubai - TSL": "ERF-DU.YY.-"
			}
			frm.set_value("naming_series", d[frm.doc.branch]);
		}
	}
});
