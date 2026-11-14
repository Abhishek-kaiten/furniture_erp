# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureProductFamily(Document):

	def validate(self):
		self._validate_single_default(self.allowed_materials, "material")
		self._validate_single_default(self.allowed_finishes, "finish")

	def _validate_single_default(self, rows, label):
		defaults = [row for row in (rows or []) if row.is_default]
		if len(defaults) > 1:
			frappe.throw(frappe._("Only one default {0} is allowed.").format(label))

