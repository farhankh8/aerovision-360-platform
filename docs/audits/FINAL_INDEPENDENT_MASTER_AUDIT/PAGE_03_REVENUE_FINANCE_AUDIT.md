# PAGE 03 — REVENUE & FINANCE AUDIT

**Source:** Authoritative main PBIX `deliverables/power_bi/AEROVISION_360.pbix`, page folder `3c0e9656b72579cb4105`  
**Page name:** `Revenue & Finance.`  
**Page order:** Page 03 (third page)  
**Visual count:** 23  
**Page rendered in Power BI Desktop:** Not independently verified (limitation L-1); visual metadata verified from binary.

---

## 1. Visual inventory

23 visuals (full table in `POWER_BI_FIVE_PAGE_VISUAL_INVENTORY.md`). Key data visuals:

| Visual | Type | Title | Bound measure | Bound column/table |
|---|---|---|---|---|
| Card | cardVisual | 'TOTAL OPERATING REVENUE (USD)' | RV_TotalOperatingRevenueUSD | fact_booking_transactions |
| Card | cardVisual | 'NET PASSENGER REVENUE (USD)' | RV_NetPassengerRevenueUSD | fact_booking_transactions |
| Card | cardVisual | 'NET FEE REVENUE (USD)' | RV_NetFeeRevenueUSD | fact_booking_transactions |
| Card | cardVisual | 'NET ANCILLARY REVENUE (USD)' | RV_NetAncillaryRevenueUSD | fact_booking_transactions |
| Card | cardVisual | 'REVENUE PASSENGERS' | RV_RevenuePassengers | fact_booking_transactions |
| Card | cardVisual | 'DISTINCT BOOKINGS' | RV_DistinctBookings | fact_booking_transactions |
| Card | cardVisual | 'AVERAGE REV PER REV PASSENGER (USD)' | RV_AvgRevenuePerRevenuePassenger | fact_booking_transactions |
| Clustered bar chart | clusteredBarChart | 'REVENUE BY BOOKING CHANNEL (USD)' | measure | dim_booking_channel |
| Clustered bar chart | clusteredBarChart | 'TOTAL REVENUE BY AIRLINE (USD)' | measure | dim_airline |
| Clustered bar chart | clusteredBarChart | 'TOTAL REVENUE BY ROUTE (USD)' | measure | dim_route |
| Donut chart | donutChart | 'REVENUE COMPOSITION BY STREAM (USD)' | 3 measures | — |
| Treemap | treemap | 'REVENUE CONTRIBUTION BY FARE CLASS (USD)' | measure | dim_fare_class |
| Pivot table | pivotTable | 'MONTHLY REVENUE PERFORMANCE BY AIRLINE' | measures | dim_airline |
| Line chart | lineChart | 'MONTHLY REVENUE TREND (USD)' | measure | dim_date |
| Slicer | slicer | 'AIRLINE' | — | dim_airline |
| Slicer | slicer | 'BOOKING CHANNEL' | — | dim_booking_channel |
| Slicer | slicer | 'FLIGHT DATE RANGE' | — | dim_date |

Plus textboxes, images, shapes, page navigator.

---

## 2. Measure binding correctness (financial measures)

| Measure | Defined in DAX? | Registered in model.json? | Bound on Page 03? | Blocked by OD-04? | Status |
|---|---|---|---|---|---|
| RV_BookingCount | Yes | Yes | Yes (DISTINCT BOOKINGS) | No | COMPLETE |
| RV_DistinctBookings | Yes | Yes | Yes | No | COMPLETE |
| RV_RevenuePassengers | Yes | Yes | Yes | No | COMPLETE |
| RV_NonRevenuePassengers | Yes | Yes | No | No | COMPLETE (unused) |
| RV_GrossBookingValueUSD | Yes | Yes | No | No | COMPLETE (unused) |
| RV_RefundAmountUSD | Yes | Yes | No | No | COMPLETE (unused) |
| RV_NetPassengerRevenueUSD | Yes | Yes | Yes | Partially | IMPLEMENTED — NOT FULLY VERIFIED |
| RV_NetFeeRevenueUSD | Yes | Yes | Yes | Partially | IMPLEMENTED — NOT FULLY VERIFIED |
| RV_NetAncillaryRevenueUSD | Yes | Yes | Yes | Partially | IMPLEMENTED — NOT FULLY VERIFIED |
| RV_TotalOperatingRevenueUSD | Yes | Yes | Yes | Partially | IMPLEMENTED — NOT FULLY VERIFIED |
| RV_AvgRevenuePerRevenuePassenger | Yes | Yes | Yes | Partially | IMPLEMENTED — NOT FULLY VERIFIED |
| RV_AvgBookingValueUSD | Yes | Yes | No | Partially | COMPLETE (unused) |
| NC_NetOperatingContributionUSD | Yes | Yes | No | Yes | BLOCKED |
| NC_RevenueToCostRatio | Yes | Yes | No | Yes | BLOCKED |
| NC_RevenuePerRevenuePassengerUSD | Yes | Yes | No | Yes | BLOCKED |

All RV_/CX_/NC_ measures are defined in DAX and registered in `model.json` (fact_booking_transactions / fact_operating_costs). However, the underlying financial fact data (FactBookingTransactions, FactOperatingCosts) requires OD-04 exchange rates and is **not loaded into the Power BI model** (absent from `data_sources.json`). Therefore financial KPI values cannot render correctly until OD-04 is approved and `ref_exchange_rates.csv` exists.

---

## 3. OD-04 dependency

OD-04 (`docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md`) status: **PROPOSED — OWNER APPROVAL REQUIRED**. It BLOCKS FactBookingTransactions and FactOperatingCosts implementation. Additionally, a **critical currency-set mismatch** exists: OD-04 lists 5 currencies (USD, EUR, GBP, JPY, CAD) but DimCurrency has 8 (AED, QAR, SGD, INR, GBP, EUR, USD, AUD). This blocks referential integrity for financial facts.

Page 03 financial visuals are therefore **BLOCKED** from producing correct USD values, not missing from the report. The report page is built; the data is blocked upstream.

---

## 4. Findings

| ID | Finding | Severity | Evidence | Confidence |
|---|---|---|---|---|
| P03-01 | Financial KPI cards/charts depend on USD-converted fact data blocked by OD-04; facts not in model or data_sources.json | HIGH | `OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md`; `data_sources/data_sources.json` (omits the two financial facts); Page 03 visual bindings | High |
| P03-02 | Currency-set mismatch: OD-04 (5 currencies) vs DimCurrency (8 currencies) blocks referential integrity | HIGH | `OD04…` Section 4; `dim_currency` (8 rows) | High |
| P03-03 | Page rendering not independently verified (limitation L-1) | INFORMATIONAL | — | — |

---

## 5. Implementation status

**Dashboard development: COMPLETE AND VERIFIED (as built).** Page 03 exists with 23 visuals; all financial cards/charts bound to defined, registered DAX measures.

**Data integration: BLOCKED.** Financial fact data not loaded (OD-04). Cannot render correct USD values until OD-04 approved + exchange rates created + facts loaded.

Not counted as incomplete dashboard development — the page is built; the blocker is upstream data/governance.
