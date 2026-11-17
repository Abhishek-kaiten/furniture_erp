# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureJobFile(Document):

	def validate(self):
		if not (self.job_file_title or "").strip():
			frappe.throw(frappe._("Job File Title is required."))
		order = self.order_amount or 0
		received = self.received_amount or 0
		self.outstanding_amount = order - received
		if self.outstanding_amount < 0:
			frappe.throw(frappe._("Received Amount cannot exceed Order Amount."))

