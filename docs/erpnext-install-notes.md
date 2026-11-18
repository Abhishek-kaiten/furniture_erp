# ERPNext Install Notes (DEC-002)

**Date:** 2026-11-18  
**Benches:** `~/carpenter_erp` (site `carpenter`, port 8001), `~/carpenter_erp_test` (site `test_carpenter`, port 8002)  
**ERPNext branch:** `develop` (compatible with Frappe 17.0.0-dev)

## Commands used

```bash
# Development bench
cd ~/carpenter_erp
bench get-app erpnext --branch develop
# Rename furniture_erp modules that clash with ERPNext (Setup, Manufacturing)
# before install-app — see below
bench --site carpenter install-app erpnext

# Test bench
cd ~/carpenter_erp_test
bench get-app erpnext --branch develop
# same module rename on site DB
bench --site test_carpenter install-app erpnext
```

## Module name conflict

`furniture_erp` originally shipped modules named **Setup** and **Manufacturing**, which collide with ERPNext Module Defs.

**Resolution (Phase 3):**
- Renamed to **Furniture Setup** and **Furniture Manufacturing**
- Folders: `furniture_setup/`, `furniture_manufacturing/`
- Updated `modules.txt` and DocType/Workspace `module` fields

Do **not** reintroduce a module literally named `Setup` or `Manufacturing` in `furniture_erp`.

## App dependency

`furniture_erp/hooks.py` now sets:

```python
required_apps = ["erpnext"]
```

## Deferred

- **india_compliance** / GST packaging: still DEC-008 (not installed)
- kaiten / other apps: not installed
- Company / chart of accounts: create via ERPNext Setup Wizard or for tests via `_Test Furniture Co`

## Verify

```bash
bench --site carpenter list-apps
# expect: frappe, furniture_erp, erpnext
```
