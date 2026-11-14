# Role & Permission Matrix

Roles are **planned** unless noted. Frappe **System Manager** retains full access. Matrix assumes ERPNext roles are imported/merged after install.

## Custom roles (furniture_erp)

| Role | Purpose |
|------|---------|
| Furniture Admin | Settings, role setup, integration |
| Catalogue Manager | Families, materials, finishes, approve specs |
| Furniture Designer | Create/edit specs, families (draft) |
| Sales User | Quotations, customers (ERPNext) |
| Sales Manager | Approve quotations, discount limits |
| Purchase User | MR, PO (ERPNext) |
| Purchase Manager | Approve PO |
| Production Planner | BOM, WO, production plan |
| Shop Floor User | Job Card time & qty |
| Stock User | Stock entries, pick lists |
| Accounts User | Invoices, payments, GST |
| Installation Coordinator | Installation jobs (M6) |

## DocType permissions — custom (M1–M2)

Legend: **R** read, **W** write/create, **S** submit/cancel, **A** amend, **—** none.

| DocType | Furniture Admin | Catalogue Manager | Designer | Sales User | System Manager |
|---------|-----------------|-------------------|----------|------------|----------------|
| Furniture ERP Settings | RW | R | R | — | RW |
| Furniture Product Family | RW | RW | RW | R | RW |
| Furniture Material | RW | RW | R | R | RW |
| Furniture Finish | RW | RW | R | R | RW |
| Furniture Specification | RW | RWA | RWA | R | RW |
| Child tables (all above) | via parent | via parent | via parent | R | RW |

## ERPNext DocTypes (target — blocked)

| DocType | Sales User | Sales Mgr | Purchase User | Stock User | Accounts | Production |
|---------|------------|-----------|---------------|------------|----------|------------|
| Customer | RW | RW | R | R | R | R |
| Item | R | R | R | RW | R | RW |
| Quotation | RW | RWS | — | — | — | R |
| Sales Order | RW | RWS | — | R | R | R |
| BOM | R | R | R | R | R | RW |
| Work Order | R | R | — | R | — | RWS |
| Material Request | — | — | RW | R | — | RW |
| Purchase Order | — | — | RWS | R | R | — |
| Delivery Note | RW | RWS | — | RWS | R | — |
| Sales Invoice | R | RW | — | — | RWS | — |
| Payment Entry | — | — | — | — | RWS | — |

Use ERPNext **Role Profile** templates as starting point, then add custom role permissions for `furniture_erp` DocTypes.

## User permissions (data scope)

| Scenario | Mechanism |
|----------|-----------|
| Sales rep sees own customers | User Permission on Customer |
| Project team | User Permission on Project |
| Warehouse picker | User Permission on Warehouse |

## API / desk

| Rule | Detail |
|------|--------|
| Whitelisted methods | `require_type_annotated_api_methods = True` in hooks — all new APIs must be typed. |
| Guest access | No catalogue write; public read only if portal enabled (deferred). |

## SoD (segregation of duties)

| Conflict | Mitigation |
|----------|------------|
| Create PO + approve PO | Separate Purchase User vs Purchase Manager |
| Create SI + post payment | Accounts Manager approval over threshold |
| Approve own specification | Designer cannot Approve; Catalogue Manager only |