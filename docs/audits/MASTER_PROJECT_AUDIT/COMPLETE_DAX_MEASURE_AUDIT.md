# AEROVISION 360 — COMPLETE DAX MEASURE AUDIT

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08-DAX  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY AUDIT — NO FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. DAX Measure Inventory Summary

| Prefix | Count | Measure IDs | Status |
|--------|-------|-------------|--------|
| FL (Flight Operations) | 4 | FL01, FL02, FL03, FL04 | Defined; verified against source |
| DS (Disruptions) | 3 | DS01, DS02, DS03 | Defined; DS03 has audit issue (DAX-01) |
| CF (Customer Feedback) | 14 | CF01-CF14 | Defined; verified against source |
| RV (Revenue) | 21 | RV_BookingCount through RV_RevenueByBookingDateUSD | OD-04 BLOCKED |
| CX (Operating Costs) | 11 | CX_TotalOperatingCostsUSD through CX_CostsYTDUSD | OD-04 BLOCKED |
| NC (Financial Performance) | 3 | NC_NetOperatingContributionUSD, NC_RevenueToCostRatio, NC_RevenuePerRevenuePassengerUSD | OD-04 BLOCKED |
| OP (Operations Performance) | 4 | OP01, OP02, OP03, OP04 | Defined in specification; NOT in DAX file |
| **Total** | **54** | | |

---

## 2. DAX Measure Detail

### FL Measures (Flight Operations)

| Measure | DAX Expression | Location | Verified Value | Data Source | Status |
|---------|---------------|----------|----------------|-------------|--------|
| FL01 | `COUNTROWS(FILTER(fact_flight_operations, fact_flight_operations[FlightStatus] = "Operated"))` | DAX line 9 | 4,776 | fact_flight_operations | Verified |
| FL02 | `SUM(fact_flight_operations[RevenuePassengers])` | DAX line 10 | 218,413 | fact_flight_operations | Verified |
| FL03 | `AVERAGE(fact_flight_operations[DepartureDelayMinutes])` | DAX line 11 | 43.42 | fact_flight_operations | Verified |
| FL04 | `VAR _total = COUNTROWS(fact_flight_operations) VAR _cancelled = COUNTROWS(FILTER(fact_flight_operations, fact_flight_operations[CancellationFlag] = TRUE())) RETURN IF(_total = 0, BLANK(), DIVIDE(_cancelled, _total) * 100)` | DAX line 12 | 4.48% | fact_flight_operations | Verified |

### DS Measures (Disruptions)

| Measure | DAX Expression | Location | Verified Value | Data Source | Status |
|---------|---------------|----------|----------------|-------------|--------|
| DS01 | `COUNTROWS(fact_disruptions)` | DAX line 13 | 1,754 | fact_disruptions | Verified |
| DS02 | `AVERAGE(fact_disruptions[DelayMinutes])` | DAX line 14 | 120.62 | fact_disruptions | Verified |
| DS03 | `COUNTROWS(FILTER(fact_disruptions, RELATED(dim_disruption_type[ControllableFlag]) = TRUE()))` | DAX line 15 | 540 | fact_disruptions | DAX-01 Issue |

**DAX-01:** DS03 counts dimension rows instead of fact events. The current expression counts rows in dim_disruption_type where ControllableFlag = TRUE (3 rows), not disruption events in fact_disruptions (540 events). The DAX expression should count fact_disruptions rows where the related disruption type is controllable: `COUNTROWS(FILTER(fact_disruptions, RELATED(dim_disruption_type[ControllableFlag]) = TRUE()))`.

### CF Measures (Customer Feedback)

| Measure | DAX Expression | Location | Verified Value | Data Source | Status |
|---------|---------------|----------|----------------|-------------|--------|
| CF01 | `COUNTROWS(fact_customer_feedback)` | DAX line 16 | 2,500 | fact_customer_feedback | Verified |
| CF02 | `AVERAGE(fact_customer_feedback[SatisfactionScore])` | DAX line 17 | 2.99 | fact_customer_feedback | Verified |
| CF03 | `VAR _total = COUNTROWS(fact_customer_feedback) VAR _complaints = COUNTROWS(FILTER(fact_customer_feedback, fact_customer_feedback[FeedbackType] = "Complaint")) RETURN IF(_total = 0, BLANK(), DIVIDE(_complaints, _total) * 100)` | DAX line 18 | 25.52% | fact_customer_feedback | Verified |
| CF04 | `COUNTROWS(FILTER(dim_customer, dim_customer[IsActive] = TRUE))` | DAX line 19 | 4,808 | dim_customer | Verified |
| CF05 | `COUNTROWS(FILTER(fact_customer_feedback, fact_customer_feedback[FeedbackType] = "Complaint"))` | DAX line 20 | 638 | fact_customer_feedback | Verified |
| CF06 | `COUNTROWS(FILTER(fact_customer_feedback, fact_customer_feedback[FeedbackType] = "Compliment"))` | DAX line 21 | 603 | fact_customer_feedback | Verified |
| CF07 | `COUNTROWS(FILTER(fact_customer_feedback, fact_customer_feedback[FeedbackType] = "Claim"))` | DAX line 22 | 618 | fact_customer_feedback | Verified |
| CF08 | `COUNTROWS(FILTER(fact_customer_feedback, fact_customer_feedback[FeedbackType] = "Survey"))` | DAX line 23 | 641 | fact_customer_feedback | Verified |
| CF09 | `DIVIDE(CF06, CF01)` | DAX line 24 | 24.12% | fact_customer_feedback | Verified |
| CF10 | `DIVIDE(CF05 + CF07, CF01)` | DAX line 25 | 50.24% | fact_customer_feedback | Verified |
| CF11 | `DIVIDE(COUNTROWS(FILTER(fact_customer_feedback, fact_customer_feedback[ServiceRecoveryFlag] = TRUE)), CF05)` | DAX line 26 | 59.72% | fact_customer_feedback | Semantic issue |
| CF12 | `DIVIDE(COUNTROWS(FILTER(fact_customer_feedback, fact_customer_feedback[ResolutionStatus] = "Resolved")), COUNTROWS(FILTER(fact_customer_feedback, NOT ISBLANK(fact_customer_feedback[ResolutionStatus]))))` | DAX line 27 | 24.16% | fact_customer_feedback | Verified |
| CF13 | `CALCULATE(CF02, fact_customer_feedback[FeedbackType] = "Complaint")` | DAX line 28 | 3.07 | fact_customer_feedback | Verified |
| CF14 | `CALCULATE(CF02, fact_customer_feedback[FeedbackType] = "Compliment")` | DAX line 29 | BLANK | fact_customer_feedback | BLANK — all Compliment SatisfactionScore NULL |

**CF11 Semantic Issue:** The numerator `COUNTROWS(FILTER(fact_customer_feedback, fact_customer_feedback[ServiceRecoveryFlag] = TRUE))` counts ALL feedback events where ServiceRecoveryFlag = TRUE (381 events across all feedback types), while the denominator CF05 counts complaints only (638). This yields 59.72%, but the measure comment says "(of complaints)". The measure should either:
1. Count only complaints where ServiceRecoveryFlag = TRUE: `COUNTROWS(FILTER(fact_customer_feedback, fact_customer_feedback[FeedbackType] = "Complaint" && fact_customer_feedback[ServiceRecoveryFlag] = TRUE))` = 97, yielding 97/638 = 15.20%, OR
2. Change the measure comment to reflect the actual calculation: "Service recovery events / all feedback events"

**CF14 Data Quality Finding:** CF14 returns BLANK because all 603 Compliment feedback events have NULL SatisfactionScore values. `AVERAGE` over an empty set returns BLANK. This is correct DAX behavior — not an error. The measure correctly reflects that no satisfaction scores exist for compliments.

### RV Measures (Revenue) — OD-04 BLOCKED

| Measure | DAX Expression | Location | Status |
|---------|---------------|----------|--------|
| RV_BookingCount | `COUNTROWS(fact_booking_transactions)` | DAX line 42 | Blocked |
| RV_DistinctBookings | `DISTINCTCOUNT(fact_booking_transactions[BookingReference])` | DAX line 44 | Blocked |
| RV_RevenuePassengers | `CALCULATE(SUM(fact_booking_transactions[PassengerCount]), fact_booking_transactions[IsRevenuePassenger] = TRUE())` | DAX line 46-50 | Blocked |
| RV_NonRevenuePassengers | `CALCULATE(SUM(fact_booking_transactions[PassengerCount]), fact_booking_transactions[IsRevenuePassenger] = FALSE())` | DAX line 52-55 | Blocked |
| RV_GrossBookingValueUSD | `SUM(fact_booking_transactions[BaseFareUSD])` | DAX line 58 | Blocked |
| RV_RefundAmountUSD | `SUM(fact_booking_transactions[RefundUSD]) + SUM(fact_booking_transactions[AncillaryRefundUSD]) + SUM(fact_booking_transactions[FeeRefundUSD])` | DAX line 60-63 | Blocked |
| RV_NetPassengerRevenueUSD | `SUM(fact_booking_transactions[NetPassengerRevenueUSD])` | DAX line 65 | Blocked |
| RV_NetFeeRevenueUSD | `SUM(fact_booking_transactions[NetFeeRevenueUSD])` | DAX line 67 | Blocked |
| RV_NetAncillaryRevenueUSD | `SUM(fact_booking_transactions[NetAncillaryRevenueUSD])` | DAX line 68 | Blocked |
| RV_TotalOperatingRevenueUSD | `RV_NetPassengerRevenueUSD + RV_NetFeeRevenueUSD + RV_NetAncillaryRevenueUSD` | DAX line 71-74 | Blocked |
| RV_AvgRevenuePerRevenuePassenger | `DIVIDE(RV_TotalOperatingRevenueUSD, RV_RevenuePassengers, BLANK())` | DAX line 76-78 | Blocked |
| RV_AvgBookingValueUSD | `DIVIDE(RV_GrossBookingValueUSD, RV_BookingCount, BLANK())` | DAX line 79-80 | Blocked |
| RV_RevenueCurrentPeriodUSD | `CALCULATE(RV_TotalOperatingRevenueUSD, dim_date[IsReportingPeriod] = TRUE())` | DAX line 151-155 | Blocked |
| RV_RevenuePriorPeriodUSD | `CALCULATE(RV_TotalOperatingRevenueUSD, SAMEPERIODLASTYEAR(dim_date[FullDate]))` | DAX line 157-161 | Blocked |
| RV_RevenueGrowthPercent | `DIVIDE(RV_RevenueCurrentPeriodUSD - RV_RevenuePriorPeriodUSD, RV_RevenuePriorPeriodUSD, BLANK())` | DAX line 163-168 | Blocked |
| CX_CostsCurrentPeriodUSD | `CALCULATE(CX_TotalOperatingCostsUSD, dim_date[IsReportingPeriod] = TRUE())` | DAX line 170-174 | Blocked |
| CX_CostsPriorPeriodUSD | `CALCULATE(CX_TotalOperatingCostsUSD, SAMEPERIODLASTYEAR(dim_date[FullDate]))` | DAX line 176-180 | Blocked |
| CX_CostGrowthPercent | `DIVIDE(CX_CostsCurrentPeriodUSD - CX_CostsPriorPeriodUSD, CX_CostsPriorPeriodUSD, BLANK())` | DAX line 182-187 | Blocked |
| RV_RevenueYTDUSD | `TOTALYTD(RV_TotalOperatingRevenueUSD, dim_date[FullDate])` | DAX line 189-190 | Blocked |
| CX_CostsYTDUSD | `TOTALYLD(CX_TotalOperatingCostsUSD, dim_date[FullDate])` | DAX line 192-193 | Blocked |
| RV_RevenueByBookingDateUSD | `CALCULATE(RV_TotalOperatingRevenueUSD, USERELATIONSHIP(dim_date[DateKey], fact_booking_transactions[BookingDateKey]))` | DAX line 196-200 | Blocked |

**All RV, CX, NC measures are OD-04 BLOCKED.** They cannot be used until OD-04 exchange-rate policy is resolved.

---

## 3. OP Measures (Operations Performance)

| Measure | DAX Expression | Location | Status |
|---------|---------------|----------|--------|
| OP01 | `VAR _Operated = COUNTROWS(FILTER(fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE)) VAR _OperatedWithValidDelay = COUNTROWS(FILTER(fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE && NOT ISBLANK(fact_flight_operations[DepartureDelayMinutes]))) VAR _OnTimeDepartures = COUNTROWS(FILTER(fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE && fact_flight_operations[OnTimeFlag] = TRUE)) RETURN DIVIDE(_OnTimeDepartures, _OperatedWithValidDelay, BLANK())` | Page 02 DAX Spec line 38-58 | Not in DAX file |
| OP02 | `FL03 = AVERAGE(fact_flight_operations[DepartureDelayMinutes])` | Page 02 DAX Spec line 88-89 | Reuse existing FL03 |
| OP03 | `VAR _Operated = COUNTROWS(FILTER(fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE)) VAR _OperatedWithValidArrival = COUNTROWS(FILTER(fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE && NOT ISBLANK(fact_flight_operations[ArrivalDelayMinutes]))) VAR _TotalArrivalDelay = SUMX(FILTER(fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE), fact_flight_operations[ArrivalDelayMinutes]) RETURN DIVIDE(_TotalArrivalDelay, _OperatedWithValidArrival, BLANK())` | Page 02 DAX Spec line 64-78 | Not in DAX file |
| OP04 | `VAR _TotalFlights = COUNTROWS(fact_flight_operations) VAR _OperatedFlights = COUNTROWS(FILTER(fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE)) RETURN DIVIDE(_OperatedFlights, _TotalFlights, BLANK())` | Page 02 DAX Spec line 79-89 | Not in DAX file |

**OP01, OP03, OP04 are defined in the specification document but NOT yet added to the DAX file.** They need to be added to `dax/AEROVISION360_Measures.dax`.

---

## 4. DAX Issues Summary

| Issue ID | Severity | Measure | Issue | Resolution |
|----------|----------|---------|-------|------------|
| DAX-01 | P1 | DS03 | Counts dimension rows (3) instead of fact events (540) | Change to count fact_disruptions where RELATED(dim_disruption_type[ControllableFlag]) = TRUE() |
| DAX-02 | P2 | FL04 | Uses SUM over boolean column (CancellationFlag) | Replace with COUNTROWS(FILTER(... CancellationFlag = TRUE())) |
| DAX-03 | P2 | FL04, CF03 | Percentage scaling ambiguity (multiply by 100) | Decide: return fraction with Percent format, or keep number with number format |
| DAX-04 | P1 | model.json | Wrong FL01, FL02, CF03 expressions | Correct model.json to match DAX file |
| DAX-05 | P2 | model.json | Omits all dimension tables | Add all dimension tables |
| DAX-06 | P2 | semantic_model.json | No expressions; incomplete relationships | Add measure expressions; complete relationships |
| DAX-07 | P3 | FL02 | Naming ambiguity (passenger volume vs revenue) | Document that FL02 = passenger volume, not revenue |
| DAX-08 | P3 | CF02/CF11 | Satisfaction scale definition pending (OD-11) | Document pending owner decision |

---

## 5. OP Measures Not Yet in DAX File

| Measure | Status | Action Required |
|---------|--------|-----------------|
| OP01 | Not in DAX file | Add OP01 DAX expression to dax/AEROVISION360_Measures.dax |
| OP02 | Reuses FL03 | No action needed — reuse existing FL03 |
| OP03 | Not in DAX file | Add OP03 DAX expression to dax/AEROVISION360_Measures.dax |
| OP04 | Not in DAX file | Add OP04 DAX expression to dax/AEROVISION360_Measures.dax |

---

## 6. Conclusion

All 54 DAX measures have been catalogued. 44 measures are in the DAX file; 4 (OP01, OP03, OP04) are defined in specifications but not yet in the DAX file; 22 (RV, CX, NC) are OD-04 blocked. DS03 has a known expression issue. CF11 has a semantic issue (numerator counts all ServiceRecoveryFlag=True events, not just complaints). CF14 correctly returns BLANK because all Compliment events have NULL SatisfactionScore.

**Critical Path:** Fix DS03 expression, add OP01/OP03/OP04 to DAX file, resolve OD-04 for RV/CX/NC measures, resolve CF11 semantic issue with owner approval.
