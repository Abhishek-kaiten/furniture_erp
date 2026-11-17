# Assumptions & Decisions Register

Living register for Furniture ERP discovery and delivery. Status: **Proposed** until stakeholder sign-off unless marked **Decided**.

## Critical decisions

| ID | Date | Topic | Decision | Status | Rationale / impact |
|----|------|-------|----------|--------|-------------------|
| DEC-001 | 2025-11-14 | ERPNext installation | **ERPNext is not installed** on site `carpenter`. Target architecture assumes ERPNext will be installed before transactional milestones (SO, stock, GL). | **Decided (environment fact)** | Blocks reuse of Customer, Item, BOM, SO, PO, Stock Entry, Payment Entry, GST. All related requirements **blocked** until DEC-002. |
| DEC-002 | — | ERPNext install gate | Install ERPNext version compatible with Frappe 17 on `carpenter` and `test_carpenter`, add `required_apps`. | Proposed | Unblocks standard-vs-custom matrix execution. |
| DEC-003 | 2025-11-14 | Requirements source | **No formal BRD** supplied. Master Build Prompt v1.0 is baseline; gaps flagged in traceability CSV. | **Decided (discovery)** | Legal/commercial scope not contractually frozen. |
| DEC-004 | 2025-11-14 | Tax jurisdiction | **India (GST)** assumed as default for tax templates, HSN, place of supply. | Proposed (pending confirmation) | Drives Item tax templates, e-invoice/e-way assumptions in accounting-stock-design.md. |
| DEC-005 | 2025-11-14 | App naming | Package `furniture_erp`, display **Furniture ERP**; module folder `Furniture_erp` until renamed. | Decided | Align UI strings in M1. |
| DEC-006 | — | Variant strategy | Use ERPNext Item + Attributes / Template Items for configurable SKUs; catalogue in `furniture_erp` holds design intent. | Proposed | Avoid duplicate item master. |
| DEC-007 | — | Multi-warehouse | Factory, finished goods, site/WIP warehouses per company standard ERPNext pattern. | Proposed | Detailed in accounting-stock-design.md. |
| DEC-008 | — | India Compliance app | Evaluate `india_compliance` (or ERPNext built-in GST for v17) at ERPNext install. | Proposed | Depends on ERPNext version choice. |
| DEC-009 | 2026-11-14 | Development bench | Implement Master Development Prompt on **`~/carpenter_erp`**, not `~/frappe-bench`. | **Decided** | GitHub app lives on carpenter_erp; frappe-bench has ERPNext v16 incompatible with Frappe 17. |
| DEC-010 | 2026-11-14 | Phase 2 ERPNext fields | Store ERPNext targets as **Data** placeholders; convert via patch after DEC-002. | **Decided** | See `docs/phase2-field-map.md`. |
| DEC-011 | 2026-11-14 | Product Family vs Category | Keep **Furniture Product Family**; add **Furniture Category / Model / Variant** per Master Prompt §4. | **Decided** | Family remains allowlist helper; Category is commercial taxonomy. |

## Assumptions

| ID | Assumption | Risk if wrong |
|----|------------|---------------|
| ASM-001 | Business is B2B and B2C furniture with made-to-order and some catalogue SKUs. | Process flows and roles may need redesign. |
| ASM-002 | Single primary company on site `carpenter` initially. | Multi-company permissions and reporting scope change. |
| ASM-003 | Dimensions use metric (mm) for manufacturing; display can show ft/in. | Field types and conversion rules change. |
| ASM-004 | Shop floor captured via Job Card / Work Order, not third-party MES in v1. | Integration register scope grows. |
| ASM-005 | Payment gateways and logistics APIs are phase-2+ unless listed in Master Prompt §P. | Integration effort deferred. |
| ASM-006 | Users operate primarily in English UI. | Translation and label work later. |
| ASM-007 | Frappe 17 dev track stability acceptable for greenfield bench. | Pin versions before UAT. |

## Open questions

| ID | Question | Owner | Due |
|----|----------|-------|-----|
| OQ-001 | Confirm India GST and state(s) of registration. | Finance | Before M3 pricing/tax |
| OQ-002 | Provide signed BRD or amend Master Build Prompt v1.0. | Product | Before M2 freeze |
| OQ-003 | ERPNext version and India compliance package selection. | Tech | DEC-002 |
| OQ-004 | Variant explosion limits (max attributes per family). | Product / Eng | Before configurator M4 |
| OQ-005 | Installation/delivery as separate service Item? | Operations | Before SO design |

## BRD status

| Document | Status |
|----------|--------|
| Business Requirements Document | **Missing** |
| Master Build Prompt v1.0 | **Baseline** (referenced in requirements-traceability.csv) |
| Milestone 0 discovery pack | **This docs folder** |

## Change log

| Date | Change |
|------|--------|
| 2025-11-14 | Initial M0 register: ERPNext absent, BRD missing, India GST default. |