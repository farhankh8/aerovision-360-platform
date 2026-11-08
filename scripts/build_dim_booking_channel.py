from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "03_curated"
MANIFESTS = ROOT / "data" / "manifests"

CSV = OUT / "dim_booking_channel.csv"
PARQUET = OUT / "dim_booking_channel.parquet"
MANIFEST = MANIFESTS / "dim_booking_channel_manifest.json"

COLUMNS = [
    "BookingChannelKey",
    "ChannelCode",
    "ChannelName",
    "ChannelCategory",
    "IsDirect",
    "IsActive"
]

# Provisional synthetic channel taxonomy.
ROWS = [
    (1, "WEB", "Airline Website", "Direct Web", True, True),
    (2, "APP", "Airline Mobile App", "Mobile App", True, True),
    (3, "OTA", "Online Travel Agency", "OTA", False, True),
    (4, "GDS", "Global Distribution System", "GDS", False, True),
    (5, "CALL", "Call Center", "Call Center", False, True),
    (6, "CORP", "Corporate Travel Desk", "Corporate", False, True),
    (7, "AIRPT", "Airport Ticket Office", "Airport", False, True)
]

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

df = pd.DataFrame(ROWS, columns=COLUMNS)

df = df.astype({
    "BookingChannelKey": "int32",
    "ChannelCode": "string",
    "ChannelName": "string",
    "ChannelCategory": "string",
    "IsDirect": "bool",
    "IsActive": "bool"
})

allowed_categories = {
    "Direct Web",
    "Mobile App",
    "OTA",
    "GDS",
    "Call Center",
    "Corporate",
    "Airport"
}

assert df.shape == (7, 6)
assert list(df.columns) == COLUMNS
assert df.notna().all().all()

assert df["BookingChannelKey"].is_unique
assert df["ChannelCode"].is_unique
assert df["ChannelName"].is_unique
assert set(df["ChannelCategory"]) == allowed_categories
assert df["ChannelCategory"].is_unique

# Direct flag must agree with channel ownership.
expected_direct = df["ChannelCategory"].isin(
    ["Direct Web", "Mobile App"]
)
assert (df["IsDirect"] == expected_direct).all()

assert df["IsActive"].all()
assert df["ChannelCode"].str.len().between(1, 10).all()

df.to_csv(CSV, index=False, encoding="utf-8-sig")
df.to_parquet(PARQUET, index=False, engine="pyarrow")

csv_check = pd.read_csv(CSV, encoding="utf-8-sig")
parquet_check = pd.read_parquet(PARQUET)

assert csv_check.shape == (7, 6)
assert parquet_check.shape == (7, 6)
assert parquet_check["BookingChannelKey"].is_unique
assert parquet_check["ChannelName"].is_unique

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    "dataset": "DimBookingChannel",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "grain": "One row per booking channel",
    "primary_key": "BookingChannelKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "taxonomy_status": "Provisional baseline taxonomy",
    "direct_channel_rule": "True only for airline-owned Direct Web and Mobile App channels",
    "validation": {
        "exact_column_order": True,
        "unique_primary_key": True,
        "unique_channel_code": True,
        "unique_channel_name": True,
        "all_contract_categories_present": True,
        "category_values_unique": True,
        "direct_flag_consistency": True,
        "all_baseline_channels_active": True,
        "no_null_values": True,
        "csv_round_trip": True,
        "parquet_round_trip": True
    },
    "files": {
        "csv": {
            "path": "data/03_curated/dim_booking_channel.csv",
            "sha256": sha256(CSV)
        },
        "parquet": {
            "path": "data/03_curated/dim_booking_channel.parquet",
            "sha256": sha256(PARQUET)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("DIM_BOOKING_CHANNEL_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("DIRECT_CHANNELS:", int(df["IsDirect"].sum()))
print("INDIRECT_CHANNELS:", int((~df["IsDirect"]).sum()))
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
