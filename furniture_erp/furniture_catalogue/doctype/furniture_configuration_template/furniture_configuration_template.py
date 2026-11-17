# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FurnitureConfigurationTemplate(Document):

	def validate(self):
		pairs = (
			("minimum_width", "maximum_width", "Width"),
			("minimum_height", "maximum_height", "Height"),
			("minimum_depth", "maximum_depth", "Depth"),
		)
		for mn, mx, label in pairs:
			lo, hi = self.get(mn), self.get(mx)
			if lo is not None and hi is not None and lo > hi:
				frappe.throw(frappe._("Minimum {0} cannot exceed maximum {0}.").format(label))
		defaults = [r for r in (self.configuration_options or []) if r.default_option]
		if len(defaults) > 1:
			frappe.throw(frappe._("Only one default configuration option is allowed."))

