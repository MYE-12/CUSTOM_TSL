def get_data():
	return {
		'fieldname': 'supply_order_data',
		
		# 'internal_links': {
			
		# 	'Request for Quotation': ['items', 'request_for_quotation'],
			
		# },
		'transactions': [
			{
				'items': ['Request for Quotation']
			},
			{
				'items': ['Supplier Quotation']
			},
			{
				'items' : ['Quotation']
			},
			{
				'items' : ['Purchase Order']
			},
			{
				
				'items': ['Sales Invoice']
			},
			{
				
				'items': ['Delivery Note']
			},
			{
				
				'items': ['Payment Entry']
			}
		]
	}
