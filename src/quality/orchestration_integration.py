"""Orchestration Integration for AEROVISION 360.

Provides quality-to-incident lifecycle integration with existing pipeline components.
Connects data quality rules, anomaly detection, and governance workflows into
a seamless orchestration layer that drives incident creation, remediation
proposals, and governance approval without silently modifying production data.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.quality.engine import QualityResult, QualitySchema
from src.quality.models import QualityRecordOutcome
from src.quality.anomaly_detection import AnomalyResult, detect_with_fallback
from src.quality.incident_management import (
    Incident,
    IncidentID,
    IncidentRegistry,
)
from src.quality.governance_workflow import (
    GovernanceDecision,
    GovernanceDecisionRegistry,
    GovernanceOutcome,
    is_valid_decision_transition,
)
from src.quality.remediation_safeguards import (
    RemediationSafeguardsRegistry,
    RemediationTransformation,
    RemediationTransaction,
    RemediationOrchestrator,
)


# ---------------------------------------------------------------------------
# Orchestration status and types
# ---------------------------------------------------------------------------

class OrchestrationStatus(str, Enum):
    """Status of an orchestration cycle."""
    
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


# ---------------------------------------------------------------------------
# Orchestration result
# ---------------------------------------------------------------------------

@dataclass
class OrchestrationResult:
    """Result of an orchestration cycle."""
    
    run_id: str
    status: OrchestrationStatus
    datasets_validated: int = 0
    incidents_created: int = 0
    anomalies_detected: int = 0
    remediation_proposed: int = 0
    governance_decisions: int = 0
    quality_outcome: str = "passed"
    errors: list[str] = field(default_factory=list)
    completed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "datasets_validated": self.datasets_validated,
            "incidents_created": self.incidents_created,
            "anomalies_detected": self.anomalies_detected,
            "remediation_proposed": self.remediation_proposed,
            "governance_decisions": self.governance_decisions,
            "quality_outcome": self.quality_outcome,
            "errors": self.errors,
            "completed_at": self.completed_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OrchestrationResult":
        status = OrchestrationStatus(data["status"]) if "status" in data else OrchestrationStatus.IDLE
        return cls(
            run_id=data["run_id"],
            status=status,
            datasets_validated=data.get("datasets_validated", 0),
            incidents_created=data.get("incidents_created", 0),
            anomalies_detected=data.get("anomalies_detected", 0),
            remediation_proposed=data.get("remediation_proposed", 0),
            governance_decisions=data.get("governance_decisions", 0),
            quality_outcome=data.get("quality_outcome", "passed"),
            errors=data.get("errors", []),
            completed_at=(
                datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else datetime.now(timezone.utc)
            ),
        )


# ---------------------------------------------------------------------------
# Quality-to-Incident Orchestrator
# ---------------------------------------------------------------------------

class QualityToIncidentOrchestrator:
    """Orchestrates the quality-to-incident lifecycle.
    
    Transforms quality rule results and anomaly detection outputs into
    actionable incidents with proper severity, evidence, and lifecycle
    tracking. All incident creation funnels through governance for
    approved remediation pathways.
    """
    
    def __init__(
        self,
        incident_registry: IncidentRegistry | None = None,
        decision_registry: GovernanceDecisionRegistry | None = None,
        remediation_registry: RemediationSafeguardsRegistry | None = None,
    ) -> None:
        self.incident_registry = incident_registry or IncidentRegistry()
        self.decision_registry = decision_registry or GovernanceDecisionRegistry()
        self.remediation_registry = remediation_registry or RemediationSafeguardsRegistry()
        self.logger = logging.getLogger(__name__)
    
    def orchestrate_quality_result(
        self,
        run_id: str,
        dataset_id: str,
        quality_result: QualityResult,
        schema: QualitySchema,
        records: list[dict[str, Any]] | None = None,
    ) -> OrchestrationResult:
        """Orchestrate a full quality validation run into incidents and governance.
        
        Process:
        1. Examine rule outcomes to identify issues
        2. Create incidents for rule failures and anomalies
        3. Propose remediations linked to governance decisions
        4. Track lifecycle through approved remediation
        
        Returns:
            OrchestrationResult with full lifecycle summary.
        """
        result = OrchestrationResult(run_id=run_id, status=OrchestrationStatus.PROCESSING)
        
        try:
            self._process_rule_outcomes(
                run_id=run_id,
                dataset_id=dataset_id,
                quality_result=quality_result,
                schema=schema,
                records=records,
            )
            
            # Summarize outcomes
            result.datasets_validated = 1
            result.quality_outcome = quality_result.outcome
            
            # Count incidents and governance actions from the registry
            incidents = self.incident_registry.list_incidents(dataset_id=dataset_id)
            result.incidents_created = len(incidents)
            
            # Count remediation transactions
            transactions = self.remediation_registry.list_transactions(dataset_id=dataset_id)
            result.remediation_proposed = sum(1 for t in transactions if t.status in ("APPROVED", "EXECUTED"))
            result.governance_decisions = self.decision_registry.count_by_state().get("DRAFT", 0) + \
                                          self.decision_registry.count_by_state().get("PENDING_REVIEW", 0) + \
                                          self.decision_registry.count_by_state().get("APPROVED", 0) + \
                                          self.decision_registry.count_by_state().get("REJECTED", 0) + \
                                          self.decision_registry.count_by_state().get("EXPIRED", 0) + \
                                          self.decision_registry.count_by_state().get("REVOKED", 0)
            
            result.status = OrchestrationStatus.COMPLETED
            
        except Exception as e:
            self.logger.error(f"Orchestration failed for run {run_id}: {e}")
            result.status = OrchestrationStatus.FAILED
            result.errors.append(str(e))
        
        return result
    
    def _process_rule_outcomes(
        self,
        run_id: str,
        dataset_id: str,
        quality_result: QualityResult,
        schema: QualitySchema,
        records: list[dict[str, Any]] | None,
    ) -> None:
        """Process quality rule outcomes and create incidents where needed."""
        
        for rule_id, outcomes in quality_result.rule_results.items():
            for outcome in outcomes:
                self._create_incident_for_outcome(
                    run_id=run_id,
                    dataset_id=dataset_id,
                    rule_id=rule_id,
                    outcome=outcome,
                    schema=schema,
                    records=records,
                )
    
    def _create_incident_for_outcome(
        self,
        run_id: str,
        dataset_id: str,
        rule_id: str,
        outcome: QualityRecordOutcome,
        schema: QualitySchema,
        records: list[dict[str, Any]] | None,
    ) -> Optional[Incident]:
        """Create an incident from a quality rule outcome."""
        
        # Only create incidents for failed or warning outcomes
        if outcome.outcome not in ("failed", "warning"):
            return None
        
        # Determine severity based on rule criticality
        from src.quality.rules import is_critical, is_warning
        is_critical_rule = is_critical(rule_id)
        
        if is_critical_rule and outcome.outcome == "failed":
            severity = "CRITICAL"
        elif outcome.outcome == "warning" or (not is_critical_rule and outcome.outcome == "failed"):
            severity = "WARNING"
        else:
            severity = "INFO"
        
        # Build description and evidence
        field_name = outcome.field_name or rule_id
        reason = outcome.reason or f"Rule {rule_id} outcome"
        
        # Build evidence from the outcome
        evidence = outcome.evidence if outcome.evidence else {}
        
        # Add run context
        evidence["run_id"] = run_id
        evidence["rule_id"] = rule_id
        
        # Create the incident
        incident = self.incident_registry.create_incident(
            dataset_id=dataset_id,
            run_id=run_id,
            quality_run_id=run_id,
            rule_id=rule_id,
            severity=severity,
            description=f"{reason}: {field_name}" if field_name else reason,
            evidence=evidence,
            owner="system",
        )
        
        self.logger.info(
            f"Created incident {incident.incident_id} for rule {rule_id} "
            f"on dataset {dataset_id} with severity {severity}"
        )
        
        return incident
    
    def orchestrate_anomaly_detection(
        self,
        run_id: str,
        dataset_id: str,
        metric_name: str,
        values: list[float],
        historical_values: list[float] | None = None,
        schema: QualitySchema | None = None,
    ) -> OrchestrationResult:
        """Orchestrate anomaly detection and create associated incidents.
        
        Runs anomaly detection on the given metric values with optional
        historical baseline comparison. Creates incidents for any detected
        anomalies, funneling through the governance workflow for approved
        remediation.
        
        Returns:
            OrchestrationResult with anomaly detection summary.
        """
        result = OrchestrationResult(run_id=run_id, status=OrchestrationStatus.PROCESSING)
        
        try:
            # Run anomaly detection with fallback for insufficient history
            anomalies, historical_sufficient = detect_with_fallback(
                dataset_id=dataset_id,
                metric_name=metric_name,
                values=values,
                historical_values=historical_values,
            )
            
            result.anomalies_detected = len(anomalies)
            
            # Create incidents for detected anomalies
            for anomaly in anomalies:
                self._create_incident_from_anomaly(
                    run_id=run_id,
                    dataset_id=dataset_id,
                    anomaly=anomaly,
                )
            
            # If historical data was insufficient, record as informational
            if not historical_sufficient:
                result.errors.append(f"Anomaly detection deferred for {metric_name}: insufficient historical data")
            
            result.status = OrchestrationStatus.COMPLETED
            
        except Exception as e:
            self.logger.error(f"Anomaly orchestration failed for run {run_id}: {e}")
            result.status = OrchestrationStatus.FAILED
            result.errors.append(str(e))
        
        return result
    
    def _create_incident_from_anomaly(
        self,
        run_id: str,
        dataset_id: str,
        anomaly: AnomalyResult,
    ) -> Optional[Incident]:
        """Create an incident from an anomaly result."""
        
        # Map anomaly severity to incident severity
        severity_map = {
            "critical": "CRITICAL",
            "high": "WARNING",
            "medium": "INFO",
            "low": "INFO",
            "info": "INFO",
        }
        
        incident_severity = severity_map.get(anomaly.severity, "INFO")
        
        # Build evidence combining anomaly data
        evidence = {
            "detection_method": anomaly.detection_method,
            "threshold": anomaly.threshold,
            "observed_value": anomaly.observed_value,
            "baseline_value": anomaly.baseline_value,
            "expected_range": list(anomaly.expected_range) if anomaly.expected_range else None,
            "confidence": anomaly.confidence,
            "is_data_quality_failure": anomaly.is_data_quality_failure,
            "explanation": anomaly.explanation,
        }
        
        # Create the incident
        incident = self.incident_registry.create_incident(
            dataset_id=dataset_id,
            run_id=run_id,
            quality_run_id=run_id,
            anomaly_id=anomaly.dataset_id if anomaly.dataset_id else "",
            severity=incident_severity,
            description=anomaly.explanation,
            evidence=evidence,
            owner="system",
        )
        
        self.logger.info(
            f"Created incident {incident.incident_id} from anomaly "
            f"metric={anomaly.metric} severity={incident_severity}"
        )
        
        return incident
    
    def propose_remediation_for_incident(
        self,
        incident_id: str,
        transformation_type: str,
        target_dataset_id: str,
        source_column: str | None = None,
        target_column: str | None = None,
        old_value: Any = None,
        new_value: Any = None,
        filter_condition: dict[str, Any] | None = None,
        requester: str = "system",
    ) -> dict[str, Any]:
        """Propose remediation for an existing incident.
        
        Creates a remediation transformation and linked governance decision.
        The transformation cannot be executed until the governance decision
        is explicitly approved.
        
        Returns:
            Dict with proposal details including decision ID for tracking.
        """
        # Use the orchestrator's propose_remediation method
        orchestrator = RemediationOrchestrator(
            incident_registry=self.incident_registry,
            decision_registry=self.decision_registry,
            remediation_registry=self.remediation_registry,
        )
        
        proposal = orchestrator.propose_remediation(
            incident_id=incident_id,
            transformation_type=transformation_type,
            target_dataset_id=target_dataset_id,
            source_column=source_column,
            target_column=target_column,
            old_value=old_value,
            new_value=new_value,
            filter_condition=filter_condition,
            requester=requester,
        )
        
        return proposal
    
    def propose_remediation(
        self,
        incident_id: str,
        transformation_type: str,
        target_dataset_id: str,
        source_column: str | None = None,
        target_column: str | None = None,
        old_value: Any = None,
        new_value: Any = None,
        filter_condition: dict[str, Any] | None = None,
        requester: str = "system",
    ) -> dict[str, Any]:
        """Propose remediation for an incident.
        
        Creates a remediation transformation and linked governance decision.
        The transformation cannot be executed until the governance decision
        is explicitly approved.
        
        Returns:
            Dict with proposal details including decision ID for tracking.
        """
        return self.propose_remediation_for_incident(
            incident_id=incident_id,
            transformation_type=transformation_type,
            target_dataset_id=target_dataset_id,
            source_column=source_column,
            target_column=target_column,
            old_value=old_value,
            new_value=new_value,
            filter_condition=filter_condition,
            requester=requester,
        )
    
    def approve_incident_remediation(self, decision_id: str, reviewer: str) -> dict[str, Any]:
        """Approve a remediation governance decision for an incident.
        
        Transitions the decision through the proper state machine path
        (DRAFT -> PENDING_REVIEW -> APPROVED) and marks the associated
        transformation as ready for execution.
        
        Returns:
            Dict with approval details.
        """
        orchestrator = RemediationOrchestrator(
            incident_registry=self.incident_registry,
            decision_registry=self.decision_registry,
            remediation_registry=self.remediation_registry,
        )
        
        approval = orchestrator.approve_incident_remediation(decision_id=decision_id, reviewer=reviewer)
        
        return approval
    
    def execute_approved_remediation(self, transaction_id: str, executor: str = "system") -> dict[str, Any]:
        """Execute an approved remediation transaction.
        
        Applies approved transformations to the dataset with full validation
        and rollback capability.
        
        Returns:
            Dict with execution details.
        """
        orchestrator = RemediationOrchestrator(
            incident_registry=self.incident_registry,
            decision_registry=self.decision_registry,
            remediation_registry=self.remediation_registry,
        )
        
        execution = orchestrator.execute_remediation(transaction_id=transaction_id, executor=executor)
        
        return execution
    
    def rollback_approved_remediation(self, transaction_id: str, actor: str = "system") -> dict[str, Any]:
        """Rollback an executed remediation transaction.
        
        Restores the dataset to its pre-remediation state.
        
        Returns:
            Dict with rollback details.
        """
        orchestrator = RemediationOrchestrator(
            incident_registry=self.incident_registry,
            decision_registry=self.decision_registry,
            remediation_registry=self.remediation_registry,
        )
        
        rollback = orchestrator.rollback_remediation(transaction_id=transaction_id, actor=actor)
        
        return rollback
    
    def get_orchestration_summary(self, dataset_id: str | None = None) -> dict[str, Any]:
        """Get a summary of all orchestration activity."""
        
        incidents = self.incident_registry.list_incidents(dataset_id=dataset_id)
        transactions = self.remediation_registry.list_transactions(dataset_id=dataset_id)
        decisions = self.decision_registry.count_by_state()
        
        summary = {
            "total_incidents": len(incidents),
            "incidents_by_severity": {},
            "total_transactions": len(transactions),
            "transactions_by_status": {status: sum(1 for t in transactions if t.status == status) for status in ["PENDING", "APPROVED", "EXECUTED", "ROLLED_BACK", "REJECTED"]},
            "decisions_by_state": decisions,
            "dataset_id": dataset_id,
        }
        
        return summary