// Copyright (c) 2016, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Work Order Status"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": "2023-09-23"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"width": "80",
		}

	],

	
	after_datatable_render: table_instance => {
		let data = table_instance.datamanager.data;
		let col = 16;
		for (let row = 0; row < data.length; ++row) {
			if (data[row]['status'] == 'NE-Need Evaluation') {
			table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#f04864'});
			}
			else if(data[row]['status'] == 'SP-Searching Parts'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#F08080'});

			}
			else if(data[row]['status'] == 'AP-Available Parts'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#ce67a0'});

			}
			else if(data[row]['status'] == 'A-Approved'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#00c251'});

			}
			else if(data[row]['status'] == 'C-Comparison'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#7c00a0'});

			}
			else if(data[row]['status'] == 'CC-Comparison Client'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#7c00a0'});

			}
			else if(data[row]['status'] == 'EP-Extra Parts'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#7ae150'});

			}
			else if(data[row]['status'] == 'NER-Need Evaluation Return'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#ff0000'});

			}
			else if(data[row]['status'] == 'P-Paid'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#0063c1'});

			}
			else if(data[row]['status'] == 'Q-Quoted'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#FDC27E'});

			}
			else if(data[row]['status'] == 'RNA-Return Not Approved'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#cccccc'});

			}
			else if(data[row]['status'] == 'RNAP-Return Not Approved Client'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#cccccc'});

			}
			else if(data[row]['status'] == 'RNP-Return No Parts'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#f6c82d'});

			}
			else if(data[row]['status'] == 'RNPC-Return No Parts Client'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#f6c82d'});

			}
			else if(data[row]['status'] == 'RNR-Return Not Repaired'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#faff00'});

			}
			else if(data[row]['status'] == 'RNRC-Return Not Repaired Client'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#faff00'});

			}
			else if(data[row]['status'] == 'RS-Repaired and Shipped'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#c3d7f0'});

			}
			else if(data[row]['status'] == 'RSC-Repaired and Shipped Client'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#c3d7f0'});

			}
			else if(data[row]['status'] == 'TR-Technician Repair'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#ace0a8'});

			}
			else if(data[row]['status'] == 'W-Working'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#7c00a0'});

			}
			else if(data[row]['status'] == 'WP-Waiting Parts'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#FFFEB6'});

			}
			else if(data[row]['status'] == 'UE-Under Evaluation'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#ffaa00'});

			}
			else if(data[row]['status'] == 'IQ-Internally Quoted'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#aaff00'});

			}
			else if(data[row]['status'] == 'UTR-Under Technician Repair'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#ffaa00'});

			}
			else if(data[row]['status'] == 'RNF-Return No Fault'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#86a6ff'});

			}
			else if(data[row]['status'] == 'RNFC-Return No Fault Client'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#6176ff'});

			}
			else if(data[row]['status'] == 'RSI-Repaired and Shipped Invoiced'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#6176ff'});

			}

			else if(data[row]['status'] == 'RNAC-Return Not Approved Client'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#FF9195'});

			}

			else if(data[row]['status'] == 'RNAC-Return Not Approved Client'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#FF9195'});

			}

			else if(data[row]['status'] == 'CT-Customer Testing'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#FB9DF3'});

			}

			else if(data[row]['status'] == 'Pending Internal Approval'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#D3FFF5'});

			}

			else if(data[row]['status'] == 'Parts Priced'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#EBEBBC'});

			}
		

		}
	    table_instance.style.setStyle(`.dt-scrollable`, {height: '600px;'});
	 
    }

};

