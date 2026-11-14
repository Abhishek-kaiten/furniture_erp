# Reports & Dashboards

Reporting split between **Frappe Query Reports / Script Reports** in `furniture_erp` and **standard ERPNext reports** (after install).

## Workspaces (planned)

| Workspace | Audience | Widgets |
|-----------|----------|---------|
| Furniture Catalogue | Catalogue Manager | Shortcuts: Family, Material, Finish, Spec; chart Specs by status |
| Furniture Sales | Sales | Open quotations, SO pipeline (ERPNext) |
| Furniture Production | Production | Open WO, JC pending (ERPNext) |
| Furniture Accounts | Finance | Sales register, GST summary (ERPNext) |

**M0:** No custom workspace JSON exported.

## Custom reports (furniture_erp)

| Report | Type | Milestone | Description |
|--------|------|-----------|-------------|
| Catalogue — Materials by Type | Query | M2 | Active materials grouped by material_type |
| Catalogue — Family Allowlist Audit | Script | M2 | Families missing default material/finish |
| Specification Register | Query | M2 | Filters: family, status, customer, date |
| Specification vs Item Linkage | Script | M4 | Specs without `target_item` |
| Open Specifications In Review | Query | M2 | Workflow aging |
| Integration Log Summary | Query | M3 | Failed outbound calls |

## ERPNext standard reports (blocked — use when available)

| Report | Use |
|--------|-----|
| Sales Order Trends | Pipeline |
| BOM Stock Report | Material availability for WO |
| Stock Balance | On-hand by warehouse |
| Gross Profit | Margin by item/customer |
| General Ledger | Audit |
| GST Sales Register | Compliance (India) |
| Production Analytics | WO completion |

## Dashboards (ERPNext Dashboard — planned)

| Dashboard | Charts |
|-----------|--------|
| Executive | Monthly sales, top families (custom join Spec→SO later), FG stock value |
| Factory | WO completion rate, JC hours |
| Procurement | PO pending, lead time variance |

## KPI definitions (Master Build alignment)

| KPI | Formula source | Milestone |
|-----|----------------|-----------|
| Catalogue coverage | % Active families with ≥1 approved spec | M2 |
| Quote cycle time | Lead created → Quotation submitted | M4 |
| OTIF delivery | DN date vs SO delivery date | M6 |
| WIP age | Days WO open | M5 |
| Gross margin % | ERPNext Gross Profit report | M3+ |

## Export / print formats

| DocType | Print format | Milestone |
|---------|--------------|-----------|
| Furniture Specification | Customer spec sheet PDF | M2 |
| Quotation | Branded quote with spec appendix | M4 |

## Permissions

Reports inherit role permissions on underlying DocTypes; Script Reports must enforce `frappe.has_permission` checks.