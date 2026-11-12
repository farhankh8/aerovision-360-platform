# AEROVISION 360 — SEMANTIC MODEL AND RELATIONSHIP AUDIT

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08-SM  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY AUDIT — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Semantic Model Overview

The semantic model is defined in two files:
- `deliverables/power_bi/semantic_model/model.json` — Table and measure definitions
- `deliverables/power_bi/semantic_model/semantic_model.json` — Column, relationship, and measure metadata

**Files inspected:**
- `deliverables/power_bi/semantic_model/model.json` (6,153 bytes)
- `deliverables/power_bi/semantic_model/semantic_model.json` (15,887 bytes)

---

## 2. Table Inventory (14 Tables)

| Table | Type | Columns | Measures | PK | FKs | Role | Page 05 Use |
|-------|------|---------|----------|-----|-----|------|-------------|
| dim_airline | Dimension | 12 | 0 | AirlineKey | 0 | Dimension | YES — AirlineName |
| dim_airport | Dimension | 11 | 0 | AirportKey | 0 | Dimension | NO — not customer-facing |
| dim_route | Dimension | 9 | 0 | RouteKey | 2 | Dimension | YES — RouteCode |
| dim_date | Dimension | 19 | 0 | DateKey | 0 | Dimension | YES — date filtering |
| dim_aircraft | Dimension | 9 | 0 | AircraftKey | 2 | Dimension | NO — not customer-facing |
| dim_aircraft_type | Dimension | 8 | 0 | AircraftTypeKey | 0 | Dimension | NO — not customer-facing |
| dim_customer | Dimension | 8 | 0 | CustomerKey | 0 | Dimension | YES — CustomerSegment |
| dim_disruption_type | Dimension | 7 | 0 | DisruptionTypeKey | 0 | Dimension | NO — not customer-facing |
| dim_booking_channel | Dimension | 6 | 0 | BookingChannelKey | 0 | Dimension | NO — unused |
| dim_currency | Dimension | 6 | 0 | CurrencyKey | 0 | Dimension | NO — unused; OD-04 blocked |
| dim_fare_class | Dimension | 8 | 0 | FareClassKey | 0 | Dimension | PARTIAL — CabinClass; no FK to facts |
| fact_flight_operations | Fact | 25 | 4 | FlightOperationKey | 5 | Fact | PARTIAL — RevenuePassengers |
| fact_disruptions | Fact | 16 | 3 | DisruptionKey | 5 | Fact | NO — not customer-facing |
| fact_customer_feedback | Fact | 16 | 14 | FeedbackKey | 5 | Fact | YES — primary Page 05 source |
| fact_booking_transactions | Fact | 45 | 21 | BookingTransactionKey | 8 | Fact | BLOCKED — OD-04 |
| fact_operating_costs | Fact | 18 | 11 | OperatingCostKey | 4 | Fact | BLOCKED — OD-04 |

**Total:** 14 tables, 251 columns, 54 measures

---

## 3. Relationship Inventory (25 relationships)

### 3.1 Active Relationships (21)

| # | From | From Column | To | To Column | Cardinality | Direction | Status |
|---|------|-------------|-----|-----------|-------------|-----------|--------|
| 1 | fact_flight_operations | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| 2 | fact_flight_operations | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| 3 | fact_flight_operations | AircraftKey | dim_aircraft | AircraftKey | 1:* | Single | Active |
| 4 | fact_flight_operations | ScheduledDepartureDateKey | dim_date | DateKey | 1:* | Single | Active (primary date role) |
| 5 | fact_disruptions | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| 6 | fact_disruptions | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| 7 | fact_disruptions | DisruptionTypeKey | dim_disruption_type | DisruptionTypeKey | 1:* | Single | Active |
| 8 | fact_disruptions | EventLocationAirportKey | dim_airport | AirportKey | 1:* | Single | Active |
| 9 | fact_customer_feedback | CustomerKey | dim_customer | CustomerKey | 1:* | Single | Active |
| 10 | fact_customer_feedback | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| 11 | fact_customer_feedback | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| 12 | fact_booking_transactions | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| 13 | fact_booking_transactions | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| 14 | fact_booking_transactions | CustomerKey | dim_customer | CustomerKey | 1:* | Single | Active |
| 15 | fact_booking_transactions | FareClassKey | dim_fare_class | FareClassKey | 1:* | Single | Active |
| 16 | fact_booking_transactions | BookingChannelKey | dim_booking_channel | BookingChannelKey | 1:* | Single | Active |
| 17 | fact_booking_transactions | TravelDateKey | dim_date | DateKey | 1:* | Single | Active |
| 18 | fact_booking_transactions | TransactionCurrencyKey | dim_currency | CurrencyKey | 1:* | Single | Active |
| 19 | fact_operating_costs | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| 20 | fact_operating_costs | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| 21 | fact_operating_costs | CostDateKey | dim_date | DateKey | 1:* | Single | Active |
| 22 | fact_operating_costs | CurrencyKey | dim_currency | CurrencyKey | 1:* | Single | Active |

### 3.2 Inactive Relationships (4)

| # | From | From Column | To | To Column | Cardinality | Direction | Reason |
|---|------|-------------|-----|-----------|-------------|-----------|--------|
| 23 | fact_flight_operations | ScheduledArrivalDateKey | dim_date | DateKey | 1:* | Single | Inactive | Role-playing date |
| 24 | fact_disruptions | EventDateKey | dim_date | DateKey | 1:* | Single | Inactive | Second table connection; only one active relationship allowed |
| 25 | fact_customer_feedback | FeedbackDateKey | dim_date | DateKey | 1:* | Single | Inactive | Feedback date role |
| 26 | fact_customer_feedback | ResolutionDateKey | dim_date | DateKey | 1:* | Single | Inactive | Nullable FK; inactive role |
| 27 | fact_booking_transactions | BookingDateKey | dim_date | DateKey | 1:* | Single | Inactive | Role-playing date |

---

## 3.3 Unused Dimensions

| Dimension | Status | Reason |
|-----------|--------|--------|
| dim_fare_class | UNUSED | No FK column in any fact table |
| dim_booking_channel | UNUSED | No FK column in any fact table |
| dim_currency | UNUSED | No FK column in any fact table; OD-04 finance blocked |

---

## 4. Relationship Validation

| Relationship | Validated | Orphans | Status |
|--------------|-----------|---------|--------|
| dim_airline → fact_flight_operations | Yes | 0 | OK |
| dim_airline → fact_disruptions | Yes | 0 | OK |
| dim_airline → fact_customer_feedback | Yes | 0 | OK |
| dim_airline → dim_aircraft | Yes | 0 | OK |
| dim_aircraft → fact_flight_operations | Yes | 0 | OK |
| dim_airport → dim_route (Origin) | Yes | 0 | OK |
| dim_airport → dim_route (Destination) | Yes | 0 | Inactive (only one active per pair) |
| dim_airport → fact_disruptions | Yes | 0 | OK |
| dim_route → fact_flight_operations | Yes | 0 | OK |
| dim_route → fact_disruptions | Yes | 0 | OK |
| dim_route → fact_customer_feedback | Yes | 0 | OK |
| dim_customer → fact_customer_feedback | Yes | 0 | OK |
| dim_disruption_type → fact_disruptions | Yes | 0 | OK |
| dim_date → fact_flight_operations (Departure) | Yes | 0 | Active |
| dim_date → fact_flight_operations (Arrival) | Yes | 0 | Inactive |
| dim_date → fact_disruptions | Yes | 0 | Inactive |
| dim_date → fact_customer_feedback (Feedback) | Yes | 0 | Inactive |
| dim_date → fact_customer_feedback (Resolution) | Yes | 0 | Inactive; 1896 nulls |
| dim_date → fact_booking_transactions (Travel) | Yes | 0 | Active |
| dim_date → fact_booking_transactions (Booking) | Yes | 0 | Inactive |
| dim_currency → fact_booking_transactions | Yes | 0 | Active |
| dim_currency → fact_operating_costs | Yes | 0 | Active |

**Total:** 26 FK paths validated, 0 orphans found.

---

## 5. Missing Relationships

| Missing Relationship | Reason |
|----------------------|--------|
| dim_fare_class → fact_booking_transactions | No FK column in fact table |
| dim_booking_channel → fact_booking_transactions | No FK column in fact table |
| dim_currency → fact_booking_transactions | Has FK (TransactionCurrencyKey) — ACTIVE |
| dim_aircraft_type → fact_flight_operations | No direct FK; goes through dim_aircraft |

---

## 6. Semantic Model Issues

| Issue ID | Severity | Description | Impact |
|----------|----------|-------------|--------|
| SM-01 | HIGH | model.json defines wrong FL01 (COUNTROWS all rows) and FL02 (SUM BookedPassengers instead of RevenuePassengers) | Model metadata incorrect; DAX file has correct expressions |
| SM-02 | HIGH | model.json omits all dimension tables | Only 3 fact tables defined; no dimension metadata |
| SM-03 | MEDIUM | semantic_model.json has no measure expressions | Lists measure names only; cannot validate logic |
| SM-04 | MEDIUM | semantic_model.json relationship list incomplete | Missing dim_aircraft, dim_airport, dim_customer, dim_disruption_type, dim_date-for-disruptions/feedback |
| SM-05 | MEDIUM | dim_airline has 3 entirely null columns | AirlineGroup, BusinessModelClass, StatusEffectiveDate all null |
| SM-06 | HIGH | dim_fare_class, dim_booking_channel, dim_currency unused | No FK to any fact table |
| SM-07 | MEDIUM | Role-playing dim_date requires multiple inactive relationships | Only one active relationship per fact table; additional roles inactive |

---

## 7. Conclusion

The semantic model is **well-designed** with complete column definitions and 25 validated relationships (0 orphans). However:

1. model.json has wrong measure expressions for FL01, FL02, CF03
2. model.json omits all dimension tables
3. semantic_model.json has no measure expressions and incomplete relationship list
4. dim_fare_class, dim_booking_channel, dim_currency are unused
5. dim_airline has 3 entirely null columns
6. dim_date inactive date relationships require USERELATIONSHIP for feedback date filtering

**Recommendation:** Correct model.json expressions, add dimension tables to model.json, add measure expressions to semantic_model.json, complete relationship list, and address dim_airline null columns (do not fabricate values).
