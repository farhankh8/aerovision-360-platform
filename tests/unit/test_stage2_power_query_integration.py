"""Stage 2 — Power Query Integration validation tests.

Simulates the Power Query M loading process (Csv.Document + PromoteAllHeaders +
TransformColumnTypes) against the CSV files in deliverables/data/ and validates
that the two financial fact tables integrate correctly.

Tests cover:
1. Source row counts match loaded row counts
2. Column names and types match the approved schemas
3. Primary keys remain unique
4. Foreign keys resolve
5. Currency and exchange-rate references remain valid
6. Original and converted monetary values remain unchanged
7. No unexpected rows are dropped
8. No unexpected nulls are introduced
9. Repeated refreshes produce consistent results
10. Synthetic provenance remains intact
"""

import json
from datetime import date, datetime

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from src.utilities.hashing import sha256_file
from src.utilities.paths import project_path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# Power Query imports from deliverables/data/ (existing convention).
PQ_DATA = project_path("deliverables", "data")

# Source-of-truth curated files (Stage 1 outputs).
CURATED = project_path("data", "03_curated")
MANIFESTS = project_path("data", "manifests")

PQ_BOOKING_CSV = PQ_DATA / "fact_booking_transactions.csv"
PQ_OPERATING_COSTS_CSV = PQ_DATA / "fact_operating_costs.csv"

CURATED_BOOKING_CSV = CURATED / "fact_booking_transactions.csv"
CURATED_OPERATING_COSTS_CSV = CURATED / "fact_operating_costs.csv"

FFO_PATH = CURATED / "fact_flight_operations.parquet"
AIRLINE_PATH = CURATED / "dim_airline.parquet"
ROUTE_PATH = CURATED / "dim_route.parquet"
DATE_PATH = CURATED / "dim_date.parquet"
CUSTOMER_PATH = CURATED / "dim_customer.parquet"
FARE_CLASS_PATH = CURATED / "dim_fare_class.parquet"
BOOKING_CHANNEL_PATH = CURATED / "dim_booking_channel.parquet"
CURRENCY_PATH = CURATED / "dim_currency.parquet"
FX_PATH = project_path("data", "04_reference", "ref_exchange_rates.csv")

# Approved schemas (from data contracts v1.5 sections 6.3.2 / 6.3.3,
# and GOV-D-04 Sections 4/5).
BOOKING_COLUMNS = [
    "BookingTransactionKey", "BookingReference", "TicketNumber",
    "TicketCouponNumber", "CustomerKey", "AirlineKey", "FlightOperationKey",
    "RouteKey", "FareClassKey", "BookingChannelKey", "BookingDateKey",
    "TravelDateKey", "PassengerCount", "IsRevenuePassenger",
    "BaseFareAmount", "DiscountAmount", "TaxAmount", "FeeAmount",
    "AncillaryRevenueAmount", "RefundAmount", "AncillaryRefundAmount",
    "FeeRefundAmount", "CancellationFeeAmount", "NoShowFeeAmount",
    "TransactionCurrencyKey", "ExchangeRateToUSD", "RateDateKey",
    "RateVersion", "BaseFareUSD", "DiscountUSD", "TaxUSD", "FeeUSD",
    "AncillaryRevenueUSD", "RefundUSD", "AncillaryRefundUSD",
    "FeeRefundUSD", "CancellationFeeUSD", "NoShowFeeUSD",
    "NetPassengerRevenueUSD", "NetFeeRevenueUSD", "NetAncillaryRevenueUSD",
    "TransactionStatus", "IsRefunded", "BookingLeadTimeDays",
    "SyntheticProvenance",
]

OPERATING_COSTS_COLUMNS = [
    "OperatingCostKey", "CostLineID", "FlightOperationKey", "AirlineKey",
    "RouteKey", "CostDateKey", "CostCategory", "CostSubcategory",
    "CostAmount", "CurrencyKey", "ExchangeRateToUSD", "RateDateKey",
    "RateVersion", "CostAmountUSD", "CostDescription",
    "SourceDocumentNumber", "IsAllocated", "SyntheticProvenance",
]

BOOKING_MONEY_COLS = [
    "BaseFareAmount", "DiscountAmount", "TaxAmount", "FeeAmount",
    "AncillaryRevenueAmount", "RefundAmount", "AncillaryRefundAmount",
    "FeeRefundAmount", "CancellationFeeAmount", "NoShowFeeAmount",
    "BaseFareUSD", "DiscountUSD", "TaxUSD", "FeeUSD",
    "AncillaryRevenueUSD", "RefundUSD", "AncillaryRefundUSD",
    "FeeRefundUSD", "CancellationFeeUSD", "NoShowFeeUSD",
    "NetPassengerRevenueUSD", "NetFeeRevenueUSD", "NetAncillaryRevenueUSD",
]

OPERATING_COSTS_MONEY_COLS = ["CostAmount", "CostAmountUSD"]

SYNTHETIC_PROVENANCE = "Synthetic Simulation — Not Actual Airline Performance."

# M type mapping (mirrors AEROVISION360_DataLoad.m TransformColumnTypes).
BOOKING_M_TYPES = {
    "BookingTransactionKey": "Int64",
    "BookingReference": "text",
    "TicketNumber": "text",
    "TicketCouponNumber": "Int64",
    "CustomerKey": "Int64",
    "AirlineKey": "Int64",
    "FlightOperationKey": "Int64",
    "RouteKey": "Int64",
    "FareClassKey": "Int64",
    "BookingChannelKey": "Int64",
    "BookingDateKey": "Int64",
    "TravelDateKey": "Int64",
    "PassengerCount": "Int64",
    "IsRevenuePassenger": "logical",
    "BaseFareAmount": "number",
    "DiscountAmount": "number",
    "TaxAmount": "number",
    "FeeAmount": "number",
    "AncillaryRevenueAmount": "number",
    "RefundAmount": "number",
    "AncillaryRefundAmount": "number",
    "FeeRefundAmount": "number",
    "CancellationFeeAmount": "number",
    "NoShowFeeAmount": "number",
    "TransactionCurrencyKey": "Int64",
    "ExchangeRateToUSD": "number",
    "RateDateKey": "Int64",
    "RateVersion": "text",
    "BaseFareUSD": "number",
    "DiscountUSD": "number",
    "TaxUSD": "number",
    "FeeUSD": "number",
    "AncillaryRevenueUSD": "number",
    "RefundUSD": "number",
    "AncillaryRefundUSD": "number",
    "FeeRefundUSD": "number",
    "CancellationFeeUSD": "number",
    "NoShowFeeUSD": "number",
    "NetPassengerRevenueUSD": "number",
    "NetFeeRevenueUSD": "number",
    "NetAncillaryRevenueUSD": "number",
    "TransactionStatus": "text",
    "IsRefunded": "logical",
    "BookingLeadTimeDays": "Int64",
    "SyntheticProvenance": "text",
}

OPERATING_COSTS_M_TYPES = {
    "OperatingCostKey": "Int64",
    "CostLineID": "text",
    "FlightOperationKey": "Int64",
    "AirlineKey": "Int64",
    "RouteKey": "Int64",
    "CostDateKey": "Int64",
    "CostCategory": "text",
    "CostSubcategory": "text",
    "CostAmount": "number",
    "CurrencyKey": "Int64",
    "ExchangeRateToUSD": "number",
    "RateDateKey": "Int64",
    "RateVersion": "text",
    "CostAmountUSD": "number",
    "CostDescription": "text",
    "SourceDocumentNumber": "text",
    "IsAllocated": "logical",
    "SyntheticProvenance": "text",
}


# ---------------------------------------------------------------------------
# Fixtures — simulate Power Query load from deliverables/data/ CSVs
# ---------------------------------------------------------------------------

def _load_simulated_power_query(csv_path, m_types, columns):
    """Simulate Power Query: Csv.Document + PromoteAllHeaders +
    TransformColumnTypes with the declared M types."""
    df = pd.read_csv(csv_path, encoding="utf-8", dtype=str)
    # All columns must be present after header promotion.
    assert list(df.columns) == columns, (
        f"Column mismatch: expected {len(columns)} columns, "
        f"got {len(df.columns)}"
    )
    # Apply M type conversions (simulating Table.TransformColumnTypes).
    for col, m_type in m_types.items():
        if m_type == "Int64":
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        elif m_type == "logical":
            df[col] = df[col].map({"True": True, "False": False,
                                   "true": True, "false": False})
        elif m_type == "number":
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif m_type == "text":
            df[col] = df[col].astype(str)
    return df


@pytest.fixture
def booking_pq():
    return _load_simulated_power_query(
        PQ_BOOKING_CSV, BOOKING_M_TYPES, BOOKING_COLUMNS
    )


@pytest.fixture
def operating_costs_pq():
    return _load_simulated_power_query(
        PQ_OPERATING_COSTS_CSV, OPERATING_COSTS_M_TYPES,
        OPERATING_COSTS_COLUMNS
    )


@pytest.fixture
def booking_curated():
    return pd.read_csv(CURATED_BOOKING_CSV, encoding="utf-8")


@pytest.fixture
def operating_costs_curated():
    return pd.read_csv(CURATED_OPERATING_COSTS_CSV, encoding="utf-8")


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
def dim_customer():
    return pd.read_parquet(CUSTOMER_PATH)


@pytest.fixture
def dim_fare_class():
    return pd.read_parquet(FARE_CLASS_PATH)


@pytest.fixture
def dim_booking_channel():
    return pd.read_parquet(BOOKING_CHANNEL_PATH)


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
# Test 1: Source row counts match loaded row counts (no rows dropped)
# ---------------------------------------------------------------------------

def test_source_row_count_matches_loaded_booking(booking_pq, booking_curated):
    assert len(booking_pq) == len(booking_curated), (
        f"Power Query loaded {len(booking_pq)} rows but source has "
        f"{len(booking_curated)} rows."
    )


def test_source_row_count_matches_loaded_operating_costs(
    operating_costs_pq, operating_costs_curated
):
    assert len(operating_costs_pq) == len(operating_costs_curated), (
        f"Power Query loaded {len(operating_costs_pq)} rows but source has "
        f"{len(operating_costs_curated)} rows."
    )


def test_deliverables_csv_matches_curated_booking():
    """The deliverables/data/ copy must be byte-identical to the curated source."""
    pq_hash = sha256_file(PQ_BOOKING_CSV)
    curated_hash = sha256_file(CURATED_BOOKING_CSV)
    assert pq_hash == curated_hash, (
        "deliverables/data/fact_booking_transactions.csv differs from "
        "data/03_curated/fact_booking_transactions.csv"
    )


def test_deliverables_csv_matches_curated_operating_costs():
    """The deliverables/data/ copy must be byte-identical to the curated source."""
    pq_hash = sha256_file(PQ_OPERATING_COSTS_CSV)
    curated_hash = sha256_file(CURATED_OPERATING_COSTS_CSV)
    assert pq_hash == curated_hash, (
        "deliverables/data/fact_operating_costs.csv differs from "
        "data/03_curated/fact_operating_costs.csv"
    )


# ---------------------------------------------------------------------------
# Test 2: Column names and types match the approved schemas
# ---------------------------------------------------------------------------

def test_booking_column_names_match_schema(booking_pq):
    assert list(booking_pq.columns) == BOOKING_COLUMNS


def test_operating_costs_column_names_match_schema(operating_costs_pq):
    assert list(operating_costs_pq.columns) == OPERATING_COSTS_COLUMNS


def test_booking_column_types_after_m_transform(booking_pq):
    """Verify M type conversions produced correct pandas dtypes."""
    int64_cols = [c for c, t in BOOKING_M_TYPES.items() if t == "Int64"]
    for col in int64_cols:
        assert booking_pq[col].dtype == "Int64", f"{col} not Int64 after M transform"

    logical_cols = [c for c, t in BOOKING_M_TYPES.items() if t == "logical"]
    for col in logical_cols:
        assert booking_pq[col].dtype == "bool", f"{col} not bool after M transform"

    number_cols = [c for c, t in BOOKING_M_TYPES.items() if t == "number"]
    for col in number_cols:
        assert pd.api.types.is_float_dtype(
            booking_pq[col]
        ) or pd.api.types.is_integer_dtype(booking_pq[col]), \
            f"{col} not numeric after M transform"

    text_cols = [c for c, t in BOOKING_M_TYPES.items() if t == "text"]
    for col in text_cols:
        col_dtype = booking_pq[col].dtype
        is_text = (col_dtype == object) or isinstance(
            col_dtype, pd.StringDtype
        )
        assert is_text, f"{col} not text after M transform, got {col_dtype}"


def test_operating_costs_column_types_after_m_transform(operating_costs_pq):
    """Verify M type conversions produced correct pandas dtypes."""
    int64_cols = [c for c, t in OPERATING_COSTS_M_TYPES.items() if t == "Int64"]
    for col in int64_cols:
        assert operating_costs_pq[col].dtype == "Int64", f"{col} not Int64 after M transform"

    logical_cols = [c for c, t in OPERATING_COSTS_M_TYPES.items() if t == "logical"]
    for col in logical_cols:
        assert operating_costs_pq[col].dtype == "bool", f"{col} not bool after M transform"

    number_cols = [c for c, t in OPERATING_COSTS_M_TYPES.items() if t == "number"]
    for col in number_cols:
        assert pd.api.types.is_float_dtype(
            operating_costs_pq[col]
        ) or pd.api.types.is_integer_dtype(operating_costs_pq[col]), \
            f"{col} not numeric after M transform"

    text_cols = [c for c, t in OPERATING_COSTS_M_TYPES.items() if t == "text"]
    for col in text_cols:
        col_dtype = operating_costs_pq[col].dtype
        is_text = (col_dtype == object) or isinstance(col_dtype, pd.StringDtype)
        assert is_text, f"{col} not text after M transform, got {col_dtype}"


# ---------------------------------------------------------------------------
# Test 3: Primary keys remain unique
# ---------------------------------------------------------------------------

def test_booking_primary_key_unique(booking_pq):
    assert booking_pq["BookingTransactionKey"].is_unique, (
        "BookingTransactionKey must be unique after Power Query load."
    )


def test_operating_costs_primary_key_unique(operating_costs_pq):
    assert operating_costs_pq["OperatingCostKey"].is_unique, (
        "OperatingCostKey must be unique after Power Query load."
    )


# ---------------------------------------------------------------------------
# Test 4: Foreign keys resolve
# ---------------------------------------------------------------------------

def test_booking_fks_resolve(booking_pq, dim_customer, dim_airline,
                              fact_flight_operations, dim_route,
                              dim_fare_class, dim_booking_channel,
                              dim_date, dim_currency):
    valid_customers = set(dim_customer["CustomerKey"].astype(int))
    valid_airlines = set(dim_airline["AirlineKey"].astype(int))
    valid_ffo = set(fact_flight_operations["FlightOperationKey"].astype(int))
    valid_routes = set(dim_route["RouteKey"].astype(int))
    valid_fare = set(dim_fare_class["FareClassKey"].astype(int))
    valid_channels = set(dim_booking_channel["BookingChannelKey"].astype(int))
    valid_dates = set(dim_date["DateKey"].astype(int))
    valid_currencies = set(dim_currency["CurrencyKey"].astype(int))

    assert set(booking_pq["CustomerKey"].dropna().astype(int)).issubset(
        valid_customers
    )
    assert set(booking_pq["AirlineKey"].dropna().astype(int)).issubset(
        valid_airlines
    )
    assert set(booking_pq["FlightOperationKey"].dropna().astype(int)).issubset(
        valid_ffo
    )
    assert set(booking_pq["RouteKey"].dropna().astype(int)).issubset(
        valid_routes
    )
    assert set(booking_pq["FareClassKey"].dropna().astype(int)).issubset(
        valid_fare
    )
    assert set(booking_pq["BookingChannelKey"].dropna().astype(int)).issubset(
        valid_channels
    )
    assert set(booking_pq["BookingDateKey"].dropna().astype(int)).issubset(
        valid_dates
    )
    assert set(booking_pq["TravelDateKey"].dropna().astype(int)).issubset(
        valid_dates
    )
    assert set(booking_pq["RateDateKey"].dropna().astype(int)).issubset(
        valid_dates
    )
    assert set(booking_pq["TransactionCurrencyKey"].dropna().astype(int)).issubset(
        valid_currencies
    )


def test_operating_costs_fks_resolve(operating_costs_pq, dim_airline,
                                      fact_flight_operations, dim_route,
                                      dim_date, dim_currency):
    valid_airlines = set(dim_airline["AirlineKey"].astype(int))
    valid_ffo = set(fact_flight_operations["FlightOperationKey"].astype(int))
    valid_routes = set(dim_route["RouteKey"].astype(int))
    valid_dates = set(dim_date["DateKey"].astype(int))
    valid_currencies = set(dim_currency["CurrencyKey"].astype(int))

    assert set(operating_costs_pq["FlightOperationKey"].dropna().astype(int)).issubset(
        valid_ffo
    )
    assert set(operating_costs_pq["AirlineKey"].dropna().astype(int)).issubset(
        valid_airlines
    )
    assert set(operating_costs_pq["RouteKey"].dropna().astype(int)).issubset(
        valid_routes
    )
    assert set(operating_costs_pq["CostDateKey"].dropna().astype(int)).issubset(
        valid_dates
    )
    assert set(operating_costs_pq["RateDateKey"].dropna().astype(int)).issubset(
        valid_dates
    )
    assert set(operating_costs_pq["CurrencyKey"].dropna().astype(int)).issubset(
        valid_currencies
    )


# ---------------------------------------------------------------------------
# Test 5: Currency and exchange-rate references remain valid
# ---------------------------------------------------------------------------

def test_booking_currency_valid(booking_pq, dim_currency, fx_rates):
    currency_key_to_code = dict(zip(
        dim_currency["CurrencyKey"].astype(int),
        dim_currency["CurrencyCode"].astype(str),
    ))
    fx_lookup = {}
    for _, fx_row in fx_rates.iterrows():
        fx_lookup[(str(fx_row["CurrencyCode"]), str(fx_row["RateDate"]))] = \
            float(fx_row["ExchangeRateToUSD"])

    dates = pd.read_parquet(DATE_PATH)
    def _to_date_obj(v):
        if isinstance(v, date):
            return v
        return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()
    dates["_full_date"] = dates["FullDate"].apply(_to_date_obj)
    date_key_to_date = dict(zip(dates["DateKey"].astype(int), dates["_full_date"]))

    for _, row in booking_pq.iterrows():
        ccy = currency_key_to_code[int(row["TransactionCurrencyKey"])]
        rate_date = date_key_to_date[int(row["RateDateKey"])].isoformat()
        assert (ccy, rate_date) in fx_lookup, (
            f"Missing exact-date FX rate for {ccy} on {rate_date}"
        )


def test_operating_costs_currency_valid(operating_costs_pq, dim_currency, fx_rates):
    currency_key_to_code = dict(zip(
        dim_currency["CurrencyKey"].astype(int),
        dim_currency["CurrencyCode"].astype(str),
    ))
    fx_lookup = {}
    for _, fx_row in fx_rates.iterrows():
        fx_lookup[(str(fx_row["CurrencyCode"]), str(fx_row["RateDate"]))] = \
            float(fx_row["ExchangeRateToUSD"])

    dates = pd.read_parquet(DATE_PATH)
    def _to_date_obj(v):
        if isinstance(v, date):
            return v
        return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()
    dates["_full_date"] = dates["FullDate"].apply(_to_date_obj)
    date_key_to_date = dict(zip(dates["DateKey"].astype(int), dates["_full_date"]))

    for _, row in operating_costs_pq.iterrows():
        ccy = currency_key_to_code[int(row["CurrencyKey"])]
        rate_date = date_key_to_date[int(row["RateDateKey"])].isoformat()
        assert (ccy, rate_date) in fx_lookup, (
            f"Missing exact-date FX rate for {ccy} on {rate_date}"
        )


def test_exchange_rate_positive_booking(booking_pq):
    assert (booking_pq["ExchangeRateToUSD"] > 0).all()


def test_exchange_rate_positive_operating_costs(operating_costs_pq):
    assert (operating_costs_pq["ExchangeRateToUSD"] > 0).all()


# ---------------------------------------------------------------------------
# Test 6: Original and converted monetary values remain unchanged
# ---------------------------------------------------------------------------

def test_booking_monetary_values_unchanged(booking_pq, booking_curated):
    for col in BOOKING_MONEY_COLS + ["ExchangeRateToUSD"]:
        pd.testing.assert_series_equal(
            booking_pq[col].reset_index(drop=True),
            booking_curated[col].reset_index(drop=True),
            check_names=False,
        )


def test_operating_costs_monetary_values_unchanged(operating_costs_pq,
                                                    operating_costs_curated):
    for col in OPERATING_COSTS_MONEY_COLS + ["ExchangeRateToUSD"]:
        pd.testing.assert_series_equal(
            operating_costs_pq[col].reset_index(drop=True),
            operating_costs_curated[col].reset_index(drop=True),
            check_names=False,
        )


def test_booking_usd_conversion_accuracy(booking_pq, dim_currency, fx_rates):
    currency_key_to_code = dict(zip(
        dim_currency["CurrencyKey"].astype(int),
        dim_currency["CurrencyCode"].astype(str),
    ))
    fx_lookup = {}
    for _, fx_row in fx_rates.iterrows():
        fx_lookup[(str(fx_row["CurrencyCode"]), str(fx_row["RateDate"]))] = \
            float(fx_row["ExchangeRateToUSD"])

    dates = pd.read_parquet(DATE_PATH)
    def _to_date_obj(v):
        if isinstance(v, date):
            return v
        return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()
    dates["_full_date"] = dates["FullDate"].apply(_to_date_obj)
    date_key_to_date = dict(zip(dates["DateKey"].astype(int), dates["_full_date"]))

    amount_pairs = [
        ("BaseFareAmount", "BaseFareUSD"), ("DiscountAmount", "DiscountUSD"),
        ("TaxAmount", "TaxUSD"), ("FeeAmount", "FeeUSD"),
        ("AncillaryRevenueAmount", "AncillaryRevenueUSD"),
        ("RefundAmount", "RefundUSD"),
        ("AncillaryRefundAmount", "AncillaryRefundUSD"),
        ("FeeRefundAmount", "FeeRefundUSD"),
        ("CancellationFeeAmount", "CancellationFeeUSD"),
        ("NoShowFeeAmount", "NoShowFeeUSD"),
    ]
    for orig_col, usd_col in amount_pairs:
        for _, row in booking_pq.iterrows():
            ccy = currency_key_to_code[int(row["TransactionCurrencyKey"])]
            rate_date = date_key_to_date[int(row["RateDateKey"])].isoformat()
            rate = fx_lookup[(ccy, rate_date)]
            expected_usd = round(float(row[orig_col]) * rate, 2)
            assert abs(float(row[usd_col]) - expected_usd) <= 0.01, (
                f"{usd_col} conversion mismatch: {row[usd_col]} vs {expected_usd}"
            )


def test_operating_costs_usd_conversion_accuracy(operating_costs_pq,
                                                  dim_currency, fx_rates):
    currency_key_to_code = dict(zip(
        dim_currency["CurrencyKey"].astype(int),
        dim_currency["CurrencyCode"].astype(str),
    ))
    fx_lookup = {}
    for _, fx_row in fx_rates.iterrows():
        fx_lookup[(str(fx_row["CurrencyCode"]), str(fx_row["RateDate"]))] = \
            float(fx_row["ExchangeRateToUSD"])

    dates = pd.read_parquet(DATE_PATH)
    def _to_date_obj(v):
        if isinstance(v, date):
            return v
        return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()
    dates["_full_date"] = dates["FullDate"].apply(_to_date_obj)
    date_key_to_date = dict(zip(dates["DateKey"].astype(int), dates["_full_date"]))

    for _, row in operating_costs_pq.iterrows():
        ccy = currency_key_to_code[int(row["CurrencyKey"])]
        rate_date = date_key_to_date[int(row["RateDateKey"])].isoformat()
        rate = fx_lookup[(ccy, rate_date)]
        expected_usd = round(float(row["CostAmount"]) * rate, 2)
        assert abs(float(row["CostAmountUSD"]) - expected_usd) <= 0.01, (
            f"CostAmountUSD conversion mismatch: {row['CostAmountUSD']} vs {expected_usd}"
        )


# ---------------------------------------------------------------------------
# Test 7: No unexpected nulls are introduced
# ---------------------------------------------------------------------------

def test_booking_no_nulls(booking_pq):
    for col in BOOKING_COLUMNS:
        null_count = booking_pq[col].isna().sum()
        assert null_count == 0, f"{col} has {null_count} nulls after Power Query load."


def test_operating_costs_no_nulls(operating_costs_pq):
    for col in OPERATING_COSTS_COLUMNS:
        null_count = operating_costs_pq[col].isna().sum()
        assert null_count == 0, f"{col} has {null_count} nulls after Power Query load."


# ---------------------------------------------------------------------------
# Test 8: Repeated refreshes produce consistent results
# ---------------------------------------------------------------------------

def test_booking_refresh_consistency():
    """Loading the same CSV twice must produce identical results."""
    df1 = _load_simulated_power_query(
        PQ_BOOKING_CSV, BOOKING_M_TYPES, BOOKING_COLUMNS
    )
    df2 = _load_simulated_power_query(
        PQ_BOOKING_CSV, BOOKING_M_TYPES, BOOKING_COLUMNS
    )
    pd.testing.assert_frame_equal(df1, df2)


def test_operating_costs_refresh_consistency():
    """Loading the same CSV twice must produce identical results."""
    df1 = _load_simulated_power_query(
        PQ_OPERATING_COSTS_CSV, OPERATING_COSTS_M_TYPES,
        OPERATING_COSTS_COLUMNS
    )
    df2 = _load_simulated_power_query(
        PQ_OPERATING_COSTS_CSV, OPERATING_COSTS_M_TYPES,
        OPERATING_COSTS_COLUMNS
    )
    pd.testing.assert_frame_equal(df1, df2)


# ---------------------------------------------------------------------------
# Test 9: Synthetic provenance remains intact
# ---------------------------------------------------------------------------

def test_booking_synthetic_provenance(booking_pq):
    assert (booking_pq["SyntheticProvenance"] == SYNTHETIC_PROVENANCE).all()


def test_operating_costs_synthetic_provenance(operating_costs_pq):
    assert (operating_costs_pq["SyntheticProvenance"] == SYNTHETIC_PROVENANCE).all()


# ---------------------------------------------------------------------------
# Test 10: Business key uniqueness preserved after load
# ---------------------------------------------------------------------------

def test_booking_business_key_unique(booking_pq):
    assert not booking_pq.duplicated(
        ["BookingReference", "TicketNumber", "TicketCouponNumber"]
    ).any(), "Business key must be unique after Power Query load."


def test_operating_costs_cost_line_id_unique(operating_costs_pq):
    assert operating_costs_pq["CostLineID"].is_unique, (
        "CostLineID must be unique after Power Query load."
    )


def test_operating_costs_composite_grain_unique(operating_costs_pq):
    assert not operating_costs_pq.duplicated(
        ["FlightOperationKey", "CostCategory", "CostSubcategory",
         "CostDateKey", "SourceDocumentNumber"]
    ).any(), "Composite grain key must be unique after Power Query load."
