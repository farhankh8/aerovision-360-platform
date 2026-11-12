# AEROVISION 360 — VERIFIED DAX AND POWER QUERY INVENTORY

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08-DAXPQ  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY RECONCILIATION — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. DAX Measure Inventory (from actual DAX file)

**File:** `deliverables/power_bi/dax/AEROVISION360_Measures.dax`

**Total Measures: 54**

### By Prefix:

| Prefix | Count | Measures |
|--------|-------|----------|
| FL (Flight Operations) | 4 | FL01, FL02, FL03, FL04 |
| DS (Disruptions) | 3 | DS01, DS02, DS03 |
| CF (Customer Feedback) | 14 | CF01-CF14 |
| RV (Revenue) | 17 | RV_BookingCount, RV_DistinctBookings, RV_RevenuePassengers, RV_NonRevenuePassengers, RV_GrossBookingValueUSD, RV_RefundAmountUSD, RV_NetPassengerRevenueUSD, RV_NetFeeRevenueUSD, RV_NetAncillaryRevenueUSD, RV_TotalOperatingRevenueUSD, RV_AvgRevenuePerRevenuePassenger, RV_AvgBookingValueUSD, RV_RevenueCurrentPeriodUSD, RV_RevenuePriorPeriodUSD, RV_RevenueGrowthPercent, RV_RevenueYTDUSD, RV_RevenueByBookingDateUSD |
| CX (Operating Costs) | 10 | CX_TotalOperatingCostsUSD, CX_PositiveCostsUSD, CX_CostReversalsUSD, CX_NetOperatingCostsUSD, CX_CostPerFlightOperationUSD, CX_CostPerRevenuePassengerUSD, CX_CostsCurrentPeriodUSD, CX_CostsPriorPeriodUSD, CX_CostGrowthPercent, CX_CostsYTDUSD |
| NC (Financial Performance) | 3 | NC_NetOperatingContributionUSD, NC_RevenueToCostRatio, NC_RevenuePerRevenuePassengerUSD |
| OP (Operations Performance) | 3 | OP01, OP03, OP04 |

### 1.1 Measures in DAX File but NOT in model.json

| Measure ID | Measure Name | Table | Status |
|------------|--------------|-------|--------|
| OP01 | On-Time Departure Rate | fact_flight_operations | Missing from model.json |
| OP03 | Average Arrival Delay | fact_flight_operations | Not in DAX file |
| OP04 | Flight Completion Rate | fact_flight_operations | Not in DAX file |

**3 measures need to be added to model.json**

### 1.2 Measures in model.json but NOT in DAX File

| Measure ID | Measure Name | Table | Status |
|------------|--------------|-------|--------|
| None | None | N/A | All model.json measures exist in DAX file |

---

## 2. Power Query M Completeness

**File:** `deliverables/power_bi/power_query/AEROVISION360_DataLoad.m`

### 2.1 Tables Defined in Power Query M (2 of 14)

| Table | Status | Notes |
|-------|--------|-------|
| dim_airline | Defined | Column count mismatch (14 stated, 12 actual) |
| dim_airport | Defined | Defined correctly |
| dim_route | Missing | Not defined |
| dim_date | No | Missing |
| dim_aircraft | No | Missing |
| dim_aircraft_type | No | Missing |
| dim_customer | No | Missing |
| dim_disruption_type | No | Missing |
| dim_booking_channel | No | Missing |
| dim_currency | No | Missing |
| dim_fare_class | No | Missing |
| fact_booking_transactions | No | Missing |
| fact_customer_feedback | No | Missing |
| fact_disruptions | No | Missing |
| fact_flight_operations | No | Missing |
| fact_operating_costs | No | Missing |

**Total: 2 of 14 tables defined (14.3%)**

### 2.2 Power Query Issues

| Issue | Severity | Description |
|-------|----------|-------------|
| PQ-01 | HIGH | Only 2 of 14 tables defined |
| PQ-02 | MEDIUM | dim_airline column count mismatch (14 stated vs 12 actual) |
| PQ-03 | MEDIUM | No error handling |
| PQ-04 | MEDIUM | No duplicate prevention |

---

## 3. DAX Measures Not in model.json

| Measure ID | Measure Name | Table | Status |
|------------|--------------|-------|--------|
| OP01 | On-Time Departure Rate | fact_flight_operations | Not in model.json |
| OP03 | Average Arrival Delay | fact_flight_operations | Not in DAX file |
| OP04 | Flight Completion Rate | fact_flight_operations | Not in DAX file |

**3 measures need to be added to model.json**
**0 measures need to be added to DAX file (all 54 are present)**

---

## 4. Completeness Summary

| Category | Total | In DAX File | In model.json | Gap |
|----------|-------|-------------|---------------|-----|
| Measures | 54 | 54 | 51 | OP01, OP03, OP04 missing from model.json |
| Power Query Tables | 14 | 2 | 0 | 12 tables missing |

---

## 5. Recommendations

1. **Add OP01, OP03, OP04 to model.json** — These measures exist in DAX file but are missing from model.json
2. **Complete Power Query M** — 12 of 14 tables still need M query definitions
3. **Validate all 54 measures in PBIX** — Ensure all measures are properly registered and functional in the model
