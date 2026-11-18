# Integration Register

External systems and integration points. Priority: **P0** critical path, **P1** soon after go-live, **P2** deferred.

## Current state

Phase 3: ERPNext same-site integration via Custom Fields + `doc_events` on Quotation / Sales Order. No external webhooks yet.

## Register

| ID | System | Direction | Protocol | Trigger | Data | Priority | Milestone | Status |
|----|--------|-----------|----------|---------|------|----------|-----------|--------|
| INT-01 | ERPNext (same site) | Internal | Frappe ORM | Doc save/submit | Lead, Opportunity, Customer, Quotation, SO (+ Item later) | P0 | Phase 3 | **Active** (CRM/Sales); stock/BOM later phases |
| INT-02 | India GST / e-Invoice | Outbound | API (compliance app) | Sales Invoice submit | IRN, QR | P0 | M3 | Planned |
| INT-03 | Payment gateway (Razorpay / etc.) | Inbound | REST webhook | Payment | Payment Entry | P1 | M7 | Deferred |
| INT-04 | Logistics (Delhivery / etc.) | Outbound | REST | DN submit | AWB, tracking | P2 | M8 | Deferred |
| INT-05 | CAD / nesting (Opticut, etc.) | Outbound | File/API | WO release | Cut list | P2 | M8 | Deferred |
| INT-06 | WhatsApp / SMS notifications | Outbound | Provider API | Workflow action | Template msg | P2 | M8 | Deferred |
| INT-07 | Website catalogue | Inbound | REST / guest | Public | Families, finishes | P2 | M9 | Deferred |
| INT-08 | Webhook (generic) | Outbound | HTTPS POST | Configurable | JSON payload | P1 | M3 | Planned |

## INT-08 — Furniture Integration Log (planned DocType)

| Field | Purpose |
|-------|---------|
| integration_id | e.g. INT-08 |
| reference_doctype / reference_name | Source document |
| status | Queued, Success, Failed |
| request_body / response_body | JSON (truncate large) |
| idempotency_key | Dedup |

## Security

| Control | Detail |
|---------|--------|
| Secrets | Site config / env, not in git |
| Webhook signing | HMAC header validation |
| Retry | Exponential backoff in background job |
| PII | Minimise customer phone in logs |

## ERPNext coupling patterns

| Pattern | When |
|---------|------|
| Custom field + `doc_events` | Link Spec → Quotation Item |
| `frappe.enqueue` | Async outbound calls |
| Data Import | One-time vendor/material load |

## Test environments

| Site | Use |
|------|-----|
| test_carpenter | Integration sandbox (mock endpoints) |
| carpenter | Production-like UAT |