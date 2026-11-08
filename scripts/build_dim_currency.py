import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utilities.hashing import sha256_file
from src.utilities.paths import project_root

ROOT = project_root()

OUTPUT_DIR = ROOT / "data" / "03_curated"
MANIFEST_DIR = ROOT / "data" / "manifests"

CSV_PATH = OUTPUT_DIR / "dim_currency.csv"
PARQUET_PATH = OUTPUT_DIR / "dim_currency.parquet"
MANIFEST_PATH = MANIFEST_DIR / "dim_currency_manifest.json"

COLUMNS = [
    "CurrencyKey",
    "CurrencyCode",
    "CurrencyName",
    "CurrencySymbol",
    "DecimalPlaces",
    "IsReportingCurrency"
]

# Provisional baseline covering the ten-airline home-market countries.
CURRENCIES = [
    (1, "AED", "UAE Dirham", "د.إ", 2, False),
    (2, "QAR", "Qatari Riyal", "ر.ق", 2, False),
    (3, "SGD", "Singapore Dollar", "S$", 2, False),
    (4, "INR", "Indian Rupee", "₹", 2, False),
    (5, "GBP", "Pound Sterling", "£", 2, False),
    (6, "EUR", "Euro", "€", 2, False),
    (7, "USD", "US Dollar", "$", 2, True),
    (8, "AUD", "Australian Dollar", "A$", 2, False)
]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

for path in [CSV_PATH, PARQUET_PATH, MANIFEST_PATH]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

df = pd.DataFrame(CURRENCIES, columns=COLUMNS)

df = df.astype({
    "CurrencyKey": "int32",
    "CurrencyCode": "string",
    "CurrencyName": "string",
    "CurrencySymbol": "string",
    "DecimalPlaces": "int8",
    "IsReportingCurrency": "bool"
})

# Structural and business-rule validation.
assert len(df) == 8
assert len(df.columns) == 6
assert list(df.columns) == COLUMNS
assert df.notna().all().all()

assert df["CurrencyKey"].is_unique
assert df["CurrencyCode"].is_unique
assert df["CurrencyCode"].str.fullmatch(r"[A-Z]{3}").all()

assert df["DecimalPlaces"].between(0, 4).all()
assert int(df["IsReportingCurrency"].sum()) == 1
assert df.loc[df["IsReportingCurrency"], "CurrencyCode"].iloc[0] == "USD"

df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
df.to_parquet(PARQUET_PATH, index=False, engine="pyarrow")

# Reopen and validate persisted outputs.
csv_check = pd.read_csv(CSV_PATH)
parquet_check = pd.read_parquet(PARQUET_PATH)

assert csv_check.shape == (8, 6)
assert parquet_check.shape == (8, 6)
assert parquet_check["CurrencyCode"].is_unique
assert int(parquet_check["IsReportingCurrency"].sum()) == 1


manifest = {
    "dataset": "DimCurrency",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "grain": "One row per currency",
    "primary_key": "CurrencyKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "reporting_currency": "USD",
    "currency_population": "Provisional baseline for airline home markets",
    "validation": {
        "exact_column_order": True,
        "unique_currency_key": True,
        "unique_currency_code": True,
        "valid_currency_code_format": True,
        "decimal_places_range": True,
        "exactly_one_reporting_currency": True,
        "reporting_currency_is_usd": True,
        "csv_round_trip": True,
        "parquet_round_trip": True
    },
    "files": {
        "csv": {
            "path": "data/03_curated/dim_currency.csv",
            "sha256": sha256_file(CSV_PATH)
        },
        "parquet": {
            "path": "data/03_curated/dim_currency.parquet",
            "sha256": sha256_file(PARQUET_PATH)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST_PATH.write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("DIM_CURRENCY_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("CURRENCIES:", ", ".join(df["CurrencyCode"].tolist()))
print("REPORTING_CURRENCY: USD")
print("CSV:", CSV_PATH)
print("PARQUET:", PARQUET_PATH)
print("MANIFEST:", MANIFEST_PATH)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
