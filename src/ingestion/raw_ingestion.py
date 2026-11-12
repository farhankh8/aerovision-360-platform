"""RAW data ingestion module for AEROVISION 360.

Provides controlled ingestion of source files into the RAW layer.
Original files are never modified. Each ingestion run produces
immutable snapshots with SHA-256 checksums and full provenance metadata.

All path resolution uses src.utilities.paths.project_path. File hashing
uses src.utilities.hashing.sha256_file. Atomic JSON writing uses
src.utilities.io.write_json_atomic. Logging uses
src.utilities.logging.get_logger.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from src.utilities.hashing import sha256_file
from src.utilities.io import write_json_atomic
from src.utilities.logging import get_logger
from src.utilities.paths import project_path


class IngestionStatus(str, Enum):
    """Status of an ingestion operation."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class SourceFormat(str, Enum):
    """Supported source file formats."""

    XLSX = "xlsx"
    CSV = "csv"
    JSON = "json"


@dataclass(frozen=True)
class SourceRecord:
    """Describes a known source file available for ingestion."""

    source_id: str
    source_path: str  # Relative to project root
    source_name: str
    source_format: SourceFormat
    description: str


@dataclass(frozen=True)
class SourceMeta:
    """Metadata for an ingested source."""

    source_id: str
    source_name: str
    source_format: SourceFormat
    source_path: str  # Original relative path
    original_filename: str
    byte_size: int
    source_sha256: str
    status: IngestionStatus


@dataclass(frozen=True)
class SnapshotRecord:
    """Describes a stored snapshot."""

    snapshot_path: str  # Relative to project root
    snapshot_sha256: str
    snapshot_size: int


@dataclass
class IngestionResult:
    """Result of ingesting a single source."""

    source_id: str
    status: IngestionStatus
    source_meta: SourceMeta | None = None
    snapshot: SnapshotRecord | None = None
    error: str | None = None


@dataclass
class IngestionRun:
    """A complete ingestion run."""

    run_id: str
    run_timestamp: str
    results: list[IngestionResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def completed_count(self) -> int:
        return sum(1 for r in self.results if r.status == IngestionStatus.COMPLETED)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if r.status == IngestionStatus.FAILED)

    @property
    def skipped_count(self) -> int:
        return sum(1 for r in self.results if r.status == IngestionStatus.SKIPPED)

    @property
    def total_count(self) -> int:
        return len(self.results)


class RawIngestionError(Exception):
    """Base exception for RAW ingestion errors."""

    pass


class DuplicateSourceError(RawIngestionError):
    """Raised when attempting to ingest a source that's already been ingested."""

    pass


class MissingSourceError(RawIngestionError):
    """Raised when a source file doesn't exist."""

    pass


class RawIngestionManager:
    """Manages RAW layer ingestion.

    Reads source files from data/04_reference/ (or other registered
    locations), computes SHA-256 checksums, creates immutable snapshot
    copies under data/01_raw/, and writes a run manifest with full
    provenance metadata.

    All operations are read-only with respect to source files. Snapshots
    are never overwritten.
    """

    def __init__(self, run_id: str | None = None):
        self.run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        self.run_timestamp = datetime.now(timezone.utc).isoformat()
        self.logger = get_logger(f"aerovision.ingestion.{self.run_id}")
        self._raw_root = project_path("data", "01_raw")
        self._runs_dir = self._raw_root / "runs"
        self._source_index_path = self._raw_root / "source_index.json"
        self._source_index = self._load_source_index()

    def _load_source_index(self) -> dict[str, Any]:
        """Load the source index if it exists."""
        if self._source_index_path.exists():
            return json.loads(self._source_index_path.read_text(encoding="utf-8"))
        return {"sources": {}, "runs": []}

    def _save_source_index(self) -> None:
        """Atomically save the source index."""
        write_json_atomic(self._source_index_path, self._source_index)

    def _is_source_ingested(self, source_id: str) -> bool:
        """Check if a source has already been ingested."""
        return source_id in self._source_index["sources"]

    def _register_source(self, source_id: str, run_id: str, snapshot_path: str) -> None:
        """Register a source in the index."""
        if source_id not in self._source_index["sources"]:
            self._source_index["sources"][source_id] = {
                "first_ingested_run": run_id,
                "runs": [],
            }
        self._source_index["sources"][source_id]["runs"].append(
            {
                "run_id": run_id,
                "snapshot_path": snapshot_path,
            }
        )
        if run_id not in self._source_index["runs"]:
            self._source_index["runs"].append(run_id)

    def ingest_source(self, source: SourceRecord) -> IngestionResult:
        """Ingest a single source file into the RAW layer.

        Reads the source file, computes its SHA-256 checksum, creates an
        immutable snapshot copy under the RAW layer, and records lineage
        metadata. The source file is opened read-only and is never
        modified.

        Args:
            source: The source record describing what to ingest.

        Returns:
            An IngestionResult with the outcome.
        """
        source_path = project_path(source.source_path)

        # Validate source exists
        if not source_path.exists():
            return IngestionResult(
                source_id=source.source_id,
                status=IngestionStatus.FAILED,
                error=f"Source file not found: {source.source_path}",
            )

        # Check for duplicate ingestion
        if self._is_source_ingested(source.source_id):
            return IngestionResult(
                source_id=source.source_id,
                status=IngestionStatus.SKIPPED,
                error=f"Source already ingested: {source.source_id}",
            )

        # Compute source checksum
        source_sha256 = sha256_file(source_path)
        byte_size = source_path.stat().st_size

        # Create snapshot directory
        snapshot_dir = self._runs_dir / self.run_id / "sources" / source.source_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        # Determine snapshot filename (preserve original extension)
        source_path_obj = Path(source.source_path)
        snapshot_filename = source_path_obj.name
        snapshot_path = snapshot_dir / snapshot_filename

        # Check if snapshot already exists (shouldn't, but be safe)
        if snapshot_path.exists():
            return IngestionResult(
                source_id=source.source_id,
                status=IngestionStatus.FAILED,
                error=f"Snapshot already exists: {snapshot_path}",
            )

        # Copy file bytes (read-only source, write snapshot)
        shutil.copy2(source_path, snapshot_path)

        # Verify snapshot checksum matches source
        snapshot_sha256 = sha256_file(snapshot_path)
        if snapshot_sha256 != source_sha256:
            # Snapshot mismatch - remove the bad snapshot
            snapshot_path.unlink()
            return IngestionResult(
                source_id=source.source_id,
                status=IngestionStatus.FAILED,
                error=(
                    f"Snapshot checksum mismatch: "
                    f"source={source_sha256}, snapshot={snapshot_sha256}"
                ),
            )

        # Record snapshot relative path
        snapshot_rel_path = str(snapshot_path.relative_to(self._raw_root))

        # Build source metadata
        source_meta = SourceMeta(
            source_id=source.source_id,
            source_name=source.source_name,
            source_format=source.source_format,
            source_path=source.source_path,
            original_filename=source_path_obj.name,
            byte_size=byte_size,
            source_sha256=source_sha256,
            status=IngestionStatus.COMPLETED,
        )

        snapshot_record = SnapshotRecord(
            snapshot_path=snapshot_rel_path,
            snapshot_sha256=snapshot_sha256,
            snapshot_size=byte_size,
        )

        # Register in source index
        self._register_source(source.source_id, self.run_id, snapshot_rel_path)

        return IngestionResult(
            source_id=source.source_id,
            status=IngestionStatus.COMPLETED,
            source_meta=source_meta,
            snapshot=snapshot_record,
        )

    def ingest_all(self, sources: list[SourceRecord]) -> IngestionRun:
        """Ingest all sources in the registry.

        Args:
            sources: List of SourceRecord objects to ingest.

        Returns:
            An IngestionRun with the results of all ingestion attempts.
        """
        run = IngestionRun(
            run_id=self.run_id,
            run_timestamp=self.run_timestamp,
        )

        for source in sources:
            result = self.ingest_source(source)
            run.results.append(result)
            if result.status == IngestionStatus.FAILED:
                run.errors.append(f"{source.source_id}: {result.error}")
            elif result.status == IngestionStatus.SKIPPED:
                run.warnings.append(f"{source.source_id}: {result.error}")

        # Save source index (overwrite since run data accumulates)
        write_json_atomic(self._source_index_path, self._source_index,
                          overwrite=True)

        return run

    def write_run_manifest(self, run: IngestionRun) -> Path:
        """Write the run manifest atomically.

        The manifest contains run-level metadata, per-source metadata,
        snapshot information, and SHA-256 checksums for both source
        files and snapshots.

        Args:
            run: The IngestionRun to manifest.

        Returns:
            The path to the written manifest file.
        """
        manifest_dir = self._runs_dir / self.run_id
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = manifest_dir / "run_manifest.json"

        manifest_data = {
            "run_id": run.run_id,
            "run_timestamp": run.run_timestamp,
            "tool": "build_raw_layer.py",
            "tool_version": "1.0.0",
            "raw_layer": "data/01_raw",
            "summary": {
                "total_sources": run.total_count,
                "completed": run.completed_count,
                "failed": run.failed_count,
                "skipped": run.skipped_count,
            },
            "sources": {},
        }

        for result in run.results:
            if result.source_id not in manifest_data["sources"]:
                manifest_data["sources"][result.source_id] = {}
            if result.source_meta:
                manifest_data["sources"][result.source_id].update({
                    "source_name": result.source_meta.source_name,
                    "source_format": result.source_meta.source_format.value,
                    "source_path": result.source_meta.source_path,
                    "original_filename": result.source_meta.original_filename,
                    "byte_size": result.source_meta.byte_size,
                    "source_sha256": result.source_meta.source_sha256,
                    "status": result.source_meta.status.value,
                })
            if result.snapshot:
                manifest_data["sources"][result.source_id]["snapshot"] = {
                    "path": result.snapshot.snapshot_path,
                    "sha256": result.snapshot.snapshot_sha256,
                    "size": result.snapshot.snapshot_size,
                }
            if result.error:
                manifest_data["sources"][result.source_id]["error"] = result.error

        write_json_atomic(manifest_path, manifest_data)
        return manifest_path


def create_default_source_registry() -> list[SourceRecord]:
    """Create the default source registry for AEROVISION 360 RAW ingestion.

    Registers source files from data/04_reference/ that are available
    for ingestion into the RAW layer. These are the project's controlled
    reference data files.

    Returns:
        A list of SourceRecord objects ready for registration.
    """
    reference = project_path("data", "04_reference")

    return [
        SourceRecord(
            source_id="airline_reference_workbook",
            source_path="data/04_reference/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx",
            source_name="AEROVISION 360 Airline Reference Workbook",
            source_format=SourceFormat.XLSX,
            description=(
                "Ten-airline reference workbook with Airlines, "
                "Source Register, Reference Readme, and Change Log sheets"
            ),
        ),
        SourceRecord(
            source_id="airline_id_crosswalk",
            source_path="data/04_reference/AIRLINE_ID_CROSSWALK.csv",
            source_name="Airline ID Crosswalk",
            source_format=SourceFormat.CSV,
            description=(
                "Mapping between source airline IDs and semantic "
                "DimAirline IDs"
            ),
        ),
        SourceRecord(
            source_id="dim_route_keymap_v1",
            source_path="data/04_reference/DIM_ROUTE_KEYMAP_V1.csv",
            source_name="DimRoute KeyMap V1",
            source_format=SourceFormat.CSV,
            description="Immutable versioned route key registry (320 routes)",
        ),
        SourceRecord(
            source_id="dim_route_keymap_v1_manifest",
            source_path="data/04_reference/DIM_ROUTE_KEYMAP_V1_MANIFEST.json",
            source_name="DimRoute KeyMap V1 Manifest",
            source_format=SourceFormat.JSON,
            description="Manifest for the DimRoute KeyMap V1 registry",
        ),
    ]
