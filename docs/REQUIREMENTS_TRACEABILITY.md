# Requirements Traceability Matrix

Status values: NOT STARTED, IN PROGRESS, BLOCKED, PASS, FAIL.

| ID | Requirement | Planned evidence | Status |
|---|---|---|---|
| REQ-001 | 10 real airline identities, with source verification required before reference approval, and synthetic operational and financial simulations | Airline identity reference and provenance register; reference manifest; T-72 to T-78 evidence; T-79 disclosure evidence; generator configuration and validation report | NOT STARTED |
| REQ-002 | Reporting window 2025-10-01 to 2026-09-30 | Date coverage validation | NOT STARTED |
| REQ-003 | Documented data grain and schema | Data dictionary and model specification | NOT STARTED |
| REQ-004 | Reproducible synthetic data with a stable `AirlineId` to `AirlineKey` mapping and one selected `ReferenceVersion` | Seeded rerun comparison; key-map hash; reference manifest; T-78 evidence | NOT STARTED |
| REQ-005 | Documented data-quality defects | Quality rules and test results | NOT STARTED |
| REQ-006 | Validated dimensional model with `AirlineKey` relationships, hidden `ReferenceVersion`, and no ambiguous airline filter path | Model diagram, relationship checks, and Power BI reference-version test | NOT STARTED |
| REQ-007 | Defined airline KPI calculations | KPI dictionary and independent reconciliation | NOT STARTED |
| REQ-008 | Five executive report pages | Power BI Desktop review evidence | NOT STARTED |
| REQ-009 | Drill-through and scenario interactions | Interaction test results | NOT STARTED |
| REQ-010 | Power BI Desktop runtime validation | Refresh and KPI validation evidence | NOT STARTED |
| REQ-011 | Reproducible portfolio release | Setup documentation and release checklist | NOT STARTED |
| REQ-012 | Aircraft availability reference schema, composite grain, controlled statuses, hours and version integrity | 03_DATA_CONTRACTS.md Section 3.4; T-56, T-57, T-58 and T-59 evidence | NOT STARTED |
| REQ-013 | K-13 aircraft utilization numerator, eligible available-hours denominator and selected reference version | 03_DATA_CONTRACTS.md Section 11.3; T-60 independent KPI validation evidence | NOT STARTED |
| REQ-014 | Aircraft availability reference-version reproducibility and historical correction controls | 03_DATA_CONTRACTS.md Section 3.4; T-59 version validation evidence | NOT STARTED |
| REQ-015 | Aircraft availability status and hours eligibility rules | 03_DATA_CONTRACTS.md Section 3.4; T-58 status validation evidence | NOT STARTED |
| REQ-016 | Aircraft utilization denominator reconciliation and zero-denominator behavior | 03_DATA_CONTRACTS.md Section 11.3; T-37 and T-60 validation evidence | NOT STARTED |
| REQ-017 | Controlled cost classification reference, active-version integrity, and exact cost category/subcategory matching | 03_DATA_CONTRACTS.md OD-13; T-66 and T-69 evidence | NOT STARTED |
| REQ-018 | Controlled disruption classification reference reconciled with DimDisruptionType attributes | 03_DATA_CONTRACTS.md OD-13; T-67 evidence | NOT STARTED |
| REQ-019 | Deterministic, unique source-to-standard classification mappings with no ambiguous accepted mappings | 03_DATA_CONTRACTS.md OD-13; T-68 evidence | NOT STARTED |
| REQ-020 | Invalid, inactive, unmapped, and ambiguous classifications quarantined with reason and lineage metadata | 03_DATA_CONTRACTS.md OD-13; T-70 evidence | NOT STARTED |
| REQ-021 | Consistent approved cost and disruption taxonomies across all ten synthetic airline simulations | 03_DATA_CONTRACTS.md OD-13; T-71 evidence | NOT STARTED |
| REQ-022 | Revenue component identities and classification integrity without a redundant separate revenue classification reference or FactRevenue table | 03_DATA_CONTRACTS.md OD-13 and OD-15; T-65 evidence | NOT STARTED |
| REQ-023 | Ten intended real airline identities reconciled to the fixed roster using `AirlineId` and supported by attribute-level source provenance; OD-01A remains pending formal approval | 03_DATA_CONTRACTS.md Sections 2.1 and 3.4; T-72 and T-75 evidence; OD-01A | NOT STARTED |
| REQ-024 | Durable `AirlineId` business identity and permanent `AirlineKey` warehouse surrogate, with separate unique IATA and ICAO attributes that are version-qualified and not used as keys | 03_DATA_CONTRACTS.md Sections 4.3, 6.2.2, and 7; T-73, T-74, and T-78 evidence | NOT STARTED |
| REQ-025 | Attribute-level airline identity provenance register with documented source hierarchy, verification status, evidence durability, and conflict resolution | 03_DATA_CONTRACTS.md Section 3.4; T-75 and T-76 evidence | NOT STARTED |
| REQ-026 | Nullable unsupported airline identity attributes and quarantined conflicting or unsupported values with no fabrication or inference; `BusinessModelClass` remains analytical and optional | 03_DATA_CONTRACTS.md Sections 2.1, 3.4, and 4.3; T-76 evidence | NOT STARTED |
| REQ-027 | Exact reconciliation between the approved airline identity reference and `DimAirline`, including `AirlineId`, `AirlineKey`, version-qualified attributes, and `ReferenceVersion` | 03_DATA_CONTRACTS.md Sections 3.4, 4.3, and 7; T-77 evidence | NOT STARTED |
| REQ-028 | Reference-version, manifest, refresh, and key integrity: one approved `ReferenceVersion` per generation/refresh, manifest authority, stable key mapping, and no mixed-version facts; approved through `G3-RV-01`, not OD-23 | 03_DATA_CONTRACTS.md Sections 3.4, 7.1, and 13; T-78 evidence; `G3-RV-01` | NOT STARTED |

**Status note:** Every requirement remains `NOT STARTED`. No reference CSV,
data dictionary, dataset, semantic model, DAX measure, Power BI report, or
validation test has been created or executed. OD-01A and OD-01B are
owner-confirmed designs with formal signature and approval pending.
