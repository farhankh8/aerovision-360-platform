"""Unit tests for shared SHA-256 utilities."""

from io import BytesIO

from src.utilities.hashing import (
    sha256_bytes,
    sha256_file,
    sha256_stream,
)

EXPECTED_ABC = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_sha256_bytes():
    assert sha256_bytes(b"abc") == EXPECTED_ABC


def test_sha256_stream():
    assert sha256_stream(BytesIO(b"abc")) == EXPECTED_ABC


def test_sha256_file(tmp_path):
    file_path = tmp_path / "sample.bin"
    file_path.write_bytes(b"abc")

    assert sha256_file(file_path) == EXPECTED_ABC
