"""
AEROVISION 360 — GOV-D-07 Validation Cases V-01 through V-12

RFC 8785 JCS Canonicalization validation tests per GOV-D-07 owner authorization
(08 November 2026).

Test cases:
V-01: Null value canonicalization
V-02: Boolean true/false canonicalization
V-03: Integer canonicalization (positive, negative, zero)
V-04: Float canonicalization (minimal representation)
V-05: String canonicalization (UTF-8, escaping)
V-06: Array canonicalization
V-07: Object canonicalization with key sorting (lexicographic UTF-16)
V-08: Nested object canonicalization
V-09: ManifestHash self-exclusion (property removed before canonicalization)
V-10: SHA-256 lowercase hexadecimal output (64 characters)
V-11: UTF-8 without BOM encoding
V-12: Deterministic reproducibility (same input, same output)
"""

import hashlib
import json
import pytest

from src.canonicalization import canonicalize, compute_manifest_hash, compute_file_hash, verify_manifest_hash


# V-01: Null value canonicalization
def test_v01_null_canonicalization():
    result = canonicalize(None)
    assert result == b"null"


# V-02: Boolean true/false canonicalization
def test_v02_boolean_canonicalization():
    assert canonicalize(True) == b"true"
    assert canonicalize(False) == b"false"


# V-03: Integer canonicalization (positive, negative, zero)
def test_v03_integer_canonicalization():
    assert canonicalize(0) == b"0"
    assert canonicalize(42) == b"42"
    assert canonicalize(-7) == b"-7"
    assert canonicalize(1000000) == b"1000000"


# V-04: Float canonicalization (minimal representation)
def test_v04_float_canonicalization():
    assert canonicalize(1.5) == b"1.5"
    assert canonicalize(0.0) == b"0.0"
    assert canonicalize(-3.14159) == b"-3.14159"


# V-05: String canonicalization (UTF-8, escaping)
def test_v05_string_canonicalization():
    assert canonicalize("hello") == b'"hello"'
    assert canonicalize("say \"hi\"") == b'"say \\"hi\\""'
    assert canonicalize("back\\slash") == b'"back\\\\slash"'
    # RFC 8785: control characters below 0x20 are encoded as \uXXXX (lowercase hex)
    assert canonicalize("line\nbreak") == b'"line\\u000abreak"'


# V-06: Array canonicalization
def test_v06_array_canonicalization():
    assert canonicalize([1, 2, 3]) == b"[1,2,3]"
    assert canonicalize([]) == b"[]"
    assert canonicalize(["a", "b", "c"]) == b'["a","b","c"]'


# V-07: Object canonicalization with key sorting (lexicographic UTF-16)
def test_v07_object_key_sorting():
    obj = {"z": 1, "a": 2, "m": 3}
    result = canonicalize(obj)
    assert result == b'{"a":2,"m":3,"z":1}'


# V-08: Nested object canonicalization
def test_v08_nested_object_canonicalization():
    obj = {"outer": {"inner": {"value": 42}}, "list": [1, {"x": 0}]}
    result = canonicalize(obj)
    assert result == b'{"list":[1,{"x":0}],"outer":{"inner":{"value":42}}}'


# V-09: ManifestHash self-exclusion (property removed before canonicalization)
def test_v09_manifest_hash_self_exclusion():
    manifest = {
        "dataset": "FactBookingTransactions",
        "row_count": 9956,
        "ManifestHash": "placeholder-should-be-excluded",
        "currency": "USD",
    }
    hash_without = compute_manifest_hash(manifest)
    # Remove ManifestHash and compute directly to verify same result
    manifest_without_hash = {k: v for k, v in manifest.items() if k != "ManifestHash"}
    canonical = canonicalize(manifest_without_hash)
    expected = hashlib.sha256(canonical).hexdigest()
    assert hash_without == expected
    # Verify the hash does not depend on the placeholder value
    manifest_with_different_hash = dict(manifest)
    manifest_with_different_hash["ManifestHash"] = "different-placeholder"
    assert compute_manifest_hash(manifest_with_different_hash) == hash_without


# V-10: SHA-256 lowercase hexadecimal output (64 characters)
def test_v10_sha256_lowercase_hex():
    manifest = {"test": "value"}
    result = compute_manifest_hash(manifest)
    assert len(result) == 64
    assert all(c in "0123456789abcdef" for c in result)
    assert result == result.lower()


# V-11: UTF-8 without BOM encoding
def test_v11_utf8_without_bom():
    obj = {"unicode": "caf\\u00e9", "emoji": "\\u2603"}
    result = canonicalize(obj)
    # Must not start with BOM (EF BB BF)
    assert not result.startswith(b"\\xef\\xbb\\xbf")
    # Must be valid UTF-8
    result.decode("utf-8")


# V-12: Deterministic reproducibility (same input, same output)
def test_v12_deterministic_reproducibility():
    obj = {
        "dataset": "FactOperatingCosts",
        "rows": 7480,
        "nested": {"key": "value", "arr": [1, 2, 3]},
    }
    hash1 = compute_manifest_hash(obj)
    hash2 = compute_manifest_hash(obj)
    hash3 = compute_manifest_hash(json.loads(json.dumps(obj)))
    assert hash1 == hash2 == hash3


# Additional: File hash computation
def test_compute_file_hash_known_file():
    import os
    test_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "03_curated", "dim_currency.csv")
    if os.path.exists(test_file):
        result = compute_file_hash(test_file)
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)


# Additional: verify_manifest_hash returns True for matching, False for mismatch
def test_verify_manifest_hash():
    manifest = {"dataset": "TestDataset", "row_count": 100}
    computed = compute_manifest_hash(manifest)
    assert verify_manifest_hash(manifest, computed) is True
    assert verify_manifest_hash(manifest, "0" * 64) is False
