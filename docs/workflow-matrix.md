# Workflow Matrix

Workflows use Frappe **Workflow** on DocTypes with `docstatus` where applicable. ERPNext transactional workflows are **configured after install**.

## Custom DocTypes (furniture_erp)

### Furniture Specification

| State | Docstatus | Allowed edits | Next states |
|-------|-----------|---------------|-------------|
| Draft | 0 | Designer, Catalogue Manager | In Review, Cancelled |
| In Review | 0 | Catalogue Manager (fields locked for Designer) | Approved, Rejected, Draft |
| Approved | 0 | System / Manager only via Amend | Obsolete |
| Rejected | 0 | Designer | Draft |
| Obsolete | 0 | None (read-only) | — |

**Workflow actions**

| Action | From | To | Role |
|--------|------|-----|------|
| Submit for Review | Draft | In Review | Designer |
| Approve | In Review | Approved | Catalogue Manager |
| Reject | In Review | Rejected | Catalogue Manager |
| Recall | In Review | Draft | Designer |
| Amend | Approved | Draft (new version) | Catalogue Manager |

**Email alerts:** Notify Catalogue Manager on Submit for Review; notify Designer on Reject/Approve.

### Furniture Product Family / Material / Finish

| State | Notes |
|-------|--------|
| Active / Inactive / Discontinued | Simple `status` field; no multi-step workflow in M1. |
| Future | Optional approval before **Discontinued** if linked to open specs. |

### Furniture ERP Settings

| Rule | Detail |
|------|--------|
| Single document | No workflow; change only by System Manager / Furniture Admin. |

## ERPNext DocTypes (planned configuration)

| DocType | Typical workflow | Milestone |
|---------|------------------|-----------|
| Quotation | Draft → Submitted → (Lost/Ordered) | M4 |
| Sales Order | Standard submit / close | M4 |
| Material Request | Draft → Submitted → Ordered | M5 |
| Purchase Order | Draft → Submitted | M5 |
| Work Order | Not Started → In Process → Completed | M5 |
| Sales Invoice | Draft → Submitted | M3+ |
| Payment Entry | Draft → Submitted | M3+ |

**Note:** ERPNext may use role permissions without custom Workflow for some DocTypes; align with company policy at DEC-002.

## Cross-workflow rules

| Rule ID | Description |
|---------|-------------|
| WF-01 | Cannot submit SO if linked Specification is not **Approved** (custom validation M4). |
| WF-02 | Cannot cancel approved Spec if referenced by submitted SO (block or force unlink policy — OQ). |
| WF-03 | PO over certain value requires **Purchase Manager** workflow action (ERPNext). |

## Delegation & alternate approvers

Use Frappe **Assignment Rule** and **User Permission** for project-scoped customers (ERPNext). Configure in M3 after masters exist.