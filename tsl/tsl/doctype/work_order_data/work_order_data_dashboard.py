from __future__ import unicode_literals

from frappe import _


def get_data():
	return {
		'fieldname': 'work_order_data',
		'non_standard_fieldnames': {
			'Quotation': 'wod_no',
		},
		'transactions': [
			{
				'label': _(''),
				'items': ['Quotation']
			},
			{
                                'label': _(''),
                                'items': ['Part Sheet']
                        },
			{
				'label': _(''),
				'items': ['Evaluation Report']
			}
		]
	}
