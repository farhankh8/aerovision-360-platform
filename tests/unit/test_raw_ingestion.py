"""Regression tests for the RAW ingestion layer.

Uses temporary directories for source files, avoiding any modification
to existing project datasets. All tests run in isolation and clean up
after themselves.
"""

import json
from pathlib import Path

import pytest

from src.ingestion.raw_ingestion import (
    IngestionRun,
    IngestionResult,
    IngestionStatus,
    RawIngestionManager,
    SourceFormat,
    SourceRecord,
    SnapshotRecord,
    create_default_source_registry,
)
from src.utilities.hashing import sha256_file
from src.utilities.paths import project_path


# ---------------------------------------------------------------------------
# SourceRecord tests
# ---------------------------------------------------------------------------

def test_source_record_creation():
    """A SourceRecord can be created with all required fields."""
    source = SourceRecord(
        source_id="test_source",
        source_path="data/04_reference/test.csv",
        source_name="Test Source",
        source_format=SourceFormat.CSV,
        description="A test source file",
    )
    assert source.source_id == "test_source"
    assert source.source_path == "data/04_reference/test.csv"
    assert source.source_name == "Test Source"
    assert source.source_format == SourceFormat.CSV


def test_source_format_values():
    """SourceFormat enum contains expected values."""
    assert SourceFormat.XLSX.value == "xlsx"
    assert SourceFormat.CSV.value == "csv"
    assert SourceFormat.JSON.value == "json"


# ---------------------------------------------------------------------------
# IngestionResult tests
# ---------------------------------------------------------------------------

def test_ingestion_result_completed():
    """An IngestionResult can represent a completed ingestion."""
    result = IngestionResult(
        source_id="test_source",
        status=IngestionStatus.COMPLETED,
    )
    assert result.source_id == "test_source"
    assert result.status == IngestionStatus.COMPLETED
    assert result.source_meta is None
    assert result.snapshot is None
    assert result.error is None


def test_ingestion_result_failed():
    """An IngestionResult can represent a failed ingestion."""
    result = IngestionResult(
        source_id="test_source",
        status=IngestionStatus.FAILED,
        error="Source file not found",
    )
    assert result.status == IngestionStatus.FAILED
    assert result.error == "Source file not found"


def test_ingestion_result_skipped():
    """An IngestionResult can represent a skipped ingestion."""
    result = IngestionResult(
        source_id="test_source",
        status=IngestionStatus.SKIPPED,
        error="Source already ingested",
    )
    assert result.status == IngestionStatus.SKIPPED
    assert result.error == "Source already ingested"


# ---------------------------------------------------------------------------
# IngestionRun tests
# ---------------------------------------------------------------------------

def test_ingestion_run_creation():
    """An IngestionRun can be created with all required fields."""
    run = IngestionRun(
        run_id="20261104_120000_000000",
        run_timestamp="2026-11-04T12:00:00+00:00",
    )
    assert run.run_id == "20261104_120000_000000"
    assert run.total_count == 0
    assert run.completed_count == 0
    assert run.failed_count == 0
    assert run.skipped_count == 0


def test_ingestion_run_counts():
    """IngestionRun counts reflect the results added."""
    run = IngestionRun(
        run_id="test_run",
        run_timestamp="2026-11-04T12:00:00+00:00",
    )
    run.results.append(
        IngestionResult(source_id="s1", status=IngestionStatus.COMPLETED)
    )
    run.results.append(
        IngestionResult(source_id="s2", status=IngestionStatus.FAILED)
    )
    run.results.append(
        IngestionResult(source_id="s3", status=IngestionStatus.SKIPPED)
    )
    assert run.total_count == 3
    assert run.completed_count == 1
    assert run.failed_count == 1
    assert run.skipped_count == 1


# ---------------------------------------------------------------------------
# Helper functions for manager tests
# ---------------------------------------------------------------------------

def _create_source_file(tmp_path: Path, rel_path: str, content: bytes) -> Path:
    """Create a source file under tmp_path/data/04_reference/."""
    full_path = tmp_path / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_bytes(content)
    return full_path


def _make_project_path_fn(tmp_path: Path):
    """Create a fake project_path function that maps data/ paths to tmp_path."""
    import src.ingestion.raw_ingestion as ri_mod
    original_pp = ri_mod.project_path

    def fake_project_path(*parts):
        if parts[0] == "data" or parts[0].startswith("data/"):
            return tmp_path / Path(*parts)
        return original_pp(*parts)

    ri_mod.project_path = fake_project_path
    return original_pp


# ---------------------------------------------------------------------------
# RawIngestionManager tests
# ---------------------------------------------------------------------------

def test_manager_ingests_single_source(tmp_path):
    """A single source file can be ingested into the RAW layer."""
    source_file = _create_source_file(
        tmp_path, "data/04_reference/test_source.csv", b"col1,col2\n1,2\n3,4\n"
    )

    import src.ingestion.raw_ingestion as ri_mod
    original_pp = _make_project_path_fn(tmp_path)

    try:
        manager = RawIngestionManager(run_id="test_run")
        source = SourceRecord(
            source_id="test_csv",
            source_path="data/04_reference/test_source.csv",
            source_name="Test CSV",
            source_format=SourceFormat.CSV,
            description="Debug test",
        )

        result = manager.ingest_source(source)

        assert result.status == IngestionStatus.COMPLETED
        assert result.source_meta is not None
        assert result.source_meta.source_id == "test_csv"
        assert result.source_meta.byte_size > 0
        assert result.source_meta.source_sha256 == sha256_file(source_file)
        assert result.snapshot is not None
        assert result.snapshot.snapshot_sha256 == result.source_meta.source_sha256

        # Verify snapshot exists
        snapshot_full = tmp_path / "data" / "01_raw" / result.snapshot.snapshot_path
        assert snapshot_full.exists()
        assert snapshot_full.read_bytes() == source_file.read_bytes()

        # Verify source file unchanged
        assert source_file.read_bytes() == b"col1,col2\n1,2\n3,4\n"
    finally:
        ri_mod.project_path = original_pp


def test_manager_duplicate_source_skipped(tmp_path):
    """Ingesting the same source twice results in SKIPPED status."""
    source_file = _create_source_file(
        tmp_path, "data/04_reference/dup_source.csv", b"col1\n1\n"
    )

    import src.ingestion.raw_ingestion as ri_mod
    original_pp = _make_project_path_fn(tmp_path)

    try:
        manager = RawIngestionManager(run_id="test_run_dup")
        source = SourceRecord(
            source_id="dup_csv",
            source_path="data/04_reference/dup_source.csv",
            source_name="Dup CSV",
            source_format=SourceFormat.CSV,
            description="Duplicate test",
        )

        # First ingestion
        result1 = manager.ingest_source(source)
        assert result1.status == IngestionStatus.COMPLETED

        # Second ingestion - should be skipped
        result2 = manager.ingest_source(source)
        assert result2.status == IngestionStatus.SKIPPED
        assert result2.error is not None
        assert "already ingested" in result2.error
    finally:
        ri_mod.project_path = original_pp


def test_manager_missing_source(tmp_path):
    """Ingesting a missing source file results in FAILED status."""
    import src.ingestion.raw_ingestion as ri_mod
    original_pp = _make_project_path_fn(tmp_path)

    try:
        manager = RawIngestionManager(run_id="test_run_missing")
        source = SourceRecord(
            source_id="missing_csv",
            source_path="data/04_reference/nonexistent.csv",
            source_name="Missing CSV",
            source_format=SourceFormat.CSV,
            description="Missing source",
        )

        result = manager.ingest_source(source)
        assert result.status == IngestionStatus.FAILED
        assert result.error is not None
        assert "not found" in result.error
        assert result.source_meta is None
        assert result.snapshot is None
    finally:
        ri_mod.project_path = original_pp


def test_manager_snapshot_checksum_matches_source(tmp_path):
    """Snapshot SHA-256 matches source SHA-256 after ingestion."""
    source_content = b"header1,header2\nvalue1,value2\nvalue3,value4\n"
    source_file = _create_source_file(
        tmp_path, "data/04_reference/checksum_test.csv", source_content
    )

    import src.ingestion.raw_ingestion as ri_mod
    original_pp = _make_project_path_fn(tmp_path)

    try:
        manager = RawIngestionManager(run_id="test_run_checksum")
        source = SourceRecord(
            source_id="checksum_csv",
            source_path="data/04_reference/checksum_test.csv",
            source_name="Checksum CSV",
            source_format=SourceFormat.CSV,
            description="Checksum test",
        )

        result = manager.ingest_source(source)
        assert result.status == IngestionStatus.COMPLETED
        assert result.source_meta.source_sha256 == sha256_file(source_file)
        assert result.snapshot.snapshot_sha256 == sha256_file(source_file)
        assert result.source_meta.source_sha256 == result.snapshot.snapshot_sha256
    finally:
        ri_mod.project_path = original_pp


def test_ingestion_run_manifest_written(tmp_path):
    """A run manifest is written after ingestion."""
    source_file = _create_source_file(
        tmp_path, "data/04_reference/manifest_test.csv", b"col1\nval1\n"
    )

    import src.ingestion.raw_ingestion as ri_mod
    original_pp = _make_project_path_fn(tmp_path)

    try:
        manager = RawIngestionManager(run_id="test_run_manifest")
        source = SourceRecord(
            source_id="manifest_csv",
            source_path="data/04_reference/manifest_test.csv",
            source_name="Manifest CSV",
            source_format=SourceFormat.CSV,
            description="Manifest test",
        )

        run = manager.ingest_all([source])
        manifest_path = manager.write_run_manifest(run)

        assert manifest_path.exists()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        assert manifest["run_id"] == "test_run_manifest"
        assert manifest["run_timestamp"] is not None
        assert manifest["tool"] == "build_raw_layer.py"
        assert manifest["summary"]["total_sources"] == 1
        assert manifest["summary"]["completed"] == 1
        assert manifest["summary"]["failed"] == 0
        assert manifest["summary"]["skipped"] == 0

        source_manifest = manifest["sources"]["manifest_csv"]
        assert source_manifest["source_name"] == "Manifest CSV"
        assert source_manifest["source_format"] == "csv"
        assert source_manifest["byte_size"] > 0
        assert source_manifest["source_sha256"] == sha256_file(source_file)
        assert source_manifest["status"] == "completed"
        assert "snapshot" in source_manifest
        assert source_manifest["snapshot"]["sha256"] == sha256_file(source_file)
    finally:
        ri_mod.project_path = original_pp


def test_manager_no_overwrite_existing_snapshot(tmp_path):
    """Re-ingesting a source does not overwrite an existing snapshot."""
    source_file = _create_source_file(
        tmp_path, "data/04_reference/no_overwrite.csv", b"original\ncontent\n"
    )

    import src.ingestion.raw_ingestion as ri_mod
    original_pp = _make_project_path_fn(tmp_path)

    try:
        manager = RawIngestionManager(run_id="test_run_no_overwrite")
        source = SourceRecord(
            source_id="no_overwrite_csv",
            source_path="data/04_reference/no_overwrite.csv",
            source_name="No Overwrite CSV",
            source_format=SourceFormat.CSV,
            description="No overwrite test",
        )

        # First ingestion
        result1 = manager.ingest_source(source)
        assert result1.status == IngestionStatus.COMPLETED

        # Capture original snapshot bytes
        snapshot_path = tmp_path / "data" / "01_raw" / result1.snapshot.snapshot_path
        original_snapshot = snapshot_path.read_bytes()

        # Second ingestion - should be skipped, not overwrite
        result2 = manager.ingest_source(source)
        assert result2.status == IngestionStatus.SKIPPED

        # Snapshot should be unchanged
        assert snapshot_path.read_bytes() == original_snapshot
    finally:
        ri_mod.project_path = original_pp


def test_manager_path_traversal_protection(tmp_path):
    """Sources outside the project root are rejected."""
    import src.ingestion.raw_ingestion as ri_mod
    original_pp = ri_mod.project_path

    def fake_project_path(*parts):
        return tmp_path / Path(*parts)

    ri_mod.project_path = fake_project_path

    try:
        manager = RawIngestionManager(run_id="test_run_traversal")
        # Attempt path traversal
        source = SourceRecord(
            source_id="traversal_csv",
            source_path="../../../etc/passwd",
            source_name="Traversal CSV",
            source_format=SourceFormat.CSV,
            description="Traversal attempt",
        )

        result = manager.ingest_source(source)
        assert result.status == IngestionStatus.FAILED
        assert "not found" in result.error.lower()
    finally:
        ri_mod.project_path = original_pp


def test_default_source_registry():
    """create_default_source_registry returns expected sources."""
    registry = create_default_source_registry()
    assert len(registry) == 4

    source_ids = {s.source_id for s in registry}
    assert "airline_reference_workbook" in source_ids
    assert "airline_id_crosswalk" in source_ids
    assert "dim_route_keymap_v1" in source_ids
    assert "dim_route_keymap_v1_manifest" in source_ids

    # All sources should reference data/04_reference/
    for source in registry:
        assert source.source_path.startswith("data/04_reference/")


def test_default_source_registry_formats():
    """Default registry has correct formats for each source."""
    registry = {s.source_id: s for s in create_default_source_registry()}
    assert registry["airline_reference_workbook"].source_format == SourceFormat.XLSX
    assert registry["airline_id_crosswalk"].source_format == SourceFormat.CSV
    assert registry["dim_route_keymap_v1"].source_format == SourceFormat.CSV
    assert registry["dim_route_keymap_v1_manifest"].source_format == SourceFormat.JSON


def test_manager_run_id_is_unique():
    """Each RawIngestionManager gets a unique run ID."""
    import time
    manager1 = RawIngestionManager()
    time.sleep(0.001)
    manager2 = RawIngestionManager()
    assert manager1.run_id != manager2.run_id


def test_run_manifest_contains_all_required_fields(tmp_path):
    """Run manifest contains all required fields per the spec."""
    source_file = _create_source_file(
        tmp_path, "data/04_reference/manifest_fields.csv", b"col1\nval1\n"
    )

    import src.ingestion.raw_ingestion as ri_mod
    original_pp = _make_project_path_fn(tmp_path)

    try:
        manager = RawIngestionManager(run_id="test_run_manifest_fields")
        source = SourceRecord(
            source_id="manifest_fields_csv",
            source_path="data/04_reference/manifest_fields.csv",
            source_name="Manifest Fields CSV",
            source_format=SourceFormat.CSV,
            description="Manifest fields test",
        )

        run = manager.ingest_all([source])
        manifest_path = manager.write_run_manifest(run)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        # Required top-level fields
        assert "run_id" in manifest
        assert "run_timestamp" in manifest
        assert "tool" in manifest
        assert "tool_version" in manifest
        assert "raw_layer" in manifest
        assert "summary" in manifest
        assert "sources" in manifest

        # Summary fields
        assert "total_sources" in manifest["summary"]
        assert "completed" in manifest["summary"]
        assert "failed" in manifest["summary"]
        assert "skipped" in manifest["summary"]

        # Per-source fields
        src_manifest = manifest["sources"]["manifest_fields_csv"]
        assert "source_name" in src_manifest
        assert "source_format" in src_manifest
        assert "source_path" in src_manifest
        assert "original_filename" in src_manifest
        assert "byte_size" in src_manifest
        assert "source_sha256" in src_manifest
        assert "status" in src_manifest
        assert "snapshot" in src_manifest

        # Snapshot fields
        snap = src_manifest["snapshot"]
        assert "path" in snap
        assert "sha256" in snap
        assert "size" in snap
    finally:
        ri_mod.project_path = original_pp
