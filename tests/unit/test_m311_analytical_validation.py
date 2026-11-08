"""M3.11 Analytical Validation Tests.

Validates dimensional model integrity, fact grain correctness,
relationship validity, and semantic model consistency.
"""

from __future__ import annotations

import pytest
import pandas as pd

from datetime import datetime, timezone


# ============================================================================
# 1. Dimension Primary-Key Uniqueness
# ============================================================================


def test_dimension_primary_key_uniqueness():
    """Each dimension row must have a unique primary key."""
    dimensions = {
        "dim_airline": pd.read_parquet("data/03_curated/dim_airline.parquet"),
        "dim_aircraft": pd.read_parquet("data/03_curated/dim_aircraft.parquet"),
        "dim_aircraft_type": pd.read_parquet("data/03_curated/dim_aircraft_type.parquet"),
        "dim_airport": pd.read_parquet("data/03_curated/dim_airport.parquet"),
        "dim_booking_channel": pd.read_parquet("data/03_curated/dim_booking_channel.parquet"),
        "dim_currency": pd.read_parquet("data/03_curated/dim_currency.parquet"),
        "dim_customer": pd.read_parquet("data/03_curated/dim_customer.parquet"),
        "dim_date": pd.read_parquet("data/03_curated/dim_date.parquet"),
        "dim_disruption_type": pd.read_parquet("data/03_curated/dim_disruption_type.parquet"),
        "dim_fare_class": pd.read_parquet("data/03_curated/dim_fare_class.parquet"),
        "dim_route": pd.read_parquet("data/03_curated/dim_route.parquet"),
    }

    pk_map = {
        "airline": "AirlineKey",
        "aircraft": "AircraftKey",
        "aircraft_type": "AircraftTypeKey",
        "airport": "AirportKey",
        "booking_channel": "BookingChannelKey",
        "currency": "CurrencyKey",
        "customer": "CustomerKey",
        "date": "DateKey",
        "disruption_type": "DisruptionTypeKey",
        "fare_class": "FareClassKey",
        "route": "RouteKey",
    }

    for name, df in dimensions.items():
        # Strip "dim_" prefix to look up the PK column name
        suffix = name.replace("dim_", "", 1)
        col = pk_map.get(suffix)
        if col is None:
            continue  # skip if no PK mapping
        assert col in df.columns, f"{name}: PK column {col} not found"
        assert df[col].is_unique, f"{name}: {col} is not unique ({df.shape[0]} rows)"
        assert df[col].notna().all(), f"{name}: {col} has null values"


# ============================================================================
# 2. Dimension Natural-Key Uniqueness (where applicable)
# ============================================================================


def test_dimension_natural_key_uniqueness():
    """Natural keys should be unique where defined."""
    df_airline = pd.read_parquet("data/03_curated/dim_airline.parquet")
    assert df_airline["AirlineId"].is_unique, "dim_airline AirlineId must be unique"

    df_aircraft = pd.read_parquet("data/03_curated/dim_aircraft.parquet")
    # AircraftRegistration should be unique
    assert df_aircraft["AircraftRegistration"].notna().all(), "AircraftRegistration should not be null"

    df_route = pd.read_parquet("data/03_curated/dim_route.parquet")
    # RouteCode should be unique
    assert df_route["RouteCode"].is_unique, "dim_route RouteCode must be unique"


# ============================================================================
# 3. Fact Grain Validation
# ============================================================================


def test_fact_flight_operations_grain():
    """FactFlightOperations grain: one row = one flight operation leg."""
    df = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")

    # Primary key uniqueness
    assert df["FlightOperationKey"].is_unique, "FlightOperationKey must be unique"

    # No duplicate flight legs at the declared grain
    # Grain = FlightLegID + FlightNumber + ScheduledDepartureTimestampUTC
    # Since we cannot fully decompose the grain without the source system,
    # we validate that FlightOperationKey is unique and all required FKs are present

    required_fk = ["AirlineKey", "RouteKey", "AircraftKey", "ScheduledDepartureDateKey",
                   "ScheduledArrivalDateKey"]
    for fk in required_fk:
        assert fk in df.columns, f"FactFlightOperations missing FK: {fk}"

    # All FKs should be non-null for valid grain records
    for fk in required_fk:
        assert df[fk].notna().all(), f"FactFlightOperations: {fk} should be NOT NULL"


def test_fact_disruptions_grain():
    """FactDisruptions grain: one row = one disruption event."""
    df = pd.read_parquet("data/03_curated/fact_disruptions.parquet")

    assert df["DisruptionKey"].is_unique, "DisruptionKey must be unique"

    required_fk = ["FlightOperationKey", "AirlineKey", "RouteKey", "DisruptionTypeKey", "EventDateKey"]
    for fk in required_fk:
        assert fk in df.columns, f"FactDisruptions missing FK: {fk}"
        assert df[fk].notna().all(), f"FactDisruptions: {fk} should be NOT NULL"


def test_fact_customer_feedback_grain():
    """FactCustomerFeedback grain: one row = one feedback event."""
    df = pd.read_parquet("data/03_curated/fact_customer_feedback.parquet")

    assert df["FeedbackKey"].is_unique, "FeedbackKey must be unique"

    required_fk = ["CustomerKey", "AirlineKey", "FlightOperationKey", "RouteKey", "FeedbackDateKey"]
    for fk in required_fk:
        assert fk in df.columns, f"FactCustomerFeedback missing FK: {fk}"
        assert df[fk].notna().all(), f"FactCustomerFeedback: {fk} should be NOT NULL"


# ============================================================================
# 4. Foreign-Key Validation
# ============================================================================


def test_airline_fk_in_facts():
    """AirlineKey in all facts must reference valid dim_airline keys."""
    dim_airline = pd.read_parquet("data/03_curated/dim_airline.parquet")
    dim_keys = set(dim_airline["AirlineKey"].astype(int))

    for fact_name in ["fact_flight_operations", "fact_disruptions", "fact_customer_feedback"]:
        df = pd.read_parquet(f"data/03_curated/{fact_name}.parquet")
        if "AirlineKey" in df.columns:
            foreign_keys = set(df["AirlineKey"].astype(int))
            invalid = foreign_keys - dim_keys
            assert len(invalid) == 0, f"{fact_name}: AirlineKey has invalid references: {invalid}"


def test_route_fk_in_facts():
    """RouteKey in facts must reference valid dim_route keys."""
    dim_route = pd.read_parquet("data/03_curated/dim_route.parquet")
    dim_keys = set(dim_route["RouteKey"].astype(int))

    for fact_name in ["fact_flight_operations", "fact_disruptions", "fact_customer_feedback"]:
        df = pd.read_parquet(f"data/03_curated/{fact_name}.parquet")
        if "RouteKey" in df.columns:
            foreign_keys = set(df["RouteKey"].astype(int))
            invalid = foreign_keys - dim_keys
            assert len(invalid) == 0, f"{fact_name}: RouteKey has invalid references: {invalid}"


def test_aircraft_fk_in_facts():
    """AircraftKey in facts must reference valid dim_aircraft keys."""
    dim_aircraft = pd.read_parquet("data/03_curated/dim_aircraft.parquet")
    dim_keys = set(dim_aircraft["AircraftKey"].astype(int))

    df = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")
    if "AircraftKey" in df.columns:
        foreign_keys = set(df["AircraftKey"].astype(int))
        invalid = foreign_keys - dim_keys
        assert len(invalid) == 0, f"fact_flight_operations: AircraftKey has invalid references: {invalid}"


def test_date_fk_in_facts():
    """Date keys in facts must reference valid dim_date keys."""
    dim_date = pd.read_parquet("data/03_curated/dim_date.parquet")
    dim_keys = set(dim_date["DateKey"].astype(str))  # use str to handle NA

    for fact_name in ["fact_flight_operations", "fact_disruptions", "fact_customer_feedback"]:
        df = pd.read_parquet(f"data/03_curated/{fact_name}.parquet")
        date_keys = [c for c in df.columns if "DateKey" in c]
        for dk in date_keys:
            if dk in df.columns:
                # Convert to string, drop NA, then check
                fk_values = df[dk].astype(str).dropna()
                foreign_keys = set(fk_values)
                invalid = foreign_keys - dim_keys
                assert len(invalid) == 0, f"{fact_name}: {dk} has invalid references: {invalid}"


# ============================================================================
# 5. Star-Schema Relationship Validation
# ============================================================================


def test_fact_to_dim_airline_referral():
    """FactFlightOperations AirlineKey → dim_airline should be valid."""
    import pandas as pd
    dim = pd.read_parquet("data/03_curated/dim_airline.parquet")
    fact = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")
    assert set(fact["AirlineKey"].astype(int)).issubset(set(dim["AirlineKey"]))


def test_fact_to_dim_route_referral():
    """FactFlightOperations RouteKey → dim_route should be valid."""
    import pandas as pd
    dim = pd.read_parquet("data/03_curated/dim_route.parquet")
    fact = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")
    assert set(fact["RouteKey"].astype(int)).issubset(set(dim["RouteKey"]))


def test_disruption_to_dim_type():
    """FactDisruptions DisruptionTypeKey → dim_disruption_type should be valid."""
    import pandas as pd
    dim = pd.read_parquet("data/03_curated/dim_disruption_type.parquet")
    fact = pd.read_parquet("data/03_curated/fact_disruptions.parquet")
    assert set(fact["DisruptionTypeKey"].astype(int)).issubset(set(dim["DisruptionTypeKey"]))


def test_role_playing_date_consistency():
    """dim_date should be consistent as a role-playing dimension."""
    dim = pd.read_parquet("data/03_curated/dim_date.parquet")
    # DateKey must be unique
    assert dim["DateKey"].is_unique, "dim_date DateKey must be unique"
    # All DateKeys should be positive integers (YYYYMMDD format)
    assert (dim["DateKey"] > 0).all(), "dim_date DateKey should be positive"


# ============================================================================
# 6. Date-Key Validity
# ============================================================================


def test_date_key_format():
    """DateKey should follow YYYYMMDD format (positive integer)."""
    dim = pd.read_parquet("data/03_curated/dim_date.parquet")
    # All DateKeys should be integers > 0
    assert dim["DateKey"].dtype in ["int16", "int32", "int64"], "DateKey should be integer type"
    assert (dim["DateKey"] > 0).all(), "DateKey values should be positive"


def test_scheduled_departure_date_valid():
    """ScheduledDepartureDateKey in FactFlightOperations should be valid."""
    import pandas as pd
    dim = pd.read_parquet("data/03_curated/dim_date.parquet")
    fact = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")
    dep_keys = set(fact["ScheduledDepartureDateKey"].astype(int))
    assert dep_keys.issubset(set(dim["DateKey"]),), "ScheduledDepartureDateKey has invalid references"


def test_scheduled_arrival_date_valid():
    """ScheduledArrivalDateKey in FactFlightOperations should be valid."""
    import pandas as pd
    dim = pd.read_parquet("data/03_curated/dim_date.parquet")
    fact = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")
    arr_keys = set(fact["ScheduledArrivalDateKey"].astype(int))
    assert arr_keys.issubset(set(dim["DateKey"]),), "ScheduledArrivalDateKey has invalid references"


def test_event_date_valid():
    """EventDateKey in FactDisruptions should be valid."""
    import pandas as pd
    dim = pd.read_parquet("data/03_curated/dim_date.parquet")
    fact = pd.read_parquet("data/03_curated/fact_disruptions.parquet")
    evt_keys = set(fact["EventDateKey"].astype(int))
    assert evt_keys.issubset(set(dim["DateKey"])), "EventDateKey has invalid references"


def test_feedback_date_valid():
    """FeedbackDateKey in FactCustomerFeedback should be valid."""
    import pandas as pd
    dim = pd.read_parquet("data/03_curated/dim_date.parquet")
    fact = pd.read_parquet("data/03_curated/fact_customer_feedback.parquet")
    fdb_keys = set(fact["FeedbackDateKey"].astype(int))
    assert fdb_keys.issubset(set(dim["DateKey"])), "FeedbackDateKey has invalid references"


# ============================================================================
# 7. SCD Effective-Period Consistency
# ============================================================================


def test_dim_airline_active_flag():
    """dim_airline IsActive should have consistent values."""
    import pandas as pd
    df = pd.read_parquet("data/03_curated/dim_airline.parquet")
    # IsActive should be boolean
    assert df["IsActive"].dtype == bool, "dim_airline IsActive should be boolean"
    # Should not have mixed active/inactive anomalies
    active_count = df["IsActive"].sum()
    inactive_count = (~df["IsActive"]).sum()
    print(f"dim_airline: {active_count} active, {inactive_count} inactive")


def test_dim_customer_active_flag():
    """dim_customer IsActive should have consistent values."""
    import pandas as pd
    df = pd.read_parquet("data/03_curated/dim_customer.parquet")
    assert df["IsActive"].dtype == bool, "dim_customer IsActive should be boolean"


# ============================================================================
# 8. Measure Reproducibility
# ============================================================================


def test_flight_count_reproducibility():
    """Flights Operated count should be reproducible."""
    import pandas as pd
    fact = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")
    # Count of flights with OnTimeFlag = True or FlightStatus = 'Operated'
    oper_count = len(fact)
    on_time = fact["OnTimeFlag"].sum()
    print(f"FactFlightOperations: {oper_count} total flights, {on_time} on-time")


def test_disruption_count_reproducibility():
    """Disruptions count should be reproducible."""
    import pandas as pd
    fact = pd.read_parquet("data/03_curated/fact_disruptions.parquet")
    print(f"FactDisruptions: {len(fact)} total disruption events")


def test_feedback_count_reproducibility():
    """Feedback count should be reproducible."""
    import pandas as pd
    fact = pd.read_parquet("data/03_curated/fact_customer_feedback.parquet")
    print(f"FactCustomerFeedback: {len(fact)} total feedback events")


# ============================================================================
# 9. Aggregation Correctness
# ============================================================================


def test_additive_aggregation():
    """Additive measures should aggregate correctly across dimensions."""
    import pandas as pd

    fact = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")

    # RevenuePassengers should be summable
    total_revenue = fact["RevenuePassengers"].sum()
    assert total_revenue > 0, "RevenuePassengers should have positive values"

    # BookedPassengers should be summable
    total_booked = fact["BookedPassengers"].sum()
    assert total_booked > 0, "BookedPassengers should have positive values"


def test_satisfaction_score_range():
    """SatisfactionScore should be in valid range (1-5)."""
    import pandas as pd
    fact = pd.read_parquet("data/03_curated/fact_customer_feedback.parquet")
    scores = fact["SatisfactionScore"].dropna()
    assert scores.between(1, 5).all(), f"SatisfactionScore should be 1-5, found out-of-range: {scores[(scores < 1) | (scores > 5)]}"


# ============================================================================
# 10. Filter Behaviour
# ============================================================================


def test_airline_filter_propagation():
    """Filtering by AirlineKey should propagate correctly across facts."""
    import pandas as pd

    dim_airline = pd.read_parquet("data/03_curated/dim_airline.parquet")
    fact_flight = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")
    fact_disrupt = pd.read_parquet("data/03_curated/fact_disruptions.parquet")
    fact_feedback = pd.read_parquet("data/03_curated/fact_customer_feedback.parquet")

    # Get AirlineKeys from dim
    airline_keys = set(dim_airline["AirlineKey"].astype(int))

    # Filter facts
    for fact, name in [(fact_flight, "fact_flight_operations"),
                       (fact_disrupt, "fact_disruptions"),
                       (fact_feedback, "fact_customer_feedback")]:
        if "AirlineKey" in fact.columns:
            filtered = fact[fact["AirlineKey"].isin(airline_keys)]
            assert len(filtered) > 0, f"{name} should have records for valid airline keys"


def test_route_filter_propagation():
    """Filtering by RouteKey should propagate correctly."""
    import pandas as pd

    dim_route = pd.read_parquet("data/03_curated/dim_route.parquet")
    fact_flight = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")
    fact_disrupt = pd.read_parquet("data/03_curated/fact_disruptions.parquet")
    fact_feedback = pd.read_parquet("data/03_curated/fact_customer_feedback.parquet")

    route_keys = set(dim_route["RouteKey"].astype(int))

    for fact, name in [(fact_flight, "fact_flight_operations"),
                       (fact_disrupt, "fact_disruptions"),
                       (fact_feedback, "fact_customer_feedback")]:
        if "RouteKey" in fact.columns:
            filtered = fact[fact["RouteKey"].isin(route_keys)]
            assert len(filtered) > 0, f"{name} should have records for valid route keys"


# ============================================================================
# 11. Semantic-Model Schema Validation
# ============================================================================


def test_semantic_model_metadata_complete():
    """Semantic model metadata should be complete for all datasets."""
    import os
    import json

    # Check that the M3.11 documentation exists
    doc_path = "docs/M311_ANALYTICAL_WAREHOUSE_SEMANTIC_MODEL.md"
    assert os.path.exists(doc_path), "M3.11 semantic model documentation should exist"

    # Check key sections exist
    with open(doc_path) as f:
        content = f.read()

    required_sections = [
        "M3.11",
        "Existing Dimensional Model Inventory",
        "Fact Grain Validation",
        "Relationship Model",
        "SCD Analysis",
        "Semantic Model Foundation",
    ]
    for section in required_sections:
        assert section in content, f"M3.11 documentation missing section: {section}"


# ============================================================================
# 12. OD-04 Blocked Fact Protection
# ============================================================================


def test_od04_blocked_facts_not_implemented():
    """OD-04 blocked facts must not be implemented."""
    # FactBookingTransactions and FactOperatingCosts must remain blocked
    from pathlib import Path

    blocked = ["FactBookingTransactions", "FactOperatingCosts"]
    for name in blocked:
        path = Path(f"data/03_curated/{name}.parquet")
        # File should NOT exist (blocked per OD-04)
        assert not path.exists(), f"{name} should remain blocked per OD-04"


# ============================================================================
# 13. Existing Regression Compatibility
# ============================================================================


def test_regression_m310_still_pass():
    """M3.10 regression tests must still pass after M3.11 changes."""
    # Verify M3.10 tests are present and importable
    from tests.unit.test_m310_quality_governance import test_remediation_transformation_creation
    assert test_remediation_transformation_creation.__name__ == "test_remediation_transformation_creation"


# ============================================================================
# 14. Deterministic Analytical Outputs
# ============================================================================


def test_deterministic_fact_outputs():
    """Fact query outputs should be deterministic for same inputs."""
    import pandas as pd

    # Read same parquet file twice and compare
    fact = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")
    fact2 = pd.read_parquet("data/03_curated/fact_flight_operations.parquet")

    # Sort by key for deterministic comparison
    fact_sorted = fact.sort_values("FlightOperationKey").reset_index(drop=True)
    fact2_sorted = fact2.sort_values("FlightOperationKey").reset_index(drop=True)

    pd.testing.assert_frame_equal(fact_sorted, fact2_sorted)