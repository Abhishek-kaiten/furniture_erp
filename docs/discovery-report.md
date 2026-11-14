# Furniture ERP — Milestone 0 Discovery Report

**Date:** 2025-11-14 (discovery)  
**App:** Furniture ERP (`furniture_erp` v0.0.1)  
**Baseline:** Master Build Prompt v1.0 (no separate BRD on file — see [assumptions-decisions-register.md](./assumptions-decisions-register.md))

## Executive summary

Milestone 0 confirms a working Frappe bench and an installable custom app shell. Business logic, catalogue DocTypes, and ERP transactional flows are **not implemented**. ERPNext is **not installed**, which blocks reuse of standard Customer, Item, BOM, Sales Order, Purchase Order, stock, and accounting flows until a deliberate install and configuration milestone is executed.

## Environment

| Item | Value |
|------|--------|
| Bench root | `/home/abhishek-jangir/carpenter_erp` |
| Primary site | `carpenter` |
| Test bench / site | `carpenter_erp_test` / `test_carpenter` (referenced; not validated in this pass) |
| Python (app) | `>=3.14` per `pyproject.toml` |

## Installed applications (site `carpenter`)

| App | Version | Notes |
|-----|---------|--------|
| frappe | 17.0.0-dev | Platform only |
| furniture_erp | 0.0.1 | Scaffold; commit `fc37b56` in `sites/apps.json` resolution |
| **erpnext** | — | **Not installed** |

Source: `sites/apps.json`, `sites/apps.txt`.

## Git state (`apps/furniture_erp`)

| Item | Value |
|------|--------|
| Remote | `https://github.com/Abhishek-kaiten/furniture_erp.git` |
| Current branch | `feature/m0-m1-foundation-catalogue` (branched from `dev`) |
| Other local branches | `main`, `develop`, `dev` |
| Recent commits | `fc37b56` rename app from carpenter_erp to furniture_erp; `1e1f1c5` Initialize App |

## Application artefact inventory

| Path | Purpose |
|------|---------|
| `furniture_erp/hooks.py` | Default Frappe hooks; `export_python_type_annotations`, `require_type_annotated_api_methods` enabled |
| `furniture_erp/modules.txt` | Single module: `Furniture_erp` |
| `furniture_erp/patches.txt` | Empty |
| `furniture_erp/__init__.py` | Version `0.0.1` |
| `.github/workflows/` | CI + linter workflows (template) |

**No custom DocTypes, workspaces, reports, or client scripts exist in the repository.**

## Reusable functionality today

| Capability | Available? | Notes |
|------------|------------|--------|
| User / Role / Permission (Frappe core) | Yes | Standard site setup |
| File attachments, Comments, Assignments | Yes | Frappe document model |
| Workspaces, Desk, Notifications | Yes | Unconfigured for Furniture ERP |
| Customer, Item, BOM, SO, PO, Stock, GL | **No** | Requires ERPNext install |
| India GST (GST Settings, e-invoice hooks) | **No** | ERPNext + India Compliance stack not present |
| Custom catalogue (Product Family, Material, Finish, Spec) | **No** | Planned M1–M2 |

## Discovery deliverables

All Milestone 0 documentation lives under `apps/furniture_erp/docs/`:

1. architecture.md  
2. doctype-catalog.md  
3. doctype-field-specifications.md  
4. process-flows.md  
5. workflow-matrix.md  
6. role-permission-matrix.md  
7. accounting-stock-design.md  
8. integration-register.md  
9. reports-and-dashboards.md  
10. test-strategy.md  
11. assumptions-decisions-register.md  
12. implementation-plan.md  
13. requirements-traceability.csv  
14. standard-vs-custom-doctype-matrix.md  
15. discovery-report.md (this file)

## Top blockers (summary)

1. **ERPNext not installed** — cannot implement or test standard master/transaction DocTypes.  
2. **BRD missing** — scope traced to Master Build Prompt v1.0 only; business sign-off pending.  
3. **No custom DocTypes** — M1 catalogue work not started in code.  
4. **GST jurisdiction** — assumed India; legal/tax confirmation required.  
5. **Branch vs bench resolution** — `sites/apps.json` references branch `develop` at `fc37b56` while active dev branch is `feature/m0-m1-foundation-catalogue`; align before production cut.

## Recommended next gate (M0 → M1)

- Decision record: install ERPNext (version line compatible with Frappe 17) on `carpenter` and `test_carpenter`.  
- Import/sync Master Build Prompt or BRD for formal requirement IDs.  
- Implement M1 DocTypes per [doctype-field-specifications.md](./doctype-field-specifications.md) with unit tests.