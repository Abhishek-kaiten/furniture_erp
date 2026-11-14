# Copyright (c) 2026, abhishek and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFurnitureCategory(FrappeTestCase):
	def test_parent_cannot_be_self(self):
		suffix = frappe.generate_hash(length=6).upper()
		cat = frappe.get_doc(
			{
				"doctype": "Furniture Category",
				"category_name": "Seating",
				"category_code": f"CAT-SEAT-{suffix}",
			}
		).insert()
		cat.parent_category = cat.name
		self.assertRaises(frappe.ValidationError, cat.save)

	def test_code_normalized(self):
		suffix = frappe.generate_hash(length=6)
		cat = frappe.get_doc(
			{
				"doctype": "Furniture Category",
				"category_name": "Bedroom",
				"category_code": f"cat-bed-{suffix}",
			}
		).insert()
		self.assertEqual(cat.category_code, f"CAT-BED-{suffix.upper()}")
		self.assertEqual(cat.name, cat.category_code)
