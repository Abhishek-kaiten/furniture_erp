# Process Flows

End-to-end processes for Furniture ERP. **Standard ERPNext steps are dashed until ERPNext is installed.**

## 1. Catalogue maintenance (M1–M2 — no ERPNext dependency)

```mermaid
flowchart LR
  A[Define Materials & Finishes] --> B[Define Product Family]
  B --> C[Allowlist Materials/Finishes]
  C --> D[Create Furniture Specification]
  D --> E{Approved?}
  E -->|Yes| F[Ready for Item/BOM linkage]
  E -->|No| D
```

**Actors:** Catalogue Manager, Designer.  
**Output:** Approved `Furniture Specification` linked to family and materials.

## 2. Lead to quotation (target — ERPNext blocked)

```mermaid
flowchart TD
  L[Lead / Opportunity] --> Q[Quotation]
  Q --> S[Select Product Family]
  S --> C[Load / Clone Specification]
  C --> P[Pricing Rule / Rate]
  P --> Q
  Q --> AP{Approval}
  AP -->|Approved| SO[Sales Order]
  AP -->|Revise| C
```

**Standard DocTypes:** Lead, Opportunity, Quotation, Sales Order. **Status:** Blocked.

## 3. Sales order to production (target)

```mermaid
flowchart TD
  SO[Sales Order] --> PP[Production Plan optional]
  PP --> WO[Work Order]
  WO --> JC[Job Cards]
  JC --> SE[Stock Entry Manufacture]
  SE --> FG[Finished Goods Warehouse]
```

**Depends on:** Item, BOM, Work Order. **Status:** Blocked.

## 4. Procurement for materials

```mermaid
flowchart LR
  MR[Material Request] --> PO[Purchase Order]
  PO --> PR[Purchase Receipt]
  PR --> SL[Stock Ledger]
  PO --> PI[Purchase Invoice]
  PI --> GL[GL Entry]
```

**Status:** Blocked.

## 5. Delivery and installation

```mermaid
flowchart LR
  SO --> DN[Delivery Note]
  DN --> SI[Sales Invoice]
  SO --> IJ[Furniture Installation Job - custom M6]
  IJ --> DN
```

Installation DocType is **planned**; DN/SI are ERPNext.

## 6. Specification revision

1. Designer sets spec to **In Review**.  
2. Engineering validates dimensions vs family rules.  
3. Manager approves → status **Approved**; prior version **Obsolete** on amend.  
4. Linked Quotation/SO (future) flagged for re-pricing if spec changes.

See [workflow-matrix.md](./workflow-matrix.md).

## 7. GST billing (India — assumed)

1. Sales Invoice with HSN from Item / Material master.  
2. Tax templates per place of supply.  
3. e-Invoice / e-Way per compliance app (**TBD** at ERPNext install).

## Process ↔ milestone map

| Process | First milestone |
|---------|-----------------|
| Catalogue maintenance | M1–M2 |
| ERPNext company & masters | M0.5 |
| Quotation with spec | M4 |
| BOM / WO | M5 |
| Procurement | M5 |
| Installation | M6 |
| Management dashboards | M7–M8 |