# PAGE_02_OPERATIONS_DAX_IMPLEMENTATION_REPORT.md

# AEROVISION 360 — Page 02 Operations Performance: DAX Implementation Report

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Page:** Page 02 — Operations Performance
**Implementation type:** DAX measure implementation (specification file only; no live PBIX modification)
**Status:** COMPLETE — MEASURES DEFINED IN DAX SPEC; NOT YET ADDED TO LIVE PBIX
**Prepared:** 2026-11-06
**Governing verification:** `docs/PAGE_02_OPERATIONS_PRE_IMPLEMENTATION_VERIFICATION.md` (APPROVED WITH DOCUMENTED LIMITATIONS)
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Executive Summary

Three new DAX measures were defined and added to the DAX specification file. One existing measure (FL03) is reused for OP02. Two metrics (OP05, V3 Turnaround Time) remain blocked due to missing source data. No live PBIX was modified, no relationships were changed, no existing measures were modified, and Page 01 was not touched.

**File modified:** `deliverables/power_bi/dax/AEROVISION360_Measures.dax` (3 measures appended)

---

## 2. Measures Implemented

| Measure ID | Measure Name | Action | Verified Result | Source |
|---|---|---|---|---|
| OP01 | On-Time Departure Rate | New measure | 31.09% | `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md` Section 4.1 |
| OP02 | Average Departure Delay | Reuse FL03 | 43.42 min | Existing FL03 (no change) |
| OP03 | Average Arrival Delay | New measure | 106.65 min | `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md` Section 4.3 |
| OP04 | Flight Completion Rate | New measure | 95.52% | `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md` Section 4.4 |
| OP05 | Aircraft Utilization hrs/day | Blocked | N/A | `ref_aircraft_availability.csv` missing |

---

## 3. Exact DAX Definitions

### OP01 — On-Time Departure Rate

```DAX
OP01 = VAR _Operated = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE ) ) VAR _OperatedWithValidDelay = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE && NOT ISBLANK ( fact_flight_operations[DepartureDelayMinutes] ) ) ) VAR _OnTimeDepartures = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE && fact_flight_operations[OnTimeFlag] = TRUE ) ) RETURN DIVIDE ( _OnTimeDepartures, _OperatedWithValidDelay, BLANK() )
```

**Numerator:** Operated flights with `OnTimeFlag = TRUE` (1,485)
**Denominator:** Operated flights with non-blank `DepartureDelayMinutes` (4,776)
**Result:** 1,485 / 4,776 = 31.09%
**Format:** `0.0%`
**Blank behavior:** `DIVIDE(..., BLANK())` returns BLANK when denominator is 0
**Cancelled-flight treatment:** Excluded from both numerator and denominator
**Threshold:** 15 minutes (precomputed in `OnTimeFlag`; OD-09 proposed, not formally approved)

### OP02 — Average Departure Delay (Reuse FL03)

```DAX
FL03 = AVERAGE ( fact_flight_operations[DepartureDelayMinutes] )
```

**Status:** Existing measure — no change required
**Result:** 43.42 minutes (verified against source data)
**Format:** `0.0 min`
**Blank handling:** `AVERAGE` ignores blanks; cancelled flights auto-excluded
**Cancelled-flight treatment:** Excluded automatically (blank delay values)

### OP03 — Average Arrival Delay

```DAX
OP03 = VAR _Operated = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE ) ) VAR _OperatedWithValidArrival = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE && NOT ISBLANK ( fact_flight_operations[ArrivalDelayMinutes] ) ) ) VAR _TotalArrivalDelay = SUMX ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE ), fact_flight_operations[ArrivalDelayMinutes] ) RETURN DIVIDE ( _TotalArrivalDelay, _OperatedWithValidArrival, BLANK() )
```

**Numerator:** Sum of `ArrivalDelayMinutes` for operated flights
**Denominator:** Operated flights with non-blank `ArrivalDelayMinutes` (4,776)
**Result:** 106.65 minutes
**Format:** `0.0 min`
**Blank behavior:** `DIVIDE(..., BLANK())` returns BLANK when denominator is 0
**Cancelled-flight treatment:** Excluded from both numerator and denominator

### OP04 — Flight Completion Rate

```DAX
OP04 = VAR _TotalFlights = COUNTROWS ( fact_flight_operations ) VAR _OperatedFlights = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE ) ) RETURN DIVIDE ( _OperatedFlights, _TotalFlights, BLANK() )
```

**Numerator:** Flights with `CompletionFlag = TRUE` (4,776)
**Denominator:** All scheduled flight legs including cancelled (5,000)
**Result:** 4,776 / 5,000 = 95.52%
**Format:** `0.0%`
**Blank behavior:** `DIVIDE(..., BLANK())` returns BLANK when denominator is 0
**Cancelled-flight treatment:** Cancelled flights remain in denominator (per K-11 definition)
**Relationship to FL04:** FL04 = Cancellation Rate = 4.48%; OP04 = 1 - FL04 = 95.52%; reconciles exactly

---

## 4. Independent Validation Results

All results were independently recalculated from `data/03_curated/fact_flight_operations.csv` (5,000 rows):

| Measure | Expected | Independently Calculated | Match? |
|---|---|---|---|
| OP01 | 31.09% | 1,485 / 4,776 = 31.09% | ✅ Yes |
| OP02 (FL03) | 43.42 min | 43.42 min | ✅ Yes |
| OP03 | 106.65 min | 106.65 min | ✅ Yes |
| OP04 | 95.52% | 4,776 / 5,000 = 95.52% | ✅ Yes |

**Data quality confirmed:**
- 0 operated flights missing actual departure/arrival timestamps
- 0 cancelled flights with actual departure/arrival timestamps
- `OnTimeFlag` matches `DepartureDelayMinutes <= 15` exactly (4,776/4,776, 0 mismatches)
- Operated + Cancelled = Total (4,776 + 224 = 5,000)

---

## 5. Duplicate Measure Check

Before implementation, the existing DAX file was inspected for duplicates:

| Existing Measure | Duplicate of OP01/OP03/OP04? |
|---|---|
| FL01 | No (flights operated count) |
| FL02 | No (revenue passengers) |
| FL03 | No (reuse for OP02 only) |
| FL04 | No (cancellation rate — related but distinct from OP04) |
| DS01–DS03 | No (disruptions) |
| CF01–CF03 | No (customer feedback) |

**No duplicates found.** OP01, OP03, OP04 are all new measure IDs.

---

## 6. Relationship and Filter Context Verification

All measures use only existing, active relationships in the semantic model:

| Measure | Relationships Used | Ambiguous Paths? | Fact-to-Fact? |
|---|---|---|---|
| OP01 | `DimDate → fact_flight_operations` (ScheduledDepartureDateKey, active); `DimAirline → fact_flight_operations` (AirlineKey, active) | No | No |
| OP03 | Same as OP01 | No | No |
| OP04 | Same as OP01 | No | No |

**Confirmed:**
- No new relationships introduced
- No fact-to-fact relationships created
- No ambiguous `DimAirline` filter paths
- Single active date role per fact (departure date) — no `USERELATIONSHIP` required

---

## 7. Instructions for Adding Measures Through Power BI Desktop

Per the governance rule ("Do not modify the live PBIX programmatically"), these measures must be added manually through Power BI Desktop:

### Step 1 — Open the PBIX
1. Open `deliverables/power_bi/AEROVISION_360.pbix` in Power BI Desktop.
2. Do not modify Page 01 or any existing visuals.

### Step 2 — Open DAX Measure Editor
1. In the Report view, select the `fact_flight_operations` table in the Fields pane.
2. Click **New measure** in the ribbon (or right-click the table → New measure).
3. This opens the DAX formula bar.

### Step 3 — Enter Each Measure
For each measure below, paste the exact DAX into the formula bar, then press Enter to commit:

**Measure 1 — OP01:**
```
OP01 = VAR _Operated = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE ) ) VAR _OperatedWithValidDelay = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE && NOT ISBLANK ( fact_flight_operations[DepartureDelayMinutes] ) ) ) VAR _OnTimeDepartures = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE && fact_flight_operations[OnTimeFlag] = TRUE ) ) RETURN DIVIDE ( _OnTimeDepartures, _OperatedWithValidDelay, BLANK() )
```
- Formatting: Percentage, 1 decimal place (`0.0%`)
- Display name: OP01 — On-Time Departure Rate

**Measure 2 — OP03:**
```
OP03 = VAR _Operated = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE ) ) VAR _OperatedWithValidArrival = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE && NOT ISBLANK ( fact_flight_operations[ArrivalDelayMinutes] ) ) ) VAR _TotalArrivalDelay = SUMX ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE ), fact_flight_operations[ArrivalDelayMinutes] ) RETURN DIVIDE ( _TotalArrivalDelay, _OperatedWithValidArrival, BLANK() )
```
- Formatting: Number, 1 decimal place (`0.0`)
- Display name: OP03 — Average Arrival Delay

**Measure 3 — OP04:**
```
OP04 = VAR _TotalFlights = COUNTROWS ( fact_flight_operations ) VAR _OperatedFlights = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CompletionFlag] = TRUE ) ) RETURN DIVIDE ( _OperatedFlights, _TotalFlights, BLANK() )
```
- Formatting: Percentage, 1 decimal place (`0.0%`)
- Display name: OP04 — Flight Completion Rate

### Step 4 — Verify FL03 (OP02)
Confirm FL03 exists in the `fact_flight_operations` table:
```
FL03 = AVERAGE ( fact_flight_operations[DepartureDelayMinutes] )
```
- Formatting: Number, 1 decimal place (`0.0`)
- No changes needed — reuse as-is for OP02.

### Step 5 — Save and Validate
1. Save the PBIX.
2. Create a card visual for each measure and confirm the values match:
   - OP01: 31.09%
   - OP02 (FL03): 43.42 min
   - OP03: 106.65 min
   - OP04: 95.52%
3. If any result differs, stop and investigate — do not proceed to visual construction.

---

## 8. Blocked Measures (Not Implemented)

| Measure | Reason | Unblock Path |
|---|---|---|
| OP05 — Aircraft Utilization hrs/day | `ref_aircraft_availability.csv` does not exist in the project (0 file matches). Not in `data/03_curated/`, `data/04_reference/`, or the semantic model. | Owner must provide `ref_aircraft_availability.csv`; then implement K-13 per `docs/DAX_KPI_CATALOGUE.md` |
| V3 — Turnaround Time | No aircraft rotation sequence or next-departure timestamps in `fact_flight_operations`. | Requires aircraft sequence data and next-departure timestamp per aircraft |

---

## 9. Known Limitations (Documented)

| # | Limitation | Impact |
|---|---|---|
| L-01 | OP01 calculates 31.09% but visual reference displays 84.27%. Variance cannot be reconciled from available data. Calculation not forced to match reference. | KPI card will show 31.09%, not 84.27% |
| L-02 | 15-minute on-time threshold (OD-09) is PROPOSED, not formally approved. `OnTimeFlag` precomputes this threshold but the threshold value is not stored in data. | Threshold assumption must be documented on report |
| L-03 | OP05 blocked — `ref_aircraft_availability.csv` missing | OP05 card cannot be implemented |
| L-04 | V3 Turnaround Time blocked — no aircraft rotation/next-departure data | V3 cannot be implemented; placeholder recommended |
| L-05 | Only 2 flight statuses exist (Operated, Cancelled); no Diverted. "Delayed" is derived. | V2 categories: On Time (1,485), Delayed (3,291), Cancelled (224) |

---

## 10. What Was NOT Done (Governance Compliance)

| Action | Status |
|---|---|
| Modify live PBIX programmatically | Not done |
| Modify existing measures (FL01–FL04, DS01–DS03, CF01–CF03) | Not done |
| Modify relationships or existing tables | Not done |
| Modify Page 01 | Not done |
| Create OP05 measure | Not done (blocked) |
| Create Turnaround Time measure | Not done (blocked) |
| Create any Power BI visuals | Not done (deferred to next milestone) |
| Introduce synthetic values into operational KPIs | Not done |

---

## 11. Next Milestone

**Three new measures implemented and verified:** OP01, OP03, OP04. FL03 reused for OP02.

**Next step:** Open Power BI Desktop, add the measures per Section 7, validate the four values (31.09%, 43.42 min, 106.65 min, 95.52%), then proceed to build the five KPI cards to match the reference layout.

---

**End of implementation report.** This document records DAX measure definitions and implementation instructions only. The live PBIX has not been modified.
