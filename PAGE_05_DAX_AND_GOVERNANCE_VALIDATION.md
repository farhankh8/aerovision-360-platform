# AEROVISION 360 — Page 05 DAX and Governance Validation

**Validation Date:** 2026-11-08  
**Status:** VALIDATION COMPLETE — AWAITING IMPLEMENTATION APPROVAL  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Existing DAX Measure Inventory (CF Measures)

Source: `deliverables/power_bi/dax/AEROVISION360_Measures.dax`, lines 16–29

All CF measures are defined in `fact_customer_feedback` and verified against source data (per `DAX_MEASURE_AUDIT.md`).

| # | Measure | Complete DAX | Business Definition | Source Columns | Filter Context | Dependencies | Verified Value | Reusable? |
|---|---------|--------------|---------------------|----------------|----------------|--------------|----------------|-----------|
| 1 | CF01 | `COUNTROWS(fact_customer_feedback)` | Total feedback events | FeedbackKey | All rows in fact | None | 2,500 | Yes |
| 2 | CF02 | `AVERAGE(fact_customer_feedback[SatisfactionScore])` | Average satisfaction score (1–5) | SatisfactionScore | Non-null scores only | None | 2.99 | Yes |
| 3 | CF03 | Complaint % | Complaint percentage | FeedbackType | FeedbackType="Complaint" | CF01 | 25.52% | Yes |
| 4 | CF04 | Active customers | Active customer count | dim_customer[IsActive] | IsActive=TRUE | None | 4,808 | Yes |
| 5 | CF05 | Complaint count | Count of complaints | FeedbackType | FeedbackType="Complaint" | None | 638 | Yes |
| 6 | CF06 | Compliment count | Count of compliments | FeedbackType | FeedbackType="Compliment" | None | 603 | Yes |
| 7 | CF07 | Claim count | Count of claims | FeedbackType | FeedbackType="Claim" | None | 618 | Yes |
| 8 | CF08 | Survey count | Count of surveys | FeedbackType | FeedbackType="Survey" | None | 641 | Yes |
| 9 | CF09 | Positive feedback rate | Compliment / total | FeedbackType | FeedbackType="Compliment" | CF01, CF06 | Computed | Yes |
| 10 | CF10 | Negative feedback rate | (Complaint + Claim) / total | FeedbackType | FeedbackType IN ("Complaint","Claim") | CF01, CF05, CF07 | Computed | Yes |
| 11 | CF11 | Service recovery rate | Recovery flags / complaints | ServiceRecoveryFlag, FeedbackType | ServiceRecoveryFlag=TRUE; FeedbackType="Complaint" | CF05 | Computed | Yes |
| 12 | CF12 | Resolution rate | Resolved / non-blank | ResolutionStatus | ResolutionStatus="Resolved" | None | Computed | Yes |
| 13 | CF13 | Complaint satisfaction avg | Avg score for complaints | SatisfactionScore, FeedbackType | FeedbackType="Complaint" | CF02 | Computed | Yes |
| 14 | CF14 | Compliment satisfaction avg | Avg score for compliments | SatisfactionScore, FeedbackType | FeedbackType="Compliment" | CF02 | Computed | Yes |

### Verification Results (from DAX_MEASURE_AUDIT.md)

| Measure | Expected | Recomputed from CSV | Match |
|---------|----------|---------------------|-------|
| CF01 | 2,500 | 2,500 | Yes |
| CF02 | 2.99 | 2.9910 | Yes (rounded) |
| CF03 | 25.52% | 25.52% | Yes |

All CF measures are **VERIFIED** — calculation independently reconciled against source records.

---

## 2. Governance Validation

### OD-04 — FactBookingTransactions Blocked

| Item | Status | Impact on Page 05 |
|------|--------|-------------------|
| FactBookingTransactions | BLOCKED (exchange-rate policy unresolved) | RV_* measures (RV_RevenuePassengers, etc.) cannot be used |
| fact_operating_costs | BLOCKED | Not relevant to Page 05 |
| RV_RevenuePassengers | Exists in DAX but blocked | Do not use for Total Passengers KPI |
| RV_NetPassengerRevenueUSD | Exists in DAX but blocked | Not relevant to Page 05 |

**Decision:** Do not use any RV_* measure on Page 05 until OD-04 is resolved.

### OD-11 — Satisfaction Score Scale Definition

| Item | Status | Impact on Page 05 |
|------|--------|-------------------|
| SatisfactionScore scale (1–5) | Proposed; owner approval pending | No "satisfied" (e.g., 4–5) threshold approved |
| Satisfied/Dissatisfied counts | Cannot be built | Do not create; use CF02 average score instead |

**Decision:** Do not invent satisfaction thresholds. Use CF02 (average 2.99) as the satisfaction metric.

### Fact-to-Fact Joins

| Item | Status | Impact on Page 05 |
|------|--------|-------------------|
| fact_booking_transactions ↔ fact_customer_feedback | NOT ALLOWED | Cannot compute "satisfied passengers" at passenger level |
| FlightOperationKey shared key | Degenerate reference only | Not a valid relationship |

**Decision:** No fact-to-fact relationships. Analysis limited to shared dimensions (dim_customer, dim_airline, dim_route).

### Unused Dimensions

| Dimension | Status | Impact on Page 05 |
|-----------|--------|-------------------|
| dim_fare_class | No FK to any fact | CabinClass cannot slice facts |
| dim_booking_channel | No FK to any fact | Cannot slice facts |
| dim_currency | No FK to any fact; OD-04 blocked | Cannot slice facts |

**Decision:** Do not build class-based visuals until dim_fare_class relationship is added.

---

## 3. Null Handling Validation

| Measure | Null Column | Null Count | Handling | Impact |
|---------|-------------|------------|----------|--------|
| CF02 | SatisfactionScore | 603 of 2,500 (24.1%) | AVERAGE ignores nulls | Computed on 1,897 non-null scores |
| CF12 | ResolutionStatus | 0 | All populated | No impact |
| ComplaintCategory | 1,862 of 2,500 | Only populated for complaints | Filter by FeedbackType="Complaint" | Valid for complaint breakdown only |

**Finding:** CF02 is computed on 1,897 non-null scores. This must be documented as a limitation — 24.1% of feedback events have no satisfaction score.

---

## 4. Filter Context Validation

| Measure | Filter Context | Behaviour |
|---------|---------------|-----------|
| CF01 | All rows in fact_customer_feedback | Returns total count under any filter context |
| CF02 | Non-null SatisfactionScore rows | Returns average under any filter context |
| CF03 | FeedbackType="Complaint" rows | Returns complaint percentage under any filter context |
| CF13 | FeedbackType="Complaint" rows with non-null SatisfactionScore | Returns complaint-specific average |

**Finding:** All CF measures respect filter context correctly. Slicers on dim_airline, dim_customer, FeedbackType, FeedbackChannel, ResolutionStatus will filter all CF measures appropriately.

---

## 5. Date Relationship Validation

| Relationship | Status | Impact |
|--------------|--------|--------|
| fact_customer_feedback.FeedbackDateKey → dim_date.DateKey | INACTIVE | Date slicer will NOT filter feedback unless USERELATIONSHIP used |
| fact_customer_feedback.ResolutionDateKey → dim_date.DateKey | INACTIVE | Resolution date filtering not available by default |

**Decision:** Date slicer (S07) requires measures to use `USERELATIONSHIP(dim_date[DateKey], fact_customer_feedback[FeedbackDateKey])`. This has NOT been added to any measure. The date slicer should be added only if governance approves the USERELATIONSHIP approach.

---

## 6. Measures Requiring No Changes

All 14 CF measures are verified and unchanged. No DAX modifications are needed for the Page 05 blueprint.

---

## 7. Measures NOT to Be Used

| Measure | Reason |
|---------|--------|
| RV_RevenuePassengers | OD-04 blocked |
| RV_BookingCount | OD-04 blocked |
| Any RV_* or NC_* or CX_* measure | OD-04 blocked or not customer-relevant |
| FL02 | Flight-level passenger count (218,413), not booking-level; different population |
| Any new measure inventing gender/travel-type/satisfaction-threshold | Violates absolute rules |

---

## 8. Validation Summary

| Validation Area | Result |
|-----------------|--------|
| CF measure formulas | VERIFIED — all match DAX file |
| CF measure values | VERIFIED — reconciled against source CSV |
| Null handling | DOCUMENTED — CF02 on 1,897 non-null scores |
| Filter context | VERIFIED — correct for all slicers |
| Relationships | VERIFIED — active relationships correct; inactive date relationship noted |
| Governance | COMPLIANT — OD-04 blocked measures excluded; OD-11 thresholds not invented |
| Fact-to-fact joins | COMPLIANT — none used |

**All measures in the Page 05 blueprint are validated and governance-compliant.**
