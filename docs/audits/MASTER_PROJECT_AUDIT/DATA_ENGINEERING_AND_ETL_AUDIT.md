# AEROVISION 360 — DATA ENGINEERING AND ETL AUDIT

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08-DE  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY AUDIT — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Data Engineering Architecture Overview

AEROVISION 360 uses a **layered batch ETL architecture** with four distinct layers:

| Layer | Folder | Purpose | Write Policy | Consumer |
|-------|--------|---------|--------------|----------|
| RAW | `data/01_raw/` | Preserve generated source records with deliberate defects | Immutable after generation | STAGING and audit |
| STAGING | `data/02_staging/` | Standardize, type, deduplicate, flag, validate | Rebuildable from RAW | CURATED |
| CURATED | `data/03_curated/` | Clean star-schema tables and USD measures | Rebuildable from STAGING | Power BI |
| REFERENCE | `data/04_reference/` | Hold controlled code lists, calendars, rates, assumptions | Version-controlled | STAGING, CURATED, Power BI |

### Cross-Layer Rules

- RAW is never overwritten, cleaned in place, or silently corrected
- Every CURATED row traces to RAW, controlled reference, or documented allocation
- Transformations are deterministic for the same seed, configuration, source files, and code version
- Invalid records are rejected with reason codes or quarantined — never silently deleted
- No aggregation that duplicates revenue/cost across tables
- No aggregation of different currencies without USD conversion

---

## 2. Build Script Inventory

### 2.1 Build Scripts (`scripts/`)

| Script | Purpose | Tables Built | Status |
|--------|---------|--------------|--------|
| build_raw_layer.py | Raw layer build | RAW layer datasets | EXISTS |
| build_staging_layer.py | Staging layer build | STAGING layer datasets | EXISTS |
| build_curated.py | Curated layer build | CURATED layer orchestration | EXISTS |
| build_dim_airline.py | Build dim_airline | dim_airline | EXISTS |
| build_dim_airline_curated.py | Build curated dim_airline | dim_airline | EXISTS |
| build_dim_airport.py | Build dim_airport | dim_airport | EXISTS |
| build_dim_aircraft.py | Build dim_aircraft | dim_aircraft | EXISTS |
| build_dim_aircraft_type.py | Build dim_aircraft_type | dim_aircraft_type | EXISTS |
| build_dim_booking_channel.py | Build dim_booking_channel | dim_booking_channel | EXISTS |
| build_dim_currency.py | Build dim_currency | dim_currency | EXISTS |
| build_dim_customer.py | Build dim_customer | dim_customer | EXISTS |
| build_dim_date.py | Build dim_date | dim_date | EXISTS |
| build_dim_disruption_type.py | Build dim_disruption_type | dim_disruption_type | EXISTS |
| build_dim_fare_class.py | Build dim_fare_class | dim_fare_class | EXISTS |
| build_dim_route.py | Build dim_route | dim_route | EXISTS |
| build_fact_booking_transactions.py | Build fact_booking_transactions | fact_booking_transactions | EXISTS |
| scripts/build_fact_customer_feedback.py | Build fact_customer_feedback | fact_customer_feedback | EXISTS |
| scripts/build_fact_disruptions.py | Build fact_disruptions | fact_disruptions | EXISTS |
| scripts/build_fact_flight_operations.py | Build fact_flight_operations | fact_flight_operations | EXISTS |
| scripts/build_fact_operating_costs.py | Build fact_operating_costs | fact_operating_costs | EXISTS |
| scripts/build_airline_reference_workbook.py | Build airline reference workbook | dim_airline reference | EXISTS |
| scripts/run_pipeline.py | Pipeline orchestrator | All tables | EXISTS |
| scripts/run_quality_checks.py | Quality check runner | Quality validation | EXISTS |

### 2.2 Source Code (`src/`)

| Subdirectory | Files | Purpose |
|--------------|-------|---------|
| src/generators/ | 3 files | Data generation (flight operations financial, financial facts, FX rates) |
| src/ingestion/ | raw_ingestion.py | Raw data ingestion |
| src/orchestration/ | 5 files | Pipeline orchestration, default registry, failure handling, run registry |
| src/quality/ | 11 files | Data quality engine, rules, anomaly detection, governance, incident management |
| src/staging/ | staging_processor.py | Staging data processing |
| src/transformations/ | staging.py | Staging transformations |
| src/utilities/ | 4 files | Hashing, I/O, logging, paths utilities |
| src/validation/ | Empty | Validation module (empty) |

---

## 3. Data Generation Pipeline

### 3.1 Deterministic Generation

All data generation uses **deterministic NumPy random generators** with fixed seeds:

| Dataset | Seed | Reference |
|---------|------|-----------|
| dim_customer | 3602026 | build_dim_customer.py |
| fact_customer_feedback | 3602026 | build_fact_customer_feedback.py |
| fact_booking_transactions | 3602027 | build_fact_booking_transactions.py |

**Determinism guarantee:** A rerun with the same seed and configuration produces the same logical dataset.

### 3.2 Data Quality Defects

The data generation includes **deliberate defects** for testing:

| Dataset | Defect Type | Count | Description |
|---------|-------------|-------|-------------|
| dim_airline | Null columns | 3 | AirlineGroup, BusinessModelClass, StatusEffectiveDate all null |
| dim_customer | Null column | 1 | LoyaltyTier has 686 nulls |
| fact_flight_operations | Null columns | 4 | ActualDeparture/Arrival timestamps, DepartureDelayMinutes, ArrivalDelayMinutes, BlockMinutes (224 each) |
| fact_disruptions | Null columns | 2 | EventEndTimestampUTC (322), ReactionaryEvidenceID (1682) |
| fact_customer_feedback | Null columns | 3 | SatisfactionScore (603), ComplaintCategory (1862), ResolutionDateKey (1896) |

---

## 4. Data Quality Checks

| Check | Status | Evidence |
|-------|--------|----------|
| Row count validation | PASS | 14 datasets pass expected row counts |
| Primary key uniqueness | PASS | All PKs unique and non-null |
| Referential integrity | PASS | 0 orphans across all validated FK paths |
| Data type validation | PARTIAL | Power Query M defines data types; only 2 of 14 tables defined |
| Duplicate row check | PASS | 0 duplicate rows in any dataset |
| Null value documentation | PARTIAL | Nulls documented in DATA_QUALITY_AUDIT.csv |

---

## 5. Data Quality Issues

| Issue ID | Severity | Dataset | Column | Count | Impact |
|----------|----------|---------|--------|-------|
| DQ-01 | MEDIUM | dim_airline | AirlineGroup | 10 nulls | Airline enrichment missing |
| DQ-02 | MEDIUM | dim_airline | BusinessModelClass | 10 nulls | Airline enrichment missing |
| DQ-03 | MEDIUM | dim_airline | StatusEffectiveDate | 10 nulls | Airline enrichment missing |
| DQ-04 | MEDIUM | dim_customer | LoyaltyTier | 686 nulls | Customer segmentation incomplete |
| DQ-05 | MEDIUM | fact_flight_operations | ActualDepartureTimestampUTC | 224 nulls | Cancelled flights; affects delay calculations |
| DQ-06 | MEDIUM | fact_flight_operations | ActualArrivalTimestampUTC | 224 nulls | Cancelled flights; affects delay calculations |
| DQ-07 | MEDIUM | fact_flight_operations | DepartureDelayMinutes | 224 nulls | Cancelled flights; affects OTP calculation |
| DQ-08 | MEDIUM | fact_flight_operations | ArrivalDelayMinutes | 224 nulls | Cancelled flights; affects arrival delay |
| DQ-09 | MEDIUM | fact_flight_operations | BlockMinutes | 224 nulls | Cancelled flights; affects block hour calculations |
| DQ-10 | MEDIUM | fact_disruptions | EventEndTimestampUTC | 322 nulls | Open disruption events; affects delay analysis |
| DQ-11 | MEDIUM | fact_disruptions | ReactionaryEvidenceID | 1682 nulls | Reactionary flag cannot be verified |
| DQ-12 | MEDIUM | fact_customer_feedback | SatisfactionScore | 603 nulls | CF02/CF13/CF14 affected |
| DQ-13 | MEDIUM | fact_customer_feedback | ComplaintCategory | 1862 nulls | Complaint analysis incomplete |
| DQ-14 | MEDIUM | fact_customer_feedback | ResolutionDateKey | 1896 nulls | Resolution tracking incomplete |

---

## 6. ETL Process Gaps

| Gap | Severity | Description |
|-----|----------|-------------|
| Power Query M incomplete | HIGH | Only 2 of 14 tables defined in AEROVISION360_DataLoad.m |
| dim_airline column count mismatch | MEDIUM | M code states 14 columns; actual CSV has 12 |
| No error handling in M | MEDIUM | No try/except or error trapping |
| No duplicate prevention | MEDIUM | No logic to prevent duplicate rows |
| No schema validation | LOW | No schema validation in Power Query |
| No data lineage tracking | LOW | No explicit lineage documentation between layers |

---

## 7. Data Quality Governance

| Aspect | Status | Evidence |
|--------|--------|----------|
| Data quality rules | DOCUMENTED | docs/M310_ADVANCED_DATA_QUALITY_GOVERNANCE.md |
| Quality rules implementation | PARTIAL | gen_data_quality.py exists in audit folder |
| Quality test execution | PARTIAL | 40 implementation tests; 0 failures |
| Data quality dashboard | MISSING | No Power BI visual for data quality monitoring |
| Data quality alerting | MISSING | No alerting for data quality issues |
| Data quality SLA | MISSING | No SLA defined for data quality |

---

## 8. Conclusion

The data engineering layer is **partially implemented**. The data contracts define complete schemas, and the build scripts exist for all 14 tables. However:

1. Power Query M only defines 2 of 14 tables
2. dim_airline has 3 entirely null columns
3. Several fact tables have NULL values in key columns
4. No data quality dashboard or alerting
5. No data lineage documentation

**Recommendation:** Complete Power Query M for all 14 tables; document data lineage; add data quality monitoring; resolve OD-04 before generating financial fact tables.
