"""Centralized AEROVISION 360 project path resolution."""

from pathlib import Path


def project_root() -> Path:
    """Return the absolute project root directory."""
    return Path(__file__).resolve().parents[2]


def project_path(*parts: str | Path) -> Path:
    """Resolve a path inside the project root.

    Raises:
        ValueError: If the resolved path escapes the project root.
    """
    root = project_root().resolve()
    target = root.joinpath(*parts).resolve()

    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"Path must remain inside the project root: {target}"
        ) from exc

    return target
