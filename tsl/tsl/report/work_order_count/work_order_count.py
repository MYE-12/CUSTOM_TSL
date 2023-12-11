# Copyright (c) 2023, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data
def get_columns(filters):
    columns = []
    columns += [
        _("Status") + ":Data/:150",_("Count") + ":Data/:200",
    ]
  
    
    return columns

def get_data(filters):
    data = []
    wo_status = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'RS-Repaired and Shipped'""")
    wo_status1 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'NE-Need Evaluation'""")
    wo_status2 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'UE-Under Evaluation'""")
    wo_status3 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'AP-Available Parts'""")
    wo_status4 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'C-Comparison'""")
    wo_status5 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'WP-Waiting Parts'""")
    wo_status6 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'SP-Searching Parts'""")
    wo_status7 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'A-Approved'""")
    wo_status8 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'Q-Quoted'""")
    wo_status9 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'Pending Internal Approval'""")
    wo_status11 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'EP-Extra Parts'""")
    wo_status12 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'UTR-Under Technician Repair'""")
    wo_status13 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'W-Working'""")
    wo_status14 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'Parts Priced'""")
    wo_status15 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'CT-Customer Testing'""")
    wo_status16 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'IQ-Internally Quoted'""")
    wo_status17 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'NER-Need Evaluation Return'""")
    wo_status18 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'P-Paid'""")
    wo_status19 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'RNA-Return Not Approved'""")
    wo_status20 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'RNAC-Return Not Approved Client'""")
    wo_status22 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'RNF-Return No Fault'""")
    wo_status23 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'RNFC-Return No Fault Client'""")
    wo_status24 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'RNP-Return No Parts'""")
    wo_status25 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'RNPC-Return No Parts Client'""")
    wo_status26 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'RNR-Return Not Repaired'""")
    wo_status27 = frappe.db.sql("""select status,count(name) from `tabWork Order Data` where status = 'RNRC-Return Not Repaired Client'""")
    frappe.errprint(wo_status)
    for wo in wo_status:
          data.append(wo)
    for wo1 in wo_status1:
          data.append(wo1)
    for wo1 in wo_status2:
          data.append(wo1)
    for wo1 in wo_status3:
          data.append(wo1)
    for wo in wo_status4:
          data.append(wo)
    for wo1 in wo_status5:
          data.append(wo1)
    for wo1 in wo_status6:
          data.append(wo1)
    for wo1 in wo_status7:
          data.append(wo1)
    for wo in wo_status8:
          data.append(wo)
    for wo1 in wo_status9:
          data.append(wo1)
    for wo1 in wo_status12:
          data.append(wo1)
    for wo1 in wo_status13:
          data.append(wo1)
    for wo in wo_status14:
          data.append(wo)
    for wo1 in wo_status15:
          data.append(wo1)
    for wo1 in wo_status16:
          data.append(wo1)
    for wo1 in wo_status17:
          data.append(wo1)
    for wo in wo_status18:
          data.append(wo)
    for wo1 in wo_status19:
          data.append(wo1)
    for wo1 in wo_status20:
          data.append(wo1)
    for wo1 in wo_status23:
          data.append(wo1)
    for wo in wo_status23:
          data.append(wo)
    for wo1 in wo_status24:
          data.append(wo1)
    for wo1 in wo_status25:
          data.append(wo1)
    for wo1 in wo_status26:
          data.append(wo1)
    for wo1 in wo_status27:
          data.append(wo1)
    return data
    




