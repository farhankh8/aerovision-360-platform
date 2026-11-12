# AEROVISION 360 — COMPLETE PROJECT FILE INVENTORY

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY — NO FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Top-Level Directory Structure

The project root is `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360` containing **18 top-level directories** and **~50 root-level files**.

| # | Directory | File Count | Primary Purpose |
|---|-----------|------------|-----------------|
| 1 | `config/` | 3 | Application configuration (settings.py) |
| 2 | `contracts/` | 1 | BI consumption model contract (bi_consumption_model_m311.json) |
| 3 | `data/` | 1,380 | RAW, STAGING, CURATED, REFERENCE layers + manifests + execution logs |
| 4 | `deliverables/` | 95 | Power BI deliverables, Excel workbook, data exports |
| 5 | `docs/` | 153 | Documentation, governance, blueprints, specifications, decision records |
| 6 | `governance_decisions/` | 211 | Individual governance decision JSON files (DEC_*.json) |
| 7 | `incident_data/` | 200 | Incident records (INC_*.json) |
| 8 | `power_bi/` | 0 | Empty directory (Power BI deliverables are under deliverables/power_bi/) |
| 9 | `qa/` | 2 | QA results and screenshots directories |
| 10 | `remediation_data/` | 2 | Remediation data (transactions, transformations) |
| 11 | `reports/` | 75 | Report outputs, audits, manifest JSONs |
| 12 | `scripts/` | 55 | Build scripts, audit scripts, pipeline scripts |
| 13 | `src/` | 32 | Python source code (generators, ingestion, orchestration, quality, staging, transformations, utilities, validation) |
| 14 | `tests/` | 25 | Unit tests (data_quality, reconciliation, unit test suites) |
| 15 | `__pycache__/` | — | Python bytecode cache |
| 16 | `.git/` | — | Git repository |
| 17 | `.venv/` | — | Python virtual environment |
| 18 | Other hidden dirs | — | .pytest_cache, .ruff_cache, .agents, .freebuff, etc. |

---

## 2. Root-Level Files (~50 files)

| File | Size | Type | Purpose |
|------|------|------|---------|
| AEROVISION_360_COMPLETE_FORENSIC_AUDIT.md | 25,405 | Markdown | Complete forensic audit report |
| README.md | 907 | Markdown | Project overview, tech stack, rules |
| all_files.txt | 67 | Text | File listing (error on generation) |
| M311_FINAL_IMPLEMENTATION_REPORT.md | 22,093 | Markdown | M311 final implementation report |
| M312_1_FINAL_IMPLEMENTATION_REPORT.md | 50,749 | Markdown | M312.1 final implementation report |
| M312_2_FINAL_IMPLEMENTATION_REPORT.md | 24,786 | Markdown | M312.2 final implementation report |
| M312_INITIALIZATION_REPORT.md | 17,410 | Markdown | M312 initialization report |
| m311_bi_contract.py | 23,720 | Python | BI contract implementation |
| m311_governed_measures.py | 26,735 | Python | Governed measure definitions |
| m312_consumption_engine.py | 30,690 | Python | Consumption engine |
| m312_measure_details.py | 10,700 | Python | Measure details |
| M312_SUMMARY.md | 628 | Markdown | M312 summary |
| M37_COMPLETION_REPORT.md | 7,133 | Markdown | M37 completion report |
| M37_FINAL_VERIFICATION_REPORT.md | 11,772 | Markdown | M37 final verification |
| M37_REMEDIATION_SUMMARY.txt | 11,777 | Text | M37 remediation summary |
| M37_SUMMARY.txt | 1,559 | Text | M37 summary |
| M38_IMPLEMENTATION_PLAN.md | 2,499 | Markdown | M38 implementation plan |
| M38_IMPLEMENTATION_REPORT.md | 7,698 | Markdown | M38 implementation report |
| M39_FINAL_IMPLEMENTATION_REPORT.md | 7,526 | Markdown | M39 final implementation report |
| PAGE_04_COMPLETE_AUDIT.md | 29,957 | Markdown | Page 04 complete audit |
| PAGE_04_KPI_VALIDATION_AUDIT.md | 15,398 | Markdown | Page 04 KPI validation audit |
| PAGE_05_ADDITIONAL_ANALYTICAL_OPPORTUNITIES.md | 11,283 | Markdown | Page 05 additional opportunities |
| PAGE_05_COMPLETE_ARCHITECTURE_REVIEW.md | 17,765 | Markdown | Page 05 architecture review |
| PAGE_05_COMPLETE_IMPLEMENTATION_PLAN.md | 17,955 | Markdown | Page 05 implementation plan |
| PAGE_05_COMPLETE_PROJECT_FILE_INVENTORY.md | 23,834 | Markdown | Page 05 file inventory |
| PAGE_05_DASHBOARD_BLUEPRINT.md | 12,402 | Markdown | Page 05 dashboard blueprint |
| PAGE_05_DATA_EXPANSION_ARCHITECTURE.md | 17,662 | Markdown | Page 05 data expansion architecture |
| PAGE_05_DATA_FEASIBILITY_MATRIX.md | 6,249 | Markdown | Page 05 feasibility matrix |
| PAGE_05_DATA_GOVERNANCE_AND_RISK_REGISTER.md | 15,737 | Markdown | Page 05 governance register |
| PAGE_05_DAX_AND_GOVERNANCE_VALIDATION.md | 8,127 | Markdown | Page 05 DAX validation |
| PAGE_05_EXTERNAL_DATA_SOURCE_VERIFICATION.md | 18,660 | Markdown | Page 05 external data verification |
| PAGE_05_GENUINE_DATA_SOURCE_CATALOG.md | 15,365 | Markdown | Page 05 data source catalog |
| PAGE_05_IMPLEMENTATION_TRACKER.md | 36,135 | Markdown | Page 05 implementation tracker |
| PAGE_05_INVESTIGATION_REPORT.md | 43,974 | Markdown | Page 05 investigation report |
| PAGE_05_PROJECT_DISCOVERY.md | 19,103 | Markdown | Page 05 project discovery |
| PAGE_05_REFERENCE_ANALYSIS.md | 12,607 | Markdown | Page 05 reference analysis |
| PAGE_05_REFERENCE_REQUIREMENTS.md | 20,982 | Markdown | Page 05 reference requirements |
| PAGE_05_REAL_DATA_SOURCE_AUDIT.md | 29,348 | Markdown | Page 05 real data source audit |
| page05_audit_data.py | 3,496 | Python | Page 05 audit data script |
| read_method.py | 371 | Python | Read method utility |
| STAGE_1_IMPLEMENTATION_REPORT.md | 9,786 | Markdown | Stage 1 implementation report |
| STAGE_2_IMPLEMENTATION_REPORT.md | 6,800 | Markdown | Stage 2 implementation report |
| STAGE_3_IMPLEMENTATION_REPORT.md | 11,431 | Markdown | Stage 3 implementation report |
| STAGE_4_IMPLEMENTATION_REPORT.md | 15,523 | Markdown | Stage 4 implementation report |
| STAGE_5_IMPLEMENTATION_REPORT.md | 11,703 | Markdown | Stage 5 implementation report |
| STAGE_6_FINAL_RELEASE_READINESS_REPORT.md | 22,175 | Markdown | Stage 6 release readiness report |
| test_m312_engine.py | 2,525 | Python | M312 engine test |
| test_output.txt | 2,214 | Text | Test output |
| test_results.txt | 10,253 | Text | Test results |
| test_run.txt | 1,809 | Text | Test run |
| test.txt | 1,809 | Text | Test file |
| trace_flow.py | 277 | Python | Trace flow utility |
| validate_pbi.py | 1,164 | Python | Power BI validation |
| verify_fx.py | 1,191 | Python | FX verification |
| verify_gates.py | 545 | Python | Gate verification |
| verify_governance.py | 369 | Python | Governance verification |
| verify_m310_checks.py | 9,677 | Python | M310 checks verification |
| verify_measures.py | 2,227 | Python | Measures verification |

---

## 3. Data Layer Inventory (`data/`)

### 3.1 `data/01_raw/` — RAW Layer

| Subdirectory | Contents |
|--------------|----------|
| `data/01_raw/runs/20261104_141009_275341/sources/` | airline_id_crosswalk CSV, airline_reference_workbook XLSX, dim_route_keymap_v1 CSV + manifest |
| `data/01_raw/runs/20261104_141249_936499/sources/` | Same raw sources |
| `data/01_raw/runs/debug_run/sources/test_csv/` | test.csv (18 bytes) |
| `data/01_raw/runs/test_run_dup/sources/dup_csv/` | dup_source_temp.csv (7 bytes) |
| `data/01_raw/source_index.json` | Raw source index |

**Total raw datasets:** ~4 raw source files across multiple run directories

### 3.2 `data/02_staging/` — STAGING Layer

| Subdirectory | Contents |
|--------------|----------|
| `data/02_staging/quarantine/` | fact_booking_transactions_quarantined.csv, fact_operating_costs_quarantined.csv |
| `data/02_staging/runs/20261104_151029_526726/` | Staging run with accepted/rejected sources |
| `data/02_staging/runs/20261104_151116_679761/` | Same staging run structure |
| `data/02_staging/runs/20261104_153105_163431/` | Same staging run structure |
| `data/02_staging/runs/20261104_153828_559064/` | Same staging run structure |
| `data/02_staging/runs/20261104_153833_337011/` | Same staging run structure |
| `data/02_staging/runs/20261104_154009_819988/` | Same staging run structure |
| `data/02_staging/runs/20261104_154105_692034/` | Same staging run structure |

### 3.3 `data/03_curated/` — CURATED Layer (33 files)

| File | Rows | Columns | Primary Key | Status |
|------|------|---------|-------------|--------|
| dim_aircraft.csv/.parquet | 440 | 9 | AircraftKey | Curated |
| dim_aircraft_type.csv/.parquet | 12 | 8 | AircraftTypeKey | Curated |
| dim_airline.csv/.parquet | 10 | 12 | AirlineKey | Curated |
| dim_airport.csv/.parquet | 72 | 11 | AirportKey | Curated |
| dim_booking_channel.csv/.parquet | 7 | 6 | BookingChannelKey | Curated |
| dim_currency.csv/.parquet | 8 | 6 | CurrencyKey | Curated |
| dim_customer.csv/.parquet | 5,000 | 8 | CustomerKey | Curated |
| dim_date.csv/.parquet | 761 | 19 | DateKey | Curated |
| dim_disruption_type.csv/.parquet | 9 | 7 | DisruptionTypeKey | Curated |
| dim_fare_class.csv/.parquet | 8 | 7 | FareClassKey | Curated |
| dim_route.csv/.parquet | 320 | 9 | RouteKey | Curated |
| fact_booking_transactions.csv/.parquet | 9,956 | 45 | BookingTransactionKey | Curated |
| fact_customer_feedback.csv/.parquet | 2,500 | 14 | FeedbackKey | Curated |
| fact_disruptions.csv/.parquet | 1,754 | 16 | DisruptionKey | Curated |
| fact_flight_operations.csv/.parquet | 5,000 | 25 | FlightOperationKey | Curated |
| fact_operating_costs.csv/.parquet | 7,480 | 18 | OperatingCostKey | Curated |
| recovery/ | recovery files | | | Recovery layer |

### 3.4 `data/04_reference/` — REFERENCE Layer

| File | Size | Purpose |
|------|------|---------|
| AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx | 18,396 | Real airline identity reference (10 airlines) |
| AIRLINE_ID_CROSSWALK.csv | 955 | Airline ID crosswalk |
| DIM_ROUTE_KEYMAP_V1.csv | 4,075 | Route keymap V1 |
| DIM_ROUTE_KEYMAP_V1_MANIFEST.json | 1,505 | Route keymap manifest |
| ref_exchange_rates.csv | 230,756 | Exchange rates (MISSING — OD-04 blocked) |
| backups/ | Backup copies of reference files | Historical reference backups |

**Critical:** `ref_exchange_rates.csv` does NOT exist — OD-04 blocked.

### 3.5 `data/execution/` — Execution Logs

| Contents | Count |
|----------|-------|
| Execution manifest JSONs | ~1,153 timestamped execution manifest files |
| Each manifest | ~5,759 bytes |

**Note:** ~1,153 execution manifest files exist, representing multiple pipeline execution runs.

### 3.6 `data/manifests/` — Dataset Manifests (18 files)

| Manifest File | Dataset |
|---------------|---------|
| airline_id_crosswalk_manifest.json | Airline ID crosswalk |
| dim_aircraft_manifest.json | DimAircraft |
| dim_aircraft_type_manifest.json | DimAircraftType |
| dim_airline_manifest.json | DimAirline |
| dim_airport_manifest.json | DimAirport |
| dim_booking_channel_manifest.json | DimBookingChannel |
| dim_currency_manifest.json | DimCurrency |
| dim_customer_manifest.json | DimCustomer |
| dim_date_manifest.json | DimDate |
| dim_disruption_type_manifest.json | DimDisruptionType |
| dim_fare_class_manifest.json | DimFareClass |
| dim_route_manifest.json | DimRoute |
| fact_booking_transactions_manifest.json | FactBookingTransactions |
| fact_customer_feedback_manifest.json | FactCustomerFeedback |
| fact_disruptions_manifest.json | FactDisruptions |
| fact_flight_operations_manifest.json | FactFlightOperations |
| fact_operating_costs_manifest.json | FactOperatingCosts |
| reference_manifest.json | Reference data |

---

## 4. Deliverables Layer Inventory (`deliverables/`)

### 4.1 `deliverables/power_bi/` — Power BI Project (95 files)

| Subdirectory/File | Contents |
|-------------------|----------|
| `deliverables/power_bi/AEROVISION_360.pbix` | 9,403,650 bytes — Power BI file (one blank page only) |
| `deliverables/power_bi/AEROVISION_360.pbip` | Power BI project file |
| `deliverables/power_bi/.platform` | Platform configuration |
| `deliverables/power_bi/AEROVISION_360_PRE_IMPLEMENTATION_BACKUP.pbix` | Pre-implementation backup |
| `deliverables/power_bi/AEROVISION_360_VERIFIED_BACKUP.pbix` | Verified backup |
| `deliverables/power_bi/data_sources/data_sources.json` | Data source definitions |
| `deliverables/power_bi/dax/AEROVISION360_Measures.dax` | All DAX measures (FL, DS, CF, RV, CX, NC, OP prefixes) |
| `deliverables/power_bi/power_query/AEROVISION360_DataLoad.m` | Power Query M script (2 of 14 tables defined) |
| `deliverables/power_bi/report/report.json` | Report page definitions (all 5 pages) |
| `deliverables/power_bi/semantic_model/model.json` | Model table/measure definitions |
| `deliverables/power_bi/semantic_model/semantic_model.json` | Semantic model columns and relationships |
| `deliverables/power_bi/theme/theme.json` | Report theme |
| `deliverables/power_bi/audit/DATA_QUALITY_AUDIT.csv` | Data quality audit results |
| `deliverables/power_bi/audit/DAX_MEASURE_AUDIT.md` | DAX measure audit |
| `deliverables/power_bi/audit/gen_data_quality.py` | Data quality generation script |
| `deliverables/power_bi/audit/gen_rel.py` | Relationship generation script |
| `deliverables/power_bi/audit/gen_semantic.py` | Semantic model generation script |
| `deliverables/power_bi/audit/GOVERNANCE_COMPLIANCE.md` | Governance compliance audit |
| `deliverables/power_bi/audit/impl_tests.py` | Implementation tests |
| `deliverables/power_bi/audit/IMPLEMENTATION_TEST_RESULTS.md` | Test results (40 tests, 0 failures) |
| `deliverables/power_bi/audit/POWER_BI_COMPLETE_AUDIT.md` | Complete Power BI audit |
| `deliverables/power_bi/audit/POWER_BI_IMPLEMENTATION_REPORT.md` | Implementation report |
| `deliverables/power_bi/audit/POWER_BI_REMEDIATION_PLAN.md` | Remediation plan (P0-P4) |
| `deliverables/power_bi/audit/RELATIONSHIP_VALIDATION.csv` | Relationship validation |
| `deliverables/power_bi/audit/SAFE_RELATIONSHIP_IMPLEMENTATION_PLAN.md` | Safe relationship implementation plan |

### 4.2 `deliverables/data/` — Curated Data Exports (34 files)

| Subdirectory | Contents |
|--------------|----------|
| `deliverables/data/customer_feedback/` | fact_customer_feedback.csv/.parquet |
| `deliverables/data/dimensions/` | All dimension CSVs/Parquet files |
| `deliverables/data/disruptions/` | fact_disruptions.csv/.parquet |
| `deliverables/data/flight_operations/` | fact_flight_operations.csv/.parquet |
| Individual CSVs/Parquet | All 14 curated datasets |

### 4.3 Other Deliverables

| File | Size | Purpose |
|------|------|---------|
| `deliverables/excel/AEROVISION_360_AIRLINE_ANALYTICS.xlsx` | 266,725 | Excel analytics workbook |
| `deliverables/README.md` | 1,939 | Deliverables README |
| `deliverables/STATUS.md` | 1,748 | Deliverables status |

---

## 5. Documentation Layer (`docs/`) — 153 Files

### 5.1 Core Project Documents

| File | Purpose |
|------|---------|
| docs/01_PROJECT_SCOPE.md | Project scope and boundaries |
| docs/02_BUSINESS_REQUIREMENTS.md | Business requirements BR-01 through BR-15 |
| docs/03_DATA_CONTRACTS.md | Data contracts v1.5 (DRAFT) |
| docs/AEROVISION_360_MASTER_BUILD_PROMPt.txt | Master build prompt v1.1 |
| docs/AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md | Governance investigation |
| docs/AEROVISION_360_MASTER_BUILD_PROMPt.txt | Master build requirements |
| docs/AEROVISION_360_OWNER_DECISION_WORKSHEET.md | Owner decision worksheet |
| docs/DAX_KPI_CATALOGUE.md | DAX KPI catalogue (21 measures) |
| docs/ENGINEERING_DATA_MODEL_BLUEPRINT.md | Engineering data model blueprint |
| docs/IMPLEMENTATION_QA_BLUEPRINT.md | Implementation QA blueprint |
| docs/IMPLEMENTATION_ROADMAP.md | Implementation roadmap |
| docs/M310_ADVANCED_DATA_QUALITY_GOVERNANCE.md | M310 data quality governance |
| docs/M311_ANALYTICAL_WAREHOUSE_SEMANTIC_MODEL.md | M311 semantic model |
| docs/MASTER_AUDIT_FINAL_RECONCILIATION.md | Master audit final reconciliation |
| docs/MASTER_HISTORICAL_MILESTONE_REGISTER.md | Historical milestone register |
| docs/MASTER_MILESTONE_VERIFICATION_REPORT.md | Milestone verification |
| docs/MASTER_PROJECT_AUDIT_AEROVISION_360.md | Master project audit |
| docs/MASTER_PROJECT_BLOCKERS_REGISTER.md | Project blockers register |
| docs/MASTER_PROJECT_COMPLETION_HISTORY.md | Completion history |
| docs/MASTER_PROJECT_COMPLETION_MATRIX.md | Completion matrix |
| docs/MASTER_PROJECT_REMAINING_ROADMAP.md | Remaining roadmap |
| docs/MILESTONE_3_DATA_ENGINEERING_ARCHITECTURE_ASSESSMENT.md | Milestone 3 assessment |
| docs/OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md | OD-01 remediation |
| docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md | OD-01 formal decision |
| docs/OD01_GOVERNANCE_CLOSURE_PROPOSAL.md | OD-01 governance closure |
| docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md | OD-01 independent audit |
| docs/OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt | OD-01 migration final report |
| docs/OD01_MIGRATION_PREPARATION_REPORT.txt | OD-01 migration preparation |
| docs/OD01_OWNER_DECISION_CONFIRMATION.md | OD-01 owner decision confirmation |
| docs/OD01_OWNER_DECISION_PACKET.md | OD-01 owner decision packet |
| docs/OD01_OWNER_DECISION_PACKET.pre-approval-backup.md | OD-01 decision packet backup |
| docs/OD01_OWNER_DECISION_RESOLUTION.md | OD-01 owner decision resolution |
| docs/OD01_REMEDIATION_CHANGE_RECORD.md | OD-01 change record |
| docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md | OD-01 remediation design |
| docs/OD01_REVISION_0.2_CHANGE_RECORD.md | OD-01 revision change record |
| docs/OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md | OD-01 revision re-audit |
| docs/OD01A_AIRLINE_POPULATION_DECISION.md | OD-01A airline population |
| docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md | OD-01B identity reference |
| docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md | OD-04 exchange rate policy |
| docs/OD04_OWNER_DECISION_PACKAGE.md | OD-04 owner decision package |
| docs/OWNER_DECISIONS_2026-11-04.md | Owner decisions summary |
| docs/PAGE_02_OPERATIONS_DATA_AUDIT.md | Page 02 data audit |
| docs/PAGE_02_OPERATIONS_DAX_IMPLEMENTATION_REPORT.md | Page 02 DAX implementation |
| docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md | Page 02 DAX specification |
| docs/PAGE_02_OPERATIONS_PRE_IMPLEMENTATION_VERIFICATION.md | Page 02 pre-implementation verification |
| docs/PAGE_02_OPERATIONS_QA_PLAN.md | Page 02 QA plan |
| docs/PAGE_02_OPERATIONS_V3_REPLACEMENT_SPEC.md | Page 02 V3 replacement spec |
| docs/PAGE_02_OPERATIONS_VISUAL_SPECIFICATION.md | Page 02 visual specification |
| docs/PAGE_02_TURNAROUND_TIME_FEASIBILITY_AUDIT.md | Page 02 turnaround time audit |
| docs/PAGE_03_REVENUE_FINANCE_DATA_AUDIT.md | Page 03 data audit |
| docs/PAGE_03_REVENUE_FINANCE_READINESS.md | Page 03 readiness (NOT IMPLEMENTABLE) |
| docs/PAGE_03_REVENUE_FINANCE_SCHEMA_DECISION.md | Page 03 schema decision |
| docs/POWER_BI_DASHBOARD_SPECIFICATION.md | Power BI dashboard specification |
| docs/POWER_BI_SEMANTIC_MODEL_BLUEPRINT.md | Semantic model blueprint |
| docs/POWER_QUERY_IMPLEMENTATION_BLUEPRINT.md | Power Query implementation blueprint |
| docs/PROGRESS_LEDGER.md | Progress ledger (phase/gate status) |
| docs/PROJECT_RISK_REGISTER.md | Project risk register (R-09, R-10, R-11) |
| docs/PYTHON_ETL_IMPLEMENTATION_BLUEPRINT.md | Python ETL blueprint |
| docs/RAW_LAYER_IMPLEMENTATION.md | Raw layer implementation |
| docs/REQUIREMENTS_TRACEABILITY.md | Requirements traceability (REQ-001 to REQ-028) |
| docs/STAGING_LAYER_IMPLEMENTATION.md | Staging layer implementation |
| docs/SYNTHETIC_DATA_GENERATION_BLUEPRINT.md | Synthetic data generation blueprint |

### 5.2 Backup Subdirectories

- `docs/alignment_backup_20261101_180153/` — Backup of project scope, data contracts, build prompt, progress ledger, requirements traceability
- `docs/g3_approval_backup_20261101/` — G3 approval backup
- `docs/governance/` — Governance decisions (36 files)
- `docs/od01_real_airline_migration_apply_backup_20261101_204216/` — OD-01 migration backup
- `docs/od01_real_airline_migration_backup_20261101_185328/` — OD-01 migration backup
- `docs/od01_remediation_backup_20261101_221748/` — OD-01 remediation backup
- `docs/scope_alignment_backup_20261102_202419/` — Scope alignment backup

### 5.3 Governance Directory (`docs/governance/`) — 36 Files

| File | Purpose |
|------|---------|
| GOVERNANCE_APPROVAL_MATRIX.md | Governance approval matrix |
| GOVERNANCE_DECISION_PACK.md | Decision pack |
| GOVERNANCE_DECISION_REGISTER.md | Decision register |
| GOVERNANCE_DEPENDENCY_MAP.md | Dependency map |
| GOVERNANCE_SIGNATURE_CHECKLIST.md | Signature checklist |
| OD_01_EVIDENCE_REQUIREMENTS_MATRIX.md | OD-01 evidence requirements |
| OD_01_PRESIGNATURE_READINESS_AUDIT.md | Pre-signature readiness |
| OD_01_REMEDIATION_ACTION_REGISTER.md | Remediation action register |
| OD04_OWNER_DECISION_BRIEF.md | OD-04 decision brief |
| OD04_OWNER_DECISION_RECORD.md | OD-04 decision record |
| PAGE_03_REVENUE_FINANCE_SCHEMA_DECISION.md | Page 03 schema decision |
| + 26 other governance decision documents |

### 5.4 Backup Subdirectories

- `docs/backups/OD01_revision_0.2_20261102_213045/` — OD-01 revision backup
- `docs/backups/PORTFOLIO_TRANSITION_20261104/` — Portfolio transition backup

---

## 6. Scripts Layer (`scripts/`) — 55 Files

| File | Purpose |
|------|---------|
| scripts/build_raw_layer.py | Raw layer build |
| scripts/build_staging_layer.py | Staging layer build |
| scripts/build_curated.py | Curated layer build |
| scripts/build_dim_airline.py | Build dim_airline |
| scripts/build_dim_airline_curated.py | Build curated dim_airline |
| scripts/build_dim_airport.py | Build dim_airport |
| scripts/build_dim_aircraft.py | Build dim_aircraft |
| scripts/build_dim_aircraft_type.py | Build dim_aircraft_type |
| scripts/build_dim_booking_channel.py | Build dim_booking_channel |
| scripts/build_dim_currency.py | Build dim_currency |
| scripts/build_dim_customer.py | Build dim_customer |
| scripts/build_dim_date.py | Build dim_date |
| scripts/build_dim_disruption_type.py | Build dim_disruption_type |
| scripts/build_dim_fare_class.py | Build dim_fare_class |
| scripts/build_dim_route.py | Build dim_route |
| scripts/build_fact_booking_transactions.py | Build fact_booking_transactions |
| scripts/build_fact_customer_feedback.py | Build fact_customer_feedback |
| scripts/build_fact_disruptions.py | Build fact_disruptions |
| scripts/build_fact_flight_operations.py | Build fact_flight_operations |
| scripts/build_fact_operating_costs.py | Build fact_operating_costs |
| scripts/build_airline_reference_workbook.py | Build airline reference workbook |
| scripts/run_pipeline.py | Pipeline orchestrator |
| scripts/run_quality_checks.py | Quality check runner |
| scripts/audit_dimensions.py | Dimension audit |
| scripts/validate_airline_reference.py | Airline reference validation |
| scripts/verify_and_populate_airline_reference.py | Verify and populate airline reference |
| scripts/promote_network_expansion_release_v2.py | Network expansion promotion |
| scripts/add_iata_numeric_codes.py | Add IATA numeric codes |
| scripts/fix_*.py (20 files) | Various fix scripts |
| scripts/find_*.py (6 files) | Various find scripts |
| scripts/debug_test.py | Debug test |
| scripts/investigate.py | Investigation script |
| scripts/inspect_dim_airline.py | Inspect dim_airline |
| scripts/inspect_tests.py | Inspect tests |

---

## 7. Source Code Layer (`src/`) — 32 Files

### 7.1 `src/generators/`
- generate_fact_flight_operations_financial.py
- generate_financial_facts.py
- generate_fx_rates.py

### 7.2 `src/ingestion/`
- raw_ingestion.py

### 7.3 `src/orchestration/`
- pipeline.py
- default_registry.py
- failure_handling.py
- run_registry.py

### 7.4 `src/quality/`
- engine.py
- rules.py
- rules_extended.py
- anomaly_detection.py
- governance_workflow.py
- incident_management.py
- manifest.py
- models.py
- orchestration_integration.py
- profiling.py
- remediation_safeguards.py

### 7.5 `src/staging/`
- staging_processor.py

### 7.6 `src/transformations/`
- staging.py

### 7.7 `src/utilities/`
- hashing.py
- io.py
- logging.py
- paths.py

### 7.8 `src/validation/`
- Empty directory

---

## 8. Test Layer (`tests/`) — 25 Files

| Subdirectory | Contents |
|--------------|----------|
| `tests/unit/` | 26 unit test files |
| `tests/data_quality/` | Empty directory |
| `tests/reconciliation/` | Empty directory |

**Unit Tests:**
| Test File | Purpose |
|-----------|---------|
| test_dim_airline_curated.py | Dim airline curated test |
| test_fact_booking_transactions.py | Fact booking transactions test |
| test_fact_customer_feedback.py | Fact customer feedback test |
| test_fact_disruptions.py | Fact disruptions test |
| test_fact_flight_operations.py | Fact flight operations test |
| test_fact_operating_costs.py | Fact operating costs test |
| test_hashing.py | Hashing utility test |
| test_io.py | I/O utility test |
| test_logging.py | Logging utility test |
| test_m310_quality_governance.py | M310 quality governance test |
| test_m311_analytical_validation.py | M311 analytical validation |
| test_m311_integration.py | M311 integration test |
| test_m38_integration.py | M38 integration test |
| test_m39_observability.py | M39 observability test |
| test_paths.py | Paths test |
| test_pipeline_cli.py | Pipeline CLI test |
| test_pipeline.py | Pipeline test |
| test_raw_ingestion.py | Raw ingestion test |
| test_settings.py | Settings test |
| test_stage2_power_query_integration.py | Stage 2 Power Query integration test |
| test_stage3_semantic_model.py | Stage 3 semantic model test |
| test_stage4_financial_dax.py | Stage 4 financial DAX test |
| test_stage5_page03_dashboard.py | Stage 5 Page 03 dashboard test |
| test_staging_layer.py | Staging layer test |
| test_staging_processor.py | Staging processor test |

---

## 9. Reports Layer (`reports/`) — 75 Files

| Subdirectory | Contents |
|--------------|----------|
| `reports/airline_reference_remediation_20261104/` | Airline reference remediation |
| `reports/audit/` | Audit reports |
| `reports/final_case_study/` | Final case study |
| `reports/network_expansion_20261104/` | Network expansion report |
| `reports/production_expansion_audit/` | Production expansion audit |
| `reports/DIMENSIONS_CONSOLIDATED_AUDIT_*.json` | 7 dimension audit JSON files |

---

## 10. Other Directories

| Directory | File Count | Purpose |
|-----------|------------|---------|
| `qa/` | 2 | QA results and screenshots directories |
| `remediation_data/` | 2 | Remediation data (transactions, transformations) |
| `config/` | 3 | Configuration (settings.py) |

---

## 11. Key Observations from File Inventory

| Observation | Detail |
|-------------|--------|
| Total files inspected | ~2,758 |
| Power BI deliverables present | report.json, DAX measures, Power Query M, semantic model JSON |
| PBIX file | Exists (9,403,650 bytes) but contains only one blank page |
| Curated datasets | 14 datasets, all present as CSV + Parquet |
| Reference datasets | Missing ref_exchange_rates.csv (OD-04 blocked) |
| Staging data | Multiple staging runs present |
| Execution logs | ~1,153 execution manifest files |
| Governance decisions | 211 decision JSON files |
| Incident records | 200 incident JSON files |
| Documentation files | ~93 markdown files in docs/ |
| DAX measures | 54 measures defined across FL, DS, CF, RV, CX, NC, OP prefixes |
| Tests | 25 unit test files; 40 implementation tests (all PASS) |

---

**Inventory complete.** All 18 top-level directories and ~50 root-level files have been catalogued. Source data files, Power BI specifications, documentation, tests, scripts, and governance documents have all been located and classified.
