# Power BI Remediation Plan — AEROVISION 360

## P0 — Critical data or model correctness
1. Do not treat `semantic_model/model.json` as valid PBIX model: it defines FL01 as all rows and FL02 as BookedPassengers. Correct or discard before use.
2. Fix DS03 DAX to count disruption events, not dimension rows.
3. Verify PBIX internal model in Power BI Desktop; automated extraction of `DataModel` was not possible (XPress9-compressed). Confirm tables/measures/relationships manually.
4. PBIX report has only one blank page; report pages and disclosure are not actually present. Rebuild report pages in Power BI Desktop.
5. Do not import both CSV and Parquet into same model; choose one (CSV per data_sources.json).

## P1 — Relationship and semantic model corrections
6. Create the 19 approved relationships in `RELATIONSHIP_VALIDATION.csv` (17 active/inactive + 2 do-not-create fact-to-fact refs).
7. Configure role-playing date relationships: one active per table pair where required; inactive for arrival, event (if not primary), feedback, resolution.
8. Configure two dim_airport -> dim_route relationships with one inactive.
9. Add missing dimension columns to semantic model metadata (or hide technical columns) to match actual CSV schemas.
10. Decide handling of unused dimensions (dim_fare_class, dim_booking_channel, dim_currency): either add FKs/data or hide/remove from report scope. Do not invent FKs.
11. Validate dim_airline entirely null columns; do not fabricate enrichment values.

## P2 — DAX and Power Query corrections
12. Replace boolean SUM in FL04 with COUNTROWS FILTER.
13. Resolve percentage formatting convention (multiply by 100 vs percent format).
14. Rewrite Power Query M to define all 14 tables; fix dim_airline column count (12, not 14); add type conversions and error handling.
15. Correct semantic_model JSON files to reflect actual schemas and approved measures.
16. Keep FL02 labeled as passenger volume; no financial revenue measures.

## P3 — Report usability and formatting
17. Rebuild 5 report pages from custom report.json spec in Power BI Desktop.
18. Add disclosure textbox and OD-04 blocked page content.
19. Add measure formatting and display folders.
20. Hide technical keys where appropriate.

## P4 — Optional enhancements
21. Add DAX time-intelligence measures only after date relationships are validated.
22. Add field parameters / drill-through after core model is stable.
23. Consider separate date dimensions for each role if USERELATIONSHIP is insufficient.

## Governance constraints (must remain)
- OD-04 unresolved; FactBookingTransactions and FactOperatingCosts blocked.
- No exchange rates; no financial revenue/cost measures.
- G3 not approved; G4 blocked; schema freeze not authorized.
- Synthetic data disclosure required on all report pages.