# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureCustomerRequirement(Document):
	def validate(self):
		self._validate_items()
		self._validate_job_file_uniqueness()
		self._compute_totals()

	def _validate_items(self):
		for row in self.requirement_items or []:
			qty = row.quantity or 0
			rate = row.estimated_rate or 0
			row.estimated_amount = qty * rate
			if qty <= 0:
				frappe.throw(frappe._("Quantity must be greater than zero in row {0}.").format(row.idx))

	def _validate_job_file_uniqueness(self):
		if not self.furniture_job_file:
			return
		other = frappe.db.get_value(
			"Furniture Customer Requirement",
			{
				"furniture_job_file": self.furniture_job_file,
				"name": ("!=", self.name),
			},
			"name",
		)
		# Same Job File can only map to one requirement (1:1 hub rule for creation path)
		# Allow if the job file's customer_requirement points to this doc.
		job_req = frappe.db.get_value(
			"Furniture Job File", self.furniture_job_file, "customer_requirement"
		)
		if job_req and job_req != self.name and other:
			frappe.throw(
				frappe._("Job File {0} is already linked to Requirement {1}.").format(
					self.furniture_job_file, job_req
				)
			)

	def _compute_totals(self):
		total_qty = 0
		total_amt = 0
		for row in self.requirement_items or []:
			total_qty += row.quantity or 0
			total_amt += row.estimated_amount or 0
		self.total_quantity = total_qty
		self.total_estimated_amount = total_amt
