# Standard vs Custom DocType Matrix

**Rule:** Use ERPNext standard DocTypes wherever possible. Custom DocTypes only for furniture catalogue and processes without a standard fit.

**ERPNext status:** Not installed — standard column is **planned reuse**.

## Masters & catalogue

| Business concept | Preferred DocType | Source | Custom? | Notes |
|------------------|-------------------|--------|---------|-------|
| Product family taxonomy | Furniture Product Family | furniture_erp | Yes | ERPNext Item Group is complementary, not replacement |
| Material library | Furniture Material | furniture_erp | Yes | Links to ERPNext Item for stock |
| Finish library | Furniture Finish | furniture_erp | Yes | Links to Item if consumable stocked |
| Configured specification | Furniture Specification | furniture_erp | Yes | |
| Sellable SKU | Item | ERPNext | No | Created from spec/material |
| Customer | Customer | ERPNext | No | Blocked |
| Supplier | Supplier | ERPNext | No | Blocked |
| Warehouse | Warehouse | ERPNext | No | Blocked |
| UOM | UOM | ERPNext | No | Blocked |
| Price list | Price List | ERPNext | No | Blocked |

## Selling

| Business concept | Preferred DocType | Custom? | Extension |
|------------------|-------------------|---------|-----------|
| Lead / opportunity | Lead, Opportunity | No | — |
| Quotation | Quotation | No | Custom fields: furniture_specification |
| Sales order | Sales Order | No | Link spec; validation WF-01 |
| Delivery | Delivery Note | No | — |
| Sales invoice | Sales Invoice | No | GST standard |
| Installation visit | Furniture Installation Job | Yes | M6 |

## Manufacturing

| Business concept | Preferred DocType | Custom? | Extension |
|------------------|-------------------|---------|-----------|
| Bill of materials | BOM | No | Custom field: furniture_specification |
| Work order | Work Order | No | — |
| Job card | Job Card | No | — |
| Routing / operation | Routing, Operation | No | Optional |
| Site measurement | Furniture Site Measurement | Yes | M5 optional |

## Buying & stock

| Business concept | Preferred DocType | Custom? |
|------------------|-------------------|---------|
| Material request | Material Request | No |
| Purchase order | Purchase Order | No |
| Purchase receipt | Purchase Receipt | No |
| Stock entry | Stock Entry | No |
| Pick list | Pick List | No |
| Stock reconciliation | Stock Reconciliation | No |

## Accounts

| Business concept | Preferred DocType | Custom? |
|------------------|-------------------|---------|
| Payment | Payment Entry | No |
| Journal entry | Journal Entry | No |
| GST settings | GST Settings / company tax | No |
| Cost center | Cost Center | No |

## Settings & platform

| Business concept | Preferred DocType | Custom? |
|------------------|-------------------|---------|
| App defaults | Furniture ERP Settings | Yes |
| Workflow | Workflow | No (config) |
| Integration audit | Furniture Integration Log | Yes |
| User / role | User, Role | No |

## Custom field strategy (ERPNext — post install)

| Host DocType | Planned fields |
|--------------|----------------|
| Item | furniture_material, furniture_finish, furniture_family |
| Quotation Item | furniture_specification |
| Sales Order Item | furniture_specification |
| BOM | furniture_specification |

## Anti-patterns (do not build)

| Avoid | Reason |
|-------|--------|
| Custom Customer table | Use ERPNext CRM |
| Custom stock ledger | INV-C-01 |
| Custom PO/SO | No ERPNext benefit |
| Duplicate material master without Item link | Stock sync failure |