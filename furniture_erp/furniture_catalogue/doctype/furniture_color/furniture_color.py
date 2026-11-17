# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureColor(Document):

	def before_naming(self):
		if self.color_code:
			self.color_code = self.color_code.strip().upper()

	def validate(self):
		if self.color_code:
			self.color_code = self.color_code.strip().upper()

