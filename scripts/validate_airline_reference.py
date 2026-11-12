from pathlib import Path
from collections import Counter
from openpyxl import load_workbook
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "04_reference" / "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"

errors = []
warnings = []

def check(condition, message):
    if not condition:
        errors.append(message)

def report():
    print("\n===== AIRLINE REFERENCE VALIDATION =====")
    print("Workbook:", FILE)

    if not FILE.exists():
        print("[FAIL] Workbook does not exist.")
        return 1

    wb = load_workbook(FILE, data_only=False)

    expected_sheets = [
        "Airlines", "Source Register", "Reference Readme", "Change Log"
    ]
    check(wb.sheetnames == expected_sheets, "Unexpected worksheet structure.")

    air = wb["Airlines"]
    src = wb["Source Register"]

    headers = {c.value: c.column for c in air[1]}
    source_headers = {c.value: c.column for c in src[1]}

    required = [
        "AirlineId", "AirlineKey", "AirlineName", "IATA_Code",
        "IATA_AirlineCode", "ICAO_Code", "CountryISO2",
        "CountryName", "IdentityVerificationStatus"
    ]

    for field in required:
        check(field in headers, f"Missing Airlines column: {field}")

    source_required = [
        "SourceRecordId", "AirlineId", "AttributeName",
        "SourcePublisher", "SourceURL", "AccessedDate",
        "VerificationStatus"
    ]

    for field in source_required:
        check(field in source_headers, f"Missing Source Register column: {field}")

    if errors:
        wb.close()
        return print_results()

    records = []
    for row in range(2, air.max_row + 1):
        records.append({
            field: air.cell(row, col).value
            for field, col in headers.items()
        })

    check(len(records) == 10, f"Expected 10 airline records; found {len(records)}.")

    for field in ["AirlineId", "AirlineKey", "AirlineName", "IATA_Code",
                  "IATA_AirlineCode", "ICAO_Code"]:
        values = [r[field] for r in records if r[field] is not None]
        duplicates = [v for v, count in Counter(values).items() if count > 1]
        check(not duplicates, f"Duplicate {field} values: {duplicates}")

    for r in records:
        name = r["AirlineName"]
        airline_id = r["AirlineId"]

        check(bool(r["AirlineId"]), f"{name}: missing AirlineId.")
        check(bool(r["AirlineKey"]), f"{name}: missing AirlineKey.")
        check(bool(r["AirlineName"]), f"{airline_id}: missing AirlineName.")

        check(
            isinstance(r["IATA_Code"], str)
            and re.fullmatch(r"[A-Z0-9]{2}", r["IATA_Code"]) is not None,
            f"{name}: invalid two-character IATA designator."
        )

        numeric = r["IATA_AirlineCode"]
        check(
            isinstance(numeric, str)
            and re.fullmatch(r"\d{3}", numeric) is not None,
            f"{name}: invalid three-digit IATA code or leading zero lost."
        )

        check(
            isinstance(r["ICAO_Code"], str)
            and re.fullmatch(r"[A-Z]{3}", r["ICAO_Code"]) is not None,
            f"{name}: invalid ICAO code."
        )

        check(
            isinstance(r["CountryISO2"], str)
            and re.fullmatch(r"[A-Z]{2}", r["CountryISO2"]) is not None,
            f"{name}: invalid ISO alpha-2 code."
        )

        check(bool(r["CountryName"]), f"{name}: missing country name.")
        check(
            r["IdentityVerificationStatus"] == "PARTIALLY_VERIFIED",
            f"{name}: unexpected verification status."
        )

    # Check source-register identifiers and attribute coverage.
    source_rows = []
    for row in range(2, src.max_row + 1):
        source_rows.append({
            field: src.cell(row, col).value
            for field, col in source_headers.items()
        })

    source_ids = [r["SourceRecordId"] for r in source_rows]
    check(
        len(source_ids) == len(set(source_ids)),
        "Duplicate SourceRecordId values found."
    )

    expected_attributes = {
        "IATA_Code", "ICAO_Code", "CountryName",
        "CountryISO2", "IATA_AirlineCode"
    }

    for airline in records:
        airline_id = airline["AirlineId"]
        matching = [r for r in source_rows if r["AirlineId"] == airline_id]

        covered = {r["AttributeName"] for r in matching}
        missing = expected_attributes - covered

        check(
            not missing,
            f"{airline['AirlineName']}: missing source records for {sorted(missing)}."
        )

        for source in matching:
            check(
                bool(source["SourceURL"])
                and str(source["SourceURL"]).startswith("https://"),
                f"{airline_id}: missing or invalid HTTPS source URL."
            )
            check(
                source["VerificationStatus"] == "VERIFIED",
                f"{airline_id}: source record not marked VERIFIED."
            )

    check(
        "AirlineReference" in air.tables,
        "AirlineReference Excel table is missing."
    )

    if "AirlineReference" in air.tables:
        check(
            air.tables["AirlineReference"].ref == "A1:Q11",
            "AirlineReference table range is incorrect."
        )

    check(
        wb["Change Log"].max_row >= 4,
        "Expected three recorded workbook changes."
    )

    legal_names = sum(bool(r["LegalName"]) for r in records)
    check(legal_names == 9, f"Expected 9 legal names; found {legal_names}.")

    if any(not r["LegalName"] for r in records):
        warnings.append(
            "Southwest Airlines legal name remains pending source verification."
        )

    if any(
        r["IdentityVerificationStatus"] != "VERIFIED"
        for r in records
    ):
        warnings.append(
            "Airline records remain partially verified; this is intentional."
        )

    check(
        len(source_rows) == 59,
        f"Expected 59 source records; found {len(source_rows)}."
    )

    wb.close()
    return print_results()

def print_results():
    print("\n===== RESULTS =====")

    for warning in warnings:
        print("[WARNING]", warning)

    for error in errors:
        print("[FAIL]", error)

    if errors:
        print(f"\nVALIDATION FAILED: {len(errors)} issue(s).")
        return 1

    print("[PASS] Ten airline records")
    print("[PASS] Unique internal IDs, keys, names and airline codes")
    print("[PASS] IATA two-character designators")
    print("[PASS] Three-digit IATA codes, including leading zeroes")
    print("[PASS] ICAO code formats")
    print("[PASS] Country ISO alpha-2 formats")
    print("[PASS] Required source-register coverage")
    print("[PASS] HTTPS source URL presence")
    print("[PASS] Excel table structure")
    print("[PASS] Change log structure")
    print("[PASS] Nine legal names; one intentionally pending")

    print("\nSTRUCTURAL VALIDATION: PASSED")
    print("SOURCE AUTHENTICITY: REQUIRES SEPARATE SOURCE REVIEW")
    return 0

sys.exit(report())
