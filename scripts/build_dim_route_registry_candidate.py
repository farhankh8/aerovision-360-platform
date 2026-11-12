# EXPANDED CANDIDATE BUILDER: 160 connections / 320 directional routes.
# Writes to isolated staging directories only.

from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import math

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "network_expansion_20261104" / "registry_validation" / "curated"
MANIFESTS = ROOT / "reports" / "network_expansion_20261104" / "registry_validation" / "manifests"

AIRPORT_PATH = ROOT / "reports" / "network_expansion_20261104" / "staging" / "curated" / "dim_airport.parquet"
CSV = OUT / "dim_route.csv"
PARQUET = OUT / "dim_route.parquet"
MANIFEST = MANIFESTS / "dim_route_manifest.json"

COLUMNS = [
    "RouteKey",
    "RouteCode",
    "OriginAirportKey",
    "DestinationAirportKey",
    "DistanceKM",
    "DistanceMiles",
    "RouteRegion",
    "IsInternational",
    "IsActive"
]

# Each tuple defines one undirected synthetic connection.
# The builder creates both directional routes automatically.
UNDIRECTED_CONNECTIONS = [
    ('XAE', 'XAH'),
    ('XAE', 'XAI'),
    ('XAE', 'XAK'),
    ('XAE', 'XAU'),
    ('XAE', 'XDE'),
    ('XAE', 'XIN'),
    ('XAE', 'XQA'),
    ('XAE', 'XSG'),
    ('XAE', 'XUK'),
    ('XAE', 'XUS'),
    ('XAF', 'XAI'),
    ('XAF', 'XAL'),
    ('XAF', 'XUK'),
    ('XAG', 'XAH'),
    ('XAG', 'XIN'),
    ('XAG', 'XQC'),
    ('XAH', 'XAJ'),
    ('XAH', 'XAL'),
    ('XAH', 'XQB'),
    ('XAH', 'XQC'),
    ('XAI', 'XQC'),
    ('XAJ', 'XAK'),
    ('XAJ', 'XQA'),
    ('XAK', 'XIO'),
    ('XAL', 'XIO'),
    ('XAU', 'XAW'),
    ('XAU', 'XAX'),
    ('XAU', 'XBA'),
    ('XAU', 'XBD'),
    ('XAU', 'XBE'),
    ('XAU', 'XBF'),
    ('XAU', 'XBK'),
    ('XAU', 'XSG'),
    ('XAU', 'XSI'),
    ('XAW', 'XIW'),
    ('XAW', 'XSH'),
    ('XAX', 'XBI'),
    ('XAX', 'XIN'),
    ('XBA', 'XBE'),
    ('XBA', 'XBK'),
    ('XBB', 'XBG'),
    ('XBB', 'XBH'),
    ('XBB', 'XBI'),
    ('XBB', 'XBL'),
    ('XBB', 'XSH'),
    ('XBC', 'XBI'),
    ('XBC', 'XBJ'),
    ('XBC', 'XIU'),
    ('XBD', 'XBK'),
    ('XBD', 'XSH'),
    ('XBE', 'XIS'),
    ('XBF', 'XBL'),
    ('XBF', 'XIT'),
    ('XBF', 'XWK'),
    ('XBG', 'XBH'),
    ('XBG', 'XBL'),
    ('XBH', 'XDI'),
    ('XBH', 'XSH'),
    ('XBJ', 'XIR'),
    ('XBJ', 'XSH'),
    ('XDE', 'XDF'),
    ('XDE', 'XDG'),
    ('XDE', 'XDH'),
    ('XDE', 'XDI'),
    ('XDE', 'XDK'),
    ('XDE', 'XQA'),
    ('XDE', 'XQC'),
    ('XDE', 'XUK'),
    ('XDE', 'XUS'),
    ('XDF', 'XQB'),
    ('XDF', 'XUT'),
    ('XDG', 'XDI'),
    ('XDG', 'XDJ'),
    ('XDG', 'XUQ'),
    ('XDH', 'XQB'),
    ('XDH', 'XUK'),
    ('XDH', 'XUL'),
    ('XDH', 'XUM'),
    ('XDH', 'XUR'),
    ('XDI', 'XQB'),
    ('XDJ', 'XDL'),
    ('XDJ', 'XUK'),
    ('XDJ', 'XUR'),
    ('XDK', 'XQB'),
    ('XDK', 'XUT'),
    ('XDL', 'XSG'),
    ('XDL', 'XUK'),
    ('XIN', 'XIO'),
    ('XIN', 'XIP'),
    ('XIN', 'XIV'),
    ('XIN', 'XIX'),
    ('XIN', 'XQA'),
    ('XIN', 'XQB'),
    ('XIN', 'XSG'),
    ('XIN', 'XWH'),
    ('XIN', 'XWJ'),
    ('XIO', 'XIT'),
    ('XIO', 'XIV'),
    ('XIO', 'XIX'),
    ('XIO', 'XSH'),
    ('XIO', 'XWE'),
    ('XIO', 'XWI'),
    ('XIO', 'XWK'),
    ('XIP', 'XIR'),
    ('XIP', 'XIS'),
    ('XIP', 'XIU'),
    ('XIP', 'XIY'),
    ('XIQ', 'XIW'),
    ('XIQ', 'XIY'),
    ('XIQ', 'XSI'),
    ('XIR', 'XQB'),
    ('XIS', 'XIY'),
    ('XIT', 'XQB'),
    ('XIU', 'XQB'),
    ('XIV', 'XQB'),
    ('XIW', 'XQB'),
    ('XIX', 'XQB'),
    ('XQC', 'XUT'),
    ('XSG', 'XUK'),
    ('XSG', 'XUM'),
    ('XSG', 'XUO'),
    ('XSG', 'XUQ'),
    ('XSG', 'XWL'),
    ('XSI', 'XWF'),
    ('XUK', 'XUL'),
    ('XUK', 'XUM'),
    ('XUK', 'XUR'),
    ('XUK', 'XUS'),
    ('XUL', 'XUO'),
    ('XUN', 'XUO'),
    ('XUN', 'XUP'),
    ('XUN', 'XUQ'),
    ('XUN', 'XUR'),
    ('XUP', 'XUQ'),
    ('XUP', 'XUT'),
    ('XUS', 'XUT'),
    ('XUS', 'XUV'),
    ('XUS', 'XWH'),
    ('XUS', 'XWK'),
    ('XUT', 'XWA'),
    ('XUT', 'XWE'),
    ('XUT', 'XWH'),
    ('XUT', 'XWJ'),
    ('XUT', 'XWK'),
    ('XUV', 'XWF'),
    ('XUV', 'XWG'),
    ('XWA', 'XWB'),
    ('XWA', 'XWC'),
    ('XWA', 'XWE'),
    ('XWA', 'XWF'),
    ('XWA', 'XWG'),
    ('XWA', 'XWI'),
    ('XWA', 'XWJ'),
    ('XWB', 'XWC'),
    ('XWB', 'XWI'),
    ('XWC', 'XWD'),
    ('XWC', 'XWF'),
    ('XWC', 'XWL'),
    ('XWD', 'XWG'),
    ('XWD', 'XWL'),
]

EARTH_MEAN_RADIUS_KM = 6371.0088
MILES_CONVERSION = Decimal("0.621371")
TWO_DECIMALS = Decimal("0.01")

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

if not AIRPORT_PATH.exists():
    raise FileNotFoundError(
        f"Required DimAirport dataset not found: {AIRPORT_PATH}"
    )

for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

airports = pd.read_parquet(AIRPORT_PATH)

expected_airport_columns = [
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

assert list(airports.columns) == expected_airport_columns
assert airports["AirportKey"].is_unique
assert airports["AirportCode"].is_unique
assert airports.notna().all().all()

airport_lookup = {
    str(row["AirportCode"]): row
    for _, row in airports.iterrows()
}

# Validate the connection specification.
assert len(UNDIRECTED_CONNECTIONS) == 160
assert len(set(UNDIRECTED_CONNECTIONS)) == 160

for origin, destination in UNDIRECTED_CONNECTIONS:
    assert origin in airport_lookup, f"Unknown airport: {origin}"
    assert destination in airport_lookup, f"Unknown airport: {destination}"
    assert origin != destination

# Calculate great-circle distance using the Haversine formula.
def haversine_km(origin, destination):
    lat1 = math.radians(float(origin["Latitude"]))
    lon1 = math.radians(float(origin["Longitude"]))
    lat2 = math.radians(float(destination["Latitude"]))
    lon2 = math.radians(float(destination["Longitude"]))

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    a = max(0.0, min(1.0, a))
    central_angle = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return EARTH_MEAN_RADIUS_KM * central_angle


route_records = []

for airport_a, airport_b in UNDIRECTED_CONNECTIONS:
    for origin_code, destination_code in [
        (airport_a, airport_b),
        (airport_b, airport_a)
    ]:
        origin = airport_lookup[origin_code]
        destination = airport_lookup[destination_code]

        raw_distance = haversine_km(origin, destination)

        assert raw_distance > 0

        distance_km = Decimal(
            str(raw_distance)
        ).quantize(TWO_DECIMALS, rounding=ROUND_HALF_UP)

        distance_miles = (
            distance_km * MILES_CONVERSION
        ).quantize(TWO_DECIMALS, rounding=ROUND_HALF_UP)

        # RouteRegion is a controlled reporting group:
        # same-region routes retain that region;
        # cross-region routes are labelled Interregional.
        if origin["Region"] == destination["Region"]:
            route_region = str(origin["Region"])
        else:
            route_region = "Interregional"

        route_records.append({
            "RouteCode": f"{origin_code}-{destination_code}",
            "OriginAirportKey": int(origin["AirportKey"]),
            "DestinationAirportKey": int(destination["AirportKey"]),
            "DistanceKM": distance_km,
            "DistanceMiles": distance_miles,
            "RouteRegion": route_region,
            "IsInternational": (
                str(origin["CountryCode"])
                != str(destination["CountryCode"])
            ),
            "IsActive": True,
            "_RawDistanceKM": raw_distance
        })


# Load the permanent versioned RouteCode-to-RouteKey registry.
ROUTE_KEYMAP_PATH = (
    ROOT / "data" / "04_reference" / "DIM_ROUTE_KEYMAP_V1.csv"
)

ROUTE_KEYMAP_MANIFEST_PATH = (
    ROOT / "data" / "04_reference"
    / "DIM_ROUTE_KEYMAP_V1_MANIFEST.json"
)

EXPECTED_ROUTE_KEYMAP_SHA256 = (
    "c410627a1c6c377333ca301ee2acc4ee"
    "10b05261cd7c3e595503ee3356482199"
)

if not ROUTE_KEYMAP_PATH.exists():
    raise FileNotFoundError(ROUTE_KEYMAP_PATH)

if not ROUTE_KEYMAP_MANIFEST_PATH.exists():
    raise FileNotFoundError(ROUTE_KEYMAP_MANIFEST_PATH)

route_keymap_hash = hashlib.sha256(
    ROUTE_KEYMAP_PATH.read_bytes()
).hexdigest()

assert route_keymap_hash == EXPECTED_ROUTE_KEYMAP_SHA256, (
    "Permanent route key registry SHA256 mismatch."
)

route_keymap_manifest = json.loads(
    ROUTE_KEYMAP_MANIFEST_PATH.read_text(encoding="utf-8")
)

assert route_keymap_manifest.get("dataset") == "DimRouteKeyMap"
assert route_keymap_manifest.get("version") == "V1"
assert route_keymap_manifest.get("status") == "IMMUTABLE_VERSIONED_REFERENCE"
assert route_keymap_manifest.get("row_count") == 320

assert (
    route_keymap_manifest.get("files", {})
    .get("csv", {})
    .get("sha256")
    == route_keymap_hash
), "Route key registry manifest hash mismatch."

route_keymap_df = pd.read_csv(
    ROUTE_KEYMAP_PATH,
    encoding="utf-8-sig"
)

assert route_keymap_df.shape == (320, 2)
assert list(route_keymap_df.columns) == ["RouteKey", "RouteCode"]
assert route_keymap_df["RouteKey"].is_unique
assert route_keymap_df["RouteCode"].is_unique

assert set(
    route_keymap_df["RouteKey"].astype(int)
) == set(range(1, 321))

existing_route_key_map = {
    str(row["RouteCode"]): int(row["RouteKey"])
    for _, row in route_keymap_df.iterrows()
}

current_route_codes = {
    str(record["RouteCode"])
    for record in route_records
}

assert current_route_codes == set(existing_route_key_map), (
    "Generated network route identities do not exactly match "
    "the permanent registry."
)

for record in route_records:
    code = str(record["RouteCode"])
    record["RouteKey"] = existing_route_key_map[code]

assert len(route_records) == 320
assert len({record["RouteKey"] for record in route_records}) == 320

# Output order is deterministic and follows the assigned surrogate key.
route_records.sort(key=lambda x: x["RouteKey"])


df = pd.DataFrame(route_records)

# Remove internal calculation field from output.
raw_distances = df["_RawDistanceKM"].tolist()
df = df.drop(columns=["_RawDistanceKM"])

df = df[COLUMNS]

df = df.astype({
    "RouteKey": "int32",
    "RouteCode": "string",
    "OriginAirportKey": "int32",
    "DestinationAirportKey": "int32",
    "RouteRegion": "string",
    "IsInternational": "bool",
    "IsActive": "bool"
})

# Structural validation.
assert df.shape == (320, 9)
assert list(df.columns) == COLUMNS
assert df.notna().all().all()

assert df["RouteKey"].is_unique
assert df["RouteCode"].is_unique

assert (
    df["OriginAirportKey"] != df["DestinationAirportKey"]
).all()

assert (
    df["DistanceKM"].map(lambda x: Decimal(str(x))) > 0
).all()

assert (
    df["DistanceMiles"].map(lambda x: Decimal(str(x))) > 0
).all()

# Every directional pair must be unique.
assert not df.duplicated(
    ["OriginAirportKey", "DestinationAirportKey"]
).any()

# Route code must match the airport keys.
airport_code_by_key = {
    int(row["AirportKey"]): str(row["AirportCode"])
    for _, row in airports.iterrows()
}

for _, route in df.iterrows():
    expected_code = (
        airport_code_by_key[int(route["OriginAirportKey"])]
        + "-"
        + airport_code_by_key[int(route["DestinationAirportKey"])]
    )
    assert route["RouteCode"] == expected_code

# Verify referential integrity and every airport's network participation.
valid_airport_keys = set(airports["AirportKey"].astype(int))

referenced_keys = (
    set(df["OriginAirportKey"].astype(int))
    | set(df["DestinationAirportKey"].astype(int))
)

assert referenced_keys == valid_airport_keys

# Validate reciprocal directional routes.
route_lookup = set(df["RouteCode"].astype(str))

for _, route in df.iterrows():
    reverse_code = (
        airport_code_by_key[int(route["DestinationAirportKey"])]
        + "-"
        + airport_code_by_key[int(route["OriginAirportKey"])]
    )
    assert reverse_code in route_lookup

# Verify route distance against original unrounded Haversine distance.
for index, route in df.iterrows():
    rounded_km = float(route["DistanceKM"])
    raw_km = raw_distances[index]

    relative_error = abs(rounded_km - raw_km) / raw_km
    assert relative_error <= 0.02

    expected_miles = (
        Decimal(str(route["DistanceKM"])) * MILES_CONVERSION
    ).quantize(TWO_DECIMALS, rounding=ROUND_HALF_UP)

    assert Decimal(str(route["DistanceMiles"])) == expected_miles

# Validate domestic / international classification.
for _, route in df.iterrows():
    origin = airports.loc[
        airports["AirportKey"] == route["OriginAirportKey"]
    ].iloc[0]

    destination = airports.loc[
        airports["AirportKey"] == route["DestinationAirportKey"]
    ].iloc[0]

    expected_international = (
        origin["CountryCode"] != destination["CountryCode"]
    )

    assert bool(route["IsInternational"]) == bool(expected_international)

allowed_route_regions = (
    set(airports["Region"].astype(str).unique())
    | {"Interregional"}
)

assert set(df["RouteRegion"].astype(str)).issubset(
    allowed_route_regions
)

assert df["IsActive"].all()

# Write CSV.
df.to_csv(CSV, index=False, encoding="utf-8-sig")

# Write Parquet with explicit contract data types.
schema = pa.schema([
    pa.field("RouteKey", pa.int32(), nullable=False),
    pa.field("RouteCode", pa.string(), nullable=False),
    pa.field("OriginAirportKey", pa.int32(), nullable=False),
    pa.field("DestinationAirportKey", pa.int32(), nullable=False),
    pa.field("DistanceKM", pa.decimal128(9, 2), nullable=False),
    pa.field("DistanceMiles", pa.decimal128(9, 2), nullable=False),
    pa.field("RouteRegion", pa.string(), nullable=False),
    pa.field("IsInternational", pa.bool_(), nullable=False),
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

assert csv_check.shape == (320, 9)
assert parquet_check.shape == (320, 9)
assert list(parquet_check.columns) == COLUMNS

assert parquet_schema.field("RouteKey").type == pa.int32()
assert parquet_schema.field("OriginAirportKey").type == pa.int32()
assert parquet_schema.field("DistanceKM").type == pa.decimal128(9, 2)
assert parquet_schema.field("DistanceMiles").type == pa.decimal128(9, 2)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    "dataset": "DimRoute",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    "grain": "One row per directional origin-destination airport pair",
    "primary_key": "RouteKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "undirected_connection_count": len(UNDIRECTED_CONNECTIONS),
    "directional_route_count": len(df),
    "columns": COLUMNS,
    "distance_method": "Haversine great-circle distance",
    "earth_mean_radius_km": EARTH_MEAN_RADIUS_KM,
    "distance_tolerance_percent": 2,
    "distance_miles_conversion": "DistanceKM * 0.621371, rounded to 2 decimals",
    "route_region_rule": (
        "Same-region routes retain the airport region; "
        "cross-region routes are labelled Interregional."
    ),
    "source": {
        "path": "reports/network_expansion_20261104/staging/curated/dim_airport.parquet",
        "sha256": sha256(AIRPORT_PATH)
    },
    "route_key_registry": {
        "path": "data/04_reference/DIM_ROUTE_KEYMAP_V1.csv",
        "version": "V1",
        "row_count": len(route_keymap_df),
        "sha256": sha256(ROUTE_KEYMAP_PATH)
    },
    "route_regions": sorted(df["RouteRegion"].unique().tolist()),
    "validation": {
        "exact_column_order": True,
        "unique_route_keys": True,
        "unique_directional_route_codes": True,
        "unique_directional_airport_pairs": True,
        "different_origin_and_destination": True,
        "positive_distances": True,
        "great_circle_distance_within_2_percent": True,
        "miles_conversion": True,
        "route_code_consistency": True,
        "airport_referential_integrity": True,
        "all_airports_used": True,
        "reciprocal_directional_routes": True,
        "international_flag_consistency": True,
        "controlled_route_regions": True,
        "all_baseline_routes_active": True,
        "no_null_values": True,
        "parquet_int32_keys": True,
        "parquet_decimal_9_2_distances": True,
        "csv_round_trip": True,
        "parquet_round_trip": True
    },
    "files": {
        "csv": {
            "path": "reports/network_expansion_20261104/staging/curated/dim_route.csv",
            "sha256": sha256(CSV)
        },
        "parquet": {
            "path": "reports/network_expansion_20261104/staging/curated/dim_route.parquet",
            "sha256": sha256(PARQUET)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("DIM_ROUTE_BUILD_SUCCESS")
print("UNDIRECTED_CONNECTIONS:", len(UNDIRECTED_CONNECTIONS))
print("DIRECTIONAL_ROUTES:", len(df))
print("AIRPORTS_CONNECTED:", len(referenced_keys))
print("INTERNATIONAL_ROUTES:", int(df["IsInternational"].sum()))
print("DOMESTIC_ROUTES:", int((~df["IsInternational"]).sum()))
print("ROUTE REGIONS:", ", ".join(sorted(df["RouteRegion"].unique())))
print("GREAT-CIRCLE DISTANCE VALIDATION: PASSED")
print("DISTANCE MILES CONVERSION: PASSED")
print("REFERENTIAL INTEGRITY: PASSED")
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
