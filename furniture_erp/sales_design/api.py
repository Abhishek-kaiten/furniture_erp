# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt
"""Phase 3 CRM/Sales conversion APIs."""

from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt, today


def _require_erpnext():
	if "erpnext" not in frappe.get_installed_apps():
		frappe.throw(_("ERPNext must be installed for this action."))


def _check_perm(doctype: str, ptype: str = "write", doc=None):
	if not frappe.has_permission(doctype, ptype, doc=doc):
		frappe.throw(_("Not permitted"), frappe.PermissionError)


@frappe.whitelist()
def create_requirement_from_opportunity(opportunity: str) -> str:
	"""Create or return linked Furniture Customer Requirement for an Opportunity."""
	_require_erpnext()
	_check_perm("Opportunity", "write", opportunity)
	_check_perm("Furniture Customer Requirement", "create")

	opp = frappe.get_doc("Opportunity", opportunity)
	existing = opp.get("furniture_customer_requirement")
	if existing and frappe.db.exists("Furniture Customer Requirement", existing):
		return existing

	# also find by opportunity link
	found = frappe.db.get_value(
		"Furniture Customer Requirement", {"opportunity": opportunity}, "name"
	)
	if found:
		opp.db_set("furniture_customer_requirement", found, update_modified=False)
		return found

	customer = None
	if opp.opportunity_from == "Customer":
		customer = opp.party_name
	elif getattr(opp, "customer", None):
		customer = opp.customer

	req = frappe.get_doc(
		{
			"doctype": "Furniture Customer Requirement",
			"requirement_date": today(),
			"status": "Draft",
			"opportunity": opportunity,
			"lead": opp.party_name if opp.opportunity_from == "Lead" else None,
			"customer": customer,
			"project_name": opp.customer_name or opportunity,
			"project_type": opp.get("furniture_project_type"),
			"project_location": opp.get("furniture_project_location"),
			"customer_budget": opp.get("furniture_project_budget") or opp.get("opportunity_amount"),
			"requirement_description": opp.get("notes") or "",
			"priority": "Medium",
		}
	)
	req.insert(ignore_permissions=False)
	opp.db_set("furniture_customer_requirement", req.name, update_modified=False)
	if opp.get("furniture_job_file"):
		req.db_set("furniture_job_file", opp.furniture_job_file, update_modified=False)
	return req.name


@frappe.whitelist()
def get_or_create_job_file(requirement: str) -> str:
	"""Return existing Job File for a requirement or create one. Never duplicates."""
	_check_perm("Furniture Customer Requirement", "write", requirement)
	_check_perm("Furniture Job File", "create")

	req = frappe.get_doc("Furniture Customer Requirement", requirement)
	if req.furniture_job_file and frappe.db.exists("Furniture Job File", req.furniture_job_file):
		return req.furniture_job_file

	existing = frappe.db.get_value(
		"Furniture Job File", {"customer_requirement": requirement}, "name"
	)
	if existing:
		req.db_set("furniture_job_file", existing, update_modified=False)
		return existing

	title = req.project_name or req.customer or requirement
	job = frappe.get_doc(
		{
			"doctype": "Furniture Job File",
			"job_file_title": title,
			"job_status": "Quotation Pending",
			"customer": req.customer,
			"lead": req.lead,
			"opportunity": req.opportunity,
			"customer_requirement": requirement,
			"job_type": req.requirement_type or "Custom",
			"priority": req.priority or "Medium",
			"job_creation_date": today(),
			"expected_completion_date": req.preferred_delivery_date,
			"project_location": req.project_location,
			"installation_site": req.site_address,
			"project_value": req.total_estimated_amount or req.customer_budget,
		}
	)
	job.insert(ignore_permissions=False)
	req.db_set("furniture_job_file", job.name, update_modified=False)

	# back-link on Opportunity / Lead when present
	if req.opportunity and frappe.db.exists("Opportunity", req.opportunity):
		frappe.db.set_value(
			"Opportunity", req.opportunity, "furniture_job_file", job.name, update_modified=False
		)
	if req.lead and frappe.db.exists("Lead", req.lead):
		frappe.db.set_value("Lead", req.lead, "furniture_job_file", job.name, update_modified=False)

	return job.name


@frappe.whitelist()
def create_quotation_from_requirement(requirement: str, force: int = 0) -> str:
	"""Create a draft Quotation from requirement items; link Job File."""
	_require_erpnext()
	_check_perm("Furniture Customer Requirement", "read", requirement)
	_check_perm("Quotation", "create")

	req = frappe.get_doc("Furniture Customer Requirement", requirement)
	job_name = get_or_create_job_file(requirement)
	job = frappe.get_doc("Furniture Job File", job_name)

	if job.quotation and not int(force or 0):
		if frappe.db.exists("Quotation", job.quotation):
			frappe.throw(
				_("Quotation {0} already linked to Job File {1}. Pass force=1 to create another.").format(
					job.quotation, job_name
				)
			)

	if not req.customer:
		frappe.throw(_("Customer is required on the Requirement before creating a Quotation."))

	company = job.company or frappe.db.get_single_value("Global Defaults", "default_company")
	if not company:
		companies = frappe.get_all("Company", pluck="name", limit=1)
		company = companies[0] if companies else None
	if not company:
		frappe.throw(_("Set Company on Job File or create a Company first."))

	items = []
	for row in req.requirement_items or []:
		item_code = row.item_code
		if not item_code:
			frappe.throw(
				_("Row {0}: Item Code is required to create Quotation lines.").format(row.idx)
			)
		items.append(
			{
				"item_code": item_code,
				"qty": row.quantity or 1,
				"rate": row.estimated_rate or 0,
				"uom": row.uom,
				"description": row.description,
				"furniture_category": row.furniture_category,
				"furniture_model": row.furniture_model,
				"furniture_variant": row.furniture_variant,
				"furniture_material": row.material,
				"furniture_finish": row.finish,
				"furniture_color": row.color,
				"furniture_length": row.length,
				"furniture_width": row.width,
				"furniture_height": row.height,
			}
		)
	if not items:
		frappe.throw(_("Add at least one requirement item with Item Code."))

	quotation = frappe.get_doc(
		{
			"doctype": "Quotation",
			"quotation_to": "Customer",
			"party_name": req.customer,
			"transaction_date": today(),
			"company": company,
			"furniture_job_file": job_name,
			"furniture_customer_requirement": requirement,
			"furniture_project_type": req.project_type,
			"furniture_customization_notes": req.remarks,
			"items": items,
		}
	)
	quotation.insert(ignore_permissions=False)
	job.db_set("quotation", quotation.name, update_modified=False)
	if job.job_status in ("Draft", "Requirement Pending", "Quotation Pending"):
		job.db_set("job_status", "Quotation Pending", update_modified=False)
	return quotation.name


def sync_job_file_from_quotation(doc, method=None):
	"""Keep Job File quotation link and status in sync."""
	job_name = doc.get("furniture_job_file")
	if not job_name or not frappe.db.exists("Furniture Job File", job_name):
		return
	job = frappe.get_doc("Furniture Job File", job_name)
	updates = {}
	if job.quotation != doc.name:
		updates["quotation"] = doc.name
	if doc.docstatus == 1 and job.job_status not in (
		"Sales Order Confirmed",
		"Completed",
		"Closed",
		"Cancelled",
	):
		updates["job_status"] = "Quotation Approved"
	if doc.get("grand_total"):
		updates["project_value"] = flt(doc.grand_total)
		updates["order_amount"] = flt(doc.grand_total)
	if updates:
		job.db_set(updates, update_modified=False)


def sync_job_file_from_sales_order(doc, method=None):
	"""Keep Job File sales order link and status in sync."""
	job_name = doc.get("furniture_job_file")
	if not job_name or not frappe.db.exists("Furniture Job File", job_name):
		# try copy from quotation
		if doc.get("quotation") and frappe.db.exists("Quotation", doc.quotation):
			job_name = frappe.db.get_value("Quotation", doc.quotation, "furniture_job_file")
			if job_name:
				doc.db_set("furniture_job_file", job_name, update_modified=False)
				req = frappe.db.get_value("Quotation", doc.quotation, "furniture_customer_requirement")
				if req and not doc.get("furniture_customer_requirement"):
					doc.db_set("furniture_customer_requirement", req, update_modified=False)
	if not job_name or not frappe.db.exists("Furniture Job File", job_name):
		return
	job = frappe.get_doc("Furniture Job File", job_name)
	updates = {"sales_order": doc.name}
	if doc.docstatus == 1:
		updates["job_status"] = "Sales Order Confirmed"
	if doc.get("grand_total"):
		updates["project_value"] = flt(doc.grand_total)
		updates["order_amount"] = flt(doc.grand_total)
	job.db_set(updates, update_modified=False)


@frappe.whitelist()
def make_sales_order_from_quotation(quotation: str) -> str:
	"""Wrapper around ERPNext make_sales_order that preserves furniture links."""
	_require_erpnext()
	_check_perm("Quotation", "write", quotation)
	from erpnext.selling.doctype.quotation.quotation import make_sales_order

	so = make_sales_order(quotation)
	q = frappe.get_doc("Quotation", quotation)
	if isinstance(so, dict) or not hasattr(so, "insert"):
		# older APIs return dict-like mapped doc
		so_doc = frappe.get_doc(so)
	else:
		so_doc = so
	so_doc.furniture_job_file = q.get("furniture_job_file")
	so_doc.furniture_customer_requirement = q.get("furniture_customer_requirement")
	so_doc.furniture_installation_required = q.get("furniture_installation_required")
	if not so_doc.get("name"):
		so_doc.insert(ignore_permissions=False)
	sync_job_file_from_sales_order(so_doc)
	return so_doc.name
