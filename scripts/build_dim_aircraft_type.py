from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "03_curated"
MANIFESTS = ROOT / "data" / "manifests"

CSV = OUT / "dim_aircraft_type.csv"
PARQUET = OUT / "dim_aircraft_type.parquet"
MANIFEST = MANIFESTS / "dim_aircraft_type_manifest.json"

COLUMNS = [
    "AircraftTypeKey",
    "Manufacturer",
    "AircraftModel",
    "AircraftCategory",
    "TypicalSeatCapacity",
    "MaximumSeatCapacity",
    "RangeKM",
    "BodyType"
]

# Synthetic aircraft reference taxonomy.
# All manufacturers and aircraft models are fictional.
ROWS = [(1, 'AeroWorks', 'NB-180', 'Narrowbody', 150, 190, '6100.00', 'Passenger'),
 (2, 'AeroWorks', 'NB-220', 'Narrowbody', 186, 240, '7200.00', 'Passenger'),
 (3, 'Meridian Aircraft', 'WB-280', 'Widebody', 250, 300, '12500.00', 'Passenger'),
 (4, 'Meridian Aircraft', 'WB-360', 'Widebody', 320, 390, '14500.00', 'Passenger'),
 (5, 'Regional Aviation Works', 'RJ-90', 'Regional Jet', 76, 96, '3500.00', 'Passenger'),
 (6, 'Regional Aviation Works', 'RJ-120', 'Regional Jet', 100, 132, '4800.00', 'Passenger'),
 (7, 'Continental Aero', 'TP-70', 'Turboprop', 60, 78, '1800.00', 'Passenger'),
 (8, 'Continental Aero', 'TP-90', 'Turboprop', 76, 96, '2400.00', 'Passenger'),
 (9, 'AeroWorks', 'NB-260', 'Narrowbody', 220, 270, '8200.00', 'Passenger'),
 (10, 'Meridian Aircraft', 'WB-420', 'Widebody', 370, 440, '17000.00', 'Passenger'),
 (11, 'Regional Aviation Works', 'RJ-150', 'Regional Jet', 120, 150, '5500.00', 'Passenger'),
 (12, 'Continental Aero', 'TP-110', 'Turboprop', 88, 112, '3000.00', 'Passenger')]

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")

df = pd.DataFrame(ROWS, columns=COLUMNS)

df["RangeKM"] = df["RangeKM"].map(
    lambda value: Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )
)

df = df.astype({
    "AircraftTypeKey": "int32",
    "Manufacturer": "string",
    "AircraftModel": "string",
    "AircraftCategory": "string",
    "TypicalSeatCapacity": "int16",
    "MaximumSeatCapacity": "int16",
    "BodyType": "string"
})

assert len(df) == 12
assert len(df.columns) == 8
assert list(df.columns) == COLUMNS
assert df.notna().all().all()
assert df["AircraftTypeKey"].is_unique
assert not df.duplicated(["Manufacturer", "AircraftModel"]).any()

allowed_categories = {
    "Narrowbody", "Widebody", "Regional Jet", "Turboprop"
}
allowed_body_types = {"Passenger", "Freighter", "Mixed"}

assert set(df["AircraftCategory"]).issubset(allowed_categories)
assert set(df["BodyType"]).issubset(allowed_body_types)
assert (df["TypicalSeatCapacity"] > 0).all()
assert (df["MaximumSeatCapacity"] > 0).all()
assert (df["TypicalSeatCapacity"] <= df["MaximumSeatCapacity"]).all()
assert all(value > 0 for value in df["RangeKM"])

df.to_csv(CSV, index=False, encoding="utf-8-sig")

schema = pa.schema([
    pa.field("AircraftTypeKey", pa.int32(), nullable=False),
    pa.field("Manufacturer", pa.string(), nullable=False),
    pa.field("AircraftModel", pa.string(), nullable=False),
    pa.field("AircraftCategory", pa.string(), nullable=False),
    pa.field("TypicalSeatCapacity", pa.int16(), nullable=False),
    pa.field("MaximumSeatCapacity", pa.int16(), nullable=False),
    pa.field("RangeKM", pa.decimal128(9, 2), nullable=False),
    pa.field("BodyType", pa.string(), nullable=False)
])

table = pa.Table.from_pandas(
    df,
    schema=schema,
    preserve_index=False,
    safe=True
)

pq.write_table(table, PARQUET, compression="snappy")

csv_check = pd.read_csv(
    CSV,
    encoding="utf-8-sig",
    dtype={"RangeKM": "string"}
)

parquet_check = pd.read_parquet(PARQUET)
parquet_schema = pq.read_schema(PARQUET)

assert csv_check.shape == (12, 8)
assert parquet_check.shape == (12, 8)
assert list(parquet_check.columns) == COLUMNS
assert parquet_check["AircraftTypeKey"].is_unique
assert parquet_schema.field("RangeKM").type == pa.decimal128(9, 2)

for csv_value, parquet_value in zip(
    csv_check["RangeKM"],
    parquet_check["RangeKM"]
):
    assert Decimal(str(csv_value)) == parquet_value

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    "dataset": "DimAircraftType",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "grain": "One row per synthetic aircraft type",
    "primary_key": "AircraftTypeKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "synthetic_reference": True,
    "disclosure": "Synthetic Simulation ? Not Actual Airline Performance",
    "aircraft_type_portfolio": {
        "total_types": len(df),
        "category_counts": {
            str(category): int(count)
            for category, count in df["AircraftCategory"].value_counts().items()
        }
    },
    "validation": {
        "exact_column_order": True,
        "unique_primary_key": True,
        "unique_manufacturer_model": True,
        "valid_aircraft_categories": True,
        "valid_body_types": True,
        "positive_seat_capacities": True,
        "typical_capacity_not_above_maximum": True,
        "positive_range": True,
        "parquet_decimal_9_2_range": True,
        "no_null_values": True,
        "csv_round_trip": True,
        "parquet_round_trip": True
    },
    "files": {
        "csv": {
            "path": "data/03_curated/dim_aircraft_type.csv",
            "sha256": sha256(CSV)
        },
        "parquet": {
            "path": "data/03_curated/dim_aircraft_type.parquet",
            "sha256": sha256(PARQUET)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("DIM_AIRCRAFT_TYPE_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("CATEGORIES:", ", ".join(sorted(df["AircraftCategory"].unique())))
print("RANGEKM PARQUET TYPE: DECIMAL(9,2)")
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL SYNTHETIC REFERENCE")
print("VALIDATION: PASSED")
