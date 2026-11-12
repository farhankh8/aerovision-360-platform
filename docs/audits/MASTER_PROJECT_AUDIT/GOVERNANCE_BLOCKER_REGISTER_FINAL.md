# AEROVISION 360 — Governance Blockers Register (Final)

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY INVESTIGATION — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Purpose

This register documents all confirmed governance blockers that prevent Page 05 — Customer & Service Intelligence (and the broader AEROVISION 360 project) from proceeding to data generation, Power BI model implementation, and report deployment. It consolidates findings from the complete master audit into a single, actionable register.

## 2. Blocker Summary

| Blocker ID | Blocker | Severity | Source Document | Status | Blocks |
|------------|---------|----------|-------------|--------|
| B-01 | OD-04 Exchange-Rate Policy | CRITICAL | UNRESOLVED | FactBookingTransactions, FactOperatingCosts; Page 03 (Revenue & Finance), Page 04 (Cost & Financial Intelligence) |
| G-01 | OD-01A Airline Population | CRITICAL | OWNER-CONFIRMED, NOT FORMALLY SIGNED | Data generation (G4) |
| G-02 | OD-01B Airline Identity Reference | CRITICAL | OWNER-CONFIRMED, FORMAL SIGNATURE PENDING | Data generation, reference CSV creation |
| G-03 | G3-RV-01 Reference Version Approval | CRITICAL | NOT EXECUTED | Data generation, schema freeze |
| G-04 | G4 Data Generation | BLOCKED | BLOCKED | All fact table generation, semantic model population, report page implementation |

---

## 2. Blocker Detail

### OD-04 — Exchange-Rate Policy (CRITICAL, UNRESOLVED)

**Source documents:**
- `docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md`
- `docs/GOVERNANCE_COMPLIANCE.md`
- `docs/03_DATA_CONTRACTS.md` Section 10

**Affected tables:** `fact_booking_transactions`, `fact_operating_costs`

**Blocked measures (22):** RV_BookingCount, RV_DistinctBookings, RV_RevenuePassengers, RV_NonRevenuePassengers, RV_GrossBookingValueUSD, RV_RefundAmountUSD, RV_NetPassengerRevenueUSD, RV_NetFeeRevenueUSD, RV_NetAncillaryRevenueUSD, RV_TotalOperatingRevenueUSD, RV_AvgRevenuePerRevenuePassenger, RV_AvgBookingValueUSD, RV_RevenueCurrentPeriodUSD, RV_RevenuePriorPeriodUSD, RV_RevenueGrowthPercent, RV_RevenueYTDUSD, RV_RevenueByBookingDateUSD, CX_TotalOperatingCostsUSD, CX_PositiveCostsUSD, CX_CostReversalsUSD, CX_NetOperatingCostsUSD, CX_CostPerFlightOperationUSD, CX_CostPerRevenuePassengerUSD, CX_CostsCurrentPeriodUSD, CX_CostsPriorPeriodUSD, CX_CostGrowthPercent, CX_CostsYTDUSD, NC_NetOperatingContributionUSD, NC_RevenueToCostRatio, NC_RevenuePerRevenuePassengerUSD

**Required resolution:** Owner decision on exchange-rate policy, creation of `ref_exchange_rates.csv` with rate coverage for all TransactionCurrencyKey / CurrencyKey values referenced by facts.

---

## 3. Governance Approval Status

| Decision ID | Status | Owner Decision Required? | Blocks |
|-------------|--------|------------------------|----------|
| OD-01A | Owner-confirmed design, formal approval pending | Yes — formal signature | Data generation (G4) |
| OD-01B | Owner-confirmed design, formal approval pending | Yes — formal signature | Data generation, reference version |
| OD-04 | Unresolved | Yes — owner decision | FactBookingTransactions, FactOperatingCosts |
| G3-RV-01 | NOT EXECUTED | Yes — owner approval | Data generation, reference CSV creation |

---

## 4. Independently Executable Work

None. All data generation, schema creation, and model implementation are blocked by OD-01A/OD-01B and G3-RV-01. OD-04 additionally blocks all financial fact implementation.
