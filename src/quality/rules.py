"""Rule registry and rule definitions for the Data Quality Engine.

Registered rules use stable identifiers (RULE_ prefix) and have associated
severity levels. The engine executes rules against STAGING datasets and
produces auditable quality results.

Each rule can be:
  - CRITICAL: failure blocks CURATED publication
  - WARNING: non-critical quality issue
  - INFO: informational check only
"""
from __future__ import annotations

from .models import QualityColumnRule, QualityIntegrityRule, QualityRecordOutcome


# ---------------------------------------------------------------------------
# Rule identifiers (stable, deterministic, namespaced)
# ---------------------------------------------------------------------------

# Schema validation rules
RULE_REQUIRED_COLUMN = "RULE-001"
RULE_TYPE_COLUMN = "RULE-002"
RULE_NULLABLE_COLUMN = "RULE-003"
RULE_PRIMARY_KEY_UNIQUE = "RULE-010"
RULE_COMPOSITE_KEY_UNIQUE = "RULE-011"
RULE_UNEXPECTED_COLUMN = "RULE-012"

# Integrity validation rules
RULE_FOREIGN_KEY = "RULE-101"
RULE_ALLOWED_VALUE = "RULE-102"
RULE_NUMERIC_BOUNDARY = "RULE-103"
RULE_DATE_BOUNDARY = "RULE-104"
RULE_DUPLICATE_RECORD = "RULE-110"

# Information rules
RULE_RECORD_COUNT = "RULE-201"


# ---------------------------------------------------------------------------
# Rule severity classification
# ---------------------------------------------------------------------------

# Rules whose failure CRITICALLY blocks CURATED publication
CRITICAL_RULES = {
    RULE_REQUIRED_COLUMN,
    RULE_TYPE_COLUMN,
    RULE_PRIMARY_KEY_UNIQUE,
    RULE_FOREIGN_KEY,
}

# Rules whose failure produces a WARNING only
WARNING_RULES = {
    RULE_NULLABLE_COLUMN,
    RULE_COMPOSITE_KEY_UNIQUE,
    RULE_ALLOWED_VALUE,
    RULE_NUMERIC_BOUNDARY,
    RULE_DATE_BOUNDARY,
    RULE_DUPLICATE_RECORD,
    RULE_UNEXPECTED_COLUMN,
    RULE_RECORD_COUNT,
}

# All registered rules
ALL_REGISTERED_RULES = {
    RULE_REQUIRED_COLUMN,
    RULE_TYPE_COLUMN,
    RULE_NULLABLE_COLUMN,
    RULE_PRIMARY_KEY_UNIQUE,
    RULE_COMPOSITE_KEY_UNIQUE,
    RULE_UNEXPECTED_COLUMN,
    RULE_FOREIGN_KEY,
    RULE_ALLOWED_VALUE,
    RULE_NUMERIC_BOUNDARY,
    RULE_DATE_BOUNDARY,
    RULE_DUPLICATE_RECORD,
    RULE_RECORD_COUNT,
}


# ---------------------------------------------------------------------------
# Pre-registered rule definitions
# ---------------------------------------------------------------------------

# Maps rule ID -> (description, severity)
REGISTERED_RULES: dict[str, tuple[str, str]] = {
    # Schema validation
    RULE_REQUIRED_COLUMN: (
        "Required column missing from record",
        "CRITICAL",
    ),
    RULE_TYPE_COLUMN: (
        "Value cannot be converted to declared staging type",
        "CRITICAL",
    ),
    RULE_NULLABLE_COLUMN: (
        "Optional column has unexpected value",
        "WARNING",
    ),
    RULE_PRIMARY_KEY_UNIQUE: (
        "Primary key value is not unique within dataset",
        "CRITICAL",
    ),
    RULE_COMPOSITE_KEY_UNIQUE: (
        "Composite key is not unique within dataset",
        "WARNING",
    ),
    RULE_UNEXPECTED_COLUMN: (
        "Column present that is not in the contract schema",
        "WARNING",
    ),

    # Integrity validation
    RULE_FOREIGN_KEY: (
        "Foreign key reference does not resolve to a valid parent record",
        "CRITICAL",
    ),
    RULE_ALLOWED_VALUE: (
        "Column value not in the permitted allowed-values set",
        "WARNING",
    ),
    RULE_NUMERIC_BOUNDARY: (
        "Numeric value outside the permitted boundary range",
        "WARNING",
    ),
    RULE_DATE_BOUNDARY: (
        "Date value outside the permitted boundary range",
        "WARNING",
    ),
    RULE_DUPLICATE_RECORD: (
        "Duplicate record detected based on key signature",
        "WARNING",
    ),

    # Information
    RULE_RECORD_COUNT: (
        "Dataset row count outside expected range",
        "INFO",
    ),
}


def register_rule(rule_id: str, description: str, severity: str) -> None:
    """Register a new quality rule at runtime.

    Args:
        rule_id: stable rule identifier (RULE-XXX format)
        description: human-readable rule description
        severity: one of "CRITICAL", "WARNING", or "INFO"
    """
    REGISTERED_RULES[rule_id] = (description, severity)
    ALL_REGISTERED_RULES.add(rule_id)


def is_critical(rule_id: str) -> bool:
    """Return True if a rule failure is classified as CRITICAL."""
    return rule_id in CRITICAL_RULES


def is_warning(rule_id: str) -> bool:
    """Return True if a rule failure is classified as WARNING."""
    return rule_id in WARNING_RULES


def is_registered(rule_id: str) -> bool:
    """Return True if the rule ID is known to the engine."""
    return rule_id in ALL_REGISTERED_RULES


def get_rule_info(rule_id: str) -> tuple[str, str] | None:
    """Return (description, severity) for a rule, or None if unknown."""
    return REGISTERED_RULES.get(rule_id)