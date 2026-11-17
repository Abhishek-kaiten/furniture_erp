# Phase 2 Field Map — ERPNext Data vs Future Link

**Bench:** `~/carpenter_erp` · **Site:** `carpenter` · **Branch:** `feature/master-furniture-erp-phases`

Until ERPNext is installed (DEC-002), fields that the Master Prompt specifies as Links to ERPNext DocTypes are stored as **Data** with suffix/description `(ERPNext)`. After ERPNext install, a patch will convert them to Link fields.

| DocType | Prompt Link target | Current field | Future |
|---------|-------------------|---------------|--------|
| Furniture Model | Brand | `brand` (Data) | Link → Brand |
| Furniture Model | Item | `item_code` (Data) | Link → Item |
| Furniture Variant | Item | `item_code` (Data) | Link → Item |
| Furniture Material | Item | `linked_item_code` / `item_code` (Data) | Link → Item |
| Furniture Material | Supplier | `supplier` (Data) | Link → Supplier |
| Furniture Material | UOM | `uom` (Select) | Link → UOM |
| Furniture Customer Requirement | Customer | `customer` (Data) | Link → Customer |
| Furniture Customer Requirement | Lead | `lead` (Data) | Link → Lead |
| Furniture Customer Requirement | Opportunity | `opportunity` (Data) | Link → Opportunity |
| Furniture Job File | Customer / Company / Branch / Project / Employee / Contact / Address / Quotation / SO / etc. | Data fields | Link → standard DocTypes |
| Furniture ERP Settings | Warehouse | `*_warehouse` (Data) | Link → Warehouse |

Furniture-to-furniture Links (Category, Model, Variant, Material, Finish, Color, Job File) are real **Link** fields.
