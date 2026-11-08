"""Build curated DimAirline dataset from the reference workbook.

Reads the DimAirline worksheet from the AEROVISION 360 airline reference
workbook and writes controlled CSV, Parquet, and manifest outputs to the
curated layer. Does not modify the source workbook.
"""

from pathlib import Path
from datetime import datetime, timezone
import sys

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl import load_workbook

# Ensure project root is importable when run directly.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utilities.hashing import sha256_file
from src.utilities.io import write_json_atomic
from src.utilities.paths import project_path

OUT = project_path("data", "03_curated")
MANIFESTS = project_path("data", "manifests")
WORKBOOK = project_path(
    "data", "04_reference", "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"
)

CSV = OUT / "dim_airline.csv"
PARQUET = OUT / "dim_airline.parquet"
MANIFEST = MANIFESTS / "dim_airline_manifest.json"

COLUMNS = [
    "AirlineKey",
    "AirlineId",
    "AirlineIATACode",
    "AirlineICAOCode",
    "AirlineName",
    "AirlineGroup",
    "HomeCountry",
    "HomeCountryCode",
    "BusinessModelClass",
    "IsActive",
    "StatusEffectiveDate",
    "ReferenceVersion",
]

# Verify source workbook exists.
if not WORKBOOK.exists():
    raise FileNotFoundError(f"Reference workbook not found: {WORKBOOK}")

# Verify outputs do not already exist (never overwrite).
for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

# Read DimAirline from the workbook (read-only; workbook is never modified).
wb = load_workbook(WORKBOOK, read_only=True, data_only=True)
if "DimAirline" not in wb.sheetnames:
    raise RuntimeError("DimAirline sheet missing from reference workbook.")

ws = wb["DimAirline"]
rows = list(ws.iter_rows(values_only=True))
headers = list(rows[0])

if headers != COLUMNS:
    raise RuntimeError(f"DimAirline schema mismatch: {headers}")

records = []
for values in rows[1:]:
    if not values or all(v is None for v in values):
        continue
    record = {col: values[i] for i, col in enumerate(COLUMNS)}
    records.append(record)

wb.close()

if len(records) != 10:
    raise RuntimeError(f"Expected 10 airline records; got {len(records)}")

# Validate existing identifiers are preserved exactly.
airline_keys = [r["AirlineKey"] for r in records]
if len(set(airline_keys)) != 10:
    raise RuntimeError("AirlineKey values are not unique.")
if set(airline_keys) != set(range(1, 11)):
    raise RuntimeError("AirlineKey values must be 1 through 10.")

airline_ids = [r["AirlineId"] for r in records]
expected_ids = [f"AIR-{i:04d}" for i in range(1, 11)]
if airline_ids != expected_ids:
    raise RuntimeError(
        f"AirlineId values do not match expected: {expected_ids}"
    )
if len(set(airline_ids)) != 10:
    raise RuntimeError("AirlineId values are not unique.")

if not all(r["IsActive"] is True for r in records):
    raise RuntimeError("Not all baseline airlines are active.")

# Build DataFrame from validated records.
df = pd.DataFrame(records, columns=COLUMNS)

# Apply explicit pandas dtypes. Nullable fields remain as object with None
# so PyArrow can convert them to proper nulls in the target schema.
df = df.astype({
    "AirlineKey": "int32",
    "AirlineId": "string",
    "AirlineIATACode": "string",
    "AirlineICAOCode": "string",
    "AirlineName": "string",
    "AirlineGroup": "string",
    "HomeCountry": "string",
    "HomeCountryCode": "string",
    "BusinessModelClass": "string",
    "IsActive": "bool",
    "ReferenceVersion": "string",
})

# Structural validation.
assert df.shape == (10, 12), f"Expected (10, 12); got {df.shape}"
assert list(df.columns) == COLUMNS
assert df["AirlineKey"].is_unique
assert df["AirlineId"].is_unique
assert df["IsActive"].all()

# Nullable fields must remain null (no uninferred values).
assert df["AirlineGroup"].isna().all(), "AirlineGroup should be null."
assert df["BusinessModelClass"].isna().all(), "BusinessModelClass should be null."
assert df["StatusEffectiveDate"].isna().all(), "StatusEffectiveDate should be null."

# Write UTF-8 CSV.
df.to_csv(CSV, index=False, encoding="utf-8-sig")

# Write Parquet with explicit contract schema.
schema = pa.schema([
    pa.field("AirlineKey", pa.int32(), nullable=False),
    pa.field("AirlineId", pa.string(), nullable=False),
    pa.field("AirlineIATACode", pa.string(), nullable=False),
    pa.field("AirlineICAOCode", pa.string(), nullable=False),
    pa.field("AirlineName", pa.string(), nullable=False),
    pa.field("AirlineGroup", pa.string(), nullable=True),
    pa.field("HomeCountry", pa.string(), nullable=False),
    pa.field("HomeCountryCode", pa.string(), nullable=False),
    pa.field("BusinessModelClass", pa.string(), nullable=True),
    pa.field("IsActive", pa.bool_(), nullable=False),
    pa.field("StatusEffectiveDate", pa.date32(), nullable=True),
    pa.field("ReferenceVersion", pa.string(), nullable=False),
])

table = pa.Table.from_pandas(
    df,
    schema=schema,
    preserve_index=False,
    safe=True,
)

pq.write_table(table, PARQUET, compression="snappy")

# Round-trip checks.
csv_check = pd.read_csv(CSV, encoding="utf-8-sig")
parquet_check = pd.read_parquet(PARQUET)
parquet_schema = pq.read_schema(PARQUET)

assert csv_check.shape == (10, 12)
assert parquet_check.shape == (10, 12)
assert list(parquet_check.columns) == COLUMNS
assert parquet_check["AirlineKey"].is_unique
assert parquet_check["AirlineId"].is_unique

# Verify Parquet schema types.
assert parquet_schema.field("AirlineKey").type == pa.int32()
assert parquet_schema.field("IsActive").type == pa.bool_()
assert parquet_schema.field("StatusEffectiveDate").type == pa.date32()

# Verify nullable fields are null in Parquet.
assert parquet_check["AirlineGroup"].isna().all()
assert parquet_check["BusinessModelClass"].isna().all()
assert parquet_check["StatusEffectiveDate"].isna().all()

# Write manifest using the existing atomic JSON utility.
manifest = {
    "dataset": "DimAirline",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    "grain": "One row per airline identity",
    "primary_key": "AirlineKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "source": {
        "path": "data/04_reference/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx",
        "sheet": "DimAirline",
        "sha256": sha256_file(WORKBOOK),
    },
    "validation": {
        "exact_column_order": True,
        "unique_airline_keys": True,
        "unique_airline_ids": True,
        "ten_airline_records": True,
        "airline_keys_one_through_ten": True,
        "airline_ids_air_0001_through_air_0010": True,
        "all_baseline_airlines_active": True,
        "nullable_fields_preserved": True,
        "no_uninferred_values": True,
        "csv_round_trip": True,
        "parquet_round_trip": True,
    },
    "files": {
        "csv": {
            "path": "data/03_curated/dim_airline.csv",
            "sha256": sha256_file(CSV),
        },
        "parquet": {
            "path": "data/03_curated/dim_airline.parquet",
            "sha256": sha256_file(PARQUET),
        },
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
}

write_json_atomic(MANIFEST, manifest)

print("DIM_AIRLINE_CURATED_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("AIRLINE KEYS:", ", ".join(str(k) for k in sorted(df["AirlineKey"])))
print("AIRLINE IDS:", ", ".join(df["AirlineId"]))
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
