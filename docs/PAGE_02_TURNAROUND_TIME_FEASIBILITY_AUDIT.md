# PAGE_02_TURNAROUND_TIME_FEASIBILITY_AUDIT.md

# AEROVISION 360 — Page 02: Turnaround Time Visual Feasibility Audit

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Page:** Page 02 — Operations Performance
**Visual:** Turnaround Time (Visual 3 — Monthly Line Chart)
**Audit type:** Focused feasibility investigation
**Status:** COMPLETE — INVESTIGATION ONLY; NO DATA, MODEL, DAX, PBIX, OR REPORT MODIFIED
**Prepared:** 2026-11-06
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Executive Verdict

**VERDICT: NOT FEASIBLE**

A valid aircraft turnaround-time KPI **cannot be calculated** using the existing AEROVISION 360 source data.

A valid turnaround calculation requires linking the same aircraft's actual arrival to its subsequent actual departure with a defensible flight sequence. The existing data lacks an explicit flight sequence number or aircraft rotation column. While aircraft identifiers and both timestamps exist, flights for the same aircraft are scattered across the entire 12-month reporting period. A naive sort-by-arrival approach produces turnarounds averaging **39,745 minutes (27.6 days)**, which are not operational turnarounds.

No synthetic or inferred turnaround values should be generated.

---

## 2. Source Data and Field Investigation

### 2.1 Datasets Inspected

| Dataset | Location | Format | Row Count | Relevance |
|---|---|---|---|---|
| fact_flight_operations.csv | data/03_curated/ | CSV | 5,000 | Primary source for flight timestamps and aircraft |
| dim_aircraft.csv | data/03_curated/ | CSV | 440 | Aircraft master (registration, fleet status) |
| dim_route.csv | data/03_curated/ | CSV | 320 | Route → origin/destination airport mapping |
| dim_airport.csv | data/03_curated/ | CSV | 72 | Airport master |
| dim_date.csv | data/03_curated/ | CSV | 761 | Calendar dimension |

### 2.2 Field Availability for Turnaround Calculation

| Required Field | Field Name | Table | Present? | Notes |
|---|---|---|---|---|
| Aircraft identifier | `AircraftKey` | fact_flight_operations | YES | 400 unique aircraft in fact; 440 in dim |
| Aircraft registration | `AircraftRegistration` | dim_aircraft | YES | Via AircraftKey join |
| Actual arrival timestamp | `ActualArrivalTimestampUTC` | fact_flight_operations | YES | 224 nulls (all cancelled flights) |
| Actual departure timestamp | `ActualDepartureTimestampUTC` | fact_flight_operations | YES | 224 nulls (all cancelled flights) |
| Flight sequence / rotation number | None | fact_flight_operations | **NO** | No sequence column exists |
| Subsequent departure link | None | fact_flight_operations | **NO** | No "next flight" reference |
| Origin airport | `OriginAirportKey` (via RouteKey) | dim_route | YES | 320 routes, 0 orphans |
| Destination airport | `DestinationAirportKey` (via RouteKey) | dim_route | YES | 320 routes, 0 orphans |
| Flight status | `FlightStatus` | fact_flight_operations | YES | Operated / Cancelled |
| Completion flag | `CompletionFlag` | fact_flight_operations | YES | Excludes cancelled flights |

### 2.3 Semantic Model Relationships

All relationships relevant to turnaround are active and valid:

- `fact_flight_operations[AircraftKey] → dim_aircraft[AircraftKey]` (active, 1:*)
- `fact_flight_operations[RouteKey] → dim_route[RouteKey]` (active, 1:*)
- `dim_route[OriginAirportKey] → dim_airport[AirportKey]` (active)
- `dim_route[DestinationAirportKey] → dim_airport[AirportKey]` (inactive role)

No relationship exists for aircraft rotation sequencing.

---

## 3. Aircraft Rotation Test Results

A direct rotation analysis was performed on the 4,776 completed flights with valid actual departure and arrival timestamps.

### 3.1 Flight Distribution per Aircraft

| Flights per Aircraft | Aircraft Count |
|---|---|
| 4 | 4 |
| 5 | 2 |
| 6–10 | 142 |
| 11–15 | 182 |
| 16–20 | 71 |
| 21–22 | 5 |
| **Total** | **400** |

All 400 aircraft in the fact table have multiple flights (minimum 4 per aircraft).

### 3.2 Naive Turnaround Calculation (Sort by Aircraft + Actual Arrival)

Flights for each aircraft were sorted by `ActualArrivalTimestampUTC`, and consecutive arrival→departure pairs were computed.

| Metric | Value |
|---|---|
| Potential turnaround pairs | 4,345 |
| Average turnaround (naive) | **39,744.84 minutes** (~27.6 days) |
| Median turnaround (naive) | Not computed (distribution clearly invalid) |

### 3.3 Sample Turnaround Results (Illustrative of the Problem)

| Aircraft | Arrival Flight | Arrival Time | Departure Flight | Departure Time | Turnaround |
|---|---|---|---|---|---|
| 2 | 4295 | 2025-10-09 06:03 | 4724 | 2025-10-29 17:18 | 29,475 min (20.5 days) |
| 2 | 4724 | 2025-10-29 23:48 | 4381 | 2026-01-17 20:20 | 114,992 min (79.9 days) |
| 2 | 4381 | 2026-01-18 04:20 | 2728 | 2026-01-19 02:23 | 1,323 min (22.1 hours) |
| 2 | 2728 | 2026-01-19 11:45 | 3163 | 2026-05-04 03:24 | 150,699 min (104.7 days) |

**These are not turnarounds.** They represent arbitrary gaps between unrelated flights for the same aircraft across the reporting period.

### 3.4 Why the Naive Approach Fails

1. **No operational sequence:** The data does not record which departure follows which arrival for the same aircraft. Sorting by arrival time is a guess, not a fact.
2. **Multi-month gaps:** Same-aircraft flights span the entire reporting period (Oct 2025 – Sep 2026), with gaps of days, weeks, or months between consecutive records.
3. **No same-day rotation context:** Turnaround time is a same-day, same-airport concept. The data does not guarantee that a flight's arrival and the next flight's departure occur at the same airport or on the same operational day.
4. **No tail-number rotation tracking:** There is no "tail number sequence" or "rotation ID" column to link flights into operational sequences.

---

## 4. Data-Quality Limitations

| Limitation | Impact on Turnaround Calculation |
|---|---|
| No flight sequence column | Cannot determine which departure follows which arrival for the same aircraft |
| No same-day/airport constraint | Cannot ensure arrival and subsequent departure are at the same airport |
| Synthetic flight records | Each row appears to be an independent leg, not part of a tracked aircraft rotation |
| 224 cancelled flights with null timestamps | Correctly excluded via CompletionFlag, but reduces rotation chain completeness |
| No ground-handling timestamps | Even with correct sequencing, no pushback/to-block/off-block times to calculate true ground time |

---

## 5. Additional Source Data Required

To implement a valid turnaround-time KPI, the following would be required:

| Required Data | Purpose | Current Status |
|---|---|---|
| Flight sequence number per aircraft per day | Defensible ordering of same-aircraft flights | **MISSING** |
| Aircraft rotation ID or tail-number sequence | Group flights into operational rotations | **MISSING** |
| Same-airport constraint validation | Ensure arrival and next departure are at same airport | Can be derived via RouteKey, but sequence is missing |
| Block-in / block-out timestamps | True ground time (not just arrival-to-departure) | Not present; `BlockMinutes` is flight block, not ground time |

---

## 6. Recommendation

**Do not implement the Turnaround Time visual.**

The existing data cannot support a valid, defensible turnaround-time KPI. Per the governing rules:
- Do not invent data
- Do not generate synthetic turnaround values
- Do not substitute unrelated delay measures (DepartureDelayMinutes, ArrivalDelayMinutes are not turnaround time)

### Recommended Alternative Visual

Replace V3 (Turnaround Time) with a supported operational visual. Options:

| Alternative | Data Availability | Rationale |
|---|---|---|
| Block Minutes by Airline/Month | `BlockMinutes` exists | Directly supported; measures aircraft time in the air |
| Delay by Cause (Disruption Type) | `fact_disruptions` + `dim_disruption_type` | Supported; shows operational disruption drivers |
| Scheduled vs Actual Block Time | Both timestamps exist | Supported; shows schedule adherence in block time |

Any replacement must use only existing, verified columns and must not fabricate aircraft rotation data.

---

## 7. Implementation Constraints Honored

| Constraint | Status |
|---|---|
| Do not invent data | Honored — no synthetic turnaround values generated |
| Do not modify PBIX, source data, DAX, relationships, or report pages | Honored — investigation only |
| Do not rebuild anything | Honored — no changes made |
| Provide verdict and justification | Provided — NOT FEASIBLE with documented evidence |

---

## 8. Conclusion

**Turnaround Time is NOT FEASIBLE with the existing AEROVISION 360 data.** The fundamental gap is the absence of an aircraft flight sequence or rotation column. Without it, there is no defensible way to link an aircraft's actual arrival to its subsequent actual departure. The naive calculation produces meaningless multi-day gaps, confirming that the data represents independent flight legs, not tracked aircraft rotations.

The Turnaround Time visual (V3) should be replaced with a supported operational visual using existing columns, or deferred until aircraft rotation data is added to the source.

---

**End of audit.** This document is investigation evidence only. No data, model, DAX, PBIX, or report was modified.
