# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureVariant(Document):

	def before_naming(self):
		if self.variant_code:
			self.variant_code = self.variant_code.strip().upper()

	def validate(self):
		if self.variant_code:
			self.variant_code = self.variant_code.strip().upper()
		if not self.furniture_model:
			frappe.throw(frappe._("Furniture Model is required."))

