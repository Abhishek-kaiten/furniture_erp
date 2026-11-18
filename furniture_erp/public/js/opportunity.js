// Copyright (c) 2026, abhishek and contributors
// For license information, please see license.txt

frappe.ui.form.on("Opportunity", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Create / Open Requirement"), () => {
				frappe.call({
					method: "furniture_erp.sales_design.api.create_requirement_from_opportunity",
					args: { opportunity: frm.doc.name },
					freeze: true,
					callback(r) {
						if (r.message) {
							frm.reload_doc();
							frappe.set_route("Form", "Furniture Customer Requirement", r.message);
						}
					},
				});
			}, __("Furniture"));
		}
		if (frm.doc.furniture_job_file) {
			frm.add_custom_button(__("Open Job File"), () => {
				frappe.set_route("Form", "Furniture Job File", frm.doc.furniture_job_file);
			}, __("Furniture"));
		}
		if (frm.doc.furniture_customer_requirement) {
			frm.add_custom_button(__("Open Requirement"), () => {
				frappe.set_route(
					"Form",
					"Furniture Customer Requirement",
					frm.doc.furniture_customer_requirement
				);
			}, __("Furniture"));
		}
	},
});
