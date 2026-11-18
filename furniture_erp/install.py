# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe

CUSTOM_ROLES = [
	"Furniture ERP Administrator",
	"Furniture Administrator",
	"Furniture Product Manager",
	"CRM Executive",
	"Sales Manager",
	"Sales Executive",
	"Showroom Manager",
	"Furniture Project Manager",
	"Project Manager",
	"Survey Engineer",
	"Designer",
	"Furniture Designer",
	"Design Manager",
	"Measurement Technician",
	"Procurement Manager",
	"Purchase Executive",
	"Purchase Manager",
	"Buyer",
	"Store Manager",
	"Inventory Manager",
	"Store User",
	"Production Planner",
	"Production Manager",
	"Production Supervisor",
	"Production Worker",
	"Machine Operator",
	"Quality Inspector",
	"QC Inspector",
	"Quality Manager",
	"QC Manager",
	"Dispatch Coordinator",
	"Dispatch Manager",
	"Delivery Manager",
	"Installer",
	"Installation Manager",
	"Installation Technician",
	"Installation Supervisor",
	"Service Coordinator",
	"Service Manager",
	"Service Technician",
	"Finance Manager",
	"Accounts Executive",
	"Accounts Manager",
	"Accounts User",
	"Management Viewer",
	"Auditor",
]


def after_install():
	_ensure_roles()
	_seed_settings_defaults()
	_sync_erpnext_custom_fields()
	_ensure_furniture_uoms()


def after_migrate():
	_ensure_roles()
	_seed_settings_defaults()
	_sync_erpnext_custom_fields()
	_ensure_furniture_uoms()


def before_tests():
	_ensure_roles()
	_ensure_furniture_uoms()


def _sync_erpnext_custom_fields():
	if "erpnext" not in frappe.get_installed_apps():
		return
	from furniture_erp.sales_design.custom_fields import sync_custom_fields

	sync_custom_fields()


def _ensure_furniture_uoms():
	"""UOMs used by catalogue masters / tests after Link conversion."""
	if "erpnext" not in frappe.get_installed_apps():
		return
	if not frappe.db.exists("DocType", "UOM"):
		return
	for name in ("Nos", "Sheet", "Kg", "Meter", "Litre", "Set", "Box"):
		if frappe.db.exists("UOM", name):
			continue
		frappe.get_doc({"doctype": "UOM", "uom_name": name}).insert(ignore_permissions=True)


def _ensure_roles():
	for role_name in CUSTOM_ROLES:
		if frappe.db.exists("Role", role_name):
			continue
		doc = frappe.get_doc(
			{
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 1,
				"is_custom": 1,
			}
		)
		doc.insert(ignore_permissions=True)


def _seed_settings_defaults():
	if not frappe.db.exists("DocType", "Furniture ERP Settings"):
		return
	settings = frappe.get_single("Furniture ERP Settings")
	dirty = False
	defaults = {
		"default_currency": "INR",
		"default_length_unit": "mm",
		"default_area_unit": "sq m",
		"family_naming_series": "FPF-.#####",
		"material_naming_series": "FMAT-.#####",
		"finish_naming_series": "FFIN-.#####",
		"specification_naming_series": "FSPEC-.YYYY.-.#####",
		"job_file_naming_series": "FJF-.YYYY.-.#####",
		"requirement_naming_series": "FCR-.YYYY.-.#####",
		"enforce_allowed_materials": 1,
		"enforce_allowed_finishes": 1,
		"max_discount_percent": 5,
		"minimum_profit_margin": 10,
		"required_advance_percent": 20,
		"default_warranty_period": 12,
		"default_warranty_unit": "Months",
		"design_approval_required_for_custom": 1,
		"qc_mandatory_before_dispatch": 1,
	}
	for key, value in defaults.items():
		if settings.meta.has_field(key) and not settings.get(key):
			settings.set(key, value)
			dirty = True
	if dirty:
		settings.save(ignore_permissions=True)
