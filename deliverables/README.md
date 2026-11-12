# AEROVISION 360 — Deliverables

## Excel

Open: `excel/AEROVISION_360_AIRLINE_ANALYTICS.xlsx`
- 12 sheets: Executive Dashboard, Flight Operations, Network Analysis, Disruption Analysis, Customer Intelligence, Airline Performance, Airport Analysis, Route Analysis, KPI Definitions, Data Dictionary, Data Quality, About & Disclaimer
- Values are calculated from `data/03_curated` parquet files (10 approved measures; FL02 = passenger count, not USD)
- Charts and formulas reference actual data; filters & freeze panes set
- Disclosure: Synthetic Simulation — Not Actual Airline Performance

## Power BI

Path: `power_bi/` — native project layout, import-ready
- `AEROVISION_360.pbip`, `.platform`, `report/report.json` (5 pages)
- Report pages:
  1. Executive Overview (FL01, FL02, FL03, airline comparison, trend)
  2. Network & Capacity Intelligence (route/airport/airline activity)
  3. Revenue & Yield Intelligence — OD-04 governance-blocked page (no financial values; exception text only)
  4. Operations & Disruption (FL04, DS01–DS03)
  5. Customer & Service Intelligence (CF01–CF03)
- Semantic model: `semantic_model/model.json`, `semantic_model/semantic_model.json`
- DAX: `dax/AEROVISION360_Measures.dax` — FL01–FL04, DS01–DS03, CF01–CF03
- Power Query: `power_query/AEROVISION360_DataLoad.m`
- Theme: `theme/theme.json`

To open in Power BI Desktop: Open `power_bi/AEROVISION_360.pbip`, import CSVs from `deliverables/data/`, apply M scripts, then add the DAX measures.

**Validation limitation:** `.pbip` files are validated as JSON structure only in this session. The binary `.pbix` cannot be generated without Power BI Desktop GUI export; Excel can be opened directly (openpyxl-verified). Diagrams were generated as placeholder JSON — the native layout is the authoritative deliverable.

## Data files

`deliverables/data/` — CSV + Parquet exports of the 11 dimensions & 3 facts from `data/03_curated/`
