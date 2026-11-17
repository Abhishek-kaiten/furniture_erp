# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureModel(Document):

	def before_naming(self):
		if self.model_code:
			self.model_code = self.model_code.strip().upper()

	def validate(self):
		if self.model_code:
			self.model_code = self.model_code.strip().upper()
		for fname, label in (
			("standard_width", "Standard Width"),
			("standard_height", "Standard Height"),
			("standard_depth", "Standard Depth"),
		):
			value = self.get(fname)
			if value is not None and value < 0:
				frappe.throw(frappe._("{0} cannot be negative.").format(label))

