import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utilities.hashing import sha256_file
from src.utilities.paths import project_root

ROOT = project_root()
OUT = ROOT / "data" / "03_curated"
MANIFESTS = ROOT / "data" / "manifests"

CSV = OUT / "dim_disruption_type.csv"
PARQUET = OUT / "dim_disruption_type.parquet"
MANIFEST = MANIFESTS / "dim_disruption_type_manifest.json"

COLUMNS = [
    "DisruptionTypeKey",
    "DisruptionCode",
    "DisruptionName",
    "DisruptionCategory",
    "ControllableFlag",
    "ReactionaryEligibleFlag",
    "IsActive"
]

# Provisional synthetic disruption taxonomy.
# Reactionary eligibility is deliberately restricted to an
# explicitly identifiable upstream inbound-aircraft delay.
ROWS = [
    (1, "WEATHER", "Severe Weather", "Weather", False, False, True),
    (2, "ATC", "Air Traffic Control Restriction", "Air Traffic Control", False, False, True),
    (3, "TECH", "Aircraft Technical Defect", "Technical", True, False, True),
    (4, "CREW", "Crew Availability", "Crew", True, False, True),
    (5, "AIRPORT", "Airport Infrastructure Constraint", "Airport", False, False, True),
    (6, "SECURITY", "Security Event", "Security", False, False, True),
    (7, "PAX", "Passenger Handling Issue", "Passenger", True, False, True),
    (8, "REACTION", "Late Inbound Aircraft", "Reactionary", False, True, True),
    (9, "OTHER", "Other Operational Cause", "Other", False, False, True)
]

ALLOWED_CATEGORIES = {
    "Weather",
    "Air Traffic Control",
    "Technical",
    "Crew",
    "Airport",
    "Security",
    "Passenger",
    "Reactionary",
    "Other"
}

OUT.mkdir(parents=True, exist_ok=True)
MANIFESTS.mkdir(parents=True, exist_ok=True)

for path in [CSV, PARQUET, MANIFEST]:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

df = pd.DataFrame(ROWS, columns=COLUMNS)

df = df.astype({
    "DisruptionTypeKey": "int32",
    "DisruptionCode": "string",
    "DisruptionName": "string",
    "DisruptionCategory": "string",
    "ControllableFlag": "bool",
    "ReactionaryEligibleFlag": "bool",
    "IsActive": "bool"
})

assert df.shape == (9, 7)
assert list(df.columns) == COLUMNS
assert df.notna().all().all()

assert df["DisruptionTypeKey"].is_unique
assert df["DisruptionCode"].is_unique
assert df["DisruptionName"].is_unique
assert set(df["DisruptionCategory"]) == ALLOWED_CATEGORIES
assert df["DisruptionCategory"].is_unique

# Reactionary eligibility is not the same as controllability.
assert df["ReactionaryEligibleFlag"].sum() == 1
assert df.loc[
    df["ReactionaryEligibleFlag"],
    "DisruptionCategory"
].iloc[0] == "Reactionary"

assert df["IsActive"].all()
assert df["DisruptionCode"].str.len().between(1, 10).all()

df.to_csv(CSV, index=False, encoding="utf-8-sig")
df.to_parquet(PARQUET, index=False, engine="pyarrow")

csv_check = pd.read_csv(CSV, encoding="utf-8-sig")
parquet_check = pd.read_parquet(PARQUET)

assert csv_check.shape == (9, 7)
assert parquet_check.shape == (9, 7)
assert parquet_check["DisruptionTypeKey"].is_unique


manifest = {
    "dataset": "DimDisruptionType",
    "project": "AEROVISION 360",
    "status": "PROVISIONAL_PORTFOLIO_IMPLEMENTATION",
    "grain": "One row per disruption type",
    "primary_key": "DisruptionTypeKey",
    "row_count": len(df),
    "column_count": len(df.columns),
    "columns": COLUMNS,
    "taxonomy_status": "Provisional synthetic baseline taxonomy",
    "reactionary_rule": (
        "Late inbound aircraft is the only baseline reactionary-eligible "
        "type. Fact-level reactionary attribution requires explicit evidence."
    ),
    "validation": {
        "exact_column_order": True,
        "unique_primary_key": True,
        "unique_disruption_code": True,
        "unique_disruption_name": True,
        "all_nine_contract_categories_present": True,
        "one_reactionary_eligible_type": True,
        "reactionary_category_consistency": True,
        "all_baseline_types_active": True,
        "no_null_values": True,
        "csv_round_trip": True,
        "parquet_round_trip": True
    },
    "files": {
        "csv": {
            "path": "data/03_curated/dim_disruption_type.csv",
            "sha256": sha256_file(CSV)
        },
        "parquet": {
            "path": "data/03_curated/dim_disruption_type.parquet",
            "sha256": sha256_file(PARQUET)
        }
    },
    "generated_at_utc": datetime.now(timezone.utc).isoformat()
}

MANIFEST.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("DIM_DISRUPTION_TYPE_BUILD_SUCCESS")
print("ROWS:", len(df))
print("COLUMNS:", len(df.columns))
print("CATEGORIES:", ", ".join(sorted(df["DisruptionCategory"])))
print("REACTIONARY_ELIGIBLE_TYPES:", int(df["ReactionaryEligibleFlag"].sum()))
print("CSV:", CSV)
print("PARQUET:", PARQUET)
print("MANIFEST:", MANIFEST)
print("STATUS: PROVISIONAL")
print("VALIDATION: PASSED")
