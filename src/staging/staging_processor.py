"""STAGING data processing module for AEROVISION 360.

Standardizes RAW source snapshots into typed staging records, applies
validation and duplicate detection, and separates accepted records from
rejected records with explicit disposition reasons.

All path resolution uses src.utilities.paths.project_path. File hashing
uses src.utilities.hashing.sha256_file. Atomic JSON writing uses
src.utilities.io.write_json_atomic. Logging uses
src.utilities.logging.get_logger.

RAW is never modified here. STAGING is rebuildable from RAW and REFERENCE
without manual edits, per the data contract.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import openpyxl

from src.ingestion.raw_ingestion import SourceFormat, create_default_source_registry
from src.utilities.hashing import sha256_file
from src.utilities.io import write_json_atomic
from src.utilities.logging import get_logger
from src.utilities.paths import project_path


STAGING_METADATA_COLUMNS: tuple[str, ...] = (
    "SourceFile",
    "SourceRowNumber",
    "IngestedAtUTC",
    "SchemaVersion",
    "QualityStatus",
    "QualityRuleID",
    "Disposition",
    "DispositionReason",
)

DEFAULT_TRANSFORMATION_VERSION = "1.0.0"
DEFAULT_SCHEMA_VERSION = "1.0.0"


class StagingStatus(str, Enum):
    """Status of a staging operation."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class QualityStatus(str, Enum):
    """Quality outcome of a staged record."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DUPLICATE = "duplicate"


class Disposition(str, Enum):
    """Downstream disposition of a staged record."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"


class StagingError(Exception):
    """Base exception for STAGING errors."""

    pass


class StagingIntegrityError(StagingError):
    """Raised when a RAW snapshot fails integrity verification."""

    pass


class StagingFormatError(StagingError):
    """Raised when a source snapshot cannot be parsed."""

    pass


@dataclass(frozen=True)
class SourceStagingPlan:
    """Defines the staging schema and validation rules for one source."""

    source_id: str
    dataset_name: str
    source_format: str
    sheet_name: str | None = None
    column_names: tuple[str, ...] = ()
    required_columns: tuple[str, ...] = ()
    primary_key: str | None = None
    unique_keys: tuple[str, ...] = ()
    type_rules: dict[str, str] = field(default_factory=dict)
    allowed_values: dict[str, tuple[Any, ...]] | None = None


@dataclass(frozen=True)
class StagingSourceContext:
    """RAW provenance and source metadata required for staging."""

    source_id: str
    source_path: str
    source_name: str
    source_format: str
    source_description: str
    source_sha256: str
    raw_run_id: str
    raw_snapshot_path: str


@dataclass
class StagedRecord:
    """A single staged record with quality and disposition outcome."""

    source_id: str
    source_row_number: int
    source_file: str
    source_sha256: str
    raw_run_id: str
    raw_snapshot_path: str
    transformation_version: str
    schema_version: str
    ingested_at_utc: str
    quality_status: QualityStatus
    disposition: Disposition
    quality_rule_id: str | None
    disposition_reason: str | None
    fields: dict[str, Any] = field(default_factory=dict)

    @property
    def is_accepted(self) -> bool:
        return self.quality_status == QualityStatus.ACCEPTED


@dataclass
class StagingResult:
    """Result of staging a single source."""

    source_id: str
    source_format: str
    staging_run_id: str
    status: StagingStatus
    schema: SourceStagingPlan | None = None
    records: list[StagedRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    source_path: str | None = None
    source_name: str | None = None
    source_sha256: str | None = None
    raw_run_id: str | None = None
    raw_snapshot_path: str | None = None
    transformation_version: str | None = None
    dataset_name: str | None = None
    output_path: str | None = None
    output_sha256: str | None = None

    @property
    def accepted_count(self) -> int:
        return sum(
            1 for r in self.records if r.quality_status == QualityStatus.ACCEPTED
        )

    @property
    def rejected_count(self) -> int:
        return sum(
            1 for r in self.records if r.quality_status != QualityStatus.ACCEPTED
        )

    @property
    def duplicate_count(self) -> int:
        return sum(
            1 for r in self.records if r.quality_status == QualityStatus.DUPLICATE
        )

    @property
    def processed_count(self) -> int:
        return len(self.records)


def get_staging_plan(source_id: str) -> SourceStagingPlan | None:
    """Return the registered staging plan for a source, or None."""
    return STAGING_PLANS.get(source_id)


STAGING_PLANS: dict[str, SourceStagingPlan] = {
    "airline_reference_workbook": SourceStagingPlan(
        source_id="airline_reference_workbook",
        dataset_name="DimAirline",
        source_format=SourceFormat.XLSX.value,
        sheet_name="DimAirline",
        column_names=(
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
        ),
        required_columns=("AirlineKey", "AirlineId", "AirlineName"),
        primary_key="AirlineKey",
        unique_keys=("AirlineId",),
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
    ),
    "airline_id_crosswalk": SourceStagingPlan(
        source_id="airline_id_crosswalk",
        dataset_name="DimAirlineCrosswalk",
        source_format=SourceFormat.CSV.value,
        column_names=(
            "AirlineName",
            "SourceAirlineId",
            "DimAirlineId",
            "SourceAirlineKey",
            "DimAirlineKey",
            "AirlineIdMatches",
            "MappingStatus",
        ),
        required_columns=(
            "SourceAirlineId",
            "DimAirlineId",
            "SourceAirlineKey",
            "DimAirlineKey",
            "MappingStatus",
        ),
        primary_key="DimAirlineKey",
        unique_keys=("SourceAirlineId",),
        type_rules={
            "AirlineName": "string",
            "SourceAirlineId": "string",
            "DimAirlineId": "string",
            "SourceAirlineKey": "string",
            "DimAirlineKey": "int",
            "AirlineIdMatches": "boolean",
            "MappingStatus": "string",
        },
    ),
    "dim_route_keymap_v1": SourceStagingPlan(
        source_id="dim_route_keymap_v1",
        dataset_name="DimRouteKeyMap",
        source_format=SourceFormat.CSV.value,
        column_names=("RouteKey", "RouteCode"),
        required_columns=("RouteKey", "RouteCode"),
        primary_key="RouteCode",
        unique_keys=("RouteKey",),
        type_rules={
            "RouteKey": "int",
            "RouteCode": "string",
        },
    ),
    "dim_route_keymap_v1_manifest": SourceStagingPlan(
        source_id="dim_route_keymap_v1_manifest",
        dataset_name="DimRouteKeyMapManifest",
        source_format=SourceFormat.JSON.value,
        column_names=(
            "dataset",
            "version",
            "status",
            "row_count",
            "primary_key",
            "unique_surrogate_key",
            "key_range_min",
            "key_range_max",
            "allocation_policy",
        ),
        required_columns=("dataset", "version", "row_count", "primary_key"),
        primary_key=None,
        unique_keys=("dataset",),
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
        allowed_values={
            "status": ("IMMUTABLE_VERSIONED_REFERENCE",),
        },
    ),
}


def _convert_type(value: Any, type_name: str) -> Any:
    """Convert a raw value to the declared staging type."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        if type_name == "int":
            return int(value)
        if type_name == "number":
            return float(value)
        return value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    text = str(value).strip()
    if text == "":
        return None
    if type_name == "int":
        return int(text)
    if type_name == "number":
        return float(text)
    if type_name == "boolean":
        lowered = text.lower()
        if lowered in {"true", "1", "yes", "y", "t"}:
            return True
        if lowered in {"false", "0", "no", "n", "f"}:
            return False
        raise ValueError(f"Cannot convert {text!r} to boolean.")
    return text


def _read_csv_records(path: Path) -> list[tuple[int, dict[str, Any]]]:
    """Read a CSV snapshot into (row_number, fields) pairs.

    Row numbers are 1-based data row ordinals (header excluded).
    """
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return []
    header = [(cell or "").strip() for cell in rows[0]]
    records: list[tuple[int, dict[str, Any]]] = []
    row_number = 0
    for values in rows[1:]:
        row_number += 1
        if not any(str(cell).strip() for cell in values if cell is not None):
            continue
        raw: dict[str, Any] = {}
        for index, key in enumerate(header):
            raw[key] = values[index] if index < len(values) else None
        records.append((row_number, raw))
    return records


def _read_json_records(path: Path) -> list[tuple[int, dict[str, Any]]]:
    """Read a JSON snapshot into (row_number, fields) pairs."""
    data = json.loads(path.read_text(encoding="utf-8"))
    records: list[tuple[int, dict[str, Any]]] = []
    if isinstance(data, dict):
        records.append((1, data))
    elif isinstance(data, list):
        for index, item in enumerate(data, start=1):
            records.append((index, item if isinstance(item, dict) else {"value": item}))
    return records


def _read_xlsx_records(
    path: Path, sheet_name: str | None
) -> list[tuple[int, dict[str, Any]]]:
    """Read an XLSX snapshot into (row_number, fields) pairs."""
    workbook = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
    sheet = workbook[sheet_name] if sheet_name else workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return []
    header = [str(cell).strip() if cell is not None else "" for cell in rows[0]]
    records: list[tuple[int, dict[str, Any]]] = []
    row_number = 0
    for values in rows[1:]:
        row_number += 1
        if not any(value is not None and str(value).strip() != "" for value in values):
            continue
        raw: dict[str, Any] = {}
        for index, key in enumerate(header):
            value = values[index] if index < len(values) else None
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            elif isinstance(value, float) and value.is_integer():
                value = int(value)
            raw[key] = value
        records.append((row_number, raw))
    return records


def read_source_records(
    plan: SourceStagingPlan, path: Path
) -> list[tuple[int, dict[str, Any]]]:
    """Read raw records from a snapshot according to the staging plan."""
    source_format = (plan.source_format or "").lower()
    if source_format == SourceFormat.CSV.value:
        return _read_csv_records(path)
    if source_format == SourceFormat.JSON.value:
        return _read_json_records(path)
    if source_format == SourceFormat.XLSX.value:
        return _read_xlsx_records(path, plan.sheet_name)
    raise StagingFormatError(
        f"Unsupported source format for staging plan '{plan.source_id}': {plan.source_format}"
    )


def _key_signature(values: dict[str, Any], plan: SourceStagingPlan) -> str | None:
    """Return a deterministic key signature for a record."""
    if plan.primary_key is None:
        return None
    value = values.get(plan.primary_key)
    return f"{plan.primary_key}={value if value is not None else ''}"


class StagingProcessor:
    """Processes RAW sources into validated STAGING records.

    For every source the processor verifies the RAW snapshot checksum,
    normalizes values to the staging schema, validates required fields,
    types, allowed values and uniqueness, and writes accepted records plus
    a rejected/quarantine output with explicit disposition reasons.

    STAGING outputs are written atomically and never overwrite existing
    files for the same run.
    """

    def __init__(
        self,
        *,
        staging_root: str | Path | None = None,
        source_index_path: str | Path | None = None,
        run_id: str | None = None,
        transformation_version: str = DEFAULT_TRANSFORMATION_VERSION,
        schema_version: str = DEFAULT_SCHEMA_VERSION,
    ) -> None:
        self.staging_root = (
            Path(staging_root)
            if staging_root is not None
            else project_path("data", "02_staging")
        )
        if source_index_path is not None:
            self.source_index_path = Path(source_index_path)
        else:
            self.source_index_path = (
                project_path("data", "01_raw") / "source_index.json"
            )
        self.run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        self.transformation_version = transformation_version
        self.schema_version = schema_version
        self.logger = get_logger(f"aerovision.staging.{self.run_id}")
        self._staging_run_dir = self.staging_root / "runs" / self.run_id

    @property
    def staging_run_dir(self) -> Path:
        return self._staging_run_dir

    # ------------------------------------------------------------------
    # Snapshot resolution and integrity
    # ------------------------------------------------------------------

    def _resolve_snapshot(self, context: StagingSourceContext) -> Path:
        """Resolve a RAW snapshot path inside the RAW layer."""
        raw_root = project_path("data", "01_raw").resolve()
        candidate = (raw_root / context.raw_snapshot_path).resolve()
        if not candidate.is_relative_to(raw_root):
            raise ValueError(
                f"Snapshot path escapes RAW layer: {context.raw_snapshot_path}"
            )
        return candidate

    # ------------------------------------------------------------------
    # Source discovery
    # ------------------------------------------------------------------

    def discover_sources(
        self, source_ids: list[str] | None = None
    ) -> list[StagingSourceContext]:
        """Discover ingested RAW sources to stage.

        Sources are read from the RAW source index and their run manifests.
        Only sources registered in the RAW source registry and present in
        the source index are returned.
        """
        if not self.source_index_path.exists():
            return []

        index = json.loads(self.source_index_path.read_text(encoding="utf-8"))
        sources_index = index.get("sources", {}) if isinstance(index, dict) else {}

        registered = {s.source_id: s for s in create_default_source_registry()}
        target_ids = (
            list(source_ids)
            if source_ids is not None
            else [source_id for source_id in registered if source_id in sources_index]
        )

        contexts: list[StagingSourceContext] = []
        for source_id in target_ids:
            if source_id not in sources_index:
                continue
            runs = sources_index[source_id].get("runs", [])
            if not runs:
                continue
            latest_run = runs[-1]
            run_id = str(latest_run.get("run_id"))
            manifest_path = (
                project_path("data", "01_raw") / "runs" / run_id / "run_manifest.json"
            )
            if not manifest_path.exists():
                continue
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            source_entry = manifest.get("sources", {}).get(source_id, {})
            source_record = registered.get(source_id)
            contexts.append(
                StagingSourceContext(
                    source_id=source_id,
                    source_path=str(
                        source_entry.get("source_path", "")
                        or (source_record.source_path if source_record else "")
                    ),
                    source_name=str(
                        source_entry.get("source_name", "")
                        or (source_record.source_name if source_record else source_id)
                    ),
                    source_format=str(
                        source_entry.get("source_format", "")
                        or (source_record.source_format.value if source_record else "")
                    ),
                    source_description=(
                        source_record.description if source_record else ""
                    ),
                    source_sha256=str(source_entry.get("source_sha256", "")),
                    raw_run_id=str(latest_run.get("run_id", "")),
                    raw_snapshot_path=str(
                        source_entry.get("snapshot", {}).get("path", "")
                    ),
                )
            )
        return contexts

    # ------------------------------------------------------------------
    # Source processing
    # ------------------------------------------------------------------

    def process_source(self, context: StagingSourceContext) -> StagingResult:
        """Stage a single RAW source into validated records."""
        result = StagingResult(
            source_id=context.source_id,
            source_format=context.source_format,
            staging_run_id=self.run_id,
            status=StagingStatus.COMPLETED,
        )

        plan = get_staging_plan(context.source_id)
        if plan is None:
            result.status = StagingStatus.FAILED
            result.errors.append(
                f"No staging plan registered for source: {context.source_id}"
            )
            return result
        result.schema = plan

        try:
            snapshot_path = self._resolve_snapshot(context)
        except ValueError as exc:
            result.status = StagingStatus.FAILED
            result.errors.append(str(exc))
            return result

        if not snapshot_path.exists():
            result.status = StagingStatus.FAILED
            result.errors.append(f"Snapshot not found: {context.raw_snapshot_path}")
            return result

        snapshot_sha256 = sha256_file(snapshot_path)
        if snapshot_sha256 != context.source_sha256:
            result.status = StagingStatus.FAILED
            result.errors.append(
                f"Snapshot checksum mismatch: source={context.source_sha256}, snapshot={snapshot_sha256}"
            )
            return result

        result.source_path = context.source_path
        result.source_name = context.source_name
        result.source_sha256 = context.source_sha256
        result.raw_run_id = context.raw_run_id
        result.raw_snapshot_path = context.raw_snapshot_path
        result.transformation_version = self.transformation_version
        result.dataset_name = plan.dataset_name

        try:
            raw_records = read_source_records(plan, snapshot_path)
        except StagingFormatError as exc:
            result.status = StagingStatus.FAILED
            result.errors.append(str(exc))
            return result
        except Exception as exc:  # noqa: BLE001 - record any parse failure
            result.status = StagingStatus.FAILED
            result.errors.append(f"Failed to read source records: {exc}")
            return result

        accepted: list[StagedRecord] = []
        rejected: list[StagedRecord] = []
        seen_keys: set[str] = set()
        ingested_at_utc = datetime.now(timezone.utc).isoformat()

        for row_number, raw in raw_records:
            values, quality_status, disposition, rule_id, reason = (
                self._validate_record(plan, raw, seen_keys)
            )
            record = StagedRecord(
                source_id=context.source_id,
                source_row_number=row_number,
                source_file=Path(context.source_path).name,
                source_sha256=context.source_sha256,
                raw_run_id=context.raw_run_id,
                raw_snapshot_path=context.raw_snapshot_path,
                transformation_version=self.transformation_version,
                schema_version=self.schema_version,
                ingested_at_utc=ingested_at_utc,
                quality_status=quality_status,
                disposition=disposition,
                quality_rule_id=rule_id,
                disposition_reason=reason,
                fields=values,
            )
            if quality_status == QualityStatus.ACCEPTED:
                accepted.append(record)
                signature = _key_signature(values, plan)
                if signature is not None:
                    seen_keys.add(signature)
            else:
                rejected.append(record)

        result.records = accepted + rejected

        original_filename = Path(context.source_path).name
        source_stage_dir = (
            self._staging_run_dir / "sources" / context.source_id / "accepted"
        )
        source_stage_dir.mkdir(parents=True, exist_ok=True)
        accepted_path = source_stage_dir / original_filename
        write_json_atomic(
            accepted_path, [_staged_record_to_dict(r) for r in accepted]
        )
        output_sha256 = sha256_file(accepted_path)

        rejected_dir = (
            self._staging_run_dir / "sources" / context.source_id / "rejected"
        )
        rejected_dir.mkdir(parents=True, exist_ok=True)
        rejected_path = rejected_dir / original_filename
        write_json_atomic(
            rejected_path, [_staged_record_to_dict(r) for r in rejected]
        )

        duplicate_count = sum(
            1
            for r in rejected
            if r.quality_status == QualityStatus.DUPLICATE
        )
        metadata = {
            "source_id": context.source_id,
            "source_name": context.source_name,
            "source_format": context.source_format,
            "source_path": context.source_path,
            "source_sha256": context.source_sha256,
            "raw_run_id": context.raw_run_id,
            "raw_snapshot_path": context.raw_snapshot_path,
            "transformation_version": self.transformation_version,
            "schema_version": self.schema_version,
            "dataset_name": plan.dataset_name,
            "staging_schema": {
                "source_id": plan.source_id,
                "source_format": plan.source_format,
                "dataset_name": plan.dataset_name,
                "sheet_name": plan.sheet_name,
                "columns": list(plan.column_names),
                "required_columns": list(plan.required_columns),
                "primary_key": plan.primary_key,
                "unique_keys": list(plan.unique_keys),
                "type_rules": dict(plan.type_rules),
                "allowed_values": (
                    {
                        key: list(values)
                        for key, values in plan.allowed_values.items()
                    }
                    if plan.allowed_values
                    else None
                ),
            },
            "processed_record_count": len(accepted) + len(rejected),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
            "duplicate_count": duplicate_count,
            "output_path": str(accepted_path),
            "output_sha256": output_sha256,
            "status": result.status.value,
            "ingested_at_utc": ingested_at_utc,
            "dispositions": {
                "accepted": len(accepted),
                "rejected": len(rejected),
                "duplicates": duplicate_count,
            },
        }
        metadata_path = (
            self._staging_run_dir
            / "sources"
            / context.source_id
            / "metadata.json"
        )
        write_json_atomic(metadata_path, metadata)

        result.output_path = str(accepted_path)
        result.output_sha256 = output_sha256
        return result

    def process_sources(
        self, contexts: list[StagingSourceContext]
    ) -> list[StagingResult]:
        """Stage a list of RAW sources."""
        return [self.process_source(context) for context in contexts]

    def write_run_manifest(self, results: list[StagingResult]) -> Path:
        """Write the STAGING run manifest atomically."""
        run_manifest = {
            "run_id": self.run_id,
            "run_timestamp": datetime.now(timezone.utc).isoformat(),
            "tool": "build_staging_layer.py",
            "tool_version": "1.0.0",
            "staging_layer": "data/02_staging",
            "transformation_version": self.transformation_version,
            "schema_version": self.schema_version,
            "summary": {
                "total_sources": len(results),
                "completed": sum(
                    1 for r in results if r.status == StagingStatus.COMPLETED
                ),
                "failed": sum(
                    1 for r in results if r.status == StagingStatus.FAILED
                ),
                "skipped": sum(
                    1 for r in results if r.status == StagingStatus.SKIPPED
                ),
                "accepted_records": sum(
                    r.accepted_count
                    for r in results
                    if r.status == StagingStatus.COMPLETED
                ),
                "rejected_records": sum(
                    r.rejected_count
                    for r in results
                    if r.status == StagingStatus.COMPLETED
                ),
            },
            "sources": {},
        }

        for result in results:
            entry: dict[str, Any] = {
                "source_id": result.source_id,
                "source_format": result.source_format,
                "status": result.status.value,
                "errors": list(result.errors),
            }
            if result.schema is not None:
                entry["staging"] = {
                    "dataset_name": result.dataset_name,
                    "transformation_version": result.transformation_version,
                    "schema_version": self.schema_version,
                    "columns": list(result.schema.column_names),
                    "required_columns": list(result.schema.required_columns),
                    "primary_key": result.schema.primary_key,
                    "unique_keys": list(result.schema.unique_keys),
                    "type_rules": dict(result.schema.type_rules),
                    "allowed_values": (
                        {
                            key: list(values)
                            for key, values in (result.schema.allowed_values or {}).items()
                        }
                        if result.schema.allowed_values
                        else None
                    ),
                }
            for key in (
                "source_path",
                "source_name",
                "source_sha256",
                "raw_run_id",
                "raw_snapshot_path",
                "transformation_version",
                "output_path",
                "output_sha256",
            ):
                value = getattr(result, key, None)
                if value is not None:
                    entry[key] = value
            run_manifest["sources"][result.source_id] = entry

        manifest_path = self._staging_run_dir / "run_manifest.json"
        write_json_atomic(manifest_path, run_manifest)
        return manifest_path

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_record(
        self,
        plan: SourceStagingPlan,
        raw: dict[str, Any],
        seen_keys: set[str],
    ) -> tuple[dict[str, Any], QualityStatus, Disposition, str | None, str | None]:
        """Validate one raw record against the staging plan.

        Returns:
            (normalized_values, quality_status, disposition, quality_rule_id, disposition_reason)
        """
        values: dict[str, Any] = {}
        for column in plan.column_names:
            raw_value = raw.get(column)
            type_name = plan.type_rules.get(column, "string")
            try:
                converted = _convert_type(raw_value, type_name)
            except (ValueError, TypeError):
                return (
                    {},
                    QualityStatus.REJECTED,
                    Disposition.REJECTED,
                    "STG_TYPE",
                    f"type_conversion_failed:{column}",
                )
            values[column] = converted

        for column in plan.required_columns:
            value = values.get(column)
            if value is None or value == "":
                return (
                    {},
                    QualityStatus.REJECTED,
                    Disposition.REJECTED,
                    "STG_REQUIRED",
                    f"missing_required_field:{column}",
                )

        if plan.allowed_values:
            for column, allowed in plan.allowed_values.items():
                value = values.get(column)
                if value is None:
                    continue
                if value not in allowed:
                    return (
                        {},
                        QualityStatus.REJECTED,
                        Disposition.REJECTED,
                        "STG_ALLOWED",
                        f"invalid_allowed_value:{column}",
                    )

        signature = _key_signature(values, plan)
        if signature is not None and signature in seen_keys:
            return (
                values,
                QualityStatus.DUPLICATE,
                Disposition.REJECTED,
                "STG_DUPLICATE",
                f"duplicate_key:{plan.primary_key}",
            )

        if signature is not None:
            seen_keys.add(signature)

        return (
            values,
            QualityStatus.ACCEPTED,
            Disposition.ACCEPTED,
            None,
            None,
        )


def _staged_record_to_dict(record: StagedRecord) -> dict[str, Any]:
    """Convert a StagedRecord into its persisted staging representation."""
    data = dict(record.fields)
    data["SourceFile"] = record.source_file
    data["SourceRowNumber"] = record.source_row_number
    data["IngestedAtUTC"] = record.ingested_at_utc
    data["SchemaVersion"] = record.schema_version
    data["QualityStatus"] = record.quality_status.value
    data["QualityRuleID"] = record.quality_rule_id
    data["Disposition"] = record.disposition.value
    data["DispositionReason"] = record.disposition_reason
    data["SourceID"] = record.source_id
    data["SourceSHA256"] = record.source_sha256
    data["RAWRunID"] = record.raw_run_id
    data["RawSnapshotPath"] = record.raw_snapshot_path
    data["TransformationVersion"] = record.transformation_version
    return data
