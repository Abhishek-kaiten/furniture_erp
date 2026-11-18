# Copyright (c) 2026, abhishek and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFurnitureJobFile(FrappeTestCase):
	def test_create_job_file_and_requirement(self):
		req = frappe.get_doc(
			{
				"doctype": "Furniture Customer Requirement",
				"naming_series": "FCR-.YYYY.-.#####",
				"requirement_date": frappe.utils.today(),
				"requirement_type": "Custom",
				"status": "Draft",
				"project_name": "Demo Custom Wardrobe",
				"requirement_items": [
					{
						"description": "Wardrobe",
						"quantity": 2,
						"estimated_rate": 25000,
					}
				],
			}
		).insert()
		self.assertEqual(req.requirement_items[0].estimated_amount, 50000)
		self.assertEqual(req.total_estimated_amount, 50000)

		job = frappe.get_doc(
			{
				"doctype": "Furniture Job File",
				"naming_series": "FJF-.YYYY.-.#####",
				"job_file_title": "Demo Custom Wardrobe Job",
				"job_type": "Custom",
				"job_status": "Draft",
				"customer_requirement": req.name,
				"order_amount": 100000,
				"received_amount": 20000,
			}
		).insert()
		self.assertEqual(job.outstanding_amount, 80000)

	def test_outstanding_cannot_go_negative(self):
		job = frappe.get_doc(
			{
				"doctype": "Furniture Job File",
				"naming_series": "FJF-.YYYY.-.#####",
				"job_file_title": "Bad Payment Job",
				"job_status": "Draft",
				"order_amount": 1000,
				"received_amount": 1500,
			}
		)
		self.assertRaises(frappe.ValidationError, job.insert)
