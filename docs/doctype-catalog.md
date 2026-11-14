# DocType Catalogue

Planned and standard DocTypes for Furniture ERP. **Legend:**  
- **Implemented** — exists in repo/site today  
- **Planned** — specified for a milestone  
- **Standard (ERPNext)** — available only after ERPNext install  
- **Blocked** — depends on ERPNext or upstream decision

## furniture_erp custom DocTypes

### Milestone 1–2 (foundation catalogue)

| DocType | Type | Milestone | Status |
|---------|------|-----------|--------|
| Furniture ERP Settings | Single | M1 | Planned |
| Furniture Product Family | Setup | M1 | Planned |
| Furniture Material | Setup | M1 | Planned |
| Furniture Finish | Setup | M1 | Planned |
| Furniture Specification | Setup | M2 | Planned |
| Furniture Specification Attribute | Child Table | M2 | Planned |
| Furniture Family Allowed Material | Child Table | M1 | Planned |
| Furniture Family Allowed Finish | Child Table | M1 | Planned |
| Furniture Material Supplier Preference | Child Table | M2 | Planned |

### Later milestones (indicative)

| DocType | Type | Milestone | Status |
|---------|------|-----------|--------|
| Furniture Quote Configuration | Document | M4 | Planned |
| Furniture Work Package | Document | M5 | Planned |
| Furniture Site Measurement | Document | M5 | Planned |
| Furniture Installation Job | Document | M6 | Planned |
| Furniture Warranty Registration | Document | M7 | Planned |
| Furniture Integration Log | Log | M3 | Planned |

## Frappe core (available now)

| DocType | Use |
|---------|-----|
| User, Role, Role Profile | Access control |
| Company | Placeholder until ERPNext (Company exists in ERPNext; Frappe has limited org setup) |
| File, Comment, ToDo, Assignment Rule | Collaboration |
| Workflow, Workflow State, Workflow Action | Approval flows (configured per matrix) |

## ERPNext standard DocTypes (blocked — not installed)

### Masters

| DocType | Furniture use |
|---------|----------------|
| Customer, Customer Group, Territory | Clients, dealers, projects |
| Supplier, Supplier Group | Material vendors, hardware |
| Item, Item Group, UOM, Brand | SKUs, raw boards, hardware, services |
| Warehouse, Item Default | Factory, FG, transit |
| Price List, Pricing Rule | List and project pricing |
| BOM, Operation, Workstation, Routing | Manufacturing structure |
| Project, Task | Large fit-out jobs |

### Selling & fulfilment

| DocType | Furniture use |
|---------|----------------|
| Quotation, Sales Order, Delivery Note | Quote-to-deliver |
| Sales Invoice, Payment Entry | Billing and receipts |

### Buying & stock

| DocType | Furniture use |
|---------|----------------|
| Material Request, Purchase Order, Purchase Receipt | Procurement |
| Stock Entry, Pick List, Stock Reconciliation | Material issue, FG receipt |
| Serial and Batch Bundle | Lot tracking (if enabled) |

### Manufacturing

| DocType | Furniture use |
|---------|----------------|
| Work Order, Job Card | Shop orders |
| Production Plan | Capacity planning (optional) |

### Accounts (India)

| DocType | Furniture use |
|---------|----------------|
| Chart of Accounts, Cost Center | GL structure |
| GST Settings / Company tax | **After** India setup (package TBD) |

## Naming conventions

| Entity | Pattern | Example |
|--------|---------|---------|
| Product Family | `FPF-.#####` or title-based name | `FPF-DINING-01` |
| Material | `FMAT-.#####` | `FMAT-PLY-18MM` |
| Finish | `FFIN-.#####` | `FFIN-LAM-OAK` |
| Specification | `FSPEC-.YYYY.-.#####` | `FSPEC-2025-00042` |

Series defined in **Furniture ERP Settings** (planned).

## Module assignment

All custom DocTypes: **Furniture_erp** module (rename display to **Furniture ERP** in workspace).

## Related

- Field-level detail: [doctype-field-specifications.md](./doctype-field-specifications.md)  
- Standard vs custom: [standard-vs-custom-doctype-matrix.md](./standard-vs-custom-doctype-matrix.md)