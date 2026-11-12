# PAGE_02_OPERATIONS_QA_PLAN.md

# AEROVISION 360 — Page 02 Operations Performance: QA Plan

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Page:** Page 02 — Operations Performance
**Status:** PLANNED — NO TESTS EXECUTED; NO REPORT RENDERED
**Prepared:** 2026-11-06
**Companion:** `docs/IMPLEMENTATION_QA_BLUEPRINT.md`, `docs/PAGE_02_OPERATIONS_DATA_AUDIT.md`, `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md`, `docs/PAGE_02_OPERATIONS_VISUAL_SPECIFICATION.md`
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Test-State Model

This QA plan uses the canonical status vocabulary from `docs/IMPLEMENTATION_QA_BLUEPRINT.md`:

| Status | Meaning | Can release? |
|---|---|---|
| PLANNED | Test designed; code/data/report not available | No |
| IMPLEMENTED | Test code or manual procedure exists; not executed | No |
| EXECUTED | Test was run; evidence not reviewed/accepted | No |
| PASSED | Executed with evidence; reviewer accepted | Yes, if all gates pass |
| FAILED | Executed; expected result not met | No |
| BLOCKED | Cannot execute because prerequisite is absent | No |

**Current state:** All tests in this plan are PLANNED or BLOCKED. No test is IMPLEMENTED, EXECUTED, PASSED, or FAILED.

A test cannot be PASSED without a named reviewer and evidence. A document review is not a data test. A schema parse is not a reconciliation.

---

## 2. QA Test Matrix

| Test ID | Test objective | Expected result | Actual result | Pass/Fail | Evidence | Defect ref |
|---|---|---|---|---|---|---|
| T-P02-01 | Airline slicer — single airline | All KPIs and visuals reflect only the selected airline's flights | — | PLANNED | — | — |
| T-P02-02 | Airline slicer — multiple airlines | All KPIs and visuals reflect the union of selected airlines | — | PLANNED | — | — |
| T-P02-03 | Airline slicer — all airlines (default) | Values match full-dataset reconciliation (5,000 flights) | — | PLANNED | — | — |
| T-P02-04 | Date range slicer — full range | Values cover 2025-10-01 to 2026-09-30 | — | PLANNED | — | — |
| T-P02-05 | Date range slicer — restricted range | Values cover only selected dates; monthly trend shows subset | — | PLANNED | — | — |
| T-P02-06 | Monthly trend — departure OTP | Blue columns show monthly departure OTP %; reconciles to per-month OP01 | — | PLANNED | — | — |
| T-P02-07 | Monthly trend — arrival OTP line | Dark line shows monthly arrival OTP %; reconciles to per-month arrival OTP | — | PLANNED | — | — |
| T-P02-08 | Route ranking — Top 5 | Table shows exactly 5 routes, sorted descending by flight count | — | PLANNED | — | — |
| T-P02-09 | Airline ranking — descending | Horizontal bar sorted descending by flight count; all 10 airlines shown | — | PLANNED | — | — |
| T-P02-10 | Flight-status distribution | Donut: On Time + Delayed + Cancelled = 100%; centre shows total | — | PLANNED | — | — |
| T-P02-11 | Status distribution by month | 100% stacked column; each month sums to 100% | — | PLANNED | — | — |
| T-P02-12 | KPI 1 — OP01 On-Time Departure Rate | 1,485 / 4,776 = 31.09% at full dataset | — | PLANNED | — | — |
| T-P02-13 | KPI 2 — OP02 Avg Departure Delay | 43.42 min (matches FL03) | — | PLANNED | — | — |
| T-P02-14 | KPI 3 — OP03 Avg Arrival Delay | 106.65 min at full dataset | — | PLANNED | — | — |
| T-P02-15 | KPI 4 — OP04 Completion Rate | 4,776 / 5,000 = 95.52% | — | PLANNED | — | — |
| T-P02-16 | KPI 5 — OP05 Aircraft Utilization | BLOCKED — no `ref_aircraft_availability.csv`; cannot measure | — | BLOCKED | Missing data | DQ-08 |
| T-P02-17 | Filter interactions — airline click on V5 | V1, V2, V4, V6 filter; KPI cards unchanged unless via slicer | — | PLANNED | — | — |
| T-P02-18 | Blank data behaviour | BLANK ratios display as em dash, not zero | — | PLANNED | — | — |
| T-P02-19 | Single-airline selection | All values recompute for one airline; no division-by-zero errors | — | PLANNED | — | — |
| T-P02-20 | Multiple-airline selection | All values recompute for selected airlines | — | PLANNED | — | — |
| T-P02-21 | Full date range | All data visible; monthly trend shows all 12 reporting months | — | PLANNED | — | — |
| T-P02-22 | Restricted date range | Only selected dates visible; KPIs recompute | — | PLANNED | — | — |
| T-P02-23 | Totals reconciliation | V2 donut total = 5,000; V2 categories sum to total; V6 monthly = 100% | — | PLANNED | — | — |
| T-P02-24 | Block Minutes by Airline/Month | Stacked column shows block minutes by month, stacked by airline; total = 1,503,155 min | — | PLANNED | — | — |
| T-P02-25 | Disclosure visibility | "Synthetic Simulation — Not Actual Airline Performance" visible on page and tooltips | — | PLANNED | — | T-79 dependency |
| T-P02-26 | Negative delay handling | Early departures (negative delay) counted as on-time if <= 15 min; included in averages | — | PLANNED | — | DQ-02, DQ-03 |
| T-P02-27 | Cancelled-flight treatment | Cancelled flights excluded from OTP and delay averages; included in completion-rate denominator | — | PLANNED | — | DQ-01 |

---

## 3. KPI-Specific Validation Tests

### T-P02-12: OP01 On-Time Departure Rate
| Step | Action | Expected |
|---|---|---|
| 1 | Select all airlines, full date range | OP01 = 31.09% |
| 2 | Select one airline | OP01 recomputes for that airline only |
| 3 | Select date range with no flights | OP01 = BLANK (em dash) |
| 4 | Independent CSV recalc | 1,485 on-time departures / 4,776 operated with valid delay = 31.09% |

### T-P02-13: OP02 Average Departure Delay
| Step | Action | Expected |
|---|---|---|
| 1 | Select all airlines, full date range | OP02 = 43.42 min (matches FL03) |
| 2 | Verify cancelled flights excluded | No cancelled flights in average (their delays are blank) |
| 3 | Verify negative delays included | 997 negative departure delays remain in average |

### T-P02-14: OP03 Average Arrival Delay
| Step | Action | Expected |
|---|---|---|
| 1 | Select all airlines, full date range | OP03 = 106.65 min |
| 2 | Verify cancelled flights excluded | Their arrival delays are blank |
| 3 | Independent CSV recalc | SUM(ArrivalDelayMinutes for operated) / 4,776 |

### T-P02-15: OP04 Flight Completion Rate
| Step | Action | Expected |
|---|---|---|
| 1 | Select all airlines, full date range | OP04 = 95.52% |
| 2 | Verify OP04 + FL04 = 100% | 95.52% + 4.48% = 100.00% |
| 3 | Verify cancelled flights in denominator | 224 cancelled included in 5,000 total |

### T-P02-16: OP05 Aircraft Utilization
| Step | Action | Expected |
|---|---|---|
| 1 | Attempt to display OP05 | BLOCKED — measure cannot be implemented (missing `ref_aircraft_availability.csv`) |
| 2 | Document missing field | `ref_aircraft_availability[AircraftKey, CalendarDateKey, AvailableHours, AvailabilityStatus, ReferenceVersion]` |

---

## 4. Data-Quality Test Cases

| Test ID | Data-quality rule | Expected | Linked DQ finding |
|---|---|---|---|
| T-DQ-01 | No cancelled flight has actual departure | 0 cancelled flights with ActualDepartureTimestampUTC | DQ-01 |
| T-DQ-02 | No operated flight missing actual departure | 0 operated flights with null ActualDepartureTimestampUTC | DQ-01 |
| T-DQ-03 | Negative departure delays are valid | 997 negative values exist; treated as early departures | DQ-02 |
| T-DQ-04 | Negative arrival delays are valid | 1,369 negative values exist; remain in averages | DQ-03 |
| T-DQ-05 | Flight statuses reconcile | Operated (4,776) + Cancelled (224) = 5,000 total | DQ-05 |
| T-DQ-06 | No duplicate FlightOperationKey | All 5,000 keys unique | — |
| T-DQ-07 | Date range consistency | All flights within 2025-10-01 to 2026-09-30 reporting period | — |
| T-DQ-08 | Airline referential integrity | All 10 airline keys in fact exist in dim_airline | — |
| T-DQ-09 | BlockMinutes completeness | All 4,776 operated flights have valid BlockMinutes; 224 cancelled flights have null | Verified: 4,776 valid, 224 null |
| T-DQ-10 | BlockMinutes non-negative | All BlockMinutes values >= 0 | Verified: 0 negative values |
| T-DQ-11 | BlockMinutes reconciliation | Sum by airline = Sum by month = 1,503,155 | Verified: 1,503,155 both dimensions |

---

## 5. Blocked Tests and Missing Prerequisites

| Test ID | Blocker | Required to unblock | Owner decision needed? |
|---|---|---|---|
| T-P02-16 (OP05) | `ref_aircraft_availability.csv` absent | Create/populate aircraft availability reference table; add to semantic model; implement K-13 per DAX_KPI_CATALOGUE | Yes — OD-10 availability assumption pending |
| T-P02-24 (V3 Block Minutes) | None — all data verified | N/A — ready for implementation | No |

---

## 6. Entry and Exit Criteria

**Entry criteria (before test execution):**
1. OP01, OP03, OP04 measures implemented in semantic model
2. FL03 (OP02) verified and present
3. Report page created per `PAGE_02_OPERATIONS_VISUAL_SPECIFICATION.md`
4. PBIX opened in Power BI Desktop; model refreshed from `data/03_curated/`
5. Named QA reviewer assigned

**Exit criteria (for test to be PASSED):**
1. Test executed with recorded evidence (screenshot, CSV recalc, or DAX query result)
2. Actual result matches expected result within documented tolerance
3. Reviewer signs off
4. Disclosure visible on page and in all tooltips

**Exit criteria (for page to be release-ready):**
1. All non-blocked tests PASSED
2. All blocked tests documented with missing prerequisites
3. No critical or high-severity defects open
4. Disclosure T-79 passes
5. Page 01 unchanged and unaffected

---

## 7. Evidence Requirements

For every PASSED test, evidence must include:
- Test ID and date
- Reviewer name
- Screenshot of visual or measure value
- Independent recalculation (CSV or SQL query) showing expected vs actual
- Filter state (airline selection, date range)
- Disclosure visible in screenshot

---

## 8. Known Gaps in QA Coverage

| Gap | Reason |
|---|---|
| T-37 zero-denominator runtime test | BLOCKED — requires Power BI runtime execution; no rendered report |
| T-46 report KPI reconciliation | BLOCKED — no rendered report exists |
| T-79 disclosure test | BLOCKED — no rendered report exists |
| Aircraft utilization runtime validation | BLOCKED — OP05 not implementable (missing data) |
| Turnaround time validation | BLOCKED — V3 not implementable (missing data) |

---

## 9. Recommended QA Execution Sequence

1. Verify data-quality tests (T-DQ-01 through T-DQ-08) against CSVs — can run now
2. Implement OP01, OP03, OP04 measures; verify FL03 (OP02)
3. Create report page per visual specification
4. Execute KPI validation tests (T-P02-12 through T-P02-15)
5. Execute visual tests (T-P02-01 through T-P02-11, T-P02-17 through T-P02-23)
6. Document blocked tests (T-P02-16, T-P02-24) with missing prerequisites
7. Obtain reviewer sign-off on all PASSED tests
8. Confirm Page 01 is unchanged

---

**End of QA plan.** This document is test-plan evidence only. No test has been executed, no report has been rendered, and no result is claimed PASS.
