#!/usr/bin/env python3
"""Run quality checks against AEROVISION 360 STAGING datasets.

Validates the four registered staging sources using the reusable Data Quality
Engine and produces auditable quality results and manifests.

Usage:
    python scripts/run_quality_checks.py                   # Validate latest successful STAGING run
    python scripts/run_quality_checks.py --run-id 20261104_154009_828238  # Specify run ID
    python scripts/run_quality_checks.py --json             # JSON output format
    python scripts/run_quality_checks.py --datasets airline_id_crosswalk  # Individual datasets
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure project root is importable when run directly.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.quality.engine import QualityEngine, QualityResult
from src.quality.manifest import QualityManifest
from src.staging.staging_processor import (
    StagingSourceContext,
    create_default_source_registry,
    StagingStatus,
)
from src.utilities.paths import project_path
from src.utilities.hashing import sha256_file
from src.utilities.io import read_json


# ---------------------------------------------------------------------------
# Schema definitions per registered staging source
# ---------------------------------------------------------------------------

# These schemas are derived from the existing SourceStagingPlan definitions
# in src/staging/staging_processor.py. They describe the column structure,
# types, required fields, and keys for each staging source.

AIRLINE_REFERENCE_SCHEMA = QualitySchema(
    required_columns=("AirlineKey", "AirlineId", "AirlineName"),
    type_rules={
        "AirlineKey": "int",
        "AirlineId": "string",
        "AirlineIATACode": "string",
        "AirlineICAOCode": "string",
        "AirlineName": "string",
        "AirlineGroup": "string",
        "HomeCountry": "string",
        "HomeCountryCode": "string",
        "BusinessModelClass": "string",
        "IsActive": "boolean",
        "StatusEffectiveDate": "string",
        "ReferenceVersion": "string",
    },
    nullable_columns=set(),
    primary_key="AirlineKey",
    composite_key=None,
    foreign_keys={},
    allowed_values={},
    numeric_boundaries={},
    date_boundaries={},
    expected_row_count_range=(1, 10),
)

AIRLINE_CROSSWALK_SCHEMA = QualitySchema(
    required_columns=("SourceAirlineId", "DimAirlineId", "SourceAirlineKey", "DimAirlineKey", "MappingStatus"),
    type_rules={
        "AirlineName": "string",
        "SourceAirlineId": "string",
        "DimAirlineId": "string",
        "SourceAirlineKey": "string",
        "DimAirlineKey": "int",
        "AirlineIdMatches": "boolean",
        "MappingStatus": "string",
    },
    nullable_columns=set(),  # All are effectively required; None handled by RULE-001
    primary_key="DimAirlineKey",
    composite_key=None,
    foreign_keys={},
    allowed_values={
        "MappingStatus": ("PROVISIONAL_REQUIRES_OWNER_REVIEW",),
    },
    numeric_boundaries={},
    date_boundaries={},
    expected_row_count_range=(1, 10),
)

ROUTE_KEYMAP_V1_SCHEMA = QualitySchema(
    required_columns=("RouteKey", "RouteCode"),
    type_rules={
        "RouteKey": "int",
        "RouteCode": "string",
    },
    nullable_columns=set(),
    primary_key="RouteCode",
    composite_key=None,
    foreign_keys={},
    allowed_values={},
    numeric_boundaries={},
    date_boundaries={},
    expected_row_count_range=(1, 320),
)

ROUTE_KEYMAP_MANIFEST_SCHEMA = QualitySchema(
    required_columns=("dataset", "version", "row_count", "primary_key"),
    type_rules={
        "dataset": "string",
        "version": "string",
        "status": "string",
        "row_count": "int",
        "primary_key": "string",
        "unique_surrogate_key": "string",
        "key_range_min": "int",
        "key_range_max": "int",
        "allocation_policy": "string",
    },
    nullable_columns=set(),
    primary_key=None,  # single manifest record; no PK in the usual sense
    composite_key=("dataset",),  # composite: (dataset,) uniqueness
    foreign_keys={},
    allowed_values={
        "status": ("IMMUTABLE_VERSIONED_REFERENCE",),
    },
    numeric_boundaries={},
    date_boundaries={},
    expected_row_count_range=(1, 1),
)


# ---------------------------------------------------------------------------
# Per-dataset validation helpers
# ---------------------------------------------------------------------------

def validate_source(
    source_id: str,
    records: list[dict[str, Any]],
    staging_run_id: str,
    schema: QualitySchema,
) -> QualityResult:
    """Validate one staging source against its schema and rule set."""
    engine = QualityEngine(
        dataset_id=source_id,
        staging_run_id=staging_run_id,
        schema=schema,
    )
    # Infer columns from records if not provided
    columns = sorted(records[0].keys()) if records else []
    engine.validate(records, columns=columns)
    return engine.result


def discover_latest_staging_run() -> str | None:
    """Discover the latest completed successful RAW run ID, then find the
    corresponding STAGING run.

    Returns the STAGING run ID or None if no completed RAW run exists.
    """
    from src.ingestion.raw_ingestion import create_default_source_registry

    # Check the RAW source index for completed runs
    raw_root = project_path("data", "01_raw")
    index_path = raw_root / "source_index.json"

    if not index_path.exists():
        return None

    try:
        index = read_json(index_path)
    except Exception:
        return None

    sources = index.get("sources", {})
    if not sources:
        return None

    # Find the latest run across all sources
    all_runs: list[str] = []
    for source_id, source_data in sources.items():
        runs = source_data.get("runs", [])
        for run_info in runs:
            run_id = run_info.get("run_id")
            if run_id:
                all_runs.append(run_id)

    if not all_runs:
        return None

    # Sort by timestamp determinism: YYYYMMDD_HHMMSS_ffffff format sorts lexicographically
    all_runs.sort()
    latest = all_runs[-1]

    # Verify it was completed successfully
    run_manifest_path = raw_root / "runs" / latest / "run_manifest.json"
    if not run_manifest_path.exists():
        return None

    try:
        manifest = read_json(run_manifest_path)
        summary = manifest.get("summary", {})
        completed = int(summary.get("completed", 0) or 0)
        total = int(summary.get("total_sources", 0) or 0)
        if total == 0 or completed != total:
            return None  # Not all sources completed
    except Exception:
        return None

    return latest


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the quality checks CLI."""
    parser = argparse.ArgumentParser(
        prog="run_quality_checks.py",
        description=(
            "Run Data Quality Engine validation against AEROVISION 360 "
            "STAGING datasets."
        ),
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="STAGING run ID to validate. Defaults to the latest completed successful run.",
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=None,
        help="Specific source IDs to validate. If omitted, validates all four registered sources.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Produce JSON output format.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/quality",
        help="Directory for quality manifest output files.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Return non-zero exit code if any dataset outcome is FAIL.",
    )
    return parser


def main() -> int:
    """Run the quality checks CLI."""
    parser = build_parser()
    args = parser.parse_args()

    # Determine which sources to validate
    all_source_ids = [
        "airline_reference_workbook",
        "airline_id_crosswalk",
        "dim_route_keymap_v1",
        "dim_route_keymap_v1_manifest",
    ]

    if args.datasets:
        source_ids = args.datasets
        # Validate that requested datasets are known
        unknown = [s for s in source_ids if s not in all_source_ids]
        if unknown:
            print(f"Error: Unknown source IDs: {unknown}", file=sys.stderr)
            return 1
    else:
        source_ids = all_source_ids

    # Determine the staging run ID
    staging_run_id = args.run_id
    if not staging_run_id:
        latest = discover_latest_staging_run()
        if latest is None:
            print(
                "No completed STAGING run found. Run build_raw_layer.py and "
                "build_staging_layer.py first.",
                file=sys.stderr,
            )
            return 1
        staging_run_id = latest

    print(f"AEROVISION 360 - Quality Checks")
    print(f"  STAGING run ID: {staging_run_id}")
    print(f"  Sources: {len(source_ids)}")
    print()

    # Validate each source
    # source_root must point to the STAGING run directory, not the output dir.
    # manifest_dir controls where the quality manifest is written.
    manifest = QualityManifest(
        run_id=staging_run_id,
        source_root=project_path("data", "02_staging"),
        manifest_dir=args.output_dir,
    )

    exit_code = 0
    for source_id in source_ids:
        # Read the staging output for this source
        source_schema = _schema_for_source(source_id)
        staging_root = project_path("data", "02_staging")
        run_dir = staging_root / staging_run_id / "sources" / source_id

        accepted_path = run_dir / "accepted" / f"{source_id}.csv"
        # Also try parquet
        if not accepted_path.exists():
            accepted_path = run_dir / "accepted" / f"{source_id}.parquet"

        if not accepted_path.exists():
            # Record an explicit failed result so the dataset does not silently
            # disappear from quality evidence.  This ensures the manifest identifies
            # the missing source and the CLI returns a non-zero exit code when
            # strict mode is active.
            result = QualityResult(
                dataset_id=source_id,
                staging_run_id=staging_run_id,
                schema=_schema_for_source(source_id),
                outcome="failed",
            )
            manifest.add_result(source_id, result)
            print(
                f"  [{source_id}] No accepted output found — recorded as FAILED",
                file=sys.stderr,
            )
            if exit_code == 0 and args.strict:
                exit_code = 1
            continue

        # Read the accepted records
        try:
            records = _read_accepted_records(accepted_path, source_schema)
        except Exception as exc:
            print(f"  [{source_id}] Error reading accepted records: {exc}")
            result = QualityResult(dataset_id=source_id, staging_run_id=staging_run_id)
            result.engine.outcome = "failed"
            manifest.add_result(source_id, result)
            if exit_code == 0 and args.strict:
                exit_code = 1
            continue

        # Run quality validation
        result = validate_source(source_id, records, staging_run_id, source_schema)
        manifest.add_result(source_id, result)

        # Console output
        outcome_label = result.outcome.upper()
        print(f"  [{source_id}] {outcome_label} "
              f"(critical={result.failed_count}, warning={result.warning_count})")

        if result.outcome == "failed":
            exit_code = 1

    # Write consolidated manifest
    manifest_path = manifest.manifest_path
    print()
    print(f"  Manifest: {manifest_path}")

    # Print summary
    summary = manifest.summary()
    print(f"  Summary: {summary['total_datasets']} datasets, "
          f"{summary['outcomes']}")

    # Strict mode: fail if any dataset is missing from the manifest
    # (i.e. was silently skipped without a result record).
    if args.strict:
        missing_datasets = [s for s in source_ids
                            if s not in manifest._dataset_results]
        if missing_datasets:
            print(
                f"  Strict mode: missing datasets from manifest: "
                f"{missing_datasets}", file=sys.stderr,
            )
            exit_code = 1

    if exit_code == 0 and args.strict:
        # Re-check if any failed
        for source_id in source_ids:
            if manifest.get_dataset_outcome(source_id) == "failed":
                exit_code = 1
                break

    if args.json:
        # Emit JSON summary
        json_summary = {
            "run_id": staging_run_id,
            "sources_validated": source_ids,
            "outcomes": {k: v for k, v in summary["outcomes"].items()},
            "total_datasets": summary["total_datasets"],
            "total_failed_records": summary["total_failed_records"],
            "total_warning_records": summary["total_warning_records"],
            "manifest_path": str(manifest_path),
        }
        print(json.dumps(json_summary, indent=2, sort_keys=True))

    if args.strict and exit_code == 0:
        # Final strict check
        for source_id in source_ids:
            if manifest.get_dataset_outcome(source_id) == "failed":
                exit_code = 1

    return exit_code


def _schema_for_source(source_id: str) -> QualitySchema:
    """Return the QualitySchema for a given registered source ID."""
    schemas = {
        "airline_reference_workbook": AIRLINE_REFERENCE_SCHEMA,
        "airline_id_crosswalk": AIRLINE_CROSSWALK_SCHEMA,
        "dim_route_keymap_v1": ROUTE_KEYMAP_V1_SCHEMA,
        "dim_route_keymap_v1_manifest": ROUTE_KEYMAP_MANIFEST_SCHEMA,
    }
    return schemas.get(source_id, QualitySchema())


def _read_accepted_records(accepted_path: Path, schema: QualitySchema) -> list[dict[str, Any]]:
    """Read accepted staging records from a CSV or Parquet file."""
    import csv

    if accepted_path.suffix.lower() == ".csv":
        records: list[dict[str, Any]] = []
        with open(accepted_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Trim string values and convert known types
                cleaned = {}
                for k, v in row.items():
                    v = v.strip() if isinstance(v, str) else v
                    cleaned[k] = v
                records.append(cleaned)
        return records

    # Fallback: simple CSV reader for non-standard paths
    # In production, parquet would use pandas; here we skip parquet reading
    # to keep dependencies minimal.
    raise FileNotFoundError(f"Unsupported format for {accepted_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())