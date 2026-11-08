"""Build curated FactCustomerFeedback dataset.

Generates a deterministic synthetic customer feedback event fact table from
the existing curated dimensions and FactFlightOperations. Writes controlled
CSV, Parquet, and manifest outputs. Never modifies source data.

OD-11 NOTE: The satisfaction score scale of 1 through 5 is described in the
data contract but remains pending formal owner approval (OD-11). This
implementation applies the scale as documented in contract Section 5.6 /
6.3.5 and flags it as provisional in the manifest. It does not claim the
scale is an approved business rule.
"""

from pathlib import Path
from datetime import datetime, timezone, timedelta
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
CUSTOMER_PATH = OUT / "dim_customer.parquet"
AIRLINE_PATH = OUT / "dim_airline.parquet"
ROUTE_PATH = OUT / "dim_route.parquet"
DATE_PATH = OUT / "dim_date.parquet"

CSV = OUT / "fact_customer_feedback.csv"
PARQUET = OUT / "fact_customer_feedback.parquet"
MANIFEST = MANIFESTS / "fact_customer_feedback_manifest.json"

COLUMNS = [
    "FeedbackKey",
    "FeedbackID",
    "CustomerKey",
    "AirlineKey",
    "FlightOperationKey",
    "RouteKey",
    "FeedbackDateKey",
    "FeedbackType",
    "SatisfactionScore",
    "ComplaintCategory",
    "ServiceRecoveryFlag",
    "ResolutionStatus",
    "ResolutionDateKey",
    "FeedbackChannel",
]

# Verify source dimensions and fact exist.
for path in [FLIGHT_OPS_PATH, CUSTOMER_PATH, AIRLINE_PATH, ROUTE_PATH,
             DATE_PATH]:
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
customers = pd.read_parquet(CUSTOMER_PATH)
airlines = pd.read_parquet(AIRLINE_PATH)
routes = pd.read_parquet(ROUTE_PATH)
dates = pd.read_parquet(DATE_PATH)

valid_flight_keys = set(flight_ops["FlightOperationKey"].astype(int))
valid_customer_keys = set(customers["CustomerKey"].astype(int))
valid_airline_keys = set(airlines["AirlineKey"].astype(int))
valid_route_keys = set(routes["RouteKey"].astype(int))
valid_date_keys = set(dates["DateKey"].astype(int))

# Flight leg date key mapping for route consistency check.
flight_route_map = dict(
    zip(
        flight_ops["FlightOperationKey"].astype(int),
        flight_ops["RouteKey"].astype(int),
    )
)

# Date key lookup.
date_keys = dates["DateKey"].astype(int).tolist()

# Reporting period bounds.
REPORTING_START = "2025-10-01"
REPORTING_END = "2026-09-30"

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------
COMPLAINT_CATEGORIES = [
    "Baggage",
    "Boarding",
    "Cancellation",
    "Customer Service",
    "Delay",
    "In-Flight Experience",
    "Seat",
    "Other",
]

FEEDBACK_CHANNELS = ["Web", "Mobile", "Email", "Call Center", "Airport", "Social"]

FEEDBACK_TYPES = ["Survey", "Complaint", "Compliment", "Claim"]

RESOLUTION_STATUSES = ["Open", "In Progress", "Resolved", "Closed - No Action"]

# Validation volumes (initial validation volumes, not guaranteed production
# volumes. Full portfolio volume requires confirmation against documented
# requirements.)
N_FEEDBACK_EVENTS = 2500

# Select source flights for feedback events.
feedback_flights = flight_ops.sample(
    n=min(len(flight_ops), N_FEEDBACK_EVENTS), random_state=int(SEED)
)

# ---------------------------------------------------------------------------
# Generate feedback events
# ---------------------------------------------------------------------------
records = []
feedback_key = 1
used_feedback_ids = set()

# Tracking for duplicate detection: customer + flight + type + timestamp.
seen_feedback_tuples = set()

for _, flight in feedback_flights.iterrows():
    fop_key = int(flight["FlightOperationKey"])
    airline_key = int(flight["AirlineKey"])
    route_key = int(flight["RouteKey"])
    dep_date_key = int(flight["ScheduledDepartureDateKey"])

    # Select a customer.
    customer_key = int(RNG.choice(customers["CustomerKey"].astype(int).tolist()))

    # Feedback type.
    feedback_type = str(RNG.choice(FEEDBACK_TYPES))

    # Satisfaction score: 1-5, null when type does not collect a score.
    satisfaction_score = None
    if feedback_type in ("Survey", "Complaint", "Claim"):
        satisfaction_score = int(RNG.integers(1, 6))

    # Complaint category: required for Complaint, null otherwise.
    complaint_category = None
    if feedback_type == "Complaint":
        complaint_category = str(RNG.choice(COMPLAINT_CATEGORIES))

    # Service recovery flag: TRUE only when service-recovery case triggered.
    service_recovery_flag = bool(RNG.random() < 0.15)

    # Resolution status.
    resolution_status = str(RNG.choice(RESOLUTION_STATUSES))

    # Resolution date key: required when Resolved, must be on or after
    # FeedbackDateKey.
    resolution_date_key = None
    if resolution_status == "Resolved":
        resolution_date_key = dep_date_key  # Simplified: resolution on dep date

    # Feedback date key: UTC calendar date of submission.
    feedback_date_key = dep_date_key

    # Feedback channel.
    feedback_channel = str(RNG.choice(FEEDBACK_CHANNELS))

    # Feedback ID: unique business key.
    feedback_id = f"FB{feedback_key:08d}"
    if feedback_id in used_feedback_ids:
        continue
    used_feedback_ids.add(feedback_id)

    # Duplicate detection: customer + flight + type + timestamp.
    feedback_tuple = (
        customer_key,
        fop_key,
        feedback_type,
        feedback_date_key,
    )
    if feedback_tuple in seen_feedback_tuples:
        continue
    seen_feedback_tuples.add(feedback_tuple)

    records.append(
        {
            "FeedbackKey": feedback_key,
            "FeedbackID": feedback_id,
            "CustomerKey": customer_key,
            "AirlineKey": airline_key,
            "FlightOperationKey": fop_key,
            "RouteKey": route_key,
            "FeedbackDateKey": feedback_date_key,
            "FeedbackType": feedback_type,
            "SatisfactionScore": satisfaction_score,
            "ComplaintCategory": complaint_category,
            "ServiceRecoveryFlag": service_recovery_flag,
            "ResolutionStatus": resolution_status,
            "ResolutionDateKey": resolution_date_key,
            "FeedbackChannel": feedback_channel,
        }
    )
    feedback_key += 1

df = pd.DataFrame(records, columns=COLUMNS)

# ---------------------------------------------------------------------------
# Structural and business-rule validation
# ---------------------------------------------------------------------------
assert len(df) > 0, "No feedback events generated."
assert list(df.columns) == COLUMNS

assert df["FeedbackKey"].is_unique, "FeedbackKey must be unique."
assert df["FeedbackID"].is_unique, "FeedbackID must be unique."

# FK resolution.
assert set(df["CustomerKey"].astype(int)).issubset(
    valid_customer_keys
), "CustomerKey FK must resolve."
assert set(df["AirlineKey"].astype(int)).issubset(
    valid_airline_keys
), "AirlineKey FK must resolve."
assert set(df["FlightOperationKey"].astype(int)).issubset(
    valid_flight_keys
), "FlightOperationKey FK must resolve to FactFlightOperations."
assert set(df["RouteKey"].astype(int)).issubset(
    valid_route_keys
), "RouteKey FK must resolve."
assert set(df["FeedbackDateKey"].astype(int)).issubset(
    valid_date_keys
), "FeedbackDateKey FK must resolve."

# RouteKey must agree with the flight leg.
for _, row in df.iterrows():
    fop_key = int(row["FlightOperationKey"])
    rk = int(row["RouteKey"])
    flight_rk = int(flight_ops[flight_ops["FlightOperationKey"] == fop_key][
        "RouteKey"
    ].iloc[0])
    assert rk == flight_rk, (
        f"RouteKey {rk} does not match flight leg {fop_key} route {flight_rk}"
    )

# Duplicate detection: no duplicate customer + flight + type + date tuples.
assert not df.duplicated(
    ["CustomerKey", "FlightOperationKey", "FeedbackType", "FeedbackDateKey"]
).any(), "Duplicate feedback events detected."

# SatisfactionScore: integer 1-5 or null.
scored = df["SatisfactionScore"].dropna()
assert all(1 <= s <= 5 for s in scored), "SatisfactionScore must be 1-5."

# ComplaintCategory: required for Complaint, null otherwise.
complaints = df[df["FeedbackType"] == "Complaint"]
assert complaints["ComplaintCategory"].notna().all(), (
    "ComplaintCategory required for Complaint type."
)
non_complaints = df[df["FeedbackType"] != "Complaint"]
assert non_complaints["ComplaintCategory"].isna().all(), (
    "ComplaintCategory must be null for non-Complaint types."
)

# ServiceRecoveryFlag: boolean.
assert df["ServiceRecoveryFlag"].dtype == bool

# ResolutionStatus: controlled set.
assert set(df["ResolutionStatus"]).issubset(set(RESOLUTION_STATUSES))

# ResolutionDateKey: required when Resolved, must be on or after FeedbackDateKey.
resolved = df[df["ResolutionStatus"] == "Resolved"]
assert resolved["ResolutionDateKey"].notna().all(), (
    "ResolutionDateKey required when Resolved."
)
for _, row in resolved.iterrows():
    assert int(row["ResolutionDateKey"]) >= int(
        row["FeedbackDateKey"]
    ), "ResolutionDateKey must be on or after FeedbackDateKey."

# Non-resolved: ResolutionDateKey may be null.
non_resolved = df[df["ResolutionStatus"] != "Resolved"]
# (null is permitted; no assertion required)

# FeedbackDateKey must be within DimDate coverage.
assert (df["FeedbackDateKey"] > 0).all()

# ---------------------------------------------------------------------------
# Apply dtypes
# ---------------------------------------------------------------------------
df = df.astype({
    "FeedbackKey": "int64",
    "FeedbackID": "string",
    "CustomerKey": "int32",
    "AirlineKey": "int32",
    "FlightOperationKey": "int64",
    "RouteKey": "int32",
    "FeedbackDateKey": "int32",
    "FeedbackType": "string",
    "SatisfactionScore": "Int8",  # nullable
    "ComplaintCategory": "string",
    "ServiceRecoveryFlag": "bool",
    "ResolutionStatus": "string",
    "ResolutionDateKey": "Int32",  # nullable
    "FeedbackChannel": "string",
})

# ---------------------------------------------------------------------------
# Write CSV and Parquet
# ---------------------------------------------------------------------------
df.to_csv(CSV, index=False, encoding="utf-8-sig")

schema = pa.schema([
    pa.field("FeedbackKey", pa.int64(), nullable=False),
    pa.field("FeedbackID", pa.string(), nullable=False),
    pa.field("CustomerKey", pa.int32(), nullable=False),
    pa.field("AirlineKey", pa.int32(), nullable=False),
    pa.field("FlightOperationKey", pa.int64(), nullable=False),
    pa.field("RouteKey", pa.int32(), nullable=False),
    pa.field("FeedbackDateKey", pa.int32(), nullable=False),
    pa.field("FeedbackType", pa.string(), nullable=False),
    pa.field("SatisfactionScore", pa.int8(), nullable=True),
    pa.field("ComplaintCategory", pa.string(), nullable=True),
    pa.field("ServiceRecoveryFlag", pa.bool_(), nullable=False),
    pa.field("ResolutionStatus", pa.string(), nullable=False),
    pa.field("ResolutionDateKey", pa.int32(), nullable=True),
    pa.field("FeedbackChannel", pa.string(), nullable=False),
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
assert parquet_check["FeedbackKey"].is_unique
assert parquet_check["FeedbackID"].is_unique

# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------
manifest = {
    "dataset": "FactCustomerFeedback",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    "grain": "One row per customer feedback event",
    "primary_key": "FeedbackKey",
    "business_key": "FeedbackID",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "source_dimensions": {
        "fact_flight_operations": {
            "path": "data/03_curated/fact_flight_operations.parquet",
            "sha256": sha256_file(FLIGHT_OPS_PATH),
            "rows": int(flight_ops.shape[0]),
        },
        "dim_customer": {
            "path": "data/03_curated/dim_customer.parquet",
            "sha256": sha256_file(CUSTOMER_PATH),
            "rows": int(customers.shape[0]),
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
        "dim_date": {
            "path": "data/03_curated/dim_date.parquet",
            "sha256": sha256_file(DATE_PATH),
            "rows": int(dates.shape[0]),
        },
    },
    "generation": {
        "method": "Deterministic NumPy random generator",
        "random_seed": SEED,
        "n_feedback_events": int(len(df)),
        "satisfaction_score_scale": "1-5 (OD-11, proposed, formal owner approval pending)",
        "feedback_types": ["Survey", "Complaint", "Compliment", "Claim"],
        "resolution_statuses": [
            "Open",
            "In Progress",
            "Resolved",
            "Closed - No Action",
        ],
    },
    "governance": {
        "od_11_satisfaction_scale": (
            "Proposed satisfaction score scale of 1 through 5 under OD-11; "
            "formal owner approval pending. Applied as documented in "
            "contract Section 5.6 / 6.3.5, not claimed as an approved rule."
        ),
        "od_17_service_recovery": (
            "Service-recovery case is a complaint with ServiceRecoveryFlag "
            "= TRUE; recovered means ResolutionStatus = Resolved. "
            "Proposed under OD-17, formal owner approval pending."
        ),
    },
    "validation": {
        "exact_column_order": True,
        "unique_feedback_keys": True,
        "unique_feedback_ids": True,
        "customer_foreign_keys_resolve": True,
        "airline_foreign_keys_resolve": True,
        "flight_operation_keys_resolve": True,
        "route_foreign_keys_resolve": True,
        "feedback_date_key_foreign_key_resolves": True,
        "route_key_agrees_with_flight_leg": True,
        "no_duplicate_feedback_events": True,
        "satisfaction_score_range_1_to_5": True,
        "complaint_category_required_for_complaint": True,
        "complaint_category_null_for_non_complaint": True,
        "resolution_date_key_required_when_resolved": True,
        "resolution_date_key_on_or_after_feedback_date": True,
        "service_recovery_flag_boolean": True,
        "csv_round_trip": True,
        "parquet_round_trip": True,
    },
    "files": {
        "csv": {
            "path": "data/03_curated/fact_customer_feedback.csv",
            "sha256": sha256_file(CSV),
        },
        "parquet": {
            "path": "data/03_curated/fact_customer_feedback.parquet",
            "sha256": sha256_file(PARQUET),
        },
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
}

write_json_atomic(MANIFEST, manifest)

print("FACT_CUSTOMER_FEEDBACK_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("UNIQUE FEEDBACK KEYS:", df["FeedbackKey"].nunique())
print("UNIQUE FEEDBACK IDS:", df["FeedbackID"].nunique())
print("FEEDBACK TYPES:", df["FeedbackType"].value_counts().to_dict())
print("RESOLUTION STATUSES:", df["ResolutionStatus"].value_counts().to_dict())
print("SERVICE RECOVERY EVENTS:", int(df["ServiceRecoveryFlag"].sum()))
print("SCORED EVENTS:", int(df["SatisfactionScore"].notna().sum()))
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
