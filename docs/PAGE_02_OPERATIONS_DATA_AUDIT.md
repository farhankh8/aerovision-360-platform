# PAGE_02_OPERATIONS_DATA_AUDIT.md

# AEROVISION 360 — Page 02 Operations Performance: Data Audit Report

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Page:** Page 02 — Operations Performance
**Audit type:** Discovery, gap analysis, and measure availability
**Status:** DISCOVERY COMPLETE — NO PBIX OR MODEL MODIFIED
**Prepared:** 2026-11-06
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Executive Summary

This audit investigates whether the AEROVISION 360 project's existing source data, semantic model, and measures can support Page 02 — Operations Performance as specified in the reference dashboard requirements.

**Headline finding:** Five KPIs and six visuals were evaluated. Of the five KPIs, three are directly AVAILABLE from existing data, one is DERIVABLE with a new measure, and one (Aircraft Utilization) is PARTIALLY AVAILABLE / UNSAFE TO CALCULATE because a required reference dataset (`ref_aircraft_availability.csv`) does not exist in the curated layer or semantic model. Of the six visuals, four are AVAILABLE or DERIVABLE, one (Turnaround Time) is MISSING due to absent source fields, and one (Flights by Status) requires careful denominator definition because only two status categories exist (Operated, Cancelled) — there is no Diverted status.

No existing data was modified. No PBIX was edited. No synthetic values were introduced.

---

## 2. Source-Data Inventory

The following table inventories every relevant dataset inspected in the project. All datasets are located under `data/03_curated/` (the CURATED layer consumed by Power BI).

| # | Dataset name | Location | Format | Row count | Column count | Primary key | Date fields | Airline fields | Flight fields | Route fields | Status fields | Delay fields | Aircraft fields | Quality issues |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | fact_flight_operations.csv | data/03_curated/ | CSV | 5,000 | 26 | FlightOperationKey | ScheduledDepartureTimestampUTC, ActualDepartureTimestampUTC, ScheduledArrivalTimestampUTC, ActualArrivalTimestampUTC, ScheduledDepartureDateKey, ScheduledArrivalDateKey | AirlineKey | FlightNumber, FlightLegID | RouteKey | FlightStatus | DepartureDelayMinutes, ArrivalDelayMinutes | AircraftKey, BlockMinutes | 224 nulls in ActualDeparture/ActualArrival/DepartureDelayMinutes/ArrivalDelayMinutes (all cancelled flights); 997 negative departure delays; 1,369 negative arrival delays |
| 2 | fact_disruptions.csv | data/03_curated/ | CSV | 1,754 | 16 | DisruptionKey | EventStartTimestampUTC, EventEndTimestampUTC, EventDateKey | AirlineKey | FlightOperationKey (FK) | RouteKey | (none) | DelayMinutes | (none) | 9 disruption types; DelayMinutes null on some rows |
| 3 | fact_customer_feedback.csv | data/03_curated/ | CSV | 2,500 | 16 | FeedbackKey | FeedbackDateKey, ResolutionDateKey | AirlineKey | FlightOperationKey (FK) | RouteKey | (none) | (none) | (none) | 1,896 null ResolutionDateKey; 3 entirely null enrichment columns in dim_airline (not this table) |
| 4 | dim_airline.csv | data/03_curated/ | CSV | 10 | 12 | AirlineKey | StatusEffectiveDate | AirlineKey, AirlineId, AirlineIATACode, AirlineICAOCode, AirlineName, AirlineGroup | (none) | (none) | (none) | (none) | (none) | AirlineGroup, BusinessModelClass, StatusEffectiveDate entirely null for all 10 rows |
| 5 | dim_airport.csv | data/03_curated/ | CSV | 72 | 11 | AirportKey | (none) | (none) | (none) | AirportCode (origin/destination via dim_route) | (none) | (none) | (none) | All airports are synthetic |
| 6 | dim_route.csv | data/03_curated/ | CSV | 320 | 9 | RouteKey | (none) | (none) | (none) | RouteKey, RouteCode, OriginAirportKey, DestinationAirportKey, DistanceKM | (none) | (none) | (none) | Directional routes (A->B != B->A) |
| 7 | dim_date.csv | data/03_curated/ | CSV | 761 | 19 | DateKey | FullDate, YearMonth, YearMonthSort, IsReportingPeriod | (none) | (none) | (none) | (none) | (none) | (none) | Covers 2024-10-01 through 2026-10-31; IsReportingPeriod=True only for 2025-10-01 to 2026-09-30 (365 days) |
| 8 | dim_aircraft.csv | data/03_curated/ | CSV | 440 | 9 | AircraftKey | FleetEntryDate | AirlineKey | (none) | (none) | FleetStatus | (none) | AircraftKey, AircraftRegistration, AircraftTypeKey, SeatCapacity, PlannedDailyAvailableHours, IsActive | 400 active, 40 maintenance/stored; PlannedDailyAvailableHours = 14.00 for all rows |
| 9 | dim_aircraft_type.csv | data/03_curated/ | CSV | 12 | 8 | AircraftTypeKey | (none) | (none) | (none) | (none) | (none) | (none) | AircraftTypeKey, Manufacturer, AircraftModel, TypicalSeatCapacity, MaximumSeatCapacity, RangeKM | All types are fictional/generic |
| 10 | dim_customer.csv | data/03_curated/ | CSV | — | 8 | CustomerKey | RegistrationDate | (none) | (none) | (none) | (none) | (none) | (none) | Synthetic customer data; no PII |
| 11 | dim_disruption_type.csv | data/03_curated/ | CSV | 9 | 7 | DisruptionTypeKey | (none) | (none) | (none) | (none) | DisruptionCategory, ControllableFlag | (none) | (none) | 9 types: Weather, ATC, Technical, Crew, Airport, Security, Passenger, Reactionary, Other |
| 12 | dim_booking_channel.csv | data/03_curated/ | CSV | — | 5 | BookingChannelKey | (none) | (none) | (none) | (none) | (none) | (none) | (none) | Unused by any fact (no FK) |
| 13 | dim_currency.csv | data/03_curated/ | CSV | — | 6 | CurrencyKey | (none) | (none) | (none) | (none) | (none) | (none) | (none) | Unused by any fact (no FK); OD-04 blocked |
| 14 | dim_fare_class.csv | data/03_curated/ | CSV | — | 8 | FareClassKey | (none) | (none) | (none) | (none) | (none) | (none) | (none) | Unused by any fact (no FK) |

**Missing reference dataset:** `ref_aircraft_availability.csv` — required by the governed DAX_KPI_CATALOGUE for K-13 (Aircraft Utilization). Does NOT exist in `data/03_curated/`, `data/04_reference/`, or the semantic model. Confirmed via glob search — zero matches.

---

## 3. Semantic-Model Inventory

The semantic model is defined in:
- `deliverables/power_bi/semantic_model/semantic_model.json`
- `deliverables/power_bi/semantic_model/model.json`

### 3.1 Tables

| Table | Type | Columns | Measures | Role |
|---|---|---|---|---|
| fact_flight_operations | Fact | 26 | FL01, FL02, FL03, FL04 | Central operations fact |
| fact_disruptions | Fact | 16 | DS01, DS02, DS03 | Disruption events |
| fact_customer_feedback | Fact | 16 | CF01, CF02, CF03 | Customer feedback |
| dim_airline | Dimension | 12 | — | Airline master (10 airlines) |
| dim_airport | Dimension | 11 | — | Airport master (72 airports) |
| dim_route | Dimension | 9 | — | Route master (320 directional routes) |
| dim_date | Dimension | 19 | — | Calendar (761 dates, 2024-10-01 to 2026-10-31) |
| dim_aircraft | Dimension | 9 | — | Fleet master (440 aircraft) |
| dim_aircraft_type | Dimension | 8 | — | Aircraft type reference (12 types) |
| dim_disruption_type | Dimension | 7 | — | Disruption cause taxonomy (9 types) |
| dim_customer | Dimension | 8 | — | Customer master |
| dim_booking_channel | Dimension | 5 | — | Unused (no FK) |
| dim_currency | Dimension | 6 | — | Unused (no FK); OD-04 blocked |
| dim_fare_class | Dimension | 8 | — | Unused (no FK) |

### 3.2 Relationships

All relationships are 1:*, single, active unless noted:

| From | From Column | To | To Column | Active |
|---|---|---|---|---|
| dim_airline | AirlineKey | fact_flight_operations | AirlineKey | Yes |
| dim_route | RouteKey | fact_flight_operations | RouteKey | Yes |
| dim_aircraft | AircraftKey | fact_flight_operations | AircraftKey | Yes |
| dim_date | DateKey | fact_flight_operations | ScheduledDepartureDateKey | Yes (primary date role) |
| dim_date | DateKey | fact_flight_operations | ScheduledArrivalDateKey | No (inactive, role-playing) |
| dim_airline | AirlineKey | fact_disruptions | AirlineKey | Yes |
| dim_route | RouteKey | fact_disruptions | RouteKey | Yes |
| dim_disruption_type | DisruptionTypeKey | fact_disruptions | DisruptionTypeKey | Yes |
| dim_airport | AirportKey | fact_disruptions | EventLocationAirportKey | Yes |
| dim_date | DateKey | fact_disruptions | EventDateKey | No (inactive) |
| dim_customer | CustomerKey | fact_customer_feedback | CustomerKey | Yes |
| dim_airline | AirlineKey | fact_customer_feedback | AirlineKey | Yes |
| dim_route | RouteKey | fact_customer_feedback | RouteKey | Yes |
| dim_date | DateKey | fact_customer_feedback | FeedbackDateKey | No (inactive) |
| dim_date | DateKey | fact_customer_feedback | ResolutionDateKey | No (inactive) |
| dim_airline | AirlineKey | dim_aircraft | AirlineKey | Yes |
| dim_aircraft_type | AircraftTypeKey | dim_aircraft | AircraftTypeKey | Yes |
| dim_airport | AirportKey | dim_route | OriginAirportKey | Yes |
| dim_airport | AirportKey | dim_route | DestinationAirportKey | No (inactive) |

**Missing relationships:** No relationship exists between `fact_flight_operations` and any aircraft-availability table (because `ref_aircraft_availability` is not in the model). No fact-to-fact relationships (correctly avoided).

### 3.3 Existing Measures (10 total)

| Measure | Table | Expression | Verified Value | Reusable for Page 02? |
|---|---|---|---|---|
| FL01 | fact_flight_operations | COUNTROWS(FILTER(FlightStatus="Operated")) | 4,776 | Partially (basis for completion rate) |
| FL02 | fact_flight_operations | SUM(RevenuePassengers) | 218,413 | No (passenger volume, not operations) |
| FL03 | fact_flight_operations | AVERAGE(DepartureDelayMinutes) | 43.42 min | **Yes — OP02** |
| FL04 | fact_flight_operations | Cancellation rate (Cancelled/Total) | 4.48% | Partially (inverse of completion rate) |
| DS01 | fact_disruptions | COUNTROWS(fact_disruptions) | 1,754 | No |
| DS02 | fact_disruptions | AVERAGE(DelayMinutes) | 120.62 | No |
| DS03 | fact_disruptions | Count controllable disruptions | 540 | No |
| CF01 | fact_customer_feedback | COUNTROWS(fact_customer_feedback) | 2,500 | No |
| CF02 | fact_customer_feedback | AVERAGE(SatisfactionScore) | 2.99 | No |
| CF03 | fact_customer_feedback | Complaint percentage | 25.52% | No |

---

## 4. Operations KPI Availability Matrix

| Requirement | Existing fields | Existing measures | Status | Missing information | Recommended implementation |
|---|---|---|---|---|---|
| OP01 — On-Time Departure Rate | `fact_flight_operations[FlightStatus]`, `[CompletionFlag]`, `[OnTimeFlag]`, `[DepartureDelayMinutes]`, `[ScheduledDepartureDateKey]` | FL01 (operated count basis) | AVAILABLE | On-time threshold not formally approved (OD-09 proposes 15 min); `OnTimeFlag` is precomputed (<=15 min) | New measure: DIVIDE(OnTimeDepartures, OperatedWithValidDeparture, BLANK()) using `OnTimeFlag` and `CompletionFlag` |
| OP02 — Average Departure Delay | `fact_flight_operations[DepartureDelayMinutes]`, `[CompletionFlag]` | FL03 | AVAILABLE (reuse FL03) | None — FL03 already averages DepartureDelayMinutes (blank values auto-exclude cancelled) | Reuse FL03; verify blank handling |
| OP03 — Average Arrival Delay | `fact_flight_operations[ArrivalDelayMinutes]`, `[CompletionFlag]` | None | DERIVABLE | None — all source columns exist | New measure: DIVIDE(SUM(ArrivalDelayMinutes) where CompletionFlag=True, OperatedWithValidArrival, BLANK()) |
| OP04 — Flight Completion Rate | `fact_flight_operations[CompletionFlag]`, `[CancellationFlag]`, `COUNTROWS(*)` | FL04 (cancellation rate, inverse) | DERIVABLE | None | New measure: DIVIDE(COUNTROWS(CompletionFlag=True), COUNTROWS(all), BLANK()) |
| OP05 — Aircraft Utilization hrs/day | `fact_flight_operations[BlockMinutes]`, `[AircraftKey]`, `[ScheduledDepartureDateKey]`; `dim_aircraft[PlannedDailyAvailableHours]`, `[IsActive]` | None | PARTIALLY AVAILABLE / UNSAFE TO CALCULATE | `ref_aircraft_availability.csv` does NOT exist; no per-aircraft-day availability calendar; `PlannedDailyAvailableHours` is a constant 14.00, not a calendar; cannot compute governed K-13 | Do NOT implement OP05 per governed method. Document missing `ref_aircraft_availability` requirement. Optional simplified proxy (block hours / active aircraft / days) requires owner decision. |

### 4.1 KPI Verification Results (computed from actual data)

| KPI | Numerator | Denominator | Result | Source basis |
|---|---|---|---|---|
| OP01 — On-Time Departure Rate | 1,485 (OnTimeFlag=True & CompletionFlag=True) | 4,776 (operated with valid delay) | 31.09% | `OnTimeFlag` (precomputed <=15 min) / operated count |
| OP02 — Average Departure Delay | Sum of DepartureDelayMinutes (4,776 valid values) | 4,776 | 43.42 min | Matches FL03 exactly |
| OP03 — Average Arrival Delay | Sum of ArrivalDelayMinutes (4,776 valid values) | 4,776 | 106.65 min | New measure required |
| OP04 — Flight Completion Rate | 4,776 (CompletionFlag=True) | 5,000 (all scheduled) | 95.52% | 1 - FL04 (4.48% cancellation rate) |
| OP05 — Aircraft Utilization | — | — | NOT CALCULABLE | `ref_aircraft_availability` missing |

---

## 5. Visual Availability Analysis

| Visual | Reference design | Status | Missing information | Notes |
|---|---|---|---|---|
| V1 — On-Time Performance Trend | Monthly trend: blue columns (departure OTP%), dark line (arrival OTP%) | DERIVABLE | None — monthly OTP can be computed from `FactFlightOperations` + `DimDate[YearMonth]` via active `ScheduledDepartureDateKey` relationship | Arrival OTP requires `USERELATIONSHIP(DimDate, ScheduledArrivalDateKey)` or computed arrival delay bucket |
| V2 — Flights by Status | Donut: On Time, Delayed, Cancelled; total in centre | AVAILABLE | Only 2 status values exist: Operated (4,776) and Cancelled (224). No "Diverted" status. "Delayed" must be derived (Operated AND NOT OnTime) | Categories: On Time (1,485), Delayed (3,291), Cancelled (224). Total = 5,000 |
| V3 — Block Minutes by Airline/Month | Monthly stacked column: block minutes by airline | AVAILABLE | None — `BlockMinutes` exists in `fact_flight_operations` (4,776 valid values, 224 null for cancelled); `AirlineKey` and `ScheduledDepartureDateKey` relationships active | Replaces Turnaround Time (NOT FEASIBLE). Total = 1,503,155 minutes. See `docs/PAGE_02_OPERATIONS_V3_REPLACEMENT_SPEC.md`. |
| V4 — Operational KPIs by Route (Top 5) | Table: Route, Flights, On-Time %, Avg Delay | DERIVABLE | None — `RouteKey` + `DimRoute[RouteCode]` + delay fields exist | Top 5 by flight count; join `DimRoute` for origin/destination |
| V5 — Flight Operations by Airline | Horizontal bar: airline, flight count, descending | AVAILABLE | None — `DimAirline[AirlineName]` + `FactFlightOperations[AirlineKey]` active relationship | 10 airlines; descending by flight count |
| V6 — Flight Status Distribution by Month | 100% stacked column: month, status % | DERIVABLE | None — monthly status breakdown computable | Denominator = flights per month; statuses: On Time / Delayed / Cancelled |

---

## 6. Exact Missing Fields

| # | Field | Required for | Where expected | Current state |
|---|---|---|---|---|
| 1 | `ref_aircraft_availability[AircraftKey, CalendarDateKey, AvailableHours, AvailabilityStatus, ReferenceVersion]` | OP05 (K-13 Aircraft Utilization) | `data/03_curated/` or `data/04_reference/` | **DOES NOT EXIST** — confirmed via glob search (0 matches). Not in semantic model. |
| 2 | Formal on-time threshold approval | OP01 | OD-09 (owner decision) | OD-09 is PROPOSED (15 minutes), not formally approved |

---

## 7. Data-Quality Findings

| # | Issue | Severity | Evidence | Affected KPIs |
|---|---|---|---|---|
| DQ-01 | Cancelled flights have null `ActualDepartureTimestampUTC`, `ActualArrivalTimestampUTC`, `DepartureDelayMinutes`, `ArrivalDelayMinutes` | Low (expected) | 224 nulls in each column; all are cancelled | OP01, OP02, OP03 — blank handling required |
| DQ-02 | 997 negative `DepartureDelayMinutes` (early departures) | Low (valid) | Early departures count as on-time if <=15 min early | OP01 (OnTimeFlag precomputed), OP02 |
| DQ-03 | 1,369 negative `ArrivalDelayMinutes` (early arrivals) | Low (valid) | Early arrivals remain negative in average | OP03 |
| DQ-04 | `OnTimeFlag` precomputed; threshold basis not documented in data | Medium | No column records the threshold value; OD-09 pending approval | OP01 — threshold assumption must be documented |
| DQ-05 | Only 2 flight statuses exist (Operated, Cancelled); no Diverted | Medium | Status distinct values: Operated (4,776), Cancelled (224) | V2 — "Delayed" must be derived, not a native status |
| DQ-06 | `dim_airline[AirlineGroup]`, `[BusinessModelClass]`, `[StatusEffectiveDate]` entirely null | Low | All 10 rows have nulls | V5 — no impact (uses AirlineName only) |
| DQ-07 | `dim_aircraft[PlannedDailyAvailableHours]` = 14.00 constant for all aircraft | Medium | Not a calendar; cannot support per-day availability | OP05 — cannot compute governed utilization |
| DQ-08 | `ref_aircraft_availability.csv` absent from project | High (blocking) | 0 file matches found | OP05 — cannot implement governed K-13 |

---

## 8. Reconciliation Test Specifications

| Test ID | Test | Expected result | Actual (from data) | Pass? |
|---|---|---|---|---|
| R-01 | Total scheduled flights | 5,000 | 5,000 | Pass |
| R-02 | Operated flights | 4,776 | 4,776 (matches FL01) | Pass |
| R-03 | Cancelled flights | 224 | 224 (matches FL04 numerator) | Pass |
| R-04 | Operated + Cancelled = Total | 5,000 | 4,776 + 224 = 5,000 | Pass |
| R-05 | No cancelled flight has actual departure | 0 | 0 | Pass |
| R-06 | No operated flight missing actual departure | 0 | 0 | Pass |
| R-07 | On-time departures (<=15 min) | 1,485 | 1,485 (OnTimeFlag=True) | Pass |
| R-08 | OTP = 1,485 / 4,776 | 31.09% | 31.09% | Pass |
| R-09 | Avg departure delay | 43.42 min | 43.42 min (matches FL03) | Pass |
| R-10 | Avg arrival delay | 106.65 min | 106.65 min | Pass |
| R-11 | Completion rate | 95.52% | 4,776 / 5,000 = 95.52% | Pass |
| R-12 | Cancellation rate | 4.48% | 224 / 5,000 = 4.48% (matches FL04) | Pass |
| R-13 | Completion + Cancellation = 100% | 100.00% | 95.52% + 4.48% = 100.00% | Pass |
| R-14 | Total block hours | 25,052.58 | 1,503,155 min / 60 = 25,052.58 hrs | Pass |
| R-15 | Active aircraft count | 400 | 400 (IsActive=True) | Pass |

---

## 9. Known Limitations

1. **OP05 (Aircraft Utilization) cannot be implemented per the governed DAX_KPI_CATALOGUE (K-13)** because `ref_aircraft_availability.csv` does not exist. The `dim_aircraft[PlannedDailyAvailableHours]` column (constant 14.00) is not a substitute for a per-aircraft-day availability calendar.
2. **V3 (Turnaround Time) cannot be implemented** because the source data lacks aircraft rotation/sequence information (no next departure timestamp per aircraft, no flight sequence).
3. **On-time threshold (15 minutes) is proposed per OD-09 but not formally approved.** The `OnTimeFlag` column precomputes this threshold but the threshold value itself is not stored in the data.
4. **Only two flight statuses exist** (Operated, Cancelled). There is no "Diverted" status. The "Delayed" category in V2 must be derived as "Operated AND NOT On Time."
5. The PBIX file exists but its internal data model could not be programmatically inspected (XPress9 compression). Custom JSON specs are not automatically loaded into the PBIX.
6. No reference dashboard screenshot was found in the project (`deliverables/screenshots/` is empty; no .png/.jpg files anywhere).

---

## 10. Recommended Implementation Sequence

1. Implement OP01, OP02, OP03, OP04 measures (all AVAILABLE/DERIVABLE from existing columns).
2. Implement V1, V2, V4, V5, V6 visuals (all DERIVABLE/AVAILABLE).
3. Defer OP05 and V3 pending owner decisions on missing data (`ref_aircraft_availability`, aircraft sequence).
4. Do NOT modify the live PBIX without an approved implementation plan.
5. Do NOT modify Page 01.

---

**End of audit.** This document is discovery evidence only. No DAX was created, no model was changed, and no report was built.
