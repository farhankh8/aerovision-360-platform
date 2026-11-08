from pathlib import Path
from datetime import datetime
from shutil import copy2
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.comments import Comment
import hashlib

root = Path(__file__).resolve().parents[1]
workbook = root / "data/04_reference/AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"
backup_dir = root / "data/04_reference/backups"

if not workbook.exists():
    raise FileNotFoundError(workbook)

backup_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = backup_dir / f"AIRLINE_REFERENCE_PRE_DIM_AIRLINE_{timestamp}.xlsx"

if backup.exists():
    raise FileExistsError(backup)

original_hash = hashlib.sha256(workbook.read_bytes()).hexdigest()
copy2(workbook, backup)

backup_hash = hashlib.sha256(backup.read_bytes()).hexdigest()
if original_hash != backup_hash:
    raise RuntimeError("Backup verification failed. Workbook not modified.")

wb = load_workbook(workbook)

if "DimAirline" in wb.sheetnames:
    raise RuntimeError("DimAirline sheet already exists. No changes made.")

source = wb["Airlines"]
headers = {cell.value: cell.column for cell in source[1]}

required = [
    "AirlineName", "IATA_Code", "ICAO_Code",
    "CountryISO2", "CountryName", "IsActive"
]

missing = [field for field in required if field not in headers]
if missing:
    raise RuntimeError(f"Missing source columns: {missing}")

output_headers = [
    "AirlineKey",
    "AirlineId",
    "AirlineIATACode",
    "AirlineICAOCode",
    "AirlineName",
    "AirlineGroup",
    "HomeCountry",
    "HomeCountryCode",
    "BusinessModelClass",
    "IsActive",
    "StatusEffectiveDate",
    "ReferenceVersion"
]

ws = wb.create_sheet("DimAirline")
ws.append(output_headers)

version = "AIR-2026-11-04-001"

for row_number in range(2, source.max_row + 1):
    get = lambda field: source.cell(row_number, headers[field]).value

    airline_name = get("AirlineName")
    if not airline_name:
        continue

    numeric_key = row_number - 1

    ws.append([
        numeric_key,
        f"AIR-{numeric_key:04d}",
        get("IATA_Code"),
        get("ICAO_Code"),
        airline_name,
        None,
        get("CountryName"),
        get("CountryISO2"),
        None,
        True,
        None,
        version
    ])

ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:L{ws.max_row}"
ws.sheet_view.showGridLines = False

for cell in ws[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="17365D")
    cell.alignment = Alignment(horizontal="center", vertical="center")

for column in ws.columns:
    letter = column[0].column_letter
    max_length = max(len(str(c.value or "")) for c in column)
    ws.column_dimensions[letter].width = min(max(max_length + 3, 14), 32)

table = Table(displayName="DimAirlineTable", ref=f"A1:L{ws.max_row}")
table.tableStyleInfo = TableStyleInfo(
    name="TableStyleMedium2",
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=False
)
ws.add_table(table)

ws["A1"].comment = Comment(
    "Provisional warehouse surrogate key. Uses the proposed administrative allocation; formal reference approval remains pending.",
    "AEROVISION 360"
)
ws["B1"].comment = Comment(
    "Durable project business identifier. Provisional mapping follows the contract's proposed allocation.",
    "AEROVISION 360"
)
ws["L1"].comment = Comment(
    "Technical snapshot identifier. This value does not represent formal approval.",
    "AEROVISION 360"
)

readme = wb["Reference Readme"]
readme.append([])
readme.append(["DimAirline semantic dimension"])
readme.append(["Status", "PROVISIONAL — identity source review and formal reference approval pending"])
readme.append(["Source", "Derived from the Airlines reference worksheet"])
readme.append(["ReferenceVersion", version])
readme.append(["Key mapping", "Proposed contract allocation; not a newly inferred identity attribute"])
readme.append(["LegalName", "Retained only in reference data; excluded from DimAirline"])
readme.append(["BusinessModelClass", "NULL pending an approved analytical classification"])
readme.append(["AirlineGroup", "NULL unless a verified source supports the value"])

wb.save(workbook)

# Reopen and verify the saved workbook.
check = load_workbook(workbook, data_only=False)
dim = check["DimAirline"]

assert dim.max_row == 11, f"Expected 10 airlines; got {dim.max_row - 1}"
assert dim.max_column == 12, f"Expected 12 columns; got {dim.max_column}"
assert list(dim.tables.keys()) == ["DimAirlineTable"]
assert [dim.cell(r, 1).value for r in range(2, 12)] == list(range(1, 11))
assert [dim.cell(r, 2).value for r in range(2, 12)] == [
    f"AIR-{i:04d}" for i in range(1, 11)
]
assert all(dim.cell(r, 9).value is None for r in range(2, 12))
assert all(dim.cell(r, 6).value is None for r in range(2, 12))

check.close()

print("DIM_AIRLINE_CREATED")
print("ROWS:", dim.max_row - 1)
print("COLUMNS:", dim.max_column)
print("REFERENCE_VERSION:", version)
print("STATUS: PROVISIONAL")
print("BACKUP:", backup)
print("VALIDATION: PASSED")
