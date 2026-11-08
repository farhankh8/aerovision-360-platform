"""Unit tests for shared JSON file I/O utilities."""

import pytest

from src.utilities.io import read_json, write_json_atomic


def test_json_write_and_read_round_trip(tmp_path):
    path = tmp_path / "nested" / "sample.json"
    payload = {"name": "AEROVISION 360", "version": 1}

    write_json_atomic(path, payload)

    assert read_json(path) == payload


def test_json_write_refuses_overwrite_by_default(tmp_path):
    path = tmp_path / "sample.json"
    path.write_text('{"original": true}', encoding="utf-8")

    with pytest.raises(FileExistsError):
        write_json_atomic(path, {"replacement": True})

    assert read_json(path) == {"original": True}


def test_json_write_allows_explicit_overwrite(tmp_path):
    path = tmp_path / "sample.json"
    write_json_atomic(path, {"version": 1})

    write_json_atomic(path, {"version": 2}, overwrite=True)

    assert read_json(path) == {"version": 2}
