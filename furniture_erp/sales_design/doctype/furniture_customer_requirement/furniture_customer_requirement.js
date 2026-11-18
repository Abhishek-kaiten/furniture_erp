// Copyright (c) 2026, abhishek and contributors
// For license information, please see license.txt

frappe.ui.form.on("Furniture Customer Requirement", {
	refresh(frm) {
		if (frm.doc.furniture_job_file) {
			frm.add_custom_button(__("Open Job File"), () => {
				frappe.set_route("Form", "Furniture Job File", frm.doc.furniture_job_file);
			});
		} else if (!frm.is_new()) {
			frm.add_custom_button(__("Create Job File"), () => {
				frappe.call({
					method: "furniture_erp.sales_design.api.get_or_create_job_file",
					args: { requirement: frm.doc.name },
					freeze: true,
					callback(r) {
						if (r.message) {
							frm.reload_doc();
							frappe.set_route("Form", "Furniture Job File", r.message);
						}
					},
				});
			});
		}

		if (!frm.is_new() && frm.doc.customer) {
			frm.add_custom_button(__("Create Quotation"), () => {
				frappe.call({
					method: "furniture_erp.sales_design.api.create_quotation_from_requirement",
					args: { requirement: frm.doc.name },
					freeze: true,
					callback(r) {
						if (r.message) {
							frappe.set_route("Form", "Quotation", r.message);
						}
					},
				});
			}, __("Create"));
		}
	},

	opportunity(frm) {
		if (!frm.doc.opportunity) return;
		frappe.db.get_doc("Opportunity", frm.doc.opportunity).then((opp) => {
			if (opp.opportunity_from === "Customer" && opp.party_name) {
				frm.set_value("customer", opp.party_name);
			}
			if (opp.opportunity_from === "Lead" && opp.party_name) {
				frm.set_value("lead", opp.party_name);
			}
			if (opp.furniture_project_type) {
				frm.set_value("project_type", opp.furniture_project_type);
			}
			if (opp.furniture_project_location) {
				frm.set_value("project_location", opp.furniture_project_location);
			}
			if (opp.furniture_project_budget) {
				frm.set_value("customer_budget", opp.furniture_project_budget);
			}
		});
	},
});
