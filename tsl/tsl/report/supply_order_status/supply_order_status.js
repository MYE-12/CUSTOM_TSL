// Copyright (c) 2016, Tsl and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Supply Order Status"] = {
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
		let col = 21;
		for (let row = 0; row < data.length; ++row) {
			if (data[row]['status'] == 'NE-Need Evaluation') {
			table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#f04864'});
			}
			else if(data[row]['status'] == 'SP-Searching Parts'){
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#938e52'});

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
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#f25b00'});

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
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: '#836300'});

			}
		}
	    table_instance.style.setStyle(`.dt-scrollable`, {height: '600px;'});
	 
    }
};
