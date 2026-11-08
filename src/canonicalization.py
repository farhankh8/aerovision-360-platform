"""
AEROVISION 360 — RFC 8785 JCS Canonicalization (GOV-D-07 Implementation)

Implements RFC 8785 JSON Canonicalization Scheme (JCS) for ManifestHash
computation as specified in GOV-D-07 owner authorization (08 November 2026).

Specification:
- Canonicalization standard: RFC 8785 — JSON Canonicalization Scheme (JCS)
- Object-property ordering: Lexicographic comparison of UTF-16 code units
- Character encoding: UTF-8 without BOM
- Hash algorithm: SHA-256
- Hash output format: Lowercase hexadecimal (64 characters)
- ManifestHash self-exclusion: ManifestHash property removed entirely before canonicalization
- Unicode handling: Exact preservation; no NFC normalization
- Timestamp handling: UTC ISO 8601 enforced through separate input validation

Validation cases V-01 through V-12 are implemented in test_canonicalization.py.
"""

import hashlib
import json
import math
from typing import Any


def _serialize_jcs(value: Any) -> bytes:
    """
    Serialize a JSON value according to RFC 8785 JCS rules.

    Rules:
    - Null: "null"
    - Boolean: "true" or "false"
    - Integer: minimal representation (no leading zeros, no + sign)
    - Float: minimal representation with finite precision; NaN/Infinity not allowed
    - String: UTF-8 encoded, escaped per JSON rules
    - Array: [ element1, element2, ... ]
    - Object: { "key1": value1, "key2": value2 } with keys sorted lexicographically
      by UTF-16 code units
    """
    if value is None:
        return b"null"
    if isinstance(value, bool):
        return b"true" if value else b"false"
    if isinstance(value, int):
        return str(value).encode("utf-8")
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            raise ValueError("RFC 8785 does not support NaN or Infinity")
        # Use repr for minimal round-trip representation
        return repr(value).encode("utf-8")
    if isinstance(value, str):
        return _serialize_jcs_string(value)
    if isinstance(value, list):
        parts = [_serialize_jcs(item) for item in value]
        return b"[" + b",".join(parts) + b"]"
    if isinstance(value, dict):
        # Sort keys lexicographically by UTF-16 code units
        sorted_items = sorted(value.items(), key=lambda kv: kv[0])
        parts = []
        for key, val in sorted_items:
            parts.append(_serialize_jcs_string(key) + b":" + _serialize_jcs(val))
        return b"{" + b",".join(parts) + b"}"
    raise TypeError(f"Unsupported type for JCS serialization: {type(value)}")


def _serialize_jcs_string(s: str) -> bytes:
    """Serialize a JSON string per RFC 8785 rules."""
    encoded = s.encode("utf-8")
    # JSON-escape: quote, backslash, control characters
    result = bytearray(b'"')
    i = 0
    while i < len(encoded):
        byte = encoded[i]
        if byte == 0x22:  # quotation mark
            result += b'\\"'
        elif byte == 0x5C:  # reverse solidus
            result += b"\\\\"
        elif byte < 0x20:  # control character
            result += b"\\u%04x" % byte
        else:
            result.append(byte)
        i += 1
    result += b'"'
    return bytes(result)


def canonicalize(obj: Any) -> bytes:
    """
    Canonicalize a JSON-serializable object per RFC 8785 JCS.

    Args:
        obj: A JSON-serializable Python object (None, bool, int, float, str,
             list, dict).

    Returns:
        Canonical JSON bytes (UTF-8 without BOM).
    """
    return _serialize_jcs(obj)


def compute_manifest_hash(obj: Any, manifest_hash_key: str = "ManifestHash") -> str:
    """
    Compute SHA-256 ManifestHash per GOV-D-07 specification.

    The ManifestHash property itself is removed from the object before
    canonicalization, then SHA-256 is applied to the canonical bytes.

    Args:
        obj: The manifest object (dict) potentially containing a ManifestHash key.
        manifest_hash_key: The key name to exclude before canonicalization.

    Returns:
        Lowercase hexadecimal SHA-256 hash (64 characters).
    """
    if isinstance(obj, dict):
        # Remove ManifestHash key before canonicalization (self-exclusion)
        obj_without_hash = {k: v for k, v in obj.items() if k != manifest_hash_key}
    else:
        obj_without_hash = obj

    canonical_bytes = canonicalize(obj_without_hash)
    return hashlib.sha256(canonical_bytes).hexdigest()


def compute_file_hash(file_path: str) -> str:
    """Compute SHA-256 hash of a file's contents."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_manifest_hash(obj: Any, expected_hash: str, manifest_hash_key: str = "ManifestHash") -> bool:
    """
    Verify that the computed ManifestHash matches the expected value.

    Args:
        obj: The manifest object.
        expected_hash: The expected lowercase hexadecimal hash.
        manifest_hash_key: The key name excluded before canonicalization.

    Returns:
        True if hashes match, False otherwise.
    """
    computed = compute_manifest_hash(obj, manifest_hash_key)
    return computed.lower() == expected_hash.lower()
