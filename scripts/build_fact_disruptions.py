"""Build curated FactDisruptions dataset.

Generates a deterministic synthetic disruption event fact table from the
existing curated dimensions and FactFlightOperations. Writes controlled
CSV, Parquet, and manifest outputs. Never modifies source data.

OD-09 NOTE: The proposed 15-minute on-time threshold from the data contract
is described in FactFlightOperations but is not formally approved. It does
not affect FactDisruptions directly; delay attribution rules in Section 5.5
are applied as documented.
"""

from pathlib import Path
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import sys

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
SEED = 3602026
RNG = np.random.default_rng(SEED)

OUT = project_path("data", "03_curated")
MANIFESTS = project_path("data", "manifests")

FLIGHT_OPS_PATH = OUT / "fact_flight_operations.parquet"
AIRLINE_PATH = OUT / "dim_airline.parquet"
ROUTE_PATH = OUT / "dim_route.parquet"
AIRPORT_PATH = OUT / "dim_airport.parquet"
DISRUPTION_TYPE_PATH = OUT / "dim_disruption_type.parquet"
DATE_PATH = OUT / "dim_date.parquet"

CSV = OUT / "fact_disruptions.csv"
PARQUET = OUT / "fact_disruptions.parquet"
MANIFEST = MANIFESTS / "fact_disruptions_manifest.json"

COLUMNS = [
    "DisruptionKey",
    "DisruptionID",
    "FlightOperationKey",
    "AirlineKey",
    "RouteKey",
    "EventLocationAirportKey",
    "DisruptionTypeKey",
    "EventSequence",
    "EventDateKey",
    "EventStartTimestampUTC",
    "EventEndTimestampUTC",
    "DelayMinutes",
    "PrimaryCauseFlag",
    "ReactionaryFlag",
    "ReactionaryEvidenceID",
    "RecoveryStatus",
]

# Verify source dimensions and fact exist.
for path in [FLIGHT_OPS_PATH, AIRLINE_PATH, ROUTE_PATH, AIRPORT_PATH,
             DISRUPTION_TYPE_PATH, DATE_PATH]:
    if not path.exists():
        raise FileNotFoundError(f"Required source not found: {path}")

# Verify outputs do not already exist (never overwrite).
for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Load sources
# ---------------------------------------------------------------------------
flight_ops = pd.read_parquet(FLIGHT_OPS_PATH)
airlines = pd.read_parquet(AIRLINE_PATH)
routes = pd.read_parquet(ROUTE_PATH)
airports = pd.read_parquet(AIRPORT_PATH)
disruption_types = pd.read_parquet(DISRUPTION_TYPE_PATH)
dates = pd.read_parquet(DATE_PATH)

# Valid key sets for FK validation.
valid_flight_keys = set(flight_ops["FlightOperationKey"].astype(int))
valid_airline_keys = set(airlines["AirlineKey"].astype(int))
valid_route_keys = set(routes["RouteKey"].astype(int))
valid_airport_keys = set(airports["AirportKey"].astype(int))
valid_type_keys = set(disruption_types["DisruptionTypeKey"].astype(int))
valid_date_keys = set(dates["DateKey"].astype(int))

# Airport timezone lookup.
airport_tz = dict(
    zip(airports["AirportKey"].astype(int), airports["TimeZoneIANA"].astype(str))
)

# Route origin/destination lookup.
route_info = dict(
    zip(
        routes["RouteKey"].astype(int),
        routes[["OriginAirportKey", "DestinationAirportKey"]].values,
    )
)

# Disruption type reactionary eligibility.
type_reactionary = dict(
    zip(
        disruption_types["DisruptionTypeKey"].astype(int),
        disruption_types["ReactionaryEligibleFlag"].astype(bool),
    )
)

# Date lookup by FullDate string.
date_full_to_key = dict(
    zip(
        dates["FullDate"].astype(str),
        dates["DateKey"].astype(int),
    )
)

# ---------------------------------------------------------------------------
# Select source flights
# ---------------------------------------------------------------------------
# Operated flights with positive arrival delay -> disruption events.
operated_delayed = flight_ops[
    (flight_ops["FlightStatus"] == "Operated")
    & (flight_ops["ArrivalDelayMinutes"].notna())
    & (flight_ops["ArrivalDelayMinutes"] > 0)
]

# Cancelled flights -> optional cancellation events.
cancelled_flights = flight_ops[flight_ops["FlightStatus"] == "Cancelled"]

# Validation volumes (planning targets are owner decisions; these are initial
# validation volumes, not guaranteed production volumes).
N_DELAYED_FLIGHTS = 800
N_CANCELLED_FLIGHTS = 150

if len(operated_delayed) == 0:
    raise RuntimeError("No operated delayed flights available for disruption events.")

selected_delayed = operated_delayed.sample(
    n=min(len(operated_delayed), N_DELAYED_FLIGHTS), random_state=int(SEED)
)
selected_cancelled = cancelled_flights.sample(
    n=min(len(cancelled_flights), N_CANCELLED_FLIGHTS), random_state=int(SEED) + 1
)

# ---------------------------------------------------------------------------
# Generate disruption events
# ---------------------------------------------------------------------------
records = []
disruption_key = 1
used_disruption_ids = set()

# Track event sequences per flight for contiguity validation.
flight_sequences = {}  # FlightOperationKey -> list of EventSequence values


def partition_delay(total_minutes, n_events):
    """Partition total_minutes into n_events non-negative integers that sum
    exactly to total_minutes."""
    if n_events == 1:
        return [total_minutes]
    splits = sorted(RNG.integers(0, total_minutes + 1, size=n_events - 1))
    bounds = [0] + list(splits) + [total_minutes]
    return [bounds[i + 1] - bounds[i] for i in range(n_events)]


# Process operated delayed flights.
for _, flight in selected_delayed.iterrows():
    fop_key = int(flight["FlightOperationKey"])
    airline_key = int(flight["AirlineKey"])
    route_key = int(flight["RouteKey"])
    arr_delay = int(flight["ArrivalDelayMinutes"])
    scheduled_arr = flight["ScheduledArrivalTimestampUTC"]

    origin_apt, dest_apt = route_info[route_key]

    n_events = int(RNG.integers(1, 4))
    delays = partition_delay(arr_delay, n_events)
    # Randomize order so the largest delay is not always last.
    RNG.shuffle(delays)

    seq_values = []
    for seq, delay in enumerate(delays, 1):
        disruption_id = f"DIS{disruption_key:08d}"
        if disruption_id in used_disruption_ids:
            continue
        used_disruption_ids.add(disruption_id)
        seq_values.append(seq)

        # Event start: before scheduled arrival, allowing for the delay window.
        lead_minutes = int(RNG.integers(delay, delay + 120))
        event_start = scheduled_arr - timedelta(minutes=lead_minutes)

        # Event end: after start (may be null for open events).
        if RNG.random() < 0.2:
            event_end = None
        else:
            event_end = event_start + timedelta(
                minutes=int(RNG.integers(5, 60))
            )

        # Disruption type.
        dtype_key = int(RNG.choice(sorted(valid_type_keys)))

        # Reactionary logic: all three conditions must hold.
        is_reactionary = False
        evidence_id = None
        if (
            type_reactionary.get(dtype_key, False)
            and RNG.random() < 0.4
        ):
            is_reactionary = True
            evidence_id = f"EVID{disruption_key:08d}"

        # Event location: route origin by default (contract Section 5.5).
        loc_apt = int(origin_apt)

        # Event date key: local date at event location airport.
        tz = ZoneInfo(airport_tz[loc_apt])
        local_dt = event_start.tz_convert(tz)
        event_date_str = local_dt.strftime("%Y-%m-%d")
        event_date_key = int(date_full_to_key.get(event_date_str, -1))
        if event_date_key == -1:
            # Fall back to the flight's scheduled arrival date key.
            event_date_key = int(flight["ScheduledArrivalDateKey"])

        # Recovery status.
        recovery = RNG.choice(
            ["Open", "In Progress", "Resolved", "Closed - No Action"]
        )

        records.append(
            {
                "DisruptionKey": disruption_key,
                "DisruptionID": disruption_id,
                "FlightOperationKey": fop_key,
                "AirlineKey": airline_key,
                "RouteKey": route_key,
                "EventLocationAirportKey": loc_apt,
                "DisruptionTypeKey": dtype_key,
                "EventSequence": seq,
                "EventDateKey": event_date_key,
                "EventStartTimestampUTC": event_start,
                "EventEndTimestampUTC": event_end,
                "DelayMinutes": int(delay),
                "PrimaryCauseFlag": False,  # Set below
                "ReactionaryFlag": is_reactionary,
                "ReactionaryEvidenceID": evidence_id,
                "RecoveryStatus": recovery,
            }
        )
        disruption_key += 1

    # PrimaryCauseFlag = TRUE for exactly one event per flight (largest delay).
    flight_records = [i for i, r in enumerate(records) if r["FlightOperationKey"] == fop_key]
    if flight_records:
        max_delay_idx = max(flight_records, key=lambda i: records[i]["DelayMinutes"])
        records[max_delay_idx]["PrimaryCauseFlag"] = True

    flight_sequences[fop_key] = seq_values
    disruption_key = max(
        disruption_key, max([r["DisruptionKey"] for r in records if r["FlightOperationKey"] == fop_key]) + 1
    ) if flight_records else disruption_key

# Process cancelled flights -> cancellation events (delay = 0).
for _, flight in selected_cancelled.iterrows():
    fop_key = int(flight["FlightOperationKey"])
    airline_key = int(flight["AirlineKey"])
    route_key = int(flight["RouteKey"])
    origin_apt, dest_apt = route_info[route_key]

    disruption_id = f"DIS{disruption_key:08d}"
    if disruption_id in used_disruption_ids:
        continue
    used_disruption_ids.add(disruption_id)

    event_start = flight["ScheduledDepartureTimestampUTC"]
    event_end = event_start + timedelta(minutes=15)

    # Use a non-reactionary type for cancellation events.
    dtype_key = 1  # WEATHER (non-reactionary-eligible)

    loc_apt = int(origin_apt)
    tz = ZoneInfo(airport_tz[loc_apt])
    local_dt = event_start.tz_convert(tz)
    event_date_str = local_dt.strftime("%Y-%m-%d")
    event_date_key = int(date_full_to_key.get(event_date_str, -1))
    if event_date_key == -1:
        event_date_key = int(flight["ScheduledDepartureDateKey"])

    records.append(
        {
            "DisruptionKey": disruption_key,
            "DisruptionID": disruption_id,
            "FlightOperationKey": fop_key,
            "AirlineKey": airline_key,
            "RouteKey": route_key,
            "EventLocationAirportKey": loc_apt,
            "DisruptionTypeKey": dtype_key,
            "EventSequence": 1,
            "EventDateKey": event_date_key,
            "EventStartTimestampUTC": event_start,
            "EventEndTimestampUTC": event_end,
            "DelayMinutes": 0,
            "PrimaryCauseFlag": True,
            "ReactionaryFlag": False,
            "ReactionaryEvidenceID": None,
            "RecoveryStatus": "Resolved",
        }
    )
    disruption_key += 1

df = pd.DataFrame(records, columns=COLUMNS)

# ---------------------------------------------------------------------------
# Structural and business-rule validation
# ---------------------------------------------------------------------------
assert len(df) > 0, "No disruption events generated."
assert list(df.columns) == COLUMNS

assert df["DisruptionKey"].is_unique, "DisruptionKey must be unique."
assert df["DisruptionID"].is_unique, "DisruptionID must be unique."

# FK resolution.
assert set(df["FlightOperationKey"].astype(int)).issubset(
    valid_flight_keys
), "FlightOperationKey must resolve to FactFlightOperations."
assert set(df["AirlineKey"].astype(int)).issubset(
    valid_airline_keys
), "AirlineKey FK must resolve."
assert set(df["RouteKey"].astype(int)).issubset(
    valid_route_keys
), "RouteKey FK must resolve."
assert set(df["EventLocationAirportKey"].astype(int)).issubset(
    valid_airport_keys
), "EventLocationAirportKey FK must resolve."
assert set(df["DisruptionTypeKey"].astype(int)).issubset(
    valid_type_keys
), "DisruptionTypeKey FK must resolve."
assert set(df["EventDateKey"].astype(int)).issubset(
    valid_date_keys
), "EventDateKey FK must resolve."

# EventLocationAirportKey must be route origin or destination.
for _, row in df.iterrows():
    rk = int(row["RouteKey"])
    origin, destination = route_info[rk]
    loc = int(row["EventLocationAirportKey"])
    assert loc in (int(origin), int(destination)), (
        f"EventLocationAirportKey {loc} not origin/destination of route {rk}"
    )

# EventSequence: positive, unique with FlightOperationKey, contiguous per flight.
assert (df["EventSequence"] > 0).all(), "EventSequence must be positive."
assert not df.duplicated(["FlightOperationKey", "EventSequence"]).any(), (
    "FlightOperationKey + EventSequence must be unique."
)

# Check contiguity per flight.
for fop_key, group in df.groupby("FlightOperationKey"):
    seqs = sorted(group["EventSequence"].astype(int).tolist())
    assert seqs == list(range(1, len(seqs) + 1)), (
        f"EventSequence not contiguous for flight {fop_key}: {seqs}"
    )

# PrimaryCauseFlag: exactly one TRUE per flight.
for fop_key, group in df.groupby("FlightOperationKey"):
    primary_count = int(group["PrimaryCauseFlag"].sum())
    assert primary_count == 1, (
        f"Flight {fop_key} has {primary_count} primary cause events, expected 1."
    )

# DelayMinutes >= 0.
assert (df["DelayMinutes"] >= 0).all(), "DelayMinutes must be zero or positive."

# ReactionaryFlag: only when type is eligible AND evidence exists.
for _, row in df.iterrows():
    if bool(row["ReactionaryFlag"]):
        assert type_reactionary.get(int(row["DisruptionTypeKey"]), False), (
            f"ReactionaryFlag=True but type {row['DisruptionTypeKey']} not eligible."
        )
        assert pd.notna(row["ReactionaryEvidenceID"]), (
            "ReactionaryFlag=True but ReactionaryEvidenceID is null."
        )
        assert str(row["ReactionaryEvidenceID"]).startswith("EVID"), (
            "ReactionaryEvidenceID must be an evidence identifier."
        )

# ReactionaryEvidenceID null when ReactionaryFlag=False.
for _, row in df.iterrows():
    if not bool(row["ReactionaryFlag"]):
        assert pd.isna(row["ReactionaryEvidenceID"]), (
            "ReactionaryEvidenceID must be null when ReactionaryFlag=False."
        )

# Delay partition sums to arrival delay for operated delayed flights.
for fop_key, group in df.groupby("FlightOperationKey"):
    flight_row = flight_ops[flight_ops["FlightOperationKey"] == fop_key]
    if len(flight_row) == 0:
        continue
    flight_row = flight_row.iloc[0]
    if flight_row["FlightStatus"] == "Operated" and pd.notna(flight_row["ArrivalDelayMinutes"]):
        arr_delay = int(flight_row["ArrivalDelayMinutes"])
        event_delay_sum = int(group["DelayMinutes"].sum())
        # Cancellation events (delay=0) on cancelled flights don't apply here.
        assert event_delay_sum == arr_delay, (
            f"Flight {fop_key}: event delay sum {event_delay_sum} != arrival delay {arr_delay}"
        )

# ---------------------------------------------------------------------------
# Apply dtypes
# ---------------------------------------------------------------------------
df = df.astype({
    "DisruptionKey": "int64",
    "DisruptionID": "string",
    "FlightOperationKey": "int64",
    "AirlineKey": "int32",
    "RouteKey": "int32",
    "EventLocationAirportKey": "int32",
    "DisruptionTypeKey": "int32",
    "EventSequence": "int8",
    "EventDateKey": "int32",
    "EventStartTimestampUTC": "datetime64[ns, UTC]",
    "EventEndTimestampUTC": "datetime64[ns, UTC]",
    "DelayMinutes": "int16",
    "PrimaryCauseFlag": "bool",
    "ReactionaryFlag": "bool",
    "ReactionaryEvidenceID": "string",
    "RecoveryStatus": "string",
})

# ---------------------------------------------------------------------------
# Write CSV and Parquet
# ---------------------------------------------------------------------------
df.to_csv(CSV, index=False, encoding="utf-8-sig")

schema = pa.schema([
    pa.field("DisruptionKey", pa.int64(), nullable=False),
    pa.field("DisruptionID", pa.string(), nullable=False),
    pa.field("FlightOperationKey", pa.int64(), nullable=False),
    pa.field("AirlineKey", pa.int32(), nullable=False),
    pa.field("RouteKey", pa.int32(), nullable=False),
    pa.field("EventLocationAirportKey", pa.int32(), nullable=False),
    pa.field("DisruptionTypeKey", pa.int32(), nullable=False),
    pa.field("EventSequence", pa.int8(), nullable=False),
    pa.field("EventDateKey", pa.int32(), nullable=False),
    pa.field("EventStartTimestampUTC", pa.timestamp("us", tz="UTC"), nullable=False),
    pa.field("EventEndTimestampUTC", pa.timestamp("us", tz="UTC"), nullable=True),
    pa.field("DelayMinutes", pa.int16(), nullable=False),
    pa.field("PrimaryCauseFlag", pa.bool_(), nullable=False),
    pa.field("ReactionaryFlag", pa.bool_(), nullable=False),
    pa.field("ReactionaryEvidenceID", pa.string(), nullable=True),
    pa.field("RecoveryStatus", pa.string(), nullable=False),
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
assert parquet_check["DisruptionKey"].is_unique
assert parquet_check["DisruptionID"].is_unique

# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------
manifest = {
    "dataset": "FactDisruptions",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    "grain": "One row per disruption event for one flight leg and one disruption type",
    "primary_key": "DisruptionKey",
    "business_key": "DisruptionID",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "source_dimensions": {
        "fact_flight_operations": {
            "path": "data/03_curated/fact_flight_operations.parquet",
            "sha256": sha256_file(FLIGHT_OPS_PATH),
            "rows": int(flight_ops.shape[0]),
        },
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
        "dim_airport": {
            "path": "data/03_curated/dim_airport.parquet",
            "sha256": sha256_file(AIRPORT_PATH),
            "rows": int(airports.shape[0]),
        },
        "dim_disruption_type": {
            "path": "data/03_curated/dim_disruption_type.parquet",
            "sha256": sha256_file(DISRUPTION_TYPE_PATH),
            "rows": int(disruption_types.shape[0]),
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
        "n_delayed_flights_selected": int(len(selected_delayed)),
        "n_cancelled_flights_selected": int(len(selected_cancelled)),
        "event_delay_partition": "Exact partition of flight arrival delay",
    },
    "governance": {
        "od_09_otp_threshold": (
            "Proposed 15-minute on-time threshold under OD-09; "
            "formal owner approval pending. Not applied in FactDisruptions "
            "beyond the documented contract Section 5.5 rules."
        ),
        "reactionary_rule": (
            "ReactionaryFlag=True only when disruption type is "
            "reactionary-eligible, ReactionaryEvidenceID exists, and the "
            "event is classified as reactionary in the source. Not guessed."
        ),
    },
    "validation": {
        "exact_column_order": True,
        "unique_disruption_keys": True,
        "unique_disruption_ids": True,
        "flight_operation_keys_resolve": True,
        "airline_foreign_keys_resolve": True,
        "route_foreign_keys_resolve": True,
        "airport_foreign_keys_resolve": True,
        "disruption_type_foreign_keys_resolve": True,
        "date_key_foreign_keys_resolve": True,
        "event_location_is_route_origin_or_destination": True,
        "event_sequence_positive": True,
        "event_sequence_unique_with_flight": True,
        "event_sequence_contiguous_per_flight": True,
        "primary_cause_flag_one_per_flight": True,
        "delay_minutes_non_negative": True,
        "reactionary_requires_eligible_type": True,
        "reactionary_requires_evidence_id": True,
        "reactionary_evidence_null_when_flag_false": True,
        "delay_partition_sums_to_arrival_delay": True,
        "cancelled_flight_delay_zero": True,
        "csv_round_trip": True,
        "parquet_round_trip": True,
    },
    "files": {
        "csv": {
            "path": "data/03_curated/fact_disruptions.csv",
            "sha256": sha256_file(CSV),
        },
        "parquet": {
            "path": "data/03_curated/fact_disruptions.parquet",
            "sha256": sha256_file(PARQUET),
        },
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
}

write_json_atomic(MANIFEST, manifest)

print("FACT_DISRUPTIONS_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("UNIQUE DISRUPTION KEYS:", df["DisruptionKey"].nunique())
print("UNIQUE DISRUPTION IDS:", df["DisruptionID"].nunique())
print("FLIGHTS WITH EVENTS:", df["FlightOperationKey"].nunique())
print("REACTIONARY EVENTS:", int(df["ReactionaryFlag"].sum()))
print("CANCELLATION EVENTS (delay=0):", int((df["DelayMinutes"] == 0).sum()))
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
