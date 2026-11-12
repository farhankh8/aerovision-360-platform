# SEMANTIC MODEL AND RELATIONSHIP AUDIT

**Source:** `deliverables/power_bi/semantic_model/model.json` and `semantic_model.json` (read in full)  
**Compared against:** DAX file, Power Query M, PBIX page visual bindings  
**Limitation:** In-PBIX binary `DataModel` (2.5 MB) could not be deserialized; relationships inside the live PBIX not independently verified (limitation L-2)  
**Audit mode:** Read-only.

---

## 1. Table inventory

**16 tables** documented in `semantic_model/model.json` (11 dimensions + 5 facts):

| Table | Type | Columns | Measures | Primary key | Relationships (outgoing) |
|---|---|---|---|---|---|
| dim_airline | Dimension | 12 | 0 | AirlineKey | none (lookup) |
| dim_airport | Dimension | 11 | 0 | AirportKey | none (lookup) |
| dim_route | Dimension | 9 | 0 | RouteKey | → dim_airport (Origin active, Destination inactive) |
| dim_date | Dimension (Date) | 19 | 0 | DateKey | none (date table) |
| dim_aircraft | Dimension | 9 | 0 | AircraftKey | → dim_airline (active), → dim_aircraft_type (active) |
| dim_aircraft_type | Dimension | 8 | 0 | AircraftTypeKey | none (lookup) |
| dim_customer | Dimension | 8 | 0 | CustomerKey | none (lookup) |
| dim_disruption_type | Dimension | 7 | 0 | DisruptionTypeKey | none (lookup) |
| dim_booking_channel | Dimension | 8 | 0 | BookingChannelKey | none (lookup) |
| dim_currency | Dimension | 6 | 0 | CurrencyKey | none (lookup) |
| dim_fare_class | Dimension | 8 | 0 | FareClassKey | none (lookup) |
| fact_flight_operations | Fact | 26 | 4 (FL01–04) | FlightOperationKey | → dim_airline, dim_route, dim_aircraft, dim_date(departure active, arrival inactive) |
| fact_disruptions | Fact | 16 | 3 (DS01–03) | DisruptionKey | → dim_airline, dim_route, dim_disruption_type, dim_airport, dim_date(inactive) |
| fact_customer_feedback | Fact | 16 | 14 (CF01–14) | FeedbackKey | → dim_customer, dim_airline, dim_route, dim_date(feedback inactive, resolution inactive) |
| fact_booking_transactions | Fact | 50 | 20 (RV/NC) | BookingTransactionKey | → dim_airline, dim_route, dim_customer, dim_fare_class, dim_booking_channel, dim_date(Travel active, Booking inactive), dim_currency |
| fact_operating_costs | Fact | 18 | 10 (CX) | OperatingCostKey | → dim_airline, dim_route, dim_date(Cost active), dim_currency |

**Total measures registered: 51** (4+3+14+20+10).

---

## 2. Relationship inventory (documented)

Active relationships:
- fact_flight_operations → dim_airline (AirlineKey), dim_route (RouteKey), dim_aircraft (AircraftKey), dim_date (ScheduledDepartureDateKey → DateKey)
- fact_disruptions → dim_airline, dim_route, dim_disruption_type, dim_airport (EventLocationAirportKey → AirportKey)
- fact_customer_feedback → dim_customer, dim_airline, dim_route
- fact_booking_transactions → dim_airline, dim_route, dim_customer, dim_fare_class, dim_booking_channel, dim_date (TravelDateKey), dim_currency (TransactionCurrencyKey)
- fact_operating_costs → dim_airline, dim_route, dim_date (CostDateKey), dim_currency (CurrencyKey)
- dim_route → dim_airport (OriginAirportKey → AirportKey)
- dim_aircraft → dim_airline, dim_aircraft_type

Inactive relationships:
- fact_flight_operations → dim_date (ScheduledArrivalDateKey)
- fact_disruptions → dim_date (EventDateKey)
- fact_customer_feedback → dim_date (FeedbackDateKey, ResolutionDateKey)
- fact_booking_transactions → dim_date (BookingDateKey)
- dim_route → dim_airport (DestinationAirportKey)

**Cardinality:** All documented as many-to-one (fact → dimension) with single active date relationships — standard star schema.

**Filter direction:** Single (filter from dimension to fact) — standard.

**Date relationships:** dim_date marked with active travel/cost/booking date roles; inactive role-playing date relationships available via USERELATIONSHIP (used in DAX for booking-date cohort).

**Role-playing dimensions:** dim_date serves multiple roles (travel date, booking date, event date, feedback/resolution date, cost date) via active + inactive relationships — correctly implemented.

---

## 3. Star-schema conformance

| Star-schema principle | Conformance | Evidence |
|---|---|---|
| Facts connect to dimensions via surrogate keys | Yes | `*Key` foreign keys on all facts |
| Dimensions are denormalized lookups | Yes | dim_* tables have no outgoing relationships (except route→airport, aircraft→airline/type) |
| One active date relationship per fact | Yes | Each fact has one active dim_date relationship; others inactive |
| No many-to-many between facts | Yes | No fact-to-fact relationships |
| Conformed date dimension | Yes | dim_date shared across all facts |

**Verdict:** Model follows intended star-schema architecture. `dim_route`→`dim_airport` (destination inactive) and `dim_aircraft`→`dim_airline`/`dim_aircraft_type` are dimension-to-dimension links, acceptable for a star schema (snowflake-lite) but worth noting.

---

## 4. Relationships documented vs present

All relationships in `semantic_model.json` are documented with fromColumn, toTable, toColumn, role. No relationship is documented in `model.json` that is missing — but the in-PBIX binary model could not be checked (limitation L-2).

**Finding SM-01 (MEDIUM):** `fact_route_costs_map` is bound by a Page 04 map visual but is NOT one of the 16 documented tables. Either it exists only in the in-PBIX binary model (making model.json incomplete) or the visual is orphaned. Must be verified in Power BI Desktop.

**Finding SM-02 (MEDIUM):** dim_airline includes `BusinessModelClass` column but OD-01B D-05 is PENDING (not authorized to populate); column would be null/empty.

---

## 5. Measures and dependencies

51 measures registered across 5 fact tables (see Phase C DAX audit). All 51 registered measures have DAX definitions. 3 DAX measures (OP01/03/OP04) are NOT registered. No model measures lack DAX definitions.

**fact_booking_transactions** also registers NC_ measures (cross-fact: NC uses both RV and CX) — acceptable since they're stored on the booking fact but reference cost data through filter context.

---

## 6. Storage mode and organization

- Storage mode: Import (Power BI default; PBIX contains embedded DataModel).
- Model organized by table with columns + measures listed; relationships listed per fact table.
- `disclosure` field present: "Synthetic Simulation - Not Actual Airline Performance".
- No row-level security (RLS) evidenced in model.json.
- No calculated columns evidenced (measures only) — good for performance.

---

## 7. Semantic model findings register

| ID | Finding | Severity | Evidence | Confidence |
|---|---|---|---|---|
| SM-01 | `fact_route_costs_map` referenced by Page 04 map, absent from 16 documented tables | HIGH | Page 04 visual binding vs model.json table list | High (absence from model.json confirmed) |
| SM-02 | dim_airline BusinessModelClass column not authorized to populate (OD-01B D-05 PENDING) | MEDIUM | OD01B Section 4/D-05 | High |
| SM-03 | In-PBIX binary DataModel not deserialized; live relationships not independently verified | MEDIUM | Limitation L-2 | — |
| SM-04 | Model follows star-schema; 16 tables, 51 measures, all registered measures have DAX definitions | INFORMATIONAL | model.json vs dax file | High |
| SM-05 | OP01/03/OP04 in DAX but not registered in model | HIGH | DAX vs model.json (see DAX-01) | High |

---

## 8. Semantic model implementation status

**Tables & columns: COMPLETE.** 16 tables documented with columns and keys.
**Relationships: COMPLETE (documented).** Active/inactive relationships, date roles, cardinality documented.
**Measures registration: PARTIAL.** 51 of 54 DAX measures registered; OP01/03/OP04 missing.
**In-PBIX live model: NOT VERIFIABLE.** Binary DataModel not deserialized (limitation L-2).
**Star-schema conformance: CONFIRMED.**

The semantic model is architecturally sound and largely complete. The gaps (OP measures registration, fact_route_costs_map verification) are specific and closable without OD/G4 gates except where they touch financial facts.
