# Phase 1 — Application Audit (Master Development Prompt)

**Date:** 2026-11-14  
**Branch:** `feature/master-furniture-erp-phases` (from `dev`)  
**App path (actual):** `~/carpenter_erp/apps/furniture_erp`  
**Prompt path note:** Prompt cites `~/frappe-bench/apps/furniture_erp` — that folder does **not** exist. Work continues on `carpenter_erp` where the GitHub app lives.

## Environment

| Bench | Frappe | ERPNext | furniture_erp |
|-------|--------|---------|---------------|
| `~/carpenter_erp` | **17.0.0-dev** | **Not installed** | Yes (active) |
| `~/carpenter_erp_test` | 17.0.0-dev | Not installed | Yes |
| `~/frappe-bench` | 16.31.0 | 16.32.3 (+ hrms, india_compliance, kaiten_erp) | Listed in apps.txt but **no app folder** |

**Conflict:** Installing ERPNext v16 on Frappe 17 is incompatible. ERPNext for Frappe 17 would need a matching develop/v17 track. Until ERPNext is installed on this bench, **all Link fields to Item, Customer, Lead, Supplier, Company, UOM, Employee, Brand, Warehouse, etc. are implemented as forward-compatible Data / deferred Links** and documented as **BLOCKED**.

## Existing furniture_erp DocTypes (keep / extend)

| DocType | Module | Decision |
|---------|--------|----------|
| Furniture ERP Settings | Setup | Extend with business settings (warehouses as Data until ERPNext) |
| Furniture Product Family | Furniture Catalogue | Keep as catalogue family; **not** a substitute for Category/Model. Map later. |
| Furniture Material | Furniture Catalogue | **Enhance** to Master Prompt §4.5 fields |
| Furniture Finish | Furniture Catalogue | **Enhance** to Master Prompt §4.6 fields |
| Furniture Specification | Furniture Catalogue | Keep; relate to Design/Model later |
| Family Allowed Material/Finish (child) | Furniture Catalogue | Keep |
| Specification Attribute (child) | Furniture Catalogue | Keep |

## Required vs status (high level)

| Area | Status |
|------|--------|
| Phase 2 Masters (Category, Model, Variant, Design, Color, Config) | **Implementing now** |
| Enhance Material / Finish | **Implementing now** |
| Lead/Opportunity/Quotation/SO custom fields | **BLOCKED** (needs ERPNext) |
| Customer Requirement, Job File | Implement structure; ERPNext links as Data until DEC-002 |
| Purchase / Stock / WO / QC / Delivery / Payment / Warranty | Pending phases 7–12; ERPNext required |
| Reports / Workspace | Partial workspace for masters now |
| Workflows / Notifications | After DocTypes stable + ERPNext |

## Standard vs Custom (short)

- Reuse ERPNext: Lead, Opportunity, Customer, Item, Quotation, SO, PO, PR, BOM, WO, Job Card, QI, DN, SI, PE — **when ERPNext installed**.
- Custom in `furniture_erp`: all Furniture* masters, Job File, Requirement, Survey, Design Approval, Dispatch Plan, Installation, Payment Milestone, Warranty, Service*, AMC, etc.

## Roadmap this branch

1. Audit (this file) — done  
2. Phase 2 masters + Material/Finish enhance + Color  
3. Furniture Customer Requirement + Furniture Job File (core fields)  
4. Furniture Business Settings fields on Settings  
5. Roles refresh + Workspace shortcuts for masters  
6. Migrate + unit tests for masters  
7. Later PRs: ERPNext install gate, then CRM custom fields through Service  

## Checklist

- [x] Audit  
- [x] Deferred Link register (`phase2-field-map.md`, DEC-009–011)  
- [x] Phase 2 masters  
- [x] Requirement + Job File  
- [x] Settings / roles / workspace  
- [x] Migrate / tests (8/8 OK on `carpenter`)  
- [x] Push branch / PR → `dev` (https://github.com/Abhishek-kaiten/furniture_erp/pull/2)  

## Status legend (this PR)

| Status | Meaning |
|--------|---------|
| Completed | Implemented and migrated on `carpenter` |
| In Progress | Current branch work |
| Pending | Later PR on carpenter after this one |
| Blocked | Needs ERPNext (DEC-002) |
