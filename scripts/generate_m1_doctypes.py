#!/usr/bin/env python3
"""Generate Milestone 1–2 DocType JSON/controllers for furniture_erp (Frappe-only safe)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "furniture_erp"


def field(**kwargs):
	return {k: v for k, v in kwargs.items() if v is not None}


def section(label, name=None):
	return field(fieldname=name or f"section_{label.lower().replace(' ', '_')}", fieldtype="Section Break", label=label)


def col(name):
	return field(fieldname=name, fieldtype="Column Break")


def write_doctype(module_path: Path, name: str, meta: dict, fields: list, permissions: list, py_extra: str = ""):
	slug = name.lower().replace(" ", "_")
	folder = module_path / "doctype" / slug
	folder.mkdir(parents=True, exist_ok=True)
	(folder / "__init__.py").write_text("")
	meta = {
		"doctype": "DocType",
		"name": name,
		"module": meta["module"],
		"engine": "InnoDB",
		"actions": [],
		"links": [],
		"states": [],
		"fields": fields,
		"permissions": permissions,
		"field_order": [f["fieldname"] for f in fields],
		**{k: v for k, v in meta.items() if k != "module"},
	}
	(folder / f"{slug}.json").write_text(json.dumps(meta, indent=1) + "\n")
	controller = f'''# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class {name.replace(" ", "")}(Document):
{py_extra or "	pass\n"}
'''
	(folder / f"{slug}.py").write_text(controller)
	(folder / f"{slug}.js").write_text(
		f'''// Copyright (c) 2026, abhishek and contributors
// For license information, please see license.txt

frappe.ui.form.on("{name}", {{
	refresh(frm) {{}}
}});
'''
	)


def perm(role, **flags):
	base = {
		"role": role,
		"read": 1,
		"write": 0,
		"create": 0,
		"delete": 0,
		"submit": 0,
		"cancel": 0,
		"amend": 0,
		"report": 1,
		"export": 1,
		"import": 0,
		"share": 0,
		"print": 1,
		"email": 0,
	}
	base.update(flags)
	return base


def settings_fields():
	return [
		section("Defaults"),
		field(fieldname="default_currency", fieldtype="Link", label="Default Currency", options="Currency", reqd=1, default="INR"),
		col("col_defaults_2"),
		field(fieldname="default_length_unit", fieldtype="Select", label="Default Length Unit", options="mm\ncm\ninch", reqd=1, default="mm"),
		col("col_defaults_3"),
		field(fieldname="default_area_unit", fieldtype="Select", label="Default Area Unit", options="sq m\nsq ft", default="sq m"),
		section("Naming Series"),
		field(fieldname="family_naming_series", fieldtype="Data", label="Product Family Naming Series", reqd=1, default="FPF-.#####"),
		col("col_ns_2"),
		field(fieldname="material_naming_series", fieldtype="Data", label="Material Naming Series", reqd=1, default="FMAT-.#####"),
		col("col_ns_3"),
		field(fieldname="finish_naming_series", fieldtype="Data", label="Finish Naming Series", reqd=1, default="FFIN-.#####"),
		field(fieldname="specification_naming_series", fieldtype="Data", label="Specification Naming Series", reqd=1, default="FSPEC-.YYYY.-.#####"),
		section("Catalogue Rules"),
		field(fieldname="enforce_allowed_materials", fieldtype="Check", label="Enforce Allowed Materials on Spec", default="1"),
		col("col_rules_2"),
		field(fieldname="enforce_allowed_finishes", fieldtype="Check", label="Enforce Allowed Finishes on Spec", default="1"),
		col("col_rules_3"),
		field(fieldname="allow_draft_spec_duplication", fieldtype="Check", label="Allow Duplicate Draft Specs", default="0"),
		field(fieldname="default_gst_hsn_code", fieldtype="Data", label="Default HSN Code"),
		field(fieldname="spec_requires_approval", fieldtype="Check", label="Specification Requires Approval", default="0"),
		section("Integration"),
		field(fieldname="enable_portal_catalogue", fieldtype="Check", label="Enable Portal Catalogue", default="0"),
		col("col_int_2"),
		field(fieldname="integration_webhook_url", fieldtype="Data", label="Integration Webhook URL", options="URL"),
		col("col_int_3"),
		field(
			fieldname="erpnext_note",
			fieldtype="Small Text",
			label="ERPNext Status Note",
			read_only=1,
			default="ERPNext is not installed on this site. Company/Item/Warehouse/Customer links are deferred until ERPNext is added.",
		),
	]


def family_fields():
	return [
		section("Identity"),
		field(fieldname="family_name", fieldtype="Data", label="Family Name", reqd=1, in_list_view=1, in_standard_filter=1, bold=1),
		col("col_id_2"),
		field(fieldname="family_code", fieldtype="Data", label="Family Code", in_list_view=1),
		col("col_id_3"),
		field(fieldname="status", fieldtype="Select", label="Status", options="Draft\nActive\nDiscontinued", reqd=1, default="Active", in_list_view=1, in_standard_filter=1),
		field(fieldname="description", fieldtype="Text Editor", label="Description"),
		field(fieldname="default_lead_time_days", fieldtype="Int", label="Default Lead Time (Days)"),
		section("Classification"),
		field(
			fieldname="product_category",
			fieldtype="Select",
			label="Product Category",
			options="Seating\nTables\nStorage\nKitchen\nBedroom\nOffice\nOutdoor\nOther",
			in_standard_filter=1,
		),
		col("col_cls_2"),
		field(
			fieldname="construction_type",
			fieldtype="Select",
			label="Construction Type",
			options="Panel\nSolid Wood\nHybrid\nUpholstered\nMetal",
		),
		col("col_cls_3"),
		field(fieldname="is_configurable", fieldtype="Check", label="Configurable", default="1", reqd=1),
		section("Media"),
		field(fieldname="hero_image", fieldtype="Attach Image", label="Hero Image"),
		field(fieldname="drawing_attachment", fieldtype="Attach", label="Reference Drawing"),
		section("Allowed Materials"),
		field(fieldname="allowed_materials", fieldtype="Table", label="Allowed Materials", options="Furniture Family Allowed Material"),
		section("Allowed Finishes"),
		field(fieldname="allowed_finishes", fieldtype="Table", label="Allowed Finishes", options="Furniture Family Allowed Finish"),
		field(fieldname="naming_series", fieldtype="Select", label="Series", options="FPF-.#####", hidden=1, default="FPF-.#####"),
	]


def material_fields():
	return [
		section("Identity"),
		field(fieldname="material_name", fieldtype="Data", label="Material Name", reqd=1, in_list_view=1, bold=1),
		col("col_m_2"),
		field(
			fieldname="material_type",
			fieldtype="Select",
			label="Material Type",
			options="Plywood\nMDF\nParticle Board\nHardwood\nHardware\nGlass\nStone\nOther",
			reqd=1,
			in_list_view=1,
			in_standard_filter=1,
		),
		col("col_m_3"),
		field(fieldname="status", fieldtype="Select", label="Status", options="Active\nInactive", reqd=1, default="Active", in_list_view=1),
		field(fieldname="grade", fieldtype="Data", label="Grade"),
		field(
			fieldname="linked_item_code",
			fieldtype="Data",
			label="Linked Item Code (ERPNext)",
			description="Forward-compatible Item code once ERPNext is installed.",
		),
		section("Physical"),
		field(fieldname="default_thickness_mm", fieldtype="Float", label="Default Thickness (mm)"),
		col("col_p_2"),
		field(fieldname="default_width_mm", fieldtype="Float", label="Default Width (mm)"),
		col("col_p_3"),
		field(fieldname="default_length_mm", fieldtype="Float", label="Default Length (mm)"),
		field(fieldname="weight_per_unit", fieldtype="Float", label="Weight per Unit"),
		field(
			fieldname="uom",
			fieldtype="Select",
			label="UOM",
			options="Nos\nSq Meter\nMeter\nKg\nSheet\nRoll",
			reqd=1,
			default="Nos",
		),
		field(fieldname="hsn_code", fieldtype="Data", label="HSN Code"),
		section("Costing Hints"),
		field(fieldname="reference_rate", fieldtype="Currency", label="Reference Rate"),
		col("col_c_2"),
		field(fieldname="currency", fieldtype="Link", label="Currency", options="Currency"),
		col("col_c_3"),
		field(fieldname="last_rate_updated_on", fieldtype="Date", label="Last Rate Updated On"),
		field(fieldname="naming_series", fieldtype="Select", label="Series", options="FMAT-.#####", hidden=1, default="FMAT-.#####"),
	]


def finish_fields():
	return [
		section("Identity"),
		field(fieldname="finish_name", fieldtype="Data", label="Finish Name", reqd=1, in_list_view=1, bold=1),
		col("col_f_2"),
		field(
			fieldname="finish_type",
			fieldtype="Select",
			label="Finish Type",
			options="Laminate\nVeneer\nPU Paint\nMelamine\nEdge Band\nPowder Coat\nFabric\nLeather\nOther",
			reqd=1,
			in_list_view=1,
			in_standard_filter=1,
		),
		col("col_f_3"),
		field(fieldname="status", fieldtype="Select", label="Status", options="Active\nInactive", reqd=1, default="Active", in_list_view=1),
		field(fieldname="finish_code", fieldtype="Data", label="Finish Code"),
		field(fieldname="linked_item_code", fieldtype="Data", label="Linked Item Code (ERPNext)"),
		section("Appearance and Process"),
		field(fieldname="color_name", fieldtype="Data", label="Color Name"),
		col("col_a_2"),
		field(fieldname="color_code", fieldtype="Data", label="Color / Shade Code"),
		col("col_a_3"),
		field(fieldname="gloss_level", fieldtype="Select", label="Gloss Level", options="\nMatte\nSatin\nGloss"),
		field(fieldname="grain_direction_required", fieldtype="Check", label="Grain Direction Required"),
		field(fieldname="curing_lead_time_days", fieldtype="Int", label="Curing Lead Time (Days)"),
		section("Compliance"),
		field(fieldname="voc_compliant", fieldtype="Check", label="Low VOC Compliant"),
		col("col_cmp_2"),
		field(fieldname="fire_rating", fieldtype="Data", label="Fire Rating"),
		col("col_cmp_3"),
		field(fieldname="hsn_code", fieldtype="Data", label="HSN Code"),
		section("Media"),
		field(fieldname="swatch_image", fieldtype="Attach Image", label="Swatch Image"),
		field(fieldname="naming_series", fieldtype="Select", label="Series", options="FFIN-.#####", hidden=1, default="FFIN-.#####"),
	]


def spec_fields():
	return [
		section("Header"),
		field(fieldname="naming_series", fieldtype="Select", label="Series", options="FSPEC-.YYYY.-.#####", reqd=1, default="FSPEC-.YYYY.-.#####"),
		col("col_h_2"),
		field(fieldname="spec_title", fieldtype="Data", label="Specification Title", reqd=1, in_list_view=1, bold=1),
		col("col_h_3"),
		field(
			fieldname="spec_status",
			fieldtype="Select",
			label="Status",
			options="Draft\nIn Review\nApproved\nRejected\nObsolete",
			reqd=1,
			default="Draft",
			in_list_view=1,
			in_standard_filter=1,
		),
		field(fieldname="product_family", fieldtype="Link", label="Product Family", options="Furniture Product Family", reqd=1, in_list_view=1, in_standard_filter=1),
		field(fieldname="version", fieldtype="Int", label="Version", reqd=1, default="1", read_only=1),
		field(fieldname="valid_from", fieldtype="Date", label="Valid From"),
		field(fieldname="valid_upto", fieldtype="Date", label="Valid Upto"),
		field(
			fieldname="customer_name",
			fieldtype="Data",
			label="Customer Name",
			description="Temporary until ERPNext Customer is available.",
		),
		field(fieldname="project_name", fieldtype="Data", label="Project Name"),
		section("Dimensions (outer)"),
		field(fieldname="width_mm", fieldtype="Float", label="Width (mm)", reqd=1, in_list_view=1),
		col("col_d_2"),
		field(fieldname="depth_mm", fieldtype="Float", label="Depth (mm)", reqd=1),
		col("col_d_3"),
		field(fieldname="height_mm", fieldtype="Float", label="Height (mm)", reqd=1),
		field(fieldname="weight_kg_est", fieldtype="Float", label="Estimated Weight (kg)"),
		section("Materials and Finishes"),
		field(fieldname="primary_material", fieldtype="Link", label="Primary Material", options="Furniture Material", reqd=1),
		col("col_mf_2"),
		field(fieldname="primary_finish", fieldtype="Link", label="Primary Finish", options="Furniture Finish", reqd=1),
		col("col_mf_3"),
		field(fieldname="secondary_finish", fieldtype="Link", label="Secondary Finish", options="Furniture Finish"),
		field(fieldname="edge_band_finish", fieldtype="Link", label="Edge Band Finish", options="Furniture Finish"),
		section("Manufacturing Links"),
		field(fieldname="target_item_code", fieldtype="Data", label="Target Item Code (ERPNext)"),
		col("col_ml_2"),
		field(fieldname="drawing_no", fieldtype="Data", label="Drawing Number"),
		col("col_ml_3"),
		field(fieldname="default_bom_name", fieldtype="Data", label="Default BOM Name (ERPNext)"),
		section("Attributes"),
		field(fieldname="attributes", fieldtype="Table", label="Attributes", options="Furniture Specification Attribute"),
		section("Notes"),
		field(fieldname="internal_notes", fieldtype="Text Editor", label="Internal Notes"),
		field(fieldname="customer_facing_notes", fieldtype="Text Editor", label="Customer Facing Notes"),
		field(fieldname="amended_from", fieldtype="Link", label="Amended From", options="Furniture Specification", read_only=1, no_copy=1, print_hide=1),
	]


FAMILY_VALIDATE = '''
	def validate(self):
		self._validate_single_default(self.allowed_materials, "material")
		self._validate_single_default(self.allowed_finishes, "finish")

	def _validate_single_default(self, rows, label):
		defaults = [row for row in (rows or []) if row.is_default]
		if len(defaults) > 1:
			frappe.throw(frappe._("Only one default {0} is allowed.").format(label))
'''

SPEC_VALIDATE = '''
	def validate(self):
		self._validate_dimensions()
		self._validate_allowlists()
		self._validate_approval_ready()

	def before_save(self):
		if self.amended_from and not self.flags.in_insert_from_amend:
			pass

	def _validate_dimensions(self):
		for fieldname, label in (("width_mm", "Width"), ("depth_mm", "Depth"), ("height_mm", "Height")):
			value = self.get(fieldname)
			if value is not None and value <= 0:
				frappe.throw(frappe._("{0} must be greater than zero.").format(label))

	def _settings(self):
		if frappe.db.exists("DocType", "Furniture ERP Settings"):
			return frappe.get_single("Furniture ERP Settings")
		return None

	def _validate_allowlists(self):
		settings = self._settings()
		if not settings or not self.product_family:
			return
		family = frappe.get_doc("Furniture Product Family", self.product_family)
		if settings.enforce_allowed_materials and self.primary_material:
			allowed = {row.material for row in family.allowed_materials or []}
			if allowed and self.primary_material not in allowed:
				frappe.throw(
					frappe._("Primary Material {0} is not allowed for family {1}.").format(
						self.primary_material, self.product_family
					)
				)
		if settings.enforce_allowed_finishes:
			allowed = {row.finish for row in family.allowed_finishes or []}
			if allowed:
				for fieldname, label in (
					("primary_finish", "Primary Finish"),
					("secondary_finish", "Secondary Finish"),
					("edge_band_finish", "Edge Band Finish"),
				):
					value = self.get(fieldname)
					if value and value not in allowed:
						frappe.throw(
							frappe._("{0} {1} is not allowed for family {2}.").format(
								label, value, self.product_family
							)
						)

	def _validate_approval_ready(self):
		if self.spec_status != "Approved":
			return
		missing = []
		for fieldname, label in (
			("width_mm", "Width"),
			("depth_mm", "Depth"),
			("height_mm", "Height"),
			("primary_material", "Primary Material"),
			("primary_finish", "Primary Finish"),
		):
			if not self.get(fieldname):
				missing.append(label)
		if missing:
			frappe.throw(frappe._("Cannot approve specification. Missing: {0}").format(", ".join(missing)))
'''


def main():
	setup = ROOT / "setup"
	catalogue = ROOT / "furniture_catalogue"
	(setup / "doctype").mkdir(parents=True, exist_ok=True)
	(catalogue / "doctype").mkdir(parents=True, exist_ok=True)
	(setup / "doctype" / "__init__.py").write_text("")
	(catalogue / "doctype" / "__init__.py").write_text("")

	write_doctype(
		setup,
		"Furniture ERP Settings",
		{
			"module": "Setup",
			"issingle": 1,
			"is_submittable": 0,
			"track_changes": 1,
			"icon": "setting",
		},
		settings_fields(),
		[
			perm("System Manager", write=1, create=1, delete=1, share=1),
			perm("Furniture ERP Administrator", write=1, create=1, share=1),
			perm("Furniture Product Manager", read=1, report=1),
		],
	)

	write_doctype(
		catalogue,
		"Furniture Family Allowed Material",
		{
			"module": "Furniture Catalogue",
			"istable": 1,
			"editable_grid": 1,
			"track_changes": 0,
		},
		[
			field(fieldname="material", fieldtype="Link", label="Material", options="Furniture Material", reqd=1, in_list_view=1),
			field(fieldname="is_default", fieldtype="Check", label="Default", in_list_view=1),
			field(fieldname="notes", fieldtype="Small Text", label="Notes"),
		],
		[],
	)

	write_doctype(
		catalogue,
		"Furniture Family Allowed Finish",
		{
			"module": "Furniture Catalogue",
			"istable": 1,
			"editable_grid": 1,
		},
		[
			field(fieldname="finish", fieldtype="Link", label="Finish", options="Furniture Finish", reqd=1, in_list_view=1),
			field(
				fieldname="application",
				fieldtype="Select",
				label="Application",
				options="\nCarcass\nShutter\nTop\nAll",
				in_list_view=1,
			),
			field(fieldname="is_default", fieldtype="Check", label="Default", in_list_view=1),
		],
		[],
	)

	write_doctype(
		catalogue,
		"Furniture Specification Attribute",
		{
			"module": "Furniture Catalogue",
			"istable": 1,
			"editable_grid": 1,
		},
		[
			field(fieldname="attribute_name", fieldtype="Data", label="Attribute", reqd=1, in_list_view=1),
			field(fieldname="attribute_value", fieldtype="Data", label="Value", reqd=1, in_list_view=1),
			field(fieldname="uom", fieldtype="Data", label="UOM", in_list_view=1),
			field(fieldname="is_price_driver", fieldtype="Check", label="Price Driver", in_list_view=1),
		],
		[],
	)

	write_doctype(
		catalogue,
		"Furniture Product Family",
		{
			"module": "Furniture Catalogue",
			"autoname": "naming_series:",
			"title_field": "family_name",
			"search_fields": "family_name,family_code,product_category,status",
			"track_changes": 1,
			"allow_rename": 1,
			"sort_field": "modified",
			"sort_order": "DESC",
		},
		family_fields(),
		[
			perm("System Manager", write=1, create=1, delete=1, share=1, import_=1),
			perm("Furniture ERP Administrator", write=1, create=1, delete=1, share=1, import_=1),
			perm("Furniture Product Manager", write=1, create=1, delete=0, share=1, import_=1),
			perm("Sales Manager", read=1),
			perm("Designer", read=1),
		],
		FAMILY_VALIDATE,
	)

	# fix import_ key
	# rewrite permissions properly without import_
	family_json = catalogue / "doctype" / "furniture_product_family" / "furniture_product_family.json"
	data = json.loads(family_json.read_text())
	for p in data["permissions"]:
		if "import_" in p:
			p["import"] = p.pop("import_")
	family_json.write_text(json.dumps(data, indent=1) + "\n")

	write_doctype(
		catalogue,
		"Furniture Material",
		{
			"module": "Furniture Catalogue",
			"autoname": "naming_series:",
			"title_field": "material_name",
			"search_fields": "material_name,material_type,grade,status",
			"track_changes": 1,
			"allow_rename": 1,
		},
		material_fields(),
		[
			perm("System Manager", write=1, create=1, delete=1, share=1),
			perm("Furniture ERP Administrator", write=1, create=1, delete=1, share=1),
			perm("Furniture Product Manager", write=1, create=1, share=1),
			perm("Procurement Manager", read=1),
			perm("Designer", read=1),
		],
	)

	write_doctype(
		catalogue,
		"Furniture Finish",
		{
			"module": "Furniture Catalogue",
			"autoname": "naming_series:",
			"title_field": "finish_name",
			"search_fields": "finish_name,finish_type,finish_code,status",
			"track_changes": 1,
			"allow_rename": 1,
		},
		finish_fields(),
		[
			perm("System Manager", write=1, create=1, delete=1, share=1),
			perm("Furniture ERP Administrator", write=1, create=1, delete=1, share=1),
			perm("Furniture Product Manager", write=1, create=1, share=1),
			perm("Designer", read=1),
		],
	)

	write_doctype(
		catalogue,
		"Furniture Specification",
		{
			"module": "Furniture Catalogue",
			"autoname": "naming_series:",
			"title_field": "spec_title",
			"search_fields": "spec_title,product_family,spec_status,drawing_no",
			"track_changes": 1,
			"is_submittable": 0,
			"allow_auto_repeat": 0,
		},
		spec_fields(),
		[
			perm("System Manager", write=1, create=1, delete=1, share=1),
			perm("Furniture ERP Administrator", write=1, create=1, delete=1, share=1),
			perm("Furniture Product Manager", write=1, create=1, share=1),
			perm("Designer", write=1, create=1, share=1),
			perm("Sales Manager", read=1),
			perm("Sales Executive", read=1),
		],
		SPEC_VALIDATE,
	)

	print("Generated DocTypes under", ROOT)


if __name__ == "__main__":
	main()
