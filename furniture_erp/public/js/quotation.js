// Copyright (c) 2026, abhishek and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quotation", {
	refresh(frm) {
		if (frm.doc.furniture_job_file) {
			frm.add_custom_button(__("Open Job File"), () => {
				frappe.set_route("Form", "Furniture Job File", frm.doc.furniture_job_file);
			}, __("Furniture"));
		}
	},
});
