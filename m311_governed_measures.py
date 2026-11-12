"""M3.11.6 — Governed Analytical Measure Definitions.

Governed measure calculation functions using actual approved fields.
Only measures supported by existing curated facts and approved definitions.
Undefined measures marked UNDEFINED or OWNER_APPROVAL_REQUIRED.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


# ============================================================================
# Measure Governance Enforcement
# ============================================================================

class GovernanceStatus:
    """Governance status for a measure definition."""
    APPROVED = "approved"
    UNDEFINED = "undefined"
    OWNER_APPROVAL_REQUIRED = "owner_approval_required"
    BLOCKED = "blocked"  # OD-04 blocked, etc.


# ============================================================================
# Measure Definitions (Approved)
# ============================================================================

# Flight Operations Measures (from FactFlightOperations)
FLIGHTS_OPERATED = {
    "measure_id": "FL01",
    "display_name": "Flights Operated",
    "business_definition": "Count of flight operation legs that were operated",
    "formula": "COUNT(*) FILTER (WHERE FlightStatus = 'Operated')",
    "source_fact": "fact_flight_operations",
    "grain": "one row = one flight operation leg",
    "aggregation": "count",
    "unit": "flights",
    "applicable_dimensions": ["dim_airline", "dim_route", "dim_date"],
    "filters": ["FlightStatus = 'Operated'"],
    "null_handling": "exclude_nulls",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "Requires FlightStatus differentiation; does not include cancelled flights",
}

TOTAL_REVENUE_PASSENGERS = {
    "measure_id": "FL02",
    "display_name": "Total Revenue Passengers",
    "business_definition": "Sum of revenue passenger counts across all flight operations",
    "formula": "SUM(RevenuePassengers)",
    "source_fact": "fact_flight_operations",
    "grain": "one row = one flight operation leg",
    "aggregation": "sum",
    "unit": "passengers",
    "applicable_dimensions": ["dim_airline", "dim_route", "dim_date"],
    "filters": None,
    "null_handling": "coalesce_to_zero",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "Includes all passengers regardless of flight status",
}

AVERAGE_DELAY_MINUTES = {
    "measure_id": "FL03",
    "display_name": "Average Delay Minutes",
    "business_definition": "Average departure delay across all flight operations",
    "formula": "AVG(DepartureDelayMinutes)",
    "source_fact": "fact_flight_operations",
    "grain": "one row = one flight operation leg",
    "aggregation": "avg",
    "unit": "minutes",
    "applicable_dimensions": ["dim_airline", "dim_route", "dim_date"],
    "filters": None,
    "null_handling": "exclude_nulls",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "Excludes null delay values; does not include cancelled flights",
}

CANCELLATION_RATE = {
    "measure_id": "FL04",
    "display_name": "Cancellation Rate",
    "business_definition": "Percentage of flight operations that were cancelled",
    "formula": (
        "SUM(CASE WHEN CancellationFlag = 1 THEN 1 ELSE 0 END)::numeric / "
        "NULLIF(COUNT(*), 0) * 100"
    ),
    "source_fact": "fact_flight_operations",
    "grain": "one row = one flight operation leg",
    "aggregation": "ratio",
    "unit": "percent",
    "applicable_dimensions": ["dim_airline", "dim_route", "dim_date"],
    "filters": ["CancellationFlag IS NOT NULL"],
    "null_handling": "exclude_nulls",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "Requires CancellationFlag to be populated; denominator is total flight operations",
}

# Disruption Measures (from FactDisruptions)
DISRUPTIONS_TOTAL = {
    "measure_id": "DS01",
    "display_name": "Total Disruptions",
    "business_definition": "Count of disruption events",
    "formula": "COUNT(*)",
    "source_fact": "fact_disruptions",
    "grain": "one row = one disruption event",
    "aggregation": "count",
    "unit": "events",
    "applicable_dimensions": ["dim_airline", "dim_route", "dim_disruption_type", "dim_date"],
    "filters": None,
    "null_handling": "exclude_nulls",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "None",
}

AVERAGE_DELAY_DISRUPTION = {
    "measure_id": "DS02",
    "display_name": "Average Delay Minutes (Disruption)",
    "business_definition": "Average delay duration across disruption events",
    "formula": "AVG(DelayMinutes)",
    "source_fact": "fact_disruptions",
    "grain": "one row = one disruption event",
    "aggregation": "avg",
    "unit": "minutes",
    "applicable_dimensions": ["dim_airline", "dim_route", "dim_disruption_type", "dim_date"],
    "filters": None,
    "null_handling": "exclude_nulls",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "DelayMinutes may be null for some disruption records",
}

CONTROLLABLE_DISRUPTIONS = {
    "measure_id": "DS03",
    "display_name": "Controllable Disruptions",
    "business_definition": "Count of disruptions where the airline had control, determined from disruption type classification",
    "formula": "COUNT(*) FILTER (WHERE dt.ControllableFlag = TRUE)",
    "source_fact": "fact_disruptions",
    "source_dimension": "dim_disruption_type",
    "grain": "one row = one disruption event",
    "aggregation": "count",
    "unit": "events",
    "applicable_dimensions": ["dim_airline", "dim_route", "dim_disruption_type", "dim_date"],
    "filters": ["dt.ControllableFlag = TRUE"],
    "null_handling": "exclude_nulls",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "ControllableFlag in dim_disruption_type may not be populated for all disruption type records; requires join to dimension",
}

# Customer Feedback Measures (from FactCustomerFeedback)
FEEDBACK_TOTAL = {
    "measure_id": "CF01",
    "display_name": "Total Feedback Events",
    "business_definition": "Count of customer feedback entries",
    "formula": "COUNT(*)",
    "source_fact": "fact_customer_feedback",
    "grain": "one row = one feedback event",
    "aggregation": "count",
    "unit": "feedbacks",
    "applicable_dimensions": ["dim_customer", "dim_airline", "dim_route", "dim_date"],
    "filters": None,
    "null_handling": "exclude_nulls",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "None",
}

AVERAGE_SATISFACTION = {
    "measure_id": "CF02",
    "display_name": "Average Satisfaction Score",
    "business_definition": "Mean satisfaction score across all feedback entries",
    "formula": "AVG(SatisfactionScore)",
    "source_fact": "fact_customer_feedback",
    "grain": "one row = one feedback event",
    "aggregation": "avg",
    "unit": "score (1-5)",
    "applicable_dimensions": ["dim_customer", "dim_airline", "dim_route", "dim_date"],
    "filters": None,
    "null_handling": "exclude_nulls",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "SatisfactionScore range is 1-5; null scores excluded",
}

COMPLAINT_PERCENTAGE = {
    "measure_id": "CF03",
    "display_name": "Complaint Percentage",
    "business_definition": "Percentage of feedback entries classified as complaints",
    "formula": (
        "COUNT(*) FILTER (WHERE FeedbackType = 'Complaint')::numeric / "
        "NULLIF(COUNT(*), 0) * 100"
    ),
    "source_fact": "fact_customer_feedback",
    "grain": "one row = one feedback event",
    "aggregation": "ratio",
    "unit": "percent",
    "applicable_dimensions": ["dim_customer", "dim_airline", "dim_route", "dim_date"],
    "filters": ["FeedbackType IS NOT NULL"],
    "null_handling": "exclude_nulls",
    "governance_status": GovernanceStatus.APPROVED,
    "definition_version": "m311-1.0",
    "known_limitations": "FeedbackType may not be populated for all records",
}


# ============================================================================
# Undefined / Blocked Measures (NOT to be implemented)
# ============================================================================

# These must NOT be implemented per OD-04 and owner decisions

REVENUE_TOTAL = {
    "measure_id": "UNDEF-01",
    "display_name": "Total Revenue",
    "business_definition": "NOT IMPLEMENTED — blocked per OD-04",
    "formula": "NOT IMPLEMENTABLE — FactBookingTransactions blocked",
    "source_fact": "FactBookingTransactions (OD-04 blocked)",
    "grain": "NOT APPLICABLE",
    "aggregation": "NOT APPLICABLE",
    "unit": "NOT APPLICABLE",
    "applicable_dimensions": [],
    "filters": None,
    "null_handling": "NOT APPLICABLE",
    "governance_status": GovernanceStatus.BLOCKED,
    "definition_version": "m311-1.0",
    "known_limitations": "FactBookingTransactions blocked per OD-04 exchange-rate policy",
}

OPERATING_COST_TOTAL = {
    "measure_id": "UNDEF-02",
    "display_name": "Total Operating Costs",
    "business_definition": "NOT IMPLEMENTABLE — blocked per OD-04",
    "formula": "NOT IMPLEMENTABLE — FactOperatingCosts blocked",
    "source_fact": "FactOperatingCosts (OD-04 blocked)",
    "grain": "NOT APPLICABLE",
    "aggregation": "NOT APPLICABLE",
    "unit": "NOT APPLICABLE",
    "applicable_dimensions": [],
    "filters": None,
    "null_handling": "NOT APPLICABLE",
    "governance_status": GovernanceStatus.BLOCKED,
    "definition_version": "m311-1.0",
    "known_limitations": "FactOperatingCosts blocked per OD-04 exchange-rate policy",
}

OTP_THRESHOLD = {
    "measure_id": "UNDEF-03",
    "display_name": "On-Time Performance Threshold",
    "business_definition": "NOT IMPLEMENTABLE — OD-09 OTP threshold unresolved",
    "formula": "NOT IMPLEMENTABLE — OTP threshold unresolved per owner decision",
    "source_fact": "NOT APPLICABLE",
    "grain": "NOT APPLICABLE",
    "aggregation": "NOT APPLICABLE",
    "unit": "NOT APPLICABLE",
    "applicable_dimensions": [],
    "filters": None,
    "null_handling": "NOT APPLICABLE",
    "governance_status": GovernanceStatus.OWNER_APPROVAL_REQUIRED,
    "definition_version": "m311-1.0",
    "known_limitations": "OD-09 OTP threshold owner decision pending",
}

SATISFACTION_SCALE_DEFINITION = {
    "measure_id": "UNDEF-04",
    "display_name": "Satisfaction Score Scale Definition",
    "business_definition": "NOT IMPLEMENTABLE — OD-11 satisfaction score scale unresolved",
    "formula": "NOT IMPLEMENTABLE — OD-11 unresolved per owner decision",
    "source_fact": "fact_customer_feedback",
    "grain": "one row = one feedback event",
    "aggregation": "NOT IMPLEMENTABLE",
    "unit": "NOT APPLICABLE",
    "applicable_dimensions": ["dim_customer"],
    "filters": None,
    "null_handling": "NOT APPLICABLE",
    "governance_status": GovernanceStatus.OWNER_APPROVAL_REQUIRED,
    "definition_version": "m311-1.0",
    "known_limitations": "OD-11 satisfaction score scale owner decision pending",
}

COUPON_ALLOCATION = {
    "measure_id": "UNDEF-05",
    "display_name": "Coupon Allocation Metric",
    "business_definition": "NOT IMPLEMENTABLE — OD-14 coupon allocation unresolved",
    "formula": "NOT IMPLEMENTABLE — OD-14 unresolved per owner decision",
    "source_fact": "NOT APPLICABLE",
    "grain": "NOT APPLICABLE",
    "aggregation": "NOT APPLICABLE",
    "unit": "NOT APPLICABLE",
    "applicable_dimensions": [],
    "filters": None,
    "null_handling": "NOT APPLICABLE",
    "governance_status": GovernanceStatus.OWNER_APPROVAL_REQUIRED,
    "definition_version": "m311-1.0",
    "known_limitations": "OD-14 coupon allocation owner decision pending",
}

SERVICE_RECOVERY_METRIC = {
    "measure_id": "UNDEF-06",
    "display_name": "Service Recovery Metric",
    "business_definition": "NOT IMPLEMENTABLE — OD-17 service-recovery definition unresolved",
    "formula": "NOT IMPLEMENTABLE — OD-17 unresolved per owner decision",
    "source_fact": "fact_customer_feedback",
    "grain": "one row = one feedback event",
    "aggregation": "NOT IMPLEMENTABLE",
    "unit": "NOT APPLICABLE",
    "applicable_dimensions": ["dim_customer"],
    "filters": None,
    "null_handling": "NOT APPLICABLE",
    "governance_status": GovernanceStatus.OWNER_APPROVAL_REQUIRED,
    "definition_version": "m311-1.0",
    "known_limitations": "OD-17 service-recovery definition owner decision pending",
}


# ============================================================================
# Measure Calculation Functions
# ============================================================================


def calculate_flights_operated(fact_df: pd.DataFrame) -> int:
    """Calculate FL01: Flights Operated from FactFlightOperations."""
    if fact_df is None or fact_df.empty:
        return 0
    # Filter to operated flights only
    operated = fact_df[fact_df["FlightStatus"] == "Operated"]
    return int(len(operated))


def calculate_total_revenue_passengers(fact_df: pd.DataFrame) -> int:
    """Calculate FL02: Total Revenue Passengers from FactFlightOperations."""
    if fact_df is None or fact_df.empty:
        return 0
    # Sum revenue passengers, coalesce null to 0
    rev = fact_df["RevenuePassengers"].fillna(0)
    return int(rev.sum())


def calculate_average_delay_minutes(fact_df: pd.DataFrame) -> Optional[float]:
    """Calculate FL03: Average Delay Minutes from FactFlightOperations."""
    if fact_df is None or fact_df.empty:
        return None
    delays = fact_df["DepartureDelayMinutes"].dropna()
    if delays.empty:
        return None
    return float(delays.mean())


def calculate_cancellation_rate(fact_df: pd.DataFrame) -> Optional[float]:
    """Calculate FL04: Cancellation Rate from FactFlightOperations."""
    if fact_df is None or fact_df.empty:
        return None
    total = len(fact_df)
    if total == 0:
        return None
    cancelled = int((fact_df["CancellationFlag"] == 1).sum())
    return round(cancelled / total * 100, 2)


def calculate_disruptions_total(disrupt_df: pd.DataFrame) -> int:
    """Calculate DS01: Total Disruptions from FactDisruptions."""
    if disrupt_df is None or disrupt_df.empty:
        return 0
    return int(len(disrupt_df))


def calculate_average_delay_disruption(disrupt_df: pd.DataFrame) -> Optional[float]:
    """Calculate DS02: Average Delay Minutes (Disruption) from FactDisruptions."""
    if disrupt_df is None or disrupt_df.empty:
        return None
    delays = disrupt_df["DelayMinutes"].dropna()
    if delays.empty:
        return None
    return float(delays.mean())


def calculate_controllable_disruptions(
    disrupt_df: pd.DataFrame, dim_disruption_type: pd.DataFrame
) -> int:
    """Calculate DS03: Controllable Disruptions.

    Determines controllability by joining FactDisruptions with dim_disruption_type
    on DisruptionTypeKey. The ControllableFlag is stored in the dimension, not the fact.
    """
    if disrupt_df is None or disrupt_df.empty or dim_disruption_type is None or dim_disruption_type.empty:
        return 0

    # Join fact to dimension on DisruptionTypeKey
    try:
        joined = disrupt_df.merge(
            dim_disruption_type[["DisruptionTypeKey", "ControllableFlag"]],
            on="DisruptionTypeKey",
            how="left",
        )
        # Fill null ControllableFlag as False (not marked as controllable)
        joined["ControllableFlag"] = joined["ControllableFlag"].fillna(False)
        return int((joined["ControllableFlag"] == True).sum())
    except (KeyError, Exception):
        # If join fails, fall back to counting from fact if column exists
        if "ControllableFlag" in disrupt_df.columns:
            return int((disrupt_df["ControllableFlag"] == True).sum())
        return 0


def calculate_feedback_total(feedback_df: pd.DataFrame) -> int:
    """Calculate CF01: Total Feedback Events from FactCustomerFeedback."""
    if feedback_df is None or feedback_df.empty:
        return 0
    return int(len(feedback_df))


def calculate_average_satisfaction(feedback_df: pd.DataFrame) -> Optional[float]:
    """Calculate CF02: Average Satisfaction Score from FactCustomerFeedback."""
    if feedback_df is None or feedback_df.empty:
        return None
    scores = feedback_df["SatisfactionScore"].dropna()
    if scores.empty:
        return None
    return round(float(scores.mean()), 2)


def calculate_complaint_percentage(feedback_df: pd.DataFrame) -> Optional[float]:
    """Calculate CF03: Complaint Percentage from FactCustomerFeedback."""
    if feedback_df is None or feedback_df.empty:
        return None
    total = len(feedback_df)
    if total == 0:
        return None
    complaints = int((feedback_df["FeedbackType"] == "Complaint").sum())
    return round(complaints / total * 100, 2)


# ============================================================================
# Governance Enforcement
# ============================================================================

def check_governance_status(measure_id: str) -> GovernanceStatus:
    """Check the governance status of a measure ID."""
    # All approved measures
    approved_measures = {
        "FL01", "FL02", "FL03", "FL04",
        "DS01", "DS02", "DS03",
        "CF01", "CF02", "CF03",
    }
    # All blocked measures
    blocked_measures = {"UNDEF-01", "UNDEF-02"}
    # All owner approval required
    owner_required = {"UNDEF-03", "UNDEF-04", "UNDEF-05", "UNDEF-06"}

    if measure_id in approved_measures:
        return GovernanceStatus.APPROVED
    if measure_id in blocked_measures:
        return GovernanceStatus.BLOCKED
    if measure_id in owner_required:
        return GovernanceStatus.OWNER_APPROVAL_REQUIRED
    # Unknown measure
    return GovernanceStatus.UNDEFINED


def is_measure_implementable(measure_id: str) -> bool:
    """Whether a measure can be implemented (not blocked)."""
    status = check_governance_status(measure_id)
    return status in (GovernanceStatus.APPROVED, GovernanceStatus.OWNER_APPROVAL_REQUIRED)


def validate_measure_access(measure_id: str, user_role: str = "analyst") -> dict:
    """Validate whether a user role can access a measure."""
    status = check_governance_status(measure_id)

    validation = {
        "measure_id": measure_id,
        "governance_status": status,
        "access_granted": False,
        "reason": "",
    }

    if status == GovernanceStatus.APPROVED:
        validation["access_granted"] = True
        validation["reason"] = "Approved measure — access granted"
    elif status == GovernanceStatus.OWNER_APPROVAL_REQUIRED:
        validation["reason"] = (
            "Owner approval required — access pending governance sign-off"
        )
    elif status == GovernanceStatus.BLOCKED:
        validation["reason"] = (
            f"Measure blocked — {measure_id}: OD-04 exchange-rate policy restriction"
        )
    elif status == GovernanceStatus.UNDEFINED:
        validation["reason"] = f"Measure undefined — {measure_id}: not in approved measure registry"

    return validation


# ============================================================================
# Semantic Model Metadata Export
# ============================================================================

def export_semantic_model_metadata() -> dict:
    """Export the complete semantic model metadata in machine-readable format."""
    # Collect all approved measures
    all_measures = {}
    all_measures.update(FLIGHTS_OPERATED)
    all_measures.update(TOTAL_REVENUE_PASSENGERS)
    all_measures.update(AVERAGE_DELAY_MINUTES)
    all_measures.update(CANCELLATION_RATE)
    all_measures.update(DISRUPTIONS_TOTAL)
    all_measures.update(AVERAGE_DELAY_DISRUPTION)
    all_measures.update(CONTROLLABLE_DISRUPTIONS)
    all_measures.update(FEEDBACK_TOTAL)
    all_measures.update(AVERAGE_SATISFACTION)
    all_measures.update(COMPLAINT_PERCENTAGE)

    # Collect undefined/blocked measures
    all_undefined = {
        "REVENUE_TOTAL": REVENUE_TOTAL,
        "OPERATING_COST_TOTAL": OPERATING_COST_TOTAL,
        "OTP_THRESHOLD": OTP_THRESHOLD,
        "SATISFACTION_SCALE_DEFINITION": SATISFACTION_SCALE_DEFINITION,
        "COUPON_ALLOCATION": COUPON_ALLOCATION,
        "SERVICE_RECOVERY_METRIC": SERVICE_RECOVERY_METRIC,
    }

    return {
        "semantic_model_version": "m311-1.0",
        "owner": "data_engineering@aerovision360",
        "measures": all_measures,
        "undefined_measures": all_undefined,
        "dimensions": {
            "dim_airline": {"rows": 10, "key": "AirlineKey"},
            "dim_route": {"rows": 320, "key": "RouteKey"},
            "dim_date": {"rows": 761, "key": "DateKey", "role_playing": True},
            "dim_disruption_type": {"rows": 9, "key": "DisruptionTypeKey"},
            "dim_customer": {"rows": 5000, "key": "CustomerKey"},
            "dim_aircraft": {"rows": 440, "key": "AircraftKey"},
            "dim_aircraft_type": {"rows": 12, "key": "AircraftTypeKey"},
            "dim_airport": {"rows": 72, "key": "AirportKey"},
            "dim_booking_channel": {"rows": 7, "key": "BookingChannelKey"},
            "dim_currency": {"rows": 8, "key": "CurrencyKey"},
            "dim_fare_class": {"rows": 8, "key": "FareClassKey"},
        },
        "facts": {
            "fact_flight_operations": {
                "rows": 5000,
                "grain": "one row = one flight operation leg",
                "measures": list(
                    list(FLIGHTS_OPERATED.keys())
                    + list(TOTAL_REVENUE_PASSENGERS.keys())
                    + list(AVERAGE_DELAY_MINUTES.keys())
                    + list(CANCELLATION_RATE.keys())
                ),
            },
            "fact_disruptions": {
                "rows": 1754,
                "grain": "one row = one disruption event",
                "measures": list(
                    list(DISRUPTIONS_TOTAL.keys())
                    + list(AVERAGE_DELAY_DISRUPTION.keys())
                    + list(CONTROLLABLE_DISRUPTIONS.keys())
                ),
            },
            "fact_customer_feedback": {
                "rows": 2500,
                "grain": "one row = one feedback event",
                "measures": list(
                    list(FEEDBACK_TOTAL.keys())
                    + list(AVERAGE_SATISFACTION.keys())
                    + list(COMPLAINT_PERCENTAGE.keys())
                ),
            },
        },
        "od04_restrictions": {
            "blocked_facts": ["FactBookingTransactions", "FactOperatingCosts"],
            "blocked_measure_ids": ["UNDEF-01", "UNDEF-02"],
            "status": "enforced",
        },
        "measure_ownership": {
            "flights_operated": "data_engineering@aerovision360",
            "total_revenue_passengers": "commercial_operations@aerovision360",
            "average_delay_minutes": "operations_management@aerovision360",
            "cancellation_rate": "operations_management@aerovision360",
            "disruptions_total": "operations_management@aerovision360",
            "average_delay_disruption": "operations_management@aerovision360",
            "controllable_disruptions": "operations_management@aerovision360",
            "feedback_total": "customer_experience@aerovision360",
            "average_satisfaction": "customer_experience@aerovision360",
            "complaint_percentage": "customer_experience@aerovision360",
        },
    }


# ============================================================================
# Test Data Loaders
# ============================================================================

def load_fact_flight_operations() -> pd.DataFrame:
    """Load FactFlightOperations parquet for testing."""
    return pd.read_parquet("data/03_curated/fact_flight_operations.parquet")


def load_fact_disruptions() -> pd.DataFrame:
    """Load FactDisruptions parquet for testing."""
    return pd.read_parquet("data/03_curated/fact_disruptions.parquet")


def load_fact_customer_feedback() -> pd.DataFrame:
    """Load FactCustomerFeedback parquet for testing."""
    return pd.read_parquet("data/03_curated/fact_customer_feedback.parquet")


def load_dim_disruption_type() -> pd.DataFrame:
    """Load dim_disruption_type parquet for testing."""
    return pd.read_parquet("data/03_curated/dim_disruption_type.parquet")


def load_dim_airline() -> pd.DataFrame:
    """Load dim_airline parquet for testing."""
    return pd.read_parquet("data/03_curated/dim_airline.parquet")


# ============================================================================
# Pre-computed Results (for verification)
# ============================================================================

# Pre-compute from actual data for test fixtures
_fact_flight = load_fact_flight_operations()
_fact_disrupt = load_fact_disruptions()
_fact_feedback = load_fact_customer_feedback()
_dim_disrupt = load_dim_disruption_type()

FLIGHTS_OPERATED_RESULT = calculate_flights_operated(_fact_flight)
TOTAL_REVENUE_PASSENGERS_RESULT = calculate_total_revenue_passengers(_fact_flight)
AVG_DELAY_RESULT = calculate_average_delay_minutes(_fact_flight)
CANCELLATION_RATE_RESULT = calculate_cancellation_rate(_fact_flight)
DISRUPTIONS_TOTAL_RESULT = calculate_disruptions_total(_fact_disrupt)
AVG_DELAY_DISRUPT_RESULT = calculate_average_delay_disruption(_fact_disrupt)
CONTROLLABLE_DISRUPT_RESULT = calculate_controllable_disruptions(_fact_disrupt, _dim_disrupt)
FEEDBACK_TOTAL_RESULT = calculate_feedback_total(_fact_feedback)
AVG_SATISFACTION_RESULT = calculate_average_satisfaction(_fact_feedback)
COMPLAINT_PERCENTAGE_RESULT = calculate_complaint_percentage(_fact_feedback)

print(f"Pre-computed results:")
print(f"  FL01 Flights Operated: {FLIGHTS_OPERATED_RESULT}")
print(f"  FL02 Total Revenue Passengers: {TOTAL_REVENUE_PASSENGERS_RESULT}")
print(f"  FL03 Avg Delay Minutes: {AVG_DELAY_RESULT}")
print(f"  FL04 Cancellation Rate: {CANCELLATION_RATE_RESULT}%")
print(f"  DS01 Total Disruptions: {DISRUPTIONS_TOTAL_RESULT}")
print(f"  DS02 Avg Delay Disruption: {AVG_DELAY_DISRUPT_RESULT}")
print(f"  DS03 Controllable Disruptions: {CONTROLLABLE_DISRUPT_RESULT}")
print(f"  CF01 Total Feedback: {FEEDBACK_TOTAL_RESULT}")
print(f"  CF02 Avg Satisfaction: {AVG_SATISFACTION_RESULT}")
print(f"  CF03 Complaint Percentage: {COMPLAINT_PERCENTAGE_RESULT}%")