# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureCustomerRequirement(Document):

	def validate(self):
		for row in self.requirement_items or []:
			qty = row.quantity or 0
			rate = row.estimated_rate or 0
			row.estimated_amount = qty * rate
			if qty <= 0:
				frappe.throw(frappe._("Quantity must be greater than zero in row {0}.").format(row.idx))

