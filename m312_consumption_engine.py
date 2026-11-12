"""
M3.12.2 — Semantic Contract Integration & Governed BI Consumption Engine.

Implements a governed BI consumption layer between the M3.11 analytical measures
and future dashboard interfaces. Uses the existing m311_governed_measures.py and
m311_bi_contract.py implementations. No new framework introduced.

Enforces OD-04 restrictions, measure authorization, filter propagation, and
standardized response formatting. Fail-closed at every boundary.
"""

from __future__ import annotations

import json
import logging
from decimal import Decimal
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd

from m311_governed_measures import (
    calculate_flights_operated,
    calculate_total_revenue_passengers,
    calculate_average_delay_minutes,
    calculate_cancellation_rate,
    calculate_disruptions_total,
    calculate_average_delay_disruption,
    calculate_controllable_disruptions,
    calculate_feedback_total,
    calculate_average_satisfaction,
    calculate_complaint_percentage,
    check_governance_status,
    GovernanceStatus,
    is_measure_implementable,
    validate_measure_access,
)
from m311_bi_contract import (
    MEASURE_DEFINITIONS,
    BLOCKED_MEASURES,
    DATASET_IDS,
    MODEL_VERSION,
    validate_contract_against_schemas,
    export_contract_json,
)

# ============================================================================
# Logger
# ============================================================================

logger = logging.getLogger("m312.consumption")
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s [m312} %(levelname)s: %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ============================================================================
# Contract Caching
# ============================================================================

_contract_cache: dict | None = None


def get_contract() -> dict:
    """Load and cache the BI consumption contract."""
    global _contract_cache
    if _contract_cache is not None:
        return _contract_cache

    contract_path = Path("contracts/bi_consumption_model_m311.json")
    if not contract_path.exists():
        msg = f"Contract file not found: {contract_path}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    with open(contract_path, "r", encoding="utf-8") as f:
        contract = json.load(f)

    # Validate required top-level fields
    required_fields = ["model_id", "model_name", "model_version", "measures", "datasets"]
    missing = [f for f in required_fields if f not in contract]
    if missing:
        msg = f"Contract missing required fields: {missing}"
        logger.error(msg)
        raise ValueError(msg)

    # Validate model version
    if contract.get("model_version") != MODEL_VERSION:
        logger.warning(
            f"Contract version mismatch: file={contract.get('model_version')}, "
            f"expected={MODEL_VERSION}"
        )

    # Validate approved measure identifiers
    approved_measure_ids = set(MEASURE_DEFINITIONS.keys())
    contract_measure_ids = set()
    for mid, mdef in contract.get("measures", {}).items():
        if isinstance(mdef, dict) and "id" in mdef:
            contract_measure_ids.add(mdef["id"])
        else:
            contract_measure_ids.add(mid)

    # Report any discrepancies
    extra_in_contract = contract_measure_ids - approved_measure_ids
    missing_from_contract = approved_measure_ids - contract_measure_ids
    if extra_in_contract:
        logger.warning(f"Contract contains unexpected measure IDs: {extra_in_contract}")
    if missing_from_contract:
        logger.warning(f"Contract missing approved measure IDs: {missing_from_contract}")

    # Validate dataset identifiers
    contract_dataset_ids = set(contract.get("datasets", {}).keys())
    expected_dataset_ids = set(DATASET_IDS.keys())
    missing_datasets = expected_dataset_ids - contract_dataset_ids
    extra_datasets = contract_dataset_ids - expected_dataset_ids
    if missing_datasets:
        logger.warning(f"Contract missing dataset IDs: {missing_datasets}")
    if extra_datasets:
        logger.warning(f"Contract contains unexpected dataset IDs: {extra_datasets}")

    _contract_cache = contract
    logger.info(f"Contract loaded and cached: {contract_path}")
    return contract


# ============================================================================
# Governance Enforcement
# ============================================================================

def verify_measure_access(measure_id: str, context: dict | None = None) -> dict:
    """Verify that a measure is accessible per governance rules."""
    status = check_governance_status(measure_id)

    result = {
        "measure_id": measure_id,
        "governance_status": status,
        "allowed": False,
        "reason": "",
        "block_code": "",
    }

    if status == GovernanceStatus.APPROVED:
        result["allowed"] = True
        result["reason"] = "Approved measure — access granted"
        result["block_code"] = ""
    elif status == GovernanceStatus.UNDEFINED:
        result["reason"] = f"Measure undefined — {measure_id}: not in approved measure registry"
        result["block_code"] = "undefined"
    elif status == GovernanceStatus.BLOCKED:
        result["reason"] = (
            f"Measure blocked — {measure_id}: OD-04 exchange-rate policy restriction"
        )
        result["block_code"] = "od04"
    elif status == GovernanceStatus.OWNER_APPROVAL_REQUIRED:
        result["reason"] = (
            f"Owner approval required — {measure_id}: pending governance sign-off"
        )
        result["block_code"] = "owner_approval"
    else:
        result["reason"] = f"Governance error — unknown status: {status}"
        result["block_code"] = "governance_error"

    logger.info(
        f"Measure access check: {measure_id} -> allowed={result['allowed']}, "
        f"status={result['governance_status']}, block={result['block_code']}"
    )
    return result


def verify_dataset_access(dataset_id: str) -> dict:
    """Verify that a dataset is accessible per OD-04 and governance rules."""
    result = {
        "accessible": False,
        "reason": "",
        "block_code": "",
    }

    # Check if dataset is a blocked fact per OD-04
    blocked_facts = ["FactBookingTransactions", "FactOperatingCosts"]
    if dataset_id in blocked_facts:
        result["accessible"] = False
        result["reason"] = f"Dataset blocked per OD-04: {dataset_id}"
        result["block_code"] = "od04_blocked_fact"
        return result

    # Check if dataset ID is known
    if dataset_id not in DATASET_IDS.values():
        result["accessible"] = False
        result["reason"] = f"Unknown dataset ID: {dataset_id}"
        result["block_code"] = "unknown_dataset"
        return result

    result["accessible"] = True
    result["reason"] = "Dataset accessible"
    result["block_code"] = ""
    logger.info(f"Dataset access check: {dataset_id} -> accessible={result['accessible']}")
    return result


# ============================================================================
# Measure Execution Engine
# ============================================================================

# Map measure IDs to their calculation functions
_MEASURE_FUNCTIONS: dict[str, callable] = {
    "FL01": calculate_flights_operated,
    "FL02": calculate_total_revenue_passengers,
    "FL03": calculate_average_delay_minutes,
    "FL04": calculate_cancellation_rate,
    "DS01": calculate_disruptions_total,
    "DS02": calculate_average_delay_disruption,
    "DS03": calculate_controllable_disruptions,
    "CF01": calculate_feedback_total,
    "CF02": calculate_average_satisfaction,
    "CF03": calculate_complaint_percentage,
}

# Map measure IDs to their source fact names
_MEASURE_SOURCE_FACT: dict[str, str] = {
    "FL01": "fact_flight_operations",
    "FL02": "fact_flight_operations",
    "FL03": "fact_flight_operations",
    "FL04": "fact_flight_operations",
    "DS01": "fact_disruptions",
    "DS02": "fact_disruptions",
    "DS03": "fact_disruptions",
    "CF01": "fact_customer_feedback",
    "CF02": "fact_customer_feedback",
    "CF03": "fact_customer_feedback",
}

# Map measure IDs to their grain descriptions
_MEASURE_GRAIN: dict[str, str] = {
    "FL01": "one row = one flight operation leg",
    "FL02": "one row = one flight operation leg",
    "FL03": "one row = one flight operation leg",
    "FL04": "one row = one flight operation leg",
    "DS01": "one row = one disruption event",
    "DS02": "one row = one disruption event",
    "DS03": "one row = one disruption event (with dim_disruption_type join)",
    "CF01": "one row = one feedback event",
    "CF02": "one row = one feedback event",
    "CF03": "one row = one feedback event",
}

# Map measure IDs to their aggregation behavior
_MEASURE_AGGREGATION: dict[str, str] = {
    "FL01": "count",
    "FL02": "sum",
    "FL03": "avg",
    "FL04": "ratio",
    "DS01": "count",
    "DS02": "avg",
    "DS03": "count",
    "CF01": "count",
    "CF02": "avg",
    "CF03": "ratio",
}


def execute_measure(
    measure_id: str,
    fact_data: pd.DataFrame,
    filters: dict[str, Any] | None = None,
    group_by: str | List[str] | None = None,
) -> dict:
    """Execute a governed measure calculation with full governance and filter enforcement.

    Parameters
    ----------
    measure_id : str
        The measure ID (FL01-FL04, DS01-DS03, CF01-CF03)
    fact_data : pd.DataFrame
        The fact table data (read-only; not modified)
    filters : dict, optional
        Filter dict with column_name -> value pairs to apply before calculation
    group_by : str or List[str], optional
        Dimension column(s) to group by. If None, returns overall result.

    Returns
    -------
    dict with keys:
    - success: bool
    - measure_id: str
    - measure_name: str
    - value: any (scalar or dict of grouped values)
    - unit: str
    - grain: str
    - aggregation: str
    - applied_filters: dict
    - source_fact: str
    - governance_status: GovernanceStatus
    - execution_status: str
    - disclosure: str
    - error: str | None
    """
    # ---- Governance check ----
    governance = verify_measure_access(measure_id)
    if not governance["allowed"]:
        return {
            "success": False,
            "measure_id": measure_id,
            "measure_name": MEASURE_DEFINITIONS.get(measure_id, {}).get("name", measure_id),
            "value": None,
            "unit": "?",
            "grain": "?",
            "aggregation": "?",
            "applied_filters": {},
            "source_fact": _MEASURE_SOURCE_FACT.get(measure_id, "?"),
            "governance_status": governance["governance_status"],
            "execution_status": "rejected_governance",
            "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
            "error": governance["reason"],
        }

    # ---- Dataset accessibility check ----
    source_fact = _MEASURE_SOURCE_FACT.get(measure_id, "")
    dataset_check = verify_dataset_access(source_fact)
    if not dataset_check["accessible"]:
        return {
            "success": False,
            "measure_id": measure_id,
            "measure_name": MEASURE_DEFINITIONS.get(measure_id, {}).get("name", measure_id),
            "value": None,
            "unit": "?",
            "grain": "?",
            "aggregation": "?",
            "applied_filters": {},
            "source_fact": source_fact,
            "governance_status": governance["governance_status"],
            "execution_status": "rejected_dataset",
            "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
            "error": dataset_check["reason"],
        }

    # ---- Filter enforcement ----
    # Make a copy to avoid modifying the original DataFrame
    df = fact_data.copy()

    # Apply filters if provided
    applied_filters: dict[str, Any] = {} if filters is None else dict(filters)
    if filters is not None and filters:
        for col, value in filters.items():
            if col not in df.columns:
                return {
                    "success": False,
                    "measure_id": measure_id,
                    "measure_name": MEASURE_DEFINITIONS.get(measure_id, {}).get("name", measure_id),
                    "value": None,
                    "unit": "?",
                    "grain": "?",
                    "aggregation": "?",
                    "applied_filters": applied_filters,
                    "source_fact": source_fact,
                    "governance_status": governance["governance_status"],
                    "execution_status": "rejected_invalid_filter",
                    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
                    "error": f"Filter column '{col}' not found in fact table",
                }
            # Apply the filter
            df = df[df[col] == value]

    # ---- Group-by handling ----
    group_columns: List[str] = (
        [group_by] if isinstance(group_by, str) else (group_by or [])
    )

    try:
        if group_columns:
            # Group by specified dimensions
            valid_groupby = [g for g in group_columns if g in df.columns]
            if not valid_groupby:
                return {
                    "success": False,
                    "measure_id": measure_id,
                    "measure_name": MEASURE_DEFINITIONS.get(measure_id, {}).get("name", measure_id),
                    "value": None,
                    "unit": "?",
                    "grain": "?",
                    "aggregation": "?",
                    "applied_filters": applied_filters,
                    "source_fact": source_fact,
                    "governance_status": governance["governance_status"],
                    "execution_status": "rejected_invalid_groupby",
                    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
                    "error": f"No valid group-by columns found. Requested: {group_columns}",
                }

            # Perform the grouping and calculation
            if _MEASURE_AGGREGATION.get(measure_id) == "count":
                result_df = df.groupby(valid_groupby).size().reset_index(name="value")
            elif _MEASURE_AGGREGATION.get(measure_id) == "sum":
                numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
                if numeric_cols:
                    first_numeric = numeric_cols[0]
                    result_df = df.groupby(valid_groupby)[first_numeric].sum().reset_index(name="value")
                else:
                    result_df = df.groupby(valid_groupby).size().reset_index(name="value")
            elif _MEASURE_AGGREGATION.get(measure_id) == "avg":
                numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
                if numeric_cols:
                    first_numeric = numeric_cols[0]
                    if first_numeric in ["DepartureDelayMinutes", "DelayMinutes", "SatisfactionScore"]:
                        result_df = (
                            df.groupby(valid_groupby)[first_numeric]
                            .mean(numeric_only=True)
                            .reset_index(name="value")
                        )
                    else:
                        result_df = df.groupby(valid_groupby)[first_numeric].mean().reset_index(name="value")
                else:
                    result_df = df.groupby(valid_groupby).size().reset_index(name="value")
            elif _MEASURE_AGGREGATION.get(measure_id) == "ratio":
                import numpy as np
                numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
                if len(numeric_cols) >= 2:
                    first, second = numeric_cols[0], numeric_cols[1]
                    with np.errstate(divide="ignore", invalid="ignore"):
                        result_df = (
                            df.groupby(valid_groupby)
                            .apply(lambda g: (g[first].sum() / g[second].sum() * 100 if g[second].sum() else None))
                            .reset_index(name="value")
                        )
                else:
                    result_df = df.groupby(valid_groupby).size().reset_index(name="value")
            else:
                result_df = df.groupby(valid_groupby).size().reset_index(name="value")

            # Trim to requested group_by columns only
            result_columns = valid_groupby + ["value"]
            result_df = result_df[result_columns]

            # Convert to dict for JSON serialization
            if len(result_df) == 0:
                value_result = {}
            elif len(result_df) == 1:
                value_result = float(result_df["value"].iloc[0])
            else:
                value_result = {}
                for _, row in result_df.iterrows():
                    key = tuple(row[valid_groupby].tolist()) if valid_groupby else "overall"
                    value_result[key] = float(row["value"]) if pd.notna(row["value"]) else None

            value = value_result
            execution_status = "grouped_success"
        else:
            # ---- No group-by: calculate overall result ----
            # CRITICAL: For average measures, we must calculate from raw observations,
            # not by averaging pre-aggregated averages.
            # This is the most important technical rule.

            agg = _MEASURE_AGGREGATION.get(measure_id, "count")

            if agg == "count":
                value = int(len(df))
            elif agg == "sum":
                if "RevenuePassengers" in df.columns:
                    value = int(df["RevenuePassengers"].fillna(0).sum())
                elif "DelayMinutes" in df.columns:
                    value = float(df["DelayMinutes"].sum())
                else:
                    value = float(df.select_dtypes(include=["number"]).sum().iloc[0]) if not df.empty else 0
            elif agg == "avg":
                # CRITICAL: Calculate from raw observations, NOT by averaging averages
                if measure_id == "FL03":
                    delays = df["DepartureDelayMinutes"].dropna()
                    if delays.empty:
                        value = None
                    else:
                        value = float(delays.mean())
                elif measure_id == "CF02":
                    scores = df["SatisfactionScore"].dropna()
                    if scores.empty:
                        value = None
                    else:
                        value = round(float(scores.mean()), 2)
                else:
                    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
                    if numeric_cols:
                        val = df[numeric_cols[0]].mean()
                        value = float(val) if pd.notna(val) else None
                    else:
                        value = None
            elif agg == "ratio":
                if measure_id == "FL04":
                    total = len(df)
                    if total == 0:
                        value = None
                    else:
                        cancelled = int((df["CancellationFlag"] == 1).sum())
                        value = round(cancelled / total * 100, 2)
                elif measure_id == "CF03":
                    total = len(df)
                    if total == 0:
                        value = None
                    else:
                        complaints = int((df["FeedbackType"] == "Complaint").sum())
                        value = round(complaints / total * 100, 2)
                else:
                    value = None
            else:
                value = None

            # Apply zero-denominator safety
            if value is not None and isinstance(value, float):
                formula = MEASURE_DEFINITIONS.get(measure_id, {}).get("formula", "")
                if "NULLIF" in formula and abs(value) == 0:
                    value = None

            execution_status = "scalar_success"
            return {
                "success": True,
                "measure_id": measure_id,
                "measure_name": MEASURE_DEFINITIONS.get(measure_id, {}).get("name", measure_id),
                "value": value,
                "unit": _get_measure_unit(measure_id),
                "grain": _MEASURE_GRAIN.get(measure_id, "one row"),
                "aggregation": _MEASURE_AGGREGATION.get(measure_id, "count"),
                "applied_filters": applied_filters,
                "source_fact": source_fact,
                "governance_status": governance["governance_status"],
                "execution_status": execution_status,
                "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
                "error": None,
            }

    except Exception as e:
        logger.error(f"Error executing measure {measure_id}: {e}", exc_info=True)
        return {
            "success": False,
            "measure_id": measure_id,
            "measure_name": MEASURE_DEFINITIONS.get(measure_id, {}).get("name", measure_id),
            "value": None,
            "unit": "?",
            "grain": "?",
            "aggregation": "?",
            "applied_filters": applied_filters,
            "source_fact": source_fact,
            "governance_status": governance["governance_status"],
            "execution_status": "error",
            "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
            "error": str(e),
        }


def _get_measure_unit(measure_id: str) -> str:
    """Get the unit string for a measure ID."""
    units: dict[str, str] = {
        "FL01": "flights",
        "FL02": "passengers",
        "FL03": "minutes",
        "FL04": "percent",
        "DS01": "events",
        "DS02": "minutes",
        "DS03": "events",
        "CF01": "feedbacks",
        "CF02": "score (1-5)",
        "CF03": "percent",
    }
    return units.get(measure_id, "?")


# ============================================================================
# Dimension Filter Support
# ============================================================================

_DIMENSION_FKS: dict[str, dict[str, str]] = {
    "fact_flight_operations": {
        "AirlineKey": "DimAirline",
        "RouteKey": "DimRoute",
        "ScheduledDepartureDateKey": "DimDate",
        "ScheduledArrivalDateKey": "DimDate",
        "EventDateKey": "DimDate",
        "AircraftKey": "DimAircraft",
        "RouteKey": "DimRoute",
        "AvailableSeats": "int16",
        "BookedPassengers": "int16",
        "RevenuePassengers": "int16",
        "FlightStatus": "string",
        "DepartureDelayMinutes": "int16",
        "CancellationFlag": "bool",
        "CompletionFlag": "bool",
        "OnTimeFlag": "bool",
        "OnTimeArrivalFlag": "bool",
    },
    "fact_disruptions": {
        "AirlineKey": "DimAirline",
        "RouteKey": "DimRoute",
        "DisruptionTypeKey": "DimDisruptionType",
        "EventLocationAirportKey": "DimAirport",
        "EventDateKey": "DimDate",
        "DelayMinutes": "int16",
        "PrimaryCauseFlag": "bool",
        "ReactionaryFlag": "bool",
    },
    "fact_customer_feedback": {
        "CustomerKey": "DimCustomer",
        "AirlineKey": "DimAirline",
        "RouteKey": "DimRoute",
        "FeedbackDateKey": "DimDate",
        "FeedbackType": "string",
        "SatisfactionScore": "int8",
        "ComplaintCategory": "string",
    },
}

_ROLE_PLAYING_DATES: dict[str, str] = {
    "ScheduledDepartureDateKey": "departure (active)",
    "ScheduledArrivalDateKey": "arrival (inactive)",
    "EventDateKey": "event (active)",
}


def apply_dimension_filter(
    df: pd.DataFrame,
    dimension: str,
    filter_value: Any,
    filter_column: str | None = None,
) -> pd.DataFrame:
    """Apply a dimension filter based on verified foreign-key relationships."""
    if filter_column is None:
        for fact, fks in _DIMENSION_FKS.items():
            for fk_col, dim_name in fks.items():
                if dim_name == dimension:
                    filter_column = fk_col
                    break
            if filter_column:
                break

    if filter_column is None or filter_column not in df.columns:
        logger.warning(f"Could not determine FK column for dimension '{dimension}'. Returning unfiltered DataFrame.")
        return df

    df_filtered = df[df[filter_column] == filter_value]
    logger.info(f"Applied dimension filter: {dimension} -> {filter_column} = {filter_value}, rows retained: {len(df_filtered)} / {len(df)}")
    return df_filtered


def apply_role_playing_date_filter(
    df: pd.DataFrame,
    date_fk: str,
    date_value: int,
    dim_date: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Apply a role-playing date filter using the verified FK name."""
    if date_fk not in df.columns:
        logger.warning(f"Date FK '{date_fk}' not found in DataFrame")
        return df

    try:
        df_filtered = df[df[date_fk] == date_value]
    except TypeError:
        df_filtered = df[df[date_fk].astype(str) == str(date_value)]

    if dim_date is not None and "DateKey" in dim_date.columns:
        valid_dates = set(dim_date["DateKey"].astype(int).tolist())
        df_filtered = df_filtered[df_filtered[date_fk].isin(valid_dates)]

    logger.info(f"Role-playing date filter: {date_fk} = {date_value}, rows retained: {len(df_filtered)} / {len(df)}")
    return df_filtered


# ============================================================================
# Standard BI Response Structure
# ============================================================================

def build_response(
    measure_id: str,
    result: dict,
    request_id: str | None = None,
    applied_filters: dict | None = None,
    grouping_dims: list | None = None,
    source_dataset: str | None = None,
    lineage: list | None = None,
    governance_status: GovernanceStatus | None = None,
) -> dict:
    """Build a standardized BI consumption response."""
    disclaimer = "Synthetic Simulation — Not Actual Airline Performance"

    response: dict = {
        "request_id": request_id or f"m312-{measure_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "contract_version": MODEL_VERSION,
        "measure_id": measure_id,
        "measure_name": MEASURE_DEFINITIONS.get(measure_id, {}).get("name", measure_id),
        "value": result.get("value"),
        "unit": result.get("unit", _get_measure_unit(measure_id)),
        "grain": result.get("grain", _MEASURE_GRAIN.get(measure_id, "one row")),
        "aggregation": result.get("aggregation", _MEASURE_AGGREGATION.get(measure_id, "count")),
        "applied_filters": applied_filters or {},
        "grouping_dimensions": grouping_dims or [],
        "source_fact": result.get("source_fact", ""),
        "source_dataset": source_dataset or _MEASURE_SOURCE_FACT.get(measure_id, ""),
        "data_lineage": lineage or [MODEL_VERSION, measure_id, datetime.utcnow().isoformat()],
        "governance_status": governance_status.value if governance_status else "unknown",
        "execution_status": result.get("execution_status", "unknown"),
        "disclaimer": disclaimer,
        "error": result.get("error"),
    }

    return response


# ============================================================================
# High-Level Convenience Functions
# ============================================================================

def get_measure_info(measure_id: str) -> dict:
    """Get metadata about a governed measure."""
    status = check_governance_status(measure_id)
    definition = MEASURE_DEFINITIONS.get(measure_id, {})

    return {
        "measure_id": measure_id,
        "name": definition.get("name", measure_id),
        "governance_status": status,
        "implementable": is_measure_implementable(measure_id),
        "formula": definition.get("formula", "N/A"),
        "grain": definition.get("grain", "N/A"),
        "aggregation": definition.get("aggregation", "N/A"),
        "unit": definition.get("unit", "N/A"),
        "filters": definition.get("filters", []),
        "null_handling": definition.get("null_handling", "N/A"),
        "known_limitations": definition.get("known_limitations", "N/A"),
        "source_fact": definition.get("source_fact", "N/A"),
    }


def list_approved_measures() -> dict[str, dict]:
    """List all approved measures with their metadata."""
    result = {}
    for mid in MEASURE_DEFINITIONS:
        status = check_governance_status(mid)
        result[mid] = {
            "name": MEASURE_DEFINITIONS[mid].get("name", mid),
            "governance_status": status,
            "implementable": is_measure_implementable(mid),
        }
    result["_blocked"] = BLOCKED_MEASURES
    return result


# ============================================================================
# Test Hook: Direct Function Exposure for Behavioral Tests
# ============================================================================

# All tests must use actual production functions from m311_governed_measures.py
# and m311_bi_contract.py, not hardcoded values or fixture JSON.

# ============================================================================
# End of Module
# ============================================================================

if __name__ == "__main__":
    print("M3.12.2 Semantic Contract Integration Engine")
    print(f"Contract version: {MODEL_VERSION}")
    print(f"Approved measures: {list(MEASURE_DEFINITIONS.keys())}")
    print(f"Blocked measures: {list(BLOCKED_MEASURES.keys())}")
    print(f"Dataset IDs: {len(DATASET_IDS)}")
    print("Engine ready.")