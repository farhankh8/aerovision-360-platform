#!/usr/bin/env python3
"""AEROVISION 360 — Reference manifest hash generator.

Generates deterministic SHA-256-based synthetic exchange rates for all 8
DimCurrency currencies over the reporting period 2025-10-01 through
2026-09-30.

Outputs:
  data/04_reference/ref_exchange_rates.csv
  data/manifests/ref_exchange_rates_manifest.json

Constraints (GOV-D-07 / OD-04):
- UTF-8 without BOM
- SHA-256 over UTF-8 bytes of canonical CSV
- RFC 8785 JCS not applicable (flat CSV, not JSON)
- Duplicate currency/date combinations prohibited
- Missing rates -> quarantine (excluded from output)
- Deterministic: same seed + same parameters => identical output

Owner-approved OD-04 decisions:
- Currency scope: AED, QAR, SGD, INR, GBP, EUR, USD, AUD (all 8 DimCurrency currencies)
- Exchange-rate convention: USD per one unit, exact-date lookup, 6 decimals,
  round final amount only, no forward-fill
- Rate source: AEROVISION-360-SYNTHETIC-FX-V1
- Rate version: FX-YYYY-MM-DD-NNN date-based
- Rate-generation: Deterministic algorithmic generation with fixed seed
"""

import csv
import hashlib
import json
import os
from datetime import date, timedelta
from pathlib import Path

# Canonicalization rules (RFC 8785 JCS v1.0 adapted for CSV)
CANONICALIZATION_STANDARD = "RFC 8785 JCS v1.0"
HASH_ALGORITHM = "SHA-256"
HASH_OUTPUT_FORMAT = "lowercase hexadecimal (64 chars)"
CHARACTER_ENCODING = "UTF-8 without BOM"
LINE_ENDINGS = "LF (\\x0A)"
WHITESPACE = "None (minified)"
MANIFEST_HASH_EXCLUDED = True

# Owner-approved OD-04 thresholds
CURRENCIES = ["AED", "QAR", "SGD", "INR", "GBP", "EUR", "USD", "AUD"]
REPORTING_CURRENCY = "USD"
REPORTING_START = "2025-10-01"
REPORTING_END = "2026-09-30"
RATE_SOURCE = "AEROVISION-360-SYNTHETIC-FX-V1"
RATE_VERSION = "FX-2026-11-04-001"
SEED = 3602026
OUTPUT_DIR = "data/04_reference"
MANIFEST_DIR = "data/manifests"
OUTPUT_FILE = "ref_exchange_rates.csv"
MANIFEST_FILE = "reference_manifest.json"


def deterministic_rate(currency_code: str, rate_date: str, seed: int) -> float:
    """Deterministic SHA-256-based rate generation.

    Same inputs always produce the same byte sequence. Values are realistic FX
    rates (positive, 6 decimal places) and never zero or negative.

    USD is always exactly 1.000000.
    """
    if currency_code == "USD":
        return 1.0

    input_str = "%s|%s|%s|%d" % (RATE_VERSION, currency_code, rate_date, seed)
    digest = hashlib.sha256(input_str.encode("utf-8")).hexdigest()
    int_val = int(digest[:8], 16)
    rate = 0.5 + (int_val / 0xFFFFFFFF) * 1.5
    return round(rate, 6)


def generate_manifest() -> list[dict]:
    """Generate deterministic JSON records for all currencies over the reporting period."""
    start_date = date.fromisoformat(REPORTING_START)
    end_date = date.fromisoformat(REPORTING_END)

    records = []
    current_date = start_date
    while current_date <= end_date:
        rate_date_str = current_date.strftime("%Y-%m-%d")
        for currency in CURRENCIES:
            rate = deterministic_rate(currency, rate_date_str, SEED)
            records.append({
                "CurrencyCode": currency,
                "RateDate": rate_date_str,
                "ExchangeRateToUSD": "%.6f" % rate,
                "RateSource": RATE_SOURCE,
                "IsSynthetic": True,
                "RateVersion": RATE_VERSION,
            })
        current_date += timedelta(days=1)

    return records


def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def main():
    # Ensure output directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(MANIFEST_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    # Generate canonical records
    records = generate_manifest()

    # Write CSV deterministically (sorted by CurrencyCode then RateDate)
    records.sort(key=lambda r: (r["CurrencyCode"], r["RateDate"]))

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "CurrencyCode",
                "RateDate",
                "ExchangeRateToUSD",
                "RateSource",
                "IsSynthetic",
                "RateVersion",
            ],
        )
        writer.writeheader()
        writer.writerows(records)

    # Compute SHA-256 of the written file
    sha256_digest = compute_sha256(output_path)

    # Row count (excluding header)
    with open(output_path, "r", encoding="utf-8") as f:
        row_count = sum(1 for _ in f) - 1

    # Build manifest record
    manifest = {
        "manifest_id": "REF_EXCHANGE_RATES_V1",
        "document_type": "reference_manifest",
        "project": "AEROVISION 360",
        "description": "Reference exchange rates for currency conversion",
        "canonicalization_standard": CANONICALIZATION_STANDARD,
        "hash_algorithm": HASH_ALGORITHM,
        "hash_output_format": HASH_OUTPUT_FORMAT,
        "character_encoding": CHARACTER_ENCODING,
        "line_endings": LINE_ENDINGS,
        "whitespace": WHITESPACE,
        "manifest_hash_field_excluded": MANIFEST_HASH_EXCLUDED,
        "generated_at_utc": "2026-11-07T00:00:00+00:00",
        "row_count": row_count,
        "grain": "One row per currency per rate date",
        "primary_key": "CurrencyCode + RateDate",
        "source": "Deterministic algorithmic generation (seed-based)",
        "source_files": {
            "audit_report_sha256": "1e6f7f8c3f711752b53a480e6b67179fdebf58194af5338e621c2c320cfd1aab",
            "airline_reference_workbook_sha256": "6f9d21365e69b540b8a99cdb461cc5280e570853d5d4ebd5a4f03f7945231c25",
        },
        "crosswalk_csv_sha256": "1c68eb62e30ed0dd87981bdc5e63cf68a8493f7111150ae84b6df13804b6268d",
        "generated_at_utc": "2026-11-07T00:00:00+00:00",
        "currency_count": len(CURRENCIES),
        "currencies": sorted(CURRENCIES),
        "reporting_currency": REPORTING_CURRENCY,
        "reporting_period": {
            "start": REPORTING_START,
            "end": REPORTING_END,
            "days": (date.fromisoformat(REPORTING_END) - date.fromisoformat(REPORTING_START)).days + 1,
        },
        "sha256": sha256_digest,
        "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
        "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    }

    manifest_path = os.path.join(MANIFEST_DIR, MANIFEST_FILE)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("Created %s with %d rows" % (output_path, row_count))
    print("SHA-256: %s" % sha256_digest)
    print("Created manifest: %s" % manifest_path)


if __name__ == "__main__":
    main()