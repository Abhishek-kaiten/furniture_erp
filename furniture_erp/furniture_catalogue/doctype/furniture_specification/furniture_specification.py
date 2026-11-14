# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureSpecification(Document):

	def validate(self):
		self._validate_dimensions()
		self._validate_allowlists()
		self._validate_approval_ready()

	def before_save(self):
		if self.amended_from and not self.flags.in_insert_from_amend:
			pass

	def _validate_dimensions(self):
		for fieldname, label in (("width_mm", "Width"), ("depth_mm", "Depth"), ("height_mm", "Height")):
			value = self.get(fieldname)
			if value is not None and value <= 0:
				frappe.throw(frappe._("{0} must be greater than zero.").format(label))

	def _settings(self):
		if frappe.db.exists("DocType", "Furniture ERP Settings"):
			return frappe.get_single("Furniture ERP Settings")
		return None

	def _validate_allowlists(self):
		settings = self._settings()
		if not settings or not self.product_family:
			return
		family = frappe.get_doc("Furniture Product Family", self.product_family)
		if settings.enforce_allowed_materials and self.primary_material:
			allowed = {row.material for row in family.allowed_materials or []}
			if allowed and self.primary_material not in allowed:
				frappe.throw(
					frappe._("Primary Material {0} is not allowed for family {1}.").format(
						self.primary_material, self.product_family
					)
				)
		if settings.enforce_allowed_finishes:
			allowed = {row.finish for row in family.allowed_finishes or []}
			if allowed:
				for fieldname, label in (
					("primary_finish", "Primary Finish"),
					("secondary_finish", "Secondary Finish"),
					("edge_band_finish", "Edge Band Finish"),
				):
					value = self.get(fieldname)
					if value and value not in allowed:
						frappe.throw(
							frappe._("{0} {1} is not allowed for family {2}.").format(
								label, value, self.product_family
							)
						)

	def _validate_approval_ready(self):
		if self.spec_status != "Approved":
			return
		missing = []
		for fieldname, label in (
			("width_mm", "Width"),
			("depth_mm", "Depth"),
			("height_mm", "Height"),
			("primary_material", "Primary Material"),
			("primary_finish", "Primary Finish"),
		):
			if not self.get(fieldname):
				missing.append(label)
		if missing:
			frappe.throw(frappe._("Cannot approve specification. Missing: {0}").format(", ".join(missing)))

