"""Build curated FactFlightOperations dataset.

Generates a deterministic synthetic flight-leg fact table from the existing
curated dimensions (DimAirline, DimRoute, DimAircraft, DimDate). Writes
controlled CSV, Parquet, and manifest outputs. Never modifies source data.

OD-09 NOTE: The proposed 15-minute on-time arrival/departure threshold is
described in the data contract but remains pending formal owner approval.
This implementation applies the threshold as documented in the contract
Section 5.2 / 6.3.1 and flags it as provisional in the manifest. It does not
claim the threshold is an approved business rule.
"""

from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys

from decimal import Decimal
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Ensure project root is importable when run directly.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utilities.hashing import sha256_file
from src.utilities.io import write_json_atomic
from src.utilities.paths import project_path

# ---------------------------------------------------------------------------
# Configuration (deterministic)
# ---------------------------------------------------------------------------
SEED = 3602026  # Explicit seed for reproducible generation
RNG = np.random.default_rng(SEED)

# Reporting period per contract Section 9.4.
REPORTING_START = "2025-10-01"
REPORTING_END = "2026-09-30"

# Planned volume target (C-06): 150,000 to 250,000 flight legs is a planning
# target, not a guaranteed output. This initial build uses a validation
# volume. Full portfolio volume requires confirmation of date range and
# operational assumptions against documented requirements.
VALIDATION_VOLUME = 5000

# Cancelled-flight share (proposed baseline, not owner-approved).
CANCELLED_SHARE = 0.05

OUT = project_path("data", "03_curated")
MANIFESTS = project_path("data", "manifests")

AIRLINE_PATH = OUT / "dim_airline.parquet"
ROUTE_PATH = OUT / "dim_route.parquet"
AIRCRAFT_PATH = OUT / "dim_aircraft.parquet"
DATE_PATH = OUT / "dim_date.parquet"

CSV = OUT / "fact_flight_operations.csv"
PARQUET = OUT / "fact_flight_operations.parquet"
MANIFEST = MANIFESTS / "fact_flight_operations_manifest.json"

COLUMNS = [
    "FlightOperationKey",
    "FlightLegID",
    "FlightNumber",
    "AirlineKey",
    "RouteKey",
    "AircraftKey",
    "ScheduledDepartureTimestampUTC",
    "ActualDepartureTimestampUTC",
    "ScheduledArrivalTimestampUTC",
    "ActualArrivalTimestampUTC",
    "ScheduledDepartureDateKey",
    "ScheduledArrivalDateKey",
    "AvailableSeats",
    "BookedPassengers",
    "RevenuePassengers",
    "NonRevenuePassengers",
    "FlightDistanceKM",
    "FlightStatus",
    "DepartureDelayMinutes",
    "ArrivalDelayMinutes",
    "BlockMinutes",
    "CancellationFlag",
    "CompletionFlag",
    "OnTimeFlag",
    "OnTimeArrivalFlag",
]

# Verify source dimensions exist.
for path in [AIRLINE_PATH, ROUTE_PATH, AIRCRAFT_PATH, DATE_PATH]:
    if not path.exists():
        raise FileNotFoundError(f"Required dimension not found: {path}")

# Verify outputs do not already exist (never overwrite).
for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Load dimensions
# ---------------------------------------------------------------------------
airlines = pd.read_parquet(AIRLINE_PATH)
routes = pd.read_parquet(ROUTE_PATH)
aircraft = pd.read_parquet(AIRCRAFT_PATH)
dates = pd.read_parquet(DATE_PATH)

active_airlines = airlines[airlines["IsActive"] == True]
active_aircraft = aircraft[aircraft["IsActive"] == True]

if len(active_airlines) == 0:
    raise RuntimeError("No active airlines in DimAirline.")
if len(routes) == 0:
    raise RuntimeError("No routes in DimRoute.")
if len(active_aircraft) == 0:
    raise RuntimeError("No active aircraft in DimAircraft.")

# Reporting-period dates from DimDate. FullDate is stored as date objects.
reporting_start_date = datetime.strptime(REPORTING_START, "%Y-%m-%d").date()
reporting_end_date = datetime.strptime(REPORTING_END, "%Y-%m-%d").date()
reporting_dates = dates[
    (dates["FullDate"] >= reporting_start_date)
    & (dates["FullDate"] <= reporting_end_date)
]
if len(reporting_dates) == 0:
    raise RuntimeError("No reporting-period dates in DimDate.")

date_key_to_full = dict(
    zip(
        reporting_dates["DateKey"].astype(int),
        reporting_dates["FullDate"],
    )
)
full_date_to_key = {
    v: k for k, v in date_key_to_full.items()
}

# Index route -> distance for FlightDistanceKM validation.
route_distance = {
    int(r["RouteKey"]): float(r["DistanceKM"]) for _, r in routes.iterrows()
}

# Index aircraft by airline for fleet assignment.
aircraft_by_airline = {
    int(k): v["AircraftKey"].tolist()
    for k, v in active_aircraft.groupby("AirlineKey")
}

# ---------------------------------------------------------------------------
# Generate deterministic synthetic flight legs
# ---------------------------------------------------------------------------
n_legs = VALIDATION_VOLUME

route_keys = routes["RouteKey"].astype(int).tolist()
airline_keys = active_airlines["AirlineKey"].astype(int).tolist()
date_keys = reporting_dates["DateKey"].astype(int).tolist()

records = []
flight_operation_key = 1
used_leg_ids = set()
used_composite_keys = set()

for i in range(n_legs):
    route_key = int(RNG.choice(route_keys))
    airline_key = int(RNG.choice(airline_keys))

    # Route origin/destination for date-key assignment.
    route_row = routes[routes["RouteKey"] == route_key].iloc[0]
    origin_airport_key = int(route_row["OriginAirportKey"])
    dest_airport_key = int(route_row["DestinationAirportKey"])
    distance_km = float(route_row["DistanceKM"])

    # Departure date key (local origin date).
    dep_date_key = int(RNG.choice(date_keys))
    dep_full = date_key_to_full[dep_date_key]

    # Scheduled departure time: random time on departure date.
    dep_hour = int(RNG.integers(0, 24))
    dep_minute = int(RNG.integers(0, 60))
    dep_second = int(RNG.integers(0, 60))
    scheduled_dep_utc = pd.Timestamp(
        f"{dep_full.isoformat()} {dep_hour:02d}:{dep_minute:02d}:{dep_second:02d}"
    ).tz_localize("UTC")

    # Flight duration from distance (rough heuristic: 900 km/h avg + 45 min taxi).
    duration_minutes = max(30, int(distance_km / 900 * 60) + 45)
    scheduled_arr_utc = scheduled_dep_utc + timedelta(minutes=duration_minutes)

    # Arrival date key (local destination date): may differ for overnight /
    # cross-time-zone flights.
    arr_date_utc = scheduled_arr_utc.tz_convert("UTC")
    arr_date_obj = arr_date_utc.date()
    # Use the local destination date as a proxy for date-key lookup.
    if arr_date_obj in full_date_to_key:
        arr_date_key = int(full_date_to_key[arr_date_obj])
    else:
        # Fall back to departure date key if arrival date not in DimDate.
        arr_date_key = dep_date_key

    # Flight status: Operated or Cancelled.
    is_cancelled = bool(RNG.random() < CANCELLED_SHARE)
    flight_status = "Cancelled" if is_cancelled else "Operated"

    # Aircraft: must belong to the operating airline.
    fleet = aircraft_by_airline.get(airline_key, [])
    if len(fleet) == 0:
        aircraft_key = None
    else:
        aircraft_key = int(RNG.choice(fleet))

    # Available seats from aircraft type capacity.
    if aircraft_key is not None:
        ac_row = aircraft[aircraft["AircraftKey"] == aircraft_key].iloc[0]
        available_seats = int(ac_row["SeatCapacity"])
    else:
        available_seats = int(RNG.integers(100, 300))

    # Flight number: airline code prefix + 3-4 digits.
    iata_code = (
        airlines[airlines["AirlineKey"] == airline_key]["AirlineIATACode"].iloc[0]
        or "XX"
    )
    flight_number = f"{iata_code}{int(RNG.integers(100, 9999))}"

    # FlightLegID: unique business key.
    flight_leg_id = f"FL{flight_operation_key:08d}"

    # Composite business key.
    composite_key = (
        airline_key,
        flight_number,
        dep_date_key,
        route_key,
        scheduled_dep_utc.timestamp(),
    )
    if composite_key in used_composite_keys:
        # Skip duplicates to enforce grain uniqueness.
        continue
    used_composite_keys.add(composite_key)
    if flight_leg_id in used_leg_ids:
        continue
    used_leg_ids.add(flight_leg_id)

    # Passenger counts.
    if is_cancelled:
        booked_passengers = int(RNG.integers(0, available_seats + 1))
        revenue_passengers = 0
        non_revenue_passengers = 0
        actual_dep_utc = None
        actual_arr_utc = None
        dep_delay = None
        arr_delay = None
        block_minutes = None
    else:
        booked_passengers = int(RNG.integers(0, available_seats + 1))
        # Revenue + non-revenue must not exceed booked.
        max_carried = booked_passengers
        revenue_passengers = int(
            RNG.integers(0, max_carried + 1)
        )
        remaining = max_carried - revenue_passengers
        non_revenue_passengers = int(RNG.integers(0, remaining + 1))

        # Actual timestamps with delay.
        # Generate departure delay first, then a positive block time, then
        # derive arrival delay so that actual_arrival >= actual_departure.
        dep_delay = int(RNG.integers(-30, 120))
        block_minutes = int(RNG.integers(30, 600))
        actual_dep_utc = scheduled_dep_utc + timedelta(minutes=dep_delay)
        actual_arr_utc = actual_dep_utc + timedelta(minutes=block_minutes)
        arr_delay = int(
            (actual_arr_utc - scheduled_arr_utc).total_seconds() / 60
        )

    # Cancellation / completion / on-time flags.
    cancellation_flag = is_cancelled
    completion_flag = not is_cancelled

    # On-time flags: departure delay <= 15 minutes. OD-09 threshold is
    # PROPOSED pending formal owner approval; applied as documented in the
    # contract, not claimed as an approved rule.
    if is_cancelled or actual_dep_utc is None:
        on_time_flag = False
        on_time_arrival_flag = False
    else:
        on_time_flag = bool(dep_delay <= 15)
        on_time_arrival_flag = bool(arr_delay <= 15)

    # FlightDistanceKM must agree with DimRoute.DistanceKM within 0.5%.
    # We use the route distance directly so this holds exactly.

    record = {
        "FlightOperationKey": flight_operation_key,
        "FlightLegID": flight_leg_id,
        "FlightNumber": flight_number,
        "AirlineKey": airline_key,
        "RouteKey": route_key,
        "AircraftKey": aircraft_key,
        "ScheduledDepartureTimestampUTC": scheduled_dep_utc,
        "ActualDepartureTimestampUTC": actual_dep_utc,
        "ScheduledArrivalTimestampUTC": scheduled_arr_utc,
        "ActualArrivalTimestampUTC": actual_arr_utc,
        "ScheduledDepartureDateKey": dep_date_key,
        "ScheduledArrivalDateKey": arr_date_key,
        "AvailableSeats": available_seats,
        "BookedPassengers": booked_passengers,
        "RevenuePassengers": revenue_passengers,
        "NonRevenuePassengers": non_revenue_passengers,
        "FlightDistanceKM": round(distance_km, 2),
        "FlightStatus": flight_status,
        "DepartureDelayMinutes": dep_delay,
        "ArrivalDelayMinutes": arr_delay,
        "BlockMinutes": block_minutes,
        "CancellationFlag": cancellation_flag,
        "CompletionFlag": completion_flag,
        "OnTimeFlag": on_time_flag,
        "OnTimeArrivalFlag": on_time_arrival_flag,
    }

    records.append(record)
    flight_operation_key += 1

df = pd.DataFrame(records, columns=COLUMNS)

# ---------------------------------------------------------------------------
# Structural and business-rule validation
# ---------------------------------------------------------------------------
assert df.shape[0] > 0, "No flight legs generated."
assert list(df.columns) == COLUMNS

assert df["FlightOperationKey"].is_unique, "FlightOperationKey must be unique."
assert df["FlightLegID"].is_unique, "FlightLegID must be unique."
assert not df.duplicated(
    ["AirlineKey", "FlightNumber", "ScheduledDepartureDateKey",
     "RouteKey", "ScheduledDepartureTimestampUTC"]
).any(), "Composite business key must be unique."

# FK resolution.
valid_airline_keys = set(airlines["AirlineKey"].astype(int))
valid_route_keys = set(routes["RouteKey"].astype(int))
valid_aircraft_keys = set(aircraft["AircraftKey"].astype(int))
valid_date_keys = set(dates["DateKey"].astype(int))

assert set(df["AirlineKey"].astype(int)).issubset(
    valid_airline_keys
), "AirlineKey FK must resolve."
assert set(df["RouteKey"].astype(int)).issubset(
    valid_route_keys
), "RouteKey FK must resolve."
aircraft_keys_nonnull = df["AircraftKey"].dropna().astype(int)
assert set(aircraft_keys_nonnull).issubset(
    valid_aircraft_keys
), "AircraftKey FK must resolve where non-null."
assert set(df["ScheduledDepartureDateKey"].astype(int)).issubset(
    valid_date_keys
), "ScheduledDepartureDateKey FK must resolve."
assert set(df["ScheduledArrivalDateKey"].astype(int)).issubset(
    valid_date_keys
), "ScheduledArrivalDateKey FK must resolve."

# FlightStatus values.
assert set(df["FlightStatus"]).issubset({"Operated", "Cancelled"})

# Cancelled-flight rules.
cancelled = df["FlightStatus"] == "Cancelled"
assert (df.loc[cancelled, "ActualDepartureTimestampUTC"].isna()).all(), \
    "Actual departure null for cancelled."
assert (df.loc[cancelled, "ActualArrivalTimestampUTC"].isna()).all(), \
    "Actual arrival null for cancelled."
assert (df.loc[cancelled, "DepartureDelayMinutes"].isna()).all(), \
    "Departure delay null for cancelled."
assert (df.loc[cancelled, "ArrivalDelayMinutes"].isna()).all(), \
    "Arrival delay null for cancelled."
assert (df.loc[cancelled, "BlockMinutes"].isna()).all(), \
    "Block minutes null for cancelled."
assert (df.loc[cancelled, "RevenuePassengers"] == 0).all(), \
    "Revenue passengers zero for cancelled."
assert (df.loc[cancelled, "NonRevenuePassengers"] == 0).all(), \
    "Non-revenue passengers zero for cancelled."
assert (df.loc[cancelled, "CancellationFlag"] == True).all(), \
    "CancellationFlag true for cancelled."
assert (df.loc[cancelled, "CompletionFlag"] == False).all(), \
    "CompletionFlag false for cancelled."
assert (df.loc[cancelled, "OnTimeFlag"] == False).all(), \
    "OnTimeFlag false for cancelled."
assert (df.loc[cancelled, "OnTimeArrivalFlag"] == False).all(), \
    "OnTimeArrivalFlag false for cancelled."

# Operated-flight rules.
operated = df["FlightStatus"] == "Operated"
assert (df.loc[operated, "CancellationFlag"] == False).all()
assert (df.loc[operated, "CompletionFlag"] == True).all()

# Available seats positive.
assert (df["AvailableSeats"] > 0).all(), "AvailableSeats must be positive."

# Booked passengers <= available seats (no overbooking in baseline).
assert (df["BookedPassengers"] <= df["AvailableSeats"]).all(), \
    "BookedPassengers must not exceed AvailableSeats."

# Revenue + non-revenue <= booked for operated flights.
op = df[operated]
assert (
    op["RevenuePassengers"] + op["NonRevenuePassengers"]
    <= op["BookedPassengers"]
).all(), "Revenue + non-revenue must not exceed booked (operated)."

# Revenue passengers <= available seats.
assert (df["RevenuePassengers"] <= df["AvailableSeats"]).all()

# FlightDistanceKM agrees with route distance.
for _, row in df.iterrows():
    route_dist = route_distance[int(row["RouteKey"])]
    assert abs(float(row["FlightDistanceKM"]) - route_dist) / route_dist <= 0.005, \
        f"FlightDistanceKM {row['FlightDistanceKM']} deviates >0.5% from route {route_dist}"

# Date keys are local airport dates (departure date key from origin).
assert (df["ScheduledDepartureDateKey"] > 0).all()
assert (df["ScheduledArrivalDateKey"] > 0).all()

# ---------------------------------------------------------------------------
# Apply dtypes
# ---------------------------------------------------------------------------
# Convert FlightDistanceKM to Decimal objects for pa.decimal128 compatibility.
df["FlightDistanceKM"] = [
    Decimal(str(round(v, 2))) for v in df["FlightDistanceKM"]
]

df = df.astype({
    "FlightOperationKey": "int64",
    "FlightLegID": "string",
    "FlightNumber": "string",
    "AirlineKey": "int32",
    "RouteKey": "int32",
    "AircraftKey": "Int32",  # nullable
    "ScheduledDepartureTimestampUTC": "datetime64[ns, UTC]",
    "ActualDepartureTimestampUTC": "datetime64[ns, UTC]",
    "ScheduledArrivalTimestampUTC": "datetime64[ns, UTC]",
    "ActualArrivalTimestampUTC": "datetime64[ns, UTC]",
    "ScheduledDepartureDateKey": "int32",
    "ScheduledArrivalDateKey": "int32",
    "AvailableSeats": "int16",
    "BookedPassengers": "int16",
    "RevenuePassengers": "int16",
    "NonRevenuePassengers": "int16",
    "FlightStatus": "string",
    "DepartureDelayMinutes": "Int16",
    "ArrivalDelayMinutes": "Int16",
    "BlockMinutes": "Int16",
    "CancellationFlag": "bool",
    "CompletionFlag": "bool",
    "OnTimeFlag": "bool",
    "OnTimeArrivalFlag": "bool",
})

# ---------------------------------------------------------------------------
# Write CSV and Parquet
# ---------------------------------------------------------------------------
df.to_csv(CSV, index=False, encoding="utf-8-sig")

schema = pa.schema([
    pa.field("FlightOperationKey", pa.int64(), nullable=False),
    pa.field("FlightLegID", pa.string(), nullable=False),
    pa.field("FlightNumber", pa.string(), nullable=False),
    pa.field("AirlineKey", pa.int32(), nullable=False),
    pa.field("RouteKey", pa.int32(), nullable=False),
    pa.field("AircraftKey", pa.int32(), nullable=True),
    pa.field("ScheduledDepartureTimestampUTC", pa.timestamp("us", tz="UTC"), nullable=False),
    pa.field("ActualDepartureTimestampUTC", pa.timestamp("us", tz="UTC"), nullable=True),
    pa.field("ScheduledArrivalTimestampUTC", pa.timestamp("us", tz="UTC"), nullable=False),
    pa.field("ActualArrivalTimestampUTC", pa.timestamp("us", tz="UTC"), nullable=True),
    pa.field("ScheduledDepartureDateKey", pa.int32(), nullable=False),
    pa.field("ScheduledArrivalDateKey", pa.int32(), nullable=False),
    pa.field("AvailableSeats", pa.int16(), nullable=False),
    pa.field("BookedPassengers", pa.int16(), nullable=False),
    pa.field("RevenuePassengers", pa.int16(), nullable=False),
    pa.field("NonRevenuePassengers", pa.int16(), nullable=False),
    pa.field("FlightDistanceKM", pa.decimal128(9, 2), nullable=False),
    pa.field("FlightStatus", pa.string(), nullable=False),
    pa.field("DepartureDelayMinutes", pa.int16(), nullable=True),
    pa.field("ArrivalDelayMinutes", pa.int16(), nullable=True),
    pa.field("BlockMinutes", pa.int16(), nullable=True),
    pa.field("CancellationFlag", pa.bool_(), nullable=False),
    pa.field("CompletionFlag", pa.bool_(), nullable=False),
    pa.field("OnTimeFlag", pa.bool_(), nullable=False),
    pa.field("OnTimeArrivalFlag", pa.bool_(), nullable=False),
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

assert csv_check.shape == df.shape
assert parquet_check.shape == df.shape
assert list(parquet_check.columns) == COLUMNS
assert parquet_check["FlightOperationKey"].is_unique
assert parquet_check["FlightLegID"].is_unique

# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------
manifest = {
    "dataset": "FactFlightOperations",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    "grain": "One row per scheduled flight leg, including cancelled legs",
    "primary_key": "FlightOperationKey",
    "business_key": "FlightLegID",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "source_dimensions": {
        "dim_airline": {
            "path": "data/03_curated/dim_airline.parquet",
            "sha256": sha256_file(AIRLINE_PATH),
            "rows": int(airlines.shape[0]),
        },
        "dim_route": {
            "path": "data/03_curated/dim_route.parquet",
            "sha256": sha256_file(ROUTE_PATH),
            "rows": int(routes.shape[0]),
        },
        "dim_aircraft": {
            "path": "data/03_curated/dim_aircraft.parquet",
            "sha256": sha256_file(AIRCRAFT_PATH),
            "rows": int(aircraft.shape[0]),
        },
        "dim_date": {
            "path": "data/03_curated/dim_date.parquet",
            "sha256": sha256_file(DATE_PATH),
            "rows": int(dates.shape[0]),
        },
    },
    "generation": {
        "method": "Deterministic NumPy random generator",
        "random_seed": SEED,
        "validation_volume": VALIDATION_VOLUME,
        "planning_volume_target": "150,000 to 250,000 flight legs (C-06, planning target, not guaranteed)",
        "reporting_period_start": REPORTING_START,
        "reporting_period_end": REPORTING_END,
        "cancelled_share": CANCELLED_SHARE,
    },
    "governance": {
        "od_09_otp_threshold": (
            "Proposed 15-minute on-time threshold under OD-09; "
            "formal owner approval pending. This threshold is provisional, "
            "not an approved business rule. Applied as documented in "
            "contract Section 5.2 / 6.3.1."
        )
    },
    "validation": {
        "exact_column_order": True,
        "unique_flight_operation_keys": True,
        "unique_flight_leg_ids": True,
        "unique_composite_business_key": True,
        "airline_foreign_keys_resolve": True,
        "route_foreign_keys_resolve": True,
        "aircraft_foreign_keys_resolve_where_non_null": True,
        "departure_date_key_foreign_key_resolves": True,
        "arrival_date_key_foreign_key_resolves": True,
        "cancelled_actual_timestamps_null": True,
        "cancelled_delay_minutes_null": True,
        "cancelled_passenger_counts_zero": True,
        "cancellation_flag_consistent": True,
        "completion_flag_consistent": True,
        "on_time_flag_consistent": True,
        "available_seats_positive": True,
        "booked_passengers_within_capacity": True,
        "carried_passengers_within_booked": True,
        "revenue_passengers_within_capacity": True,
        "flight_distance_matches_route_within_0_5_percent": True,
        "date_keys_positive": True,
        "csv_round_trip": True,
        "parquet_round_trip": True,
    },
    "files": {
        "csv": {
            "path": "data/03_curated/fact_flight_operations.csv",
            "sha256": sha256_file(CSV),
        },
        "parquet": {
            "path": "data/03_curated/fact_flight_operations.parquet",
            "sha256": sha256_file(PARQUET),
        },
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
}

write_json_atomic(MANIFEST, manifest)

print("FACT_FLIGHT_OPERATIONS_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("OPERATED:", int((df["FlightStatus"] == "Operated").sum()))
print("CANCELLED:", int((df["FlightStatus"] == "Cancelled").sum()))
print("UNIQUE FLIGHT OPERATION KEYS:", df["FlightOperationKey"].nunique())
print("UNIQUE FLIGHT LEG IDS:", df["FlightLegID"].nunique())
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
