"""Data Quality Engine for AEROVISION 360.

Provides reusable, deterministic validation of STAGING datasets with
auditable quality results, publication gates, and rule-based reporting.

Quality outcomes:
  PASS   — all critical rules pass
  WARNING — non-critical issues exist
  FAIL    — at least one critical rule fails; blocks CURATED publication

Rule model:
  - Stable rule identifier (RULE_ prefix)
  - Severity (CRITICAL / WARNING / INFO)
  - Affected dataset, record key, or field
  - Clear failure reason
  - Evidence (sample values, count, hash)

Engine supports:
  - Rule registration by name and severity
  - Per-dataset validation with configurable rules
  - Record-level validation with affected key tracking
  - Dataset-level summary (passed/failed/warnings counts)
  - Quality manifest generation with hashes and lineage
  - Publication-gate evaluation (FAIL blocks CURATED approval)
  - Deterministic results for identical inputs

Advanced capabilities:
  - Data profiling engine
  - Advanced quality rules (distribution drift, temporal consistency, etc.)
  - Statistical anomaly detection (Z-score, MAD, IQR, volume, missingness, category frequency)
  - Data quality incident management (full lifecycle tracking)
  - Governance approval workflow (traceable decision making)
  - Governance policy registry (versioned policies)
  - Controlled remediation safeguards

"""

from __future__ import annotations

from .rules import (
    ALL_REGISTERED_RULES,
    is_critical,
    is_warning,
    is_registered,
    get_rule_info,
)
from .engine import QualityEngine, QualityResult
from .models import QualityOutcome
from .models import (
    QualitySchema,
    QualityColumnRule,
    QualityIntegrityRule,
    QualityRecordOutcome,
    QualityDatasetSummary,
)
from .manifest import QualityManifest
from .rules_extended import (
    ALL_NEW_RULES,
    CRITICAL_RULES as NEW_CRITICAL_RULES,
    WARNING_RULES as NEW_WARNING_RULES,
    REGISTERED_RULES as NEW_REGISTERED_RULES,
    RULE_DISTRIBUTION_DRIFT,
    RULE_TEMPORAL_CONSISTENCY,
    RULE_CROSS_COLUMN_CONSISTENCY,
    RULE_DATASET_FRESHNESS,
    RULE_RECORD_COUNT_RECONCILIATION,
    RULE_SCHEMA_VERSION_COMPLIANCE,
    RULE_MISSING_DATA_PATTERN,
    RULE_VALUE_DISTRIBUTION,
    RULE_DUPLICATE_THRESHOLD,
    RULE_METRIC_DEVIATION,
    AdvancedQualityEngine,
    evaluate_distribution_drift,
    evaluate_temporal_consistency,
    evaluate_cross_column_consistency,
    evaluate_dataset_freshness,
    evaluate_record_count_reconciliation,
    evaluate_schema_version_compliance,
    evaluate_missing_data_pattern,
    evaluate_value_distribution,
    evaluate_duplicate_threshold,
    evaluate_metric_deviation,
)
from .anomaly_detection import (
    AnomalySeverity,
    AnomalyStatus,
    AnomalyResult,
    detect_anomalies,
    detect_with_fallback,
    detect_z_score,
    detect_mad,
    detect_iqr,
    detect_volume_anomaly,
    detect_missingness_anomaly,
    detect_category_frequency_anomaly,
    run_anomaly_cli,
)
from .governance_workflow import (
    GovernanceDecision,
    GovernancePolicy,
    GovernanceDecisionRegistry,
    GovernancePolicyRegistry,
    GovernanceOutcome,
    is_valid_decision_transition,
    create_decision_cli,
    approve_decision_cli,
    reject_decision_cli,
    create_policy_cli,
    list_decisions_cli,
    list_policies_cli,
)
from .remediation_safeguards import (
    RemediationTransformation,
    RemediationTransaction,
    RemediationSafeguardsRegistry,
    RemediationOrchestrator,
)
from .orchestration_integration import (
    QualityToIncidentOrchestrator,
    OrchestrationResult,
    OrchestrationStatus,
)

__all__ = [
    "RuleRegistry",
    "QualityRule",
    "QualityEngine",
    "QualityResult",
    "QualityOutcome",
    "QualitySchema",
    "QualityColumnRule",
    "QualityIntegrityRule",
    "QualityRecordOutcome",
    "QualityDatasetSummary",
    "QualityManifest",
    "AdvancedQualityEngine",
    "evaluate_distribution_drift",
    "evaluate_temporal_consistency",
    "evaluate_cross_column_consistency",
    "evaluate_dataset_freshness",
    "evaluate_record_count_reconciliation",
    "evaluate_schema_version_compliance",
    "evaluate_missing_data_pattern",
    "evaluate_value_distribution",
    "evaluate_duplicate_threshold",
    "evaluate_metric_deviation",
    "RULE_DISTRIBUTION_DRIFT",
    "RULE_TEMPORAL_CONSISTENCY",
    "RULE_CROSS_COLUMN_CONSISTENCY",
    "RULE_DATASET_FRESHNESS",
    "RULE_RECORD_COUNT_RECONCILIATION",
    "RULE_SCHEMA_VERSION_COMPLIANCE",
    "RULE_MISSING_DATA_PATTERN",
    "RULE_VALUE_DISTRIBUTION",
    "RULE_DUPLICATE_THRESHOLD",
    "RULE_METRIC_DEVIATION",
    "AnomalySeverity",
    "AnomalyStatus",
    "AnomalyResult",
    "detect_anomalies",
    "detect_with_fallback",
    "detect_z_score",
    "detect_mad",
    "detect_iqr",
    "detect_volume_anomaly",
    "detect_missingness_anomaly",
    "detect_category_frequency_anomaly",
    "run_anomaly_cli",
    "GovernanceDecision",
    "GovernancePolicy",
    "GovernanceDecisionRegistry",
    "GovernancePolicyRegistry",
    "GovernanceOutcome",
    "is_valid_decision_transition",
    "create_decision_cli",
    "approve_decision_cli",
    "reject_decision_cli",
    "create_policy_cli",
    "list_decisions_cli",
    "list_policies_cli",
    "RemediationTransformation",
    "RemediationTransaction",
    "RemediationSafeguardsRegistry",
    "RemediationOrchestrator",
    "QualityToIncidentOrchestrator",
    "OrchestrationResult",
    "OrchestrationStatus",
]