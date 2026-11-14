# Milestone Status — feature/m0-m1-foundation-catalogue

**Date:** 2026-11-14  
**Branch:** `feature/m0-m1-foundation-catalogue` (from `dev`)  
**App:** `furniture_erp` on Frappe 17.0.0-dev  

## Detected environment

| Item | Value |
|------|-------|
| Installed apps | frappe, furniture_erp |
| ERPNext | **Not installed** (blocker for Item/Customer/SO/BOM/stock/GST) |
| BRD file | Not supplied — Master Build Prompt v1.0 used as baseline |
| Sites | `carpenter`, `test_carpenter` |

## Completed in this branch

### Milestone 0 — Discovery
- [x] `docs/` architecture, catalogues, matrices, plans, traceability CSV, discovery report

### Milestone 1 — App foundation
- [x] App title **Furniture ERP**, module layout (10 modules)
- [x] `Furniture ERP Settings` (Single)
- [x] Custom furniture roles via `after_install` / `after_migrate`
- [x] Install hooks, tests scaffold

### Milestone 2 — Catalogue (partial)
- [x] Furniture Product Family (+ allowed material/finish children)
- [x] Furniture Material
- [x] Furniture Finish
- [x] Furniture Specification (+ attributes child)
- [x] Server validations: allowlists, positive dimensions, approval readiness
- [x] Unit tests for specification validations

## Explicitly deferred / blocked

- All ERPNext Link fields (Company, Item, Warehouse, Customer, Supplier, BOM, UOM as Link)
- CRM → quote → order → manufacture → delivery → warranty flows
- Portals, reports dashboards, GST e-invoice
- Installing ERPNext (requires explicit approval — infrastructure change)

## Next safe commands

```bash
cd ~/carpenter_erp
bench --site carpenter migrate
bench --site carpenter run-tests --app furniture_erp
# then PR into dev
```
