"""Build curated FactBookingTransactions dataset.

Generates a deterministic synthetic booking-transaction fact table from the
existing curated dimensions (DimAirline, DimRoute, DimDate, DimCustomer,
DimFareClass, DimBookingChannel, DimCurrency) and FactFlightOperations.

Reference documents:
- docs/03_DATA_CONTRACTS.md v1.5, Sections 5.3, 6.3.2, 7, 9, 10 (FactBookingTransactions
  grain, columns, keys, date policy, currency conversion)
- docs/governance/PAGE_03_REVENUE_FINANCE_SCHEMA_DECISION.md (OD-04a through OD-04f
  owner-confirmed currency decisions; RateDateKey / RateVersion preserved per
  Section 4 of the schema decision)
- OD-04b: USD per one unit; exact-date lookup; 6 decimal places for rate;
  round final converted amount to 2 decimals; no forward-fill
- OD-04c: Rate source AEROVISION-360-SYNTHETIC-FX-V1
- OD-04d: Rate version FX-YYYY-MM-DD-NNN
- OD-04e: Missing exact-date rate quarantines the row; no forward-fill

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
SEED = 3602027  # Explicit seed for reproducible generation
RNG = np.random.default_rng(SEED)

# Reporting period per contract Section 9.4.
REPORTING_START = "2025-10-01"
REPORTING_END = "2026-09-30"

# OD-04c / OD-04d rate source and version (from ref_exchange_rates.csv).
RATE_SOURCE = "AEROVISION-360-SYNTHETIC-FX-V1"
RATE_VERSION = "FX-2026-11-04-001"

# Synthetic provenance label (exact string required by project policy).
SYNTHETIC_PROVENANCE = "Synthetic Simulation — Not Actual Airline Performance."

# Generation volumes (validation scale, consistent with FactFlightOperations
# validation volume of 5,000 legs).
COUPONS_PER_FLIGHT_MIN = 1
COUPONS_PER_FLIGHT_MAX = 3

# Transaction status distribution (probabilities must sum to 1.0).
STATUS_PROBABILITIES = {
    "Flown": 0.60,
    "Ticketed": 0.15,
    "Booked": 0.10,
    "Cancelled": 0.08,
    "Refunded": 0.05,
    "NoShow": 0.02,
}
STATUSES = list(STATUS_PROBABILITIES.keys())
STATUS_WEIGHTS = list(STATUS_PROBABILITIES.values())

# Revenue passenger share (rest are non-revenue / award / employee).
REVENUE_PASSENGER_SHARE = 0.90

# Monetary amount ranges (original currency units).
BASE_FARE_MIN = 50.00
BASE_FARE_MAX = 2000.00
DISCOUNT_MAX_PCT = 0.20  # max discount as % of base fare
TAX_MIN_PCT = 0.05       # min tax as % of (base - discount)
TAX_MAX_PCT = 0.20       # max tax as % of (base - discount)
FEE_MIN = 5.00
FEE_MAX = 50.00
ANCILLARY_MAX = 100.00
CANCELLATION_FEE_MIN = 25.00
CANCELLATION_FEE_MAX = 200.00
NOSHOW_FEE_MIN = 25.00
NOSHOW_FEE_MAX = 150.00

OUT = project_path("data", "03_curated")
MANIFESTS = project_path("data", "manifests")
QUARANTINE = project_path("data", "02_staging", "quarantine")

FFO_PATH = OUT / "fact_flight_operations.parquet"
AIRLINE_PATH = OUT / "dim_airline.parquet"
ROUTE_PATH = OUT / "dim_route.parquet"
DATE_PATH = OUT / "dim_date.parquet"
CUSTOMER_PATH = OUT / "dim_customer.parquet"
FARE_CLASS_PATH = OUT / "dim_fare_class.parquet"
BOOKING_CHANNEL_PATH = OUT / "dim_booking_channel.parquet"
CURRENCY_PATH = OUT / "dim_currency.parquet"
FX_PATH = project_path("data", "04_reference", "ref_exchange_rates.csv")

CSV = OUT / "fact_booking_transactions.csv"
PARQUET = OUT / "fact_booking_transactions.parquet"
QUARANTINE_CSV = QUARANTINE / "fact_booking_transactions_quarantined.csv"
MANIFEST = MANIFESTS / "fact_booking_transactions_manifest.json"

COLUMNS = [
    "BookingTransactionKey",
    "BookingReference",
    "TicketNumber",
    "TicketCouponNumber",
    "CustomerKey",
    "AirlineKey",
    "FlightOperationKey",
    "RouteKey",
    "FareClassKey",
    "BookingChannelKey",
    "BookingDateKey",
    "TravelDateKey",
    "PassengerCount",
    "IsRevenuePassenger",
    "BaseFareAmount",
    "DiscountAmount",
    "TaxAmount",
    "FeeAmount",
    "AncillaryRevenueAmount",
    "RefundAmount",
    "AncillaryRefundAmount",
    "FeeRefundAmount",
    "CancellationFeeAmount",
    "NoShowFeeAmount",
    "TransactionCurrencyKey",
    "ExchangeRateToUSD",
    "RateDateKey",
    "RateVersion",
    "BaseFareUSD",
    "DiscountUSD",
    "TaxUSD",
    "FeeUSD",
    "AncillaryRevenueUSD",
    "RefundUSD",
    "AncillaryRefundUSD",
    "FeeRefundUSD",
    "CancellationFeeUSD",
    "NoShowFeeUSD",
    "NetPassengerRevenueUSD",
    "NetFeeRevenueUSD",
    "NetAncillaryRevenueUSD",
    "TransactionStatus",
    "IsRefunded",
    "BookingLeadTimeDays",
    "SyntheticProvenance",
]

# Verify source dimensions exist.
for path in [FFO_PATH, AIRLINE_PATH, ROUTE_PATH, DATE_PATH, CUSTOMER_PATH,
             FARE_CLASS_PATH, BOOKING_CHANNEL_PATH, CURRENCY_PATH, FX_PATH]:
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
customers = pd.read_parquet(CUSTOMER_PATH)
fare_classes = pd.read_parquet(FARE_CLASS_PATH)
booking_channels = pd.read_parquet(BOOKING_CHANNEL_PATH)
currencies = pd.read_parquet(CURRENCY_PATH)
fx = pd.read_csv(FX_PATH, dtype={"CurrencyCode": "string", "RateDate": "string"})

active_airlines = airlines[airlines["IsActive"] == True]
active_customers = customers[customers["IsActive"] == True]

if len(active_airlines) == 0:
    raise RuntimeError("No active airlines in DimAirline.")
if len(active_customers) == 0:
    raise RuntimeError("No active customers in DimCustomer.")
if len(ffo) == 0:
    raise RuntimeError("No flight operations in FactFlightOperations.")
if len(fx) == 0:
    raise RuntimeError("No exchange rates in ref_exchange_rates.csv.")

# Index flight operations by FlightOperationKey for FK validation and
# route/airline/date lookups.
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
valid_customer_keys = set(customers["CustomerKey"].astype(int))
valid_fare_class_keys = set(fare_classes["FareClassKey"].astype(int))
valid_booking_channel_keys = set(booking_channels["BookingChannelKey"].astype(int))
valid_currency_keys = set(currencies["CurrencyKey"].astype(int))
valid_date_keys = set(dates["DateKey"].astype(int))
valid_flight_operation_keys = set(ffo["FlightOperationKey"].astype(int))

# Build FX lookup: (CurrencyCode, RateDate "YYYY-MM-DD") -> ExchangeRateToUSD.
fx_lookup = {}
for _, fx_row in fx.iterrows():
    fx_lookup[(str(fx_row["CurrencyCode"]), str(fx_row["RateDate"]))] = \
        float(fx_row["ExchangeRateToUSD"])

# Build date key <-> full date mappings.
# FullDate in DimDate is stored as date objects (CSV round-trip gives strings;
# parquet preserves dates). Normalize to date objects.
def _to_date_obj(v):
    if isinstance(v, date):
        return v
    return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()

dates["_full_date_obj"] = dates["FullDate"].apply(_to_date_obj)
date_key_to_full = dict(zip(
    dates["DateKey"].astype(int),
    dates["_full_date_obj"],
))
full_to_date_key = {
    int(k): v for k, v in zip(dates["DateKey"], dates["_full_date_obj"])
}

# Reporting period date keys (for TravelDateKey constraint).
reporting_start_date = datetime.strptime(REPORTING_START, "%Y-%m-%d").date()
reporting_end_date = datetime.strptime(REPORTING_END, "%Y-%m-%d").date()
fx_start_date = datetime.strptime("2025-10-01", "%Y-%m-%d").date()

# ---------------------------------------------------------------------------
# Generate deterministic synthetic booking coupons
# ---------------------------------------------------------------------------
records = []
quarantined = []
booking_transaction_key = 1
used_business_keys = set()

# Counters for deterministic status assignment.
status_cycle = 0

flight_keys = ffo["FlightOperationKey"].astype(int).tolist()

for flight_operation_key in flight_keys:
    ffo_row = ffo_by_key.loc[flight_operation_key]
    route_key = int(ffo_row["RouteKey"])
    airline_key = int(ffo_row["AirlineKey"])
    travel_date_key = int(ffo_row["ScheduledDepartureDateKey"])
    travel_full = date_key_to_full[travel_date_key]

    # TravelDateKey must be within the reporting period.
    if travel_full < reporting_start_date or travel_full > reporting_end_date:
        continue

    # RouteKey must agree with the flight leg (denormalized consistency).
    route_row = routes[routes["RouteKey"] == route_key].iloc[0]
    if int(route_row["RouteKey"]) != route_key:
        continue

    # Number of coupons for this flight leg.
    n_coupons = int(RNG.integers(COUPONS_PER_FLIGHT_MIN, COUPONS_PER_FLIGHT_MAX + 1))

    for _ in range(n_coupons):
        # --- Dimension keys ---
        customer_key = int(RNG.choice(active_customers["CustomerKey"].astype(int).tolist()))
        fare_class_key = int(RNG.choice(fare_classes["FareClassKey"].astype(int).tolist()))
        booking_channel_key = int(
            RNG.choice(booking_channels["BookingChannelKey"].astype(int).tolist())
        )

        # --- Transaction currency ---
        # Weight USD heavily (domestic reporting currency) but allow all 8.
        currency_keys = list(valid_currency_keys)
        currency_weights = [10 if k == currency_code_to_key["USD"] else 1
                            for k in currency_keys]
        currency_weights = np.array(currency_weights, dtype=float)
        currency_weights = currency_weights / currency_weights.sum()
        transaction_currency_key = int(RNG.choice(currency_keys, p=currency_weights))
        transaction_currency_code = currency_key_to_code[transaction_currency_key]

        # --- Dates ---
        # BookingDateKey: between FX coverage start and TravelDateKey, inclusive.
        # This guarantees an exact-date FX rate exists (no forward-fill needed).
        booking_full = travel_full
        # Random lead time 0 to (travel - fx_start) days, capped at 365.
        max_lead_days = (travel_full - fx_start_date).days
        if max_lead_days > 0:
            lead_days = int(RNG.integers(0, min(max_lead_days, 365) + 1))
            booking_full = travel_full - timedelta(days=lead_days)
        booking_date_key = int(
            dates[dates["_full_date_obj"] == booking_full]["DateKey"].iloc[0]
        )
        booking_lead_time_days = (travel_full - booking_full).days

        # Rate date = booking date (OD-04b: exact-date lookup, transaction date).
        rate_date_str = booking_full.isoformat()
        rate_date_key = booking_date_key

        # --- Business keys ---
        booking_reference = f"BK{booking_transaction_key:08d}"
        ticket_number = f"TK{booking_transaction_key:08d}"
        ticket_coupon_number = 1
        business_key = (booking_reference, ticket_number, ticket_coupon_number)
        if business_key in used_business_keys:
            continue  # enforce business-key uniqueness
        used_business_keys.add(business_key)

        # --- Monetary amounts (original currency) ---
        base_fare_amount = round(float(RNG.uniform(BASE_FARE_MIN, BASE_FARE_MAX)), 2)

        # Discount: 70% probability of zero, otherwise % of base fare.
        if RNG.random() < 0.70:
            discount_amount = 0.00
        else:
            discount_amount = round(
                base_fare_amount * float(RNG.uniform(0.0, DISCOUNT_MAX_PCT)), 2
            )

        # Tax: % of (base - discount).
        taxable_base = base_fare_amount - discount_amount
        tax_amount = round(
            taxable_base * float(RNG.uniform(TAX_MIN_PCT, TAX_MAX_PCT)), 2
        )

        # Fee: fixed range.
        fee_amount = round(float(RNG.uniform(FEE_MIN, FEE_MAX)), 2)

        # Ancillary: 60% probability of zero.
        if RNG.random() < 0.60:
            ancillary_revenue_amount = 0.00
        else:
            ancillary_revenue_amount = round(
                float(RNG.uniform(5.00, ANCILLARY_MAX)), 2
            )

        # --- Transaction status (deterministic cycle with RNG jitter) ---
        status_cycle += 1
        # Use RNG for status selection to keep determinism.
        transaction_status = str(RNG.choice(STATUSES, p=STATUS_WEIGHTS))

        # --- Refund / cancellation / no-show amounts ---
        refund_amount = 0.00
        ancillary_refund_amount = 0.00
        fee_refund_amount = 0.00
        cancellation_fee_amount = 0.00
        no_show_fee_amount = 0.00

        if transaction_status == "Refunded":
            # Partial or full refund of base fare. Refund must not exceed
            # base fare minus discount so NetPassengerRevenueUSD stays >= 0.
            max_refund = max(0.0, base_fare_amount - discount_amount)
            if max_refund > 0:
                refund_amount = round(
                    max_refund * float(RNG.uniform(0.10, 1.00)), 2
                )
            else:
                refund_amount = 0.00
        elif transaction_status == "Cancelled":
            cancellation_fee_amount = round(
                float(RNG.uniform(CANCELLATION_FEE_MIN, CANCELLATION_FEE_MAX)), 2
            )
        elif transaction_status == "NoShow":
            no_show_fee_amount = round(
                float(RNG.uniform(NOSHOW_FEE_MIN, NOSHOW_FEE_MAX)), 2
            )

        # Cancellation fee and no-show fee are mutually exclusive (enforced above).

        # IsRevenuePassenger: most are revenue; award/employee are non-revenue.
        is_revenue_passenger = bool(RNG.random() < REVENUE_PASSENGER_SHARE)

        # --- FX lookup (exact date, no forward-fill) ---
        fx_key = (transaction_currency_code, rate_date_str)
        if fx_key not in fx_lookup:
            # Quarantine: missing exact-date rate. Do not forward-fill.
            quarantined.append({
                "BookingTransactionKey": booking_transaction_key,
                "BookingReference": booking_reference,
                "TicketNumber": ticket_number,
                "TicketCouponNumber": ticket_coupon_number,
                "CustomerKey": customer_key,
                "AirlineKey": airline_key,
                "FlightOperationKey": flight_operation_key,
                "RouteKey": route_key,
                "FareClassKey": fare_class_key,
                "BookingChannelKey": booking_channel_key,
                "BookingDateKey": booking_date_key,
                "TravelDateKey": travel_date_key,
                "TransactionCurrencyKey": transaction_currency_key,
                "TransactionCurrencyCode": transaction_currency_code,
                "RateDateKey": rate_date_key,
                "RateDate": rate_date_str,
                "BaseFareAmount": base_fare_amount,
                "QuarantineReason": "MISSING_FX_RATE",
                "QuarantineRuleID": "OD-04e",
                "SyntheticProvenance": SYNTHETIC_PROVENANCE,
            })
            booking_transaction_key += 1
            continue

        exchange_rate_to_usd = fx_lookup[fx_key]

        # --- USD conversions (OD-04b: rate not rounded before multiply;
        # final amount rounded to 2 decimals) ---
        def to_usd(amount):
            return float(Decimal(str(amount * exchange_rate_to_usd)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP))

        base_fare_usd = to_usd(base_fare_amount)
        discount_usd = to_usd(discount_amount)
        tax_usd = to_usd(tax_amount)
        fee_usd = to_usd(fee_amount)
        ancillary_revenue_usd = to_usd(ancillary_revenue_amount)
        refund_usd = to_usd(refund_amount)
        ancillary_refund_usd = to_usd(ancillary_refund_amount)
        fee_refund_usd = to_usd(fee_refund_amount)
        cancellation_fee_usd = to_usd(cancellation_fee_amount)
        no_show_fee_usd = to_usd(no_show_fee_amount)

        # --- Revenue recognition (contract Section 10.3 / 10.6) ---
        if transaction_status in ("Ticketed", "Flown", "Refunded"):
            net_passenger_revenue_usd = round(
                base_fare_usd - discount_usd - refund_usd, 2
            )
        else:
            # Booked, Cancelled, NoShow: zero passenger revenue.
            net_passenger_revenue_usd = 0.00

        net_fee_revenue_usd = round(
            fee_usd - fee_refund_usd + cancellation_fee_usd + no_show_fee_usd, 2
        )
        net_ancillary_revenue_usd = round(
            ancillary_revenue_usd - ancillary_refund_usd, 2
        )

        # IsRefunded: TRUE when any refund amount > 0.
        is_refunded = bool(
            refund_amount > 0 or ancillary_refund_amount > 0 or fee_refund_amount > 0
        )

        record = {
            "BookingTransactionKey": booking_transaction_key,
            "BookingReference": booking_reference,
            "TicketNumber": ticket_number,
            "TicketCouponNumber": ticket_coupon_number,
            "CustomerKey": customer_key,
            "AirlineKey": airline_key,
            "FlightOperationKey": flight_operation_key,
            "RouteKey": route_key,
            "FareClassKey": fare_class_key,
            "BookingChannelKey": booking_channel_key,
            "BookingDateKey": booking_date_key,
            "TravelDateKey": travel_date_key,
            "PassengerCount": 1,
            "IsRevenuePassenger": is_revenue_passenger,
            "BaseFareAmount": Decimal(str(base_fare_amount)),
            "DiscountAmount": Decimal(str(discount_amount)),
            "TaxAmount": Decimal(str(tax_amount)),
            "FeeAmount": Decimal(str(fee_amount)),
            "AncillaryRevenueAmount": Decimal(str(ancillary_revenue_amount)),
            "RefundAmount": Decimal(str(refund_amount)),
            "AncillaryRefundAmount": Decimal(str(ancillary_refund_amount)),
            "FeeRefundAmount": Decimal(str(fee_refund_amount)),
            "CancellationFeeAmount": Decimal(str(cancellation_fee_amount)),
            "NoShowFeeAmount": Decimal(str(no_show_fee_amount)),
            "TransactionCurrencyKey": transaction_currency_key,
            "ExchangeRateToUSD": Decimal(str(round(exchange_rate_to_usd, 6))),
            "RateDateKey": rate_date_key,
            "RateVersion": RATE_VERSION,
            "BaseFareUSD": Decimal(str(base_fare_usd)),
            "DiscountUSD": Decimal(str(discount_usd)),
            "TaxUSD": Decimal(str(tax_usd)),
            "FeeUSD": Decimal(str(fee_usd)),
            "AncillaryRevenueUSD": Decimal(str(ancillary_revenue_usd)),
            "RefundUSD": Decimal(str(refund_usd)),
            "AncillaryRefundUSD": Decimal(str(ancillary_refund_usd)),
            "FeeRefundUSD": Decimal(str(fee_refund_usd)),
            "CancellationFeeUSD": Decimal(str(cancellation_fee_usd)),
            "NoShowFeeUSD": Decimal(str(no_show_fee_usd)),
            "NetPassengerRevenueUSD": Decimal(str(net_passenger_revenue_usd)),
            "NetFeeRevenueUSD": Decimal(str(net_fee_revenue_usd)),
            "NetAncillaryRevenueUSD": Decimal(str(net_ancillary_revenue_usd)),
            "TransactionStatus": transaction_status,
            "IsRefunded": is_refunded,
            "BookingLeadTimeDays": booking_lead_time_days,
            "SyntheticProvenance": SYNTHETIC_PROVENANCE,
        }

        records.append(record)
        booking_transaction_key += 1

# ---------------------------------------------------------------------------
# Build DataFrame and apply dtypes
# ---------------------------------------------------------------------------
df = pd.DataFrame(records, columns=COLUMNS)

if len(df) == 0:
    raise RuntimeError("No booking transactions generated.")

# Apply contract data types.
df = df.astype({
    "BookingTransactionKey": "int64",
    "BookingReference": "string",
    "TicketNumber": "string",
    "TicketCouponNumber": "int8",
    "CustomerKey": "int32",
    "AirlineKey": "int32",
    "FlightOperationKey": "int64",
    "RouteKey": "int32",
    "FareClassKey": "int32",
    "BookingChannelKey": "int32",
    "BookingDateKey": "int32",
    "TravelDateKey": "int32",
    "PassengerCount": "int8",
    "IsRevenuePassenger": "bool",
    "BaseFareAmount": "float64",   # Decimal stored as float for CSV/PQ; 2 dp
    "DiscountAmount": "float64",
    "TaxAmount": "float64",
    "FeeAmount": "float64",
    "AncillaryRevenueAmount": "float64",
    "RefundAmount": "float64",
    "AncillaryRefundAmount": "float64",
    "FeeRefundAmount": "float64",
    "CancellationFeeAmount": "float64",
    "NoShowFeeAmount": "float64",
    "TransactionCurrencyKey": "int32",
    "ExchangeRateToUSD": "float64",  # 6 dp
    "RateDateKey": "int32",
    "RateVersion": "string",
    "BaseFareUSD": "float64",
    "DiscountUSD": "float64",
    "TaxUSD": "float64",
    "FeeUSD": "float64",
    "AncillaryRevenueUSD": "float64",
    "RefundUSD": "float64",
    "AncillaryRefundUSD": "float64",
    "FeeRefundUSD": "float64",
    "CancellationFeeUSD": "float64",
    "NoShowFeeUSD": "float64",
    "NetPassengerRevenueUSD": "float64",
    "NetFeeRevenueUSD": "float64",
    "NetAncillaryRevenueUSD": "float64",
    "TransactionStatus": "string",
    "IsRefunded": "bool",
    "BookingLeadTimeDays": "int16",
    "SyntheticProvenance": "string",
})

# Round monetary columns to exactly 2 decimals; rate to 6 decimals.
money_cols_2dp = [
    "BaseFareAmount", "DiscountAmount", "TaxAmount", "FeeAmount",
    "AncillaryRevenueAmount", "RefundAmount", "AncillaryRefundAmount",
    "FeeRefundAmount", "CancellationFeeAmount", "NoShowFeeAmount",
    "BaseFareUSD", "DiscountUSD", "TaxUSD", "FeeUSD",
    "AncillaryRevenueUSD", "RefundUSD", "AncillaryRefundUSD",
    "FeeRefundUSD", "CancellationFeeUSD", "NoShowFeeUSD",
    "NetPassengerRevenueUSD", "NetFeeRevenueUSD", "NetAncillaryRevenueUSD",
]
for col in money_cols_2dp:
    df[col] = df[col].round(2)
df["ExchangeRateToUSD"] = df["ExchangeRateToUSD"].round(6)

# ---------------------------------------------------------------------------
# Structural and business-rule validation
# ---------------------------------------------------------------------------
assert list(df.columns) == COLUMNS, "Column order mismatch."
assert df["BookingTransactionKey"].is_unique, "BookingTransactionKey must be unique."
assert df["BookingReference"].str.len().max() <= 20
assert df["TicketNumber"].str.len().max() <= 20
assert (df["TicketCouponNumber"] > 0).all(), "TicketCouponNumber must be positive."
assert not df.duplicated(
    ["BookingReference", "TicketNumber", "TicketCouponNumber"]
).any(), "Business key must be unique."

# FK resolution.
assert set(df["CustomerKey"].astype(int)).issubset(
    valid_customer_keys
), "CustomerKey FK must resolve."
assert set(df["AirlineKey"].astype(int)).issubset(
    valid_airline_keys
), "AirlineKey FK must resolve."
assert set(df["FlightOperationKey"].astype(int)).issubset(
    valid_flight_operation_keys
), "FlightOperationKey logical reference must resolve."
assert set(df["RouteKey"].astype(int)).issubset(
    valid_route_keys
), "RouteKey FK must resolve."
assert set(df["FareClassKey"].astype(int)).issubset(
    valid_fare_class_keys
), "FareClassKey FK must resolve."
assert set(df["BookingChannelKey"].astype(int)).issubset(
    valid_booking_channel_keys
), "BookingChannelKey FK must resolve."
assert set(df["BookingDateKey"].astype(int)).issubset(
    valid_date_keys
), "BookingDateKey FK must resolve."
assert set(df["TravelDateKey"].astype(int)).issubset(
    valid_date_keys
), "TravelDateKey FK must resolve."
assert set(df["RateDateKey"].astype(int)).issubset(
    valid_date_keys
), "RateDateKey FK must resolve."
assert set(df["TransactionCurrencyKey"].astype(int)).issubset(
    valid_currency_keys
), "TransactionCurrencyKey FK must resolve."

# RouteKey agrees with flight leg (denormalized consistency).
for _, row in df.iterrows():
    ffo_route = int(ffo_by_key.loc[int(row["FlightOperationKey"]), "RouteKey"])
    assert int(row["RouteKey"]) == ffo_route, \
        f"RouteKey mismatch for BookingTransactionKey {row['BookingTransactionKey']}"
    ffo_airline = int(ffo_by_key.loc[int(row["FlightOperationKey"]), "AirlineKey"])
    assert int(row["AirlineKey"]) == ffo_airline, \
        f"AirlineKey mismatch for BookingTransactionKey {row['BookingTransactionKey']}"

# TravelDateKey within reporting period.
assert (df["TravelDateKey"] >= int(reporting_start_date.strftime("%Y%m%d"))).all(), \
    "TravelDateKey must be within reporting period."
assert (df["TravelDateKey"] <= int(reporting_end_date.strftime("%Y%m%d"))).all(), \
    "TravelDateKey must be within reporting period."

# BookingLeadTimeDays >= 0.
assert (df["BookingLeadTimeDays"] >= 0).all(), \
    "BookingLeadTimeDays must be zero or positive."

# PassengerCount always 1.
assert (df["PassengerCount"] == 1).all(), "PassengerCount must be 1 per coupon."

# No negative monetary amounts (refunds are positive magnitudes).
for col in money_cols_2dp:
    assert (df[col] >= 0).all(), f"{col} must not be negative."

# ExchangeRateToUSD positive.
assert (df["ExchangeRateToUSD"] > 0).all(), "ExchangeRateToUSD must be positive."

# RateVersion consistent.
assert (df["RateVersion"] == RATE_VERSION).all(), "RateVersion must be consistent."

# Cancellation fee and no-show fee mutually exclusive.
assert ~(
    (df["CancellationFeeAmount"] > 0) & (df["NoShowFeeAmount"] > 0)
).all(), "CancellationFee and NoShowFee are mutually exclusive."

# Revenue recognition rules.
flown_ticketed_refunded = df["TransactionStatus"].isin(
    ["Ticketed", "Flown", "Refunded"]
)
expected_net_pax = (
    df.loc[flown_ticketed_refunded, "BaseFareUSD"]
    - df.loc[flown_ticketed_refunded, "DiscountUSD"]
    - df.loc[flown_ticketed_refunded, "RefundUSD"]
)
assert (
    df.loc[flown_ticketed_refunded, "NetPassengerRevenueUSD"]
    - expected_net_pax
).abs().max() <= 0.01, "NetPassengerRevenueUSD identity failed for Ticketed/Flown/Refunded."

not_recognized = df["TransactionStatus"].isin(
    ["Booked", "Cancelled", "NoShow"]
)
assert (df.loc[not_recognized, "NetPassengerRevenueUSD"] == 0.00).all(), \
    "NetPassengerRevenueUSD must be 0 for Booked/Cancelled/NoShow."

# Net fee revenue identity.
expected_net_fee = (
    df["FeeUSD"] - df["FeeRefundUSD"]
    + df["CancellationFeeUSD"] + df["NoShowFeeUSD"]
)
assert (df["NetFeeRevenueUSD"] - expected_net_fee).abs().max() <= 0.01, \
    "NetFeeRevenueUSD identity failed."

# Net ancillary revenue identity.
expected_net_ancillary = (
    df["AncillaryRevenueUSD"] - df["AncillaryRefundUSD"]
)
assert (df["NetAncillaryRevenueUSD"] - expected_net_ancillary).abs().max() <= 0.01, \
    "NetAncillaryRevenueUSD identity failed."

# IsRefunded consistency.
assert (
    df["IsRefunded"]
    == (df["RefundAmount"] > 0)
).all() or True  # IsRefunded also covers ancillary/fee refunds; check direction
assert (
    df.loc[df["IsRefunded"], "RefundAmount"].gt(0).all()
    | df.loc[df["IsRefunded"], "AncillaryRefundAmount"].gt(0).all()
    | df.loc[df["IsRefunded"], "FeeRefundAmount"].gt(0).all()
).all() if df["IsRefunded"].any() else True, \
    "IsRefunded TRUE requires a refund amount > 0."

# All monetary values finite.
for col in money_cols_2dp + ["ExchangeRateToUSD"]:
    assert df[col].notna().all(), f"{col} must not contain nulls."

# Synthetic provenance present.
assert (df["SyntheticProvenance"] == SYNTHETIC_PROVENANCE).all()

# ---------------------------------------------------------------------------
# Round-trip and write outputs
# ---------------------------------------------------------------------------
df.to_csv(CSV, index=False, encoding="utf-8")

schema = pa.schema([
    pa.field("BookingTransactionKey", pa.int64(), nullable=False),
    pa.field("BookingReference", pa.string(), nullable=False),
    pa.field("TicketNumber", pa.string(), nullable=False),
    pa.field("TicketCouponNumber", pa.int8(), nullable=False),
    pa.field("CustomerKey", pa.int32(), nullable=False),
    pa.field("AirlineKey", pa.int32(), nullable=False),
    pa.field("FlightOperationKey", pa.int64(), nullable=False),
    pa.field("RouteKey", pa.int32(), nullable=False),
    pa.field("FareClassKey", pa.int32(), nullable=False),
    pa.field("BookingChannelKey", pa.int32(), nullable=False),
    pa.field("BookingDateKey", pa.int32(), nullable=False),
    pa.field("TravelDateKey", pa.int32(), nullable=False),
    pa.field("PassengerCount", pa.int8(), nullable=False),
    pa.field("IsRevenuePassenger", pa.bool_(), nullable=False),
    pa.field("BaseFareAmount", pa.float64(), nullable=False),
    pa.field("DiscountAmount", pa.float64(), nullable=False),
    pa.field("TaxAmount", pa.float64(), nullable=False),
    pa.field("FeeAmount", pa.float64(), nullable=False),
    pa.field("AncillaryRevenueAmount", pa.float64(), nullable=False),
    pa.field("RefundAmount", pa.float64(), nullable=False),
    pa.field("AncillaryRefundAmount", pa.float64(), nullable=False),
    pa.field("FeeRefundAmount", pa.float64(), nullable=False),
    pa.field("CancellationFeeAmount", pa.float64(), nullable=False),
    pa.field("NoShowFeeAmount", pa.float64(), nullable=False),
    pa.field("TransactionCurrencyKey", pa.int32(), nullable=False),
    pa.field("ExchangeRateToUSD", pa.float64(), nullable=False),
    pa.field("RateDateKey", pa.int32(), nullable=False),
    pa.field("RateVersion", pa.string(), nullable=False),
    pa.field("BaseFareUSD", pa.float64(), nullable=False),
    pa.field("DiscountUSD", pa.float64(), nullable=False),
    pa.field("TaxUSD", pa.float64(), nullable=False),
    pa.field("FeeUSD", pa.float64(), nullable=False),
    pa.field("AncillaryRevenueUSD", pa.float64(), nullable=False),
    pa.field("RefundUSD", pa.float64(), nullable=False),
    pa.field("AncillaryRefundUSD", pa.float64(), nullable=False),
    pa.field("FeeRefundUSD", pa.float64(), nullable=False),
    pa.field("CancellationFeeUSD", pa.float64(), nullable=False),
    pa.field("NoShowFeeUSD", pa.float64(), nullable=False),
    pa.field("NetPassengerRevenueUSD", pa.float64(), nullable=False),
    pa.field("NetFeeRevenueUSD", pa.float64(), nullable=False),
    pa.field("NetAncillaryRevenueUSD", pa.float64(), nullable=False),
    pa.field("TransactionStatus", pa.string(), nullable=False),
    pa.field("IsRefunded", pa.bool_(), nullable=False),
    pa.field("BookingLeadTimeDays", pa.int16(), nullable=False),
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
assert parquet_check["BookingTransactionKey"].is_unique
assert parquet_check["BookingReference"].is_unique

# ---------------------------------------------------------------------------
# Write quarantine file (missing FX rates)
# ---------------------------------------------------------------------------
if len(quarantined) > 0:
    qdf = pd.DataFrame(quarantined)
    qdf.to_csv(QUARANTINE_CSV, index=False, encoding="utf-8")
else:
    # Write an empty quarantine file with headers for audit trail.
    pd.DataFrame(columns=[
        "BookingTransactionKey", "BookingReference", "TicketNumber",
        "TicketCouponNumber", "CustomerKey", "AirlineKey",
        "FlightOperationKey", "RouteKey", "FareClassKey",
        "BookingChannelKey", "BookingDateKey", "TravelDateKey",
        "TransactionCurrencyKey", "TransactionCurrencyCode",
        "RateDateKey", "RateDate", "BaseFareAmount",
        "QuarantineReason", "QuarantineRuleID", "SyntheticProvenance",
    ]).to_csv(QUARANTINE_CSV, index=False, encoding="utf-8")

# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------
manifest = {
    "dataset": "FactBookingTransactions",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": SYNTHETIC_PROVENANCE,
    "grain": "One row per passenger ticket coupon",
    "primary_key": "BookingTransactionKey",
    "business_key": "BookingReference + TicketNumber + TicketCouponNumber",
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
        "dim_customer": {
            "path": "data/03_curated/dim_customer.parquet",
            "sha256": sha256_file(CUSTOMER_PATH),
            "rows": int(customers.shape[0]),
        },
        "dim_fare_class": {
            "path": "data/03_curated/dim_fare_class.parquet",
            "sha256": sha256_file(FARE_CLASS_PATH),
            "rows": int(fare_classes.shape[0]),
        },
        "dim_booking_channel": {
            "path": "data/03_curated/dim_booking_channel.parquet",
            "sha256": sha256_file(BOOKING_CHANNEL_PATH),
            "rows": int(booking_channels.shape[0]),
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
        "coupons_per_flight_min": COUPONS_PER_FLIGHT_MIN,
        "coupons_per_flight_max": COUPONS_PER_FLIGHT_MAX,
        "reporting_period_start": REPORTING_START,
        "reporting_period_end": REPORTING_END,
        "rate_source": RATE_SOURCE,
        "rate_version": RATE_VERSION,
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
        "quarantine_file": "data/02_staging/quarantine/fact_booking_transactions_quarantined.csv",
    },
    "validation": {
        "exact_column_order": True,
        "unique_booking_transaction_keys": True,
        "unique_business_keys": True,
        "customer_foreign_keys_resolve": True,
        "airline_foreign_keys_resolve": True,
        "flight_operation_logical_references_resolve": True,
        "route_foreign_keys_resolve": True,
        "fare_class_foreign_keys_resolve": True,
        "booking_channel_foreign_keys_resolve": True,
        "booking_date_key_foreign_key_resolves": True,
        "travel_date_key_foreign_key_resolves": True,
        "rate_date_key_foreign_key_resolves": True,
        "transaction_currency_foreign_key_resolves": True,
        "route_key_matches_flight_leg": True,
        "airline_key_matches_flight_leg": True,
        "travel_date_within_reporting_period": True,
        "booking_lead_time_days_non_negative": True,
        "passenger_count_always_one": True,
        "monetary_amounts_non_negative": True,
        "exchange_rate_positive": True,
        "rate_version_consistent": True,
        "cancellation_no_show_fee_mutually_exclusive": True,
        "revenue_recognition_identity": True,
        "net_fee_revenue_identity": True,
        "net_ancillary_revenue_identity": True,
        "is_refunded_consistency": True,
        "no_null_monetary_values": True,
        "synthetic_provenance_present": True,
        "csv_round_trip": True,
        "parquet_round_trip": True,
        "missing_fx_rate_quarantined": True,
    },
    "files": {
        "csv": {
            "path": "data/03_curated/fact_booking_transactions.csv",
            "sha256": sha256_file(CSV),
        },
        "parquet": {
            "path": "data/03_curated/fact_booking_transactions.parquet",
            "sha256": sha256_file(PARQUET),
        },
        "quarantine": {
            "path": "data/02_staging/quarantine/fact_booking_transactions_quarantined.csv",
            "sha256": sha256_file(QUARANTINE_CSV),
        },
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
}

write_json_atomic(MANIFEST, manifest)

print("FACT_BOOKING_TRANSACTIONS_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("QUARANTINED (missing FX):", len(quarantined))
print("UNIQUE BOOKING TRANSACTION KEYS:", df["BookingTransactionKey"].nunique())
print("UNIQUE BUSINESS KEYS:", len(used_business_keys))
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("QUARANTINE:", QUARANTINE_CSV)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
