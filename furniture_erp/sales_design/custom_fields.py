# Copyright (c) 2026, abhishek and contributors
# For license information, please see license.txt
"""Furniture-specific Custom Fields on ERPNext CRM/Sales DocTypes."""

from __future__ import annotations

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def get_custom_fields() -> dict:
	return {
		"Lead": [
			{
				"fieldname": "furniture_section",
				"fieldtype": "Section Break",
				"label": "Furniture Details",
				"insert_after": "notes",
				"collapsible": 1,
			},
			{
				"fieldname": "furniture_business_type",
				"fieldtype": "Select",
				"label": "Furniture Business Type",
				"options": "\nRetail\nProject\nWholesale\nInterior Designer",
				"insert_after": "furniture_section",
			},
			{
				"fieldname": "requirement_category",
				"fieldtype": "Link",
				"label": "Requirement Category",
				"options": "Furniture Category",
				"insert_after": "furniture_business_type",
			},
			{
				"fieldname": "interested_furniture_models",
				"fieldtype": "Small Text",
				"label": "Interested Furniture Models",
				"insert_after": "requirement_category",
			},
			{
				"fieldname": "preferred_material",
				"fieldtype": "Link",
				"label": "Preferred Material",
				"options": "Furniture Material",
				"insert_after": "interested_furniture_models",
			},
			{
				"fieldname": "preferred_finish",
				"fieldtype": "Link",
				"label": "Preferred Finish",
				"options": "Furniture Finish",
				"insert_after": "preferred_material",
			},
			{
				"fieldname": "approximate_budget",
				"fieldtype": "Currency",
				"label": "Approximate Budget",
				"insert_after": "preferred_finish",
			},
			{
				"fieldname": "project_location",
				"fieldtype": "Data",
				"label": "Project Location",
				"insert_after": "approximate_budget",
			},
			{
				"fieldname": "expected_purchase_date",
				"fieldtype": "Date",
				"label": "Expected Purchase Date",
				"insert_after": "project_location",
			},
			{
				"fieldname": "requirement_summary",
				"fieldtype": "Small Text",
				"label": "Requirement Summary",
				"insert_after": "expected_purchase_date",
			},
			{
				"fieldname": "furniture_job_file",
				"fieldtype": "Link",
				"label": "Furniture Job File",
				"options": "Furniture Job File",
				"insert_after": "requirement_summary",
			},
		],
		"Opportunity": [
			{
				"fieldname": "furniture_section",
				"fieldtype": "Section Break",
				"label": "Furniture Details",
				"insert_after": "notes",
				"collapsible": 1,
			},
			{
				"fieldname": "furniture_customer_requirement",
				"fieldtype": "Link",
				"label": "Furniture Customer Requirement",
				"options": "Furniture Customer Requirement",
				"insert_after": "furniture_section",
			},
			{
				"fieldname": "furniture_project_type",
				"fieldtype": "Select",
				"label": "Project Type",
				"options": "\nResidential\nCommercial\nOffice\nHotel",
				"insert_after": "furniture_customer_requirement",
			},
			{
				"fieldname": "furniture_project_budget",
				"fieldtype": "Currency",
				"label": "Project Budget",
				"insert_after": "furniture_project_type",
			},
			{
				"fieldname": "furniture_project_timeline",
				"fieldtype": "Data",
				"label": "Project Timeline",
				"insert_after": "furniture_project_budget",
			},
			{
				"fieldname": "furniture_project_location",
				"fieldtype": "Data",
				"label": "Project Location",
				"insert_after": "furniture_project_timeline",
			},
			{
				"fieldname": "expected_furniture_value",
				"fieldtype": "Currency",
				"label": "Expected Furniture Value",
				"insert_after": "furniture_project_location",
			},
			{
				"fieldname": "furniture_job_file",
				"fieldtype": "Link",
				"label": "Furniture Job File",
				"options": "Furniture Job File",
				"insert_after": "expected_furniture_value",
			},
		],
		"Customer": [
			{
				"fieldname": "furniture_section",
				"fieldtype": "Section Break",
				"label": "Furniture Customer",
				"insert_after": "customer_details",
				"collapsible": 1,
			},
			{
				"fieldname": "furniture_customer_type",
				"fieldtype": "Select",
				"label": "Customer Type",
				"options": "\nB2B\nB2C\nInterior Designer\nBuilder",
				"insert_after": "furniture_section",
			},
			{
				"fieldname": "furniture_project_category",
				"fieldtype": "Data",
				"label": "Project Category",
				"insert_after": "furniture_customer_type",
			},
			{
				"fieldname": "furniture_site_address",
				"fieldtype": "Link",
				"label": "Site Address",
				"options": "Address",
				"insert_after": "furniture_project_category",
			},
			{
				"fieldname": "furniture_preferred_communication",
				"fieldtype": "Select",
				"label": "Preferred Communication Method",
				"options": "\nPhone\nEmail\nWhatsApp\nIn Person",
				"insert_after": "furniture_site_address",
			},
			{
				"fieldname": "furniture_customer_classification",
				"fieldtype": "Select",
				"label": "Customer Classification",
				"options": "\nStandard\nPremium\nVIP",
				"insert_after": "furniture_preferred_communication",
			},
			{
				"fieldname": "furniture_customer_since",
				"fieldtype": "Date",
				"label": "Furniture Customer Since",
				"insert_after": "furniture_customer_classification",
			},
		],
		"Quotation": [
			{
				"fieldname": "furniture_section",
				"fieldtype": "Section Break",
				"label": "Furniture Project",
				"insert_after": "opportunity",
				"collapsible": 1,
			},
			{
				"fieldname": "furniture_job_file",
				"fieldtype": "Link",
				"label": "Furniture Job File",
				"options": "Furniture Job File",
				"insert_after": "furniture_section",
			},
			{
				"fieldname": "furniture_customer_requirement",
				"fieldtype": "Link",
				"label": "Customer Requirement",
				"options": "Furniture Customer Requirement",
				"insert_after": "furniture_job_file",
			},
			{
				"fieldname": "furniture_design_reference",
				"fieldtype": "Data",
				"label": "Design Reference",
				"insert_after": "furniture_customer_requirement",
			},
			{
				"fieldname": "furniture_site_survey_reference",
				"fieldtype": "Data",
				"label": "Site Survey Reference",
				"insert_after": "furniture_design_reference",
			},
			{
				"fieldname": "furniture_project_type",
				"fieldtype": "Select",
				"label": "Furniture Project Type",
				"options": "\nResidential\nCommercial\nOffice\nHotel",
				"insert_after": "furniture_site_survey_reference",
			},
			{
				"fieldname": "furniture_design_revision",
				"fieldtype": "Data",
				"label": "Design Revision",
				"insert_after": "furniture_project_type",
			},
			{
				"fieldname": "furniture_installation_required",
				"fieldtype": "Check",
				"label": "Installation Required",
				"insert_after": "furniture_design_revision",
			},
			{
				"fieldname": "furniture_warranty_period",
				"fieldtype": "Data",
				"label": "Warranty Period",
				"insert_after": "furniture_installation_required",
			},
			{
				"fieldname": "furniture_customization_notes",
				"fieldtype": "Small Text",
				"label": "Customization Notes",
				"insert_after": "furniture_warranty_period",
			},
		],
		"Quotation Item": [
			{
				"fieldname": "furniture_category",
				"fieldtype": "Link",
				"label": "Furniture Category",
				"options": "Furniture Category",
				"insert_after": "item_code",
			},
			{
				"fieldname": "furniture_model",
				"fieldtype": "Link",
				"label": "Furniture Model",
				"options": "Furniture Model",
				"insert_after": "furniture_category",
			},
			{
				"fieldname": "furniture_variant",
				"fieldtype": "Link",
				"label": "Furniture Variant",
				"options": "Furniture Variant",
				"insert_after": "furniture_model",
			},
			{
				"fieldname": "furniture_material",
				"fieldtype": "Link",
				"label": "Material",
				"options": "Furniture Material",
				"insert_after": "furniture_variant",
			},
			{
				"fieldname": "furniture_finish",
				"fieldtype": "Link",
				"label": "Finish",
				"options": "Furniture Finish",
				"insert_after": "furniture_material",
			},
			{
				"fieldname": "furniture_color",
				"fieldtype": "Link",
				"label": "Color",
				"options": "Furniture Color",
				"insert_after": "furniture_finish",
			},
			{
				"fieldname": "furniture_length",
				"fieldtype": "Float",
				"label": "Length",
				"insert_after": "furniture_color",
			},
			{
				"fieldname": "furniture_width",
				"fieldtype": "Float",
				"label": "Width",
				"insert_after": "furniture_length",
			},
			{
				"fieldname": "furniture_height",
				"fieldtype": "Float",
				"label": "Height",
				"insert_after": "furniture_width",
			},
		],
		"Sales Order": [
			{
				"fieldname": "furniture_section",
				"fieldtype": "Section Break",
				"label": "Furniture Project",
				"insert_after": "title",
				"collapsible": 1,
			},
			{
				"fieldname": "furniture_job_file",
				"fieldtype": "Link",
				"label": "Furniture Job File",
				"options": "Furniture Job File",
				"insert_after": "furniture_section",
			},
			{
				"fieldname": "furniture_customer_requirement",
				"fieldtype": "Link",
				"label": "Furniture Customer Requirement",
				"options": "Furniture Customer Requirement",
				"insert_after": "furniture_job_file",
			},
			{
				"fieldname": "furniture_approved_design",
				"fieldtype": "Data",
				"label": "Approved Design",
				"insert_after": "furniture_customer_requirement",
			},
			{
				"fieldname": "furniture_project_manager",
				"fieldtype": "Link",
				"label": "Project Manager",
				"options": "Employee",
				"insert_after": "furniture_approved_design",
			},
			{
				"fieldname": "furniture_project_delivery_date",
				"fieldtype": "Date",
				"label": "Project Delivery Date",
				"insert_after": "furniture_project_manager",
			},
			{
				"fieldname": "furniture_installation_required",
				"fieldtype": "Check",
				"label": "Installation Required",
				"insert_after": "furniture_project_delivery_date",
			},
			{
				"fieldname": "furniture_payment_terms_reference",
				"fieldtype": "Data",
				"label": "Payment Terms Reference",
				"insert_after": "furniture_installation_required",
			},
			{
				"fieldname": "furniture_warranty_reference",
				"fieldtype": "Data",
				"label": "Warranty Reference",
				"insert_after": "furniture_payment_terms_reference",
			},
		],
	}


def sync_custom_fields() -> None:
	if "erpnext" not in frappe.get_installed_apps():
		return
	create_custom_fields(get_custom_fields(), update=True)
