"""STAGING layer for AEROVISION 360.

The STAGING layer is rebuildable from the RAW layer. It standardizes,
types, validates, flags, and quarantines records before CURATED publication.

Contract rules implemented here:

* invalid records are never silently deleted;
* rejected and flagged rows keep their original values and lineage;
* every row carries the required staging metadata columns;
* staging is rebuildable from RAW snapshots and does not require manual edits;
* staging does not perform business aggregations or KPI calculations.

RAW snapshots are verified against the completed RAW run manifest before
any STAGING output is written. Record-level validation failures are written
to per-table quarantine datasets. Cross-source inconsistencies and RAW
integrity failures are critical errors and are surfaced to the caller.
"""

from __future__ import annotations

import csv
import json
import os
import re
import tempfile
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from openpyxl import load_workbook

from src.utilities.hashing import sha256_file
from src.utilities.io import write_json_atomic
from src.utilities.logging import get_logger
from src.utilities.paths import project_path

STAGING_SCHEMA_VERSION = "staging-1.0.0"
STAGING_TOOL = "build_staging_layer.py"
STAGING_TOOL_VERSION = "1.0.0"

EXPECTED_AIRLINE_COUNT = 10

METADATA_COLUMNS = [
    "SourceFile",
    "SourceRowNumber",
    "SourceSheet",
    "IngestedAtUTC",
    "SchemaVersion",
    "QualityStatus",
    "QualityRuleID",
    "Disposition",
    "DispositionReason",
]

PASS_RULE = "STG-000"
RULE_REQUIRED = "STG-001"
RULE_PATTERN = "STG-002"
RULE_TYPE = "STG-003"
RULE_DATE = "STG-004"
RULE_URL = "STG-005"
RULE_DUPLICATE = "STG-006"
RULE_UNSUPPORTED = "STG-007"
RULE_CROSS_SOURCE = "STG-008"
RULE_EMPTY_ROW = "STG-009"
RULE_UNPARSEABLE = "STG-010"
RULE_OPTIONAL_IDENTITY = "STG-011"
RULE_PROVISIONAL = "STG-012"
RULE_OPTIONAL_TEXT = "STG-013"

ROUTE_HEADERS = ["RouteKey", "RouteCode"]

REQUIRED_COLUMNS = {
    "airline_id_crosswalk": [
        "AirlineName",
        "SourceAirlineId",
        "DimAirlineId",
        "SourceAirlineKey",
        "DimAirlineKey",
        "AirlineIdMatches",
        "MappingStatus",
    ],
    "airline_reference_airlines": [
        "AirlineId",
        "AirlineKey",
        "AirlineName",
        "IATA_Code",
        "IATA_AirlineCode",
        "ICAO_Code",
        "CountryISO2",
        "CountryName",
        "IdentityVerificationStatus",
        "RosterOrigin",
        "ReferenceVersion",
    ],
    "airline_reference_source_register": [
        "SourceRecordId",
        "AirlineId",
        "AttributeName",
        "SourcePublisher",
        "SourceTitle",
        "SourceURL",
        "AccessedDate",
        "VerificationStatus",
        "EvidenceNotes",
    ],
    "airline_reference_readme": ["Topic"],
    "airline_reference_change_log": [
        "ChangeId",
        "Date",
        "ReferenceVersion",
        "ChangeDescription",
        "ChangedBy",
        "Evidence",
    ],
    "airline_reference_dim_airline": [
        "AirlineKey",
        "AirlineId",
        "AirlineIATACode",
        "AirlineICAOCode",
        "AirlineName",
        "HomeCountry",
        "HomeCountryCode",
        "IsActive",
        "ReferenceVersion",
    ],
}

WORKBOOK_SHEETS = {
    "Airlines": "airline_reference_airlines",
    "Source Register": "airline_reference_source_register",
    "Reference Readme": "airline_reference_readme",
    "Change Log": "airline_reference_change_log",
    "DimAirline": "airline_reference_dim_airline",
}


class StagingError(Exception):
    """Base exception for STAGING layer errors."""


class MissingRawRunError(StagingError):
    """Raised when no completed RAW run can be found."""


class RawSnapshotIntegrityError(StagingError):
    """Raised when a RAW snapshot does not match its manifest."""


class StagingSchemaError(StagingError):
    """Raised when a source schema cannot support staging."""


@dataclass(frozen=True)
class Issue:
    """A validation finding attached to a source row."""

    rule_id: str
    message: str
    fatal: bool = True


@dataclass
class TableOutcome:
    """Validated records for a single staged table."""

    table_id: str
    source_id: str
    source_sheet: str | None
    original_columns: list[str]
    input_rows: int
    accepted_records: list[dict[str, Any]]
    quarantine_records: list[dict[str, Any]]
    errors: list[str] = field(default_factory=list)

    @property
    def columns(self) -> list[str]:
        return self.original_columns + METADATA_COLUMNS

    @property
    def flagged_count(self) -> int:
        return sum(
            1 for record in self.accepted_records
            if record.get("QualityStatus") == "FLAGGED"
        )

    @property
    def accepted_count(self) -> int:
        return len(self.accepted_records)

    @property
    def rejected_count(self) -> int:
        return len(self.quarantine_records)


@dataclass(frozen=True)
class TableResult:
    """Published counts and output locations for one staged table."""

    table_id: str
    source_id: str
    source_sheet: str | None
    input_rows: int
    accepted_count: int
    rejected_count: int
    flagged_count: int
    outputs: dict[str, dict[str, Any]]
    errors: list[str]


@dataclass
class StagingRun:
    """Complete STAGING run record."""

    run_id: str
    run_timestamp: str
    raw_run_id: str
    raw_manifest_path: str
    output_dir: str
    status: str
    quality_status: str
    tables: list[TableResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_input_rows(self) -> int:
        return sum(table.input_rows for table in self.tables)

    @property
    def total_accepted_rows(self) -> int:
        return sum(table.accepted_count for table in self.tables)

    @property
    def total_rejected_rows(self) -> int:
        return sum(table.rejected_count for table in self.tables)

    @property
    def total_flagged_rows(self) -> int:
        return sum(table.flagged_count for table in self.tables)


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, datetime):
        return value.date().isoformat() if value.time() == datetime.min.time() else value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else format(value, ".15g")
    return str(value).strip()


def _clean_ws(value: Any) -> str:
    return " ".join(_text(value).split())


def _upper(value: Any) -> str:
    return _clean_ws(value).upper()


def _blank(value: Any) -> bool:
    return _text(value) == ""


def _parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    text = _text(value).lower()
    if text == "true":
        return True
    if text == "false":
        return False
    return None


def _parse_int(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        parsed = value
    elif isinstance(value, float) and value.is_integer():
        parsed = int(value)
    else:
        text = _text(value)
        if not re.fullmatch(r"\d+", text):
            return None
        parsed = int(text)
    if positive and parsed <= 0:
        return None
    return parsed


def _parse_date(value: Any) -> str | None:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = _text(value)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
    except ValueError:
        return None


def _jsonable(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, (date, datetime)):
        return _text(value)
    return _text(value)


def _metadata(source_file: str, source_sheet: str | None, row_number: int, ingested_at: str) -> dict[str, Any]:
    return {
        "SourceFile": source_file,
        "SourceRowNumber": row_number,
        "SourceSheet": source_sheet or "",
        "IngestedAtUTC": ingested_at,
        "SchemaVersion": STAGING_SCHEMA_VERSION,
    }


def _quality_fields(issues: list[Issue]) -> dict[str, str]:
    fatal = [issue for issue in issues if issue.fatal]
    flags = [issue for issue in issues if not issue.fatal]

    if fatal:
        rule_ids = ";".join(dict.fromkeys([issue.rule_id for issue in fatal + flags]))
        reason = " | ".join([issue.message for issue in fatal + flags])
        return {
            "QualityStatus": "REJECTED",
            "QualityRuleID": rule_ids,
            "Disposition": "QUARANTINED",
            "DispositionReason": reason,
        }

    if flags:
        rule_ids = ";".join(dict.fromkeys(issue.rule_id for issue in flags))
        reason = " | ".join(issue.message for issue in flags)
        return {
            "QualityStatus": "FLAGGED",
            "QualityRuleID": rule_ids,
            "Disposition": "ACCEPTED",
            "DispositionReason": reason,
        }

    return {
        "QualityStatus": "ACCEPTED",
        "QualityRuleID": PASS_RULE,
        "Disposition": "ACCEPTED",
        "DispositionReason": "passed staging rules",
    }


def _record(
    values: dict[str, Any],
    issues: list[Issue],
    source_file: str,
    source_sheet: str | None,
    row_number: int,
    ingested_at: str,
) -> dict[str, Any]:
    record = dict(values)
    record.update(_metadata(source_file, source_sheet, row_number, ingested_at))
    record.update(_quality_fields(issues))
    return record


def _classify(
    rows: list[tuple[dict[str, Any], list[Issue]]],
    source_file: str,
    source_sheet: str | None,
    ingested_at: str,
    start_row: int = 2,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    quarantine: list[dict[str, Any]] = []
    for offset, (values, issues) in enumerate(rows):
        row_number = start_row + offset
        record = _record(values, issues, source_file, source_sheet, row_number, ingested_at)
        if record["QualityStatus"] == "REJECTED":
            quarantine.append(record)
        else:
            accepted.append(record)
    return accepted, quarantine


def _merge_quality_fields(record: dict[str, Any], duplicate_issues: list[Issue]) -> None:
    existing_rules = [r for r in str(record.get("QualityRuleID", "")).split(";") if r and r != PASS_RULE]
    existing_reasons = [r for r in str(record.get("DispositionReason", "")).split(" | ") if r and r != "passed staging rules"]
    rules = list(dict.fromkeys(existing_rules + [issue.rule_id for issue in duplicate_issues]))
    reasons = existing_reasons + [issue.message for issue in duplicate_issues]
    record["QualityStatus"] = "REJECTED"
    record["Disposition"] = "QUARANTINED"
    record["QualityRuleID"] = ";".join(rules) if rules else RULE_DUPLICATE
    record["DispositionReason"] = " | ".join(reasons) if reasons else "duplicate business key"


def _quarantine_duplicates(
    accepted: list[dict[str, Any]],
    quarantine: list[dict[str, Any]],
    unique_columns: list[str],
) -> None:
    duplicate_messages: dict[int, list[Issue]] = {id(record): [] for record in accepted}

    for column in unique_columns:
        seen: dict[Any, int] = {}
        for record in accepted:
            key = record.get(column)
            if key is None or _text(key) == "":
                continue
            first_row = seen.get(key)
            if first_row is None:
                seen[key] = int(record["SourceRowNumber"])
                continue
            message = f"Duplicate {column}; first occurrence at source row {first_row} retained"
            duplicate_messages[id(record)].append(Issue(RULE_DUPLICATE, message, True))

    retained: list[dict[str, Any]] = []
    for record in accepted:
        issues = duplicate_messages.get(id(record), [])
        if issues:
            _merge_quality_fields(record, issues)
            quarantine.append(record)
        else:
            retained.append(record)

    accepted[:] = retained


def _snapshot_relative(raw_root: Path, snapshot_path_value: str) -> Path:
    normalized = str(snapshot_path_value).replace("\\", "/")
    candidate = raw_root.joinpath(*[part for part in normalized.split("/") if part]).resolve()
    root = raw_root.resolve()

    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise RawSnapshotIntegrityError(
            f"Snapshot path escapes RAW root: {snapshot_path_value}"
        ) from exc

    return candidate


def _raw_manifest_from_directory(run_dir: Path) -> dict[str, Any] | None:
    manifest_path = run_dir / "run_manifest.json"
    if not manifest_path.exists():
        return None

    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def _completed_raw_candidates(raw_root: Path) -> list[tuple[str, Path, dict[str, Any]]]:
    runs_root = raw_root / "runs"
    candidates: list[tuple[str, Path, dict[str, Any]]] = []

    if not runs_root.exists():
        return candidates

    for run_dir in runs_root.iterdir():
        if not run_dir.is_dir():
            continue
        manifest = _raw_manifest_from_directory(run_dir)
        if not manifest:
            continue
        summary = manifest.get("summary", {})
        total = int(summary.get("total_sources", 0) or 0)
        completed = int(summary.get("completed", 0) or 0)
        failed = int(summary.get("failed", 0) or 0)
        if total == 0 or completed != total or failed != 0:
            continue
        sort_key = str(manifest.get("run_timestamp") or manifest.get("run_id") or run_dir.name)
        candidates.append((sort_key, run_dir, manifest))

    return sorted(candidates, key=lambda item: item[0])


def _read_csv_table(
    path: Path,
    table_id: str,
) -> tuple[list[str], list[tuple[int, list[str]]]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.reader(file)
            try:
                raw_headers = next(reader)
            except StopIteration as exc:
                raise StagingSchemaError(f"CSV source is empty: {path}") from exc

            headers = [_text(cell) for cell in raw_headers]

            if table_id == "dim_route_keymap_v1":
                if headers != ROUTE_HEADERS:
                    raise StagingSchemaError(
                        f"dim_route_keymap_v1 header must be {ROUTE_HEADERS}; found {headers}"
                    )
            elif table_id == "airline_id_crosswalk":
                required = REQUIRED_COLUMNS["airline_id_crosswalk"]
                missing = [column for column in required if column not in headers]
                extra = [column for column in headers if column not in required]
                if missing or extra:
                    raise StagingSchemaError(
                        f"airline_id_crosswalk schema mismatch; missing={missing}, extra={extra}"
                    )

            rows: list[tuple[int, list[str]]] = []
            for row_number, raw_row in enumerate(reader, start=2):
                rows.append((row_number, [_text(cell) for cell in raw_row]))

    except UnicodeDecodeError as exc:
        raise StagingSchemaError(f"CSV source is not valid UTF-8: {path}") from exc

    if not rows:
        raise StagingSchemaError(f"CSV source has no data rows: {path}")

    return headers, rows


def _read_json_file(path: Path) -> tuple[str, Any | None, str | None]:
    raw_text = path.read_text(encoding="utf-8")
    try:
        return raw_text, json.loads(raw_text), None
    except json.JSONDecodeError as exc:
        return raw_text, None, str(exc)


def _read_workbook_headers(path: Path) -> dict[str, tuple[list[str], list[tuple[int, list[Any]]]]]:
    try:
        workbook = load_workbook(path, read_only=True, data_only=True)
    except Exception as exc:  # openpyxl raises several exception types; all are fatal here.
        raise StagingSchemaError(f"Airline reference workbook cannot be opened: {path}") from exc

    sheets: dict[str, tuple[list[str], list[tuple[int, list[Any]]]]] = {}

    try:
        missing = [sheet for sheet in WORKBOOK_SHEETS if sheet not in workbook.sheetnames]
        if missing:
            raise StagingSchemaError(f"Airline reference workbook is missing sheets: {missing}")

        for sheet in WORKBOOK_SHEETS:
            worksheet = workbook[sheet]
            values = list(worksheet.iter_rows(values_only=True))
            if not values:
                raise StagingSchemaError(f"Workbook sheet is empty: {sheet}")

            headers = [_text(cell) for cell in values[0]]
            table_id = WORKBOOK_SHEETS[sheet]
            required = REQUIRED_COLUMNS.get(table_id, [])
            missing_columns = [column for column in required if column not in headers]
            if missing_columns:
                raise StagingSchemaError(
                    f"Workbook sheet {sheet!r} is missing columns: {missing_columns}"
                )

            rows: list[tuple[int, list[Any]]] = []
            for row_number, row_values in enumerate(values[1:], start=2):
                rows.append((row_number, list(row_values)))
            if not rows:
                raise StagingSchemaError(f"Workbook sheet has no data rows: {sheet}")
            sheets[sheet] = (headers, rows)
    finally:
        workbook.close()

    return sheets


def _map_row(headers: list[str], row: list[Any]) -> tuple[dict[str, str], list[Issue]]:
    issues: list[Issue] = []
    expected = len(headers)
    actual = len(row)

    if actual < expected:
        issues.append(
            Issue(
                RULE_UNPARSEABLE,
                f"row has {actual} cells; expected {expected}; trailing blanks assumed",
                True,
            )
        )
    elif actual > expected:
        extra = [_text(cell) for cell in row[expected:]]
        issues.append(
            Issue(
                RULE_UNPARSEABLE,
                f"row has {actual} cells; expected {expected}; extra cells={extra}",
                True,
            )
        )

    values: dict[str, str] = {}
    for index, header in enumerate(headers):
        values[header] = _text(row[index]) if index < actual else ""

    return values, issues


def _finalize_table(
    table_id: str,
    source_id: str,
    source_sheet: str | None,
    original_columns: list[str],
    rows: list[tuple[dict[str, Any], list[Issue]]],
    unique_columns: list[str],
    source_file: str,
    ingested_at: str,
    start_row: int = 2,
) -> TableOutcome:
    accepted: list[dict[str, Any]] = []
    quarantine: list[dict[str, Any]] = []

    for offset, (values, issues) in enumerate(rows):
        row_number = start_row + offset
        record = _record(values, issues, source_file, source_sheet, row_number, ingested_at)
        if record["QualityStatus"] == "REJECTED":
            quarantine.append(record)
        else:
            accepted.append(record)

    _quarantine_duplicates(accepted, quarantine, unique_columns)

    return TableOutcome(
        table_id=table_id,
        source_id=source_id,
        source_sheet=source_sheet,
        original_columns=list(original_columns),
        input_rows=len(rows),
        accepted_records=accepted,
        quarantine_records=quarantine,
    )

def _require_nonblank(values, issues, column):
    if _blank(values.get(column)):
        issues.append(Issue(RULE_REQUIRED, f"{column} is required", True))


def _pattern_nonblank(values, issues, column, pattern, message):
    value = _upper(values.get(column, ""))
    if value and not re.fullmatch(pattern, value):
        issues.append(Issue(RULE_PATTERN, f"{message}; raw={values.get(column)!r}", True))
    return value


def _optional_date(values, issues, column):
    value = values.get(column, "")
    if _blank(value):
        return ""
    parsed = _parse_date(value)
    if not parsed:
        issues.append(Issue(RULE_DATE, f"{column} must be YYYY-MM-DD; raw={value!r}", True))
        return _text(value)
    return parsed


def _required_date(values, issues, column):
    value = values.get(column, "")
    if _blank(value):
        issues.append(Issue(RULE_REQUIRED, f"{column} is required", True))
        return ""
    parsed = _parse_date(value)
    if not parsed:
        issues.append(Issue(RULE_DATE, f"{column} must be YYYY-MM-DD; raw={value!r}", True))
        return _text(value)
    return parsed


def _optional_bool(values, issues, column):
    value = values.get(column, "")
    if _blank(value):
        return None
    parsed = _parse_bool(value)
    if parsed is None:
        issues.append(Issue(RULE_TYPE, f"{column} must be true/false; raw={value!r}", True))
        return _text(value)
    return parsed


def _required_bool(values, issues, column):
    value = values.get(column, "")
    if _blank(value):
        issues.append(Issue(RULE_REQUIRED, f"{column} is required", True))
        return None
    parsed = _parse_bool(value)
    if parsed is None:
        issues.append(Issue(RULE_TYPE, f"{column} must be true/false; raw={value!r}", True))
        return _text(value)
    return parsed


def _required_positive_int(values, issues, column):
    value = values.get(column, "")
    if _blank(value):
        issues.append(Issue(RULE_REQUIRED, f"{column} is required", True))
        return _text(value)
    parsed = _parse_int(value, positive=True)
    if parsed is None:
        issues.append(Issue(RULE_TYPE, f"{column} must be a positive integer; raw={value!r}", True))
        return _text(value)
    return parsed


def _validate_url(value):
    if _blank(value):
        return None
    text = _text(value)
    if not text.startswith("https://"):
        return Issue(RULE_URL, "SourceURL must use HTTPS", True)
    if "<" in text or ">" in text or any(char.isspace() for char in text):
        return Issue(RULE_URL, "SourceURL contains markup or whitespace", True)
    lowered = text.lower()
    if "utm_" in lowered:
        return Issue(RULE_URL, "SourceURL contains tracking parameters", True)
    if re.search(r"^https://[^/@\s]+@\S+", text):
        return Issue(RULE_URL, "SourceURL contains embedded credentials", True)
    return None


def _flag_populated(values, issues, column, message):
    if not _blank(values.get(column)):
        issues.append(Issue(RULE_UNSUPPORTED, message, False))


def _reject_populated(values, issues, column, message):
    if not _blank(values.get(column)):
        issues.append(Issue(RULE_UNSUPPORTED, message, True))


def _flag_blank(values, issues, column, message):
    if _blank(values.get(column)):
        issues.append(Issue(RULE_OPTIONAL_IDENTITY, message, False))


def _stage_route_csv(snapshot_path, source_file, ingested_at):
    headers, raw_rows = _read_csv_table(snapshot_path, "dim_route_keymap_v1")
    rows = []
    numeric_keys = []

    for _row_number, row in raw_rows:
        values, issues = _map_row(headers, row)
        route_key_raw = values["RouteKey"]
        route_code_raw = values["RouteCode"]
        route_key = _parse_int(route_key_raw, positive=True)

        if route_key is None:
            issues.append(
                Issue(RULE_TYPE, f"RouteKey must be a positive integer; raw={route_key_raw!r}", True)
            )
        else:
            numeric_keys.append(route_key)

        route_code = _upper(route_code_raw)
        if not route_code:
            issues.append(Issue(RULE_REQUIRED, "RouteCode is required", True))
        elif not re.fullmatch(r"X[A-Z]{2}-X[A-Z]{2}", route_code):
            issues.append(
                Issue(RULE_PATTERN, f"RouteCode must match 'XAA-XBB'; raw={route_code_raw!r}", True)
            )

        rows.append(
            (
                {
                    "RouteKey": route_key if route_key is not None else _text(route_key_raw),
                    "RouteCode": route_code,
                },
                issues,
            )
        )

    outcome = _finalize_table(
        table_id="dim_route_keymap_v1",
        source_id="dim_route_keymap_v1",
        source_sheet=None,
        original_columns=ROUTE_HEADERS,
        rows=rows,
        unique_columns=["RouteKey", "RouteCode"],
        source_file=source_file,
        ingested_at=ingested_at,
    )
    return outcome, numeric_keys


def _stage_route_manifest(
    snapshot_path,
    source_file,
    ingested_at,
    csv_outcome,
    csv_snapshot_sha256,
    numeric_keys,
):
    raw_text, parsed, parse_error = _read_json_file(snapshot_path)
    columns = [
        "Dataset",
        "Project",
        "Version",
        "Status",
        "Disclosure",
        "Purpose",
        "RowCount",
        "Columns",
        "PrimaryKey",
        "UniqueSurrogateKey",
        "KeyMinimum",
        "KeyMaximum",
        "OriginalBaselinePath",
        "OriginalBaselineRowCount",
        "OriginalBaselineSha256",
        "ExpandedSourcePath",
        "ExpandedSourceRowCount",
        "ExpandedSourceSha256",
        "AllocationPolicy",
        "CsvPath",
        "CsvSha256",
        "GeneratedAtUTC",
    ]

    if parse_error or not isinstance(parsed, dict):
        issue = Issue(
            RULE_UNPARSEABLE,
            f"DIM_ROUTE_KEYMAP_V1_MANIFEST.json is not a valid JSON object: {parse_error}",
            True,
        )
        outcome = _finalize_table(
            table_id="dim_route_keymap_v1_manifest",
            source_id="dim_route_keymap_v1_manifest",
            source_sheet=None,
            original_columns=columns,
            rows=[({column: "" for column in columns}, [issue])],
            unique_columns=[],
            source_file=source_file,
            ingested_at=ingested_at,
            start_row=1,
        )
        outcome.errors = [issue.message]
        return outcome

    issues = []
    key_range = parsed.get("key_range") if isinstance(parsed.get("key_range"), dict) else {}
    files = parsed.get("files") if isinstance(parsed.get("files"), dict) else {}
    csv_info = files.get("csv") if isinstance(files.get("csv"), dict) else {}
    original_baseline = parsed.get("original_baseline") if isinstance(parsed.get("original_baseline"), dict) else {}
    expanded_source = parsed.get("expanded_source") if isinstance(parsed.get("expanded_source"), dict) else {}

    dataset = _clean_ws(parsed.get("dataset"))
    project = _clean_ws(parsed.get("project"))
    version = _clean_ws(parsed.get("version"))
    status = _clean_ws(parsed.get("status"))
    disclosure = _clean_ws(parsed.get("disclosure"))
    purpose = _clean_ws(parsed.get("purpose"))
    allocation_policy = _clean_ws(parsed.get("allocation_policy"))
    generated_at = _clean_ws(parsed.get("generated_at_utc"))

    if not dataset:
        issues.append(Issue(RULE_REQUIRED, "manifest dataset is required", True))
    if not project:
        issues.append(Issue(RULE_REQUIRED, "manifest project is required", True))
    if not version:
        issues.append(Issue(RULE_REQUIRED, "manifest version is required", True))
    if not status:
        issues.append(Issue(RULE_REQUIRED, "manifest status is required", True))

    row_count = _parse_int(parsed.get("row_count"), positive=True)
    if row_count is None:
        issues.append(Issue(RULE_TYPE, f"manifest row_count must be a positive integer; raw={parsed.get('row_count')!r}", True))

    raw_columns = parsed.get("columns")
    columns_list = [str(column).strip() for column in raw_columns] if isinstance(raw_columns, list) else None
    if columns_list is None:
        issues.append(Issue(RULE_REQUIRED, "manifest columns must be a list", True))
    elif columns_list != ROUTE_HEADERS:
        issues.append(
            Issue(RULE_CROSS_SOURCE, f"manifest columns must be {ROUTE_HEADERS}; found {columns_list}", True)
        )

    primary_key = _clean_ws(parsed.get("primary_key"))
    unique_key = _clean_ws(parsed.get("unique_surrogate_key"))
    if primary_key != "RouteCode":
        issues.append(Issue(RULE_CROSS_SOURCE, f"manifest primary_key must be 'RouteCode'; found {primary_key!r}", True))
    if unique_key != "RouteKey":
        issues.append(Issue(RULE_CROSS_SOURCE, f"manifest unique_surrogate_key must be 'RouteKey'; found {unique_key!r}", True))

    key_minimum = _parse_int(key_range.get("minimum")) if key_range else None
    key_maximum = _parse_int(key_range.get("maximum")) if key_range else None
    if key_minimum is None or key_maximum is None:
        issues.append(Issue(RULE_REQUIRED, "manifest key_range minimum and maximum are required positive integers", True))
    elif key_minimum > key_maximum:
        issues.append(Issue(RULE_TYPE, "manifest key_range minimum is greater than maximum", True))

    csv_path = _text(csv_info.get("path"))
    csv_sha = _text(csv_info.get("sha256")).lower()
    if not csv_path:
        issues.append(Issue(RULE_REQUIRED, "manifest files.csv.path is required", True))
    if not re.fullmatch(r"[0-9a-f]{64}", csv_sha):
        issues.append(Issue(RULE_PATTERN, "manifest files.csv.sha256 must be a SHA-256 hex digest", True))
    elif csv_sha != csv_snapshot_sha256.lower():
        issues.append(
            Issue(
                RULE_CROSS_SOURCE,
                "manifest files.csv.sha256 does not match the RAW CSV snapshot",
                True,
            )
        )

    if row_count is not None and row_count != csv_outcome.input_rows:
        issues.append(
            Issue(
                RULE_CROSS_SOURCE,
                f"manifest row_count {row_count} does not match RAW CSV rows {csv_outcome.input_rows}",
                True,
            )
        )

    if not numeric_keys:
        issues.append(Issue(RULE_CROSS_SOURCE, "RAW CSV has no parsable positive RouteKey values", True))
    else:
        if key_minimum is not None and key_minimum != min(numeric_keys):
            issues.append(
                Issue(RULE_CROSS_SOURCE, f"manifest key_range minimum {key_minimum} does not match {min(numeric_keys)}", True)
            )
        if key_maximum is not None and key_maximum != max(numeric_keys):
            issues.append(
                Issue(RULE_CROSS_SOURCE, f"manifest key_range maximum {key_maximum} does not match {max(numeric_keys)}", True)
            )

    baseline_row_count = _parse_int(original_baseline.get("row_count"), positive=True) if original_baseline else None
    expanded_row_count = _parse_int(expanded_source.get("row_count"), positive=True) if expanded_source else None

    normalized = {
        "Dataset": dataset,
        "Project": project,
        "Version": version,
        "Status": status,
        "Disclosure": disclosure,
        "Purpose": purpose,
        "RowCount": row_count if row_count is not None else _text(parsed.get("row_count")),
        "Columns": json.dumps(columns_list, ensure_ascii=False) if columns_list is not None else _text(raw_columns),
        "PrimaryKey": primary_key,
        "UniqueSurrogateKey": unique_key,
        "KeyMinimum": key_minimum if key_minimum is not None else "",
        "KeyMaximum": key_maximum if key_maximum is not None else "",
        "OriginalBaselinePath": _text(original_baseline.get("path")) if original_baseline else "",
        "OriginalBaselineRowCount": baseline_row_count if baseline_row_count is not None else "",
        "OriginalBaselineSha256": _text(original_baseline.get("sha256")).lower() if original_baseline else "",
        "ExpandedSourcePath": _text(expanded_source.get("path")) if expanded_source else "",
        "ExpandedSourceRowCount": expanded_row_count if expanded_row_count is not None else "",
        "ExpandedSourceSha256": _text(expanded_source.get("sha256")).lower() if expanded_source else "",
        "AllocationPolicy": allocation_policy,
        "CsvPath": csv_path,
        "CsvSha256": csv_sha,
        "GeneratedAtUTC": generated_at,
    }

    outcome = _finalize_table(
        table_id="dim_route_keymap_v1_manifest",
        source_id="dim_route_keymap_v1_manifest",
        source_sheet=None,
        original_columns=columns,
        rows=[(normalized, issues)],
        unique_columns=[],
        source_file=source_file,
        ingested_at=ingested_at,
        start_row=1,
    )
    outcome.errors = [issue.message for issue in issues if issue.fatal]
    if parse_error:
        outcome.errors.append(parse_error)
    return outcome

def _stage_crosswalk(snapshot_path, source_file, ingested_at):
    headers, raw_rows = _read_csv_table(snapshot_path, "airline_id_crosswalk")
    rows = []

    for _row_number, row in raw_rows:
        values, issues = _map_row(headers, row)
        normalized = dict(values)

        name = _clean_ws(values.get("AirlineName"))
        if not name:
            issues.append(Issue(RULE_REQUIRED, "AirlineName is required", True))

        source_airline_id = _upper(values.get("SourceAirlineId"))
        dim_airline_id = _upper(values.get("DimAirlineId"))
        source_key = _upper(values.get("SourceAirlineKey"))
        mapping_status = _upper(values.get("MappingStatus"))

        if not source_airline_id:
            issues.append(Issue(RULE_REQUIRED, "SourceAirlineId is required", True))
        elif not re.fullmatch(r"AIR\d{3}", source_airline_id):
            issues.append(Issue(RULE_PATTERN, f"SourceAirlineId must match 'AIR999'; raw={values.get('SourceAirlineId')!r}", True))

        if not dim_airline_id:
            issues.append(Issue(RULE_REQUIRED, "DimAirlineId is required", True))
        elif not re.fullmatch(r"AIR-\d{4}", dim_airline_id):
            issues.append(Issue(RULE_PATTERN, f"DimAirlineId must match 'AIR-9999'; raw={values.get('DimAirlineId')!r}", True))

        if not source_key:
            issues.append(Issue(RULE_REQUIRED, "SourceAirlineKey is required", True))
        elif not re.fullmatch(r"A360-AIR-\d{3}", source_key):
            issues.append(Issue(RULE_PATTERN, f"SourceAirlineKey must match 'A360-AIR-999'; raw={values.get('SourceAirlineKey')!r}", True))

        dim_airline_key = _required_positive_int(values, issues, "DimAirlineKey")
        airline_id_matches = _required_bool(values, issues, "AirlineIdMatches")

        if not mapping_status:
            issues.append(Issue(RULE_REQUIRED, "MappingStatus is required", True))
        else:
            known_statuses = {
                "PROVISIONAL_REQUIRES_OWNER_REVIEW",
                "VERIFIED",
                "UNVERIFIED",
                "CONFLICTED",
                "SUPERSEDED",
            }
            if mapping_status not in known_statuses:
                issues.append(
                    Issue(RULE_UNSUPPORTED, f"Unrecognized MappingStatus {mapping_status!r}; requires owner review", False)
                )
            if mapping_status == "PROVISIONAL_REQUIRES_OWNER_REVIEW":
                issues.append(
                    Issue(RULE_PROVISIONAL, "Crosswalk mapping is provisional and requires owner review", False)
                )

        if airline_id_matches is False:
            issues.append(
                Issue(RULE_PROVISIONAL, "AirlineIdMatches is false; mapping must not be consumed as approved", False)
            )

        normalized.update(
            {
                "AirlineName": name,
                "SourceAirlineId": source_airline_id,
                "DimAirlineId": dim_airline_id,
                "SourceAirlineKey": source_key,
                "DimAirlineKey": dim_airline_key,
                "AirlineIdMatches": airline_id_matches,
                "MappingStatus": mapping_status,
            }
        )
        rows.append((normalized, issues))

    return _finalize_table(
        table_id="airline_id_crosswalk",
        source_id="airline_id_crosswalk",
        source_sheet=None,
        original_columns=headers,
        rows=rows,
        unique_columns=["SourceAirlineId", "DimAirlineId", "SourceAirlineKey", "DimAirlineKey"],
        source_file=source_file,
        ingested_at=ingested_at,
    )


def _stage_airlines(headers, raw_rows, source_file, source_sheet, ingested_at):
    rows = []

    for _row_number, row in raw_rows:
        values, issues = _map_row(headers, row)
        normalized = dict(values)

        airline_name = _clean_ws(values.get("AirlineName"))
        if not airline_name:
            issues.append(Issue(RULE_REQUIRED, "AirlineName is required", True))

        airline_id = _upper(values.get("AirlineId"))
        airline_key = _upper(values.get("AirlineKey"))
        iata_code = _upper(values.get("IATA_Code"))
        iata_airline_code = _text(values.get("IATA_AirlineCode"))
        icao_code = _upper(values.get("ICAO_Code"))
        country_iso2 = _upper(values.get("CountryISO2"))
        country_name = _clean_ws(values.get("CountryName"))
        verification_status = _upper(values.get("IdentityVerificationStatus"))
        roster_origin = _upper(values.get("RosterOrigin"))
        reference_version = _clean_ws(values.get("ReferenceVersion"))

        if not airline_id:
            issues.append(Issue(RULE_REQUIRED, "AirlineId is required", True))
        elif not re.fullmatch(r"AIR\d{3}", airline_id):
            issues.append(Issue(RULE_PATTERN, f"AirlineId must match 'AIR999'; raw={values.get('AirlineId')!r}", True))

        if not airline_key:
            issues.append(Issue(RULE_REQUIRED, "AirlineKey is required", True))
        elif not re.fullmatch(r"A360-AIR-\d{3}", airline_key):
            issues.append(Issue(RULE_PATTERN, f"AirlineKey must match 'A360-AIR-999'; raw={values.get('AirlineKey')!r}", True))

        if not iata_code:
            issues.append(Issue(RULE_REQUIRED, "IATA_Code is required", True))
        elif not re.fullmatch(r"[A-Z0-9]{2}", iata_code):
            issues.append(Issue(RULE_PATTERN, f"IATA_Code must be two letters/digits; raw={values.get('IATA_Code')!r}", True))

        if not iata_airline_code:
            issues.append(Issue(RULE_REQUIRED, "IATA_AirlineCode is required", True))
        elif not re.fullmatch(r"\d{3}", iata_airline_code):
            issues.append(Issue(RULE_PATTERN, f"IATA_AirlineCode must be exactly three digits; raw={values.get('IATA_AirlineCode')!r}", True))

        if not icao_code:
            issues.append(Issue(RULE_REQUIRED, "ICAO_Code is required", True))
        elif not re.fullmatch(r"[A-Z]{3}", icao_code):
            issues.append(Issue(RULE_PATTERN, f"ICAO_Code must be three letters; raw={values.get('ICAO_Code')!r}", True))

        if not country_iso2:
            issues.append(Issue(RULE_REQUIRED, "CountryISO2 is required", True))
        elif not re.fullmatch(r"[A-Z]{2}", country_iso2):
            issues.append(Issue(RULE_PATTERN, f"CountryISO2 must be two letters; raw={values.get('CountryISO2')!r}", True))

        if not country_name:
            issues.append(Issue(RULE_REQUIRED, "CountryName is required", True))

        if not verification_status:
            issues.append(Issue(RULE_REQUIRED, "IdentityVerificationStatus is required", True))
        elif verification_status not in {
            "VERIFIED",
            "PARTIALLY_VERIFIED",
            "UNVERIFIED",
            "CONFLICTING",
            "SUPERSEDED",
        }:
            issues.append(
                Issue(RULE_UNSUPPORTED, f"Unrecognized IdentityVerificationStatus {verification_status!r}", False)
            )

        if not roster_origin:
            issues.append(Issue(RULE_REQUIRED, "RosterOrigin is required", True))

        if not reference_version:
            issues.append(Issue(RULE_REQUIRED, "ReferenceVersion is required", True))

        legal_name = _clean_ws(values.get("LegalName"))
        airline_group = _clean_ws(values.get("AirlineGroup"))
        business_model = _clean_ws(values.get("BusinessModelClass"))
        is_active = _optional_bool(values, issues, "IsActive")
        status_effective = _optional_date(values, issues, "StatusEffectiveDate")

        _flag_blank(values, issues, "LegalName", "Optional LegalName is blank; do not infer or invent one")
        _reject_populated(values, issues, "BusinessModelClass", "BusinessModelClass must remain blank until an approved rubric exists")
        _flag_populated(values, issues, "AirlineGroup", "AirlineGroup populated; requires verified source evidence and effective date")

        normalized.update(
            {
                "AirlineId": airline_id,
                "AirlineKey": airline_key,
                "AirlineName": airline_name,
                "LegalName": legal_name,
                "IATA_Code": iata_code,
                "IATA_AirlineCode": iata_airline_code,
                "ICAO_Code": icao_code,
                "CountryISO2": country_iso2,
                "CountryName": country_name,
                "BusinessModelClass": business_model,
                "AirlineGroup": airline_group,
                "IsActive": is_active,
                "StatusEffectiveDate": status_effective,
                "IdentityVerificationStatus": verification_status,
                "RosterOrigin": roster_origin,
                "ReferenceVersion": reference_version,
                "Notes": _clean_ws(values.get("Notes", "")),
            }
        )
        rows.append((normalized, issues))

    return _finalize_table(
        table_id="airline_reference_airlines",
        source_id="airline_reference_workbook",
        source_sheet=source_sheet,
        original_columns=headers,
        rows=rows,
        unique_columns=["AirlineId", "IATA_Code", "ICAO_Code"],
        source_file=source_file,
        ingested_at=ingested_at,
    )


def _stage_source_register(headers, raw_rows, source_file, source_sheet, ingested_at):
    rows = []

    for _row_number, row in raw_rows:
        values, issues = _map_row(headers, row)
        normalized = dict(values)

        record_id = _upper(values.get("SourceRecordId"))
        airline_id = _upper(values.get("AirlineId"))
        attribute_name = _clean_ws(values.get("AttributeName"))
        publisher = _clean_ws(values.get("SourcePublisher"))
        title = _clean_ws(values.get("SourceTitle"))
        url = _text(values.get("SourceURL"))
        accessed_date = _required_date(values, issues, "AccessedDate")
        verification_status = _upper(values.get("VerificationStatus"))
        evidence_notes = _clean_ws(values.get("EvidenceNotes"))

        if not record_id:
            issues.append(Issue(RULE_REQUIRED, "SourceRecordId is required", True))
        elif not re.fullmatch(r"SRC-\d{4}", record_id):
            issues.append(Issue(RULE_PATTERN, f"SourceRecordId must match 'SRC-9999'; raw={values.get('SourceRecordId')!r}", True))

        if not airline_id:
            issues.append(Issue(RULE_REQUIRED, "AirlineId is required", True))
        elif not re.fullmatch(r"AIR\d{3}", airline_id):
            issues.append(Issue(RULE_PATTERN, f"AirlineId must match 'AIR999'; raw={values.get('AirlineId')!r}", True))

        if not attribute_name:
            issues.append(Issue(RULE_REQUIRED, "AttributeName is required", True))
        if not publisher:
            issues.append(Issue(RULE_REQUIRED, "SourcePublisher is required", True))
        if not title:
            issues.append(Issue(RULE_REQUIRED, "SourceTitle is required", True))

        if not url:
            issues.append(Issue(RULE_REQUIRED, "SourceURL is required", True))
        else:
            url_issue = _validate_url(url)
            if url_issue:
                issues.append(url_issue)

        if not verification_status:
            issues.append(Issue(RULE_REQUIRED, "VerificationStatus is required", True))
        elif verification_status not in {
            "VERIFIED",
            "UNVERIFIED",
            "CONFLICTING",
            "NOT_AVAILABLE",
            "PENDING",
            "REJECTED",
        }:
            issues.append(Issue(RULE_UNSUPPORTED, f"Unrecognized VerificationStatus {verification_status!r}", False))

        if not evidence_notes:
            issues.append(Issue(RULE_REQUIRED, "EvidenceNotes is required", True))

        normalized.update(
            {
                "SourceRecordId": record_id,
                "AirlineId": airline_id,
                "AttributeName": attribute_name,
                "SourcePublisher": publisher,
                "SourceTitle": title,
                "SourceURL": url,
                "AccessedDate": accessed_date,
                "VerificationStatus": verification_status,
                "EvidenceNotes": evidence_notes,
            }
        )
        rows.append((normalized, issues))

    return _finalize_table(
        table_id="airline_reference_source_register",
        source_id="airline_reference_workbook",
        source_sheet=source_sheet,
        original_columns=headers,
        rows=rows,
        unique_columns=["SourceRecordId"],
        source_file=source_file,
        ingested_at=ingested_at,
    )


def _stage_readme(headers, raw_rows, source_file, source_sheet, ingested_at):
    rows = []

    for _row_number, row in raw_rows:
        values, issues = _map_row(headers, row)
        normalized = dict(values)

        topic = _clean_ws(values.get("Topic"))
        definition = _clean_ws(values.get("Definition", ""))

        if not topic and not definition:
            issues.append(Issue(RULE_EMPTY_ROW, "Blank source row", True))
        else:
            if not topic:
                issues.append(Issue(RULE_REQUIRED, "Topic is required", True))
            if not definition:
                issues.append(
                    Issue(RULE_OPTIONAL_TEXT, "Definition is blank; treating as a section heading or incomplete note", False)
                )

        normalized.update({"Topic": topic, "Definition": definition})
        rows.append((normalized, issues))

    return _finalize_table(
        table_id="airline_reference_readme",
        source_id="airline_reference_workbook",
        source_sheet=source_sheet,
        original_columns=headers,
        rows=rows,
        unique_columns=[],
        source_file=source_file,
        ingested_at=ingested_at,
    )


def _stage_change_log(headers, raw_rows, source_file, source_sheet, ingested_at):
    rows = []

    for _row_number, row in raw_rows:
        values, issues = _map_row(headers, row)
        normalized = dict(values)

        change_id = _upper(values.get("ChangeId"))
        changed_date = _required_date(values, issues, "Date")
        reference_version = _clean_ws(values.get("ReferenceVersion"))
        change_description = _clean_ws(values.get("ChangeDescription"))
        changed_by = _clean_ws(values.get("ChangedBy"))
        evidence = _clean_ws(values.get("Evidence"))

        if not change_id:
            issues.append(Issue(RULE_REQUIRED, "ChangeId is required", True))
        elif not re.fullmatch(r"CHG-\d{4}", change_id):
            issues.append(Issue(RULE_PATTERN, f"ChangeId must match 'CHG-9999'; raw={values.get('ChangeId')!r}", True))

        if not reference_version:
            issues.append(Issue(RULE_REQUIRED, "ReferenceVersion is required", True))
        if not change_description:
            issues.append(Issue(RULE_REQUIRED, "ChangeDescription is required", True))
        if not changed_by:
            issues.append(Issue(RULE_REQUIRED, "ChangedBy is required", True))
        if not evidence:
            issues.append(Issue(RULE_REQUIRED, "Evidence is required", True))

        normalized.update(
            {
                "ChangeId": change_id,
                "Date": changed_date,
                "ReferenceVersion": reference_version,
                "ChangeDescription": change_description,
                "ChangedBy": changed_by,
                "Evidence": evidence,
            }
        )
        rows.append((normalized, issues))

    return _finalize_table(
        table_id="airline_reference_change_log",
        source_id="airline_reference_workbook",
        source_sheet=source_sheet,
        original_columns=headers,
        rows=rows,
        unique_columns=["ChangeId"],
        source_file=source_file,
        ingested_at=ingested_at,
    )


def _stage_dim_airline(headers, raw_rows, source_file, source_sheet, ingested_at):
    rows = []

    for _row_number, row in raw_rows:
        values, issues = _map_row(headers, row)
        normalized = dict(values)

        airline_key = _required_positive_int(values, issues, "AirlineKey")
        airline_id = _upper(values.get("AirlineId"))
        iata_code = _upper(values.get("AirlineIATACode"))
        icao_code = _upper(values.get("AirlineICAOCode"))
        airline_name = _clean_ws(values.get("AirlineName"))
        home_country = _clean_ws(values.get("HomeCountry"))
        home_country_code = _upper(values.get("HomeCountryCode"))
        business_model = _clean_ws(values.get("BusinessModelClass"))
        airline_group = _clean_ws(values.get("AirlineGroup"))
        is_active = _required_bool(values, issues, "IsActive")
        status_effective = _optional_date(values, issues, "StatusEffectiveDate")
        reference_version = _clean_ws(values.get("ReferenceVersion"))

        if not airline_id:
            issues.append(Issue(RULE_REQUIRED, "AirlineId is required", True))
        elif not re.fullmatch(r"AIR-\d{4}", airline_id):
            issues.append(Issue(RULE_PATTERN, f"AirlineId must match 'AIR-9999'; raw={values.get('AirlineId')!r}", True))

        if not iata_code:
            issues.append(Issue(RULE_REQUIRED, "AirlineIATACode is required", True))
        elif not re.fullmatch(r"[A-Z0-9]{2}", iata_code):
            issues.append(Issue(RULE_PATTERN, f"AirlineIATACode must be two letters/digits; raw={values.get('AirlineIATACode')!r}", True))

        if not icao_code:
            issues.append(Issue(RULE_REQUIRED, "AirlineICAOCode is required", True))
        elif not re.fullmatch(r"[A-Z]{3}", icao_code):
            issues.append(Issue(RULE_PATTERN, f"AirlineICAOCode must be three letters; raw={values.get('AirlineICAOCode')!r}", True))

        if not airline_name:
            issues.append(Issue(RULE_REQUIRED, "AirlineName is required", True))
        if not home_country:
            issues.append(Issue(RULE_REQUIRED, "HomeCountry is required", True))

        if not home_country_code:
            issues.append(Issue(RULE_REQUIRED, "HomeCountryCode is required", True))
        elif not re.fullmatch(r"[A-Z]{2}", home_country_code):
            issues.append(Issue(RULE_PATTERN, f"HomeCountryCode must be two letters; raw={values.get('HomeCountryCode')!r}", True))

        if not reference_version:
            issues.append(Issue(RULE_REQUIRED, "ReferenceVersion is required", True))

        _reject_populated(values, issues, "BusinessModelClass", "BusinessModelClass must remain blank until an approved rubric exists")
        _flag_populated(values, issues, "AirlineGroup", "AirlineGroup populated; requires verified source evidence and effective date")

        normalized.update(
            {
                "AirlineKey": airline_key,
                "AirlineId": airline_id,
                "AirlineIATACode": iata_code,
                "AirlineICAOCode": icao_code,
                "AirlineName": airline_name,
                "AirlineGroup": airline_group,
                "HomeCountry": home_country,
                "HomeCountryCode": home_country_code,
                "BusinessModelClass": business_model,
                "IsActive": is_active,
                "StatusEffectiveDate": status_effective,
                "ReferenceVersion": reference_version,
            }
        )
        rows.append((normalized, issues))

    return _finalize_table(
        table_id="airline_reference_dim_airline",
        source_id="airline_reference_workbook",
        source_sheet=source_sheet,
        original_columns=headers,
        rows=rows,
        unique_columns=["AirlineKey", "AirlineId", "AirlineIATACode", "AirlineICAOCode"],
        source_file=source_file,
        ingested_at=ingested_at,
    )


def _stage_workbook(snapshot_path, source_file, ingested_at):
    sheets = _read_workbook_headers(snapshot_path)
    outcomes = []

    for sheet, table_id in WORKBOOK_SHEETS.items():
        headers, raw_rows = sheets[sheet]
        if table_id == "airline_reference_airlines":
            outcomes.append(_stage_airlines(headers, raw_rows, source_file, sheet, ingested_at))
        elif table_id == "airline_reference_source_register":
            outcomes.append(_stage_source_register(headers, raw_rows, source_file, sheet, ingested_at))
        elif table_id == "airline_reference_readme":
            outcomes.append(_stage_readme(headers, raw_rows, source_file, sheet, ingested_at))
        elif table_id == "airline_reference_change_log":
            outcomes.append(_stage_change_log(headers, raw_rows, source_file, sheet, ingested_at))
        elif table_id == "airline_reference_dim_airline":
            outcomes.append(_stage_dim_airline(headers, raw_rows, source_file, sheet, ingested_at))
        else:
            raise StagingSchemaError(f"Unsupported workbook table mapping: {table_id}")

    return outcomes


def _airline_number(value):
    match = re.search(r"\d+", _text(value))
    return int(match.group(0)) if match else None


def _check_roster_consistency(outcomes_by_id):
    errors = []

    crosswalk = outcomes_by_id["airline_id_crosswalk"].accepted_records
    airlines = outcomes_by_id["airline_reference_airlines"].accepted_records
    dim_airline = outcomes_by_id["airline_reference_dim_airline"].accepted_records

    sets = []
    for name, records, column in [
        ("airline_id_crosswalk", crosswalk, "SourceAirlineId"),
        ("airline_reference_airlines", airlines, "AirlineId"),
        ("airline_reference_dim_airline", dim_airline, "AirlineId"),
    ]:
        numbers = {_airline_number(record.get(column)) for record in records}
        numbers.discard(None)
        sets.append((name, numbers))
        if len(numbers) != EXPECTED_AIRLINE_COUNT:
            errors.append(
                f"{name} accepted rows cover {len(numbers)} airline identities; expected {EXPECTED_AIRLINE_COUNT}"
            )

    if sets:
        reference = sets[0][1]
        for name, numbers in sets[1:]:
            missing = sorted(reference - numbers)
            extra = sorted(numbers - reference)
            if missing or extra:
                errors.append(
                    f"{name} airline identity set does not match airline_id_crosswalk; missing={missing}, extra={extra}"
                )

    for record in crosswalk:
        number = _airline_number(record.get("SourceAirlineId"))
        if number is None:
            continue
        expected_key = f"A360-AIR-{number:03d}"
        if _upper(record.get("SourceAirlineKey")) != expected_key:
            errors.append(
                f"airline_id_crosswalk {record.get('SourceAirlineId')} SourceAirlineKey must be {expected_key}; found {record.get('SourceAirlineKey')!r}"
            )
        if record.get("DimAirlineKey") != number:
            errors.append(
                f"airline_id_crosswalk {record.get('SourceAirlineId')} DimAirlineKey must be {number}; found {record.get('DimAirlineKey')!r}"
            )
        expected_dim_id = f"AIR-{number:04d}"
        if _upper(record.get("DimAirlineId")) != expected_dim_id:
            errors.append(
                f"airline_id_crosswalk {record.get('SourceAirlineId')} DimAirlineId must be {expected_dim_id}; found {record.get('DimAirlineId')!r}"
            )

    for record in airlines:
        number = _airline_number(record.get("AirlineId"))
        if number is None:
            continue
        expected_key = f"A360-AIR-{number:03d}"
        if _upper(record.get("AirlineKey")) != expected_key:
            errors.append(
                f"airline_reference_airlines {record.get('AirlineId')} AirlineKey must be {expected_key}; found {record.get('AirlineKey')!r}"
            )

    for record in dim_airline:
        number = _airline_number(record.get("AirlineId"))
        if number is None:
            continue
        expected_id = f"AIR-{number:04d}"
        if _upper(record.get("AirlineId")) != expected_id:
            errors.append(
                f"airline_reference_dim_airline AirlineId must be {expected_id}; found {record.get('AirlineId')!r}"
            )
        if record.get("AirlineKey") != number:
            errors.append(
                f"airline_reference_dim_airline {record.get('AirlineId')} AirlineKey must be {number}; found {record.get('AirlineKey')!r}"
            )

    return errors

def _jsonable_record(record):
    return {key: _jsonable(value) for key, value in record.items()}


def _string_value(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (date, datetime)):
        return _text(value)
    return str(value).strip()


def _output_relative(run_id, filename):
    return f"data/02_staging/{run_id}/{filename}"


def _dtype_columns(table_id, columns):
    int_by_table = {
        "dim_route_keymap_v1": {"RouteKey"},
        "airline_id_crosswalk": {"DimAirlineKey"},
        "airline_reference_dim_airline": {"AirlineKey"},
        "dim_route_keymap_v1_manifest": {
            "RowCount",
            "KeyMinimum",
            "KeyMaximum",
            "OriginalBaselineRowCount",
            "ExpandedSourceRowCount",
        },
    }
    boolean_by_table = {
        "airline_id_crosswalk": {"AirlineIdMatches"},
        "airline_reference_airlines": {"IsActive"},
        "airline_reference_dim_airline": {"IsActive"},
    }

    integer = (int_by_table.get(table_id, set()) | {"SourceRowNumber"}) & set(columns)
    boolean = boolean_by_table.get(table_id, set()) & set(columns)
    return integer, boolean


def _frame_for_records(records, columns, table_id, accepted):
    frame = pd.DataFrame(list(records), columns=columns)
    integer_columns, boolean_columns = _dtype_columns(table_id, columns)

    if accepted:
        for column in columns:
            if column in integer_columns:
                values = []
                for value in frame[column]:
                    if value is None or _text(value) == "":
                        values.append(pd.NA)
                    else:
                        try:
                            values.append(int(value))
                        except (TypeError, ValueError) as exc:
                            raise StagingError(
                                f"Accepted {table_id}.{column} is not an integer: {value!r}"
                            ) from exc
                frame[column] = pd.Series(values, dtype="Int64")
            elif column in boolean_columns:
                values = []
                for value in frame[column]:
                    if value is None or _text(value) == "":
                        values.append(pd.NA)
                    elif isinstance(value, bool):
                        values.append(value)
                    else:
                        parsed = _parse_bool(value)
                        if parsed is None:
                            raise StagingError(
                                f"Accepted {table_id}.{column} is not a boolean: {value!r}"
                            )
                        values.append(parsed)
                frame[column] = pd.Series(values, dtype="boolean")
            else:
                frame[column] = frame[column].map(
                    lambda value: None if value is None else _string_value(value)
                ).astype("string")
        return frame

    return frame.map(lambda value: _string_value(value)).astype("string")


def _atomic_write_frame(frame, path, kind):
    if path.exists():
        raise StagingError(f"Refusing to overwrite existing STAGING output: {path}")

    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=path.suffix,
        dir=path.parent,
    )
    os.close(file_descriptor)
    temporary_path = Path(temporary_name)

    try:
        if kind == "csv":
            frame.to_csv(
                temporary_path,
                index=False,
                encoding="utf-8",
                lineterminator="\n",
            )
        elif kind == "parquet":
            frame.to_parquet(temporary_path, index=False, engine="pyarrow")
        else:
            raise StagingError(f"Unsupported output kind: {kind}")

        if temporary_path.stat().st_size == 0 and kind == "parquet":
            raise StagingError(f"Parquet writer produced an empty file: {temporary_path}")

        temporary_path.rename(path)
        return path
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _output_info(path, relative_path, row_count):
    return {
        "path": relative_path,
        "sha256": sha256_file(path),
        "size": path.stat().st_size,
        "row_count": row_count,
    }


def _write_outcome_outputs(outcome, output_dir, run_id):
    columns = outcome.columns
    accepted_frame = _frame_for_records(
        outcome.accepted_records,
        columns,
        outcome.table_id,
        accepted=True,
    )
    quarantine_frame = _frame_for_records(
        outcome.quarantine_records,
        columns,
        outcome.table_id,
        accepted=False,
    )

    accepted_csv = output_dir / f"stg_{outcome.table_id}.csv"
    accepted_parquet = output_dir / f"stg_{outcome.table_id}.parquet"
    quarantine_csv = output_dir / f"quarantine_{outcome.table_id}.csv"
    quarantine_parquet = output_dir / f"quarantine_{outcome.table_id}.parquet"

    _atomic_write_frame(accepted_frame, accepted_csv, "csv")
    _atomic_write_frame(accepted_frame, accepted_parquet, "parquet")
    _atomic_write_frame(quarantine_frame, quarantine_csv, "csv")
    _atomic_write_frame(quarantine_frame, quarantine_parquet, "parquet")

    outputs = {
        "accepted": {
            "csv": _output_info(
                accepted_csv,
                _output_relative(run_id, accepted_csv.name),
                len(outcome.accepted_records),
            ),
            "parquet": _output_info(
                accepted_parquet,
                _output_relative(run_id, accepted_parquet.name),
                len(outcome.accepted_records),
            ),
        },
        "quarantine": {
            "csv": _output_info(
                quarantine_csv,
                _output_relative(run_id, quarantine_csv.name),
                len(outcome.quarantine_records),
            ),
            "parquet": _output_info(
                quarantine_parquet,
                _output_relative(run_id, quarantine_parquet.name),
                len(outcome.quarantine_records),
            ),
        },
    }

    return TableResult(
        table_id=outcome.table_id,
        source_id=outcome.source_id,
        source_sheet=outcome.source_sheet,
        input_rows=outcome.input_rows,
        accepted_count=outcome.accepted_count,
        rejected_count=outcome.rejected_count,
        flagged_count=outcome.flagged_count,
        outputs=outputs,
        errors=outcome.errors,
    )


def _write_rejections_index(outcomes, output_dir, run_id):
    columns = [
        "Table",
        "SourceFile",
        "SourceSheet",
        "SourceRowNumber",
        "QualityRuleID",
        "DispositionReason",
        "RecordJson",
    ]
    rows = []

    for outcome in outcomes:
        for record in outcome.quarantine_records:
            rows.append(
                {
                    "Table": outcome.table_id,
                    "SourceFile": record.get("SourceFile", ""),
                    "SourceSheet": record.get("SourceSheet", ""),
                    "SourceRowNumber": str(record.get("SourceRowNumber", "")),
                    "QualityRuleID": record.get("QualityRuleID", ""),
                    "DispositionReason": record.get("DispositionReason", ""),
                    "RecordJson": json.dumps(
                        _jsonable_record(record),
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                }
            )

    frame = pd.DataFrame(rows, columns=columns).astype("string")
    path = output_dir / "staging_rejections.csv"
    _atomic_write_frame(frame, path, "csv")
    return _output_info(path, _output_relative(run_id, path.name), len(rows))


def _table_result_dict(table):
    return {
        "table_id": table.table_id,
        "source_id": table.source_id,
        "source_sheet": table.source_sheet,
        "input_rows": table.input_rows,
        "accepted_count": table.accepted_count,
        "rejected_count": table.rejected_count,
        "flagged_count": table.flagged_count,
        "outputs": table.outputs,
        "errors": table.errors,
    }


def _write_staging_manifest(run, output_dir, snapshots, rejection_info):
    manifest = {
        "schema_version": STAGING_SCHEMA_VERSION,
        "tool": STAGING_TOOL,
        "tool_version": STAGING_TOOL_VERSION,
        "run_id": run.run_id,
        "run_timestamp": run.run_timestamp,
        "raw_run_id": run.raw_run_id,
        "raw_manifest_path": run.raw_manifest_path,
        "staging_layer": "data/02_staging",
        "status": run.status,
        "quality_status": run.quality_status,
        "summary": {
            "tables": len(run.tables),
            "input_rows": run.total_input_rows,
            "accepted_rows": run.total_accepted_rows,
            "rejected_rows": run.total_rejected_rows,
            "flagged_rows": run.total_flagged_rows,
        },
        "source_snapshots": snapshots,
        "tables": [_table_result_dict(table) for table in run.tables],
        "rejections_index": rejection_info,
        "errors": run.errors,
        "warnings": run.warnings,
    }
    write_json_atomic(output_dir / "staging_manifest.json", manifest)


class StagingManager:
    """Build rebuildable STAGING outputs from the latest completed RAW run."""

    def __init__(self, raw_run_id=None, staging_run_id=None):
        self.raw_run_id = raw_run_id
        self.run_id = staging_run_id or _run_id()
        self.run_timestamp = _utc_timestamp()
        self.logger = get_logger(f"aerovision.staging.{self.run_id}")
        self.raw_root = project_path("data", "01_raw")
        self.staging_root = project_path("data", "02_staging")
        self._raw_manifest = None
        self._raw_manifest_path = None
        self._snapshots: dict[str, dict[str, Any]] = {}

    def _resolve_raw_run(self):
        if self.raw_run_id:
            run_dir = self.raw_root / "runs" / self.raw_run_id
            manifest = _raw_manifest_from_directory(run_dir)
            if not manifest:
                raise MissingRawRunError(
                    f"Requested RAW run is missing a valid run_manifest.json: {self.raw_run_id}"
                )
            summary = manifest.get("summary", {})
            total = int(summary.get("total_sources", 0) or 0)
            completed = int(summary.get("completed", 0) or 0)
            failed = int(summary.get("failed", 0) or 0)
            if total == 0 or completed != total or failed != 0:
                raise MissingRawRunError(
                    f"Requested RAW run is not complete and successful: {self.raw_run_id}"
                )
            return run_dir, manifest

        candidates = _completed_raw_candidates(self.raw_root)
        if not candidates:
            raise MissingRawRunError(
                "No completed RAW ingestion run was found under data/01_raw/runs"
            )

        _sort_key, run_dir, manifest = candidates[-1]
        self.raw_run_id = run_dir.name
        return run_dir, manifest

    def _verify_sources(self):
        run_dir, manifest = self._resolve_raw_run()
        self._raw_manifest = manifest
        self._raw_manifest_path = f"data/01_raw/runs/{self.raw_run_id}/run_manifest.json"

        errors = []
        snapshots: dict[str, dict[str, Any]] = {}

        for source_id in (
            "airline_reference_workbook",
            "airline_id_crosswalk",
            "dim_route_keymap_v1",
            "dim_route_keymap_v1_manifest",
        ):
            source = manifest.get("sources", {}).get(source_id)
            if not source:
                errors.append(f"RAW manifest does not contain source {source_id}")
                continue

            snapshot = source.get("snapshot") or {}
            snapshot_value = snapshot.get("path")
            expected_sha = str(snapshot.get("sha256") or source.get("source_sha256") or "").lower()
            expected_size = snapshot.get("size") or source.get("byte_size")

            if not snapshot_value:
                errors.append(f"RAW manifest source {source_id} has no snapshot path")
                continue

            try:
                snapshot_path = _snapshot_relative(self.raw_root, str(snapshot_value))
            except RawSnapshotIntegrityError as exc:
                errors.append(str(exc))
                continue

            if not snapshot_path.exists():
                errors.append(f"RAW snapshot does not exist: {snapshot_path}")
                continue

            actual_sha = sha256_file(snapshot_path).lower()
            actual_size = snapshot_path.stat().st_size

            if expected_sha and actual_sha != expected_sha:
                errors.append(
                    f"RAW snapshot hash mismatch for {source_id}: expected {expected_sha}, found {actual_sha}"
                )
            if expected_size is not None and int(expected_size) != actual_size:
                errors.append(
                    f"RAW snapshot size mismatch for {source_id}: expected {expected_size}, found {actual_size}"
                )

            source_file = f"data/01_raw/{snapshot_path.relative_to(self.raw_root.resolve()).as_posix()}"
            snapshots[source_id] = {
                "path": source_file,
                "sha256": actual_sha,
                "size": actual_size,
                "verified": not errors,
            }

        if errors:
            raise RawSnapshotIntegrityError("; ".join(errors))

        self._snapshots = snapshots

    def _preflight_sources(self):
        _read_csv_table(self._snapshot_path("dim_route_keymap_v1"), "dim_route_keymap_v1")
        _read_csv_table(self._snapshot_path("airline_id_crosswalk"), "airline_id_crosswalk")
        _read_workbook_headers(self._snapshot_path("airline_reference_workbook"))

    def _snapshot_path(self, source_id):
        relative = self._snapshots[source_id]["path"].split("data/01_raw/", 1)[1]
        return self.raw_root / Path(*relative.split("/"))

    def _create_output_dir(self):
        output_dir = self.staging_root / self.run_id
        if output_dir.exists():
            raise StagingError(f"STAGING run output already exists: {output_dir}")
        output_dir.mkdir(parents=True)
        return output_dir

    def stage_all(self):
        self._verify_sources()
        self._preflight_sources()

        output_dir = self._create_output_dir()
        ingested_at = _utc_timestamp()
        errors: list[str] = []
        warnings: list[str] = []
        outcomes: list[TableOutcome] = []

        route_csv, numeric_keys = _stage_route_csv(
            self._snapshot_path("dim_route_keymap_v1"),
            self._snapshots["dim_route_keymap_v1"]["path"],
            ingested_at,
        )
        outcomes.append(route_csv)
        if route_csv.rejected_count:
            warnings.append(
                f"dim_route_keymap_v1 has {route_csv.rejected_count} rejected row(s); reference is not publishable until CURATED quality gates pass"
            )

        route_manifest = _stage_route_manifest(
            self._snapshot_path("dim_route_keymap_v1_manifest"),
            self._snapshots["dim_route_keymap_v1_manifest"]["path"],
            ingested_at,
            route_csv,
            self._snapshots["dim_route_keymap_v1"]["sha256"],
            numeric_keys,
        )
        outcomes.append(route_manifest)
        errors.extend(route_manifest.errors)

        crosswalk = _stage_crosswalk(
            self._snapshot_path("airline_id_crosswalk"),
            self._snapshots["airline_id_crosswalk"]["path"],
            ingested_at,
        )
        outcomes.append(crosswalk)

        workbook_outcomes = _stage_workbook(
            self._snapshot_path("airline_reference_workbook"),
            self._snapshots["airline_reference_workbook"]["path"],
            ingested_at,
        )
        outcomes.extend(workbook_outcomes)

        outcomes_by_id = {outcome.table_id: outcome for outcome in outcomes}
        errors.extend(_check_roster_consistency(outcomes_by_id))

        table_results = []
        for outcome in outcomes:
            table_results.append(_write_outcome_outputs(outcome, output_dir, self.run_id))

        rejection_info = _write_rejections_index(outcomes, output_dir, self.run_id)

        total_input = sum(table.input_rows for table in table_results)
        total_accepted = sum(table.accepted_count for table in table_results)
        total_rejected = sum(table.rejected_count for table in table_results)
        total_flagged = sum(table.flagged_count for table in table_results)

        status = "failed" if errors else "completed"
        quality_status = (
            "FAILED"
            if errors
            else "QUARANTINE_REQUIRED"
            if total_rejected
            else "FLAGGED"
            if total_flagged
            else "PASS"
        )

        run = StagingRun(
            run_id=self.run_id,
            run_timestamp=self.run_timestamp,
            raw_run_id=str(self.raw_run_id),
            raw_manifest_path=str(self._raw_manifest_path),
            output_dir=str(output_dir),
            status=status,
            quality_status=quality_status,
            tables=table_results,
            errors=errors,
            warnings=warnings,
        )

        _write_staging_manifest(run, output_dir, self._snapshots, rejection_info)
        return run


def create_staging_manager(raw_run_id=None, staging_run_id=None):
    """Create a STAGING manager bound to a RAW run and output run ID."""
    return StagingManager(raw_run_id=raw_run_id, staging_run_id=staging_run_id)


