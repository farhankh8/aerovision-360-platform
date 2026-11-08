"""Build the STAGING layer for AEROVISION 360.

Reads the latest completed RAW run by default, verifies every RAW snapshot
against its manifest, stages the four controlled reference sources using the
reusable StagingProcessor, and writes:

* one accepted and one quarantine dataset per table (CSV + Parquet),
* a combined staging_rejections.csv index,
* a run manifest with counts, output hashes, and RAW lineage.

Record-level rejections are non-fatal: they are written to quarantine outputs
with original values and reason codes. Critical RAW integrity failures or
cross-source inconsistencies fail the run. Use --strict to also fail when
record-level quarantine rows exist.

OD-04 is not relevant to this task. No exchange-rate data is created here.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is importable when run directly.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.staging.staging_processor import (  # noqa: E402
    StagingError,
    StagingProcessor,
    StagingStatus,
    STAGING_PLANS,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the STAGING layer CLI."""
    parser = argparse.ArgumentParser(
        prog="build_staging_layer.py",
        description=(
            "Build STAGING outputs from the completed RAW run. "
            "RAW snapshots are verified before any STAGING output is written."
        ),
    )
    parser.add_argument(
        "--raw-run-id",
        default=None,
        help="RAW run ID to stage. Defaults to the latest completed, successful RAW run.",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional STAGING run ID. Defaults to a UTC microsecond timestamp.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a non-zero exit code when any record is quarantined.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text).",
    )
    return parser


def main() -> int:
    """Run the STAGING build.

    Returns:
        Exit code: 0 for a completed run with no critical errors,
        1 for precondition/cross-source failure, or when --strict is set
        and quarantined records exist.
    """
    parser = build_parser()
    args = parser.parse_args()

    # Discover the latest completed RAW run and source contexts
    processor = StagingProcessor()
    contexts = processor.discover_sources()
    if not contexts:
        print(
            "No completed RAW run found. Run build_raw_layer.py first.",
            file=sys.stderr,
        )
        return 1

    # Use a staging run ID: explicit arg, or UTC microsecond timestamp
    staging_run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")

    processor.run_id = staging_run_id
    processor.staging_root = processor.staging_root  # ensure initialized

    if args.format == "text":
        print("AEROVISION 360 - STAGING Layer")
        print(f"  RAW run ID: {args.raw_run_id or 'latest completed successful run'}")
        print(f"  STAGING run ID: {processor.run_id}")
        print(f"  Sources to stage: {len(contexts)}")
        print()

    try:
        results = processor.process_sources(contexts)
    except Exception as exc:  # noqa: BLE001 - unexpected errors propagate
        if args.format == "json":
            print(json.dumps({"status": "failed", "error": str(exc)}, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    # Write the staging run manifest
    manifest_path = processor.write_run_manifest(results)

    if args.format == "json":
        # Emit a concise JSON summary
        summary = {
            "run_id": processor.run_id,
            "raw_run_id": contexts[0].raw_run_id if contexts else None,
            "status": "completed",
            "sources": len(results),
            "accepted_rows": sum(r.accepted_count for r in results if r.status == StagingStatus.COMPLETED),
            "rejected_rows": sum(r.rejected_count for r in results if r.status == StagingStatus.COMPLETED),
            "manifest_path": str(manifest_path),
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        for result in results:
            status_line = (
                f"  [{result.accepted_count}/{result.rejected_count}/"
                f"{result.duplicate_count}] {result.source_id} "
                f"(input={result.processed_count})"
            )
            print(status_line)
            if result.errors:
                for error in result.errors:
                    print(f"         error: {error}")

        print()
        print(f"  Manifest: {manifest_path}")
        print("  Summary:")
        completed = [r for r in results if r.status == StagingStatus.COMPLETED]
        print(f"    Tables: {len(completed)}")
        print(f"    Input rows: {sum(r.processed_count for r in completed)}")
        print(f"    Accepted rows: {sum(r.accepted_count for r in completed)}")
        print(f"    Rejected rows: {sum(r.rejected_count for r in completed)}")
        print(f"    Duplicate count: {sum(r.duplicate_count for r in completed)}")
        status_str = _status_str_from_results(results)
        print(f"    Status: {status_str}")
        warnings = _warnings_from_results(results)
        if warnings:
            print("    Warnings:")
            for warning in warnings:
                print(f"      - {warning}")
        errors = _errors_from_results(results)
        if errors:
            print("    Errors:")
            for error in errors:
                print(f"      - {error}")

    if _has_errors(results):
        return 1
    if args.strict and _total_rejected(results) > 0:
        return 1
    return 0


def _status_str_from_results(results: list) -> str:
    """Return a concise status string for the staging run."""
    completed = [r for r in results if r.status == StagingStatus.COMPLETED]
    failed = [r for r in results if r.status == StagingStatus.FAILED]
    skipped = [r for r in results if r.status == StagingStatus.SKIPPED]
    parts = [f"{len(completed)}/{len(failed)}/{len(skipped)}"]
    if completed:
        accepted = sum(r.accepted_count for r in completed)
        rejected = sum(r.rejected_count for r in completed)
        parts.append(f"{accepted}/{rejected}")
    return " ".join(parts)


def _warnings_from_results(results: list) -> list[str] | None:
    """Extract warning messages from staging results."""
    warnings: list[str] = []
    for r in results:
        if hasattr(r, "warnings") and r.warnings:
            warnings.extend(r.warnings)
    return warnings if warnings else None


def _errors_from_results(results: list) -> list[str] | None:
    """Extract error messages from staging results."""
    errors: list[str] = []
    for r in results:
        if hasattr(r, "errors") and r.errors:
            errors.extend(r.errors)
    return errors if errors else None


def _total_rejected(results: list) -> int:
    """Return total rejected record count across all results."""
    total = 0
    for r in results:
        if r.status == StagingStatus.COMPLETED:
            total += r.rejected_count
    return total


def _has_errors(results: list) -> bool:
    """Return True if any staging result has errors."""
    for r in results:
        if r.status == StagingStatus.FAILED:
            return True
        if r.errors:
            return True
    return False


def main_entry() -> None:
    """Entry point for use as a module script."""
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())