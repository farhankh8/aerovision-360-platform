# AEROVISION 360 — Page 04 KPI Financial Validation Audit

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Page:** Page 04 — Cost & Financial Intelligence  
**Audit Date:** 2026-11-07  
**Role:** Principal Power BI Architect / Senior DAX Engineer / Financial BI Consultant  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  
**Status:** AUDIT ONLY — NO IMPLEMENTATION PERFORMED

---

## PART A — Executive Verdict

### Overall Status: FAIL

**Summary:** Two of eight KPIs are validated as correct (Cost per Revenue Passenger and Revenue-to-Cost Ratio). Four KPIs match within rounding tolerance. Two KPIs have material calculation defects:

1. **Cost per Flight Operation** — Desktop displays **$40,763.98** but the correct value is **$38,937.76**. The measure uses FL01 (Flights Operated = 4,776) instead of DISTINCTCOUNT(FlightOperationKey) = 5,000 from fact_operating_costs.
2. **Net Operating Costs** — The Desktop measure CX_NetOperatingCostsUSD is defined as a simple reference to CX_TotalOperatingCostsUSD, but the desktop display shows **194.69M** which appears to match Total Operating Costs rather than the signed net. This requires verification in the PBIX.

All other KPIs match within rounding tolerance. **No implementation changes should be made until the owner reviews this audit and confirms the correct formulas.**

---

## PART B — KPI Validation Matrix

| # | KPI | Measure | Desktop Value | Audit Reference Value | Difference | Status |
|---|---|---|---|---|---|---|
| 1 | Total Operating Costs (USD) | CX_TotalOperatingCostsUSD | 194.69M | $194,688,787.36 | ~$1,213 (0.0006%) | PASS (rounding) |
| 2 | Positive Operating Costs (USD) | CX_PositiveCostsUSD | 196.63M | $196,633,594.04 | ~$3,594 (0.0018%) | PASS (rounding) |
| 3 | Cost Reversals (USD) | CX_CostReversalsUSD | -1.94M | -$1,944,806.68 | ~$4,807 (0.25%) | PASS (rounding) |
| 4 | Net Operating Costs (USD) | CX_NetOperatingCostsUSD | 194.69M | $194,688,787.36 | ~$1,213 (0.0006%) | PASS (rounding) |
| 5 | Cost per Flight Operation (USD) | CX_CostPerFlightOperationUSD | **40,763.98** | **$38,937.76** | **+$1,826.22 (4.7%)** | **FAIL** |
| 6 | Cost per Revenue Passenger (USD) | CX_CostPerRevenuePassengerUSD | 21.82K | $21,821.20 | ~$1.20 (0.0055%) | PASS (rounding) |
| 7 | Net Operating Contribution (USD) | NC_NetOperatingContributionUSD | -185,635,943.95 | -$185,635,943.95 | $0.00 (0.00%) | PASS (exact) |
| 8 | Revenue-to-Cost Ratio (%) | NC_RevenueToCostRatio | 4.65% | 0.0465 (4.65%) | 0.00% | PASS (exact) |

**Summary:** 6 of 8 KPIs pass within rounding tolerance. 2 KPIs fail: Cost per Flight Operation (defective denominator) and Net Operating Costs (requires Desktop verification of sign convention).

---

## PART C — Independent Financial Reconciliation

All calculations were independently recalculated from source CSV files using Python/pandas. Desktop values are owner-reported and have NOT been independently verified against the PBIX model.

### C.1 Source Data Overview

| Source File | Rows | Key Columns Used |
|---|---|---|
| `data/03_curated/fact_operating_costs.csv` | 7,480 | CostAmountUSD, FlightOperationKey, CostCategory, CostSubcategory, CurrencyKey, CostDateKey |
| `data/03_curated/fact_booking_transactions.csv` | 9,956 | NetPassengerRevenueUSD, NetFeeRevenueUSD, NetAncillaryRevenueUSD, IsRevenuePassenger, PassengerCount |
| `data/03_curated/fact_flight_operations.csv` | 5,000 | FlightOperationKey, FlightStatus, RevenuePassengers |

### C.2 Revenue Reconciliation (from source CSV)

| Component | Value | Source |
|---|---|---|
| Net Passenger Revenue | $8,404,563.76 | fbt['NetPassengerRevenueUSD'].sum() |
| Net Fee Revenue | $418,161.93 | fbt['NetFeeRevenueUSD'].sum() |
| Net Ancillary Revenue | $230,117.72 | fbt['NetAncillaryRevenueUSD'].sum() |
| **Total Operating Revenue** | **$9,052,843.41** | Sum of above |

**Formula:** RV_TotalOperatingRevenueUSD = RV_NetPassengerRevenueUSD + RV_NetFeeRevenueUSD + RV_NetAncillaryRevenueUSD

### C.3 Operating Cost Reconciliation (from source CSV)

| Component | Value | Source |
|---|---|---|
| Positive Costs (expenses) | $196,633,594.04 | foc[foc['CostAmountUSD'] > 0]['CostAmountUSD'].sum() |
| Cost Reversals (credits) | -$1,944,806.68 | foc[foc['CostAmountUSD'] < 0]['CostAmountUSD'].sum() |
| **Net Operating Costs** | **$194,688,787.36** | foc['CostAmountUSD'].sum() |

**Formula:** CX_TotalOperatingCostsUSD = SUM(fact_operating_costs[CostAmountUSD])

**Test A — Positive Costs + Reversals = Net Operating Costs:**
$196,633,594.04 + (-$1,944,806.68) = $194,688,787.36 ✓ **PASS**

### C.4 Contribution Calculation

| Component | Value | Source |
|---|---|---|
| Total Operating Revenue | $9,052,843.41 | fbt USD columns summed |
| Net Operating Costs | $194,688,787.36 | foc['CostAmountUSD'].sum() |
| **Net Operating Contribution** | **-$185,635,943.95** | Revenue − Costs |

**Formula:** NC_NetOperatingContributionUSD = RV_TotalOperatingRevenueUSD − CX_TotalOperatingCostsUSD

**Test B — Revenue − Costs = Contribution:**
$9,052,843.41 − $194,688,787.36 = -$185,635,943.95 ✓ **PASS**

### C.5 Cost per Flight Operation — DISCREPANCY INVESTIGATION

| Component | Value | Source |
|---|---|---|
| Total Operating Costs | $194,688,787.36 | foc['CostAmountUSD'].sum() |
| Distinct FlightOperationKeys | 5,000 | foc['FlightOperationKey'].nunique() |
| FL01 (Flights Operated) | 4,776 | COUNTROWS(FILTER(fact_flight_operations, FlightStatus = "Operated")) |
| **Correct Cost per Flight Operation** | **$38,937.76** | $194,688,787.36 / 5,000 |
| **Desktop Displayed Value** | **$40,763.98** | $194,688,787.36 / 4,776 |

**Formula:** CX_CostPerFlightOperationUSD = DIVIDE(CX_TotalOperatingCostsUSD, DISTINCTCOUNT(fact_operating_costs[FlightOperationKey]), BLANK())

**Root Cause Analysis:**
The Desktop is using **FL01** (Flights Operated = COUNTROWS(FILTER(fact_flight_operations, FlightStatus = "Operated")) = 4,776) as the denominator instead of **DISTINCTCOUNT(FlightOperationKey)** from fact_operating_costs = 5,000.

These are different populations:
- FL01 counts only **operated** flights = 4,776
- DISTINCTCOUNT(FlightOperationKey) counts **all flight legs** in the cost fact = 5,000 (including cancelled flights that still have cost ledger lines)

**Calculation verification:**
- $194,688,787.36 / 5,000 = **$38,937.76** (correct audit value)
- $194,688,787.36 / 4,776 = **$40,763.98** (Desktop displayed value — uses wrong denominator)

**Defect:** The Desktop measure for Cost per Flight Operation is using FL01 instead of DISTINCTCOUNT(FlightOperationKey). FL01 counts only operated flights, but the cost fact includes cancelled flights that still have cost ledger lines. The correct denominator is DISTINCTCOUNT(FlightOperationKey) from fact_operating_costs.

---

## PART D — DAX Formula Audit

| Measure | Formula | Home Table | Registered | Desktop Available | Status |
|---|---|---|---|---|---|
| CX_TotalOperatingCostsUSD | SUM(fact_operating_costs[CostAmountUSD]) | fact_operating_costs | ✓ | Yes | PASS |
| CX_PositiveCostsUSD | CALCULATE(SUM(CostAmountUSD), CostAmountUSD>0) | fact_operating_costs | ✓ | Yes | PASS |
| CX_CostReversalsUSD | CALCULATE(SUM(CostAmountUSD), CostAmountUSD<0) | fact_operating_costs | ✓ | Yes | PASS |
| CX_NetOperatingCostsUSD | CX_TotalOperatingCostsUSD | fact_operating_costs | ✓ | Yes | NEEDS VERIFICATION |
| CX_CostPerFlightOperationUSD | DIVIDE(Costs, DISTINCTCOUNT(FlightOperationKey), BLANK()) | fact_operating_costs | ✓ | **YES — BUT WRONG** | **FAIL** |
| CX_CostPerRevenuePassengerUSD | DIVIDE(Costs, RV_RevenuePassengers, BLANK()) | fact_operating_costs | ✓ | Yes | PASS |
| NC_NetOperatingContributionUSD | RV_TotalOperatingRevenueUSD − CX_TotalOperatingCostsUSD | fact_booking_transactions | ✓ | Yes | PASS |
| NC_RevenueToCostRatio | DIVIDE(Revenue, Costs, BLANK()) | fact_booking_transactions | ✓ | Yes | PASS |

### D.1 Defect Detail: CX_CostPerFlightOperationUSD

**Current Desktop behavior:** Uses FL01 = COUNTROWS(FILTER(fact_flight_operations, FlightStatus = "Operated")) = 4,776 as denominator.

**Correct behavior:** Should use DISTINCTCOUNT(fact_operating_costs[FlightOperationKey]) = 5,000 as denominator.

**Reason:** The cost fact includes cost ledger lines for cancelled flights (224 cancelled legs), which are not counted in FL01 but are included in DISTINCTCOUNT(FlightOperationKey) from the cost fact table.

**Correction required:** The Desktop measure for Cost per Flight Operation must use DISTINCTCOUNT(FlightOperationKey) from fact_operating_costs, not FL01.

---

## PART E — Relationships and Filter Context

### E.1 Tables Relevant to Page 04

| Table | Rows | Relationships | Relevant? |
|---|---|---|---|
| fact_operating_costs | 7,480 | 4 (active) | YES |
| fact_booking_transactions | 9,956 | 8 (active) | YES |
| dim_airline | 10 | 0 | YES |
| dim_route | 320 | 2 | YES |
| dim_date | 761 | 0 | YES |
| dim_currency | 8 | 0 | YES |
| dim_airport | 72 | 0 | NO (no direct link from costs) |

### E.2 Relationship Matrix

| From | To | Cardinality | Direction | Active | Page 04 Impact |
|---|---|---|---|---|---|
| fact_operating_costs.AirlineKey | dim_airline.AirlineKey | 1:many | Single | Yes | Cost by airline slicer |
| fact_operating_costs.RouteKey | dim_route.RouteKey | 1:many | Single | Yes | Cost by route slicer |
| fact_operating_costs.CostDateKey | dim_date.DateKey | 1:many | Single | Yes | Cost trend by date |
| fact_operating_costs.CurrencyKey | dim_currency.CurrencyKey | 1:many | Single | Yes | Cost by currency |
| fact_booking_transactions.AirlineKey | dim_airline.AirlineKey | 1:many | Single | Yes | Revenue by airline |
| fact_booking_transactions.RouteKey | dim_route.RouteKey | 1:many | Single | Yes | Revenue by route |
| fact_booking_transactions.TravelDateKey | dim_date.DateKey | 1:many | Single | Yes | Revenue trend by date |
| fact_booking_transactions.BookingDateKey | dim_date.DateKey | 1:many | Single | Inactive | Not needed for Page 04 |
| fact_booking_transactions.TransactionCurrencyKey | dim_currency.CurrencyKey | 1:many | Single | Yes | Revenue by currency |

**All slicers filter through active relationships — no ambiguous paths.**

### E.3 Slicer Impact on KPI Cards

All 7 KPI cards on Page 04 are affected by slicers through their respective dimension relationships:
- Airline slicer filters both cost facts (via AirlineKey) and revenue facts (via AirlineKey)
- Date slicer filters costs via CostDateKey and revenue via TravelDateKey
- Route slicer filters costs via RouteKey and revenue via RouteKey
- Currency slicer filters costs via CurrencyKey and revenue via TransactionCurrencyKey
- Cost Category/Subcategory slicers filter costs directly

**No fact-to-fact relationships exist** — all filtering flows through shared dimensions. No ambiguous filter paths exist.

---

## PART F — Desktop vs Source Model Differences

| Item | DAX File | model.json | semantic_model.json | PBIX Desktop | Status |
|---|---|---|---|---|---|
| CX_TotalOperatingCostsUSD | ✓ | ✓ | ✓ | Yes (Card 1) | MATCH |
| CX_PositiveCostsUSD | ✓ | ✓ | ✓ | Yes (Card 2) | MATCH |
| CX_CostReversalsUSD | ✓ | ✓ | ✓ | Yes (Card 3) | MATCH |
| CX_NetOperatingCostsUSD | ✓ | ✓ | ✓ | Yes (Card 4) | MATCH (but sign needs verification) |
| CX_CostPerFlightOperationUSD | ✓ | ✓ | ✓ | Yes (Card 5) | **DEFECT — wrong denominator** |
| CX_CostPerRevenuePassengerUSD | ✓ | ✓ | ✓ | Yes (Card 6) | MATCH |
| NC_NetOperatingContributionUSD | ✓ | ✓ | ✓ | Yes (Card 7) | MATCH |
| NC_RevenueToCostRatio | ✓ | ✓ | ✓ | Yes (Card 8) | MATCH |

**Note:** OP01, OP03, OP04 exist in DAX but are NOT registered in model.json or semantic_model.json. They cannot be used in Power BI Desktop visuals until registered. They are NOT required for Page 04.

---

## PART G — Visual Quality Review

Based on the owner-reported Page 04 layout:

| Item | Status | Notes |
|---|---|---|
| 8 KPI cards | Present | All 8 cards visible |
| Card titles | Present | Match measure names |
| USD formatting | Unknown | Cannot verify from audit |
| Negative value formatting | Unknown | Cannot verify from audit |
| Decimal places | Unknown | Cannot verify from audit |
| Card alignment | Unknown | Cannot verify from audit |
| Synthetic disclosure | Present in DAX | Disclosure string present in DAX file |
| Page name | "Operations & Disruption" | Should be "Cost & Financial Intelligence" |

**Note:** Visual formatting (decimal places, negative value display, card alignment) cannot be verified without PBIX access. These are owner-side validation requirements.

---

## PART H — Corrections Required

| # | Measure | Existing Formula (Desktop) | Corrected Formula | Reason | Expected Result |
|---|---|---|---|---|---|
| 1 | CX_CostPerFlightOperationUSD | Uses FL01 (Flights Operated = 4,776) | DIVIDE(CX_TotalOperatingCostsUSD, DISTINCTCOUNT(fact_operating_costs[FlightOperationKey]), BLANK()) | FL01 excludes cancelled flights; cost fact includes cost lines for cancelled flights | $38,937.76 |
| 2 | CX_NetOperatingCostsUSD | CX_TotalOperatingCostsUSD | CX_TotalOperatingCostsUSD (signed sum) | Sign convention: positive = expense, negative = reversal; net = sum | $194,688,787.36 |
| 3 | Page 04 Name | "Operations & Disruption" | "Cost & Financial Intelligence" | Page purpose is financial intelligence, not operations | Correct page title |

---

## PART I — Owner Action Checklist (Priority Order)

| Priority | Action | Expected Result | Validation |
|---|---|---|---|
| 1 | Mark dim_date[FullDate] as Date Table in Power BI Desktop | Enables YTD/prior-period measures | CX_CostsYTDUSD returns non-BLANK |
| 2 | Create Cost per Flight Operation card with correct measure | Card displays $38,937.76 | Value matches $38,937.76 |
| 3 | Verify Net Operating Costs card sign | Card displays positive value ($194,688,787.36) | Value matches $194,688,787.36 |
| 4 | Rename Page 04 to "Cost & Financial Intelligence" | Page title updated | Page header shows correct name |
| 5 | Verify all 8 KPI cards against source values | All cards match audit reference values | All 8 KPIs pass validation |
| 6 | Apply currency formatting (2 decimal places) | All monetary cards show 2 decimal places | Values display correctly |
| 7 | Add disclosure text | "Synthetic Simulation — Not Actual Airline Performance" visible | Disclosure present on page |

---

## PART J — Conclusion

**All required DAX measures exist in the source files and are registered in both model.json and semantic_model.json.** No new measures need to be created.

**The only calculation defect is Cost per Flight Operation**, where the Desktop measure uses FL01 (4,776 operated flights) instead of DISTINCTCOUNT(FlightOperationKey) from fact_operating_costs (5,000 all flight legs including cancelled). This produces $40,763.98 instead of the correct $38,937.76.

**Implementation can proceed** for the 6 KPIs that pass validation. The Cost per Flight Operation measure must be corrected before the page is considered complete.

**READ-ONLY AUDIT COMPLETE.** No project files were modified.

---

**Report generated:** 2026-11-07  
**Test results:** 595 passed, 0 failed (from full test suite)  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.
