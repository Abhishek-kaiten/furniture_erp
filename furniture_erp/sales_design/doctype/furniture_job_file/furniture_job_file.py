# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class FurnitureJobFile(Document):
	def validate(self):
		if not (self.job_file_title or "").strip():
			frappe.throw(frappe._("Job File Title is required."))
		self._prevent_duplicate_requirement()
		order = self.order_amount or 0
		received = self.received_amount or 0
		self.outstanding_amount = order - received
		if self.outstanding_amount < 0:
			frappe.throw(frappe._("Received Amount cannot exceed Order Amount."))
		if self.project_value is None and self.order_amount:
			self.project_value = self.order_amount

	def onload(self):
		self.set_onload("linked_documents_html", self.build_hub_html())

	def _prevent_duplicate_requirement(self):
		if not self.customer_requirement:
			return
		other = frappe.db.get_value(
			"Furniture Job File",
			{"customer_requirement": self.customer_requirement, "name": ("!=", self.name)},
			"name",
		)
		if other:
			frappe.throw(
				frappe._(
					"Requirement {0} already has Job File {1}. Duplicate Job Files are not allowed."
				).format(self.customer_requirement, other)
			)

	def build_hub_html(self) -> str:
		rows = []
		pairs = [
			("Lead", self.lead),
			("Opportunity", self.opportunity),
			("Customer", self.customer),
			("Furniture Customer Requirement", self.customer_requirement),
			("Quotation", self.quotation),
			("Sales Order", self.sales_order),
			("Site Survey", self.site_survey),
			("Production Plan", self.production_plan),
		]
		for label, value in pairs:
			if not value:
				continue
			safe_label = frappe.utils.escape_html(label)
			safe_value = frappe.utils.escape_html(str(value))
			if frappe.db.exists("DocType", label) and frappe.db.exists(label, value):
				route = frappe.scrub(label)
				rows.append(
					f"<li><strong>{safe_label}</strong>: "
					f"<a href='/app/{route}/{safe_value}'>{safe_value}</a></li>"
				)
			else:
				rows.append(f"<li><strong>{safe_label}</strong>: {safe_value}</li>")
		progress = flt(self.progress_percentage)
		status = frappe.utils.escape_html(self.job_status or "")
		body = "".join(rows) if rows else "<li>No linked documents yet.</li>"
		return (
			f"<p><strong>Status:</strong> {status} &nbsp;|&nbsp; "
			f"<strong>Progress:</strong> {progress}%</p><ul>{body}</ul>"
		)
