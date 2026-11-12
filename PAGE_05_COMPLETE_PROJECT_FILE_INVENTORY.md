# AEROVISION 360 — Page 05 Complete Project File Inventory

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY FORENSIC EXAMINATION COMPLETE  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Top-Level Directory Structure

| Directory | File Count | Primary Purpose |
|-----------|-----------|-----------------|
| `data/` | 1,380 | Raw, staging, curated, reference, execution manifests, dataset manifests |
| `governance_decisions/` | 211 | Governance decision JSON records |
| `incident_data/` | 200 | Incident records |
| `remediation_data/` | 422 | Remediation data records |
| `reports/` | 75 | Network expansion reports, audit reports, manifests |
| `scripts/` | 55 | Build scripts, audit scripts, pipeline scripts |
| `deliverables/` | 95 | Power BI deliverables, Excel, data exports |
| `docs/` | 153 | Documentation, governance, blueprints, specifications |
| `src/` | 32 | Source code (generators, ingestion, orchestration, quality, staging, transformations, utilities) |
| `tests/` | 25 | Unit tests |
| `config/` | 2 | Configuration |
| `contracts/` | 1 | BI consumption model contract |
| `qa/` | — | QA directory |
| `power_bi/` | — | Power BI directory (empty at root) |

**Total files:** 2,758 (excluding `.git`, `__pycache__`, `.venv`, `.pytest_cache`, `.ruff_cache`, `.pytest_basetemp*`, `.agents`, `.freebuff`)

---

## 2. Data Layer Inventory

### 2.1 `data/01_raw/` — Raw Layer (Immutable)

| File | Size | Purpose |
|------|------|---------|
| `data/01_raw/source_index.json` | 1,595 bytes | Raw source index |
| `data/01_raw/runs/20261104_141009_275341/sources/airline_id_crosswalk/AIRLINE_ID_CROSSWALK.csv` | 955 | Airline ID crosswalk raw source |
| `data/01_raw/runs/20261104_141009_275341/sources/airline_reference_workbook/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx` | 18,396 | Airline reference workbook (real airline identities) |
| `data/01_raw/runs/20261104_141009_275341/sources/dim_route_keymap_v1/DIM_ROUTE_KEYMAP_V1.csv` | 4,075 | Route keymap raw source |
| `data/01_raw/runs/20261104_141009_275341/sources/dim_route_keymap_v1_manifest/DIM_ROUTE_KEYMAP_V1_MANIFEST.json` | 1,505 | Route keymap manifest |
| `data/01_raw/runs/20261104_141249_936499/run_manifest.json` | 2,993 | Run manifest |
| `data/01_raw/runs/debug_run/sources/test_csv/test.csv` | 18 | Debug test CSV |
| `data/01_raw/runs/test_run_dup/sources/dup_csv/dup_source_temp.csv` | 7 | Duplicate source temp |

**Raw layer notes:** Contains raw source files for airline reference, route keymap, and airline ID crosswalk. No raw passenger feedback or booking transaction raw files are present in this directory.

### 2.2 `data/02_staging/` — Staging Layer (Rebuildable)

Contains multiple staging run directories with accepted/rejected/quarantined sources and staging manifests. Key files:

| File | Size | Purpose |
|------|------|---------|
| `data/02_staging/quarantine/fact_booking_transactions_quarantined.csv` | 320 | Quarantined booking transactions |
| `data/02_staging/quarantine/fact_operating_costs_quarantined.csv` | 220 | Quarantined operating costs |

**Staging layer notes:** Multiple staging runs from 2026-11-04. Contains airline ID crosswalk, airline reference, and route keymap staging data. No customer feedback or booking transaction staging data (those go directly to curated).

### 2.3 `data/03_curated/` — Curated Layer (Power BI Source)

| File | Size | Rows | Columns | PK | Page 05 Relevant? |
|------|------|------|---------|-----|-------------------|
| `dim_customer.csv/.parquet` | 334,985 / 80,485 | 5,000 | 8 | CustomerKey | YES — CustomerSegment, LoyaltyTier, HomeCountry, IsActive |
| `fact_customer_feedback.csv/.parquet` | 204,912 / 80,135 | 2,500 | 14 | FeedbackKey | YES — PRIMARY SOURCE for Page 05 |
| `fact_booking_transactions.csv/.parquet` | 2,974,726 / 974,518 | 9,956 | 45 | BookingTransactionKey | BLOCKED — OD-04 |
| `dim_fare_class.csv/.parquet` | 555 / 4,928 | 8 | 7 | FareClassKey | PARTIAL — CabinClass exists, no FK to facts |
| `dim_airline.csv/.parquet` | 900 / 7,697 | 10 | 12 | AirlineKey | YES — AirlineName |
| `dim_date.csv/.parquet` | 79,083 / 21,801 | 761 | 19 | DateKey | YES — Date filtering |
| `dim_route.csv/.parquet` | 17,914 / 12,440 | 320 | 9 | RouteKey | YES — RouteCode |
| `dim_booking_channel.csv/.parquet` | 407 / 4,138 | 7 | 6 | BookingChannelKey | NO — no FK to facts |
| `dim_currency.csv/.parquet` | 343 / 4,218 | 8 | 6 | CurrencyKey | BLOCKED — OD-04 |
| `dim_airport.csv/.parquet` | 7,927 / 10,217 | 72 | 11 | AirportKey | NO — not customer-facing |
| `dim_aircraft.csv/.parquet` | 24,913 / 13,403 | 440 | 9 | AircraftKey | NO — not customer-facing |
| `dim_aircraft_type.csv/.parquet` | 885 / 5,689 | 12 | 8 | AircraftTypeKey | NO — not customer-facing |
| `dim_disruption_type.csv/.parquet` | 654 / 5,090 | 9 | 7 | DisruptionTypeKey | NO — not customer-facing |
| `fact_flight_operations.csv/.parquet` | 1,075,849 / 376,892 | 5,000 | 25 | FlightOperationKey | PARTIAL — RevenuePassengers (flight-level) |
| `fact_disruptions.csv/.parquet` | 207,939 / 80,458 | 1,754 | 16 | DisruptionKey | NO — not customer-facing |
| `fact_operating_costs.csv/.parquet` | 1,891,279 / 375,123 | 7,480 | 18 | OperatingCostKey | BLOCKED — OD-04 |

**Curated layer notes:** All 16 datasets present as both CSV and Parquet. `fact_customer_feedback` is the primary Page 05 source. `fact_booking_transactions` and `fact_operating_costs` are OD-04 blocked.

### 2.4 `data/04_reference/` — Reference Layer

| File | Size | Purpose |
|------|------|---------|
| `data/04_reference/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx` | 18,396 | Real airline identity reference (10 airlines) |
| `data/04_reference/AIRLINE_ID_CROSSWALK.csv` | 955 | Airline ID crosswalk |
| `data/04_reference/DIM_ROUTE_KEYMAP_V1.csv` | 4,075 | Route keymap V1 |
| `data/04_reference/DIM_ROUTE_KEYMAP_V1_MANIFEST.json` | 1,505 | Route keymap manifest |
| `data/04_reference/ref_exchange_rates.csv` | 230,756 | Exchange rates (2,920 rows, 8 currencies) |
| `data/04_reference/backups/` | — | Backup copies of reference files |

### 2.5 `data/manifests/` — Dataset Manifests

| Manifest File | Size | Dataset |
|---------------|------|---------|
| `airline_id_crosswalk_manifest.json` | 1,286 | Airline ID crosswalk |
| `dim_aircraft_manifest.json` | 3,591 | DimAircraft |
| `dim_aircraft_type_manifest.json` | 1,607 | DimAircraftType |
| `dim_airline_manifest.json` | 1,644 | DimAirline |
| `dim_airport_manifest.json` | 2,173 | DimAirport |
| `dim_booking_channel_manifest.json` | 1,365 | DimBookingChannel |
| `dim_currency_manifest.json` | 1,239 | DimCurrency |
| `dim_customer_manifest.json` | 3,352 | DimCustomer |
| `dim_date_manifest.json` | 1,746 | DimDate |
| `dim_disruption_type_manifest.json` | 1,515 | DimDisruptionType |
| `dim_fare_class_manifest.json` | 1,341 | DimFareClass |
| `dim_route_manifest.json` | 2,656 | DimRoute |
| `fact_booking_transactions_manifest.json` | 6,823 | FactBookingTransactions |
| `fact_customer_feedback_manifest.json` | 3,837 | FactCustomerFeedback |
| `fact_disruptions_manifest.json` | 4,075 | FactDisruptions |
| `fact_flight_operations_manifest.json` | 3,913 | FactFlightOperations |
| `fact_operating_costs_manifest.json` | 5,423 | FactOperatingCosts |
| `reference_manifest.json` | 1,545 | Reference data |

---

## 3. Deliverables Layer Inventory

### 3.1 `deliverables/power_bi/` — Power BI Project

| File | Size | Purpose | Page 05 Relevant? |
|------|------|---------|-------------------|
| `deliverables/power_bi/AEROVISION_360.pbix` | 9,402,888 | Power BI report file | YES — contains report definition |
| `deliverables/power_bi/AEROVISION_360.pbip` | 195 | Power BI project file | YES |
| `deliverables/power_bi/.platform` | 182 | Platform config | YES |
| `deliverables/power_bi/data_sources/data_sources.json` | 1,373 | Data source definitions | YES |
| `deliverables/power_bi/dax/AEROVISION360_Measures.dax` | 11,629 | All DAX measures | YES — CF01-CF14, RV_*, CX_*, NC_*, FL_*, DS_*, OP_* |
| `deliverables/power_bi/power_query/AEROVISION360_DataLoad.m` | 12,628 | Power Query M script | YES |
| `deliverables/power_bi/report/report.json` | 30,205 | Report page/visual definitions | YES — Page 05 defined with 13 visuals |
| `deliverables/power_bi/semantic_model/model.json` | 6,153 | Model table/measure definitions | YES |
| `deliverables/power_bi/semantic_model/semantic_model.json` | 15,887 | Semantic model columns/relationships | YES — complete relationship map |
| `deliverables/power_bi/theme/theme.json` | 189 | Report theme | YES |
| `deliverables/power_bi/audit/DATA_QUALITY_AUDIT.csv` | 1,969 | Data quality audit results | YES |
| `deliverables/power_bi/audit/DAX_MEASURE_AUDIT.md` | 5,188 | DAX measure audit | YES |
| `deliverables/power_bi/audit/GOVERNANCE_COMPLIANCE.md` | 2,866 | Governance compliance audit | YES |
| `deliverables/power_bi/audit/POWER_BI_COMPLETE_AUDIT.md` | 3,481 | Complete Power BI audit | YES |
| `deliverables/power_bi/audit/POWER_BI_IMPLEMENTATION_REPORT.md` | 3,324 | Implementation report | YES |
| `deliverables/power_bi/audit/POWER_BI_REMEDIATION_PLAN.md` | 2,813 | Remediation plan | YES |
| `deliverables/power_bi/audit/RELATIONSHIP_VALIDATION.csv` | 3,838 | Relationship validation | YES |
| `deliverables/power_bi/audit/SAFE_RELATIONSHIP_IMPLEMENTATION_PLAN.md` | 5,650 | Safe relationship plan | YES |

### 3.2 `deliverables/data/` — Deliverable Data Exports

| File | Size | Rows | Purpose |
|------|------|------|---------|
| `deliverables/data/fact_customer_feedback.csv/.parquet` | 204,909 / 80,135 | 2,500 | Duplicate of curated feedback data |
| `deliverables/data/fact_booking_transactions.csv/.parquet` | 2,974,726 / — | 9,956 | Duplicate of curated booking data |
| `deliverables/data/fact_flight_operations.csv/.parquet` | 1,076,408 / 376,892 | 5,000 | Duplicate of curated flight ops |
| `deliverables/data/fact_disruptions.csv/.parquet` | 207,936 / 80,458 | 1,754 | Duplicate of curated disruptions |
| `deliverables/data/fact_operating_costs.csv/.parquet` | 1,891,279 / — | 7,480 | Duplicate of curated operating costs |
| `deliverables/data/dim_*.csv/.parquet` | various | various | Duplicates of curated dimensions |
| `deliverables/excel/AEROVISION_360_AIRLINE_ANALYTICS.xlsx` | 266,725 | — | Excel workbook with 12 sheets |

### 3.3 `deliverables/power_bi_backup_20261105/` — Power BI Backup

Contains backup copies of PBIP, data_sources, DAX, Power Query, report, semantic_model, and theme from 2026-11-05.

---

## 4. Scripts Layer Inventory

### 4.1 Build Scripts (`scripts/`)

| Script | Size | Purpose | Page 05 Relevant? |
|--------|------|---------|-------------------|
| `scripts/build_dim_customer.py` | 11,993 | Builds dim_customer (8 cols, NO Gender) | YES — confirms no Gender |
| `scripts/build_fact_customer_feedback.py` | 17,453 | Builds fact_customer_feedback (14 cols, no TravelType/ratings) | YES — confirms missing fields |
| `scripts/build_fact_booking_transactions.py` | 39,830 | Builds fact_booking_transactions (45 cols, OD-04 blocked) | PARTIAL — booking data source |
| `scripts/build_dim_fare_class.py` | 4,261 | Builds dim_fare_class (8 rows, CabinClass values) | PARTIAL — class dimension |
| `scripts/build_dim_airline.py` | 5,184 | Builds dim_airline | YES — airline dimension |
| `scripts/build_dim_airline_curated.py` | 7,967 | Builds curated dim_airline | YES — airline dimension |
| `scripts/build_dim_date.py` | 6,462 | Builds dim_date | YES — date dimension |
| `scripts/build_dim_route.py` | 18,502 | Builds dim_route | YES — route dimension |
| `scripts/build_dim_airport.py` | 17,877 | Builds dim_airport | NO — not customer-facing |
| `scripts/build_dim_aircraft.py` | 16,390 | Builds dim_aircraft | NO — not customer-facing |
| `scripts/build_dim_aircraft_type.py` | 6,491 | Builds dim_aircraft_type | NO — not customer-facing |
| `scripts/build_dim_booking_channel.py` | 4,276 | Builds dim_booking_channel | NO — unused dimension |
| `scripts/build_dim_currency.py` | 4,294 | Builds dim_currency | BLOCKED — OD-04 |
| `scripts/build_dim_disruption_type.py` | 5,252 | Builds dim_disruption_type | NO — not customer-facing |
| `scripts/build_fact_disruptions.py` | 22,968 | Builds fact_disruptions | NO — not customer-facing |
| `scripts/build_fact_operating_costs.py` | 27,860 | Builds fact_operating_costs | BLOCKED — OD-04 |
| `scripts/build_raw_layer.py` | 2,661 | Builds raw layer | NO — infrastructure |
| `scripts/build_staging_layer.py` | 7,861 | Builds staging layer | NO — infrastructure |
| `scripts/build_curated.py` | 197 | Curated layer orchestrator | NO — infrastructure |
| `scripts/build_airline_reference_workbook.py` | 8,040 | Builds airline reference workbook | YES — real airline identities |
| `scripts/run_pipeline.py` | 11,680 | Pipeline orchestrator | NO — infrastructure |
| `scripts/run_quality_checks.py` | 15,425 | Quality check runner | YES — data quality |
| `scripts/validate_airline_reference.py` | 6,996 | Validates airline reference | YES — airline data |
| `scripts/verify_and_populate_airline_reference.py` | 8,348 | Verifies/populates airline reference | YES — airline data |
| `scripts/audit_dimensions.py` | 35,930 | Dimension audit | YES — dimension validation |
| `scripts/audit_dimensions_production_candidate.py` | 35,930 | Production candidate audit | YES — dimension validation |
| `scripts/audit_dimensions_expanded_candidate.py` | 35,993 | Expanded candidate audit | YES — dimension validation |
| `scripts/promote_network_expansion_release_v2.py` | 14,603 | Network expansion promotion | NO — not customer-facing |
| `scripts/add_iata_numeric_codes.py` | 6,110 | Adds IATA numeric codes | NO — not customer-facing |

### 4.2 Source Code (`src/`)

| Path | Purpose | Page 05 Relevant? |
|------|---------|-------------------|
| `src/generators/generate_fact_flight_operations_financial.py` | Financial fact generator | NO |
| `src/generators/generate_financial_facts.py` | Financial facts generator | NO |
| `src/generators/generate_fx_rates.py` | FX rate generator | NO |
| `src/ingestion/raw_ingestion.py` | Raw ingestion | NO |
| `src/orchestration/pipeline.py` | Pipeline orchestration | NO |
| `src/orchestration/default_registry.py` | Default registry | NO |
| `src/orchestration/failure_handling.py` | Failure handling | NO |
| `src/orchestration/run_registry.py` | Run registry | NO |
| `src/quality/engine.py` | Quality engine | YES — data quality rules |
| `src/quality/rules.py` | Quality rules | YES — data quality rules |
| `src/quality/rules_extended.py` | Extended quality rules | YES — data quality rules |
| `src/quality/anomaly_detection.py` | Anomaly detection | YES — data quality |
| `src/quality/governance_workflow.py` | Governance workflow | YES — governance |
| `src/quality/incident_management.py` | Incident management | YES — incident tracking |
| `src/quality/manifest.py` | Manifest handling | YES — manifest validation |
| `src/quality/models.py` | Quality models | YES — quality models |
| `src/quality/orchestration_integration.py` | Quality orchestration | YES — quality integration |
| `src/quality/profiling.py` | Data profiling | YES — profiling |
| `src/quality/remediation_safeguards.py` | Remediation safeguards | YES — remediation |
| `src/staging/staging_processor.py` | Staging processor | NO — infrastructure |
| `src/transformations/staging.py` | Staging transformations | NO — infrastructure |
| `src/utilities/hashing.py` | SHA-256 hashing | YES — file integrity |
| `src/utilities/io.py` | I/O utilities | NO — infrastructure |
| `src/utilities/logging.py` | Logging utilities | NO — infrastructure |
| `src/utilities/paths.py` | Path utilities | NO — infrastructure |
| `config/settings.py` | Configuration settings | NO — infrastructure |

---

## 5. Documentation Layer Inventory (`docs/`)

### 5.1 Core Project Documents

| Document | Size | Purpose | Page 05 Relevant? |
|----------|------|---------|-------------------|
| `docs/01_PROJECT_SCOPE.md` | 7,176 | Project scope and boundaries | YES |
| `docs/02_BUSINESS_REQUIREMENTS.md` | 5,921 | Business requirements BR-01 through BR-15 | YES |
| `docs/03_DATA_CONTRACTS.md` | 214,355 | Master data contracts (v1.5 DRAFT) | YES — authoritative |
| `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt` | 20,426 | Master build requirements | YES |
| `docs/DAX_KPI_CATALOGUE.md` | 40,677 | 21 KPI definitions (K-01 through K-21) | YES — Page 05 uses K-17 to K-21 |
| `docs/POWER_BI_DASHBOARD_SPECIFICATION.md` | 34,263 | Power BI dashboard specification | YES — Page 5 layout defined |
| `docs/POWER_BI_SEMANTIC_MODEL_BLUEPRINT.md` | 23,627 | Semantic model blueprint | YES |
| `docs/POWER_QUERY_IMPLEMENTATION_BLUEPRINT.md` | 19,215 | Power Query implementation blueprint | YES |
| `docs/SYNTHETIC_DATA_GENERATION_BLUEPRINT.md` | 31,774 | Synthetic data generation blueprint | YES |
| `docs/STAGING_LAYER_IMPLEMENTATION.md` | 20,781 | Staging layer implementation | NO — infrastructure |
| `docs/RAW_LAYER_IMPLEMENTATION.md` | 8,394 | Raw layer implementation | NO — infrastructure |
| `docs/PYTHON_ETL_IMPLEMENTATION_BLUEPRINT.md` | 24,046 | Python ETL blueprint | NO — infrastructure |
| `docs/ENGINEERING_DATA_MODEL_BLUEPRINT.md` | 43,500 | Engineering data model blueprint | YES |

### 5.2 Page-Specific Documents

| Document | Size | Purpose |
|----------|------|---------|
| `docs/PAGE_02_OPERATIONS_DATA_AUDIT.md` | 20,010 | Page 02 audit |
| `docs/PAGE_02_OPERATIONS_DAX_IMPLEMENTATION_REPORT.md` | 12,431 | Page 02 DAX report |
| `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md` | 11,147 | Page 02 DAX spec |
| `docs/PAGE_02_OPERATIONS_PRE_IMPLEMENTATION_VERIFICATION.md` | 17,896 | Page 02 verification |
| `docs/PAGE_02_OPERATIONS_QA_PLAN.md` | 11,161 | Page 02 QA plan |
| `docs/PAGE_02_OPERATIONS_V3_REPLACEMENT_SPEC.md` | 9,428 | Page 02 V3 spec |
| `docs/PAGE_02_OPERATIONS_VISUAL_SPECIFICATION.md` | 14,907 | Page 02 visual spec |
| `docs/PAGE_02_TURNAROUND_TIME_FEASIBILITY_AUDIT.md` | 9,423 | Page 02 TAT audit |
| `docs/PAGE_03_REVENUE_FINANCE_DATA_AUDIT.md` | 20,217 | Page 03 audit |
| `docs/PAGE_03_REVENUE_FINANCE_READINESS.md` | 21,255 | Page 03 readiness |
| `docs/PAGE_03_REVENUE_FINANCE_SCHEMA_DECISION.md` | 15,167 | Page 03 schema decision (OD-04a through OD-04f) |

**No Page 05-specific design document exists in docs/ prior to this investigation.**

---

## 6. Governance Layer Inventory

### 6.1 Governance Decisions (`governance_decisions/`)

211 JSON decision files (decision_DEC_*.json). Key decisions include OD-01A, OD-01B, OD-04, OD-09, OD-11, OD-17, and others. Individual files range from 662 to 854 bytes.

### 6.2 Governance Documentation (`docs/governance/`)

| Document | Size | Purpose |
|----------|------|---------|
| `docs/governance/GOVERNANCE_DECISION_REGISTER.md` | 9,776 | Decision register |
| `docs/governance/GOVERNANCE_APPROVAL_MATRIX.md` | 14,250 | Approval matrix |
| `docs/governance/GOVERNANCE_DECISION_PACK.md` | 39,030 | Decision pack |
| `docs/governance/GOVERNANCE_DEPENDENCY_MAP.md` | 10,828 | Dependency map |
| `docs/governance/OD04_OWNER_DECISION_BRIEF.md` | 15,345 | OD-04 exchange rate decision |
| `docs/governance/OD04_OWNER_DECISION_RECORD.md` | 6,535 | OD-04 decision record |

### 6.3 Owner Decision Documents (`docs/`)

| Document | Size | Purpose |
|----------|------|---------|
| `docs/OD01A_AIRLINE_POPULATION_DECISION.md` | 17,843 | OD-01A airline population |
| `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | 28,471 | OD-01B airline identity |
| `docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md` | 13,891 | OD-04 exchange rate |
| `docs/OWNER_DECISIONS_2026-11-04.md` | 1,395 | Owner decisions summary |
| `docs/AEROVISION_360_OWNER_DECISION_WORKSHEET.md` | 116,895 | Owner decision worksheet |
| `docs/AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md` | 95,042 | Governance investigation |

---

## 7. Other Directories

| Directory | File Count | Purpose |
|-----------|-----------|---------|
| `tests/` | 25 | Unit tests (test_fact_customer_feedback, test_fact_booking_transactions, etc.) |
| `reports/` | 75 | Network expansion reports and audits |
| `qa/` | 0 | QA directory (empty) |
| `power_bi/` | 0 | Power BI directory at root (empty) |
| `config/` | 2 | Configuration (settings.py) |
| `contracts/` | 1 | BI consumption model contract (bi_consumption_model_m311.json) |

---

## 8. Page 05 Relevant File Summary

### Critical Files for Page 05 Implementation

| File | Role |
|------|------|
| `data/03_curated/fact_customer_feedback.parquet` | Primary feedback data source (2,500 rows) |
| `data/03_curated/dim_customer.parquet` | Customer dimension (5,000 rows) |
| `data/03_curated/dim_airline.parquet` | Airline dimension (10 rows) |
| `data/03_curated/dim_date.parquet` | Date dimension (761 rows) |
| `data/03_curated/dim_route.parquet` | Route dimension (320 rows) |
| `data/03_curated/dim_fare_class.parquet` | Fare class dimension (8 rows, no FK to facts) |
| `data/03_curated/fact_booking_transactions.parquet` | Booking data — OD-04 BLOCKED |
| `data/03_curated/fact_flight_operations.parquet` | Flight operations (5,000 rows) |
| `scripts/build_dim_customer.py` | Confirms no Gender column |
| `scripts/build_fact_customer_feedback.py` | Confirms no TravelType, no service ratings |
| `scripts/build_dim_fare_class.py` | Confirms CabinClass values (no Economy Plus) |
| `docs/03_DATA_CONTRACTS.md` | Authoritative data contracts (v1.5 DRAFT) |
| `docs/DAX_KPI_CATALOGUE.md` | K-17 through K-21 definitions for Page 05 |
| `docs/POWER_BI_DASHBOARD_SPECIFICATION.md` | Page 5 layout and filter specification |
| `deliverables/power_bi/dax/AEROVISION360_Measures.dax` | All DAX measures (CF01-CF14 verified) |
| `deliverables/power_bi/report/report.json` | Page 05 visual definitions (13 visuals) |
| `deliverables/power_bi/semantic_model/semantic_model.json` | Complete relationship map |
| `deliverables/power_bi/audit/DATA_QUALITY_AUDIT.csv` | Data quality audit results |
| `deliverables/power_bi/audit/DAX_MEASURE_AUDIT.md` | DAX measure validation |
| `deliverables/power_bi/audit/RELATIONSHIP_VALIDATION.csv` | Relationship validation |
| `deliverables/power_bi/audit/GOVERNANCE_COMPLIANCE.md` | OD-04, OD-11 compliance status |

### Files That Do NOT Exist (Critical Gaps)

| Expected File | Status | Impact |
|---------------|--------|--------|
| `data/03_curated/fact_passenger_satisfaction.parquet` | NOT FOUND | No separate passenger satisfaction dataset |
| `data/03_curated/dim_customer with Gender column` | NOT FOUND | No gender data anywhere |
| `data/03_curated/fact_customer_feedback with TravelType column` | NOT FOUND | No travel type data |
| `data/03_curated/fact_service_ratings.parquet` | NOT FOUND | No six service-rating columns |
| `docs/PAGE_05_*.md` (pre-existing) | NOT FOUND | No prior Page 05 design document |
| Any file containing "Gender" in source data | NOT FOUND | Zero matches in all data files |

---

## 9. Inventory Confidence

- **File enumeration:** Complete (2,758 files across all directories)
- **Data file profiling:** Complete for all 16 curated datasets
- **Build script inspection:** Complete for all customer-relevant scripts
- **Documentation review:** Complete for data contracts, DAX catalogue, dashboard specification
- **Governance review:** Complete for OD-04, OD-11, and related decisions
- **Power BI deliverables:** Complete for report.json, semantic model, DAX, Power Query

**No files were modified during this inventory.** All findings are based on read-only inspection of actual project files.
