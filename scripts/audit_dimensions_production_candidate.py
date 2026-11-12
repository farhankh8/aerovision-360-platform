from pathlib import Path
from datetime import date, datetime
from decimal import Decimal
import hashlib
import json

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CURATED = DATA / "03_curated"
MANIFESTS = DATA / "manifests"
REFERENCE = DATA / "04_reference"

STAGING = (
    ROOT / "reports" / "network_expansion_20261104" / "staging"
)
STAGING_CURATED = STAGING / "curated"
STAGING_MANIFESTS = STAGING / "manifests"

REPORTS = ROOT / "reports" / "production_expansion_audit"
REPORTS.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
REPORT_PATH = REPORTS / f"DIMENSIONS_CONSOLIDATED_AUDIT_{TIMESTAMP}.json"

if REPORT_PATH.exists():
    raise FileExistsError(f"Refusing to overwrite: {REPORT_PATH}")

results = []
failures = []
open_items = []
loaded = {}

def record(name, passed, evidence=""):
    item = {
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "evidence": str(evidence)
    }
    results.append(item)

    if not passed:
        failures.append(item)

def add_open_item(title, detail):
    open_items.append({
        "status": "OPEN",
        "title": title,
        "detail": detail
    })

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical(value):
    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass

    if isinstance(value, pd.Timestamp):
        return value.date().isoformat()

    if isinstance(value, datetime):
        return value.date().isoformat()

    if isinstance(value, date):
        return value.isoformat()

    if isinstance(value, Decimal):
        return format(value, "f")

    if isinstance(value, (bool, np.bool_)):
        return str(bool(value))

    if isinstance(value, (int, np.integer)):
        return str(int(value))

    return str(value)

# ----------------------------------------------------------
# 1. Authoritative dimension schemas and expected counts.
# ----------------------------------------------------------

SPECS = {
    "DimDate": {
        "file": "dim_date",
        "key": "DateKey",
        "rows": 761,
        "columns": [
            "DateKey", "FullDate", "Year", "Quarter",
            "MonthNumber", "MonthName", "MonthShortName",
            "YearMonth", "YearMonthSort", "WeekNumber",
            "WeekStartDate", "DayOfMonth", "DayName",
            "DayOfWeekNumber", "IsWeekend",
            "IsReportingPeriod", "FiscalYear",
            "FiscalQuarter", "FiscalMonthNumber"
        ]
    },
    "DimAirport": {
        "file": "dim_airport",
        "key": "AirportKey",
        "rows": 72,
        "columns": [
            "AirportKey", "AirportCode", "AirportName",
            "City", "Country", "CountryCode", "Region",
            "Latitude", "Longitude", "TimeZoneIANA", "IsActive"
        ]
    },
    "DimRoute": {
        "file": "dim_route",
        "key": "RouteKey",
        "rows": 320,
        "columns": [
            "RouteKey", "RouteCode", "OriginAirportKey",
            "DestinationAirportKey", "DistanceKM",
            "DistanceMiles", "RouteRegion",
            "IsInternational", "IsActive"
        ]
    },
    "DimAircraft": {
        "file": "dim_aircraft",
        "key": "AircraftKey",
        "rows": 440,
        "columns": [
            "AircraftKey", "AircraftRegistration", "AirlineKey",
            "AircraftTypeKey", "FleetEntryDate", "FleetStatus",
            "SeatCapacity", "PlannedDailyAvailableHours", "IsActive"
        ]
    },
    "DimAircraftType": {
        "file": "dim_aircraft_type",
        "key": "AircraftTypeKey",
        "rows": 12,
        "columns": [
            "AircraftTypeKey", "Manufacturer", "AircraftModel",
            "AircraftCategory", "TypicalSeatCapacity",
            "MaximumSeatCapacity", "RangeKM", "BodyType"
        ]
    },
    "DimCustomer": {
        "file": "dim_customer",
        "key": "CustomerKey",
        "rows": 5000,
        "columns": [
            "CustomerKey", "CustomerID", "CustomerSegment",
            "LoyaltyTier", "HomeCountry", "HomeCountryCode",
            "RegistrationDate", "IsActive"
        ]
    },
    "DimFareClass": {
        "file": "dim_fare_class",
        "key": "FareClassKey",
        "rows": 8,
        "columns": [
            "FareClassKey", "FareClassCode", "FareClassName",
            "CabinClass", "RefundabilityCategory",
            "IsAncillaryEligible", "DisplayOrder"
        ]
    },
    "DimBookingChannel": {
        "file": "dim_booking_channel",
        "key": "BookingChannelKey",
        "rows": 7,
        "columns": [
            "BookingChannelKey", "ChannelCode", "ChannelName",
            "ChannelCategory", "IsDirect", "IsActive"
        ]
    },
    "DimDisruptionType": {
        "file": "dim_disruption_type",
        "key": "DisruptionTypeKey",
        "rows": 9,
        "columns": [
            "DisruptionTypeKey", "DisruptionCode", "DisruptionName",
            "DisruptionCategory", "ControllableFlag",
            "ReactionaryEligibleFlag", "IsActive"
        ]
    },
    "DimCurrency": {
        "file": "dim_currency",
        "key": "CurrencyKey",
        "rows": 8,
        "columns": [
            "CurrencyKey", "CurrencyCode", "CurrencyName",
            "CurrencySymbol", "DecimalPlaces",
            "IsReportingCurrency"
        ]
    }
}

# ----------------------------------------------------------
# 2. Inspect every Parquet dimension, CSV and manifest.
# ----------------------------------------------------------

for name, spec in SPECS.items():

    stem = spec["file"]
    key = spec["key"]

    # Production audit: every dimension loads from production.
    dimension_curated = CURATED
    dimension_manifests = MANIFESTS

    parquet_path = dimension_curated / f"{stem}.parquet"
    csv_path = dimension_curated / f"{stem}.csv"
    manifest_path = dimension_manifests / f"{stem}_manifest.json"

    files_exist = all(
        path.exists()
        for path in [parquet_path, csv_path, manifest_path]
    )

    record(
        f"{name}: required files exist",
        files_exist,
        f"{parquet_path.name}, {csv_path.name}, {manifest_path.name}"
    )

    if not files_exist:
        continue

    try:
        df = pd.read_parquet(parquet_path)
        csv = pd.read_csv(
            csv_path,
            dtype=str,
            keep_default_na=False,
            encoding="utf-8-sig"
        )
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )

        loaded[name] = df

        record(
            f"{name}: exact column order",
            list(df.columns) == spec["columns"],
            list(df.columns)
        )

        record(
            f"{name}: expected record count",
            len(df) == spec["rows"],
            len(df)
        )

        record(
            f"{name}: unique primary key",
            df[key].is_unique,
            f"Key={key}; rows={len(df)}"
        )

        record(
            f"{name}: no null values",
            df.notna().all().all(),
            f"Null cells={int(df.isna().sum().sum())}"
        )

        record(
            f"{name}: CSV schema and row count",
            list(csv.columns) == spec["columns"]
            and len(csv) == spec["rows"],
            f"CSV rows={len(csv)}"
        )

        # Compare CSV and Parquet values by primary key.
        if (
            list(df.columns) == spec["columns"]
            and list(csv.columns) == spec["columns"]
            and df[key].is_unique
        ):
            csv_index = csv.set_index(key, drop=False)

            values_match = True
            mismatch_detail = ""

            for _, parquet_row in df.iterrows():
                pk_value = canonical(parquet_row[key])

                if pk_value not in csv_index.index:
                    values_match = False
                    mismatch_detail = f"Missing CSV key {pk_value}"
                    break

                csv_row = csv_index.loc[pk_value]

                for column in spec["columns"]:
                    left = canonical(parquet_row[column])
                    right = canonical(csv_row[column])

                    if left != right:
                        values_match = False
                        mismatch_detail = (
                            f"Key={pk_value}, column={column}, "
                            f"Parquet={left!r}, CSV={right!r}"
                        )
                        break

                if not values_match:
                    break

            record(
                f"{name}: CSV/Parquet value consistency",
                values_match,
                mismatch_detail or "All values match by primary key"
            )

        record(
            f"{name}: manifest counts and schema",
            manifest.get("row_count") == spec["rows"]
            and manifest.get("column_count") == len(spec["columns"])
            and manifest.get("columns") == spec["columns"],
            f"Manifest rows={manifest.get('row_count')}"
        )

        # Validate recorded file hashes.
        manifest_files = manifest.get("files", {})
        hashes_valid = True
        hash_details = []

        for fmt, path in [
            ("csv", csv_path),
            ("parquet", parquet_path)
        ]:
            metadata = manifest_files.get(fmt, {})
            expected_hash = metadata.get("sha256")

            actual_hash = sha256(path)

            if not expected_hash or expected_hash != actual_hash:
                hashes_valid = False
                hash_details.append(f"{fmt}: MISMATCH")
            else:
                hash_details.append(f"{fmt}: MATCH")

        record(
            f"{name}: SHA256 integrity",
            hashes_valid,
            "; ".join(hash_details)
        )

    except Exception as exc:
        record(
            f"{name}: load and inspection",
            False,
            f"{type(exc).__name__}: {exc}"
        )

# ----------------------------------------------------------
# 3. Inspect DimAirline in the reference workbook.
# ----------------------------------------------------------

workbook_path = (
    REFERENCE / "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"
)

airline_columns = [
    "AirlineKey", "AirlineId", "AirlineIATACode",
    "AirlineICAOCode", "AirlineName", "AirlineGroup",
    "HomeCountry", "HomeCountryCode", "BusinessModelClass",
    "IsActive", "StatusEffectiveDate", "ReferenceVersion"
]

airline_dimension = None
crosswalk = []

if workbook_path.exists():

    try:
        wb = load_workbook(
            workbook_path,
            read_only=True,
            data_only=True
        )

        sheet_exists = "DimAirline" in wb.sheetnames
        source_exists = "Airlines" in wb.sheetnames

        record(
            "DimAirline: required workbook sheets",
            sheet_exists and source_exists,
            wb.sheetnames
        )

        if sheet_exists and source_exists:

            ws = wb["DimAirline"]
            values = list(ws.iter_rows(values_only=True))

            headers = list(values[0])
            airline_dimension = pd.DataFrame(
                values[1:],
                columns=headers
            ).dropna(how="all")

            record(
                "DimAirline: exact schema",
                headers == airline_columns,
                headers
            )

            record(
                "DimAirline: ten records",
                len(airline_dimension) == 10,
                len(airline_dimension)
            )

            record(
                "DimAirline: unique permanent keys",
                airline_dimension["AirlineKey"].is_unique
                and set(
                    pd.to_numeric(
                        airline_dimension["AirlineKey"]
                    ).astype(int)
                ) == set(range(1, 11)),
                "Expected AirlineKey 1 through 10"
            )

            record(
                "DimAirline: unique durable IDs",
                airline_dimension["AirlineId"].is_unique,
                "AirlineId uniqueness"
            )

            record(
                "DimAirline: ten active baseline airlines",
                airline_dimension["IsActive"].eq(True).all(),
                "All baseline records active"
            )

            # Compare source and semantic airline identities by commercial name.
            source_ws = wb["Airlines"]
            source_values = list(
                source_ws.iter_rows(values_only=True)
            )

            source_headers = list(source_values[0])
            source_records = pd.DataFrame(
                source_values[1:],
                columns=source_headers
            ).dropna(how="all")

            required_source_fields = {
                "AirlineId", "AirlineKey", "AirlineName"
            }

            source_schema_ok = required_source_fields.issubset(
                set(source_headers)
            )

            record(
                "Airline source roster: required identity fields",
                source_schema_ok,
                sorted(required_source_fields)
            )

            if source_schema_ok:

                source_by_name = {
                    str(row["AirlineName"]): row
                    for _, row in source_records.iterrows()
                }

                dimension_by_name = {
                    str(row["AirlineName"]): row
                    for _, row in airline_dimension.iterrows()
                }

                names_match = (
                    set(source_by_name) == set(dimension_by_name)
                    and len(source_by_name) == 10
                )

                record(
                    "Airline source-to-dimension name coverage",
                    names_match,
                    f"Source={len(source_by_name)}; dimension={len(dimension_by_name)}"
                )

                if names_match:
                    for name in sorted(dimension_by_name):

                        source = source_by_name[name]
                        semantic = dimension_by_name[name]

                        source_id = str(source["AirlineId"])
                        semantic_id = str(semantic["AirlineId"])

                        crosswalk.append({
                            "AirlineName": name,
                            "SourceAirlineId": source_id,
                            "DimAirlineId": semantic_id,
                            "SourceAirlineKey": str(source["AirlineKey"]),
                            "DimAirlineKey": int(semantic["AirlineKey"]),
                            "AirlineIdMatches": (
                                source_id == semantic_id
                            )
                        })

                    mismatches = [
                        row for row in crosswalk
                        if not row["AirlineIdMatches"]
                    ]

                    if mismatches:
                        crosswalk_csv_path = (
                            REFERENCE / "AIRLINE_ID_CROSSWALK.csv"
                        )
                        crosswalk_manifest_path = (
                            MANIFESTS / "airline_id_crosswalk_manifest.json"
                        )

                        if (
                            crosswalk_csv_path.exists()
                            and crosswalk_manifest_path.exists()
                        ):
                            add_open_item(
                                "Airline identifier crosswalk approval",
                                (
                                    f"An explicit {len(mismatches)}-row "
                                    "identifier crosswalk exists and has been "
                                    "independently verified. Owner review, "
                                    "formal OD-01B approval and source "
                                    "authenticity review remain pending. "
                                    "Source and semantic identifiers must "
                                    "not be treated as interchangeable."
                                )
                            )
                        else:
                            add_open_item(
                                "Airline identifier crosswalk implementation",
                                (
                                    f"{len(mismatches)} source AirlineId values "
                                    "differ from semantic DimAirline AirlineId "
                                    "values. The explicit crosswalk or its "
                                    "manifest is missing."
                                )
                            )


        wb.close()

    except Exception as exc:
        record(
            "DimAirline workbook inspection",
            False,
            f"{type(exc).__name__}: {exc}"
        )

else:
    record(
        "DimAirline workbook exists",
        False,
        str(workbook_path)
    )

# ----------------------------------------------------------
# 3A. Independently validate the implemented airline crosswalk.
# ----------------------------------------------------------

crosswalk_csv_path = REFERENCE / "AIRLINE_ID_CROSSWALK.csv"
crosswalk_manifest_path = MANIFESTS / "airline_id_crosswalk_manifest.json"

if (
    crosswalk_csv_path.exists()
    and crosswalk_manifest_path.exists()
    and len(crosswalk) == 10
):
    try:
        xw = pd.read_csv(
            crosswalk_csv_path,
            dtype=str,
            keep_default_na=False,
            encoding="utf-8-sig"
        )

        xw_manifest = json.loads(
            crosswalk_manifest_path.read_text(encoding="utf-8")
        )

        expected_xw_columns = [
            "AirlineName",
            "SourceAirlineId",
            "DimAirlineId",
            "SourceAirlineKey",
            "DimAirlineKey",
            "AirlineIdMatches",
            "MappingStatus"
        ]

        record(
            "Airline crosswalk: exact schema and ten rows",
            list(xw.columns) == expected_xw_columns and len(xw) == 10,
            f"Rows={len(xw)}; columns={len(xw.columns)}"
        )

        unique_fields = [
            "AirlineName",
            "SourceAirlineId",
            "DimAirlineId",
            "SourceAirlineKey",
            "DimAirlineKey"
        ]

        unique_ok = all(xw[field].is_unique for field in unique_fields)

        record(
            "Airline crosswalk: unique identifiers",
            unique_ok,
            "Names, source IDs, semantic IDs and keys"
        )

        expected_by_name = {
            str(row["AirlineName"]): row
            for row in crosswalk
        }

        actual_by_name = {
            str(row["AirlineName"]): row
            for _, row in xw.iterrows()
        }

        exact_mapping = (
            set(expected_by_name) == set(actual_by_name)
            and len(actual_by_name) == 10
        )

        if exact_mapping:
            for name, expected in expected_by_name.items():
                actual = actual_by_name[name]

                comparisons = {
                    "SourceAirlineId": str(expected["SourceAirlineId"]),
                    "DimAirlineId": str(expected["DimAirlineId"]),
                    "SourceAirlineKey": str(expected["SourceAirlineKey"]),
                    "DimAirlineKey": str(int(expected["DimAirlineKey"])),
                    "AirlineIdMatches": str(
                        bool(expected["AirlineIdMatches"])
                    ).lower(),
                    "MappingStatus": "PROVISIONAL_REQUIRES_OWNER_REVIEW"
                }

                for field, expected_value in comparisons.items():
                    actual_value = str(actual[field]).strip()
                    expected_value = str(expected_value).strip()

                    # Boolean text is compared case-insensitively.
                    if field == "AirlineIdMatches":
                        actual_value = actual_value.casefold()
                        expected_value = expected_value.casefold()

                    if actual_value != expected_value:
                        exact_mapping = False
                        break

                if not exact_mapping:
                    break

        record(
            "Airline crosswalk: all ten mappings match workbook",
            exact_mapping,
            "Source and semantic identities reconciled by airline name"
        )

        approval = xw_manifest.get("approval", {})

        approval_pending = (
            xw_manifest.get("status")
            == "PROVISIONAL_REQUIRES_OWNER_REVIEW"
            and approval.get("owner_review") == "PENDING"
            and approval.get("formal_od01b_approval") == "PENDING"
            and approval.get("source_authenticity_review") == "PENDING"
            and all(
                str(v).lower() == "false"
                for v in xw["AirlineIdMatches"]
            )
        )

        record(
            "Airline crosswalk: provisional approval state preserved",
            approval_pending,
            "Owner, OD-01B and source-authenticity reviews remain pending"
        )

        crosswalk_hash_ok = (
            xw_manifest.get("crosswalk_csv_sha256")
            == sha256(crosswalk_csv_path)
        )

        workbook_hash_ok = (
            xw_manifest.get("source_files", {}).get(
                "airline_reference_workbook_sha256"
            )
            == sha256(workbook_path)
        )

        record(
            "Airline crosswalk: SHA256 integrity",
            crosswalk_hash_ok and workbook_hash_ok,
            "Crosswalk CSV and source workbook hashes"
        )

    except Exception as exc:
        record(
            "Airline crosswalk: independent audit",
            False,
            f"{type(exc).__name__}: {exc}"
        )
else:
    record(
        "Airline crosswalk: required artifacts exist",
        False,
        "Crosswalk CSV, manifest or ten-row mapping missing"
    )

# ----------------------------------------------------------
# 4. Cross-dimension referential integrity.
# ----------------------------------------------------------

if all(
    name in loaded
    for name in ["DimRoute", "DimAirport"]
):

    airports = loaded["DimAirport"]
    routes = loaded["DimRoute"]

    airport_keys = set(airports["AirportKey"].astype(int))

    route_origin_keys = set(
        routes["OriginAirportKey"].astype(int)
    )

    route_destination_keys = set(
        routes["DestinationAirportKey"].astype(int)
    )

    record(
        "DimRoute: origin airport foreign keys",
        route_origin_keys.issubset(airport_keys),
        f"Distinct origin airports={len(route_origin_keys)}"
    )

    record(
        "DimRoute: destination airport foreign keys",
        route_destination_keys.issubset(airport_keys),
        f"Distinct destination airports={len(route_destination_keys)}"
    )

    record(
        "DimRoute: every airport participates",
        route_origin_keys | route_destination_keys == airport_keys,
        f"Connected airports={len(route_origin_keys | route_destination_keys)}"
    )

    record(
        "DimRoute: origin differs from destination",
        (
            routes["OriginAirportKey"]
            != routes["DestinationAirportKey"]
        ).all(),
        "No self-referencing routes"
    )

if all(
    name in loaded
    for name in ["DimAircraft", "DimAircraftType"]
) and airline_dimension is not None:

    aircraft = loaded["DimAircraft"]
    aircraft_types = loaded["DimAircraftType"]

    valid_airline_keys = set(
        pd.to_numeric(
            airline_dimension["AirlineKey"]
        ).astype(int)
    )

    valid_type_keys = set(
        aircraft_types["AircraftTypeKey"].astype(int)
    )

    record(
        "DimAircraft: airline foreign keys",
        set(aircraft["AirlineKey"].astype(int)).issubset(
            valid_airline_keys
        ),
        "AirlineKey references resolve"
    )

    record(
        "DimAircraft: aircraft type foreign keys",
        set(aircraft["AircraftTypeKey"].astype(int)).issubset(
            valid_type_keys
        ),
        "AircraftTypeKey references resolve"
    )

    type_maximum = {
        int(row["AircraftTypeKey"]): int(row["MaximumSeatCapacity"])
        for _, row in aircraft_types.iterrows()
    }

    capacity_ok = all(
        int(row["SeatCapacity"])
        <= type_maximum[int(row["AircraftTypeKey"])]
        for _, row in aircraft.iterrows()
    )

    record(
        "DimAircraft: capacity compatible with type",
        capacity_ok,
        "Every aircraft within maximum type capacity"
    )

# ----------------------------------------------------------
# 5. Additional dimension business-rule checks.
# ----------------------------------------------------------

if "DimDate" in loaded:

    dates = loaded["DimDate"]
    full_dates = pd.to_datetime(dates["FullDate"])

    record(
        "DimDate: complete date range",
        full_dates.min() == pd.Timestamp("2024-10-01")
        and full_dates.max() == pd.Timestamp("2026-10-31"),
        f"{full_dates.min().date()} through {full_dates.max().date()}"
    )

    record(
        "DimDate: reporting-period population",
        int(dates["IsReportingPeriod"].sum()) == 365,
        f"Reporting rows={int(dates['IsReportingPeriod'].sum())}"
    )

    record(
        "DimDate: continuous calendar",
        full_dates.sort_values().diff().dropna().eq(
            pd.Timedelta(days=1)
        ).all(),
        "No missing dates"
    )

if "DimCurrency" in loaded:

    currency = loaded["DimCurrency"]

    reporting_rows = currency[
        currency["IsReportingCurrency"]
    ]

    record(
        "DimCurrency: exactly one USD reporting currency",
        len(reporting_rows) == 1
        and reporting_rows.iloc[0]["CurrencyCode"] == "USD",
        f"Reporting currency rows={len(reporting_rows)}"
    )

if "DimFareClass" in loaded:

    fare = loaded["DimFareClass"]

    record(
        "DimFareClass: unique display order within cabin",
        not fare.duplicated(
            ["CabinClass", "DisplayOrder"]
        ).any(),
        "Cabin-level sorting"
    )

if "DimBookingChannel" in loaded:

    booking = loaded["DimBookingChannel"]

    expected_direct = booking["ChannelCategory"].isin(
        ["Direct Web", "Mobile App"]
    )

    record(
        "DimBookingChannel: direct-channel classification",
        (booking["IsDirect"] == expected_direct).all(),
        "Only airline-owned direct channels are flagged direct"
    )

if "DimDisruptionType" in loaded:

    disruptions = loaded["DimDisruptionType"]

    reactionary = disruptions[
        disruptions["ReactionaryEligibleFlag"]
    ]

    record(
        "DimDisruptionType: reactionary taxonomy",
        len(reactionary) == 1
        and reactionary.iloc[0]["DisruptionCategory"] == "Reactionary",
        f"Reactionary-eligible types={len(reactionary)}"
    )

if "DimAircraft" in loaded:

    aircraft = loaded["DimAircraft"]

    record(
        "DimAircraft: active status consistency",
        (
            aircraft["IsActive"]
            == (aircraft["FleetStatus"] == "Active")
        ).all(),
        "Active flag follows fleet status"
    )

    expected_airline_keys = set(range(1, 11))

    airline_counts = {
        int(key): int(value)
        for key, value in aircraft.groupby("AirlineKey").size().items()
    }

    active_counts = {
        int(key): int(value)
        for key, value in aircraft[
            aircraft["IsActive"]
        ].groupby("AirlineKey").size().items()
    }

    maintenance_aircraft = aircraft[
        aircraft["FleetStatus"] == "Maintenance"
    ]

    maintenance_counts = {
        int(key): int(value)
        for key, value in maintenance_aircraft.groupby(
            "AirlineKey"
        ).size().items()
    }

    record(
        "DimAircraft: 44 aircraft per airline",
        airline_counts == {
            key: 44 for key in expected_airline_keys
        },
        f"Airlines represented={len(airline_counts)}"
    )

    record(
        "DimAircraft: 40 active aircraft per airline",
        active_counts == {
            key: 40 for key in expected_airline_keys
        },
        f"Airlines with 40 active records={sum(v == 40 for v in active_counts.values())}"
    )

    record(
        "DimAircraft: 4 maintenance aircraft per airline",
        maintenance_counts == {
            key: 4 for key in expected_airline_keys
        },
        f"Airlines with 4 maintenance records={sum(v == 4 for v in maintenance_counts.values())}"
    )

    record(
        "DimAircraft: 400 active and 40 maintenance globally",
        (
            int(aircraft["IsActive"].sum()) == 400
            and len(maintenance_aircraft) == 40
        ),
        (
            f"Active={int(aircraft['IsActive'].sum())}; "
            f"Maintenance={len(maintenance_aircraft)}"
        )
    )

    if "DimAircraftType" in loaded:

        aircraft_types = loaded["DimAircraftType"]

        actual_type_keys = set(
            aircraft["AircraftTypeKey"].astype(int)
        )

        record(
            "DimAircraft: all 12 aircraft types represented",
            actual_type_keys == set(range(1, 13)),
            f"Distinct aircraft types={len(actual_type_keys)}"
        )

        type_category = {
            int(row["AircraftTypeKey"]): str(row["AircraftCategory"])
            for _, row in aircraft_types.iterrows()
        }

        maintenance_with_category = maintenance_aircraft[
            ["AirlineKey", "AircraftTypeKey"]
        ].copy()

        maintenance_with_category["AircraftCategory"] = (
            maintenance_with_category["AircraftTypeKey"].map(type_category)
        )

        category_counts = maintenance_with_category.groupby(
            ["AirlineKey", "AircraftCategory"]
        ).size()

        expected_category_pairs = {
            (airline_key, str(category))
            for airline_key in expected_airline_keys
            for category in aircraft_types["AircraftCategory"].unique()
        }

        actual_category_pairs = {
            (int(index[0]), str(index[1]))
            for index in category_counts.index
        }

        record(
            "DimAircraft: one maintenance aircraft per category per airline",
            (
                actual_category_pairs == expected_category_pairs
                and (category_counts == 1).all()
            ),
            f"Maintenance airline-category combinations={len(category_counts)}"
        )

# ----------------------------------------------------------
# 6. Record outstanding issues honestly.
# ----------------------------------------------------------

add_open_item(
    "Airline reference approval",
    (
        "DimAirline records remain provisional. Formal OD-01B approval "
        "and airline source-authenticity review have not been established "
        "by this technical audit."
    )
)

add_open_item(
    "Aircraft availability assumption",
    (
        "PlannedDailyAvailableHours = 14.00 is implemented as a provisional "
        "baseline. Formal OD-10 approval remains pending."
    )
)

add_open_item(
    "Customer first-booking chronology",
    (
        "Customer registration dates are generated and validated. "
        "RegistrationDate <= first booking date must be tested after "
        "FactBookingTransactions is generated."
    )
)

add_open_item(
    "Provisional synthetic taxonomies",
    (
        "Airport, route, aircraft, fare, booking-channel and disruption "
        "baseline records are synthetic portfolio implementation data. "
        "Their provisional status must remain visible."
    )
)

# ----------------------------------------------------------
# 7. Final audit result and evidence report.
# ----------------------------------------------------------

passed = sum(x["status"] == "PASS" for x in results)
failed = sum(x["status"] == "FAIL" for x in results)

if failed:
    overall_status = "FAIL"
elif open_items:
    overall_status = "PASS_WITH_OPEN_ITEMS"
else:
    overall_status = "PASS"

report = {
    "project": "AEROVISION 360",
    "audit": "Consolidated Dimensional Model Audit",
    "status": overall_status,
    "disclosure": "Synthetic Simulation — Not Actual Airline Performance",
    "dimensions_expected": 11,
    "dimensions_loaded": len(loaded) + (
        1 if airline_dimension is not None else 0
    ),
    "expected_curated_dimension_records": sum(
        spec["rows"] for spec in SPECS.values()
    ),
    "airline_reference_records": (
        len(airline_dimension)
        if airline_dimension is not None else 0
    ),
    "total_dimension_records_including_airline": (
        sum(spec["rows"] for spec in SPECS.values())
        + (
            len(airline_dimension)
            if airline_dimension is not None else 0
        )
    ),
    "parquet_dimension_records": sum(
        len(df) for df in loaded.values()
    ),
    "checks_passed": passed,
    "checks_failed": failed,
    "open_item_count": len(open_items),
    "checks": results,
    "open_items": open_items,
    "airline_identifier_crosswalk_review": crosswalk,
    "fact_tables_started": False,
    "audit_timestamp": datetime.now().isoformat()
}

REPORT_PATH.write_text(
    json.dumps(report, indent=2, default=str),
    encoding="utf-8"
)

print("\n===== AEROVISION 360 CONSOLIDATED DIMENSION AUDIT =====")
print("DIMENSIONS EXPECTED: 11")
print("PARQUET DIMENSIONS LOADED:", len(loaded))
print(
    "DIM AIRLINE:",
    "LOADED" if airline_dimension is not None else "NOT LOADED"
)
print(
    "EXPECTED CURATED RECORDS:",
    report["expected_curated_dimension_records"]
)
print(
    "PARQUET RECORDS:",
    report["parquet_dimension_records"]
)
print(
    "AIRLINE REFERENCE RECORDS:",
    report["airline_reference_records"]
)
print(
    "TOTAL DIMENSION RECORDS:",
    report["total_dimension_records_including_airline"]
)

print("\nCHECK RESULTS")
for item in results:
    print(
        f"{item['status']}: {item['check']}"
        + (
            f" — {item['evidence']}"
            if item["status"] == "FAIL"
            else ""
        )
    )

print("\nCHECKS PASSED:", passed)
print("CHECKS FAILED:", failed)

print("\nOPEN ITEMS")
for item in open_items:
    print(f"OPEN: {item['title']}")
    print("  ", item["detail"])

print("\nOVERALL RESULT:", overall_status)
print("AUDIT REPORT:", REPORT_PATH)
print("SOURCE DATA MODIFIED: NO")
print("FACT TABLE GENERATION: NOT STARTED")
