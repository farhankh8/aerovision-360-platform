"""Data models for the AEROVISION 360 Data Quality Engine.

Defines the pydantic-like (but dependency-free) models used throughout
the quality validation pipeline: record outcomes, dataset summaries,
column/integrity rules, and manifest structures.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Set, Tuple, Optional


class QualityOutcome(Enum):
    """Outcome of a single rule check against a record or dataset."""
    PASS = "passed"
    WARNING = "warning"
    FAIL = "failed"


@dataclass
class QualityRecordOutcome:
    """Outcome of one quality rule against a single record (or aggregated)."""

    rule_id: str
    outcome: str  # QualityOutcome.value
    field_name: str | None = None
    reason: str | None = None
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "outcome": self.outcome,
            "field_name": self.field_name,
            "reason": self.reason,
            "evidence": self.evidence,
        }


@dataclass
class QualityColumnRule:
    """Schema-level column constraint for quality validation."""

    column_name: str
    rule_type: str  # e.g. "required", "type", "nullable", "allowed_values"
    description: str = ""
    severity: str = "CRITICAL"


@dataclass
class QualityIntegrityRule:
    """Integrity constraint (FK, uniqueness, allowed values)."""

    rule_id: str
    description: str = ""
    affected_fields: Tuple[str, ...] = field(default_factory=tuple)
    severity: str = "CRITICAL"


@dataclass
class QualityDatasetSummary:
    """Aggregate summary of a dataset's quality validation."""

    dataset_id: str
    total_records: int = 0
    passed_critical_rules: int = 0
    failed_critical_rules: int = 0
    warning_rules: int = 0
    info_rules: int = 0
    overall_outcome: str = "passed"  # passed / warning / failed
    failed_record_count: int = 0
    warning_record_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "total_records": self.total_records,
            "passed_critical_rules": self.passed_critical_rules,
            "failed_critical_rules": self.failed_critical_rules,
            "warning_rules": self.warning_rules,
            "info_rules": self.info_rules,
            "overall_outcome": self.overall_outcome,
            "failed_record_count": self.failed_record_count,
            "warning_record_count": self.warning_record_count,
        }


def outcome_from_severity(severity: str, has_critical: bool, has_warning: bool) -> str:
    """Convert severity counts to overall outcome string."""
    if has_critical:
        return "failed"
    if has_warning:
        return "warning"
    return "passed"


class QualitySchema:
    """Schema contract that describes a STAGING dataset's structure and rules."""

    def __init__(
        self,
        required_columns: tuple[str, ...] = (),
        type_rules: dict[str, str] | None = None,
        nullable_columns: set[str] | None = None,
        primary_key: str | None = None,
        composite_key: tuple[str, ...] | None = None,
        foreign_keys: dict[str, str] | None = None,
        allowed_values: dict[str, tuple[Any, ...]] | None = None,
        numeric_boundaries: dict[str, dict[str, float]] | None = None,
        date_boundaries: dict[str, dict[str, str]] | None = None,
        expected_row_count_range: tuple[int, int] | None = None,
    ) -> None:
        self.required_columns = required_columns
        self.type_rules = type_rules or {}
        self.nullable_columns = nullable_columns or set()
        self.primary_key = primary_key
        self.composite_key = composite_key
        self.foreign_keys = foreign_keys or {}
        self.allowed_values = allowed_values or {}
        self.numeric_boundaries = numeric_boundaries or {}
        self.date_boundaries = date_boundaries or {}
        self.expected_row_count_range = expected_row_count_range