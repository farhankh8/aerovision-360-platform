# Governance Compliance Audit — AEROVISION 360

## Synthetic data disclosure
- Required disclosure present in `deliverables/power_bi/data_sources/data_sources.json`, `semantic_model/semantic_model.json`, and `report/report.json`: "Synthetic Simulation — Not Actual Airline Performance".
- Report page "Revenue & Yield Intelligence - OD-04 BLOCKED" contains disclosure textbox. Good.
- Status: PASS (disclosure present in custom specs; must be verified in PBIX report, which currently has only one blank page).

## OD-04 exchange-rate policy
- Status: UNRESOLVED (must remain unresolved).
- `FactBookingTransactions` and `FactOperatingCosts` are blocked.
- No exchange rates invented.
- No financial revenue or operating cost measures defined in DAX.
- FL02 is passenger volume only.
- Report page for Revenue & Yield correctly blocked.
- Status: PASS (no violations found in provided files).

## Blocked measures
- UNDEF-01 Total Revenue — blocked.
- UNDEF-02 Total Operating Costs — blocked.
- UNDEF-03 On-Time Performance Threshold — owner approval pending (OD-09).
- UNDEF-04 Satisfaction Score Scale Definition — owner approval pending (OD-11).
- UNDEF-05 Coupon Allocation Metric — owner approval pending (OD-14).
- UNDEF-06 Service Recovery Metric — owner approval pending (OD-17).
- No blocked measure implemented in provided DAX. PASS.

## Airline reference governance
- OD-01A / OD-01B pending formal approval.
- G3 not approved; G4 blocked.
- Schema freeze not authorized.
- dim_airline has 3 entirely null columns (AirlineGroup, BusinessModelClass, StatusEffectiveDate) and ReferenceVersion populated with draft value.
- Status: INCOMPLETE but not violated by audit (no unauthorized changes made).

## Findings
### GOV-01 (P0) — PBIX report has only one blank page
- File: `deliverables/power_bi/AEROVISION_360.pbix` (extracted report definition)
- Evidence: pages.json contains one page "Page 1" with no visuals; custom `report/report.json` pages are not loaded.
- Impact: disclosure and blocked-status pages are not actually in PBIX. Must be rebuilt in Power BI Desktop.

### GOV-02 (P1) — Custom JSON files are not automatically loaded into PBIX
- `report/report.json`, `semantic_model/model.json`, `semantic_model/semantic_model.json`, `theme/theme.json`, `data_sources/data_sources.json` are specifications.
- They are not Power BI definitions by themselves. Do not assume they are in PBIX.

### GOV-03 (P2) — dim_airline has entirely null enrichment columns
- File: `deliverables/data/dim_airline.csv`
- Columns: AirlineGroup, BusinessModelClass, StatusEffectiveDate all null for 10 rows.
- This is a data completeness gap, not a governance violation. Do not fabricate values.

## Violation count
- Governance violations found: 0 (in provided files). PBIX-level disclosure not verifiable due to blank report, counted as GOV-01.