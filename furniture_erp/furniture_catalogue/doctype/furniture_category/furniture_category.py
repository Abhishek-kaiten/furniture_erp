# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureCategory(Document):

	def before_naming(self):
		if self.category_code:
			self.category_code = self.category_code.strip().upper()

	def validate(self):
		if self.parent_category and self.parent_category == self.name:
			frappe.throw(frappe._("Parent Category cannot be the same as this Category."))
		if self.category_code:
			self.category_code = self.category_code.strip().upper()

