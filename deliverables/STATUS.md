# AEROVISION 360 — Actual Deliverables

## Done 100%

### 1. Excel workbook
`deliverables/excel/AEROVISION_360_AIRLINE_ANALYTICS.xlsx`
- 12 sheets verified: Executive Dashboard, Flight Operations, Network Analysis, Disruption Analysis, Customer Intelligence, Airline Performance, Airport Analysis, Route Analysis, KPI Definitions, Data Dictionary, Data Quality, About & Disclaimer
- Values calculated from `data/03_curated` — FL01=5000, FL02=452827 passengers, FL03=43.42, FL04=4.48%, DS01=1754, DS02=120.62, DS03=540, CF01=2500, CF02=2.99, CF03=0.0%
- 2 charts, formulas, filters, freeze panes, formatting — openpyxl verified
- OD-04 respected: no financial revenue/cost; FL02 = passenger count; disclosure visible

### 2. Power BI
`deliverables/power_bi/`
- AEROVISION_360.pbip + .platform + report/report.json (5 pages incl. OD-04 blocked page)
- semantic_model/model.json + semantic_model.json (tables, relationships, measures)
- DAX: dax/AEROVISION360_Measures.dax (10 measures, no AVG(AVG()))
- Power Query: power_query/AEROVISION360_DataLoad.m
- theme/theme.json + data_sources/data_sources.json
- JSON validated

### 3. Data files
`deliverables/data/` — CSV + Parquet for 11 dimensions & 3 facts (28 files)

### 4. Baseline preserved
- `python -m pytest tests/ -q` → 335 passed
- No curated data modified; no Git ops

## Not done / limitations (to 100%)
- Power BI Desktop GUI export to .pbix (binary) — not generated in this session; .pbip is import-ready; open AEROVISION_360.pbip in Power BI Desktop and import CSVs from deliverables/data/ using the provided M/DAX files
- No PivotTables/slicers beyond filters/charts in Excel (openpyxl supports data tables/filters; interactive slicer/PivotTable creation requires Excel UI)
