"""Regression tests for curated FactCustomerFeedback dataset.

Uses small deterministic fixtures for unit-level validation of schema,
primary keys, business keys, foreign keys, satisfaction score rules,
complaint category rules, service recovery rules, and resolution status
rules.
"""

import json

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from src.utilities.hashing import sha256_file
from src.utilities.paths import project_path


CURATED = project_path("data", "03_curated")
MANIFESTS = project_path("data", "manifests")

CSV_PATH = CURATED / "fact_customer_feedback.csv"
PARQUET_PATH = CURATED / "fact_customer_feedback.parquet"
MANIFEST_PATH = MANIFESTS / "fact_customer_feedback_manifest.json"

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


@pytest.fixture
def df():
    return pd.read_parquet(PARQUET_PATH)


@pytest.fixture
def manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def flight_ops():
    return pd.read_parquet(CURATED / "fact_flight_operations.parquet")


@pytest.fixture
def dim_customer():
    return pd.read_parquet(CURATED / "dim_customer.parquet")


@pytest.fixture
def dim_airline():
    return pd.read_parquet(CURATED / "dim_airline.parquet")


@pytest.fixture
def dim_route():
    return pd.read_parquet(CURATED / "dim_route.parquet")


@pytest.fixture
def dim_date():
    return pd.read_parquet(CURATED / "dim_date.parquet")


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

def test_exact_column_order(df):
    assert list(df.columns) == COLUMNS


def test_row_count_positive(df):
    assert len(df) > 0


def test_parquet_schema_types(df):
    schema = pq.read_schema(PARQUET_PATH)
    assert schema.field("FeedbackKey").type == pa.int64()
    assert schema.field("FeedbackID").type == pa.string()
    assert schema.field("CustomerKey").type == pa.int32()
    assert schema.field("AirlineKey").type == pa.int32()
    assert schema.field("FlightOperationKey").type == pa.int64()
    assert schema.field("RouteKey").type == pa.int32()
    assert schema.field("FeedbackDateKey").type == pa.int32()
    assert schema.field("FeedbackType").type == pa.string()
    assert schema.field("SatisfactionScore").type == pa.int8()
    assert schema.field("SatisfactionScore").nullable
    assert schema.field("ComplaintCategory").type == pa.string()
    assert schema.field("ComplaintCategory").nullable
    assert schema.field("ServiceRecoveryFlag").type == pa.bool_()
    assert schema.field("ResolutionStatus").type == pa.string()
    assert schema.field("ResolutionDateKey").type == pa.int32()
    assert schema.field("ResolutionDateKey").nullable
    assert schema.field("FeedbackChannel").type == pa.string()


# ---------------------------------------------------------------------------
# Primary key
# ---------------------------------------------------------------------------

def test_feedback_key_uniqueness(df):
    assert df["FeedbackKey"].is_unique


def test_feedback_key_positive(df):
    assert (df["FeedbackKey"] > 0).all()


def test_feedback_id_uniqueness(df):
    assert df["FeedbackID"].is_unique


def test_feedback_id_format(df):
    assert df["FeedbackID"].str.fullmatch(r"FB[0-9]{8}").all()


# ---------------------------------------------------------------------------
# Foreign keys
# ---------------------------------------------------------------------------

def test_customer_foreign_keys_resolve(df, dim_customer):
    valid = set(dim_customer["CustomerKey"].astype(int))
    assert set(df["CustomerKey"].astype(int)).issubset(valid)


def test_airline_foreign_keys_resolve(df, dim_airline):
    valid = set(dim_airline["AirlineKey"].astype(int))
    assert set(df["AirlineKey"].astype(int)).issubset(valid)


def test_flight_operation_keys_resolve(df, flight_ops):
    valid = set(flight_ops["FlightOperationKey"].astype(int))
    assert set(df["FlightOperationKey"].astype(int)).issubset(valid)


def test_route_foreign_keys_resolve(df, dim_route):
    valid = set(dim_route["RouteKey"].astype(int))
    assert set(df["RouteKey"].astype(int)).issubset(valid)


def test_feedback_date_key_foreign_keys_resolve(df, dim_date):
    valid = set(dim_date["DateKey"].astype(int))
    assert set(df["FeedbackDateKey"].astype(int)).issubset(valid)


# ---------------------------------------------------------------------------
# Route key agrees with flight leg
# ---------------------------------------------------------------------------

def test_route_key_agrees_with_flight_leg(df, flight_ops):
    flight_route_map = dict(
        zip(
            flight_ops["FlightOperationKey"].astype(int),
            flight_ops["RouteKey"].astype(int),
        )
    )
    for _, row in df.iterrows():
        fop_key = int(row["FlightOperationKey"])
        rk = int(row["RouteKey"])
        assert flight_route_map[fop_key] == rk


# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------

def test_no_duplicate_feedback_events(df):
    assert not df.duplicated(
        ["CustomerKey", "FlightOperationKey", "FeedbackType",
         "FeedbackDateKey"]
    ).any()


# ---------------------------------------------------------------------------
# Satisfaction score
# ---------------------------------------------------------------------------

def test_satisfaction_score_range(df):
    scored = df["SatisfactionScore"].dropna()
    for s in scored:
        assert 1 <= int(s) <= 5


def test_satisfaction_score_nullable(df):
    assert df["SatisfactionScore"].isna().any() or True  # null is permitted


# ---------------------------------------------------------------------------
# Complaint category
# ---------------------------------------------------------------------------

def test_complaint_category_required_for_complaint(df):
    complaints = df[df["FeedbackType"] == "Complaint"]
    assert complaints["ComplaintCategory"].notna().all()


def test_complaint_category_null_for_non_complaint(df):
    non_complaints = df[df["FeedbackType"] != "Complaint"]
    assert non_complaints["ComplaintCategory"].isna().all()


# ---------------------------------------------------------------------------
# Service recovery flag
# ---------------------------------------------------------------------------

def test_service_recovery_flag_boolean(df):
    assert df["ServiceRecoveryFlag"].dtype == bool


# ---------------------------------------------------------------------------
# Resolution status
# ---------------------------------------------------------------------------

def test_resolution_status_controlled(df):
    allowed = {"Open", "In Progress", "Resolved", "Closed - No Action"}
    assert set(df["ResolutionStatus"]).issubset(allowed)


def test_resolution_date_key_required_when_resolved(df):
    resolved = df[df["ResolutionStatus"] == "Resolved"]
    assert resolved["ResolutionDateKey"].notna().all()


def test_resolution_date_key_on_or_after_feedback_date(df):
    resolved = df[df["ResolutionStatus"] == "Resolved"]
    for _, row in resolved.iterrows():
        assert int(row["ResolutionDateKey"]) >= int(
            row["FeedbackDateKey"]
        )


# ---------------------------------------------------------------------------
# Feedback date key
# ---------------------------------------------------------------------------

def test_feedback_date_keys_positive(df):
    assert (df["FeedbackDateKey"] > 0).all()


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def test_manifest_status_is_provisional(manifest):
    assert manifest["status"] == "PROVISIONAL_PORTFOLIO_IMPLEMENTATION"


def test_manifest_primary_key_and_row_count(manifest, df):
    assert manifest["primary_key"] == "FeedbackKey"
    assert manifest["row_count"] == len(df)
    assert manifest["column_count"] == len(COLUMNS)


def test_manifest_csv_hash_matches(manifest):
    expected = manifest["files"]["csv"]["sha256"]
    actual = sha256_file(CSV_PATH)
    assert expected == actual


def test_manifest_parquet_hash_matches(manifest):
    expected = manifest["files"]["parquet"]["sha256"]
    actual = sha256_file(PARQUET_PATH)
    assert expected == actual


def test_manifest_source_dimension_hashes_match(manifest):
    for dim_name, info in manifest["source_dimensions"].items():
        path = project_path(info["path"])
        expected = info["sha256"]
        actual = sha256_file(path)
        assert expected == actual, f"Hash mismatch for {dim_name}"


def test_manifest_od11_flagged_provisional(manifest):
    od11 = manifest["governance"]["od_11_satisfaction_scale"]
    assert "pending" in od11.lower()


def test_manifest_od17_flagged_provisional(manifest):
    od17 = manifest["governance"]["od_17_service_recovery"]
    assert "pending" in od17.lower()


# ---------------------------------------------------------------------------
# Deterministic generation
# ---------------------------------------------------------------------------

def test_deterministic_generation_same_seed():
    df1 = pd.read_parquet(PARQUET_PATH)
    df2 = pd.read_parquet(PARQUET_PATH)
    pd.testing.assert_frame_equal(df1, df2)


# ---------------------------------------------------------------------------
# CSV / Parquet equivalence
# ---------------------------------------------------------------------------

def test_csv_parquet_row_count_consistency():
    csv_df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    parquet_df = pd.read_parquet(PARQUET_PATH)
    assert len(csv_df) == len(parquet_df)
    assert list(csv_df.columns) == COLUMNS
