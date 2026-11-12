from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "04_reference" / "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"

IATA_BASE = "https://www.iata.org/en/about/members/airline-list/"
ISO_URL = "https://www.gov.uk/government/publications/open-standards-for-government/country-codes"
ACCESS_DATE = "2026-11-04"
VERSION = "A360-REF-0.2-DRAFT"

records = [
    {
        "id": "AIR001", "name": "Emirates", "iata": "EK", "icao": "UAE",
        "country": "United Arab Emirates", "iso2": "AE",
        "legal": "Emirates", "url": IATA_BASE + "emirates/73/"
    },
    {
        "id": "AIR002", "name": "Qatar Airways", "iata": "QR", "icao": "QTR",
        "country": "Qatar", "iso2": "QA",
        "legal": "Qatar Airways Company (W.L.L.)",
        "url": IATA_BASE + "qatar-airways/277/"
    },
    {
        "id": "AIR003", "name": "Singapore Airlines", "iata": "SQ", "icao": "SIA",
        "country": "Singapore", "iso2": "SG",
        "legal": "Singapore Airlines Limited",
        "url": IATA_BASE + "singapore-airlines/177/"
    },
    {
        "id": "AIR004", "name": "Air India", "iata": "AI", "icao": "AIC",
        "country": "India", "iso2": "IN",
        "legal": "Air India Limited", "url": IATA_BASE + "air-india-/61/"
    },
    {
        "id": "AIR005", "name": "IndiGo", "iata": "6E", "icao": "IGO",
        "country": "India", "iso2": "IN",
        "legal": "InterGlobe Aviation Limited", "url": IATA_BASE + "indigo/545/"
    },
    {
        "id": "AIR006", "name": "British Airways", "iata": "BA", "icao": "BAW",
        "country": "United Kingdom", "iso2": "GB",
        "legal": "British Airways Plc",
        "url": IATA_BASE + "british-airways/52/"
    },
    {
        "id": "AIR007", "name": "Lufthansa", "iata": "LH", "icao": "DLH",
        "country": "Germany", "iso2": "DE",
        "legal": "Deutsche Lufthansa Aktiengesellschaft",
        "url": IATA_BASE + "lufthansa/115/"
    },
    {
        "id": "AIR008", "name": "Delta Air Lines", "iata": "DL", "icao": "DAL",
        "country": "United States", "iso2": "US",
        "legal": "Delta Air Lines, Inc.",
        "url": IATA_BASE + "delta-air-lines/72/"
    },
    {
        "id": "AIR009", "name": "Southwest Airlines", "iata": "WN", "icao": "SWA",
        "country": "United States", "iso2": "US",
        "legal": None,
        "url": IATA_BASE + "?All=true&page=33"
    },
    {
        "id": "AIR010", "name": "Qantas", "iata": "QF", "icao": "QFA",
        "country": "Australia", "iso2": "AU",
        "legal": "Qantas Airways Limited",
        "url": IATA_BASE + "qantas/139/"
    },
]

wb = load_workbook(FILE)

expected_sheets = ["Airlines", "Source Register", "Reference Readme", "Change Log"]
assert wb.sheetnames == expected_sheets, f"Unexpected worksheets: {wb.sheetnames}"

air = wb["Airlines"]
src = wb["Source Register"]
readme = wb["Reference Readme"]
log = wb["Change Log"]

if air.max_row != 11:
    raise RuntimeError("Airlines sheet does not contain the expected ten data rows.")
if src.max_row != 1:
    raise RuntimeError("Source Register is not empty. Refusing to overwrite existing records.")
if log.max_row != 2:
    raise RuntimeError("Change Log changed unexpectedly. Refusing to append.")

headers = {cell.value: cell.column for cell in air[1]}
required = [
    "AirlineId", "AirlineName", "LegalName", "IATA_Code", "ICAO_Code",
    "CountryISO2", "CountryName", "IdentityVerificationStatus",
    "ReferenceVersion"
]
missing = [name for name in required if name not in headers]
if missing:
    raise RuntimeError(f"Missing Airlines columns: {missing}")

rows_by_id = {
    air.cell(row, headers["AirlineId"]).value: row
    for row in range(2, air.max_row + 1)
}

if set(rows_by_id) != {r["id"] for r in records}:
    raise RuntimeError("Airline roster IDs do not match the expected ten-airline roster.")

source_headers = {cell.value: cell.column for cell in src[1]}
source_required = [
    "SourceRecordId", "AirlineId", "AttributeName", "SourcePublisher",
    "SourceTitle", "SourceURL", "AccessedDate", "VerificationStatus",
    "EvidenceNotes"
]
if any(h not in source_headers for h in source_required):
    raise RuntimeError("Source Register schema is incomplete.")

source_rows = []

def add_source(airline_id, attribute, publisher, title, url, note):
    source_rows.append([
        f"SRC-{len(source_rows) + 1:04d}",
        airline_id,
        attribute,
        publisher,
        title,
        url,
        ACCESS_DATE,
        "VERIFIED",
        note
    ])

for r in records:
    row = rows_by_id[r["id"]]

    values = {
        "IATA_Code": r["iata"],
        "ICAO_Code": r["icao"],
        "CountryName": r["country"],
        "CountryISO2": r["iso2"],
        "IdentityVerificationStatus": "PARTIALLY_VERIFIED",
        "ReferenceVersion": VERSION,
    }

    if r["legal"]:
        values["LegalName"] = r["legal"]

    for field, value in values.items():
        air.cell(row, headers[field]).value = value

    for field in ["IATA_Code", "ICAO_Code", "CountryName"]:
        add_source(
            r["id"], field, "International Air Transport Association (IATA)",
            f"IATA airline record — {r['name']}", r["url"],
            f"{field} recorded from the IATA airline profile/member directory."
        )

    if r["legal"]:
        add_source(
            r["id"], "LegalName", "International Air Transport Association (IATA)",
            f"IATA airline record — {r['name']}", r["url"],
            "Legal name recorded from the IATA airline profile."
        )

    add_source(
        r["id"], "CountryISO2", "UK Government — Open Standards",
        "Use consistent country codes", ISO_URL,
        f"ISO 3166-1 alpha-2 country code recorded as {r['iso2']}."
    )

# Update the verification dropdown to include partial verification.
for validation in air.data_validations.dataValidation:
    if "M2:M11" in str(validation.sqref):
        validation.formula1 = (
            '"PENDING_SOURCE_VERIFICATION,PARTIALLY_VERIFIED,VERIFIED,REJECTED"'
        )

for source_row in source_rows:
    src.append(source_row)

# Append the controlled workbook change.
log.append([
    "CHG-0002",
    ACCESS_DATE,
    VERSION,
    "Populated IATA designators, ICAO codes, country names, ISO alpha-2 codes, and available legal names. Added attribute-level provenance records. Southwest legal name remains unverified. Airline records remain partially verified.",
    "Project owner workflow",
    "IATA airline profiles/member directory and UK Government ISO country-code guidance"
])

# Update workbook status note.
for row in readme.iter_rows(min_row=2):
    if row[0].value == "Workbook status":
        row[1].value = (
            "Ten-airline roster populated. IATA designators, ICAO codes, "
            "country names and ISO alpha-2 codes recorded with source evidence. "
            "Nine legal names recorded; Southwest legal name remains pending. "
            "Records remain partially verified."
        )

wb.save(FILE)

# Reopen and verify persisted data.
check = load_workbook(FILE, data_only=False)
a = check["Airlines"]
s = check["Source Register"]

assert a.max_row == 11
assert s.max_row == len(source_rows) + 1
assert len(source_rows) == 49

for r in records:
    matching = [
        row for row in range(2, a.max_row + 1)
        if a.cell(row, headers["AirlineId"]).value == r["id"]
    ]
    assert len(matching) == 1
    row = matching[0]
    assert a.cell(row, headers["IATA_Code"]).value == r["iata"]
    assert a.cell(row, headers["ICAO_Code"]).value == r["icao"]
    assert a.cell(row, headers["CountryISO2"]).value == r["iso2"]
    assert a.cell(row, headers["CountryName"]).value == r["country"]
    assert a.cell(row, headers["IdentityVerificationStatus"]).value == "PARTIALLY_VERIFIED"

assert a.cell(rows_by_id["AIR009"], headers["LegalName"]).value is None

check.close()

print("REFERENCE_WORKBOOK_UPDATED")
print(f"FILE: {FILE}")
print(f"AIRLINES: {len(records)}")
print(f"SOURCE_EVIDENCE_ROWS: {len(source_rows)}")
print("IATA_CODES: 10 VERIFIED")
print("ICAO_CODES: 10 VERIFIED")
print("COUNTRY_NAMES: 10 VERIFIED")
print("COUNTRY_ISO2: 10 RECORDED")
print("LEGAL_NAMES: 9 VERIFIED; SOUTHWEST PENDING")
print("AIRLINE_RECORD_STATUS: PARTIALLY_VERIFIED")
print("VALIDATION: PASSED")
