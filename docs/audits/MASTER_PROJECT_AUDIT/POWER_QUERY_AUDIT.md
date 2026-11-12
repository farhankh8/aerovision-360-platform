# AEROVISION 360 — POWER QUERY AUDIT

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08-PQ  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY AUDIT — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Power Query Overview

**File:** `deliverables/power_bi/power_query/AEROVISION360_DataLoad.m`  
**Size:** 12,628 bytes  
**Tables Defined:** 2 of 14  
**Tables Missing:** 12  

---

## 2. Tables Defined in Power Query

| # | Table | Status | Source | Columns Defined | Data Types |
|---|-------|--------|--------|-----------------|------------|
| 1 | dim_airline | Defined | `data/dim_airline.csv` | 12 | AirlineKey(int64), AirlineId(text), AirlineIATACode(text), AirlineICAOCode(text), AirlineName(text), HomeCountry(text), HomeCountryCode(text), IsActive(logical), ReferenceVersion(text) |
| 2 | dim_airport | Defined | `data/dim_airport.csv` | 11 | AirportKey(int64), AirportCode(text), AirportName(text), City(text), Country(text), CountryCode(text), Region(text), Latitude(number), Longitude(number), TimeZoneIANA(text), IsActive(logical) |

**12 tables NOT defined:** dim_route, dim_date, dim_aircraft, dim_aircraft_type, dim_customer, dim_disruption_type, dim_booking_channel, dim_currency, dim_fare_class, fact_booking_transactions, fact_customer_feedback, fact_disruptions, fact_flight_operations, fact_operating_costs

---

## 3. Power Query Issues

| Issue ID | Severity | Description | Impact |
|----------|----------|-------------|--------|
| PQ-01 | HIGH | Only 2 of 14 tables defined | 12 tables missing from Power Query; cannot load into model without manual definition |
| PQ-02 | MEDIUM | dim_airline column count mismatch | Power Query states 14 columns; actual CSV has 12 columns |
| PQ-03 | MEDIUM | No error handling | No try/except or error trapping in M code |
| PQ-04 | MEDIUM | No duplicate prevention | No logic to prevent duplicate rows |
| PQ-05 | LOW | Comments only; no implementation logic | M script contains comments describing transformations but minimal actual transformation logic |

---

## 4. Required Power Query Tables (Missing)

| Table | Source File | Required Columns | Status |
|-------|-------------|------------------|--------|
| dim_airline | dim_airline.csv | 12 columns | Defined |
| dim_airport | dim_airport.csv | 11 columns | Defined |
| dim_route | dim_route.csv | 9 columns | NOT DEFINED |
| dim_date | dim_date.csv | 19 columns | NOT DEFINED |
| dim_aircraft | dim_aircraft.csv | 9 columns | NOT DEFINED |
| dim_aircraft_type | dim_aircraft_type.csv | 8 columns | NOT DEFINED |
| dim_customer | dim_customer.csv | 8 columns | NOT DEFINED |
| dim_disruption_type | dim_disruption_type.csv | 7 columns | NOT DEFINED |
| dim_booking_channel | dim_booking_channel.csv | 6 columns | NOT DEFINED |
| dim_currency | dim_currency.csv | 6 columns | NOT DEFINED |
| dim_fare_class | dim_fare_class.csv | 8 columns | NOT DEFINED |
| fact_flight_operations | fact_flight_operations.csv | 25 columns | NOT DEFINED |
| fact_customer_feedback | fact_customer_feedback.csv | 14 columns | NOT DEFINED |
| fact_disruptions | fact_disruptions.csv | 16 columns | NOT DEFINED |
| fact_booking_transactions | fact_booking_transactions.csv | 45 columns | NOT DEFINED |
| fact_operating_costs | fact_operating_costs.csv | 18 columns | NOT DEFINED |

---

## 5. Data Type Conversion Issues

| Table | Column | Expected Type | M Code Type | Issue |
|-------|--------|---------------|-------------|-------|
| dim_airline | AirlineKey | Int32 | Int64 | Mismatch (Int64 vs Int32) |
| dim_airport | AirportKey | Int32 | Int64 | Mismatch (Int64 vs Int32) |
| dim_route | RouteKey | Int32 | Not defined | Missing |
| dim_date | DateKey | Int32 | Not defined | Missing |
| dim_customer | CustomerKey | Int32 | Not defined | Missing |

---

## 6. Conclusion

Power Query M script is **incomplete** — only 2 of 14 tables defined. The M script needs a complete rewrite to define all 14 tables with correct data types, error handling, and duplicate prevention. This is a P1 priority item in the remediation plan (P2-14).
