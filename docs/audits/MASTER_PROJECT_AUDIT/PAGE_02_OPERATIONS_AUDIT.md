# AEROVISION 360 — PAGE 02 OPERATIONS AUDIT

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08-PAGE02  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY AUDIT — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Page Overview

| Attribute | Value |
|-----------|-------|
| Page Name | Operations & Disruption |
| Page Type | Visible (Page 4 of 5) |
| Purpose | Where is reliability failing, what causes it, and how does disruption affect the network? |
| Primary KPIs | K-09 (On-Time Performance), K-10 (Cancellation Rate), K-11 (Completion Rate), K-12 (Average Delay), K-13 (Aircraft Utilization) |
| Canvas Size | 1280 × 720 px (16:9) |
| Status | PARTIALLY IMPLEMENTED (DAX only); NOT IMPLEMENTED in PBIX |

---

## 2. Visual Inventory

| Visual ID | Visual Type | Measure(s) | Category/Axis | Purpose | Status |
|-----------|-------------|------------|---------------|---------|--------|
| OP-01 | Card | [On-Time Performance] | Reliability | Departure reliability | NOT IMPLEMENTED |
| OP-02 | Card | [S-03 On-Time Arrival %] | Arrival reliability | Arrival reliability | NOT IMPLEMENTED |
| OP-03 | Bar Chart | Category: AirlineName; Value: DisruptionName; Values: DS01 | Disruptions by Type | Disruptions by type | NOT IMPLEMENTED |
| OP-04 | Card | [Cancellation Rate] | Reliability | Cancellation rate | NOT IMPLEMENTED |
| OP-05 | Card | [Average Arrival Delay] | Reliability | Average arrival delay | NOT IMPLEMENTED |
| OP-06 | Card | [Flight Completion Rate] | Reliability | Flight completion rate | NOT IMPLEMENTED |

**Total Visuals:** 6 (5 KPI cards, 1 bar chart)

---

## 3. DAX Measures Required

| Measure ID | Measure Name | DAX Expression Location | Verified Value | Data Source | Status |
|------------|--------------|------------------------|----------------|-------------|--------|
| FL01 | Flights Operated | `dax/AEROVISION360_Measures.dax` line 9 | 4,776 | fact_flight_operations | Verified |
| FL02 | Total Revenue Passengers | `dax/AEROVISION360_Measures.dax` line 10 | 218,413 | fact_flight_operations | Verified |
| FL03 | Average Departure Delay | `dax/AEROVISION360_Measures.dax` line 11 | 43.42 | fact_flight_operations | Verified |
| FL04 | Cancellation Rate | `dax/AEROVISION360_Measures.dax` line 12 | 4.48% | fact_flight_operations | Verified |
| DS01 | Total Disruptions | `dax/AEROVISION360_Measures.dax` line 13 | 1,754 | fact_disruptions | Verified |
| DS02 | Average Delay Minutes | `dax/AEROVISION360_Measures.dax` line 14 | 120.62 | fact_disruptions | Verified |
| DS03 | Controllable Disruptions | `dax/AEROVISION360_Measures.dax` line 15 | 540 | fact_disruptions | Audit issue DAX-01 |
| OP01 | On-Time Departure Rate | Page 02 DAX Specification | 31.09% | fact_flight_operations | Not in DAX file |
| OP03 | Average Arrival Delay | Page 02 DAX Specification | 106.65 min | fact_flight_operations | Not in DAX file |
| OP04 | Flight Completion Rate | Page 02 DAX Specification | 95.52% | fact_flight_operations | Not in DAX file |

**Note:** OP01, OP03, OP04 are defined in `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md` but NOT yet added to `dax/AEROVISION360_Measures.dax`. They need to be added.

---

## 4. Data Quality and Validation

| Validation Check | Result | Evidence |
|------------------|--------|----------|
| FL01 Flights Operated = 4,776 | PASS | DAX_MEASURE_AUDIT.md reconciled against CSV |
| FL02 Total Revenue Passengers = 218,413 | PASS | DAX_MEASURE_AUDIT.md reconciled against CSV |
| FL03 Average Departure Delay = 43.42 | PASS | DAX_MEASURE_AUDIT.md reconciled against CSV |
| FL04 Cancellation Rate = 4.48% | PASS | DAX_MEASURE_AUDIT.md reconciled against CSV |
| DS01 Total Disruptions = 1,754 | PASS | DAX_MEASURE_AUDIT.md reconciled against CSV |
| DS02 Average Delay = 120.62 | PASS | DAX_MEASURE_AUDIT.md reconciled against CSV |
| DS03 Controllable Disruptions = 540 | PARTIAL | DAX expression counts dimension rows instead of fact events (DAX-01) |
| FlightOperationKey unique | PASS | 5,000 unique keys; 0 nulls |
| RouteKey FK valid | PASS | 0 orphans; 320 unique routes |
| AirlineKey FK valid | PASS | 0 orphans; 10 unique airlines |
| AircraftKey FK valid | PASS | 0 orphans; 440 unique aircraft |
| ScheduledDepartureDateKey FK valid | PASS | 0 orphans; 761 unique dates |

---

## 5. Data Quality Issues

| Issue | Impact | Severity |
|-------|--------|----------|
| ActualDepartureTimestampUTC null (224 rows) | Cancelled flights; affects delay calculations | MEDIUM |
| ActualArrivalTimestampUTC null (224 rows) | Cancelled flights; affects delay calculations | MEDIUM |
| DepartureDelayMinutes null (224 rows) | Cancelled flights; affects OTP calculation | MEDIUM |
| ArrivalDelayMinutes null (224 rows) | Cancelled flights; affects arrival delay | MEDIUM |
| BlockMinutes null (224 rows) | Cancelled flights; affects block hour calculations | LOW |
| DS03 counts dimension rows | Counts 3 dimension types instead of 540 disruption events | HIGH — DS03 incorrect |

---

## 6. Relationship Dependencies

| Relationship | From | To | Active | Impact on Page 02 |
|--------------|------|----|--------|-------------------|
| fact_flight_operations → dim_airline | AirlineKey | AirlineKey | Active | Enables airline filtering |
| fact_flight_operations → dim_route | RouteKey | RouteKey | Active | Enables route filtering |
| fact_flight_operations → dim_aircraft | AircraftKey | AircraftKey | Active | Enables aircraft filtering |
| fact_flight_operations → dim_date | ScheduledDepartureDateKey | DateKey | Active | Enables departure date filtering |
| fact_flight_operations → dim_date | ScheduledArrivalDateKey | DateKey | Inactive | Arrival date role-playing; requires USERELATIONSHIP |
| fact_disruptions → dim_airline | AirlineKey | AirlineKey | Active | Enables airline filtering for disruptions |
| fact_disruptions → dim_route | RouteKey | RouteKey | Active | Enables route filtering for disruptions |
| fact_disruptions → dim_disruption_type | DisruptionTypeKey | DisruptionTypeKey | Active | Enables disruption type filtering |
| fact_disruptions → dim_airport | EventLocationAirportKey | AirportKey | Active | Enables disruption location filtering |
| fact_disruptions → dim_date | EventDateKey | DateKey | Inactive | Disruption event date; requires USERELATIONSHIP |

---

## 7. Missing Elements

| Element | Status | Impact |
|---------|--------|--------|
| Visual titles | Missing | report.json has no explicit titles |
| Card formatting | Missing | No number formatting specified |
| Tooltips | Missing | No custom tooltips defined |
| Disclosure textbox | Missing | Synthetic Simulation disclosure not in report.json |
| Slicers | Missing | No slicers defined on Page 04 |
| OP05 Aircraft Utilization | MISSING DATA | ref_aircraft_availability.csv not in model |
| OP01, OP03, OP04 measures | NOT IN DAX FILE | Defined in specification but not in DAX file |

---

## 8. Conclusion

Page 02 Operations & Disruption is **NOT IMPLEMENTED in Power BI Desktop**. The visual structure is defined in `report.json` (3 visuals: 2 cards + 1 barChart), and measures are defined in DAX for FL01-FL04 and DS01-DS03. OP01, OP03, OP04 are defined in the specification document but NOT yet in the DAX file. OP05 is blocked due to missing ref_aircraft_availability.csv.

Key gaps:
1. PBIX contains only one blank page
2. No visuals created in Power BI Desktop
3. OP01, OP03, OP04 measures not yet in DAX file
4. DS03 expression counts dimension rows instead of fact events (DAX-01)
5. ref_aircraft_availability.csv missing (OP05 blocked)
6. No explicit titles, formatting, or tooltips
7. No slicers configured
