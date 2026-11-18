# Phase 3 Completion Checklist — CRM and Sales

**Branch:** `feature/phase-3-crm-sales`  
**Depends on:** DEC-002 ERPNext install

## Environment

- [x] ERPNext `develop` installed on `carpenter`
- [x] ERPNext `develop` installed on `test_carpenter`
- [x] `required_apps = ["erpnext"]`
- [x] Module rename: Setup → Furniture Setup, Manufacturing → Furniture Manufacturing
- [x] Install notes documented (`docs/erpnext-install-notes.md`)

## Data → Link

- [x] Patch `convert_erpnext_data_to_link`
- [x] Requirement / Job File / catalogue JSON fieldtypes updated
- [x] Phase 4+ placeholders left as Data (`site_survey`, etc.)

## DocTypes extended

- [x] Furniture Customer Requirement (Links + location/address/totals)
- [x] Furniture Requirement Item (family, design, length, UOM, customization details)
- [x] Furniture Job File hub (Links, progress/value, linked docs HTML, duplicate prevention)

## ERPNext custom fields

- [x] Lead, Opportunity, Customer, Quotation, Quotation Item, Sales Order
- [x] Synced via `after_migrate` + fixtures filter in `hooks.py`
- [x] Client scripts: Lead, Opportunity, Quotation, Sales Order

## APIs

- [x] `create_requirement_from_opportunity`
- [x] `get_or_create_job_file` (no duplicates)
- [x] `create_quotation_from_requirement`
- [x] Quotation / Sales Order `doc_events` sync to Job File
- [x] `make_sales_order_from_quotation` wrapper

## Tests

- [x] Requirement amount/totals
- [x] Opportunity → Requirement uniqueness
- [x] Job File uniqueness
- [x] Quotation create + Job File sync + duplicate guard
- [x] `bench --site carpenter run-tests --app furniture_erp` → **11/11 OK**
- [x] `bench --site test_carpenter run-tests --app furniture_erp` → **11/11 OK**

## Out of scope (later phases)

- Site Survey / Design Approval (Phase 4)
- Purchase / Stock / Manufacturing / QC / Payments / Warranty / Dashboards (Phases 5–10)
