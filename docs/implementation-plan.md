# Implementation Plan — Milestones 0–9

Each milestone has **entry criteria**, **deliverables**, and **acceptance gate**. ERPNext-dependent work is gated at **M0.5**.

## Overview

| MS | Name | ERPNext? |
|----|------|----------|
| M0 | Discovery & architecture | No |
| M0.5 | ERPNext platform install | Yes |
| M1 | Catalogue masters (Material, Finish, Family, Settings) | Links optional |
| M2 | Specification & reports | Optional Item link |
| M3 | Company, COA, tax, items bootstrap | Yes |
| M4 | Quotation + spec integration | Yes |
| M5 | BOM, WO, procurement | Yes |
| M6 | Delivery & installation | Yes |
| M7 | Dashboards & AR workflows | Yes |
| M8 | Integrations phase 1 | Partial |
| M9 | Portal / polish / UAT exit | Optional |

---

### M0 — Discovery & architecture

**Entry:** Bench and app installable.  
**Deliverables:** This `docs/` pack, assumptions register, traceability CSV.  
**Acceptance gate:**

- [ ] Stakeholder ack: BRD missing, Master Prompt baseline, India GST assumption.  
- [ ] Decision log entry DEC-001 recorded.  
- [ ] Branch `feature/m0-m1-foundation-catalogue` contains docs.

---

### M0.5 — ERPNext platform install

**Entry:** M0 gate passed; DEC-002 approved.  
**Deliverables:** ERPNext on `carpenter` + `test_carpenter`; `required_apps = ["erpnext"]`; site company skeleton.  
**Acceptance gate:**

- [ ] `bench --site carpenter list-apps` shows erpnext.  
- [ ] Create test Customer, Item, Warehouse in UI.  
- [ ] Patch `sites/apps.json` branch alignment documented.

---

### M1 — Catalogue masters

**Entry:** M0.5 recommended (Item Group links); minimum Frappe-only possible.  
**Deliverables:** DocTypes: Settings, Product Family, Material, Finish + child allowlist tables; roles; basic list views.  
**Acceptance gate:**

- [ ] All TC-CAT-01..03 pass.  
- [ ] Fixtures for sample catalogue load without error.  
- [ ] Migrations via patches for re-run install.

---

### M2 — Specification

**Entry:** M1 complete.  
**Deliverables:** Furniture Specification + attributes; workflow; Specification Register report; print format draft.  
**Acceptance gate:**

- [ ] TC-CAT-04, TC-CAT-05 pass.  
- [ ] Approve/Reject workflow per matrix.  
- [ ] KPI: catalogue coverage report runs.

---

### M3 — Financial & item bootstrap

**Entry:** M0.5; M2 specs exist.  
**Deliverables:** COA, warehouses, GST settings (India), Item linkage from materials/finishes; pricing list skeleton.  
**Acceptance gate:**

- [ ] TC-INT-01 pass.  
- [ ] Trial Sales Invoice with tax lines (no submit or test submit in sandbox).  
- [ ] Furniture ERP Settings company defaults populated.

---

### M4 — Quotation integration

**Entry:** M3.  
**Deliverables:** Custom fields on Quotation Item; validation WF-01; pricing hooks (baseline).  
**Acceptance gate:**

- [ ] TC-INT-02 pass.  
- [ ] Cannot submit SO without approved spec (if spec linked).  
- [ ] Sales role permissions verified.

---

### M5 — Manufacturing & procurement

**Entry:** M4.  
**Deliverables:** BOM templates, WO from SO, MR→PO flow; material issue.  
**Acceptance gate:**

- [ ] TC-INT-03 pass.  
- [ ] BOM references specification ID (custom field).  
- [ ] WIP warehouse balances correct on test WO.

---

### M6 — Delivery & installation

**Entry:** M5.  
**Deliverables:** Installation Job DocType; DN/SI linkage; OTIF report prototype.  
**Acceptance gate:**

- [ ] Installation complete closes loop on test SO.  
- [ ] Customer-facing DN print with line specs.

---

### M7 — Management reporting

**Entry:** M6.  
**Deliverables:** Workspaces, executive dashboard, AR ageing use.  
**Acceptance gate:**

- [ ] Dashboard charts render with 30 days test data.  
- [ ] Role-based workspace visibility.

---

### M8 — Integrations phase 1

**Entry:** M7.  
**Deliverables:** Integration Log, INT-08 webhook, GST live API in UAT (if applicable).  
**Acceptance gate:**

- [ ] Failed webhook retry tested.  
- [ ] No secrets in repository scan.

---

### M9 — Portal & UAT exit

**Entry:** M8 or defer integrations.  
**Deliverables:** Optional website catalogue; UAT sign-off script; training docs.  
**Acceptance gate:**

- [ ] UAT checklist 100% P0 scenarios.  
- [ ] Production cut checklist (backup, roles, series).  
- [ ] Tag release `v1.0.0-rc1` or agreed version.

---

## Branching strategy

| Branch | Use |
|--------|-----|
| `feature/m0-m1-foundation-catalogue` | Current catalogue foundation |
| `dev` | Integration branch |
| `develop` | CI default per README |
| `main` | Release |

## Risk buffers

- Add **1 sprint** after M0.5 for ERPNext version friction on Frappe 17.  
- BRD arrival may replan M4+ scope — update traceability CSV.