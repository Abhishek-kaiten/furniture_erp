# Copyright (c) 2026, abhishek and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFurnitureSpecification(FrappeTestCase):
	def setUp(self):
		suffix = frappe.generate_hash(length=6).upper()
		self.material = frappe.get_doc(
			{
				"doctype": "Furniture Material",
				"material_name": f"Test Plywood {suffix}",
				"material_code": f"MAT-SPEC-{suffix}",
				"material_type": "Plywood",
				"active": 1,
				"uom": "Sheet",
			}
		).insert()
		self.finish = frappe.get_doc(
			{
				"doctype": "Furniture Finish",
				"finish_name": f"Test Finish {suffix}",
				"finish_code": f"FIN-SPEC-{suffix}",
				"finish_type": "Laminate",
				"active": 1,
			}
		).insert()
		self.family = frappe.get_doc(
			{
				"doctype": "Furniture Product Family",
				"family_name": f"Test Wardrobe {suffix}",
				"status": "Active",
				"product_category": "Storage",
				"construction_type": "Panel",
				"is_configurable": 1,
				"naming_series": "FPF-.#####",
				"allowed_materials": [{"material": self.material.name, "is_default": 1}],
				"allowed_finishes": [{"finish": self.finish.name, "application": "All", "is_default": 1}],
			}
		).insert()

	def test_reject_non_allowed_material(self):
		suffix = frappe.generate_hash(length=6).upper()
		other = frappe.get_doc(
			{
				"doctype": "Furniture Material",
				"material_name": f"Blocked MDF {suffix}",
				"material_code": f"MAT-BLOCK-{suffix}",
				"material_type": "MDF",
				"active": 1,
				"uom": "Sheet",
			}
		).insert()
		settings = frappe.get_single("Furniture ERP Settings")
		settings.enforce_allowed_materials = 1
		settings.save()

		doc = frappe.get_doc(
			{
				"doctype": "Furniture Specification",
				"naming_series": "FSPEC-.YYYY.-.#####",
				"spec_title": "Blocked Spec",
				"product_family": self.family.name,
				"spec_status": "Draft",
				"version": 1,
				"width_mm": 1800,
				"depth_mm": 600,
				"height_mm": 2100,
				"primary_material": other.name,
				"primary_finish": self.finish.name,
			}
		)
		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_approve_requires_dimensions(self):
		doc = frappe.get_doc(
			{
				"doctype": "Furniture Specification",
				"naming_series": "FSPEC-.YYYY.-.#####",
				"spec_title": "Incomplete Spec",
				"product_family": self.family.name,
				"spec_status": "Approved",
				"version": 1,
				"width_mm": 1800,
				"depth_mm": 600,
				"height_mm": 2100,
				"primary_material": self.material.name,
			}
		)
		doc.primary_finish = None
		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_create_valid_draft(self):
		doc = frappe.get_doc(
			{
				"doctype": "Furniture Specification",
				"naming_series": "FSPEC-.YYYY.-.#####",
				"spec_title": "Valid Wardrobe Spec",
				"product_family": self.family.name,
				"spec_status": "Draft",
				"version": 1,
				"width_mm": 1800,
				"depth_mm": 600,
				"height_mm": 2100,
				"primary_material": self.material.name,
				"primary_finish": self.finish.name,
			}
		).insert()
		self.assertTrue(doc.name)
		self.assertEqual(doc.spec_status, "Draft")
