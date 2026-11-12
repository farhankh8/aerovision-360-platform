"""Shared JSON file I/O utilities."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def read_json(path: str | Path) -> Any:
    """Read and parse a UTF-8 JSON file."""
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json_atomic(
    path: str | Path,
    data: Any,
    *,
    overwrite: bool = False,
) -> Path:
    """Write JSON through a temporary file before publishing it.

    Existing files are protected unless overwrite=True.
    The temporary file is created in the destination directory.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and not overwrite:
        stg = None
        raise FileExistsError(f"Refusing to overwrite existing file: {target}")

    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=target.parent,
    )
    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        if overwrite:
            os.replace(temporary_path, target)
        else:
            temporary_path.rename(target)

        return target

    finally:
        if temporary_path.exists():
            temporary_path.unlink()
