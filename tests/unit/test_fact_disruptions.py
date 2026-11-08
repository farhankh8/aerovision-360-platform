"""Regression tests for curated FactDisruptions dataset.

Uses small deterministic fixtures for unit-level validation of schema,
primary keys, business keys, foreign keys, event sequences, and reactionary
classification rules.
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

CSV_PATH = CURATED / "fact_disruptions.csv"
PARQUET_PATH = CURATED / "fact_disruptions.parquet"
MANIFEST_PATH = MANIFESTS / "fact_disruptions_manifest.json"

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
def dim_airline():
    return pd.read_parquet(CURATED / "dim_airline.parquet")


@pytest.fixture
def dim_route():
    return pd.read_parquet(CURATED / "dim_route.parquet")


@pytest.fixture
def dim_airport():
    return pd.read_parquet(CURATED / "dim_airport.parquet")


@pytest.fixture
def dim_disruption_type():
    return pd.read_parquet(CURATED / "dim_disruption_type.parquet")


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
    assert schema.field("DisruptionKey").type == pa.int64()
    assert schema.field("DisruptionID").type == pa.string()
    assert schema.field("FlightOperationKey").type == pa.int64()
    assert schema.field("AirlineKey").type == pa.int32()
    assert schema.field("RouteKey").type == pa.int32()
    assert schema.field("EventLocationAirportKey").type == pa.int32()
    assert schema.field("DisruptionTypeKey").type == pa.int32()
    assert schema.field("EventSequence").type == pa.int8()
    assert schema.field("EventDateKey").type == pa.int32()
    assert schema.field("EventStartTimestampUTC").type == pa.timestamp("us", tz="UTC")
    assert schema.field("EventEndTimestampUTC").type == pa.timestamp("us", tz="UTC")
    assert schema.field("EventEndTimestampUTC").nullable
    assert schema.field("DelayMinutes").type == pa.int16()
    assert schema.field("PrimaryCauseFlag").type == pa.bool_()
    assert schema.field("ReactionaryFlag").type == pa.bool_()
    assert schema.field("ReactionaryEvidenceID").type == pa.string()
    assert schema.field("ReactionaryEvidenceID").nullable
    assert schema.field("RecoveryStatus").type == pa.string()


# ---------------------------------------------------------------------------
# Primary key
# ---------------------------------------------------------------------------

def test_disruption_key_uniqueness(df):
    assert df["DisruptionKey"].is_unique


def test_disruption_key_positive(df):
    assert (df["DisruptionKey"] > 0).all()


def test_disruption_id_uniqueness(df):
    assert df["DisruptionID"].is_unique


def test_disruption_id_format(df):
    assert df["DisruptionID"].str.fullmatch(r"DIS[0-9]{8}").all()


# ---------------------------------------------------------------------------
# Foreign keys
# ---------------------------------------------------------------------------

def test_flight_operation_keys_resolve(df, flight_ops):
    valid = set(flight_ops["FlightOperationKey"].astype(int))
    assert set(df["FlightOperationKey"].astype(int)).issubset(valid)


def test_airline_foreign_keys_resolve(df, dim_airline):
    valid = set(dim_airline["AirlineKey"].astype(int))
    assert set(df["AirlineKey"].astype(int)).issubset(valid)


def test_route_foreign_keys_resolve(df, dim_route):
    valid = set(dim_route["RouteKey"].astype(int))
    assert set(df["RouteKey"].astype(int)).issubset(valid)


def test_airport_foreign_keys_resolve(df, dim_airport):
    valid = set(dim_airport["AirportKey"].astype(int))
    assert set(df["EventLocationAirportKey"].astype(int)).issubset(valid)


def test_disruption_type_foreign_keys_resolve(df, dim_disruption_type):
    valid = set(dim_disruption_type["DisruptionTypeKey"].astype(int))
    assert set(df["DisruptionTypeKey"].astype(int)).issubset(valid)


def test_date_key_foreign_keys_resolve(df, dim_date):
    valid = set(dim_date["DateKey"].astype(int))
    assert set(df["EventDateKey"].astype(int)).issubset(valid)


# ---------------------------------------------------------------------------
# Event location
# ---------------------------------------------------------------------------

def test_event_location_is_route_origin_or_destination(df, dim_route):
    route_info = dict(
        zip(
            dim_route["RouteKey"].astype(int),
            dim_route[["OriginAirportKey", "DestinationAirportKey"]].values,
        )
    )
    for _, row in df.iterrows():
        rk = int(row["RouteKey"])
        origin, destination = route_info[rk]
        loc = int(row["EventLocationAirportKey"])
        assert loc in (int(origin), int(destination))


# ---------------------------------------------------------------------------
# Event sequence
# ---------------------------------------------------------------------------

def test_event_sequence_positive(df):
    assert (df["EventSequence"] > 0).all()


def test_event_sequence_unique_with_flight(df):
    assert not df.duplicated(["FlightOperationKey", "EventSequence"]).any()


def test_event_sequence_contiguous_per_flight(df):
    for fop_key, group in df.groupby("FlightOperationKey"):
        seqs = sorted(group["EventSequence"].astype(int).tolist())
        assert seqs == list(range(1, len(seqs) + 1))


# ---------------------------------------------------------------------------
# Primary cause flag
# ---------------------------------------------------------------------------

def test_primary_cause_flag_one_per_flight(df):
    for fop_key, group in df.groupby("FlightOperationKey"):
        primary_count = int(group["PrimaryCauseFlag"].sum())
        assert primary_count == 1


# ---------------------------------------------------------------------------
# Delay minutes
# ---------------------------------------------------------------------------

def test_delay_minutes_non_negative(df):
    assert (df["DelayMinutes"] >= 0).all()


# ---------------------------------------------------------------------------
# Reactionary rules
# ---------------------------------------------------------------------------

def test_reactionary_requires_eligible_type(df, dim_disruption_type):
    eligible_types = set(
        dim_disruption_type.loc[
            dim_disruption_type["ReactionaryEligibleFlag"] == True,
            "DisruptionTypeKey",
        ].astype(int)
    )
    reactionary_rows = df[df["ReactionaryFlag"] == True]
    for _, row in reactionary_rows.iterrows():
        assert int(row["DisruptionTypeKey"]) in eligible_types


def test_reactionary_requires_evidence_id(df):
    reactionary_rows = df[df["ReactionaryFlag"] == True]
    for _, row in reactionary_rows.iterrows():
        assert pd.notna(row["ReactionaryEvidenceID"])
        assert str(row["ReactionaryEvidenceID"]).startswith("EVID")


def test_reactionary_evidence_null_when_flag_false(df):
    non_reactionary = df[df["ReactionaryFlag"] == False]
    for _, row in non_reactionary.iterrows():
        assert pd.isna(row["ReactionaryEvidenceID"])


# ---------------------------------------------------------------------------
# Delay partition sums to arrival delay
# ---------------------------------------------------------------------------

def test_delay_partition_sums_to_arrival_delay(df, flight_ops):
    for fop_key, group in df.groupby("FlightOperationKey"):
        flight_row = flight_ops[flight_ops["FlightOperationKey"] == fop_key]
        if len(flight_row) == 0:
            continue
        flight_row = flight_row.iloc[0]
        if (
            flight_row["FlightStatus"] == "Operated"
            and pd.notna(flight_row["ArrivalDelayMinutes"])
            and int(flight_row["ArrivalDelayMinutes"]) > 0
        ):
            arr_delay = int(flight_row["ArrivalDelayMinutes"])
            event_delay_sum = int(group["DelayMinutes"].sum())
            assert event_delay_sum == arr_delay


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def test_manifest_status_is_provisional(manifest):
    assert manifest["status"] == "PROVISIONAL_PORTFOLIO_IMPLEMENTATION"


def test_manifest_primary_key_and_row_count(manifest, df):
    assert manifest["primary_key"] == "DisruptionKey"
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


def test_manifest_reactionary_rule_provisional(manifest):
    reactionary = manifest["governance"]["reactionary_rule"]
    assert "not guessed" in reactionary.lower()
    assert "reactionary-eligible" in reactionary.lower()


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
