from __future__ import unicode_literals

from frappe import _

def get_data():
	return {
		'fieldname': 'equipment_recieved_form',
		'non_standard_fieldnames': {
			'Stock Entry': 'equipment_received_form'
			
		},
		'transactions': [
			{
				'label': _(''),
				'items': ['Work Order Data']
			},
			{
				'label': _(''),
				'items': ['Stock Entry']
			}
		]
	}
