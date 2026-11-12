# COMPLETE POWER QUERY AND ETL AUDIT

**Source:** `deliverables/power_bi/power_query/AEROVISION360_DataLoad.m` (read in full, 132 lines)  
**Compared against:** source data in `data/03_curated/` and `deliverables/data/`; data contract `docs/03_DATA_CONTRACTS.md`  
**Audit mode:** Read-only. M script not executed.

---

## 1. Query inventory

The M script defines **16 query blocks** (one `let…in` block per table), each reading a CSV from `deliverables/data/` and promoting headers + changing types. No query folding, no parameters, no error-handling blocks beyond type conversion.

| # | Query (table) | Source file | Rows (source) | Columns | Status |
|---|---|---|---|---|---|
| 1 | dim_airline | `deliverables/data/dim_airline.csv` | 10 | 12 | Defined |
| 2 | dim_airport | `deliverables/data/dim_airport.csv` | 72 | 11 | Defined |
| 3 | dim_route | `deliverables/data/dim_route.csv` | 320 | 9 | Defined |
| 4 | dim_date | `deliverables/data/dim_date.csv` | 761 | 19 | Defined |
| 5 | dim_aircraft | `deliverables/data/dim_aircraft.csv` | 440 | 9 | Defined |
| 6 | dim_aircraft_type | `deliverables/data/dim_aircraft_type.csv` | 12 | 8 | Defined |
| 7 | dim_customer | `deliverables/data/dim_customer.csv` | 785 | 8 | Defined |
| 8 | dim_disruption_type | `deliverables/data/dim_disruption_type.csv` | 9 | 7 | Defined |
| 9 | dim_booking_channel | `deliverables/data/dim_booking_channel.csv` | 7 | 6 | Defined |
| 10 | dim_currency | `deliverables/data/dim_currency.csv` | 8 | 6 | Defined |
| 11 | dim_fare_class | `deliverables/data/dim_fare_class.csv` | 8 | 8 | Defined |
| 12 | fact_flight_operations | `deliverables/data/fact_flight_operations.csv` | 5,000 | 26 | Defined |
| 13 | fact_disruptions | `deliverables/data/fact_disruptions.csv` | 1,754 | 16 | Defined |
| 14 | fact_customer_feedback | `deliverables/data/fact_customer_feedback.csv` | 2,500 | 16 | Defined |
| 15 | fact_booking_transactions | `deliverables/data/fact_booking_transactions.csv` | 9,956 | 50 | Defined |
| 16 | fact_operating_costs | `deliverables/data/fact_operating_costs.csv` | 7,480 | 18 | Defined |

**Total: 16 query blocks = 11 dimensions + 5 facts.** This reconciles to the 16 tables in `model.json`/`semantic_model.json`.

> Contradiction resolved: prior reports claimed "Power Query defines only 2 of 14 tables" or "2 of 16". The actual M file defines 16 query blocks covering all 16 model tables. The "2 of 14/16" figures are stale/incorrect (see Phase J).

---

## 2. Per-query review

Each query follows the identical pattern:
```
let
    Source = Csv.Document(File.Contents("deliverables/data/<table>.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"<col>", <type>}, ...})
in
    ChangedType
```

Observations per query:
- All sources are CSV files under `deliverables/data/`. Parquet counterparts exist but are NOT imported by the M script (comment on line 3: "Parquet counterparts exist but are not imported alongside CSV").
- `Encoding=65001` (UTF-8) specified for all.
- Column types are explicitly mapped (Int64, type text, type number, type date, type datetimezone, type logical).
- No custom columns, no filtering, no error handling, no null handling, no duplicate handling, no query parameters.
- All 16 expected tables from the specification are present: dim_airline, dim_airport, dim_route, dim_date, dim_aircraft, dim_aircraft_type, dim_customer, dim_disruption_type, dim_booking_channel, dim_currency, dim_fare_class, fact_booking_transactions, fact_customer_feedback, fact_disruptions, fact_flight_operations, fact_operating_costs.

---

## 3. Data type and handling review

| Aspect | Finding | Severity |
|---|---|---|
| Source connection | CSV files in `deliverables/data/`; paths relative (`deliverables/data/…`) | INFORMATIONAL |
| Header promotion | `Table.PromoteAllHeaders` used for all | OK |
| Type mapping | Explicit types for every column; matches `semantic_model.json` columns | OK |
| Error handling | None (no `try/otherwise`, no remove errors) | MEDIUM — malformed rows would fail refresh |
| Null handling | None explicit; logical/number columns may contain nulls | MEDIUM |
| Duplicate handling | None (no duplicate removal on keys) | MEDIUM — PK uniqueness not enforced in query |
| Refresh dependency | All queries depend on CSV files; no query-to-query dependencies (flat load) | OK |
| Connected to semantic model | Queries defined but the PBIX data source connection is via `data_sources/data_sources.json` (14 CSV refs; omits fact_booking_transactions & fact_operating_costs) | MEDIUM |

---

## 4. Required-table reconciliation

The audit standard lists 16 expected tables (11 dims + 5 facts). **All 16 are defined in the M file.** This contradicts prior reports of "2 of 14" vs "2 of 16".

| Expected table | Defined in M? | In model.json? | In source data (03_curated)? |
|---|---|---|---|
| dim_airline | Yes | Yes | Yes |
| dim_airport | Yes | Yes | Yes |
| dim_route | Yes | Yes | Yes |
| dim_date | Yes | Yes | Yes |
| dim_aircraft | Yes | Yes | Yes |
| dim_aircraft_type | Yes | Yes | Yes |
| dim_customer | Yes | Yes | Yes |
| dim_disruption_type | Yes | Yes | Yes |
| dim_booking_channel | Yes | Yes | Yes |
| dim_currency | Yes | Yes | Yes |
| dim_fare_class | Yes | Yes | Yes |
| fact_booking_transactions | Yes | Yes | Yes |
| fact_customer_feedback | Yes | Yes | Yes |
| fact_disruptions | Yes | Yes | Yes |
| fact_flight_operations | Yes | Yes | Yes |
| fact_operating_costs | Yes | Yes | Yes |

All 16 reconciled across M, model, and source data.

---

## 5. Data source connection

`data_sources/data_sources.json` references **14 CSV files** (fact_flight_operations, fact_disruptions, fact_customer_feedback, and the 11 dimensions). It **omits** `fact_booking_transactions` and `fact_operating_costs` — consistent with OD-04 blocking those financial facts. The M script itself defines all 16, but the registered data sources only wire up 14.

**Finding PQ-01 (MEDIUM):** `data_sources.json` references only 14 of 16 tables; fact_booking_transactions and fact_operating_costs are defined in M and model but not in data_sources.json (blocked by OD-04). This is consistent with the OD-04 block, not a defect — but it means financial facts cannot refresh until OD-04 is approved and the sources are added.

**Finding PQ-02 (MEDIUM):** No error/null/duplicate handling in M queries; no PK uniqueness enforcement. Refresh could fail on malformed rows.

**Finding PQ-03 (INFORMATIONAL):** Parquet counterparts exist but are not imported; M imports CSV only.

---

## 6. Power Query implementation status

**Query definitions: COMPLETE.** All 16 expected tables defined with sources, types, and header promotion.
**Connection to model: PARTIALLY CONNECTED.** 14 of 16 sources wired in data_sources.json; 2 financial facts blocked by OD-04.
**Execution: NOT EXECUTED.** M script not run (read-only); no live gateway; refresh reliability not tested.

Power Query is **not the gating item** — queries are written. The gate is OD-04 (financial facts) and G4 authorization (data generation/load).
