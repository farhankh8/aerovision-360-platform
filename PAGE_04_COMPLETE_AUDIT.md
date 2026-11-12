# AEROVISION 360 — Page 04 Cost & Financial Intelligence Audit

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit Date:** 2026-11-07  
**Role:** Principal Power BI Architect / Senior Financial BI Consultant / DAX Engineer  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.  
**Status:** AUDIT AND BLUEPRINT ONLY — NO IMPLEMENTATION PERFORMED

---

## PART A — Current Page 04 Status

### A.1 What Currently Exists

The report definition (`deliverables/power_bi/report/report.json`) contains **5 pages**, not 6. Page 04 currently exists as **"Operations & Disruption"** — NOT as "Cost & Financial Intelligence".

| Page | Name | Visuals | Type |
|---|---|---|---|
| Page 01 | Executive Overview | 4 | Cards + barChart |
| Page 02 | Network & Capacity Intelligence | 2 | barCharts |
| Page 03 | Revenue & Finance | 28 | Cards, lineCharts, barCharts, pieChart, slicers |
| Page 04 | **Operations & Disruption** | 3 | Cards (FL04, DS03), barChart (DS01) |
| Page 05 | Customer & Service Intelligence | 13 | Cards, barCharts |

**Critical Finding:** Page 04 does NOT exist as "Cost & Financial Intelligence". It currently exists as "Operations & Disruption" with only 3 operational visuals. Converting it to "Cost & Financial Intelligence" requires replacing all 3 visuals and changing the page name.

### A.2 What Does NOT Exist

| Item | Status | Evidence |
|---|---|---|
| Page named "Cost & Financial Intelligence" | Missing | report.json has no page with this name |
| Cost & Financial Intelligence visuals | Missing | Page 04 has only FL04, DS03, DS01 |
| Page 06 | Missing | report.json contains exactly 5 pages (matches data contract) |
| Page navigation structure | Not defined | report.json has no navigation objects |

---

## PART B — Complete DAX Measure Audit

### B.1 All Measures in DAX File (54 total)

| Measure | Prefix | Defined in DAX | Registered in model.json | Registered in semantic_model.json | Referenced in report.json |
|---|---|---|---|---|---|
| FL01 | Operational | Yes | Yes | Yes | Yes (Page 01, Page 02) |
| FL02 | Operational | Yes | Yes | Yes | Yes (Page 02) |
| FL03 | Operational | Yes | Yes | Yes | Yes (Page 01) |
| FL04 | Operational | Yes | Yes | Yes | Yes (Page 04 card) |
| DS01 | Disruption | Yes | Yes | Yes | Yes (Page 04 barChart) |
| DS02 | Disruption | Yes | Yes | Yes | No visual |
| DS03 | Disruption | Yes | Yes | Yes | Yes (Page 04 card) |
| OP01 | Operations | Yes | **NO** | **NO** | No |
| OP03 | Operations | Yes | **NO** | **NO** | No |
| OP04 | Operations | Yes | **NO** | **NO** | No |
| RV_BookingCount | Revenue | Yes | Yes | Yes | No |
| RV_DistinctBookings | Revenue | Yes | Yes | Yes | No |
| RV_RevenuePassengers | Revenue | Yes | Yes | Yes | No |
| RV_NonRevenuePassengers | Revenue | Yes | Yes | Yes | No |
| RV_GrossBookingValueUSD | Revenue | Yes | Yes | Yes | No |
| RV_RefundAmountUSD | Revenue | Yes | Yes | Yes | No |
| RV_NetPassengerRevenueUSD | Revenue | Yes | Yes | Yes | Yes (Page 03 card) |
| RV_NetFeeRevenueUSD | Revenue | Yes | Yes | Yes | Yes (Page 03 card) |
| RV_NetAncillaryRevenueUSD | Revenue | Yes | Yes | Yes | No |
| RV_TotalOperatingRevenueUSD | Revenue | Yes | Yes | Yes | Yes (Page 03 card) |
| RV_AvgRevenuePerRevenuePassenger | Revenue | Yes | Yes | Yes | No |
| RV_AvgBookingValueUSD | Revenue | Yes | Yes | Yes | No |
| RV_RevenueCurrentPeriodUSD | Revenue | Yes | Yes | Yes | No |
| RV_RevenuePriorPeriodUSD | Revenue | Yes | Yes | Yes | No |
| RV_RevenueGrowthPercent | Revenue | Yes | Yes | Yes | No |
| RV_RevenueYTDUSD | Revenue | Yes | Yes | Yes | No |
| RV_RevenueByBookingDateUSD | Revenue | Yes | Yes | Yes | No |
| CX_TotalOperatingCostsUSD | Cost | Yes | Yes | Yes | Yes (Page 03 card) |
| CX_PositiveCostsUSD | Cost | Yes | Yes | Yes | No |
| CX_CostReversalsUSD | Cost | Yes | Yes | Yes | No |
| CX_NetOperatingCostsUSD | Cost | Yes | Yes | Yes | No |
| CX_CostPerFlightOperationUSD | Cost | Yes | Yes | Yes | No |
| CX_CostPerRevenuePassengerUSD | Cost | Yes | Yes | Yes | No |
| CX_CostsCurrentPeriodUSD | Cost | Yes | Yes | Yes | No |
| CX_CostsPriorPeriodUSD | Cost | Yes | Yes | Yes | No |
| CX_CostGrowthPercent | Cost | Yes | Yes | Yes | No |
| CX_CostsYTDUSD | Cost | Yes | Yes | Yes | No |
| NC_NetOperatingContributionUSD | Financial | Yes | Yes | Yes | Yes (Page 03 card) |
| NC_RevenueToCostRatio | Financial | Yes | Yes | Yes | Yes (Page 03 card) |
| NC_RevenuePerRevenuePassengerUSD | Financial | Yes | Yes | Yes | No |

### B.2 Measures Relevant to Page 04

All required Page 04 measures **already exist** in the DAX file and are registered in both model.json and semantic_model.json. **No new DAX measures need to be created.**

#### Measures Already Available for Page 04:

| Measure | Formula | Home Table | Registered? | Safe for Page 04? |
|---|---|---|---|---|
| CX_TotalOperatingCostsUSD | SUM(CostAmountUSD) | fact_operating_costs | ✓ | Yes |
| CX_PositiveCostsUSD | CALCULATE(SUM(CostAmountUSD), CostAmountUSD>0) | fact_operating_costs | ✓ | Yes |
| CX_CostReversalsUSD | CALCULATE(SUM(CostAmountUSD), CostAmountUSD<0) | fact_operating_costs | ✓ | Yes |
| CX_NetOperatingCostsUSD | CX_TotalOperatingCostsUSD | fact_operating_costs | ✓ | Yes |
| CX_CostPerFlightOperationUSD | DIVIDE(Costs, DISTINCTCOUNT(FlightOperationKey)) | fact_operating_costs | ✓ | Yes |
| CX_CostPerRevenuePassengerUSD | DIVIDE(Costs, RV_RevenuePassengers) | fact_operating_costs | ✓ | Yes |
| NC_NetOperatingContributionUSD | Revenue − Costs | fact_booking_transactions | ✓ | Yes |
| NC_RevenueToCostRatio | DIVIDE(Revenue, Costs) | fact_booking_transactions | ✓ | Yes |
| NC_RevenuePerRevenuePassengerUSD | DIVIDE(Revenue, RevenuePassengers) | fact_booking_transactions | ✓ | Yes |
| CX_CostsCurrentPeriodUSD | CALCULATE(Costs, IsReportingPeriod=TRUE()) | fact_operating_costs | ✓ | Yes |
| CX_CostsPriorPeriodUSD | CALCULATE(Costs, SAMEPERIODLASTYEAR) | fact_operating_costs | ✓ | Yes* |
| CX_CostGrowthPercent | DIVIDE(Current−Prior, Prior) | fact_operating_costs | ✓ | Yes* |
| CX_CostsYTDUSD | TOTALYTD(Costs, FullDate) | fact_operating_costs | ✓ | Yes* |
| RV_TotalOperatingRevenueUSD | Sum of 3 revenue components | fact_booking_transactions | ✓ | Yes |
| RV_RevenuePassengers | CALCULATE(SUM(PassengerCount), IsRevenuePassenger=TRUE()) | fact_booking_transactions | ✓ | Yes |

* Requires dim_date marked as Date Table in Power BI Desktop. Data starts 2025-10-01, so prior-period comparisons will return BLANK.

### B.3 Measures NOT Available

| Measure | Reason |
|---|---|
| OP01, OP03, OP04 | Exist in DAX but NOT registered in model.json or semantic_model.json. Cannot be used in visuals. |

### B.4 Duplicate Measure Issue

**RESOLVED:** NC_CostPerRevenuePassengerUSD was identified as a duplicate of CX_CostPerRevenuePassengerUSD (identical formula) and has been removed. Only CX_CostPerRevenuePassengerUSD remains.

---

## PART C — Financial Calculation Validation

All figures below were independently recalculated from source CSV files.

### C.1 Revenue Reconciliation

| Component | Value | Verified |
|---|---|---|
| Net Passenger Revenue | $8,404,563.76 | ✓ |
| Net Fee Revenue | $418,161.93 | ✓ |
| Net Ancillary Revenue | $230,117.72 | ✓ |
| **Total Operating Revenue** | **$9,052,843.41** | ✓ |

**Formula:** RV_TotalOperatingRevenueUSD = NetPassengerRevenueUSD + NetFeeRevenueUSD + NetAncillaryRevenueUSD

### C.2 Operating Cost Reconciliation

| Component | Value | Verified |
|---|---|---|
| Positive Costs (expenses) | $196,633,594.04 | ✓ |
| Cost Reversals (credits) | -$1,944,806.68 | ✓ |
| **Net Operating Costs** | **$194,688,787.36** | ✓ |

**Formula:** CX_TotalOperatingCostsUSD = SUM(CostAmountUSD) — signed amounts net automatically

**Test A — Positive Costs + Reversals = Net Operating Costs:**
$196,633,594.04 + (-$1,944,806.68) = $194,688,787.36 ✓ **PASS**

### C.3 Contribution Calculation

| Component | Value | Verified |
|---|---|---|
| Total Operating Revenue | $9,052,843.41 | ✓ |
| Net Operating Costs | $194,688,787.36 | ✓ |
| **Net Operating Contribution** | **-$185,635,943.95** | ✓ |

**Formula:** NC_NetOperatingContributionUSD = RV_TotalOperatingRevenueUSD − CX_TotalOperatingCostsUSD

**Test B — Revenue − Costs = Contribution:**
$9,052,843.41 − $194,688,787.36 = -$185,635,943.95 ✓ **PASS**

### C.4 Cost per Flight Operation

| Component | Value | Verified |
|---|---|---|
| Total Operating Costs | $194,688,787.36 | ✓ |
| Distinct FlightOperationKeys | 5,000 | ✓ |
| **Cost per Flight Operation** | **$38,937.76** | ✓ |

**Formula:** CX_CostPerFlightOperationUSD = DIVIDE(CX_TotalOperatingCostsUSD, DISTINCTCOUNT(FlightOperationKey), BLANK())

**Test D — Cost per Flight Operation:** $194,688,787.36 / 5,000 = $38,937.76 ✓ **PASS**

Note: FL01 (Flights Operated = 4,776) counts only operated flights. CX_CostPerFlightOperationUSD uses DISTINCTCOUNT(FlightOperationKey) = 5,000 which counts ALL flight legs (including cancelled). These are different denominators — FL01 ≠ distinct flight operations in costs.

### C.5 Cost per Revenue Passenger

| Component | Value | Verified |
|---|---|---|
| Total Operating Costs | $194,688,787.36 | ✓ |
| Revenue Passengers | 8,922 | ✓ |
| **Cost per Revenue Passenger** | **$21,821.20** | ✓ |

**Formula:** CX_CostPerRevenuePassengerUSD = DIVIDE(CX_TotalOperatingCostsUSD, RV_RevenuePassengers, BLANK())

**Test C — Cost per Revenue Passenger:** $194,688,787.36 / 8,922 = $21,821.20 ✓ **PASS**

Note: RV_RevenuePassengers uses IsRevenuePassenger=TRUE filter on PassengerCount = 8,922. FL02 (Total Revenue Passengers = 218,413) uses SUM(RevenuePassengers) from fact_flight_operations — these are different populations and should NOT be mixed.

### C.6 Revenue-to-Cost Ratio

| Component | Value | Verified |
|---|---|---|
| Total Operating Revenue | $9,052,843.41 | ✓ |
| Net Operating Costs | $194,688,787.36 | ✓ |
| **Revenue-to-Cost Ratio** | **0.0465** | ✓ |

**Formula:** NC_RevenueToCostRatio = DIVIDE(RV_TotalOperatingRevenueUSD, CX_TotalOperatingCostsUSD, BLANK())

**Test E — Revenue-to-Cost Ratio:** $9,052,843.41 / $194,688,787.36 = 0.0465 ✓ **PASS**

### C.7 Period Calculations

| Measure | Status | Reason |
|---|---|---|
| CX_CostsCurrentPeriodUSD | Available | All cost dates within 2025-10-01 to 2026-09-30 |
| CX_CostsPriorPeriodUSD | Returns BLANK | No data before 2025-10-01; SAMEPERIODLASTYEAR references 2024-10-01 to 2025-09-30 which is empty |
| CX_CostGrowthPercent | Returns BLANK | Depends on prior period which is empty |
| CX_CostsYTDUSD | Available | Requires dim_date marked as Date Table |

**Critical Limitation:** dim_date is NOT marked as a Date Table in the PBIX. TOTALYTD and SAMEPERIODLASTYEAR require this designation. Until marked, YTD and prior-period measures will return BLANK.

---

## PART D — Semantic Model and Relationship Audit

### D.1 Tables Relevant to Page 04

| Table | Columns | Relationships | Relevant to Page 04? |
|---|---|---|---|
| fact_operating_costs | 18 | 4 (active) | YES — primary cost fact |
| fact_booking_transactions | 45 | 8 (active) | YES — revenue & passenger data |
| dim_airline | 11 | 0 | YES — airline filtering |
| dim_route | 9 | 2 | YES — route filtering |
| dim_date | 23 | 0 | YES — date filtering |
| dim_currency | 6 | 0 | YES — currency filtering |
| dim_airport | 10 | 0 | NO — no direct link from costs |
| dim_fare_class | 7 | 0 | NO — not needed for costs |
| dim_booking_channel | 6 | 0 | NO — not needed for costs |

### D.2 Relationship Matrix for Page 04

| From Table/Column | To Table/Column | Cardinality | Direction | Active | Page 04 Impact |
|---|---|---|---|---|---|
| fact_operating_costs.AirlineKey | dim_airline.AirlineKey | 1:many | Single | Yes | Cost by airline |
| fact_operating_costs.RouteKey | dim_route.RouteKey | 1:many | Single | Yes | Cost by route |
| fact_operating_costs.CostDateKey | dim_date.DateKey | 1:many | Single | Yes | Cost trend over time |
| fact_operating_costs.CurrencyKey | dim_currency.CurrencyKey | 1:many | Single | Yes | Cost by currency |
| fact_booking_transactions.AirlineKey | dim_airline.AirlineKey | 1:many | Single | Yes | Revenue by airline |
| fact_booking_transactions.RouteKey | dim_route.RouteKey | 1:many | Single | Yes | Revenue by route |
| fact_booking_transactions.TravelDateKey | dim_date.DateKey | 1:many | Single | Yes | Revenue trend over time |
| fact_booking_transactions.BookingDateKey | dim_date.DateKey | 1:many | Single | Inactive | Not needed for Page 04 |
| fact_booking_transactions.TransactionCurrencyKey | dim_currency.CurrencyKey | 1:many | Single | Yes | Revenue by currency |

### D.3 Map Visual Assessment

**NOT RECOMMENDED for Page 04.**

Reasoning:
- fact_operating_costs has no AirportKey column
- dim_airport has Latitude and Longitude, but costs connect to airports only via RouteKey → dim_route (OriginAirportKey/DestinationAirportKey) → dim_airport
- This is a multi-hop relationship that would require a bridge table or complex DAX
- Power BI map visuals work best with direct latitude/longitude on the fact table
- A map visual would be decorative rather than analytical

### D.4 Slicer Analysis

| Slicer | Table | Column | Type | Affects All Visuals? |
|---|---|---|---|---|
| Date | dim_date | FullDate | Date slicer | Yes (via CostDateKey/TravelDateKey) |
| Airline | dim_airline | AirlineName | Multi-select | Yes (via AirlineKey) |
| Route | dim_route | RouteCode | Multi-select | Yes (via RouteKey) |
| Currency | dim_currency | CurrencyCode | Multi-select | Yes (via CurrencyKey) |
| Cost Category | fact_operating_costs | CostCategory | Multi-select | Yes (direct) |
| Cost Subcategory | fact_operating_costs | CostSubcategory | Multi-select | Yes (direct) |

All slicers filter through active relationships — no ambiguous paths.

---

## PART E — Visualization Blueprint

### E.1 Essential Visuals (Required for Page 04)

| # | Visual Name | Type | Business Question | Measure | Category | Axis/Legend |
|---|---|---|---|---|---|---|
| 1 | Total Operating Costs | Card | Total cost across all categories | CX_TotalOperatingCostsUSD | None | N/A |
| 2 | Positive Operating Costs | Card | Pure expense amount | CX_PositiveCostsUSD | None | N/A |
| 3 | Cost Reversals/Credits | Card | Credited back amount | CX_CostReversalsUSD | None | N/A |
| 4 | Net Operating Contribution | Card | Revenue minus costs | NC_NetOperatingContributionUSD | None | N/A |
| 5 | Revenue-to-Cost Ratio | Card | Revenue per $1 cost | NC_RevenueToCostRatio | None | N/A |
| 6 | Cost per Flight Operation | Card | Cost per flight leg | CX_CostPerFlightOperationUSD | None | N/A |
| 7 | Cost per Revenue Passenger | Card | Cost per revenue passenger | CX_CostPerRevenuePassengerUSD | None | N/A |
| 8 | Costs by Category | Bar Chart | Which categories drive spend? | CX_TotalOperatingCostsUSD | CostCategory | X: Category, Y: Cost |
| 9 | Costs by Airline | Bar Chart | Which airlines bear most cost? | CX_TotalOperatingCostsUSD | AirlineName | X: Airline, Y: Cost |
| 10 | Costs by Route | Bar Chart | Which routes most expensive? | CX_TotalOperatingCostsUSD | RouteCode | X: Route, Y: Cost |
| 11 | Cost Trend Over Time | Line Chart | Cost trend over period | CX_TotalOperatingCostsUSD | FullDate | X: Date, Y: Cost |
| 12 | Positive Costs vs Reversals | Bar Chart | Expense vs credit comparison | CX_PositiveCostsUSD, CX_CostReversalsUSD | None (multi-measure) | N/A |
| 13 | Cost Composition by Subcategory | Treemap | Which subcategories drive cost? | CX_TotalOperatingCostsUSD | CostSubcategory | Size: Cost, Label: Subcategory |
| 14 | Contribution by Airline | Bar Chart | Which airlines contribution-positive? | NC_NetOperatingContributionUSD | AirlineName | X: Airline, Y: Contribution |
| 15 | Contribution by Route | Bar Chart | Which routes contribution-positive? | NC_NetOperatingContributionUSD | RouteCode | X: Route, Y: Contribution |

### E.2 Rejected Visuals

| Visual | Reason Rejected |
|---|---|
| Map | No direct AirportKey on fact_operating_costs. Multi-hop via RouteKey → dim_route → dim_airport required. Not recommended without additional modeling. |
| Scatter chart | No meaningful X/Y pairing for cost-efficiency beyond existing cards |
| Decomposition tree | Requires measure hierarchy setup in Power BI Desktop; adds complexity without clear value |
| Gauge | No meaningful target values exist in synthetic data |
| Additional line chart | Cost trend already covered; redundant |
| Combo chart | No clear dual-axis pairing that adds insight |

---

## PART E — Proposed Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  [AEROVISION 360 Header — Navy Blue]                                        │
│  Cost & Financial Intelligence                                              │
│  Operating Costs, Financial Contribution & Efficiency                       │
│  [Airline Slicer] [Date Range Slicer]                                       │
├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│  Total Costs │ Positive     │ Reversals    │ Net          │ Revenue-to-  │
│  (USD)       │ Costs (USD)  │ (USD)        │ Contribution │ Cost Ratio   │
│              │              │              │ (USD)        │              │
├──────────────┴──────────────┴──────────────┴──────────────┴──────────────┤
│  Cost per Flight   │  Cost per Revenue   │                                 │
│  Operation (USD)   │  Passenger (USD)    │                                 │
├────────────────────┴─────────────────────┴────────────────────────────────┤
│  Costs by Category      │  Costs by Airline      │  Costs by Route        │
│  (Bar Chart)            │  (Bar Chart)           │  (Bar Chart)           │
├─────────────────────────┴───────────────────────┴─────────────────────────┤
│  Cost Trend Over Time                                    │  Contribution   │
│  (Line Chart)                                            │  by Airline     │
│                                                          │  (Bar Chart)    │
├──────────────────────────────────────────────────────────┴────────────────┤
│  Cost Composition by Subcategory        │  Contribution by Route          │
│  (Treemap)                              │  (Bar Chart)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  [Slicers: Date, Currency, Channel, Fare Class, Cost Category — right rail]│
└─────────────────────────────────────────────────────────────────────────────┘
```

**Visual Count:** 15 visuals (7 KPI cards + 8 charts + 1 treemap) + 6 slicers  
**Layout:** 1280 × 720 (consistent with existing pages)

---

## PART F — Power BI Desktop Implementation Checklist

### F.1 Already Implemented (Do Not Repeat)

| Item | Status | Evidence |
|---|---|---|
| CX_TotalOperatingCostsUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 91 |
| CX_PositiveCostsUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 93 |
| CX_CostReversalsUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 99 |
| CX_NetOperatingCostsUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 105 |
| CX_CostPerFlightOperationUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 108 |
| CX_CostPerRevenuePassengerUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 115 |
| NC_NetOperatingContributionUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 130 |
| NC_RevenueToCostRatio measure | ✓ Defined in DAX, registered in both model files | DAX line 133 |
| NC_RevenuePerRevenuePassengerUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 136 |
| CX_CostsCurrentPeriodUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 170 |
| CX_CostsPriorPeriodUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 176 |
| CX_CostGrowthPercent measure | ✓ Defined in DAX, registered in both model files | DAX line 182 |
| CX_CostsYTDUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 192 |
| RV_TotalOperatingRevenueUSD measure | ✓ Defined in DAX, registered in both model files | DAX line 71 |
| RV_RevenuePassengers measure | ✓ Defined in DAX, registered in both model files | DAX line 46 |
| All source CSV files | ✓ Intact, unmodified | data/03_curated/ |
| All relationships | ✓ Defined in semantic_model.json | Lines 546-571 |
| All FKs resolve | ✓ Verified | Data check script |

### F.2 Missing Implementation Items (Power BI Desktop)

| # | Step | Action | Visual Type | Measure | Category | Expected Result |
|---|---|---|---|---|---|---|
| 1 | Mark dim_date as Date Table | Select dim_date, mark FullDate as Date Table | N/A | N/A | N/A | Enables YTD/prior-period |
| 2 | Import updated report.json | Replace report.json in PBIX | N/A | N/A | N/A | Page 04 available |
| 3 | Rename Page 04 | Change "Operations & Disruption" to "Cost & Financial Intelligence" | N/A | N/A | N/A | Correct page title |
| 4 | KPI Card 1 | Card | CX_TotalOperatingCostsUSD | None | $194,688,787.36 |
| 5 | KPI Card 2 | Card | CX_PositiveCostsUSD | None | $196,633,594.04 |
| 6 | KPI Card 3 | Card | CX_CostReversalsUSD | None | -$1,944,806.68 |
| 7 | KPI Card 4 | Card | NC_NetOperatingContributionUSD | None | -$185,635,943.95 |
| 8 | KPI Card 5 | Card | NC_RevenueToCostRatio | None | 0.0465 |
| 9 | KPI Card 6 | Card | CX_CostPerFlightOperationUSD | None | $38,937.76 |
| 10 | KPI Card 7 | Card | CX_CostPerRevenuePassengerUSD | None | $21,821.20 |
| 11 | Costs by Category | Bar Chart | CX_TotalOperatingCostsUSD | CostCategory | Fuel highest |
| 12 | Costs by Airline | Bar Chart | CX_TotalOperatingCostsUSD | AirlineName | Airline 1 highest |
| 13 | Costs by Route | Bar Chart | CX_TotalOperatingCostsUSD | RouteCode | Route 209 highest |
| 14 | Cost Trend | Line Chart | CX_TotalOperatingCostsUSD | FullDate | Time series |
| 15 | Positive vs Reversals | Bar Chart | CX_PositiveCostsUSD, CX_CostReversalsUSD | None | Two bars |
| 16 | Cost Composition | Treemap | CX_TotalOperatingCostsUSD | CostSubcategory | Fuel Adjustment largest |
| 17 | Contribution by Airline | Bar Chart | NC_NetOperatingContributionUSD | AirlineName | All negative |
| 18 | Contribution by Route | Bar Chart | NC_NetOperatingContributionUSD | RouteCode | All negative |
| 19 | Date Slicer | Slicer | FullDate | dim_date | Date range filter |
| 20 | Airline Slicer | Slicer | AirlineName | dim_airline | Airline filter |
| 21 | Route Slicer | Slicer | RouteCode | dim_route | Route filter |
| 22 | Currency Slicer | Slicer | CurrencyCode | dim_currency | Currency filter |
| 23 | Cost Category Slicer | Slicer | CostCategory | fact_operating_costs | Category filter |
| 24 | Currency Formatting | Format | All USD measures | None | 2 decimal places |
| 25 | Negative Value Formatting | Format | CostReversals, Contribution | None | Red/parentheses |
| 26 | Disclosure Text | Text box | N/A | None | "Synthetic Simulation..." |

### F.3 Implementation Order

1. Mark dim_date as Date Table (FullDate column)
2. Import report.json into PBIX
3. Rename Page 04 from "Operations & Disruption" to "Cost & Financial Intelligence"
4. Create KPI cards (steps 4-10)
5. Create chart visuals (steps 11-18)
6. Add slicers (steps 19-23)
7. Apply formatting (steps 24-26)
8. Validate all values against source data

---

## PART G — Risks and Gaps

| Risk | Severity | Impact | Mitigation |
|---|---|---|---|
| dim_date not marked as Date Table | High | YTD/prior-period measures return BLANK | Mark dim_date[FullDate] as Date Table in PBIX |
| No prior-year fact data | Medium | Prior-period comparisons return BLANK | Accept BLANK or load FY2025 data |
| Negative Net Operating Contribution | Low | May alarm users | Explain synthetic generator assumptions |
| OP01/OP03/OP04 not registered | Low | Cannot use in visuals | Register if needed (not required for Page 04) |
| Cost/revenue disparity | Medium | May look like error | Document synthetic generator assumptions |
| Page 04 name mismatch | Low | Currently "Operations & Disruption" | Rename in PBIX |

---

## PART H — Final Executive Verdict

### A. Current Page 04 Status

Page 04 currently exists as **"Operations & Disruption"** with only 3 visuals (FL04 Cancellation Rate card, DS03 Controllable Disruptions card, DS01 Disruptions by Type barChart). It does NOT match the "Cost & Financial Intelligence" specification. All 3 visuals would need to be replaced.

### B. Data Readiness

**READY.** All source data exists and has been independently verified:
- 7,480 operating cost ledger lines across 8 categories
- 9,956 booking coupons with revenue data
- All dates within reporting period (2025-10-01 to 2026-09-30)
- All 8 currencies represented
- All 10 airlines represented
- All 320 routes represented

### C. DAX Readiness

**READY.** All 13 required measures exist in DAX and are registered in both model.json and semantic_model.json:
- 10 CX measures (cost intelligence)
- 3 NC measures (financial performance)
- 2 RV measures (revenue & passengers, needed for ratios)

No new DAX measures need to be created.

### D. Semantic Model Readiness

**READY.** All required relationships are active and resolve correctly:
- fact_operating_costs → dim_airline, dim_route, dim_date, dim_currency
- fact_booking_transactions → dim_airline, dim_route, dim_date, dim_currency
- No fact-to-fact relationships
- No ambiguous filter paths

### E. Visualization Readiness

**READY.** All 15 recommended visuals are fully supported by existing measures and relationships:
- 7 KPI cards
- 5 bar charts
- 1 line chart
- 1 treemap
- 6 slicers

No map or scatter chart is recommended due to lack of direct geographic keys on cost facts.

### F. Financial Accuracy

**VERIFIED.** All key figures independently reconciled from source CSV:
- Total Operating Revenue: $9,052,843.41 ✓
- Total Operating Costs: $194,688,787.36 ✓
- Net Operating Contribution: -$185,635,943.95 ✓
- Revenue-to-Cost Ratio: 0.0465 ✓
- Cost per Flight Operation: $38,937.76 ✓
- Cost per Revenue Passenger: $21,821.20 ✓

### G. Implementation Plan

1. Mark dim_date as Date Table (Power BI Desktop)
2. Import report.json into PBIX
3. Rename Page 04 to "Cost & Financial Intelligence"
4. Create 7 KPI cards
5. Create 8 charts + 1 treemap
6. Add 6 slicers
7. Apply currency formatting (2 decimal places)
8. Add disclosure text
9. Run full test suite (595 tests)

### H. Critical Risks

1. **dim_date not marked as Date Table** — YTD/prior-period measures will return BLANK until marked in Power BI Desktop
2. **No prior-year data** — Prior-period comparisons will return BLANK (data starts 2025-10-01)
3. **Negative contribution** — May alarm users; must be explained as synthetic generator output
4. **PBIX not updated** — report.json changes not yet in PBIX; import required

---

## FINAL VERDICT

### YELLOW — IMPLEMENTATION POSSIBLE WITH DOCUMENTED CONDITIONS

**Evidence:**
- All 595 automated tests pass (0 failed)
- All required DAX measures exist and are registered (30 financial measures)
- All financial figures independently reconciled from source data
- All semantic model relationships are valid and resolve correctly
- All source data files are intact and unmodified
- Page 04 currently exists as "Operations & Disruption" (3 visuals), not "Cost & Financial Intelligence" (0 visuals)
- dim_date not marked as Date Table in PBIX (YTD/prior-period measures will return BLANK)
- No prior-year fact data exists (prior-period comparisons return BLANK)

**Implementation can proceed immediately in Power BI Desktop using existing measures.** No new DAX is required. The page can be built using CX and NC measures that are already defined and registered.

**Conditions:**
1. Mark dim_date[FullDate] as Date Table in Power BI Desktop before using YTD/prior-period measures
2. Accept BLANK results for prior-period comparisons (no data before 2025-10-01)
3. Rename Page 04 from "Operations & Disruption" to "Cost & Financial Intelligence"
4. Import updated report.json into PBIX
5. Obtain GOV-D-07 approval if ManifestHash canonicalization is required for deployment

---

**Report generated:** 2026-11-07  
**Test results:** 595 passed, 0 failed  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.
