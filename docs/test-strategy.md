# Test Strategy

## Objectives

- Verify catalogue masters and validation rules without ERPNext (M1–M2).  
- After ERPNext install, run **integrated** quote-to-stock scenarios on `test_carpenter`.  
- Keep CI fast with unit tests; reserve E2E for milestone gates.

## Test environments

| Environment | Bench | Site | Apps |
|-------------|-------|------|------|
| Local dev | carpenter_erp | carpenter | frappe, furniture_erp |
| CI | GitHub Actions | ephemeral | per `.github/workflows/ci.yml` |
| UAT | carpenter_erp_test | test_carpenter | + erpnext when installed |

## Levels

| Level | Scope | Tools |
|-------|--------|-------|
| Unit | Python validators, naming, allowlist logic | `bench run-tests --app furniture_erp` |
| API | Whitelisted methods | Frappe test client |
| UI | Critical forms (optional) | Playwright / manual checklist |
| Integration | Spec → Item → SO → WO | Manual + data fixtures |
| Regression | Milestone gate suite | Tagged tests `@milestone_m2` etc. |

## CI (current app repo)

- **CI workflow:** installs app, runs unit tests on push to `develop`.  
- **Linters:** Semgrep, pip-audit on PR.  
- **Gap:** CI does not yet install ERPNext; integration tests marked `skip` until DEC-002.

## Test data

| Fixture | Content |
|---------|---------|
| `catalogue_materials.json` | Sample plywood, laminate |
| `catalogue_family.json` | Dining table family with allowlists |
| `spec_draft.json` | Draft specification |
| ERPNext masters | Company, warehouses, COA — post M0.5 |

Use Frappe `export_fixtures` / data import; no production PII.

## M1–M2 test cases (catalogue)

| ID | Case | Expected |
|----|------|----------|
| TC-CAT-01 | Create Material with required fields | Saved, named series applied |
| TC-CAT-02 | Family allowlist enforce ON, invalid material on spec | ValidationError |
| TC-CAT-03 | Two defaults in allowlist table | ValidationError |
| TC-CAT-04 | Spec workflow Approve without dimensions | Blocked |
| TC-CAT-05 | Settings singleton | Only one record |

## Post–ERPNext scenarios (gated)

| ID | Scenario |
|----|----------|
| TC-INT-01 | Create Item linked from Material |
| TC-INT-02 | Quotation with linked Approved Spec |
| TC-INT-03 | SO → WO → Manufacture → FG stock |
| TC-INT-04 | Sales Invoice GST totals smoke test |

## Non-functional

| Area | Target |
|------|--------|
| Permission | Designer cannot Approve spec |
| Performance | List view < 2s for 10k materials (indexes on status, family) |
| Security | No unauthenticated write APIs |

## Defect severity

| Sev | Definition |
|-----|------------|
| S1 | Data corruption, wrong GL/stock |
| S2 | Blocked workflow, no workaround |
| S3 | Minor UX, workaround exists |

## Sign-off

Each milestone in [implementation-plan.md](./implementation-plan.md) lists **acceptance tests** that must pass before promote to `dev` / release branch.