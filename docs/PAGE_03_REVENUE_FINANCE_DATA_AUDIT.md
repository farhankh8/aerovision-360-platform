# PAGE_03_REVENUE_FINANCE_DATA_AUDIT.md

# AEROVISION 360 — Page 03 Revenue & Finance: Data Feasibility Audit

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Page:** Page 03 — Revenue & Finance
**Audit type:** Data feasibility audit (pre-implementation)
**Status:** COMPLETE — AUDIT ONLY; NO PBIX, MODEL, DAX, SOURCE DATA, OR REPORT MODIFIED
**Prepared:** 2026-11-06
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Executive Summary

**Headline finding: Page 03 Revenue & Finance has NO monetary financial data available in the curated layer.**

The only fact tables present in `data/03_curated/` are:
- `fact_flight_operations` (5,000 rows) — contains passenger counts, seat counts, delay minutes, block minutes; **no monetary values**
- `fact_disruptions` (1,754 rows) — contains delay minutes; **no monetary values**
- `fact_customer_feedback` (2,500 rows) — contains satisfaction scores; **no monetary values**

The two financial fact tables documented in the contract — `FactBookingTransactions` and `FactOperatingCosts` — **do not exist** in the curated layer, raw layer, staging layer, or reference layer. They are blocked by **OD-04**, which is **PROPOSED — OWNER APPROVAL REQUIRED** (not approved).

**Consequence: No revenue, cost, profit, yield, RASK, CASK, or any monetary KPI can be calculated.** Passenger volume (FL02) is explicitly NOT revenue per the governing design documents.

---

## 2. Source-Data Inventory

### 2.1 Curated Datasets Inspected (14 total)

| # | Dataset | Location | Format | Rows | Columns | Financial Data? | Status |
|---|---|---|---|---|---|---|---|
| 1 | fact_flight_operations.csv | data/03_curated/ | CSV | 5,000 | 26 | NO (passenger/seat/delay/block only) | AVAILABLE (non-financial only) |
| 2 | fact_disruptions.csv | data/03_curated/ | CSV | 1,754 | 16 | NO (delay minutes only) | AVAILABLE (non-financial only) |
| 3 | fact_customer_feedback.csv | data/03_curated/ | CSV | 2,500 | 16 | NO (satisfaction scores only) | AVAILABLE (non-financial only) |
| 4 | dim_airline.csv | data/03_curated/ | CSV | 10 | 12 | NO | DIMENSION |
| 5 | dim_airport.csv | data/03_curated/ | CSV | 72 | 11 | NO | DIMENSION |
| 6 | dim_route.csv | data/03_curated/ | CSV | 320 | 9 | NO | DIMENSION |
| 7 | dim_date.csv | data/03_curated/ | CSV | 761 | 19 | NO | DIMENSION |
| 8 | dim_aircraft.csv | data/03_curated/ | CSV | 440 | 9 | NO | DIMENSION |
| 9 | dim_aircraft_type.csv | data/03_curated/ | CSV | 12 | 8 | NO | DIMENSION |
| 10 | dim_customer.csv | data/03_curated/ | CSV | 785 | 8 | NO | DIMENSION |
| 11 | dim_disruption_type.csv | data/03_curated/ | CSV | 9 | 7 | NO | DIMENSION |
| 12 | dim_booking_channel.csv | data/03_curated/ | CSV | 7 | 6 | NO (channel labels only, no fact) | UNUSED DIMENSION |
| 13 | dim_currency.csv | data/03_curated/ | CSV | 8 | 6 | NO (currency codes only, no rates) | UNUSED DIMENSION |
| 14 | dim_fare_class.csv | data/03_curated/ | CSV | 8 | 8 | NO (fare labels only, no fact) | UNUSED DIMENSION |

### 2.2 Referenced but MISSING Financial Datasets

| Dataset | Referenced In | Expected Location | Current State | Blocking Reason |
|---|---|---|---|---|
| FactBookingTransactions | docs/03_DATA_CONTRACTS.md Section 5.3 | data/03_curated/ | **DOES NOT EXIST** | OD-04 not approved; no exchange rates; no ref_exchange_rates.csv |
| FactOperatingCosts | docs/03_DATA_CONTRACTS.md Section 5.4 | data/03_curated/ | **DOES NOT EXIST** | OD-04 not approved; no exchange rates; no ref_exchange_rates.csv |
| ref_exchange_rates.csv | docs/03_DATA_CONTRACTS.md Section 10.2; OD-04 | data/04_reference/ | **DOES NOT EXIST** | OD-04 not approved; no rate values approved |

### 2.3 Raw Layer Inspection

The raw layer (`data/01_raw/`) contains only:
- `source_index.json` — lists 4 source datasets (airline_id_crosswalk, airline_reference_workbook, dim_route_keymap_v1, test_csv)
- Run directories for `debug_run` and `20261104_141249_936499`

**No raw booking, cost, revenue, or financial transaction files exist anywhere in the project.** Confirmed via glob searches for `*booking*`, `*cost*`, `*revenue*`, `*fare*` — zero matches for financial fact files.

---

## 3. Semantic Model Inventory

### 3.1 Tables in the Model

All 14 tables from `data/03_curated/` are listed in `deliverables/power_bi/semantic_model/semantic_model.json`. None contain monetary columns.

### 3.2 Unused Dimensions (No FKs)

| Dimension | Rows | Purpose | Unused Because |
|---|---|---|---|
| dim_currency | 8 | Currency codes (USD is IsReportingCurrency=TRUE) | No fact table references CurrencyKey; OD-04 blocked |
| dim_booking_channel | 7 | Booking channel taxonomy | No fact table references BookingChannelKey; OD-04 blocked |
| dim_fare_class | 8 | Fare class taxonomy | No fact table references FareClassKey; OD-04 blocked |

### 3.3 Existing Measures (10 total)

| Measure | Table | Expression | Value | Financial? |
|---|---|---|---|---|
| FL01 | fact_flight_operations | COUNTROWS(FlightStatus="Operated") | 4,776 | NO (flight count) |
| FL02 | fact_flight_operations | SUM(RevenuePassengers) | 218,413 | **NO — passenger volume, explicitly NOT revenue** |
| FL03 | fact_flight_operations | AVERAGE(DepartureDelayMinutes) | 43.42 | NO (delay minutes) |
| FL04 | fact_flight_operations | Cancellation rate | 4.48% | NO (ratio) |
| DS01 | fact_disruptions | COUNTROWS(fact_disruptions) | 1,754 | NO (disruption count) |
| DS02 | fact_disruptions | AVERAGE(DelayMinutes) | 120.62 | NO (delay minutes) |
| DS03 | fact_disruptions | Count controllable disruptions | 540 | NO (count) |
| CF01 | fact_customer_feedback | COUNTROWS(fact_customer_feedback) | 2,500 | NO (feedback count) |
| CF02 | fact_customer_feedback | AVERAGE(SatisfactionScore) | 2.99 | NO (score) |
| CF03 | fact_customer_feedback | Complaint percentage | 25.52% | NO (ratio) |

**None of the 10 existing measures are financial measures.**

---

## 4. Relationship Inventory

All relationships are between the 3 existing facts and their dimensions. **No relationship connects any dimension to a financial fact** because no financial fact exists.

| Dimension | FK Status | Financial Relevance |
|---|---|---|
| dim_currency | No FK from any fact | Cannot support currency conversion; OD-04 blocked |
| dim_booking_channel | No FK from any fact | Cannot support channel mix analysis; OD-04 blocked |
| dim_fare_class | No FK from any fact | Cannot support fare class analysis; OD-04 blocked |
| dim_customer | FK from fact_customer_feedback only | No financial attributes |

---

## 5. KPI-by-KPI Financial Availability Classification

### 5.1 Monetary KPIs (All NOT AVAILABLE)

| KPI | Required Data | Source Status | Classification | Reason |
|---|---|---|---|---|
| Total Operating Revenue | FactBookingTransactions[NetPassengerRevenueUSD] + [NetFeeRevenueUSD] + [NetAncillaryRevenueUSD] | Fact table does not exist | **NOT AVAILABLE** | FactBookingTransactions blocked by OD-04; ref_exchange_rates.csv missing |
| Net Passenger Revenue | FactBookingTransactions[NetPassengerRevenueUSD] | Fact table does not exist | **NOT AVAILABLE** | FactBookingTransactions blocked by OD-04 |
| Net Ancillary Revenue | FactBookingTransactions[NetAncillaryRevenueUSD] | Fact table does not exist | **NOT AVAILABLE** | FactBookingTransactions blocked by OD-04 |
| Net Fee Revenue | FactBookingTransactions[NetFeeRevenueUSD] | Fact table does not exist | **NOT AVAILABLE** | FactBookingTransactions blocked by OD-04 |
| Operating Cost USD | FactOperatingCosts[CostAmountUSD] | Fact table does not exist | **NOT AVAILABLE** | FactOperatingCosts blocked by OD-04 |
| Total RASK | Revenue / ASK | Revenue unavailable; ASK available | **NOT AVAILABLE** | Revenue numerator missing |
| Passenger RASK | Passenger Revenue / ASK | Revenue unavailable; ASK available | **NOT AVAILABLE** | Revenue numerator missing |
| CASK | Operating Cost / ASK | Cost unavailable; ASK available | **NOT AVAILABLE** | Cost numerator missing |
| Unit Contribution | Revenue − Cost / ASK | Both unavailable | **NOT AVAILABLE** | Both numerators missing |
| Passenger Yield | Passenger Revenue / RPK | Revenue unavailable; RPK available | **NOT AVAILABLE** | Revenue numerator missing |
| Ancillary Revenue per Passenger | Ancillary Revenue / Revenue Passengers | Revenue unavailable | **NOT AVAILABLE** | Revenue numerator missing |
| Average Passenger Revenue | Passenger Revenue / Revenue Passengers | Revenue unavailable | **NOT AVAILABLE** | Revenue numerator missing |
| Refund Rate | Refunded coupons / Eligible coupons | FactBookingTransactions missing | **NOT AVAILABLE** | Fact table missing |
| Booking Lead Time | BookingDate, TravelDate per booking | FactBookingTransactions missing | **NOT AVAILABLE** | Fact table missing |
| Repeat Booking Rate | Customer bookings over time | FactBookingTransactions missing | **NOT AVAILABLE** | Fact table missing |
| Service Recovery Rate | ServiceRecoveryFlag, ResolutionStatus | Available in fact_customer_feedback | **PARTIALLY AVAILABLE** | Feedback table exists; could calculate but not a financial KPI |

### 5.2 Non-Monetary Operational KPIs That CAN Be Reported on Page 03

These are not financial KPIs but could provide context if the page design permits non-financial measures:

| Measure | Source | Status | Notes |
|---|---|---|---|
| Revenue Passengers | fact_flight_operations[RevenuePassengers] | AVAILABLE | FL02 = 218,413; passenger count, NOT revenue |
| Available Seats | fact_flight_operations[AvailableSeats] | AVAILABLE | Capacity measure |
| Load Factor | RPK / ASK | DERIVABLE | RPK and ASK calculable from flight data |
| ASK | AvailableSeats × FlightDistanceKM | DERIVABLE | Capacity measure |
| RPK | RevenuePassengers × FlightDistanceKM | DERIVABLE | Traffic measure |

---

## 6. Visual-by-Visual Financial Feasibility

The Page 03 dashboard specification (`docs/POWER_BI_DASHBOARD_SPECIFICATION.md`) lists these visuals:

| Visual ID | Visual | Required Financial Data | Classification | Feasible? |
|---|---|---|---|---|
| RV-01 | Total Operating Revenue KPI | Net Passenger + Fee + Ancillary Revenue USD | NOT AVAILABLE | ❌ No |
| RV-02 | Passenger Revenue KPI | NetPassengerRevenueUSD | NOT AVAILABLE | ❌ No |
| RV-03 | Ancillary Revenue KPI | NetAncillaryRevenueUSD | NOT AVAILABLE | ❌ No |
| RV-04 | Passenger Yield KPI | Passenger Revenue / RPK | NOT AVAILABLE | ❌ No |
| RV-05 | Passenger RASK KPI | Passenger Revenue / ASK | NOT AVAILABLE | ❌ No |
| RV-06 | Total RASK KPI | Total Revenue / ASK | NOT AVAILABLE | ❌ No |
| RV-07 | CASK KPI | Operating Cost / ASK | NOT AVAILABLE | ❌ No |
| RV-08 | Unit Contribution KPI | (Revenue − Cost) / ASK | NOT AVAILABLE | ❌ No |
| RV-09 | Revenue trend by stream | Net Passenger/Fee/Ancillary Revenue by month | NOT AVAILABLE | ❌ No |
| RV-10 | Yield and RASK trend | Yield/RASK by month | NOT AVAILABLE | ❌ No |
| RV-11 | RASK vs CASK | RASK and CASK by month | NOT AVAILABLE | ❌ No |
| RV-12 | Fare class mix | Revenue by FareClass | PARTIALLY AVAILABLE | ⚠️ Dimension exists; no fact data |
| RV-13 | Channel mix | Revenue by BookingChannel | PARTIALLY AVAILABLE | ⚠️ Dimension exists; no fact data |
| RV-14 | Average passenger revenue | Revenue / Revenue Passengers | NOT AVAILABLE | ❌ No |
| RV-15 | Ancillary per passenger | Ancillary Revenue / Revenue Passengers | NOT AVAILABLE | ❌ No |
| RV-16 | Booking lead time | BookingDate vs TravelDate per booking | NOT AVAILABLE | ❌ No |
| RV-17 | Refund rate trend | Refunded coupons by month | NOT AVAILABLE | ❌ No |
| RV-18 | Scenario panel | Fare/fuel/capacity change inputs | NOT AVAILABLE | ❌ No |

**Result: 0 of 18 revenue/finance visuals are feasible with existing data.**

---

## 7. OD-04 Blocking Analysis

OD-04 (Exchange-Rate Policy) is the root cause of all financial data unavailability:

| OD-04 Decision | Status | Impact |
|---|---|---|
| OD-04a — Formal owner approval | PROPOSED — PENDING | Blocks all financial fact generation |
| OD-04b — Currency scope | CONFLICT | OD-04 lists 5 currencies (USD, EUR, GBP, JPY, CAD); DimCurrency has 8 (AED, QAR, SGD, INR, GBP, EUR, USD, AUD). Mismatch unresolved. |
| OD-04c — Rate source | UNSPECIFIED | No RateSource value defined |
| OD-04d — Rate version | UNSPECIFIED | No RateVersion value defined |
| OD-04e — Missing-date behaviour | PROPOSED — PENDING | No forward-fill approved |
| OD-04f — Rate generation methodology | UNSPECIFIED | No rate values or algorithm approved |

**OD-04 blocks:**
- `ref_exchange_rates.csv` creation
- `FactBookingTransactions` builder
- `FactOperatingCosts` builder
- All financial KPIs and visuals on Page 03

The audit report (`docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md`) explicitly states: "Do not mark OD-04 approved. Do not create ref_exchange_rates.csv. Do not implement FactBookingTransactions or FactOperatingCosts until OD-04 is formally approved and the currency mismatch is resolved."

---

## 8. What Is NOT Available — Summary Table

| Category | Item | Classification | Path to Availability |
|---|---|---|---|
| Revenue | Total Operating Revenue | NOT AVAILABLE | OD-04 approval + ref_exchange_rates.csv + FactBookingTransactions |
| Revenue | Passenger Revenue | NOT AVAILABLE | OD-04 approval + ref_exchange_rates.csv + FactBookingTransactions |
| Revenue | Ancillary Revenue | NOT AVAILABLE | OD-04 approval + ref_exchange_rates.csv + FactBookingTransactions |
| Revenue | Fee Revenue | NOT AVAILABLE | OD-04 approval + ref_exchange_rates.csv + FactBookingTransactions |
| Cost | Operating Cost USD | NOT AVAILABLE | OD-04 approval + ref_exchange_rates.csv + FactOperatingCosts |
| Ratio | RASK (all variants) | NOT AVAILABLE | Revenue + Cost + ASK (all blocked) |
| Ratio | CASK | NOT AVAILABLE | Cost + ASK (both blocked) |
| Ratio | Unit Contribution | NOT AVAILABLE | Revenue + Cost + ASK (all blocked) |
| Ratio | Yield | NOT AVAILABLE | Revenue + RPK (revenue blocked) |
| Ratio | Refund Rate | NOT AVAILABLE | FactBookingTransactions |
| Behavior | Booking Lead Time | NOT AVAILABLE | FactBookingTransactions |
| Behavior | Repeat Booking Rate | NOT AVAILABLE | FactBookingTransactions |
| Channel | Channel Mix (revenue) | PARTIALLY AVAILABLE | Dimension exists; needs FactBookingTransactions |
| Fare | Fare Class Mix (revenue) | PARTIALLY AVAILABLE | Dimension exists; needs FactBookingTransactions |

---

## 9. What Passenger Volume (FL02) IS and IS NOT

**FL02 = SUM(fact_flight_operations[RevenuePassengers]) = 218,413**

| Is | Is Not |
|---|---|
| A count of revenue passengers carried | Monetary revenue in any currency |
| A volume measure (passenger traffic) | Passenger Revenue, Net Passenger Revenue, or Yield |
| Additive across flight legs | A financial KPI |
| Usable for load factor (RPK/ASK) | Usable for RASK, CASK, or unit economics |

**Per the governing design documents:**
- `docs/DAX_KPI_CATALOGUE.md` Section 1: "FL02 represents passenger volume only (count), not financial revenue."
- `docs/POWER_BI_DASHBOARD_SPECIFICATION.md` Section 2.5: Financial measures must use USD columns from FactBookingTransactions.
- `docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md`: "All financial KPIs in Section 11 are calculated from USD columns."

**FL02 must never be labeled, formatted, or presented as revenue on Page 03.**

---

## 10. Data-Quality Findings (Financial)

| # | Issue | Severity | Impact on Page 03 |
|---|---|---|---|
| FDQ-01 | FactBookingTransactions does not exist | Critical | All revenue KPIs blocked |
| FDQ-02 | FactOperatingCosts does not exist | Critical | All cost KPIs blocked |
| FDQ-03 | ref_exchange_rates.csv does not exist | Critical | Currency conversion impossible |
| FDQ-04 | OD-04 not approved | Critical | FactBookingTransactions/FactOperatingCosts cannot be generated |
| FDQ-05 | Currency set mismatch (OD-04: 5 vs DimCurrency: 8) | High | Referential integrity risk for any future financial facts |
| FDQ-06 | dim_currency, dim_booking_channel, dim_fare_class unused | Medium | Dimensions exist but have no fact data to analyze |
| FDQ-07 | FL02 could be mislabeled as revenue | High | Must be explicitly labeled as passenger volume, not revenue |

---

## 11. Implementation Recommendation

### Recommended Approach: Page 03 as Non-Financial Operational Context Page

Since no financial data exists and OD-04 is not approved, Page 03 cannot display revenue, cost, profit, yield, RASK, CASK, or any monetary metric. Two options are available:

#### Option A: Defer Page 03 Entirely (Recommended)

Do not build Page 03 until OD-04 is approved and FactBookingTransactions/FactOperatingCosts are generated. This preserves data integrity and avoids presenting incomplete or misleading financial information.

**Prerequisites to unblock:**
1. Owner formally approves OD-04 (all 7 decision questions)
2. Currency set mismatch resolved (align OD-04 with DimCurrency's 8 currencies)
3. `ref_exchange_rates.csv` created with owner-approved synthetic rates
4. `FactBookingTransactions` built and loaded to curated layer
5. `FactOperatingCosts` built and loaded to curated layer
6. Semantic model relationships added for new facts
7. Financial DAX measures defined and validated

#### Option B: Build Page 03 with Non-Financial Operational Context Only

Build Page 3 using only the operational measures that ARE available (passenger volume, available seats, load factor, ASK, RPK), explicitly labeled as non-financial. This would NOT satisfy the "Revenue & Finance" page purpose and would require a scope change to the dashboard specification.

**Not recommended** because it misrepresents the page's purpose and cannot answer the business questions defined in the dashboard specification.

### Final Recommendation

**DEFER Page 03.** Do not build any visuals. Do not create any financial measures. Do not present passenger volume as revenue. Document OD-04 as the blocking prerequisite. Return to Page 03 only after OD-04 is formally approved and the financial fact tables exist in the curated layer.

---

## 12. Documents to Update When OD-04 Is Approved

| Document | Section | Update Required |
|---|---|---|
| docs/03_DATA_CONTRACTS.md | Section 10 (Currency/Financial) | Confirm OD-04 approval status |
| docs/03_DATA_CONTRACTS.md | Section 11 (KPI Definitions) | Implement financial KPIs once facts exist |
| docs/DAX_KPI_CATALOGUE.md | Section 3 | Add financial measures (RASK, CASK, Yield, etc.) |
| docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md | N/A | No change (Page 02 is complete) |
| New: docs/PAGE_03_REVENUE_FINANCE_DAX_SPECIFICATION.md | All | Create when financial facts exist |
| New: docs/PAGE_03_REVENUE_FINANCE_VISUAL_SPECIFICATION.md | All | Create when financial facts exist |

---

## 13. Governance Compliance Confirmation

| Rule | Status |
|---|---|
| Never treat passenger volume as monetary revenue | ✅ Compliant — FL02 explicitly labeled as passenger count |
| Never fabricate financial values | ✅ Compliant — no financial measures proposed |
| Never introduce unsupported financial measures | ✅ Compliant — all financial KPIs classified NOT AVAILABLE |
| Do not modify the PBIX | ✅ Compliant — no PBIX changes |
| Do not modify source data | ✅ Compliant — no source data changes |
| Do not modify Page 01 or Page 02 | ✅ Compliant — neither page touched |
| Audit only; no implementation | ✅ Compliant — this is an audit report |

---

## 14. Conclusion

**Page 03 Revenue & Finance is NOT IMPLEMENTABLE with existing data.**

All 18 revenue/finance visuals are blocked by the absence of `FactBookingTransactions` and `FactOperatingCosts`, which are themselves blocked by unapproved OD-04 and missing `ref_exchange_rates.csv`. No monetary data exists anywhere in the project. Passenger volume (FL02 = 218,413) is explicitly not revenue and must not be presented as such.

**The project should defer Page 03 until OD-04 is formally approved, exchange rates are established, and the two financial fact tables are built and loaded.**

---

**End of audit.** This document is audit evidence only. No data, model, DAX, PBIX, or report was modified.
