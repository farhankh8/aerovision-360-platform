"""Governance Approval Workflow for AEROVISION 360.

Provides a traceable governance decision workflow for quality remediation
approvals. Supports approval requests, decision status, authorized reviewer
identity, decision rationale, scope of approval, and audit history.

Possible decision states:
  DRAFT
  PENDING_REVIEW
  APPROVED
  REJECTED
  EXPIRED
  REVOKED

Enforces authorization and valid state transitions.
An approval must be explicitly recorded by an authorized actor.
Does not generate fake approval identities.
Does not mark an action approved simply because a test passes.
Does not assume a project owner has approved an unresolved policy.
"""

from __future__ import annotations

import json
import os
import uuid
from enum import Enum
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from dataclasses import dataclass, field

from src.quality.models import QualityOutcome


class GovernanceOutcome(str, Enum):
    """Outcome of a governance decision."""
    
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    REVOKED = "revoked"


# ---------------------------------------------------------------------------
# Governance decision state machine - valid transitions
# ---------------------------------------------------------------------------

GOVERNANCE_DECISION_TRANSITIONS: dict[str, set[str]] = {
    "DRAFT": {"pending_review", "revoked"},
    "PENDING_REVIEW": {"approved", "rejected", "revoked", "expired"},
    "APPROVED": {"revoked", "expired"},
    "REJECTED": set(),  # Terminal state
    "EXPIRED": set(),  # Terminal state
    "REVOKED": set(),  # Terminal state
}


# ============================================================================
# Governance decision state machine - valid transitions
# ============================================================================

GOVERNANCE_DECISION_TRANSITIONS: dict[str, set[str]] = {
    "DRAFT": {"pending_review", "revoked"},
    "PENDING_REVIEW": {"approved", "rejected", "revoked", "expired"},
    "APPROVED": {"revoked", "expired"},
    "REJECTED": set(),  # Terminal state
    "EXPIRED": set(),  # Terminal state
    "REVOKED": set(),  # Terminal state
}


def is_valid_decision_transition(from_state: str, to_state: str) -> bool:
    """Check if a decision state transition is valid.

    The GOVERNANCE_DECISION_TRANSITIONS dict uses uppercase keys
    (DRAFT, PENDING_REVIEW, etc.) and lowercase values
    (pending_review, approved, etc.). Both are normalized here.
    """
    from_state_upper = from_state.upper()
    to_state_lower = to_state.lower()
    allowed = GOVERNANCE_DECISION_TRANSITIONS.get(from_state_upper, set())
    return to_state_lower in allowed


class GovernanceDecision:
    """Represents a governance approval decision."""
    
    decision_id: str
    requester: str
    reviewer: str | None
    decision_state: str  # DRAFT, PENDING_REVIEW, APPROVED, REJECTED, EXPIRED, REVOKED
    decision_rationale: str
    scope_of_approval: str
    approved_action: str
    rejection_reason: str | None = None
    expiration_timestamp: datetime | None = None
    created_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    validity_period_hours: int | None = None
    audit_trail: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize audit trail on creation."""
        if not self.audit_trail:
            self.audit_trail = [
                {
                    "timestamp": self.created_timestamp.isoformat(),
                    "actor": self.requester,
                    "action": "decision_created",
                    "state_before": None,
                    "state_after": self.decision_state,
                }
            ]

    def transition_state(self, new_state: str, actor: str) -> bool:
        """Attempt to transition decision to new status.

        Returns True if transition is valid, False otherwise.
        """
        # Normalize state names for comparison (case-insensitive)
        from_state = self.decision_state.upper()
        to_state = new_state.upper()
        
        if not is_valid_decision_transition(from_state, to_state):
            return False


# ============================================================================
# Governance decision model
# ============================================================================

@dataclass
class GovernanceDecision:
    """Represents a governance approval decision."""

    decision_id: str
    requester: str
    reviewer: str | None
    decision_state: str  # DRAFT, PENDING_REVIEW, APPROVED, REJECTED, EXPIRED, REVOKED
    decision_rationale: str
    scope_of_approval: str
    approved_action: str
    rejection_reason: str | None = None
    expiration_timestamp: datetime | None = None
    created_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    validity_period_hours: int | None = None
    audit_trail: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize audit trail on creation."""
        if not self.audit_trail:
            self.audit_trail = [
                {
                    "timestamp": self.created_timestamp.isoformat(),
                    "actor": self.requester,
                    "action": "decision_created",
                    "state_before": None,
                    "state_after": self.decision_state,
                }
            ]

    def transition_state(self, new_state: str, actor: str) -> bool:
        """Attempt to transition decision to new status.

        Returns True if transition is valid, False otherwise.
        """
        if not is_valid_decision_transition(self.decision_state, new_state):
            return False

        # Record the transition in audit trail
        self.audit_trail.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "actor": actor,
                "action": f"state_transition_to_{new_state}",
                "state_before": self.decision_state,
                "state_after": new_state,
            }
        )

        # Update state and timestamps
        self.decision_state = new_state
        self.updated_timestamp = datetime.now(timezone.utc)

        # If transitioning to EXPIRED or REVOKED, set expiration
        if new_state in ("EXPIRED", "REVOKED"):
            self.expiration_timestamp = datetime.now(timezone.utc)

        return True

    def approve(self, reviewer: str) -> bool:
        """Approve the decision (transition to APPROVED)."""
        return self.transition_state("APPROVED", reviewer)

    def reject(self, reviewer: str, rejection_reason: str) -> bool:
        """Reject the decision (transition to REJECTED)."""
        self.rejection_reason = rejection_reason
        return self.transition_state("REJECTED", reviewer)

    def revoke(self, actor: str) -> bool:
        """Revoke the decision (transition to REVOKED)."""
        return self.transition_state("REVOKED", actor)

    def expire(self, actor: str) -> bool:
        """Expire the decision (transition to EXPIRED)."""
        return self.transition_state("EXPIRED", actor)

    def is_expired(self) -> bool:
        """Check if decision has expired based on validity period."""
        if self.expiration_timestamp is not None:
            return datetime.now(timezone.utc) > self.expiration_timestamp
        if self.validity_period_hours is not None:
            created = self.created_timestamp
            # Compute expiry by adding validity_period_hours to created timestamp
            from datetime import timedelta
            expiry = created + timedelta(hours=self.validity_period_hours)
            return datetime.now(timezone.utc) > expiry
        return False

    def to_dict(self) -> dict[str, Any]:
        """Convert decision to dictionary for serialization."""
        return {
            "decision_id": self.decision_id,
            "requester": self.requester,
            "reviewer": self.reviewer,
            "decision_state": self.decision_state,
            "decision_rationale": self.decision_rationale,
            "scope_of_approval": self.scope_of_approval,
            "approved_action": self.approved_action,
            "rejection_reason": self.rejection_reason,
            "expiration_timestamp": (
                self.expiration_timestamp.isoformat() if self.expiration_timestamp else None
            ),
            "created_timestamp": self.created_timestamp.isoformat(),
            "updated_timestamp": self.updated_timestamp.isoformat(),
            "validity_period_hours": self.validity_period_hours,
            "audit_trail": self.audit_trail,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GovernanceDecision":
        """Create decision from dictionary."""
        decision = cls(
            decision_id=data["decision_id"],
            requester=data["requester"],
            reviewer=data.get("reviewer"),
            decision_state=data["decision_state"],
            decision_rationale=data["decision_rationale"],
            scope_of_approval=data["scope_of_approval"],
            approved_action=data["approved_action"],
            rejection_reason=data.get("rejection_reason"),
            expiration_timestamp=(
                datetime.fromisoformat(data["expiration_timestamp"])
                if data.get("expiration_timestamp") is not None
                else None
            ),
            created_timestamp=(
                datetime.fromisoformat(data["created_timestamp"])
                if data.get("created_timestamp")
                else datetime.now(timezone.utc)
            ),
            updated_timestamp=(
                datetime.fromisoformat(data["updated_timestamp"])
                if data.get("updated_timestamp")
                else datetime.now(timezone.utc)
            ),
            validity_period_hours=data.get("validity_period_hours"),
        )
        decision.audit_trail = data.get("audit_trail", [])
        return decision


# ============================================================================
# Governance policy model
# ============================================================================

@dataclass
class GovernancePolicy:
    """Represents a governance policy."""

    policy_id: str
    name: str
    description: str
    scope: str
    rule_ids: tuple[str, ...]
    severity_requirements: str  # "CRITICAL", "WARNING", "INFO"
    thresholds: dict[str, Any]
    effective_date: datetime
    version: str
    owner_or_authority: str
    approval_reference: str | None  # Reference to a governance decision
    status: str  # "active", "suspended", "retired"
    created_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        """Convert policy to dictionary for serialization."""
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "description": self.description,
            "scope": self.scope,
            "rule_ids": list(self.rule_ids),
            "severity_requirements": self.severity_requirements,
            "thresholds": self.thresholds,
            "effective_date": self.effective_date.isoformat(),
            "version": self.version,
            "owner_or_authority": self.owner_or_authority,
            "approval_reference": self.approval_reference,
            "status": self.status,
            "created_timestamp": self.created_timestamp.isoformat(),
            "last_modified": self.last_modified.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GovernancePolicy":
        """Create policy from dictionary."""
        policy = cls(
            policy_id=data["policy_id"],
            name=data["name"],
            description=data["description"],
            scope=data["scope"],
            rule_ids=tuple(data.get("rule_ids", [])),
            severity_requirements=data.get("severity_requirements", "INFO"),
            thresholds=data.get("thresholds", {}),
            effective_date=(
                datetime.fromisoformat(data["effective_date"])
                if data.get("effective_date")
                else datetime.now(timezone.utc)
            ),
            version=data.get("version", "1.0"),
            owner_or_authority=data.get("owner_or_authority", "system"),
            approval_reference=data.get("approval_reference"),
            status=data.get("status", "active"),
            created_timestamp=(
                datetime.fromisoformat(data["created_timestamp"])
                if data.get("created_timestamp")
                else datetime.now(timezone.utc)
            ),
            last_modified=(
                datetime.fromisoformat(data["last_modified"])
                if data.get("last_modified")
                else datetime.now(timezone.utc)
            ),
        )
        return policy


# ============================================================================
# Governance decision registry - persistent storage
# ============================================================================

class GovernanceDecisionRegistry:
    """Persistent storage for governance decisions."""

    def __init__(self, base_dir: str | Path | None = None):
        """Initialize the governance decision registry."""
        if base_dir is not None:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path("governance_decisions")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._decisions: dict[str, GovernanceDecision] = {}
        self._load_existing()

    def _load_existing(self) -> None:
        """Load existing decisions from disk."""
        if not self.base_dir.exists():
            return
        for entry in self.base_dir.iterdir():
            if entry.is_file() and entry.suffix == ".json":
                try:
                    with open(entry, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    decision = GovernanceDecision.from_dict(data)
                    self._decisions[decision.decision_id] = decision
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

    def create_decision(
        self,
        requester: str,
        decision_rationale: str,
        scope_of_approval: str,
        approved_action: str,
        validity_period_hours: int | None = None,
    ) -> GovernanceDecision:
        """Create a new governance decision with DRAFT status."""
        decision = GovernanceDecision(
            decision_id=f"DEC_{uuid.uuid4().hex[:8].upper()}",
            requester=requester,
            reviewer=None,
            decision_state="DRAFT",
            decision_rationale=decision_rationale,
            scope_of_approval=scope_of_approval,
            approved_action=approved_action,
            validity_period_hours=validity_period_hours,
        )
        self._decisions[decision.decision_id] = decision
        self._persist_decision(decision)
        return decision

    def get_decision(self, decision_id: str) -> GovernanceDecision | None:
        """Retrieve a decision by ID."""
        return self._decisions.get(decision_id)

    def list_decisions(
        self,
        requester: str | None = None,
        state: str | None = None,
    ) -> list[GovernanceDecision]:
        """List decisions, optionally filtered by requester or state."""
        decisions = list(self._decisions.values())
        if requester:
            decisions = [d for d in decisions if d.requester == requester]
        if state:
            decisions = [d for d in decisions if d.decision_state == state]
        decisions.sort(key=lambda d: d.created_timestamp, reverse=True)
        return decisions

    def update_decision(
        self,
        decision_id: str,
        new_state: str,
        actor: str,
        rejection_reason: str | None = None,
    ) -> GovernanceDecision | None:
        """Update a governance decision's state."""
        decision = self._decisions.get(decision_id)
        if decision is None:
            return None
        if not decision.transition_state(new_state, actor):
            return None
        if rejection_reason is not None and new_state == "REJECTED":
            decision.rejection_reason = rejection_reason
        self._persist_decision(decision)
        return decision

    def approve_decision(self, decision_id: str, reviewer: str) -> GovernanceDecision | None:
        """Approve a governance decision."""
        decision = self._decisions.get(decision_id)
        if decision is None:
            return None
        if decision.is_expired():
            return None
        if not decision.approve(reviewer):
            return None
        self._persist_decision(decision)
        return decision

    def reject_decision(self, decision_id: str, reviewer: str, rejection_reason: str) -> GovernanceDecision | None:
        """Reject a governance decision."""
        decision = self._decisions.get(decision_id)
        if decision is None:
            return None
        if not decision.reject(reviewer, rejection_reason):
            return None
        self._persist_decision(decision)
        return decision

    def _persist_decision(self, decision: GovernanceDecision) -> None:
        """Persist a single decision to disk."""
        decision_path = self.base_dir / f"decision_{decision.decision_id}.json"
        with open(decision_path, "w", encoding="utf-8") as f:
            json.dump(decision.to_dict(), f, indent=2, ensure_ascii=False)

    def count_by_state(self) -> dict[str, int]:
        """Count decisions by state."""
        counts: dict[str, int] = {}
        for decision in self._decisions.values():
            counts[decision.decision_state] = counts.get(decision.decision_state, 0) + 1
        return counts

    def count_by_state_and_severity(self) -> dict[str, dict[str, int]]:
        """Count decisions by state and severity."""
        counts: dict[str, dict[str, int]] = {}
        for decision in self._decisions.values():
            state_counts = counts.get(decision.decision_state, {})
            state_counts["total"] = state_counts.get("total", 0) + 1
            counts[decision.decision_state] = state_counts
        return counts


# ============================================================================
# Governance policy registry - persistent storage
# ============================================================================

class GovernancePolicyRegistry:
    """Persistent storage for governance policies."""

    def __init__(self, base_dir: str | Path | None = None):
        """Initialize the governance policy registry."""
        if base_dir is not None:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path("governance_policies")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._policies: dict[str, GovernancePolicy] = {}
        self._load_existing()

    def _load_existing(self) -> None:
        """Load existing policies from disk."""
        if not self.base_dir.exists():
            return
        for entry in self.base_dir.iterdir():
            if entry.is_file() and entry.suffix == ".json":
                try:
                    with open(entry, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    policy = GovernancePolicy.from_dict(data)
                    self._policies[policy.policy_id] = policy
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

    def create_policy(
        self,
        name: str,
        description: str,
        scope: str,
        rule_ids: list[str],
        severity_requirements: str,
        thresholds: dict[str, Any],
        effective_date: datetime,
        version: str = "1.0",
        owner_or_authority: str = "system",
    ) -> GovernancePolicy:
        """Create a new governance policy."""
        policy = GovernancePolicy(
            policy_id=f"POL_{uuid.uuid4().hex[:8].upper()}",
            name=name,
            description=description,
            scope=scope,
            rule_ids=tuple(rule_ids),
            severity_requirements=severity_requirements,
            thresholds=thresholds,
            effective_date=effective_date,
            version=version,
            owner_or_authority=owner_or_authority,
            status="active",
        )
        self._policies[policy.policy_id] = policy
        self._persist_policy(policy)
        return policy

    def get_policy(self, policy_id: str) -> GovernancePolicy | None:
        """Retrieve a policy by ID."""
        return self._policies.get(policy_id)

    def list_policies(self) -> list[GovernancePolicy]:
        """List all policies."""
        return list(self._policies.values())

    def update_policy(
        self,
        policy_id: str,
        **updates: Any,
    ) -> GovernancePolicy | None:
        """Update a governance policy."""
        policy = self._policies.get(policy_id)
        if policy is None:
            return None
        for key, value in updates.items():
            if hasattr(policy, key):
                setattr(policy, key, value)
        policy.last_modified = datetime.now(timezone.utc)
        self._persist_policy(policy)
        return policy

    def retire_policy(self, policy_id: str) -> bool:
        """Retire a governance policy."""
        policy = self._policies.get(policy_id)
        if policy is None:
            return False
        policy.status = "retired"
        policy.last_modified = datetime.now(timezone.utc)
        self._persist_policy(policy)
        return True

    def _persist_policy(self, policy: GovernancePolicy) -> None:
        """Persist a single policy to disk."""
        policy_path = self.base_dir / f"policy_{policy.policy_id}.json"
        with open(policy_path, "w", encoding="utf-8") as f:
            json.dump(policy.to_dict(), f, indent=2, ensure_ascii=False)


# ============================================================================
# CLI entry point
# ============================================================================

def create_policy_cli(
    name: str,
    description: str,
    scope: str,
    rule_ids: list[str],
    severity_requirements: str,
    thresholds: dict[str, Any],
    effective_date: str,
    version: str = "1.0",
    owner_or_authority: str = "system",
) -> str:
    """CLI entry point for creating a governance policy."""
    registry = GovernancePolicyRegistry()
    try:
        effective_dt = datetime.fromisoformat(effective_date)
    except (ValueError, TypeError):
        effective_dt = datetime.now(timezone.utc)
    policy = registry.create_policy(
        name=name,
        description=description,
        scope=scope,
        rule_ids=rule_ids,
        severity_requirements=severity_requirements,
        thresholds=thresholds,
        effective_date=effective_dt,
        version=version,
        owner_or_authority=owner_or_authority,
    )
    return policy.policy_id


def create_decision_cli(
    requester: str,
    decision_rationale: str,
    scope_of_approval: str,
    approved_action: str,
    validity_period_hours: int | None = None,
) -> str:
    """CLI entry point for creating a governance decision."""
    registry = GovernanceDecisionRegistry()
    decision = registry.create_decision(
        requester=requester,
        decision_rationale=decision_rationale,
        scope_of_approval=scope_of_approval,
        approved_action=approved_action,
        validity_period_hours=validity_period_hours,
    )
    return decision.decision_id


def approve_decision_cli(decision_id: str, reviewer: str) -> bool:
    """CLI entry point for approving a governance decision."""
    registry = GovernanceDecisionRegistry()
    decision = registry.approve_decision(decision_id, reviewer)
    return decision is not None


def reject_decision_cli(decision_id: str, reviewer: str, rejection_reason: str) -> bool:
    """CLI entry point for rejecting a governance decision."""
    registry = GovernanceDecisionRegistry()
    decision = registry.reject_decision(decision_id, reviewer, rejection_reason)
    return decision is not None


def list_decisions_cli(requester: str | None = None, state: str | None = None) -> list[dict[str, Any]]:
    """CLI entry point for listing governance decisions."""
    registry = GovernanceDecisionRegistry()
    decisions = registry.list_decisions(requester=requester, state=state)
    return [d.to_dict() for d in decisions]


def list_policies_cli() -> list[dict[str, Any]]:
    """CLI entry point for listing governance policies."""
    registry = GovernancePolicyRegistry()
    policies = registry.list_policies()
    return [p.to_dict() for p in policies]