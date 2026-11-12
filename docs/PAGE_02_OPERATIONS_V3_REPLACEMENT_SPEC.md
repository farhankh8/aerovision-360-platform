# PAGE_02_OPERATIONS_V3_REPLACEMENT_SPEC.md

# AEROVISION 360 — Page 02: Visual 3 Replacement — Block Minutes by Airline/Month

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Page:** Page 02 — Operations Performance
**Visual ID:** V3 (replacement for Turnaround Time — NOT FEASIBLE)
**Replacement:** Block Minutes by Airline/Month
**Status:** IMPLEMENTATION-READY SPECIFICATION — NOT YET BUILT
**Prepared:** 2026-11-06
**Verified against source:** data/03_curated/fact_flight_operations.csv (5,000 rows)
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Reason for Replacement

The original V3 (Turnaround Time) was audited and determined **NOT FEASIBLE** because the source data lacks an aircraft flight sequence or rotation column. A naive sort-by-arrival approach produced meaningless multi-day gaps (average 39,745 minutes / ~27.6 days). No synthetic turnaround values were generated.

**Replacement rationale:** `BlockMinutes` exists in `fact_flight_operations`, is directly related to flight operations, can be analysed by airline and month, requires no fabricated data, and strengthens the Operations Performance page.

---

## 2. Data Verification — BlockMinutes

### 2.1 Field Profile

| Attribute | Value |
|---|---|
| Field name | `BlockMinutes` |
| Table | `fact_flight_operations` |
| Column index | 20 (0-based) |
| Data type | Integer (minutes) |
| Total rows | 5,000 |
| Valid (non-null) | 4,776 |
| Null | 224 (all cancelled flights) |
| Negative values | 0 |
| Zero values | 0 |
| Sum (all valid) | 1,503,155 minutes |
| Average | 314.73 minutes |

### 2.2 Null Pattern

| Status | BlockMinutes Null? | Count |
|---|---|---|
| Operated | No | 4,776 (all valid) |
| Cancelled | Yes | 224 (all null) |

**Conclusion:** BlockMinutes is null exactly when `CompletionFlag = FALSE` / `CancellationFlag = TRUE`. No operated flight is missing BlockMinutes. This is clean, expected behavior.

### 2.3 Aggregation Validation

| Aggregation Dimension | Sum (minutes) |
|---|---|
| By airline (completed flights) | 1,503,155 |
| By month (completed flights) | 1,503,155 |
| Difference | 0 (perfect reconciliation) |

---

## 3. Visual Specification — V3 Replacement

### 3.1 Visual Definition

| Attribute | Specification |
|---|---|
| Visual type | Stacked column chart |
| Title | Block Minutes by Airline/Month |
| X-axis | `DimDate[YearMonth]` (monthly, ascending chronologically) |
| Y-axis | Block minutes (SUM of `fact_flight_operations[BlockMinutes]`) |
| Legend | `DimAirline[AirlineName]` (10 airlines) |
| Values measure | `SUM ( fact_flight_operations[BlockMinutes] )` — no new measure needed; use existing column directly |
| Filter context | Completed flights only (`CompletionFlag = TRUE`) — BlockMinutes is null for cancelled, so SUM automatically excludes them |
| Sort | X-axis ascending by YearMonth; legend in airline roster order |
| Data labels | Off (too many segments for labels) |
| Colours | 10 distinct colours from design system palette (max 5 data colours per visual rule — note: 10 airlines exceeds the 5-colour guideline; see Limitations) |
| Tooltip | Airline, month, block minutes, disclosure |
| Status | AVAILABLE — all source columns verified |

### 3.2 Measure Definition (No New DAX Required)

No new DAX measure is required. Use the existing column directly in the visual:

```
Values: SUM ( fact_flight_operations[BlockMinutes] )
```

BlockMinutes is null for cancelled flights, so SUM automatically excludes them — no additional filter needed.

If a named measure is desired for consistency:

```DAX
Block Minutes = SUM ( fact_flight_operations[BlockMinutes] )
```

### 3.3 Expected Results (Full Dataset)

| Month | Block Minutes (verified from CSV) |
|---|---|
| 2025-10 | 136,346 |
| 2025-11 | 114,617 |
| 2025-12 | 119,545 |
| 2026-01 | 123,741 |
| 2026-02 | 119,127 |
| 2026-03 | 143,487 |
| 2026-04 | 118,272 |
| 2026-05 | 124,246 |
| 2026-06 | 127,528 |
| 2026-07 | 125,725 |
| 2026-08 | 130,893 |
| 2026-09 | 118,844 |
| 2026-10 | 784 (partial month — reporting period ends 2026-09-30) |

**Total:** 1,503,155 minutes

**Note:** 2026-10 has only 784 minutes because the reporting period ends 2026-09-30; any October 2026 rows are outside the reporting period and should be filtered out by the date range slicer.

---

## 4. Relationship and Filter Context

| Relationship | Role | Status |
|---|---|---|
| `DimDate[DateKey] → fact_flight_operations[ScheduledDepartureDateKey]` | Date filtering (departure date role) | Active, 1:* |
| `DimAirline[AirlineKey] → fact_flight_operations[AirlineKey]` | Airline filtering | Active, 1:* |

Both relationships are existing and active. No new relationships required. No ambiguous filter paths.

### 4.1 Slicer Interactions

| Slicer | Effect on V3 |
|---|---|
| Airline slicer | Filters to selected airline(s); stacked columns show only selected airlines' block minutes |
| Flight Date Range slicer | Filters to selected date range; monthly columns show only months in range |

Clicking an airline in V5 (Flight Operations by Airline) should cross-filter V3 to show that airline's block minutes by month.

---

## 5. Layout Positioning

V3 replaces Turnaround Time in the middle row:

```
+---------+---------+---------+
|  V1     |  V2     |  V3     |
| On-Time | Flights | Block   |
| Trend   | by Status| Minutes |
| (combo) | (donut) | by Airline|
|         |         | /Month  |
|         |         | (stacked|
|         |         |  col)   |
+---------+---------+---------+
```

Position: Middle row, rightmost visual (same position as the original V3). No layout changes required.

---

## 6. Number Formatting

| Attribute | Specification |
|---|---|
| Display unit | None |
| Decimal places | 0 |
| Format | `#,##0` |
| Blank behavior | Em dash (—), never zero |

---

## 7. Limitations

| # | Limitation | Impact |
|---|---|---|
| V3-L1 | 10 airlines exceed the design system's "max five data colours per visual" rule | Use a colour palette with distinguishable hues; consider grouping smaller airlines or using a sequential colour scale. Alternatively, use a 100% stacked column to show proportion of block minutes. |
| V3-L2 | 2026-10 shows only 784 minutes (partial month outside reporting period) | The date range slicer default (2025-10-01 to 2026-09-30) will exclude this. Label the axis as reporting period only. |
| V3-L3 | BlockMinutes measures time in the air (block-to-block), not ground time | This is not turnaround time. Do not label it as turnaround. Title clearly states "Block Minutes". |
| V3-L4 | SUM of BlockMinutes across airlines is additive; averages would be misleading | Use SUM only. Do not display average block minutes per airline/month without context. |

---

## 8. Validation Checks

| Check ID | Expected Result | Validation Method |
|---|---|---|
| V3-V1 | Total block minutes = 1,503,155 | SUM of all valid BlockMinutes in CSV |
| V3-V2 | No negative block minutes | All values >= 0 (verified: 0 negative) |
| V3-V3 | Cancelled flights excluded automatically | BlockMinutes null for all 224 cancelled flights |
| V3-V4 | Airline totals reconcile | Sum by airline = Sum by month = 1,503,155 |
| V3-V5 | Monthly totals reconcile with slicer | Selecting a date range updates columns accordingly |
| V3-V6 | Airline filtering works | Selecting one airline shows only that airline's segments |

---

## 9. Documents to Update

| Document | Section | Change |
|---|---|---|
| `PAGE_02_OPERATIONS_VISUAL_SPECIFICATION.md` | Section 3 (Middle Row) | Replace V3 Turnaround Time with V3 Block Minutes by Airline/Month |
| `PAGE_02_OPERATIONS_VISUAL_SPECIFICATION.md` | Section 6 (Number Formatting) | Remove "Turnaround minutes" row; keep "Block minutes" row |
| `PAGE_02_OPERATIONS_VISUAL_SPECIFICATION.md` | Section 9 (Visuals Not Implementable) | Remove V3 entry; add replacement note |
| `PAGE_02_OPERATIONS_QA_PLAN.md` | QA Test Matrix | Replace T-P02-24 (Turnaround Time) with Block Minutes validation tests |
| `PAGE_02_OPERATIONS_DATA_AUDIT.md` | Visual Availability | Update V3 status from MISSING to AVAILABLE (replacement) |

---

## 10. Implementation Instructions (Power BI Desktop)

1. **Do not modify the PBIX programmatically.** Add the visual manually in Power BI Desktop.
2. **No new DAX measure required.** Use `fact_flight_operations[BlockMinutes]` directly in the Values well with SUM aggregation.
3. **Create a stacked column chart:**
   - Axis: `DimDate[YearMonth]`
   - Values: `fact_flight_operations[BlockMinutes]` (SUM)
   - Legend: `DimAirline[AirlineName]`
4. **Set formatting:**
   - Title: "Block Minutes by Airline/Month"
   - Values format: `#,##0` (0 decimal places)
   - X-axis: ascending chronological
   - Data labels: Off
5. **Configure interactions:**
   - Respond to Airline slicer and Flight Date Range slicer
   - Cross-filter from V5 (airline click)
6. **Validate:** Confirm total = 1,503,155 minutes at full dataset.

---

## 11. Next Steps

1. Update `PAGE_02_OPERATIONS_VISUAL_SPECIFICATION.md` with the V3 replacement details.
2. Update `PAGE_02_OPERATIONS_QA_PLAN.md` with Block Minutes validation tests.
3. Build the visual in Power BI Desktop.
4. Validate against expected results (Section 8).

---

**End of specification.** This document is implementation-ready. No PBIX, source data, DAX, or report has been modified.
