// Copyright (c) 2026, abhishek and contributors
// For license information, please see license.txt

frappe.ui.form.on("Furniture Job File", {
	refresh(frm) {
		const html = frm.doc.__onload && frm.doc.__onload.linked_documents_html;
		if (html && frm.fields_dict.linked_documents_html) {
			frm.fields_dict.linked_documents_html.$wrapper.html(html);
		}

		if (!frm.is_new() && frm.doc.customer_requirement && !frm.doc.quotation) {
			frm.add_custom_button(__("Create Quotation"), () => {
				frappe.call({
					method: "furniture_erp.sales_design.api.create_quotation_from_requirement",
					args: { requirement: frm.doc.customer_requirement },
					freeze: true,
					callback(r) {
						if (r.message) {
							frm.reload_doc();
							frappe.set_route("Form", "Quotation", r.message);
						}
					},
				});
			}, __("Create"));
		}
	},
});
