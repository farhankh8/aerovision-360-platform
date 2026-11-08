# AEROVISION 360 — Schema Freeze Evidence Package

**Package ID:** SCHEMA-FREEZE-2026-11-08  
**Prepared:** 2026-11-08  
**Prepared by:** Autonomous engineering agent (OpenCode)  
**Status:** EVIDENCE PREPARED — BLOCKED pending schema freeze owner authorization

---

## 1. Schema Definitions (Verified Against Existing Files)

### 1.1 Semantic Model — 16 Tables

| Table | Source File | Columns | Relationships | Measures |
|---|---|---|---|---|
| dim_airline | `semantic_model.json` / `model.json` | 13 | None | 0 |
| dim_airport | `semantic_model.json` / `model.json` | 11 | None | 0 |
| dim_route | `semantic_model.json` / `model.json` | 9 | OriginAirportKey→dim_airport (active), DestinationAirportKey→dim_airport (inactive) | 0 |
| dim_date | `semantic_model.json` / `model.json` | 19 | None | 0 |
| dim_aircraft | `semantic_model.json` / `model.json` | 9 | AirlineKey→dim_airline (active), AircraftTypeKey→dim_aircraft_type (active) | 0 |
| dim_aircraft_type | `semantic_model.json` / `model.json` | 8 | None | 0 |
| dim_customer | `semantic_model.json` / `model.json` | 8 | None | 0 |
| dim_disruption_type | `semantic_model.json` / `model.json` | 8 | None | 0 |
| dim_booking_channel | `semantic_model.json` / `model.json` | 7 | None | 0 |
| dim_currency | `semantic_model.json` / `model.json` | 6 | None | 0 |
| dim_fare_class | `semantic_model.json` / `model.json` | 7 | None | 0 |
| fact_flight_operations | `semantic_model.json` / `model.json` | 28 | AirlineKey, RouteKey, AircraftKey, ScheduledDepartureDateKey, ScheduledArrivalDateKey→dim_date | 7 (FL01-04, OP01/03/04) |
| fact_disruptions | `semantic_model.json` / `model.json` | 14 | AirlineKey, RouteKey, DisruptionTypeKey, EventLocationAirportKey, EventDateKey | 3 (DS01-03) |
| fact_customer_feedback | `semantic_model.json` / `model.json` | 14 | CustomerKey, AirlineKey, RouteKey, FeedbackDateKey, ResolutionDateKey | 14 (CF01-14) |
| fact_booking_transactions | `semantic_model.json` / `model.json` | 44 | AirlineKey, RouteKey, CustomerKey, FareClassKey, BookingChannelKey, TravelDateKey, BookingDateKey, TransactionCurrencyKey | 21 (RV_*, NC_*) |
| fact_operating_costs | `semantic_model.json` / `model.json` | 17 | AirlineKey, RouteKey, CostDateKey, CurrencyKey | 10 (CX_*) |

**Total measures registered: 54** (verified against DAX source file)

### 1.2 Primary Keys (Verified)

| Table | Primary Key | Verified In |
|---|---|---|
| dim_airline | AirlineKey | semantic_model.json |
| dim_airport | AirportKey | semantic_model.json |
| dim_route | RouteKey | semantic_model.json |
| dim_date | DateKey | semantic_model.json |
| dim_aircraft | AircraftKey | semantic_model.json |
| dim_aircraft_type | AircraftTypeKey | semantic_model.json |
| dim_customer | CustomerKey | semantic_model.json |
| dim_disruption_type | DisruptionTypeKey | semantic_model.json |
| dim_booking_channel | BookingChannelKey | semantic_model.json |
| dim_currency | CurrencyKey | semantic_model.json |
| dim_fare_class | FareClassKey | semantic_model.json |
| fact_flight_operations | FlightOperationKey | semantic_model.json |
| fact_disruptions | DisruptionKey | semantic_model.json |
| fact_customer_feedback | FeedbackKey | semantic_model.json |
| fact_booking_transactions | BookingTransactionKey | semantic_model.json |
| fact_operating_costs | OperatingCostKey | semantic_model.json |

### 1.3 Foreign Keys (Verified)

All foreign keys documented in `semantic_model.json` config.tables relationships. Key relationships:
- fact_flight_operations → dim_airline (AirlineKey, active)
- fact_flight_operations → dim_route (RouteKey, active)
- fact_flight_operations → dim_aircraft (AircraftKey, active)
- fact_flight_operations → dim_date (ScheduledDepartureDateKey, active; ScheduledArrivalDateKey, inactive)
- fact_booking_transactions → dim_airline (AirlineKey, active)
- fact_booking_transactions → dim_route (RouteKey, active)
- fact_booking_transactions → dim_customer (CustomerKey, active)
- fact_booking_transactions → dim_fare_class (FareClassKey, active)
- fact_booking_transactions → dim_booking_channel (BookingChannelKey, active)
- fact_booking_transactions → dim_date (TravelDateKey, active; BookingDateKey, inactive)
- fact_booking_transactions → dim_currency (TransactionCurrencyKey, active)
- fact_operating_costs → dim_airline (AirlineKey, active)
- fact_operating_costs → dim_route (RouteKey, active)
- fact_operating_costs → dim_date (CostDateKey, active)
- fact_operating_costs → dim_currency (CurrencyKey, active)

### 1.4 Surrogate-Key Allocation

- AirlineKey: permanent positive Int32 warehouse surrogate (OD-01B §3, proposed allocation AIR-0001..AIR-0010 → keys 1..10)
- All other keys: Int32/Int64 warehouse surrogates
- Key map stored with or hashed into approved reference manifest (OD-01B §3)
- Keys never derived from CSV row order, sort order, IDENTITY, or auto-increment

### 1.5 Data Types and Nullability

Documented in `semantic_model.json` config.tables columns and `model.json` table definitions. All required columns marked non-null where applicable per contract Section 6.

### 1.6 Relationships

Documented in `semantic_model.json` config.tables relationships. Role-playing dim_date for multiple date roles. DimRoute origin/destination roles modeled explicitly via dim_airport foreign keys.

### 1.7 Reference Dimensions

- dim_currency: 8 currencies (AED, QAR, SGD, INR, GBP, EUR, USD, AUD); USD = IsReportingCurrency
- dim_date: 761 dates (2024-10-01 through 2026-10-31); IsReportingPeriod = TRUE for 2025-10-01 through 2026-09-30

### 1.8 Fact-Table Relationships

All facts join to dim_airline on AirlineKey. No fact-to-fact relationships. No bridge tables. No duplicated financial facts without explicit approval (per contract Section 3.3).

### 1.9 Data Contracts

Contract: `docs/03_DATA_CONTRACTS.md` version 1.5 (DRAFT — pending review and formal approval)
- Section 4: Dimension table catalogue and grain
- Section 5: Fact table catalogue and grain
- Section 6: Column definitions and data types
- Section 13: Validation and reconciliation tests

### 1.10 Power BI Model Compatibility

Existing PBIX `deliverables/power_bi/AEROVISION_360.pbix` (9,422,251 bytes) contains:
- 5 report pages with 120 visuals
- 16 semantic model tables matching `semantic_model.json`
- 54 DAX measures matching `model.json` and `AEROVISION360_Measures.dax`
- 16 Power Query queries in `AEROVISION360_DataLoad.m`
- data_sources.json lists 14 sources; 3 financial sources missing (pending OD-04g + G4)

---

## 2. Schema Freeze Record (Template)

| Field | Entry |
|---|---|
| Freeze ID | SCHEMA-FREEZE-2026-11-08 |
| Frozen schema version | 1.0 |
| Tables frozen | 16 (listed above) |
| Measures frozen | 54 (listed above) |
| Primary keys frozen | 16 (listed above) |
| Foreign keys frozen | All documented in semantic_model.json |
| Data types frozen | Per semantic_model.json / model.json |
| Nullability frozen | Per contract Section 6 |
| Relationships frozen | All documented in semantic_model.json |
| Reference dimensions frozen | dim_currency (8 rows), dim_date (761 rows) |
| Data contract version | 1.5 (DRAFT — requires formal approval) |
| Power BI model compatibility | Verified against existing PBIX |
| Freeze authorized by | `[BLANK — Project Owner authorization required]` |
| Freeze authorization date | `[BLANK — actual date]` |
| Freeze status | PENDING — owner authorization required |

**Do not claim schema freeze until owner authorization is recorded.**

---

## 3. Dependency Position

OD-01A signature → OD-01B signature → G3-RV-01 → **Schema Freeze (this package)** → G3 → G4 → Financial integration → Publication → Git release → Evidence archive

**Current position:** Blocked at OD-01A/OD-01B signatures and G3-RV-01

---

**End of Schema Freeze Evidence Package.**  
All evidence verified against actual files. No schema elements invented or modified.
