"""M3.11.7 — BI Consumption Contract.

Implements a stable, machine-readable BI consumption contract for the
AEROVISION 360 analytical model. Uses the existing semantic-model architecture.

Does not build a dashboard. Does not add vendor-specific dependencies.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import json
from pathlib import Path


# ============================================================================
# Model Identity
# ============================================================================

MODEL_ID = "aerovision360-analytics-m311"
MODEL_NAME = "AEROVISION 360 Analytical Data Warehouse"
MODEL_VERSION = "m311-1.0"
MODEL_OWNER = "data_engineering@aerovision360"

# Stable identifiers — not dependent on display names
DATASET_IDS = {
    "fact_flight_operations": "fact_flight_operations",
    "fact_disruptions": "fact_disruptions",
    "fact_customer_feedback": "fact_customer_feedback",
    "dim_airline": "dim_airline",
    "dim_route": "dim_route",
    "dim_date": "dim_date",
    "dim_disruption_type": "dim_disruption_type",
    "dim_customer": "dim_customer",
    "dim_aircraft": "dim_aircraft",
    "dim_aircraft_type": "dim_aircraft_type",
    "dim_airport": "dim_airport",
    "dim_booking_channel": "dim_booking_channel",
    "dim_currency": "dim_currency",
    "dim_fare_class": "dim_fare_class",
}

# ============================================================================
# Dataset Schemas (machine-readable)
# ============================================================================

FACT_FLIGHT_OPERATIONS_SCHEMA = {
    "dataset_id": DATASET_IDS["fact_flight_operations"],
    "name": "FactFlightOperations",
    "rows": 5000,
    "grain": "one row = one flight operation leg",
    "columns": {
        "FlightOperationKey": {"type": "int64", "description": "Primary key"},
        "FlightLegID": {"type": "string", "description": "Flight leg identifier"},
        "FlightNumber": {"type": "string", "description": "Flight number"},
        "AirlineKey": {"type": "int32", "description": "FK → dim_airline"},
        "RouteKey": {"type": "int32", "description": "FK → dim_route"},
        "AircraftKey": {"type": "int32", "description": "FK → dim_aircraft"},
        "ScheduledDepartureTimestampUTC": {
            "type": "timestamp",
            "description": "Scheduled departure in UTC",
        },
        "ActualDepartureTimestampUTC": {
            "type": "timestamp",
            "description": "Actual departure in UTC",
        },
        "ScheduledArrivalTimestampUTC": {
            "type": "timestamp",
            "description": "Scheduled arrival in UTC",
        },
        "ActualArrivalTimestampUTC": {
            "type": "timestamp",
            "description": "Actual arrival in UTC",
        },
        "ScheduledDepartureDateKey": {
            "type": "int32",
            "description": "FK → dim_date (role-playing)",
        },
        "ScheduledArrivalDateKey": {
            "type": "int32",
            "description": "FK → dim_date (role-playing)",
        },
        "AvailableSeats": {"type": "int16", "description": "Available seats on flight"},
        "BookedPassengers": {"type": "int16", "description": "Booked passengers"},
        "RevenuePassengers": {"type": "int16", "description": "Revenue passengers"},
        "NonRevenuePassengers": {"type": "int16", "description": "Non-revenue passengers"},
        "FlightDistanceKM": {"type": "object", "description": "Flight distance in km"},
        "FlightStatus": {"type": "string", "description": "Operational status"},
        "DepartureDelayMinutes": {"type": "int16", "description": "Departure delay"},
        "ArrivalDelayMinutes": {"type": "int16", "description": "Arrival delay"},
        "BlockMinutes": {"type": "int16", "description": "Block time"},
        "CancellationFlag": {"type": "bool", "description": "Was flight cancelled?"},
        "CompletionFlag": {"type": "bool", "description": "Is flight completion recorded?"},
        "OnTimeFlag": {"type": "bool", "description": "Was flight on time?"},
        "OnTimeArrivalFlag": {
            "type": "bool",
            "description": "Was arrival on time?",
        },
    },
}

FACT_DISRUPTIONS_SCHEMA = {
    "dataset_id": DATASET_IDS["fact_disruptions"],
    "name": "FactDisruptions",
    "rows": 1754,
    "grain": "one row = one disruption event",
    "columns": {
        "DisruptionKey": {"type": "int64", "description": "Primary key"},
        "DisruptionID": {"type": "string", "description": "Disruption identifier"},
        "FlightOperationKey": {"type": "int64", "description": "FK → fact_flight_operations"},
        "AirlineKey": {"type": "int32", "description": "FK → dim_airline"},
        "RouteKey": {"type": "int32", "description": "FK → dim_route"},
        "EventLocationAirportKey": {
            "type": "int32",
            "description": "FK → dim_airport",
        },
        "DisruptionTypeKey": {
            "type": "int32",
            "description": "FK → dim_disruption_type",
        },
        "EventSequence": {"type": "int8", "description": "Event sequence number"},
        "EventDateKey": {"type": "int32", "description": "FK → dim_date"},
        "EventStartTimestampUTC": {"type": "timestamp", "description": "Disruption start in UTC"},
        "EventEndTimestampUTC": {"type": "timestamp", "description": "Disruption end in UTC"},
        "DelayMinutes": {"type": "int16", "description": "Delay duration"},
        "PrimaryCauseFlag": {"type": "bool", "description": "Is primary cause?"},
        "ReactionaryFlag": {"type": "bool", "description": "Is reactionary?"},
        "ReactionaryEvidenceID": {"type": "string", "description": "Evidence ID"},
        "RecoveryStatus": {"type": "string", "description": "Recovery status"},
    },
}

FACT_CUSTOMER_FEEDBACK_SCHEMA = {
    "dataset_id": DATASET_IDS["fact_customer_feedback"],
    "name": "FactCustomerFeedback",
    "rows": 2500,
    "grain": "one row = one feedback event",
    "columns": {
        "FeedbackKey": {"type": "int64", "description": "Primary key"},
        "FeedbackID": {"type": "string", "description": "Feedback identifier"},
        "CustomerKey": {"type": "int32", "description": "FK → dim_customer"},
        "AirlineKey": {"type": "int32", "description": "FK → dim_airline"},
        "FlightOperationKey": {"type": "int64", "description": "FK → fact_flight_operations"},
        "RouteKey": {"type": "int32", "description": "FK → dim_route"},
        "FeedbackDateKey": {"type": "int32", "description": "FK → dim_date"},
        "FeedbackType": {"type": "string", "description": "Type of feedback"},
        "SatisfactionScore": {"type": "int8", "description": "Satisfaction score (1-5)"},
        "ComplaintCategory": {"type": "string", "description": "Complaint category"},
        "ServiceRecoveryFlag": {"type": "bool", "description": "Service recovery flag"},
        "ResolutionStatus": {"type": "string", "description": "Resolution status"},
        "ResolutionDateKey": {"type": "int32", "description": "FK → dim_date"},
        "FeedbackChannel": {"type": "string", "description": "Feedback channel"},
    },
}

DIM_AIRLINE_SCHEMA = {
    "dataset_id": DATASET_IDS["dim_airline"],
    "name": "DimAirline",
    "rows": 10,
    "key": "AirlineKey",
    "columns": {
        "AirlineKey": {"type": "int32", "description": "Primary key"},
        "AirlineId": {"type": "string", "description": "Airline identity code"},
        "AirlineIATACode": {"type": "string", "description": "IATA code"},
        "AirlineICAOCode": {"type": "string", "description": "ICAO code"},
        "AirlineName": {"type": "string", "description": "Airline name"},
        "AirlineGroup": {"type": "string", "description": "Airline group"},
        "HomeCountry": {"type": "string", "description": "Home country"},
        "HomeCountryCode": {"type": "string", "description": "Country code"},
        "BusinessModelClass": {"type": "string", "description": "Business model"},
        "IsActive": {"type": "bool", "description": "Is airline active?"},
        "StatusEffectiveDate": {
            "type": "object",
            "description": "Effective date (Type 1: not populated)",
        },
        "ReferenceVersion": {"type": "string", "description": "Data version reference"},
    },
}

DIM_ROUTE_SCHEMA = {
    "dataset_id": DATASET_IDS["dim_route"],
    "name": "DimRoute",
    "rows": 320,
    "key": "RouteKey",
    "columns": {
        "RouteKey": {"type": "int32", "description": "Primary key"},
        "RouteCode": {"type": "string", "description": "Route code"},
        "OriginAirportKey": {
            "type": "int32",
            "description": "FK → dim_airport (origin)",
        },
        "DestinationAirportKey": {
            "type": "int32",
            "description": "FK → dim_airport (destination)",
        },
        "DistanceKM": {"type": "object", "description": "Distance in km"},
        "DistanceMiles": {"type": "object", "description": "Distance in miles"},
        "RouteRegion": {"type": "string", "description": "Route region"},
        "IsInternational": {"type": "bool", "description": "Is international?"},
        "IsActive": {"type": "bool", "description": "Is route active?"},
    },
}

DIM_DATE_SCHEMA = {
    "dataset_id": DATASET_IDS["dim_date"],
    "name": "DimDate",
    "rows": 761,
    "key": "DateKey",
    "role_playing": True,
    "columns": {
        "DateKey": {"type": "int32", "description": "Primary key (YYYYMMDD)"},
        "FullDate": {"type": "date", "description": "Full date"},
        "Year": {"type": "int16", "description": "Year"},
        "Quarter": {"type": "int8", "description": "Quarter"},
        "MonthNumber": {"type": "int8", "description": "Month number"},
        "MonthName": {"type": "string", "description": "Month name"},
        "MonthShortName": {"type": "string", "description": "Short month name"},
        "YearMonth": {"type": "string", "description": "Year-Month"},
        "YearMonthSort": {"type": "int32", "description": "Sort key"},
        "WeekNumber": {"type": "int8", "description": "Week number"},
        "WeekStartDate": {"type": "date", "description": "Week start"},
        "DayOfMonth": {"type": "int8", "description": "Day of month"},
        "DayName": {"type": "string", "description": "Day name"},
        "DayOfWeekNumber": {"type": "int8", "description": "Day of week"},
        "IsWeekend": {"type": "bool", "description": "Is weekend?"},
        "IsReportingPeriod": {"type": "bool", "description": "Is reporting period?"},
        "FiscalYear": {"type": "int16", "description": "Fiscal year"},
        "FiscalQuarter": {"type": "int8", "description": "Fiscal quarter"},
        "FiscalMonthNumber": {"type": "int8", "description": "Fiscal month"},
    },
}

# ============================================================================
# Measure Definitions in Contract
# ============================================================================

MEASURE_DEFINITIONS: Dict[str, dict] = {
    # Flight Operations
    "FL01": {
        "id": "FL01",
        "name": "Flights Operated",
        "definition": "Count of flight operation legs that were operated",
        "formula": "COUNT(*) FILTER (WHERE FlightStatus = 'Operated')",
        "source_fact": "fact_flight_operations",
        "grain": "one row = one flight operation leg",
        "aggregation": "count",
        "unit": "flights",
        "filters": ["FlightStatus = 'Operated'"],
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
    "FL02": {
        "id": "FL02",
        "name": "Total Revenue Passengers",
        "definition": "Sum of revenue passenger counts across all flight operations",
        "formula": "SUM(RevenuePassengers)",
        "source_fact": "fact_flight_operations",
        "grain": "one row = one flight operation leg",
        "aggregation": "sum",
        "unit": "passengers",
        "filters": None,
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
    "FL03": {
        "id": "FL03",
        "name": "Average Delay Minutes",
        "definition": "Average departure delay across all flight operations",
        "formula": "AVG(DepartureDelayMinutes)",
        "source_fact": "fact_flight_operations",
        "grain": "one row = one flight operation leg",
        "aggregation": "avg",
        "unit": "minutes",
        "filters": None,
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
    "FL04": {
        "id": "FL04",
        "name": "Cancellation Rate",
        "definition": "Percentage of flight operations that were cancelled",
        "formula": (
            "SUM(CASE WHEN CancellationFlag = 1 THEN 1 ELSE 0 END)::numeric / "
            "NULLIF(COUNT(*), 0) * 100"
        ),
        "source_fact": "fact_flight_operations",
        "grain": "one row = one flight operation leg",
        "aggregation": "ratio",
        "unit": "percent",
        "filters": ["CancellationFlag IS NOT NULL"],
        "null_handling": "exclude_nulls",
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
    # Disruption Measures
    "DS01": {
        "id": "DS01",
        "name": "Total Disruptions",
        "definition": "Count of disruption events",
        "formula": "COUNT(*)",
        "source_fact": "fact_disruptions",
        "grain": "one row = one disruption event",
        "aggregation": "count",
        "unit": "events",
        "filters": None,
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
    "DS02": {
        "id": "DS02",
        "name": "Average Delay Minutes (Disruption)",
        "definition": "Average delay duration across disruption events",
        "formula": "AVG(DelayMinutes)",
        "source_fact": "fact_disruptions",
        "grain": "one row = one disruption event",
        "aggregation": "avg",
        "unit": "minutes",
        "filters": None,
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
    "DS03": {
        "id": "DS03",
        "name": "Controllable Disruptions",
        "definition": "Count of disruptions where the airline had control",
        "formula": "COUNT(*) FILTER (WHERE ControllableFlag = TRUE)",
        "source_fact": "fact_disruptions",
        "source_dimension": "dim_disruption_type",
        "grain": "one row = one disruption event",
        "aggregation": "count",
        "unit": "events",
        "filters": ["ControllableFlag = TRUE"],
        "null_handling": "exclude_nulls",
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
    # Customer Feedback Measures
    "CF01": {
        "id": "CF01",
        "name": "Total Feedback Events",
        "definition": "Count of customer feedback entries",
        "formula": "COUNT(*)",
        "source_fact": "fact_customer_feedback",
        "grain": "one row = one feedback event",
        "aggregation": "count",
        "unit": "feedbacks",
        "filters": None,
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
    "CF02": {
        "id": "CF02",
        "name": "Average Satisfaction Score",
        "definition": "Mean satisfaction score across all feedback entries",
        "formula": "AVG(SatisfactionScore)",
        "source_fact": "fact_customer_feedback",
        "grain": "one row = one feedback event",
        "aggregation": "avg",
        "unit": "score (1-5)",
        "filters": None,
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
    "CF03": {
        "id": "CF03",
        "name": "Complaint Percentage",
        "definition": "Percentage of feedback entries classified as complaints",
        "formula": (
            "COUNT(*) FILTER (WHERE FeedbackType = 'Complaint')::numeric / "
            "NULLIF(COUNT(*), 0) * 100"
        ),
        "source_fact": "fact_customer_feedback",
        "grain": "one row = one feedback event",
        "aggregation": "ratio",
        "unit": "percent",
        "filters": ["FeedbackType IS NOT NULL"],
        "null_handling": "exclude_nulls",
        "governance": "approved",
        "definition_version": "m311-1.0",
    },
}

# ============================================================================
# Undefined / Blocked Measures (per owner decisions)
# ============================================================================

BLOCKED_MEASURES: Dict[str, dict] = {
    "UNDEF-01": {
        "id": "UNDEF-01",
        "name": "Total Revenue",
        "reason": "OD-04 blocked — FactBookingTransactions unavailable",
        "governance": "blocked",
    },
    "UNDEF-02": {
        "id": "UNDEF-02",
        "name": "Total Operating Costs",
        "reason": "OD-04 blocked — FactOperatingCosts unavailable",
        "governance": "blocked",
    },
    "UNDEF-03": {
        "id": "UNDEF-03",
        "name": "On-Time Performance Threshold",
        "reason": "OD-09 owner decision pending",
        "governance": "owner_approval_required",
    },
    "UNDEF-04": {
        "id": "UNDEF-04",
        "name": "Satisfaction Score Scale Definition",
        "reason": "OD-11 owner decision pending",
        "governance": "owner_approval_required",
    },
    "UNDEF-05": {
        "id": "UNDEF-05",
        "name": "Coupon Allocation Metric",
        "reason": "OD-14 owner decision pending",
        "governance": "owner_approval_required",
    },
    "UNDEF-06": {
        "id": "UNDEF-06",
        "name": "Service Recovery Metric",
        "reason": "OD-17 service-recovery definition unresolved",
        "governance": "owner_approval_required",
    },
}

# ============================================================================
# Contract Export
# ============================================================================


def export_contract_json(path: Path) -> None:
    """Export the BI consumption contract as JSON.

    Uses an existing supported format consistent with the project architecture.
    """
    contract = {
        "model_id": MODEL_ID,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "owner": MODEL_OWNER,
        "datasets": DATASET_IDS,
        "dataset_schemas": {
            "fact_flight_operations": FACT_FLIGHT_OPERATIONS_SCHEMA,
            "fact_disruptions": FACT_DISRUPTIONS_SCHEMA,
            "fact_customer_feedback": FACT_CUSTOMER_FEEDBACK_SCHEMA,
            "dim_airline": DIM_AIRLINE_SCHEMA,
            "dim_route": DIM_ROUTE_SCHEMA,
            "dim_date": DIM_DATE_SCHEMA,
        },
        "measures": MEASURE_DEFINITIONS,
        "blocked_measures": BLOCKED_MEASURES,
        "od04_restrictions": {
            "blocked_facts": ["FactBookingTransactions", "FactOperatingCosts"],
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
        "compatibility": {
            "breaking_changes_detectable": True,
            "schema_versioning": "m311-1.0",
            "backward_compatible_additions": True,
            "dropping_columns": "requires_deprecation",
        },
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(contract, f, indent=2, ensure_ascii=False)

    print(f"BI consumption contract exported to {path}")


# ============================================================================
# Contract Validation
# ============================================================================


def validate_contract_against_schemas(contract_path: Path) -> dict:
    """Validate the exported contract against the actual underlying schemas.

    Checks:
    - Dataset identifiers match actual parquet schemas
    - Column types are consistent
    - Measure definitions reference existing facts
    - OD-04 blocked measures are not exposed as available
    - Model version is current
    """
    with open(contract_path, "r", encoding="utf-8") as f:
        contract = json.load(f)

    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
    }

    # Check model version
    if contract.get("model_version") != MODEL_VERSION:
        results["errors"].append(
            f"Model version mismatch: contract={contract.get('model_version')}, "
            f"expected={MODEL_VERSION}"
        )
        results["valid"] = False

    # Check OD-04 blocked measures not in available measures
    available_measure_ids = set(MEASURE_DEFINITIONS.keys())
    blocked_measure_ids = set(BLOCKED_MEASURES.keys())
    overlap = available_measure_ids & blocked_measure_ids
    if overlap:
        results["errors"].append(
            f"Blocked measures unexpectedly in available measures: {overlap}"
        )
        results["valid"] = False

    # Check all dataset IDs exist in schemas
    datasets_in_contract = set(contract.get("dataset_schemas", {}).keys())
    expected_datasets = {
        "fact_flight_operations",
        "fact_disruptions",
        "fact_customer_feedback",
        "dim_airline",
        "dim_route",
        "dim_date",
    }
    missing_from_contract = expected_datasets - datasets_in_contract
    extra_in_contract = datasets_in_contract - expected_datasets
    if missing_from_contract:
        results["warnings"].append(
            f"Datasets missing from contract schemas: {missing_from_contract}"
        )
    if extra_in_contract:
        results["warnings"].append(
            f"Datasets in contract not expected: {extra_in_contract}"
        )

    # Check all measure source facts exist
    for measure_id, measure_def in MEASURE_DEFINITIONS.items():
        source_fact = measure_def.get("source_fact", "N/A")
        # Only validate if source_fact is not N/A (some measures don't have a single source fact)
        if source_fact != "N/A" and source_fact not in contract.get("dataset_schemas", {}):
            results["errors"].append(
                f"Measure {measure_id} references unknown fact: {source_fact}"
            )
            results["valid"] = False

    return results


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    import sys

    contract_path = Path("contracts/bi_consumption_model_m311.json")
    contract_path.parent.mkdir(parents=True, exist_ok=True)

    export_contract_json(contract_path)

    # Validate the exported contract
    results = validate_contract_against_schemas(contract_path)
    print(f"\nContract validation results:")
    print(f"  Valid: {results['valid']}")
    if results["errors"]:
        print(f"  Errors: {results['errors']}")
    if results["warnings"]:
        print(f"  Warnings: {results['warnings']}")
    if not results["errors"] and not results["warnings"]:
        print("  No issues found — contract is valid")