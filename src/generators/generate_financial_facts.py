#!/usr/bin/env python3
"""AEROVISION 360 — FactBookingTransactions and FactOperatingCosts Generator.

Generates synthetic financial fact tables for Page 03 Revenue & Finance.

Sources:
- data/03_curated/fact_flight_operations.csv
- data/03_curated/dim_airline.csv
- data/03_curated/dim_route.csv
- data/03_curated/dim_date.csv
- data/03_curated/dim_currency.csv
- data/04_reference/ref_exchange_rates.csv

Constraints (GOV-D-07 / OD-04):
- UTF-8 without BOM
- SHA-256 manifest for each output file
- Deterministic: same seed + same parameters => identical output
- USD per one unit of transaction currency
- Exact-date lookup: RateDateKey = BookingDateKey or CostDateKey
- 6 decimal places for ExchangeRateToUSD
- Round final converted amount to 2 decimals
- No forward-fill: missing rate quarantines row
- IsSynthetic = True for all records
- RateVersion = FX-2026-11-04-001
- RateSource = AEROVISION-360-SYNTHETIC-FX-V1
- IsSynthetic = True for all records

FactBookingOperations columns:
- BookingTransactionKey: Int64
- FlightOperationKey: Int64
- AirlineKey: Int64
- RouteKey: Int64
- BookingDateKey: Int64
- TravelDateKey: Int64
- AvailableSeats: Int64
- BookedPassengers: Int64
- RevenuePassengers: Int64
- NonRevenuePassengers: Int64
- FlightStatus: String(20)
- DepartureDelayMinutes: Int64
- ArrivalDelayMinutes: Int64
- BlockMinutes: Int64
- CancellationFlag: Boolean
- CompletionFlag: Boolean
- OnTimeFlag: Boolean
- OnTimeArrivalFlag: Boolean
- OriginalCurrencyKey: Int64
- OriginalAmount: Decimal(18,2)
- ExchangeRateToUSD: Decimal(18,6)
- RateDateKey: Int64
- RateVersion: String(20)
- NetPassengerRevenueUSD: Decimal(18,2)

FactOperatingCosts columns:
- OperatingCostKey: Int64
- OperatingCostID: String(20)
- AirlineKey: Int64
- FlightOperationKey: Int64
- RouteKey: Int64
- CostDateKey: Int64
- CostCategory: String(50)
- CostSubcategory: String(50)
- CostAmountOriginal: Decimal(18,2)
- OriginalCurrencyKey: Int64
- ExchangeRateToUSD: Decimal(18,6)
- CostAmountUSD: Decimal(18,2)
- IsSynthetic: Boolean
- RateVersion: String(20)
- CancellationFlag: Boolean
- CompletionFlag: Boolean
"""

import csv
import hashlib
import json
import os
import random
from datetime import date, timedelta
from pathlib import Path

# Owner-approved OD-04 decisions
CANONICALIZATION_STANDARD = "RFC 8785 JCS v1.0"
HASH_ALGORITHM = "SHA-256"
HASH_OUTPUT_FORMAT = "lowercase hexadecimal (64 chars)"
CHARACTER_ENCODING = "UTF-8 without BOM"
LINE_ENDINGS = "LF (\\x0A)"
WHITESPACE = "None (minified)"
MANIFEST_HASH_EXCLUDED = True

CURRENCIES = ["AED", "QAR", "SGD", "INR", "GBP", "EUR", "USD", "AUD"]
REPORTING_CURRENCY = "USD"
REPORTING_START = "2025-10-01"
REPORTING_END = "2026-09-30"
RATE_SOURCE = "AEROVISION-360-SYNTHETIC-FX-V1"
RATE_VERSION = "FX-2026-11-04-001"
SEED = 3602026
OUTPUT_DIR = "data/03_curated"
MANIFEST_DIR = "data/manifests"
OUTPUT_FILE_BOOKING = "fact_booking_transactions.csv"
OUTPUT_FILE_OPERATING = "fact_operating_costs.csv"
MANIFEST_FILE_BOOKING = "fact_booking_transactions_manifest.json"
MANIFEST_FILE_OPERATING = "fact_operating_costs_manifest.json"


def deterministic_rate(currency_code: str, rate_date: str, seed: int) -> float:
    """Deterministic SHA-256-based rate generation.

    Same inputs always produce the same byte sequence. Values are realistic FX
    rates (positive, 6 decimal places) and never zero or negative.

    USD is always exactly 1.000000.
    """
    if currency_code == "USD":
        return 1.0

    input_str = f"{RATE_VERSION}|{currency_code}|{rate_date}|{seed}"
    digest = hashlib.sha256(input_str.encode("utf-8")).hexdigest()
    int_val = int(digest[:8], 16)
    rate = 0.5 + (int_val / 0xFFFFFFFF) * 1.5
    return round(rate, 6)


def load_exchange_rates(path: str) -> dict:
    """Load exchange rates into dict keyed by (CurrencyCode, RateDate)."""
    rates = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rates[(row["CurrencyCode"], row["RateDate"])] = float(row["ExchangeRateToUSD"])
    return rates


def load_fact_flight_operations(path: str) -> list[dict]:
    """Load fact_flight_operations.csv."""
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def generate_booking_transactions(
    fact_ops_path: str,
    ref_aircraft_path: str,
    exchange_rates: dict,
) -> list[dict]:
    """Generate FactBookingTransactions records from fact_flight_operations.

    Each row in fact_flight_operations generates one FactBookingTransactions row.
    """
    fact_ops = []
    with open(fact_ops_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fact_ops.append(row)

    records = []
    for row in fact_ops:
        flight_operation_key = int(row["FlightOperationKey"])
        airline_key = int(row["AirlineKey"])
        route_key = int(row["RouteKey"])
        scheduled_departure_date_key = int(row["ScheduledDepartureDateKey"])
        travel_date_key = scheduled_departure_date_key
        available_seats = int(row["AvailableSeats"])
        booked_passengers = int(row["BookedPassengers"])
        revenue_passengers = int(row["RevenuePassengers"])
        non_revenue_passengers = int(row["NonRevenuePassengers"])
        flight_status = row["FlightStatus"]
        departure_delay = int(row["DepartureDelayMinutes"])
        arrival_delay = int(row["ArrivalDelayMinutes"])
        block_minutes = int(row["BlockMinutes"])
        cancellation_flag = row["CancellationFlag"].lower() == "true"
        completion_flag = int(row["CompletionFlag"]) == 1
        on_time_flag = row["OnTimeFlag"].lower() == "true"
        on_time_arrival_flag = row["OnTimeArrivalFlag"].lower() == "true"

        booking_id = f"FBK-{flight_operation_key:06d}"

        currency_code = random.choice(CURRENCIES)
        currency_key = CURRENCIES.index(currency_code) + 1

        flight_distance_km = float(row["FlightDistanceKM"])
        base_amount = available_seats * 0.15 * flight_distance_km / 1000
        original_amount = round(base_amount * random.uniform(0.5, 2.0), 2)

        rate_date_str = str(scheduled_departure_date_key)
        exchange_rate = rates.get((currency_code, rate_date_str))
        if exchange_rate is None:
            raise ValueError(f"No exchange rate for {currency_code} on {rate_date_key_str}")

        net_passenger_revenue_usd = round(original_amount * exchange_rate, 2)

        record = {
            "BookingTransactionKey": flight_operation_key,
            "BookingID": booking_id,
            "AirlineKey": airline_key,
            "FlightOperationKey": flight_operation_key,
            "RouteKey": route_key,
            "BookingDateKey": scheduled_departure_date_key,
            "TravelDateKey": travel_date_key,
            "AvailableSeats": available_seats,
            "BookedPassengers": booked_passengers,
            "RevenuePassengers": revenue_passengers,
            "NonRevenuePassengers": non_revenue_passengers,
            "FlightStatus": flight_status,
            "DepartureDelayMinutes": departure_delay,
            "ArrivalDelayMinutes": arrival_delay,
            "BlockMinutes": block_minutes,
            "CancellationFlag": cancellation_flag,
            "CompletionFlag": completion_flag,
            "OnTimeFlag": on_time_flag,
            "OnTimeArrivalFlag": on_time_arrival_flag,
            "OriginalCurrencyKey": currency_key,
            "OriginalAmount": original_amount,
            "ExchangeRateToUSD": exchange_rate,
            "RateDateKey": scheduled_departure_date_key,
            "RateVersion": RATE_VERSION,
            "NetPassengerRevenueUSD": net_passenger_revenue_usd,
        }
        records.append(record)

    return records


def generate_operating_costs(
    fact_flight_operations_path: str,
) -> list[dict]:
    """Generate FactOperatingCosts records from fact_flight_operations."""
    with open(fact_flight_operations_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fact_ops = list(reader)

    records = []
    for row in fact_ops:
        flight_operation_key = int(row["FlightOperationKey"])
        airline_key = int(row["AirlineKey"])
        route_key = int(row["RouteKey"])
        cost_date_key = int(row["ScheduledDepartureDateKey"])
        cancellation_flag = row["CancellationFlag"].lower() == "true"
        completion_flag = int(row["CompletionFlag"]) == 1

        operating_cost_id = f"OC-{flight_operation_key:06d}"

        aircraft_type_key = int(row["AircraftTypeKey"])
        aircraft_category = get_aircraft_type_category(aircraft_type_key)

        base_amount = random.uniform(500, 50000)
        original_amount = round(base_amount, 2)

        rate_date_str = str(cost_date_key)
        exchange_rate = rates.get((currency_code, rate_date_str))
        if exchange_rate is None:
            raise ValueError(f"No exchange rate for {currency_code} on {rate_date_key_str}")

        cost_amount_usd = round(original_amount * exchange_rate, 2)

        record = {
            "OperatingCostKey": flight_operation_key,
            "OperatingCostID": operating_cost_id,
            "AirlineKey": airline_key,
            "FlightOperationKey": flight_operation_key,
            "RouteKey": route_key,
            "CostDateKey": cost_date_key,
            "CostCategory": cost_category,
            "CostSubcategory": cost_subcategory,
            "CostAmountOriginal": original_amount,
            "OriginalCurrencyKey": currency_key,
            "ExchangeRateToUSD": exchange_rate,
            "CostAmountUSD": cost_amount_usd,
            "IsSynthetic": True,
            "RateVersion": RATE_VERSION,
            "CancellationFlag": cancellation_flag,
            "CompletionFlag": completion_flag,
        }
        records.append(record)

    return records


def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def main():
    # Ensure output directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(MANIFEST_DIR, exist_ok=True)

    # Load fact_flight_operations
    fact_flight_operations_path = os.path.join(OUTPUT_DIR, "fact_flight_operations.csv")
    fact_flight_operations = load_fact_flight_operations(fact_flight_operations_path)

    # Load exchange rates
    exchange_rates_path = os.path.join(OUTPUT_DIR, "ref_exchange_rates.csv")
    rates = load_exchange_rates(exchange_rates_path)

    # Generate Booking Transactions
    booking_records = generate_booking_transactions(
        fact_flight_operations_path,
        dim_aircraft_path,
        exchange_rates,
    )

    # Write FactBookingOperations
    booking_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE_BOOKING)
    with open(booking_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "BookingTransactionKey",
                "BookingID",
                "AirlineKey",
                "FlightOperationKey",
                "RouteKey",
                "BookingDateKey",
                "TravelDateKey",
                "AvailableSeats",
                "BookedPassengers",
                "RevenuePassengers",
                "NonRevenuePassengers",
                "FlightStatus",
                "DepartureDelayMinutes",
                "ArrivalDelayMinutes",
                "BlockMinutes",
                "CancellationFlag",
                "CompletionFlag",
                "OnTimeFlag",
                "OnTimeArrivalFlag",
                "OriginalCurrencyKey",
                "OriginalAmount",
                "ExchangeRateToUSD",
                "RateDateKey",
                "RateVersion",
                "NetPassengerRevenueUSD",
            ],
        )
        writer.writeheader()
        writer.writerows(booking_records)

    # Compute SHA-256
    sha256_digest = compute_sha256(booking_path)

    # Row count
    with open(booking_path, "r", encoding="utf-8") as f:
        booking_row_count = sum(1 for _ in f) - 1

    # Build manifest
    manifest = {
        "manifest_id": "FACT_BOOKING_TRANSACTIONS_V1",
        "document_type": "fact_manifest",
        "project": "AEROVISION 360",
        "description": "FactBookingTransactions - Flight booking transactions with monetary data",
        "canonicalization_standard": CANONICALIZATION_STANDARD,
        "hash_algorithm": HASH_ALGORITHM,
        "hash_output_format": HASH_OUTPUT_FORMAT,
        "character_encoding": CHARACTER_ENCODING,
        "line_endings": LINE_ENDINGS,
        "whitespace": WHITESPACE,
        "manifest_hash_field_excluded": MANIFEST_HASH_EXCLUDED,
        "generated_at_utc": "2026-11-07T00:00:00+00:00",
        "row_count": booking_row_count,
        "grain": "One row per scheduled flight booking transaction",
        "primary_key": "BookingTransactionKey",
        "source": "Deterministic synthetic generation (seed-based)",
        "source_files": {
            "fact_flight_operations_sha256": compute_sha256(fact_flight_operations_path),
            "dim_airline_sha256": compute_sha256("data/03_curated/dim_airline.csv"),
            "dim_route_sha256": compute_sha256("data/03_curated/dim_route.csv"),
            "ref_exchange_rates_sha256": compute_sha256(
                os.path.join(OUTPUT_DIR, OUTPUT_FILE_BOOKING)
            ),
        },
        "currency_count": len(CURRENCIES),
        "currencies": sorted(CURRENCIES),
        "reporting_currency": REPORTING_CURRENCY,
        "reporting_period": {
            "start": REPORTING_START,
            "end": REPORTING_END,
            "days": (date.fromisoformat(REPORTING_END) - date.fromisoformat(REPORTING_START)).days + 1,
        },
        "sha256": sha256_digest,
        "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
        "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    }

    manifest_path = os.path.join(MANIFEST_DIR, MANIFEST_FILE_BOOKING)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Created {booking_path} with {booking_row_count} rows")
    print(f"SHA-256: {sha256_digest}")
    print(f"Created manifest: {manifest_path}")


if __name__ == "__main__":
    main()