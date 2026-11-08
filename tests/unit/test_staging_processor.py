"""Regression tests for the STAGING data layer.

Uses temporary directories for source snapshots and staging outputs,
avoiding any modification to existing project datasets. All tests run in
isolation and clean up after themselves.
"""

import json
from pathlib import Path

import openpyxl
import pytest

import src.staging.staging_processor as sp_mod
from src.staging.staging_processor import (
    QualityStatus,
    StagingProcessor,
    StagingSourceContext,
    StagingStatus,
    get_staging_plan,
)
from src.utilities.hashing import sha256_file
from src.utilities.io import read_json
from src.utilities.paths import project_path


CROSSWALK_CSV = (
    "AirlineName,SourceAirlineId,DimAirlineId,SourceAirlineKey,DimAirlineKey,"
    "AirlineIdMatches,MappingStatus\n"
    "Emirates,AIR001,AIR-0001,A360-AIR-001,1,False,PROVISIONAL_REQUIRES_OWNER_REVIEW\n"
    "Qatar Airways,AIR002,AIR-0002,A360-AIR-002,2,False,PROVISIONAL_REQUIRES_OWNER_REVIEW\n"
)

OPTIONAL_NULL_CSV = (
    "AirlineName,SourceAirlineId,DimAirlineId,SourceAirlineKey,DimAirlineKey,"
    "AirlineIdMatches,MappingStatus\n"
    ",AIR001,AIR-0001,A360-AIR-001,1,False,PROVISIONAL_REQUIRES_OWNER_REVIEW\n"
)

BAD_REQUIRED_CSV = (
    "AirlineName,SourceAirlineId,DimAirlineId,SourceAirlineKey,DimAirlineKey,"
    "AirlineIdMatches,MappingStatus\n"
    "Emirates,AIR001,AIR-0001,A360-AIR-001,1,False,\n"
)

BAD_TYPE_CSV = (
    "AirlineName,SourceAirlineId,DimAirlineId,SourceAirlineKey,DimAirlineKey,"
    "AirlineIdMatches,MappingStatus\n"
    "Emirates,AIR001,AIR-0001,A360-AIR-001,not_an_int,False,PROVISIONAL_REQUIRES_OWNER_REVIEW\n"
)

DUP_ROUTES_CSV = "RouteKey,RouteCode\n1,XAE-XAU\n1,XAE-XAU\n"

VALID_MANIFEST_JSON = json.dumps(
    {
        "dataset": "DimRouteKeyMap",
        "version": "V1",
        "status": "IMMUTABLE_VERSIONED_REFERENCE",
        "row_count": 320,
        "primary_key": "RouteCode",
        "unique_surrogate_key": "RouteKey",
        "key_range_min": 1,
        "key_range_max": 320,
        "allocation_policy": "Existing mappings are permanent.",
    }
).encode("utf-8")

INVALID_MANIFEST_JSON = json.dumps(
    {
        "dataset": "DimRouteKeyMap",
        "version": "V1",
        "status": "NOT_A_VALID_STATUS",
        "row_count": 320,
        "primary_key": "RouteCode",
    }
).encode("utf-8")


RAW_SNAPSHOT_ROOT = "data/01_raw/runs/20260101_000000_000000"


def _create_snapshot(tmp_path: Path, rel_path: str, content: bytes) -> Path:
    full_path = tmp_path / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_bytes(content)
    return full_path


@pytest.fixture
def tmp_project(tmp_path, monkeypatch):
    """Point the staging module's project_path at a temporary project."""

    def fake_project_path(*parts):
        if parts[0] == "data" or parts[0].startswith("data/"):
            return tmp_path / Path(*parts)
        return project_path(*parts)

    monkeypatch.setattr(sp_mod, "project_path", fake_project_path)
    return tmp_path


def _context(
    source_id: str,
    source_path: str,
    source_sha256: str,
    *,
    source_name: str | None = None,
    source_format: str = "csv",
    raw_run_id: str = "20260101_000000_000000",
) -> StagingSourceContext:
    return StagingSourceContext(
        source_id=source_id,
        source_path=source_path,
        source_name=source_name or source_id,
        source_format=source_format,
        source_description="test source",
        source_sha256=source_sha256,
        raw_run_id=raw_run_id,
        raw_snapshot_path=(
            f"runs/{raw_run_id}/sources/{source_id}/{Path(source_path).name}"
        ),
    )


def _processor(tmp_path: Path, run_id: str = "test_staging_run") -> StagingProcessor:
    return StagingProcessor(
        staging_root=tmp_path / "data" / "02_staging",
        source_index_path=tmp_path / "data" / "01_raw" / "source_index.json",
        run_id=run_id,
    )


# ---------------------------------------------------------------------------
# Staging plan registry
# ---------------------------------------------------------------------------

def test_get_staging_plan_known_sources():
    """Registered plans exist for all four RAW sources."""
    for source_id in (
        "airline_reference_workbook",
        "airline_id_crosswalk",
        "dim_route_keymap_v1",
        "dim_route_keymap_v1_manifest",
    ):
        plan = get_staging_plan(source_id)
        assert plan is not None
        assert plan.source_id == source_id


def test_get_staging_plan_unknown_source_returns_none():
    """Unknown sources have no staging plan."""
    assert get_staging_plan("not_a_source") is None


# ---------------------------------------------------------------------------
# CSV source staging
# ---------------------------------------------------------------------------

def test_staging_csv_source_accepted_and_nullable(tmp_project, tmp_path):
    """A valid CSV source is staged with type conversion and nullability."""
    context = _context(
        "airline_id_crosswalk",
        "data/04_reference/AIRLINE_ID_CROSSWALK.csv",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/airline_id_crosswalk/AIRLINE_ID_CROSSWALK.csv",
                CROSSWALK_CSV.encode("utf-8"),
            )
        ),
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.COMPLETED
    assert result.accepted_count == 2
    assert result.rejected_count == 0
    assert result.processed_count == 2
    assert result.output_sha256 is not None

    accepted = result.records[0]
    assert accepted.quality_status == QualityStatus.ACCEPTED
    assert accepted.fields["DimAirlineKey"] == 1
    assert accepted.fields["AirlineIdMatches"] is False
    assert accepted.fields["MappingStatus"] == "PROVISIONAL_REQUIRES_OWNER_REVIEW"

    optional_context = _context(
        "airline_id_crosswalk",
        "data/04_reference/optional_null.csv",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/airline_id_crosswalk/optional_null.csv",
                OPTIONAL_NULL_CSV.encode("utf-8"),
            )
        ),
    )
    optional_result = _processor(
        tmp_path, run_id="test_staging_run_optional"
    ).process_source(optional_context)
    assert optional_result.accepted_count == 1
    assert optional_result.rejected_count == 0
    assert optional_result.records[0].fields["AirlineName"] is None


def test_staging_csv_source_rejects_missing_required(tmp_project, tmp_path):
    """A row missing a required field is rejected with a reason."""
    context = _context(
        "airline_id_crosswalk",
        "data/04_reference/bad_required.csv",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/airline_id_crosswalk/bad_required.csv",
                BAD_REQUIRED_CSV.encode("utf-8"),
            )
        ),
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.COMPLETED
    assert result.accepted_count == 0
    assert result.rejected_count == 1
    rejected = result.records[0]
    assert rejected.quality_status == QualityStatus.REJECTED
    assert rejected.disposition.value == "rejected"
    assert rejected.quality_rule_id == "STG_REQUIRED"
    assert rejected.disposition_reason == "missing_required_field:MappingStatus"


def test_staging_csv_source_rejects_invalid_type(tmp_project, tmp_path):
    """A value that cannot be converted to the staging type is rejected."""
    context = _context(
        "airline_id_crosswalk",
        "data/04_reference/bad_type.csv",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/airline_id_crosswalk/bad_type.csv",
                BAD_TYPE_CSV.encode("utf-8"),
            )
        ),
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.COMPLETED
    assert result.accepted_count == 0
    assert result.rejected_count == 1
    assert result.records[0].quality_rule_id == "STG_TYPE"
    assert result.records[0].disposition_reason == "type_conversion_failed:DimAirlineKey"


def test_staging_csv_source_detects_duplicate(tmp_project, tmp_path):
    """Duplicate staging keys are flagged and never silently accepted."""
    context = _context(
        "dim_route_keymap_v1",
        "data/04_reference/dup_routes.csv",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/dim_route_keymap_v1/dup_routes.csv",
                DUP_ROUTES_CSV.encode("utf-8"),
            )
        ),
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.COMPLETED
    assert result.accepted_count == 1
    assert result.rejected_count == 1
    duplicate = result.records[1]
    assert duplicate.quality_status == QualityStatus.DUPLICATE
    assert duplicate.disposition.value == "rejected"
    assert duplicate.quality_rule_id == "STG_DUPLICATE"
    assert duplicate.disposition_reason == "duplicate_key:RouteCode"


# ---------------------------------------------------------------------------
# JSON source staging
# ---------------------------------------------------------------------------

def test_staging_json_source_accepts_valid_manifest(tmp_project, tmp_path):
    """A valid JSON source is staged into a single typed record."""
    context = _context(
        "dim_route_keymap_v1_manifest",
        "data/04_reference/DIM_ROUTE_KEYMAP_V1_MANIFEST.json",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/dim_route_keymap_v1_manifest/"
                "DIM_ROUTE_KEYMAP_V1_MANIFEST.json",
                VALID_MANIFEST_JSON,
            )
        ),
        source_format="json",
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.COMPLETED
    assert result.source_format == "json"
    assert result.accepted_count == 1
    assert result.rejected_count == 0
    fields = result.records[0].fields
    assert fields["dataset"] == "DimRouteKeyMap"
    assert fields["row_count"] == 320
    assert fields["key_range_max"] == 320


def test_staging_json_source_rejects_invalid_allowed_value(tmp_project, tmp_path):
    """A JSON record violating an allowed value is rejected."""
    context = _context(
        "dim_route_keymap_v1_manifest",
        "data/04_reference/DIM_ROUTE_KEYMAP_V1_MANIFEST.json",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/dim_route_keymap_v1_manifest/"
                "DIM_ROUTE_KEYMAP_V1_MANIFEST.json",
                INVALID_MANIFEST_JSON,
            )
        ),
        source_format="json",
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.COMPLETED
    assert result.accepted_count == 0
    assert result.rejected_count == 1
    assert result.records[0].quality_rule_id == "STG_ALLOWED"


# ---------------------------------------------------------------------------
# XLSX source staging
# ---------------------------------------------------------------------------

def test_staging_xlsx_source_stages_dim_airline_sheet(tmp_project, tmp_path):
    """An XLSX workbook snapshot is staged from its DimAirline sheet."""
    workbook_path = tmp_path / f"{RAW_SNAPSHOT_ROOT}/sources/airline_reference_workbook/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"
    workbook_path.parent.mkdir(parents=True, exist_ok=True)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "DimAirline"
    sheet.append(
        [
            "AirlineKey",
            "AirlineId",
            "AirlineIATACode",
            "AirlineICAOCode",
            "AirlineName",
            "AirlineGroup",
            "HomeCountry",
            "HomeCountryCode",
            "BusinessModelClass",
            "IsActive",
            "StatusEffectiveDate",
            "ReferenceVersion",
        ]
    )
    sheet.append(
        [
            1,
            "AIR-0001",
            "EK",
            "UAE",
            "Emirates",
            None,
            "United Arab Emirates",
            "AE",
            None,
            True,
            None,
            "AIR-2026-11-04-001",
        ]
    )
    workbook.save(str(workbook_path))
    source_sha256 = sha256_file(workbook_path)

    context = _context(
        "airline_reference_workbook",
        "data/04_reference/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx",
        source_sha256,
        source_format="xlsx",
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.COMPLETED
    assert result.accepted_count == 1
    assert result.rejected_count == 0
    fields = result.records[0].fields
    assert fields["AirlineKey"] == 1
    assert fields["AirlineId"] == "AIR-0001"
    assert fields["AirlineName"] == "Emirates"
    assert fields["IsActive"] is True
    assert fields["AirlineGroup"] is None


# ---------------------------------------------------------------------------
# Integrity, errors, traversal and no-overwrite behaviour
# ---------------------------------------------------------------------------

def test_staging_snapshot_checksum_mismatch_fails(tmp_project, tmp_path):
    """A snapshot whose checksum differs from the source is rejected."""
    context = _context(
        "airline_id_crosswalk",
        "data/04_reference/mismatch.csv",
        "0" * 64,
    )
    context = StagingSourceContext(
        source_id=context.source_id,
        source_path=context.source_path,
        source_name=context.source_name,
        source_format=context.source_format,
        source_description=context.source_description,
        source_sha256=context.source_sha256,
        raw_run_id=context.raw_run_id,
        raw_snapshot_path=(
            f"runs/{context.raw_run_id}/sources/{context.source_id}/mismatch.csv"
        ),
    )
    _create_snapshot(
        tmp_path,
        f"data/01_raw/runs/{context.raw_run_id}/sources/{context.source_id}/mismatch.csv",
        CROSSWALK_CSV.encode("utf-8"),
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.FAILED
    assert len(result.errors) == 1
    assert "checksum mismatch" in result.errors[0].lower()


def test_staging_snapshot_not_found_fails(tmp_project, tmp_path):
    """A missing snapshot results in a failed staging result."""
    context = _context(
        "airline_id_crosswalk",
        "data/04_reference/missing.csv",
        "0" * 64,
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.FAILED
    assert "not found" in result.errors[0].lower()


def test_staging_path_traversal_rejected(tmp_project, tmp_path):
    """A snapshot path escaping the RAW layer is rejected."""
    context = StagingSourceContext(
        source_id="airline_id_crosswalk",
        source_path="data/04_reference/AIRLINE_ID_CROSSWALK.csv",
        source_name="Airline ID Crosswalk",
        source_format="csv",
        source_description="test source",
        source_sha256="0" * 64,
        raw_run_id="20260101_000004_000000",
        raw_snapshot_path="../../../../../etc/passwd",
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.FAILED
    assert "escapes RAW layer" in result.errors[0]


def test_staging_no_overwrite_existing_output(tmp_project, tmp_path):
    """Staging refuses to overwrite an existing staging output."""
    context = _context(
        "airline_id_crosswalk",
        "data/04_reference/overwrite.csv",
        sha256_file(
            _create_snapshot(
                tmp_path,
                "data/01_raw/runs/test_staging_run/sources/airline_id_crosswalk/overwrite.csv",
                CROSSWALK_CSV.encode("utf-8"),
            )
        ),
        raw_run_id="test_staging_run",
    )
    processor = _processor(tmp_path, run_id="test_staging_run")

    first = processor.process_source(context)
    assert first.status == StagingStatus.COMPLETED

    second = _processor(tmp_path, run_id="test_staging_run")
    with pytest.raises(FileExistsError):
        second.process_source(context)


def test_staging_unknown_source_has_no_plan(tmp_project, tmp_path):
    """Sources without a registered staging plan fail explicitly."""
    context = _context(
        "custom_source",
        "data/04_reference/custom.csv",
        sha256_file(_create_snapshot(tmp_path, "data/04_reference/custom.csv", b"a,b\n1,2\n")),
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)

    assert result.status == StagingStatus.FAILED
    assert "No staging plan registered" in result.errors[0]


# ---------------------------------------------------------------------------
# Lineage, determinism and manifest
# ---------------------------------------------------------------------------

def test_staged_record_contains_contract_metadata(tmp_project, tmp_path):
    """Staged records carry contract metadata columns and lineage."""
    context = _context(
        "airline_id_crosswalk",
        "data/04_reference/lineage.csv",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/airline_id_crosswalk/lineage.csv",
                CROSSWALK_CSV.encode("utf-8"),
            )
        ),
    )
    processor = _processor(tmp_path)

    result = processor.process_source(context)
    record = result.records[0]
    persisted = sp_mod._staged_record_to_dict(record)

    for column in (
        "SourceFile",
        "SourceRowNumber",
        "IngestedAtUTC",
        "SchemaVersion",
        "QualityStatus",
        "QualityRuleID",
        "Disposition",
        "DispositionReason",
    ):
        assert column in persisted
    assert persisted["SourceFile"] == "lineage.csv"
    assert persisted["SourceRowNumber"] == 1
    assert persisted["IngestedAtUTC"] is not None
    assert persisted["SchemaVersion"] == "1.0.0"
    assert persisted["QualityStatus"] == "accepted"
    assert persisted["Disposition"] == "accepted"
    assert persisted["SourceID"] == "airline_id_crosswalk"
    assert persisted["SourceSHA256"] == sha256_file(
        tmp_path / f"{RAW_SNAPSHOT_ROOT}/sources/airline_id_crosswalk/lineage.csv"
    )
    assert persisted["RAWRunID"] == context.raw_run_id
    assert persisted["RawSnapshotPath"] == context.raw_snapshot_path
    assert persisted["TransformationVersion"] == "1.0.0"


def test_staging_run_manifest_written(tmp_project, tmp_path):
    """The staging run manifest contains required provenance fields."""
    context = _context(
        "airline_id_crosswalk",
        "data/04_reference/manifest_check.csv",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/airline_id_crosswalk/manifest_check.csv",
                CROSSWALK_CSV.encode("utf-8"),
            )
        ),
    )
    processor = _processor(tmp_path, run_id="test_staging_run_manifest")

    result = processor.process_source(context)
    manifest_path = processor.write_run_manifest([result])
    manifest = read_json(manifest_path)

    assert manifest["run_id"] == "test_staging_run_manifest"
    assert manifest["tool"] == "build_staging_layer.py"
    assert manifest["staging_layer"] == "data/02_staging"
    assert manifest["transformation_version"] == "1.0.0"
    assert "sources" in manifest
    source_entry = manifest["sources"]["airline_id_crosswalk"]
    assert source_entry["status"] == "completed"
    assert source_entry["source_sha256"] == sha256_file(
        tmp_path / f"{RAW_SNAPSHOT_ROOT}/sources/airline_id_crosswalk/manifest_check.csv"
    )
    assert source_entry["raw_run_id"] == context.raw_run_id
    assert source_entry["raw_snapshot_path"] == context.raw_snapshot_path
    assert source_entry["staging"]["primary_key"] == "DimAirlineKey"
    assert source_entry["staging"]["dataset_name"] == "DimAirlineCrosswalk"
    assert source_entry["output_sha256"] == result.output_sha256


def test_staging_output_is_deterministic(tmp_project, tmp_path):
    """Repeated staging of identical sources yields equal business fields."""
    context = _context(
        "airline_id_crosswalk",
        "data/04_reference/deterministic.csv",
        sha256_file(
            _create_snapshot(
                tmp_path,
                f"{RAW_SNAPSHOT_ROOT}/sources/airline_id_crosswalk/deterministic.csv",
                CROSSWALK_CSV.encode("utf-8"),
            )
        ),
    )

    first = _processor(tmp_path, run_id="test_staging_run_a").process_source(context)
    second = _processor(tmp_path, run_id="test_staging_run_b").process_source(context)

    assert first.accepted_count == 2
    assert second.accepted_count == 2
    assert [r.fields for r in first.records] == [r.fields for r in second.records]
