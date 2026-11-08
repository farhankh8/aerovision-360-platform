"""Build the RAW ingestion layer for AEROVISION 360.

Ingests registered source files into data/01_raw/ as immutable
snapshots with SHA-256 checksums and full provenance metadata.
Original source files are never modified.

This script is run-safe: it can be executed multiple times without
duplicating or overwriting existing snapshots. Sources that have
already been ingested are skipped.

OD-04 is not relevant to this task - no exchange-rate data is
ingested here.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is importable when run directly.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ingestion.raw_ingestion import (  # noqa: E402
    RawIngestionManager,
    create_default_source_registry,
)


def main() -> int:
    """Run the RAW ingestion build.

    Returns:
        Exit code: 0 for success, 1 for failure.
    """
    manager = RawIngestionManager()
    sources = create_default_source_registry()

    print("AEROVISION 360 - RAW Ingestion Layer")
    print(f"  Run ID: {manager.run_id}")
    print(f"  Sources to ingest: {len(sources)}")
    print()

    run = manager.ingest_all(sources)

    # Print results
    for result in run.results:
        status_icon = {
            "completed": "OK",
            "skipped": "SKIP",
            "failed": "FAIL",
        }.get(result.status.value, result.status.value.upper())
        print(f"  [{status_icon}] {result.source_id}")
        if result.source_meta:
            print(f"         Source: {result.source_meta.original_filename}")
            print(f"         Size: {result.source_meta.byte_size} bytes")
            print(f"         SHA-256: {result.source_meta.source_sha256}")
        if result.snapshot:
            print(f"         Snapshot: {result.snapshot.snapshot_path}")
            print(f"         Snapshot SHA-256: {result.snapshot.snapshot_sha256}")
        if result.error:
            print(f"         Error: {result.error}")

    # Write run manifest
    manifest_path = manager.write_run_manifest(run)
    print(f"\n  Manifest: {manifest_path}")

    # Summary
    print("\nSummary:")
    print(f"  Total sources: {run.total_count}")
    print(f"  Completed: {run.completed_count}")
    print(f"  Failed: {run.failed_count}")
    print(f"  Skipped: {run.skipped_count}")

    if run.failed_count > 0:
        print("\nErrors:")
        for error in run.errors:
            print(f"  - {error}")
        return 1

    print("\nRAW ingestion complete. No source files were modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
