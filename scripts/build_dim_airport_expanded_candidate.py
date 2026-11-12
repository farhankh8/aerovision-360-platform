# EXPANDED CANDIDATE BUILDER: 72 fictional airports.
# Writes to isolated staging directories only.

from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import json
import hashlib
import re

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "network_expansion_20261104" / "staging" / "curated"
MANIFESTS = ROOT / "reports" / "network_expansion_20261104" / "staging" / "manifests"

CSV = OUT / "dim_airport.csv"
PARQUET = OUT / "dim_airport.parquet"
MANIFEST = MANIFESTS / "dim_airport_manifest.json"

COLUMNS = [
    "AirportKey",
    "AirportCode",
    "AirportName",
    "City",
    "Country",
    "CountryCode",
    "Region",
    "Latitude",
    "Longitude",
    "TimeZoneIANA",
    "IsActive"
]

# All airport codes, names and cities below are fictional project
# identifiers. Coordinates are approximate geographic reference
# positions and do not identify actual airport facilities.
#
# Format:
# Key, Code, AirportName, City, Country, CountryCode,
# Region, Latitude, Longitude, IANA timezone, IsActive

ROWS = [
    (1, 'XAE', 'Nourah Synthetic Airport', 'Nourah', 'United Arab Emirates', 'AE', 'Middle East', 24.950000, 55.120000, 'Asia/Dubai', True),
    (2, 'XAF', 'Sahra Synthetic Airport', 'Sahra', 'United Arab Emirates', 'AE', 'Middle East', 24.330000, 54.650000, 'Asia/Dubai', True),
    (3, 'XAG', 'Miraz Synthetic Airport', 'Miraz', 'United Arab Emirates', 'AE', 'Middle East', 25.250000, 55.050000, 'Asia/Dubai', True),
    (4, 'XQA', 'Qasira Synthetic Airport', 'Qasira', 'Qatar', 'QA', 'Middle East', 25.370000, 51.430000, 'Asia/Qatar', True),
    (5, 'XQB', 'Lusara Synthetic Airport', 'Lusara', 'Qatar', 'QA', 'Middle East', 25.480000, 51.520000, 'Asia/Qatar', True),
    (6, 'XQC', 'Duhara Synthetic Airport', 'Duhara', 'Qatar', 'QA', 'Middle East', 25.230000, 51.570000, 'Asia/Qatar', True),
    (7, 'XSG', 'Meridian Synthetic Airport', 'Meridian', 'Singapore', 'SG', 'Southeast Asia', 1.310000, 103.820000, 'Asia/Singapore', True),
    (8, 'XSH', 'Seraya Synthetic Airport', 'Seraya', 'Singapore', 'SG', 'Southeast Asia', 1.275000, 103.880000, 'Asia/Singapore', True),
    (9, 'XSI', 'Tanjora Synthetic Airport', 'Tanjora', 'Singapore', 'SG', 'Southeast Asia', 1.360000, 103.700000, 'Asia/Singapore', True),
    (10, 'XIN', 'Suryanagar Synthetic Airport', 'Suryanagar', 'India', 'IN', 'South Asia', 28.620000, 77.210000, 'Asia/Kolkata', True),
    (11, 'XIO', 'Vasantpur Synthetic Airport', 'Vasantpur', 'India', 'IN', 'South Asia', 19.090000, 72.880000, 'Asia/Kolkata', True),
    (12, 'XIP', 'Neelambay Synthetic Airport', 'Neelambay', 'India', 'IN', 'South Asia', 12.980000, 77.600000, 'Asia/Kolkata', True),
    (13, 'XUK', 'Westmere Synthetic Airport', 'Westmere', 'United Kingdom', 'GB', 'Europe', 51.520000, -0.120000, 'Europe/London', True),
    (14, 'XUL', 'Northwick Synthetic Airport', 'Northwick', 'United Kingdom', 'GB', 'Europe', 55.960000, -3.210000, 'Europe/London', True),
    (15, 'XUM', 'Kingswell Synthetic Airport', 'Kingswell', 'United Kingdom', 'GB', 'Europe', 53.490000, -2.250000, 'Europe/London', True),
    (16, 'XDE', 'Eichenfeld Synthetic Airport', 'Eichenfeld', 'Germany', 'DE', 'Europe', 52.530000, 13.405000, 'Europe/Berlin', True),
    (17, 'XDF', 'Lindenhafen Synthetic Airport', 'Lindenhafen', 'Germany', 'DE', 'Europe', 48.150000, 11.580000, 'Europe/Berlin', True),
    (18, 'XDG', 'Westtal Synthetic Airport', 'Westtal', 'Germany', 'DE', 'Europe', 50.120000, 8.680000, 'Europe/Berlin', True),
    (19, 'XUS', 'Eastport Synthetic Airport', 'Eastport', 'United States', 'US', 'North America', 40.730000, -73.990000, 'America/New_York', True),
    (20, 'XUT', 'Midvale Synthetic Airport', 'Midvale', 'United States', 'US', 'North America', 41.890000, -87.630000, 'America/Chicago', True),
    (21, 'XUV', 'Suncrest Synthetic Airport', 'Suncrest', 'United States', 'US', 'North America', 34.060000, -118.240000, 'America/Los_Angeles', True),
    (22, 'XAU', 'Harbourton Synthetic Airport', 'Harbourton', 'Australia', 'AU', 'Oceania', -33.860000, 151.210000, 'Australia/Sydney', True),
    (23, 'XAW', 'Westhaven Synthetic Airport', 'Westhaven', 'Australia', 'AU', 'Oceania', -31.960000, 115.870000, 'Australia/Perth', True),
    (24, 'XAX', 'Southridge Synthetic Airport', 'Southridge', 'Australia', 'AU', 'Oceania', -34.940000, 138.600000, 'Australia/Adelaide', True),
    (25, 'XAH', 'Qamarah Synthetic Airport', 'Qamarah', 'United Arab Emirates', 'AE', 'Middle East', 23.550000, 53.720000, 'Asia/Dubai', True),
    (26, 'XAI', 'Nahran Synthetic Airport', 'Nahran', 'United Arab Emirates', 'AE', 'Middle East', 24.100000, 52.900000, 'Asia/Dubai', True),
    (27, 'XAJ', 'Barqah Synthetic Airport', 'Barqah', 'United Arab Emirates', 'AE', 'Middle East', 25.650000, 54.550000, 'Asia/Dubai', True),
    (28, 'XAK', 'Safirah Synthetic Airport', 'Safirah', 'United Arab Emirates', 'AE', 'Middle East', 26.000000, 56.100000, 'Asia/Dubai', True),
    (29, 'XAL', 'Zafran Synthetic Airport', 'Zafran', 'United Arab Emirates', 'AE', 'Middle East', 22.950000, 55.750000, 'Asia/Dubai', True),
    (30, 'XIQ', 'Aranya Synthetic Airport', 'Aranya', 'India', 'IN', 'South Asia', 22.570000, 88.360000, 'Asia/Kolkata', True),
    (31, 'XIR', 'Vihara Synthetic Airport', 'Vihara', 'India', 'IN', 'South Asia', 13.080000, 80.270000, 'Asia/Kolkata', True),
    (32, 'XIS', 'Keshav Synthetic Airport', 'Keshav', 'India', 'IN', 'South Asia', 17.380000, 78.490000, 'Asia/Kolkata', True),
    (33, 'XIT', 'Samudra Synthetic Airport', 'Samudra', 'India', 'IN', 'South Asia', 23.020000, 72.570000, 'Asia/Kolkata', True),
    (34, 'XIU', 'Pranava Synthetic Airport', 'Pranava', 'India', 'IN', 'South Asia', 9.930000, 76.260000, 'Asia/Kolkata', True),
    (35, 'XIV', 'Devika Synthetic Airport', 'Devika', 'India', 'IN', 'South Asia', 26.910000, 75.790000, 'Asia/Kolkata', True),
    (36, 'XIW', 'Suryakot Synthetic Airport', 'Suryakot', 'India', 'IN', 'South Asia', 26.140000, 91.740000, 'Asia/Kolkata', True),
    (37, 'XIX', 'Varunika Synthetic Airport', 'Varunika', 'India', 'IN', 'South Asia', 34.080000, 74.800000, 'Asia/Kolkata', True),
    (38, 'XIY', 'Amaya Synthetic Airport', 'Amaya', 'India', 'IN', 'South Asia', 20.300000, 85.820000, 'Asia/Kolkata', True),
    (39, 'XUN', 'Aldermere Synthetic Airport', 'Aldermere', 'United Kingdom', 'GB', 'Europe', 52.630000, -1.130000, 'Europe/London', True),
    (40, 'XUO', 'Bracken Synthetic Airport', 'Bracken', 'United Kingdom', 'GB', 'Europe', 54.600000, -5.930000, 'Europe/London', True),
    (41, 'XUP', 'Casterby Synthetic Airport', 'Casterby', 'United Kingdom', 'GB', 'Europe', 51.480000, -3.180000, 'Europe/London', True),
    (42, 'XUQ', 'Dunleigh Synthetic Airport', 'Dunleigh', 'United Kingdom', 'GB', 'Europe', 50.820000, -1.080000, 'Europe/London', True),
    (43, 'XUR', 'Elmswick Synthetic Airport', 'Elmswick', 'United Kingdom', 'GB', 'Europe', 52.950000, 1.150000, 'Europe/London', True),
    (44, 'XDH', 'Falken Synthetic Airport', 'Falken', 'Germany', 'DE', 'Europe', 53.550000, 9.990000, 'Europe/Berlin', True),
    (45, 'XDI', 'Granit Synthetic Airport', 'Granit', 'Germany', 'DE', 'Europe', 48.780000, 9.180000, 'Europe/Berlin', True),
    (46, 'XDJ', 'Hohen Synthetic Airport', 'Hohen', 'Germany', 'DE', 'Europe', 51.230000, 6.780000, 'Europe/Berlin', True),
    (47, 'XDK', 'Isenfeld Synthetic Airport', 'Isenfeld', 'Germany', 'DE', 'Europe', 51.340000, 12.370000, 'Europe/Berlin', True),
    (48, 'XDL', 'Jorvik Synthetic Airport', 'Jorvik', 'Germany', 'DE', 'Europe', 53.080000, 8.800000, 'Europe/Berlin', True),
    (49, 'XWA', 'Alder Synthetic Airport', 'Alder', 'United States', 'US', 'North America', 33.750000, -84.390000, 'America/New_York', True),
    (50, 'XWB', 'Bayhaven Synthetic Airport', 'Bayhaven', 'United States', 'US', 'North America', 32.780000, -96.800000, 'America/Chicago', True),
    (51, 'XWC', 'Crestview Synthetic Airport', 'Crestview', 'United States', 'US', 'North America', 39.740000, -104.990000, 'America/Denver', True),
    (52, 'XWD', 'Deltown Synthetic Airport', 'Deltown', 'United States', 'US', 'North America', 47.610000, -122.330000, 'America/Los_Angeles', True),
    (53, 'XWE', 'Evermont Synthetic Airport', 'Evermont', 'United States', 'US', 'North America', 25.760000, -80.190000, 'America/New_York', True),
    (54, 'XWF', 'Foxbridge Synthetic Airport', 'Foxbridge', 'United States', 'US', 'North America', 33.450000, -112.070000, 'America/Phoenix', True),
    (55, 'XWG', 'Glenport Synthetic Airport', 'Glenport', 'United States', 'US', 'North America', 37.770000, -122.420000, 'America/Los_Angeles', True),
    (56, 'XWH', 'Highmesa Synthetic Airport', 'Highmesa', 'United States', 'US', 'North America', 42.360000, -71.060000, 'America/New_York', True),
    (57, 'XWI', 'Ironwood Synthetic Airport', 'Ironwood', 'United States', 'US', 'North America', 29.760000, -95.370000, 'America/Chicago', True),
    (58, 'XWJ', 'Juniper Synthetic Airport', 'Juniper', 'United States', 'US', 'North America', 44.980000, -93.270000, 'America/Chicago', True),
    (59, 'XWK', 'Kingsbay Synthetic Airport', 'Kingsbay', 'United States', 'US', 'North America', 42.330000, -83.050000, 'America/Detroit', True),
    (60, 'XWL', 'Lakewood Synthetic Airport', 'Lakewood', 'United States', 'US', 'North America', 61.220000, -149.900000, 'America/Anchorage', True),
    (61, 'XBA', 'Amberley Synthetic Airport', 'Amberley', 'Australia', 'AU', 'Oceania', -37.810000, 144.960000, 'Australia/Melbourne', True),
    (62, 'XBB', 'Banksia Synthetic Airport', 'Banksia', 'Australia', 'AU', 'Oceania', -27.470000, 153.030000, 'Australia/Brisbane', True),
    (63, 'XBC', 'Coralton Synthetic Airport', 'Coralton', 'Australia', 'AU', 'Oceania', -12.460000, 130.840000, 'Australia/Darwin', True),
    (64, 'XBD', 'Duskvale Synthetic Airport', 'Duskvale', 'Australia', 'AU', 'Oceania', -42.880000, 147.330000, 'Australia/Hobart', True),
    (65, 'XBE', 'Eucalypt Synthetic Airport', 'Eucalypt', 'Australia', 'AU', 'Oceania', -35.280000, 149.130000, 'Australia/Sydney', True),
    (66, 'XBF', 'Fairhaven Synthetic Airport', 'Fairhaven', 'Australia', 'AU', 'Oceania', -28.020000, 153.430000, 'Australia/Brisbane', True),
    (67, 'XBG', 'Greenhaven Synthetic Airport', 'Greenhaven', 'Australia', 'AU', 'Oceania', -19.260000, 146.820000, 'Australia/Brisbane', True),
    (68, 'XBH', 'Highridge Synthetic Airport', 'Highridge', 'Australia', 'AU', 'Oceania', -16.920000, 145.770000, 'Australia/Brisbane', True),
    (69, 'XBI', 'Ironbark Synthetic Airport', 'Ironbark', 'Australia', 'AU', 'Oceania', -23.700000, 133.880000, 'Australia/Darwin', True),
    (70, 'XBJ', 'Jasper Bay Synthetic Airport', 'Jasper Bay', 'Australia', 'AU', 'Oceania', -17.960000, 122.240000, 'Australia/Perth', True),
    (71, 'XBK', 'Kookaburra Synthetic Airport', 'Kookaburra', 'Australia', 'AU', 'Oceania', -41.430000, 147.140000, 'Australia/Hobart', True),
    (72, 'XBL', 'Larkspur Synthetic Airport', 'Larkspur', 'Australia', 'AU', 'Oceania', -23.380000, 150.510000, 'Australia/Brisbane', True),
]

ALLOWED_COUNTRIES = {
    "AE", "QA", "SG", "IN", "GB", "DE", "US", "AU"
}

ALLOWED_REGIONS = {
    "Middle East",
    "Southeast Asia",
    "South Asia",
    "Europe",
    "North America",
    "Oceania"
}

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

# Fail clearly if the system does not have an IANA time-zone database.
for row in ROWS:
    zone_name = row[9]
    try:
        ZoneInfo(zone_name)
    except ZoneInfoNotFoundError as exc:
        raise RuntimeError(
            "IANA time-zone database is unavailable. "
            "Run: python -m pip install tzdata "
            "Then rerun this builder."
        ) from exc

df = pd.DataFrame(ROWS, columns=COLUMNS)

df = df.astype({
    "AirportKey": "int32",
    "AirportCode": "string",
    "AirportName": "string",
    "City": "string",
    "Country": "string",
    "CountryCode": "string",
    "Region": "string",
    "TimeZoneIANA": "string",
    "IsActive": "bool"
})

# Preserve six decimal places for the contract's Decimal(9,6) fields.
df["Latitude"] = [
    Decimal(str(v)).quantize(Decimal("0.000001"))
    for v in df["Latitude"]
]

df["Longitude"] = [
    Decimal(str(v)).quantize(Decimal("0.000001"))
    for v in df["Longitude"]
]

assert df.shape == (72, 11)
assert list(df.columns) == COLUMNS
assert df.notna().all().all()

assert df["AirportKey"].is_unique
assert df["AirportCode"].is_unique
assert df["AirportName"].is_unique
assert df["City"].is_unique

assert df["AirportCode"].str.fullmatch(r"[A-Z]{3}").all()
assert df["AirportCode"].str.startswith("X").all()

assert set(df["CountryCode"]) == ALLOWED_COUNTRIES
assert set(df["Region"]).issubset(ALLOWED_REGIONS)

assert all(-90 <= float(v) <= 90 for v in df["Latitude"])
assert all(-180 <= float(v) <= 180 for v in df["Longitude"])

assert df["IsActive"].all()
assert len(set(df["TimeZoneIANA"])) >= 10

# Verify each country is assigned to the intended broad region.
country_region = {
    "AE": "Middle East",
    "QA": "Middle East",
    "SG": "Southeast Asia",
    "IN": "South Asia",
    "GB": "Europe",
    "DE": "Europe",
    "US": "North America",
    "AU": "Oceania"
}

for _, row in df.iterrows():
    assert row["Region"] == country_region[row["CountryCode"]]
    ZoneInfo(str(row["TimeZoneIANA"]))

# Write CSV.
df.to_csv(CSV, index=False, encoding="utf-8-sig")

# Write Parquet with explicit contract types.
schema = pa.schema([
    pa.field("AirportKey", pa.int32(), nullable=False),
    pa.field("AirportCode", pa.string(), nullable=False),
    pa.field("AirportName", pa.string(), nullable=False),
    pa.field("City", pa.string(), nullable=False),
    pa.field("Country", pa.string(), nullable=False),
    pa.field("CountryCode", pa.string(), nullable=False),
    pa.field("Region", pa.string(), nullable=False),
    pa.field("Latitude", pa.decimal128(9, 6), nullable=False),
    pa.field("Longitude", pa.decimal128(9, 6), nullable=False),
    pa.field("TimeZoneIANA", pa.string(), nullable=False),
    pa.field("IsActive", pa.bool_(), nullable=False)
])

table = pa.Table.from_pandas(
    df,
    schema=schema,
    preserve_index=False,
    safe=True
)

pq.write_table(table, PARQUET, compression="snappy")

# Initial round-trip checks.
csv_check = pd.read_csv(CSV, encoding="utf-8-sig")
parquet_check = pd.read_parquet(PARQUET)
parquet_schema = pq.read_schema(PARQUET)

assert csv_check.shape == (72, 11)
assert parquet_check.shape == (72, 11)
assert list(parquet_check.columns) == COLUMNS

assert parquet_schema.field("AirportKey").type == pa.int32()
assert parquet_schema.field("Latitude").type == pa.decimal128(9, 6)
assert parquet_schema.field("Longitude").type == pa.decimal128(9, 6)

assert parquet_check["AirportCode"].is_unique
assert parquet_check["AirportKey"].is_unique

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    "dataset": "DimAirport",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    "grain": "One row per fictional airport",
    "primary_key": "AirportKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "airport_code_disclaimer": (
        "All airport codes are project-generated fictional identifiers. "
        "They are not official IATA airport codes."
    ),
    "geography_disclaimer": (
        "City and airport names are fictional. Coordinates are approximate "
        "geographic reference positions, not actual airport facility locations."
    ),
    "regions": sorted(df["Region"].unique().tolist()),
    "countries": sorted(df["CountryCode"].unique().tolist()),
    "validation": {
        "exact_column_order": True,
        "unique_airport_keys": True,
        "unique_airport_codes": True,
        "three_letter_uppercase_codes": True,
        "fictional_code_prefix": True,
        "unique_airport_names": True,
        "unique_city_names": True,
        "country_codes_in_baseline": True,
        "controlled_regions": True,
        "country_region_consistency": True,
        "latitude_bounds": True,
        "longitude_bounds": True,
        "valid_iana_timezones": True,
        "all_baseline_airports_active": True,
        "no_null_values": True,
        "parquet_int32_key": True,
        "parquet_decimal_9_6_coordinates": True,
        "csv_round_trip": True,
        "parquet_round_trip": True
    },
    "files": {
        "csv": {
            "path": "reports/network_expansion_20261104/staging/curated/dim_airport.csv",
            "sha256": sha256(CSV)
        },
        "parquet": {
            "path": "reports/network_expansion_20261104/staging/curated/dim_airport.parquet",
            "sha256": sha256(PARQUET)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("DIM_AIRPORT_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("COUNTRIES:", len(df["CountryCode"].unique()))
print("REGIONS:", len(df["Region"].unique()))
print("TIME ZONES:", len(df["TimeZoneIANA"].unique()))
print("VALID IANA TIME ZONES: PASSED")
print("DECIMAL(9,6) COORDINATES: PASSED")
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
