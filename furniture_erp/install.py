# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe

CUSTOM_ROLES = [
	"Furniture ERP Administrator",
	"Furniture Product Manager",
	"Sales Manager",
	"Sales Executive",
	"Showroom Manager",
	"Designer",
	"Measurement Technician",
	"Procurement Manager",
	"Buyer",
	"Store Manager",
	"Store User",
	"Production Planner",
	"Production Manager",
	"Machine Operator",
	"Quality Inspector",
	"Quality Manager",
	"Dispatch Coordinator",
	"Delivery Manager",
	"Installer",
	"Installation Supervisor",
	"Service Coordinator",
	"Service Technician",
	"Finance Manager",
	"Accounts User",
	"Project Manager",
	"Auditor",
]


def after_install():
	_ensure_roles()
	_seed_settings_defaults()


def after_migrate():
	_ensure_roles()
	_seed_settings_defaults()


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
		"enforce_allowed_materials": 1,
		"enforce_allowed_finishes": 1,
	}
	for key, value in defaults.items():
		if not settings.get(key):
			settings.set(key, value)
			dirty = True
	if dirty:
		settings.save(ignore_permissions=True)
