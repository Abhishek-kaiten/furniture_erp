# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today

from furniture_erp.sales_design.api import (
	create_quotation_from_requirement,
	create_requirement_from_opportunity,
	get_or_create_job_file,
)


def _ensure_company():
	if frappe.db.exists("Company", "_Test Furniture Co"):
		return "_Test Furniture Co"
	company = frappe.get_doc(
		{
			"doctype": "Company",
			"company_name": "_Test Furniture Co",
			"abbr": "_TFC",
			"default_currency": "INR",
			"country": "India",
		}
	)
	company.insert(ignore_permissions=True)
	return company.name


def _ensure_customer(name="_Test Furniture Customer"):
	if frappe.db.exists("Customer", name):
		return name
	customer_group = frappe.db.get_value("Customer Group", {"is_group": 0}, "name") or "Commercial"
	territory = frappe.db.get_value("Territory", {"is_group": 0}, "name") or "All Territories"
	if territory == "All Territories" and frappe.db.get_value("Territory", "All Territories", "is_group"):
		territory = frappe.db.get_value("Territory", {"is_group": 0}, "name") or "India"
	doc = frappe.get_doc(
		{
			"doctype": "Customer",
			"customer_name": name,
			"customer_type": "Company",
			"customer_group": customer_group,
			"territory": territory,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_item(code="_Test-Furniture-Item"):
	if frappe.db.exists("Item", code):
		return code
	# Item Group
	if not frappe.db.exists("Item Group", "All Item Groups"):
		frappe.get_doc(
			{"doctype": "Item Group", "item_group_name": "All Item Groups", "is_group": 1}
		).insert(ignore_permissions=True)
	doc = frappe.get_doc(
		{
			"doctype": "Item",
			"item_code": code,
			"item_name": code,
			"item_group": "All Item Groups",
			"stock_uom": "Nos",
			"is_stock_item": 0,
			"is_sales_item": 1,
			"include_item_in_manufacturing": 0,
		}
	)
	doc.insert(ignore_permissions=True)
	return code


class TestFurnitureCustomerRequirement(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		if "erpnext" not in frappe.get_installed_apps():
			raise cls.skipTest("ERPNext not installed")
		_ensure_company()
		_ensure_customer()
		_ensure_item()

	def test_item_amount_and_totals(self):
		req = frappe.get_doc(
			{
				"doctype": "Furniture Customer Requirement",
				"requirement_date": today(),
				"status": "Draft",
				"customer": "_Test Furniture Customer",
				"requirement_items": [
					{
						"item_code": "_Test-Furniture-Item",
						"quantity": 2,
						"estimated_rate": 1500,
					}
				],
			}
		)
		req.insert()
		self.assertEqual(req.requirement_items[0].estimated_amount, 3000)
		self.assertEqual(req.total_estimated_amount, 3000)
		self.assertEqual(req.total_quantity, 2)
		req.delete()

	def test_requirement_from_opportunity_and_unique_job_file(self):
		lead = frappe.get_doc(
			{
				"doctype": "Lead",
				"lead_name": "_Test Furniture Lead",
				"status": "Lead",
			}
		).insert(ignore_permissions=True)

		opp = frappe.get_doc(
			{
				"doctype": "Opportunity",
				"opportunity_from": "Lead",
				"party_name": lead.name,
				"opportunity_type": "Sales",
				"company": _ensure_company(),
				"furniture_project_type": "Residential",
				"furniture_project_budget": 50000,
			}
		).insert(ignore_permissions=True)

		req_name = create_requirement_from_opportunity(opp.name)
		req_name_2 = create_requirement_from_opportunity(opp.name)
		self.assertEqual(req_name, req_name_2)

		job1 = get_or_create_job_file(req_name)
		job2 = get_or_create_job_file(req_name)
		self.assertEqual(job1, job2)

		# duplicate Job File for same requirement must fail
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "Furniture Job File",
					"job_file_title": "Duplicate",
					"job_status": "Draft",
					"customer_requirement": req_name,
					"customer": "_Test Furniture Customer",
				}
			).insert()

		frappe.delete_doc("Furniture Job File", job1, force=True)
		frappe.delete_doc("Furniture Customer Requirement", req_name, force=True)
		frappe.delete_doc("Opportunity", opp.name, force=True)
		frappe.delete_doc("Lead", lead.name, force=True)

	def test_quotation_from_requirement_syncs_job_file(self):
		company = _ensure_company()
		customer = _ensure_customer()
		item = _ensure_item()

		req = frappe.get_doc(
			{
				"doctype": "Furniture Customer Requirement",
				"requirement_date": today(),
				"status": "Draft",
				"customer": customer,
				"project_name": "Quote Project",
				"requirement_items": [
					{"item_code": item, "quantity": 1, "estimated_rate": 2500}
				],
			}
		).insert()

		job = get_or_create_job_file(req.name)
		frappe.db.set_value("Furniture Job File", job, "company", company)

		quotation = create_quotation_from_requirement(req.name)
		self.assertTrue(frappe.db.exists("Quotation", quotation))
		q = frappe.get_doc("Quotation", quotation)
		self.assertEqual(q.furniture_job_file, job)
		self.assertEqual(q.furniture_customer_requirement, req.name)
		self.assertEqual(frappe.db.get_value("Furniture Job File", job, "quotation"), quotation)

		# second create without force should fail
		with self.assertRaises(frappe.ValidationError):
			create_quotation_from_requirement(req.name, force=0)

		frappe.delete_doc("Quotation", quotation, force=True)
		frappe.delete_doc("Furniture Job File", job, force=True)
		frappe.delete_doc("Furniture Customer Requirement", req.name, force=True)
