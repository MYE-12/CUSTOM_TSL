from __future__ import unicode_literals

from frappe import _


def get_data():
	return {
		'fieldname': 'work_order_data',
		'non_standard_fieldnames': {
			'Quotation': 'wod_no',
		},
		# 'internal_links': {
		# 	'Quotation': ['quotation'],
		# 	# 'Supplier Quotation': ['items', 'supplier_quotation'],
		# 	# 'Project': ['items', 'project'],
		# },
		'transactions': [
			{
				'label': _(''),
				'items': ['Quotation']
			},
			{
				'label': _(''),
				'items': ['Evaluation Report']
			},
			{
				'label': _(''),
				'items': ['Request for Quotation']
			},
			{
				'label': _(''),
				'items': ['Supplier Quotation']
			},
			{
				'label': _(''),
				'items': ['Purchase Order']
			},
			{
				'label': _(''),
				'items': ['Sales Invoice']
			},
			{
				'label': _(''),
				'items': ['Delivery Note']
			},
			{
				'label': _(''),
				'items': ['Stock Entry']
			},


		]
	}
