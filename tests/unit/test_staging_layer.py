"""Unit tests for the STAGING layer.

All tests use temporary directories and synthetic reference fixtures. They do not
modify AEROVISION 360 production datasets.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from openpyxl import Workbook

import src.transformations.staging as staging_mod
from src.transformations.staging import (
    MissingRawRunError,
    RawSnapshotIntegrityError,
    StagingManager,
)

AIRLINE_NAMES = [
    "Emirates",
    "Qatar Airways",
    "Singapore Airlines",
    "Air India",
    "IndiGo",
    "British Airways",
    "Lufthansa",
    "Delta Air Lines",
    "Southwest Airlines",
    "Qantas",
]
IATA = ["EK", "QR", "SQ", "AI", "6E", "BA", "LH", "DL", "WN", "QF"]
ICAO = ["UAE", "QTR", "SIA", "AIC", "IGO", "BAW", "DLH", "DAL", "SWA", "QFA"]
NUMERIC = ["176", "157", "618", "098", "312", "125", "220", "006", "526", "081"]
COUNTRIES = [
    "United Arab Emirates",
    "Qatar",
    "Singapore",
    "India",
    "India",
    "United Kingdom",
    "Germany",
    "United States",
    "United States",
    "Australia",
]
COUNTRY_CODES = ["AE", "QA", "SG", "IN", "IN", "GB", "DE", "US", "US", "AU"]


def _fake_project_path_factory(tmp_path: Path):
    import src.utilities.paths as original_paths

    def fake_project_path(*parts):
        if parts and parts[0] == "data":
            return tmp_path / Path(*parts)
        return original_paths.project_path(*parts)

    return fake_project_path


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _write_raw_file(
    raw_root: Path,
    raw_run_id: str,
    source_id: str,
    filename: str,
    content: bytes,
) -> dict:
    snapshot_path = raw_root / "runs" / raw_run_id / "sources" / source_id / filename
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_bytes(content)
    relative = snapshot_path.relative_to(raw_root).as_posix()
    return {
        "source_id": source_id,
        "filename": filename,
        "path": relative,
        "source_path": f"data/04_reference/{filename}",
        "byte_size": len(content),
        "sha256": _sha256_bytes(content),
    }


def _build_workbook(path: Path, *, invalid: bool = False) -> None:
    workbook = Workbook()
    airlines = workbook.active
    airlines.title = "Airlines"
    airlines.append([
        "AirlineId",
        "AirlineKey",
        "AirlineName",
        "LegalName",
        "IATA_Code",
        "IATA_AirlineCode",
        "ICAO_Code",
        "CountryISO2",
        "CountryName",
        "BusinessModelClass",
        "AirlineGroup",
        "IsActive",
        "StatusEffectiveDate",
        "IdentityVerificationStatus",
        "RosterOrigin",
        "ReferenceVersion",
        "Notes",
    ])
    for index in range(10):
        airlines.append([
            f"AIR{index + 1:03d}",
            f"A360-AIR-{index + 1:03d}",
            AIRLINE_NAMES[index],
            f"{AIRLINE_NAMES[index]} Limited",
            IATA[index],
            NUMERIC[index],
            ICAO[index],
            COUNTRY_CODES[index],
            COUNTRIES[index],
            "Hybrid" if invalid and index == 0 else None,
            None,
            True,
            None,
            "VERIFIED",
            "TEST_FIXTURE",
            "A360-REF-0.3-DRAFT",
            "test fixture",
        ])

    register = workbook.create_sheet("Source Register")
    register.append([
        "SourceRecordId",
        "AirlineId",
        "AttributeName",
        "SourcePublisher",
        "SourceTitle",
        "SourceURL",
        "AccessedDate",
        "VerificationStatus",
        "EvidenceNotes",
    ])
    for index in range(10):
        register.append([
            f"SRC-{index + 1:04d}",
            f"AIR{index + 1:03d}",
            "IATA_Code",
            "Test Publisher",
            "Test evidence record",
            "http://insecure.example.invalid/source" if invalid and index == 0 else "https://example.invalid/source",
            "2026-11-04",
            "VERIFIED",
            "" if invalid and index == 0 else "test fixture evidence",
        ])

    readme = workbook.create_sheet("Reference Readme")
    readme.append(["Topic", "Definition"])
    readme.append(["Project", "AEROVISION 360 test fixture"])
    readme.append(["Simulation boundary", "Synthetic operations; real identity reference only"])
    if invalid:
        readme.append([None, None])

    change_log = workbook.create_sheet("Change Log")
    change_log.append(["ChangeId", "Date", "ReferenceVersion", "ChangeDescription", "ChangedBy", "Evidence"])
    change_log.append(["CHG-0001", "2026-11-04", "A360-REF-0.3-DRAFT", "test fixture change", "test fixture", "test fixture evidence"])

    dim_airline = workbook.create_sheet("DimAirline")
    dim_airline.append([
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
    ])
    for index in range(10):
        dim_airline.append([
            index + 1,
            f"AIR-{index + 1:04d}",
            IATA[index],
            ICAO[index],
            AIRLINE_NAMES[index],
            None,
            COUNTRIES[index],
            COUNTRY_CODES[index],
            "Low Cost" if invalid and index == 0 else None,
            True,
            None,
            "AIR-2026-11-04-001",
        ])

    workbook.save(path)


def _make_raw_run(
    tmp_path: Path,
    monkeypatch,
    *,
    invalid: bool = False,
    manifest_row_count: int | None = None,
    manifest_sha_override: str | None = None,
):
    monkeypatch.setattr(staging_mod, "project_path", _fake_project_path_factory(tmp_path))

    raw_root = tmp_path / "data" / "01_raw"
    raw_run_id = "raw_test"

    route_rows = [
        ("1", "XAA-XBB"),
        ("2", "XAC-XAD"),
        ("3", "XBC-XBD"),
    ]
    if invalid:
        route_rows = [
            ("1", "XAA-XBB"),
            ("2", "XAC-XAD"),
            ("2", "XAC-XAE"),
            ("4", "not-a-code"),
        ]

    route_csv = "RouteKey,RouteCode\n" + "\n".join(f"{key},{code}" for key, code in route_rows) + "\n"
    route_snapshot = _write_raw_file(
        raw_root,
        raw_run_id,
        "dim_route_keymap_v1",
        "DIM_ROUTE_KEYMAP_V1.csv",
        route_csv.encode("utf-8"),
    )

    numeric_keys = [int(row[0]) for row in route_rows if row[0].isdigit()]
    manifest = {
        "dataset": "DimRouteKeyMap",
        "project": "AEROVISION 360",
        "version": "V1",
        "status": "IMMUTABLE_VERSIONED_REFERENCE",
        "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
        "purpose": "test fixture route key map",
        "row_count": manifest_row_count if manifest_row_count is not None else len(route_rows),
        "columns": ["RouteKey", "RouteCode"],
        "primary_key": "RouteCode",
        "unique_surrogate_key": "RouteKey",
        "key_range": {
            "minimum": min(numeric_keys),
            "maximum": max(numeric_keys),
        },
        "original_baseline": {
            "path": "data/03_curated/test.csv",
            "row_count": 64,
            "sha256": "a" * 64,
            "preserved_original_mappings": True,
        },
        "expanded_source": {
            "path": "reports/test.csv",
            "row_count": len(route_rows),
            "sha256": "b" * 64,
        },
        "allocation_policy": "test fixture allocation policy",
        "files": {
            "csv": {
                "path": "data/04_reference/DIM_ROUTE_KEYMAP_V1.csv",
                "sha256": manifest_sha_override or route_snapshot["sha256"],
            }
        },
        "generated_at_utc": "2026-11-04T08:24:24.539774+00:00",
    }
    manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
    manifest_snapshot = _write_raw_file(
        raw_root,
        raw_run_id,
        "dim_route_keymap_v1_manifest",
        "DIM_ROUTE_KEYMAP_V1_MANIFEST.json",
        manifest_bytes,
    )

    crosswalk_rows = ["AirlineName,SourceAirlineId,DimAirlineId,SourceAirlineKey,DimAirlineKey,AirlineIdMatches,MappingStatus"]
    for index in range(10):
        if invalid and index == 9:
            crosswalk_rows.append("Bad Airline,BAD,AIR-0010,A360-AIR-010,x,yes,PROVISIONAL_REQUIRES_OWNER_REVIEW")
        else:
            crosswalk_rows.append(
                f"{AIRLINE_NAMES[index]},AIR{index + 1:03d},AIR-{index + 1:04d},A360-AIR-{index + 1:03d},{index + 1},true,VERIFIED"
            )
    crosswalk_bytes = ("\n".join(crosswalk_rows) + "\n").encode("utf-8")
    crosswalk_snapshot = _write_raw_file(
        raw_root,
        raw_run_id,
        "airline_id_crosswalk",
        "AIRLINE_ID_CROSSWALK.csv",
        crosswalk_bytes,
    )

    workbook_path = raw_root / "runs" / raw_run_id / "sources" / "airline_reference_workbook" / "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"
    workbook_path.parent.mkdir(parents=True, exist_ok=True)
    _build_workbook(workbook_path, invalid=invalid)
    workbook_bytes = workbook_path.read_bytes()
    workbook_snapshot = {
        "source_id": "airline_reference_workbook",
        "filename": workbook_path.name,
        "path": workbook_path.relative_to(raw_root).as_posix(),
        "source_path": "data/04_reference/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx",
        "byte_size": len(workbook_bytes),
        "sha256": _sha256_bytes(workbook_bytes),
    }

    sources = {}
    snapshots = [route_snapshot, manifest_snapshot, crosswalk_snapshot, workbook_snapshot]
    source_meta = {
        "airline_id_crosswalk": ("Airline ID Crosswalk", "csv"),
        "airline_reference_workbook": ("AEROVISION 360 Airline Reference Workbook", "xlsx"),
        "dim_route_keymap_v1": ("DimRoute KeyMap V1", "csv"),
        "dim_route_keymap_v1_manifest": ("DimRoute KeyMap V1 Manifest", "json"),
    }
    for snapshot in snapshots:
        source_name, source_format = source_meta[snapshot["source_id"]]
        sources[snapshot["source_id"]] = {
            "source_name": source_name,
            "source_format": source_format,
            "source_path": snapshot["source_path"],
            "original_filename": snapshot["filename"],
            "byte_size": snapshot["byte_size"],
            "source_sha256": snapshot["sha256"],
            "status": "completed",
            "snapshot": {
                "path": snapshot["path"],
                "sha256": snapshot["sha256"],
                "size": snapshot["byte_size"],
            },
        }

    manifest = {
        "run_id": raw_run_id,
        "run_timestamp": "2026-11-04T12:00:00+00:00",
        "tool": "test_fixture",
        "tool_version": "1.0.0",
        "raw_layer": "data/01_raw",
        "summary": {
            "total_sources": 4,
            "completed": 4,
            "failed": 0,
            "skipped": 0,
        },
        "sources": sources,
    }
    raw_manifest_path = raw_root / "runs" / raw_run_id / "run_manifest.json"
    raw_manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {
        "raw_root": raw_root,
        "raw_run_id": raw_run_id,
        "workbook_snapshot_path": workbook_path,
        "crosswalk_snapshot_path": raw_root / "runs" / raw_run_id / "sources" / "airline_id_crosswalk" / "AIRLINE_ID_CROSSWALK.csv",
    }


def test_valid_fixture_stages_complete(tmp_path, monkeypatch):
    fixture = _make_raw_run(tmp_path, monkeypatch)
    before = fixture["crosswalk_snapshot_path"].read_bytes()

    manager = StagingManager(raw_run_id=fixture["raw_run_id"], staging_run_id="staging_valid")
    run = manager.stage_all()

    assert run.status == "completed"
    assert run.errors == []
    assert run.total_input_rows == 47
    assert run.total_accepted_rows == 47
    assert run.total_rejected_rows == 0
    assert run.quality_status == "PASS"
    assert fixture["crosswalk_snapshot_path"].read_bytes() == before

    manifest_path = Path(run.output_dir) / "staging_manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["raw_run_id"] == fixture["raw_run_id"]
    assert manifest["status"] == "completed"
    assert manifest["summary"]["accepted_rows"] == 47
    assert manifest["source_snapshots"]["airline_id_crosswalk"]["verified"] is True

    accepted = Path(run.output_dir) / "stg_airline_id_crosswalk.csv"
    assert accepted.exists()
    content = accepted.read_text(encoding="utf-8")
    assert "AIR001,AIR-0001" in content
    assert "VERIFIED" in content


def test_invalid_records_are_quarantined_not_discarded(tmp_path, monkeypatch):
    _make_raw_run(tmp_path, monkeypatch, invalid=True)
    monkeypatch.setattr(staging_mod, "_check_roster_consistency", lambda outcomes_by_id: [])

    manager = StagingManager(raw_run_id="raw_test", staging_run_id="staging_invalid")
    run = manager.stage_all()

    assert run.status == "completed"
    assert run.errors == []
    assert run.quality_status == "QUARANTINE_REQUIRED"
    assert run.total_rejected_rows == 7

    by_table = {table.table_id: table for table in run.tables}
    assert by_table["dim_route_keymap_v1"].rejected_count == 2
    assert by_table["airline_id_crosswalk"].rejected_count == 1
    assert by_table["airline_reference_airlines"].rejected_count == 1
    assert by_table["airline_reference_source_register"].rejected_count == 1
    assert by_table["airline_reference_readme"].rejected_count == 1
    assert by_table["airline_reference_dim_airline"].rejected_count == 1
    assert by_table["dim_route_keymap_v1_manifest"].accepted_count == 1

    output_dir = Path(run.output_dir)
    assert (output_dir / "quarantine_dim_route_keymap_v1.csv").exists()
    assert (output_dir / "quarantine_airline_reference_readme.csv").exists()
    assert (output_dir / "staging_rejections.csv").exists()
    rejections = (output_dir / "staging_rejections.csv").read_text(encoding="utf-8")
    assert "STG-" in rejections
    assert "QUARANTINE" not in rejections or "QUARANTINED" in rejections

    accepted_dim = (output_dir / "stg_airline_reference_dim_airline.csv").read_text(encoding="utf-8")
    assert "Low Cost" not in accepted_dim
    assert "AIR-0002" in accepted_dim

    accepted_readme = (output_dir / "stg_airline_reference_readme.csv").read_text(encoding="utf-8")
    assert "test fixture" in accepted_readme


def test_manifest_mismatch_fails_closed_and_quarantines_manifest(tmp_path, monkeypatch):
    _make_raw_run(tmp_path, monkeypatch, manifest_row_count=999)
    monkeypatch.setattr(staging_mod, "_check_roster_consistency", lambda outcomes_by_id: [])

    manager = StagingManager(raw_run_id="raw_test", staging_run_id="staging_manifest_bad")
    run = manager.stage_all()

    assert run.status == "failed"
    assert run.errors
    by_table = {table.table_id: table for table in run.tables}
    assert by_table["dim_route_keymap_v1_manifest"].accepted_count == 0
    assert by_table["dim_route_keymap_v1_manifest"].rejected_count == 1
    assert (Path(run.output_dir) / "quarantine_dim_route_keymap_v1_manifest.parquet").exists()


def test_route_manifest_hash_mismatch_is_rejected(tmp_path, monkeypatch):
    _make_raw_run(tmp_path, monkeypatch, manifest_sha_override="0" * 64)
    monkeypatch.setattr(staging_mod, "_check_roster_consistency", lambda outcomes_by_id: [])

    manager = StagingManager(raw_run_id="raw_test", staging_run_id="staging_manifest_hash_bad")
    run = manager.stage_all()

    assert run.status == "failed"
    assert any("sha256" in error.lower() for error in run.errors)


def test_raw_snapshot_hash_mismatch_blocks_before_outputs(tmp_path, monkeypatch):
    fixture = _make_raw_run(tmp_path, monkeypatch)
    snapshot = fixture["crosswalk_snapshot_path"]
    snapshot.write_bytes(snapshot.read_bytes() + b"\n")

    manager = StagingManager(raw_run_id="raw_test", staging_run_id="staging_hash_bad")

    with pytest.raises(RawSnapshotIntegrityError):
        manager.stage_all()

    assert not (tmp_path / "data" / "02_staging" / "staging_hash_bad").exists()


def test_no_completed_raw_run_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(staging_mod, "project_path", _fake_project_path_factory(tmp_path))

    manager = StagingManager(staging_run_id="staging_missing")

    with pytest.raises(MissingRawRunError):
        manager.stage_all()
