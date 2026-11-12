# PAGE_02_OPERATIONS_DAX_SPECIFICATION.md

# AEROVISION 360 — Page 02 Operations Performance: DAX Specification

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Page:** Page 02 — Operations Performance
**Status:** PROPOSED — NOT IMPLEMENTED; NO DAX CREATED IN MODEL
**Prepared:** 2026-11-06
**Governing contract:** `docs/03_DATA_CONTRACTS.md` v1.5
**KPI authority:** `docs/DAX_KPI_CATALOGUE.md` (K-09, K-10, K-11, K-12, K-13)
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Naming Convention

All new measures follow the `OPxx` prefix pattern specified in the reference requirements, consistent with the existing `FLxx`, `DSxx`, `CFxx` conventions:

| Measure ID | Measure name | Status |
|---|---|---|
| OP01 | On-Time Departure Rate | To be implemented |
| OP02 | Average Departure Delay | Reuse FL03 |
| OP03 | Average Arrival Delay | To be implemented |
| OP04 | Flight Completion Rate | To be implemented |
| OP05 | Aircraft Utilization Hours per Day | NOT IMPLEMENTED (missing data) |

Existing measures that can be reused:
- **FL03** = Average Departure Delay (43.42 min) — directly satisfies OP02

---

## 2. Approved DAX Measures

### OP01 — On-Time Departure Rate

**DAX:**
```DAX
OP01 On-Time Departure Rate =
VAR _Operated =
    CALCULATE (
        COUNTROWS ( fact_flight_operations ),
        fact_flight_operations[CompletionFlag] = TRUE
    )
VAR _OperatedWithValidDelay =
    CALCULATE (
        COUNTROWS ( fact_flight_operations ),
        fact_flight_operations[CompletionFlag] = TRUE,
        NOT ISBLANK ( fact_flight_operations[DepartureDelayMinutes] )
    )
VAR _OnTimeDepartures =
    CALCULATE (
        COUNTROWS ( fact_flight_operations ),
        fact_flight_operations[CompletionFlag] = TRUE,
        fact_flight_operations[OnTimeFlag] = TRUE
    )
RETURN
    DIVIDE ( _OnTimeDepartures, _OperatedWithValidDelay, BLANK() )
```

**Numerator:** Count of operated flights where `OnTimeFlag = TRUE`. `OnTimeFlag` is precomputed as `DepartureDelayMinutes <= 15` (15-minute threshold, per DAX_KPI_CATALOGUE K-09 / OD-09).

**Denominator:** Count of operated flights with a non-blank `DepartureDelayMinutes`. Cancelled flights (blank delay) are excluded.

**Filter context:** Filtered by active `DimDate[ScheduledDepartureDateKey]` relationship (departure date role). Responds to airline slicer via `DimAirline`. Responds to route/airport filters via `DimRoute`/`DimAirport`.

**Date handling:** Uses `ScheduledDepartureDateKey` (active relationship to `DimDate`). A date-range slicer filters departure dates.

**Airline filtering:** Flows through active `DimAirline[AirlineKey] → fact_flight_operations[AirlineKey]`.

**Blank/null handling:** `DIVIDE(..., BLANK())` returns BLANK when denominator is 0. Cancelled flights have blank `DepartureDelayMinutes` and are excluded by `NOT ISBLANK`.

**Cancelled-flight treatment:** Cancelled flights are excluded from both numerator and denominator (handled via `CompletionFlag = TRUE` and `NOT ISBLANK(DepartureDelayMinutes)`).

**Double-counting risk:** None — each flight operation key is counted once at flight-leg grain.

**Validation calculation:**
```
Expected: 1,485 / 4,776 = 31.09%
Source: OnTimeFlag=True count (1,485) / operated count (4,776)
```

---

### OP02 — Average Departure Delay (Reuse FL03)

**DAX (existing, verified):**
```DAX
FL03 = AVERAGE ( fact_flight_operations[DepartureDelayMinutes] )
```

**Status:** AVAILABLE — reuse as-is. FL03 automatically excludes cancelled flights because `DepartureDelayMinutes` is blank for cancelled rows, and `AVERAGE` ignores blanks.

**Verified value:** 43.42 minutes (matches independent recalculation from CSV).

**Numerator:** Sum of `DepartureDelayMinutes` for operated flights with valid delays.

**Denominator:** Count of operated flights with non-blank `DepartureDelayMinutes` (4,776).

**Filter context:** Same as OP01 (departure date role, airline, route).

**Note:** Negative values (early departures, 997 occurrences) remain in the average — they are not excluded.

---

### OP03 — Average Arrival Delay

**DAX:**
```DAX
OP03 Average Arrival Delay =
VAR _Operated =
    CALCULATE (
        COUNTROWS ( fact_flight_operations ),
        fact_flight_operations[CompletionFlag] = TRUE
    )
VAR _OperatedWithValidArrival =
    CALCULATE (
        COUNTROWS ( fact_flight_operations ),
        fact_flight_operations[CompletionFlag] = TRUE,
        NOT ISBLANK ( fact_flight_operations[ArrivalDelayMinutes] )
    )
VAR _TotalArrivalDelay =
    CALCULATE (
        SUM ( fact_flight_operations[ArrivalDelayMinutes] ),
        fact_flight_operations[CompletionFlag] = TRUE
    )
RETURN
    DIVIDE ( _TotalArrivalDelay, _OperatedWithValidArrival, BLANK() )
```

**Numerator:** Sum of `ArrivalDelayMinutes` for operated flights (blank values excluded by SUM).

**Denominator:** Count of operated flights with non-blank `ArrivalDelayMinutes`.

**Filter context:** Default departure date role (`ScheduledDepartureDateKey`). For arrival-date analysis, would require `USERELATIONSHIP(DimDate[DateKey], fact_flight_operations[ScheduledArrivalDateKey])` — not used in this baseline.

**Date handling:** Uses `ScheduledDepartureDateKey` (active relationship).

**Airline filtering:** Flows through active `DimAirline[AirlineKey]`.

**Blank/null handling:** `DIVIDE(..., BLANK())`. Cancelled flights have blank `ArrivalDelayMinutes`.

**Cancelled-flight treatment:** Excluded via `CompletionFlag = TRUE`.

**Double-counting risk:** None.

**Validation calculation:**
```
Expected: 106.65 minutes (computed from 4,776 operated flights with valid arrival delays)
Source: SUM(ArrivalDelayMinutes) / 4,776
```

---

### OP04 — Flight Completion Rate

**DAX:**
```DAX
OP04 Flight Completion Rate =
VAR _TotalFlights = COUNTROWS ( fact_flight_operations )
VAR _OperatedFlights =
    CALCULATE (
        COUNTROWS ( fact_flight_operations ),
        fact_flight_operations[CompletionFlag] = TRUE
    )
RETURN
    DIVIDE ( _OperatedFlights, _TotalFlights, BLANK() )
```

**Numerator:** Count of flights where `CompletionFlag = TRUE` (4,776).

**Denominator:** Count of all scheduled flight legs, including cancelled (5,000).

**Filter context:** Departure date role. Responds to airline/route/airport filters.

**Date handling:** `ScheduledDepartureDateKey`.

**Airline filtering:** Via `DimAirline`.

**Blank/null handling:** `DIVIDE(..., BLANK())`. Zero total flights returns BLANK.

**Cancelled-flight treatment:** Cancelled flights remain in the denominator (per K-11 definition: "cancelled flights remain in denominator").

**Double-counting risk:** None.

**Relationship to FL04:** FL04 = Cancellation Rate = 224/5,000 = 4.48%. OP04 = 1 - FL04 = 95.52%. OP04 is the direct completion-rate measure; FL04 is its inverse.

**Validation calculation:**
```
Expected: 4,776 / 5,000 = 95.52%
Source: CompletionFlag=True count / total row count
```

---

### OP05 — Aircraft Utilization Hours per Day (NOT IMPLEMENTED)

**Status:** NOT IMPLEMENTED — required source data missing.

**Per DAX_KPI_CATALOGUE K-13**, the governed formula is:
```
Aircraft Utilization = DIVIDE ( [Operating Block Hours], [Available Aircraft Hours], BLANK() )
```
where:
- `Operating Block Hours` = SUM(BlockMinutes / 60) for operated flights
- `Available Aircraft Hours` = SUM(ref_aircraft_availability[AvailableHours]) where AvailabilityStatus = "Available"

**Missing:** `ref_aircraft_availability.csv` does not exist in the project (confirmed: 0 file matches). It is not in `data/03_curated/`, `data/04_reference/`, or the semantic model.

**Partial data available:**
- `fact_flight_operations[BlockMinutes]`: total 1,503,155 minutes (25,052.58 hours) for operated flights
- `dim_aircraft[PlannedDailyAvailableHours]`: constant 14.00 for all 440 aircraft (400 active)
- `dim_aircraft[IsActive]`: 400 active aircraft

**Why not to implement:** Using `PlannedDailyAvailableHours` (a constant) instead of a per-aircraft-day availability calendar would produce an incorrect utilization ratio. The governed K-13 requires the reference availability table. Implementing without it would violate Rule 4 (no unverified assumptions) and Rule 5 (no fabricated metrics).

**Required to proceed:** Create/populate `ref_aircraft_availability.csv` with one row per aircraft per calendar date per reference version, then add it to the semantic model and implement K-13 per the DAX_KPI_CATALOGUE.

---

## 3. Measure Reuse Summary

| Page 02 measure | Reuses existing measure? | Existing measure | Notes |
|---|---|---|---|
| OP01 | No | — | New measure (uses OnTimeFlag, CompletionFlag) |
| OP02 | Yes | FL03 | FL03 = AVERAGE(DepartureDelayMinutes) = 43.42 min |
| OP03 | No | — | New measure (parallel to FL03 but for arrival) |
| OP04 | No | FL04 (inverse relationship) | FL04 = cancellation rate; OP04 = completion rate = 1 - FL04 |
| OP05 | No | — | Cannot implement (missing ref_aircraft_availability) |

---

## 4. Data-Type and Format Conventions

| Measure | Data type | Format string | Blank behavior |
|---|---|---|---|
| OP01 | Decimal (ratio) | `0.0%` | BLANK if denominator = 0 |
| OP02 | Decimal (minutes) | `0.0` | BLANK if no valid delays |
| OP03 | Decimal (minutes) | `0.0` | BLANK if no valid delays |
| OP04 | Decimal (ratio) | `0.0%` | BLANK if denominator = 0 |
| OP05 | Decimal (ratio) | `0.00` | BLANK if no available hours |

All percentages are stored as decimal fractions and formatted as percent in the report (per DAX_KPI_CATALOGUE convention: "Percentages are stored as decimal fractions; format as percent in the report.").

---

## 5. Dependencies

| Measure | Depends on tables | Depends on relationships | Depends on measures |
|---|---|---|---|
| OP01 | fact_flight_operations, dim_date, dim_airline | DimDate→FactFlightOperations (ScheduledDepartureDateKey, active); DimAirline→FactFlightOperations | None |
| OP02 (FL03) | fact_flight_operations | Same as OP01 | None |
| OP03 | fact_flight_operations, dim_date, dim_airline | Same as OP01 | None |
| OP04 | fact_flight_operations, dim_date, dim_airline | Same as OP01 | None |
| OP05 | fact_flight_operations, dim_aircraft, ref_aircraft_availability (MISSING) | DimAircraft→FactFlightOperations; DimDate→RefAircraftAvailability | None (blocked) |

---

## 6. Governance Notes

- No measure is claimed to compile or run until implemented in the semantic model and tested against source data (per DAX_KPI_CATALOGUE Section 6).
- No unsupported fields are introduced. OP05 is explicitly deferred due to missing `ref_aircraft_availability`.
- The 15-minute on-time threshold (OD-09) is proposed, not formally approved. The `OnTimeFlag` column precomputes this threshold but the threshold value is not stored in data.
- All measures carry the `DIVIDE(..., BLANK())` zero-denominator guard per contract Section 11.
- Every measure must return the synthetic disclosure context when used in report visuals.

---

**End of DAX specification.** This document is design evidence only. No DAX was created, no model was changed, and no report was built.
