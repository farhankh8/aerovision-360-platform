from pathlib import Path
from copy import copy
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "04_reference" / "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"

VERSION = "A360-REF-0.3-DRAFT"
DATE = "2026-11-04"
BASE = "https://www.iata.org/en/about/members/airline-list/"

records = [
    ("AIR001", "Emirates", "176", 15),
    ("AIR002", "Qatar Airways", "157", 30),
    ("AIR003", "Singapore Airlines", "618", 32),
    ("AIR004", "Air India", "098", 4),
    ("AIR005", "IndiGo", "312", 20),
    ("AIR006", "British Airways", "125", 10),
    ("AIR007", "Lufthansa", "220", 25),
    ("AIR008", "Delta Air Lines", "006", 14),
    ("AIR009", "Southwest Airlines", "526", 33),
    ("AIR010", "Qantas", "081", 30),
]

wb = load_workbook(FILE)
air = wb["Airlines"]
src = wb["Source Register"]
log = wb["Change Log"]
readme = wb["Reference Readme"]

if air.max_row != 11:
    raise RuntimeError("Unexpected airline row count.")
if src.max_row != 50:
    raise RuntimeError(f"Expected 49 source records; found {src.max_row - 1}.")
if any("IATA_AirlineCode" == c.value for c in air[1]):
    raise RuntimeError("IATA_AirlineCode already exists; refusing duplicate insertion.")

headers = {c.value: c.column for c in air[1]}
id_col = headers["AirlineId"]

row_map = {
    air.cell(row, id_col).value: row
    for row in range(2, air.max_row + 1)
}

if set(row_map) != {r[0] for r in records}:
    raise RuntimeError("Airline ID roster mismatch.")

# Insert the numeric code as a distinct field after the two-character designator.
air.insert_cols(6, 1)
air["F1"] = "IATA_AirlineCode"
air["F1"]._style = copy(air["E1"]._style)
air["F1"].alignment = copy(air["E1"].alignment)
air.column_dimensions["F"].width = 18

# Rebuild the table so its range and headers match the new schema.
for table_name in list(air.tables.keys()):
    del air.tables[table_name]

table = Table(displayName="AirlineReference", ref="A1:Q11")
table.tableStyleInfo = TableStyleInfo(
    name="TableStyleMedium2",
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=False
)
air.add_table(table)

# Remove and recreate validations because the inserted column shifts fields.
air.data_validations.dataValidation = []

status_validation = DataValidation(
    type="list",
    formula1='"PENDING_SOURCE_VERIFICATION,PARTIALLY_VERIFIED,VERIFIED,REJECTED"',
    allow_blank=False
)
status_validation.showErrorMessage = True
status_validation.error = "Choose a valid verification status."
air.add_data_validation(status_validation)
status_validation.add("N2:N11")

active_validation = DataValidation(
    type="list",
    formula1='"TRUE,FALSE"',
    allow_blank=True
)
active_validation.showErrorMessage = True
air.add_data_validation(active_validation)
active_validation.add("L2:L11")

# Store all numeric codes as text to preserve leading zeroes.
for airline_id, name, numeric_code, page in records:
    row = row_map[airline_id]
    air.cell(row, 6).number_format = "@"
    air.cell(row, 6).value = numeric_code
    air.cell(row, 16).value = VERSION

# Add provenance for the numeric IATA airline code.
src_headers = {c.value: c.column for c in src[1]}
next_id = src.max_row

for airline_id, name, numeric_code, page in records:
    next_id += 1
    source_url = f"{BASE}?All=true&page={page}"
    values = {
        "SourceRecordId": f"SRC-{next_id - 1:04d}",
        "AirlineId": airline_id,
        "AttributeName": "IATA_AirlineCode",
        "SourcePublisher": "International Air Transport Association (IATA)",
        "SourceTitle": "Current Airline Members — IATA three-digit airline code",
        "SourceURL": source_url,
        "AccessedDate": DATE,
        "VerificationStatus": "VERIFIED",
        "EvidenceNotes": (
            f"IATA current airline member directory; three-digit code for {name}. "
            "Stored as text to preserve leading zeroes."
        ),
    }
    for field, value in values.items():
        src.cell(next_id, src_headers[field]).value = value

# Update workbook documentation.
readme.append([
    "IATA_AirlineCode",
    "Three-digit IATA airline code. Store as text because leading zeroes are significant."
])

for row in readme.iter_rows(min_row=2):
    if row[0].value == "Workbook status":
        row[1].value = (
            "Ten-airline roster with two-character IATA designators, three-digit "
            "IATA airline codes, ICAO codes, country names and ISO alpha-2 codes. "
            "Southwest legal name remains pending. Airline records remain partially verified."
        )

log.append([
    "CHG-0003",
    DATE,
    VERSION,
    "Added the distinct three-digit IATA airline code field, preserved leading zeroes as text, added ten attribute-level IATA directory source records, and rebuilt the Airlines Excel table and dropdown validations.",
    "Project owner workflow",
    "IATA Current Airline Members directory"
])

# Save and reopen for structural and data checks.
wb.save(FILE)

check = load_workbook(FILE, data_only=False)
a = check["Airlines"]
s = check["Source Register"]

assert a.max_row == 11
assert a.max_column == 17
assert s.max_row == 60
assert "IATA_AirlineCode" == a["F1"].value
assert a.tables["AirlineReference"].ref == "A1:Q11"

expected = {r[0]: r[2] for r in records}
for row in range(2, 12):
    airline_id = a.cell(row, 1).value
    code = a.cell(row, 6).value
    assert code == expected[airline_id], (airline_id, code)
    assert isinstance(code, str), (airline_id, type(code))
    assert a.cell(row, 14).value == "PARTIALLY_VERIFIED"

assert a["F5"].value == "098"
assert a["F9"].value == "006"
assert a["F11"].value == "081"

check.close()

print("IATA_NUMERIC_CODES_ADDED")
print(f"FILE: {FILE}")
print("AIRLINES: 10")
print("NEW_FIELD: IATA_AirlineCode")
print("NEW_SOURCE_RECORDS: 10")
print("TOTAL_SOURCE_RECORDS: 59")
print("LEADING_ZERO_CHECKS: 098, 006, 081 PASSED")
print("EXCEL_TABLE: A1:Q11")
print("VALIDATION: PASSED")
