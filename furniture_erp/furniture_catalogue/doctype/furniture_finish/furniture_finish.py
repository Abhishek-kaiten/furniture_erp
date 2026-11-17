# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureFinish(Document):

	def before_naming(self):
		if self.finish_code:
			self.finish_code = self.finish_code.strip().upper()

	def validate(self):
		if self.finish_code:
			self.finish_code = self.finish_code.strip().upper()
		if self.active is not None:
			self.status = "Active" if self.active else "Inactive"

