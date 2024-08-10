# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

from datetime import date,datetime
from genericpath import exists
import json
import re
import frappe
from frappe.model.document import Document
from frappe.utils import cstr
from frappe.utils.data import add_days, today

class WorkOrderStatusLive(Document):
	pass

@frappe.whitelist()
def wod():
    country = get_country_by_ip()
    if country:
        frappe.errprint(country)


    today = date.today()
    date_obj = datetime.strptime(str(today), "%Y-%m-%d")

    # Format the datetime object to the desired string format
    formatted_date = date_obj.strftime("%d-%m-%Y")
    obj = datetime.strptime(str(formatted_date), "%d-%m-%Y")
    formatted= obj.strftime("%-d %b %Y")
    now = datetime.now()
    frappe.errprint(datetime.now())
    current_hour = now.hour
    current_minute = now.minute
    time = str(current_hour) + ":" + str(current_minute)

    data = {}
    wd = frappe.db.sql(""" select `tabUser`.full_name,`tabMaterial List`.item_name,`tabWork Order Data`.name,
	`tabWork Order Data`.sales_rep,`tabWork Order Data`.technician,
	`tabWork Order Data`.status from `tabWork Order Data` 
	left join `tabMaterial List` on `tabWork Order Data`.name = `tabMaterial List`.parent 
    right join `tabUser` on `tabUser`.name = `tabWork Order Data`.technician
	where `tabWork Order Data`.company = "TSL COMPANY - Kuwait" """,as_dict=1)
	# wd = frappe.get_all("Work Order Data",{"company":"TSL COMPANY - Kuwait"},["*"])
	# frappe.errprint(wd)
    data.update({
		"wod":wd,
		"due_date":formatted_date,
        "date":formatted,
        "time":time
	})
    return data

def get_country_by_ip():
    try:
        # Get the IP address information from ipinfo.io
        response = requests.get('https://ipinfo.io')
        data = response.json()
        
        # Extract the country information
        country = data.get('country')
        return country
    except Exception as e:
        print(f"Error: {e}")
        return None