from pathlib import Path
from datetime import date, timedelta, datetime, timezone
import hashlib
import json

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]

OUT = ROOT / "data" / "03_curated"
MANIFESTS = ROOT / "data" / "manifests"

CSV = OUT / "dim_customer.csv"
PARQUET = OUT / "dim_customer.parquet"
MANIFEST = MANIFESTS / "dim_customer_manifest.json"

COLUMNS = [
    "CustomerKey",
    "CustomerID",
    "CustomerSegment",
    "LoyaltyTier",
    "HomeCountry",
    "HomeCountryCode",
    "RegistrationDate",
    "IsActive"
]

# Reproducible portfolio baseline.
CUSTOMER_COUNT = 5000
RANDOM_SEED = 3602026

REGISTRATION_START = date(2024, 10, 1)
REGISTRATION_END = date(2025, 9, 30)

CUSTOMER_SEGMENTS = [
    "Leisure",
    "Business",
    "Corporate",
    "Group"
]

LOYALTY_TIERS = [
    "None",
    "Silver",
    "Gold",
    "Platinum"
]

# Synthetic customer home-market distribution.
COUNTRIES = [
    ("United Arab Emirates", "AE", 0.18),
    ("Qatar", "QA", 0.10),
    ("Singapore", "SG", 0.10),
    ("India", "IN", 0.25),
    ("United Kingdom", "GB", 0.12),
    ("Germany", "DE", 0.08),
    ("United States", "US", 0.10),
    ("Australia", "AU", 0.07)
]

# Provisional segment distribution.
SEGMENT_PROBABILITIES = [
    0.62,  # Leisure
    0.22,  # Business
    0.10,  # Corporate
    0.06   # Group
]

# Loyalty probabilities vary by customer segment.
LOYALTY_PROBABILITIES = {
    "Leisure":    [0.15, 0.42, 0.30, 0.13],
    "Business":   [0.08, 0.32, 0.38, 0.22],
    "Corporate":  [0.05, 0.25, 0.40, 0.30],
    "Group":      [0.35, 0.35, 0.22, 0.08]
}

# Synthetic customer activity assumption.
ACTIVE_PROBABILITY = 0.96

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

rng = np.random.default_rng(RANDOM_SEED)

# ----------------------------------------------------------
# 1. Generate deterministic synthetic customer attributes.
# ----------------------------------------------------------

segment_values = rng.choice(
    CUSTOMER_SEGMENTS,
    size=CUSTOMER_COUNT,
    p=SEGMENT_PROBABILITIES
)

country_labels = [row[0] for row in COUNTRIES]
country_codes = [row[1] for row in COUNTRIES]
country_probabilities = [row[2] for row in COUNTRIES]

country_indices = rng.choice(
    len(COUNTRIES),
    size=CUSTOMER_COUNT,
    p=country_probabilities
)

country_values = [
    country_labels[int(i)]
    for i in country_indices
]

country_code_values = [
    country_codes[int(i)]
    for i in country_indices
]

loyalty_values = []

for segment in segment_values:
    loyalty_values.append(
        rng.choice(
            LOYALTY_TIERS,
            p=LOYALTY_PROBABILITIES[str(segment)]
        )
    )

registration_days = (
    REGISTRATION_END - REGISTRATION_START
).days

registration_offsets = rng.integers(
    low=0,
    high=registration_days + 1,
    size=CUSTOMER_COUNT
)

registration_dates = [
    REGISTRATION_START + timedelta(days=int(offset))
    for offset in registration_offsets
]

active_values = rng.random(CUSTOMER_COUNT) < ACTIVE_PROBABILITY

records = []

for i in range(CUSTOMER_COUNT):
    customer_key = i + 1

    records.append({
        "CustomerKey": customer_key,
        "CustomerID": f"SYN-CUST-{customer_key:06d}",
        "CustomerSegment": str(segment_values[i]),
        "LoyaltyTier": str(loyalty_values[i]),
        "HomeCountry": str(country_values[i]),
        "HomeCountryCode": str(country_code_values[i]),
        "RegistrationDate": registration_dates[i],
        "IsActive": bool(active_values[i])
    })

df = pd.DataFrame(records, columns=COLUMNS)

# ----------------------------------------------------------
# 2. Apply explicit contract data types.
# ----------------------------------------------------------

df = df.astype({
    "CustomerKey": "int32",
    "CustomerID": "string",
    "CustomerSegment": "string",
    "LoyaltyTier": "string",
    "HomeCountry": "string",
    "HomeCountryCode": "string",
    "IsActive": "bool"
})

# ----------------------------------------------------------
# 3. Structural and business-rule validation.
# ----------------------------------------------------------

assert df.shape == (CUSTOMER_COUNT, 8)
assert list(df.columns) == COLUMNS
assert df.notna().all().all()

assert df["CustomerKey"].is_unique
assert df["CustomerID"].is_unique

assert df["CustomerKey"].tolist() == list(
    range(1, CUSTOMER_COUNT + 1)
)

assert df["CustomerID"].str.fullmatch(
    r"SYN-CUST-[0-9]{6}"
).all()

assert set(df["CustomerSegment"].unique()) == set(
    CUSTOMER_SEGMENTS
)

assert set(df["LoyaltyTier"].unique()).issubset(
    set(LOYALTY_TIERS)
)

assert set(df["HomeCountryCode"].unique()) == set(
    country_codes
)

country_lookup = {
    code: name
    for name, code, _ in COUNTRIES
}

for _, customer in df.iterrows():
    assert (
        country_lookup[customer["HomeCountryCode"]]
        == customer["HomeCountry"]
    )

assert df["RegistrationDate"].between(
    REGISTRATION_START,
    REGISTRATION_END
).all()

assert df["IsActive"].dtype == bool

# No real personal-information fields are permitted.
forbidden_columns = {
    "Name",
    "FirstName",
    "LastName",
    "Email",
    "Phone",
    "Address",
    "PassportNumber",
    "DateOfBirth"
}

assert forbidden_columns.isdisjoint(set(df.columns))

# Ensure the provisional distribution produced every segment and tier.
assert df["CustomerSegment"].nunique() == 4
assert df["LoyaltyTier"].nunique() == 4
assert df["HomeCountryCode"].nunique() == 8

# ----------------------------------------------------------
# 4. Write CSV and Parquet.
# ----------------------------------------------------------

df.to_csv(CSV, index=False, encoding="utf-8-sig")

schema = pa.schema([
    pa.field("CustomerKey", pa.int32(), nullable=False),
    pa.field("CustomerID", pa.string(), nullable=False),
    pa.field("CustomerSegment", pa.string(), nullable=False),
    pa.field("LoyaltyTier", pa.string(), nullable=False),
    pa.field("HomeCountry", pa.string(), nullable=False),
    pa.field("HomeCountryCode", pa.string(), nullable=False),
    pa.field("RegistrationDate", pa.date32(), nullable=False),
    pa.field("IsActive", pa.bool_(), nullable=False)
])

table = pa.Table.from_pandas(
    df,
    schema=schema,
    preserve_index=False,
    safe=True
)

pq.write_table(table, PARQUET, compression="snappy")

# ----------------------------------------------------------
# 5. Initial round-trip and physical type checks.
# ----------------------------------------------------------

csv_check = pd.read_csv(CSV, encoding="utf-8-sig")
parquet_check = pd.read_parquet(PARQUET)
parquet_schema = pq.read_schema(PARQUET)

assert csv_check.shape == (CUSTOMER_COUNT, 8)
assert parquet_check.shape == (CUSTOMER_COUNT, 8)

assert list(parquet_check.columns) == COLUMNS

assert parquet_schema.field("CustomerKey").type == pa.int32()
assert parquet_schema.field("RegistrationDate").type == pa.date32()
assert parquet_schema.field("IsActive").type == pa.bool_()

assert parquet_check["CustomerKey"].is_unique
assert parquet_check["CustomerID"].is_unique

# ----------------------------------------------------------
# 6. Record counts and distribution evidence.
# ----------------------------------------------------------

segment_counts = (
    df["CustomerSegment"]
    .value_counts()
    .sort_index()
    .to_dict()
)

loyalty_counts = (
    df["LoyaltyTier"]
    .value_counts()
    .sort_index()
    .to_dict()
)

country_counts = (
    df["HomeCountryCode"]
    .value_counts()
    .sort_index()
    .to_dict()
)

active_count = int(df["IsActive"].sum())
inactive_count = int((~df["IsActive"]).sum())

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# ----------------------------------------------------------
# 7. Write manifest.
# ----------------------------------------------------------

manifest = {
    "dataset": "DimCustomer",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    "grain": "One row per fictional customer",
    "primary_key": "CustomerKey",
    "business_key": "CustomerID",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "generation": {
        "method": "Deterministic NumPy random generator",
        "random_seed": RANDOM_SEED,
        "customer_population_size": CUSTOMER_COUNT,
        "population_size_status": "Provisional portfolio design choice",
        "registration_start": REGISTRATION_START.isoformat(),
        "registration_end": REGISTRATION_END.isoformat(),
        "active_probability": ACTIVE_PROBABILITY
    },
    "distributions": {
        "customer_segments": segment_counts,
        "loyalty_tiers": loyalty_counts,
        "home_country_codes": country_counts,
        "active_customers": active_count,
        "inactive_customers": inactive_count
    },
    "privacy": {
        "all_customer_ids_synthetic": True,
        "real_personal_information_used": False,
        "names_generated": False,
        "email_addresses_generated": False,
        "phone_numbers_generated": False,
        "addresses_generated": False,
        "passport_numbers_generated": False
    },
    "first_booking_rule": {
        "contract_requirement": (
            "RegistrationDate must be on or before the customer's first booking date."
        ),
        "current_status": "PENDING_FACT_BOOKING_INTEGRATION",
        "downstream_requirement": (
            "Booking generation must enforce BookingDate >= RegistrationDate "
            "for every customer and preserve registration on or before first booking."
        )
    },
    "customer_history_rule": (
        "Customer attributes are Type 1 in the baseline. Historical "
        "segmentation changes are outside the baseline scope."
    ),
    "validation": {
        "exact_column_order": True,
        "5000_customer_records": True,
        "unique_customer_keys": True,
        "unique_synthetic_customer_ids": True,
        "customer_id_format": True,
        "four_customer_segments_present": True,
        "four_loyalty_tiers_present": True,
        "eight_country_codes_present": True,
        "country_name_code_consistency": True,
        "registration_dates_in_defined_range": True,
        "no_null_values": True,
        "no_personal_information_columns": True,
        "parquet_int32_customer_key": True,
        "parquet_date32_registration_date": True,
        "parquet_boolean_active_flag": True,
        "csv_round_trip": True,
        "parquet_round_trip": True,
        "first_booking_date_rule": "Pending fact integration"
    },
    "files": {
        "csv": {
            "path": "data/03_curated/dim_customer.csv",
            "sha256": sha256(CSV)
        },
        "parquet": {
            "path": "data/03_curated/dim_customer.parquet",
            "sha256": sha256(PARQUET)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("DIM_CUSTOMER_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("CUSTOMER SEGMENTS:", df["CustomerSegment"].nunique())
print("LOYALTY TIERS:", df["LoyaltyTier"].nunique())
print("HOME COUNTRIES:", df["HomeCountryCode"].nunique())
print("ACTIVE CUSTOMERS:", active_count)
print("INACTIVE CUSTOMERS:", inactive_count)
print("UNIQUE SYNTHETIC CUSTOMER IDS: PASSED")
print("NO REAL PERSONAL INFORMATION: PASSED")
print("REGISTRATION DATE RANGE: PASSED")
print("PARQUET CONTRACT TYPES: PASSED")
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("FIRST BOOKING DATE RULE: PENDING FACT INTEGRATION")
print("VALIDATION: PASSED")

