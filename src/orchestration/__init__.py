"""Pipeline orchestration package for AEROVISION 360.

Provides dependency-aware pipeline orchestration with dry-run support.
"""

from src.orchestration.pipeline import (
    ComponentExecutionRecord,
    ComponentInput,
    ComponentOutput,
    ComponentStatus,
    ExecutionMode,
    PipelineComponent,
    PipelineOrchestrator,
    PipelineOrchestratorError,
    PipelineRun,
    CircularDependencyError,
    DuplicateComponentError,
    MissingDependencyError,
    create_default_registry,
)

__all__ = [
    "ComponentExecutionRecord",
    "ComponentInput",
    "ComponentOutput",
    "ComponentStatus",
    "ExecutionMode",
    "PipelineComponent",
    "PipelineOrchestrator",
    "PipelineOrchestratorError",
    "PipelineRun",
    "CircularDependencyError",
    "DuplicateComponentError",
    "MissingDependencyError",
    "create_default_registry",
]
