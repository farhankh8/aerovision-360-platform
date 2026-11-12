"""Reusable SHA-256 hashing utilities."""

from hashlib import sha256
from pathlib import Path
from typing import BinaryIO

CHUNK_SIZE = 1024 * 1024


def sha256_bytes(data: bytes) -> str:
    """Return the SHA-256 hexadecimal digest of bytes."""
    return sha256(data).hexdigest()


def sha256_stream(stream: BinaryIO) -> str:
    """Hash a binary stream incrementally without loading it entirely."""
    digest = sha256()

    while chunk := stream.read(CHUNK_SIZE):
        digest.update(chunk)

    return digest.hexdigest()


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 digest of a file."""
    with Path(path).open("rb") as file:
        return sha256_stream(file)
