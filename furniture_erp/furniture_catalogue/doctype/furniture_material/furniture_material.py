# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureMaterial(Document):

	def before_naming(self):
		if self.material_code:
			self.material_code = self.material_code.strip().upper()

	def validate(self):
		if self.material_code:
			self.material_code = self.material_code.strip().upper()
		if self.active is not None:
			self.status = "Active" if self.active else "Inactive"
		if self.material_grade and not self.grade:
			self.grade = self.material_grade
		if self.item_code and not self.linked_item_code:
			self.linked_item_code = self.item_code
		if self.thickness and not self.default_thickness_mm:
			self.default_thickness_mm = self.thickness
		if self.width and not self.default_width_mm:
			self.default_width_mm = self.width
		if self.length and not self.default_length_mm:
			self.default_length_mm = self.length
		if self.standard_rate and not self.reference_rate:
			self.reference_rate = self.standard_rate

