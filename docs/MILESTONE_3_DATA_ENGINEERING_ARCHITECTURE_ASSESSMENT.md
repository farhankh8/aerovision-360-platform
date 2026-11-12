# AEROVISION 360 — Milestone 3 Data Engineering Architecture Assessment

**Document type:** Architecture assessment — data engineering pipeline design  
**Milestone:** 3 — Data Engineering Architecture  
**Task:** 01 — Independent assessment (read-only)  
**Project root:** `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`  
**Prepared:** 2026-11-04  
**Governing baseline:** `docs/03_DATA_CONTRACTS.md` version 1.5  
**Status:** DRAFT — for review  

---

## STATUS NOTICE — READ-ONLY ASSESSMENT

This document is an architectural assessment only. It describes the current state, identifies gaps, and proposes a target architecture. No files have been modified, moved, or created as part of this assessment except this document itself.

---

## 1. Executive Summary

AEROVISION 360 has successfully built a curated-dimension foundation (11 dimensions) and three verified fact tables (FactFlightOperations, FactDisruptions, FactCustomerFeedback). Each dataset is built by standalone Python scripts with embedded validation, CSV+Parquet outputs, and SHA-256 manifests. However, these scripts operate independently with hardcoded paths, duplicated inline logic, no shared orchestration, and no RAW/STAGING layer. The project lacks a coherent data-engineering pipeline that connects these components with dependency sequencing, failure recovery, data quality gates, and full data lineage.

This assessment identifies what exists, what is missing, what can be reused, and the safest implementation sequence to transform the individual builders into a production-grade pipeline.

---

## 2. Current-State Architecture

### 2.1 Repository Structure (Verified)

```
AEROVISION_360/
├── .git/                          (initialized, 0 commits, unborn HEAD on main)
├── .venv/                         (15 packages; openpyxl 3.1.5 installed)
├── .gitignore
├── README.md
├── config/
│   ├── __init__.py
│   └── settings.py                (load_settings JSON/YAML, require_settings)
├── data/
│   ├── 03_curated/                (11 dimensions + 3 facts as CSV/Parquet)
│   ├── 04_reference/              (airline workbook, crosswalk, route keymap)
│   └── manifests/                 (14 manifest JSON files)
├── docs/                          (contracts, blueprints, decisions, governance)
├── power_bi/                      (empty directory)
├── qa/
│   ├── results/                   (empty)
│   └── screenshots/               (empty)
├── reports/                       (audit reports, deployment packages, backups)
├── scripts/                       (ALL active Python implementation)
│   ├── build_*_curated.py         (dimension + fact builders)
│   ├── build_dim_airline.py       (workbook DimAirline sheet builder)
│   ├── build_airline_reference_workbook.py
│   ├── verify_and_populate_airline_reference.py
│   ├── validate_airline_reference.py
│   ├── add_iata_numeric_codes.py
│   ├── audit_dimensions.py        (comprehensive audit script)
│   ├── promote_network_expansion_release_v2.py
│   └── backups/                   (8 timestamped backup directories)
├── src/
│   ├── __init__.py
│   └── utilities/
│       ├── __init__.py
│       ├── hashing.py             (sha256_bytes, sha256_stream, sha256_file)
│       ├── io.py                  (read_json, write_json_atomic)
│       ├── logging.py             (get_logger)
│       └── paths.py               (project_root, project_path)
└── tests/
    ├── data_quality/              (empty)
    ├── reconciliation/            (empty)
    └── unit/
        ├── test_dim_airline_curated.py
        ├── test_fact_customer_feedback.py
        ├── test_fact_disruptions.py
        ├── test_fact_flight_operations.py
        ├── test_hashing.py
        ├── test_io.py
        ├── test_logging.py
        ├── test_paths.py
        └── test_settings.py       (130 tests passing)
```

### 2.2 What Exists (Verified)

| Component | Status | Evidence |
|-----------|--------|----------|
| 11 curated dimensions | Complete | CSV + Parquet + manifest for each |
| FactFlightOperations | Verified | 5,000 rows, 25 columns, 35 tests |
| FactDisruptions | Verified | 1,754 rows, 16 columns, 31 tests |
| FactCustomerFeedback | Verified | 2,500 rows, 14 columns, 35 tests |
| Shared utilities | Complete | hashing, io, logging, paths (4 modules) |
| Configuration loader | Complete | config/settings.py (JSON/YAML) |
| Unit tests | Complete | 130 tests passing across 7 files |
| Airline reference tooling | Complete | workbook builder, populator, validator, crosswalk |
| Audit script | Complete | audit_dimensions.py (~359 lines) |
| Deployment/promotion script | Complete | promote_network_expansion_release_v2.py |
| Git repository | Initialized | main branch, 0 commits, remote origin configured |

### 2.3 What Is Missing

| Component | Status | Impact |
|-----------|--------|--------|
| RAW layer (`data/01_raw/`) | Missing | No immutable source preservation |
| STAGING layer (`data/02_staging/`) | Missing | No type normalization, cleansing, or quarantine |
| Pipeline orchestrator | Missing | No dependency sequencing or failure recovery |
| Pipeline entry point | Missing | No CLI or `python -m` execution |
| Pipeline run ID / versioning | Missing | No run tracking or dataset versioning |
| Data quality gates | Partial | Builders self-validate; no pipeline-level gates |
| Rejected-record handling | Missing | No quarantine mechanism for invalid records |
| Incremental refresh | Missing | All builders are full-rebuild only |
| Pipeline-level tests | Missing | Unit tests exist; pipeline integration tests do not |
| Data lineage tracking | Partial | Manifests exist per dataset; no cross-dataset lineage |

---

## 3. Layer Responsibilities (Target State)

### 3.1 RAW Layer — `data/01_raw/`

**Purpose:** Immutable preservation of original source records exactly as generated or received.

| Responsibility | Detail |
|---------------|--------|
| Original source preservation | Store raw generated records before any transformation |
| Immutable input snapshots | Files are write-once; never modified or cleaned in place |
| Source metadata | Ingestion timestamp, source filename, generator version, seed |
| File-level checksums | SHA-256 for every RAW file |
| Provenance | Trace every CURATED row back to its RAW source |

**Constraint:** RAW is never overwritten, cleaned in place, or silently corrected (per Section 3 of `03_DATA_CONTRACTS.md`).

**Current state:** Missing. `data/01_raw/` does not exist.

### 3.2 STAGING Layer — `data/02_staging/`

**Purpose:** Standardize, type, deduplicate, flag, validate, and quarantine records before CURATED publication.

| Responsibility | Detail |
|---------------|--------|
| Type normalization | Convert raw types to contract types |
| Schema validation | Verify column order, types, nullability per Section 6 |
| Data cleansing | Standardize codes, trim text, fix casing |
| Rejected-record handling | Quarantine invalid records with reason codes |
| Intermediate validation | Foreign-key resolution, business-rule checks |
| Currency conversion | Apply approved exchange rates (blocked by OD-04) |
| Defect detection | Detect controlled defects per Section 12 catalogue |

**Constraint:** Staging must be rebuildable from RAW and REFERENCE without manual edits. Preserve defect flags, rejection reasons, and source lineage.

**Current state:** Missing. `data/02_staging/` does not exist.

### 3.3 CURATED Layer — `data/03_curated/`

**Purpose:** Publish clean star-schema tables and USD measures. Power BI consumes CURATED only.

| Responsibility | Detail |
|---------------|--------|
| Existing dimensions | 11 dimensions already curated |
| Existing facts | 3 facts already curated |
| Contract enforcement | All required columns present; types match |
| Referential integrity | All FKs resolve; zero orphans |
| Final manifests | SHA-256 hashes, row counts, validation checklists |
| Power BI boundary | Power BI imports CURATED and approved REFERENCE only |

**Current state:** Partially complete. 11 dimensions + 3 facts curated. Facts blocked by OD-04: FactBookingTransactions, FactOperatingCosts.

---

## 4. Data Flow Diagram

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   RAW LAYER     │      │  STAGING LAYER  │      │  CURATED LAYER  │
│  data/01_raw/   │─────▶│ data/02_staging/│─────▶│ data/03_curated/│
│                 │      │                 │      │                 │
│ • Immutable     │      │ • Type norm.    │      │ • Dimensions    │
│ • Source hashes │      │ • Schema val.   │      │ • Facts         │
│ • Ingestion meta│      │ • Cleansing     │      │ • Manifests     │
│ • Provenance    │      │ • Quarantine    │      │ • Power BI      │
└─────────────────┘      └─────────────────┘      └─────────────────┘
       ▲                      ▲                      ▲
       │                      │                      │
       │              REFERENCE LAYER               │
       │              data/04_reference/            │
       │ • Code lists    │      │ • Calendar      │
       │ • Exchange rates│      │ • Route keymap  │
       └─────────────────┘      └─────────────────┘
```

**Data flow rules (per Section 3 of contract):**
1. Data moves in one direction: RAW → STAGING → CURATED
2. REFERENCE data is available to STAGING and CURATED
3. Power BI consumes CURATED and approved REFERENCE only
4. RAW is never cleaned in place; corrections are written to STAGING or CURATED with disposition records

---

## 5. Component Responsibilities

### 5.1 Existing Components (Reusable — Do Not Rebuild)

| Component | Path | Responsibility | Reusability |
|-----------|------|---------------|-------------|
| `src/utilities/hashings.py` | Hashing utilities | SHA-256 bytes/stream/file | HIGH — use for all layer checksums |
| `src/utilities/io.py` | JSON I/O | Atomic JSON write, read | HIGH — use for manifests and settings |
| `src/utilities/logging.py` | Centralized logging | get_logger with dedup handlers | HIGH — pipeline logger |
| `src/utilities/paths.py` | Path resolution | project_root, project_path | HIGH — all layer paths |
| `config/settings.py` | Configuration | load_settings (JSON/YAML), require_settings | HIGH — pipeline configuration |
| `scripts/audit_dimensions.py` | Dimension audit | ~100 checks across 10 dimensions | MEDIUM — extend for pipeline QA |
| `scripts/build_dim_*_curated.py` | Dimension builders | 10 dimension builders | MEDIUM — adapt to STAGING→CURATED pattern |
| `scripts/build_fact_*_operations.py` | Fact builders | 3 fact builders | MEDIUM — adapt to STAGING→CURATED pattern |
| `tests/unit/` (7 files, 130 tests) | Unit tests | Utility + dimension + fact tests | HIGH — extend with pipeline tests |

### 5.2 New Components Needed

| Component | Path | Responsibility | Priority |
|-----------|------|---------------|----------|
| Pipeline orchestrator | `src/orchestration/pipeline.py` | Dependency sequencing, run ID, failure recovery | HIGH |
| Pipeline CLI entry | `scripts/run_pipeline.py` or `src/orchestration/__main__.py` | Execution entry point | HIGH |
| RAW layer builder | `scripts/build_raw_layer.py` | Immutable source snapshot generation | HIGH |
| STAGING layer builder | `scripts/build_staging_layer.py` | Type norm, validation, quarantine | HIGH |
| Pipeline settings | `config/pipeline_settings.json` or `.yaml` | Pipeline configuration | MEDIUM |
| Pipeline tests | `tests/unit/test_pipeline_orchestrator.py` | Orchestrator unit tests | MEDIUM |
| Pipeline integration tests | `tests/integration/test_pipeline_end_to_end.py` | End-to-end validation | MEDIUM |
| Data quality gate module | `src/validation/quality_gates.py` | Pipeline-level QA gates | MEDIUM |
| Lineage tracker | `src/lineage/lineage_tracker.py` | Cross-dataset lineage recording | LOW (post-M3) |

### 5.3 Components to Leave Unchanged

| Component | Reason |
|-----------|--------|
| All 11 dimension builders | Verified complete; do not rebuild |
| All 3 fact builders | Verified complete; do not rebuild |
| `src/utilities/*` | Working and tested; reuse as-is |
| `config/settings.py` | Working; reuse for pipeline config |
| All 130 unit tests | Passing; extend, don't modify |
| Existing manifests | Accurate; reuse pattern for new manifests |

---

## 6. Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                     PIPELINE DEPENDENCY GRAPH                   │
└─────────────────────────────────────────────────────────────────┘

  REFERENCE (data/04_reference/)
  ├── airline workbook (DimAirline source)
  ├── route key map (DimRoute source)
  ├── airline crosswalk (governance)
  └── exchange rates (BLOCKED by OD-04)

  RAW LAYER (data/01_raw/)
  ├── dim_airline_raw
  ├── dim_route_raw
  ├── dim_aircraft_raw
  ├── dim_date_raw
  ├── fact_flight_operations_raw
  └── ... (all dimension/fact raw snapshots)

  STAGING LAYER (data/02_staging/)
  ├── dim_airline_stg  ◀── dim_airline_raw + reference
  ├── dim_route_stg    ◀── dim_route_raw + route keymap + reference
  ├── dim_aircraft_stg ◀── dim_aircraft_raw + airline + type + reference
  ├── dim_customer_stg ◀── dim_customer_raw + reference
  ├── dim_date_stg     ◀── dim_date_raw
  ├── dim_airport_stg  ◀── dim_airport_raw + reference
  ├── dim_booking_channel_stg
  ├── dim_currency_stg
  ├── dim_disruption_type_stg
  ├── dim_fare_class_stg
  ├── fact_flight_operations_stg ◀── raw + dim_airline + dim_route + dim_aircraft + dim_date
  ├── fact_booking_transactions_stg ◀── BLOCKED by OD-04 (exchange rates)
  ├── fact_operating_costs_stg     ◀── BLOCKED by OD-04 (exchange rates)
  ├── fact_disruptions_stg ◀── fact_flight_operations + dim_airline + dim_route + dim_airport + dim_disruption_type + dim_date
  └── fact_customer_feedback_stg ◀── fact_flight_operations + dim_customer + dim_airline + dim_route + dim_date

  CURATED LAYER (data/03_curated/)
  ├── All dimensions (existing)
  ├── FactFlightOperations (existing)
  ├── FactDisruptions (existing)
  ├── FactCustomerFeedback (existing)
  ├── FactBookingTransactions (BLOCKED by OD-04)
  └── FactOperatingCosts (BLOCKED by OD-04)

  PIPELINE ORCHESTRATOR
  ├── Sequences builds in dependency order
  ├── Emits run ID and manifests
  ├── Enforces data quality gates
  └── Handles failure recovery
```

**Critical dependency chain:**
1. Reference data → Dimension RAW → Dimension STAGING → Dimension CURATED
2. Dimension CURATED → Fact RAW → Fact STAGING → Fact CURATED
3. FactFlightOperations is the root fact — all other facts logically reference it
4. FactBookingTransactions and FactOperatingCosts are BLOCKED by OD-04 (exchange rates)

---

## 7. Implementation Sequence

The safest implementation sequence preserves all existing verified work and introduces new infrastructure incrementally:

| Phase | Task | Dependencies | Blocked By |
|-------|------|--------------|------------|
| 3.1 | Create `src/orchestration/pipeline.py` with run ID, dependency sequencing, failure recovery | src/utilities/* (existing) | None |
| 3.2 | Create pipeline CLI entry point | src/orchestration/ | 3.1 |
| 3.3 | Create RAW layer builder (immutable source snapshots) | src/utilities/paths, hashing, io | None |
| 3.4 | Create STAGING layer builder (type norm, validation, quarantine) | src/utilities/*, config/settings | 3.3 |
| 3.5 | Add pipeline-level unit tests | Existing test infrastructure | 3.1–3.4 |
| 3.6 | Add pipeline integration tests (end-to-end) | 3.5 | 3.5 |
| 3.7 | Add data quality gate module | Existing audit_dimensions.py patterns | 3.4 |
| 3.8 | Resolve OD-04 (owner approval) | Owner decision | External |
| 3.9 | Create `ref_exchange_rates.csv` (after OD-04 approval) | OD-04 approval | 3.8 |
| 3.10 | Implement FactBookingTransactions | OD-04 + exchange rates | 3.9 |
| 3.11 | Implement FactOperatingCosts | OD-04 + exchange rates | 3.9 |

**Critical path:** OD-04 owner approval → exchange rate reference → FactBookingTransactions + FactOperatingCosts. Nothing else is blocked.

---

## 8. Risks and Trade-offs

| Risk | Severity | Mitigation |
|------|----------|------------|
| **OD-04 not approved** | High | FactBookingTransactions and FactOperatingCosts cannot proceed. Document clearly; proceed with RAW/STAGING/orchestrator for unblocked facts. |
| **Currency set mismatch** | High | OD-04 lists 5 currencies; DimCurrency has 8. Must be resolved by owner before exchange rate reference creation. |
| **Duplicate builder versions** | Medium | Multiple candidate versions exist in scripts/ (e.g., build_dim_airport.py, _production_candidate.py, _expanded_candidate.py). Do not delete; document which is authoritative. |
| **Duplicate backup files** | Medium | .bak files and timestamped backups exist in scripts/ and data/. Document as historical; exclude from pipeline. |
| **openpyxl dependency** | Medium | 7 scripts import openpyxl. Confirmed installed (3.1.5). Document in pipeline requirements. |
| **No pipeline-level tests** | Medium | Unit tests exist; pipeline integration tests must be added before production use. |
| **Full-rebuild only** | Low | All builders are full-rebuild with FileExistsError protection. Incremental refresh is future work. |
| **Git repo has 0 commits** | Low | All work is untracked. Recommend initial commit after M3 architecture is approved. |

---

## 9. Testing Strategy

### 9.1 Existing Tests (130 passing)
| File | Tests | Coverage |
|------|-------|----------|
| test_hashing.py | 3 | SHA-256 utilities |
| test_io.py | 3 | JSON atomic write/read |
| test_logging.py | 3 | Logger configuration |
| test_paths.py | 3 | Path resolution |
| test_settings.py | 6 | Configuration loading |
| test_dim_airline_curated.py | 14 | Dimension schema, keys, manifest |
| test_fact_flight_operations.py | 35 | Fact schema, keys, FKs, cancelled rules |
| test_fact_disruptions.py | 31 | Fact schema, keys, FKs, event sequences, reactionary |
| test_fact_customer_feedback.py | 35 | Fact schema, keys, FKs, scores, complaint rules |

### 9.2 New Tests Required

| Test File | Purpose | Priority |
|-----------|---------|----------|
| `tests/unit/test_pipeline_orchestrator.py` | Orchestrator sequencing, run ID, failure recovery | HIGH |
| `tests/unit/test_raw_layer.py` | RAW snapshot immutability, checksums | HIGH |
| `tests/unit/test_staging_layer.py` | Type normalization, quarantine, FK resolution | HIGH |
| `tests/unit/test_quality_gates.py` | Pipeline-level QA gates | MEDIUM |
| `tests/integration/test_pipeline_end_to_end.py` | Full RAW→STAGING→CURATED flow | HIGH |
| `tests/unit/test_lineage.py` | Cross-dataset lineage tracking | LOW |

### 9.3 Test Standards
- All tests use pytest
- Small deterministic fixtures (no production data generation)
- No test may modify existing datasets
- Windows teardown PermissionError is a pre-existing environment issue, not a test failure

---

## 10. Acceptance Criteria

Milestone 3 is complete when:

1. **RAW layer builder exists** — produces immutable source snapshots with SHA-256 checksums and ingestion metadata
2. **STAGING layer builder exists** — performs type normalization, schema validation, cleansing, and rejected-record quarantine
3. **Pipeline orchestrator exists** — sequences builders in dependency order, emits run ID, handles failure recovery
4. **Pipeline CLI entry point exists** — can execute the full pipeline via command line
5. **Pipeline-level unit tests exist and pass** — orchestrator, RAW, STAGING, quality gates
6. **Pipeline integration tests exist and pass** — end-to-end RAW→STAGING→CURATED flow
7. **All 130 existing tests continue to pass** — no regression
8. **No existing verified dataset is modified** — dimensions and facts unchanged
9. **OD-04 remains unapproved** — no exchange rate reference created without owner approval
10. **Documentation is current** — this assessment reflects actual repository state

---

## 11. Reusable Components Summary

| Component | Path | Lines | Reusable For |
|-----------|------|-------|--------------|
| hashing.py | src/utilities/hashings.py | 700 | All layer checksums, manifest integrity |
| io.py | src/utilities/io.py | 1,578 | Manifest writing, settings loading |
| logging.py | src/utilities/logging.py | 1,425 | Pipeline logger with deduplication |
| paths.py | src/utilities/paths.py | 686 | All layer path resolution |
| settings.py | config/settings.py | 1,771 | Pipeline configuration (JSON/YAML) |
| audit_dimensions.py | scripts/audit_dimensions.py | ~35930 | Pattern for pipeline QA checks |
| test_*.py (7 files) | tests/unit/ | ~24,000 | Test patterns for new pipeline tests |

---

## 12. Conclusion

AEROVISION 360 has a solid curated-dimension foundation with three verified fact tables. The missing infrastructure for Milestone 3 is:

1. **RAW layer** — immutable source preservation
2. **STAGING layer** — type normalization, validation, quarantine
3. **Pipeline orchestrator** — dependency sequencing, run ID, failure recovery
4. **Pipeline CLI** — execution entry point
5. **Pipeline tests** — orchestrator, RAW, STAGING, integration

The existing shared utilities (hashing, io, logging, paths), configuration loader, and 130 passing tests provide a strong foundation. The safest implementation sequence introduces RAW and STAGING builders first, then the orchestrator, then pipeline tests — all without modifying any existing verified component.

OD-04 remains the sole external blocker for FactBookingTransactions and FactOperatingCosts. The RAW/STAGING/orchestrator work can proceed independently of OD-04 resolution.

---

**End of assessment.** No files were modified except this document.