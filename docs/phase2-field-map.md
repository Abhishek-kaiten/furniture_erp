# Phase 2 Field Map — ERPNext Data vs Link

**Bench:** `~/carpenter_erp` · **Sites:** `carpenter`, `test_carpenter`  
**Status after Phase 3 (DEC-002):** CRM/catalogue deferred fields converted to **Link** where the target DocType exists.

Conversion patch: `furniture_erp.patches.v1_0.convert_erpnext_data_to_link`

| DocType | Prompt Link target | Field | Status |
|---------|-------------------|-------|--------|
| Furniture Model | Brand | `brand` | **Link → Brand** |
| Furniture Model | Item | `item_code` | **Link → Item** |
| Furniture Variant | Item | `item_code` | **Link → Item** |
| Furniture Material | Item | `linked_item_code` / `item_code` | **Link → Item** |
| Furniture Material | Supplier | `supplier` | **Link → Supplier** |
| Furniture Material | UOM | `uom` | **Link → UOM** |
| Furniture Customer Requirement | Customer | `customer` | **Link → Customer** |
| Furniture Customer Requirement | Lead | `lead` | **Link → Lead** |
| Furniture Customer Requirement | Opportunity | `opportunity` | **Link → Opportunity** |
| Furniture Job File | Customer / Contact / Company / Project / Employee / Lead / Opportunity / Quotation / Sales Order / Sales Person / Address / Production Plan | respective fields | **Link** (see DocType JSON) |
| Furniture Job File | Branch | `branch` | Still **Data** (no standard Branch DocType) |
| Furniture Job File | Site Survey | `site_survey` | Still **Data** until Phase 4 DocType |
| Furniture ERP Settings | Warehouse | `*_warehouse` | **Link → Warehouse** |

Furniture-to-furniture Links (Category, Model, Variant, Material, Finish, Color, Job File) remain real **Link** fields.
