# Copyright (c) 2025, Tsl and contributors
# For license information, please see license.txt


from itertools import groupby

import frappe
from frappe import _
from frappe.utils import add_days, cint, flt, getdate

from hrms.hr.doctype.leave_allocation.leave_allocation import get_previous_allocation
from hrms.hr.doctype.leave_application.leave_application import (
	get_leave_balance_on,
	get_leaves_for_period,
)

Filters = frappe._dict


def execute(filters: Filters | None = None) -> tuple:
	if filters.to_date <= filters.from_date:
		frappe.throw(_('"From Date" can not be greater than or equal to "To Date"'))

	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	columns = [
		{
			"label": _("Leave Type"),
			"fieldtype": "Link",
			"fieldname": "leave_type",
			"width": 200,
			"options": "Leave Type",
		},
		{
			"label": _("Employee"),
			"fieldtype": "Link",
			"fieldname": "employee",
			"width": 250,
			"options": "Employee",
		},
		{
			"label": _("Employee Name"),
			"fieldtype": "Dynamic Link",
			"fieldname": "employee_name",
			"width": 250,
			"options": "employee",
		},
		{
			"label": _("Available Leaves"),
			"fieldtype": "float",
			"fieldname": "closing_balance",
			"width": 200,
		}
	]
	if filters.get("type") == "Leave Payment":
		columns.extend([
			{
				"label": _("Leave Payment"),
				"fieldtype": "float",
				"fieldname": "leave_payment",
				"width": 200,
			},
		])
	if filters.get("type") == "Availed Leaves":
		columns.extend([
			{
				"label": _("Availed Annual Leaves"),
				"fieldtype": "float",
				"fieldname": "availed_leaves",
				"width": 200,
			},
			{
				"label": _("Annual Leave Payment"),
				"fieldtype": "float",
				"fieldname": "annual_leave_payment",
				"width": 200,
			},
		])

	return columns


def get_data(filters: Filters) -> list:
	leave_types = get_leave_types()
	active_employees = get_employees(filters)

	precision = cint(frappe.db.get_single_value("System Settings", "float_precision"))
	consolidate_leave_types = len(active_employees) > 1 and filters.consolidate_leave_types
	row = None

	data = []

	for leave_type in leave_types:
		if consolidate_leave_types:
			data.append({"leave_type": leave_type})
		else:
			row = frappe._dict({"leave_type": leave_type})

		for employee in active_employees:
			if consolidate_leave_types:
				row = frappe._dict()
			else:
				row = frappe._dict({"leave_type": leave_type})

			row.employee = employee.name
			row.employee_name = employee.employee_name

			leaves_taken = (
				get_leaves_for_period(employee.name, leave_type, filters.from_date, filters.to_date) * -1
			)

			new_allocation, expired_leaves, carry_forwarded_leaves = get_allocated_and_expired_leaves(
				filters.from_date, filters.to_date, employee.name, leave_type
			)
			opening = get_opening_balance(employee.name, leave_type, filters, carry_forwarded_leaves)
			closing = new_allocation + opening - (flt(expired_leaves, precision) + leaves_taken)
			row.closing_balance = flt(closing, precision)
			working_days = frappe.db.get_value("Company Wise Payroll Days",{"company": filters.get("company")},"total_working_days")
			row.availed_leaves = 0
			row.annual_leave_payment = 0
			if employee.basic:
				row.leave_payment = round((flt(closing, precision)*(employee.basic/working_days)),2)
				if leave_type == "Annual Leave":
					row.availed_leaves = frappe.db.count("Attendance",{"docstatus":1,"employee":employee.name,"status": "On Leave","leave_type":"Annual Leave", "attendance_date": ("between", [filters.get("from_date"), filters.get("to_date")])}) or 0
					row.annual_leave_payment = round((row.availed_leaves * (employee.basic/working_days)),2)
			else:
				row.leave_payment = 0
				if leave_type == "Annual Leave":
					row.availed_leaves = frappe.db.count("Attendance",{"docstatus":1,"employee":employee.name,"status": "On Leave","leave_type":"Annual Leave", "attendance_date": ("between", [filters.get("from_date"), filters.get("to_date")])}) or 0
					row.annual_leave_payment = round((row.availed_leaves * (employee.basic/working_days)),2)
			row.indent = 1
			data.append(row)

	return data

def get_leave_types() -> list[str]:
	LeaveType = frappe.qb.DocType("Leave Type")
	return (frappe.qb.from_(LeaveType).select(LeaveType.name).orderby(LeaveType.name)).run(pluck="name")


def get_employees(filters: Filters) -> list[dict]:
	Employee = frappe.qb.DocType("Employee")
	query = frappe.qb.from_(Employee).select(
		Employee.name,
		Employee.employee_name,
		Employee.department,
		Employee.basic,
	)

	for field in ["company", "department"]:
		if filters.get(field):
			query = query.where(getattr(Employee, field) == filters.get(field))

	if filters.get("employee"):
		query = query.where(Employee.name == filters.get("employee"))

	if filters.get("employee_status"):
		query = query.where(Employee.status == filters.get("employee_status"))

	return query.run(as_dict=True)


def get_opening_balance(
	employee: str, leave_type: str, filters: Filters, carry_forwarded_leaves: float
) -> float:
	# allocation boundary condition
	# opening balance is the closing leave balance 1 day before the filter start date
	opening_balance_date = add_days(filters.from_date, -1)
	allocation = get_previous_allocation(filters.from_date, leave_type, employee)

	if (
		allocation
		and allocation.get("to_date")
		and opening_balance_date
		and getdate(allocation.get("to_date")) == getdate(opening_balance_date)
	):
		# if opening balance date is same as the previous allocation's expiry
		# then opening balance should only consider carry forwarded leaves
		opening_balance = carry_forwarded_leaves
	else:
		# else directly get leave balance on the previous day
		opening_balance = get_leave_balance_on(employee, leave_type, opening_balance_date)

	return opening_balance


def get_allocated_and_expired_leaves(
	from_date: str, to_date: str, employee: str, leave_type: str
) -> tuple[float, float, float]:
	new_allocation = 0
	expired_leaves = 0
	carry_forwarded_leaves = 0

	records = get_leave_ledger_entries(from_date, to_date, employee, leave_type)

	for record in records:
		# new allocation records with `is_expired=1` are created when leave expires
		# these new records should not be considered, else it leads to negative leave balance
		if record.is_expired:
			continue

		if record.to_date < getdate(to_date):
			# leave allocations ending before to_date, reduce leaves taken within that period
			# since they are already used, they won't expire
			expired_leaves += record.leaves
			leaves_for_period = get_leaves_for_period(employee, leave_type, record.from_date, record.to_date)
			expired_leaves -= min(abs(leaves_for_period), record.leaves)

		if record.from_date >= getdate(from_date):
			if record.is_carry_forward:
				carry_forwarded_leaves += record.leaves
			else:
				new_allocation += record.leaves

	return new_allocation, expired_leaves, carry_forwarded_leaves


def get_leave_ledger_entries(from_date: str, to_date: str, employee: str, leave_type: str) -> list[dict]:
	ledger = frappe.qb.DocType("Leave Ledger Entry")
	return (
		frappe.qb.from_(ledger)
		.select(
			ledger.employee,
			ledger.leave_type,
			ledger.from_date,
			ledger.to_date,
			ledger.leaves,
			ledger.transaction_name,
			ledger.transaction_type,
			ledger.is_carry_forward,
			ledger.is_expired,
		)
		.where(
			(ledger.docstatus == 1)
			& (ledger.transaction_type == "Leave Allocation")
			& (ledger.employee == employee)
			& (ledger.leave_type == leave_type)
			& (
				(ledger.from_date[from_date:to_date])
				| (ledger.to_date[from_date:to_date])
				| ((ledger.from_date < from_date) & (ledger.to_date > to_date))
			)
		)
	).run(as_dict=True)