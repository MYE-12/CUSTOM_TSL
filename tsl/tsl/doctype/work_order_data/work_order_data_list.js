frappe.listview_settings['Work Order Data'] = {
	add_fields: ["status","name"],
	get_indicator: function (doc) {
		if (doc.status === "UE-Under Evaluation") {
			return [__("UE-Under Evaluation"), "blue", "status,=,UE-Under Evaluation"];

		} else if (doc.status === "AP-Available Parts") {
			return [__("AP-Available Parts"), "orange", "status,=,AP-Available Parts"];
		} else if (doc.status === "SP-Searching Parts") {
			return [__("SP-Searching Parts"), "yellow", "status,=,SP-Searching Parts"];
        }
        else if (doc.status === "Q-Quoted") {
			return [__("Q-Quoted"), "green", "status,=,Q-Quoted"];
        }
        else if (doc.status === "IQ-Internally Quoted") {
			return [__("IQ-Internally Quoted"), "cyan", "status,=,IQ-Internally Quoted"];
        }
        else if (doc.status === "RNP-Return No Parts") {
			return [__("RNP-Return No Parts"), "grey", "status,=,RNP-Return No Parts"];
        }
        else if (doc.status === "A-Approved") {
			return [__("A-Approved"), "green", "status,=,A-Approved"];
        }
        else if (doc.status === "RNA-Return Not Approved") {
			return [__("RNA-Return Not Approved"), "grey", "status,=,RNA-Return Not Approved"];
        }
        else if (doc.status === "TR-Technician Repair") {
			return [__("TR-Technician Repair"), "yellow", "status,=,TR-Technician Repair"];
        }
        else if (doc.status === "RSC-Repaired and Shipped Client") {
			return [__("RSC-Repaired and Shipped Client"), "green", "status,=,RSC-Repaired and Shipped Client"];
        }
        else if (doc.status === "WP-Waiting Parts") {
			return [__("WP-Waiting Parts"), "cyan", "status,=,WP-Waiting Parts"];
        }
        else if (doc.status === "EP-Extra Parts") {
			return [__("EP-Extra Parts"), "pink", "status,=,EP-Extra Parts"];
        }
        else if (doc.status === "RNAC-Return Not Approved Client") {
			return [__("RNAC-Return Not Approved Client"), "darkgrey", "status,=,RNAC-Return Not Approved Client"];
        }
        else if (doc.status === "RS-Repaired and Shipped") {
			return [__("RS-Repaired and Shipped"), "green", "status,=,RS-Repaired and Shipped"];
        }
        else if (doc.status === "RNR-Return Not Repaired") {
			return [__("RNR-Return Not Repaired"), "grey", "status,=,RNR-Return Not Repaired"];
        }
        else if (doc.status === "RNRC-Return Not Repaired Client") {
			return [__("RNRC-Return Not Repaired Client"), "darkgrey", "status,=,RNRC-Return Not Repaired Client"];
        }
        else if (doc.status === "W-Working") {
			return [__("W-Working"), "lightblue", "status,=,W-Working"];
        }
        else if (doc.status === "P-Paid") {
			return [__("P-Paid"), "green", "status,=,P-Paid"];
        }
        else if (doc.status === "C-Comparison") {
			return [__("C-Comparison"), "cyan", "status,=,C-Comparison"];
        }
        else if (doc.status === "CC-Comparison Client") {
			return [__("CC-Comparison Client"), "pink", "status,=,CC-Comparison Client"];
        }
        else if (doc.status === "NER-Need Evaluation Return") {
			return [__("NER-Need Evaluation Return"), "yellow", "status,=,NER-Need Evaluation Return"];
        }
        else if (doc.status === "RNPC-Return No Parts Client") {
			return [__("RNPC-Return No Parts Client"), "darkgrey", "status,=,RNPC-Return No Parts Client"];
        }
        // else if(doc.docstatus==0){
        //     return [__("NE-Need Evaluation"), "blue", "status,=,NE-Need Evaluation"];
        // }
 },
	
};
