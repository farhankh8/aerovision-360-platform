# AEROVISION 360 — DAX AND POWER QUERY COMPLETENESS RECONCILIATION

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08-DAXPQ  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY RECONCILIATION — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. DAX Measure Completeness Reconciliation

### 1.1 DAX Measures Defined in `dax/AEROVISION360_Measures.dax`

| Prefix | Count | Measure IDs | Status |
|--------|-------|-------------|--------|
| FL (Flight Operations) | 4 | FL01-FL04 | **Defined in DAX file** |
| DS (Disruptions) | 3 | DS01-DS03 | **Defined in DAX file** |
| CF (Customer Feedback) | 14 | CF01-CF14 | **Defined in DAX file** |
| RV (Revenue) | 21 | RV_BookingCount through RV_RevenueByBookingDateUSD | **Defined in DAX file, OD-04 BLOCKED** |
| CX (Operating Costs) | 11 | CX_TotalOperatingCostsUSD through CX_CostsYTDUSD | **Defined in DAX file, OD-04 BLOCKED** |
| NC (Financial Performance) | 3 | NC_NetOperatingContributionUSD, NC_RevenueToCostRatio, NC_RevenuePerRevenuePassengerUSD | **Defined in DAX file, OD-04 BLOCKED** |
| OP (Operations Performance) | 0 | None | **NOT in DAX file** |

**Total DAX measures defined: 44 of 54 expected**
**Missing from DAX file: OP01, OP02, OP03, OP04** — These are defined in `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md` but NOT yet added to `dax/AEROVISION360_Measures.dax`.

### 1.2 Detailed Measure Status

| Measure ID | Measure Name | In DAX File? | Blocked By | Verified Value |
|------------|--------------|--------------|------------|
| FL01 | Flights Operated | Yes | 4,776 |
| FL02 | Total Revenue Passengers | Yes | 218,413 |
| FL03 | Average Departure Delay | Yes | 43.42 |
| FL04 | Cancellation Rate | Yes | 4.48% |
| DS01 | Total Disruptions | Yes | 1,754 |
| DS02 | Average Delay Minutes | Yes | 120.62 |
| DS03 | Controllable Disruptions | Yes | 540 (DAX-01: expression issue) |
| CF01 | Total Feedback Events | Yes | 2,500 |
| CF02 | Average Satisfaction Score | Yes | 2.99 |
| CF03 | Complaint Percentage | Yes | 25.52% |
| CF04 | Active Customers | Yes | 4,808 |
| CF05 | Complaint Count | Yes | 638 |
| CF06 | Compliment Count | Yes | 603 |
| CF07 | Claim Count | Yes | 618 |
| CF08 | Survey Count | Yes | 641 |
| CF09 | Positive Feedback Rate | Yes | 24.12% |
| CF10 | Negative Feedback Rate | Yes | 50.24% |
| CF11 | Service Recovery Rate | Yes | 59.72% (semantic issue) |
| CF12 | Resolution Rate | Yes | 24.16% |
| CF13 | Complaint Satisfaction Avg | Yes | 3.07 |
| CF14 | Compliment Satisfaction Avg | Yes | BLANK (all NULL) |
| RV_BookingCount | Total booking transactions | Yes | OD-04 BLOCKED |
| RV_DistinctBookings | Distinct booking references | Yes | OD-04 BLOCKED |
| RV_RevenuePassengers | Revenue passengers | Yes | OD-04 BLOCKED |
| RV_NonRevenuePassengers | Non-revenue passengers | Yes | OD-04 BLOCKED |
| RV_GrossBookingValueUSD | Gross booking value | Yes | OD-04 BLOCKED |
| RV_RefundAmountUSD | Total refunds | Yes | OD-04 BLOCKED |
| RV_NetPassengerRevenueUSD | Net passenger revenue | Yes | OD-04 BLOCKED |
| RV_NetFeeRevenueUSD | Net fee revenue | Yes | OD-04 BLOCKED |
| RV_NetAncillaryRevenueUSD | Net ancillary revenue | Yes | OD-04 BLOCKED |
| RV_TotalOperatingRevenueUSD | Total operating revenue | Yes | OD-04 BLOCKED |
| RV_AvgRevenuePerRevenuePassenger | Revenue per revenue passenger | Yes | OD-04 BLOCKED |
| RV_AvgBookingValueUSD | Average booking value | Yes | OD-04 BLOCKED |
| RV_RevenueCurrentPeriodUSD | Current-period revenue | Yes | OD-04 BLOCKED |
| RV_RevenuePriorPeriodUSD | Prior-period revenue | Yes | OD-04 BLOCKED |
| RV_RevenueGrowthPercent | Revenue growth % | Yes | OD-04 BLOCKED |
| RV_RevenueYTDUSD | Year-to-date revenue | Yes | OD-04 BLOCKED |
| RV_RevenueByBookingDateUSD | Revenue by booking date | Yes | OD-04 BLOCKED |
| CX_TotalOperatingCostsUSD | Total operating costs | Yes | OD-04 BLOCKED |
| CX_PositiveCostsUSD | Positive cost amounts | Yes | OD-04 BLOCKED |
| CX_CostReversalsUSD | Cost reversals | Yes | OD-04 BLOCKED |
| CX_NetOperatingCostsUSD | Net operating costs | Yes | OD-04 BLOCKED |
| CX_CostPerFlightOperationUSD | Cost per flight operation | Yes | OD-04 BLOCKED |
| CX_CostPerRevenuePassengerUSD | Cost per revenue passenger | Yes | OD-04 BLOCKED |
| CX_CostsCurrentPeriodUSD | Current-period costs | Yes | OD-04 BLOCKED |
| CX_CostsPriorPeriodUSD | Prior-period costs | Yes | OD-04 BLOCKED |
| CX_CostGrowthPercent | Cost growth % | Yes | OD-04 BLOCKED |
| CX_CostsYTDUSD | Year-to-date costs | Yes | OD-04 BLOCKED |
| NC_NetOperatingContributionUSD | Net operating contribution | Yes | OD-04 BLOCKED |
| NC_RevenueToCostRatio | Revenue-to-cost ratio | Yes | OD-04 BLOCKED |
| NC_RevenuePerRevenuePassengerUSD | Revenue per revenue passenger | Yes | OD-04 BLOCKED |
| OP01 | On-Time Departure Rate | **NOT in DAX file** | Defined in specification only |
| OP02 | Average Departure Delay | Reuses FL03 | Not separately defined |
| OP03 | Average Arrival Delay | **NOT in DAX file** | Defined in specification only |
| OP04 | Flight Completion Rate | **NOT in DAX file** | Defined in specification only |
| OP05 | Aircraft Utilization | NOT defined | Missing source data (ref_aircraft_availability.csv) |

---

## 1.3 DAX Measures Missing from DAX File

| Measure ID | Measure Name | Defined In | Status |
|------------|--------------|------------|--------|
| OP01 | On-Time Departure Rate | docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md | Not in DAX file — needs to be added |
| OP03 | Average Arrival Delay | docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md | Not in DAX file — needs to be added |
| OP04 | Flight Completion Rate | docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md | Not in DAX file — needs to be added |

**3 measures need to be added to `dax/AEROVISION360_Measures.dax`.**

---

## 2. Power Query Completeness Reconciliation

### 2.1 Power Query M Script (`dax/AEROVISION360_Measures.dax` vs `power_query/AEROVISION360_DataLoad.m`)

The Power Query M script (`AEROVISION360_DataLoad.m`) defines **only 2 of 14 tables**:

| Table | Defined in Power Query M? | Source File | Status |
|-------|--------------------------|-------------|--------|
| dim_airline | Yes | AEROVISION360_DataLoad.m | Defined |
| dim_airport | Yes | AEROVISION360_DataLoad.m | Defined |
| dim_route | No | — | Missing |
| dim_date | No | — | Missing |
| dim_aircraft | No | — | Missing |
| dim_aircraft_type | No | — | Missing |
| dim_customer | No | — | Missing |
| dim_disruption_type | No | — | Missing |
| dim_booking_channel | No | — | Missing |
| dim_currency | No | — | Missing |
| dim_fare_class | No | — | Missing |
| fact_flight_operations | No | — | Missing |
| fact_customer_feedback | No | — | Missing |
| fact_disruptions | No | — | Missing |
| fact_booking_transactions | No | — | Missing |
| fact_operating_costs | No | — | Missing |

**12 of 14 tables are NOT defined in Power Query M.**

### 2.2 Power Query Issues

| Issue ID | Severity | Description | Impact |
|----------|----------|-------------|--------|
| PQ-01 | HIGH | Only 2 of 14 tables defined in Power Query M | 12 tables cannot be loaded into Power BI |
| PQ-02 | MEDIUM | dim_airline column count mismatch | M code states 14 columns; actual CSV has 12 |
| PQ-03 | MEDIUM | No error handling | Errors may fail silently |
| PQ-04 | MEDIUM | No duplicate prevention | Duplicate rows may pass through |

---

## 3. DAX Measure Governance Status

| Measure | OD-04 Blocked? | Reason |
|---------|---------------|--------|
| All RV_* measures (21) | YES | FactBookingTransactions blocked |
| All CX_* measures (11) | YES | FactOperatingCosts blocked |
| All NC_* measures (3) | YES | Depends on RV and CX measures |
| All other measures (20) | NO | Not blocked |

**Total: 22 measures blocked by OD-04, 32 measures not blocked.**

---

## 7. DAX Measures Not in DAX File but Defined in Specifications

| Measure ID | Measure Name | Defined In | Required Action |
|------------|--------------|------------|-----------------|
| OP01 | On-Time Departure Rate | docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md | Add to DAX file |
| OP03 | Average Arrival Delay | docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md | Add to DAX file |
| OP04 | Flight Completion Rate | docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md | Add to DAX file |

---

## 8. Conclusion

**DAX Measures:** 44 of 54 measures are defined in `dax/AEROVISION360_Measures.dax`. 3 measures (OP01, OP03, OP04) are defined in specifications but not yet in the DAX file. 22 measures are blocked by OD-04.

**Power Query M:** Only 2 of 14 tables defined. 12 tables need Power Query M code written.

**Key Issue:** The DAX file has 44 measures but is missing OP01, OP03, OP04 which are defined in the Page 02 DAX specification. These need to be added to complete the DAX measure set.
