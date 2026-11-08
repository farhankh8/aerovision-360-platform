"""Regression tests for curated FactOperatingCosts dataset.

Covers: schema and data types, primary-key uniqueness, business-key uniqueness,
foreign-key integrity, currency validity, exact-date FX lookup, missing-rate
quarantine, USD conversion accuracy, decimal precision and rounding,
deterministic reproducibility, duplicate detection, null and invalid-value
detection, cost category/subcategory integrity, sign convention, and
synthetic provenance.
"""

import json
from datetime import date, datetime

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from src.utilities.hashing import sha256_file
from src.utilities.paths import project_path

CURATED = project_path("data", "03_curated")
MANIFESTS = project_path("data", "manifests")
QUARANTINE = project_path("data", "02_staging", "quarantine")

CSV_PATH = CURATED / "fact_operating_costs.csv"
PARQUET_PATH = CURATED / "fact_operating_costs.parquet"
MANIFEST_PATH = MANIFESTS / "fact_operating_costs_manifest.json"
QUARANTINE_PATH = QUARANTINE / "fact_operating_costs_quarantined.csv"

FFO_PATH = CURATED / "fact_flight_operations.parquet"
AIRLINE_PATH = CURATED / "dim_airline.parquet"
ROUTE_PATH = CURATED / "dim_route.parquet"
DATE_PATH = CURATED / "dim_date.parquet"
CURRENCY_PATH = CURATED / "dim_currency.parquet"
FX_PATH = project_path("data", "04_reference", "ref_exchange_rates.csv")

COLUMNS = [
    "OperatingCostKey",
    "CostLineID",
    "FlightOperationKey",
    "AirlineKey",
    "RouteKey",
    "CostDateKey",
    "CostCategory",
    "CostSubcategory",
    "CostAmount",
    "CurrencyKey",
    "ExchangeRateToUSD",
    "RateDateKey",
    "RateVersion",
    "CostAmountUSD",
    "CostDescription",
    "SourceDocumentNumber",
    "IsAllocated",
    "SyntheticProvenance",
]

MONEY_COLS_2DP = ["CostAmount", "CostAmountUSD"]

SYNTHETIC_PROVENANCE = "Synthetic Simulation — Not Actual Airline Performance."

COST_CATEGORIES = {
    "Fuel": ["Jet Fuel", "Fuel Surcharge", "Fuel Adjustment"],
    "Crew": ["Flight Crew", "Cabin Crew", "Crew Accommodation",
             "Crew Transport", "Crew Training"],
    "Maintenance": ["Line Maintenance", "Base Maintenance",
                    "Aircraft Parts", "Component Overhaul"],
    "Airport Charges": ["Landing Charges", "Parking Charges",
                        "Passenger Handling", "Ground Handling"],
    "Navigation": ["En-route Charges", "Terminal Navigation Charges"],
    "Sales and Distribution": ["Agency Commission", "GDS Fees",
                               "Payment Processing", "Distribution Fees"],
    "Overhead": ["Administration", "IT", "Facilities", "Insurance",
                 "Professional Services"],
    "Other": ["Operational Supplies", "Other Direct Operating Expenses"],
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def df():
    return pd.read_parquet(PARQUET_PATH)


@pytest.fixture
def csv_df():
    return pd.read_csv(CSV_PATH, encoding="utf-8")


@pytest.fixture
def manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def dim_route():
    return pd.read_parquet(ROUTE_PATH)


@pytest.fixture
def dim_airline():
    return pd.read_parquet(AIRLINE_PATH)


@pytest.fixture
def dim_date():
    return pd.read_parquet(DATE_PATH)


@pytest.fixture
def dim_currency():
    return pd.read_parquet(CURRENCY_PATH)


@pytest.fixture
def fact_flight_operations():
    return pd.read_parquet(FFO_PATH)


@pytest.fixture
def fx_rates():
    return pd.read_csv(FX_PATH, dtype={"CurrencyCode": "string", "RateDate": "string"})


# ---------------------------------------------------------------------------
# Schema and data types
# ---------------------------------------------------------------------------

def test_exact_column_order(df):
    assert list(df.columns) == COLUMNS


def test_row_count_positive(df):
    assert len(df) > 0


def test_manifest_row_count_matches(df, manifest):
    assert manifest["row_count"] == len(df)


def test_manifest_column_count_matches(df, manifest):
    assert manifest["column_count"] == len(df.columns)


def test_manifest_columns_match(df, manifest):
    assert manifest["columns"] == COLUMNS


def test_parquet_schema_types(df):
    schema = pq.read_schema(PARQUET_PATH)
    assert schema.field("OperatingCostKey").type == pa.int64()
    assert schema.field("CostLineID").type == pa.string()
    assert schema.field("FlightOperationKey").type == pa.int64()
    assert schema.field("AirlineKey").type == pa.int32()
    assert schema.field("RouteKey").type == pa.int32()
    assert schema.field("CostDateKey").type == pa.int32()
    assert schema.field("CostCategory").type == pa.string()
    assert schema.field("CostSubcategory").type == pa.string()
    assert schema.field("CostAmount").type == pa.float64()
    assert schema.field("CurrencyKey").type == pa.int32()
    assert schema.field("ExchangeRateToUSD").type == pa.float64()
    assert schema.field("RateDateKey").type == pa.int32()
    assert schema.field("RateVersion").type == pa.string()
    assert schema.field("CostAmountUSD").type == pa.float64()
    assert schema.field("CostDescription").type == pa.string()
    assert schema.field("SourceDocumentNumber").type == pa.string()
    assert schema.field("IsAllocated").type == pa.bool_()
    assert schema.field("SyntheticProvenance").type == pa.string()


def test_csv_parquet_row_count_consistency(csv_df, df):
    assert len(csv_df) == len(df)


# ---------------------------------------------------------------------------
# Primary-key uniqueness
# ---------------------------------------------------------------------------

def test_operating_cost_key_uniqueness(df):
    assert df["OperatingCostKey"].is_unique


def test_operating_cost_key_positive(df):
    assert (df["OperatingCostKey"] > 0).all()


# ---------------------------------------------------------------------------
# Business-key uniqueness
# ---------------------------------------------------------------------------

def test_cost_line_id_uniqueness(df):
    assert df["CostLineID"].is_unique


def test_cost_line_id_format(df):
    assert df["CostLineID"].str.len().max() <= 30
    assert df["CostLineID"].notna().all()


# ---------------------------------------------------------------------------
# Composite grain-key uniqueness
# ---------------------------------------------------------------------------

def test_composite_grain_key_uniqueness(df):
    assert not df.duplicated(
        ["FlightOperationKey", "CostCategory", "CostSubcategory",
         "CostDateKey", "SourceDocumentNumber"]
    ).any(), (
        "Composite grain key (FlightOperationKey + CostCategory + "
        "CostSubcategory + CostDateKey + SourceDocumentNumber) must be unique."
    )


# ---------------------------------------------------------------------------
# Foreign-key integrity
# ---------------------------------------------------------------------------

def test_flight_operation_logical_references_resolve(df, fact_flight_operations):
    valid_keys = set(fact_flight_operations["FlightOperationKey"].astype(int))
    assert set(df["FlightOperationKey"].astype(int)).issubset(valid_keys)


def test_airline_foreign_keys_resolve(df, dim_airline):
    valid_keys = set(dim_airline["AirlineKey"].astype(int))
    assert set(df["AirlineKey"].astype(int)).issubset(valid_keys)


def test_route_foreign_keys_resolve(df, dim_route):
    valid_keys = set(dim_route["RouteKey"].astype(int))
    assert set(df["RouteKey"].astype(int)).issubset(valid_keys)


def test_cost_date_key_foreign_key_resolves(df, dim_date):
    valid_keys = set(dim_date["DateKey"].astype(int))
    assert set(df["CostDateKey"].astype(int)).issubset(valid_keys)


def test_rate_date_key_foreign_key_resolves(df, dim_date):
    valid_keys = set(dim_date["DateKey"].astype(int))
    assert set(df["RateDateKey"].astype(int)).issubset(valid_keys)


def test_currency_foreign_keys_resolve(df, dim_currency):
    valid_keys = set(dim_currency["CurrencyKey"].astype(int))
    assert set(df["CurrencyKey"].astype(int)).issubset(valid_keys)


# ---------------------------------------------------------------------------
# AirlineKey and RouteKey agree with flight leg
# ---------------------------------------------------------------------------

def test_airline_key_matches_flight_leg(df, fact_flight_operations):
    ffo_by_key = fact_flight_operations.set_index("FlightOperationKey")
    for _, row in df.iterrows():
        ffo_airline = int(ffo_by_key.loc[int(row["FlightOperationKey"]), "AirlineKey"])
        assert int(row["AirlineKey"]) == ffo_airline


def test_route_key_matches_flight_leg(df, fact_flight_operations):
    ffo_by_key = fact_flight_operations.set_index("FlightOperationKey")
    for _, row in df.iterrows():
        ffo_route = int(ffo_by_key.loc[int(row["FlightOperationKey"]), "RouteKey"])
        assert int(row["RouteKey"]) == ffo_route


# ---------------------------------------------------------------------------
# Cost date within reporting period
# ---------------------------------------------------------------------------

def test_cost_date_within_reporting_period(df):
    assert (df["CostDateKey"] >= 20251001).all()
    assert (df["CostDateKey"] <= 20260930).all()


# ---------------------------------------------------------------------------
# Currency validity
# ---------------------------------------------------------------------------

def test_currency_codes_valid(df, dim_currency):
    valid_codes = set(dim_currency["CurrencyCode"].astype(str))
    currency_key_to_code = dict(zip(
        dim_currency["CurrencyKey"].astype(int),
        dim_currency["CurrencyCode"].astype(str),
    ))
    used_codes = {currency_key_to_code[k] for k in df["CurrencyKey"].astype(int)}
    assert used_codes.issubset(valid_codes)


def test_exchange_rate_positive(df):
    assert (df["ExchangeRateToUSD"] > 0).all()


def test_exchange_rate_six_decimals(df):
    scaled = (df["ExchangeRateToUSD"] * 1_000_000).round(6)
    assert (scaled == scaled.astype("int64")).all()


# ---------------------------------------------------------------------------
# Exact-date FX lookup
# ---------------------------------------------------------------------------

def test_exact_date_fx_lookup(df, dim_currency, fx_rates):
    """Every cost row has an exact-date FX rate for its currency and rate date."""
    currency_key_to_code = dict(zip(
        dim_currency["CurrencyKey"].astype(int),
        dim_currency["CurrencyCode"].astype(str),
    ))
    dates = pd.read_parquet(DATE_PATH)
    def _to_date_obj(v):
        if isinstance(v, date):
            return v
        return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()
    dates["_full_date"] = dates["FullDate"].apply(_to_date_obj)
    date_key_to_date = dict(zip(dates["DateKey"].astype(int), dates["_full_date"]))

    fx_lookup = {}
    for _, fx_row in fx_rates.iterrows():
        fx_lookup[(str(fx_row["CurrencyCode"]), str(fx_row["RateDate"]))] = \
            float(fx_row["ExchangeRateToUSD"])

    for _, row in df.iterrows():
        ccy = currency_key_to_code[int(row["CurrencyKey"])]
        rate_date = date_key_to_date[int(row["RateDateKey"])].isoformat()
        assert (ccy, rate_date) in fx_lookup, \
            f"Missing exact-date FX rate for {ccy} on {rate_date}"


# ---------------------------------------------------------------------------
# Missing-rate quarantine
# ---------------------------------------------------------------------------

def test_quarantine_file_exists():
    assert QUARANTINE_PATH.exists()


def test_quarantine_has_expected_columns():
    qdf = pd.read_csv(QUARANTINE_PATH, encoding="utf-8")
    expected = [
        "OperatingCostKey", "CostLineID", "FlightOperationKey", "AirlineKey",
        "RouteKey", "CostDateKey", "CostCategory", "CostSubcategory",
        "CurrencyKey", "CurrencyCode", "RateDateKey", "RateDate",
        "CostAmount", "QuarantineReason", "QuarantineRuleID",
        "SyntheticProvenance",
    ]
    assert list(qdf.columns) == expected


def test_quarantine_reason_is_missing_fx():
    qdf = pd.read_csv(QUARANTINE_PATH, encoding="utf-8")
    if len(qdf) > 0:
        assert (qdf["QuarantineReason"] == "MISSING_FX_RATE").all()
        assert (qdf["QuarantineRuleID"] == "OD-04e").all()


def test_no_forward_fill_no_quarantined_in_curated(df):
    assert df["ExchangeRateToUSD"].notna().all()
    assert (df["ExchangeRateToUSD"] > 0).all()


# ---------------------------------------------------------------------------
# USD conversion accuracy
# ---------------------------------------------------------------------------

def test_usd_conversion_accuracy(df, dim_currency, fx_rates):
    """CostAmountUSD == round(CostAmount * ExchangeRateToUSD, 2), same sign."""
    currency_key_to_code = dict(zip(
        dim_currency["CurrencyKey"].astype(int),
        dim_currency["CurrencyCode"].astype(str),
    ))
    dates = pd.read_parquet(DATE_PATH)
    def _to_date_obj(v):
        if isinstance(v, date):
            return v
        return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()
    dates["_full_date"] = dates["FullDate"].apply(_to_date_obj)
    date_key_to_date = dict(zip(dates["DateKey"].astype(int), dates["_full_date"]))

    fx_lookup = {}
    for _, fx_row in fx_rates.iterrows():
        fx_lookup[(str(fx_row["CurrencyCode"]), str(fx_row["RateDate"]))] = \
            float(fx_row["ExchangeRateToUSD"])

    for _, row in df.iterrows():
        ccy = currency_key_to_code[int(row["CurrencyKey"])]
        rate_date = date_key_to_date[int(row["RateDateKey"])].isoformat()
        rate = fx_lookup[(ccy, rate_date)]
        expected_usd = round(float(row["CostAmount"]) * rate, 2)
        assert abs(float(row["CostAmountUSD"]) - expected_usd) <= 0.01, \
            f"CostAmountUSD conversion mismatch: {row['CostAmountUSD']} vs {expected_usd}"


# ---------------------------------------------------------------------------
# Decimal precision and rounding
# ---------------------------------------------------------------------------

def test_monetary_columns_two_decimals(df):
    for col in MONEY_COLS_2DP:
        scaled = (df[col] * 100).round(6)
        assert (scaled == scaled.astype("int64")).all(), f"{col} not at 2 decimal places."


def test_no_null_monetary_values(df):
    for col in MONEY_COLS_2DP + ["ExchangeRateToUSD"]:
        assert df[col].notna().all(), f"{col} contains nulls."


# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------

def test_no_duplicate_operating_cost_keys(df):
    assert df["OperatingCostKey"].nunique() == len(df)


def test_no_duplicate_cost_line_ids(df):
    assert df["CostLineID"].nunique() == len(df)


def test_no_duplicate_composite_grain_keys(df):
    dupes = df.duplicated(
        ["FlightOperationKey", "CostCategory", "CostSubcategory",
         "CostDateKey", "SourceDocumentNumber"]
    )
    assert not dupes.any()


# ---------------------------------------------------------------------------
# Null and invalid-value detection
# ---------------------------------------------------------------------------

def test_no_nulls_in_required_columns(df):
    for col in COLUMNS:
        assert df[col].notna().all(), f"Required column {col} contains nulls."


def test_exchange_rate_to_usd_positive(df):
    assert (df["ExchangeRateToUSD"] > 0).all()


def test_rate_version_consistent(df):
    assert (df["RateVersion"] == "FX-2026-11-04-001").all()


def test_cost_description_not_null(df):
    assert df["CostDescription"].notna().all()
    assert df["CostDescription"].str.len().max() <= 200


def test_source_document_number_not_null(df):
    assert df["SourceDocumentNumber"].notna().all()
    assert df["SourceDocumentNumber"].str.len().max() <= 50


def test_is_allocated_boolean(df):
    assert df["IsAllocated"].isin([True, False]).all()


# ---------------------------------------------------------------------------
# Cost category and subcategory integrity
# ---------------------------------------------------------------------------

def test_cost_category_controlled_set(df):
    assert set(df["CostCategory"]).issubset(set(COST_CATEGORIES.keys()))


def test_cost_subcategory_valid_within_category(df):
    for _, row in df.iterrows():
        assert row["CostSubcategory"] in COST_CATEGORIES[row["CostCategory"]], (
            f"CostSubcategory {row['CostSubcategory']} invalid for "
            f"category {row['CostCategory']}"
        )


# ---------------------------------------------------------------------------
# Sign convention
# ---------------------------------------------------------------------------

def test_cost_amount_usd_follows_sign(df):
    """CostAmountUSD must follow the sign of CostAmount."""
    assert (
        (df["CostAmount"] >= 0) == (df["CostAmountUSD"] >= 0)
    ).all(), "CostAmountUSD sign must match CostAmount sign (positive)."
    assert (
        (df["CostAmount"] < 0) == (df["CostAmountUSD"] < 0)
    ).all(), "CostAmountUSD sign must match CostAmount sign (negative)."


# ---------------------------------------------------------------------------
# Deterministic reproducibility
# ---------------------------------------------------------------------------

def test_deterministic_generation_same_seed():
    script = project_path("scripts", "build_fact_operating_costs.py")
    content = script.read_text(encoding="utf-8")
    assert "SEED = 3602028" in content
    assert "RNG = np.random.default_rng(SEED)" in content


def test_manifest_generation_documented(manifest):
    assert manifest["generation"]["random_seed"] == 3602028
    assert manifest["generation"]["method"] == "Deterministic NumPy random generator"


# ---------------------------------------------------------------------------
# Synthetic provenance
# ---------------------------------------------------------------------------

def test_synthetic_provenance_present(df):
    assert (df["SyntheticProvenance"] == SYNTHETIC_PROVENANCE).all()


def test_manifest_disclosure(manifest):
    assert manifest["disclosure"] == SYNTHETIC_PROVENANCE


# ---------------------------------------------------------------------------
# Manifest validation
# ---------------------------------------------------------------------------

def test_manifest_csv_hash_matches(manifest):
    actual = sha256_file(CSV_PATH)
    assert manifest["files"]["csv"]["sha256"] == actual


def test_manifest_parquet_hash_matches(manifest):
    actual = sha256_file(PARQUET_PATH)
    assert manifest["files"]["parquet"]["sha256"] == actual


def test_manifest_quarantine_hash_matches(manifest):
    actual = sha256_file(QUARANTINE_PATH)
    assert manifest["files"]["quarantine"]["sha256"] == actual


def test_manifest_od04_governance_flags(manifest):
    gov = manifest["governance"]
    assert "no forward-fill" in gov["od_04e_missing_date_behaviour"].lower()
    assert "quarantine" in gov["od_04e_missing_date_behaviour"].lower()
    assert gov["od_04c_rate_source"] == "AEROVISION-360-SYNTHETIC-FX-V1"
    assert gov["od_04d_rate_version"] == "FX-2026-11-04-001"


def test_manifest_gov_d07_not_claimed_approved(manifest):
    gov = manifest["governance"]
    assert "not approved" in gov["gov_d_07_manifest_hash"].lower()
    assert "revised draft" in gov["gov_d_07_manifest_hash"].lower()
