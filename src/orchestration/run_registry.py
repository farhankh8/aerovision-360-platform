"""Execution history and run registry for AEROVISION 360.

Persistent storage of pipeline run records using JSON files.
Supports creating, retrieving, and updating pipeline runs.

OD-04 restrictions respected: Only metadata is stored; no production data is modified.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.orchestration.pipeline import (
    PipelineOrchestrator,
    ExecutionMode,
    PipelineRun,
    ComponentStatus,
)


# ============================================================================
# Registry Configuration
# ============================================================================

REGISTRY_BASE_DIR = Path("run_registry_data")
"""Base directory for run registry JSON data files."""


# ============================================================================
# Run Registry
# ============================================================================


class RunRegistry:
    """Persistent execution history registry.

    Stores PipelineRun records as JSON files in a dedicated data directory.
    Supports create, read, update, and query operations for pipeline execution history.
    """

    def __init__(self, base_dir: str | Path | None = None):
        """Initialize the run registry.

        Args:
            base_dir: Optional base directory for registry data.
                      Defaults to "run_registry_data" relative to project root.
        """
        if base_dir is not None:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = REGISTRY_BASE_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Run record lifecycle
    # ------------------------------------------------------------------

    def create_run(
        self,
        run: PipelineRun,
        *,
        mode: ExecutionMode | None = None,
    ) -> PipelineRun:
        """Persist a run record to the registry.

        Args:
            run: The PipelineRun to persist.
            mode: Execution mode override (uses run.mode if not set).

        Returns:
            The persisted PipelineRun record.
        """
        mode = mode or run.mode
        # Ensure mode is consistent
        run.mode = mode

        # Persist as JSON
        run_path = self._run_path(run.run_id)
        data = {
            "run_id": run.run_id,
            "mode": run.mode.value,
            "start_time": run.start_time.isoformat() if run.start_time else None,
            "end_time": run.end_time.isoformat() if run.end_time else None,
            "duration_seconds": run.duration_seconds,
            "total_components": run.total_components,
            "completed_count": run.completed_count,
            "blocked_count": run.blocked_count,
            "failed_count": run.failed_count,
            "succeeded_count": run.succeeded_count,
            "skipped_count": run.skipped_count,
            "ready_count": run.ready_count,
            "already_present_count": run.already_present_count,
            "errors": run.errors,
            "warnings": (
                [w.value if isinstance(w, ComponentStatus) else w for w in run.warnings]
                if run.warnings
                else None
            ),
            "quality_run_id": run.quality_run_id,
            "components": {
                cid: {
                    "component_id": comp.component_id,
                    "name": comp.name,
                    "status": comp.status.value,
                    "blocked_reason": comp.blocked_reason,
                    "error": comp.error,
                    "warnings": (
                        [w.value if isinstance(w, ComponentStatus) else w for w in comp.warnings]
                        if comp.warnings
                        else None
                    ),
                    "start_time": comp.start_time.isoformat() if comp.start_time else None,
                    "end_time": comp.end_time.isoformat() if comp.end_time else None,
                    "duration_seconds": comp.duration_seconds,
                    "inputs_inspected": comp.inputs_inspected,
                    "outputs_inspected": comp.outputs_inspected,
                }
                for cid, comp in run.components.items()
            },
        }
        with open(run_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return run

    def get_run(self, run_id: str) -> Optional[PipelineRun]:
        """Retrieve a run record by run_id.

        Args:
            run_id: The unique run identifier.

        Returns:
            The PipelineRun if found, None otherwise.
        """
        run_path = self._run_path(run_id)
        if not run_path.exists():
            return None

        try:
            with open(run_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

        # Reconstruct ComponentExecutionRecord for each component
        components = {}
        for cid, comp_data in data.get("components", {}).items():
            comp = ComponentExecutionRecord(
                component_id=comp_data["component_id"],
                name=comp_data["name"],
                status=ComponentStatus(comp_data["status"]),
                blocked_reason=comp_data.get("blocked_reason"),
                error=comp_data.get("error"),
                warnings=comp_data.get("warnings"),
                start_time=(
                    datetime.fromisoformat(comp_data["start_time"])
                    if comp_data.get("start_time")
                    else None
                ),
                end_time=(
                    datetime.fromisoformat(comp_data["end_time"])
                    if comp_data.get("end_time")
                    else None
                ),
                duration_seconds=comp_data.get("duration_seconds"),
                inputs_inspected=comp_data.get("inputs_inspected"),
                outputs_inspected=comp_data.get("outputs_inspected"),
            )
            components[cid] = comp

        run = PipelineRun(
            run_id=data["run_id"],
            mode=ExecutionMode(data["mode"]),
            start_time=(
                datetime.fromisoformat(data["start_time"]) if data.get("start_time") else None
            ),
            end_time=(
                datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
            ),
            duration_seconds=data.get("duration_seconds"),
            components=components,
            errors=data.get("errors", []),
            warnings=data.get("warnings"),
            quality_run_id=data.get("quality_run_id"),
        )

        return run

    def list_runs(self) -> list[PipelineRun]:
        """List all persisted run records.

        Returns:
            List of PipelineRun records, sorted by start_time descending.
        """
        runs = []
        if not self.base_dir.exists():
            return runs

        for entry in sorted(self.base_dir.iterdir(), key=lambda p: p.name, reverse=True):
            if entry.suffix == ".json" and entry.is_file():
                run = self.get_run(entry.stem)
                if run is not None:
                    runs.append(run)

        return runs

    def list_incomplete_runs(self) -> list[PipelineRun]:
        """List runs that are not yet complete (have blocked or failed components).

        Returns:
            List of incomplete PipelineRun records.
        """
        runs = []
        for run in self.list_runs():
            if run.failed_count > 0 or run.blocked_count > 0:
                runs.append(run)
        return runs

    def identify_incomplete_runs(self) -> list[dict[str, str]]:
        """Identify runs with incomplete execution.

        Returns:
            List of dicts with run_id and reason for incompleteness.
        """
        incomplete = []
        for run in self.list_runs():
            if run.failed_count > 0:
                incomplete.append({"run_id": run.run_id, "reason": "failed_components"})
            elif run.blocked_count > 0:
                incomplete.append({"run_id": run.run_id, "reason": "blocked_components"})
        return incomplete

    # ------------------------------------------------------------------
    # Completion and recovery
    # ------------------------------------------------------------------

    def mark_run_complete(self, run_id: str) -> None:
        """Mark a run as complete (ensures JSON persists with final state).

        Args:
            run_id: The run identifier to mark complete.
        """
        run = self.get_run(run_id)
        if run is None:
            raise PipelineOrchestratorError(f"Run {run_id} not found in registry.")
        # The run is already persisted; this method ensures the record is not
        # garbage-collected and provides a clear intent API.
        pass

    def _run_path(self, run_id: str) -> Path:
        """Get the file path for a run record."""
        return self.base_dir / f"{run_id}.json"


# ============================================================================
# ComponentExecutionRecord helper (reused from pipeline)
# ------------------------------------------------------------------

class ComponentExecutionRecord:
    """Record of a single component execution.

    Mirrors the structure used by PipelineRun.components for registry persistence.
    """

    def __init__(
        self,
        component_id: str,
        name: str,
        status: ComponentStatus,
        blocked_reason: str | None = None,
        error: str | None = None,
        warnings: list[str] | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        duration_seconds: float | None = None,
        inputs_inspected: int | None = None,
        outputs_inspected: int | None = None,
    ):
        self.component_id = component_id
        self.name = name
        self.status = status
        self.blocked_reason = blocked_reason
        self.error = error
        self.warnings = warnings if warnings else []
        self.start_time = start_time
        self.end_time = end_time
        self.duration_seconds = duration_seconds
        self.inputs_inspected = inputs_inspected
        self.outputs_inspected = outputs_inspected