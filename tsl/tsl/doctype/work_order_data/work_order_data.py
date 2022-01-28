# Copyright (c) 2021, Tsl and contributors
# For license information, please see license.txt

from codecs import ignore_errors
from pydoc import doc
import frappe
from frappe.model.document import Document
from frappe.utils import getdate,today
from datetime import datetime,date
from frappe.utils.data import (
	add_days,
	add_months,
	add_to_date,
	date_diff,
	flt,
	get_date_str,
	nowdate,
)



@frappe.whitelist()
def get_item_image(erf_no):
	image = frappe.db.sql('''select image from `tabRecieved Equipment Image` where parent = %s order by idx limit 1''',erf_no,as_dict=1)
	if image:
		return image[0]['image']


@frappe.whitelist()
def create_part_sheet(work_order):
	doc = frappe.get_doc("Work Order Data",work_order)
	new_doc= frappe.new_doc("Part Sheet")
	new_doc.work_order_data = doc.name
	new_doc.customer = doc.customer
	new_doc.customer_name = doc.customer_name
	new_doc.technician = doc.technician
	new_doc.item = doc.material_list[0].item_name
	new_doc.manufacturer = doc.material_list[0].mfg
	new_doc.model = doc.material_list[0].model_no
	return new_doc

@frappe.whitelist()
def create_evaluation_report(doc_no):
	doc = frappe.get_doc("Work Order Data",doc_no)
	new_doc = frappe.new_doc("Evaluation Report")
	new_doc.customer = doc.customer
	new_doc.attn = doc.technician
	new_doc.work_order_data = doc.name
	for i in doc.get("material_list"):
		new_doc.append("evaluation_details",{
			"item":i.item_name,
			"description":i.type,
			"manufacturer":i.mfg,
			"model":i.model_no,
			"serial_no":i.serial_no

		})
	new_doc.item_photo = doc.image
	return new_doc

@frappe.whitelist()
def create_extra_ps(doc):
	l=[]
	extra_ps = frappe.db.sql('''select name,technician from `tabPart Sheet` where work_order_data = %s order by creation''',doc,as_dict=1)
	for i in range(1,len(extra_ps)):
		l.append(extra_ps[i])
	return l

@frappe.whitelist()
def create_status_duration(wod):
	print("\n\n\n\n")
	print(wod)
	doc = frappe.get_doc("Work Order Data",wod)
	print(len(doc.status_duration_details))
	return(doc.status_duration_details[len(doc.status_duration_details-1)])
	

	
class WorkOrderData(Document):
	def on_update_after_submit(self):
		print("\n\n\n\n")
		print("on_update..........")
		print(len(self.status_duration_details))
		if self.status != self.status_duration_details[-1].status:
			ldate = self.status_duration_details[-1].date
			now = datetime.now()
			time_date = str(ldate).split(".")[0]
			format_data = "%Y-%m-%d %H:%M:%S"
			date = datetime.strptime(time_date, format_data)
			duration = now - date
			duration_in_s = duration.total_seconds()
			minutes = divmod(duration_in_s, 60)[0]/60
			data = str(minutes).split(".")[0]+"hrs "+str(minutes).split(".")[1]+"min"
			frappe.db.set_value("Status Duration Details",self.status_duration_details[-1].name,"duration",data)
			doc = frappe.get_doc("Work Order Data",self.name)
			doc.append("status_duration_details",{
				"status":self.status,
				"date":now,
			})
			print(data)
			doc.save(ignore_permissions=True)
		# # for i in range(len(self.status_duration_details)):
		# now = datetime.now()
		# current_time = now.strftime("%H:%M:%S")
		# self.append("status_duration_details",{
		# 	"status":self.status,
		# 	"date":now,
		# 	"time":current_time,
		
		# })


	# def on_change(self):
	# 	print("\n\n\n\n")
	# 	print("on_change")
	# 	print(self.status)
	# 	print(len(self.status_duration_details))
		
		
			
		# for i in self.get("status_duration_details"):
		# 	if i.idx == len(self.status_duration_details)-1:
		# 		self.append("status_duration_details",{
		# 				"duration":data,
						
		# 			})
		# 		break
		# self.save(ignore_permissions = True)
		


	
	def before_submit(self):
		print("before submit............")
		if not self.technician:
			frappe.throw("Assign a Technician to Submit")
		if not self.department:
			frappe.throw("Set Department to Submit")
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		self.status_duration_details =[]
		self.append("status_duration_details",{
			"status":self.status,
			"date":now,
		})

	

