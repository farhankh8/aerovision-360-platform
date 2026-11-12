"""Configuration loading and validation."""

import json
from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Raised when configuration cannot be loaded or validated."""


def load_settings(path: str | Path) -> dict[str, Any]:
    """Load a JSON or YAML configuration file.

    The root configuration value must be a mapping.
    """
    source = Path(path)

    if not source.is_file():
        raise ConfigurationError(f"Configuration file not found: {source}")

    suffix = source.suffix.lower()

    try:
        with source.open("r", encoding="utf-8") as file:
            if suffix == ".json":
                settings = json.load(file)
            elif suffix in {".yaml", ".yml"}:
                settings = yaml.safe_load(file)
            else:
                raise ConfigurationError(
                    f"Unsupported configuration format: {suffix}"
                )
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ConfigurationError(
            f"Invalid configuration file: {source}"
        ) from exc

    if not isinstance(settings, dict):
        raise ConfigurationError(
            "Configuration root must be a mapping/object."
        )

    return settings


def require_settings(
    settings: dict[str, Any],
    required_keys: tuple[str, ...] | list[str],
) -> None:
    """Raise an error when required top-level settings are missing."""
    if not isinstance(settings, dict):
        raise ConfigurationError("Settings must be a mapping.")

    missing = [
        key for key in required_keys
        if key not in settings
    ]

    if missing:
        raise ConfigurationError(
            f"Missing required settings: {', '.join(missing)}"
        )
