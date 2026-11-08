"""Regression tests for the curated DimAirline dataset."""

import json

import pandas as pd
import pytest

from src.utilities.hashing import sha256_file
from src.utilities.paths import project_path


CURATED = project_path("data", "03_curated")
MANIFESTS = project_path("data", "manifests")

CSV_PATH = CURATED / "dim_airline.csv"
PARQUET_PATH = CURATED / "dim_airline.parquet"
MANIFEST_PATH = MANIFESTS / "dim_airline_manifest.json"

COLUMNS = [
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
    "ReferenceVersion",
]

EXPECTED_IDS = [f"AIR-{i:04d}" for i in range(1, 11)]


@pytest.fixture
def df():
    return pd.read_parquet(PARQUET_PATH)


@pytest.fixture
def manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_ten_records(df):
    assert len(df) == 10


def test_exact_column_order(df):
    assert list(df.columns) == COLUMNS


def test_airline_key_uniqueness(df):
    assert df["AirlineKey"].is_unique


def test_airline_id_uniqueness(df):
    assert df["AirlineId"].is_unique


def test_airline_id_preservation(df):
    assert df["AirlineId"].tolist() == EXPECTED_IDS


def test_airline_keys_one_through_ten(df):
    assert sorted(df["AirlineKey"].tolist()) == list(range(1, 11))


def test_all_baseline_airlines_active(df):
    assert df["IsActive"].all()


def test_nullable_fields_preserved_null(df):
    assert df["AirlineGroup"].isna().all()
    assert df["BusinessModelClass"].isna().all()
    assert df["StatusEffectiveDate"].isna().all()


def test_csv_parquet_row_count_consistency():
    csv_df = pd.read_csv(CSV_PATH, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    parquet_df = pd.read_parquet(PARQUET_PATH)
    assert len(csv_df) == len(parquet_df) == 10
    assert list(csv_df.columns) == COLUMNS


def test_manifest_status_is_provisional(manifest):
    assert manifest["status"] == "PROVISIONAL_PORTFOLIO_IMPLEMENTATION"


def test_manifest_primary_key_and_row_count(manifest):
    assert manifest["primary_key"] == "AirlineKey"
    assert manifest["row_count"] == 10
    assert manifest["column_count"] == 12


def test_manifest_csv_hash_matches(manifest):
    expected = manifest["files"]["csv"]["sha256"]
    actual = sha256_file(CSV_PATH)
    assert expected == actual


def test_manifest_parquet_hash_matches(manifest):
    expected = manifest["files"]["parquet"]["sha256"]
    actual = sha256_file(PARQUET_PATH)
    assert expected == actual


def test_manifest_source_hash_matches(manifest):
    workbook = project_path(
        "data", "04_reference", "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"
    )
    expected = manifest["source"]["sha256"]
    actual = sha256_file(workbook)
    assert expected == actual
