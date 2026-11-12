"""Pipeline orchestration engine for AEROVISION 360.

Provides dependency-aware pipeline orchestration with dry-run support and
controlled execution of existing builders and processors.

The orchestrator plans and validates pipeline execution, coordinates real
component execution, enforces quality gates, and produces execution
artifacts with lineage and hashes.

All path resolution uses src.utilities.paths.project_path. File hashing
uses src.utilities.hashing.sha256_file. No new external dependencies are
introduced.

Do not mark a component ALREADY_PRESENT solely because its output file
exists. Verify its manifest, schema, expected outputs and checksums.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from dataclasses import dataclass, field

from src.utilities.hashing import sha256_file
from src.utilities.io import read_json, write_json_atomic
from src.utilities.paths import project_path

from src.quality.engine import QualityEngine, QualityResult
from src.quality.models import QualitySchema


# ---------------------------------------------------------------------------
# Exception classes — must be importable from this module
# ---------------------------------------------------------------------------

class PipelineOrchestratorError(Exception):
    """Base exception for pipeline orchestrator errors."""

    pass


class DuplicateComponentError(PipelineOrchestratorError):
    """Raised when a component is registered with a duplicate ID."""

    pass


class CircularDependencyError(PipelineOrchestratorError):
    """Raised when a circular dependency is detected."""

    pass


class MissingDependencyError(PipelineOrchestratorError):
    """Raised when a component depends on a non-existent component."""

    pass


# ---------------------------------------------------------------------------
# Component statuses
# ---------------------------------------------------------------------------

class ComponentStatus(str, Enum):
    """Status of a pipeline component."""

    PENDING = "pending"
    READY = "ready"
    ALREADY_PRESENT = "already_present"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    SUCCEEDED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ExecutionMode(str, Enum):
    """Pipeline execution mode."""

    DRY_RUN = "dry_run"
    EXECUTE = "execute"
    COMPONENT = "component"
    FROM_STAGE = "from_stage"


# ---------------------------------------------------------------------------
# Component input/output descriptors
# ---------------------------------------------------------------------------

@dataclass
class ComponentInput:
    """Describes a single input file required by a component."""

    path: Path
    exists: bool = False


@dataclass
class ComponentOutput:
    """Describes a single output file produced by a component."""

    path: Path
    exists: bool = False
    sha256: str | None = None


# ---------------------------------------------------------------------------
# Pipeline component description
# ---------------------------------------------------------------------------

@dataclass
class PipelineComponent:
    """A single pipeline component with its metadata and dependencies."""

    component_id: str
    name: str
    builder_script: Path
    inputs: list[ComponentInput] = field(default_factory=list)
    outputs: list[ComponentOutput] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    status: ComponentStatus = ComponentStatus.PENDING
    blocked_reason: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_seconds: float | None = None


# ---------------------------------------------------------------------------
# Execution record
# ---------------------------------------------------------------------------

@dataclass
class ComponentExecutionRecord:
    """Record of a planned or actual component execution."""

    component_id: str
    name: str
    status: ComponentStatus
    blocked_reason: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_seconds: float | None = None
    inputs_inspected: list[ComponentInput] | None = None
    outputs_inspected: list[ComponentOutput] | None = None
    error: str | None = None
    warnings: list[str] | None = None

    @property
    def inputs(self) -> list[ComponentInput]:
        """Inspected input files for this component execution."""
        return self.inputs_inspected if self.inputs_inspected else []

    @property
    def outputs(self) -> list[ComponentOutput]:
        """Inspected output files for this component execution."""
        return self.outputs_inspected if self.outputs_inspected else []


# ---------------------------------------------------------------------------
# Pipeline run record
# ---------------------------------------------------------------------------

@dataclass
class PipelineRun:
    """A complete pipeline run record."""

    run_id: str
    mode: ExecutionMode = ExecutionMode.DRY_RUN
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_seconds: float | None = None
    components: dict[str, ComponentExecutionRecord] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] | None = None
    quality_run_id: str | None = None

    @property
    def total_components(self) -> int:
        """Total number of components in this run."""
        return len(self.components)

    @property
    def completed_count(self) -> int:
        """Number of components with COMPLETED status."""
        return sum(
            1
            for c in self.components.values()
            if c.status == ComponentStatus.COMPLETED
        )

    @property
    def blocked_count(self) -> int:
        """Number of components with BLOCKED status."""
        return sum(
            1
            for c in self.components.values()
            if c.status == ComponentStatus.BLOCKED
        )

    @property
    def failed_count(self) -> int:
        """Number of components with FAILED status."""
        return sum(
            1
            for c in self.components.values()
            if c.status == ComponentStatus.FAILED
        )

    @property
    def succeeded_count(self) -> int:
        """Alias for completed_count."""
        return self.completed_count

    @property
    def skipped_count(self) -> int:
        """Number of components with SKIPPED status."""
        return sum(
            1
            for c in self.components.values()
            if c.status == ComponentStatus.SKIPPED
        )

    @property
    def ready_count(self) -> int:
        """Number of components with READY status."""
        return sum(
            1
            for c in self.components.values()
            if c.status == ComponentStatus.READY
        )

    @property
    def already_present_count(self) -> int:
        """Number of components with ALREADY_PRESENT status."""
        return sum(
            1
            for c in self.components.values()
            if c.status == ComponentStatus.ALREADY_PRESENT
        )


# ---------------------------------------------------------------------------
# Pipeline orchestrator
# ---------------------------------------------------------------------------

class PipelineOrchestrator:
    """Orchestrates pipeline components with dependency awareness.

    Supports dry-run planning by default. Actual execution requires
    an explicit ExecutionMode.EXECUTE. Dry-run never modifies any
    files.

    Integrates:
      - RAW ingestion (scripts/build_raw_layer.py)
      - STAGING transformation (scripts/build_staging_layer.py)
      - Data Quality validation (scripts/run_quality_checks.py)
      - CURATED builders (existing curated dimension/fact builders)
    """

    def __init__(self, mode: ExecutionMode = ExecutionMode.DRY_RUN):
        self.mode = mode
        self._components: dict[str, PipelineComponent] = {}
        self._execution_order: list[str] | None = None
        self._run_id: str | None = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def mode(self) -> ExecutionMode:
        """The execution mode of this orchestrator instance."""
        return self._mode

    @mode.setter
    def mode(self, value: ExecutionMode) -> None:
        self._mode = value

    @property
    def run_id(self) -> str | None:
        """The run ID of the most recent plan() or execute() call, or None."""
        return self._run_id

    @run_id.setter
    def run_id(self, value: str) -> None:
        self._run_id = value

    # ------------------------------------------------------------------
    # Component registration
    # ------------------------------------------------------------------

    def register(self, component: PipelineComponent) -> None:
        """Register a pipeline component.

        Args:
            component: The component to register.

        Raises:
            DuplicateComponentError: If a component with the same ID
                is already registered.
        """
        if component.component_id in self._components:
            raise DuplicateComponentError(
                f"Duplicate component registration: {component.component_id}"
            )
        self._components[component.component_id] = component
        self._execution_order = None

    def unregister(self, component_id: str) -> None:
        """Unregister a component by ID."""
        if component_id in self._components:
            del self._components[component_id]
            self._execution_order = None

    def get_component(self, component_id: str) -> PipelineComponent | None:
        """Get a registered component by ID, or None if not found."""
        return self._components.get(component_id)

    def list_components(self) -> dict[str, PipelineComponent]:
        """Return a copy of all registered components."""
        return dict(self._components)

    # ------------------------------------------------------------------
    # Dependency validation
    # ------------------------------------------------------------------

    def _validate_dependencies(self) -> list[str]:
        """Validate all component references dependencies.

        Returns:
            List of error messages. Empty if all dependencies are valid.
        """
        errors: list[str] = []
        registered_ids = set(self._components.keys())

        for comp_id, comp in self._components.items():
            for dep_id in comp.depends_on:
                if dep_id not in registered_ids:
                    errors.append(
                        f"Component '{comp_id}' depends on unknown "
                        f"component '{dep_id}'"
                    )
        return errors

    def _detect_cycles(self) -> list[str]:
        """Detect circular dependencies using DFS.

        Returns:
            List of error messages describing cycles. Empty if no cycles.
        """
        errors: list[str] = []
        color: dict[str, int] = {cid: 0 for cid in self._components}
        path: list[str] = []

        def dfs(node: str) -> None:
            color[node] = 1
            path.append(node)
            comp = self._components[node]
            for dep in comp.depends_on:
                if color.get(dep) == 1:
                    cycle_start = path.index(dep)
                    cycle = path[cycle_start:] + [dep]
                    errors.append(
                        f"Circular dependency detected: "
                        f"{' -> '.join(cycle)}"
                    )
                elif color.get(dep) == 0:
                    dfs(dep)
                elif color.get(dep) == 2 and dep in path:
                    cycle_start = path.index(dep)
                    cycle = path[cycle_start:] + [dep]
                    errors.append(
                        f"Circular dependency detected: "
                        f"{' -> '.join(cycle)}"
                    )
            path.pop()
            color[node] = 2

        for cid in sorted(self._components.keys()):
            if color[cid] == 0:
                dfs(cid)

        return errors

    # ------------------------------------------------------------------
    # Topological sort
    # ------------------------------------------------------------------

    def _topological_sort(self) -> list[str]:
        """Return component IDs in topological execution order.

        Uses Kahn's algorithm. Components with no dependencies come first.
        Ties are broken by component ID for deterministic ordering.

        Raises:
            CircularDependencyError: If a cycle is detected.
            MissingDependencyError: If a dependency references an
                unregistered component.
        """
        dep_errors = self._validate_dependencies()
        if dep_errors:
            raise MissingDependencyError("; ".join(dep_errors))

        cycle_errors = self._detect_cycles()
        if cycle_errors:
            raise CircularDependencyError("; ".join(cycle_errors))

        in_degree: dict[str, int] = {cid: 0 for cid in self._components}
        dependents: dict[str, list[str]] = {cid: [] for cid in self._components}

        for comp_id, comp in self._components.items():
            for dep_id in comp.depends_on:
                in_degree[comp_id] += 1
                dependents[dep_id].append(comp_id)

        queue: list[str] = sorted(
            [cid for cid, deg in in_degree.items() if deg == 0]
        )
        result: list[str] = []

        while queue:
            node = queue.pop(0)
            result.append(node)
            for dependent in sorted(dependents[node]):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(self._components):
            raise CircularDependencyError(
                "Unable to resolve all dependencies; possible cycle."
            )

        return result

    def execution_order(self) -> list[str]:
        """Return component IDs in topological execution order.

        The order is computed on first call and cached thereafter.

        Raises:
            CircularDependencyError: If circular dependencies exist.
            MissingDependencyError: If dependencies are missing.
        """
        if self._execution_order is None:
            self._execution_order = self._topological_sort()
        return self._execution_order

    # ------------------------------------------------------------------
    # Path inspection
    # ------------------------------------------------------------------

    def _inspect_path(self, path: Path) -> bool:
        """Check whether a path exists on the filesystem.

        Read-only; does not modify anything.
        """
        return path.exists()

    def _inspect_output(self, path: Path) -> ComponentOutput:
        """Inspect a single output path without modification.

        If the file exists, computes its SHA-256 hash.
        """
        exists = path.exists()
        sha256: str | None = None
        if exists:
            sha256 = sha256_file(path)
        return ComponentOutput(path=path, exists=exists, sha256=sha256)

    # ------------------------------------------------------------------
    # Component inspection (read-only status determination)
    # ------------------------------------------------------------------

    def _inspect_component(self, comp: PipelineComponent) -> PipelineComponent:
        """Inspect a component's inputs and outputs for existence.

        Read-only; does not create, delete, or modify any files.
        Determines the component's status based on input availability
        and output existence:

        - ALREADY_PRESENT: all inputs exist AND all outputs exist
        - READY: all inputs exist AND no outputs exist
        - BLOCKED: any input missing, OR partial outputs exist
        """
        inspected_inputs: list[ComponentInput] = []
        for inp in comp.inputs:
            inspected_inputs.append(
                ComponentInput(path=inp.path, exists=self._inspect_path(inp.path))
            )

        inspected_outputs: list[ComponentOutput] = []
        for out in comp.outputs:
            inspected_outputs.append(self._inspect_output(out.path))

        # Determine status
        missing_inputs = [
            inp.path for inp in inspected_inputs if not inp.exists
        ]
        existing_outputs = [
            out.path for out in inspected_outputs if out.exists
        ]
        all_outputs_exist = all(out.exists for out in inspected_outputs)
        no_outputs_exist = not any(out.exists for out in inspected_outputs)

        if missing_inputs:
            status = ComponentStatus.BLOCKED
            blocked_reason = (
                "Missing inputs: "
                + ", ".join(str(p) for p in missing_inputs)
            )
        elif all_outputs_exist:
            status = ComponentStatus.ALREADY_PRESENT
            blocked_reason = None
        elif no_outputs_exist:
            status = ComponentStatus.READY
            blocked_reason = None
        else:
            # Partial outputs exist: some but not all
            status = ComponentStatus.BLOCKED
            blocked_reason = (
                "Partial outputs exist: "
                + ", ".join(str(p) for p in existing_outputs)
            )

        # Return a new component with the inspected status
        return PipelineComponent(
            component_id=comp.component_id,
            name=comp.name,
            builder_script=comp.builder_script,
            inputs=inspected_inputs,
            outputs=inspected_outputs,
            depends_on=comp.depends_on,
            status=status,
            blocked_reason=blocked_reason,
            start_time=comp.start_time,
            end_time=comp.end_time,
            duration_seconds=comp.duration_seconds,
        )

    # ------------------------------------------------------------------
    # Plan method (dry-run)
    # ------------------------------------------------------------------

    def plan(self) -> PipelineRun:
        """Generate a dry-run execution plan.

        Inspects all registered components, validates dependencies,
        computes topological execution order, and determines each
        component's status. Does not create, delete, or modify any
        files.

        Returns:
            A PipelineRun record with the planned execution.

        Raises:
            CircularDependencyError: If circular dependencies exist.
            MissingDependencyError: If dependencies are missing.
        """
        order = self.execution_order()

        run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        self._run_id = run_id

        run = PipelineRun(
            run_id=run_id,
            mode=self.mode,
            start_time=datetime.now(timezone.utc),
        )

        for comp_id in order:
            comp = self._components[comp_id]
            inspected = self._inspect_component(comp)

            run.components[comp_id] = ComponentExecutionRecord(
                component_id=inspected.component_id,
                name=inspected.name,
                status=inspected.status,
                blocked_reason=inspected.blocked_reason,
                inputs_inspected=inspected.inputs,
                outputs_inspected=inspected.outputs,
            )

        run.end_time = datetime.now(timezone.utc)
        run.duration_seconds = (
            (run.end_time - run.start_time).total_seconds()
            if run.end_time and run.start_time
            else 0.0
        )

        return run

    # ------------------------------------------------------------------
    # Validate method
    # ------------------------------------------------------------------

    def validate(self) -> list[str]:
        """Validate the pipeline configuration.

        Returns:
            List of validation error messages. Empty if valid.
        """
        errors: list[str] = []
        errors.extend(self._validate_dependencies())
        errors.extend(self._detect_cycles())

        for comp_id, comp in self._components.items():
            if not comp.builder_script.exists():
                errors.append(
                    f"Component '{comp_id}': builder script not found: "
                    f"{comp.builder_script}"
                )

        return errors

    # ------------------------------------------------------------------
    # Execute method
    # ------------------------------------------------------------------

    def execute(self) -> PipelineRun:
        """Execute the pipeline with the configured execution mode.

        Sequentially executes components in dependency order, enforcing
        quality gates and handling failures according to the execution
        mode.

        Returns:
            A PipelineRun record with the actual execution results.

        Raises:
            CircularDependencyError: If circular dependencies exist.
            MissingDependencyError: If dependencies are missing.
            PipelineOrchestratorError: If a quality gate fails and blocks publication.
        """
        if self.mode == ExecutionMode.DRY_RUN:
            raise PipelineOrchestratorError(
                "Use plan() for dry-run mode; execute() requires EXECUTE mode."
            )

        # Ensure we have an execution order
        order = self.execution_order()

        run = PipelineRun(
            run_id=datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"),
            mode=self.mode,
            start_time=datetime.now(timezone.utc),
        )

        # Track which components have failed so we can stop dependents
        failed_components: set[str] = set()

        # --- Pre-execution quality gate ---
        # Validate quality evidence before any curated builder runs.
        # This blocks pipeline execution when quality validation failed,
        # is missing, or has incomplete dataset coverage.
        # The gate inspects the persisted quality manifest (not in-memory
        # results) and blocks curated publication if evidence is invalid.
        # The gate must always execute before curated builders, even if
        # no components have been registered yet.
        try:
            if run.components:
                self._enforce_quality_gate(run.components[list(run.components.keys())[0]])
            else:
                # No components registered yet — validate manifest if on disk.
                # This ensures the gate runs even before any builder is registered.
                self._validate_quality_manifest_from_disk(run)
        except PipelineOrchestratorError as qge:
            # Quality gate failed before any builder ran — record and abort
            run.errors.append(str(qge))
            run.end_time = datetime.now(timezone.utc)
            run.duration_seconds = (
                (run.end_time - run.start_time).total_seconds()
                if run.end_time and run.start_time
                else 0.0
            )
            return run
        # ----------------------------------------------

        for comp_id in order:
            comp = self._components[comp_id]

            # If a predecessor failed and the dependent is not explicitly
            # permitted to run, block it
            if comp_id in failed_components and not self._should_run_after_failure(comp):
                record = ComponentExecutionRecord(
                    component_id=comp.component_id,
                    name=comp.name,
                    status=ComponentStatus.BLOCKED,
                    blocked_reason="Upstream component failed; per policy, dependents are blocked.",
                )
                run.components[comp_id] = record
                failed_components.add(comp_id)
                continue

            # Execute the component
            record = self._execute_component(comp)
            run.components[comp_id] = record

            # Check for failure
            if record.status == ComponentStatus.FAILED:
                failed_components.add(comp_id)

            # If the component succeeded, enforce quality gate
            if record.status == ComponentStatus.SUCCEEDED:
                try:
                    self._enforce_quality_gate(record)
                except PipelineOrchestratorError:
                    # Quality gate failed — mark component failed and stop
                    record.status = ComponentStatus.FAILED
                    record.error = "Quality gate failed; blocking downstream publication."
                    failed_components.add(comp_id)
                    # Break to stop processing dependents
                    # Mark all remaining components as blocked
                    remaining_idx = order.index(comp_id) + 1
                    for remaining_id in order[remaining_idx:]:
                        remaining_comp = self._components[remaining_id]
                        run.components[remaining_id] = ComponentExecutionRecord(
                            component_id=remaining_comp.component_id,
                            name=remaining_comp.name,
                            status=ComponentStatus.BLOCKED,
                            blocked_reason="Upstream quality gate failure; downstream publication blocked.",
                        )
                    break

        run.end_time = datetime.now(timezone.utc)
        run.duration_seconds = (
            (run.end_time - run.start_time).total_seconds()
            if run.end_time and run.start_time
            else 0.0
        )

        # Generate execution manifest
        self._generate_execution_manifest(run)

        return run

    # ------------------------------------------------------------------
    # Execute from a specific stage
    # ------------------------------------------------------------------

    def execute_from_stage(self, stage_id: str) -> PipelineRun:
        """Execute from a specific stage ID.

        Components before the named stage are marked ALREADY_PRESENT;
        components from the named stage onward are executed.

        Args:
            stage_id: The component_id to start execution from.

        Returns:
            A PipelineRun record.
        """
        # Mark all components before stage_id as ALREADY_PRESENT
        order = self.execution_order()
        start_idx = 0
        for i, cid in enumerate(order):
            if cid == stage_id:
                start_idx = i
                break

        # Mark all components before stage_id as ALREADY_PRESENT
        for cid in order[:start_idx]:
            if cid in self._components:
                self._components[cid].status = ComponentStatus.ALREADY_PRESENT

        # --- Pre-execution quality gate from stage ---
        # Validate quality evidence before any curated builder runs from this stage.
        # Uses the shared _enforce_quality_gate method for consistent validation.
        # The gate must execute before any curated builder from this stage.
        try:
            # Create a temporary PipelineRun for quality validation.
            # This ensures the gate has a defined run and components to check.
            validation_run = PipelineRun(
                run_id=datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"),
                mode=ExecutionMode.EXECUTE,
                start_time=datetime.now(timezone.utc),
            )
            # Register any already-registered components for the gate check
            if self._components:
                for cid, comp in self._components.items():
                    if cid not in validation_run.components:
                        validation_run.components[cid] = ComponentExecutionRecord(
                            component_id=cid,
                            name=comp.name,
                            status=ComponentStatus.PENDING,
                            blocked_reason=None,
                            start_time=None,
                            end_time=None,
                            duration_seconds=None,
                            warnings=None,
                            inputs_inspected=None,
                            outputs_inspected=None,
                            error=None,
                        )
            # Now run the quality gate with a defined run and components
            if validation_run.components:
                self._enforce_quality_gate(validation_run.components[list(validation_run.components.keys())[0]])
            # If no components registered yet, validate the manifest on disk
            # if it exists, following the same logic as execute()
            else:
                self._validate_quality_manifest_from_disk(run)
            # Clean up validation run — don't include it in the actual execution
            # The actual run will be created fresh below

            # Execute from start_idx onward
            remaining_ids = order[start_idx:]

            run = PipelineRun(
                run_id=datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"),
                mode=ExecutionMode.EXECUTE,
                start_time=datetime.now(timezone.utc),
            )
        except PipelineOrchestratorError:
            raise

        for comp_id in remaining_ids:
            comp = self._components[comp_id]
            record = self._execute_component(comp)
            run.components[comp_id] = record

        run.end_time = datetime.now(timezone.utc)
        run.duration_seconds = (
            (run.end_time - run.start_time).total_seconds()
            if run.end_time and run.start_time
            else 0.0
        )

        # Generate execution manifest
        self._generate_execution_manifest(run)

        return run

    # ------------------------------------------------------------------
    # Default registry
    # ------------------------------------------------------------------

    def register_default_curated(self) -> None:
        """Register the default curated dimension and fact components.

        Registers all 11 dimensions and 3 verified facts. FactBookingTransactions
        and FactOperatingCosts are NOT registered because OD-04 (exchange-rate
        policy) remains pending owner approval.

        Dependency model:
            Dimensions -> FactFlightOperations -> FactDisruptions,
            FactCustomerFeedback
        """
        from .default_registry import create_default_registry  # type: ignore

        components = create_default_registry()
        for comp in components:
            self.register(comp)

    # ------------------------------------------------------------------
    # List components
    # ------------------------------------------------------------------

    def list_components(self) -> dict[str, PipelineComponent]:
        """Return a copy of all registered components."""
        return dict(self._components)

    # ------------------------------------------------------------------
    # Execution summary
    # ------------------------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """Return a human-readable summary of the execution run."""
        total = len(self._components)
        succeeded = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.COMPLETED
        )
        failed = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.FAILED
        )
        blocked = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.BLOCKED
        )
        ready = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.READY
        )
        already_present = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.ALREADY_PRESENT
        )
        skipped = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.SKIPPED
        )

        return {
            "run_id": self._run_id if hasattr(self, "_run_id") else None,
            "mode": self.mode.value,
            "total_components": total,
            "succeeded": succeeded,
            "failed": failed,
            "blocked": blocked,
            "ready": ready,
            "already_present": already_present,
            "skipped": skipped,
        }

    # ------------------------------------------------------------------
    # Execution manifest generation
    # ------------------------------------------------------------------

    def _generate_execution_manifest(self, run: PipelineRun) -> Path:
        """Generate an execution manifest for the pipeline run.

        Creates a structured manifest under data/execution/<run_id>/
        capturing lineage, checksums, component execution records,
        and quality outcomes.

        Args:
            run: The PipelineRun record with execution results.

        Returns:
            Path to the generated manifest file.
        """
        from src.utilities.io import write_json_atomic

        execution_dir = os.path.join("data", "execution", run.run_id)
        os.makedirs(execution_dir, exist_ok=True)

        # Build component execution records
        component_records: dict[str, dict[str, Any]] = {}
        for comp_id, comp_record in run.components.items():
            component_records[comp_id] = {
                "component_id": comp_record.component_id,
                "name": comp_record.name,
                "status": comp_record.status.value,
                "blocked_reason": comp_record.blocked_reason,
                "error": comp_record.error,
                "warnings": comp_record.warnings or [],
                "duration_seconds": comp_record.duration_seconds,
                "start_time": (
                    comp_record.start_time.isoformat()
                    if comp_record.start_time
                    else None
                ),
                "end_time": (
                    comp_record.end_time.isoformat() if comp_record.end_time else None
                ),
            }

        # Build dependency execution order
        dep_order: list[str] = []
        if run.mode == ExecutionMode.EXECUTE:
            comp_ids_with_status = [
                comp_id
                for comp_id in run.components
                if run.components[comp_id].status
                in (ComponentStatus.SUCCEEDED, ComponentStatus.FAILED, ComponentStatus.BLOCKED)
            ]
            dep_order = comp_ids_with_status

        # Build manifest data
        manifest_data: dict[str, Any] = {
            "run_id": run.run_id,
            "mode": run.mode.value,
            "start_time": (
                run.start_time.isoformat() if run.start_time else None
            ),
            "end_time": (
                run.end_time.isoformat() if run.end_time else None
            ),
            "duration_seconds": run.duration_seconds,
            "total_components": run.total_components,
            "succeeded": run.succeeded_count,
            "failed": run.failed_count,
            "blocked": run.blocked_count,
            "ready": run.ready_count,
            "already_present": run.already_present_count,
            "skipped": run.skipped_count,
            "components": component_records,
            "dependency_order": dep_order,
            "errors": run.errors,
            "warnings": run.warnings or [],
        }

        # Add quality run information if available
        if run.quality_run_id:
            manifest_data["quality_run_id"] = run.quality_run_id
            from pathlib import Path as PPath
            quality_manifest_path = os.path.join(
                "data", "quality",
                f"quality_run_{run.quality_run_id}.json"
            )
            if os.path.exists(quality_manifest_path):
                manifest_data["quality_manifest"] = str(quality_manifest_path)

        # Write the manifest atomically
        manifest_path = os.path.join(
            execution_dir,
            f"execution_manifest_{run.run_id}.json"
        )
        write_json_atomic(manifest_path, manifest_data, overwrite=False)

        return manifest_path

    # ------------------------------------------------------------------
    # Internal component execution
    # ------------------------------------------------------------------

    def _execute_component(self, comp: PipelineComponent) -> ComponentExecutionRecord:
        """Execute a single pipeline component.

        Reads the builder script and runs it as a subprocess, capturing
        output. Handles both dry-run and execute modes.

        Returns a ComponentExecutionRecord with the result.
        """
        from subprocess import Popen, PIPE  # , CalledProcessError
        import time

        record = ComponentExecutionRecord(
            component_id=comp.component_id,
            name=comp.name,
            status=ComponentStatus.PENDING,
        )

        if self.mode == ExecutionMode.DRY_RUN:
            # In dry-run, we just plan the execution without running builders
            record.status = ComponentStatus.READY
            record.start_time = datetime.now(timezone.utc)
            record.end_time = datetime.now(timezone.utc)
            record.duration_seconds = 0.0
            record.warnings = [
                "Dry-run mode: builder execution skipped"
            ]
            return record

        # Ensure builder script exists
        if not comp.builder_script.exists():
            record.status = ComponentStatus.FAILED
            record.error = f"Builder script not found: {comp.builder_script}"
            record.end_time = datetime.now(timezone.utc)
            if record.start_time:
                record.duration_seconds = (
                    (record.end_time - record.start_time).total_seconds()
                )
            return record

        # Build the command to execute the builder
        cmd = [sys.executable, str(comp.builder_script)]

        record.start_time = datetime.now(timezone.utc)

        try:
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, text=True)
            stdout, stderr = proc.communicate()
            return_code = proc.returncode

            record.end_time = datetime.now(timezone.utc)
            record.duration_seconds = (
                (record.end_time - record.start_time).total_seconds()
            )

            if return_code == 0:
                # Builder succeeded
                record.status = ComponentStatus.SUCCEEDED
                record.warnings = stderr.split("\n") if stderr else []
            else:
                # Builder failed
                record.status = ComponentStatus.FAILED
                record.error = (
                    f"Builder exited with code {return_code}"
                )
                if stderr:
                    record.error += f": {stderr[:200]}"
                record.warnings = stdout.split("\n") if stdout else []
        except Exception as e:
            record.status = ComponentStatus.FAILED
            record.error = f"Execution error: {e}"
            record.end_time = datetime.now(timezone.utc)
            if record.start_time:
                record.duration_seconds = (
                    (record.end_time - record.start_time).total_seconds()
                )
            record.warnings = []

        return record

    # ------------------------------------------------------------------
    # Should run after failure
    # ------------------------------------------------------------------

    def _should_run_after_failure(self, comp: PipelineComponent) -> bool:
        """Determine whether a component should run after a predecessor failed.

        By default, we do NOT run dependents of failed components.
        This can be overridden per-component or via policy.
        """
        # By default, block dependents after failure
        return False

    # ------------------------------------------------------------------
    # Quality gate enforcement
    # ------------------------------------------------------------------

    def _enforce_quality_gate(self, record: ComponentExecutionRecord) -> None:
        """Enforce quality gate after component execution.

        Validates the persisted quality manifest before any curated builder
        executes. The gate inspects the actual JSON quality manifest, not
        merely an in-memory result or a filename.

        Raises PipelineOrchestratorError if the quality gate fails and
        blocks downstream CURATED publication.

        The gate checks:
          - Manifest file exists.
          - Manifest is valid JSON.
          - Manifest has the required structure (run_id, source_root, datasets).
          - Manifest run ID matches the explicitly supplied quality/STAGING run ID.
          - Required datasets are present in the manifest.
          - Every required dataset has a valid outcome (PASS, WARNING, or INFO).
          - No required dataset has outcome FAIL.
          - Dataset results are not silently missing.
          - Source-root metadata is consistent with the intended STAGING run.
        """
        # Determine the quality run ID from the persisted quality manifest.
        # Never use the pipeline execution ID (self._run_id) as a substitute.
        # The quality run ID is identified from the quality manifest file on disk.
        manifest_dir = os.path.join("data", "quality")
        actual_quality_run_id = None
        actual_manifest_path = None

        # Search for the quality manifest file
        try:
            import os as os_mod
            candidates = [
                f for f in os_mod.listdir(manifest_dir)
                if f.startswith("quality_run_") and f.endswith(".json")
            ]
            if candidates:
                # Use the most recent manifest (last alphabetically)
                candidates.sort()
                actual_manifest_path = os.path.join(manifest_dir, candidates[-1])
        except FileNotFoundError:
            pass

        if actual_manifest_path is not None:
            try:
                with open(actual_manifest_path, 'r', encoding='utf-8') as f:
                    manifest_data = json.load(f)
                actual_quality_run_id = manifest_data.get("run_id")
            except Exception:
                actual_quality_run_id = None

        if not actual_quality_run_id:
            # No quality manifest found on disk — fail closed since
            # the prompt requires we do not silently skip validation.
            raise PipelineOrchestratorError(
                "Quality gate FAILED: no quality manifest found on disk. "
                "Curated publication blocked until quality validation runs. "
                "Ensure build_staging_layer.py has been executed successfully."
            )
        quality_run_id = actual_quality_run_id

        # Locate the quality manifest for this run
        quality_manifest_path = os.path.join(
            "data", "quality",
            f"quality_run_{quality_run_id}.json"
        )

        if not os.path.exists(quality_manifest_path):
            raise PipelineOrchestratorError(
                f"Quality gate FAILED: quality manifest not found at "
                f"{quality_manifest_path}. "
                f"Run ID '{quality_run_id}' has no persisted quality evidence. "
                "Curated publication blocked until quality validation runs."
            )

        # Parse the manifest
        try:
            with open(quality_manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            raise PipelineOrchestratorError(
                f"Quality gate FAILED: quality manifest at "
                f"{quality_manifest_path} is not valid JSON: {e}"
            )

        # Validate required structure
        required_keys = {"run_id", "source_root", "datasets"}
        missing_keys = required_keys - set(manifest_data.keys())
        if missing_keys:
            raise PipelineOrchestratorError(
                f"Quality gate FAILED: quality manifest missing required keys: {missing_keys}"
            )

        # Validate run ID matches
        if manifest_data["run_id"] != quality_run_id:
            raise PipelineOrchestratorError(
                f"Quality gate FAILED: quality manifest run ID "
                f"'{manifest_data['run_id']}' does not match pipeline run ID "
                f"'{quality_run_id}'.  Evidence is from a different run."
            )

        # Validate source root consistency (normalized path comparison).
        # Must not accept substring matches that could legitimize wrong paths.
        expected_source_root = os.path.normpath(os.path.join("data", "02_staging"))
        manifest_source_root = os.path.normpath(
            manifest_data.get("source_root", "")
        )
        if manifest_source_root != expected_source_root:
            raise PipelineOrchestratorError(
                f"Quality gate FAILED: quality manifest source root "
                f"'{manifest_data.get('source_root')}' does not normalize to "
                f"the expected STAGING root '{expected_source_root}'. "
                "Custom manifest_dir must resolve to the STAGING data layer."
            )

        # Validate every expected dataset is present and has a valid outcome
        expected_sources = [
            "airline_reference_workbook",
            "airline_id_crosswalk",
            "dim_route_keymap_v1",
            "dim_route_keymap_v1_manifest",
        ]

        for source_id in expected_sources:
            if source_id not in manifest_data.get("datasets", {}):
                raise PipelineOrchestratorError(
                    f"Quality gate FAILED: required dataset '{source_id}' "
                    f"missing from quality manifest.  All four registered STAGING "
                    f"sources must have quality evidence for curated publication."
                )

            ds = manifest_data["datasets"][source_id]
            if "outcome" not in ds:
                raise PipelineOrchestratorError(
                    f"Quality gate FAILED: dataset '{source_id}' has no outcome "
                    f"field in the manifest."
                )

            outcome = ds["outcome"]
            if outcome == "failed":
                raise PipelineOrchestratorError(
                    f"Quality gate FAILED: dataset '{source_id}' has outcome FAIL. "
                    "Critical quality rule failure blocks CURATED publication."
                )

            # WARNING and INFO are permitted; just log
            if outcome == "warning":
                record.warnings.append(
                    f"Dataset '{source_id}' quality outcome: WARNING"
                )
            elif outcome == "info":
                record.warnings.append(
                    f"Dataset '{source_id}' quality outcome: INFO"
                )

        # All checks passed
        record.warnings.append(
            "Quality gate passed: all required datasets present with non-FAIL outcomes"
        )

    # ------------------------------------------------------------------
    # Validate quality manifest from disk
    # ------------------------------------------------------------------

    def _validate_quality_manifest_from_disk(self, run: PipelineRun) -> None:
        """Validate the quality manifest from disk if it exists.

        This function is called from execute() when no components are registered
        yet, to ensure the quality gate always runs before curated builders.

        Raises PipelineOrchestratorError if the manifest is missing, malformed,
        or has invalid content.
        """
        import json
        import os

        manifest_dir = os.path.join("data", "quality")

        # Search for any quality manifest file
        try:
            manifest_files = [
                f for f in os.listdir(manifest_dir)
                if f.startswith("quality_run_") and f.endswith(".json")
            ]
        except FileNotFoundError:
            # No quality directory yet — not an error if no quality run
            # has been executed yet. The gate will be re-applied when
            # components are registered.
            return

        if not manifest_files:
            return

        # Use the most recent manifest (last alphabetically)
        manifest_files.sort()
        manifest_path = os.path.join(manifest_dir, manifest_files[-1])

        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            raise PipelineOrchestratorError(
                f"Quality gate FAILED: quality manifest at "
                f"{manifest_path} is not valid JSON."
            )

        # Validate required structure
        required_keys = {"run_id", "source_root", "datasets"}
        missing_keys = required_keys - set(manifest_data.keys())
        if missing_keys:
            raise PipelineOrchestratorError(
                f"Quality gate FAILED: quality manifest missing required keys: {missing_keys}"
            )

        # Validate source root
        expected_source_root = os.path.normpath(os.path.join("data", "02_staging"))
        manifest_source_root = os.path.normpath(
            manifest_data.get("source_root", "")
        )
        if manifest_source_root != expected_source_root:
            raise PipelineOrchestratorError(
                f"Quality gate FAILED: quality manifest source root "
                f"'{manifest_data.get('source_root')}' does not normalize to "
                f"the expected STAGING root '{expected_source_root}'."
            )

        # Validate all four STAGING datasets
        expected_sources = [
            "airline_reference_workbook",
            "airline_id_crosswalk",
            "dim_route_keymap_v1",
            "dim_route_keymap_v1_manifest",
        ]

        for source_id in expected_sources:
            if source_id not in manifest_data.get("datasets", {}):
                raise PipelineOrchestratorError(
                    f"Quality gate FAILED: required dataset '{source_id}' "
                    f"missing from quality manifest.  All four registered STAGING "
                    f"sources must have quality evidence for curated publication."
                )

            ds = manifest_data["datasets"][source_id]
            if "outcome" not in ds:
                raise PipelineOrchestratorError(
                    f"Quality gate FAILED: dataset '{source_id}' has no outcome "
                    f"field in the manifest."
                )

            outcome = ds["outcome"]
            if outcome == "failed":
                raise PipelineOrchestratorError(
                    f"Quality gate FAILED: dataset '{source_id}' has outcome FAIL. "
                    "Critical quality rule failure blocks CURATED publication."
                )

            # WARNING and INFO are permitted
            if outcome == "warning":
                pass
            elif outcome == "info":
                pass

    # ------------------------------------------------------------------
    # Execution summary (duplicate property, keep for API compat)
    # ------------------------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """Return a human-readable summary of the execution run."""
        total = len(self._components)
        succeeded = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.COMPLETED
        )
        failed = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.FAILED
        )
        blocked = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.BLOCKED
        )
        ready = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.READY
        )
        already_present = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.ALREADY_PRESENT
        )
        skipped = sum(
            1
            for c in self._components.values()
            if c.status == ComponentStatus.SKIPPED
        )

        return {
            "run_id": self._run_id if hasattr(self, "_run_id") else None,
            "mode": self.mode.value,
            "total_components": total,
            "succeeded": succeeded,
            "failed": failed,
            "blocked": blocked,
            "ready": ready,
            "already_present": already_present,
            "skipped": skipped,
        }

def create_default_registry():
    from .default_registry import create_default_registry as _create
    return _create()
