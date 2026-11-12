# AEROVISION 360 — STAGING LAYER IMPLEMENTATION

**Milestone:** 3 — Data Engineering Architecture  
**Task:** M3.5 — STAGING Data Layer  
**Status:** Complete  
**Date:** 2026-11-04  

---

## 1. Overview

The STAGING layer (`data/02_staging/`) standardizes, validates, and quenches RAW source snapshots before they are published to the CURATED layer. It is the critical intermediary between immutable RAW snapshots and the curated star-schema tables consumed by Power BI.

**Core design principle:** *Invalid records are never silently discarded. Every record is either accepted with explicit metadata or rejected with a specific reason code and its original values preserved.*

---

## 2. Folder Structure

```
data/02_staging/
├── runs/
│   └── <staging_run_id>/
│       ├── run_manifest.json              # Run-level provenance metadata
│       ├── sources/
│       │   ├── <source_id>/
│       │   │   ├── accepted/
│       │   │   │   ├── <original_filename>       # Accepted records (CSV + Parquet)
│       │   │   │   └── <original_filename>.quarantine (if --strict)
│       │   │   │       └── quarantine_<original_filename>  # Rejected records
│       │   │   │           └── <original_filename>
│       │   │   ├── metadata.json             # Per-source staging metadata
│       │   │   └── ...
│       │   └── ...
│       └── ...
└── ...
```

| Path | Purpose |
|------|---------|
| `data/02_staging/runs/<run_id>/` | Isolation directory for a single staging run |
| `data/02_staging/runs/<run_id>/run_manifest.json` | Run manifest with source counts, output hashes, and RAW lineage |
| `data/02_staging/runs/<run_id>/sources/<source_id>/accepted/<filename>` | Accepted/staged records, written as CSV + Parquet |
| `data/02_staging/runs/<run_id>/sources/<source_id>/rejected/<filename>` | Rejected/quarantined records with disposition reasons |
| `data/02_staging/runs/<run_id>/sources/<source_id>/metadata.json` | Per-source transformation metadata (schema, counts, timestamps) |

---

## 3. Source Scope

The STAGING layer processes exactly four sources, registered in the RAW layer:

| Source ID | Format | Sheets/Records | Description |
|-----------|--------|----------------|-------------|
| `airline_reference_workbook` | XLSX | `DimAirline` sheet (10 rows) | Ten-airline reference workbook; only the `DimAirline` sheet is staged |
| `airline_id_crosswalk` | CSV | 10 rows | Maps source airline IDs to semantic `DimAirline` IDs |
| `dim_route_keymap_v1` | CSV | 320 rows | Versioned route key-to-route-code registry (immutable) |
| `dim_route_keymap_v1_manifest` | JSON | 1 record | Manifest for the route keymap V1 registry |

**Do not invent missing source fields or alter identifiers.** The staging schema matches the RAW source exactly, with type normalization and validation added.

---

## 4. Core Functionality

### 4.1 RAW Manifest Discovery

The `StagingProcessor.discover_sources()` method reads the RAW source index (`data/01_raw/source_index.json`) and the latest completed run manifest (`data/01_raw/runs/<run_id>/run_manifest.json`) to identify which sources have been ingested and are ready for staging. Only the four registered source IDs are returned.

### 4.2 Source Snapshot Integrity Verification

Before any staging output is written, every RAW snapshot is verified against its SHA-256 checksum recorded in the run manifest. If a mismatch is detected, the staging run fails with a descriptive error and no output is written.

### 4.3 Allowlisted Source Processing

Only sources with a registered `SourceStagingPlan` are processed. Sources without a plan cause a `StagingError`. The staging plans for the four sources are defined in `src/staging/staging_processor.py:STAGING_PLANS` and specify:

- Column names and order
- Required columns
- Primary key and unique keys
- Type conversion rules
- Allowed value sets

### 4.4 CSV, JSON and XLSX Handling

| Format | Reader | Notes |
|--------|--------|-------|
| CSV | `_read_csv_records()` | Uses `csv.reader` with `utf-8-sig` encoding for BOM handling |
| JSON | `_read_json_records()` | Supports single dict or list of dicts; wraps scalar values in `{"value": ...}` |
| XLSX | `_read_xlsx_records()` | Uses `openpyxl` in `read_only=True, data_only=True` mode; reads named sheets |

All three formats are supported by actual project dependencies (`openpyxl` 3.1.5, `csv`, `json`).

### 4.5 Schema Normalization

Each source has a `SourceStagingPlan` that defines the target schema. Type conversion is applied per-column via `_convert_type()`, which handles:

- `int`: String-to-int conversion, integer floats truncated
- `number`: String-to-float conversion
- `boolean`: Case-insensitive True/False/Yes/No recognition
- `string`: Trimmed text (empty string → `None` for nullability)
- `datetime`/`date`: ISO format output

### 4.6 Explicit Type Conversion

Type conversion is **explicit** and **deterministic**. The `_convert_type()` function is the single source for all type conversion logic. If a value cannot be converted (e.g., `"not_an_int"` → `int`), the record is rejected with `quality_rule_id="STG_TYPE"` and `disposition_reason="type_conversion_failed:<column>"`.

### 4.7 Nullability Validation

Required-field validation checks that all `required_columns` have non-None, non-empty values. Failure results in `quality_rule_id="STG_REQUIRED"` and `disposition_reason="missing_required_field:<column>"`.

### 4.8 Required-Field Validation

The `required_columns` tuple for each source specifies which fields must be present. The validation runs after type conversion, so a column that fails type conversion is already rejected before the required-field check.

### 4.9 Duplicate-Record Detection

Duplicate detection uses a deterministic key signature based on the plan's `primary_key` (or `unique_keys` if no primary key). If a signature is seen again, the record is assigned `quality_status=QualityStatus.DUPLICATE` with `disposition=Disposition.REJECTED` and `quality_rule_id="STG_DUPLICATE"`.

**Duplicate records are rejected, not silently overwritten.** The original values and row number are preserved in the rejection output.

### 4.10 Rejected-Record Output

Rejected records are written to a separate `rejected/` directory with their original values and explicit rejection reasons. The rejection output includes:

- All original field values (after type conversion where applicable)
- `QualityStatus` (rejected/duplicate)
- `QualityRuleID` (STG_TYPE, STG_REQUIRED, STG_ALLOWED, STG_DUPLICATE)
- `DispositionReason` (type_conversion_failed, missing_required_field, invalid_allowed_value, duplicate_key)
- `SourceFile`, `SourceRowNumber`, `SourceID`, `SourceSHA256`
- `RAWRunID`, `RawSnapshotPath`, `TransformationVersion`, `SchemaVersion`

### 4.11 Transformation Metadata

Per-source `metadata.json` records the following transformation metadata:

| Field | Description |
|-------|-------------|
| `source_id` | Source identifier |
| `source_name` | Human-readable source name |
| `source_format` | File format (csv, json, xlsx) |
| `source_path` | Original source path |
| `source_sha256` | SHA-256 of the RAW snapshot |
| `raw_run_id` | Ingestion run ID |
| `raw_snapshot_path` | Path to the RAW snapshot |
| `transformation_version` | Staging transformation version (default: "1.0.0") |
| `schema_version` | Schema version (default: "1.0.0") |
| `dataset_name` | Target dataset name |
| `staging_schema` | Full staging plan (columns, types, keys, allowed values) |
| `processed_record_count` | Total records processed (accepted + rejected) |
| `accepted_count` | Records accepted |
| `rejected_count` | Records rejected |
| `duplicate_count` | Records flagged as duplicates |
| `dispositions` | Breakdown: accepted, rejected, duplicates |
| `output_path` | Path to accepted output file |
| `output_sha256` | SHA-256 of the accepted output file |

### 4.12 Source-to-Staging Lineage

Every staged record carries full lineage tracing back to the RAW source:

| Field | Value |
|-------|-------|
| `SourceID` | Source source_id (e.g., "airline_reference_workbook") |
| `SourceSHA256` | SHA-256 of the RAW snapshot file |
| `RAWRunID` | Ingestion run ID (e.g., "20261104_120000_000000") |
| `RawSnapshotPath` | Relative path to the RAW snapshot within `data/01_raw/` |
| `TransformationVersion` | Staging transformation version |
| `SchemaVersion` | Staging schema version |
| `SourceRowNumber` | 1-based row number in the original source |
| `SourceFile` | Original source filename |

### 4.13 Deterministic Transformations

Staging transformations are **deterministic**: given the same RAW snapshot and staging plan, the accepted output is always identical. This is verified by the test `test_staging_output_is_deterministic()`, which runs the same source through two different runs and compares the field-by-field results.

Determinism is achieved by:
- Fixed type conversion rules (`_convert_type()`)
- Deterministic duplicate detection (key signature based on primary key)
- Stable sorting/ ordering is not required (records maintain source order)

### 4.14 Atomic Manifest Writing

All manifest files (`run_manifest.json`, `metadata.json`) are written using `src.utilities.io.write_json_atomic()`, which writes to a temporary file and then renames it. This ensures that manifest files are never in a partially-written state.

### 4.15 No-Overwrite Protection

Staging refuses to overwrite existing output directories. If a staging run ID already exists under `data/02_staging/runs/`, a `FileExistsError` is raised. This prevents accidental data loss from re-running with the same run ID.

---

## 5. Transformation Details per Source

### 5.1 Airline Reference Workbook (`airline_reference_workbook`)

- **Sheet:** `DimAirline`
- **Columns (13):** AirlineKey, AirlineId, AirlineIATACode, AirlineICAOCode, AirlineName, AirlineGroup, HomeCountry, HomeCountryCode, BusinessModelClass, IsActive, StatusEffectiveDate, ReferenceVersion, Notes
- **Required:** AirlineKey, AirlineId, AirlineName
- **Primary key:** AirlineKey
- **Unique keys:** AirlineId
- **Type rules:**
  - AirlineKey → int
  - All string columns → string
  - IsActive → boolean
  - ReferenceVersion → string
  - Notes → string (may be None)
- **Accepted count:** 10 (all 10 airlines)
- **Rejected count:** 0 (all records valid)
- **Notable:** The `Notes` column contains text like "Identity attributes require source verification before reference release." — these records are accepted as-is; verification is a governance concern, not a staging failure.

### 5.2 Airline ID Crosswalk (`airline_id_crosswalk`)

- **Columns (7):** AirlineName, SourceAirlineId, DimAirlineId, SourceAirlineKey, DimAirlineKey, AirlineIdMatches, MappingStatus
- **Required:** SourceAirlineId, DimAirlineId, SourceAirlineKey, DimAirlineKey, MappingStatus
- **Primary key:** DimAirlineKey
- **Unique keys:** SourceAirlineId
- **Type rules:**
  - AirlineName → string (may be None for nullable rows)
  - SourceAirlineId → string
  - DimAirlineId → string
  - SourceAirlineKey → string
  - DimAirlineKey → int
  - AirlineIdMatches → boolean
  - MappingStatus → string
- **Allowed values for MappingStatus:** `PROVISIONAL_REQUIRES_OWNER_REVIEW`
- **Accepted count:** Varies by data quality (2 out of 2 in test fixtures; 10 out of 10 from REAL workbook)
- **Rejected cases:**
  - `AirlineName` = `None` → rejected as missing required field (nullable case in tests)
  - Invalid `DimAirlineKey` type → rejected as type conversion failure

### 5.3 Route Keymap V1 CSV (`dim_route_keymap_v1`)

- **Columns (2):** RouteKey, RouteCode
- **Required:** RouteKey, RouteCode
- **Primary key:** RouteCode
- **Unique keys:** RouteKey
- **Type rules:**
  - RouteKey → int
  - RouteCode → string
- **Duplicate detection:** Based on `RouteCode` (primary key). Duplicate RouteCode values are flagged and rejected.
- **Accepted count:** 319 out of 320 (one duplicate RouteCode in test fixture; all 320 valid from REAL workbook)
- **Rejected count:** 1 (duplicate) or 0 (from REAL workbook with no duplicate RouteCodes)

### 5.4 Route Keymap V1 Manifest JSON (`dim_route_keymap_v1_manifest`)

- **Columns (10):** dataset, version, status, row_count, primary_key, unique_surrogate_key, key_range_min, key_range_max, allocation_policy, (allowed_values for status)
- **Required:** dataset, version, row_count, primary_key
- **Primary key:** None (single manifest record)
- **Unique keys:** ("dataset",)
- **Allowed values for `status`:** `IMMUTABLE_VERSIONED_REFERENCE`
- **Type rules:**
  - dataset → string
  - version → string
  - status → string (must be "IMMUTABLE_VERSIONED_REFERENCE")
  - row_count → int
  - primary_key → string
  - unique_surrogate_key → string
  - key_range_min → int
  - key_range_max → int
  - allocation_policy → string
- **Accepted count:** 1 (single manifest record)
- **Rejected cases:** Invalid `status` value (e.g., "NOT_A_VALID_STATUS")

---

## 6. Validation Rules Summary

| Rule ID | Rule Name | When Triggered | Result |
|---------|-----------|----------------|--------|
| STG_TYPE | Type conversion failure | A value cannot be converted to the declared staging type | `quality_status=REJECTED`, `disposition=REJECTED`, `quality_rule_id=STG_TYPE`, `disposition_reason="type_conversion_failed:<column>"` |
| STG_REQUIRED | Missing required field | A required column has None or empty value after type conversion | `quality_status=REJECTED`, `disposition=REJECTED`, `quality_rule_id=STG_REQUIRED`, `disposition_reason="missing_required_field:<column>"` |
| STG_ALLOWED | Invalid allowed value | A column with `allowed_values` has a value not in the permitted set | `quality_status=REJECTED`, `disposition=REJECTED`, `quality_rule_id=STG_ALLOWED`, `disposition_reason="invalid_allowed_value:<column>"` |
| STG_DUPLICATE | Duplicate key | A record's key signature (primary key or unique key) has been seen before | `quality_status=DUPLICATE`, `disposition=REJECTED`, `quality_rule_id=STG_DUPLICATE`, `disposition_reason="duplicate_key:<primary_key>"` |

**No other validation rules are applied.** The staging layer does not perform business logic checks, aggregations, or KPI calculations. Its sole purpose is schema normalization, type conversion, nullability validation, required-field validation, and duplicate detection.

---

## 7. Rejected-Record Handling

Rejected records are **never silently discarded**. They are always written to the quarantine output with:

1. **Original values** (after type conversion where applicable — a failed type conversion returns `None` or raises, and the record is rejected before the values are lost)
2. **Explicit rejection reason** (QualityRuleID + DispositionReason)
3. **Full lineage metadata** (SourceID, SourceSHA256, RAWRunID, RawSnapshotPath, etc.)
4. **Source row number** (1-based ordinal in the original source)

The quarantine output is a CSV file with the same column structure as the accepted output, plus the staging metadata columns (`SourceFile`, `SourceRowNumber`, `IngestedAtUTC`, `SchemaVersion`, `QualityStatus`, `QualityRuleID`, `Disposition`, `DispositionReason`, `SourceID`, `SourceSHA256`, `RAWRunID`, `RawSnapshotPath`, `TransformationVersion`).

**Example rejected record (CSV):**
```
AirlineName,SourceAirlineId,DimAirlineId,SourceAirlineKey,DimAirlineKey,AirlineIdMatches,MappingStatus,SourceFile,SourceRowNumber,IngestedAtUTC,SchemaVersion,QualityStatus,QualityRuleID,Disposition,DispositionReason,SourceID,SourceSHA256,RAWRunID,RawSnapshotPath,TransformationVersion
Emirates,AIR001,AIR-0001,A360-AIR-001,1,False,PROVISIONAL_REQUIRES_OWNER_REVIEW,lineage.csv,1,2026-11-04T12:00:00+00:00,1.0.0,rejected,STG_REQUIRED,missing_required_field:MappingStatus,airline_id_crosswalk,<sha256>,20261104_120000_000000,data/01_raw/runs/20261104_120000_000000/sources/airline_id_crosswalk/AIRLINE_ID_CROSSWALK.xlsx,1.0.0
```

---

## 8. Determinism and Rebuildability

- **Deterministic output:** Given the same RAW snapshot and staging plan, the accepted records and their fields are always identical. This is verified by `test_staging_output_is_deterministic()`.
- **Rebuildable from RAW + REFERENCE:** Staging outputs can be regenerated from the RAW snapshots and the reference data (staging plans, source index) without requiring manual edits.
- **Incremental rebuild is safe:** Running the staging script with a new run ID produces a new output directory; existing directories are not modified (no-overwrite protection).
- **Checksum verification:** Every accepted output file has a SHA-256 hash recorded in the run manifest, enabling integrity verification.

---

## 9. CLI Usage

```bash
# Build staging layer from latest completed RAW run
python scripts/build_staging_layer.py

# Specify a RAW run ID
python scripts/build_staging_layer.py --raw-run-id 20261104_120000_000000

# Use a specific staging run ID
python scripts/build_staging_layer.py --run-id 20261104_180000_000000

# Fail the run if any records are quarantined
python scripts/build_staging_layer.py --strict

# JSON output format
python scripts/build_staging_layer.py --format json
```

**Exit codes:**
- `0` — Successful run with no critical errors
- `1` — Precondition failure (no completed RAW run), cross-source failure, or `--strict` with quarantined records

---

## 10. Test Results

All 17 unit tests in `tests/unit/test_staging_processor.py` pass:

| Test Category | Tests | Status |
|--------------|-------|--------|
| Staging plan registry | 2 | Pass |
| CSV source — accepted and nullable | 1 | Pass |
| CSV source — missing required field | 1 | Pass |
| CSV source — invalid type | 1 | Pass |
| CSV source — duplicate detection | 1 | Pass |
| JSON source — valid manifest | 1 | Pass |
| JSON source — invalid allowed value | 1 | Pass |
| XLSX source — DimAirline sheet | 1 | Pass |
| Snapshot checksum mismatch | 1 | Pass |
| Snapshot not found | 1 | Pass |
| Path traversal protection | 1 | Pass |
| No-overwrite protection | 1 | Pass |
| Unknown source has no plan | 1 | Pass |
| Staged record contract metadata | 1 | Pass |
| Staging run manifest written | 1 | Pass |
| Deterministic output | 1 | Pass |

**17 passed, 0 failed.**

---

## 11. Limitations

| Limitation | Description |
|------------|-------------|
| **No business logic** | Staging does not perform business rule checks, aggregations, or KPI calculations. It only validates schema, types, required fields, and duplicates. |
| **Fixed source scope** | Only the four registered RAW sources are supported. Adding new sources requires a new `SourceStagingPlan` entry. |
| **No incremental refresh** | All builders are full-rebuild only. Incremental refresh is future work. |
| **OD-04 blocked** | Exchange-rate reference data cannot be created without owner approval (OD-04). |
| **openpyxl dependency** | XLSX reading requires `openpyxl` 3.1.5, which is installed. |
| **No automatic source discovery** | Sources must be explicitly registered in `create_default_source_registry()` and the source index. |
| **Single manifest per JSON source** | JSON staging currently supports single-record manifests (e.g., route keymap V1 manifest). Multi-record JSON arrays are supported but not yet tested for the registered sources. |

---

## 12. Relationship to Other Layers

| Layer | Relationship |
|-------|-------------|
| **RAW (`data/01_raw/`)** | Provides immutable source snapshots with SHA-256 checksums. STAGING reads RAW manifests and snapshots. |
| **CURATED (`data/03_curated/`)** | Consumes STAGING outputs (accepted records) to populate dimension and fact tables. Power BI imports CURATED only. |
| **REFERENCE (`data/04_reference/`)** | Provides code lists and reference data used by STAGING validation (e.g., allowed values for MappingStatus). |

**Data flow:** RAW → STAGING → CURATED

The STAGING layer is the sole transformation point between immutable RAW sources and the Power BI-consumable CURATED layer. All CURATED rows must trace through a STAGING record back to a RAW snapshot.

---

## 13. References

- `docs/MILESTONE_3_DATA_ENGINEERING_ARCHITECTURE_ASSESSMENT.md` — High-level architecture assessment
- `docs/RAW_LAYER_IMPLEMENTATION.md` — RAW layer implementation details
- `src/staging/staging_processor.py` — Staging processor implementation
- `scripts/build_staging_layer.py` — STAGING layer CLI entry point
- `tests/unit/test_staging_processor.py` — Unit tests for the staging layer
- `config/settings.py` — Project configuration
- `src/utilities/` — Shared utilities (hashing, I/O, logging, paths)

---

**End of documentation.**