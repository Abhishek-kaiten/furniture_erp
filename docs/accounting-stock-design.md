# Accounting & Stock Design

Design for inventory valuation and accounting **after ERPNext installation**. Current site has **no** stock ledger or chart of accounts.

## Company & books

| Element | Design |
|---------|--------|
| Company | Single primary company on `carpenter` (confirm name in DEC-002 setup). |
| Currency | INR (assumed). |
| Fiscal year | April–March (India default). |
| Cost centers | Factory, Showroom, Projects, Admin (ERPNext Cost Center). |

## Chart of accounts (outline)

Standard ERPNext COA template for **manufacturing** (customise with auditor):

| Group | Examples |
|-------|----------|
| Assets | Stock, WIP, FG, Debtors, GST Input |
| Liabilities | Creditors, GST Output, TDS payable |
| Income | Furniture sales, Installation service, Freight |
| Expenses | Raw material consumed, Labour, Depreciation, Rent |

**Furniture-specific:** map **Installation** and **Design fees** as service Items with distinct income accounts.

## Stock settings

| Setting | Value / note |
|---------|----------------|
| Valuation method | FIFO (default) unless auditor requires moving average. |
| Negative stock | Disallowed for RM and FG. |
| Batch / serial | Optional for lot-tracked boards; enable per Item if needed. |
| UOM conversion | Sheet → Sq M for plywood via UOM Conversion Factor on Item. |

## Warehouse structure

| Warehouse | Purpose |
|-----------|---------|
| Raw Material - Stores | Boards, hardware receipts |
| WIP - Factory | Issued material on open WO |
| Finished Goods - FG | Completed furniture |
| Transit - Site | DN not yet installed (optional) |
| Scrap | Offcuts (M5+) |

Align defaults with **Furniture ERP Settings** fields `default_warehouse_*`.

## Item model (ERPNext)

| Item type | Example | Stock? |
|-----------|---------|--------|
| Raw material | 18mm BWP Ply | Yes |
| Consumable | Edge band, glue | Yes |
| Sub-assembly | Carcass panel set | Yes (optional) |
| Finished good | Wardrobe SKU | Yes |
| Service | Installation, delivery | No |

**Link:** `Furniture Material.linked_item`, `Furniture Finish.linked_item`, spec `target_item` for FG.

## BOM & WIP accounting

1. **Material Issue** (Stock Entry or backflush from Job Card) → Dr WIP, Cr RM.  
2. **Manufacture** Stock Entry → Dr FG, Cr WIP (+ labour/overhead via additional costs if used).  
3. **Delivery Note** → stock out of FG; COGS on invoice per ERPNext settings.

Custom furniture: BOM may be **project-specific**; use BOM with `Furniture Specification` reference (custom field M5).

## Selling & tax (India GST — assumed)

| Topic | Design |
|-------|--------|
| HSN | From Item; fallback `default_gst_hsn_code` in settings |
| Tax category | Taxable / Nil-rated per item |
| Place of supply | From Customer address |
| Templates | GST templates on Sales Invoice (intra/inter state) |
| e-Invoice | Enable via India compliance when package selected (DEC-008) |

**Blocked until ERPNext + compliance installed.**

## Pricing

| Mechanism | Use |
|-----------|-----|
| Price List | Retail vs dealer |
| Pricing Rule | Volume, customer group |
| Custom | Spec attribute price drivers (M4+) — server-side calculation |

## Period close

Use ERPNext **Accounting Period** and freeze roles. Stock reconciliation monthly for RM stores.

## What we do not build custom

- Parallel stock tables in `furniture_erp`.  
- Custom GL posting outside ERPNext controllers (only extension via `doc_events` where documented).

## Dependencies

| Dependency | Status |
|------------|--------|
| ERPNext Accounts module | Blocked |
| ERPNext Stock module | Blocked |
| India GST configuration | Proposed ASM-004 |