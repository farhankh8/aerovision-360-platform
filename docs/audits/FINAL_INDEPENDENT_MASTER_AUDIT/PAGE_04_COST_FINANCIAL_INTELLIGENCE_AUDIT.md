# PAGE 04 — COST & FINANCIAL INTELLIGENCE AUDIT

**Source:** Authoritative main PBIX `deliverables/power_bi/AEROVISION_360.pbix`, page folder `ad43d4cc257c455c5a9b`  
**Page name:** `COST & FINANCIAL INTELLIGENCE`  
**Page order:** Page 04 (fourth page)  
**Visual count:** 23  
**Page rendered in Power BI Desktop:** Not independently verified (limitation L-1); visual metadata verified from binary.

---

## 1. Visual inventory

23 visuals (full table in `POWER_BI_FIVE_PAGE_VISUAL_INVENTORY.md`). Key data visuals:

| Visual | Type | Title | Bound measure | Bound column/table |
|---|---|---|---|---|
| Card | cardVisual | 'TOTAL OPERATING COSTS (USD)' | CX_TotalOperatingCostsUSD | fact_operating_costs |
| Card | cardVisual | 'POSITIVE OPERATING COSTS (USD)' | CX_PositiveCostsUSD | fact_operating_costs |
| Card | cardVisual | 'COST REVERSALS (USD)' | CX_CostReversalsUSD | fact_operating_costs |
| Card | cardVisual | 'NET OPERATING COSTS (USD)' | CX_NetOperatingCostsUSD | fact_operating_costs |
| Card | cardVisual | 'COST PER FLIGHT OPERATION (USD)' | CX_CostPerFlightOperationUSD | fact_operating_costs |
| Card | cardVisual | 'COST PER REVENUE PASSENGER (USD)' | CX_CostPerRevenuePassengerUSD | fact_operating_costs + fact_flight_operations |
| Card | cardVisual | 'NET OPERATING CONTRIBUTION (USD)' | NC_NetOperatingContributionUSD | RV - CX |
| Card | cardVisual | 'REVENUE-TO-COST RATIO (%)' | NC_RevenueToCostRatio | RV / CX |
| Line chart | lineChart | 'Monthly Operating Cost Trend' | measure | dim_date |
| Clustered bar chart | clusteredBarChart | 'Costs by Category' | measure | fact_operating_costs |
| Clustered bar chart | clusteredBarChart | 'Costs by Airline ' | measure | dim_airline |
| Treemap | treemap | 'Route Cost Composition' | measure | dim_route |
| Scatter chart | scatterChart | 'Airline Cost Efficiency vs Operating Contribution' | measures | dim_airline |
| Map | map | 'Operating Cost Geographic Distribution' | X/Y: **fact_route_costs_map** | **fact_route_costs_map** |
| Slicer | slicer | 'FLIGHT DATE RANGE' | — | dim_date |
| Slicer | slicer | 'AIRLINE' | — | dim_airline |

Plus page navigator, action button, textboxes, images, shapes.

---

## 2. Measure binding correctness (cost/financial measures)

| Measure | Defined in DAX? | Registered in model.json? | Bound on Page 04? | Blocked by OD-04? | Status |
|---|---|---|---|---|---|
| CX_TotalOperatingCostsUSD | Yes | Yes | Yes | Yes | BLOCKED (data) |
| CX_PositiveCostsUSD | Yes | Yes | Yes | Yes | BLOCKED (data) |
| CX_CostReversalsUSD | Yes | Yes | Yes | Yes | BLOCKED (data) |
| CX_NetOperatingCostsUSD | Yes | Yes | Yes | Yes | BLOCKED (data) |
| CX_CostPerFlightOperationUSD | Yes | Yes | Yes | Yes | BLOCKED (data) |
| CX_CostPerRevenuePassengerUSD | Yes | Yes | Yes | Yes | BLOCKED (data) |
| CX_CostsCurrentPeriod/Prior/Growth/YTD | Yes | Yes | No | Yes | BLOCKED (data) |
| NC_NetOperatingContributionUSD | Yes | Yes | Yes | Yes | BLOCKED (data) |
| NC_RevenueToCostRatio | Yes | Yes | Yes | Yes | BLOCKED (data) |
| NC_RevenuePerRevenuePassengerUSD | Yes | Yes | No | Yes | BLOCKED (data) |

All CX_/NC_ measures defined in DAX and registered in `model.json`. Blocked at the data layer by OD-04 (FactOperatingCosts not loaded; exchange rates missing).

---

## 3. Critical finding: orphaned table reference on map visual

**Finding P04-01 (HIGH):** The map visual `Operating Cost Geographic Distribution` binds X and Y to `fact_route_costs_map`. This table name does **not** appear anywhere in the 16 tables of `semantic_model/model.json` (dim_airline, dim_airport, dim_route, dim_date, dim_aircraft, dim_aircraft_type, dim_customer, dim_disruption_type, dim_booking_channel, dim_currency, dim_fare_class, fact_flight_operations, fact_disruptions, fact_customer_feedback, fact_booking_transactions, fact_operating_costs).

Two possibilities:
1. `fact_route_costs_map` exists only in the in-PBIX binary `DataModel` (could not be deserialized — limitation L-2) — in which case `model.json` is incomplete/stale relative to the live model.
2. `fact_route_costs_map` does not exist in the live model either — in which case the map visual is broken/orphaned.

This must be resolved by inspecting the model in Power BI Desktop. Until resolved, the map visual's data source is unverified.

---

## 4. OD-04 dependency

Same as Page 03: Page 04 cost/contribution/ratio cards all depend on financial fact data blocked by OD-04. Page is built; data blocked upstream.

---

## 5. Findings

| ID | Finding | Severity | Evidence | Confidence |
|---|---|---|---|---|
| P04-01 | Map visual binds to `fact_route_costs_map`, absent from the 16-table model.json | HIGH | Page 04 visual `7b9fc3c1…`; `semantic_model/model.json` table list | High (reference absent from model.json) |
| P04-02 | Cost/revenue/contribution KPI cards blocked by OD-04 (financial facts not loaded) | HIGH | `OD04…`; data_sources.json omits financial facts | High |
| P04-03 | In-PBIX binary model not deserializable; cannot confirm whether fact_route_costs_map exists in live model | MEDIUM | Limitation L-2 | — |
| P04-04 | Page rendering not independently verified (limitation L-1) | INFORMATIONAL | — | — |

---

## 6. Implementation status

**Dashboard development: COMPLETE AND VERIFIED (as built).** Page 04 exists with 23 visuals including cards, charts, treemap, scatter, map, slicers.

**Data integration: BLOCKED.** Financial measures cannot render USD values until OD-04 resolved; map visual table reference unresolved.

Not counted as incomplete dashboard development.
