"""Pipeline CLI entry point for AEROVISION 360.

Provides a command-line interface for the pipeline orchestration engine.
Dry-run mode is the default. Actual execution is NOT yet supported.

Usage:

    python scripts/run_pipeline.py --dry-run
    python scripts/run_pipeline.py --dry-run --format json
    python scripts/run_pipeline.py --list-components
    python scripts/run_pipeline.py --show-dependencies
    python scripts/run_pipeline.py --component fact_flight_operations
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure project root is importable when run directly.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.orchestration.pipeline import (  # noqa: E402
    ComponentStatus,
    ExecutionMode,
    PipelineComponent,
    PipelineOrchestrator,
    create_default_registry,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the pipeline CLI."""
    parser = argparse.ArgumentParser(
        prog="run_pipeline.py",
        description=(
            "AEROVISION 360 pipeline orchestrator CLI. "
            "Dry-run mode by default. Actual execution is not yet supported."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Run in dry-run mode (default). No files are modified.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        default=False,
        help="Request actual execution. Not yet supported; will be rejected.",
    )
    parser.add_argument(
        "--list-components",
        action="store_true",
        default=False,
        help="List all registered components and exit.",
    )
    parser.add_argument(
        "--show-dependencies",
        action="store_true",
        default=False,
        help="Show the dependency graph and exit.",
    )
    parser.add_argument(
        "--component",
        type=str,
        default=None,
        help="Show details for a single component ID.",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="text",
        choices=["text", "json"],
        help="Output format: text (default) or json.",
    )
    return parser


def format_component_record(rec, indent: int = 2) -> str:
    """Format a component execution record as text."""
    pad = " " * indent
    status_line = f"{pad}{rec.component_id} ({rec.name}): {rec.status.value}"
    lines = [status_line]
    if rec.blocked_reason:
        lines.append(f"{pad}  reason: {rec.blocked_reason}")
    for inp in rec.inputs:
        lines.append(
            f"{pad}  input: {inp.path.name} -> "
            + ("EXISTS" if inp.exists else "MISSING")
        )
    for out in rec.outputs:
        lines.append(
            f"{pad}  output: {out.path.name} -> "
            + ("EXISTS" if out.exists else "MISSING")
        )
    return "\n".join(lines)


def format_dependency_line(cid: str, comp, indent: int = 2) -> str:
    """Format a single dependency line as text."""
    pad = " " * indent
    deps = ", ".join(comp.depends_on) if comp.depends_on else "(none)"
    return f"{pad}{cid} -> depends on: {deps}"


def run_cli(argv: list[str] | None = None) -> int:
    """Run the CLI with the given arguments.

    Returns an exit code:
        0 = success
        1 = error
        2 = invalid arguments
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # --execute is not supported yet
    if args.execute:
        print("ERROR: --execute is not yet supported.", file=sys.stderr)
        print(
            "       Actual pipeline execution has not been implemented.",
            file=sys.stderr,
        )
        print(
            "       Use --dry-run (default) for planning only.",
            file=sys.stderr,
        )
        return 1

    # Build the orchestrator and registry
    orch = PipelineOrchestrator(mode=ExecutionMode.DRY_RUN)
    for comp in create_default_registry():
        orch.register(comp)

    # Validate
    errors = orch.validate()
    if errors:
        print("ERROR: Pipeline configuration errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    # --list-components
    if args.list_components:
        if args.format == "json":
            comp_list = []
            for cid in sorted(orch.list_components().keys()):
                comp = orch.get_component(cid)
                comp_list.append(
                    {
                        "component_id": cid,
                        "name": comp.name,
                        "builder_script": str(comp.builder_script),
                        "depends_on": comp.depends_on,
                    }
                )
            print(json.dumps({"components": comp_list}, indent=2))
        else:
            print("Registered components:")
            for cid in sorted(orch.list_components().keys()):
                comp = orch.get_component(cid)
                deps = (
                    ", ".join(comp.depends_on) if comp.depends_on else "(none)"
                )
                print(f"  {cid} ({comp.name})")
                print(f"    builder: {comp.builder_script.name}")
                print(f"    depends_on: {deps}")
        return 0

    # --show-dependencies
    if args.show_dependencies:
        order = orch.execution_order()
        if args.format == "json":
            dep_map = {}
            for cid in order:
                comp = orch.get_component(cid)
                dep_map[cid] = {
                    "depends_on": comp.depends_on,
                }
            print(json.dumps({"dependency_graph": dep_map}, indent=2))
        else:
            print("Dependency graph (execution order):")
            for i, cid in enumerate(order, 1):
                comp = orch.get_component(cid)
                print(format_dependency_line(cid, comp, indent=2))
        return 0

    # --component (single component detail)
    if args.component is not None:
        cid = args.component
        comp = orch.get_component(cid)
        if comp is None:
            print(
                f"ERROR: Component '{cid}' not found.", file=sys.stderr
            )
            print(
                f"       Use --list-components to see available components.",
                file=sys.stderr,
            )
            return 1

        # Inspect the component
        inspected = orch._inspect_component(
            PipelineComponent(
                component_id=comp.component_id,
                name=comp.name,
                builder_script=comp.builder_script,
                inputs=comp.inputs,
                outputs=comp.outputs,
                depends_on=comp.depends_on,
            )
        )

        if args.format == "json":
            print(
                json.dumps(
                    {
                        "component_id": inspected.component_id,
                        "name": inspected.name,
                        "status": inspected.status.value,
                        "blocked_reason": inspected.blocked_reason,
                        "depends_on": inspected.depends_on,
                        "inputs": [
                            {
                                "path": str(inp.path),
                                "exists": inp.exists,
                            }
                            for inp in inspected.inputs
                        ],
                        "outputs": [
                            {
                                "path": str(out.path),
                                "exists": out.exists,
                                "sha256": out.sha256,
                            }
                            for out in inspected.outputs
                        ],
                    },
                    indent=2,
                )
            )
        else:
            print(f"Component: {inspected.component_id} ({inspected.name})")
            print(f"  Status: {inspected.status.value}")
            if inspected.blocked_reason:
                print(f"  Reason: {inspected.blocked_reason}")
            print(f"  Depends on: {', '.join(inspected.depends_on) or '(none)'}")
            print("  Inputs:")
            for inp in inspected.inputs:
                print(
                    f"    {inp.path.name}: {'EXISTS' if inp.exists else 'MISSING'}"
                )
            print("  Outputs:")
            for out in inspected.outputs:
                print(
                    f"    {out.path.name}: {'EXISTS' if out.exists else 'MISSING'}"
                )
        return 0

    # Default: full dry-run plan
    run = orch.plan()

    if args.format == "json":
        output = {
            "run_id": run.run_id,
            "mode": run.mode.value,
            "start_time": (
                run.start_time.isoformat() if run.start_time else None
            ),
            "end_time": (
                run.end_time.isoformat() if run.end_time else None
            ),
            "duration_seconds": run.duration_seconds,
            "summary": {
                "total": len(run.components),
                "ready": run.ready_count,
                "already_present": run.already_present_count,
                "blocked": run.blocked_count,
                "failed": run.failed_count,
            },
            "components": {},
        }
        for cid in orch.execution_order():
            rec = run.components[cid]
            comp = orch.get_component(cid)
            output["components"][cid] = {
                "name": rec.name,
                "status": rec.status.value,
                "blocked_reason": rec.blocked_reason,
                "depends_on": comp.depends_on if comp else [],
                "inputs": [
                    {
                        "path": str(inp.path),
                        "exists": inp.exists,
                    }
                    for inp in rec.inputs
                ],
                "outputs": [
                    {
                        "path": str(out.path),
                        "exists": out.exists,
                        "sha256": out.sha256,
                    }
                    for out in rec.outputs
                ],
            }
        print(json.dumps(output, indent=2))
    else:
        print("AEROVISION 360 - Pipeline Dry-Run Plan")
        print(f"  Run ID: {run.run_id}")
        print(f"  Mode: {run.mode.value}")
        print(f"  Duration: {run.duration_seconds:.4f}s")
        print()
        print("Summary:")
        print(f"  Total components: {len(run.components)}")
        print(f"  Ready: {run.ready_count}")
        print(f"  Already present: {run.already_present_count}")
        print(f"  Blocked: {run.blocked_count}")
        print(f"  Failed: {run.failed_count}")
        print()
        print("Execution order:")
        for i, cid in enumerate(orch.execution_order(), 1):
            rec = run.components[cid]
            comp = orch.get_component(cid)
            status_icon = {
                "ready": "READY",
                "already_present": "PRESENT",
                "blocked": "BLOCKED",
                "failed": "FAILED",
            }.get(rec.status.value, rec.status.value.upper())
            print(f"  {i:2d}. [{status_icon}] {cid} ({rec.name})")
            if rec.blocked_reason:
                print(f"         Reason: {rec.blocked_reason}")
        print()
        print("No files were modified (dry-run mode).")

    return 0


if __name__ == "__main__":
    sys.exit(run_cli())
