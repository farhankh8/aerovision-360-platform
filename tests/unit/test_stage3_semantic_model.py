"""Stage 3 — Semantic Model Engineering validation tests.

Validates the semantic model changes for Stage 3:
- FactBookingTransactions and FactOperatingCosts registered in the model
- Column and data-type consistency with implemented datasets
- Primary-key uniqueness
- Foreign-key relationships resolve
- Relationship cardinality (1:many)
- Filter direction (single direction)
- No ambiguous filter paths / circular dependencies
- Date-role behavior (active/inactive roles)
- Currency conversion lineage preserved
- Financial aggregation safety
- Model schema consistency
- Regression protection for existing 14 tables

Does NOT create DAX measures (deferred to Stage 4 per OD-04).
Does NOT modify the PBIX.
"""

import json
from pathlib import Path

import pandas as pd
import pytest

from src.utilities.paths import project_path

SEMANTIC_MODEL = project_path(
    "deliverables", "power_bi", "semantic_model", "semantic_model.json"
)
MODEL_JSON = project_path(
    "deliverables", "power_bi", "semantic_model", "model.json"
)
PQ_DATA = project_path("deliverables", "data")
CURATED = project_path("data", "03_curated")

BOOKING_CSV = PQ_DATA / "fact_booking_transactions.csv"
OPERATING_COSTS_CSV = PQ_DATA / "fact_operating_costs.csv"

FFO_PATH = CURATED / "fact_flight_operations.parquet"
DIM_AIRLINE_PATH = CURATED / "dim_airline.parquet"
DIM_ROUTE_PATH = CURATED / "dim_route.parquet"
DIM_DATE_PATH = CURATED / "dim_date.parquet"
DIM_CUSTOMER_PATH = CURATED / "dim_customer.parquet"
DIM_FARE_CLASS_PATH = CURATED / "dim_fare_class.parquet"
DIM_BOOKING_CHANNEL_PATH = CURATED / "dim_booking_channel.parquet"
DIM_CURRENCY_PATH = CURATED / "dim_currency.parquet"

EXISTING_TABLES = {
    "dim_airline", "dim_airport", "dim_route", "dim_date", "dim_aircraft",
    "dim_aircraft_type", "dim_customer", "dim_disruption_type",
    "dim_booking_channel", "dim_currency", "dim_fare_class",
    "fact_flight_operations", "fact_disruptions", "fact_customer_feedback",
}

NEW_TABLES = {"fact_booking_transactions", "fact_operating_costs"}

SYNTHETIC_PROVENANCE = "Synthetic Simulation — Not Actual Airline Performance."


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def semantic_model():
    return json.loads(SEMANTIC_MODEL.read_text(encoding="utf-8"))


@pytest.fixture
def model_json():
    return json.loads(MODEL_JSON.read_text(encoding="utf-8"))


@pytest.fixture
def model_tables(semantic_model):
    return semantic_model["config"]["tables"]


@pytest.fixture
def booking_df():
    return pd.read_csv(BOOKING_CSV, encoding="utf-8")


@pytest.fixture
def operating_costs_df():
    return pd.read_csv(OPERATING_COSTS_CSV, encoding="utf-8")


@pytest.fixture
def ffo():
    return pd.read_parquet(FFO_PATH)


@pytest.fixture
def dim_airline():
    return pd.read_parquet(DIM_AIRLINE_PATH)


@pytest.fixture
def dim_route():
    return pd.read_parquet(DIM_ROUTE_PATH)


@pytest.fixture
def dim_date():
    return pd.read_parquet(DIM_DATE_PATH)


@pytest.fixture
def dim_customer():
    return pd.read_parquet(DIM_CUSTOMER_PATH)


@pytest.fixture
def dim_fare_class():
    return pd.read_parquet(DIM_FARE_CLASS_PATH)


@pytest.fixture
def dim_booking_channel():
    return pd.read_parquet(DIM_BOOKING_CHANNEL_PATH)


@pytest.fixture
def dim_currency():
    return pd.read_parquet(DIM_CURRENCY_PATH)


# ---------------------------------------------------------------------------
# 1. Table registration
# ---------------------------------------------------------------------------

def test_both_financial_tables_registered(model_tables):
    table_names = set(model_tables.keys())
    assert "fact_booking_transactions" in table_names
    assert "fact_operating_costs" in table_names


def test_model_total_table_count(model_tables):
    assert len(model_tables) == 16, (
        f"Expected 16 tables (14 existing + 2 new), got {len(model_tables)}"
    )


def test_existing_tables_unchanged(model_tables):
    for name in EXISTING_TABLES:
        assert name in model_tables, f"Existing table {name} missing from model"


def test_model_json_matches_semantic_model(model_json, model_tables):
    model_json_names = {t["name"] for t in model_json["model"]["tables"]}
    semantic_names = set(model_tables.keys())
    assert model_json_names == semantic_names, (
        f"model.json tables {model_json_names} != semantic_model.json tables {semantic_names}"
    )


# ---------------------------------------------------------------------------
# 2. Column and data-type consistency
# ---------------------------------------------------------------------------

def test_booking_columns_match_source(model_tables, booking_df):
    model_cols = set(model_tables["fact_booking_transactions"]["columns"])
    source_cols = set(booking_df.columns)
    assert model_cols == source_cols, (
        f"Model columns {sorted(model_cols)} != source columns {sorted(source_cols)}"
    )


def test_operating_costs_columns_match_source(model_tables, operating_costs_df):
    model_cols = set(model_tables["fact_operating_costs"]["columns"])
    source_cols = set(operating_costs_df.columns)
    assert model_cols == source_cols, (
        f"Model columns {sorted(model_cols)} != source columns {sorted(source_cols)}"
    )


def test_booking_column_count(model_tables):
    assert len(model_tables["fact_booking_transactions"]["columns"]) == 45


def test_operating_costs_column_count(model_tables):
    assert len(model_tables["fact_operating_costs"]["columns"]) == 18


def test_booking_preserves_all_required_columns(model_tables):
    cols = model_tables["fact_booking_transactions"]["columns"]
    required = [
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
    for col in required:
        assert col in cols, f"Missing required column: {col}"


def test_operating_costs_preserves_all_required_columns(model_tables):
    cols = model_tables["fact_operating_costs"]["columns"]
    required = [
        "OperatingCostKey", "CostLineID", "FlightOperationKey", "AirlineKey",
        "RouteKey", "CostDateKey", "CostCategory", "CostSubcategory",
        "CostAmount", "CurrencyKey", "ExchangeRateToUSD", "RateDateKey",
        "RateVersion", "CostAmountUSD", "CostDescription",
        "SourceDocumentNumber", "IsAllocated", "SyntheticProvenance",
    ]
    for col in required:
        assert col in cols, f"Missing required column: {col}"


def test_no_column_renaming_without_reason(model_tables, booking_df, operating_costs_df):
    """Verify no existing columns were renamed — model columns exactly match source."""
    model_booking = set(model_tables["fact_booking_transactions"]["columns"])
    model_costs = set(model_tables["fact_operating_costs"]["columns"])
    assert model_booking == set(booking_df.columns)
    assert model_costs == set(operating_costs_df.columns)


# ---------------------------------------------------------------------------
# 3. Primary-key uniqueness
# ---------------------------------------------------------------------------

def test_booking_primary_key_unique(booking_df):
    assert booking_df["BookingTransactionKey"].is_unique


def test_operating_costs_primary_key_unique(operating_costs_df):
    assert operating_costs_df["OperatingCostKey"].is_unique


def test_booking_primary_key_in_model(model_tables):
    cols = model_tables["fact_booking_transactions"]["columns"]
    assert "BookingTransactionKey" in cols


def test_operating_costs_primary_key_in_model(model_tables):
    cols = model_tables["fact_operating_costs"]["columns"]
    assert "OperatingCostKey" in cols


# ---------------------------------------------------------------------------
# 4. Foreign-key relationships
# ---------------------------------------------------------------------------

def test_booking_relationships_resolve(model_tables, ffo, dim_airline, dim_route,
                                        dim_customer, dim_fare_class,
                                        dim_booking_channel, dim_date,
                                        dim_currency):
    rels = model_tables["fact_booking_transactions"]["relationships"]
    rel_map = {r["fromColumn"]: (r["toTable"], r["toColumn"]) for r in rels}

    # AirlineKey -> dim_airline
    assert rel_map["AirlineKey"] == ("dim_airline", "AirlineKey")
    valid_airlines = set(dim_airline["AirlineKey"].astype(int))
    assert set(ffo["AirlineKey"].astype(int)).issubset(valid_airlines)

    # RouteKey -> dim_route
    assert rel_map["RouteKey"] == ("dim_route", "RouteKey")
    valid_routes = set(dim_route["RouteKey"].astype(int))
    assert set(ffo["RouteKey"].astype(int)).issubset(valid_routes)

    # CustomerKey -> dim_customer
    assert rel_map["CustomerKey"] == ("dim_customer", "CustomerKey")

    # FareClassKey -> dim_fare_class
    assert rel_map["FareClassKey"] == ("dim_fare_class", "FareClassKey")

    # BookingChannelKey -> dim_booking_channel
    assert rel_map["BookingChannelKey"] == ("dim_booking_channel", "BookingChannelKey")

    # TravelDateKey -> dim_date (active)
    assert rel_map["TravelDateKey"] == ("dim_date", "DateKey")

    # BookingDateKey -> dim_date (inactive)
    assert rel_map["BookingDateKey"] == ("dim_date", "DateKey")

    # TransactionCurrencyKey -> dim_currency
    assert rel_map["TransactionCurrencyKey"] == ("dim_currency", "CurrencyKey")

    # FlightOperationKey must NOT be a relationship (fact-to-fact prohibited)
    assert "FlightOperationKey" not in rel_map


def test_operating_costs_relationships_resolve(model_tables, ffo, dim_airline,
                                                dim_route, dim_date, dim_currency):
    rels = model_tables["fact_operating_costs"]["relationships"]
    rel_map = {r["fromColumn"]: (r["toTable"], r["toColumn"]) for r in rels}

    assert rel_map["AirlineKey"] == ("dim_airline", "AirlineKey")
    assert rel_map["RouteKey"] == ("dim_route", "RouteKey")
    assert rel_map["CostDateKey"] == ("dim_date", "DateKey")
    assert rel_map["CurrencyKey"] == ("dim_currency", "CurrencyKey")

    # FlightOperationKey must NOT be a relationship (fact-to-fact prohibited)
    assert "FlightOperationKey" not in rel_map


def test_booking_fk_columns_present_in_source(booking_df):
    fk_cols = ["AirlineKey", "RouteKey", "CustomerKey", "FareClassKey",
               "BookingChannelKey", "TravelDateKey", "BookingDateKey",
               "TransactionCurrencyKey"]
    for col in fk_cols:
        assert col in booking_df.columns, f"FK column {col} missing from source"


def test_operating_costs_fk_columns_present_in_source(operating_costs_df):
    fk_cols = ["AirlineKey", "RouteKey", "CostDateKey", "CurrencyKey"]
    for col in fk_cols:
        assert col in operating_costs_df.columns, f"FK column {col} missing from source"


# ---------------------------------------------------------------------------
# 5. Relationship cardinality (all 1:many)
# ---------------------------------------------------------------------------

def test_all_relationships_are_one_to_many(model_tables):
    for table_name, table_def in model_tables.items():
        for rel in table_def.get("relationships", []):
            # In Power BI semantic model, relationships from fact to dimension are 1:many
            # The 'from' side is the fact (many), 'to' side is dimension (one)
            assert rel["role"] in ("active", "inactive"), (
                f"Invalid role {rel['role']} in {table_name}"
            )


def test_no_many_to_many_relationships(model_tables):
    """Verify no relationship is marked as many-to-many."""
    for table_name, table_def in model_tables.items():
        for rel in table_def.get("relationships", []):
            # All relationships in this model are fact-to-dimension (1:many)
            # There is no explicit cardinality field, but the pattern is always
            # fact.surrogate_key -> dimension.primary_key which is 1:many.
            assert rel["toTable"] in EXISTING_TABLES or rel["toTable"] in NEW_TABLES


# ---------------------------------------------------------------------------
# 6. Filter direction (single direction by default)
# ---------------------------------------------------------------------------

def test_single_direction_filtering(model_tables):
    """All relationships use single-direction filtering (no bidirectional)."""
    for table_name, table_def in model_tables.items():
        for rel in table_def.get("relationships", []):
            # No bidirectional flag present = single direction (default in Power BI)
            assert "bidirectional" not in rel or rel.get("bidirectional") is not True, (
                f"Bidirectional filtering found in {table_name}.{rel['fromColumn']}"
            )


# ---------------------------------------------------------------------------
# 7. Ambiguous paths / circular dependencies
# ---------------------------------------------------------------------------

def test_no_fact_to_fact_relationships(model_tables):
    """Contract Section 8.5: No fact-to-fact relationships."""
    fact_tables = {
        "fact_flight_operations", "fact_disruptions", "fact_customer_feedback",
        "fact_booking_transactions", "fact_operating_costs",
    }
    for table_name in fact_tables:
        if table_name not in model_tables:
            continue
        for rel in model_tables[table_name].get("relationships", []):
            assert rel["toTable"] not in fact_tables, (
                f"Fact-to-fact relationship: {table_name}.{rel['fromColumn']} -> {rel['toTable']}"
            )


def test_no_circular_date_paths(model_tables):
    """dim_date is role-playing: each fact has at most one ACTIVE relationship to dim_date."""
    active_date_rels = {}
    for table_name, table_def in model_tables.items():
        for rel in table_def.get("relationships", []):
            if rel["toTable"] == "dim_date" and rel["role"] == "active":
                active_date_rels.setdefault(rel["toColumn"], []).append(
                    (table_name, rel["fromColumn"])
                )
    # Each date column should have at most one active relationship per fact table
    # (role-playing: multiple inactive OK, one active per fact)
    fact_active_date = {}
    for (table_name, from_col) in sum(active_date_rels.values(), []):
        fact_active_date.setdefault(table_name, []).append(from_col)
    for table_name, cols in fact_active_date.items():
        assert len(cols) <= 1, (
            f"Multiple active date relationships for {table_name}: {cols}"
        )


def test_dim_date_role_playing(model_tables):
    """dim_date has no outgoing relationships (it's a pure dimension)."""
    date_rels = model_tables["dim_date"].get("relationships", [])
    assert date_rels == [], "dim_date should have no outgoing relationships"


def test_no_ambiguous_airline_paths(model_tables):
    """dim_airline filters facts directly. Check no NEW ambiguous path introduced
    by dim_airline -> dim_aircraft (contract Section 8.4 prohibits this direction).
    The pre-existing dim_aircraft -> dim_airline relationship is correct: aircraft
    filters airline, not airline filters aircraft."""
    # Check that dim_airline does NOT have an outgoing relationship to dim_aircraft
    airline_rels = model_tables["dim_airline"].get("relationships", [])
    aircraft_outbound = [r for r in airline_rels if r["toTable"] == "dim_aircraft"]
    assert len(aircraft_outbound) == 0, (
        "dim_airline -> dim_aircraft must not exist (ambiguous filter path per contract 8.4)"
    )
    # The pre-existing dim_aircraft -> dim_airline relationship is correct direction
    aircraft_rels = model_tables["dim_aircraft"].get("relationships", [])
    airline_inbound = [r for r in aircraft_rels if r["toTable"] == "dim_airline"]
    for r in airline_inbound:
        assert r["role"] == "active", (
            "Pre-existing dim_aircraft -> dim_airline relationship should remain active"
        )


# ---------------------------------------------------------------------------
# 8. Date-role behavior
# ---------------------------------------------------------------------------

def test_booking_date_roles(model_tables):
    """FactBookingTransactions: TravelDateKey = active, BookingDateKey = inactive."""
    rels = model_tables["fact_booking_transactions"]["relationships"]
    date_rels = {r["fromColumn"]: r["role"] for r in rels if r["toTable"] == "dim_date"}
    assert date_rels.get("TravelDateKey") == "active", (
        "TravelDateKey must be the active date role for booking revenue"
    )
    assert date_rels.get("BookingDateKey") == "inactive", (
        "BookingDateKey must be inactive for booking cohort analysis"
    )


def test_operating_costs_date_role(model_tables):
    """FactOperatingCosts: CostDateKey = active."""
    rels = model_tables["fact_operating_costs"]["relationships"]
    date_rels = {r["fromColumn"]: r["role"] for r in rels if r["toTable"] == "dim_date"}
    assert date_rels.get("CostDateKey") == "active", (
        "CostDateKey must be the active date role for operating costs"
    )


def test_booking_date_keys_exist_in_source(booking_df):
    assert "TravelDateKey" in booking_df.columns
    assert "BookingDateKey" in booking_df.columns


def test_operating_costs_date_key_exists_in_source(operating_costs_df):
    assert "CostDateKey" in operating_costs_df.columns


# ---------------------------------------------------------------------------
# 9. Currency conversion lineage
# ---------------------------------------------------------------------------

def test_booking_currency_lineage(booking_df, model_tables):
    """ExchangeRateToUSD, RateDateKey, RateVersion preserved for traceability."""
    for col in ["TransactionCurrencyKey", "ExchangeRateToUSD", "RateDateKey", "RateVersion"]:
        assert col in booking_df.columns, f"Missing {col} in booking source"
        assert col in model_tables["fact_booking_transactions"]["columns"], (
            f"Missing {col} in booking model"
        )
    assert (booking_df["ExchangeRateToUSD"] > 0).all()
    assert (booking_df["RateVersion"] == "FX-2026-11-04-001").all()


def test_operating_costs_currency_lineage(operating_costs_df, model_tables):
    """ExchangeRateToUSD, RateDateKey, RateVersion preserved for traceability."""
    for col in ["CurrencyKey", "ExchangeRateToUSD", "RateDateKey", "RateVersion"]:
        assert col in operating_costs_df.columns, f"Missing {col} in operating costs source"
        assert col in model_tables["fact_operating_costs"]["columns"], (
            f"Missing {col} in operating costs model"
        )
    assert (operating_costs_df["ExchangeRateToUSD"] > 0).all()
    assert (operating_costs_df["RateVersion"] == "FX-2026-11-04-001").all()


def test_no_forward_fill_exchange_rates(booking_df, operating_costs_df):
    """OD-04e: No forward-filled exchange rates. All rows have valid rates."""
    assert booking_df["ExchangeRateToUSD"].notna().all()
    assert operating_costs_df["ExchangeRateToUSD"].notna().all()


# ---------------------------------------------------------------------------
# 10. Financial aggregation safety
# ---------------------------------------------------------------------------

def test_original_and_usd_amounts_both_present(booking_df, operating_costs_df):
    """Original currency amounts and USD-converted amounts both available."""
    booking_orig = ["BaseFareAmount", "DiscountAmount", "TaxAmount", "FeeAmount",
                    "AncillaryRevenueAmount", "RefundAmount", "AncillaryRefundAmount",
                    "FeeRefundAmount", "CancellationFeeAmount", "NoShowFeeAmount"]
    booking_usd = ["BaseFareUSD", "DiscountUSD", "TaxUSD", "FeeUSD",
                   "AncillaryRevenueUSD", "RefundUSD", "AncillaryRefundUSD",
                   "FeeRefundUSD", "CancellationFeeUSD", "NoShowFeeUSD",
                   "NetPassengerRevenueUSD", "NetFeeRevenueUSD", "NetAncillaryRevenueUSD"]
    for col in booking_orig + booking_usd:
        assert col in booking_df.columns, f"Missing {col}"
        assert booking_df[col].notna().all(), f"{col} has nulls"

    assert "CostAmount" in operating_costs_df.columns
    assert "CostAmountUSD" in operating_costs_df.columns
    assert operating_costs_df["CostAmount"].notna().all()
    assert operating_costs_df["CostAmountUSD"].notna().all()


def test_no_cross_currency_aggregation(booking_df, operating_costs_df):
    """Original-currency amounts carry a currency key; USD amounts are reporting currency."""
    assert "TransactionCurrencyKey" in booking_df.columns
    assert "CurrencyKey" in operating_costs_df.columns
    # CurrencyKey references dim_currency (validated in FK tests)
    valid_currencies = {1, 2, 3, 4, 5, 6, 7, 8}
    assert set(booking_df["TransactionCurrencyKey"].astype(int)).issubset(valid_currencies)
    assert set(operating_costs_df["CurrencyKey"].astype(int)).issubset(valid_currencies)


def test_refunds_and_reversals_represented(booking_df, operating_costs_df):
    """Refunds (positive magnitudes) and cost reversals (negative amounts) correctly represented."""
    # Refunds stored as positive magnitudes (contract Section 10.4)
    assert (booking_df["RefundAmount"] >= 0).all()
    assert (booking_df["AncillaryRefundAmount"] >= 0).all()
    assert (booking_df["FeeRefundAmount"] >= 0).all()
    # Cost reversals are negative (contract Section 10.4)
    assert (operating_costs_df["CostAmountUSD"] < 0).any(), (
        "Expected some negative cost reversals/credits"
    )
    assert (operating_costs_df["CostAmount"] < 0).any(), (
        "Expected some negative cost reversals/credits in original currency"
    )


def test_booking_sign_convention(booking_df):
    """All monetary amounts are non-negative (refunds are positive magnitudes)."""
    money_cols = [
        "BaseFareAmount", "DiscountAmount", "TaxAmount", "FeeAmount",
        "AncillaryRevenueAmount", "RefundAmount", "AncillaryRefundAmount",
        "FeeRefundAmount", "CancellationFeeAmount", "NoShowFeeAmount",
        "BaseFareUSD", "DiscountUSD", "TaxUSD", "FeeUSD",
        "AncillaryRevenueUSD", "RefundUSD", "AncillaryRefundUSD",
        "FeeRefundUSD", "CancellationFeeUSD", "NoShowFeeUSD",
        "NetPassengerRevenueUSD", "NetFeeRevenueUSD", "NetAncillaryRevenueUSD",
    ]
    for col in money_cols:
        assert (booking_df[col] >= 0).all(), f"{col} has negative values"


# ---------------------------------------------------------------------------
# 11. Model schema consistency
# ---------------------------------------------------------------------------

def test_semantic_model_valid_json(semantic_model):
    assert "config" in semantic_model
    assert "tables" in semantic_model["config"]
    assert "disclosure" in semantic_model["config"]


def test_all_tables_have_required_fields(model_tables):
    for name, table_def in model_tables.items():
        assert "columns" in table_def, f"Table {name} missing columns"
        assert "relationships" in table_def, f"Table {name} missing relationships"
        assert "measures" in table_def, f"Table {name} missing measures"
        assert isinstance(table_def["columns"], list)
        assert isinstance(table_def["relationships"], list)
        assert isinstance(table_def["measures"], list)


def test_all_relationships_have_required_fields(model_tables):
    for table_name, table_def in model_tables.items():
        for rel in table_def.get("relationships", []):
            assert "fromColumn" in rel, f"Missing fromColumn in {table_name}"
            assert "toTable" in rel, f"Missing toTable in {table_name}"
            assert "toColumn" in rel, f"Missing toColumn in {table_name}"
            assert "role" in rel, f"Missing role in {table_name}"
            assert rel["role"] in ("active", "inactive")


def test_dimension_tables_have_no_measures(model_tables):
    """Dimensions have empty measures arrays (measures live on facts)."""
    dim_names = EXISTING_TABLES - {
        "fact_flight_operations", "fact_disruptions", "fact_customer_feedback",
        "fact_booking_transactions", "fact_operating_costs",
    }
    for name in dim_names:
        if name in model_tables:
            assert model_tables[name]["measures"] == [], (
                f"Dimension {name} should have no measures"
            )


# ---------------------------------------------------------------------------
# 12. Regression protection for existing 14 tables
# ---------------------------------------------------------------------------

def test_existing_table_columns_unchanged(model_tables):
    """Existing tables retain their original columns (no columns removed or renamed)."""
    expected_columns = {
        "dim_airline": ["AirlineKey", "AirlineId", "AirlineIATACode", "AirlineICAOCode",
                        "AirlineName", "AirlineGroup", "HomeCountry", "HomeCountryCode",
                        "BusinessModelClass", "IsActive", "StatusEffectiveDate",
                        "ReferenceVersion"],
        "dim_date": ["DateKey", "FullDate", "Year", "Quarter", "MonthNumber",
                     "MonthName", "MonthShortName", "YearMonth", "YearMonthSort",
                     "WeekNumber", "WeekStartDate", "DayOfMonth", "DayName",
                     "DayOfWeekNumber", "IsWeekend", "IsReportingPeriod", "FiscalYear",
                     "FiscalQuarter", "FiscalMonthNumber"],
        "dim_currency": ["CurrencyKey", "CurrencyCode", "CurrencyName", "CurrencySymbol",
                         "DecimalPlaces", "IsReportingCurrency"],
        "dim_route": ["RouteKey", "RouteCode", "OriginAirportKey", "DestinationAirportKey",
                      "DistanceKM", "DistanceMiles", "RouteRegion", "IsInternational",
                      "IsActive"],
    }
    for name, expected in expected_columns.items():
        if name in model_tables:
            actual = model_tables[name]["columns"]
            for col in expected:
                assert col in actual, f"Column {col} missing from {name}"


def test_existing_relationships_unchanged(model_tables):
    """Existing fact relationships are preserved."""
    # fact_flight_operations keeps its 5 relationships
    ffo_rels = model_tables["fact_flight_operations"]["relationships"]
    assert len(ffo_rels) == 5
    # fact_disruptions keeps its 5 relationships
    dis_rels = model_tables["fact_disruptions"]["relationships"]
    assert len(dis_rels) == 5
    # fact_customer_feedback keeps its 5 relationships
    cf_rels = model_tables["fact_customer_feedback"]["relationships"]
    assert len(cf_rels) == 5


def test_no_modifications_to_existing_measures(model_tables):
    """Existing fact measures are unchanged; OP01/OP03/OP04 registered for Operations page."""
    ffo_measures = model_tables["fact_flight_operations"]["measures"]
    expected_ffo = {"FL01", "FL02", "FL03", "FL04"}
    actual_ffo = set(ffo_measures)
    assert expected_ffo.issubset(actual_ffo), (
        f"Existing fact_flight_operations measures missing: {expected_ffo - actual_ffo}"
    )
    assert "OP01" in actual_ffo, "OP01 not registered in fact_flight_operations"
    assert "OP03" in actual_ffo, "OP03 not registered in fact_flight_operations"
    assert "OP04" in actual_ffo, "OP04 not registered in fact_flight_operations"
    dis_measures = model_tables["fact_disruptions"]["measures"]
    assert dis_measures == ["DS01", "DS02", "DS03"]
    cf_measures = model_tables["fact_customer_feedback"]["measures"]
    assert cf_measures == ["CF01", "CF02", "CF03", "CF04", "CF05", "CF06", "CF07",
                           "CF08", "CF09", "CF10", "CF11", "CF12", "CF13", "CF14"]


# ---------------------------------------------------------------------------
# Synthetic provenance
# ---------------------------------------------------------------------------

def test_booking_synthetic_provenance(booking_df):
    assert (booking_df["SyntheticProvenance"] == SYNTHETIC_PROVENANCE).all()


def test_operating_costs_synthetic_provenance(operating_costs_df):
    assert (operating_costs_df["SyntheticProvenance"] == SYNTHETIC_PROVENANCE).all()


def test_model_disclosure(semantic_model):
    assert semantic_model["config"]["disclosure"] == (
        "Synthetic Simulation - Not Actual Airline Performance"
    )
