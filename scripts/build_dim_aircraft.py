from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from decimal import Decimal
import hashlib
import json

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]

OUT = ROOT / "data" / "03_curated"
MANIFESTS = ROOT / "data" / "manifests"

AIRLINE_WORKBOOK = (
    ROOT / "data" / "04_reference"
    / "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"
)

AIRCRAFT_TYPE_PATH = OUT / "dim_aircraft_type.parquet"

CSV = OUT / "dim_aircraft.csv"
PARQUET = OUT / "dim_aircraft.parquet"
MANIFEST = MANIFESTS / "dim_aircraft_manifest.json"

COLUMNS = [
    "AircraftKey",
    "AircraftRegistration",
    "AirlineKey",
    "AircraftTypeKey",
    "FleetEntryDate",
    "FleetStatus",
    "SeatCapacity",
    "PlannedDailyAvailableHours",
    "IsActive"
]

ALLOWED_FLEET_STATUSES = {
    "Active",
    "Maintenance",
    "Stored",
    "Retired"
}

# Provisional deterministic synthetic aircraft allocation.
# Every airline receives the same 44-aircraft type portfolio.
# Type assignments do not represent real airline fleets.
BASELINE_TYPE_ASSIGNMENTS = (
    [1] * 5 + [2] * 5 + [9] * 3
    + [3] * 4 + [4] * 4 + [10] * 4
    + [5] * 3 + [6] * 3 + [11] * 3
    + [7] * 4 + [8] * 3 + [12] * 3
)

TYPE_ASSIGNMENTS = {
    airline_key: list(BASELINE_TYPE_ASSIGNMENTS)
    for airline_key in range(1, 11)
}

# One maintenance aircraft in each category for every airline.
MAINTENANCE_SLOTS = {0, 13, 25, 34}

# Deterministic seat-capacity adjustments around typical capacity.
CAPACITY_OFFSETS = [0, -8, 6, -4, 10, -6, 4, -2, 8, -10, 2]

# OD-10 baseline assumption. It remains provisional pending formal approval.
PLANNED_DAILY_AVAILABLE_HOURS = Decimal("14.00")

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

if not AIRLINE_WORKBOOK.exists():
    raise FileNotFoundError(
        f"Required airline reference workbook missing: {AIRLINE_WORKBOOK}"
    )

if not AIRCRAFT_TYPE_PATH.exists():
    raise FileNotFoundError(
        f"Required aircraft type dimension missing: {AIRCRAFT_TYPE_PATH}"
    )

# ----------------------------------------------------------
# 1. Load and validate DimAirline from the reference workbook.
# ----------------------------------------------------------

wb = load_workbook(
    AIRLINE_WORKBOOK,
    read_only=True,
    data_only=True
)

if "DimAirline" not in wb.sheetnames:
    raise AssertionError("DimAirline sheet missing from reference workbook.")

ws = wb["DimAirline"]
rows = list(ws.iter_rows(values_only=True))

headers = list(rows[0])

expected_airline_columns = [
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
    "ReferenceVersion"
]

assert headers == expected_airline_columns

airline_index = {
    column: headers.index(column)
    for column in expected_airline_columns
}

airlines = []

for values in rows[1:]:
    if not values or all(v is None for v in values):
        continue

    record = {
        column: values[airline_index[column]]
        for column in expected_airline_columns
    }

    record["AirlineKey"] = int(record["AirlineKey"])
    airlines.append(record)

assert len(airlines) == 10

airline_keys = [row["AirlineKey"] for row in airlines]

assert len(set(airline_keys)) == 10
assert set(airline_keys) == set(range(1, 11))
assert all(row["IsActive"] is True for row in airlines)

airline_lookup = {
    row["AirlineKey"]: row
    for row in airlines
}

wb.close()

# ----------------------------------------------------------
# 2. Load and validate DimAircraftType.
# ----------------------------------------------------------

aircraft_types = pd.read_parquet(AIRCRAFT_TYPE_PATH)

expected_type_columns = [
    "AircraftTypeKey",
    "Manufacturer",
    "AircraftModel",
    "AircraftCategory",
    "TypicalSeatCapacity",
    "MaximumSeatCapacity",
    "RangeKM",
    "BodyType"
]

assert list(aircraft_types.columns) == expected_type_columns
assert aircraft_types.shape == (12, 8)
assert aircraft_types["AircraftTypeKey"].is_unique
assert aircraft_types.notna().all().all()

type_lookup = {
    int(row["AircraftTypeKey"]): row
    for _, row in aircraft_types.iterrows()
}

assert set(type_lookup) == set(range(1, 13))

# ----------------------------------------------------------
# 3. Generate deterministic synthetic aircraft records.
# ----------------------------------------------------------

records = []
aircraft_key = 1

for airline_key in range(1, 11):

    assert airline_key in airline_lookup
    assert airline_key in TYPE_ASSIGNMENTS

    assigned_types = TYPE_ASSIGNMENTS[airline_key]

    assert len(assigned_types) == 44

    for slot, aircraft_type_key in enumerate(assigned_types):

        assert aircraft_type_key in type_lookup

        aircraft_type = type_lookup[aircraft_type_key]

        typical_capacity = int(
            aircraft_type["TypicalSeatCapacity"]
        )

        maximum_capacity = int(
            aircraft_type["MaximumSeatCapacity"]
        )

        seat_capacity = (
            typical_capacity + CAPACITY_OFFSETS[slot % len(CAPACITY_OFFSETS)]
        )

        assert seat_capacity > 0
        assert seat_capacity <= maximum_capacity

        fleet_status = ("Maintenance" if slot in MAINTENANCE_SLOTS else "Active")

        # Maintenance aircraft remain in the fleet record,
        # but are not marked available in the baseline.
        is_active = fleet_status == "Active"

        fleet_entry_date = (
            date(2019, 1, 1)
            + timedelta(
                days=((airline_key * 173) + (slot * 47)) % 2000
            )
        )

        registration = f"SYN-A360-{aircraft_key:04d}"

        records.append({
            "AircraftKey": aircraft_key,
            "AircraftRegistration": registration,
            "AirlineKey": airline_key,
            "AircraftTypeKey": aircraft_type_key,
            "FleetEntryDate": fleet_entry_date,
            "FleetStatus": fleet_status,
            "SeatCapacity": seat_capacity,
            "PlannedDailyAvailableHours":
                PLANNED_DAILY_AVAILABLE_HOURS,
            "IsActive": is_active
        })

        aircraft_key += 1

df = pd.DataFrame(records, columns=COLUMNS)

# ----------------------------------------------------------
# 4. Structural and business-rule checks.
# ----------------------------------------------------------

df = df.astype({
    "AircraftKey": "int32",
    "AircraftRegistration": "string",
    "AirlineKey": "int32",
    "AircraftTypeKey": "int32",
    "FleetStatus": "string",
    "SeatCapacity": "int16",
    "IsActive": "bool"
})

assert df.shape == (440, 9)
assert list(df.columns) == COLUMNS
assert df.notna().all().all()

assert df["AircraftKey"].is_unique
assert df["AircraftRegistration"].is_unique

assert df["AircraftRegistration"].str.fullmatch(
    r"SYN-A360-[0-9]{4}"
).all()

assert set(df["AirlineKey"]) == set(airline_keys)
assert set(df["AircraftTypeKey"]) == set(type_lookup)

assert set(df["FleetStatus"]).issubset(
    ALLOWED_FLEET_STATUSES
)

assert (df["SeatCapacity"] > 0).all()

for _, aircraft in df.iterrows():

    aircraft_type = type_lookup[
        int(aircraft["AircraftTypeKey"])
    ]

    assert (
        int(aircraft["SeatCapacity"])
        <= int(aircraft_type["MaximumSeatCapacity"])
    )

    assert (
        aircraft["FleetEntryDate"]
        <= date(2025, 9, 30)
    )

    assert (
        Decimal(str(aircraft["PlannedDailyAvailableHours"]))
        == PLANNED_DAILY_AVAILABLE_HOURS
    )

    assert bool(aircraft["IsActive"]) == (
        aircraft["FleetStatus"] == "Active"
    )

# Each airline has 44 records: 40 active and 4 maintenance.
counts = df.groupby("AirlineKey").size()
active_counts = (
    df[df["IsActive"]]
    .groupby("AirlineKey")
    .size()
)
maintenance_counts = (
    df[df["FleetStatus"] == "Maintenance"]
    .groupby("AirlineKey")
    .size()
)

expected_airline_counts = {
    airline_key: 44 for airline_key in airline_keys
}
expected_active_counts = {
    airline_key: 40 for airline_key in airline_keys
}
expected_maintenance_counts = {
    airline_key: 4 for airline_key in airline_keys
}

assert counts.to_dict() == expected_airline_counts
assert active_counts.to_dict() == expected_active_counts
assert maintenance_counts.to_dict() == expected_maintenance_counts

assert int(df["IsActive"].sum()) == 400
assert int((df["FleetStatus"] == "Maintenance").sum()) == 40
assert int((~df["IsActive"]).sum()) == 40

# Validate exactly one maintenance aircraft per airline and category.
type_category = {
    int(row["AircraftTypeKey"]): str(row["AircraftCategory"])
    for _, row in aircraft_types.iterrows()
}

maintenance_by_category = df[
    df["FleetStatus"] == "Maintenance"
][["AirlineKey", "AircraftTypeKey"]].copy()

maintenance_by_category["AircraftCategory"] = (
    maintenance_by_category["AircraftTypeKey"].map(type_category)
)

maintenance_category_counts = maintenance_by_category.groupby(
    ["AirlineKey", "AircraftCategory"]
).size()

expected_maintenance_pairs = {
    (airline_key, str(category))
    for airline_key in airline_keys
    for category in aircraft_types["AircraftCategory"].unique()
}

assert set(maintenance_category_counts.index) == expected_maintenance_pairs
assert (maintenance_category_counts == 1).all()

# ----------------------------------------------------------
# 5. Write CSV and Parquet with explicit contract types.
# ----------------------------------------------------------

df.to_csv(CSV, index=False, encoding="utf-8-sig")

schema = pa.schema([
    pa.field("AircraftKey", pa.int32(), nullable=False),
    pa.field("AircraftRegistration", pa.string(), nullable=False),
    pa.field("AirlineKey", pa.int32(), nullable=False),
    pa.field("AircraftTypeKey", pa.int32(), nullable=False),
    pa.field("FleetEntryDate", pa.date32(), nullable=False),
    pa.field("FleetStatus", pa.string(), nullable=False),
    pa.field("SeatCapacity", pa.int16(), nullable=False),
    pa.field(
        "PlannedDailyAvailableHours",
        pa.decimal128(4, 2),
        nullable=False
    ),
    pa.field("IsActive", pa.bool_(), nullable=False)
])

table = pa.Table.from_pandas(
    df,
    schema=schema,
    preserve_index=False,
    safe=True
)

pq.write_table(table, PARQUET, compression="snappy")

# ----------------------------------------------------------
# 6. Initial round-trip and physical schema validation.
# ----------------------------------------------------------

csv_check = pd.read_csv(CSV, encoding="utf-8-sig")
parquet_check = pd.read_parquet(PARQUET)
parquet_schema = pq.read_schema(PARQUET)

assert csv_check.shape == (440, 9)
assert parquet_check.shape == (440, 9)

assert list(parquet_check.columns) == COLUMNS

assert parquet_schema.field("AircraftKey").type == pa.int32()
assert parquet_schema.field("AirlineKey").type == pa.int32()
assert parquet_schema.field("AircraftTypeKey").type == pa.int32()
assert parquet_schema.field("FleetEntryDate").type == pa.date32()
assert parquet_schema.field("SeatCapacity").type == pa.int16()
assert parquet_schema.field(
    "PlannedDailyAvailableHours"
).type == pa.decimal128(4, 2)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# ----------------------------------------------------------
# 7. Manifest and lineage.
# ----------------------------------------------------------

manifest = {
    "dataset": "DimAircraft",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    "grain": "One row per fictional aircraft",
    "primary_key": "AircraftKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "aircraft_allocation": {
        "airline_count": 10,
        "aircraft_per_airline": 44,
        "total_aircraft_records": 440,
        "baseline_active_records": 400,
        "active_per_airline": 40,
        "maintenance_records": 40,
        "maintenance_per_airline": 4,
        "aircraft_type_count": 12,
        "category_allocation_per_airline": {
            "Narrowbody": 13,
            "Widebody": 12,
            "Regional Jet": 9,
            "Turboprop": 10
        },
        "type_counts_per_airline": {
            str(key): BASELINE_TYPE_ASSIGNMENTS.count(key)
            for key in range(1, 13)
        },
        "maintenance_policy": (
            "One maintenance aircraft per airline in each of the four "
            "aircraft categories."
        )
    },
    "synthetic_fleet_disclaimer": (
        "Aircraft registrations, assignments, capacities, and fleet "
        "records are synthetic. They do not describe actual airline fleets."
    ),
    "planned_daily_available_hours": {
        "value": "14.00",
        "status": "PROVISIONAL — OD-10 FORMAL APPROVAL PENDING"
    },
    "fleet_status_rule": (
        "Active records are marked IsActive=true. Maintenance records "
        "remain in the dimension but are marked IsActive=false."
    ),
    "source_files": {
        "airline_reference_workbook": {
            "path": "data/04_reference/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx",
            "sha256": sha256(AIRLINE_WORKBOOK)
        },
        "dim_aircraft_type": {
            "path": "data/03_curated/dim_aircraft_type.parquet",
            "sha256": sha256(AIRCRAFT_TYPE_PATH)
        }
    },
    "validation": {
        "exact_column_order": True,
        "440_aircraft_records": True,
        "ten_airline_keys_resolved": True,
        "44_aircraft_per_airline": True,
        "400_active_aircraft_records": True,
        "40_maintenance_aircraft_records": True,
        "maintenance_one_per_category_per_airline": True,
        "twelve_aircraft_types_assigned": True,
        "unique_aircraft_keys": True,
        "unique_fictional_registrations": True,
        "aircraft_type_foreign_keys_resolve": True,
        "seat_capacity_positive": True,
        "seat_capacity_within_type_maximum": True,
        "fleet_status_controlled": True,
        "active_flag_consistent_with_status": True,
        "fleet_entry_dates_before_reporting_period": True,
        "planned_hours_consistent": True,
        "no_null_values": True,
        "parquet_int32_keys": True,
        "parquet_date32_fleet_entry_date": True,
        "parquet_int16_seat_capacity": True,
        "parquet_decimal_4_2_planned_hours": True,
        "csv_round_trip": True,
        "parquet_round_trip": True
    },
    "files": {
        "csv": {
            "path": "data/03_curated/dim_aircraft.csv",
            "sha256": sha256(CSV)
        },
        "parquet": {
            "path": "data/03_curated/dim_aircraft.parquet",
            "sha256": sha256(PARQUET)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("DIM_AIRCRAFT_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("AIRLINES:", df["AirlineKey"].nunique())
print("AIRCRAFT TYPES:", df["AircraftTypeKey"].nunique())
print("ACTIVE AIRCRAFT:", int(df["IsActive"].sum()))
print("MAINTENANCE AIRCRAFT:", int((~df["IsActive"]).sum()))
print("UNIQUE FICTIONAL REGISTRATIONS: PASSED")
print("AIRLINE AND TYPE REFERENCES: PASSED")
print("SEAT CAPACITY VALIDATION: PASSED")
print("PARQUET CONTRACT TYPES: PASSED")
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
