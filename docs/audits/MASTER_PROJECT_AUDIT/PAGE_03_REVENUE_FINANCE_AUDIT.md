# AEROVISION 360 — PAGE 03 REVENUE & FINANCE AUDIT

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08-PAGE03  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY AUDIT — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Page Overview

| Attribute | Value |
|-----------|-------|
| Page Name | Revenue & Finance |
| Page Type | Visible (Page 3 of 5) |
| Purpose | What drives revenue, yield, and unit economics |
| Primary KPIs | K-04 (Passenger Yield), K-05 (Passenger RASK), K-06 (Total RASK), K-07 (CASK), K-08 (Unit Contribution), K-14 (Avg Passenger Revenue), K-15 (Ancillary Revenue per Passenger), K-16 (Booking Lead Time), K-17 (Refund Rate) |
| Canvas Size | 1280 × 720 px (16:9) |
| Status | BLOCKED — OD-04 unresolved |

---

## 2. Critical Blocking Issue: OD-04

**OD-04 (Exchange-Rate Policy) is UNRESOLVED.** This blocks Page 03 entirely.

| Affected Measure | Reason |
|------------------|--------|
| RV_BookingCount | FactBookingTransactions blocked |
| RV_DistinctBookings | FactBookingTransactions blocked |
| RV_RevenuePassengers | FactBookingTransactions blocked |
| RV_NonRevenuePassengers | FactBookingTransactions blocked |
| RV_GrossBookingValueUSD | FactBookingTransactions blocked |
| RV_RefundAmountUSD | FactBookingTransactions blocked |
| RV_NetPassengerRevenueUSD | FactBookingTransactions blocked |
| RV_NetFeeRevenueUSD | FactBookingTransactions blocked |
| RV_NetAncillaryRevenueUSD | FactBookingTransactions blocked |
| RV_TotalOperatingRevenueUSD | FactBookingTransactions blocked |
| RV_AvgRevenuePerRevenuePassenger | FactBookingTransactions blocked |
| RV_AvgBookingValueUSD | FactBookingTransactions blocked |
| CX_TotalOperatingCostsUSD | FactOperatingCosts blocked |
| CX_PositiveCostsUSD | FactOperatingCosts blocked |
| CX_CostReversalsUSD | FactOperatingCosts blocked |
| CX_NetOperatingCostsUSD | FactOperatingCosts blocked |
| CX_CostPerFlightOperationUSD | FactOperatingCosts blocked |
| CX_CostPerRevenuePassengerUSD | FactOperatingCosts + FactBookingTransactions blocked |
| NC_NetOperatingContributionUSD | RV + CX blocked |
| NC_RevenueToCostRatio | RV + CX blocked |
| NC_RevenuePerRevenuePassengerUSD | RV blocked |

**Root Cause:** OD-04 (Exchange-Rate Policy) is unresolved. FactBookingTransactions and FactOperatingCosts cannot be loaded into the model. No exchange rate source (ref_exchange_rates.csv) exists in the project.

---

## 3. Visual Inventory

| Visual ID | Visual Type | Measure(s) | Category/Axis | Purpose | Status |
|-----------|-------------|------------|---------------|---------|--------|
| RV-01 | Card | [Total Operating Revenue USD] | Scale | Total operating revenue | BLOCKED (OD-04) |
| RV-02 | Card | [Net Passenger Revenue USD] | Core revenue | Passenger revenue | BLOCKED (OD-04) |
| RV-03 | Card | [Net Ancillary Revenue USD] | Ancillary contribution | Ancillary revenue | BLOCKED (OD-04) |
| RV-04 | Card | [Passenger Yield] | Revenue per RPK | Revenue per RPK | BLOCKED (OD-04) |
| RV-05 | Card | [Passenger RASK] | Revenue per ASK | Revenue per ASK | BLOCKED (OD-04) |
| RV-06 | Card | [Total RASK] | Total unit revenue | Total unit revenue | BLOCKED (OD-04) |
| RV-07 | Card | [CASK] | Unit cost | Unit cost | BLOCKED (OD-04) |
| RV-08 | Card | [Unit Contribution] | Margin per ASK | Margin per ASK | BLOCKED (OD-04) |
| RV-09 | Stacked Column/Line | [Net Passenger Revenue USD], [Net Fee Revenue USD], [Net Ancillary Revenue USD] | X: YearMonth | Revenue trend by stream | BLOCKED (OD-04) |
| RV-10 | Line Chart | [Passenger Yield], [Passenger RASK], [Total RASK] | X: YearMonth | Unit revenue trend | BLOCKED (OD-04) |
| RV-11 | Line/Column | [Total RASK], [CASK] | X: YearMonth | Unit revenue vs cost trend | BLOCKED (OD-04) |
| RV-12 | Horizontal Bar | [Net Passenger Revenue USD] | Category: FareClassName | Fare class mix | BLOCKED (OD-04) |
| RV-13 | Horizontal Bar | [Net Passenger Revenue USD] | Category: ChannelName | Channel mix | BLOCKED (OD-04) |
| RV-14 | Bar Chart | [Average Passenger Revenue] | Category: AirlineName | Average passenger revenue | BLOCKED (OD-04) |
| RV-15 | Bar Chart | [Ancillary Revenue per Passenger] | Category: AirlineName | Ancillary per passenger | BLOCKED (OD-04) |
| RV-16 | Histogram/Column | [Booking Lead Time] | X: Lead-time bin | Booking lead time | BLOCKED (OD-04) |
| RV-17 | Line/Column | [Refund Rate] | X: YearMonth | Refund trend | BLOCKED (OD-04) |
| RV-18 | Cards/Inputs | [Fare Scenario Revenue], [Fuel Scenario Cost], [Capacity Scenario ASK] | What-if analysis | Scenario panel | BLOCKED (OD-04) |

**Total Visuals:** 18 (8 cards, 1 stacked column/line, 1 line chart, 1 line/column, 3 bar charts, 1 bar chart, 1 histogram/column, 1 line/column, 1 cards/inputs)

---

## 4. DAX Measures Required

| Measure ID | Measure Name | Status | Blocked By |
|------------|--------------|--------|------------|
| RV_BookingCount | Total booking transactions (coupons) | Not implemented | OD-04 |
| RV_DistinctBookings | Distinct booking references | Not implemented | OD-04 |
| RV_RevenuePassengers | Revenue passengers | Not implemented | OD-04 |
| RV_NonRevenuePassengers | Non-revenue passengers | Not implemented | OD-04 |
| RV_GrossBookingValueUSD | Gross booking value | Not implemented | OD-04 |
| RV_RefundAmountUSD | Total refunds | Not implemented | OD-04 |
| RV_NetPassengerRevenueUSD | Net passenger revenue | Not implemented | OD-04 |
| RV_NetFeeRevenueUSD | Net fee revenue | Not implemented | OD-04 |
| RV_NetAncillaryRevenueUSD | Net ancillary revenue | Not implemented | OD-04 |
| RV_TotalOperatingRevenueUSD | Total operating revenue | Not implemented | OD-04 |
| RV_AvgRevenuePerRevenuePassenger | Revenue per revenue passenger | Not implemented | OD-04 |
| RV_AvgBookingValueUSD | Average booking value | Not implemented | OD-04 |
| CX_TotalOperatingCostsUSD | Total operating costs | Not implemented | OD-04 |
| CX_PositiveCostsUSD | Positive cost amounts | Not implemented | OD-04 |
| CX_CostReversalsUSD | Cost reversals and credits | Not implemented | OD-04 |
| CX_NetOperatingCostsUSD | Net operating costs | Not implemented | OD-04 |
| CX_CostPerFlightOperationUSD | Cost per flight operation | Not implemented | OD-04 |
| CX_CostPerRevenuePassengerUSD | Cost per revenue passenger | Not implemented | OD-04 |
| NC_NetOperatingContributionUSD | Net operating contribution | Not implemented | OD-04 |
| NC_RevenueToCostRatio | Revenue-to-cost ratio | Not implemented | OD-04 |
| NC_RevenuePerRevenuePassengerUSD | Revenue per revenue passenger | Not implemented | OD-04 |

**Total Measures Blocked: 22**

---

## 5. Missing Data Sources

| Missing Asset | Expected Location | Referenced By | Status |
|---------------|-------------------|---------------|--------|
| FactBookingTransactions | `data/03_curated/fact_booking_transactions.csv` | Page 03 visuals RV-01 through RV-18 | DOES NOT EXIST — OD-04 blocked |
| FactOperatingCosts | `data/03_curated/fact_operating_costs.csv` | Page 03 visuals RV-07 through RV-08 | DOES NOT EXIST — OD-04 blocked |
| ref_exchange_rates.csv | `data/04_reference/ref_exchange_rates.csv` | OD-04 currency conversion | DOES NOT EXIST — OD-04 blocked |

**Root Cause:** OD-04 exchange-rate policy is unresolved. No exchange rate source has been approved. No financial fact tables exist in the curated layer.

---

## 6. Conclusion

Page 03 Revenue & Finance is **BLOCKED and cannot be implemented** until OD-04 is resolved. All 18 visuals depend on financial measures that require FactBookingTransactions and FactOperatingCosts, which are blocked by OD-04. The exchange rate source file (ref_exchange_rates.csv) does not exist.

**Recommendation:** Do not build Page 03 visuals. Wait for OD-04 resolution. Once OD-04 is approved, the financial fact tables can be created and the 18 visuals implemented according to the report.json specification.
