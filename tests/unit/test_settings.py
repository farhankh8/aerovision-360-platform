"""Unit tests for configuration loading and validation."""

import json

import pytest

from config.settings import (
    ConfigurationError,
    load_settings,
    require_settings,
)


def test_load_json_settings(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(
        json.dumps({"environment": "development", "debug": True}),
        encoding="utf-8",
    )

    assert load_settings(path) == {
        "environment": "development",
        "debug": True,
    }


def test_load_yaml_settings(tmp_path):
    path = tmp_path / "settings.yaml"
    path.write_text(
        "environment: development\ndebug: true\n",
        encoding="utf-8",
    )

    assert load_settings(path) == {
        "environment": "development",
        "debug": True,
    }


def test_missing_file_raises_configuration_error(tmp_path):
    with pytest.raises(ConfigurationError, match="not found"):
        load_settings(tmp_path / "missing.json")


def test_invalid_root_type_is_rejected(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="mapping"):
        load_settings(path)


def test_required_settings_validation():
    with pytest.raises(ConfigurationError, match="database"):
        require_settings(
            {"environment": "development"},
            ["environment", "database"],
        )


def test_required_settings_accept_valid_configuration():
    require_settings(
        {"environment": "development", "database": "local"},
        ["environment", "database"],
    )
