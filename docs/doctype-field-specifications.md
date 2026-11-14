# DocType Field Specifications (M1–M2)

Field layouts use **three-column** form sections where noted. Types follow Frappe field types. ERPNext **Item** links are **blocked** until ERPNext install; fields are still specified for forward compatibility.

---

## Furniture ERP Settings

**Type:** Single | **Milestone:** M1 | **Naming:** N/A (singleton)

### Section: Defaults — column layout **3 columns**

| Fieldname | Label | Type | Options / Link | Req | Default | Description |
|-----------|-------|------|----------------|-----|---------|-------------|
| default_company | Default Company | Link | Company | | | Active company for catalogue defaults (ERPNext). |
| default_currency | Default Currency | Link | Currency | ✓ | INR | Pricing and cost display. |
| default_uom_length | Default Length UOM | Link | UOM | ✓ | Millimeter | Spec dimensions. |
| default_uom_area | Default Area UOM | Link | UOM | | Square Meter | Panel surface rules. |
| default_warehouse_raw | Default Raw Material Warehouse | Link | Warehouse | | | GRN default (ERPNext). |
| default_warehouse_wip | Default WIP Warehouse | Link | Warehouse | | | Production issues. |
| default_warehouse_fg | Default Finished Goods Warehouse | Link | Warehouse | | | FG receipt.default |

### Section: Naming Series — column layout **3 columns**

| Fieldname | Label | Type | Options | Req | Default | Description |
|-----------|-------|------|---------|-----|---------|-------------|
| family_naming_series | Product Family Naming Series | Data | | ✓ | `FPF-.#####` | Family autoname. |
| material_naming_series | Material Naming Series | Data | | ✓ | `FMAT-.#####` | Material autoname. |
| finish_naming_series | Finish Naming Series | Data | | ✓ | `FFIN-.#####` | Finish autoname. |
| specification_naming_series | Specification Naming Series | Data | | ✓ | `FSPEC-.YYYY.-.#####` | Spec autoname. |

### Section: Catalogue Rules — column layout **3 columns**

| Fieldname | Label | Type | Options | Req | Default | Description |
|-----------|-------|------|---------|-----|---------|-------------|
| enforce_allowed_materials | Enforce Allowed Materials on Spec | Check | | | 1 | Reject spec lines outside family.allowlist. |
| enforce_allowed_finishes | Enforce Allowed Finishes on Spec | Check | | | 1 | Same for finishes. |
| allow_draft_spec_duplication | Allow Duplicate Draft Specs | Check | | | 0 | Clone policy. |
| default_gst_hsn_code | Default HSN Code | Data | | | | Fallback for new Items (India). |
| spec_requires_approval | Specification Requires Approval | Check | | | 0 | If 1, only Approved specs on quotations (later). |

### Section: Integration — column layout **3 columns**

| Fieldname | Label | Type | Options | Req | Default | Description |
|-----------|-------|------|---------|-----|---------|-------------|
| enable_portal_catalogue | Enable Portal Catalogue | Check | | | 0 | Future website (deferred). |
| integration_webhook_url | Integration Webhook URL | Data | URL | | | Outbound events (optional). |

---

## Furniture Product Family

**Type:** Setup | **Milestone:** M1 | **Naming:** `family_naming_series` | **Title field:** `family_name`

### Section: Identity — **3 columns**

| Fieldname | Label | Type | Options / Link | Req | Description |
|-----------|-------|------|----------------|-----|-------------|
| family_name | Family Name | Data | | ✓ | e.g. Dining Table, Wardrobe Carcass. |
| family_code | Family Code | Data | | | Short code for SKU composition. |
| item_group | Item Group | Link | Item Group | | ERPNext group for generated Items. |
| status | Status | Select | Draft; Active; Discontinued | ✓ | Active |
| description | Description | Text Editor | | | Marketing / internal summary. |
| default_lead_time_days | Default Lead Time (Days) | Int | | | Planning hint for quotations. |

### Section: Classification — **3 columns**

| Fieldname | Label | Type | Options | Req | Description |
|-----------|-------|------|----------------|-----|-------------|
| product_category | Product Category | Select | Seating; Tables; Storage; Kitchen; Bedroom; Office; Outdoor; Other | | |
| construction_type | Construction Type | Select | Panel; Solid Wood; Hybrid; Upholstered; Metal | | |
| is_configurable | Configurable | Check | | ✓ | 1 | If set, uses Specification / attributes. |

### Section: Media — full width

| Fieldname | Label | Type | Req | Description |
|-----------|-------|------|-----|-------------|
| hero_image | Hero Image | Attach Image | | List / portal thumbnail. |
| drawing_attachment | Reference Drawing | Attach | | PDF/DWG reference. |

### Child table: Allowed Materials

**Parent:** Furniture Product Family | **Table field:** `allowed_materials` | **DocType:** Furniture Family Allowed Material

| Fieldname | Label | Type | Link | Req | Description |
|-----------|-------|------|------|-----|-------------|
| material | Material | Link | Furniture Material | ✓ | Allowed board/substrate. |
| is_default | Default | Check | | | One default per family (validated server-side). |
| notes | Notes | Small Text | | | e.g. carcass only. |

### Child table: Allowed Finishes

**Parent:** Furniture Product Family | **Table field:** `allowed_finishes` | **DocType:** Furniture Family Allowed Finish

| Fieldname | Label | Type | Link | Req | Description |
|-----------|-------|------|------|-----|-------------|
| finish | Finish | Link | Furniture Finish | ✓ | Allowed surface treatment. |
| application | Application | Select | Carcass; Shutter; Top; All | | |
| is_default | Default | Check | | | |

---

## Furniture Material

**Type:** Setup | **Milestone:** M1 | **Naming:** `material_naming_series` | **Title:** `material_name`

### Section: Identity — **3 columns**

| Fieldname | Label | Type | Options / Link | Req | Description |
|-----------|-------|------|----------------|-----|-------------|
| material_name | Material Name | Data | | ✓ | Commercial name. |
| material_type | Material Type | Select | Plywood; MDF; Particle Board; Hardwood; Hardware; Glass; Stone; Other | ✓ | |
| grade | Grade | Data | | | e.g. BWP, MR, E1. |
| status | Status | Select | Active; Inactive | ✓ | Active |
| linked_item | Linked Item | Link | Item | | ERPNext stock item for this material. |

### Section: Physical — **3 columns**

| Fieldname | Label | Type | Req | Description |
|-----------|-------|------|-----|-------------|
| default_thickness_mm | Default Thickness (mm) | Float | | Panel goods. |
| default_width_mm | Default Width (mm) | Float | | Sheet size. |
| default_length_mm | Default Length (mm) | Float | | Sheet size. |
| weight_per_unit | Weight per Unit | Float | | kg per UOM. |
| uom | UOM | Link → UOM | ✓ | Nos, Sq Meter, etc. |
| hsn_code | HSN Code | Data | | India GST (ASM). |

### Section: Costing hints — **3 columns**

| Fieldname | Label | Type | Description |
|-----------|-------|------|-------------|
| reference_rate | Reference Rate | Currency | Non-binding planning rate. |
| currency | Currency | Link → Currency | |
| last_rate_updated_on | Last Rate Updated On | Date | |

### Child table: Supplier Preferences (M2)

**Table field:** `supplier_preferences` | **DocType:** Furniture Material Supplier Preference

| Fieldname | Label | Type | Link | Req | Description |
|-----------|-------|------|------|-----|-------------|
| supplier | Supplier | Link | Supplier | ✓ | ERPNext supplier. |
| lead_time_days | Lead Time (Days) | Int | | | |
| min_order_qty | Min Order Qty | Float | | | |
| is_preferred | Preferred | Check | | | |

---

## Furniture Finish

**Type:** Setup | **Milestone:** M1 | **Naming:** `finish_naming_series` | **Title:** `finish_name`

### Section: Identity — **3 columns**

| Fieldname | Label | Type | Options / Link | Req | Description |
|-----------|-------|------|----------------|-----|-------------|
| finish_name | Finish Name | Data | | ✓ | |
| finish_type | Finish Type | Select | Laminate; Veneer; PU Paint; Melamine; Edge Band; Powder Coat; Fabric; Leather; Other | ✓ | |
| finish_code | Finish Code | Data | | | Short code for SKU. |
| status | Status | Select | Active; Inactive | ✓ | Active |
| linked_item | Linked Item | Link | Item | | Consumable SKU if stocked. |

### Section: Appearance & process — **3 columns**

| Fieldname | Label | Type | Options | Description |
|-----------|-------|------|---------|-------------|
| color_name | Color Name | Data | | |
| color_code | Color / Shade Code | Data | | Supplier code. |
| gloss_level | Gloss Level | Select | Matte; Satin; Gloss | |
| grain_direction_required | Grain Direction Required | Check | | |
| curing_lead_time_days | Curing Lead Time (Days) | Int | | Paint/lacquer. |

### Section: Compliance — **3 columns**

| Fieldname | Label | Type | Description |
|-----------|-------|------|-------------|
| voc_compliant | Low VOC Compliant | Check | |
| fire_rating | Fire Rating | Data | If applicable. |
| hsn_code | HSN Code | Data | GST. |

### Section: Media — full width

| Fieldname | Label | Type | Description |
|-----------|-------|------|-------------|
| swatch_image | Swatch Image | Attach Image | |

---

## Furniture Specification

**Type:** Setup | **Milestone:** M2 | **Naming:** `specification_naming_series` | **Title:** `spec_title` | **Amendable:** Yes

### Section: Header — **3 columns**

| Fieldname | Label | Type | Link | Req | Description |
|-----------|-------|------|------|-----|-------------|
| spec_title | Specification Title | Data | | ✓ | Customer-facing name. |
| product_family | Product Family | Link | Furniture Product Family | ✓ | |
| customer | Customer | Link | Customer | | Project customer (ERPNext). |
| project | Project | Link | Project | | Optional large job. |
| spec_status | Status | Select | Draft; In Review; Approved; Rejected; Obsolete | ✓ | Draft |
| version | Version | Int | | ✓ | 1 | Increment on amend. |
| valid_from | Valid From | Date | | | |
| valid_upto | Valid Upto | Date | | | |

### Section: Dimensions (outer) — **3 columns**

| Fieldname | Label | Type | Req | Description |
|-----------|-------|------|-----|-------------|
| width_mm | Width (mm) | Float | ✓ | Overall. |
| depth_mm | Depth (mm) | Float | ✓ | |
| height_mm | Height (mm) | Float | ✓ | |
| weight_kg_est | Estimated Weight (kg) | Float | | |

### Section: Materials & finishes — **3 columns**

| Fieldname | Label | Type | Link | Req | Description |
|-----------|-------|------|------|-----|-------------|
| primary_material | Primary Material | Link | Furniture Material | ✓ | Must be in family allowlist if enforced. |
| primary_finish | Primary Finish | Link | Furniture Finish | ✓ | |
| secondary_finish | Secondary Finish | Link | Furniture Finish | | Accents, edging. |
| edge_band_finish | Edge Band Finish | Link | Furniture Finish | | |

### Section: Manufacturing links — **3 columns**

| Fieldname | Label | Type | Link | Description |
|-----------|-------|------|------|-------------|
| target_item | Target Item | Link | Item | Generated/configured sellable SKU. |
| default_bom | Default BOM | Link | BOM | After engineering (later milestone). |
| drawing_no | Drawing Number | Data | | |

### Section: Notes — full width

| Fieldname | Label | Type | Description |
|-----------|-------|------|-------------|
| internal_notes | Internal Notes | Text Editor | |
| customer_facing_notes | Customer Facing Notes | Text Editor | |

### Child table: Specification Attributes

**Table field:** `attributes` | **DocType:** Furniture Specification Attribute

| Fieldname | Label | Type | Options | Req | Description |
|-----------|-------|------|---------|-----|-------------|
| attribute_name | Attribute | Data | | ✓ | e.g. Drawer Count, Handle Type. |
| attribute_value | Value | Data | | ✓ | |
| uom | UOM | Link → UOM | | | For numeric attrs. |
| is_price_driver | Price Driver | Check | | | Used in pricing engine (later). |

---

## Child DocType summary

| Child DocType | Parent | Table field |
|---------------|--------|-------------|
| Furniture Family Allowed Material | Furniture Product Family | allowed_materials |
| Furniture Family Allowed Finish | Furniture Product Family | allowed_finishes |
| Furniture Material Supplier Preference | Furniture Material | supplier_preferences |
| Furniture Specification Attribute | Furniture Specification | attributes |

---

## Permissions sketch (detail in role-permission-matrix.md)

| DocType | Create | Submit | Amend |
|---------|--------|--------|-------|
| Furniture ERP Settings | System Manager | — | — |
| Furniture Product Family | Catalogue Manager | — | — |
| Furniture Material / Finish | Catalogue Manager | — | — |
| Furniture Specification | Designer | Workflow → Approved | Designer / Manager |

---

## Validation rules (server-side, planned)

1. **Allowlist:** If settings enforce flags, `primary_material` / finishes must appear in family child tables.  
2. **Default uniqueness:** At most one `is_default` per child table per parent.  
3. **Approved spec:** Cannot set `spec_status = Approved` without dimensions and primary material/finish.  
4. **Item link:** On save, optional stub to create/update ERPNext Item when integration hook enabled (post–ERPNext install).