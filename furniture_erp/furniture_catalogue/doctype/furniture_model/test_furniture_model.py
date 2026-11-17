# Copyright (c) 2026, abhishek and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFurnitureModel(FrappeTestCase):
	def setUp(self):
		suffix = frappe.generate_hash(length=6).upper()
		self.category = frappe.get_doc(
			{
				"doctype": "Furniture Category",
				"category_name": "Wardrobe Cat",
				"category_code": f"CAT-WRD-{suffix}",
			}
		).insert()
		self.material = frappe.get_doc(
			{
				"doctype": "Furniture Material",
				"material_name": "Model Test Ply",
				"material_code": f"MAT-MOD-{suffix}",
				"material_type": "Plywood",
				"active": 1,
				"uom": "Sheet",
			}
		).insert()
		self.finish = frappe.get_doc(
			{
				"doctype": "Furniture Finish",
				"finish_name": "Model Test Finish",
				"finish_code": f"FIN-MOD-{suffix}",
				"finish_type": "Laminate",
				"active": 1,
			}
		).insert()
		self.color = frappe.get_doc(
			{
				"doctype": "Furniture Color",
				"color_name": "Walnut",
				"color_code": f"COL-WAL-{suffix}",
				"active": 1,
			}
		).insert()
		self.suffix = suffix

	def test_model_and_variant(self):
		model = frappe.get_doc(
			{
				"doctype": "Furniture Model",
				"model_name": "Sliding Wardrobe",
				"model_code": f"MOD-SW-{self.suffix}",
				"furniture_category": self.category.name,
				"model_type": "Custom",
				"active": 1,
				"default_material": self.material.name,
				"default_finish": self.finish.name,
				"default_color": self.color.name,
				"standard_width": 1800,
			}
		).insert()
		variant = frappe.get_doc(
			{
				"doctype": "Furniture Variant",
				"variant_name": "SW 1800 Walnut",
				"variant_code": f"VAR-SW-{self.suffix}",
				"furniture_model": model.name,
				"material": self.material.name,
				"finish": self.finish.name,
				"color": self.color.name,
				"selling_price": 45000,
			}
		).insert()
		self.assertEqual(variant.furniture_model, model.name)
		self.assertEqual(model.model_code, f"MOD-SW-{self.suffix}")
