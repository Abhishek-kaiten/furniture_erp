#!/usr/bin/env python3
"""Generate Phase 2 masters + Requirement + Job File for furniture_erp (Frappe-only safe)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "furniture_erp"


def field(**kwargs):
	return {k: v for k, v in kwargs.items() if v is not None}


def section(label, name=None):
	return field(
		fieldname=name or f"section_{label.lower().replace(' ', '_').replace('&', 'and')[:40]}",
		fieldtype="Section Break",
		label=label,
	)


def col(name):
	return field(fieldname=name, fieldtype="Column Break")


def write_doctype(module_path: Path, name: str, meta: dict, fields: list, permissions: list, py_extra: str = "	pass\n"):
	slug = name.lower().replace(" ", "_")
	folder = module_path / "doctype" / slug
	folder.mkdir(parents=True, exist_ok=True)
	(folder / "__init__.py").write_text("")
	doc = {
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
	(folder / f"{slug}.json").write_text(json.dumps(doc, indent=1) + "\n")
	# Frappe controller class = DocType name with spaces/dashes removed
	class_name = name.replace(" ", "").replace("-", "")
	(folder / f"{slug}.py").write_text(
		f'''# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class {class_name}(Document):
{py_extra}
'''
	)
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


ADMIN = [
	perm("System Manager", write=1, create=1, delete=1, share=1, **{"import": 1}),
	perm("Furniture ERP Administrator", write=1, create=1, delete=1, share=1, **{"import": 1}),
	perm("Furniture Product Manager", write=1, create=1, share=1),
	perm("Furniture Administrator", write=1, create=1, delete=1, share=1),
]

SALES_READ = [
	perm("Sales Manager", read=1),
	perm("Sales Executive", read=1),
	perm("CRM Executive", read=1),
	perm("Designer", read=1),
	perm("Furniture Designer", read=1),
]


def category_fields():
	return [
		section("Identity"),
		field(fieldname="category_name", fieldtype="Data", label="Category Name", reqd=1, in_list_view=1, bold=1, in_standard_filter=1),
		col("c2"),
		field(fieldname="category_code", fieldtype="Data", label="Category Code", reqd=1, unique=1, in_list_view=1, in_standard_filter=1),
		col("c3"),
		field(fieldname="disabled", fieldtype="Check", label="Disabled", in_standard_filter=1),
		field(fieldname="parent_category", fieldtype="Link", label="Parent Category", options="Furniture Category", in_standard_filter=1),
		field(fieldname="is_group", fieldtype="Check", label="Is Group"),
		field(fieldname="description", fieldtype="Small Text", label="Description"),
		field(fieldname="image", fieldtype="Attach Image", label="Image"),
	]


CATEGORY_PY = '''
	def validate(self):
		if self.parent_category and self.parent_category == self.name:
			frappe.throw(frappe._("Parent Category cannot be the same as this Category."))
		if self.category_code:
			self.category_code = self.category_code.strip().upper()
'''


def color_fields():
	return [
		section("Identity"),
		field(fieldname="color_name", fieldtype="Data", label="Color Name", reqd=1, in_list_view=1, bold=1),
		col("c2"),
		field(fieldname="color_code", fieldtype="Data", label="Color Code", reqd=1, unique=1, in_list_view=1),
		col("c3"),
		field(fieldname="active", fieldtype="Check", label="Active", default="1", in_standard_filter=1),
		field(fieldname="hex_code", fieldtype="Data", label="Hex Code"),
		field(
			fieldname="color_family",
			fieldtype="Select",
			label="Color Family",
			options="\nNeutral\nWarm\nCool\nWood Tone\nMetallic\nOther",
			in_standard_filter=1,
		),
		field(fieldname="description", fieldtype="Small Text", label="Description"),
		field(fieldname="color_image", fieldtype="Attach Image", label="Color Image"),
	]


def material_fields():
	return [
		section("Identity"),
		field(fieldname="material_name", fieldtype="Data", label="Material Name", reqd=1, in_list_view=1, bold=1),
		col("c2"),
		field(fieldname="material_code", fieldtype="Data", label="Material Code", reqd=1, unique=1, in_list_view=1),
		col("c3"),
		field(fieldname="active", fieldtype="Check", label="Active", default="1", in_standard_filter=1),
		field(
			fieldname="material_type",
			fieldtype="Select",
			label="Material Type",
			options="Wood\nPlywood\nMDF\nParticle Board\nMetal\nGlass\nFabric\nFoam\nHardware\nPolish\nOther",
			reqd=1,
			in_list_view=1,
			in_standard_filter=1,
		),
		field(fieldname="material_grade", fieldtype="Data", label="Material Grade", in_standard_filter=1),
		field(fieldname="item_code", fieldtype="Data", label="Item Code (ERPNext)"),
		field(fieldname="supplier", fieldtype="Data", label="Supplier (ERPNext)"),
		field(fieldname="status", fieldtype="Select", label="Legacy Status", options="Active\nInactive", default="Active", hidden=1),
		field(fieldname="grade", fieldtype="Data", label="Legacy Grade", hidden=1),
		field(fieldname="linked_item_code", fieldtype="Data", label="Linked Item Code (ERPNext)", hidden=1),
		section("Physical"),
		field(fieldname="thickness", fieldtype="Float", label="Thickness"),
		col("p2"),
		field(fieldname="length", fieldtype="Float", label="Length"),
		col("p3"),
		field(fieldname="width", fieldtype="Float", label="Width"),
		field(fieldname="default_thickness_mm", fieldtype="Float", label="Default Thickness (mm)", hidden=1),
		field(fieldname="default_width_mm", fieldtype="Float", label="Default Width (mm)", hidden=1),
		field(fieldname="default_length_mm", fieldtype="Float", label="Default Length (mm)", hidden=1),
		field(fieldname="weight_per_unit", fieldtype="Float", label="Weight per Unit"),
		field(
			fieldname="uom",
			fieldtype="Select",
			label="Unit",
			options="Nos\nSq Meter\nMeter\nKg\nSheet\nRoll",
			reqd=1,
			default="Nos",
		),
		field(fieldname="minimum_stock", fieldtype="Float", label="Minimum Stock"),
		field(fieldname="hsn_code", fieldtype="Data", label="HSN Code"),
		field(fieldname="description", fieldtype="Small Text", label="Description"),
		field(fieldname="image", fieldtype="Attach Image", label="Image"),
		section("Costing"),
		field(fieldname="standard_rate", fieldtype="Currency", label="Standard Rate"),
		col("cost2"),
		field(fieldname="reference_rate", fieldtype="Currency", label="Reference Rate"),
		col("cost3"),
		field(fieldname="currency", fieldtype="Link", label="Currency", options="Currency"),
		field(fieldname="last_rate_updated_on", fieldtype="Date", label="Last Rate Updated On"),
		field(fieldname="naming_series", fieldtype="Select", label="Series", options="FMAT-.#####", hidden=1, default="FMAT-.#####"),
	]


MATERIAL_PY = '''
	def validate(self):
		if self.material_code:
			self.material_code = self.material_code.strip().upper()
		if self.active is not None:
			self.status = "Active" if self.active else "Inactive"
		if self.material_grade and not self.grade:
			self.grade = self.material_grade
		if self.item_code and not self.linked_item_code:
			self.linked_item_code = self.item_code
		if self.thickness and not self.default_thickness_mm:
			self.default_thickness_mm = self.thickness
		if self.width and not self.default_width_mm:
			self.default_width_mm = self.width
		if self.length and not self.default_length_mm:
			self.default_length_mm = self.length
		if self.standard_rate and not self.reference_rate:
			self.reference_rate = self.standard_rate
'''


def finish_fields():
	return [
		section("Identity"),
		field(fieldname="finish_name", fieldtype="Data", label="Finish Name", reqd=1, in_list_view=1, bold=1),
		col("c2"),
		field(fieldname="finish_code", fieldtype="Data", label="Finish Code", reqd=1, unique=1, in_list_view=1),
		col("c3"),
		field(fieldname="active", fieldtype="Check", label="Active", default="1", in_standard_filter=1),
		field(
			fieldname="finish_type",
			fieldtype="Select",
			label="Finish Type",
			options="Matte\nGlossy\nPolish\nLaminate\nPaint\nVeneer\nOther",
			reqd=1,
			in_list_view=1,
			in_standard_filter=1,
		),
		field(fieldname="status", fieldtype="Select", label="Legacy Status", options="Active\nInactive", default="Active", hidden=1),
		field(fieldname="description", fieldtype="Small Text", label="Description"),
		field(
			fieldname="application_method",
			fieldtype="Select",
			label="Application Method",
			options="\nSpray\nBrush\nRoller\nPress\nHand Apply\nOther",
		),
		field(fieldname="expected_durability", fieldtype="Data", label="Expected Durability"),
		field(fieldname="color_name", fieldtype="Data", label="Color Name"),
		field(fieldname="color_code", fieldtype="Data", label="Color / Shade Code"),
		field(fieldname="gloss_level", fieldtype="Select", label="Gloss Level", options="\nMatte\nSatin\nGloss"),
		field(fieldname="grain_direction_required", fieldtype="Check", label="Grain Direction Required"),
		field(fieldname="curing_lead_time_days", fieldtype="Int", label="Curing Lead Time (Days)"),
		field(fieldname="voc_compliant", fieldtype="Check", label="Low VOC Compliant"),
		field(fieldname="fire_rating", fieldtype="Data", label="Fire Rating"),
		field(fieldname="hsn_code", fieldtype="Data", label="HSN Code"),
		field(fieldname="linked_item_code", fieldtype="Data", label="Linked Item Code (ERPNext)"),
		field(fieldname="swatch_image", fieldtype="Attach Image", label="Swatch Image"),
		field(fieldname="naming_series", fieldtype="Select", label="Series", options="FFIN-.#####", hidden=1, default="FFIN-.#####"),
	]


FINISH_PY = '''
	def validate(self):
		if self.finish_code:
			self.finish_code = self.finish_code.strip().upper()
		if self.active is not None:
			self.status = "Active" if self.active else "Inactive"
'''


def model_fields():
	return [
		section("Identity"),
		field(fieldname="model_name", fieldtype="Data", label="Model Name", reqd=1, in_list_view=1, bold=1),
		col("c2"),
		field(fieldname="model_code", fieldtype="Data", label="Model Code", reqd=1, unique=1, in_list_view=1),
		col("c3"),
		field(fieldname="active", fieldtype="Check", label="Active", default="1", in_standard_filter=1),
		field(fieldname="furniture_category", fieldtype="Link", label="Furniture Category", options="Furniture Category", in_standard_filter=1),
		field(
			fieldname="model_type",
			fieldtype="Select",
			label="Model Type",
			options="Ready Made\nCustom\nModular",
			in_standard_filter=1,
			in_list_view=1,
		),
		field(fieldname="brand", fieldtype="Data", label="Brand (ERPNext)"),
		field(fieldname="item_code", fieldtype="Data", label="Item Code (ERPNext)"),
		field(fieldname="description", fieldtype="Text Editor", label="Description"),
		section("Dimensions"),
		field(fieldname="standard_width", fieldtype="Float", label="Standard Width"),
		col("d2"),
		field(fieldname="standard_height", fieldtype="Float", label="Standard Height"),
		col("d3"),
		field(fieldname="standard_depth", fieldtype="Float", label="Standard Depth"),
		section("Defaults"),
		field(fieldname="default_material", fieldtype="Link", label="Default Material", options="Furniture Material"),
		col("def2"),
		field(fieldname="default_finish", fieldtype="Link", label="Default Finish", options="Furniture Finish"),
		col("def3"),
		field(fieldname="default_color", fieldtype="Link", label="Default Color", options="Furniture Color"),
		section("Media"),
		field(fieldname="product_image", fieldtype="Attach Image", label="Product Image"),
		field(fieldname="technical_drawing", fieldtype="Attach", label="Technical Drawing"),
	]


MODEL_PY = '''
	def validate(self):
		if self.model_code:
			self.model_code = self.model_code.strip().upper()
		for fname, label in (
			("standard_width", "Standard Width"),
			("standard_height", "Standard Height"),
			("standard_depth", "Standard Depth"),
		):
			value = self.get(fname)
			if value is not None and value < 0:
				frappe.throw(frappe._("{0} cannot be negative.").format(label))
'''


def variant_fields():
	return [
		section("Identity"),
		field(fieldname="variant_name", fieldtype="Data", label="Variant Name", reqd=1, in_list_view=1, bold=1),
		col("c2"),
		field(fieldname="variant_code", fieldtype="Data", label="Variant Code", reqd=1, unique=1, in_list_view=1),
		col("c3"),
		field(fieldname="disabled", fieldtype="Check", label="Disabled", in_standard_filter=1),
		field(fieldname="furniture_model", fieldtype="Link", label="Furniture Model", options="Furniture Model", reqd=1, in_standard_filter=1, in_list_view=1),
		field(fieldname="item_code", fieldtype="Data", label="Item Code (ERPNext)"),
		field(fieldname="color", fieldtype="Link", label="Color", options="Furniture Color", in_standard_filter=1),
		field(fieldname="material", fieldtype="Link", label="Material", options="Furniture Material", in_standard_filter=1),
		field(fieldname="finish", fieldtype="Link", label="Finish", options="Furniture Finish", in_standard_filter=1),
		section("Dimensions and Price"),
		field(fieldname="width", fieldtype="Float", label="Width"),
		col("d2"),
		field(fieldname="height", fieldtype="Float", label="Height"),
		col("d3"),
		field(fieldname="depth", fieldtype="Float", label="Depth"),
		field(fieldname="weight", fieldtype="Float", label="Weight"),
		field(fieldname="selling_price", fieldtype="Currency", label="Selling Price"),
		field(fieldname="purchase_price", fieldtype="Currency", label="Purchase Price"),
		field(fieldname="image", fieldtype="Attach Image", label="Image"),
	]


VARIANT_PY = '''
	def validate(self):
		if self.variant_code:
			self.variant_code = self.variant_code.strip().upper()
		if not self.furniture_model:
			frappe.throw(frappe._("Furniture Model is required."))
'''


def design_fields():
	return [
		section("Identity"),
		field(fieldname="design_name", fieldtype="Data", label="Design Name", reqd=1, in_list_view=1, bold=1),
		col("c2"),
		field(fieldname="design_code", fieldtype="Data", label="Design Code", reqd=1, unique=1, in_list_view=1),
		col("c3"),
		field(fieldname="is_active", fieldtype="Check", label="Is Active", default="1", in_standard_filter=1),
		field(fieldname="furniture_category", fieldtype="Link", label="Furniture Category", options="Furniture Category", in_standard_filter=1),
		field(fieldname="furniture_model", fieldtype="Link", label="Furniture Model", options="Furniture Model", in_standard_filter=1),
		field(
			fieldname="design_type",
			fieldtype="Select",
			label="Design Type",
			options="Modern\nTraditional\nContemporary\nCustom\nModular",
			in_standard_filter=1,
		),
		field(fieldname="design_version", fieldtype="Data", label="Design Version", default="1"),
		field(fieldname="design_description", fieldtype="Text Editor", label="Design Description"),
		section("Defaults"),
		field(fieldname="default_material", fieldtype="Link", label="Default Material", options="Furniture Material"),
		col("def2"),
		field(fieldname="default_finish", fieldtype="Link", label="Default Finish", options="Furniture Finish"),
		col("def3"),
		field(fieldname="default_color", fieldtype="Link", label="Default Color", options="Furniture Color"),
		section("Media"),
		field(fieldname="design_image", fieldtype="Attach Image", label="Design Image"),
		field(fieldname="drawing_2d", fieldtype="Attach", label="Drawing 2D"),
		field(fieldname="drawing_3d", fieldtype="Attach", label="Drawing 3D"),
		field(fieldname="design_file", fieldtype="Attach", label="Design File"),
	]


def config_option_fields():
	return [
		field(fieldname="option_name", fieldtype="Data", label="Option Name", reqd=1, in_list_view=1),
		field(
			fieldname="option_type",
			fieldtype="Select",
			label="Option Type",
			options="\nSize\nColor\nMaterial\nFabric\nFinish\nModular\nOther",
			in_list_view=1,
		),
		field(fieldname="option_value", fieldtype="Data", label="Option Value", in_list_view=1),
		field(fieldname="additional_price", fieldtype="Currency", label="Additional Price", in_list_view=1),
		field(fieldname="default_option", fieldtype="Check", label="Default Option", in_list_view=1),
	]


def config_template_fields():
	return [
		section("Identity"),
		field(fieldname="template_name", fieldtype="Data", label="Template Name", reqd=1, in_list_view=1, bold=1),
		col("c2"),
		field(fieldname="furniture_category", fieldtype="Link", label="Furniture Category", options="Furniture Category", in_standard_filter=1),
		col("c3"),
		field(fieldname="active", fieldtype="Check", label="Active", default="1", in_standard_filter=1),
		field(fieldname="furniture_model", fieldtype="Link", label="Furniture Model", options="Furniture Model"),
		field(
			fieldname="configuration_type",
			fieldtype="Select",
			label="Configuration Type",
			options="Size\nColor\nMaterial\nFabric\nFinish\nModular",
		),
		field(fieldname="allow_custom_size", fieldtype="Check", label="Allow Custom Size"),
		section("Size Limits"),
		field(fieldname="minimum_width", fieldtype="Float", label="Minimum Width"),
		col("s2"),
		field(fieldname="maximum_width", fieldtype="Float", label="Maximum Width"),
		col("s3"),
		field(fieldname="minimum_height", fieldtype="Float", label="Minimum Height"),
		field(fieldname="maximum_height", fieldtype="Float", label="Maximum Height"),
		field(fieldname="minimum_depth", fieldtype="Float", label="Minimum Depth"),
		field(fieldname="maximum_depth", fieldtype="Float", label="Maximum Depth"),
		section("Defaults"),
		field(fieldname="default_material", fieldtype="Link", label="Default Material", options="Furniture Material"),
		col("def2"),
		field(fieldname="default_finish", fieldtype="Link", label="Default Finish", options="Furniture Finish"),
		section("Options"),
		field(fieldname="configuration_options", fieldtype="Table", label="Configuration Options", options="Furniture Configuration Option"),
	]


CONFIG_PY = '''
	def validate(self):
		pairs = (
			("minimum_width", "maximum_width", "Width"),
			("minimum_height", "maximum_height", "Height"),
			("minimum_depth", "maximum_depth", "Depth"),
		)
		for mn, mx, label in pairs:
			lo, hi = self.get(mn), self.get(mx)
			if lo is not None and hi is not None and lo > hi:
				frappe.throw(frappe._("Minimum {0} cannot exceed maximum {0}.").format(label))
		defaults = [r for r in (self.configuration_options or []) if r.default_option]
		if len(defaults) > 1:
			frappe.throw(frappe._("Only one default configuration option is allowed."))
'''


def req_item_fields():
	return [
		field(fieldname="furniture_category", fieldtype="Link", label="Furniture Category", options="Furniture Category", in_list_view=1),
		field(fieldname="furniture_model", fieldtype="Link", label="Furniture Model", options="Furniture Model", in_list_view=1),
		field(fieldname="furniture_variant", fieldtype="Link", label="Furniture Variant", options="Furniture Variant", in_list_view=1),
		field(fieldname="item_code", fieldtype="Data", label="Item Code (ERPNext)"),
		field(fieldname="description", fieldtype="Small Text", label="Description"),
		field(fieldname="quantity", fieldtype="Float", label="Quantity", reqd=1, default="1", in_list_view=1),
		field(fieldname="width", fieldtype="Float", label="Width"),
		field(fieldname="height", fieldtype="Float", label="Height"),
		field(fieldname="depth", fieldtype="Float", label="Depth"),
		field(fieldname="material", fieldtype="Link", label="Material", options="Furniture Material"),
		field(fieldname="color", fieldtype="Link", label="Color", options="Furniture Color"),
		field(fieldname="finish", fieldtype="Link", label="Finish", options="Furniture Finish"),
		field(fieldname="estimated_rate", fieldtype="Currency", label="Estimated Rate", in_list_view=1),
		field(fieldname="estimated_amount", fieldtype="Currency", label="Estimated Amount", in_list_view=1, read_only=1),
		field(fieldname="customization_required", fieldtype="Check", label="Customization Required"),
		field(fieldname="remarks", fieldtype="Small Text", label="Remarks"),
	]


def requirement_fields():
	return [
		section("Header"),
		field(fieldname="naming_series", fieldtype="Select", label="Series", options="FCR-.YYYY.-.#####", reqd=1, default="FCR-.YYYY.-.#####"),
		col("h2"),
		field(fieldname="requirement_date", fieldtype="Date", label="Requirement Date", reqd=1, default="Today", in_list_view=1, in_standard_filter=1),
		col("h3"),
		field(
			fieldname="status",
			fieldtype="Select",
			label="Status",
			options="Draft\nSubmitted\nUnder Review\nApproved\nRejected\nCompleted",
			reqd=1,
			default="Draft",
			in_list_view=1,
			in_standard_filter=1,
		),
		field(fieldname="customer", fieldtype="Data", label="Customer (ERPNext)", in_standard_filter=1, in_list_view=1),
		field(fieldname="lead", fieldtype="Data", label="Lead (ERPNext)", in_standard_filter=1),
		field(fieldname="opportunity", fieldtype="Data", label="Opportunity (ERPNext)", in_standard_filter=1),
		field(fieldname="furniture_job_file", fieldtype="Link", label="Furniture Job File", options="Furniture Job File"),
		field(
			fieldname="requirement_type",
			fieldtype="Select",
			label="Requirement Type",
			options="Ready Made\nCustom\nProject",
			in_standard_filter=1,
		),
		field(fieldname="project_name", fieldtype="Data", label="Project Name"),
		field(
			fieldname="project_type",
			fieldtype="Select",
			label="Project Type",
			options="\nResidential\nCommercial\nOffice\nHotel",
		),
		field(fieldname="priority", fieldtype="Select", label="Priority", options="Low\nMedium\nHigh\nUrgent", default="Medium", in_standard_filter=1),
		field(fieldname="customer_budget", fieldtype="Currency", label="Customer Budget"),
		field(fieldname="preferred_delivery_date", fieldtype="Date", label="Preferred Delivery Date"),
		field(fieldname="assigned_to", fieldtype="Link", label="Assigned To", options="User", in_standard_filter=1),
		field(fieldname="requirement_description", fieldtype="Text Editor", label="Requirement Description"),
		field(fieldname="attachments", fieldtype="Attach", label="Attachments"),
		field(fieldname="remarks", fieldtype="Small Text", label="Remarks"),
		section("Items"),
		field(fieldname="requirement_items", fieldtype="Table", label="Requirement Items", options="Furniture Requirement Item"),
	]


REQ_PY = '''
	def validate(self):
		for row in self.requirement_items or []:
			qty = row.quantity or 0
			rate = row.estimated_rate or 0
			row.estimated_amount = qty * rate
			if qty <= 0:
				frappe.throw(frappe._("Quantity must be greater than zero in row {0}.").format(row.idx))
'''


def job_wo_ref_fields():
	return [
		field(fieldname="work_order", fieldtype="Data", label="Work Order (ERPNext)", in_list_view=1),
		field(fieldname="status", fieldtype="Data", label="Status", in_list_view=1),
		field(fieldname="remarks", fieldtype="Small Text", label="Remarks"),
	]


def job_dn_ref_fields():
	return [
		field(fieldname="delivery_note", fieldtype="Data", label="Delivery Note (ERPNext)", in_list_view=1),
		field(fieldname="status", fieldtype="Data", label="Status", in_list_view=1),
		field(fieldname="remarks", fieldtype="Small Text", label="Remarks"),
	]


JOB_STATUS = (
	"Draft\nRequirement Pending\nSite Survey Pending\nDesign Pending\nCustomer Approval Pending\n"
	"Quotation Pending\nQuotation Approved\nSales Order Confirmed\nMaterial Planning\nProduction Pending\n"
	"In Production\nQuality Inspection\nReady for Dispatch\nDispatched\nInstallation In Progress\n"
	"Completed\nClosed\nOn Hold\nCancelled\nRejected"
)


def job_file_fields():
	return [
		section("Basic Information"),
		field(fieldname="naming_series", fieldtype="Select", label="Series", options="FJF-.YYYY.-.#####", reqd=1, default="FJF-.YYYY.-.#####"),
		col("b2"),
		field(fieldname="job_file_title", fieldtype="Data", label="Job File Title", reqd=1, in_list_view=1, bold=1),
		col("b3"),
		field(fieldname="job_status", fieldtype="Select", label="Job Status", options=JOB_STATUS, reqd=1, default="Draft", in_list_view=1, in_standard_filter=1),
		field(fieldname="customer", fieldtype="Data", label="Customer (ERPNext)", in_standard_filter=1, in_list_view=1),
		field(fieldname="customer_type", fieldtype="Select", label="Customer Type", options="\nB2B\nB2C"),
		field(fieldname="contact_person", fieldtype="Data", label="Contact Person (ERPNext)"),
		field(fieldname="mobile_number", fieldtype="Data", label="Mobile Number"),
		field(fieldname="email", fieldtype="Data", label="Email"),
		field(fieldname="company", fieldtype="Data", label="Company (ERPNext)", in_standard_filter=1),
		field(fieldname="branch", fieldtype="Data", label="Branch (ERPNext)"),
		field(fieldname="project", fieldtype="Data", label="Project (ERPNext)"),
		field(fieldname="project_manager", fieldtype="Data", label="Project Manager (ERPNext)", in_standard_filter=1),
		field(
			fieldname="job_type",
			fieldtype="Select",
			label="Job Type",
			options="Ready Made\nCustom\nProject",
			in_standard_filter=1,
		),
		field(fieldname="priority", fieldtype="Select", label="Priority", options="Low\nMedium\nHigh\nUrgent", default="Medium"),
		field(fieldname="job_creation_date", fieldtype="Date", label="Job Creation Date", default="Today", in_standard_filter=1),
		field(fieldname="expected_completion_date", fieldtype="Date", label="Expected Completion Date", in_standard_filter=1),
		field(fieldname="assigned_to", fieldtype="Link", label="Assigned To", options="User"),
		section("CRM References"),
		field(fieldname="lead", fieldtype="Data", label="Lead (ERPNext)"),
		col("crm2"),
		field(fieldname="opportunity", fieldtype="Data", label="Opportunity (ERPNext)"),
		col("crm3"),
		field(fieldname="customer_requirement", fieldtype="Link", label="Customer Requirement", options="Furniture Customer Requirement"),
		section("Sales References"),
		field(fieldname="quotation", fieldtype="Data", label="Quotation (ERPNext)"),
		col("sales2"),
		field(fieldname="sales_order", fieldtype="Data", label="Sales Order (ERPNext)"),
		col("sales3"),
		field(fieldname="sales_person", fieldtype="Data", label="Sales Person (ERPNext)", in_standard_filter=1),
		section("Site Information"),
		field(fieldname="installation_site", fieldtype="Data", label="Installation Site (ERPNext Address)"),
		col("site2"),
		field(fieldname="site_survey", fieldtype="Data", label="Site Survey (link later)"),
		col("site3"),
		field(fieldname="measurement_status", fieldtype="Select", label="Measurement Status", options="\nPending\nIn Progress\nCompleted\nApproved"),
		field(fieldname="design_approval_status", fieldtype="Select", label="Design Approval Status", options="\nPending\nIn Review\nApproved\nRejected"),
		section("Manufacturing Information"),
		field(fieldname="production_plan", fieldtype="Data", label="Production Plan (ERPNext)"),
		field(fieldname="production_status", fieldtype="Select", label="Production Status", options="\nPending\nPlanned\nIn Progress\nCompleted\nOn Hold", in_standard_filter=1),
		field(fieldname="material_status", fieldtype="Select", label="Material Status", options="\nPending\nPartial\nAvailable\nShortage"),
		field(fieldname="qc_status", fieldtype="Select", label="QC Status", options="\nPending\nIn Progress\nPassed\nFailed"),
		field(fieldname="work_orders", fieldtype="Table", label="Work Orders", options="Furniture Job Work Order Reference"),
		section("Delivery Information"),
		field(fieldname="dispatch_status", fieldtype="Select", label="Dispatch Status", options="\nPending\nPlanned\nDispatched\nDelivered\nFailed", in_standard_filter=1),
		field(fieldname="installation_status", fieldtype="Select", label="Installation Status", options="\nPending\nScheduled\nIn Progress\nCompleted\nFailed"),
		field(fieldname="installation_completion_date", fieldtype="Date", label="Installation Completion Date"),
		field(fieldname="delivery_notes", fieldtype="Table", label="Delivery Notes", options="Furniture Job Delivery Reference"),
		section("Payment Information"),
		field(fieldname="order_amount", fieldtype="Currency", label="Order Amount"),
		col("pay2"),
		field(fieldname="advance_amount", fieldtype="Currency", label="Advance Amount"),
		col("pay3"),
		field(fieldname="received_amount", fieldtype="Currency", label="Received Amount"),
		field(fieldname="outstanding_amount", fieldtype="Currency", label="Outstanding Amount", read_only=1),
		field(
			fieldname="payment_status",
			fieldtype="Select",
			label="Payment Status",
			options="\nNot Due\nDue\nPartially Paid\nPaid\nOverdue",
			in_standard_filter=1,
		),
		section("Closure"),
		field(fieldname="completion_date", fieldtype="Date", label="Completion Date"),
		field(fieldname="closed_by", fieldtype="Link", label="Closed By", options="User"),
		field(fieldname="internal_remarks", fieldtype="Text Editor", label="Internal Remarks"),
		field(fieldname="customer_remarks", fieldtype="Small Text", label="Customer Remarks"),
		field(fieldname="closure_remarks", fieldtype="Small Text", label="Closure Remarks"),
	]


JOB_PY = '''
	def validate(self):
		if not (self.job_file_title or "").strip():
			frappe.throw(frappe._("Job File Title is required."))
		order = self.order_amount or 0
		received = self.received_amount or 0
		self.outstanding_amount = order - received
		if self.outstanding_amount < 0:
			frappe.throw(frappe._("Received Amount cannot exceed Order Amount."))
'''


def settings_extra_fields():
	"""Appended conceptually — we rewrite full settings in enhance_settings()."""
	pass


def enhance_settings():
	setup = ROOT / "setup"
	fields = [
		section("Defaults"),
		field(fieldname="default_currency", fieldtype="Link", label="Default Currency", options="Currency", reqd=1, default="INR"),
		col("d2"),
		field(fieldname="default_length_unit", fieldtype="Select", label="Default Length Unit", options="mm\ncm\ninch", reqd=1, default="mm"),
		col("d3"),
		field(fieldname="default_area_unit", fieldtype="Select", label="Default Area Unit", options="sq m\nsq ft", default="sq m"),
		field(fieldname="default_furniture_category", fieldtype="Link", label="Default Furniture Category", options="Furniture Category"),
		section("Warehouses (ERPNext codes)"),
		field(fieldname="default_warehouse_raw", fieldtype="Data", label="Default Raw Material Warehouse"),
		col("w2"),
		field(fieldname="default_warehouse_wip", fieldtype="Data", label="Default WIP Warehouse"),
		col("w3"),
		field(fieldname="default_warehouse_fg", fieldtype="Data", label="Default Finished Goods Warehouse"),
		field(fieldname="default_warehouse_scrap", fieldtype="Data", label="Default Scrap Warehouse"),
		section("Naming Series"),
		field(fieldname="family_naming_series", fieldtype="Data", label="Product Family Naming Series", reqd=1, default="FPF-.#####"),
		col("ns2"),
		field(fieldname="material_naming_series", fieldtype="Data", label="Material Naming Series", reqd=1, default="FMAT-.#####"),
		col("ns3"),
		field(fieldname="finish_naming_series", fieldtype="Data", label="Finish Naming Series", reqd=1, default="FFIN-.#####"),
		field(fieldname="specification_naming_series", fieldtype="Data", label="Specification Naming Series", reqd=1, default="FSPEC-.YYYY.-.#####"),
		field(fieldname="category_naming_hint", fieldtype="Data", label="Category Code Hint", default="CAT-"),
		field(fieldname="job_file_naming_series", fieldtype="Data", label="Job File Naming Series", default="FJF-.YYYY.-.#####"),
		field(fieldname="requirement_naming_series", fieldtype="Data", label="Requirement Naming Series", default="FCR-.YYYY.-.#####"),
		section("Catalogue Rules"),
		field(fieldname="enforce_allowed_materials", fieldtype="Check", label="Enforce Allowed Materials on Spec", default="1"),
		col("r2"),
		field(fieldname="enforce_allowed_finishes", fieldtype="Check", label="Enforce Allowed Finishes on Spec", default="1"),
		col("r3"),
		field(fieldname="allow_draft_spec_duplication", fieldtype="Check", label="Allow Duplicate Draft Specs", default="0"),
		field(fieldname="default_gst_hsn_code", fieldtype="Data", label="Default HSN Code"),
		field(fieldname="spec_requires_approval", fieldtype="Check", label="Specification Requires Approval", default="0"),
		section("Commercial Rules"),
		field(fieldname="max_discount_percent", fieldtype="Percent", label="Max Discount Percent Without Approval", default="5"),
		col("com2"),
		field(fieldname="minimum_profit_margin", fieldtype="Percent", label="Minimum Profit Margin", default="10"),
		col("com3"),
		field(fieldname="required_advance_percent", fieldtype="Percent", label="Required Advance Percent", default="20"),
		field(fieldname="default_warranty_period", fieldtype="Int", label="Default Warranty Period", default="12"),
		field(fieldname="default_warranty_unit", fieldtype="Select", label="Default Warranty Unit", options="Days\nMonths\nYears", default="Months"),
		field(fieldname="design_approval_required_for_custom", fieldtype="Check", label="Design Approval Required for Custom", default="1"),
		field(fieldname="qc_mandatory_before_dispatch", fieldtype="Check", label="QC Mandatory Before Dispatch", default="1"),
		section("Integration"),
		field(fieldname="enable_portal_catalogue", fieldtype="Check", label="Enable Portal Catalogue", default="0"),
		col("i2"),
		field(fieldname="integration_webhook_url", fieldtype="Data", label="Integration Webhook URL", options="URL"),
		col("i3"),
		field(
			fieldname="erpnext_note",
			fieldtype="Small Text",
			label="ERPNext Status Note",
			read_only=1,
			default="ERPNext is not installed on this site. Company/Item/Warehouse/Customer links are deferred as Data fields.",
		),
	]
	write_doctype(
		setup,
		"Furniture ERP Settings",
		{"module": "Setup", "issingle": 1, "track_changes": 1},
		fields,
		[
			perm("System Manager", write=1, create=1, delete=1, share=1),
			perm("Furniture ERP Administrator", write=1, create=1, share=1),
			perm("Furniture Administrator", write=1, create=1, share=1),
			perm("Furniture Product Manager", read=1),
		],
	)


def main():
	catalogue = ROOT / "furniture_catalogue"
	sales = ROOT / "sales_design"
	setup = ROOT / "setup"
	for p in (catalogue, sales, setup):
		(p / "doctype").mkdir(parents=True, exist_ok=True)
		(p / "doctype" / "__init__.py").write_text("")
		(p / "__init__.py").touch()

	write_doctype(
		catalogue,
		"Furniture Category",
		{
			"module": "Furniture Catalogue",
			"autoname": "field:category_code",
			"title_field": "category_name",
			"search_fields": "category_name,category_code,parent_category",
			"track_changes": 1,
			"allow_rename": 1,
		},
		category_fields(),
		ADMIN + SALES_READ,
		CATEGORY_PY,
	)
	write_doctype(
		catalogue,
		"Furniture Color",
		{
			"module": "Furniture Catalogue",
			"autoname": "field:color_code",
			"title_field": "color_name",
			"search_fields": "color_name,color_code,color_family",
			"track_changes": 1,
		},
		color_fields(),
		ADMIN + SALES_READ,
		'''
	def validate(self):
		if self.color_code:
			self.color_code = self.color_code.strip().upper()
''',
	)
	write_doctype(
		catalogue,
		"Furniture Material",
		{
			"module": "Furniture Catalogue",
			"autoname": "field:material_code",
			"title_field": "material_name",
			"search_fields": "material_name,material_code,material_type,material_grade",
			"track_changes": 1,
			"allow_rename": 1,
		},
		material_fields(),
		ADMIN
		+ SALES_READ
		+ [perm("Procurement Manager", read=1), perm("Purchase Executive", read=1)],
		MATERIAL_PY,
	)
	write_doctype(
		catalogue,
		"Furniture Finish",
		{
			"module": "Furniture Catalogue",
			"autoname": "field:finish_code",
			"title_field": "finish_name",
			"search_fields": "finish_name,finish_code,finish_type",
			"track_changes": 1,
			"allow_rename": 1,
		},
		finish_fields(),
		ADMIN + SALES_READ,
		FINISH_PY,
	)
	write_doctype(
		catalogue,
		"Furniture Model",
		{
			"module": "Furniture Catalogue",
			"autoname": "field:model_code",
			"title_field": "model_name",
			"search_fields": "model_name,model_code,furniture_category,model_type",
			"track_changes": 1,
		},
		model_fields(),
		ADMIN + SALES_READ,
		MODEL_PY,
	)
	write_doctype(
		catalogue,
		"Furniture Variant",
		{
			"module": "Furniture Catalogue",
			"autoname": "field:variant_code",
			"title_field": "variant_name",
			"search_fields": "variant_name,variant_code,furniture_model",
			"track_changes": 1,
		},
		variant_fields(),
		ADMIN + SALES_READ,
		VARIANT_PY,
	)
	write_doctype(
		catalogue,
		"Furniture Design",
		{
			"module": "Furniture Catalogue",
			"autoname": "field:design_code",
			"title_field": "design_name",
			"search_fields": "design_name,design_code,furniture_category,design_type",
			"track_changes": 1,
		},
		design_fields(),
		ADMIN + SALES_READ + [perm("Design Manager", write=1, create=1)],
		'''
	def validate(self):
		if self.design_code:
			self.design_code = self.design_code.strip().upper()
''',
	)
	write_doctype(
		catalogue,
		"Furniture Configuration Option",
		{"module": "Furniture Catalogue", "istable": 1, "editable_grid": 1},
		config_option_fields(),
		[],
	)
	write_doctype(
		catalogue,
		"Furniture Configuration Template",
		{
			"module": "Furniture Catalogue",
			"autoname": "field:template_name",
			"title_field": "template_name",
			"search_fields": "template_name,furniture_category,configuration_type",
			"track_changes": 1,
		},
		config_template_fields(),
		ADMIN,
		CONFIG_PY,
	)

	write_doctype(
		sales,
		"Furniture Requirement Item",
		{"module": "Sales Design", "istable": 1, "editable_grid": 1},
		req_item_fields(),
		[],
	)
	write_doctype(
		sales,
		"Furniture Customer Requirement",
		{
			"module": "Sales Design",
			"autoname": "naming_series:",
			"title_field": "customer",
			"search_fields": "customer,lead,opportunity,requirement_type,status",
			"track_changes": 1,
		},
		requirement_fields(),
		[
			perm("System Manager", write=1, create=1, delete=1, share=1),
			perm("Furniture ERP Administrator", write=1, create=1, delete=1, share=1),
			perm("Furniture Administrator", write=1, create=1, delete=1, share=1),
			perm("Sales Manager", write=1, create=1, share=1),
			perm("Sales Executive", write=1, create=1, share=1),
			perm("CRM Executive", write=1, create=1),
			perm("Furniture Project Manager", write=1, create=1, share=1),
			perm("Project Manager", write=1, create=1),
		],
		REQ_PY,
	)
	write_doctype(
		sales,
		"Furniture Job Work Order Reference",
		{"module": "Sales Design", "istable": 1, "editable_grid": 1},
		job_wo_ref_fields(),
		[],
	)
	write_doctype(
		sales,
		"Furniture Job Delivery Reference",
		{"module": "Sales Design", "istable": 1, "editable_grid": 1},
		job_dn_ref_fields(),
		[],
	)
	write_doctype(
		sales,
		"Furniture Job File",
		{
			"module": "Sales Design",
			"autoname": "naming_series:",
			"title_field": "job_file_title",
			"search_fields": "job_file_title,customer,job_type,job_status,sales_person",
			"track_changes": 1,
		},
		job_file_fields(),
		[
			perm("System Manager", write=1, create=1, delete=1, share=1),
			perm("Furniture ERP Administrator", write=1, create=1, delete=1, share=1),
			perm("Furniture Administrator", write=1, create=1, delete=1, share=1),
			perm("Furniture Project Manager", write=1, create=1, share=1),
			perm("Project Manager", write=1, create=1, share=1),
			perm("Sales Manager", write=1, create=1, share=1),
			perm("Sales Executive", write=1, create=1),
			perm("Management Viewer", read=1),
		],
		JOB_PY,
	)

	enhance_settings()
	print("Phase 2 DocTypes generated under", ROOT)


if __name__ == "__main__":
	main()
