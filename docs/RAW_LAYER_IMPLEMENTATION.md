# AEROVISION 360 — RAW Data Ingestion Layer

**Document type:** Implementation documentation  
**Milestone:** 3 — Data Engineering Architecture  
**Task:** M3.4 — RAW Layer  
**Project root:** `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`  
**Prepared:** 2026-11-04  
**Status:** IMPLEMENTED  

---

## 1. Overview

The RAW layer (`data/01_raw/`) is the first layer in the AEROVISION 360
data pipeline. It preserves immutable copies of source data exactly as
received, before any transformation, cleansing, or business-rule
correction.

The RAW layer implements the principle: **RAW is never overwritten,
cleaned in place, or silently corrected.** Every CURATED row must trace
to a RAW record, a controlled reference value, or a documented
allocation.

## 2. Folder Structure

```
data/01_raw/
├── runs/
│   <run_id>/                          One directory per ingestion run
│     run_manifest.json                Run-level manifest
│     sources/
│       <source_id>/                   One directory per source
│         <original_filename>          Immutable snapshot copy
│   ...
├── source_index.json                  Index of all ingested sources
└── ...
```

| Path | Purpose |
|------|---------|
| `data/01_raw/runs/<run_id>/` | Isolation directory for a single ingestion run |
| `data/01_raw/runs/<run_id>/run_manifest.json` | Run-level manifest with all source metadata |
| `data/01_raw/runs/<run_id>/sources/<source_id>/<filename>` | Immutable snapshot of the source file |
| `data/01_raw/source_index.json` | Index of all ingested sources across all runs |

## 3. Source Registration

Sources are registered explicitly in `create_default_source_registry()`
in `src/ingestion/raw_ingestion.py`. Each source record contains:

| Field | Description |
|-------|-------------|
| `source_id` | Unique identifier for the source |
| `source_path` | Relative path from project root |
| `source_name` | Human-readable name |
| `source_format` | File format (xlsx, csv, json) |
| `description` | Human-readable description |

### Currently Registered Sources

| Source ID | Source Path | Format |
|-----------|-------------|--------|
| `airline_reference_workbook` | `data/04_reference/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx` | xlsx |
| `airline_id_crosswalk` | `data/04_reference/AIRLINE_ID_CROSSWALK.csv` | csv |
| `dim_route_keymap_v1` | `data/04_reference/DIM_ROUTE_KEYMAP_V1.csv` | csv |
| `dim_route_keymap_v1_manifest` | `data/04_reference/DIM_ROUTE_KEYMAP_V1_MANIFEST.json` | json |

## 4. Ingestion Process

The RAW ingestion is performed by `scripts/build_raw_layer.py` using
`src/ingestion/raw_ingestion.py`. The process is:

1. **Register sources**: Load the default source registry
2. **For each source**:
   a. Verify the source file exists
   b. Check if the source has already been ingested (skip if so)
   c. Compute SHA-256 checksum of the source file
   *d*. Create a snapshot directory under `data/01_raw/runs/<run_id>/sources/<source_id>/`
   e. Copy source bytes to the snapshot (read-only source, write-only snapshot)
   f. Compute SHA-256 checksum of the snapshot and verify it matches the source
   g. Record source metadata and snapshot metadata
3. **Write run manifest**: Atomically write `run_manifest.json` with all metadata
4. **Save source index**: Update `source_index.json` with run information

### Deterministic Run ID

Each run gets a unique ID in the format `YYYYMMDD_HHMMSS_ffffff`
(UTC timestamp with microseconds), ensuring run uniqueness and
deterministic identification.

### Idempotency

Running the ingestion script multiple times is safe:
- Sources already ingested are **skipped** (not re-ingested)
- Existing snapshots are **never overwritten**
- The source index is updated atomically

### Duplicate Detection

If a source has already been ingested in a previous run, the
ingestion is skipped with status `SKIPPED` and a reason message.

## 5. Manifest Schema

### Run Manifest (`run_manifest.json`)

```json
{
  "run_id": "20261104_120000_000000",
  "run_timestamp": "2026-11-04T12:00:00+00:00",
  "tool": "build_raw_layer.py",
  "tool_version": "1.0.0",
  "raw_layer": "data/01_raw",
  "summary": {
    "total_sources": 4,
    "completed": 4,
    "failed": 0,
    "skipped": 0
  },
  "sources": {
    "airline_reference_workbook": {
      "source_name": "AEROVISION 360 Airline Reference Workbook",
      "source_format": "xlsx",
      "source_path": "data/04_reference/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx",
      "original_filename": "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx",
      "byte_size": 18396,
      "source_sha256": "<sha256_hash>",
      "status": "completed",
      "snapshot": {
        "path": "data/01_raw/runs/20261104_120000_000000/sources/airline_reference_workbook/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx",
        "sha256": "<sha256_hash>",
        "size": 18396
      }
    }
  }
}
```

### Source Index (`source_index.json`)

```json
{
  "sources": {
    "airline_reference_workbook": {
      "first_ingested_run": "20261104_120000_000000",
      "runs": [
        {
          "run_id": "20261104_120000_000000",
          "snapshot_path": "data/01_raw/runs/20261104_120000_000000/sources/airline_reference_workbook/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"
        }
      ]
    }
  },
  "runs": ["20261104_120000_000000"]
}
```

## 6. Immutability Guarantees

| Guarantee | Implementation |
|-----------|---------------|
| Source files never modified | Source files are opened read-only (`open("rb")`) and never written |
| Snapshots never overwritten | `write_json_atomic` refuses to overwrite; snapshot copy checks for existing file |
| Snapshot integrity | SHA-256 of snapshot is verified against source SHA-256 after copy; mismatch causes failure |
| Run isolation | Each run gets a unique directory under `runs/<run_id>/` |
| Atomic manifest writes | `write_json_atomic` uses temp file + rename pattern |

## 7. Duplicate Handling

| Scenario | Behavior |
|----------|----------|
| Source already ingested | Status `SKIPPED`, error message recorded, no snapshot created |
| Snapshot file already exists | Status `FAILED`, error message recorded |
| Same source ingested in multiple runs | Each run gets its own snapshot directory; source index tracks all runs |

## 8. Recovery Behaviour

| Failure Mode | Behaviour |
|--------------|-----------|
| Source file missing | Status `FAILED`, error recorded, ingestion continues for other sources |
| Checksum mismatch | Snapshot deleted, status `FAILED`, error recorded |
| Snapshot already exists | Status `FAILED`, error recorded |
| Manifest write failure | Exception propagates; source index may be partially updated |

## 9. Limitations

| Limitation | Description |
|------------|-------------|
| Source files must be under project root | `project_path()` enforces path traversal protection |
| No automatic source discovery | Sources must be explicitly registered in `create_default_source_registry()` |
| No format validation beyond extension | File format is declared in `SourceRecord`; content is not validated |
| No incremental update detection | Sources are tracked by ID; content changes are not detected |
| No compression | Snapshots are stored as raw byte copies |

## 10. Usage

```bash
# Run RAW ingestion (dry-run safe, read-only for sources)
python scripts/build_raw_layer.py

# Expected output:
# AEROVISION 360 - RAW Ingestion Layer
#   Run ID: 20261104_133312_720090
#   Sources to ingest: 4
#   [OK] airline_reference_workbook
#          Source: AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx
#          Size: 18396 bytes
#          SHA-256: <hash>
#         ...
#   Summary:
#     Total sources: 4
#     Completed: 4
#     Failed: 0
#     Skipped: 0
```

## 11. Relationship to Other Layers

| Layer | Relationship to RAW |
|-------|---------------------|
| STAGING (`data/02_staging/`) | Reads from RAW, applies transformations |
| CURATED (`data/03_curated/`) | Reads from STAGING, publishes clean star-schema tables |
| REFERENCE (`data/04_reference/`) | Source of data for RAW ingestion; also read directly by CURATED builders |

RAW is the immutable source of truth. All downstream transformations trace back to RAW snapshots via SHA-256 hashes recorded in manifests.

---

**End of document.** No existing files were modified during RAW layer implementation.