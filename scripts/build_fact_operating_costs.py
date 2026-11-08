"""Build curated FactOperatingCosts dataset.

Generates a deterministic synthetic operating-cost fact table from the
existing curated dimensions (DimAirline, DimRoute, DimDate, DimCurrency)
and FactFlightOperations.

Reference documents:
- docs/03_DATA_CONTRACTS.md v1.5, Sections 5.4, 6.3.3, 7, 9, 10 (FactOperatingCosts
  grain, columns, keys, date policy, currency conversion, cost categories)
- docs/governance/PAGE_03_REVENUE_FINANCE_SCHEMA_DECISION.md (OD-04a through OD-04f
  owner-confirmed currency decisions; RateDateKey / RateVersion preserved per
  Section 5 of the schema decision)
- OD-04b: USD per one unit; exact-date lookup; 6 decimal places for rate;
  round final converted amount to 2 decimals; no forward-fill
- OD-04c: Rate source AEROVISION-360-SYNTHETIC-FX-V1
- OD-04d: Rate version FX-YYYY-MM-DD-NNN
- OD-04e: Missing exact-date rate quarantines the row; no forward-fill
- Contract Section 10.4: CostAmount is signed — positive expense, negative
  credit/reversal. CostAmountUSD follows the same sign after conversion.
- Contract Section 5.4: CostCategory controlled set; CostSubcategory controlled
  within category; SourceDocumentNumber supports uniqueness and audit.

Writes controlled CSV, Parquet, quarantine, and manifest outputs. Never modifies
source data. Never overwrites existing outputs.
"""

from pathlib import Path
from datetime import datetime, timezone, date, timedelta
import sys
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Ensure project root is importable when run directly.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utilities.hashing import sha256_file
from src.utilities.io import write_json_atomic
from src.utilities.paths import project_path

# ---------------------------------------------------------------------------
# Configuration (deterministic)
# ---------------------------------------------------------------------------
SEED = 3602028  # Explicit seed for reproducible generation
RNG = np.random.default_rng(SEED)

# Reporting period per contract Section 9.4.
REPORTING_START = "2025-10-01"
REPORTING_END = "2026-09-30"

# OD-04c / OD-04d rate source and version (from ref_exchange_rates.csv).
RATE_SOURCE = "AEROVISION-360-SYNTHETIC-FX-V1"
RATE_VERSION = "FX-2026-11-04-001"

# Synthetic provenance label (exact string required by project policy).
SYNTHETIC_PROVENANCE = "Synthetic Simulation — Not Actual Airline Performance."

# Cost categories and subcategories (contract Section 5.4 / 6.3.3 proposed
# taxonomy; OD-13 formal approval pending — used as engineering baseline).
COST_CATEGORY_SUBCATEGORY = {
    "Fuel": [
        "Jet Fuel", "Fuel Surcharge", "Fuel Adjustment",
    ],
    "Crew": [
        "Flight Crew", "Cabin Crew", "Crew Accommodation",
        "Crew Transport", "Crew Training",
    ],
    "Maintenance": [
        "Line Maintenance", "Base Maintenance", "Aircraft Parts",
        "Component Overhaul",
    ],
    "Airport Charges": [
        "Landing Charges", "Parking Charges", "Passenger Handling",
        "Ground Handling",
    ],
    "Navigation": [
        "En-route Charges", "Terminal Navigation Charges",
    ],
    "Sales and Distribution": [
        "Agency Commission", "GDS Fees", "Payment Processing",
        "Distribution Fees",
    ],
    "Overhead": [
        "Administration", "IT", "Facilities", "Insurance",
        "Professional Services",
    ],
    "Other": [
        "Operational Supplies", "Other Direct Operating Expenses",
    ],
}

# Cost category selection weights (must sum to 1.0).
CATEGORY_WEIGHTS = {
    "Fuel": 0.25,
    "Crew": 0.20,
    "Maintenance": 0.15,
    "Airport Charges": 0.15,
    "Navigation": 0.10,
    "Sales and Distribution": 0.05,
    "Overhead": 0.05,
    "Other": 0.05,
}
CATEGORIES = list(CATEGORY_WEIGHTS.keys())
CATEGORY_WEIGHT_LIST = list(CATEGORY_WEIGHTS.values())

# Share of cost lines that are credits/reversals (negative amount).
CREDIT_REVERSAL_SHARE = 0.05

# Share of cost lines that are allocated from multi-flight pools.
ALLOCATED_SHARE = 0.20

# Cost amount ranges (original currency units).
COST_AMOUNT_MIN = 100.00
COST_AMOUNT_MAX = 50000.00
CREDIT_AMOUNT_MIN = -10000.00
CREDIT_AMOUNT_MAX = -100.00

# Generation volumes (validation scale, consistent with FactFlightOperations
# validation volume of 5,000 legs).
COST_LINES_PER_FLIGHT_MIN = 1
COST_LINES_PER_FLIGHT_MAX = 2

OUT = project_path("data", "03_curated")
MANIFESTS = project_path("data", "manifests")
QUARANTINE = project_path("data", "02_staging", "quarantine")

FFO_PATH = OUT / "fact_flight_operations.parquet"
AIRLINE_PATH = OUT / "dim_airline.parquet"
ROUTE_PATH = OUT / "dim_route.parquet"
DATE_PATH = OUT / "dim_date.parquet"
CURRENCY_PATH = OUT / "dim_currency.parquet"
FX_PATH = project_path("data", "04_reference", "ref_exchange_rates.csv")

CSV = OUT / "fact_operating_costs.csv"
PARQUET = OUT / "fact_operating_costs.parquet"
QUARANTINE_CSV = QUARANTINE / "fact_operating_costs_quarantined.csv"
MANIFEST = MANIFESTS / "fact_operating_costs_manifest.json"

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

# Verify source dimensions exist.
for path in [FFO_PATH, AIRLINE_PATH, ROUTE_PATH, DATE_PATH, CURRENCY_PATH, FX_PATH]:
    if not path.exists():
        raise FileNotFoundError(f"Required source not found: {path}")

# Verify outputs do not already exist (never overwrite).
for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)
QUARANTINE.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Load dimensions
# ---------------------------------------------------------------------------
ffo = pd.read_parquet(FFO_PATH)
airlines = pd.read_parquet(AIRLINE_PATH)
routes = pd.read_parquet(ROUTE_PATH)
dates = pd.read_parquet(DATE_PATH)
currencies = pd.read_parquet(CURRENCY_PATH)
fx = pd.read_csv(FX_PATH, dtype={"CurrencyCode": "string", "RateDate": "string"})

active_airlines = airlines[airlines["IsActive"] == True]

if len(active_airlines) == 0:
    raise RuntimeError("No active airlines in DimAirline.")
if len(ffo) == 0:
    raise RuntimeError("No flight operations in FactFlightOperations.")
if len(fx) == 0:
    raise RuntimeError("No exchange rates in ref_exchange_rates.csv.")

ffo_by_key = ffo.set_index("FlightOperationKey")

# CurrencyKey -> CurrencyCode mapping.
currency_key_to_code = dict(zip(
    currencies["CurrencyKey"].astype(int),
    currencies["CurrencyCode"].astype(str),
))
currency_code_to_key = dict(zip(
    currencies["CurrencyCode"].astype(str),
    currencies["CurrencyKey"].astype(int),
))

# Valid key sets.
valid_airline_keys = set(airlines["AirlineKey"].astype(int))
valid_route_keys = set(routes["RouteKey"].astype(int))
valid_currency_keys = set(currencies["CurrencyKey"].astype(int))
valid_date_keys = set(dates["DateKey"].astype(int))
valid_flight_operation_keys = set(ffo["FlightOperationKey"].astype(int))

# Build FX lookup: (CurrencyCode, RateDate "YYYY-MM-DD") -> ExchangeRateToUSD.
fx_lookup = {}
for _, fx_row in fx.iterrows():
    fx_lookup[(str(fx_row["CurrencyCode"]), str(fx_row["RateDate"]))] = \
        float(fx_row["ExchangeRateToUSD"])

# Build date key <-> full date mappings.
def _to_date_obj(v):
    if isinstance(v, date):
        return v
    return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()

dates["_full_date_obj"] = dates["FullDate"].apply(_to_date_obj)
date_key_to_full = dict(zip(
    dates["DateKey"].astype(int),
    dates["_full_date_obj"],
))

# Reporting period date bounds.
reporting_start_date = datetime.strptime(REPORTING_START, "%Y-%m-%d").date()
reporting_end_date = datetime.strptime(REPORTING_END, "%Y-%m-%d").date()

# ---------------------------------------------------------------------------
# Generate deterministic synthetic operating-cost ledger lines
# ---------------------------------------------------------------------------
records = []
quarantined = []
operating_cost_key = 1
used_business_keys = set()
used_composite_keys = set()

flight_keys = ffo["FlightOperationKey"].astype(int).tolist()

for flight_operation_key in flight_keys:
    ffo_row = ffo_by_key.loc[flight_operation_key]
    airline_key = int(ffo_row["AirlineKey"])
    route_key = int(ffo_row["RouteKey"])

    # RouteKey and AirlineKey must agree with the flight leg (denormalized).
    route_row = routes[routes["RouteKey"] == route_key].iloc[0]
    if int(route_row["RouteKey"]) != route_key:
        continue

    # Number of cost lines for this flight leg.
    n_cost_lines = int(RNG.integers(
        COST_LINES_PER_FLIGHT_MIN, COST_LINES_PER_FLIGHT_MAX + 1
    ))

    for _ in range(n_cost_lines):
        # --- Cost date (within reporting period) ---
        cost_full = date_key_to_full[int(
            RNG.choice(
                dates[
                    (dates["_full_date_obj"] >= reporting_start_date)
                    & (dates["_full_date_obj"] <= reporting_end_date)
                ]["DateKey"].astype(int).tolist()
            )
        )]
        cost_date_key = int(
            dates[dates["_full_date_obj"] == cost_full]["DateKey"].iloc[0]
        )
        rate_date_str = cost_full.isoformat()
        rate_date_key = cost_date_key

        # --- Cost category and subcategory ---
        cost_category = str(RNG.choice(CATEGORIES, p=CATEGORY_WEIGHT_LIST))
        cost_subcategory = str(
            RNG.choice(COST_CATEGORY_SUBCATEGORY[cost_category])
        )

        # --- Currency ---
        currency_keys = list(valid_currency_keys)
        currency_weights = [10 if k == currency_code_to_key["USD"] else 1
                            for k in currency_keys]
        currency_weights = np.array(currency_weights, dtype=float)
        currency_weights = currency_weights / currency_weights.sum()
        currency_key = int(RNG.choice(currency_keys, p=currency_weights))
        currency_code = currency_key_to_code[currency_key]

        # --- Business keys ---
        cost_line_id = f"CL{operating_cost_key:08d}"
        source_document_number = f"SD{operating_cost_key:08d}"
        composite_key = (
            flight_operation_key,
            cost_category,
            cost_subcategory,
            cost_date_key,
            source_document_number,
        )
        if cost_line_id in used_business_keys:
            continue  # enforce business-key uniqueness
        if composite_key in used_composite_keys:
            continue  # enforce grain uniqueness
        used_business_keys.add(cost_line_id)
        used_composite_keys.add(composite_key)

        # --- Signed cost amount (contract Section 10.4) ---
        # Positive = expense; negative = credit or rebate/reversal.
        if RNG.random() < CREDIT_REVERSAL_SHARE:
            cost_amount = round(
                float(RNG.uniform(abs(CREDIT_AMOUNT_MAX), abs(CREDIT_AMOUNT_MIN))),
                2
            )
            cost_amount = -cost_amount  # make negative
        else:
            cost_amount = round(
                float(RNG.uniform(COST_AMOUNT_MIN, COST_AMOUNT_MAX)), 2
            )

        # --- FX lookup (exact date, no forward-fill) ---
        fx_key = (currency_code, rate_date_str)
        if fx_key not in fx_lookup:
            # Quarantine: missing exact-date rate. Do not forward-fill.
            quarantined.append({
                "OperatingCostKey": operating_cost_key,
                "CostLineID": cost_line_id,
                "FlightOperationKey": flight_operation_key,
                "AirlineKey": airline_key,
                "RouteKey": route_key,
                "CostDateKey": cost_date_key,
                "CostCategory": cost_category,
                "CostSubcategory": cost_subcategory,
                "CurrencyKey": currency_key,
                "CurrencyCode": currency_code,
                "RateDateKey": rate_date_key,
                "RateDate": rate_date_str,
                "CostAmount": cost_amount,
                "QuarantineReason": "MISSING_FX_RATE",
                "QuarantineRuleID": "OD-04e",
                "SyntheticProvenance": SYNTHETIC_PROVENANCE,
            })
            operating_cost_key += 1
            continue

        exchange_rate_to_usd = fx_lookup[fx_key]

        # --- USD conversion (OD-04b: rate not rounded before multiply;
        # final amount rounded to 2 decimals; same sign as original) ---
        cost_amount_usd = float(Decimal(
            str(cost_amount * exchange_rate_to_usd)
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

        # --- Cost description (synthetic, no personal data) ---
        cost_description = (
            f"Synthetic {cost_category.lower()} cost — "
            f"{cost_subcategory} — {currency_code} ledger line"
        )

        # --- Allocation flag ---
        is_allocated = bool(RNG.random() < ALLOCATED_SHARE)

        record = {
            "OperatingCostKey": operating_cost_key,
            "CostLineID": cost_line_id,
            "FlightOperationKey": flight_operation_key,
            "AirlineKey": airline_key,
            "RouteKey": route_key,
            "CostDateKey": cost_date_key,
            "CostCategory": cost_category,
            "CostSubcategory": cost_subcategory,
            "CostAmount": Decimal(str(cost_amount)),
            "CurrencyKey": currency_key,
            "ExchangeRateToUSD": Decimal(str(round(exchange_rate_to_usd, 6))),
            "RateDateKey": rate_date_key,
            "RateVersion": RATE_VERSION,
            "CostAmountUSD": Decimal(str(cost_amount_usd)),
            "CostDescription": cost_description,
            "SourceDocumentNumber": source_document_number,
            "IsAllocated": is_allocated,
            "SyntheticProvenance": SYNTHETIC_PROVENANCE,
        }

        records.append(record)
        operating_cost_key += 1

# ---------------------------------------------------------------------------
# Build DataFrame and apply dtypes
# ---------------------------------------------------------------------------
df = pd.DataFrame(records, columns=COLUMNS)

if len(df) == 0:
    raise RuntimeError("No operating cost lines generated.")

df = df.astype({
    "OperatingCostKey": "int64",
    "CostLineID": "string",
    "FlightOperationKey": "int64",
    "AirlineKey": "int32",
    "RouteKey": "int32",
    "CostDateKey": "int32",
    "CostCategory": "string",
    "CostSubcategory": "string",
    "CostAmount": "float64",   # signed; 2 dp
    "CurrencyKey": "int32",
    "ExchangeRateToUSD": "float64",  # 6 dp
    "RateDateKey": "int32",
    "RateVersion": "string",
    "CostAmountUSD": "float64",  # signed; 2 dp
    "CostDescription": "string",
    "SourceDocumentNumber": "string",
    "IsAllocated": "bool",
    "SyntheticProvenance": "string",
})

# Round monetary columns to exactly 2 decimals; rate to 6 decimals.
money_cols_2dp = ["CostAmount", "CostAmountUSD"]
for col in money_cols_2dp:
    df[col] = df[col].round(2)
df["ExchangeRateToUSD"] = df["ExchangeRateToUSD"].round(6)

# ---------------------------------------------------------------------------
# Structural and business-rule validation
# ---------------------------------------------------------------------------
assert list(df.columns) == COLUMNS, "Column order mismatch."
assert df["OperatingCostKey"].is_unique, "OperatingCostKey must be unique."
assert df["CostLineID"].is_unique, "CostLineID must be unique."
assert not df.duplicated(
    ["FlightOperationKey", "CostCategory", "CostSubcategory",
     "CostDateKey", "SourceDocumentNumber"]
).any(), "Composite grain key must be unique."

# FK resolution.
assert set(df["FlightOperationKey"].astype(int)).issubset(
    valid_flight_operation_keys
), "FlightOperationKey logical reference must resolve."
assert set(df["AirlineKey"].astype(int)).issubset(
    valid_airline_keys
), "AirlineKey FK must resolve."
assert set(df["RouteKey"].astype(int)).issubset(
    valid_route_keys
), "RouteKey FK must resolve."
assert set(df["CostDateKey"].astype(int)).issubset(
    valid_date_keys
), "CostDateKey FK must resolve."
assert set(df["RateDateKey"].astype(int)).issubset(
    valid_date_keys
), "RateDateKey FK must resolve."
assert set(df["CurrencyKey"].astype(int)).issubset(
    valid_currency_keys
), "CurrencyKey FK must resolve."

# RouteKey and AirlineKey agree with flight leg.
for _, row in df.iterrows():
    ffo_airline = int(ffo_by_key.loc[int(row["FlightOperationKey"]), "AirlineKey"])
    ffo_route = int(ffo_by_key.loc[int(row["FlightOperationKey"]), "RouteKey"])
    assert int(row["AirlineKey"]) == ffo_airline, \
        f"AirlineKey mismatch for OperatingCostKey {row['OperatingCostKey']}"
    assert int(row["RouteKey"]) == ffo_route, \
        f"RouteKey mismatch for OperatingCostKey {row['OperatingCostKey']}"

# CostDateKey within reporting period.
assert (df["CostDateKey"] >= int(reporting_start_date.strftime("%Y%m%d"))).all(), \
    "CostDateKey must be within reporting period."
assert (df["CostDateKey"] <= int(reporting_end_date.strftime("%Y%m%d"))).all(), \
    "CostDateKey must be within reporting period."

# ExchangeRateToUSD positive.
assert (df["ExchangeRateToUSD"] > 0).all(), "ExchangeRateToUSD must be positive."

# RateVersion consistent.
assert (df["RateVersion"] == RATE_VERSION).all(), "RateVersion must be consistent."

# CostCategory within controlled set.
assert set(df["CostCategory"]).issubset(set(CATEGORIES)), \
    "CostCategory must be from controlled set."

# CostSubcategory valid within category.
for _, row in df.iterrows():
    assert row["CostSubcategory"] in COST_CATEGORY_SUBCATEGORY[row["CostCategory"]], \
        f"CostSubcategory {row['CostSubcategory']} invalid for category {row['CostCategory']}"

# CostAmountUSD follows sign of CostAmount.
assert (
    (df["CostAmount"] >= 0) == (df["CostAmountUSD"] >= 0)
).all(), "CostAmountUSD must follow sign of CostAmount."
assert (
    (df["CostAmount"] < 0) == (df["CostAmountUSD"] < 0)
).all(), "CostAmountUSD must follow sign of CostAmount (negative)."

# USD conversion accuracy: CostAmount * Rate == CostAmountUSD within 0.01.
usd_check = (df["CostAmount"] * df["ExchangeRateToUSD"]).round(2)
assert (
    (df["CostAmountUSD"] - usd_check).abs() <= 0.01
).all(), "CostAmountUSD conversion accuracy check failed."

# CostDescription not null, no personal data markers.
assert df["CostDescription"].notna().all()
assert df["CostDescription"].str.len().max() <= 200

# SourceDocumentNumber not null.
assert df["SourceDocumentNumber"].notna().all()

# Synthetic provenance present.
assert (df["SyntheticProvenance"] == SYNTHETIC_PROVENANCE).all()

# All monetary values finite.
for col in money_cols_2dp + ["ExchangeRateToUSD"]:
    assert df[col].notna().all(), f"{col} must not contain nulls."

# ---------------------------------------------------------------------------
# Round-trip and write outputs
# ---------------------------------------------------------------------------
df.to_csv(CSV, index=False, encoding="utf-8")

schema = pa.schema([
    pa.field("OperatingCostKey", pa.int64(), nullable=False),
    pa.field("CostLineID", pa.string(), nullable=False),
    pa.field("FlightOperationKey", pa.int64(), nullable=False),
    pa.field("AirlineKey", pa.int32(), nullable=False),
    pa.field("RouteKey", pa.int32(), nullable=False),
    pa.field("CostDateKey", pa.int32(), nullable=False),
    pa.field("CostCategory", pa.string(), nullable=False),
    pa.field("CostSubcategory", pa.string(), nullable=False),
    pa.field("CostAmount", pa.float64(), nullable=False),
    pa.field("CurrencyKey", pa.int32(), nullable=False),
    pa.field("ExchangeRateToUSD", pa.float64(), nullable=False),
    pa.field("RateDateKey", pa.int32(), nullable=False),
    pa.field("RateVersion", pa.string(), nullable=False),
    pa.field("CostAmountUSD", pa.float64(), nullable=False),
    pa.field("CostDescription", pa.string(), nullable=False),
    pa.field("SourceDocumentNumber", pa.string(), nullable=False),
    pa.field("IsAllocated", pa.bool_(), nullable=False),
    pa.field("SyntheticProvenance", pa.string(), nullable=False),
])

table = pa.Table.from_pandas(
    df,
    schema=schema,
    preserve_index=False,
    safe=True,
)
pq.write_table(table, PARQUET, compression="snappy")

# Round-trip checks.
csv_check = pd.read_csv(CSV, encoding="utf-8")
parquet_check = pd.read_parquet(PARQUET)
parquet_schema = pq.read_schema(PARQUET)

assert csv_check.shape == df.shape
assert parquet_check.shape == df.shape
assert list(parquet_check.columns) == COLUMNS
assert parquet_check["OperatingCostKey"].is_unique
assert parquet_check["CostLineID"].is_unique

# ---------------------------------------------------------------------------
# Write quarantine file (missing FX rates)
# ---------------------------------------------------------------------------
if len(quarantined) > 0:
    qdf = pd.DataFrame(quarantined)
    qdf.to_csv(QUARANTINE_CSV, index=False, encoding="utf-8")
else:
    pd.DataFrame(columns=[
        "OperatingCostKey", "CostLineID", "FlightOperationKey", "AirlineKey",
        "RouteKey", "CostDateKey", "CostCategory", "CostSubcategory",
        "CurrencyKey", "CurrencyCode", "RateDateKey", "RateDate",
        "CostAmount", "QuarantineReason", "QuarantineRuleID",
        "SyntheticProvenance",
    ]).to_csv(QUARANTINE_CSV, index=False, encoding="utf-8")

# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------
manifest = {
    "dataset": "FactOperatingCosts",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": SYNTHETIC_PROVENANCE,
    "grain": "One row per operating-cost ledger line",
    "primary_key": "OperatingCostKey",
    "business_key": "CostLineID",
    "composite_grain_key": (
        "FlightOperationKey + CostCategory + CostSubcategory + "
        "CostDateKey + SourceDocumentNumber"
    ),
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "source_dimensions": {
        "fact_flight_operations": {
            "path": "data/03_curated/fact_flight_operations.parquet",
            "sha256": sha256_file(FFO_PATH),
            "rows": int(ffo.shape[0]),
        },
        "dim_airline": {
            "path": "data/03_curated/dim_airline.parquet",
            "sha256": sha256_file(AIRLINE_PATH),
            "rows": int(airlines.shape[0]),
        },
        "dim_route": {
            "path": "data/03_curated/dim_route.parquet",
            "sha256": sha256_file(ROUTE_PATH),
            "rows": int(routes.shape[0]),
        },
        "dim_date": {
            "path": "data/03_curated/dim_date.parquet",
            "sha256": sha256_file(DATE_PATH),
            "rows": int(dates.shape[0]),
        },
        "dim_currency": {
            "path": "data/03_curated/dim_currency.parquet",
            "sha256": sha256_file(CURRENCY_PATH),
            "rows": int(currencies.shape[0]),
        },
        "ref_exchange_rates": {
            "path": "data/04_reference/ref_exchange_rates.csv",
            "sha256": sha256_file(FX_PATH),
            "rows": int(fx.shape[0]),
        },
    },
    "generation": {
        "method": "Deterministic NumPy random generator",
        "random_seed": SEED,
        "cost_lines_per_flight_min": COST_LINES_PER_FLIGHT_MIN,
        "cost_lines_per_flight_max": COST_LINES_PER_FLIGHT_MAX,
        "reporting_period_start": REPORTING_START,
        "reporting_period_end": REPORTING_END,
        "rate_source": RATE_SOURCE,
        "rate_version": RATE_VERSION,
        "credit_reversal_share": CREDIT_REVERSAL_SHARE,
        "allocated_share": ALLOCATED_SHARE,
        "fx_lookup_coverage_start": "2025-10-01",
        "fx_lookup_coverage_end": "2026-09-30",
    },
    "governance": {
        "od_04a_currency_scope": "AED, QAR, SGD, INR, GBP, EUR, USD, AUD",
        "od_04b_exchange_rate_convention": (
            "USD per one unit; exact-date lookup; 6 decimal places for rate; "
            "round final converted amount to 2 decimals; no forward-fill"
        ),
        "od_04c_rate_source": RATE_SOURCE,
        "od_04d_rate_version": RATE_VERSION,
        "od_04e_missing_date_behaviour": (
            "No forward-fill; missing exact-date rate quarantines the row"
        ),
        "od_04f_rate_generation_methodology": (
            "Deterministic algorithmic generation; fixed seed; documented parameters"
        ),
        "gov_d_07_manifest_hash": (
            "GOV-D-07 ManifestHash canonicalization is a REVISED DRAFT, "
            "not approved. No ManifestHash canonicalization method is "
            "introduced. File-level SHA-256 hashes follow the existing "
            "project manifest convention (src/utilities/hashing.py)."
        ),
    },
    "quarantine": {
        "quarantined_row_count": len(quarantined),
        "quarantine_reason": "MISSING_FX_RATE (OD-04e: no forward-fill)",
        "quarantine_file": "data/02_staging/quarantine/fact_operating_costs_quarantined.csv",
    },
    "validation": {
        "exact_column_order": True,
        "unique_operating_cost_keys": True,
        "unique_cost_line_ids": True,
        "unique_composite_grain_key": True,
        "flight_operation_logical_references_resolve": True,
        "airline_foreign_keys_resolve": True,
        "route_foreign_keys_resolve": True,
        "cost_date_key_foreign_key_resolves": True,
        "rate_date_key_foreign_key_resolves": True,
        "currency_foreign_keys_resolve": True,
        "route_key_matches_flight_leg": True,
        "airline_key_matches_flight_leg": True,
        "cost_date_within_reporting_period": True,
        "exchange_rate_positive": True,
        "rate_version_consistent": True,
        "cost_category_controlled_set": True,
        "cost_subcategory_valid_within_category": True,
        "cost_amount_usd_follows_sign": True,
        "usd_conversion_accuracy": True,
        "cost_description_not_null": True,
        "source_document_number_not_null": True,
        "no_null_monetary_values": True,
        "synthetic_provenance_present": True,
        "csv_round_trip": True,
        "parquet_round_trip": True,
        "missing_fx_rate_quarantined": True,
    },
    "files": {
        "csv": {
            "path": "data/03_curated/fact_operating_costs.csv",
            "sha256": sha256_file(CSV),
        },
        "parquet": {
            "path": "data/03_curated/fact_operating_costs.parquet",
            "sha256": sha256_file(PARQUET),
        },
        "quarantine": {
            "path": "data/02_staging/quarantine/fact_operating_costs_quarantined.csv",
            "sha256": sha256_file(QUARANTINE_CSV),
        },
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
}

write_json_atomic(MANIFEST, manifest)

print("FACT_OPERATING_COSTS_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("QUARANTINED (missing FX):", len(quarantined))
print("UNIQUE OPERATING COST KEYS:", df["OperatingCostKey"].nunique())
print("UNIQUE COST LINE IDS:", df["CostLineID"].nunique())
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("QUARANTINE:", QUARANTINE_CSV)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
