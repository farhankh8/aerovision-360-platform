# PROJECT ARCHITECTURE AND TECHNOLOGY AUDIT

**Project root:** `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`  
**Audit mode:** Read-only. No implementation files modified.

---

## 1. Technology stack

| Layer | Technology | Evidence | Assessment |
|---|---|---|---|
| Reporting / BI | Microsoft Power BI (Desktop modern file format) | `deliverables/power_bi/AEROVISION_360.pbix`, `.pbip`, `.platform`, `report/report.json` (schema 3.3.0), visual containers (schema 2.12.0) | Modern PBIP/project layout; import-ready; binary PBIX is the authoritative rendered report |
| Semantic model | Power BI tabular model (import mode) | `semantic_model/model.json`, `semantic_model.json`, binary `DataModel` (2.5 MB) | Star-schema design; 16 tables; relationships documented |
| Calculations | DAX | `dax/AEROVISION360_Measures.dax` — 54 measures | 51 registered in model; OP01/OP03/OP04 missing from registration |
| Data ingestion / ETL | Power Query M | `power_query/AEROVISION360_DataLoad.m` — 16 query blocks | CSV source; import-ready; not yet connected to live gateway |
| Source data | CSV + Parquet | `data/03_curated/` — 16 tables | Curated layer populated; raw/staging not populated |
| Reference data | CSV + Excel | `data/04_reference/`, `data/manifests/` | Partial; `ref_airlines.csv`, `ref_exchange_rates.csv`, manifest not created |
| Pipeline / orchestration | Python | `src/` (ingestion, staging, transformations, quality, orchestration, utilities, generators); `scripts/*.py` | Source present; pipeline not yet authorized/executed (G4 blocked) |
| Testing | pytest (Python) | `tests/unit/*.py` (25 files) + `tests/data_quality/`, `tests/reconciliation/` | Framework present; QA PASS gated on independent reviewer |
| Version control | Git | `.git/` — no commits yet; staged/modified/untracked changes | Repository initialized but not committed |

---

## 2. Logical architecture (as documented)

```
RAW (01)  →  STAGING (02)  →  CURATED (03)  →  REFERENCE (04)
                                             ↓
                                 Power Query → Semantic Model → DAX → Power BI Report
                                             ↓
                                 5 dashboard pages, 120 visuals
```

- **Star schema:** Fact tables (`fact_flight_operations`, `fact_disruptions`, `fact_customer_feedback`, `fact_booking_transactions`, `fact_operating_costs`) connect to dimension tables via `*Key` surrogate keys; `dim_date` is the date dimension with active/inactive role-playing relationships.
- **Reporting period:** 2025-10-01 through 2026-09-30 (365 days); `dim_date` continuous coverage 2024-10-01 through 2026-10-31 (761 dates).
- **Disclosure:** `Synthetic Simulation — Not Actual Airline Performance` present in model config, DAX header, data sources, and Excel.

---

## 3. Data model (documented, from `semantic_model/model.json`)

**16 tables:** 11 dimensions + 5 facts

| Table | Type | Measures registered | Key |
|---|---|---|---|
| dim_airline | Dimension | 0 | AirlineKey |
| dim_airport | Dimension | 0 | AirportKey |
| dim_route | Dimension | 0 | RouteKey |
| dim_date | Dimension (Date) | 0 | DateKey |
| dim_aircraft | Dimension | 0 | AircraftKey |
| dim_aircraft_type | Dimension | 0 | AircraftTypeKey |
| dim_customer | Dimension | 0 | CustomerKey |
| dim_disruption_type | Dimension | 0 | DisruptionTypeKey |
| dim_booking_channel | Dimension | 0 | BookingChannelKey |
| dim_currency | Dimension | 0 | CurrencyKey |
| dim_fare_class | Dimension | 0 | FareClassKey |
| fact_flight_operations | Fact | FL01–FL04 (4) | FlightOperationKey |
| fact_disruptions | Fact | DS01–DS03 (3) | DisruptionKey |
| fact_customer_feedback | Fact | CF01–CF14 (14) | FeedbackKey |
| fact_booking_transactions | Fact | RV_* + NC_* (20) | BookingTransactionKey |
| fact_operating_costs | Fact | CX_* (10) | OperatingCostKey |

**Total registered measures: 51.** (Source DAX defines 54; OP01/OP03/OP04 not registered.)

**Documented relationships (active/inactive):**
- `fact_flight_operations` → dim_airline (active, AirlineKey), dim_route (active, RouteKey), dim_aircraft (active, AircraftKey), dim_date ScheduledDepartureDateKey (active), dim_date ScheduledArrivalDateKey (inactive)
- `fact_disruptions` → dim_airline, dim_route, dim_disruption_type, dim_airport (active); dim_date EventDateKey (inactive)
- `fact_customer_feedback` → dim_customer, dim_airline, dim_route (active); dim_date FeedbackDateKey & ResolutionDateKey (inactive)
- `fact_booking_transactions` → dim_airline, dim_route, dim_customer, dim_fare_class, dim_booking_channel (active); dim_date TravelDateKey (active), BookingDateKey (inactive); dim_currency TransactionCurrencyKey (active)
- `fact_operating_costs` → dim_airline, dim_route (active); dim_date CostDateKey (active); dim_currency CurrencyKey (active)
- `dim_route` → dim_airport OriginAirportKey (active), DestinationAirportKey (inactive)
- `dim_aircraft` → dim_airline (active), dim_aircraft_type (active)

**Star-schema conformance:** Generally conforms (facts to dimensions, surrogate keys, date dimension). `dim_route` has an inactive self-referential-ish path to `dim_airport` (destination). `dim_airline`/`dim_airport`/`dim_currency`/`dim_disruption_type`/`dim_customer`/`dim_booking_channel`/`dim_fare_class`/`dim_aircraft_type` have no outgoing relationships (pure lookup dimensions) — expected for a star schema.

---

## 4. Architecture findings

| ID | Finding | Severity | Evidence |
|---|---|---|---|
| AR-01 | Semantic model follows intended star-schema architecture (16 tables, surrogate keys, date dimension, active/inactive date roles) | INFORMATIONAL | `semantic_model/model.json` |
| AR-02 | `dim_airline` includes `BusinessModelClass` column but OD-01B D-05 is PENDING (not authorized to populate); column would be empty/null | MEDIUM | `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` Sec 4, D-05 |
| AR-03 | `fact_route_costs_map` referenced by a Page 04 map visual but NOT present in the 16-table `model.json` | HIGH | Page 04 visual `7b9fc3c1...` (`Operating Cost Geographic Distribution`, X/Y: `fact_route_costs_map`) vs `model.json` tables |
| AR-04 | Two PBIX backups (1 MB each) are single-page stubs ("Page 1", 0 visuals) and do not match the 9.4 MB main PBIX (5 pages, 120 visuals) | HIGH | PBIX version inventory (hashes differ) |
| AR-05 | Production Python pipeline exists in `src/` but is not authorized (G4 blocked); raw/staging layers not populated | MEDIUM | `PROGRESS_LEDGER.md` (G4 BLOCKED), `data/01_raw/`, `data/02_staging/` not populated |
| AR-06 | No deployment configuration, credentials/secret store, RLS, or monitoring evidenced in repository | MEDIUM | Phase I inspection |
| AR-07 | `data_sources/data_sources.json` references 14 CSVs but omits `fact_booking_transactions` and `fact_operating_costs` (consistent with OD-04 block) | INFORMATIONAL | `data_sources/data_sources.json` |

---

## 5. Architecture verdict

The architecture is **sound and appropriately designed** (star schema, import model, DAX measures, Power Query, disclosure, synthetic-data separation). The design documents (blueprints, contracts) are present and coherent. The gap is not architectural design — it is **governance authorization and data loading**: financial facts are blocked by OD-04, reference data is not created, G3/G4 are not approved, and the pipeline is not executed. Architecture does not require rebuilding.
