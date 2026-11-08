from pathlib import Path
from datetime import date, datetime, timedelta, timezone
import json
import hashlib

import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = ROOT / "data" / "03_curated"
MANIFEST_DIR = ROOT / "data" / "manifests"

CSV_PATH = OUTPUT_DIR / "dim_date.csv"
PARQUET_PATH = OUTPUT_DIR / "dim_date.parquet"
MANIFEST_PATH = MANIFEST_DIR / "dim_date_manifest.json"

START_DATE = date(2024, 10, 1)
END_DATE = date(2026, 10, 31)

REPORTING_START = date(2025, 10, 1)
REPORTING_END = date(2026, 9, 30)

OUTPUT_COLUMNS = [
    "DateKey",
    "FullDate",
    "Year",
    "Quarter",
    "MonthNumber",
    "MonthName",
    "MonthShortName",
    "YearMonth",
    "YearMonthSort",
    "WeekNumber",
    "WeekStartDate",
    "DayOfMonth",
    "DayName",
    "DayOfWeekNumber",
    "IsWeekend",
    "IsReportingPeriod",
    "FiscalYear",
    "FiscalQuarter",
    "FiscalMonthNumber"
]

for path in [CSV_PATH, PARQUET_PATH, MANIFEST_PATH]:
    if path.exists():
        raise FileExistsError(
            f"Output already exists. No files overwritten: {path}"
        )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

records = []

current = START_DATE

while current <= END_DATE:
    iso = current.isocalendar()

    fiscal_month = ((current.month - 10) % 12) + 1
    fiscal_year = current.year + 1 if current.month >= 10 else current.year
    fiscal_quarter = ((fiscal_month - 1) // 3) + 1

    records.append({
        "DateKey": current.year * 10000 + current.month * 100 + current.day,
        "FullDate": current,
        "Year": current.year,
        "Quarter": ((current.month - 1) // 3) + 1,
        "MonthNumber": current.month,
        "MonthName": current.strftime("%B"),
        "MonthShortName": current.strftime("%b"),
        "YearMonth": current.strftime("%Y-%m"),
        "YearMonthSort": current.year * 100 + current.month,
        "WeekNumber": iso.week,
        "WeekStartDate": current - timedelta(days=current.weekday()),
        "DayOfMonth": current.day,
        "DayName": current.strftime("%A"),
        "DayOfWeekNumber": iso.weekday,
        "IsWeekend": iso.weekday >= 6,
        "IsReportingPeriod": REPORTING_START <= current <= REPORTING_END,
        "FiscalYear": fiscal_year,
        "FiscalQuarter": fiscal_quarter,
        "FiscalMonthNumber": fiscal_month
    })

    current += timedelta(days=1)

df = pd.DataFrame(records, columns=OUTPUT_COLUMNS)

# Apply explicit analytical data types.
df = df.astype({
    "DateKey": "int32",
    "Year": "int16",
    "Quarter": "int8",
    "MonthNumber": "int8",
    "MonthName": "string",
    "MonthShortName": "string",
    "YearMonth": "string",
    "YearMonthSort": "int32",
    "WeekNumber": "int8",
    "DayOfMonth": "int8",
    "DayName": "string",
    "DayOfWeekNumber": "int8",
    "IsWeekend": "bool",
    "IsReportingPeriod": "bool",
    "FiscalYear": "int16",
    "FiscalQuarter": "int8",
    "FiscalMonthNumber": "int8"
})

# Contract-level validation.
assert len(df) == 761, f"Unexpected row count: {len(df)}"
assert len(df.columns) == 19
assert list(df.columns) == OUTPUT_COLUMNS

assert df["DateKey"].is_unique
assert df["FullDate"].is_unique
assert df.notna().all().all()

assert df["FullDate"].iloc[0] == START_DATE
assert df["FullDate"].iloc[-1] == END_DATE

expected_dates = pd.date_range(
    START_DATE, END_DATE, freq="D"
).date

assert list(df["FullDate"]) == list(expected_dates)

assert df["IsReportingPeriod"].sum() == 365

assert df.loc[
    df["FullDate"] == date(2025, 10, 1), "FiscalYear"
].iloc[0] == 2026

assert df.loc[
    df["FullDate"] == date(2026, 9, 30), "FiscalYear"
].iloc[0] == 2026

assert df.loc[
    df["FullDate"] == date(2026, 10, 1), "FiscalYear"
].iloc[0] == 2027

assert (df["DayOfWeekNumber"].between(1, 7)).all()
assert (df["WeekNumber"].between(1, 53)).all()
assert (df["FiscalQuarter"].between(1, 4)).all()
assert (df["FiscalMonthNumber"].between(1, 12)).all()

# Save both analytical and portable formats.
df.to_csv(CSV_PATH, index=False, date_format="%Y-%m-%d")
df.to_parquet(PARQUET_PATH, index=False, engine="pyarrow")

# Reopen both outputs and validate persisted data.
csv_check = pd.read_csv(CSV_PATH)
parquet_check = pd.read_parquet(PARQUET_PATH)

assert csv_check.shape == (761, 19)
assert parquet_check.shape == (761, 19)

assert csv_check["DateKey"].is_unique
assert parquet_check["DateKey"].is_unique

assert parquet_check["IsReportingPeriod"].sum() == 365

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    "dataset": "DimDate",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "grain": "One row per calendar date",
    "primary_key": "DateKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": OUTPUT_COLUMNS,
    "date_range": {
        "start": START_DATE.isoformat(),
        "end": END_DATE.isoformat(),
        "inclusive": True
    },
    "reporting_period": {
        "start": REPORTING_START.isoformat(),
        "end": REPORTING_END.isoformat(),
        "expected_days": 365
    },
    "calendar_rules": {
        "week_number": "ISO 8601",
        "week_start": "Monday",
        "fiscal_year_start_month": "October",
        "fiscal_year_label": "Ending calendar year"
    },
    "validation": {
        "exact_column_order": True,
        "row_count": True,
        "unique_date_key": True,
        "unique_full_date": True,
        "continuous_dates": True,
        "no_null_values": True,
        "reporting_period_days": True,
        "fiscal_year_boundaries": True,
        "csv_round_trip": True,
        "parquet_round_trip": True
    },
    "files": {
        "csv": {
            "path": "data/03_curated/dim_date.csv",
            "sha256": sha256(CSV_PATH)
        },
        "parquet": {
            "path": "data/03_curated/dim_date.parquet",
            "sha256": sha256(PARQUET_PATH)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST_PATH.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("DIM_DATE_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("REPORTING_PERIOD_DAYS:", int(df["IsReportingPeriod"].sum()))
print("DATE_RANGE:", START_DATE, "TO", END_DATE)
print("CSV:", CSV_PATH)
print("PARQUET:", PARQUET_PATH)
print("MANIFEST:", MANIFEST_PATH)
print("VALIDATION: PASSED")
