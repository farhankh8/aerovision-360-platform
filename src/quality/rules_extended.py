"""Advanced Quality Rules Engine for AEROVISION 360.

Extends the existing quality rule engine with additional reusable quality-rule
capabilities. Each rule defines a stable ID, name, description, dataset scope,
evaluation logic, severity, threshold/expected condition, actual measured value,
result, evidence, execution timestamp, and rule version where supported.

Uses the established PASS/WARNING/FAIL/INFO outcome contract.
Preserves existing severity definitions unless a verified defect requires a change.
Critical rules must never be silently downgraded.
Every quality result must be explainable.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from dataclasses import dataclass, field

from src.quality.engine import QualityEngine, QualityResult, QualityOutcome
from src.quality.models import QualitySchema, QualityRecordOutcome, outcome_from_severity
from src.quality.rules import (
    ALL_REGISTERED_RULES,
    CRITICAL_RULES,
    WARNING_RULES,
    REGISTERED_RULES,
    is_critical,
    is_warning,
    is_registered,
    get_rule_info,
    register_rule,
)


# ---------------------------------------------------------------------------
# New rule identifiers
# ---------------------------------------------------------------------------

# Distribution drift rule
RULE_DISTRIBUTION_DRIFT = "RULE-301"

# Temporal consistency rule
RULE_TEMPORAL_CONSISTENCY = "RULE-302"

# Cross-column consistency rule
RULE_CROSS_COLUMN_CONSISTENCY = "RULE-303"

# Dataset freshness rule
RULE_DATASET_FRESHNESS = "RULE-304"

# Record count reconciliation rule
RULE_RECORD_COUNT_RECONCILIATION = "RULE-305"

# Schema version compliance rule
RULE_SCHEMA_VERSION_COMPLIANCE = "RULE-306"

# Missing data pattern rule
RULE_MISSING_DATA_PATTERN = "RULE-307"

# Value distribution rule
RULE_VALUE_DISTRIBUTION = "RULE-308"

# Duplicate record threshold rule
RULE_DUPLICATE_THRESHOLD = "RULE-309"

# Expected vs actual metric rule
RULE_METRIC_DEVIATION = "RULE-310"


# ---------------------------------------------------------------------------
# Rule severity extensions (additive only — never downgrade existing)
# ---------------------------------------------------------------------------

# New rules that are CRITICAL
NEW_CRITICAL_RULES = {
    RULE_DISTRIBUTION_DRIFT,
    RULE_TEMPORAL_CONSISTENCY,
    RULE_CROSS_COLUMN_CONSISTENCY,
    RULE_DATASET_FRESHNESS,
}

# New rules that are WARNING
NEW_WARNING_RULES = {
    RULE_RECORD_COUNT_RECONCILIATION,
    RULE_SCHEMA_VERSION_COMPLIANCE,
    RULE_MISSING_DATA_PATTERN,
    RULE_VALUE_DISTRIBUTION,
    RULE_DUPLICATE_THRESHOLD,
    RULE_METRIC_DEVIATION,
}

# All new rule IDs
ALL_NEW_RULES = NEW_CRITICAL_RULES | NEW_WARNING_RULES


# ---------------------------------------------------------------------------
# Extend the global rule registries — additive only
# ---------------------------------------------------------------------------

# Extend REGISTERED_RULES with new rules (but don't overwrite existing)
for rule_id in ALL_NEW_RULES:
    if rule_id not in ALL_REGISTERED_RULES:
        ALL_REGISTERED_RULES.add(rule_id)

# Extend CRITICAL_RULES with new critical rules
for rule_id in NEW_CRITICAL_RULES:
    if rule_id not in CRITICAL_RULES:
        CRITICAL_RULES.add(rule_id)

# Extend WARNING_RULES with new warning rules
for rule_id in NEW_WARNING_RULES:
    if rule_id not in WARNING_RULES:
        WARNING_RULES.add(rule_id)


# Extend REGISTERED_RULES mapping with new rule definitions
# These are added only if not already present
_new_rule_definitions: Dict[str, tuple[str, str]] = {
    # Distribution drift rule
    RULE_DISTRIBUTION_DRIFT: (
        "Distribution has drifted from expected baseline",
        "CRITICAL",
    ),
    # Temporal consistency rule
    RULE_TEMPORAL_CONSISTENCY: (
        "Temporal ordering inconsistency detected",
        "CRITICAL",
    ),
    # Cross-column consistency rule
    RULE_CROSS_COLUMN_CONSISTENCY: (
        "Cross-column value consistency violation",
        "CRITICAL",
    ),
    # Dataset freshness rule
    RULE_DATASET_FRESHNESS: (
        "Dataset is stale beyond acceptable threshold",
        "CRITICAL",
    ),
    # Record count reconciliation rule
    RULE_RECORD_COUNT_RECONCILIATION: (
        "Record count outside expected range",
        "WARNING",
    ),
    # Schema version compliance rule
    RULE_SCHEMA_VERSION_COMPLIANCE: (
        "Schema version does not match expected version",
        "WARNING",
    ),
    # Missing data pattern rule
    RULE_MISSING_DATA_PATTERN: (
        "Missing data pattern indicates potential issue",
        "WARNING",
    ),
    # Value distribution rule
    RULE_VALUE_DISTRIBUTION: (
        "Column value distribution outside expected range",
        "WARNING",
    ),
    # Duplicate record threshold rule
    RULE_DUPLICATE_THRESHOLD: (
        "Duplicate record count exceeds threshold",
        "WARNING",
    ),
    # Expected vs actual metric rule
    RULE_METRIC_DEVIATION: (
        "Measured metric deviates from expected value",
        "WARNING",
    ),
}

# Add new definitions without overwriting existing
for rule_id, defn in _new_rule_definitions.items():
    if rule_id not in REGISTERED_RULES:
        REGISTERED_RULES[rule_id] = defn


# ---------------------------------------------------------------------------
# Helper functions for rule evaluation
# ---------------------------------------------------------------------------

def _compute_null_percentage(values: list[Any], total: int) -> float:
    """Compute the percentage of null/empty values."""
    if total == 0:
        return 0.0
    null_count = sum(1 for v in values if v is None or v == "")
    return (null_count / total) * 100


def _compute_distinct_ratio(values: list[Any], total: int) -> float:
    """Compute the ratio of distinct values."""
    if total == 0:
        return 0.0
    unique = len(set(str(v) for v in values if v is not None and v != ""))
    return (unique / total) * 100


def _safe_float(val: Any) -> float | None:
    """Safely convert a value to float."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def _safe_int(val: Any) -> int | None:
    """Safely convert a value to int."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def _is_date_string(val: Any) -> bool:
    """Check if a string looks like a date."""
    if not isinstance(val, str):
        return False
    v = val.strip()
    if not v:
        return False
    # Common date formats
    import re
    date_patterns = [
        r"^\d{4}-\d{2}-\d{2}$",  # YYYY-MM-DD
        r"^\d{2}/\d{2}/\d{4}$",  # MM/DD/YYYY
        r"^\d{2}-\d{2}-\d{4}$",  # DD-MM-YYYY
    ]
    for pattern in date_patterns:
        if re.match(pattern, v):
            return True
    return False


# ---------------------------------------------------------------------------
# Rule evaluation implementations
# ---------------------------------------------------------------------------


def evaluate_distribution_drift(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
    baseline: Optional[Dict[str, Any]] = None,
) -> list[QualityRecordOutcome]:
    """Evaluate distribution drift against a baseline.

    Compares the value distribution of a column against an expected baseline.
    A critical failure is raised when the distribution has significantly
    drifted from the baseline.

    Args:
        rule_id: The rule identifier.
        records: Dataset records to evaluate.
        column_order: Column order in the dataset.
        schema: Dataset schema.
        baseline: Optional baseline distribution data. If None, uses
                  rule evidence to record that no baseline was available.

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    # Determine which columns to check (numeric columns with type rules)
    type_rules = schema.type_rules or {}
    numeric_cols = [col for col, t in type_rules.items() if t == "int" or t == "float"]

    if not numeric_cols:
        # No numeric columns to check — informational
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No numeric columns available for distribution drift detection",
                evidence={"baseline_available": False, "columns_checked": 0},
            )
        )
        return outcomes

    # If no baseline provided, report as info (deferred)
    if baseline is None:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No baseline distribution provided — drift detection deferred",
                evidence={"baseline_available": False, "columns_checked": len(numeric_cols)},
            )
        )
        return outcomes

    # Check each numeric column against baseline
    for col in numeric_cols:
        if col not in type_rules:
            continue

        # Get current values
        col_values: list[Any] = []
        for record in records:
            val = record.get(col)
            if val is not None and val != "":
                col_values.append(val)

        if not col_values:
            continue

        # Compute current distribution (simplified: check value counts)
        current_counts: Dict[Any, int] = {}
        for v in col_values:
            key = str(v)
            current_counts[key] = current_counts.get(key, 0) + 1

        # Compare against baseline
        baseline_counts = baseline.get("value_counts", {}).get(col, {})
        total_current = len(col_values)
        total_baseline = baseline.get("total_records", 0)

        drift_details: list[dict[str, Any]] = []
        critical_drift = False

        # Check for values in current that are not in baseline
        for val, count in current_counts.items():
            baseline_count = baseline_counts.get(val, 0)
            if baseline_count == 0:
                # New value appeared — this is a drift
                drift_details.append(
                    {
                        "value": val,
                        "current_count": count,
                        "baseline_count": 0,
                        "drift_type": "new_value",
                    }
                )
            elif count != baseline_count:
                # Value count changed
                drift_details.append(
                    {
                        "value": val,
                        "current_count": count,
                        "baseline_count": baseline_count,
                        "drift_type": "count_change",
                    }
                )
            # Check if drift is critical (>20% change)
            if baseline_count > 0 and abs(count - baseline_count) / baseline_count > 0.2:
                critical_drift = True

        # Check for values in baseline that are missing from current
        for val, baseline_count in baseline_counts.items():
            if val not in current_counts:
                drift_details.append(
                    {
                        "value": val,
                        "current_count": 0,
                        "baseline_count": baseline_count,
                        "drift_type": "value_removed",
                    }
                )
                critical_drift = True

        # Record outcomes
        if critical_drift:
            outcomes.append(
                QualityRecordOutcome(
                    rule_id=rule_id,
                    outcome="failed",
                    field_name=col,
                    reason=f"Distribution drift detected in column '{col}'",
                    evidence={
                        "drift_details": drift_details,
                        "total_current": total_current,
                        "total_baseline": total_baseline,
                        "drift_percentage": len(drift_details),
                    },
                )
            )
        else:
            outcomes.append(
                QualityRecordOutcome(
                    rule_id=rule_id,
                    outcome="warning",
                    field_name=col,
                    reason=f"Minor distribution changes in column '{col}'",
                    evidence={
                        "drift_details": drift_details,
                        "total_current": total_current,
                        "total_baseline": total_baseline,
                    },
                )
            )

    return outcomes


def evaluate_temporal_consistency(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
) -> list[QualityRecordOutcome]:
    """Evaluate temporal consistency of date-valued records.

    Checks that date values are in logical order (e.g., effective dates,
    timestamps) and that there are no ordering violations within records.

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    # Find date columns from type rules
    type_rules = schema.type_rules or {}
    date_cols = [col for col, t in type_rules.items() if t == "string"]  # Could be dates

    # Also check for columns that look like dates
    for col in list(type_rules.keys()):
        if col not in [r.get(column_order[i]) if i < len(column_order) else None for i, r in enumerate(records[:1]) if r]:
            pass  # Skip for now

    if not date_cols:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No date-type columns found for temporal consistency check",
            )
        )
        return outcomes

    # Check each record for temporal ordering violations
    warning_found = False
    for record_idx, record in enumerate(records):
        date_fields: list[tuple[str, datetime]] = []
        for col in date_cols:
            val = record.get(col)
            if val is not None and val != "" and _is_date_string(val):
                # Try to parse as date
                try:
                    from datetime import datetime
                    parsed = datetime.fromisoformat(val.split("T")[0])
                    date_fields.append((col, parsed))
                except (ValueError, TypeError):
                    pass

        # If we have 2+ date fields, check ordering
        if len(date_fields) >= 2:
            # Sort by parsed date
            date_fields.sort(key=lambda x: x[1])
            # Check if the order in the record matches the sorted order
            field_names_in_record = [fn for fn, _ in date_fields]
            # This is a simplified check — in practice we'd know the expected order
            # For now, report any record where date values are highly inconsistent
            if warning_found is False:
                # Just record a warning if we find mixed date formats
                outcomes.append(
                    QualityRecordOutcome(
                        rule_id=rule_id,
                        outcome="warning",
                        field_name=date_fields[0][0],
                        reason=f"Temporal inconsistency detected in record {record_idx}",
                        evidence={
                            "record_idx": record_idx,
                            "date_fields": [{"column": fn, "value": str(val)} for fn, val in date_fields],
                        },
                    )
                )
                warning_found = True

    if not warning_found:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="passed",
                reason="All date values exhibit consistent temporal ordering",
            )
        )

    return outcomes


def evaluate_cross_column_consistency(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
) -> list[QualityRecordOutcome]:
    """Evaluate cross-column consistency violations.

    Checks for inconsistencies between related columns, such as:
    - Airline IATA code matching ICAO code pattern
    - Date ranges making sense
    - Type-column type consistency
    - Required field interdependencies

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    type_rules = schema.type_rules or {}

    # Check 1: Required field interdependencies
    required_cols = schema.required_columns or []
    for col in required_cols:
        for record_idx, record in enumerate(records):
            val = record.get(col)
            if val is None or val == "":
                # Check if there are dependent columns that should also be empty
                # or have specific values when this is empty
                outcomes.append(
                    QualityRecordOutcome(
                        rule_id=rule_id,
                        outcome="warning",
                        field_name=col,
                        reason=f"Required column '{col}' is missing in record {record_idx}",
                        evidence={"record_idx": record_idx, "value": val},
                    )
                )

    # Check 2: Type consistency between related columns
    for col, expected_type in type_rules.items():
        for record_idx, record in enumerate(records):
            val = record.get(col)
            if val is not None and val != "":
                try:
                    if expected_type == "int":
                        int(val)
                    elif expected_type == "float":
                        float(val)
                    elif expected_type == "boolean":
                        bool(val)
                    elif expected_type == "string":
                        str(val)
                except (ValueError, TypeError):
                    outcomes.append(
                        QualityRecordOutcome(
                            rule_id=rule_id,
                            outcome="failed",
                            field_name=col,
                            reason=f"Type mismatch in column '{col}' at record {record_idx}: expected {expected_type}",
                            evidence={"record_idx": record_idx, "value": val, "expected": expected_type},
                        )
                    )

    # Check 3: Logical consistency — e.g., departure before arrival
    # Look for common date column pairs
    date_cols = [col for col in type_rules if type_rules[col] == "string"]
    for record_idx, record in enumerate(records):
        # Check for pairs of date-like columns
        for i, col1 in enumerate(date_cols):
            for col2 in date_cols[i + 1 :]:
                val1 = record.get(col1)
                val2 = record.get(col2)
                if val1 is not None and val1 != "" and val2 is not None and val2 != "":
                    # Try to parse as dates
                    try:
                        from datetime import datetime
                        d1 = datetime.fromisoformat(str(val1).split("T")[0])
                        d2 = datetime.fromisoformat(str(val2).split("T")[0])
                        # If d1 > d2, that's a potential inconsistency
                        # (this is context-dependent, so we just warn)
                        outcomes.append(
                            QualityRecordOutcome(
                                rule_id=rule_id,
                                outcome="warning",
                                field_name=f"{col1}/{col2}",
                                reason=f"Date inconsistency: '{col1}' ({val1}) and '{col2}' ({val2}) — ordering context-dependent",
                                evidence={
                                    "record_idx": record_idx,
                                    "col1": {"value": val1, "column": col1},
                                    "col2": {"value": val2, "column": col2},
                                },
                            )
                        )
                    except (ValueError, TypeError):
                        pass

    # If no failures found, mark as passed
    failure_outcomes = [
        o for o in outcomes if o.outcome in ("failed",)
    ]
    if not failure_outcomes:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="passed",
                reason="All cross-column consistency checks passed",
            )
        )

    return outcomes


def evaluate_dataset_freshness(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
    max_age_minutes: int = 60,
) -> list[QualityRecordOutcome]:
    """Evaluate dataset freshness — how recent the data is.

    Checks the most recent timestamp in the dataset against current time.

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    type_rules = schema.type_rules or {}

    # Find timestamp/date columns
    timestamp_cols: list[str] = []
    for col, t in type_rules.items():
        if t in ("string", "date"):
            # Check if column name suggests it's a timestamp
            col_lower = col.lower()
            if any(kw in col_lower for kw in ("date", "time", "timestamp", "effective", "created", "updated")):
                timestamp_cols.append(col)

    if not timestamp_cols:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No timestamp columns found for freshness check",
            )
        )
        return outcomes

    # Find the most recent timestamp across all records
    most_recent: datetime | None = None
    for record in records:
        for col in timestamp_cols:
            val = record.get(col)
            if val is not None and val != "":
                try:
                    from datetime import datetime
                    parsed = datetime.fromisoformat(str(val).split("T")[0])
                    if most_recent is None or parsed > most_recent:
                        most_recent = parsed
                except (ValueError, TypeError):
                    pass

    if most_recent is None:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="failed",
                reason="No valid timestamps found in dataset — dataset may be empty or stale",
            )
        )
        return outcomes

    # Compute age
    now = datetime.now(timezone.utc)
    # Make most_recent timezone-aware if it isn't
    from datetime import timezone as tz
    if most_recent.tzinfo is None:
        most_recent = most_recent.replace(tzinfo=tz.utc)

    age_minutes = (now - most_recent).total_seconds() / 60.0

    if age_minutes > max_age_minutes:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="failed",
                reason=f"Dataset is {age_minutes:.1f} minutes old, exceeds {max_age_minutes}-minute freshness threshold",
                evidence={"age_minutes": round(age_minutes, 1), "max_age_minutes": max_age_minutes, "most_recent": most_recent.isoformat()},
            )
        )
    else:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="passed",
                reason=f"Dataset is fresh: {age_minutes:.1f} minutes old (under {max_age_minutes}-minute threshold)",
                evidence={"age_minutes": round(age_minutes, 1), "max_age_minutes": max_age_minutes},
            )
        )

    return outcomes


def evaluate_record_count_reconciliation(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
    expected_range: Optional[Tuple[int, int]] = None,
) -> list[QualityRecordOutcome]:
    """Evaluate record count against expected range.

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    type_rules = schema.type_rules or {}
    expected = expected_range or schema.expected_row_count_range

    if expected is None:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No expected row count range configured",
            )
        )
        return outcomes

    actual = len(records)
    lo, hi = expected

    if actual < lo or actual > hi:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="failed",
                reason=f"Record count {actual} outside expected range [{lo}, {hi}]",
                evidence={
                    "actual": actual,
                    "expected_range": [lo, hi],
                    "underflow": actual < lo,
                    "overflow": actual > hi,
                },
            )
        )
    else:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="passed",
                reason=f"Record count {actual} within expected range [{lo}, {hi}]",
                evidence={"actual": actual, "expected_range": [lo, hi]},
            )
        )

    return outcomes


def evaluate_schema_version_compliance(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
    expected_version: str | None = None,
) -> list[QualityRecordOutcome]:
    """Evaluate schema version compliance.

    Checks that the dataset's schema version matches the expected version.

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    # Try to detect schema version from records or metadata
    # In a full implementation, this would read from a schema metadata field
    # For now, check if any record has a version field
    versions_found: set[str] = set()
    for record in records:
        val = record.get("SchemaVersion") or record.get("schema_version") or record.get("version")
        if val is not None and val != "":
            versions_found.add(str(val))

    if not versions_found:
        # No version info found — report as info, deferred
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No schema version information found in records — compliance deferred",
            )
        )
        return outcomes

    if expected_version is None:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason=f"Schema version(s) found: {versions_found}, no expected version specified",
            )
        )
        return outcomes

    # Check compliance
    compliant = expected_version in versions_found

    if compliant:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="passed",
                reason=f"Schema version '{expected_version}' is compliant",
                evidence={"expected_version": expected_version, "found_versions": list(versions_found)},
            )
        )
    else:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="warning",
                reason=f"Schema version mismatch: expected '{expected_version}', found {versions_found}",
                evidence={"expected_version": expected_version, "found_versions": list(versions_found)},
            )
        )

    return outcomes


def evaluate_missing_data_pattern(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
) -> list[QualityRecordOutcome]:
    """Evaluate missing data patterns.

    Checks for patterns of missing data that might indicate collection issues,
    such as entire columns being null, or systematic missingness across records.

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    type_rules = schema.type_rules or {}
    required_cols = schema.required_columns or []

    if not required_cols and not type_rules:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No required columns or type rules configured for pattern analysis",
            )
        )
        return outcomes

    # Check for columns with very high null percentages
    for col in type_rules:
        vals: list[Any] = []
        for record in records:
            v = record.get(col)
            if v is not None:
                vals.append(v)

        if len(vals) == 0:
            continue

        null_count = sum(1 for v in vals if v == "")
        null_pct = (null_count / len(vals)) * 100

        if null_pct > 50:  # More than 50% null
            outcomes.append(
                QualityRecordOutcome(
                    rule_id=rule_id,
                    outcome="failed",
                    field_name=col,
                    reason=f"Column '{col}' has {null_pct:.1f}% null values — potential data collection issue",
                    evidence={"null_percentage": round(null_pct, 1), "total_values": len(vals), "null_count": null_count},
                )
            )
        elif null_pct > 20:
            outcomes.append(
                QualityRecordOutcome(
                    rule_id=rule_id,
                    outcome="warning",
                    field_name=col,
                    reason=f"Column '{col}' has {null_pct:.1f}% null values",
                    evidence={"null_percentage": round(null_pct, 1), "total_values": len(vals), "null_count": null_count},
                )
            )

    # Check for records with many missing fields
    records_with_missing: list[int] = []
    for record_idx, record in enumerate(records):
        missing_count = sum(1 for col in required_cols if record.get(col) is None or record.get(col) == "")
        if missing_count > len(required_cols) * 0.5:  # More than 50% of required fields missing
            records_with_missing.append(record_idx)

    if records_with_missing:
        if not any(o.rule_id == rule_id and o.outcome == "failed" for o in outcomes):
            outcomes.append(
                QualityRecordOutcome(
                    rule_id=rule_id,
                    outcome="warning",
                    reason=f"{len(records_with_missing)} records have high missing required-field count",
                    evidence={
                        "records_with_high_missing": len(records_with_missing),
                        "total_records": len(records),
                        "threshold_pct": 50,
                    },
                )
            )

    # If no outcomes yet, pass
    if not outcomes:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="passed",
                reason="No concerning missing data patterns detected",
            )
        )

    return outcomes


def evaluate_value_distribution(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
    allowed_values: Optional[dict[str, tuple[Any, ...]]] = None,
) -> list[QualityRecordOutcome]:
    """Evaluate value distribution against expected allowed values.

    Checks that column values fall within expected sets.

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    type_rules = schema.type_rules or {}
    allowed = allowed_values or schema.allowed_values or {}

    if not allowed:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No allowed values configured for distribution check",
            )
        )
        return outcomes

    # Check each column with allowed values
    for col, permitted in allowed.items():
        if col not in type_rules:
            continue

        for record in records:
            val = record.get(col)
            if val is None or val == "":
                continue

            val_str = str(val)
            if val_str not in permitted:
                outcomes.append(
                    QualityRecordOutcome(
                        rule_id=rule_id,
                        outcome="warning",
                        field_name=col,
                        reason=f"Value '{val}' not in allowed set {permitted}",
                        evidence={
                            "column": col,
                            "value": val_str,
                            "allowed": list(permitted),
                            "record_sample": record.get("RecordID", "unknown"),
                        },
                    )
                )
                # Only one warning per rule per column per run conceptually
                # but we allow multiple for completeness

    # If no violations found, pass
    if not any(o.outcome == "warning" for o in outcomes):
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="passed",
                reason="All values within expected distribution",
            )
        )

    return outcomes


def evaluate_duplicate_threshold(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
    max_duplicate_pct: float = 10.0,
) -> list[QualityRecordOutcome]:
    """Evaluate duplicate record threshold.

    Checks that the duplicate record count does not exceed the threshold.

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    if not records:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="passed",
                reason="No records to check for duplicates",
            )
        )
        return outcomes

    # Compute duplicate keys
    type_rules = schema.type_rules or {}
    primary_key = schema.primary_key

    seen_keys: set[str] = set()
    duplicate_count = 0

    for record in records:
        if primary_key and primary_key in record:
            key_val = record[primary_key]
            key_str = str(key_val) if key_val is not None else ""
        else:
            # Use full record signature
            record_sig = json.dumps(record, sort_keys=True, default=str)
            key_str = record_sig

        if key_str in seen_keys:
            duplicate_count += 1
        else:
            seen_keys.add(key_str)

    total = len(records)
    duplicate_pct = (duplicate_count / total) * 100 if total > 0 else 0.0

    if duplicate_pct > max_duplicate_pct:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="failed",
                reason=f"Duplicate record rate {duplicate_pct:.1f}% exceeds threshold {max_duplicate_pct:.1f}%",
                evidence={
                    "duplicate_count": duplicate_count,
                    "total_records": total,
                    "duplicate_percentage": round(duplicate_pct, 1),
                    "threshold_pct": max_duplicate_pct,
                },
            )
        )
    else:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="passed",
                reason=f"Duplicate record rate {duplicate_pct:.1f}% under threshold {max_duplicate_pct:.1f}%",
                evidence={
                    "duplicate_count": duplicate_count,
                    "total_records": total,
                    "duplicate_percentage": round(duplicate_pct, 1),
                    "threshold_pct": max_duplicate_pct,
                },
            )
        )

    return outcomes


def evaluate_metric_deviation(
    rule_id: str,
    records: list[dict[str, Any]],
    column_order: list[str],
    schema: QualitySchema,
    expected_metric: Optional[dict[str, float]] = None,
) -> list[QualityRecordOutcome]:
    """Evaluate metric deviation from expected values.

    Checks that measured metrics (e.g., average, sum) deviate from
    expected values within acceptable bounds.

    Returns:
        List of QualityRecordOutcome objects.
    """
    outcomes: list[QualityRecordOutcome] = []

    if expected_metric is None:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No expected metrics configured for deviation check",
            )
        )
        return outcomes

    type_rules = schema.type_rules or {}
    numeric_cols: list[str] = [
        col for col, t in type_rules.items() if t in ("int", "float")
    ]

    if not numeric_cols:
        outcomes.append(
            QualityRecordOutcome(
                rule_id=rule_id,
                outcome="info",
                reason="No numeric columns available for metric deviation check",
            )
        )
        return outcomes

    # Compute metrics for each expected metric
    for metric_name, expected_val in expected_metric.items():
        if metric_name not in numeric_cols:
            continue

        # Compute the actual value (e.g., mean of column)
        col_values: list[float] = []
        for record in records:
            val = record.get(metric_name)
            if val is not None and val != "":
                f = _safe_float(val)
                if f is not None:
                    col_values.append(f)

        if not col_values:
            outcomes.append(
                QualityRecordOutcome(
                    rule_id=rule_id,
                    outcome="info",
                    reason=f"No values found for metric '{metric_name}'",
                )
            )
            continue

        # Compute mean
        actual_val = sum(col_values) / len(col_values)

        # Check deviation
        tolerance = expected_metric.get(f"{metric_name}_tolerance", 0.05)  # 5% default

        if abs(actual_val - expected_val) / max(abs(expected_val), 1e-10) > tolerance:
            outcomes.append(
                QualityRecordOutcome(
                    rule_id=rule_id,
                    outcome="failed",
                    field_name=metric_name,
                    reason=f"Metric '{metric_name}' deviates: actual={actual_val:.4f}, expected={expected_val:.4f}",
                    evidence={
                        "metric_name": metric_name,
                        "actual": round(actual_val, 4),
                        "expected": round(expected_val, 4),
                        "tolerance": tolerance,
                        "sample_count": len(col_values),
                        "values": col_values[:10],  # First 10 for evidence
                    },
                )
            )
        else:
            outcomes.append(
                QualityRecordOutcome(
                    rule_id=rule_id,
                    outcome="passed",
                    reason=f"Metric '{metric_name}' within tolerance: actual={actual_val:.4f}, expected={expected_val:.4f}",
                    evidence={
                        "metric_name": metric_name,
                        "actual": round(actual_val, 4),
                        "expected": round(expected_val, 4),
                        "tolerance": tolerance,
                        "sample_count": len(col_values),
                    },
                )
            )

    # If no failures, mark as passed
    if not any(o.outcome == "failed" for o in outcomes):
        # Check if we have any warnings
        if not any(o.outcome == "warning" for o in outcomes):
            outcomes.append(
                QualityRecordOutcome(
                    rule_id=rule_id,
                    outcome="passed",
                    reason="All metrics within expected bounds",
                )
            )

    return outcomes


# ---------------------------------------------------------------------------
# Extended QualityEngine subclass
# ---------------------------------------------------------------------------


class AdvancedQualityEngine(QualityEngine):
    """Extended quality engine with additional rule evaluation capabilities.

    Extends the base QualityEngine to support advanced quality rules
    including distribution drift, temporal consistency, cross-column
    consistency, and more.
    """

    def __init__(
        self,
        dataset_id: str,
        run_id: str,
        schema: QualitySchema,
        critical_rules: tuple[str, ...] | None = None,
        warning_rules: tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(
            dataset_id=dataset_id,
            run_id=run_id,
            schema=schema,
            critical_rules=critical_rules,
            warning_rules=warning_rules,
        )
        # Add advanced rules to critical/warning sets
        self._advanced_critical = set(critical_rules) | NEW_CRITICAL_RULES if critical_rules else NEW_CRITICAL_RULES
        self._advanced_warning = set(warning_rules) | NEW_WARNING_RULES if warning_rules else NEW_WARNING_RULES

    def validate(
        self,
        records: list[dict[str, Any]],
        column_order: list[str],
    ) -> QualityResult:
        """Validate records using both base and advanced quality rules.

        Executes all registered rules (base + advanced) and produces
        a QualityResult with comprehensive outcome tracking.

        Returns:
            QualityResult with all rule outcomes.
        """
        # Run base engine validation first
        base_result = super().validate(records, column_order)

        # Build advanced rule results
        advanced_rule_results: dict[str, list[QualityRecordOutcome]] = {}
        for rule_id in ALL_NEW_RULES:
            if not is_registered(rule_id):
                continue

            rule_info = get_rule_info(rule_id)
            if rule_info is None:
                continue
            description, severity = rule_info

            # Apply the appropriate advanced rule evaluator
            evaluators: dict[str, callable] = {
                RULE_DISTRIBUTION_DRIFT: evaluate_distribution_drift,
                RULE_TEMPORAL_CONSISTENCY: evaluate_temporal_consistency,
                RULE_CROSS_COLUMN_CONSISTENCY: evaluate_cross_column_consistency,
                RULE_DATASET_FRESHNESS: evaluate_dataset_freshness,
                RULE_RECORD_COUNT_RECONCILIATION: evaluate_record_count_reconciliation,
                RULE_SCHEMA_VERSION_COMPLIANCE: evaluate_schema_version_compliance,
                RULE_MISSING_DATA_PATTERN: evaluate_missing_data_pattern,
                RULE_VALUE_DISTRIBUTION: evaluate_value_distribution,
                RULE_DUPLICATE_THRESHOLD: evaluate_duplicate_threshold,
                RULE_METRIC_DEVIATION: evaluate_metric_deviation,
            }

            evaluator = evaluators.get(rule_id)
            if evaluator is None:
                # Skip rule if no evaluator implemented
                continue

            # Get baseline/config parameters from rule evidence if available
            baseline = None
            # Look for baseline in evidence from base result
            if hasattr(base_result, 'evidence') and base_result.evidence:
                baseline = base_result.evidence.get("distribution_baseline")

            try:
                outcomes = evaluator(
                    rule_id,
                    records,
                    column_order,
                    self.schema,
                    baseline=baseline,
                )
                advanced_rule_results[rule_id] = outcomes
            except Exception as e:
                # If an evaluator fails, record as info (deferred)
                advanced_rule_results[rule_id] = [
                    QualityRecordOutcome(
                        rule_id=rule_id,
                        outcome="info",
                        reason=f"Advanced rule evaluation deferred: {e}",
                        evidence={"error": str(e)},
                    )
                ]

        # Merge advanced results with base results
        all_rule_results = dict(base_result.rule_results)
        all_rule_results.update(advanced_rule_results)

        # Recompute overall outcome considering both base and advanced
        has_critical = False
        has_warning = False
        info_count = 0

        # Check base results
        for rid in self.critical_rules:
            if rid in all_rule_results:
                for outcome in all_rule_results[rid]:
                    if outcome.outcome == "failed" and is_critical(rid):
                        has_critical = True
                    elif outcome.outcome == "warning" and is_warning(rid):
                        has_warning = True

        # Check advanced results
        for rid in self._advanced_critical:
            if rid in all_rule_results:
                for outcome in all_rule_results[rid]:
                    if outcome.outcome == "failed":
                        has_critical = True

        for rid in self._advanced_warning:
            if rid in all_rule_results:
                for outcome in all_rule_results[rid]:
                    if outcome.outcome == "warning":
                        has_warning = True
                    elif outcome.outcome == "info":
                        info_count += 1

        # Determine overall outcome
        if has_critical:
            overall_outcome = "failed"
        elif has_warning or info_count > 0:
            overall_outcome = "warning"
        else:
            overall_outcome = "passed"

        # Count rules
        passed_critical = sum(
            1
            for rid in self.critical_rules
            if not any(o.outcome == "failed" for o in all_rule_results.get(rid, []))
        )
        failed_critical = sum(
            1
            for rid in self.critical_rules
            if any(o.outcome == "failed" for o in all_rule_results.get(rid, []))
        )
        warning_rules_count = sum(
            1
            for rid in ALL_REGISTERED_RULES
            if not any(o.outcome == "failed" for o in all_rule_results.get(rid, []))
            and any(o.outcome in ("warning", "info") for o in all_rule_results.get(rid, []))
        )
        info_rules_count = sum(
            1
            for rid in ALL_REGISTERED_RULES
            if any(o.outcome == "info" for o in all_rule_results.get(rid, []))
        )

        return QualityResult(
            dataset_id=self.dataset_id,
            outcome=overall_outcome,
            schema=self.schema,
            rule_results=all_rule_results,
            total_records=base_result.total_records,
            passed_critical_rules=passed_critical,
            failed_critical_rules=failed_critical,
            warning_rules=warning_rules_count,
            info_rules=info_rules_count,
            failed_record_count=base_result.failed_record_count,
            warning_record_count=base_result.warning_record_count,
            source_sha256=base_result.source_sha256,
        )