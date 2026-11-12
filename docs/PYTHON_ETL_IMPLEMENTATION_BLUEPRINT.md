# AEROVISION 360 — Python ETL Implementation Blueprint

**Status:** ENGINEERING PREPARATION — DESIGNED, NOT IMPLEMENTED; NO PRODUCTION CODE
**Version:** 0.1
**Prepared:** 2026-11-02
**Governing contract:** `docs/03_DATA_CONTRACTS.md` version 1.5
**Companion documents:** `SYNTHETIC_DATA_GENERATION_BLUEPRINT.md`, `ENGINEERING_DATA_MODEL_BLUEPRINT.md`
**Project root:** `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`

> **Status notice.** This is a proposed ETL architecture. No Python module, package file, configuration file, script, dataset, or pipeline output has been created. The environment has Python 3.13.2 available, but dependency versions and imports must be re-audited before implementation. G4 is `BLOCKED`; data generation is not authorized.

**Canonical disclosure:** `Synthetic Simulation — Not Actual Airline Performance`

## 1. Purpose and boundary

The Python pipeline is responsible for deterministic synthetic-data generation, reference loading, RAW preservation, STAGING validation, CURATED publication, reconciliation, manifests, and quality evidence. It is not a production airline system and must not use real passenger data.

**Design principles:**

- Fail closed on approval, reference, schema, key, or reconciliation problems.
- RAW is immutable; STAGING is rebuildable; CURATED is clean and publishable.
- Every output traces to a run ID, seed, configuration hash, reference version, and source line.
- No silent correction, no automatic placeholder, no fallback key, no coercion to a valid value.
- The same seed, configuration, reference version, and code version reproduce the same logical output.
- AirlineKey comes only from the approved immutable key map.

## 2. Existing project structure (read-only inspection)

The project structure was inspected read-only. The following directories exist and are empty unless noted:

| Path | Current state | Planned use |
|---|---|---|
| `config/` | Empty | Pipeline YAML, schema registry, environment profiles |
| `data/01_raw/` | Empty | Immutable RAW run outputs |
| `data/02_staging/` | Empty | Typed, validated, quarantined staging outputs |
| `data/03_curated/` | Empty | Star-schema CURATED outputs |
| `data/04_reference/` | Empty | Approved reference CSV files (not authorized) |
| `data/manifests/` | Empty | Run, reference, and dataset manifests |
| `src/generators/` | Empty | Synthetic data generators |
| `src/transformations/` | Empty | Staging/curated transformations |
| `src/utilities/` | Empty | IO, hashing, logging, time zones, IDs |
| `src/validation/` | Empty | Schema, rules, referential, reconciliation, manifests |
| `tests/unit/` | Empty | Unit tests |
| `tests/data_quality/` | Empty | Data-quality tests |
| `tests/reconciliation/` | Empty | Reconciliation tests |
| `scripts/` | Empty | CLI entry points |
| `qa/results/` | Empty | Test evidence |
| `qa/screenshots/` | Empty | Report screenshots (later, blocked) |
| `power_bi/` | Empty | Semantic model/report (not authorized) |
| `reports/audit/` | Empty | Audit summaries |
| `reports/final_case_study/` | Empty | Portfolio case study (later) |

No directory should be populated with production artifacts until the gates in Section 15 are satisfied.

## 3. Runtime and dependency plan

**Detected runtime:** Python 3.13.2 on Windows. The project must pin a supported Python version and record it in the manifest. Do not rely on an unpinned global environment.

**Proposed dependencies (not installed or pinned by this document):**

| Package | Purpose | Pinning rule |
|---|---|---|
| pandas | Tabular transformation and validation | Exact version in lock file |
| numpy | Seeded random generation and numeric operations | Exact version in lock file |
| pyarrow | Parquet schema enforcement and file IO | Exact version in lock file |
| duckdb | Set-based joins, reconciliation, and performance checks | Exact version in lock file |
| PyYAML | Configuration loading | Exact version in lock file |
| pytest | Unit, data-quality, and reconciliation tests | Exact version in lock file |
| ruff | Linting and formatting | Exact version in lock file |

**Rules:** pin exact versions and hashes where the package manager supports it; do not upgrade during a run; record the Python version, package versions, and virtual-environment hash in the generation manifest. `zoneinfo` is part of the standard library. Do not add a package merely to appear advanced.

## 4. Proposed module architecture

### 4.1 Configuration and utilities

| Proposed module | Responsibility | Inputs | Outputs | Dependencies | Error handling and logging | Validation and unit tests |
|---|---|---|---|---|---|---|
| `config/settings.py` | Load and validate YAML configuration; merge safe environment overrides | `config/pipeline.yaml`, env vars | Immutable settings object | PyYAML, dataclasses | Raise configuration error; log resolved non-secret settings | Required keys, types, ranges; unit tests for missing/invalid values |
| `config/schema_registry.py` | Define column order, logical/physical types, nullability for every dataset | Contract schema | Schema objects | pyarrow, contract constants | Fail on unknown dataset or duplicate column | Schema parity tests against contract Section 6 |
| `src/utilities/paths.py` | Resolve project root and run paths; prevent path traversal | Root, run ID, dataset | Safe `Path` objects | pathlib | Reject absolute/unsafe child paths | Unit tests for Windows paths and traversal |
| `src/utilities/io.py` | Atomic CSV/Parquet read/write; UTF-8 no BOM; LF | DataFrame/table, path, schema | File + hash | pandas, pyarrow, hashing | Write temp then atomic replace; never overwrite published run | Round-trip, encoding, hash, schema tests |
| `src/utilities/logging.py` | Structured JSONL logs with run/stage/dataset context | Event fields | Log file and console | stdlib logging | No secrets/PII; errors include exception type | Log-field and redaction tests |
| `src/utilities/hashing.py` | SHA-256 file/content/config/key-map hashes | Bytes/path/object | Hex digest | hashlib | Fail on unreadable file | Known-vector and stable-ordering tests |
| `src/utilities/timezones.py` | IANA validation, UTC/local conversion, DST handling | Timestamps, zone IDs, tz version | UTC timestamps, local dates | zoneinfo | Reject invalid/ambiguous cases without a rule | DST, overnight, cross-zone tests |
| `src/utilities/ids.py` | Deterministic IDs; controlled key map loader | Seed, namespace, approved map | Stable IDs/keys | hashlib, csv | Block on duplicate/missing/reassigned keys | Reorder/rebuild/key-map tests |

### 4.2 Generators

| Proposed module | Responsibility | Inputs | Outputs | Dependencies | Error handling and logging | Validation and unit tests |
|---|---|---|---|---|---|---|
| `src/generators/reference_loader.py` | Load approved reference CSV and manifest read-only | Approved reference directory, selected version | Validated reference frames | io, schema, validation | Fail on missing/unapproved/mixed version | Reference hash, version, key-map tests |
| `src/generators/dimensions.py` | Build DimDate and controlled dimensions | Reference, config | Dimension frames | pandas, ids | Fail on duplicates/missing members | Counts, business keys, date coverage |
| `src/generators/network.py` | Build synthetic airports, routes, fleets, aircraft types | Config, reference airports/types | Network frames | numpy, pandas | Fail on impossible distance/capacity | Route distance, timezone, fleet tests |
| `src/generators/flights.py` | Generate schedule and flight operations | Network, seed, config | FactFlightOperations RAW | numpy, timezones | Fail on capacity/time/status violations | Grain, capacity, flags, date-key tests |
| `src/generators/bookings.py` | Generate demand pools and coupon bookings | Flights, fare/channel/customer refs | FactBookingTransactions RAW | numpy, pandas, currency | Fail if coupon-to-flight control totals differ | Coupon grain, statuses, revenue controls |
| `src/generators/costs.py` | Generate cost ledger and allocations | Flights, cost reference, config | FactOperatingCosts RAW | numpy, pandas | Fail on classification mismatch or control imbalance | Cost identity, classification, allocation tests |
| `src/generators/disruptions.py` | Generate delay/cancellation events | Flights, disruption reference, seed | FactDisruptions RAW | numpy | Fail if delay partition fails | Sequence, attribution, reactionary evidence tests |
| `src/generators/feedback.py` | Generate feedback events | Flights, customers, seed | FactCustomerFeedback RAW | numpy | Fail on invalid flight/customer/date | Type/score/category/resolution tests |
| `src/generators/orchestrator.py` | Execute generation stages in dependency order | Settings, run context | RAW files + manifests | all generators | Stop on first critical failure; write run summary | End-to-end seed and volume tests |

### 4.3 Transformations

| Proposed module | Responsibility | Inputs | Outputs | Dependencies | Error handling and logging | Validation and unit tests |
|---|---|---|---|---|---|---|
| `src/transformations/staging.py` | Standardize names/types/codes, detect duplicates, apply DQ rules, quarantine | RAW, schema, reference | STAGING accepted + quarantine | pandas, pyarrow, duckdb | No silent correction; disposition record required | Rule, quarantine, row-count tests |
| `src/transformations/keys.py` | Resolve dimension/fact keys; load permanent AirlineKey map | Reference, dimensions | Keyed frames | ids, duckdb | Block on orphan/reassigned key | Orphan, uniqueness, key-stability tests |
| `src/transformations/currency.py` | Apply exact-date synthetic rates and populate USD columns | Financial rows, rates | USD columns | pandas | Fail on missing/duplicate/negative rate | Rate-date, rounding, tax-exclusion tests |
| `src/transformations/allocations.py` | Allocate booking-level amounts and cost pools once | Booking/cost controls | Allocated coupon/cost rows | pandas, numpy | Fail if residual cannot be assigned | Residual, tie-break, one-time allocation tests |
| `src/transformations/dates.py` | Derive local date keys and UTC timestamps | Airports, flights, events | Date-key columns | timezones | Fail on invalid zone/date | DST, overnight, boundary tests |
| `src/transformations/curated.py` | Publish final dimensions/facts, enforce schema and grain | STAGING accepted | CURATED files | pyarrow, schema | Fail closed on any critical defect | Schema, grain, count, hash tests |

### 4.4 Validation and evidence

| Proposed module | Responsibility | Inputs | Outputs | Dependencies | Error handling and logging | Validation and unit tests |
|---|---|---|---|---|---|---|
| `src/validation/schema.py` | Compare actual schema to contract | Dataset, schema registry | Pass/fail + detail | pyarrow | Fail on missing/extra/type mismatch | Schema parity tests |
| `src/validation/rules.py` | Evaluate controlled business rules and ranges | STAGING/CURATED | Rule results CSV | pandas/duckdb | No rule may silently pass on error | Rule fixtures and negative tests |
| `src/validation/referential.py` | Anti-join required/optional FKs; fact logical references | Keyed frames | Orphan report | duckdb | Fail on required orphans | Orphan fixtures |
| `src/validation/reconciliation.py` | Passenger, revenue, cost, delay, feedback controls | CURATED, controls | Reconciliation CSV | duckdb | Fail on unexplained difference | Control-total and tolerance tests |
| `src/validation/manifests.py` | Build and verify run/reference/dataset manifests | Files, hashes, config | Manifest CSV/JSON | hashing | Fail on hash/count mismatch | Manifest integrity tests |
| `src/validation/reporting.py` | Produce QA summary and evidence index | Test results | `qa/results/<run_id>/` | pandas | Do not convert BLOCKED to PASS | Evidence completeness tests |
| `scripts/run_pipeline.py` | CLI orchestration: `reference`, `raw`, `staging`, `curated`, `validate`, `all` | CLI args, config | Run outputs | all modules | Non-zero exit on failure; resumable only within a run | CLI smoke tests (not executed) |
| `scripts/validate_run.py` | Re-run validations against an existing published run | Run ID, config | Validation evidence | validation | Read-only; no data mutation | Determinism and immutability tests |

### 4.5 Test modules

| Proposed test area | Scope |
|---|---|
| `tests/unit/` | Pure functions: ID derivation, hashing, time zones, allocation, schema, config, currency |
| `tests/data_quality/` | Rule coverage, DQ-01–DQ-14 injection/detection, quarantine, null/range/domain |
| `tests/reconciliation/` | Flight/coupon/cost/delay/feedback controls, zero denominators, rollups |
| `tests/reproducibility/` | Same seed/config/reference produces same logical output and hashes |
| `tests/contract/` | Schema, grain, key, relationship and reference-version conformance |

Tests are planned, not implemented. No test result may be called PASS without execution evidence and review.

## 5. Execution order and CLI

Proposed CLI (not created):

```text
python -m scripts.run_pipeline --config config/pipeline.yaml --stage all --run-id RUN-YYYYMMDD-HHMMSS --seed <integer>
python -m scripts.run_pipeline --config config/pipeline.yaml --stage raw --run-id <id>
python -m scripts.run_pipeline --config config/pipeline.yaml --stage staging --run-id <id>
python -m scripts.run_pipeline --config config/pipeline.yaml --stage curated --run-id <id>
python -m scripts.validate_run --config config/pipeline.yaml --run-id <id>
```

**Execution order:**

1. Load config; validate Python/package versions and paths.
2. Validate approval marker, selected `ReferenceVersion`, manifest `APPROVED`, key map, and reference hashes.
3. Load reference tables read-only.
4. Build dimensions and network.
5. Generate flights.
6. Generate bookings and reconcile coupon controls to flight controls.
7. Generate costs and reconcile to cost controls.
8. Generate disruptions and reconcile delay attribution.
9. Generate feedback and reconcile to valid flights/customers.
10. Write RAW files and RAW manifests; compute hashes.
11. Run STAGING standardization, validation, quarantine, and dispositions.
12. Run CURATED key resolution, currency, allocation, schema, and grain checks.
13. Run full validation/reconciliation suite.
14. Write QA summary, run manifest, and evidence index.
15. Publish only if all required checks pass; otherwise leave the run in a failed/quarantined state.

**Failure policy:** a critical failure stops publication. A dataset may be quarantined without stopping the run only if the reason is documented and the missing data is not required for a published CURATED table. No partial CURATED publication.

## 6. Run directories, naming, and formats

```text
data/01_raw/<run_id>/raw_<dataset>.csv
data/02_staging/<run_id>/stg_<dataset>.parquet
data/02_staging/<run_id>/quarantine_<dataset>.parquet
data/03_curated/<run_id>/dim_<name>.parquet
data/03_curated/<run_id>/fact_<name>.parquet
data/manifests/<run_id>/run_manifest.json
data/manifests/<run_id>/dataset_manifest.csv
data/manifests/<run_id>/reference_version.json
qa/results/<run_id>/<test_id>.csv
```

- RAW: CSV, UTF-8 without BOM, comma-separated, header row, LF; or Parquet with a documented schema. One format per dataset version.
- STAGING: Parquet with explicit schema.
- CURATED: dimensions in Parquet and facts in Parquet; Power BI imports them through Power Query. CSV is allowed only where a documented compatibility reason exists.
- Reference: CSV, UTF-8 without BOM, LF, controlled by the reference manifest.
- No spaces in filenames; lowercase snake case.
- A published run is immutable. A new run gets a new `run_id`.
- A `latest` pointer may be a manifest field, not a symlink; do not rely on Windows symlink privileges.

## 7. Configuration and secrets

Proposed configuration sections:

```yaml
run:
  seed: 20261102
  timezone_database: "recorded-at-runtime"
paths:
  project_root: "C:/Users/KHfar/OneDrive/Desktop/AEROVISION_360"
reference:
  selected_version: "AIR-YYYY-MM-DD-NNN"
  manifest: "data/manifests/reference_versions.csv"
volumes:
  flight_legs: 150000
  customer_target: 1200000
distributions:
  load_factor: {}
  cancellation: {}
  delay: {}
defect_injection:
  enabled: true
  rates: {}
validation:
  fail_on_critical: true
  evidence_dir: "qa/results"
```

**Environment variables:** `AEROVISION_ROOT`, `AEROVISION_CONFIG`, `AEROVISION_RUN_ID`, `AEROVISION_SEED`, `AEROVISION_LOG_LEVEL`. No secrets, tokens, or credentials are required or permitted. Do not commit generated data or local paths containing personal information.

## 8. Schema enforcement and null handling

- Schema registry is the single source for column order, type, and nullability.
- Read with explicit schema; do not infer types from data.
- Reject unknown columns in CURATED; allow documented staging metadata only in STAGING.
- Preserve nulls; never replace missing numeric values with zero, missing text with `Unknown`, or missing keys with `-1` unless an approved unknown-member rule exists.
- Parse dates/timestamps strictly; reject locale-specific formats. Store UTC timestamps and local date keys.
- Normalize codes to uppercase/trimmed; reject invalid patterns.
- Decimal money uses two decimals; rates six; ratios six. Do not round before final allocation.
- Boolean values in CURATED are true/false; reject `Y`, `N`, `1`, `0`.

## 9. Idempotency, recovery, and lineage

- `run_id` is unique and immutable.
- A run directory is created atomically; partial outputs are written under a temporary suffix and renamed only after validation.
- `--resume` may continue an incomplete run with the same run ID and config hash; it must not overwrite completed datasets or change the seed.
- A completed run is read-only. To regenerate, create a new run ID.
- Every row carries lineage metadata in STAGING (`SourceFile`, `SourceRowNumber`, `IngestedAtUTC`, `SchemaVersion`, `QualityStatus`, `QualityRuleID`, `Disposition`, `DispositionReason`). CURATED may carry a subset of lineage columns, but the run manifest must map every CURATED file to its RAW source and transformations.
- The run manifest records: run ID, seed, config hash, code version/commit (if Git is later authorized), Python/package versions, selected reference version and hash, key-map hash, row counts, output hashes, defect summary, and test result paths.
- No Git operation is authorized by this document.

## 10. Performance and memory plan

- Generate and process in chunks by airline and month; do not hold a 16M-row coupon frame and all intermediates in memory at once.
- Use Parquet column pruning and predicate pushdown; use DuckDB for joins and controls.
- Avoid Python row-by-row loops except for small controlled logic; vectorize with NumPy/pandas.
- Write facts partitioned by `year_month` during generation if needed, then publish a documented CURATED layout. Power Query must read the published layout without duplicate partitions.
- Benchmark representative volumes before full generation. Record runtime, peak memory, and file sizes.
- If the model cannot meet the agreed desktop performance envelope, raise a performance/schema decision; do not silently sample or aggregate the fact grain.

## 11. Logging and observability

- JSONL logs under `qa/results/<run_id>/logs/`.
- Fields: timestamp UTC, level, run ID, stage, dataset, row count, duration, hash, error code, message.
- Never log passenger names, emails, tokens, or full source URLs with credentials.
- A run summary includes counts by disposition (accepted, corrected, quarantined, rejected), test pass/fail/blocked, and output hashes.
- A failure must identify the failing stage, dataset, rule, row count, and source row where available.

## 12. Test plan for the pipeline

| Test level | Scope | Evidence |
|---|---|---|
| Unit | Pure functions and schemas | `qa/results/<run_id>/unit/` |
| Data quality | DQ-01–DQ-14 detection and quarantine | `qa/results/<run_id>/dq/` |
| Referential | Required/optional FKs, logical fact references | `qa/results/<run_id>/referential/` |
| Reconciliation | Passenger, revenue, cost, delay, feedback | `qa/results/<run_id>/reconciliation/` |
| Reproducibility | Same seed/config/reference rerun | `qa/results/<run_id>/reproducibility/` |
| Contract | Schema, grain, keys, reference version | `qa/results/<run_id>/contract/` |

A test is not PASS until executed, evidence exists, expected and actual values are recorded, and a reviewer accepts the result. Document checks do not substitute for data tests.

## 13. Python/ETL acceptance criteria

| ID | Criterion | Evidence |
|---|---|---|
| PE-01 | Code and config are pinned and reproducible | Lock file, run manifest |
| PE-02 | Reference version and key map validated before generation | Validation log |
| PE-03 | RAW is immutable and hash-verified | RAW manifest |
| PE-04 | STAGING detects all injected defects | DQ evidence |
| PE-05 | CURATED has zero critical/high defects and zero orphan required keys | Validation evidence |
| PE-06 | Financial/passenger/cost/delay reconciliations meet approved thresholds | Reconciliation evidence |
| PE-07 | Same seed/config/reference reproduces same logical output | Reproducibility evidence |
| PE-08 | Pipeline fails closed on missing approval/reference/key | Negative test evidence |
| PE-09 | No secrets or real personal data | Repository review |
| PE-10 | G4 authorization exists before any generation | Gate record |

## 14. Implementation sequence after authorization

1. Environment audit and dependency lock.
2. Schema registry and config.
3. IO, hashing, logging, timezone, ID utilities.
4. Reference/manifest/key-map validation.
5. Dimension and network generators.
6. Flight generator and validation.
7. Booking generator and coupon-to-flight controls.
8. Cost generator and cost controls.
9. Disruption generator and delay attribution.
10. Feedback generator.
11. STAGING rules/quarantine.
12. CURATED transformations and reconciliation.
13. Reproducibility and performance tests.
14. G4/G5 evidence.

## 15. Gate dependencies

- **OD-01A/OD-01B:** formal signature and approval dates.
- **Critical OD decisions:** OD-02 to OD-22 as applicable; OD-14 and OD-15 formal records incomplete.
- **G3-RV-01:** reference version approved.
- **Schema freeze:** approved.
- **G4:** written data-generation authorization.
- **G5:** quality/reconciliation gate after execution.

No Python production code, dataset, or pipeline run may start before these dependencies are satisfied.

## 16. Open decisions and unsupported asks

- Reference manifest and key map do not exist; no generation possible.
- Exact bucket/distribution parameters require owner approval or documented synthetic assumptions.
- OD-13 cost/disruption classification codes are not approved.
- OD-14 allocation and OD-20 tolerance remain open; the 0.01 USD and one-minute thresholds are proposed engineering checks, not approved acceptance criteria.
- OD-22 maximum lead time is open; no 365-day cap may be enforced.
- Severity, sentiment, and service category are not contract columns; do not add them without an approved contract change.
- Power BI import performance at 16M coupon rows is unproven; benchmark before full generation.
- No Git operation is authorized; code version evidence must use file hashes until Git is approved.

## 17. Verification checklist for this blueprint

| Check | Status |
|---|---|
| Actual directory structure inspected read-only | VERIFIED |
| Python runtime detected | VERIFIED — 3.13.2 |
| Modules, inputs, outputs, dependencies defined | DOCUMENTED |
| Error, logging, validation, unit-test expectations defined | DOCUMENTED |
| Determinism, idempotency, recovery, lineage defined | DOCUMENTED |
| Schema/null/currency/time-zone rules defined | DOCUMENTED |
| No production code or dataset created | VERIFIED BY ABSENCE |
| G4 / schema freeze | BLOCKED / NOT AUTHORIZED |

**End of blueprint.** This document is design evidence only. It does not authorize code, data, a pipeline run, or a gate advance.
