# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt
"""Convert Phase 2 ERPNext Data placeholders to Link fields after ERPNext install."""

from __future__ import annotations

import frappe

FIELD_MAP = [
	# (doctype, fieldname, options, label)
	("Furniture Customer Requirement", "customer", "Customer", "Customer"),
	("Furniture Customer Requirement", "lead", "Lead", "Lead"),
	("Furniture Customer Requirement", "opportunity", "Opportunity", "Opportunity"),
	("Furniture Requirement Item", "item_code", "Item", "Item Code"),
	("Furniture Job File", "customer", "Customer", "Customer"),
	("Furniture Job File", "contact_person", "Contact", "Contact Person"),
	("Furniture Job File", "company", "Company", "Company"),
	("Furniture Job File", "project", "Project", "Project"),
	("Furniture Job File", "project_manager", "Employee", "Project Manager"),
	("Furniture Job File", "lead", "Lead", "Lead"),
	("Furniture Job File", "opportunity", "Opportunity", "Opportunity"),
	("Furniture Job File", "quotation", "Quotation", "Quotation"),
	("Furniture Job File", "sales_order", "Sales Order", "Sales Order"),
	("Furniture Job File", "sales_person", "Sales Person", "Sales Person"),
	("Furniture Job File", "installation_site", "Address", "Installation Site"),
	("Furniture Job File", "production_plan", "Production Plan", "Production Plan"),
	("Furniture Job Work Order Reference", "work_order", "Work Order", "Work Order"),
	("Furniture Job Delivery Reference", "delivery_note", "Delivery Note", "Delivery Note"),
	("Furniture Model", "brand", "Brand", "Brand"),
	("Furniture Model", "item_code", "Item", "Item"),
	("Furniture Variant", "item_code", "Item", "Item Code"),
	("Furniture Material", "linked_item_code", "Item", "Linked Item"),
	("Furniture Material", "item_code", "Item", "Item Code"),
	("Furniture Material", "supplier", "Supplier", "Supplier"),
	("Furniture Material", "uom", "UOM", "UOM"),
	("Furniture ERP Settings", "default_warehouse_raw", "Warehouse", "Default Raw Material Warehouse"),
	("Furniture ERP Settings", "default_warehouse_wip", "Warehouse", "Default WIP Warehouse"),
	("Furniture ERP Settings", "default_warehouse_fg", "Warehouse", "Default Finished Goods Warehouse"),
]


def execute():
	if "erpnext" not in frappe.get_installed_apps():
		frappe.logger("furniture_erp").info("Skipping Data→Link conversion: ERPNext not installed")
		return

	for doctype, fieldname, options, label in FIELD_MAP:
		if not frappe.db.exists("DocType", doctype):
			continue
		if not frappe.db.exists("DocType", options):
			continue
		_clear_invalid_link_values(doctype, fieldname, options)
		_ensure_link_property(doctype, fieldname, options, label)

	frappe.clear_cache()


def _clear_invalid_link_values(doctype: str, fieldname: str, options: str) -> None:
	"""Blank out values that are not valid document names before converting to Link."""
	meta = frappe.get_meta(doctype)
	if not meta.has_field(fieldname):
		return
	table = f"tab{doctype}"
	if not frappe.db.table_exists(doctype):
		return
	if not frappe.db.has_column(doctype, fieldname):
		return

	rows = frappe.db.sql(
		f"""
		select name, `{fieldname}` as val
		from `{table}`
		where ifnull(`{fieldname}`, '') != ''
		""",
		as_dict=True,
	)
	for row in rows:
		val = row.val
		if not frappe.db.exists(options, val):
			frappe.db.set_value(doctype, row.name, fieldname, None, update_modified=False)


def _ensure_link_property(doctype: str, fieldname: str, options: str, label: str) -> None:
	meta = frappe.get_meta(doctype)
	df = meta.get_field(fieldname)
	if not df:
		return
	if df.fieldtype == "Link" and df.options == options:
		return

	# Prefer DocType JSON sync via reload; also set Property Setter for safety on customized sites
	ps_name = f"{doctype}-{fieldname}-fieldtype"
	if not frappe.db.exists("Property Setter", ps_name):
		frappe.get_doc(
			{
				"doctype": "Property Setter",
				"doctype_or_field": "DocField",
				"doc_type": doctype,
				"field_name": fieldname,
				"property": "fieldtype",
				"value": "Link",
				"property_type": "Select",
			}
		).insert(ignore_permissions=True)
	else:
		frappe.db.set_value("Property Setter", ps_name, "value", "Link")

	ps_opt = f"{doctype}-{fieldname}-options"
	if not frappe.db.exists("Property Setter", ps_opt):
		frappe.get_doc(
			{
				"doctype": "Property Setter",
				"doctype_or_field": "DocField",
				"doc_type": doctype,
				"field_name": fieldname,
				"property": "options",
				"value": options,
				"property_type": "Text",
			}
		).insert(ignore_permissions=True)
	else:
		frappe.db.set_value("Property Setter", ps_opt, "value", options)

	ps_lab = f"{doctype}-{fieldname}-label"
	if not frappe.db.exists("Property Setter", ps_lab):
		frappe.get_doc(
			{
				"doctype": "Property Setter",
				"doctype_or_field": "DocField",
				"doc_type": doctype,
				"field_name": fieldname,
				"property": "label",
				"value": label,
				"property_type": "Data",
			}
		).insert(ignore_permissions=True)

	frappe.db.sql(
		"""
		update `tabDocField`
		set fieldtype=%s, options=%s, label=%s
		where parent=%s and fieldname=%s
		""",
		("Link", options, label, doctype, fieldname),
	)
	frappe.clear_cache(doctype=doctype)
