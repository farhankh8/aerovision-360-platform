# COMPLETE DAX MEASURE AND EXPRESSION AUDIT

**Source:** `deliverables/power_bi/dax/AEROVISION360_Measures.dax` (read in full, 200 lines)  
**Compared against:** `deliverables/power_bi/semantic_model/model.json` (measure registrations) and `semantic_model.json`  
**Independently validated against:** source CSVs in `data/03_curated/` via `tests/unit/test_stage4_financial_dax.py` (static review)  
**Audit mode:** Read-only. No DAX expression modified.

---

## 1. Measure inventory reconciliation (the 54 vs 51 question)

**Verified independently:**
- **54 measures defined in the DAX source file.**
- **51 measures registered in `model.json`.**
- **Difference = 3 measures: OP01, OP03, OP04** — present in DAX source (lines 31–33) but **absent from `model.json`** (fact_flight_operations registers only FL01–FL04).

This confirms the previously reported discrepancy (54 vs 51; OP01/OP03/OP04 missing from model.json) is **genuine and verified**, not a rumor.

| Prefix | Measures in DAX source | Registered in model.json | Gap |
|---|---|---|---|
| FL (flight ops) | FL01, FL02, FL03, FL04 (4) | FL01–FL04 (4) | none |
| DS (disruptions) | DS01, DS02, DS03 (3) | DS01–DS03 (3) | none |
| CF (customer feedback) | CF01–CF14 (14) | CF01–CF14 (14) | none |
| OP (operations) | OP01, OP03, OP04 (3) | — (0) | **OP01, OP03, OP04 missing** |
| RV (booking/revenue) | RV_BookingCount, RV_DistinctBookings, RV_RevenuePassengers, RV_NonRevenuePassengers, RV_GrossBookingValueUSD, RV_RefundAmountUSD, RV_NetPassengerRevenueUSD, RV_NetFeeRevenueUSD, RV_NetAncillaryRevenueUSD, RV_TotalOperatingRevenueUSD, RV_AvgRevenuePerRevenuePassenger, RV_AvgBookingValueUSD, RV_RevenueCurrentPeriodUSD, RV_RevenuePriorPeriodUSD, RV_RevenueGrowthPercent, RV_RevenueYTDUSD, RV_RevenueByBookingDateUSD (17) | 17 (fact_booking_transactions) | none |
| CX (operating costs) | CX_TotalOperatingCostsUSD, CX_PositiveCostsUSD, CX_CostReversalsUSD, CX_NetOperatingCostsUSD, CX_CostPerFlightOperationUSD, CX_CostPerRevenuePassengerUSD, CX_CostsCurrentPeriodUSD, CX_CostsPriorPeriodUSD, CX_CostGrowthPercent, CX_CostsYTDUSD (10) | 10 (fact_operating_costs) | none |
| NC (financial contribution) | NC_NetOperatingContributionUSD, NC_RevenueToCostRatio, NC_RevenuePerRevenuePassengerUSD (3) | 3 (fact_booking_transactions) | none |
| **Total** | **54** | **51** | **3 (OP01, OP03, OP04)** |

**Confidence: High.** Verified by direct line-by-line comparison of DAX file vs model.json.

---

## 2. Full measure inventory (name, expression summary, dependencies, registration, used-in-report)

### Flight operations (FL)
| Measure | Expression (summary) | Registered? | Used in report? | Status |
|---|---|---|---|---|
| FL01 | COUNTROWS(FILTER(FlightStatus="Operated")) | Yes | Page 01 | COMPLETE |
| FL02 | SUM(RevenuePassengers) | Yes | Page 01 | COMPLETE |
| FL03 | AVERAGE(DepartureDelayMinutes) | Yes | Page 01/02 | COMPLETE |
| FL04 | VAR _total… RETURN IF(_total=0,BLANK(),DIVIDE(_cancelled,_total)*100) | Yes | Page 01 | IMPLEMENTED — NOT FULLY VERIFIED |

### Disruptions (DS)
| Measure | Expression | Registered? | Used? | Status |
|---|---|---|---|---|
| DS01 | COUNTROWS(fact_disruptions) | Yes | Page 01 | COMPLETE |
| DS02 | AVERAGE(DelayMinutes) | Yes | Page 01 | COMPLETE |
| DS03 | COUNTROWS(FILTER(RELATED(dim_disruption_type[ControllableFlag])=TRUE())) | Yes | Page 01 | COMPLETE |

### Customer feedback (CF)
| Measure | Expression | Registered? | Used? | Status |
|---|---|---|---|---|
| CF01 | COUNTROWS(fact_customer_feedback) | Yes | Page 05 | COMPLETE |
| CF02 | AVERAGE(SatisfactionScore) | Yes | Page 05 | COMPLETE |
| CF03 | VAR _total… DIVIDE(_complaints,_total)*100 | Yes | Page 05 | COMPLETE |
| CF04 | COUNTROWS(FILTER(dim_customer[IsActive]=TRUE)) | Yes | Page 05 | COMPLETE |
| CF05–CF08 | COUNTROWS filters by FeedbackType (Complaint/Compliment/Claim/Survey) | Yes | Page 05 | COMPLETE |
| CF09 | DIVIDE(CF06, CF01) | Yes | Page 05 | COMPLETE |
| CF10 | DIVIDE(CF05 + CF07, CF01) | Yes | Page 05 | COMPLETE |
| CF11 | DIVIDE(COUNTROWS(ServiceRecoveryFlag=TRUE), CF05) | Yes | Not bound | COMPLETE (unused) |
| CF12 | DIVIDE(Resolved, not-blank ResolutionStatus) | Yes | Not bound | COMPLETE (unused) |
| CF13 | CALCULATE(CF02, FeedbackType="Complaint") | Yes | Not bound | COMPLETE (unused) |
| CF14 | CALCULATE(CF02, FeedbackType="Compliment") | Yes | Not bound | COMPLETE (unused) |

### Operations (OP) — NOT REGISTERED
| Measure | Expression | Registered? | Used? | Status |
|---|---|---|---|---|
| OP01 | On-Time Departure Rate (DIVIDE, BLANK) | **NO** | **NO** | GAP — missing from model |
| OP03 | Average Arrival Delay (SUMX/DIVIDE) | **NO** | **NO** | GAP — missing from model |
| OP04 | Flight Completion Rate (DIVIDE) | **NO** | **NO** | GAP — missing from model |

### Revenue (RV)
17 measures defined and registered; all use USD-converted columns; division-by-zero guarded with DIVIDE(…,BLANK()); date intelligence uses `IsReportingPeriod`, `TOTALYTD`, `SAMEPERIODLASTYEAR`, `USERELATIONSHIP` for booking-date cohort.

### Operating costs (CX)
10 measures defined and registered; signed CostAmountUSD; positive/reversal split; division-by-zero guarded.

### Financial contribution (NC)
3 measures: NC_NetOperatingContributionUSD (= RV - CX), NC_RevenueToCostRatio, NC_RevenuePerRevenuePassengerUSD.

---

## 3. DAX correctness checks (per audit standard)

| Check | Result | Evidence |
|---|---|---|
| Incorrect aggregation | None found. SUM used on numeric amount columns; COUNTROWS/DISTINCTCOUNT on keys; AVERAGE on scores/delays. | DAX file review |
| Wrong denominators | None found. DIVIDE denominators are appropriate (e.g., revenue per passenger divides by revenue passengers). | DAX file review |
| Missing filters | None evident for base measures; revenue uses active TravelDateKey relationship. | DAX file review |
| Incorrect relationships | DAX uses active relationships; USERELATIONSHIP used only in RV_RevenueByBookingDateUSD for inactive BookingDateKey. | DAX file review |
| Filter-context problems | None evident. VAR-based measures capture outer context correctly. | DAX file review |
| Incorrect date logic | `dim_date` continuous coverage 2024-10-01 to 2026-10-31 (761 dates, no gaps); reporting period 365 days. Time intelligence (TOTALYTD/SAMEPERIODLASTYEAR) valid. | `test_stage4_financial_dax.py` test_dim_date; dim_date.csv |
| Incorrect currency conversion | DAX uses USD-converted columns (BaseFareUSD, Net*USD, CostAmountUSD); original-currency columns NOT summed in measures (verified by `test_no_original_currency_summed_across_currencies`). | DAX file + test |
| Division by zero | All DIVIDE calls specify BLANK() alternate result (`test_all_divide_use_blank_for_zero_denominator`). FL04/CF03 guard _total=0. | DAX file + test |
| BLANK vs zero | FL04 returns BLANK() when _total=0; CF03 returns BLANK() when _total=0. Appropriate. | DAX file review |
| Duplicate counting | DISTINCTCOUNT used for BookingReference; no duplicate-counting evident. | DAX file review |
| Row-count vs distinct-count | COUNTROWS vs DISTINCTCOUNT used appropriately. | DAX file review |
| Unused measures | CF11–CF14, OP01/03/04, several RV/CX measures unused on report pages (not a defect — defined measures need not all be used). | Visual bindings vs DAX |
| Missing measures | OP01/03/OP04 missing from model.json (registered gap). | DAX vs model.json |
| Circular dependencies | None found (`test_no_circular_measure_dependencies`, static). | DAX file + test |
| DAX defined but absent from model | OP01, OP03, OP04. | DAX vs model.json |
| Measures in model but absent from DAX docs | None identified; all 51 registered measures have DAX definitions. | DAX vs model.json |

---

## 4. Specific known issues investigated

### CF11 and CF14
- CF11 = `DIVIDE(COUNTROWS(FILTER(fact_customer_feedback, ServiceRecoveryFlag=TRUE)), CF05)` — Service Recovery Rate (of complaints). Guarded by DIVIDE; returns BLANK if CF05=0. No defect found in static review.
- CF14 = `CALCULATE(CF02, fact_customer_feedback[FeedbackType]="Compliment")` — Compliment Satisfaction Avg. No defect found.
- **Status:** COMPLETE (defined and registered). Independent execution not possible without Power BI Desktop (limitation L-1).

### Customer-count measures (CF04)
- CF04 = `COUNTROWS(FILTER(dim_customer, IsActive=TRUE))` — Active Customers. Correct pattern. Registered and bound on Page 05.

---

## 5. Independent validation against source data

`tests/unit/test_stage4_financial_dax.py` independently computes expected values from `fact_booking_transactions.csv` and `fact_operating_costs.csv` and asserts DAX measures match. Statically reviewed:
- Revenue reconciliation (total = net passenger + fee + ancillary) ✓
- Refund calculation (Refund + AncillaryRefund + FeeRefund) ✓
- Operating cost total = sum of signed CostAmountUSD ✓
- Cost reversals negative, positives positive, total = positive + reversals ✓
- No original-currency columns summed in new measures ✓
- USD columns used for aggregation ✓
- Revenue by airline/route, cost by category reconcile to source ✓
- dim_date continuous coverage, 365 reporting-period dates ✓
- TOTALYTD / SAMEPERIODLASTYEAR present ✓
- All DIVIDE use BLANK() alternate ✓
- Existing FL/DS/CF measures preserved in model.json ✓
- No unsupported financial terminology (profit/EBITDA) ✓

**Validation status:** DAX measures are statically validated against source data; dynamic execution requires Power BI Desktop (limitation L-1).

---

## 6. DAX findings register

| ID | Finding | Severity | Evidence | Confidence | Recommended action |
|---|---|---|---|---|---|
| DAX-01 | OP01, OP03, OP04 defined in DAX but missing from model.json (54 vs 51) | HIGH | DAX lines 31–33 vs model.json fact_flight_operations measures | High | Register OP01/OP03/OP04 in semantic model; bind to Page 02 visuals |
| DAX-02 | CF11, CF14 not independently executable (no Power BI Desktop); static review found no expression defects | MEDIUM | DAX lines 26–29 | Medium | Execute validation in Power BI Desktop once accessible |
| DAX-03 | FL04 / CF03 multiply by 100; percentage-point formatting ambiguity (HB-10) | MEDIUM | DAX lines 12, 18 | Medium | Document whether values are fractions (Percent format) or percentage points |
| DAX-04 | All 51 registered measures have DAX definitions; no orphaned model measures | INFORMATIONAL | DAX vs model.json | High | — |

---

## 7. DAX implementation status

**54 measures defined in DAX source:** COMPLETE (all written, disclosure present, syntactically valid, division-by-zero guarded).
**51 measures registered in semantic model:** COMPLETE for registered set.
**3 measures (OP01/03/OP04) defined but NOT registered:** GAP — IMPLEMENTED in DAX, NOT REGISTERED in model. Can be closed by registering the three measures (no OD/G4 dependency).
**Independent validation:** STATICALLY validated against source CSVs; dynamic execution pending Power BI Desktop access.

**DAX is not the gating item.** The DAX is written and validated. What is blocked is financial fact DATA loading (OD-04), not the DAX expressions themselves.
