from pathlib import Path
from datetime import date
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "04_reference" / "AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx"

airlines = [
    ("AIR001", "A360-AIR-001", "Emirates"),
    ("AIR002", "A360-AIR-002", "Qatar Airways"),
    ("AIR003", "A360-AIR-003", "Singapore Airlines"),
    ("AIR004", "A360-AIR-004", "Air India"),
    ("AIR005", "A360-AIR-005", "IndiGo"),
    ("AIR006", "A360-AIR-006", "British Airways"),
    ("AIR007", "A360-AIR-007", "Lufthansa"),
    ("AIR008", "A360-AIR-008", "Delta Air Lines"),
    ("AIR009", "A360-AIR-009", "Southwest Airlines"),
    ("AIR010", "A360-AIR-010", "Qantas"),
]

wb = Workbook()
ws = wb.active
ws.title = "Airlines"

navy = "17365D"
blue = "D9EAF7"
light = "F3F6FA"
white = "FFFFFF"
grey = "666666"
thin_grey = Side(style="thin", color="D9E1F2")

def style_sheet(sheet, widths):
    sheet.freeze_panes = "A2"
    sheet.sheet_view.showGridLines = False
    for col, width in widths.items():
        sheet.column_dimensions[col].width = width
    for cell in sheet[1]:
        cell.fill = PatternFill("solid", fgColor=navy)
        cell.font = Font(name="Aptos", bold=True, color=white)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = Border(bottom=thin_grey)
    sheet.row_dimensions[1].height = 32

# AIRLINES
headers = [
    "AirlineId", "AirlineKey", "AirlineName", "LegalName",
    "IATA_Code", "ICAO_Code", "CountryISO2", "CountryName",
    "BusinessModelClass", "AirlineGroup", "IsActive",
    "StatusEffectiveDate", "IdentityVerificationStatus",
    "RosterOrigin", "ReferenceVersion", "Notes"
]
ws.append(headers)

for airline_id, airline_key, name in airlines:
    ws.append([
        airline_id, airline_key, name, None, None, None, None, None,
        None, None, None, None, "PENDING_SOURCE_VERIFICATION",
        "PROJECT_SCOPE_ROSTER", "A360-REF-0.1-DRAFT",
        "Identity attributes require source verification before reference release."
    ])

style_sheet(ws, {
    "A": 14, "B": 19, "C": 25, "D": 30, "E": 13, "F": 13,
    "G": 14, "H": 20, "I": 22, "J": 20, "K": 12, "L": 20,
    "M": 32, "N": 23, "O": 23, "P": 65
})
ws.auto_filter.ref = f"A1:P{ws.max_row}"
table = Table(displayName="AirlineReference", ref=f"A1:P{ws.max_row}")
table.tableStyleInfo = TableStyleInfo(
    name="TableStyleMedium2",
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=False
)
ws.add_table(table)

status_validation = DataValidation(
    type="list",
    formula1='"PENDING_SOURCE_VERIFICATION,VERIFIED,REJECTED"',
    allow_blank=False
)
status_validation.error = "Select a listed verification status."
status_validation.errorTitle = "Invalid verification status"
status_validation.showErrorMessage = True
ws.add_data_validation(status_validation)
status_validation.add(f"M2:M{ws.max_row}")

active_validation = DataValidation(
    type="list",
    formula1='"TRUE,FALSE"',
    allow_blank=True
)
active_validation.showErrorMessage = True
ws.add_data_validation(active_validation)
active_validation.add(f"K2:K{ws.max_row}")

# SOURCE REGISTER
src = wb.create_sheet("Source Register")
src_headers = [
    "SourceRecordId", "AirlineId", "AttributeName", "SourcePublisher",
    "SourceTitle", "SourceURL", "AccessedDate",
    "VerificationStatus", "EvidenceNotes"
]
src.append(src_headers)
style_sheet(src, {
    "A": 18, "B": 14, "C": 22, "D": 28, "E": 38,
    "F": 55, "G": 18, "H": 28, "I": 60
})
src.freeze_panes = "A2"
src.auto_filter.ref = "A1:I1"

source_status = DataValidation(
    type="list",
    formula1='"PENDING,VERIFIED,REJECTED,STALE"',
    allow_blank=True
)
src.add_data_validation(source_status)
source_status.add("H2:H1000")

# REFERENCE README
readme = wb.create_sheet("Reference Readme")
readme.append(["Topic", "Definition"])
readme_rows = [
    ("Project", "AEROVISION 360 — Global Multi-Airline Operations & Revenue Intelligence Platform"),
    ("Workbook purpose", "Controlled reference workbook for the ten-airline project population."),
    ("Simulation boundary", "Airline identities are real-world reference entities; operational and financial activity is synthetic."),
    ("Mandatory disclosure", "Synthetic Simulation — Not Actual Airline Performance"),
    ("AirlineId", "Internal stable identifier assigned within this project. It is not an external airline code."),
    ("AirlineKey", "Internal stable business key assigned within this project."),
    ("AirlineName", "Airline display name from the project roster; external identity attributes remain subject to verification."),
    ("Identity verification", "Do not mark an attribute VERIFIED without a traceable supporting source record."),
    ("Unverified values", "Leave unverified identity attributes blank. Do not invent IATA, ICAO, country, legal name, or group values."),
    ("BusinessModelClass", "Optional nullable analytical classification. Leave blank until a documented classification rubric is approved."),
    ("AirlineGroup", "Optional. Populate only when supported by a traceable source and appropriate effective date."),
    ("IsActive", "Reference status attribute. Do not infer without verification and an effective date."),
    ("Source Register", "Record one source-to-attribute evidence entry per verified reference attribute."),
    ("Reference version", "A360-REF-0.1-DRAFT. Increment when a controlled reference release is produced."),
    ("Data privacy", "No real passenger personal information may be entered into this project."),
    ("Workbook status", "Initial structure created; airline identity attributes have not yet been source-verified."),
]
for row in readme_rows:
    readme.append(row)
style_sheet(readme, {"A": 27, "B": 110})
for row in readme.iter_rows(min_row=2):
    row[1].alignment = Alignment(wrap_text=True, vertical="top")
    readme.row_dimensions[row[0].row].height = 32
readme.auto_filter.ref = f"A1:B{readme.max_row}"

# CHANGE LOG
log = wb.create_sheet("Change Log")
log.append(["ChangeId", "Date", "ReferenceVersion", "ChangeDescription", "ChangedBy", "Evidence"])
log.append([
    "CHG-0001", date.today().isoformat(), "A360-REF-0.1-DRAFT",
    "Initial reference workbook structure and ten-airline project roster created. Identity attributes remain pending verification.",
    "Project owner workflow", "Initial workbook generation"
])
style_sheet(log, {"A": 16, "B": 16, "C": 24, "D": 85, "E": 25, "F": 35})
log.auto_filter.ref = "A1:F2"

# Workbook metadata
wb.properties.title = "AEROVISION 360 Airline Reference Workbook"
wb.properties.subject = "Controlled airline identity reference and source provenance"
wb.properties.creator = "AEROVISION 360 Project"
wb.properties.description = (
    "Synthetic BI portfolio project reference workbook. "
    "Identity attributes require source verification."
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUTPUT)

# Re-open and validate the saved artifact.
check = load_workbook(OUTPUT, read_only=False, data_only=False)
expected_sheets = ["Airlines", "Source Register", "Reference Readme", "Change Log"]
assert check.sheetnames == expected_sheets, check.sheetnames
assert check["Airlines"].max_row == 11, check["Airlines"].max_row
assert check["Airlines"].max_column == 16, check["Airlines"].max_column
assert check["Airlines"]["M2"].value == "PENDING_SOURCE_VERIFICATION"
assert check["Airlines"]["C11"].value == "Qantas"
check.close()

print("WORKBOOK_CREATED")
print(f"PATH: {OUTPUT}")
print(f"SIZE_BYTES: {OUTPUT.stat().st_size}")
print(f"AIRLINE_ROWS: {len(airlines)}")
print(f"WORKSHEETS: {', '.join(expected_sheets)}")
print("VALIDATION: PASSED")
print("IDENTITY_VERIFICATION: PENDING — NO UNVERIFIED ATTRIBUTES FABRICATED")
