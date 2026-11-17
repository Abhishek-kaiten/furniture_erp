# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureDesign(Document):

	def before_naming(self):
		if self.design_code:
			self.design_code = self.design_code.strip().upper()

	def validate(self):
		if self.design_code:
			self.design_code = self.design_code.strip().upper()

