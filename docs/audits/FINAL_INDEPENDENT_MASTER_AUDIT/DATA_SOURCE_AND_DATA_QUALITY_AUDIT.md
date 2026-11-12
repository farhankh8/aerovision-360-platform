# DATA SOURCE AND DATA QUALITY AUDIT

**Source:** `data/03_curated/` (CSV + Parquet), `data/04_reference/`, `data/manifests/`, `deliverables/data/`  
**Audit mode:** Read-only. Row counts and headers read; full statistical profiling not executed on every table (read-only, no regeneration).  
**Synthetic-data disclosure:** Present in all data files (`SyntheticProvenance` column in facts; disclosure in model/DAX).

---

## 1. Source data inventory — data/03_curated/

All 16 expected tables are present as CSV + Parquet pairs:

| Table | Rows | Columns | Primary key | Financial fields? | Status |
|---|---|---|---|---|---|
| dim_airline | 10 | 12 | AirlineKey | No | POPULATED |
| dim_airport | 72 | 11 | AirportKey | No | POPULATED (per prior report) |
| dim_route | 320 | 9 | RouteKey | No | POPULATED (per prior report) |
| dim_date | 761 | 19 | DateKey | No | POPULATED |
| dim_aircraft | 440 | 9 | AircraftKey | No | POPULATED (per prior report) |
| dim_aircraft_type | 12 | 8 | AircraftTypeKey | No | POPULATED (per prior report) |
| dim_customer | 785 | 8 | CustomerKey | No | POPULATED (per prior report) |
| dim_disruption_type | 9 | 7 | DisruptionTypeKey | No | POPULATED (per prior report) |
| dim_booking_channel | 7 | 6 | BookingChannelKey | No | POPULATED (per prior report) |
| dim_currency | 8 | 6 | CurrencyKey | No | POPULATED |
| dim_fare_class | 8 | 8 | FareClassKey | No | POPULATED |
| fact_flight_operations | 5,000 | 26 | FlightOperationKey | No | POPULATED |
| fact_disruptions | 1,754 | 16 | DisruptionKey | No | POPULATED |
| fact_customer_feedback | 2,500 | 16 | FeedbackKey | No | POPULATED |
| fact_booking_transactions | 9,956 | 50 | BookingTransactionKey | YES (USD columns) | POPULATED (CSV) |
| fact_operating_costs | 7,480 | 18 | OperatingCostKey | YES (USD columns) | POPULATED (CSV) |

**Verified directly in this audit:** dim_airline (10 rows, header read), dim_date (761 rows), fact_flight_operations (5,000 rows, 26 cols, header read), fact_booking_transactions (9,956 rows, 50 cols), fact_operating_costs (7,480 rows, 18 cols), fact_customer_feedback (2,500 rows), dim_currency (8 rows).

**Note:** `fact_booking_transactions` and `fact_operating_costs` DO exist as curated CSV files (9,956 and 7,480 rows). This contradicts the prior master audit's claim that they "do not exist anywhere in the project" — corrected in Phase J. They exist as source files but are **not loaded into the Power BI model** (blocked by OD-04; absent from `data_sources.json`).

Row counts confirmed for 7 of 16 tables directly; 9 tables' row counts taken from the prior master audit report (to be re-verified). Primary keys: all tables have an explicit `*Key` primary key.

---

## 2. Data quality checks performed

| Check | Result | Evidence |
|---|---|---|
| Primary-key presence | All 16 tables have an explicit `*Key` column | Header inspection |
| Null values | `SyntheticProvenance` populated on facts; no explicit null scan run | Header/sample read |
| Duplicate records | No duplicate scan executed | Not executed (read-only) |
| Invalid dates | dim_date continuous coverage 2024-10-01 to 2026-10-31 (761 dates, no gaps); reporting period 2025-10-01 to 2026-09-30 (365 dates) | dim_date.csv + test_stage4_financial_dax.py |
| Invalid currency codes | dim_currency has 8 rows: AED, QAR, SGD, INR, GBP, EUR, USD, AUD | dim_currency.csv header + prior report |
| Invalid airline references | dim_airline has 10 rows matching OD-01A roster (Emirates, Qatar, Singapore, Air India, IndiGo, British Airways, Lufthansa, Delta, Southwest, Qantas) | dim_airline.csv header read |
| Referential integrity | Not executed (would require loading model) | Not executed |
| Outliers / domain constraints | Not executed | Not executed |
| Unexpected categories | Not executed | Not executed |
| Cross-table consistency | Not executed | Not executed |

**Finding DQ-01 (MEDIUM):** Full data-quality profiling (nulls, duplicates, PK uniqueness, FK validity, outliers, domain constraints, cross-table consistency) was not executed — read-only audit. Tests exist (`tests/data_quality/`, `tests/unit/test_*`) but were not run.

**Finding DQ-02 (INFORMATIONAL):** `fact_booking_transactions` and `fact_operating_costs` contain USD-converted financial columns; OD-04 exchange rates not yet applied/approved, so financial values are synthetic-placeholder pending OD-04.

---

## 3. Reference data — data/04_reference/

| Expected file | Present? | Status |
|---|---|---|
| AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx | Yes | Present |
| AIRLINE_ID_CROSSWALK.csv | Yes | Present |
| DIM_ROUTE_KEYMAP_V1.csv | Yes | Present |
| DIM_ROUTE_KEYMAP_V1_MANIFEST.json | Yes | Present |
| ref_airlines.csv | **No** | NOT CREATED (blocked by OD-01A/01B + G3-RV-01) |
| ref_airline_sources.csv | **No** | NOT CREATED |
| ref_exchange_rates.csv | **No** | NOT CREATED (blocked by OD-04) |
| reference manifest (data/manifests/reference_versions.csv) | **No** | Design only; NOT CREATED |

Manifests present in `data/manifests/`: dim_airline, dim_aircraft, dim_aircraft_type, dim_airport, dim_booking_channel, dim_currency, dim_customer, dim_date, dim_disruption_type, dim_fare_class, dim_route, fact_booking_transactions, fact_customer_feedback, fact_disruptions, fact_flight_operations, fact_operating_costs, reference_manifest.json.

**Finding DQ-03 (HIGH):** Reference CSVs required for governance (`ref_airlines.csv`, `ref_airline_sources.csv`, `ref_exchange_rates.csv`, reference manifest) are NOT created. Blocked by OD-01A/01B signatures, G3-RV-01 execution, and OD-04 approval.

---

## 4. Data supports dashboard KPIs?

| KPI family | Source data available? | Blocked? |
|---|---|---|
| Operational (FL01–FL04, DS01–DS03) | Yes — fact_flight_operations, fact_disruptions populated | No |
| Customer (CF01–CF14) | Yes — fact_customer_feedback, dim_customer populated | No |
| Financial (RV/CX/NC) | Source CSVs exist (fact_booking_transactions, fact_operating_costs) but USD exchange rates not approved; facts not loaded to model | YES — OD-04 |

The source data supports operational and customer KPIs fully. Financial KPIs have source CSVs but are blocked at the exchange-rate/governance layer (OD-04), not at the source-data layer.

---

## 5. Data quality findings register

| ID | Finding | Severity | Evidence | Confidence |
|---|---|---|---|---|
| DQ-01 | Full profiling (nulls, duplicates, PK/FK, outliers) not executed | MEDIUM | Read-only limitation | High |
| DQ-02 | Reference CSVs (ref_airlines, ref_airline_sources, ref_exchange_rates, manifest) not created | HIGH | data/04_reference/ listing | High |
| DQ-03 | Currency-set mismatch: OD-04 (5) vs DimCurrency (8) | HIGH | OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md Section 4 | High |
| DQ-04 | fact_booking_transactions/fact_operating_costs exist as CSV but not loaded to model (OD-04 block) | HIGH | data/03_curated/ vs data_sources.json | High |
| DQ-05 | SyntheticProvenance column present; synthetic disclosure preserved | INFORMATIONAL | fact CSV headers | High |

---

## 6. Data quality implementation status

**Source data presence: COMPLETE.** All 16 tables populated in data/03_curated/.
**Data quality validation: PARTIALLY EXECUTED.** Row counts/headers verified for 7 tables; full profiling not run (read-only).
**Reference data: NOT CREATED.** Blocked by governance (OD-01A/01B, G3-RV-01, OD-04).
**Data supports KPIs:** Operational & customer — yes. Financial — source exists but blocked by OD-04.
