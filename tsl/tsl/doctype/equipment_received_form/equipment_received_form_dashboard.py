from __future__ import unicode_literals

from frappe import _

def get_data():
	return {
		'fieldname': 'equipment_recieved_form',
		'transactions': [
			{
				'label': _(''),
				'items': ['Work Order Data']
			}
		]
	}
