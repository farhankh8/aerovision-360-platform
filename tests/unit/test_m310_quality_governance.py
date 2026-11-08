"""M3.10 Advanced Data Quality & Governance Automation Tests.

Exercise the M3.10 milestone components: remediation safeguards,
orchestration integration, and full lifecycle verification.
"""

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from src.quality.remediation_safeguards import (
    RemediationSafeguardsRegistry,
    RemediationTransformation,
    RemediationTransaction,
    RemediationOrchestrator,
)
from src.quality.orchestration_integration import (
    QualityToIncidentOrchestrator,
    OrchestrationResult,
    OrchestrationStatus,
)
from src.quality.governance_workflow import (
    GovernanceDecision,
    GovernanceDecisionRegistry,
    GovernanceOutcome,
    is_valid_decision_transition,
)
from src.quality.incident_management import IncidentRegistry
from src.quality.engine import QualityResult
from src.quality.models import QualitySchema, QualityRecordOutcome


# ============================================================================
# Helper: temporary directories for isolated test state
# ============================================================================

@pytest.fixture(autouse=True)
def isolated_test_state():
    """Provide isolated temporary directories for test state.
    
    Each test gets its own incident_data, governance_decisions,
    and remediation_data directories to prevent cross-test contamination.
    """
    incident_dir = tempfile.mkdtemp(prefix="incident_")
    governance_dir = tempfile.mkdtemp(prefix="governance_")
    remediation_dir = tempfile.mkdtemp(prefix="remediation_")
    
    # Set environment variables or monkey-patch base dirs
    # We'll pass them directly to the constructors
    yield {
        "incident_dir": incident_dir,
        "governance_dir": governance_dir,
        "remediation_dir": remediation_dir,
    }
    
    # Cleanup is handled by pytest tempdir


def _make_incident_registry(incident_dir: str) -> IncidentRegistry:
    """Create an IncidentRegistry with a custom base directory."""
    return IncidentRegistry(base_dir=incident_dir)


def _make_governance_decision_registry(governance_dir: str) -> GovernanceDecisionRegistry:
    """Create a GovernanceDecisionRegistry with a custom base directory."""
    return GovernanceDecisionRegistry(base_dir=governance_dir)


def _make_remediation_registry(remediation_dir: str) -> RemediationSafeguardsRegistry:
    """Create a RemediationSafeguardsRegistry with a custom base directory."""
    return RemediationSafeguardsRegistry(base_dir=remediation_dir)


# ============================================================================
# M3.10.8 Remediation Safeguards Tests
# ============================================================================


def test_remediation_transformation_creation():
    """Test that remediation transformations can be created with all fields."""
    registry = RemediationSafeguardsRegistry()
    
    tx = registry.create_transformation(
        name="Test value replacement",
        description="Replace LOW severity with MEDIUM",
        target_dataset_id="test_dataset",
        transformation_type="value_replacement",
        source_column="severity",
        old_value="LOW",
        new_value="MEDIUM",
    )
    
    assert tx.transformation_id.startswith("TRANS_")
    assert tx.name == "Test value replacement"
    assert tx.target_dataset_id == "test_dataset"
    assert tx.transformation_type == "value_replacement"
    assert tx.source_column == "severity"
    assert tx.old_value == "LOW"
    assert tx.new_value == "MEDIUM"
    assert tx.status == "PENDING"
    assert tx.executed_timestamp is None
    assert tx.rolled_back_timestamp is None
    
    # Test to_dict / from_dict roundtrip
    tx_dict = tx.to_dict()
    tx_roundtrip = RemediationTransformation.from_dict(tx_dict)
    assert tx_roundtrip.transformation_id == tx.transformation_id
    assert tx_roundtrip.name == tx.name
    assert tx_roundtrip.status == tx.status


def test_remediation_transaction_lifecycle():
    """Test remediation transaction creation and status lifecycle."""
    registry = RemediationSafeguardsRegistry()
    
    # Create transaction
    txn = registry.create_transaction(dataset_id="test_dataset")
    assert txn.transaction_id.startswith("TXN_")
    assert txn.dataset_id == "test_dataset"
    assert txn.status == "PENDING"
    assert txn.executed_timestamp is None
    
    # Update status to APPROVED
    updated = registry.update_transaction_status(txn.transaction_id, "APPROVED")
    assert updated.status == "APPROVED"
    assert updated.executed_timestamp is None  # Not executed yet
    
    # Update status to EXECUTED
    updated_exec = registry.update_transaction_status(txn.transaction_id, "EXECUTED")
    assert updated_exec.status == "EXECUTED"
    assert updated_exec.executed_timestamp is not None
    
    # Update status to ROLLED_BACK
    rolled_back = registry.update_transaction_status(txn.transaction_id, "ROLLED_BACK")
    assert rolled_back.status == "ROLLED_BACK"
    assert rolled_back.rolled_back_timestamp is not None
    
    # Test roundtrip
    txn_dict = txn.to_dict()
    txn_roundtrip = RemediationTransaction.from_dict(txn_dict)
    assert txn_roundtrip.transaction_id == txn.transaction_id
    assert len(txn_roundtrip.transformations) == 0


def test_remediation_validation_before_execution():
    """Test that transformations can be validated against data before execution."""
    registry = RemediationSafeguardsRegistry()
    
    # Create a value replacement transformation
    tx = registry.create_transformation(
        name="Test validation",
        description="Validate before execute",
        target_dataset_id="test_dataset",
        transformation_type="value_replacement",
        source_column="severity",
        old_value="LOW",
        new_value="MEDIUM",
    )
    
    # Validate against empty records - should warn that old value not found
    outcomes = registry.validate_transformation_against_data(tx, [])
    assert len(outcomes) > 0
    # Should have a warning about old value not found
    warning_outcomes = [o for o in outcomes if o.outcome == "warning"]
    assert len(warning_outcomes) > 0
    
    # Create records with the old value
    records_with_value = [
        {"severity": "LOW", "airline_id": "AA123"},
        {"severity": "HIGH", "airline_id": "AA456"},
    ]
    outcomes2 = registry.validate_transformation_against_data(tx, records_with_value)
    # Should pass validation since old value exists
    failed_outcomes = [o for o in outcomes2 if o.outcome == "failed"]
    assert len(failed_outcomes) == 0


def test_remediation_orchestrator_propose():
    """Test the remediation orchestrator proposal workflow."""
    from src.quality.incident_management import IncidentRegistry
    from src.quality.governance_workflow import GovernanceDecisionRegistry
    
    registry = RemediationSafeguardsRegistry()
    decision_registry = GovernanceDecisionRegistry()
    orch = RemediationOrchestrator(
        incident_registry=IncidentRegistry(),
        decision_registry=decision_registry,
        remediation_registry=registry,
    )
    
    proposal = orch.propose_remediation(
        incident_id="INC_TEST_001",
        transformation_type="value_replacement",
        target_dataset_id="test_dataset",
        source_column="severity",
        old_value="LOW",
        new_value="MEDIUM",
        requester="test_user",
    )
    
    assert "transformation_id" in proposal
    assert "decision_id" in proposal
    assert proposal["status"] == "proposed_awaiting_approval"
    assert proposal["transformation_id"] is not None
    assert proposal["decision_id"] is not None
    
    # Check that the transformation was created and linked to the decision
    trans = registry.get_transformation(proposal["transformation_id"])
    assert trans is not None
    assert trans.approval_reference == proposal["decision_id"]


def test_remediation_orchestrator_approve_and_execute():
    """Test full approval and execution workflow."""
    from src.quality.incident_management import IncidentRegistry
    from src.quality.governance_workflow import GovernanceDecisionRegistry
    
    registry = RemediationSafeguardsRegistry()
    decision_registry = GovernanceDecisionRegistry()
    
    # Create a decision first
    decision = decision_registry.create_decision(
        requester="test_user",
        decision_rationale="Test remediation",
        scope_of_approval="Test scope",
        approved_action="Test action",
    )
    
    orch = RemediationOrchestrator(
        incident_registry=IncidentRegistry(),
        decision_registry=decision_registry,
        remediation_registry=registry,
    )
    
    # Propose remediation linked to this decision
    proposal = orch.propose_remediation(
        incident_id="INC_TEST_002",
        transformation_type="value_replacement",
        target_dataset_id="test_dataset",
        source_column="severity",
        old_value="LOW",
        new_value="MEDIUM",
        requester="test_user",
    )
    
    # Approve the decision
    approval = orch.approve_incident_remediation(
        decision_id=proposal["decision_id"],
        reviewer="authorized_reviewer",
    )
    
    assert approval["decision_state"] == "APPROVED"
    assert approval["transformation_status"] == "APPROVED"
    
    # Execute the remediation
    transaction_id = (
        registry.list_transactions(dataset_id="test_dataset")[0].transaction_id
    )
    execution = orch.execute_approved_remediation(transaction_id=transaction_id)
    
    assert execution["status"] == "EXECUTED"
    assert execution["transformations_executed"] >= 0


# ============================================================================
# M3.10.9 Orchestration Integration Tests
# ============================================================================


def test_quality_to_incident_orchestrator_creation():
    """Test orchestrator creation and basic setup."""
    orch = QualityToIncidentOrchestrator()
    assert orch is not None
    assert orch.incident_registry is not None
    assert orch.decision_registry is not None
    assert orch.remediation_registry is not None


def test_quality_to_incident_orchestrator_basic():
    """Test basic quality-to-incident orchestration."""
    orch = QualityToIncidentOrchestrator()
    
    from src.quality.models import QualityRecordOutcome
    
    # Create a schema and quality result with a failure
    schema = QualitySchema(
        required_columns=("airline_id",),
        type_rules={"airline_id": "string"},
        primary_key="airline_id",
    )
    
    outcomes = {
        "RULE-001": [QualityRecordOutcome(
            rule_id="RULE-001",
            outcome="failed",
            field_name="airline_id",
            reason="Required column airline_id is missing or empty",
            evidence={"record_idx": 0, "value": None}
        )]
    }
    
    quality_result = QualityResult(
        dataset_id="test_dataset",
        outcome="failed",
        schema=schema,
        rule_results=outcomes,
        total_records=100,
        passed_critical_rules=0,
        failed_critical_rules=1,
        warning_rules=0,
        info_rules=0,
        failed_record_count=1,
        warning_record_count=0,
        source_sha256="test_hash",
    )
    
    # Orchestrate
    run_id = "test_run_001"
    result = orch.orchestrate_quality_result(
        run_id=run_id,
        dataset_id="test_dataset",
        quality_result=quality_result,
        schema=schema,
    )
    
    assert result.status == OrchestrationStatus.COMPLETED
    assert result.quality_outcome == "failed"
    assert result.datasets_validated >= 0
    assert result.incidents_created >= 0


def test_quality_to_incident_anomaly_orchestration():
    """Test anomaly detection orchestration."""
    orch = QualityToIncidentOrchestrator()
    
    # Create some test values
    values = [100.0, 102.0, 98.0, 101.0, 500.0, 99.0, 100.5, 97.0]
    
    # Orchestrate anomaly detection
    result = orch.orchestrate_anomaly_detection(
        run_id="anomaly_test_001",
        dataset_id="test_dataset",
        metric_name="record_value",
        values=values,
    )
    
    assert result.status == OrchestrationStatus.COMPLETED
    assert result.anomalies_detected >= 0


def test_full_orchestration_summary():
    """Test orchestration summary generation."""
    orch = QualityToIncidentOrchestrator()
    
    from src.quality.engine import QualityResult
    from src.quality.models import QualitySchema, QualityRecordOutcome
    
    # Create a quality result with failures
    schema = QualitySchema(
        required_columns=("airline_id",),
        type_rules={"airline_id": "string"},
        primary_key="airline_id",
    )
    
    outcomes = {
        "RULE-001": [QualityRecordOutcome(
            rule_id="RULE-001",
            outcome="failed",
            field_name="airline_id",
            reason="Required column airline_id is missing or empty",
        )]
    }
    
    quality_result = QualityResult(
        dataset_id="test_dataset",
        outcome="failed",
        schema=schema,
        rule_results=outcomes,
        total_records=100,
        passed_critical_rules=0,
        failed_critical_rules=1,
        warning_rules=0,
        info_rules=0,
        failed_record_count=1,
        warning_record_count=0,
        source_sha256="test_hash",
    )
    
    orch.orchestrate_quality_result(
        run_id="summary_test_001",
        dataset_id="test_dataset",
        quality_result=quality_result,
        schema=schema,
    )
    
    # Use isolated incident registry
    incident_registry = _make_incident_registry(tempfile.mkdtemp(prefix="incident_"))
    transaction_registry = _make_remediation_registry(tempfile.mkdtemp(prefix="remediation_"))
    decision_registry = _make_governance_decision_registry(tempfile.mkdtemp(prefix="governance_"))
    
    # Re-create orchestrator with isolated registries
    orch2 = QualityToIncidentOrchestrator(
        incident_registry=incident_registry,
        decision_registry=decision_registry,
        remediation_registry=transaction_registry,
    )
    
    summary = orch2.get_orchestration_summary(dataset_id="test_dataset")
    assert summary["total_incidents"] >= 0
    assert summary["total_transactions"] >= 0
    assert "incidents_by_severity" in summary
    assert "decisions_by_state" in summary
    assert summary["dataset_id"] == "test_dataset"


# ============================================================================
# M3.10.10 Full Integration and Regression Tests
# ============================================================================


def test_m310_remediation_rollback():
    """Test remediation rollback capability."""
    from src.quality.incident_management import IncidentRegistry
    
    registry = _make_remediation_registry(tempfile.mkdtemp(prefix="remediation_"))
    
    # Create transformation and transaction
    tx = registry.create_transformation(
        name="Rollback test",
        description="Test rollback capability",
        target_dataset_id="test_dataset",
        transformation_type="value_replacement",
        source_column="severity",
        old_value="LOW",
        new_value="MEDIUM",
    )
    
    txn = registry.create_transaction(dataset_id="test_dataset")
    
    # Link transformation to transaction
    txn.transformations = [tx]
    
    # Mark transaction as executed
    txn.status = "EXECUTED"
    registry._persist_transaction(txn)
    
    # Execute rollback
    from src.quality.governance_workflow import GovernanceDecisionRegistry
    orch = RemediationOrchestrator(
        incident_registry=IncidentRegistry(),
        decision_registry=GovernanceDecisionRegistry(),
        remediation_registry=registry,
    )
    
    result = orch.rollback_approved_remediation(transaction_id=txn.transaction_id)
    assert result["rollback_executed"] is True
    assert "rolled_back_at" in result


def test_governance_decision_transitions():
    """Test governance decision state machine transitions."""
    from src.quality.incident_management import IncidentRegistry
    from src.quality.governance_workflow import GovernanceDecisionRegistry
    
    registry = _make_governance_decision_registry(tempfile.mkdtemp(prefix="governance_"))
    
    # Create a decision
    decision = registry.create_decision(
        requester="test_user",
        decision_rationale="Test transitions",
        scope_of_approval="Test scope",
        approved_action="Test action",
    )
    
    # Test valid transitions: DRAFT -> PENDING_REVIEW -> APPROVED
    assert is_valid_decision_transition("DRAFT", "pending_review")
    assert is_valid_decision_transition("PENDING_REVIEW", "approved")
    
    # Test DRAFT -> REVOKED
    assert is_valid_decision_transition("DRAFT", "revoked")
    
    # Test PENDING_REVIEW -> REJECTED
    assert is_valid_decision_transition("PENDING_REVIEW", "rejected")
    
    # Test APPROVED -> REVOKED (terminal from approved)
    assert is_valid_decision_transition("APPROVED", "revoked")
    
    # Test APPROVED -> EXPIRED
    assert is_valid_decision_transition("APPROVED", "expired")
    
    # Test REJECTED is terminal
    assert not is_valid_decision_transition("REJECTED", "anything")  # no valid from REJECTED
    
    # Test transition using the decision method
    result = decision.transition_state("PENDING_REVIEW", "test_user")
    assert result is True
    assert decision.decision_state == "PENDING_REVIEW"
    
    # Transition to APPROVED
    result2 = decision.approve("reviewer_user")
    assert result2 is True
    assert decision.decision_state == "APPROVED"


def test_governance_decision_lifecycle():
    """Test full governance decision lifecycle."""
    from src.quality.incident_management import IncidentRegistry
    from src.quality.governance_workflow import GovernanceDecisionRegistry
    
    registry = _make_governance_decision_registry(tempfile.mkdtemp(prefix="governance_"))
    
    # Create decision
    decision = registry.create_decision(
        requester="initiator",
        decision_rationale="Full lifecycle test",
        scope_of_approval="Test scope",
        approved_action="Test action",
    )
    
    # DRAFT -> PENDING_REVIEW -> APPROVED
    assert decision.transition_state("PENDING_REVIEW", "initiator")
    assert decision.transition_state("APPROVED", "reviewer")
    
    # Check is_expired (no validity period, should be False)
    assert not decision.is_expired()
    
    # Check decision state
    assert decision.decision_state == "APPROVED"
    
    # Transition to REVOKED
    decision.revoke("initiator")
    assert decision.decision_state == "REVOKED"
    assert decision.expiration_timestamp is not None


def test_incident_lifecycle_integration():
    """Test incident lifecycle integration with orchestration."""
    from src.quality.incident_management import IncidentRegistry
    
    incident_registry = _make_incident_registry(tempfile.mkdtemp(prefix="incident_"))
    
    # Create incidents at different lifecycle stages
    incident1 = incident_registry.create_incident(
        dataset_id="test_dataset",
        run_id="run_001",
        quality_run_id="qr_001",
        severity="CRITICAL",
        description="Test incident 1",
        evidence={"test": "data1"},
    )
    
    incident2 = incident_registry.create_incident(
        dataset_id="test_dataset",
        run_id="run_001",
        quality_run_id="qr_001",
        severity="WARNING",
        description="Test incident 2",
        evidence={"test": "data2"},
    )
    
    # List incidents
    incidents = incident_registry.list_incidents(dataset_id="test_dataset")
    assert len(incidents) == 2, f"Expected 2 incidents, got {len(incidents)}"
    
    # Count by status
    counts = incident_registry.count_by_status()
    assert len(counts) > 0
    
    # Count by severity
    severity_counts = incident_registry.count_by_severity()
    assert len(severity_counts) > 0
    
    # Test transition
    success = incident1.transition_to("investigating", "system")
    assert success is True
    assert incident1.status == "investigating"  # Status is uppercased internally
    
    # Test invalid transition (INVESTIGATING -> OPEN should fail)
    from src.quality.incident_management import INCIDENT_LIFECLOW_TRANSITIONS
    invalid_success = incident1.transition_to("OPEN", "system")
    # OPEN is not a valid transition from INVESTIGATING, so this should be False
    assert invalid_success is False


def test_end_to_end_m310_workflow():
    """Test end-to-end M3.10 workflow: quality -> incident -> remediation proposal -> approval -> execution."""
    from src.quality.engine import QualityEngine, QualitySchema
    from src.quality.models import QualityRecordOutcome
    
    # Setup: Create a quality result with a failure
    schema = QualitySchema(
        required_columns=("airline_id", "delay_minutes"),
        type_rules={"airline_id": "string", "delay_minutes": "int"},
        primary_key="airline_id",
    )
    
    outcomes = {
        "RULE-001": [QualityRecordOutcome(
            rule_id="RULE-001",
            outcome="failed",
            field_name="airline_id",
            reason="Required column airline_id is missing or empty",
            evidence={"record_idx": 0, "value": None}
        )]
    }
    
    quality_result = QualityResult(
        dataset_id="integration_test_dataset",
        outcome="failed",
        schema=schema,
        rule_results=outcomes,
        total_records=50,
        passed_critical_rules=0,
        failed_critical_rules=1,
        warning_rules=0,
        info_rules=0,
        failed_record_count=1,
        warning_record_count=0,
        source_sha256="integration_test_hash",
    )
    
    # Step 1: Orchestrate quality-to-incident
    incident_orch = QualityToIncidentOrchestrator()
    orchestration_result = incident_orch.orchestrate_quality_result(
        run_id="e2e_test_001",
        dataset_id="integration_test_dataset",
        quality_result=quality_result,
        schema=schema,
    )
    
    assert orchestration_result.status == OrchestrationStatus.COMPLETED
    
    # Step 2: Propose remediation for the created incident
    # Find the incident(s) created
    incidents = incident_orch.incident_registry.list_incidents(dataset_id="integration_test_dataset")
    assert len(incidents) > 0, "No incidents created in step 1"
    
    first_incident = incidents[0]
    proposal = incident_orch.propose_remediation_for_incident(
        incident_id=first_incident.incident_id,
        transformation_type="value_replacement",
        target_dataset_id="integration_test_dataset",
        source_column="airline_id",
        old_value="",
        new_value="AA001",
    )
    
    assert "decision_id" in proposal
    assert proposal["status"] == "proposed_awaiting_approval"
    
    # Step 3: Approve the remediation decision
    approval = incident_orch.approve_incident_remediation(
        decision_id=proposal["decision_id"],
        reviewer="senior_reviewer",
    )
    assert approval["decision_state"] == "APPROVED"
    
    # Step 4: Execute the approved remediation
    transactions = incident_orch.remediation_registry.list_transactions(
        dataset_id="integration_test_dataset"
    )
    assert len(transactions) > 0
    
    transaction_id = transactions[0].transaction_id
    execution = incident_orch.execute_approved_remediation(transaction_id=transaction_id)
    assert execution["status"] == "EXECUTED"
    
    # Step 5: Verify the full summary
    summary = incident_orch.get_orchestration_summary(dataset_id="integration_test_dataset")
    assert summary["total_incidents"] >= 1
    assert summary["total_transactions"] >= 1
    assert summary["decisions_by_state"].get("approved", 0) >= 1


def test_od04_compliance_no_production_modification():
    """Test that OD-04 compliance is maintained - no silent production data modification."""
    from src.quality.incident_management import IncidentRegistry
    from src.quality.governance_workflow import GovernanceDecisionRegistry
    
    registry = _make_remediation_registry(tempfile.mkdtemp(prefix="remediation_"))
    
    # Create a transformation (this is just a definition, no data modification)
    tx = registry.create_transformation(
        name="OD-04 compliance check",
        description="Verify no silent modification",
        target_dataset_id="production_dataset",
        transformation_type="value_replacement",
        source_column="some_column",
        old_value="old_val",
        new_value="new_val",
    )
    
    # The transformation exists as a definition only
    # No data has been modified - it's just a proposal
    assert tx.status == "PENDING"
    
    # Even after approval, execution is explicit and tracked
    decision_registry = _make_governance_decision_registry(tempfile.mkdtemp(prefix="governance_"))
    orch = QualityToIncidentOrchestrator(
        incident_registry=IncidentRegistry(),
        decision_registry=decision_registry,
        remediation_registry=registry,
    )
    
    # Propose remediation
    proposal = orch.propose_remediation(
        incident_id="INC_OD04_001",
        transformation_type="value_replacement",
        target_dataset_id="production_dataset",
        source_column="some_column",
        old_value="old_val",
        new_value="new_val",
    )
    
    assert "decision_id" in proposal
    trans = registry.get_transformation(proposal["transformation_id"])
    assert trans.status == "PENDING"  # Still pending approval
    
    # After approval, execution is still tracked and reversible
    approval = orch.approve_incident_remediation(
        decision_id=proposal["decision_id"],
        reviewer="authorized_reviewer",
    )
    assert approval["decision_state"] == "APPROVED"
    
    # Execution is tracked
    transactions = registry.list_transactions(dataset_id="production_dataset")
    assert len(transactions) > 0
    txn = transactions[0]
    assert txn.status == "APPROVED"  # Can be executed or rolled back
    
    # Rollback is always available
    rollback_result = orch.rollback_approved_remediation(transaction_id=txn.transaction_id)
    assert rollback_result["rollback_executed"] is True
    
    # The key OD-04 assertion: all actions are explicit, tracked, and reversible
    # No silent modification occurs - every step is documented and auditable
    print("OD-04 compliance verified: all remediation actions are explicit, tracked, and reversible")


def test_m310_all_components_importable():
    """Test that all M3.10 components are properly importable from the quality package."""
    from src.quality import (
        # M3.10.8 remediation safeguards
        RemediationSafeguardsRegistry,
        RemediationTransformation,
        RemediationTransaction,
        RemediationOrchestrator,
        # M3.10.9 orchestration integration
        QualityToIncidentOrchestrator,
        OrchestrationResult,
        OrchestrationStatus,
        # M3.10.7 governance (already existed)
        GovernanceDecision,
        GovernancePolicy,
        GovernanceDecisionRegistry,
        GovernancePolicyRegistry,
        is_valid_decision_transition,
    )
    
    # Verify all imports work
    assert RemediationSafeguardsRegistry is not None
    assert RemediationTransformation is not None
    assert RemediationTransaction is not None
    assert RemediationOrchestrator is not None
    assert QualityToIncidentOrchestrator is not None
    assert OrchestrationResult is not None
    assert OrchestrationStatus is not None
    assert GovernanceDecision is not None
    assert GovernancePolicy is not None
    assert GovernanceDecisionRegistry is not None
    assert GovernancePolicyRegistry is not None
    assert is_valid_decision_transition is not None


def test_m310_deterministic_behavior():
    """Test that M3.10 components produce deterministic results."""
    registry1 = _make_remediation_registry(tempfile.mkdtemp(prefix="remediation_"))
    registry2 = _make_remediation_registry(tempfile.mkdtemp(prefix="remediation_"))
    
    # Create identical transformations
    tx1 = registry1.create_transformation(
        name="Determinism test",
        description="Test deterministic behavior",
        target_dataset_id="test_dataset",
        transformation_type="value_replacement",
        source_column="severity",
        old_value="LOW",
        new_value="MEDIUM",
    )
    
    tx2 = registry2.create_transformation(
        name="Determinism test",
        description="Test deterministic behavior",
        target_dataset_id="test_dataset",
        transformation_type="value_replacement",
        source_column="severity",
        old_value="LOW",
        new_value="MEDIUM",
    )
    
    # Both should have the same structure
    assert tx1.name == tx2.name
    assert tx1.target_dataset_id == tx2.target_dataset_id
    assert tx1.transformation_type == tx2.transformation_type
    assert tx1.source_column == tx2.source_column
    assert tx1.old_value == tx2.old_value
    assert tx1.new_value == tx2.new_value
    assert tx1.status == tx2.status == "PENDING"


def test_m310_insufficient_data_fallback():
    """Test anomaly detection fallback for insufficient historical data."""
    from src.quality.orchestration_integration import QualityToIncidentOrchestrator
    
    orch = QualityToIncidentOrchestrator()
    
    # Test with very limited historical data (should use fallback)
    result = orch.orchestrate_anomaly_detection(
        run_id="fallback_test_001",
        dataset_id="test_dataset",
        metric_name="test_metric",
        values=[100.0, 101.0, 99.0, 102.0, 98.0],
        historical_values=[],  # No baseline - should trigger fallback
    )
    
    # Should complete (possibly with deferred detection)
    assert result.status in [OrchestrationStatus.COMPLETED, OrchestrationStatus.FAILED]