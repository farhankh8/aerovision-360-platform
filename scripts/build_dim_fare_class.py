from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "03_curated"
MANIFESTS = ROOT / "data" / "manifests"

CSV = OUT / "dim_fare_class.csv"
PARQUET = OUT / "dim_fare_class.parquet"
MANIFEST = MANIFESTS / "dim_fare_class_manifest.json"

COLUMNS = [
    "FareClassKey",
    "FareClassCode",
    "FareClassName",
    "CabinClass",
    "RefundabilityCategory",
    "IsAncillaryEligible",
    "DisplayOrder"
]

# Provisional synthetic analytical fare taxonomy.
ROWS = [
    (1, "Y", "Economy Flexible", "Economy", "Refundable", True, 1),
    (2, "M", "Economy Standard", "Economy", "Partially Refundable", True, 2),
    (3, "B", "Economy Basic", "Economy", "Non-Refundable", True, 3),
    (4, "W", "Premium Economy Flexible", "Premium Economy", "Refundable", True, 1),
    (5, "E", "Premium Economy Standard", "Premium Economy", "Partially Refundable", True, 2),
    (6, "J", "Business Flexible", "Business", "Refundable", True, 1),
    (7, "C", "Business Standard", "Business", "Partially Refundable", True, 2),
    (8, "F", "First Flexible", "First", "Refundable", True, 1)
]

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

df = pd.DataFrame(ROWS, columns=COLUMNS)

df = df.astype({
    "FareClassKey": "int32",
    "FareClassCode": "string",
    "FareClassName": "string",
    "CabinClass": "string",
    "RefundabilityCategory": "string",
    "IsAncillaryEligible": "bool",
    "DisplayOrder": "int16"
})

assert df.shape == (8, 7)
assert list(df.columns) == COLUMNS
assert df.notna().all().all()

assert df["FareClassKey"].is_unique
assert df["FareClassCode"].is_unique

assert set(df["CabinClass"]).issubset({
    "Economy", "Premium Economy", "Business", "First"
})

assert set(df["RefundabilityCategory"]).issubset({
    "Refundable", "Partially Refundable", "Non-Refundable"
})

assert not df.duplicated(["CabinClass", "DisplayOrder"]).any()

assert df["FareClassCode"].str.len().between(1, 5).all()
assert df["DisplayOrder"].gt(0).all()

df.to_csv(CSV, index=False, encoding="utf-8-sig")
df.to_parquet(PARQUET, index=False, engine="pyarrow")

csv_check = pd.read_csv(CSV, encoding="utf-8-sig")
parquet_check = pd.read_parquet(PARQUET)

assert csv_check.shape == (8, 7)
assert parquet_check.shape == (8, 7)
assert parquet_check["FareClassKey"].is_unique
assert not parquet_check.duplicated(
    ["CabinClass", "DisplayOrder"]
).any()

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    "dataset": "DimFareClass",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "grain": "One row per synthetic fare class",
    "primary_key": "FareClassKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "taxonomy_status": "Provisional analytical taxonomy; not airline-specific fare products",
    "validation": {
        "exact_column_order": True,
        "unique_primary_key": True,
        "unique_fare_class_code": True,
        "valid_cabin_classes": True,
        "valid_refundability_categories": True,
        "unique_display_order_within_cabin": True,
        "valid_fare_code_length": True,
        "positive_display_order": True,
        "no_null_values": True,
        "csv_round_trip": True,
        "parquet_round_trip": True
    },
    "files": {
        "csv": {
            "path": "data/03_curated/dim_fare_class.csv",
            "sha256": sha256(CSV)
        },
        "parquet": {
            "path": "data/03_curated/dim_fare_class.parquet",
            "sha256": sha256(PARQUET)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("DIM_FARE_CLASS_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("CABINS:", ", ".join(df["CabinClass"].unique()))
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
