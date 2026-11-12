"""Data Quality Incident Management for AEROVISION 360.

Provides incident management capabilities for tracking, investigating,
and resolving data-quality incidents through a complete lifecycle.

Incident lifecycle:
  OPEN
    ↓
  INVESTIGATING
    ↓
  REMEDIATION_PROPOSED
    ↓
  PENDING_APPROVAL
    ↓
  APPROVED
    ↓
  REMEDIATION_EXECUTED
    ↓
  VALIDATING
    ↓
  RESOLVED

Also supports:
  - REJECTED
  - DEFERRED
  - CLOSED_WITHOUT_REMEDIATION

Each incident has:
  - Unique incident ID
  - Dataset ID
  - Related run ID
  - Related quality run ID
  - Related rule ID
  - Related anomaly ID where applicable
  - Severity
  - Description
  - Evidence
  - Status
  - Created timestamp
  - Updated timestamp
  - Owner or assignee
  - Resolution details
  - Closure timestamp
"""

from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from dataclasses import dataclass, field

from src.quality.models import QualityOutcome, QualityRecordOutcome


# ---------------------------------------------------------------------------
# Incident state machine - valid transitions
# ---------------------------------------------------------------------------

INCIDENT_LIFECLOW_TRANSITIONS: Dict[str, set[str]] = {
    "OPEN": {"investigating", "rejected", "deferred", "closed_without_remediation"},
    "INVESTIGATING": {"open", "remediation_proposed", "rejected", "deferred", "closed_without_remediation"},
    "REMEDIATION_PROPOSED": {"pending_approval", "rejected", "deferred", "closed_without_remediation"},
    "PENDING_APPROVAL": {"investigating", "rejected", "deferred", "closed_without_remediation"},
    "APPROVED": {"remediation_executed", "rejected", "deferred", "closed_without_remediation"},
    "REMEDIATION_EXECUTED": {"validating", "rejected", "deferred", "closed_without_remediation"},
    "VALIDATING": {"resolved", "rejected", "deferred", "closed_without_remediation"},
    "RESOLVED": set(),  # Terminal state
    "REJECTED": set(),  # Terminal state
    "DEFERRED": {"investigating", "open"},  # Can be revived
    "CLOSED_WITHOUT_REMEDIATION": set(),  # Terminal state
}


def is_valid_transition(from_state: str, to_state: str) -> bool:
    """Check if a state transition is valid according to the incident lifecycle."""
    allowed = INCIDENT_LIFECLOW_TRANSITIONS.get(from_state, set())
    return to_state in allowed


# ---------------------------------------------------------------------------
# Incident models
# ---------------------------------------------------------------------------

@dataclass
class IncidentID:
    """Unique incident identifier."""
    value: str = field(default_factory=lambda: f"INC_{uuid.uuid4().hex[:12].upper()}")
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, IncidentID):
            return self.value == other.value
        return str(self) == str(other)
    
    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class Incident:
    """Represents a data quality incident."""
    incident_id: IncidentID
    dataset_id: str
    run_id: str
    quality_run_id: str | None
    rule_id: str | None
    anomaly_id: str | None
    severity: str  # "CRITICAL", "WARNING", "INFO"
    description: str
    evidence: dict[str, Any]
    status: str  # INCIDENT_LIFECLOW_TRANSITIONS keys
    created_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    owner: str | None = None
    assignee: str | None = None
    resolution_details: str | None = None
    closed_timestamp: datetime | None = None
    
    # Lifecycle tracking
    history: list[dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Initialize history on creation."""
        if not self.history:
            self.history = [{
                "from": None,
                "to": self.status,
                "timestamp": self.created_timestamp.isoformat(),
                "actor": "system",
            }]
    
    def transition_to(self, new_status: str, actor: str = "system") -> bool:
        """Attempt to transition incident to new status.
        
        Returns True if transition is valid, False otherwise.
        """
        if not is_valid_transition(self.status, new_status):
            return False
        
        # Record the transition in history
        self.history.append({
            "from": self.status,
            "to": new_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
        })
        
        # Update status and timestamps
        self.status = new_status
        self.updated_timestamp = datetime.now(timezone.utc)
        
        # If transitioning to a terminal or near-terminal state, set closure
        if new_status in ("RESOLVED", "REJECTED", "CLOSED_WITHOUT_REMEDIATION"):
            self.closed_timestamp = datetime.now(timezone.utc)
            if self.resolution_details is None:
                self.resolution_details = f"Incident {self.incident_id} {new_status.lower()}"
        
        return True
    
    def to_dict(self) -> dict[str, Any]:
        """Convert incident to dictionary for serialization."""
        return {
            "incident_id": str(self.incident_id),
            "dataset_id": self.dataset_id,
            "run_id": self.run_id,
            "quality_run_id": self.quality_run_id,
            "rule_id": self.rule_id,
            "anomaly_id": self.anomaly_id,
            "severity": self.severity,
            "description": self.description,
            "evidence": self.evidence,
            "status": self.status,
            "created_timestamp": self.created_timestamp.isoformat(),
            "updated_timestamp": self.updated_timestamp.isoformat(),
            "owner": self.owner,
            "assignee": self.assignee,
            "resolution_details": self.resolution_details,
            "closed_timestamp": self.closed_timestamp.isoformat() if self.closed_timestamp else None,
            "history": self.history,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Incident":
        """Create incident from dictionary."""
        incident = cls(
            incident_id=IncidentID(data["incident_id"]),
            dataset_id=data["dataset_id"],
            run_id=data["run_id"],
            quality_run_id=data.get("quality_run_id"),
            rule_id=data.get("rule_id"),
            anomaly_id=data.get("anomaly_id"),
            severity=data["severity"],
            description=data["description"],
            evidence=data.get("evidence", {}),
            status=data["status"],
            owner=data.get("owner"),
            assignee=data.get("assignee"),
            resolution_details=data.get("resolution_details"),
            closed_timestamp=(
                datetime.fromisoformat(data["closed_timestamp"]) 
                if data.get("closed_timestamp") else None
            ),
        )
        incident.history = data.get("history", [])
        return incident


# ---------------------------------------------------------------------------
# Incident registry - persistent storage
# ---------------------------------------------------------------------------

class IncidentRegistry:
    """Persistent storage for data quality incidents.
    
    Stores incident records as JSON files in a dedicated data directory.
    Supports create, read, update, and query operations.
    """
    
    def __init__(self, base_dir: str | Path | None = None):
        """Initialize the incident registry.
        
        Args:
            base_dir: Optional base directory for incident data.
                      Defaults to "incident_data" relative to project root.
        """
        if base_dir is not None:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path("incident_data")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._incidents: dict[str, Incident] = {}
        self._load_existing()
    
    def _load_existing(self) -> None:
        """Load existing incidents from disk."""
        if not self.base_dir.exists():
            return
        
        for entry in self.base_dir.iterdir():
            if entry.is_file() and entry.suffix == ".json":
                try:
                    with open(entry, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    incident = Incident.from_dict(data)
                    self._incidents[incident.incident_id.value] = incident
                except (json.JSONDecodeError, KeyError, ValueError):
                    # Skip corrupted files
                    continue
    
    def create_incident(
        self,
        dataset_id: str,
        run_id: str,
        quality_run_id: str,
        rule_id: str | None = None,
        anomaly_id: str | None = None,
        severity: str = "INFO",
        description: str = "",
        evidence: dict[str, Any] | None = None,
        owner: str | None = None,
    ) -> Incident:
        """Create a new incident with OPEN status."""
        incident = Incident(
            incident_id=IncidentID(),
            dataset_id=dataset_id,
            run_id=run_id,
            quality_run_id=quality_run_id,
            rule_id=rule_id,
            anomaly_id=anomaly_id,
            severity=severity,
            description=description,
            evidence=evidence or {},
            status="OPEN",
            owner=owner,
        )
        
        # Store in memory and on disk
        self._incidents[incident.incident_id.value] = incident
        self._persist_incident(incident)
        
        return incident
    
    def get_incident(self, incident_id: str) -> Incident | None:
        """Retrieve an incident by ID."""
        return self._incidents.get(incident_id)
    
    def list_incidents(
        self,
        dataset_id: str | None = None,
        status: str | None = None,
        severity: str | None = None,
    ) -> list[Incident]:
        """List incidents, optionally filtered by dataset, status, or severity."""
        incidents = list(self._incidents.values())
        
        if dataset_id:
            incidents = [i for i in incidents if i.dataset_id == dataset_id]
        if status:
            incidents = [i for i in incidents if i.status == status]
        if severity:
            incidents = [i for i in incidents if i.severity == severity]
        
        # Sort by created timestamp descending
        incidents.sort(key=lambda i: i.created_timestamp, reverse=True)
        return incidents
    
    def update_incident(
        self,
        incident_id: str,
        new_status: str,
        actor: str = "system",
        resolution_details: str | None = None,
    ) -> Incident | None:
        """Update an incident's status and optionally add resolution details."""
        incident = self._incidents.get(incident_id)
        if incident is None:
            return None
        
        # Attempt status transition
        if not incident.transition_to(new_status, actor):
            return None  # Invalid transition
        
        # Add resolution details if provided
        if resolution_details is not None:
            incident.resolution_details = resolution_details
        
        # Persist to disk
        self._persist_incident(incident)
        
        return incident
    
    def _persist_incident(self, incident: Incident) -> None:
        """Persist a single incident to disk."""
        incident_path = self.base_dir / f"incident_{incident.incident_id.value}.json"
        with open(incident_path, "w", encoding="utf-8") as f:
            json.dump(incident.to_dict(), f, indent=2, ensure_ascii=False)
    
    def delete_incident(self, incident_id: str) -> bool:
        """Delete an incident from the registry."""
        incident = self._incidents.get(incident_id)
        if incident is None:
            return False
        
        # Remove from memory
        del self._incidents[incident_id]
        
        # Remove from disk
        incident_path = self.base_dir / f"incident_{incident_id}.json"
        if incident_path.exists():
            incident_path.unlink()
        
        return True
    
    def deduplicate_incidents(
        self,
        new_incident: Incident,
        evidence_key_fields: list[str] | None = None,
        similarity_threshold: float = 0.9,
    ) -> list[str]:
        """Check for duplicate incidents based on stable evidence.
        
        Args:
            new_incident: The new incident to check against existing ones.
            evidence_key_fields: Fields from evidence to use for comparison.
            similarity_threshold: Similarity threshold (0-1) for considering
                               incidents as duplicates.
        
        Returns:
            List of incident IDs that are considered duplicates of the new incident.
        """
        if evidence_key_fields is None:
            # Default: use rule_id and anomaly_id as evidence keys
            evidence_key_fields = ["rule_id", "anomaly_id"]
        
        duplicates: list[str] = []
        
        for existing_id, existing_incident in self._incidents.items():
            if existing_incident.incident_id.value == new_incident.incident_id.value:
                continue  # Skip self
            
            # Check if evidence keys match
            evidence_match = True
            for field in evidence_key_fields:
                new_val = new_incident.evidence.get(field)
                existing_val = existing_incident.evidence.get(field)
                
                if new_val is None and existing_val is None:
                    continue  # Both None, check next field
                if new_val != existing_val:
                    evidence_match = False
                    break
            
            if evidence_match:
                # Also check dataset and severity match
                if (existing_incident.dataset_id == new_incident.dataset_id and
                    existing_incident.severity == new_incident.severity):
                    duplicates.append(existing_incident.incident_id.value)
        
        return duplicates
    
    def count_by_status(self) -> dict[str, int]:
        """Count incidents by status."""
        counts: dict[str, int] = {}
        for incident in self._incidents.values():
            counts[incident.status] = counts.get(incident.status, 0) + 1
        return counts
    
    def count_by_severity(self) -> dict[str, int]:
        """Count incidents by severity."""
        counts: dict[str, int] = {}
        for incident in self._incidents.values():
            counts[incident.severity] = counts.get(incident.severity, 0) + 1
        return counts


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def create_incident_cli(
    dataset_id: str,
    run_id: str,
    quality_run_id: str,
    rule_id: str | None = None,
    anomaly_id: str | None = None,
    severity: str = "INFO",
    description: str = "",
    evidence: dict[str, Any] | None = None,
    owner: str | None = None,
) -> str:
    """CLI entry point for creating a data quality incident.
    
    Returns the incident ID as a string.
    """
    from src.quality import IncidentRegistry
    
    registry = IncidentRegistry()
    incident = registry.create_incident(
        dataset_id=dataset_id,
        run_id=run_id,
        quality_run_id=quality_run_id,
        rule_id=rule_id,
        anomaly_id=anomaly_id,
        severity=severity,
        description=description,
        evidence=evidence,
        owner=owner,
    )
    
    return str(incident.incident_id)


def transition_incident_cli(
    incident_id: str,
    new_status: str,
    actor: str = "system",
    resolution_details: str | None = None,
) -> bool:
    """CLI entry point for transitioning an incident to a new status."""
    registry = IncidentRegistry()
    incident = registry.update_incident(
        incident_id=incident_id,
        new_status=new_status,
        actor=actor,
        resolution_details=resolution_details,
    )
    
    return incident is not None


def list_incidents_cli(
    dataset_id: str | None = None,
    status: str | None = None,
    severity: str | None = None,
) -> list[dict[str, Any]]:
    """CLI entry point for listing incidents."""
    registry = IncidentRegistry()
    incidents = registry.list_incidents(dataset_id=dataset_id, status=status, severity=severity)
    return [i.to_dict() for i in incidents]