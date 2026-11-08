"""Unit tests for centralized project path handling."""

import pytest

from src.utilities.paths import project_path, project_root


def test_project_root_exists():
    root = project_root()

    assert root.is_dir()
    assert (root / "scripts").is_dir()
    assert (root / "src").is_dir()


def test_project_path_resolves_inside_root():
    result = project_path("src", "utilities")

    assert result == project_root() / "src" / "utilities"


def test_project_path_rejects_parent_traversal():
    with pytest.raises(ValueError):
        project_path("..", "outside-project")
