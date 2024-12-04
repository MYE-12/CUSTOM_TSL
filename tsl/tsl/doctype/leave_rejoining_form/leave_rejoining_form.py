# Copyright (c) 2024, Tsl and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import (
	add_days,
	today,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_fullname,
	get_link_to_form,
	getdate,now_datetime,
	nowdate,
	get_first_day,
	get_last_day
)


class LeaveRejoiningForm(Document):
	def on_submit(self):
		if self.leave_type:
			l_ap = frappe.new_doc("Leave Application")
			l_ap.rejoining = self.name
			l_ap.employee = self.emp_no
			l_ap.leave_type = self.leave_type
			l_ap.from_date = self.rejoining_date
			l_ap.to_date = self.actual_rejoining_date
			l_ap.save()


from hrms.hr.doctype.leave_application.leave_application import get_holidays
@frappe.whitelist()
def get_number_of_leave_days(
	employee: str,
	from_date: datetime.date,
	to_date: datetime.date,
	half_day: int | str | None = None,
	half_day_date: datetime.date | str | None = None,
	holiday_list: str | None = None,
) -> float:
	"""Returns number of leave days between 2 dates after considering half day and holidays
	(Based on the include_holiday setting in Leave Type)"""
	number_of_days = 0
	if cint(half_day) == 1:
		if getdate(from_date) == getdate(to_date):
			number_of_days = 0.5
		elif half_day_date and getdate(from_date) <= getdate(half_day_date) <= getdate(to_date):
			number_of_days = date_diff(to_date, from_date) + 0.5
		else:
			number_of_days = date_diff(to_date, from_date) + 1
	else:
		number_of_days = date_diff(to_date, from_date) + 1

	number_of_days = flt(number_of_days) - flt(
		get_holidays(employee, from_date, to_date, holiday_list=holiday_list)
	)
	return number_of_days