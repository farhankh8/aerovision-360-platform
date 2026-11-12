# PAGE_02_OPERATIONS_VISUAL_SPECIFICATION.md

# AEROVISION 360 — Page 02 Operations Performance: Visual Specification

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Page:** Page 02 — Operations Performance
**Status:** PROPOSED — NOT IMPLEMENTED; NO REPORT PAGE CREATED
**Prepared:** 2026-11-06
**Visual acceptance target:** Reference dashboard specification (Operations Performance page)
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Page Header and Chrome

| Element | Specification |
|---|---|
| Page name | Operations Performance |
| Page subtitle | Flight Operations, On-Time Performance, Turnaround & Capacity Utilization |
| Branding | AEROVISION 360 |
| Sidebar | Dark navy (existing Page 01 design language) |
| Icons | Existing airplane icon; airport/aircraft panoramic banner |
| Slicers | Airline (multi-select, all 10 airlines); Flight Date Range (date range, default = reporting period 2025-10-01 to 2026-09-30) |
| Layout canvas | 16:9, consistent with Page 01 |
| Disclosure | "Synthetic Simulation — Not Actual Airline Performance" visible on page |

**Design language:** Preserve Page 01's dark navy sidebar, branding, banner, filter bar, and visual style. No deviation from established design system.

---

## 2. KPI Row — Five Cards

| Card | KPI ID | Measure | Format | Data source | Treatment |
|---|---|---|---|---|---|
| KPI 1 | OP01 | [OP01 On-Time Departure Rate] | `0.0%` | fact_flight_operations + OnTimeFlag | New measure; 15-minute threshold |
| KPI 2 | OP02 | [FL03 Average Departure Delay] (reuse) | `0.0 min` | fact_flight_operations[DepartureDelayMinutes] | Reuse existing FL03 |
| KPI 3 | OP03 | [OP03 Average Arrival Delay] | `0.0 min` | fact_flight_operations[ArrivalDelayMinutes] | New measure |
| KPI 4 | OP04 | [OP04 Flight Completion Rate] | `0.0%` | fact_flight_operations[CompletionFlag] | New measure |
| KPI 5 | OP05 | [Aircraft Utilization] | `0.00 hrs/day` | ref_aircraft_availability (MISSING) | NOT IMPLEMENTED — missing data |

**Card specification (per POWER_BI_DASHBOARD_SPECIFICATION Section 2.5):**
- Title: Business name only (KPI ID in tooltip, not card title)
- Value: Formatted per DAX catalogue; BLANK displays as em dash, not zero
- Context: Comparison label only when valid comparison exists; no invented target
- Subtext: Denominator/response count for ratios; unit for volumes
- Sparkline: Optional only if same measure and valid time axis
- Interaction: KPI cards respond to page slicers only; not cross-filtered by other visuals
- Tooltip: Custom tooltip with definition, numerator, denominator, date role, disclosure

**KPI card placement:** Horizontal row across top of content area, 5 equal-width cards.

---

## 3. Middle Row — Three Visuals

### Visual 1: On-Time Performance Trend

| Attribute | Specification |
|---|---|
| Visual type | Combo chart: clustered column + line |
| Title | On-Time Performance Trend |
| X-axis | DimDate[YearMonth] (monthly, sorted chronologically) |
| Left Y-axis (columns) | [OP01 On-Time Departure Rate] — percentage format `0.0%` |
| Right Y-axis (line) | Arrival on-time percentage — computed from OP03 logic on arrival basis |
| Column color | Blue (departure OTP) |
| Line color | Dark (arrival OTP) |
| Data labels | On (percentage, 1 decimal) |
| Tooltip | Month, departure OTP %, arrival OTP %, disclosure |
| Sort | Ascending by YearMonth |
| Interactions | Responds to airline, date range slicers |
| Status | DERIVABLE — arrival OTP requires arrival-date logic (USERELATIONSHIP or computed arrival on-time flag) |

**Arrival on-time calculation for line series:**
- Derived from fact_flight_operations where `CompletionFlag = TRUE` and `ArrivalDelayMinutes <= 15` and `NOT ISBLANK(ArrivalDelayMinutes)`
- Denominator: operated flights with valid arrival delay
- Date role: arrival date (requires USERELATIONSHIP with ScheduledArrivalDateKey)

---

### Visual 2: Flights by Status

| Attribute | Specification |
|---|---|
| Visual type | Donut chart |
| Title | Flights by Status |
| Legend field | Computed status category: On Time / Delayed / Cancelled |
| Values | Count of flights |
| Centre label | Total flights (COUNTROWS fact_flight_operations) |
| Data labels | Percentage labels on segments |
| Legend position | Right |
| Sort | Descending by count |
| Colours | On Time = green, Delayed = amber, Cancelled = red (per design system: positive green, attention amber, negative red) |
| Interactions | Responds to airline, date range slicers |
| Status | AVAILABLE — but only 2 native statuses exist (Operated, Cancelled); "Delayed" must be derived |

**Status category logic (DAX or calculated column):**
```
Status Category =
SWITCH (
    TRUE (),
    fact_flight_operations[CancellationFlag] = TRUE, "Cancelled",
    fact_flight_operations[OnTimeFlag] = TRUE, "On Time",
    "Delayed"
)
```

**Expected values (full dataset):**
| Category | Count | % of total |
|---|---|---|
| On Time | 1,485 | 29.70% |
| Delayed | 3,291 | 65.82% |
| Cancelled | 224 | 4.48% |
| Total | 5,000 | 100.00% |

**Mutually exclusive check:** Operated + Cancelled = 5,000 (all records). On Time + Delayed = 4,776 (all operated). Totals reconcile.

---

### Visual 3: Block Minutes by Airline/Month (Replacement for Turnaround Time)

**Note:** The original Turnaround Time visual was audited and determined NOT FEASIBLE (see `docs/PAGE_02_TURNAROUND_TIME_FEASIBILITY_AUDIT.md`). It is replaced by Block Minutes by Airline/Month, which uses existing verified data.

| Attribute | Specification |
|---|---|
| Visual type | Stacked column chart |
| Title | Block Minutes by Airline/Month |
| X-axis | DimDate[YearMonth] (monthly, ascending chronologically) |
| Y-axis | Block minutes (SUM of `fact_flight_operations[BlockMinutes]`) |
| Legend | DimAirline[AirlineName] (10 airlines) |
| Values measure | SUM(fact_flight_operations[BlockMinutes]) — existing column, no new DAX required |
| Filter context | Completed flights only (BlockMinutes is null for cancelled flights; SUM auto-excludes them) |
| Sort | X-axis ascending by YearMonth; legend in airline roster order |
| Data labels | Off (too many segments for labels) |
| Colours | 10 distinct colours — note: exceeds 5-colour guideline; see Limitations |
| Tooltip | Airline, month, block minutes, disclosure |
| Status | AVAILABLE — all source columns verified |

**Expected results (full dataset):**
| Month | Block Minutes |
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
| 2026-10 | 784 (partial — outside reporting period) |
| **Total** | **1,503,155** |

**Limitations:**
- 10 airlines exceed the 5-colour guideline; use distinguishable hues or group smaller airlines.
- BlockMinutes measures time in the air (block-to-block), not ground time. Do not label as turnaround time.
- 2026-10 shows only 784 minutes (outside reporting period); date range slicer default excludes it.

**See also:** `docs/PAGE_02_OPERATIONS_V3_REPLACEMENT_SPEC.md` for full specification.

---

## 4. Bottom Row — Three Visuals

### Visual 4: Operational KPIs by Route (Top 5)

| Attribute | Specification |
|---|---|
| Visual type | Table or matrix |
| Title | Operational KPIs by Route — Top 5 |
| Rows | DimRoute[RouteCode] (e.g., "XAE-XAU") plus origin/destination from DimAirport |
| Columns | Flights (count), On-Time % (OP01 basis), Average Delay (min) (OP02 basis) |
| Top 5 logic | Rank by flight count descending; show top 5 routes |
| Data format | Flights: #,##0; On-Time %: 0.0%; Average Delay: 0.0 min |
| Sort | Descending by flight count |
| Tooltip | Route, origin, destination, distance, airline, disclosure |
| Interactions | Responds to airline, date range slicers |
| Status | DERIVABLE |

**Route key:** DimRoute[RouteCode] (directional: Origin-Destination). Origin/destination airport names via DimAirport relationships (OriginAirportKey active, DestinationAirportKey inactive).

---

### Visual 5: Flight Operations by Airline

| Attribute | Specification |
|---|---|
| Visual type | Horizontal bar chart |
| Title | Flight Operations by Airline |
| Y-axis | DimAirline[AirlineName] (10 airlines) |
| X-axis | Count of flights (COUNTROWS fact_flight_operations) |
| Sort | Descending by flight count |
| Data labels | On (count, #,##0) |
| Colour | Brand teal (#0B7285) per design system |
| Tooltip | Airline, flight count, OTP, cancellation rate, disclosure |
| Interactions | Responds to date range slicer; clicking an airline filters supporting visuals (not KPI cards) |
| Status | AVAILABLE |

**Airline list (10):** Emirates, Qatar Airways, Singapore Airlines, Air India, IndiGo, British Airways, Lufthansa, Delta Air Lines, Southwest Airlines, Qantas.

---

### Visual 6: Flight Status Distribution by Month

| Attribute | Specification |
|---|---|
| Visual type | 100% stacked column chart |
| Title | Flight Status Distribution by Month |
| X-axis | DimDate[YearMonth] (monthly) |
| Y-axis | Percentage (0% to 100%) |
| Legend | Status category: On Time, Delayed, Cancelled |
| Stack order | On Time (bottom), Delayed (middle), Cancelled (top) |
| Data labels | Percentage on segments |
| Colours | On Time = green, Delayed = amber, Cancelled = red |
| Denominator | Flights per month (monthly total = 100%) |
| Sort | Ascending by YearMonth |
| Tooltip | Month, status, count, percentage, disclosure |
| Interactions | Responds to airline, date range slicers |
| Status | DERIVABLE |

**Percentage calculation:** Each status count / monthly total flights × 100. Monthly total excludes no flights (all statuses accounted for).

---

## 5. Slicer Interactions

| Slicer | Field | Type | Default | Affected visuals |
|---|---|---|---|---|
| Airline slicer | DimAirline[AirlineName] | Multi-select | All 10 airlines | All KPI cards and all 6 visuals |
| Flight Date Range slicer | DimDate[FullDate] or [YearMonth] | Date range | 2025-10-01 to 2026-09-30 (reporting period) | All KPI cards and all 6 visuals |

**Interaction rules (per POWER_BI_DASHBOARD_SPECIFICATION Section 4):**
- KPI cards respond to page slicers only; unrelated visuals do not cross-filter them
- Clicking an airline in V5 filters V1, V2, V3, V4, V6; does not change KPI cards unless via slicer
- Sync slicers: airline and date range are page-level, apply to all visuals
- Edit interactions must be reviewed page by page

---

## 6. Number Formatting and Display Units

| Measure/field | Display unit | Decimal places | Format |
|---|---|---|---|
| OP01 On-Time Departure Rate | None | 1 | `0.0%` |
| OP02 Average Departure Delay | None | 1 | `0.0 min` |
| OP03 Average Arrival Delay | None | 1 | `0.0 min` |
| OP04 Flight Completion Rate | None | 1 | `0.0%` |
| Flight counts | None | 0 | `#,##0` |
| Percentages (donut, stacked column) | None | 1 | `0.0%` |
| Turnaround minutes | None | 1 | `0.0 min` |
| Block minutes | None | 0 | `#,##0` |

**Blank behavior:** BLANK displays as em dash (—), never as zero (per design system Section 2.5).

---

## 7. Tooltips

Every visual uses a custom tooltip page containing:
- Definition of the measure
- Numerator and denominator (for ratios)
- Date role (departure, arrival, etc.)
- Selected filters (airline, date range)
- Exact disclosure: "Synthetic Simulation — Not Actual Airline Performance"

Default tooltips are disabled (per design system Section 2.7 / T-79 requirement).

---

## 8. Relative Positioning (Wireframe)

```
+-----------------------------------------------------------------------+
| [AEROVISION 360]  Operations Performance                              |
|  Flight Operations, On-Time Performance, Turnaround & Capacity Util.  |
|  [Airline slicer]  [Flight Date Range slicer]                         |
+-----------------------------------------------------------------------+
|  KPI 1  |  KPI 2  |  KPI 3  |  KPI 4  |  KPI 5  |              |
|  OP01   |  OP02   |  OP03   |  OP04   |  OP05   |              |
|  (card) |  (card) |  (card) |  (card) |  (card) |              |
+---------+---------+---------+---------+---------+------+----------+
|         |         |         |         |         |      |          |
|  V1     |  V2     |  V3     |         |         |      |          |
| On-Time | Flights | Turnaround|         |         |      |          |
| Trend   | by Status | Time    |         |         |      |          |
| (combo) | (donut) | (line)  |         |         |      |          |
|         |         |         |         |         |      |          |
+---------+---------+---------+---------+---------+------+----------+
|         |         |         |         |         |      |          |
|  V4     |  V5     |  V6     |         |         |      |          |
| Ops KPIs| Flights | Status  |         |         |      |          |
| by Route| by Airline| by Month|         |         |      |          |
| (table) | (bar)   | (stacked|         |         |      |          |
| Top 5   |         |  col)   |         |         |      |          |
|         |         |         |         |         |      |          |
+---------+---------+---------+---------+---------+------+----------+
|                                                                       |
|  Footer: Synthetic Simulation — Not Actual Airline Performance        |
+-----------------------------------------------------------------------+
```

---

## 9. Visuals Not Implementable (with reason)

| Visual | Reason | Required data | Status |
|---|---|---|---|
| OP05 KPI card | `ref_aircraft_availability.csv` missing; no per-aircraft-day availability calendar | Aircraft availability reference table | MISSING DATA — do not implement |

**Note:** V3 Turnaround Time has been replaced with Block Minutes by Airline/Month (see Section 3 and `docs/PAGE_02_OPERATIONS_V3_REPLACEMENT_SPEC.md`). No visuals remain blocked other than OP05.

---

## 10. Implementation Instructions

1. Create OP01, OP03, OP04 measures per `PAGE_02_OPERATIONS_DAX_SPECIFICATION.md`.
2. Reuse FL03 for OP02.
3. Do NOT create OP05 until `ref_aircraft_availability.csv` is added to the project and semantic model.
4. Do NOT create V3 until aircraft rotation/sequence data is available.
5. Create V1, V2, V4, V5, V6 per this specification.
6. Apply dark navy sidebar, branding, and banner consistent with Page 01.
7. Add slicers: Airline (all 10), Flight Date Range (default reporting period).
8. Add disclosure footer with exact string.
9. Do not modify Page 01.
10. Do not modify the live PBIX without an approved implementation plan.

---

**End of visual specification.** This document is design evidence only. No report page, visual, or PBIX was created or modified.
