"""Regression tests for the pipeline CLI entry point.

Tests cover:
- Default dry-run mode
- Component listing (text and JSON)
- Dependency display
- Individual component selection
- JSON output format
- Invalid component identifiers
- Invalid arguments
- Meaningful exit codes
- --execute rejection
- No filesystem modification during dry-run
"""

import json
import sys
from io import StringIO
from pathlib import Path

import pytest

from src.orchestration.pipeline import (
    ComponentStatus,
    PipelineOrchestrator,
    create_default_registry,
)
from scripts.run_pipeline import run_cli, build_parser


# ---------------------------------------------------------------------------
# Argument parser tests
# ---------------------------------------------------------------------------

def test_default_mode_is_dry_run():
    """The default execution mode is DRY_RUN."""
    parser = build_parser()
    args = parser.parse_args([])
    assert args.dry_run is True
    assert args.execute is False


def test_execute_flag_is_false_by_default():
    """--execute is False unless explicitly provided."""
    parser = build_parser()
    args = parser.parse_args([])
    assert args.execute is False


def test_list_components_flag():
    """--list-components flag is recognised."""
    parser = build_parser()
    args = parser.parse_args(["--list-components"])
    assert args.list_components is True


def test_show_dependencies_flag():
    """--show-dependencies flag is recognised."""
    parser = build_parser()
    args = parser.parse_args(["--show-dependencies"])
    assert args.show_dependencies is True


def test_component_flag_accepts_value():
    """--component accepts a component ID value."""
    parser = build_parser()
    args = parser.parse_args(["--component", "dim_airport"])
    assert args.component == "dim_airport"


def test_format_flag_defaults_to_text():
    """--format defaults to 'text'."""
    parser = build_parser()
    args = parser.parse_args([])
    assert args.format == "text"


def test_format_flag_accepts_json():
    """--format json is accepted."""
    parser = build_parser()
    args = parser.parse_args(["--format", "json"])
    assert args.format == "json"


# ---------------------------------------------------------------------------
# CLI execution tests
# ---------------------------------------------------------------------------

def test_cli_default_dry_run():
    """Running the CLI with no arguments defaults to dry-run plan."""
    exit_code = run_cli([])
    assert exit_code == 0


def test_cli_dry_run_explicit():
    """Explicit --dry-run flag works."""
    exit_code = run_cli(["--dry-run"])
    assert exit_code == 0


def test_cli_execute_rejected():
    """--execute is rejected with a clear message and non-zero exit code."""
    exit_code = run_cli(["--execute"])
    assert exit_code == 1


def test_cli_list_components():
    """--list-components lists all registered components."""
    exit_code = run_cli(["--list-components"])
    assert exit_code == 0


def test_cli_list_components_json():
    """--list-components with --format json produces valid JSON."""
    exit_code = run_cli(["--list-components", "--format", "json"])
    assert exit_code == 0


def test_cli_show_dependencies():
    """--show-dependencies displays the dependency graph."""
    exit_code = run_cli(["--show-dependencies"])
    assert exit_code == 0


def test_cli_show_dependencies_json():
    """--show-dependencies with --format json produces valid JSON."""
    exit_code = run_cli(["--show-dependencies", "--format", "json"])
    assert exit_code == 0


def test_cli_single_component():
    """--component displays details for a single component."""
    exit_code = run_cli(["--component", "dim_airport"])
    assert exit_code == 0


def test_cli_single_component_json():
    """--component with --format json produces valid JSON."""
    exit_code = run_cli(["--component", "fact_flight_operations", "--format", "json"])
    assert exit_code == 0


def test_cli_invalid_component_id():
    """An invalid component ID returns exit code 1."""
    exit_code = run_cli(["--component", "nonexistent_component"])
    assert exit_code == 1


# ---------------------------------------------------------------------------
# Output capture tests
# ---------------------------------------------------------------------------

def test_cli_output_contains_summary(capsys):
    """The dry-run output contains a summary section."""
    run_cli([])
    captured = capsys.readouterr()
    assert "Summary:" in captured.out
    assert "Total components:" in captured.out


def test_cli_output_contains_execution_order(capsys):
    """The dry-run output contains the execution order."""
    run_cli([])
    captured = capsys.readouterr()
    assert "Execution order:" in captured.out


def test_cli_output_no_files_modified(capsys):
    """The dry-run output states that no files were modified."""
    run_cli([])
    captured = capsys.readouterr()
    assert "No files were modified" in captured.out


def test_cli_json_output_is_valid(capsys):
    """--format json produces valid JSON output."""
    run_cli(["--format", "json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "run_id" in data
    assert "mode" in data
    assert "summary" in data
    assert "components" in data


def test_cli_list_components_json_is_valid(capsys):
    """--list-components --format json produces valid JSON."""
    run_cli(["--list-components", "--format", "json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "components" in data
    assert len(data["components"]) == 14


def test_cli_show_dependencies_json_is_valid(capsys):
    """--show-dependencies --format json produces valid JSON."""
    run_cli(["--show-dependencies", "--format", "json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "dependency_graph" in data


def test_cli_single_component_json_is_valid(capsys):
    """--component --format json produces valid JSON."""
    run_cli(["--component", "dim_airport", "--format", "json"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["component_id"] == "dim_airport"
    assert "status" in data
    assert "inputs" in data
    assert "outputs" in data


def test_cli_invalid_component_error_message(capsys):
    """Invalid component ID produces an error message on stderr."""
    run_cli(["--component", "nonexistent_component"])
    captured = capsys.readouterr()
    assert "not found" in captured.err.lower()


def test_cli_execute_error_message(capsys):
    """--execute produces an error message on stderr."""
    run_cli(["--execute"])
    captured = capsys.readouterr()
    assert "not yet supported" in captured.err.lower()


# ---------------------------------------------------------------------------
# Orchestrator status semantics tests
# ---------------------------------------------------------------------------

def test_default_registry_components_all_already_present():
    """All existing dimension and fact outputs exist on disk, so all
    components should be ALREADY_PRESENT in a dry-run plan."""
    orch = PipelineOrchestrator()
    for comp in create_default_registry():
        orch.register(comp)
    run = orch.plan()

    assert run.already_present_count == 14
    assert run.ready_count == 0
    assert run.blocked_count == 0
    assert run.failed_count == 0


def test_component_status_values():
    """ComponentStatus enum contains all expected values."""
    assert ComponentStatus.READY.value == "ready"
    assert ComponentStatus.ALREADY_PRESENT.value == "already_present"
    assert ComponentStatus.BLOCKED.value == "blocked"
    assert ComponentStatus.COMPLETED.value == "completed"
    assert ComponentStatus.FAILED.value == "failed"
    assert ComponentStatus.SKIPPED.value == "skipped"
    assert ComponentStatus.PENDING.value == "pending"


def test_run_summary_counts():
    """PipelineRun summary properties reflect component statuses."""
    orch = PipelineOrchestrator()
    for comp in create_default_registry():
        orch.register(comp)
    run = orch.plan()

    assert len(run.components) == 14
    assert run.already_present_count == 14
    assert run.ready_count == 0
    assert run.blocked_count == 0
    assert run.failed_count == 0
