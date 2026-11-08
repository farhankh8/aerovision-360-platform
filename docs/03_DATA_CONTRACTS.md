# AEROVISION 360 - Data Contracts

**Global Multi-Airline Operations, Revenue & Customer Intelligence Platform**

| Document control | Value |
|---|---|
| Document | 03_DATA_CONTRACTS.md |
| Version | 1.5 |
| Status | DRAFT - CONTROLLED OD-01 REMEDIATION COMPLETE; PENDING REVIEW AND FORMAL APPROVAL |
| Last updated | 2026-11-01 |
| Reporting period | 2025-10-01 through 2026-09-30, inclusive |
| Reporting currency | USD |
| Airline population | Exactly 10 real airline identities (fixed roster; source verification required before reference approval; see Section 2.1) |
| Platform | Microsoft Power BI |
| Data source | Real airline identity attributes, to be source-verified before reference approval; synthetic operational and financial data |

> This document is a design contract. It does not authorize data generation, semantic-model implementation, DAX development, report construction, or a release-readiness claim. Those activities begin only after the approval conditions in Section 15 are met.

## 1. Purpose

This document defines the data architecture and data contracts for AEROVISION 360. It is the controlling reference for how real airline identities, subject to source verification before reference approval, and synthetic operational and financial data are structured, keyed, related, measured, validated, and accepted.

It establishes:

- The RAW, STAGING, CURATED, and REFERENCE layers and the responsibility boundary of each layer.
- The dimension and fact tables, their business purpose, and one authoritative grain per table.
- The durable `AirlineId` identity, permanent `AirlineKey` warehouse mapping, version-qualified airline attributes, and immutable reference-version snapshots.
- Primary keys, business keys, foreign keys, and referential-integrity rules.
- Required columns, data types, formats, nullability, and business definitions.
- Relationship cardinality, filter direction, role-playing dimensions, and semantic-model constraints.
- Date, timestamp, time-zone, fiscal-calendar, and reporting-period rules.
- Currency conversion and financial-recognition rules.
- KPI definitions, formulas, numerators, denominators, exclusions, and zero-denominator behavior.
- Controlled data-quality defects and their required treatment.
- Validation and reconciliation tests, including evidence requirements.
- Decisions that require explicit approval before data generation.
- Acceptance criteria and the document's current status.

**Normative language.** "Must" and "shall" identify mandatory requirements. "Should" identifies a recommended design that may be changed only with documented rationale. "May" identifies an optional capability. "OPEN DECISION" identifies a business or design choice that is not approved and must not be treated as settled.

**Scope boundary.** This document covers data design only. It does not create datasets, generators, Power BI models, DAX measures, dashboards, or additional documentation files.

**Related documents:**

- `README.md` - project status and validation policy.
- `docs/01_PROJECT_SCOPE.md` - approved project scope and fixed boundaries.
- `docs/02_BUSINESS_REQUIREMENTS.md` - business requirements BR-01 through BR-15.
- `docs/REQUIREMENTS_TRACEABILITY.md` - requirement-to-evidence tracking.
- `docs/PROGRESS_LEDGER.md` - phase and gate status.
- `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt` - master build requirements.
- `docs/OD01A_AIRLINE_POPULATION_DECISION.md` - OD-01A population decision (owner-confirmed design; formal signature and approval pending).
- `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` - OD-01B identity and reference-version decision (owner-confirmed design; formal signature and approval pending).
- `docs/OD01_REMEDIATION_CHANGE_RECORD.md` - controlled change record for contract version 1.5.

## 2. Fixed Project Constraints

The following constraints are fixed for the baseline. A material change requires documented change control, an impact assessment, and approval. It must not be introduced silently.

| ID | Constraint | Baseline value |
|---|---|---|
| C-01 | Project | AEROVISION 360 - Global Multi-Airline Operations, Revenue & Customer Intelligence Platform |
| C-02 | Airline population | Exactly 10 real airline identities (fixed roster in Section 2.1); source verification required before reference approval |
| C-03 | Reporting start | 2025-10-01 |
| C-04 | Reporting end | 2026-09-30, inclusive |
| C-05 | Reporting duration | 12 complete calendar months, 365 days |
| C-06 | Flight volume target | 150,000 to 250,000 flight legs, subject to validation |
| C-07 | Reporting currency | USD |
| C-08 | Source data | Real airline identity attributes, to be source-verified before reference approval; all operational, customer, and financial data synthetic; no real passenger personal information |
| C-09 | Analytics platform | Microsoft Power BI Desktop |
| C-10 | Engineering tools | Python, Power Query M, DAX, Git, CSV/Parquet/Excel where justified |
| C-11 | Flight-leg grain | One row per scheduled flight leg, including cancelled flights |
| C-12 | Fiscal calendar | Fiscal year starts 01 October; FY2026 is 2025-10-01 through 2026-09-30 |
| C-13 | Data layers | RAW, STAGING, CURATED, REFERENCE |
| C-14 | Reporting pages | Exactly five primary pages, listed below |

**Flight-volume rule.** The 150,000 to 250,000 range is a planning target, not a guaranteed output. The final volume must be validated against grain, model size, refresh performance, and storage. A volume outside the target requires documented approval and an explanation; it must not be hidden.

**Identity and synthetic-data rule.** The ten airline identities are real. Before a reference version is approved, `AirlineName` (commercial brand), IATA code, ICAO code, `HomeCountry`, `HomeCountryCode`, and any populated optional identity attribute must be source-verified and recorded at attribute level. `LegalName` is optional and remains in the reference/provenance layer only; it is not a `DimAirline` column. `AirlineGroup` is the optional ultimate parent company or group brand. `BusinessModelClass` is an optional analytical classification, not a source-verified identity attribute. `OperatingRegion` is not an airline identity attribute; analytical region is derived from route/airport geography. Airports, routes, aircraft, fleet assignments, customers, bookings, revenue, costs, operations, disruptions, feedback, and financial results are synthetic. No output may be presented as the actual performance of any named airline. Every dashboard page, tooltip while a page is visible, and exported report result must carry the exact unconditional disclosure: "Synthetic Simulation — Not Actual Airline Performance". Real passenger personal information must not be used.

### 2.1 Airline identity roster (intended population; formal approval pending)

The project population is fixed to these ten real airline identities. The roster is the owner-confirmed intended population; the formal OD-01A population approval and OD-01B identity/reference approval remain PENDING SIGNATURE.

| Airline | IATA | ICAO | Home country | Country code |
|---|---|---|---|---|
| Emirates | EK | UAE | United Arab Emirates | AE |
| Qatar Airways | QR | QTR | Qatar | QA |
| Singapore Airlines | SQ | SIA | Singapore | SG |
| Air India | AI | AIC | India | IN |
| IndiGo | 6E | IGO | India | IN |
| British Airways | BA | BAW | United Kingdom | GB |
| Lufthansa | LH | DLH | Germany | DE |
| Delta Air Lines | DL | DAL | United States | US |
| Southwest Airlines | WN | SWA | United States | US |
| Qantas | QF | QFA | Australia | AU |

**Roster rule.** The roster is fixed for the baseline. Identity attributes must be verified against the source hierarchy in Section 3.4 and recorded at attribute level in `ref_airline_sources.csv`. `AirlineGroup` is optional and may be populated only from a `VERIFIED` source for the ultimate parent company or group brand; otherwise it is null. `LegalName` is optional and reference-only. `BusinessModelClass` is analytical and has no identity provenance. `OperatingRegion` is not an identity attribute. Group ownership must not be inferred from the airline's home country, brand similarity, or ownership assumptions. The roster does not authorize data generation, schema freeze, reference-data creation, or a G3 PASS.

**Five primary report pages:**

1. Executive Overview
2. Network & Capacity Intelligence
3. Revenue & Yield Intelligence
4. Operations & Disruption
5. Customer & Service Intelligence

**Page-name rule.** These names are fixed for navigation and traceability. Supporting pages, tooltips, and drill-through views may be added later only if they do not displace or rename the five primary pages.

## 3. Data Architecture

AEROVISION 360 uses a layered batch architecture. Each layer has one responsibility. Data moves in one direction: RAW to STAGING to CURATED, with REFERENCE data available to STAGING and CURATED. Power BI consumes CURATED data and approved reference data only; it does not read RAW or STAGING.

| Layer | Folder | Primary purpose | Write policy | Consumer |
|---|---|---|---|---|
| RAW | `data/01_raw/` | Preserve generated source records and seeded defects | Immutable after generation | STAGING and audit |
| STAGING | `data/02_staging/` | Standardize, type, deduplicate, flag, and validate | Rebuildable from RAW | CURATED |
| CURATED | `data/03_curated/` | Publish clean star-schema tables and USD measures | Rebuildable from STAGING | Power BI |
| REFERENCE | `data/04_reference/` | Hold controlled code lists, calendars, rates, and assumptions | Version-controlled | STAGING, CURATED, Power BI |

**Cross-layer rules:**

- RAW is never overwritten, cleaned in place, or silently corrected.
- Every CURATED row must trace to a RAW record, a controlled reference value, or a documented allocation.
- Transformations must be deterministic for the same seed, configuration, source files, and code version.
- Row counts must reconcile between layers. Accepted, rejected, quarantined, corrected, and duplicate records must be counted separately.
- Invalid records must not disappear. They must be rejected with a reason code or quarantined with a disposition.
- No layer may aggregate financial data in a way that duplicates revenue or cost across tables.
- No layer may aggregate different currencies without conversion to USD.
- All dates and timestamps must follow Section 9. All financial values must follow Section 10.

### 3.1 RAW Layer

**Purpose:** preserve the generated source records exactly as produced, including deliberate defects, so that cleaning and validation are reproducible and auditable.

**Folder:** `data/01_raw/`

**Required properties:**

- One file per source entity, for example `raw_flight_operations.csv`, `raw_booking_transactions.csv`, and `raw_customer_feedback.csv`.
- UTF-8 encoding without a byte-order mark.
- Comma-separated values with a header row, or Parquet with a documented schema. One format per dataset version.
- Original source identifiers, source filenames, generation timestamp, seed, configuration version, and schema version recorded in `data/manifests/`.
- Deliberately seeded defects preserved exactly as generated.
- No deduplication, type correction, currency conversion, imputation, or business-rule correction in RAW.
- No deletion of records because they fail a quality rule.

**RAW manifest fields:** `dataset_name`, `schema_version`, `source_filename`, `row_count`, `generated_at_utc`, `generator_version`, `seed`, `configuration_hash`, `sha256`, `defect_injection_summary`.

**RAW acceptance rule:** a RAW file is valid when it is readable, matches its manifest hash, preserves the declared schema, and contains the documented defect population. RAW validity does not mean business validity.

### 3.2 STAGING Layer

**Purpose:** standardize source records, assign types, detect defects, resolve or quarantine invalid records, and prepare conformed data for CURATED.

**Folder:** `data/02_staging/`

**Required responsibilities:**

- Standardize column names to the contract names in Section 6.
- Assign declared data types and reject values that cannot be converted safely.
- Normalize text casing, whitespace, codes, and currency codes.
- Normalize timestamps to UTC and derive local date keys under Section 9.
- Detect exact and business-key duplicates.
- Validate required fields, allowed values, ranges, and cross-field rules.
- Validate foreign keys against dimension and reference data.
- Convert financial amounts to USD using the approved rate policy.
- Preserve defect flags, rejection reasons, and source lineage.
- Produce a disposition record for every rejected or corrected row.

**Staging rules:**

- Staging must not contain business aggregations or KPI calculations.
- Staging must not silently choose one duplicate over another. The chosen record and the rejection reason must be logged.
- Staging must not map an invalid required foreign key to a valid dimension member unless an approved unknown-member rule exists.
- Staging must not delete source rows; it must write accepted rows to staging and rejected rows to a quarantine dataset with the original values and reason code.
- Staging must be rebuildable from RAW and REFERENCE without manual edits.

**Required staging metadata columns:** `SourceFile`, `SourceRowNumber`, `IngestedAtUTC`, `SchemaVersion`, `QualityStatus`, `QualityRuleID`, `Disposition`, `DispositionReason`.

### 3.3 CURATED Layer

**Purpose:** provide clean, business-ready dimension and fact tables for the Power BI semantic model, with resolved keys, consistent types, USD financial measures, and no uncontrolled defects.

**Folder:** `data/03_curated/`

**Required responsibilities:**

- Publish the conformed dimensions and facts defined in Sections 4 through 6.
- Enforce unique primary keys and unique business keys.
- Resolve every required foreign key to exactly one dimension row.
- Apply approved business rules, allocations, and financial definitions.
- Store monetary measures in original currency and USD where both are required.
- Preserve additive measures at the declared fact grain.
- Exclude quarantined records and disclose their counts.
- Provide a curated manifest with row counts, key counts, file hashes, and reconciliation totals.

**Curated rules:**

- No duplicate fact rows at the declared grain.
- No orphan required foreign keys.
- No uncontrolled nulls in required columns.
- No unresolved currency codes.
- No aggregate row mixed with detail rows in the same fact table.
- No fact-to-fact relationship, bridge table, or duplicated financial fact without explicit approval.
- No hidden correction: every correction must map to a staging disposition.

**Power BI boundary:** Power BI imports CURATED tables and approved REFERENCE tables only. It must not import RAW or STAGING files.

### 3.4 REFERENCE Layer

**Purpose:** hold controlled values that must be consistent across layers, including code lists, calendars, exchange rates, time-zone mappings, and utilization assumptions.

**Folder:** `data/04_reference/`

**Required reference datasets:**

| Reference dataset | Grain | Purpose |
|---|---|---|
| `ref_airlines.csv` | One row per approved airline per reference version | Controlled ten-airline identity roster and supported attributes |
| `ref_airline_sources.csv` | One row per airline attribute source record per reference version | Attribute-level provenance, source hierarchy, and verification status for airline identity values |
| `ref_airports.csv` | One row per airport | Airport codes, geography, and IANA time zones |
| `ref_aircraft_types.csv` | One row per aircraft type | Manufacturer, model, capacity, and range |
| `ref_fare_classes.csv` | One row per fare class | Cabin and refundability mapping |
| `ref_booking_channels.csv` | One row per channel | Channel taxonomy |
| `ref_disruption_types.csv` | One row per disruption type | Cause taxonomy and reactionary eligibility |
| `ref_cost_classification.csv` | One row per cost classification per reference version | Controlled cost category and subcategory taxonomy |
| `ref_currencies.csv` | One row per currency | ISO 4217 codes and display metadata |
| `ref_exchange_rates.csv` | One row per currency per rate date | Synthetic USD conversion rates |
| `ref_aircraft_availability.csv` | One row per aircraft per calendar date per reference version | Daily planned available hours and availability status |
| `ref_calendar.csv` | One row per calendar date | Controlled calendar used to build DimDate |

**Reference rules:**

- `ref_aircraft_availability.csv` contains `AircraftKey`, `CalendarDateKey`, `AvailableHours`, `AvailabilityStatus`, and `ReferenceVersion`.
- Reference values must be version-controlled and must not be edited ad hoc in Power BI. Only versions with the required owner approvals may be treated as approved business reference data; unapproved proposals remain provisional.
- Effective dating must be represented explicitly where a reference dataset requires it. For `ref_aircraft_availability.csv`, `CalendarDateKey` is the effective business date at daily grain. Separate `ValidFrom`, `ValidTo`, and row-level `IsActive` fields are not used; version selection is controlled by `ReferenceVersion` and the generation manifest.
- Exchange rates are synthetic and must be identified as synthetic. They must not be represented as market data.
- Reference changes that affect historical results require a new version and a reconciliation note.
- The generator must record the reference version in every manifest.

**Airline-identity reference schema and rules (owner-confirmed design; OD-01B formal signature and approval pending):**

- **Datasets:** `ref_airlines.csv` and `ref_airline_sources.csv`. The reference manifest is the authoritative approval record. `DimAirline.ReferenceVersion` is a technical lineage field only.
- **`ref_airlines.csv` grain and primary key:** one row per `AirlineId` per `ReferenceVersion`; primary key `AirlineId` + `ReferenceVersion`. `AirlineId` is the durable business identity and is never reused. IATA and ICAO are mutable, version-qualified attributes, not keys.
- **`ref_airlines.csv` required fields:** `AirlineId` (`String(20)`), `AirlineIATACode` (`String(2)`), `AirlineICAOCode` (`String(3)`), `AirlineName` (`String(100)`), `HomeCountry` (`String(100)`), `HomeCountryCode` (`String(2)`), `IsActive` (`Boolean`), and `ReferenceVersion` (`String(30)`).
- **`ref_airlines.csv` optional fields:** `LegalName` (`String(200)`), `AirlineGroup` (`String(100)`), and `StatusEffectiveDate` (`Date`). `StatusEffectiveDate` is required when `IsActive = FALSE` and null for the baseline active state. `LegalName` and `AirlineGroup` remain null when no `VERIFIED` source exists.
- **Excluded from `ref_airlines.csv`:** `OperatingRegion`, `BusinessModelClass`, `LifecycleStatus`, and `MergedIntoAirlineId`. `OperatingRegion` is not an airline identity attribute. `BusinessModelClass` is an optional analytical attribute in `DimAirline`, not a source-verified identity field.
- **`ref_airline_sources.csv` grain:** one row per source-attribute assertion per `ReferenceVersion`. A source document supporting four attributes produces four rows sharing an optional `SourceDocumentID`, each with its own globally unique `SourceRecordID`. The primary key is `SourceRecordID`.
- **`ref_airline_sources.csv` required fields:** `SourceRecordID` (`String(30)`, format `SRC-000001`), `AirlineId` (`String(20)`), `AttributeName` (`String(30)`), `AttributeValue` (`String(200)`), `SourceOrganization` (`String(150)`), `SourceURL` (`String(500)`), `SourceType` (`String(30)`), `SourceRetrievedDate` (`Date`), `SourceVerifiedDate` (`Date`), `VerificationStatus` (`String(20)`), `VerificationMethod` (`String(50)`), `IsAuthoritative` (`Boolean`), `ReferenceVersion` (`String(30)`), `CreatedBy` (`String(100)`), and `CreatedDate` (`Date`).
- **`ref_airline_sources.csv` optional fields:** `SourceDocumentID` (`String(30)`), `AirlineIATACodeAtVerification` (`String(2)`), `SourceAttributeValue` (`String(200)`), `SourceTitle` (`String(200)`), `SourcePublishedDate` (`Date`), `EvidenceHash` (`String(64)`), `SourceArchiveRef` (`String(200)`), `SupersedesSourceRecordID` (`String(30)`), `SupersededBySourceRecordID` (`String(30)`), `QuarantineReason` (`String(50)`), `Notes` (`String(500)`), `ReviewedBy` (`String(100)`), and `ReviewedDate` (`Date`).
- **Attribute-level lineage:** every populated identity attribute in `ref_airlines.csv` must resolve to exactly one authoritative `VERIFIED` source record for the same `AirlineId`, `AttributeName`, and `AttributeValue` in the selected reference version. Provenance joins on `AirlineId`, never on IATA or ICAO. A source record that supports no loaded value must be `QUARANTINED` or `SUPERSEDED` with a reason.
- **Controlled `AttributeName` values:** `AirlineName`, `LegalName`, `AirlineIATACode`, `AirlineICAOCode`, `HomeCountry`, `HomeCountryCode`, `AirlineGroup`, and `IsActive` (only when a status change is recorded). `OperatingRegion` and `BusinessModelClass` are excluded because they are not source-verified identity attributes.
- **Source hierarchy:** `AirlineName`, `LegalName`, and `AirlineGroup` prefer the parent group or airline official corporate source, then a government/civil-aviation registry, then an official ICAO/IATA directory, then a reputable documented industry source. IATA and ICAO prefer the applicable official code registry/directory, then the airline official source, then a government registry, then another documented source. `HomeCountry` and `HomeCountryCode` prefer the government/civil-aviation registry, then the airline official source, then an official ICAO/IATA directory, then another documented source. The hierarchy is a preference order, not permission to invent a source.
- **Source types:** `OfficialAirline`, `GovernmentRegistry`, `IndustryAuthority`, `OtherDocumented`.
- **Verification status:** `VERIFIED`, `CONFLICTING`, `UNVERIFIED`, `SUPERSEDED`, `QUARANTINED`. A stale record is `QUARANTINED` with `QuarantineReason = STALE`; do not add a sixth status. Only one authoritative `VERIFIED` record may support a populated attribute in an approved version. `CONFLICTING` and `QUARANTINED` records must not be loaded into `ref_airlines.csv`.
- **Verification methods:** `ManualSourceReview`, `RegistryLookup`, `OfficialDirectory`, `DocumentReview`.
- **Quarantine reasons:** `CONFLICT`, `UNVERIFIED`, `STALE`, `MALFORMED`, `DUPLICATE`, `UNSUPPORTED`, `URL_INVALID`, `EVIDENCE_MISSING`, `OTHER`.
- **Source date format:** `SourceRetrievedDate` and `SourceVerifiedDate` are ISO 8601 calendar dates (`YYYY-MM-DD`). `SourceVerifiedDate` records the date the value was actually checked, must be on or after retrieval, and must not be in the future.
- **Evidence durability:** every `VERIFIED` record must have either a SHA-256 `EvidenceHash` of the captured content or a `SourceArchiveRef` to a read-only archived copy. If both exist, they must agree. A URL without a capture is not durable evidence. HTTPS only; no credentials, tokens, session identifiers, personal data, tracking parameters, shorteners, raw IP addresses, localhost, or link-only redirects.
- **Staleness:** the proposed maximum age is 365 days for names, legal names and group, and 180 days for IATA and ICAO codes, measured from `SourceVerifiedDate` to the reference-version approval date (or the current date if earlier). A stale record is `QUARANTINED` with `STALE` and cannot support a new approved version until re-verified. These thresholds are proposed policy, not owner-approved values.
- **Conflict resolution:** if two same-tier sources disagree, mark both `CONFLICTING`; no authoritative record; a required attribute blocks approval and an optional attribute remains null. A higher-tier source may resolve a lower-tier conflict, but the lower-tier record remains recorded as `UNVERIFIED` or `CONFLICTING`; it is never deleted. A conflict must not be resolved by memory, inference, brand similarity or home-country assumption.
- **Missing attributes:** required identity fields must never be blank. If a required value cannot be verified, the airline record is incomplete and must not be treated as approved reference data. Optional fields remain null; no placeholder, inferred value, or fabricated source may be inserted.
- **Version control and reproducibility:** `ReferenceVersion` format is `AIR-YYYY-MM-DD-NNN`, regex `^AIR-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$`. Published versions are immutable. A correction requires a new version, a reconciliation note, and a new source record where the evidence changed. The selected version must be recorded in every generation manifest and semantic-model refresh configuration.
- **Reference manifest:** the authoritative version register is `data/manifests/reference_versions.csv` (design only; not created by this document). It records `ReferenceVersion`, `EffectiveFrom`, `EffectiveTo`, `IsCurrent`, `Status`, `ApprovedBy`, `ApprovalDate`, `ManifestHash`, `SupersedesReferenceVersion`, and `ReconciliationNote`. Exactly one version may be `IsCurrent = TRUE` for a generation or refresh. `ApprovedBy` and `ApprovalDate` remain blank until a real approval occurs.
- **Reference-version approval:** use gate artifact `G3-RV-01`, not an OD-series decision. It records the owner, criteria, exact version, file hashes, source evidence, T-75/T-76 results, T-78 plan/results and refresh configuration. No reference version is approved by this document.
- **Airline key mapping:** `AirlineId` is the durable business identity. `AirlineKey` is a permanent positive `Int32` warehouse surrogate assigned once per airline. The mapping is loaded from a controlled, immutable key map stored with or hashed into the approved reference manifest; it is never derived from CSV row order, sort order, `row_number`, hash order, random selection, database `IDENTITY`, auto-increment, or a newly generated sequence during a clean rebuild. A retired airline retains both identifiers. Facts are never re-keyed. No separate enterprise airline registry table is introduced.
- **Historical semantics:** `DimAirline` is Type 1. Immutable reference snapshots preserve build reproducibility, but Type 1 does not preserve as-was historical identity labels. Type 2 is deferred and becomes necessary only if future requirements demand as-was identity reporting.
- **No fabrication:** source URLs, source organizations, verification dates, and verification statuses must be real and recorded only after verification. A blank or unavailable source is not evidence. This section does not create the reference CSV files and does not constitute formal OD-01B approval.

**Cost-classification reference schema and rules (proposed engineering baseline; owner approval required):**

- **Dataset:** `ref_cost_classification.csv`.
- **Grain:** one row per controlled cost classification per `ReferenceVersion`.
- **Required fields:** `CostClassificationCode` (`String(30)`), `CostCategory` (`String(30)`), `CostSubcategory` (`String(50)`), `Description` (`String(200)`), `IsActive` (`Boolean`), and `ReferenceVersion` (`String(30)`).
- **Business key:** `CostClassificationCode` + `ReferenceVersion`. The code must identify one category/subcategory pair within a version. Duplicate codes, duplicate category/subcategory pairs, and conflicting mappings within the selected version are invalid.
- Every `FactOperatingCosts` row must match exactly one active classification in the selected reference version using its existing `CostCategory` and `CostSubcategory` values. Zero matches or multiple matches must be quarantined; no silent fallback to `Other` is permitted.
- The reference validates the existing fact columns. It does not add a `CostClassificationKey`, a new fact table, or a `DimCostCategory` dimension.
- Proposed category values are Fuel, Crew, Maintenance, Airport Charges, Navigation, Sales and Distribution, Overhead, and Other. These remain subject to OD-13 approval.
- Proposed subcategories are provisional: Fuel—Jet Fuel, Fuel Surcharge, Fuel Adjustment; Crew—Flight Crew, Cabin Crew, Crew Accommodation, Crew Transport, Crew Training; Maintenance—Line Maintenance, Base Maintenance, Aircraft Parts, Component Overhaul; Airport Charges—Landing Charges, Parking Charges, Passenger Handling, Ground Handling; Navigation—En-route Charges, Terminal Navigation Charges; Sales and Distribution—Agency Commission, GDS Fees, Payment Processing, Distribution Fees; Overhead—Administration, IT, Facilities, Insurance, Professional Services; Other—Operational Supplies, Other Direct Operating Expenses.
- Inactive classifications must not be used for new generated cost rows. Historical versions must remain reproducible and must not be overwritten.
- These categories and subcategories are engineering proposals, not formal owner approval of OD-13 or any financial tolerance.

**Disruption-type reference schema and rules (proposed engineering baseline; owner approval required):**

- `ref_disruption_types.csv` is version-controlled at one row per `DisruptionCode` per `ReferenceVersion`.
- Required fields are `DisruptionCode` (`String(10)`), `DisruptionName` (`String(50)`), `DisruptionCategory` (`String(50)`), `ControllableFlag` (`Boolean`), `ReactionaryEligibleFlag` (`Boolean`), `IsActive` (`Boolean`), and `ReferenceVersion` (`String(30)`).
- `DisruptionCode` must be unique within a reference version. Each code maps to exactly one name, category, controllability flag, and reactionary-eligibility flag within that version.
- The curated `DimDisruptionType` must reconcile to the selected reference version. Its surrogate `DisruptionTypeKey` remains a curated-model key and is not stored in the reference file.
- The proposed category set remains Weather, Air Traffic Control, Technical, Crew, Airport, Security, Passenger, Reactionary, and Other. Exact event codes and names require OD-13 approval.
- Every disruption fact row must resolve to exactly one active type in the selected version. Unmapped, inactive, duplicate, or ambiguous mappings must be quarantined with a reason; they must not be silently mapped to `Other` or `Unattributed`.
- `Unattributed` remains an explicit event type for delay whose cause cannot be attributed. It is not a fallback for invalid source mappings.
- Reference changes require a new version and a reconciliation note. The selected version must be recorded in the generation manifest.
- These rules are proposals and do not formally approve OD-13.

**Aircraft-availability reference schema and rules (proposed engineering baseline; owner approval required):**

- **Grain:** one row per `AircraftKey`, `CalendarDateKey`, and `ReferenceVersion`.
- **Composite business key:** `AircraftKey` + `CalendarDateKey` + `ReferenceVersion`. Duplicate combinations are invalid. Within one selected reference version, there must be no more than one row per aircraft per calendar date.
- **`AircraftKey`:** required `Int32` reference to `DimAircraft.AircraftKey`.
- **`CalendarDateKey`:** required `Int32` date key in `YYYYMMDD` format, referencing `DimDate.DateKey`. It represents the effective business date for that daily availability record.
- **`AvailableHours`:** required `Decimal(4,2)` value from 0.00 through 24.00 inclusive.
- **`AvailabilityStatus`:** required controlled value, one of `Available`, `Maintenance`, `Stored`, `Retired`, or `No Planned Availability`. These daily statuses describe the aircraft's availability for the calendar date and are distinct from `DimAircraft.FleetStatus`.
- **`ReferenceVersion`:** required `String(30)` identifier for the exact reference dataset version. It is a dataset-version identifier, not an effective date or an approval status.
- **Status and hours validation:** `Available` requires `AvailableHours` greater than 0.00 and no greater than 24.00. `Maintenance`, `Stored`, `Retired`, and `No Planned Availability` require `AvailableHours` equal to 0.00 for the full calendar date. Partial-day planned availability is represented by `Available` with the applicable positive hours.
- Invalid status/hour combinations, duplicate keys, and invalid dimension references must be rejected or quarantined with a recorded reason. They must not be silently corrected.
- Each generated dataset manifest must identify its exact `ReferenceVersion`. A semantic-model refresh must use exactly one explicitly selected reference version; multiple versions must not be aggregated together.
- Historical corrections require a new reference version and a reconciliation note. Previously published versions must remain reproducible.
- The proposed controlled status set and validation rules are engineering proposals pending the applicable owner approval. They do not constitute formal approval of OD-10 or any other open decision.
- The proposed 14.00 available-hours-per-active-aircraft-day baseline remains governed exclusively by OD-10, which is `PROPOSED - OWNER APPROVAL REQUIRED`. It must not be treated as an approved business assumption until formally approved.
- This reference is used for K-13 aircraft utilization only. It must relate to `DimAircraft` and `DimDate` and must not create a relationship or join that multiplies `FactFlightOperations` rows.

**Reference-versus-dimension rule:** a reference dataset is the controlled source; a dimension is the curated, query-ready representation. For example, `ref_airlines.csv` is the source, and `DimAirline` is the curated dimension. They must reconcile exactly.

## 4. Dimension Table Catalogue and Grain

Dimensions provide the conformed business context for filtering, grouping, and labeling facts. Every dimension has one row per business member, one surrogate primary key, and one or more unique business keys. Detailed column definitions and data types are in Section 6.2.

### 4.1 Dimension Summary

| Dimension | Business purpose | Grain | Primary key | Foreign keys | Key business rule |
|---|---|---|---|---|---|
| DimDate | Shared calendar for all date roles | One row per calendar date | DateKey | None | Covers 2024-10-01 through 2026-10-31; reporting-period flag is explicit |
| DimAirline | Airline master for comparison and filtering | One row per airline (Type 1) | AirlineKey | None | Exactly 10 active airlines; unique `AirlineId`; version-qualified IATA/ICAO/name; permanent `AirlineKey` mapping |
| DimAirport | Airport master for network and geography | One row per airport | AirportKey | None | Unique airport code and valid IANA time zone |
| DimRoute | Directional origin-destination route | One row per directional origin-destination pair | RouteKey | OriginAirportKey, DestinationAirportKey | Origin and destination differ; distance is positive |
| DimAircraft | Aircraft fleet master | One row per aircraft | AircraftKey | AirlineKey, AircraftTypeKey | Unique registration; one operator at a time |
| DimAircraftType | Aircraft type and capacity reference | One row per aircraft type | AircraftTypeKey | None | Unique manufacturer-model combination |
| DimCustomer | Synthetic customer master | One row per fictional customer | CustomerKey | None | Unique customer ID; no real personal data |
| DimFareClass | Fare and cabin taxonomy | One row per fare class | FareClassKey | None | Unique fare-class code; one cabin per fare class |
| DimBookingChannel | Booking distribution taxonomy | One row per booking channel | BookingChannelKey | None | Unique channel code; direct flag is consistent |
| DimDisruptionType | Disruption cause taxonomy | One row per disruption type | DisruptionTypeKey | None | Unique disruption code; reactionary eligibility explicit |
| DimCurrency | Currency display and validation | One row per currency | CurrencyKey | None | ISO 4217 code; exactly one USD reporting-currency row |

**Dimension count rule:** DimDate is a role-playing calendar dimension. DimAirport is used in two roles through DimRoute: origin and destination. These roles must be modeled explicitly under Section 8; they must not create ambiguous filter paths.

### 4.2 DimDate

- **Business purpose:** provide a complete, consistent calendar for flight departure, flight arrival, booking, travel, cost, feedback, fiscal-period, and trend analysis.
- **Grain:** one row per calendar date.
- **Primary key:** DateKey, an intelligent integer in `YYYYMMDD` format.
- **Foreign keys:** none.
- **Required columns:** see Table 6.2.1. The complete date range is 2024-10-01 through 2026-10-31 inclusive.
- **Business rules:**
  - `FullDate` is unique and is the model date column.
  - `IsReportingPeriod = TRUE` only for 2025-10-01 through 2026-09-30.
  - Dates outside the reporting period exist only to support booking lead time, prior-period comparison, and overnight arrival analysis.
  - `FiscalYear` starts on 01 October. FY2026 covers 2025-10-01 through 2026-09-30.
  - `WeekNumber` follows ISO 8601. `WeekStartDate` is the ISO week start.
  - No missing dates, duplicate dates, or locale-specific date strings are allowed.

### 4.3 DimAirline

- **Business purpose:** identify and compare the ten real airline identities and their documented identity attributes and synthetic operating profiles.
- **Grain:** one row per airline (Type 1 baseline).
- **Primary key:** `AirlineKey` (permanent warehouse surrogate).
- **Foreign keys:** none.
- **Required columns:** see Table 6.2.2.
- **Business rules:**
  - Exactly 10 rows with `IsActive = TRUE` for the baseline period.
  - `AirlineId` is the durable business identity, unique and never reused. `AirlineKey` is the permanent positive `Int32` warehouse surrogate, unique and never reused. The same `AirlineId` must always resolve to the same `AirlineKey`.
  - `AirlineIATACode`, `AirlineICAOCode`, and `AirlineName` are unique within a `ReferenceVersion`; they are mutable attributes, not primary or foreign keys. There is no standalone airline-code column.
  - `AirlineName` is the commercial brand name used by the project. `LegalName` is optional, reference/provenance-only, and is not a `DimAirline` column.
  - `HomeCountry` is the country of the airline's principal headquarters or domicile, not incorporation country, AOC state, or ultimate ownership. `HomeCountryCode` is its ISO 3166-1 alpha-2 code.
  - `AirlineGroup` is the optional ultimate parent company or group brand; it is null when the airline is independent or no `VERIFIED` source exists. It is not inferred from home country, brand similarity, or ownership assumptions.
  - `BusinessModelClass` is an optional, nullable analytical classification. It has no identity provenance, is excluded from T-72/T-75, and must be labelled as analytical in reports.
  - `OperatingRegion` is not a `DimAirline` column. Where regional grouping is required, derive it from `DimRoute`/`DimAirport` geography using a documented classification method.
  - `IsActive` is the airline operating status. `StatusEffectiveDate` is required when `IsActive = FALSE` and null for the baseline active state. `LifecycleStatus` and `MergedIntoAirlineId` are deferred and are not columns.
  - `ReferenceVersion` is a hidden technical lineage column identifying the immutable snapshot that produced the row. Its presence is not approval. The reference manifest is the authoritative approval record.
  - Airline identity attributes must reconcile exactly to `ref_airlines.csv` and the attribute-level provenance in `ref_airline_sources.csv` for the selected version.
  - Airline membership must not change during the reporting period. A merger, rebrand, or code change follows the change-control tiers in Section 3.4. A successor entity receives a new `AirlineId` and `AirlineKey`; old facts retain the old key.
  - `DimAirline` is Type 1. Immutable reference snapshots preserve build reproducibility but not as-was historical identity labels. Type 2 is deferred until a future requirement demands as-was identity reporting.

**Proposed administrative key allocation (OD-01B formal approval pending; not a source-verified fact):**

| # | Airline | Proposed `AirlineId` | Proposed `AirlineKey` |
|---:|---|---|---:|
| 1 | Emirates | `AIR-0001` | 1 |
| 2 | Qatar Airways | `AIR-0002` | 2 |
| 3 | Singapore Airlines | `AIR-0003` | 3 |
| 4 | Air India | `AIR-0004` | 4 |
| 5 | IndiGo | `AIR-0005` | 5 |
| 6 | British Airways | `AIR-0006` | 6 |
| 7 | Lufthansa | `AIR-0007` | 7 |
| 8 | Delta Air Lines | `AIR-0008` | 8 |
| 9 | Southwest Airlines | `AIR-0009` | 9 |
| 10 | Qantas | `AIR-0010` | 10 |

The table is an administrative allocation, not an airline identity fact. The mapping is loaded from the controlled key map; it is not re-derived from row order or a database identity sequence. A new airline receives the next unused pair; a retired airline retains its pair.

### 4.4 DimAirport

- **Business purpose:** provide airport geography, codes, and time zones for network, route, and operational analysis.
- **Grain:** one row per airport.
- **Primary key:** AirportKey.
- **Foreign keys:** none.
- **Required columns:** see Table 6.2.3.
- **Business rules:**
  - `AirportCode` is a unique three-letter uppercase code.
  - Airport codes and names are synthetic or explicitly designated as fictional for this project.
  - `Latitude` is between -90 and 90. `Longitude` is between -180 and 180.
  - `TimeZoneIANA` must be a valid IANA identifier, for example `America/New_York`, not an abbreviation such as `EST`.
  - An airport may serve multiple airlines and routes.
  - `IsActive` indicates whether the airport is in the baseline network; it does not remove historical rows.

### 4.5 DimRoute

- **Business purpose:** define the directional route network and its distance, region, and international status.
- **Grain:** one row per directional origin-destination pair. Route A-to-B is distinct from B-to-A.
- **Primary key:** RouteKey.
- **Foreign keys:** `OriginAirportKey` and `DestinationAirportKey` reference DimAirport.
- **Required columns:** see Table 6.2.4.
- **Business rules:**
  - Origin and destination must be different airports.
  - `DistanceKM` must be positive and must agree with the great-circle distance between the two airports within a documented tolerance, initially 2 percent.
  - `DistanceMiles = DistanceKM * 0.621371`, rounded to two decimals.
  - `RouteCode` is unique and follows `ORIGIN-DEST`, for example `AAA-BBB`.
  - `IsInternational = TRUE` when the origin and destination countries differ.
  - `RouteRegion` is a controlled grouping used for reporting, not a substitute for country.

### 4.6 DimAircraft

- **Business purpose:** identify each aircraft, its operator, type, capacity, fleet status, and planned availability.
- **Grain:** one row per aircraft.
- **Primary key:** AircraftKey.
- **Foreign keys:** `AirlineKey` references DimAirline; `AircraftTypeKey` references DimAircraftType.
- **Required columns:** see Table 6.2.5.
- **Business rules:**
  - `AircraftRegistration` is unique.
  - `SeatCapacity` is positive and must not exceed the aircraft type's `MaximumSeatCapacity`.
  - `FleetStatus` uses a controlled set: Active, Maintenance, Stored, Retired.
  - An aircraft has exactly one operator airline in the baseline. A lease transfer requires a new effective-dated record and approval.
  - `AirlineKey` is retained for lineage and validation. It must not create a second active filter path from DimAirline to FactFlightOperations; see Section 8.
The initial proposed value is 14.00 hours per active aircraft-day under OD-10; formal owner approval remains required.

### 4.7 DimAircraftType

- **Business purpose:** provide manufacturer, model, category, seat capacity, and range for fleet and capacity analysis.
- **Grain:** one row per aircraft type.
- **Primary key:** AircraftTypeKey.
- **Foreign keys:** none.
- **Required columns:** see Table 6.2.6.
- **Business rules:**
  - The combination of `Manufacturer` and `AircraftModel` is unique.
  - `TypicalSeatCapacity` and `MaximumSeatCapacity` are positive, and typical capacity must not exceed maximum capacity.
  - `RangeKM` is positive.
  - Aircraft types are fictional or generic and must not be used to make real-world fleet claims.

### 4.8 DimCustomer

- **Business purpose:** support customer segmentation, loyalty, booking behavior, satisfaction, complaints, refunds, and repeat-booking analysis.
- **Grain:** one row per fictional customer.
- **Primary key:** CustomerKey.
- **Foreign keys:** none.
- **Required columns:** see Table 6.2.7.
- **Business rules:**
  - `CustomerID` is unique and synthetic.
  - No real names, email addresses, phone numbers, addresses, passport numbers, or other personal identifiers are allowed.
  - `CustomerSegment` and `LoyaltyTier` use controlled values.
  - `RegistrationDate` must be on or before the customer's first booking date.
  - A customer may book multiple airlines and channels.
  - Customer attributes are Type 1 in the baseline. Historical segmentation changes are out of scope unless approved.

### 4.9 DimFareClass

- **Business purpose:** classify fares by cabin, refundability, and ancillary eligibility for fare-mix and revenue analysis.
- **Grain:** one row per fare class.
- **Primary key:** FareClassKey.
- **Foreign keys:** none.
- **Required columns:** see Table 6.2.8.
- **Business rules:**
  - `FareClassCode` is unique.
  - `CabinClass` uses a controlled set: Economy, Premium Economy, Business, First.
  - `RefundabilityCategory` uses a controlled set: Refundable, Partially Refundable, Non-Refundable.
  - Each fare class maps to exactly one cabin class.
  - `DisplayOrder` controls report sorting and must be unique within cabin.

### 4.10 DimBookingChannel

- **Business purpose:** classify the distribution channel used for a booking and support channel-mix analysis.
- **Grain:** one row per booking channel.
- **Primary key:** BookingChannelKey.
- **Foreign keys:** none.
- **Required columns:** see Table 6.2.9.
- **Business rules:**
  - `ChannelCode` and `ChannelName` are unique.
  - `ChannelCategory` uses a controlled set such as Direct Web, Mobile App, OTA, GDS, Call Center, Corporate, or Airport.
  - `IsDirect = TRUE` only for airline-owned direct channels.
  - The channel taxonomy must remain stable across the reporting period.

### 4.11 DimDisruptionType

- **Business purpose:** classify disruption events by cause, controllability, and reactionary eligibility.
- **Grain:** one row per disruption type.
- **Primary key:** DisruptionTypeKey.
- **Foreign keys:** none.
- **Required columns:** see Table 6.2.10.
- **Business rules:**
  - `DisruptionCode` and `DisruptionName` are unique.
  - `DisruptionCategory` uses a controlled set such as Weather, Air Traffic Control, Technical, Crew, Airport, Security, Passenger, Reactionary, or Other.
  - `ControllableFlag` identifies whether the airline could reasonably influence the cause. It is not the same as `ReactionaryEligibleFlag`.
  - `ReactionaryEligibleFlag = TRUE` only for a type that can be caused by an upstream disruption, such as a late inbound aircraft.
  - The existence of a delay does not make it reactionary. The fact table must carry explicit evidence; see Section 5.5.

### 4.12 DimCurrency

- **Business purpose:** preserve the original transaction currency and support currency validation and display.
- **Grain:** one row per currency.
- **Primary key:** CurrencyKey.
- **Foreign keys:** none.
- **Required columns:** see Table 6.2.11.
- **Business rules:**
  - `CurrencyCode` is a unique ISO 4217 three-letter code.
  - Exactly one row has `IsReportingCurrency = TRUE`; that row is USD.
  - `DecimalPlaces` is between 0 and 4 and must match the currency's minor-unit convention.
  - Exchange rates are not stored in DimCurrency. They are stored in `ref_exchange_rates.csv` and applied to financial facts as described in Section 10.
  - A currency may be used in transactions only if it exists in DimCurrency and has an approved rate for the relevant date.

## 5. Fact Table Catalogue and Grain

Facts store additive business events or transaction lines at a declared grain. Every fact has one authoritative grain, one surrogate primary key, required foreign keys, and additive measures that are safe to aggregate. Detailed column definitions and data types are in Section 6.3.

### 5.1 Fact Summary

| Fact | Business purpose | Authoritative grain | Primary key | Foreign keys | Core additive measures |
|---|---|---|---|---|---|
| FactFlightOperations | Flight capacity, traffic, punctuality, cancellations, completion, and utilization | One row per scheduled flight leg, including cancelled legs | FlightOperationKey | AirlineKey, RouteKey, AircraftKey, ScheduledDepartureDateKey, ScheduledArrivalDateKey | AvailableSeats, BookedPassengers, RevenuePassengers, NonRevenuePassengers, FlightDistanceKM, AvailableSeatKM, RevenuePassengerKM, delay minutes, block minutes |
| FactBookingTransactions | Passenger revenue, fare, ancillary revenue, refunds, channel, and booking behavior | One row per passenger ticket coupon | BookingTransactionKey | CustomerKey, AirlineKey, FlightOperationKey, RouteKey, FareClassKey, BookingChannelKey, BookingDateKey, TravelDateKey, TransactionCurrencyKey | PassengerCount, BaseFareUSD, DiscountUSD, TaxUSD, FeeUSD, FeeRefundUSD, CancellationFeeUSD, NoShowFeeUSD, AncillaryRevenueUSD, AncillaryRefundUSD, RefundUSD, NetPassengerRevenueUSD, NetFeeRevenueUSD, NetAncillaryRevenueUSD |
| FactOperatingCosts | Operating cost, CASK, contribution, and cost-category analysis | One row per operating-cost ledger line | OperatingCostKey | FlightOperationKey, AirlineKey, RouteKey, CostDateKey, CurrencyKey | CostAmountUSD |
| FactDisruptions | Delay and disruption events, causes, reactionary classification, and recovery | One row per disruption event for one flight leg and one disruption type | DisruptionKey | FlightOperationKey, AirlineKey, RouteKey, EventLocationAirportKey, DisruptionTypeKey, EventDateKey | DelayMinutes |
| FactCustomerFeedback | Satisfaction, complaints, service recovery, and customer voice | One row per customer feedback event | FeedbackKey | CustomerKey, AirlineKey, FlightOperationKey, RouteKey, FeedbackDateKey, ResolutionDateKey | Valid satisfaction score sum, valid response count, complaint count, service-recovery case count |

Fact design rule: every fact in this contract has exactly one authoritative grain, stated in its catalogue entry and enforced by its primary key and grain-uniqueness test in Section 7.3. Additive measures must be safe to aggregate at that grain; a measure that is not additive at the declared grain must be labeled non-additive and must not be summed. A fact must not mix aggregate rows with detail rows, must carry no unallocated booking- or period-level amount, and must reconcile its row count to RAW and STAGING dispositions. Changing a fact's grain is a material change requiring change control and approval.

**Fact-to-fact rule:** no fact table may have a relationship to another fact table. Shared dimensions provide cross-fact analysis. If a report requires a combination that cannot be expressed through conformed dimensions, the design must be reviewed and approved before implementation.

### 5.2 FactFlightOperations

- **Business purpose:** provide the flight-leg record used for capacity, traffic, load factor, punctuality, cancellation, completion, and aircraft-utilization analysis.
- **Authoritative grain:** one row per scheduled flight leg. A flight leg is one operating airline, one flight number, one scheduled departure date, one origin airport, one destination airport, and one scheduled departure time. It is directional. A return flight is a separate leg.
- **Cancelled flights:** cancelled legs remain in the fact with scheduled capacity and scheduled timestamps. Actual timestamps and delay minutes are null. This prevents silent exclusion from capacity denominators.
- **Primary key:** FlightOperationKey.
- **Foreign keys:** `AirlineKey` references DimAirline; `RouteKey` references DimRoute; `AircraftKey` references DimAircraft; `ScheduledDepartureDateKey` and `ScheduledArrivalDateKey` reference DimDate.
- **Required columns:** see Table 6.3.1.
- **Core additive measures:**
  - `AvailableSeatKM = AvailableSeats * FlightDistanceKM`
  - `RevenuePassengerKM = RevenuePassengers * FlightDistanceKM`
  - `AvailableSeats`, `BookedPassengers`, `RevenuePassengers`, `NonRevenuePassengers`, `FlightDistanceKM`, `DepartureDelayMinutes`, `ArrivalDelayMinutes`, and `BlockMinutes` are additive only in the context of their declared grain.
- **Business rules:**
  - `FlightOperationKey` is unique. `FlightLegID` is the unique business key.
  - A flight leg must have exactly one row. Rebooking, codeshare marketing, or a schedule change must not create a duplicate operating leg.
Codeshare marketing flights are not duplicated. The fact represents the operating flight leg. Marketing-carrier treatment is OD-16.
  - `FlightNumber` is not unique by itself. Uniqueness requires airline, date, route, and scheduled departure time.
  - `AvailableSeats` is the scheduled seat capacity and must be positive, including for cancelled flights.
  - `BookedPassengers` is the number of seats sold at scheduled departure, including revenue and non-revenue bookings. It may include passengers who do not travel (no-shows).
  - `RevenuePassengers` is the number of revenue passengers carried. `NonRevenuePassengers` is the number of award, employee, or other non-revenue passengers carried.
  - For operated flights, `BookedPassengers >= RevenuePassengers + NonRevenuePassengers`. The difference is no-shows or other booked passengers not carried. For cancelled flights, `BookedPassengers` may be greater than zero while both carried-passenger counts are zero.
  - `BookedPassengers` must not exceed `AvailableSeats` unless overbooking is explicitly approved. Overbooking is not in the baseline.
  - `RevenuePassengers` must not exceed `AvailableSeats` unless a documented exemption exists, such as an infant lap passenger.
  - `FlightDistanceKM` is the scheduled great-circle distance and must agree with DimRoute.DistanceKM within 0.5 percent.
`FlightStatus` uses exactly Operated or Cancelled. Every scheduled leg in the historical dataset has a final status. Diversion accounting is not in the baseline; OD-19.
  - `CancellationFlag = TRUE` if and only if `FlightStatus = Cancelled`.
  - `CompletionFlag = TRUE` if and only if `FlightStatus = Operated`.
  - `CancellationRate + CompletionRate = 1` for every evaluated population, because every scheduled leg is either cancelled or operated in this baseline.
  - `DepartureDelayMinutes` is actual departure minus scheduled departure in whole minutes. Negative values mean early departure. It is null for cancelled flights.
  - `ArrivalDelayMinutes` is actual arrival minus scheduled arrival in whole minutes. Negative values mean early arrival. It is null for cancelled flights.
  - `BlockMinutes` is actual arrival minus actual departure in whole minutes. It is null for cancelled flights.
  - `OnTimeFlag` is the departure on-time flag: true when departure delay is 15 minutes or less, including early departures. It is false for cancelled flights and for operated flights with a missing actual departure.
  - `OnTimeArrivalFlag` is the arrival on-time flag: true when arrival delay is 15 minutes or less. It is false for cancelled flights and for operated flights with a missing actual arrival.
The 15-minute threshold is the proposed baseline under OD-09; formal owner approval remains required.
  - Scheduled timestamps remain populated for cancelled flights. Actual timestamps are null for cancelled flights.
  - Scheduled departure and arrival date keys are local airport dates, not UTC dates. See Section 9.
  - For flights with a positive arrival delay, the sum of attributed disruption delay minutes must equal the flight's arrival delay minutes within a documented tolerance. T-23 specifies a proposed one-minute validation threshold; this is not an owner-approved acceptance threshold unless formally approved. For early or on-time flights, disruption events are optional and attributed delay minutes must be zero. Unattributed delay must be represented by an explicit event, not left unexplained.

### 5.3 FactBookingTransactions

- **Business purpose:** provide the commercial transaction record for passenger revenue, fare mix, ancillary revenue, refunds, booking channel, booking lead time, and customer behavior.
- **Authoritative grain:** one row per passenger ticket coupon. A coupon is one passenger on one flight segment within one booking. A booking with two passengers and two segments has four coupon rows.
- **Primary key:** BookingTransactionKey.
- **Foreign keys:** `CustomerKey` references DimCustomer; `AirlineKey` references DimAirline; `FlightOperationKey` references FactFlightOperations; `RouteKey` references DimRoute; `FareClassKey` references DimFareClass; `BookingChannelKey` references DimBookingChannel; `BookingDateKey` and `TravelDateKey` reference DimDate; `TransactionCurrencyKey` references DimCurrency.
- **Required columns:** see Table 6.3.2.
- **Core additive measures:** `PassengerCount`, `BaseFareUSD`, `DiscountUSD`, `TaxUSD`, `FeeUSD`, `AncillaryRevenueUSD`, `RefundUSD`, `AncillaryRefundUSD`, `FeeRefundUSD`, `CancellationFeeUSD`, `NoShowFeeUSD`, `NetPassengerRevenueUSD`, `NetFeeRevenueUSD`, and `NetAncillaryRevenueUSD`.
- **Business rules:**
  - `BookingTransactionKey` is unique. The combination of `BookingReference`, `TicketNumber`, and `TicketCouponNumber` must be unique.
  - `PassengerCount = 1` on every coupon row. It is a count of one passenger-coupon, not the booking party size.
  - A booking reference may contain multiple tickets, passengers, coupons, and flight segments. It is not unique in this fact.
  - A ticket number may contain multiple coupons. It is not unique in this fact.
  - `IsRevenuePassenger = TRUE` for revenue tickets and `FALSE` for award, employee, or other non-revenue tickets. Passenger revenue measures filter to `IsRevenuePassenger = TRUE`.
  - `FlightOperationKey` must resolve to a flight leg in FactFlightOperations. A booking on a cancelled flight remains in the fact with its cancellation status and refund treatment.
  - `RouteKey` is the booked route and must agree with the referenced flight leg. It is denormalized to support direct route filtering without a fact-to-fact relationship.
  - `TravelDateKey` is the local scheduled departure date of the coupon and must be within 2025-10-01 through 2026-09-30. `BookingDateKey` is the UTC calendar date of the booking transaction and may precede the period. The booking fact is a travel-period snapshot; bookings for travel after 2026-09-30 are out of scope.
  - `BookingLeadTimeDays` is the calendar-date difference between the coupon travel date and the booking date, in whole days. It must be zero or positive for valid bookings. Negative values are data-quality exceptions.
  - `BaseFareAmount` is the gross published fare before discount and excludes taxes, fees, and ancillary revenue.
  - `DiscountAmount` is a positive magnitude that reduces the base fare.
  - `TaxAmount` is a positive magnitude collected on behalf of a government or authority. It is not airline revenue.
  - `FeeAmount` is a positive magnitude of carrier-retained mandatory fees. It is revenue but not passenger revenue.
  - `AncillaryRevenueAmount` is a positive magnitude of optional ancillary revenue such as bags, seats, food, or Wi-Fi.
  - `RefundAmount` is a positive magnitude of passenger-fare refund. It reduces passenger revenue.
  - `AncillaryRefundAmount` is a positive magnitude of ancillary refund. It reduces ancillary revenue.
  - `FeeRefundAmount` is a positive magnitude of fee refund. It reduces fee revenue.
  - `CancellationFeeAmount` is a positive magnitude of a non-refundable cancellation fee retained by the airline. It is fee revenue, not passenger revenue.
  - `NoShowFeeAmount` is a positive magnitude of a non-refundable no-show fee retained by the airline. It applies only to NoShow coupons and is fee revenue, not passenger revenue.
  - `NetPassengerRevenueUSD = BaseFareUSD - DiscountUSD - RefundUSD` for Ticketed, Flown, or Refunded coupons. For Booked, Cancelled, or NoShow coupons, `NetPassengerRevenueUSD = 0`. Retained cancellation and no-show amounts are recorded separately in `CancellationFeeUSD` and `NoShowFeeUSD`, respectively, as fee revenue.
  - `NetFeeRevenueUSD = FeeUSD - FeeRefundUSD + CancellationFeeUSD + NoShowFeeUSD`.
  - `NetAncillaryRevenueUSD = AncillaryRevenueUSD - AncillaryRefundUSD`.
  - `TaxUSD` is excluded from all revenue measures.
  - Booking-level discounts, ancillary amounts, and refunds must be allocated to coupons exactly once. The allocation must sum to the booking total after rounding. The initial method is pro-rata to base fare with the residual assigned to the largest coupon; this is OD-14.
  - `TransactionStatus` uses a controlled set: Booked, Ticketed, Flown, Cancelled, Refunded, NoShow. `NoShow` means the booked passenger did not travel; no-show revenue treatment is part of OD-08.
  - `IsRefunded = TRUE` when any passenger, fee, or ancillary refund is greater than zero.
  - Passenger revenue is recognized for Ticketed, Flown, and Refunded coupons. It is zero for Booked, Cancelled, and NoShow coupons. Retained cancellation fees are recorded in `CancellationFeeUSD`; retained no-show fees are recorded in `NoShowFeeUSD`. The two fee fields are mutually exclusive.
  - The sum of coupon `PassengerCount` where `IsRevenuePassenger = TRUE` and `TransactionStatus = Flown` must reconcile to FactFlightOperations.RevenuePassengers for operated flights by flight. Cancelled coupons reconcile to zero carried passengers through a separate cancellation test. This is a critical reconciliation test. The applicable tolerance remains subject to OD-20 formal owner approval; until then, differences must be reported and must not be waived using an assumed tolerance.
  - No financial amount may be stored only in a booking-level row that is also repeated across coupon rows. Every repeated amount must be allocated and marked as allocated.

### 5.4 FactOperatingCosts

- **Business purpose:** provide operating-cost ledger lines for CASK, unit contribution, cost-category analysis, and route contribution.
- **Authoritative grain:** one row per operating-cost ledger line. A ledger line is one flight leg, one cost category, one cost subcategory, one cost date, and one source document line. The combination of `FlightOperationKey`, `CostCategory`, `CostSubcategory`, `CostDateKey`, and `SourceDocumentNumber` must be unique.
- **Primary key:** OperatingCostKey.
- **Foreign keys:** `FlightOperationKey` references FactFlightOperations; `AirlineKey` references DimAirline; `RouteKey` references DimRoute; `CostDateKey` references DimDate; `CurrencyKey` references DimCurrency.
- **Required columns:** see Table 6.3.3.
- **Core additive measure:** `CostAmountUSD`.
- **Business rules:**
  - Costs are recognized at the ledger-line grain. A cost that covers multiple flights must be allocated to flight legs with a documented allocation method and an `IsAllocated = TRUE` flag.
  - `CostAmount` is signed in the original currency: positive for an expense, negative for a credit or rebate. `CostAmountUSD` follows the same sign after conversion.
  - `CostCategory` uses a controlled set: Fuel, Crew, Maintenance, Airport Charges, Navigation, Sales and Distribution, Overhead, Other.
  - `CostSubcategory` is a controlled lower-level value within the category.
  - `CostDescription` is a short synthetic description and must not contain personal data or secrets.
  - `SourceDocumentNumber` identifies the synthetic ledger document and supports uniqueness and audit.
  - Costs must not be duplicated in another fact table. There is no separate cost fact in the baseline.
  - Non-operating costs, interest, tax, foreign-exchange gains and losses, and one-off impairments are excluded from CASK.
  - `RouteKey` must agree with the referenced flight leg. It is denormalized for direct route filtering without a fact-to-fact relationship.
  - The sum of `CostAmountUSD` by airline and period must reconcile to the synthetic cost control total within the proposed 0.01 USD engineering validation threshold after allocation. This is not an owner-approved acceptance threshold.

### 5.5 FactDisruptions

- **Business purpose:** provide event-level evidence for delays, cancellations, disruption causes, reactionary classification, recovery, and operational hotspots.
- **Authoritative grain:** one row per disruption event associated with exactly one flight leg and exactly one disruption type. A flight may have multiple events. `EventSequence` distinguishes events on the same flight.
- **Primary key:** DisruptionKey.
- **Foreign keys:** `FlightOperationKey` is a logical reference to FactFlightOperations; `AirlineKey` references DimAirline; `RouteKey` references DimRoute; `EventLocationAirportKey` references DimAirport; `DisruptionTypeKey` references DimDisruptionType; `EventDateKey` references DimDate.
- **Required columns:** see Table 6.3.4.
- **Core additive measure:** `DelayMinutes`.
- **Business rules:**
  - `DisruptionID` is the globally unique business key. `DisruptionKey` is the surrogate key.
  - `EventSequence` starts at 1 for each flight and increments by exactly 1 for each successive disruption event within that flight. The combination of `FlightOperationKey` and `EventSequence` must be unique and contiguous within each flight.
  - `DelayMinutes` is the portion of the flight's delay attributed to this event. It must be zero or positive.
  - For flights with a positive arrival delay, the sum of event `DelayMinutes` for a flight must equal the flight's `ArrivalDelayMinutes` within a documented tolerance. T-23's proposed one-minute engineering validation threshold is not an owner-approved acceptance threshold unless formally approved. An explicit Unattributed event must be recorded where delay cannot be attributed. For early or on-time flights, disruption events are optional and `DelayMinutes` must be zero. Events must partition delay, not repeat it.
  - `PrimaryCauseFlag = TRUE` for exactly one event per flight when a primary cause is identified. If no cause is identified, all events have `PrimaryCauseFlag = FALSE` and an Unattributed event is created.
  - `ReactionaryFlag = TRUE` only when all three conditions hold: the disruption type is reactionary-eligible, an upstream flight or event is identified in `ReactionaryEvidenceID`, and the event is classified as reactionary in the source. A delay is not reactionary merely because it exists.
  - If evidence is missing, `ReactionaryFlag = FALSE` and the event is reported as unclassified reactionary status. It must not be guessed.
  - `EventStartTimestampUTC` and `EventEndTimestampUTC` are UTC. `EventEndTimestampUTC` may be null for an open event.
  - `EventLocationAirportKey` identifies the airport at which the disruption event occurred. In the proposed synthetic baseline, use the referenced flight route origin when no more specific airport location is supplied; use the destination only when the source explicitly associates the event with that airport. The key must resolve to the route origin or destination. Intermediate and en-route event locations are outside this baseline and must be quarantined with a reason code pending an approved scope change.
  - `EventDateKey` is derived from `EventStartTimestampUTC` converted to the IANA local time zone of `EventLocationAirportKey`. The event start timestamp is authoritative for the event date; `EventEndTimestampUTC` does not determine the date key. The applicable time-zone database version must be recorded in the generation manifest.
  - `RecoveryStatus` uses a controlled set: Open, In Progress, Resolved, Closed - No Action.
  - Cancelled flights may have a cancellation event. If a cancellation event exists, its delay minutes are zero and the cancellation is analyzed through FactFlightOperations.
  - The fact must not relate directly to FactCustomerFeedback. Customer impact is analyzed through shared dimensions and separate measures.

### 5.6 FactCustomerFeedback

- **Business purpose:** provide customer feedback events for satisfaction, complaints, service recovery, and customer-experience analysis.
- **Authoritative grain:** one row per customer feedback event. A feedback event is one survey, complaint, compliment, or claim submitted by one customer about one flight, with one unique feedback identifier.
- **Primary key:** FeedbackKey.
- **Foreign keys:** `CustomerKey` references DimCustomer; `AirlineKey` references DimAirline; `FlightOperationKey` references FactFlightOperations; `RouteKey` references DimRoute; `FeedbackDateKey` and `ResolutionDateKey` reference DimDate.
- **Required columns:** see Table 6.3.5.
- **Core additive measures:** feedback event count, complaint count, valid satisfaction score sum, valid satisfaction response count, and service-recovery case count.
- **Business rules:**
  - `FeedbackID` is unique. One feedback event must not be duplicated because it contains multiple comments or categories.
  - `FeedbackType` uses a controlled set: Survey, Complaint, Compliment, Claim.
  - `SatisfactionScore` is an integer from 1 to 5, or null when the feedback type does not collect a score. The scale is OD-11.
  - `ComplaintCategory` is required when `FeedbackType = Complaint` and is null otherwise.
  - `ServiceRecoveryFlag = TRUE` only when the event triggered a service-recovery case.
  - `ResolutionStatus` uses a controlled set: Open, In Progress, Resolved, Closed - No Action.
  - `ResolutionDateKey` is required when `ResolutionStatus = Resolved`; it must be on or after `FeedbackDateKey`.
  - `FeedbackDateKey` is the UTC calendar date of submission. `ResolutionDateKey` is the UTC calendar date of resolution.
  - A customer may submit multiple feedback events. Duplicate detection uses customer, flight, feedback type, and submission timestamp.
  - Free-text comments are out of scope in the baseline. If added, they must be synthetic and screened for personal data.
  - The fact must not relate directly to FactDisruptions. Service-recovery analysis uses complaint events and shared dimensions, not a fact-to-fact relationship.

## 6. Required Columns and Data Definitions

This section defines the required columns for every dimension and fact. A column marked required must be present and non-null in CURATED. Optional columns may be null only for the reasons stated. Data types are logical contract types; the physical CSV or Parquet representation must preserve them.

### 6.1 Data-Type and Format Conventions

| Logical type | Contract representation | Format or range | Use |
|---|---|---|---|
| Surrogate key | Int64 or Int32 | Positive integer; -1 reserved for an approved unknown member | Dimension and fact primary keys, foreign keys |
| Business key | String | Uppercase where the business code is uppercase; no leading or trailing spaces | Airline, airport, route, ticket, booking, and feedback identifiers |
| Date | Date | ISO 8601 `YYYY-MM-DD` | Calendar dates without a time |
| Timestamp | DateTime | ISO 8601 UTC `YYYY-MM-DDThh:mm:ssZ` | Operational and audit timestamps |
| Boolean | Boolean | `TRUE` or `FALSE`; no `Y`, `N`, `1`, or `0` in CURATED | Flags |
| Integer count | Int32 or Int16 | Zero or positive unless the definition allows negative | Seats, passengers, minutes, days |
| Money | Decimal(18,2) | Two decimal places; original currency or USD as named | Fares, taxes, fees, revenue, cost |
| Rate | Decimal(18,6) | Six decimal places unless otherwise stated | Exchange rates, conversion factors |
| Ratio | Decimal(18,6) | Stored as a decimal fraction, not a formatted percentage | KPI results and conversion factors |
| Distance | Decimal(9,2) | Kilometres or miles, two decimal places | Route and flight distance |
| Coordinate | Decimal(9,6) | Latitude or longitude, six decimal places | Airport geography |
| Text | String | UTF-8; trimmed; no control characters | Names, descriptions, categories |
| Code | String | Uppercase; fixed or maximum length as stated | Airline, airport, fare, channel, disruption codes |
| Percentage | Decimal(9,6) | Decimal fraction from 0 to 1 in storage; formatted as percent in Power BI | Rates and shares |

**Naming conventions:**

- `...Key` is a surrogate key or foreign key.
- `...ID` is a business identifier.
- `...Flag` is Boolean.
- `...Amount` is money in the transaction currency.
- `...USD` is money in USD.
- `...TimestampUTC` is a UTC timestamp.
- `...DateKey` is a local or contract-defined date key, as documented.
- `...Rate` is a decimal rate.
- `...Count` is an integer count.

**Null and empty-value rules:**

- Required columns are never null and never contain an empty string.
- Optional columns use null, not `N/A`, `Unknown`, `0`, or a placeholder, unless the placeholder is a controlled dimension member.
- A zero is a real value and must not be used to mean missing.
- Text values are trimmed and case-standardized before loading.
- A rejected value must not be coerced to a valid value without a disposition record.

**Rounding rules:**

- Store money at two decimals. Do not round intermediate allocations before the final allocation step.
- Store rates at six decimals. Do not round a rate before multiplying an amount.
- Store ratios at six decimals. Round only for presentation.
- Allocation residuals are assigned by the documented largest-remainder rule so that component totals equal the control total exactly at two decimals.
- KPI presentation uses one decimal for percentages, two decimals for USD, and four decimals for USD per ASK or per RPK, unless a page specifies otherwise.

### 6.2 Dimension Columns

#### 6.2.1 DimDate

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| DateKey | Int32 | No | Primary key in `YYYYMMDD` format. Unique. |
| FullDate | Date | No | Calendar date. Unique. Model date column. |
| Year | Int16 | No | Calendar year. |
| Quarter | Int8 | No | Calendar quarter 1 through 4. |
| MonthNumber | Int8 | No | Calendar month 1 through 12. |
| MonthName | String(20) | No | English month name. Sort by MonthNumber. |
| MonthShortName | String(3) | No | Three-letter month abbreviation. |
| YearMonth | String(7) | No | `YYYY-MM`. |
| YearMonthSort | Int32 | No | `YYYYMM` integer for sorting. |
| WeekNumber | Int8 | No | ISO 8601 week number. |
| WeekStartDate | Date | No | ISO week start date. |
| DayOfMonth | Int8 | No | Day 1 through 31. |
| DayName | String(10) | No | English day name. Sort by DayOfWeekNumber. |
| DayOfWeekNumber | Int8 | No | ISO weekday 1 through 7, Monday through Sunday. |
| IsWeekend | Boolean | No | True for Saturday and Sunday. |
| IsReportingPeriod | Boolean | No | True only for 2025-10-01 through 2026-09-30. |
| FiscalYear | Int16 | No | Fiscal year label. FY2026 starts 2025-10-01. |
| FiscalQuarter | Int8 | No | Fiscal quarter 1 through 4, starting in October. |
| FiscalMonthNumber | Int8 | No | Fiscal month 1 through 12, starting in October. |

#### 6.2.2 DimAirline

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| AirlineKey | Int32 | No | Primary key. Permanent warehouse surrogate; positive; unique; never reused or changed. Hidden from report view. |
| AirlineId | String(20) | No | Durable business identity. Format `^AIR-[0-9]{4}$`; unique; never reused. Used for reference and provenance reconciliation, not as a physical relationship key. |
| AirlineIATACode | String(2) | No | Two-character uppercase alphanumeric IATA attribute. Unique within `ReferenceVersion`; mutable only through a new version. Not a key. |
| AirlineICAOCode | String(3) | No | Three-character uppercase ICAO attribute. Unique within `ReferenceVersion`; mutable only through a new version. Not a key. |
| AirlineName | String(100) | No | Commercial brand name used by the project. Unique within `ReferenceVersion`; not the legal entity name; no legal suffix unless part of the brand. |
| AirlineGroup | String(100) | Yes | Optional ultimate parent company or group brand, supported by a `VERIFIED` source; null when independent or unverified. No inference. |
| HomeCountry | String(100) | No | Country of the airline's principal headquarters or domicile; not incorporation country, AOC state, or ultimate ownership. |
| HomeCountryCode | String(2) | No | ISO 3166-1 alpha-2 code for `HomeCountry`. |
| BusinessModelClass | String(50) | Yes | Optional analytical classification (Full Service, Low Cost, Regional, Charter, Hybrid/Other, Unknown). Not source-verified identity; no identity provenance; null allowed; label as analytical. |
| IsActive | Boolean | No | Airline operating status. True for the ten baseline airlines. False for a suspended or ceased airline in a later approved version. |
| StatusEffectiveDate | Date | Yes | Date the current `IsActive = FALSE` status took effect. Required when `IsActive = FALSE`; null for the baseline active state. |
| ReferenceVersion | String(30) | No | Hidden technical lineage field for the immutable snapshot that produced the row. Format `AIR-YYYY-MM-DD-NNN`. Its presence is not approval. |

#### 6.2.3 DimAirport

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| AirportKey | Int32 | No | Primary key. Unique. |
| AirportCode | String(3) | No | Unique three-letter uppercase airport code. |
| AirportName | String(100) | No | Synthetic airport name. |
| City | String(100) | No | Synthetic or generic city. |
| Country | String(100) | No | Country name. |
| CountryCode | String(2) | No | ISO 3166-1 alpha-2 code. |
| Region | String(50) | No | Controlled region label. |
| Latitude | Decimal(9,6) | No | -90.000000 through 90.000000. |
| Longitude | Decimal(9,6) | No | -180.000000 through 180.000000. |
| TimeZoneIANA | String(64) | No | Valid IANA time-zone identifier. |
| IsActive | Boolean | No | True when the airport is in the baseline network. |

#### 6.2.4 DimRoute

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| RouteKey | Int32 | No | Primary key. Unique. |
| RouteCode | String(20) | No | Unique `ORIGIN-DEST` code. |
| OriginAirportKey | Int32 | No | Foreign key to DimAirport. |
| DestinationAirportKey | Int32 | No | Foreign key to DimAirport. |
| DistanceKM | Decimal(9,2) | No | Positive scheduled great-circle distance in kilometres. |
| DistanceMiles | Decimal(9,2) | No | `DistanceKM * 0.621371`, rounded to two decimals. |
| RouteRegion | String(50) | No | Controlled route-region label. |
| IsInternational | Boolean | No | True when origin and destination countries differ. |
| IsActive | Boolean | No | True when the route is in the baseline network. |

#### 6.2.5 DimAircraft

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| AircraftKey | Int32 | No | Primary key. Unique. |
| AircraftRegistration | String(20) | No | Unique fictional registration. |
| AirlineKey | Int32 | No | Foreign key to DimAirline for lineage and validation. |
| AircraftTypeKey | Int32 | No | Foreign key to DimAircraftType. |
| FleetEntryDate | Date | No | Date the aircraft entered the operator fleet. |
| FleetStatus | String(30) | No | Active, Maintenance, Stored, or Retired. |
| SeatCapacity | Int16 | No | Positive configured seat capacity. |
| PlannedDailyAvailableHours | Decimal(4,2) | No | Planned available hours per active day. Baseline 14.00; OD-10. |
| IsActive | Boolean | No | True when the aircraft is available in the baseline fleet. |

#### 6.2.6 DimAircraftType

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| AircraftTypeKey | Int32 | No | Primary key. Unique. |
| Manufacturer | String(50) | No | Fictional or generic manufacturer. |
| AircraftModel | String(50) | No | Fictional or generic model. |
| AircraftCategory | String(30) | No | Narrowbody, Widebody, Regional Jet, or Turboprop. |
| TypicalSeatCapacity | Int16 | No | Positive typical two-class capacity. |
| MaximumSeatCapacity | Int16 | No | Positive maximum certified capacity. |
| RangeKM | Decimal(9,2) | No | Positive nominal range in kilometres. |
| BodyType | String(30) | No | Passenger, Freighter, or Mixed. |

#### 6.2.7 DimCustomer

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| CustomerKey | Int32 | No | Primary key. Unique. |
| CustomerID | String(20) | No | Unique synthetic customer identifier. |
| CustomerSegment | String(30) | No | Leisure, Business, Corporate, or Group. |
| LoyaltyTier | String(30) | No | None, Silver, Gold, or Platinum. |
| HomeCountry | String(100) | No | Synthetic or generic home country. |
| HomeCountryCode | String(2) | No | ISO 3166-1 alpha-2 code. |
| RegistrationDate | Date | No | Synthetic registration date. Must be on or before first booking. |
| IsActive | Boolean | No | True when the customer is active in the baseline. |

#### 6.2.8 DimFareClass

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| FareClassKey | Int32 | No | Primary key. Unique. |
| FareClassCode | String(5) | No | Unique fare-class code. |
| FareClassName | String(50) | No | Descriptive fare-class name. |
| CabinClass | String(30) | No | Economy, Premium Economy, Business, or First. |
| RefundabilityCategory | String(30) | No | Refundable, Partially Refundable, or Non-Refundable. |
| IsAncillaryEligible | Boolean | No | True when the fare can purchase optional ancillary services. |
| DisplayOrder | Int16 | No | Unique display order within cabin. |

#### 6.2.9 DimBookingChannel

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| BookingChannelKey | Int32 | No | Primary key. Unique. |
| ChannelCode | String(10) | No | Unique channel code. |
| ChannelName | String(50) | No | Unique channel name. |
| ChannelCategory | String(30) | No | Direct Web, Mobile App, OTA, GDS, Call Center, Corporate, or Airport. |
| IsDirect | Boolean | No | True only for airline-owned direct channels. |
| IsActive | Boolean | No | True when the channel is in the baseline. |

#### 6.2.10 DimDisruptionType

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| DisruptionTypeKey | Int32 | No | Primary key. Unique. |
| DisruptionCode | String(10) | No | Unique disruption code. |
| DisruptionName | String(50) | No | Unique disruption name. |
| DisruptionCategory | String(50) | No | Weather, Air Traffic Control, Technical, Crew, Airport, Security, Passenger, Reactionary, or Other. |
| ControllableFlag | Boolean | No | True when the airline could reasonably influence the cause. |
| ReactionaryEligibleFlag | Boolean | No | True only for types that can be caused by an upstream disruption. |
| IsActive | Boolean | No | True when the type is in the baseline taxonomy. |

#### 6.2.11 DimCurrency

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| CurrencyKey | Int32 | No | Primary key. Unique. |
| CurrencyCode | String(3) | No | Unique ISO 4217 code. |
| CurrencyName | String(50) | No | Currency name. |
| CurrencySymbol | String(5) | No | Display symbol. |
| DecimalPlaces | Int8 | No | 0 through 4, matching the currency minor unit. |
| IsReportingCurrency | Boolean | No | True only for USD. Exactly one true row. |

### 6.3 Fact Columns

#### 6.3.1 FactFlightOperations

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| FlightOperationKey | Int64 | No | Primary key. Unique. |
| FlightLegID | String(40) | No | Unique business key for the scheduled leg. |
| FlightNumber | String(10) | No | Operating flight number. Not unique by itself. |
| AirlineKey | Int32 | No | Foreign key to DimAirline. Operating airline. |
| RouteKey | Int32 | No | Foreign key to DimRoute. |
| AircraftKey | Int32 | Yes | Foreign key to DimAircraft. Null only when no aircraft was assigned before cancellation. |
| ScheduledDepartureTimestampUTC | DateTime | No | Scheduled departure in UTC. Populated for cancelled flights. |
| ActualDepartureTimestampUTC | DateTime | Yes | Actual departure in UTC. Null for cancelled flights. |
| ScheduledArrivalTimestampUTC | DateTime | No | Scheduled arrival in UTC. Populated for cancelled flights. |
| ActualArrivalTimestampUTC | DateTime | Yes | Actual arrival in UTC. Null for cancelled flights. |
| ScheduledDepartureDateKey | Int32 | No | Local calendar date at the origin airport. Foreign key to DimDate. |
| ScheduledArrivalDateKey | Int32 | No | Local calendar date at the destination airport. Foreign key to DimDate. |
| AvailableSeats | Int16 | No | Scheduled seat capacity. Positive, including cancelled flights. |
| BookedPassengers | Int16 | No | Seats sold at scheduled departure, including revenue and non-revenue bookings, including no-shows. |
| RevenuePassengers | Int16 | No | Revenue passengers carried. Zero for cancelled flights. |
| NonRevenuePassengers | Int16 | No | Award, employee, or other non-revenue passengers carried. Zero for cancelled flights. |
| FlightDistanceKM | Decimal(9,2) | No | Scheduled great-circle distance in kilometres. Positive. |
| FlightStatus | String(20) | No | Operated or Cancelled. Every historical scheduled leg has a final status. |
| DepartureDelayMinutes | Int16 | Yes | Actual minus scheduled departure in whole minutes. Negative means early. Null for cancelled. |
| ArrivalDelayMinutes | Int16 | Yes | Actual minus scheduled arrival in whole minutes. Negative means early. Null for cancelled. |
| BlockMinutes | Int16 | Yes | Actual arrival minus actual departure in whole minutes. Null for cancelled. |
| CancellationFlag | Boolean | No | True if and only if FlightStatus is Cancelled. |
| CompletionFlag | Boolean | No | True if and only if FlightStatus is Operated. |
| OnTimeFlag | Boolean | No | Departure on-time flag: DepartureDelayMinutes <= 15. False for cancelled or missing actual departure. |
| OnTimeArrivalFlag | Boolean | No | Arrival on-time flag: ArrivalDelayMinutes <= 15. False for cancelled or missing actual arrival. |

**Derived measures, not stored columns:**

- `AvailableSeatKM = AvailableSeats * FlightDistanceKM`
- `RevenuePassengerKM = RevenuePassengers * FlightDistanceKM`
- `BlockHours = BlockMinutes / 60`

These expressions are part of the contract. If they are materialized in CURATED for performance, they must be reconciled to the row-level expression and must not diverge.

#### 6.3.2 FactBookingTransactions

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| BookingTransactionKey | Int64 | No | Primary key. Unique. |
| BookingReference | String(20) | No | Booking locator. Not unique; groups one or more coupons. |
| TicketNumber | String(20) | No | Ticket number. Not unique; a ticket may have multiple coupons. |
| TicketCouponNumber | Int8 | No | Coupon sequence within the ticket. Positive. |
| CustomerKey | Int32 | No | Foreign key to DimCustomer. |
| AirlineKey | Int32 | No | Foreign key to DimAirline. Operating airline of the coupon. Ticketing-carrier differences are OD-16. |
| FlightOperationKey | Int64 | No | Logical fact reference to FactFlightOperations for lineage and reconciliation; not a Power BI model relationship. |
| RouteKey | Int32 | No | Foreign key to DimRoute. Must agree with the flight leg. |
| FareClassKey | Int32 | No | Foreign key to DimFareClass. |
| BookingChannelKey | Int32 | No | Foreign key to DimBookingChannel. |
| BookingDateKey | Int32 | No | UTC calendar date of the booking transaction. Foreign key to DimDate. |
| TravelDateKey | Int32 | No | Local scheduled departure date of the coupon. Foreign key to DimDate. |
| PassengerCount | Int8 | No | Always 1 on a coupon row. |
| IsRevenuePassenger | Boolean | No | True for revenue tickets; false for award, employee, or other non-revenue tickets. |
| BaseFareAmount | Decimal(18,2) | No | Gross published fare before discount. Excludes taxes, fees, and ancillary. |
| DiscountAmount | Decimal(18,2) | No | Positive discount magnitude applied to the base fare. |
| TaxAmount | Decimal(18,2) | No | Positive government or authority tax. Not airline revenue. |
| FeeAmount | Decimal(18,2) | No | Positive carrier-retained mandatory fee. Revenue, but not passenger revenue. |
| AncillaryRevenueAmount | Decimal(18,2) | No | Positive optional ancillary revenue. |
| RefundAmount | Decimal(18,2) | No | Positive passenger-fare refund magnitude. |
| AncillaryRefundAmount | Decimal(18,2) | No | Positive ancillary refund magnitude. |
| FeeRefundAmount | Decimal(18,2) | No | Positive fee refund magnitude. |
| CancellationFeeAmount | Decimal(18,2) | No | Positive non-refundable cancellation fee retained by the airline. |
| NoShowFeeAmount | Decimal(18,2) | No | Positive non-refundable no-show fee retained by the airline; applies only to NoShow coupons. |
| TransactionCurrencyKey | Int32 | No | Foreign key to DimCurrency. Original transaction currency. |
| ExchangeRateToUSD | Decimal(18,6) | No | USD per one unit of transaction currency. Positive. |
| BaseFareUSD | Decimal(18,2) | No | BaseFareAmount converted to USD. |
| DiscountUSD | Decimal(18,2) | No | DiscountAmount converted to USD. |
| TaxUSD | Decimal(18,2) | No | TaxAmount converted to USD. Excluded from revenue. |
| FeeUSD | Decimal(18,2) | No | FeeAmount converted to USD. |
| AncillaryRevenueUSD | Decimal(18,2) | No | AncillaryRevenueAmount converted to USD. |
| RefundUSD | Decimal(18,2) | No | RefundAmount converted to USD. |
| AncillaryRefundUSD | Decimal(18,2) | No | AncillaryRefundAmount converted to USD. |
| FeeRefundUSD | Decimal(18,2) | No | FeeRefundAmount converted to USD. |
| CancellationFeeUSD | Decimal(18,2) | No | CancellationFeeAmount converted to USD. |
| NoShowFeeUSD | Decimal(18,2) | No | NoShowFeeAmount converted to USD. |
| NetPassengerRevenueUSD | Decimal(18,2) | No | BaseFareUSD - DiscountUSD - RefundUSD for Ticketed, Flown, or Refunded coupons; zero for Booked, Cancelled, or NoShow coupons. |
| NetFeeRevenueUSD | Decimal(18,2) | No | FeeUSD - FeeRefundUSD + CancellationFeeUSD + NoShowFeeUSD. |
| NetAncillaryRevenueUSD | Decimal(18,2) | No | AncillaryRevenueUSD - AncillaryRefundUSD. |
| TransactionStatus | String(20) | No | Booked, Ticketed, Flown, Cancelled, Refunded, or NoShow. |
| IsRefunded | Boolean | No | True when any refund amount is greater than zero. |
| BookingLeadTimeDays | Int16 | No | Calendar-date difference between TravelDate and BookingDate in whole days. Zero or positive for valid bookings. Int16 is a storage-type constraint, not an approved business maximum; the proposed 365-day maximum remains open under OD-22 and must not be enforced until approved. |

**Revenue identity:** `NetPassengerRevenueUSD + NetFeeRevenueUSD + NetAncillaryRevenueUSD` is the coupon contribution to total operating revenue. `TaxUSD` is never added to revenue.

#### 6.3.3 FactOperatingCosts

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| OperatingCostKey | Int64 | No | Primary key. Unique. |
| CostLineID | String(30) | No | Unique business key for the ledger line. |
| FlightOperationKey | Int64 | No | Logical fact reference to FactFlightOperations for lineage and reconciliation; not a Power BI model relationship. |
| AirlineKey | Int32 | No | Foreign key to DimAirline. |
| RouteKey | Int32 | No | Foreign key to DimRoute. Must agree with the flight leg. |
| CostDateKey | Int32 | No | Accounting date. Foreign key to DimDate. |
| CostCategory | String(30) | No | Fuel, Crew, Maintenance, Airport Charges, Navigation, Sales and Distribution, Overhead, or Other. |
| CostSubcategory | String(50) | No | Controlled subcategory within the category. |
| CostAmount | Decimal(18,2) | No | Signed original-currency amount. Positive expense; negative credit. |
| CurrencyKey | Int32 | No | Foreign key to DimCurrency. Original cost currency. |
| ExchangeRateToUSD | Decimal(18,6) | No | USD per one unit of cost currency. Positive. |
| CostAmountUSD | Decimal(18,2) | No | CostAmount converted to USD, with the same sign. |
| CostDescription | String(200) | No | Short synthetic description. No personal data or secrets. |
| SourceDocumentNumber | String(50) | No | Synthetic ledger document identifier. |
| IsAllocated | Boolean | No | True when the cost was allocated from a multi-flight or period pool. |

#### 6.3.4 FactDisruptions

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| DisruptionKey | Int64 | No | Primary key. Unique. |
| DisruptionID | String(30) | No | Unique business key. |
| FlightOperationKey | Int64 | No | Logical fact reference to FactFlightOperations for lineage and reconciliation; not a Power BI model relationship. |
| AirlineKey | Int32 | No | Foreign key to DimAirline. |
| RouteKey | Int32 | No | Foreign key to DimRoute. Must agree with the flight leg. |
| EventLocationAirportKey | Int32 | No | Proposed foreign key to DimAirport.AirportKey. Must identify the route origin or destination airport for the referenced flight. |
| DisruptionTypeKey | Int32 | No | Foreign key to DimDisruptionType. |
| EventSequence | Int8 | No | Positive sequence of the event within the flight. Unique with FlightOperationKey. |
| EventDateKey | Int32 | No | Local calendar date derived from EventStartTimestampUTC using EventLocationAirportKey and its DimAirport.TimeZoneIANA. Foreign key to DimDate. |
| EventStartTimestampUTC | DateTime | No | Event start in UTC. |
| EventEndTimestampUTC | DateTime | Yes | Event end in UTC. Null for an open event. |
| DelayMinutes | Int16 | No | Positive portion of flight delay attributed to this event. |
| PrimaryCauseFlag | Boolean | No | True for exactly one event per flight when a primary cause is identified. |
| ReactionaryFlag | Boolean | No | True only with an eligible type and explicit upstream evidence. |
| ReactionaryEvidenceID | String(40) | Yes | Upstream flight or event identifier supporting reactionary classification. Required when ReactionaryFlag is true. |
| RecoveryStatus | String(30) | No | Open, In Progress, Resolved, or Closed - No Action. |

#### 6.3.5 FactCustomerFeedback

| Column | Data type | Null | Definition and rule |
|---|---|---|---|
| FeedbackKey | Int64 | No | Primary key. Unique. |
| FeedbackID | String(30) | No | Unique business key. |
| CustomerKey | Int32 | No | Foreign key to DimCustomer. |
| AirlineKey | Int32 | No | Foreign key to DimAirline. |
| FlightOperationKey | Int64 | No | Logical fact reference to FactFlightOperations for lineage and reconciliation; not a Power BI model relationship. |
| RouteKey | Int32 | No | Foreign key to DimRoute. Must agree with the flight leg. |
| FeedbackDateKey | Int32 | No | UTC calendar date of submission. Foreign key to DimDate. |
| FeedbackType | String(20) | No | Survey, Complaint, Compliment, or Claim. |
| SatisfactionScore | Int8 | Yes | Integer 1 through 5. Null when no score is collected. |
| ComplaintCategory | String(50) | Yes | Required for Complaint; null otherwise. |
| ServiceRecoveryFlag | Boolean | No | True only when the event triggered a service-recovery case. |
| ResolutionStatus | String(30) | No | Open, In Progress, Resolved, or Closed - No Action. |
| ResolutionDateKey | Int32 | Yes | UTC calendar date of resolution. Required when Resolved. Foreign key to DimDate. |
| FeedbackChannel | String(30) | No | Web, Mobile, Email, Call Center, Airport, or Social. |

**Feedback rule:** a feedback row represents one event, not one comment. Multiple comments, categories, or survey answers must not create duplicate feedback rows. If a multi-question survey is added later, the event grain remains one row and the answers are stored in a separate approved structure.

**Disruption timestamp rule:** when `EventEndTimestampUTC` is populated, it must be greater than or equal to `EventStartTimestampUTC`.

## 7. Primary Keys and Foreign Keys

### 7.1 Key Design Rules

- Every dimension and fact has one surrogate primary key. General dimension and fact surrogate keys are deterministic integers assigned from a documented sort order and must be stable for the same seed, configuration, and code version.
- `AirlineKey` is the exception that must be governed explicitly: it is a permanent positive `Int32` assigned once per `AirlineId` in a controlled key map. The same `AirlineId` must always resolve to the same `AirlineKey`. It must not be assigned from CSV row order, sort order, `row_number`, hash order, random selection, database `IDENTITY`, auto-increment, or a newly generated sequence during a clean rebuild.
- The airline key map is immutable after G3-RV-01 reference-version approval, is stored with or hashed into the approved reference manifest, and is loaded by every clean rebuild. OD-01B approval does not approve or immutabilize the proposed key map. A missing or inconsistent map blocks generation and refresh.
- Surrogate keys are not reused across dataset versions. A retired member remains in the dimension with `IsActive = FALSE` where applicable. A retired airline retains its `AirlineId` and `AirlineKey`.
- Key `-1` is reserved for an approved unknown member. It must not be used for a required foreign key unless the unknown-member rule is explicitly approved. The baseline does not use unknown members for required keys.
- Business keys are unique and are never used as the physical relationship key in Power BI. `AirlineId` is a durable business identity, not a physical relationship key; `AirlineKey` is the relationship key.
- DateKey is an intelligent `YYYYMMDD` integer and is the only approved intelligent surrogate key.
- Dimension foreign keys must resolve to exactly one dimension row in CURATED. Logical fact references such as `FlightOperationKey` must resolve to exactly one fact row for lineage and reconciliation; they are not model relationships. Null is allowed only where Section 6 explicitly permits it.
- Facts join `DimAirline` on `AirlineKey` only. They must not join on `AirlineId`, IATA, ICAO, or name. Historical facts are never re-keyed when an identity attribute changes.
- Orphan facts are not allowed in CURATED. They are quarantined in STAGING with a reason code. A fact `AirlineKey` that does not resolve in the selected reference version blocks refresh.
- Degenerate dimensions such as `BookingReference`, `TicketNumber`, `FlightLegID`, `CostLineID`, `DisruptionID`, and `FeedbackID` remain in the fact table. They are not separate dimension tables unless a future approved design requires one.

### 7.2 Primary Keys

| Table | Primary key | Data type | Uniqueness rule |
|---|---|---|---|
| DimDate | DateKey | Int32 | Unique `YYYYMMDD` date |
| DimAirline | AirlineKey | Int32 | Unique permanent surrogate; AirlineId is the durable business identity; IATA and ICAO are version-qualified attributes |
| DimAirport | AirportKey | Int32 | Unique surrogate; AirportCode is the business key |
| DimRoute | RouteKey | Int32 | Unique surrogate; RouteCode and directional airport pair are business keys |
| DimAircraft | AircraftKey | Int32 | Unique surrogate; AircraftRegistration is the business key |
| DimAircraftType | AircraftTypeKey | Int32 | Unique surrogate; Manufacturer plus AircraftModel is the business key |
| DimCustomer | CustomerKey | Int32 | Unique surrogate; CustomerID is the business key |
| DimFareClass | FareClassKey | Int32 | Unique surrogate; FareClassCode is the business key |
| DimBookingChannel | BookingChannelKey | Int32 | Unique surrogate; ChannelCode is the business key |
| DimDisruptionType | DisruptionTypeKey | Int32 | Unique surrogate; DisruptionCode is the business key |
| DimCurrency | CurrencyKey | Int32 | Unique surrogate; CurrencyCode is the business key |
| FactFlightOperations | FlightOperationKey | Int64 | Unique per scheduled flight leg |
| FactBookingTransactions | BookingTransactionKey | Int64 | Unique per passenger ticket coupon |
| FactOperatingCosts | OperatingCostKey | Int64 | Unique per operating-cost ledger line |
| FactDisruptions | DisruptionKey | Int64 | Unique per disruption event |
| FactCustomerFeedback | FeedbackKey | Int64 | Unique per customer feedback event |

### 7.3 Business Keys and Grain Uniqueness

| Table | Business key | Grain uniqueness test |
|---|---|---|
| DimDate | FullDate | One row per date; no duplicate date |
| DimAirline | AirlineId; AirlineIATACode within ReferenceVersion; AirlineICAOCode within ReferenceVersion; AirlineName within ReferenceVersion | No duplicate AirlineId, version-qualified IATA code, version-qualified ICAO code, or version-qualified name; exactly 10 active airlines |
| DimAirport | AirportCode | No duplicate airport code |
| DimRoute | RouteCode; OriginAirportKey plus DestinationAirportKey | No duplicate directional route |
| DimAircraft | AircraftRegistration | No duplicate registration |
| DimAircraftType | Manufacturer plus AircraftModel | No duplicate type |
| DimCustomer | CustomerID | No duplicate customer |
| DimFareClass | FareClassCode | No duplicate fare class |
| DimBookingChannel | ChannelCode; ChannelName | No duplicate channel |
| DimDisruptionType | DisruptionCode; DisruptionName | No duplicate disruption type |
| DimCurrency | CurrencyCode | No duplicate currency; exactly one USD |
| FactFlightOperations | FlightLegID; AirlineKey plus FlightNumber plus ScheduledDepartureDateKey plus RouteKey plus ScheduledDepartureTimestampUTC | No duplicate scheduled leg |
| FactBookingTransactions | BookingReference plus TicketNumber plus TicketCouponNumber | No duplicate coupon |
| FactOperatingCosts | CostLineID; FlightOperationKey plus CostCategory plus CostSubcategory plus CostDateKey plus SourceDocumentNumber | No duplicate ledger line |
| FactDisruptions | DisruptionID; FlightOperationKey plus EventSequence | DisruptionID globally unique; FlightOperationKey plus EventSequence independently unique within each flight |
| FactCustomerFeedback | FeedbackID | No duplicate feedback event |

### 7.4 Foreign Keys

| Table | Foreign key | References | Null allowed | Rule |
|---|---|---|---|---|
| DimRoute | OriginAirportKey | DimAirport.AirportKey | No | Origin airport must exist and differ from destination |
| DimRoute | DestinationAirportKey | DimAirport.AirportKey | No | Destination airport must exist and differ from origin |
| DimAircraft | AirlineKey | DimAirline.AirlineKey | No | Operator airline must exist |
| DimAircraft | AircraftTypeKey | DimAircraftType.AircraftTypeKey | No | Type must exist |
| FactFlightOperations | AirlineKey | DimAirline.AirlineKey | No | Operating airline must exist |
| FactFlightOperations | RouteKey | DimRoute.RouteKey | No | Route must exist and agree with airports |
| FactFlightOperations | AircraftKey | DimAircraft.AircraftKey | Yes | Null only when no aircraft was assigned before cancellation |
| FactFlightOperations | ScheduledDepartureDateKey | DimDate.DateKey | No | Local origin date must exist |
| FactFlightOperations | ScheduledArrivalDateKey | DimDate.DateKey | No | Local destination date must exist |
| FactBookingTransactions | CustomerKey | DimCustomer.CustomerKey | No | Customer must exist |
| FactBookingTransactions | AirlineKey | DimAirline.AirlineKey | No | Operating airline of the coupon must exist |
| FactBookingTransactions | FlightOperationKey | FactFlightOperations.FlightOperationKey | No | Coupon must resolve to a flight leg |
| FactBookingTransactions | RouteKey | DimRoute.RouteKey | No | Must agree with the flight leg |
| FactBookingTransactions | FareClassKey | DimFareClass.FareClassKey | No | Fare class must exist |
| FactBookingTransactions | BookingChannelKey | DimBookingChannel.BookingChannelKey | No | Channel must exist |
| FactBookingTransactions | BookingDateKey | DimDate.DateKey | No | Booking date must exist |
| FactBookingTransactions | TravelDateKey | DimDate.DateKey | No | Travel date must exist |
| FactBookingTransactions | TransactionCurrencyKey | DimCurrency.CurrencyKey | No | Currency must exist and have an approved rate |
| FactOperatingCosts | FlightOperationKey | FactFlightOperations.FlightOperationKey | No | Cost must resolve to a flight leg |
| FactOperatingCosts | AirlineKey | DimAirline.AirlineKey | No | Airline must exist |
| FactOperatingCosts | RouteKey | DimRoute.RouteKey | No | Must agree with the flight leg |
| FactOperatingCosts | CostDateKey | DimDate.DateKey | No | Cost date must exist |
| FactOperatingCosts | CurrencyKey | DimCurrency.CurrencyKey | No | Currency must exist and have an approved rate |
| FactDisruptions | FlightOperationKey | FactFlightOperations.FlightOperationKey | No | Event must resolve to a flight leg |
| FactDisruptions | AirlineKey | DimAirline.AirlineKey | No | Airline must exist |
| FactDisruptions | RouteKey | DimRoute.RouteKey | No | Must agree with the flight leg |
| FactDisruptions | EventLocationAirportKey | DimAirport.AirportKey | No | Origin by default; destination only when explicitly identified by the source; must agree with the referenced flight route |
| FactDisruptions | DisruptionTypeKey | DimDisruptionType.DisruptionTypeKey | No | Type must exist |
| FactDisruptions | EventDateKey | DimDate.DateKey | No | Event date must exist |
| FactCustomerFeedback | CustomerKey | DimCustomer.CustomerKey | No | Customer must exist |
| FactCustomerFeedback | AirlineKey | DimAirline.AirlineKey | No | Airline must exist |
| FactCustomerFeedback | FlightOperationKey | FactFlightOperations.FlightOperationKey | No | Feedback must resolve to a flight leg |
| FactCustomerFeedback | RouteKey | DimRoute.RouteKey | No | Must agree with the flight leg |
| FactCustomerFeedback | FeedbackDateKey | DimDate.DateKey | No | Feedback date must exist |
| FactCustomerFeedback | ResolutionDateKey | DimDate.DateKey | Yes | Required when ResolutionStatus is Resolved; must be on or after feedback date |

### 7.5 Referential-Integrity Rules

- Required dimension foreign keys must have a matching dimension row. Logical fact references must have a matching fact row. A missing match is a high-severity defect.
- Optional foreign keys may be null only for the documented reason. A non-null optional key must resolve.
- A fact's denormalized `RouteKey` must equal the route of its `FlightOperationKey`. The same rule applies to `AirlineKey` unless a codeshare rule is approved.
- A route's origin and destination must resolve to different active airports.
- A disruption EventLocationAirportKey must resolve to DimAirport and equal the referenced flight route origin by default, or its destination only when explicitly identified by the source. Intermediate and en-route locations must be quarantined under the proposed baseline.
- A disruption EventDateKey must equal the DimDate key for the local calendar date obtained by converting EventStartTimestampUTC using EventLocationAirportKey's TimeZoneIANA. The generation manifest must record the time-zone database version used.
- An aircraft's airline and type must resolve. A flight's aircraft must belong to the operating airline unless a documented lease or interchange rule applies.
- A booking's travel date must equal the flight's scheduled departure date in the origin time zone. A mismatch is a data-quality exception.
- A feedback event's flight must exist, and the feedback date must not precede the flight's scheduled departure date by more than a documented pre-travel window.
- No fact may reference a dimension member that is inactive at the event date unless historical reporting explicitly permits it.
- Referential tests must report counts by fact, key, and reason code. A zero orphan count must be evidenced, not assumed.

**Fact-reference rule:** `FlightOperationKey` in FactBookingTransactions, FactOperatingCosts, FactDisruptions, and FactCustomerFeedback is a logical fact reference for lineage and row-level reconciliation. It must not be modeled as a Power BI relationship between facts. Flight attributes are filtered through shared dimensions.

**Aircraft airline rule:** DimAircraft.AirlineKey is a physical foreign key for lineage and validation. It is not an active semantic relationship, because DimAirline also filters FactFlightOperations directly. Fleet-by-airline analysis uses a role-playing airline dimension or an approved measure; it must not activate a second filter path.

## 8. Relationships and Semantic Model Considerations

### 8.1 Star-Schema Principles

- Dimensions filter facts. Facts do not filter dimensions. The default filter direction is single, from the one-side dimension to the many-side fact.
- Every relationship is one-to-many (`1:*`) in the physical model. Many-to-many and bidirectional relationships are prohibited in the baseline.
- No fact-to-fact relationships. Cross-fact analysis uses shared conformed dimensions and separate measures.
- No circular filter paths and no ambiguous filter paths. Role-playing dimensions must be explicit.
- The model uses surrogate integer keys. Business keys are available for labels and validation but are not relationship keys.
- The model uses the CURATED tables in Section 6. It does not import RAW or STAGING.
- Ratios are measures, not stored additive columns. Additive amounts remain at fact grain.

### 8.2 Relationship Matrix

| From | To | Key | Cardinality | Filter direction | Status | Notes |
|---|---|---|---|---|---|---|
| DimDate | FactFlightOperations | ScheduledDepartureDateKey | 1:* | Single | Active | Primary flight date role |
| DimDate | FactFlightOperations | ScheduledArrivalDateKey | 1:* | Single | Inactive | Arrival date role; use USERELATIONSHIP |
| DimDate | FactBookingTransactions | TravelDateKey | 1:* | Single | Active | Travel-date revenue and demand analysis |
| DimDate | FactBookingTransactions | BookingDateKey | 1:* | Single | Inactive | Booking-date cohort analysis |
| DimDate | FactOperatingCosts | CostDateKey | 1:* | Single | Active | Cost accounting date |
| DimDate | FactDisruptions | EventDateKey | 1:* | Single | Active | Disruption event date |
| DimDate | FactCustomerFeedback | FeedbackDateKey | 1:* | Single | Active | Feedback submission date |
| DimDate | FactCustomerFeedback | ResolutionDateKey | 1:* | Single | Inactive | Resolution-date analysis |
| DimAirline | FactFlightOperations | AirlineKey | 1:* | Single | Active | Operating airline |
| DimAirline | FactBookingTransactions | AirlineKey | 1:* | Single | Active | Operating airline of the coupon |
| DimAirline | FactOperatingCosts | AirlineKey | 1:* | Single | Active | Cost-bearing airline |
| DimAirline | FactDisruptions | AirlineKey | 1:* | Single | Active | Disrupted airline |
| DimAirline | FactCustomerFeedback | AirlineKey | 1:* | Single | Active | Feedback airline |
| DimRoute | FactFlightOperations | RouteKey | 1:* | Single | Active | Directional route |
| DimRoute | FactBookingTransactions | RouteKey | 1:* | Single | Active | Booked route |
| DimRoute | FactOperatingCosts | RouteKey | 1:* | Single | Active | Costed route |
| DimRoute | FactDisruptions | RouteKey | 1:* | Single | Active | Disrupted route |
| DimRoute | FactCustomerFeedback | RouteKey | 1:* | Single | Active | Feedback route |
| DimAircraft | FactFlightOperations | AircraftKey | 1:* | Single | Active | Operating aircraft |
| DimAircraftType | DimAircraft | AircraftTypeKey | 1:* | Single | Active | Snowflake dimension |
| DimAirport - Origin role | DimRoute | OriginAirportKey | 1:* | Single | Active | Role-playing airport |
| DimAirport - Destination role | DimRoute | DestinationAirportKey | 1:* | Single | Active | Role-playing airport |
| DimAirport - Event Location role | FactDisruptions | EventLocationAirportKey | 1:* | Single | Active | Direct event-location role; not related to DimRoute |
| DimCustomer | FactBookingTransactions | CustomerKey | 1:* | Single | Active | Booking customer |
| DimCustomer | FactCustomerFeedback | CustomerKey | 1:* | Single | Active | Feedback customer |
| DimFareClass | FactBookingTransactions | FareClassKey | 1:* | Single | Active | Fare class |
| DimBookingChannel | FactBookingTransactions | BookingChannelKey | 1:* | Single | Active | Booking channel |
| DimDisruptionType | FactDisruptions | DisruptionTypeKey | 1:* | Single | Active | Disruption cause |
| DimCurrency | FactBookingTransactions | TransactionCurrencyKey | 1:* | Single | Active | Original transaction currency |
| DimCurrency | FactOperatingCosts | CurrencyKey | 1:* | Single | Active | Original cost currency |
| DimAirline | DimAircraft | AirlineKey | 1:* | Single | Not active | Retained for lineage; use a fleet role copy if needed |

### 8.3 Role-Playing Dimensions

**Dates.** One physical DimDate supports all date roles. Each fact has exactly one active DimDate relationship. Secondary date roles are inactive and are activated in measures with `USERELATIONSHIP`. The active date role is the default reporting date for that fact.

| Fact | Active date role | Inactive date roles |
|---|---|---|
| FactFlightOperations | ScheduledDepartureDateKey | ScheduledArrivalDateKey |
| FactBookingTransactions | TravelDateKey | BookingDateKey |
| FactOperatingCosts | CostDateKey | None |
| FactDisruptions | EventDateKey | None |
| FactCustomerFeedback | FeedbackDateKey | ResolutionDateKey |

**Airports.** The physical DimAirport is used for three explicit semantic roles: `DimAirport - Origin` and `DimAirport - Destination` each have one active relationship to DimRoute, while `DimAirport - Event Location` has one active relationship directly to FactDisruptions through EventLocationAirportKey. The event-location role must not relate to DimRoute. These separate role-playing dimensions avoid inactive relationships and ambiguous filter paths.

**Airlines for fleet analysis.** DimAirline does not have an active relationship to DimAircraft, because DimAirline also filters FactFlightOperations directly. Activating both paths would create an ambiguous filter path. If fleet counts by airline are required, create a role-playing `DimAirline - Fleet` dimension related to DimAircraft, or use a documented measure that transfers the airline filter with `TREATAS`. The baseline does not require this role.

### 8.4 Semantic-Model Rules

- Mark DimDate as the model date table using FullDate. Disable Power BI Auto date/time for all tables.
- Hide all surrogate keys from report view. Keep business keys and names visible. Specifically hide `DimAirline.AirlineKey` and `DimAirline.ReferenceVersion`; `AirlineId` may remain visible only as a non-slicer lineage attribute. `DimAirline.ReferenceVersion` is technical lineage, not approval.
- Set key columns to Do Not Summarize. Set numeric additive columns to Sum only when they are true measures.
- `DimAirline` must not have an active relationship to `DimAircraft`, because it already filters `FactFlightOperations` directly. Fleet-by-airline analysis uses a role-playing `DimAirline - Fleet` dimension or a documented `TREATAS` measure; never activate a second ambiguous filter path.
- The Power BI model exposes `SelectedReferenceVersion` as a parameter and validates it against the approved manifest and `DimAirline.ReferenceVersion`. A mismatch blocks refresh. Mixed reference versions are prohibited.
- Every report page must show the exact unconditional disclosure `Synthetic Simulation — Not Actual Airline Performance` in a persistent footer or header; every tooltip while a page is visible and every exported report result must carry it. No “where practical” exception.
- Sort MonthName by MonthNumber, DayName by DayOfWeekNumber, and YearMonth by YearMonthSort. Do not sort a numeric fiscal column by itself; use the fiscal month number as the sort key for any fiscal month label that is added later.
- Set data categories for Country, City, Latitude, and Longitude on DimAirport. Set TimeZoneIANA as a descriptive attribute, not a date/time category.
- Store timestamps as DateTime and dates as Date. Do not store dates as text.
- Do not create calculated columns that duplicate fact measures. Prefer explicit measures over calculated columns for ratios.
- Do not use bidirectional cross-filtering. If a visual appears to require it, review the model instead of enabling it.
- Do not create many-to-many relationships. If a business many-to-many is required, use a bridge table with an approved design and test plan.
- Do not relate facts to facts. If a report needs flight, booking, cost, disruption, and feedback data together, use shared dimensions and separate measures.
- Do not convert currency in DAX. Use the USD columns in the facts. DimCurrency is for original-currency analysis and validation.
- Do not aggregate origin-currency amounts across currencies. Always filter to one currency or use USD.
- Use DIVIDE for every ratio. Return BLANK for a zero or missing denominator unless a page explicitly requires zero.
- Keep additive measures at their native grain. Do not sum a ratio across airlines, routes, or months.
- Use `USERELATIONSHIP` only for documented date roles. Do not use it to bypass a missing relationship.
- Use `TREATAS` only for an approved role-playing or bridge design. Document the measure and test it.
- If row-level security is added later, secure DimAirline and test all five pages. RLS is not part of the baseline.
- Hide technical columns such as staging metadata and load timestamps from report view.
- `ref_aircraft_availability.csv` is a supporting reference table for K-13 only. When imported, it relates to DimAircraft and DimDate. It is not a financial fact and must not be joined to FactFlightOperations in a way that multiplies flight rows.

### 8.5 Page-to-Data Mapping

| Report page | Primary facts | Primary dimensions | Core KPIs |
|---|---|---|---|
| Executive Overview | All five facts | DimDate, DimAirline, DimRoute | ASK, RPK, Load Factor, Total RASK, CASK, Unit Contribution, OTP, Cancellation Rate |
| Network & Capacity Intelligence | FactFlightOperations, FactBookingTransactions, FactOperatingCosts | DimRoute, DimAirport roles, DimAircraft, DimDate | ASK, RPK, Load Factor, Route Contribution, Aircraft Utilization |
| Revenue & Yield Intelligence | FactBookingTransactions, FactOperatingCosts, FactFlightOperations | DimFareClass, DimBookingChannel, DimCustomer, DimRoute, DimDate | Passenger Yield, Passenger RASK, Total RASK, CASK, Unit Contribution, Average Passenger Revenue, Ancillary Revenue per Passenger, Booking Lead Time |
| Operations & Disruption | FactFlightOperations, FactDisruptions | DimAirline, DimRoute, DimAircraft, DimDisruptionType, DimDate | OTP, Cancellation Rate, Completion Rate, Average Delay, Aircraft Utilization, Reactionary Delay Share |
| Customer & Service Intelligence | FactBookingTransactions, FactCustomerFeedback, FactFlightOperations | DimCustomer, DimFareClass, DimBookingChannel, DimRoute, DimDate | Satisfaction, Complaint Rate, Refund Rate, Repeat Booking Rate, Service Recovery Rate, Ancillary Revenue per Passenger |

**Page-mapping rule:** every visual must trace to at least one fact and its conformed dimensions. A visual that cannot be traced is either out of scope or requires a documented model change.

## 9. Date and Time-Zone Policy

### 9.1 Core Rules

- Store canonical operational timestamps in UTC using ISO 8601 `YYYY-MM-DDThh:mm:ssZ`.
- Store local operational dates as date keys derived from the relevant airport's IANA time zone. Do not store local timestamps as text.
- Preserve the IANA time-zone identifier on DimAirport. Do not use abbreviations such as EST, PST, or CST because they are ambiguous and do not handle daylight saving.
- Apply the IANA time-zone database version recorded in the generation manifest. A time-zone database change that affects historical dates requires a reconciliation note.
- Calculate delays in absolute minutes from UTC timestamps. Do not subtract formatted local clock times.
- Support overnight flights: the arrival date key may be later than the departure date key.
- Support cross-time-zone flights: the departure and arrival local dates must be derived independently.
- Keep scheduled timestamps on cancelled flights. Actual timestamps are null.
- Do not infer a missing timestamp from another timestamp unless the derivation rule is documented and tested.
- Do not use locale-specific date formats such as `MM/DD/YYYY` in curated data.
- `DimAirline.StatusEffectiveDate` is an attribute date, not a `DimDate` role. It records when an inactive status took effect and does not create a fact-date relationship.

### 9.2 Date-Key Semantics

| Date key | Meaning | Time-zone basis |
|---|---|---|
| ScheduledDepartureDateKey | Calendar date of scheduled departure | Local date at origin airport |
| ScheduledArrivalDateKey | Calendar date of scheduled arrival | Local date at destination airport |
| BookingDateKey | Calendar date of booking transaction | UTC date |
| TravelDateKey | Calendar date of coupon travel | Local date at coupon origin airport |
| CostDateKey | Accounting date of cost ledger line | Airline reporting calendar; UTC date in the synthetic baseline |
| EventDateKey | Calendar date of disruption event | Local date at the event location; baseline uses flight origin unless destination is explicit |
| FeedbackDateKey | Calendar date of feedback submission | UTC date |
| ResolutionDateKey | Calendar date of feedback resolution | UTC date |

**Booking lead time.** `BookingLeadTimeDays` is the calendar-date difference between the travel date and the booking date, in whole days. Because the booking date is a UTC date and the travel date is a local date, a booking near midnight may show a one-day difference from a local-clock calculation. This is a documented limitation of the baseline, not a data error. The KPI must use the stored integer, not a re-derivation from timestamps.

### 9.3 Flight Date and Delay Rules

- `ScheduledDepartureTimestampUTC` and `ScheduledArrivalTimestampUTC` are the scheduled UTC instants.
- `ActualDepartureTimestampUTC` and `ActualArrivalTimestampUTC` are the actual UTC instants for operated flights.
- `DepartureDelayMinutes = (ActualDepartureTimestampUTC - ScheduledDepartureTimestampUTC)` in whole minutes, rounded half away from zero.
- `ArrivalDelayMinutes = (ActualArrivalTimestampUTC - ScheduledArrivalTimestampUTC)` in whole minutes, rounded half away from zero.
- `BlockMinutes = (ActualArrivalTimestampUTC - ActualDepartureTimestampUTC)` in whole minutes.
- Negative delay values mean early departure or arrival. They are valid and must not be converted to zero.
- For cancelled flights, all actual timestamps and delay minutes are null.
- `OnTimeFlag` uses departure delay less than or equal to 15 minutes. `OnTimeArrivalFlag` uses arrival delay less than or equal to 15 minutes. Early flights are on time.
The 15-minute threshold is the proposed baseline under OD-09; formal owner approval remains required.

### 9.4 Reporting-Period Rules

The primary reporting period is 2025-10-01 through 2026-09-30, inclusive. Each measure must state which date role it uses.

| Measure family | Default date role |
|---|---|
| Flight capacity, traffic, load factor, OTP, cancellation, completion | ScheduledDepartureDateKey |
| Revenue, yield, RASK, fare mix, booking channel | TravelDateKey by default; BookingDateKey for booking cohorts |
| Operating cost, CASK, contribution | CostDateKey |
| Disruption, delay cause, reactionary share | EventDateKey |
| Satisfaction, complaints, service recovery | FeedbackDateKey |
| Refund rate | BookingDateKey unless a page explicitly uses travel date |
| Repeat booking rate | BookingDateKey |
| Booking lead time | BookingDateKey |

**Period-boundary rule:** a flight that departs on 2026-09-30 and arrives on 2026-10-01 belongs to the reporting period by departure date. Its arrival date is outside the period but remains in DimDate. A booking made before 2025-10-01 for travel inside the period is included in travel-date measures but excluded from booking-date period measures. The measure definition must state which basis is used.

**Travel-snapshot rule:** FactBookingTransactions includes coupons with TravelDateKey from 2025-10-01 through 2026-09-30. BookingDateKey may precede the period. Bookings for travel after 2026-09-30 are out of scope for the baseline and must not create a DimDate orphan.

### 9.5 DimDate Coverage and Fiscal Calendar

- DimDate covers 2024-10-01 through 2026-10-31 inclusive.
- `IsReportingPeriod = TRUE` for 2025-10-01 through 2026-09-30 only.
- The pre-period dates provide BookingDateKey coverage beginning 2024-10-01. The post-period dates support prior-period comparison and overnight arrivals at the end of the reporting period. This calendar range does not establish a maximum booking lead time. Booking dates before 2024-10-01 are outside the current DimDate coverage and require an explicit scope decision.
- Fiscal year starts on 01 October. FY2026 covers 2025-10-01 through 2026-09-30.
- Fiscal quarters: Q1 October-December, Q2 January-March, Q3 April-June, Q4 July-September.
- `FiscalMonthNumber` runs 1 through 12 from October to September.
- Calendar year, calendar quarter, calendar month, ISO week, and fiscal period are all available. Reports must label which one they use.

### 9.6 Time-Zone Validation

- Every airport must have a valid IANA identifier that resolves in the recorded time-zone database.
- The conversion from UTC to a local date must be tested for at least one daylight-saving transition in each affected region.
- A cross-time-zone flight must be tested where the departure and arrival local dates differ from the UTC dates.
- An overnight flight must be tested where the arrival date key is one day after the departure date key.
- A cancelled flight must be tested to confirm that scheduled date keys remain populated and actual timestamps remain null.
- The time-zone database version and test cases must be recorded in `qa/results/`.

## 10. Currency and Financial Policy

### 10.1 Reporting Currency

- USD is the only reporting currency.
- All financial KPIs in Section 11 are calculated from USD columns.
- Original transaction currency and original amount are preserved for audit and currency-mix analysis.
- Amounts in different currencies must never be summed before conversion.
- Currency conversion must not be performed in a Power BI visual or a DAX measure. It is performed once in STAGING/CURATED using the approved rate and stored in the fact's USD columns.

### 10.2 Exchange-Rate Contract

`ref_exchange_rates.csv` has one row per currency per rate date.

| Column | Data type | Null | Definition |
|---|---|---|---|
| CurrencyCode | String(3) | No | ISO 4217 code; foreign key to DimCurrency |
| RateDate | Date | No | Effective date of the rate |
| ExchangeRateToUSD | Decimal(18,6) | No | USD per one unit of the currency; positive |
| RateSource | String(50) | No | Synthetic source identifier |
| IsSynthetic | Boolean | No | True for all baseline rates |
| RateVersion | String(20) | No | Reference version |

**Conversion formula:** `AmountUSD = Amount * ExchangeRateToUSD`, rounded to two decimals at the final amount level. The rate is not rounded before multiplication.

**Rate-date rule:** use the transaction date for bookings and the cost date for costs. A period-average rate is not allowed unless it is explicitly approved and labeled. The rate must exist for the exact date. The baseline does not use forward-filling. If forward-filling is approved later, it must have a documented maximum gap and an `IsCarriedForward` flag.

**Rate plausibility:** synthetic rates must be positive, stable enough to avoid absurd conversions, and documented as fictional. They must not be copied from a live market feed or presented as real exchange rates.

This is the proposed OD-04 design baseline and remains subject to formal owner approval. The synthetic rate regime, base currency, volatility, and exact-date coverage are defined as USD-per-one-unit rates at six decimals. Rate generation is deferred to the data generator.

### 10.3 Revenue Definitions

| Measure | Definition | Included | Excluded |
|---|---|---|---|
| Passenger revenue | Net base fare | Base fare minus discount minus passenger refund | Taxes, fees, ancillary, non-revenue tickets, Booked, cancelled, and no-show coupons |
| Fee revenue | Carrier-retained fees and charges | Fee amount minus fee refund plus cancellation fee plus no-show fee | Taxes, pass-through charges, ancillary services |
| Ancillary revenue | Optional service revenue | Ancillary amount minus ancillary refund | Taxes, mandatory fees, passenger fare |
| Total operating revenue | Passenger plus fee plus ancillary revenue | All three airline-retained revenue streams | Taxes, pass-through amounts, non-operating income, FX gains |
| Operating cost | Cost ledger total | Fuel, crew, maintenance, airport charges, navigation, sales and distribution, overhead, other | Non-operating costs, interest, tax, impairments, FX gains and losses |

**Passenger revenue rule:** passenger revenue is the net base fare. It excludes taxes, fees, and ancillary revenue, and is net of refunds. A Booked, cancelled, or no-show coupon contributes zero passenger revenue; any retained amount is fee revenue. This is a proposed design baseline and remains subject to formal owner approval.

**Tax rule:** `TaxUSD` is a pass-through amount. It is not airline revenue and must not appear in passenger revenue, total operating revenue, RASK, or yield.

This is a proposed design baseline and remains subject to formal owner approval.

**Ancillary rule:** ancillary revenue is separate from passenger revenue and is included in total operating revenue and ancillary revenue per passenger. It is not included in passenger yield or passenger RASK.

### 10.4 Sign Conventions

| Item | Sign in the fact | Effect in measures |
|---|---|---|
| Base fare | Positive | Added to passenger revenue |
| Discount | Positive magnitude | Subtracted from passenger revenue |
| Tax | Positive magnitude | Excluded from revenue |
| Fee | Positive magnitude | Added to fee revenue |
| Ancillary revenue | Positive magnitude | Added to ancillary revenue |
| Passenger refund | Positive magnitude | Subtracted from passenger revenue |
| Ancillary refund | Positive magnitude | Subtracted from ancillary revenue |
| Fee refund | Positive magnitude | Subtracted from fee revenue |
| Cancellation fee | Positive magnitude | Added to fee revenue |
| No-show fee | Positive magnitude | Added to fee revenue |
| Operating cost | Positive expense; negative credit | Added with sign to operating cost |
| Exchange rate | Positive | Multiplied by the original amount |

**No negative-refund convention:** refunds are stored as positive magnitudes and subtracted in the measure. A negative refund value is a data-quality defect. This avoids double-negation errors.

### 10.5 Financial Identities

The following identities must hold at the coupon, booking, flight, airline, route, month, and total levels after allocation and rounding:

1. `NetPassengerRevenueUSD = BaseFareUSD - DiscountUSD - RefundUSD` for Ticketed, Flown, or Refunded coupons. Booked, Cancelled, and NoShow coupons have zero passenger revenue; retained amounts are fee revenue.
2. `NetFeeRevenueUSD = FeeUSD - FeeRefundUSD + CancellationFeeUSD + NoShowFeeUSD`
3. `NetAncillaryRevenueUSD = AncillaryRevenueUSD - AncillaryRefundUSD`
4. `TotalOperatingRevenueUSD = NetPassengerRevenueUSD + NetFeeRevenueUSD + NetAncillaryRevenueUSD`
5. `TaxUSD` is excluded from identity 4.
6. `OperatingCostUSD = SUM(FactOperatingCosts[CostAmountUSD])`
7. `UnitContributionUSD = TotalOperatingRevenueUSD - OperatingCostUSD`
8. `UnitContributionPerASK = UnitContributionUSD / ASK`

**Allocation identity:** for every booking, the sum of allocated coupon discounts, refunds, fees, ancillary revenue, cancellation fees, and no-show fees must equal the booking-level control amount after rounding. The residual is assigned to the largest coupon by base fare, with ties broken by the lowest BookingTransactionKey. This is a proposed design baseline and remains subject to formal owner approval.

### 10.6 Cancellation, Refund, and Chargeback Treatment

- A cancelled flight remains in FactFlightOperations with capacity and scheduled timestamps.
- A cancelled coupon remains in FactBookingTransactions with `TransactionStatus = Cancelled`.
- Passenger revenue on a cancelled coupon is zero.
- Refundable amounts are recorded as positive refund magnitudes and subtracted through the revenue identity.
- A non-refundable cancellation fee is recorded in `CancellationFeeUSD` and included in fee revenue.
- A no-show coupon has zero passenger revenue. Any retained non-refundable amount is recorded in `NoShowFeeUSD` and included in fee revenue. Cancellation fees and no-show fees are mutually exclusive on a coupon.
- A Booked coupon that has not been ticketed has zero recognized passenger revenue. If it later becomes Ticketed, Flown, or Refunded, the status and revenue are updated in STAGING and the change is logged.
- Chargebacks are not a separate baseline field. If chargebacks are introduced, they require a separate approved field, a sign convention, and a reconciliation test. This is a proposed design baseline and remains subject to formal owner approval.
- A refund must not be counted as negative revenue in one table and positive revenue in another. There is one refund field per revenue stream, and it is used once.

### 10.7 Duplicate-Revenue Prevention

- Revenue exists only in FactBookingTransactions. There is no second revenue fact.
- Each coupon row carries its allocated revenue exactly once.
- Measures sum fact columns; they do not multiply a fact row by a dimension row count.
- No measure may use `SUMX` over a dimension table to allocate revenue to facts.
- No relationship may fan out a booking or coupon row.
- No visual may combine a booking-level amount with a flight-level amount without reconciling grain.
- Route and airline revenue use the denormalized `RouteKey` and `AirlineKey` on the coupon, not a fact-to-fact path.
- A reconciliation test must compare coupon revenue to the booking control total and to the financial control total before any KPI is accepted.

### 10.8 Financial Reconciliation

| Reconciliation | Expected result | Tolerance |
|---|---|---|
| Coupon net passenger revenue to booking control | Equal after allocation | Proposed engineering validation threshold: 0.01 USD per booking; not owner-approved |
| Coupon total operating revenue to financial control | Passenger revenue + fee revenue (including cancellation and no-show fees) + ancillary revenue; equal by airline and month | Proposed engineering validation threshold: 0.01 USD per airline-month; not owner-approved |
| Operating cost ledger to cost control | Equal by airline and month | Proposed engineering validation threshold: 0.01 USD per airline-month; not owner-approved |
| Tax collected to tax control | Equal by currency and month | Proposed engineering validation threshold: 0.01 USD per currency-month; not owner-approved |
| Refunds to refund control | Equal by airline and month | Proposed engineering validation threshold: 0.01 USD per airline-month; not owner-approved |
| USD conversion to rate table | Equal at transaction-row level | Proposed engineering validation threshold: 0.01 USD per row; not owner-approved |
| Airline revenue plus cost to contribution control | Equal after sign rules | Proposed engineering validation threshold: 0.01 USD per airline-month; not owner-approved |

**Evidence rule:** reconciliation results must be written to `qa/results/` with the run timestamp, seed, configuration hash, row counts, control totals, differences, and pass/fail status. A verbal statement is not evidence.

## 11. KPI Definitions and Formulas

### 11.1 KPI Conventions

- All financial KPIs use USD columns. Original-currency amounts are never aggregated across currencies.
- All ratios use `DIVIDE(numerator, denominator, BLANK())` or an equivalent safe-division pattern. A zero or missing denominator returns BLANK, not zero or infinity.
- Percentages are stored as decimal fractions and formatted as percentages in Power BI. A KPI displayed as 82.4% is stored as 0.824.
- ASK and RPK are volume measures. Their components are documented even though they are not ratios.
- Capacity denominators use scheduled capacity and include cancelled flights unless a KPI explicitly states otherwise. An operated-only capacity measure must be labeled `Operated ASK` and must not be substituted silently.
- Revenue and cost measures use the definitions in Section 10. Passenger revenue excludes taxes, fees, and ancillary revenue, and is net of refunds.
- A KPI must declare its date role. The default date roles are in Section 9.4.
- A KPI that mixes facts must use shared dimensions, not a fact-to-fact relationship.
- A KPI that uses a booking-level denominator must not be multiplied by coupon or segment rows.
- A KPI that uses a flight-level denominator must not be multiplied by booking rows.
- A KPI result must be reconcilable to an independent control calculation at airline, route, month, and total level.
- The initial on-time threshold is 15 minutes. The initial satisfaction scale is 1 through 5. Both remain open decisions.

### 11.2 Capacity and Economics KPIs

| ID | KPI | Business meaning | Formula | Numerator or components | Denominator or components | Exclusions and rules |
|---|---|---|---|---|---|---|
| K-01 | ASK | Available seat kilometres: scheduled capacity offered | `SUM(AvailableSeats * FlightDistanceKM)` | Available seats multiplied by scheduled flight distance for every scheduled leg | Not applicable; volume measure | Includes cancelled flights. Excludes duplicate legs, non-scheduled rows, and zero-distance rows. An operated-only variant must be labeled `Operated ASK`. |
| K-02 | RPK | Revenue passenger kilometres: passenger traffic carried | `SUM(RevenuePassengers * FlightDistanceKM)` | Revenue passengers multiplied by scheduled flight distance | Not applicable; volume measure | Excludes non-revenue passengers and cancelled flights. Cancelled flights contribute zero RPK. A revenue passenger on a cancelled leg must not be counted. |
| K-03 | Load Factor | Percentage of scheduled capacity used by revenue traffic | `RPK / ASK` | RPK | ASK, including cancelled flights | Non-revenue passengers excluded. Cancelled capacity remains in ASK. Zero ASK returns BLANK. Do not use operated ASK unless the measure is explicitly labeled. |
| K-04 | Passenger Yield | Passenger revenue per revenue passenger kilometre | `NetPassengerRevenueUSD / RPK` | Net passenger revenue in USD | RPK | Excludes taxes, fees, ancillary revenue, non-revenue passengers, and cancelled or no-show coupon passenger revenue. Refunds are netted. Zero RPK returns BLANK. |
| K-05 | Passenger RASK | Passenger revenue per available seat kilometre | `NetPassengerRevenueUSD / ASK` | Net passenger revenue in USD | ASK, including cancelled flights | Excludes taxes, fees, ancillary revenue, and non-revenue passengers. Refunds are netted. Zero ASK returns BLANK. |
| K-06 | Total RASK | Total airline-retained operating revenue per available seat kilometre | `TotalOperatingRevenueUSD / ASK` | Net passenger revenue plus net fee revenue plus net ancillary revenue | ASK, including cancelled flights | Excludes taxes, pass-through amounts, non-operating income, and FX gains. Zero ASK returns BLANK. |
| K-07 | CASK | Operating cost per available seat kilometre | `OperatingCostUSD / ASK` | Sum of operating-cost ledger lines in USD | ASK, including cancelled flights | Includes fuel, crew, maintenance, airport charges, navigation, sales and distribution, overhead, and other operating costs. Excludes non-operating costs, interest, tax, impairments, and FX gains or losses. Zero ASK returns BLANK. |
| K-08 | Unit Contribution | Operating contribution per available seat kilometre | `(TotalOperatingRevenueUSD - OperatingCostUSD) / ASK`, equivalent to `Total RASK - CASK` | Total operating revenue minus operating cost | ASK, including cancelled flights | Uses the same revenue and cost definitions as K-06 and K-07. Excludes non-operating items. A negative result is valid. Zero ASK returns BLANK. |

This is a proposed design baseline and remains subject to formal owner approval.

**Yield and RASK rule:** passenger yield, passenger RASK, total RASK, CASK, and unit contribution must be calculated from USD columns. They must not be calculated from a mix of currencies or from a booking-level amount repeated across flight rows.

**ASK and RPK materialization rule:** if `AvailableSeatKM` or `RevenuePassengerKM` is materialized in CURATED, it must equal the row-level expression exactly and must be validated against the measure. Materialization does not change the definition.

### 11.3 Operational KPIs

| ID | KPI | Business meaning | Formula | Numerator or components | Denominator or components | Exclusions and rules |
|---|---|---|---|---|---|---|
| K-09 | On-Time Performance (OTP) | Percentage of operated departures within the on-time threshold | `OnTimeDepartures / OperatedFlightsWithValidDeparture` | Count of operated flights with `OnTimeFlag = TRUE` | Count of operated flights with a non-null departure delay | Cancelled flights are excluded from the OTP denominator and reported through cancellation rate. Early departures count as on time. The threshold is 15 minutes; OD-09. The arrival variant uses `OnTimeArrivalFlag` and operated flights with a valid arrival delay. |
| K-10 | Cancellation Rate | Percentage of scheduled flights that were cancelled | `CancelledFlights / ScheduledFlights` | Count of flights with `CancellationFlag = TRUE` | Count of all scheduled flight legs, including cancelled | The denominator includes cancelled flights. Do not exclude cancelled flights from the denominator. Excludes duplicate legs. Zero scheduled flights returns BLANK. |
| K-11 | Completion Rate | Percentage of scheduled flights that were operated | `OperatedFlights / ScheduledFlights` | Count of flights with `CompletionFlag = TRUE` | Count of all scheduled flight legs, including cancelled | Cancelled flights are failures to complete and remain in the denominator. In the baseline, completion rate plus cancellation rate equals 1. Zero scheduled flights returns BLANK. |
| K-12 | Average Delay | Average arrival delay per operated flight with a valid arrival delay | `SUM(ArrivalDelayMinutes) / OperatedFlightsWithValidArrival` | Sum of arrival delay minutes for eligible operated flights | Count of operated flights with a non-null arrival delay | Cancelled flights are excluded from the delay average and reported separately. Early arrivals produce negative delay and remain in the average. The departure-delay variant uses `DepartureDelayMinutes`. Zero eligible flights returns BLANK. |
| K-13 | Aircraft Utilization | Operating block hours per available aircraft hour | `OperatingBlockHours / AvailableAircraftHours` | Sum of `BlockMinutes` divided by 60 for operated flights | Sum of `AvailableHours` from `ref_aircraft_availability.csv` for records with `AvailabilityStatus = Available`, for active aircraft-days in scope and the single selected `ReferenceVersion` | Only `Available` records contribute to the denominator. `Maintenance`, `Stored`, `Retired`, and `No Planned Availability` records are excluded. Cancelled flights are excluded from operating block hours. The proposed 14.00 available hours per active aircraft-day remains subject to OD-10 owner approval. Zero available hours returns BLANK. |

**OTP basis rule:** the primary OTP is departure OTP. Arrival OTP is a supporting metric, not a substitute. A report must label which basis it displays. Cancelled flights are not counted as on time or as operated; they are counted in the cancellation rate.

**Delay rule:** average delay is not the same as delay minutes per operated flight. Average delay uses only flights with a valid delay value. Delay minutes per operated flight uses all operated flights in the denominator and is documented in Section 11.5.

**Utilization rule:** `ref_aircraft_availability.csv` is a supporting reference table with one row per `AircraftKey`, `CalendarDateKey`, and `ReferenceVersion`. The semantic model must use exactly one explicitly selected reference version. It is modeled with relationships to `DimAircraft` and `DimDate` for the utilization measure. Only records with `AvailabilityStatus = Available` contribute their `AvailableHours` to the denominator. Records with `Maintenance`, `Stored`, `Retired`, or `No Planned Availability` status are excluded. It is not a revenue or cost fact. Operating block hours come only from `FactFlightOperations` and must not be double-counted with scheduled block hours.

### 11.4 Commercial and Customer KPIs

| ID | KPI | Business meaning | Formula | Numerator or components | Denominator or components | Exclusions and rules |
|---|---|---|---|---|---|---|
| K-14 | Average Passenger Revenue | Average net passenger revenue per revenue passenger | `NetPassengerRevenueUSD / RevenuePassengers` | Net passenger revenue in USD | Revenue passengers carried | Excludes non-revenue passengers, taxes, fees, ancillary revenue, and cancelled or no-show coupon passenger revenue. Refunds are netted. Zero revenue passengers returns BLANK. |
| K-15 | Ancillary Revenue per Passenger | Average net ancillary revenue per revenue passenger | `NetAncillaryRevenueUSD / RevenuePassengers` | Net ancillary revenue in USD | Revenue passengers carried | Excludes non-revenue passengers, taxes, fees, and passenger fare. Ancillary refunds are netted. Zero revenue passengers returns BLANK. |
| K-16 | Booking Lead Time | Average days between booking and travel | `SUM(EligibleBookingLeadTimeDays) / EligibleBookings` | Sum of lead-time days for one row per eligible BookingReference | Count of eligible bookings | Calculated at booking level, not coupon level, to avoid segment weighting. Negative lead times are excluded and reported as defects. Cancelled and fully refunded bookings are excluded in the baseline. Eligible booking is at least one ticketed or flown coupon; fully refunded means all passenger coupons have a refund greater than zero. This is OD-18. Booking date must be in the reporting period. |
| K-17 | Refund Rate | Share of eligible ticket coupons that were refunded | `RefundedEligibleCoupons / EligibleCoupons` | Count of eligible ticketed revenue coupons with `IsRefunded = TRUE` | Count of eligible ticketed revenue coupons issued in the period | Excludes non-revenue coupons, duplicate coupons, unticketed bookings, and coupons outside the booking-date period. Uses BookingDateKey. A refunded coupon remains in the denominator. Zero eligible coupons returns BLANK. |
| K-18 | Period Complaint Rate | Complaints received during the period per 1,000 revenue passengers carried during the period | `(ComplaintEvents / RevenuePassengers) * 1000` | Count of feedback events with `FeedbackType = Complaint` | Revenue passengers carried in the same period | Excludes compliments, surveys, and claims. Duplicate feedback events are removed. Period-level ratio: complaint numerator uses FeedbackDateKey and passenger denominator uses ScheduledDepartureDateKey within the same period. Zero passengers returns BLANK. |
| K-19 | Satisfaction | Average valid customer satisfaction score | `SUM(ValidSatisfactionScore) / Count(ValidSatisfactionScore)` | Sum of valid scores | Count of valid scores | Scale is 1 through 5. Null scores, out-of-range scores, and non-score feedback are excluded. Report the response count with the average so a small base is visible. This is OD-11. Zero valid responses returns BLANK. |
| K-20 | Repeat Booking Rate | Share of customers with two or more eligible bookings | `CustomersWithTwoOrMoreBookings / CustomersWithAtLeastOneBooking` | Distinct customers with at least two distinct eligible BookingReferences in the period | Distinct customers with at least one eligible BookingReference in the period | Eligible bookings use BookingDateKey in the period and exclude cancelled and fully refunded bookings in the baseline. A booking is eligible if it contains at least one ticketed or flown coupon and is not fully refunded. Multiple coupons on one booking count once. This is OD-18. Zero eligible customers returns BLANK. |
| K-21 | Service Recovery Rate | Share of eligible service cases that were resolved | `RecoveredEligibleCases / EligibleServiceCases` | Complaints with `ResolutionStatus = Resolved` | Complaints with `ServiceRecoveryFlag = TRUE` | Excludes surveys, compliments, and claims. A case is eligible only when service recovery was triggered. Resolution must have a valid ResolutionDateKey on or after FeedbackDateKey. This is OD-17. Zero eligible cases returns BLANK. |

**Customer-rate rule:** complaint rate, satisfaction, repeat booking rate, refund rate, and service recovery rate must state their denominator population and date basis. A rate with a different denominator is a different KPI and must not reuse the same measure name.

**Booking-level rule:** booking lead time and repeat booking rate use one row per BookingReference. Summing coupon rows would overweight multi-segment bookings and multi-passenger bookings. The measure must first summarize to booking grain, then calculate the ratio.

### 11.5 Supporting Metrics Required by the Five Pages

These metrics are required by the master prompt and the five report pages. They supplement, and do not replace, K-01 through K-21.

| ID | Metric | Formula | Numerator | Denominator | Notes |
|---|---|---|---|---|---|
| S-01 | Revenue Growth % | `(CurrentRevenue - PriorRevenue) / PriorRevenue` | Current-period total operating revenue minus prior comparable revenue | Prior comparable revenue | Prior period is the same number of days immediately preceding the current period, or the same fiscal period in the prior year where available. Zero prior revenue returns BLANK. |
| S-02 | Cost Growth % | `(CurrentCost - PriorCost) / PriorCost` | Current-period operating cost minus prior comparable cost | Prior comparable cost | Uses the same period logic as S-01. Excludes non-operating items. |
| S-03 | On-Time Arrival % | `OnTimeArrivals / OperatedFlightsWithValidArrival` | Operated flights with `OnTimeArrivalFlag = TRUE` | Operated flights with a non-null arrival delay | Arrival basis, separate from primary departure OTP. |
| S-04 | Delay Minutes per Operated Flight | `TotalArrivalDelayMinutes / OperatedFlights` | Sum of arrival delay minutes | Count of all operated flights | Uses all operated flights, not only flights with a valid delay. Missing delay is a data-quality exception and must not be silently treated as zero. |
| S-05 | Disruption Rate | `FlightsWithDisruption / ScheduledFlights` | Distinct flight legs with at least one disruption event | All scheduled flight legs | A flight with three events counts once in the numerator. |
| S-06 | Reactionary Delay Share | `ReactionaryDelayMinutes / TotalAttributedDelayMinutes` | Delay minutes on events with `ReactionaryFlag = TRUE` | Delay minutes on all attributed disruption events | Requires explicit evidence. Unclassified delay is not reactionary. Zero attributed minutes returns BLANK. |
| S-07 | Ancillary Revenue Share | `NetAncillaryRevenueUSD / TotalOperatingRevenueUSD` | Net ancillary revenue | Total operating revenue | Excludes taxes and pass-through amounts. Zero revenue returns BLANK. Total operating revenue includes net ancillary revenue, net passenger revenue, and net fee revenue. |
| S-08 | Booking Channel Mix | `ChannelBookings / TotalBookings` or `ChannelRevenue / TotalRevenue` | Bookings or revenue for the selected channel | Total bookings or total revenue | State whether the mix is by booking count, passenger count, or revenue. Do not mix the bases in one visual. |
| S-09 | Fare Class Mix | `FareClassPassengers / TotalPassengers` or `FareClassRevenue / TotalRevenue` | Revenue passengers or revenue for the selected fare class | Total revenue passengers or total revenue | State whether the mix is by passengers or revenue. Do not mix the bases in one visual. |
| S-10 | Route Contribution | `RouteOperatingRevenueUSD - RouteOperatingCostUSD` | Route total operating revenue | Not applicable; amount measure | Route contribution margin is route contribution divided by route operating revenue. Zero revenue returns BLANK for the margin. |
| S-11 | Target Variance | `Actual - Target` or `(Actual - Target) / Target` | Actual KPI value | Target KPI value for the ratio form | Targets are not defined in the baseline. Until approved, report actuals only and label target variance as unavailable. This is a proposed design baseline and remains subject to formal owner approval. |
| S-12 | Airline and Route Rankings | `RANKX` over the selected KPI within the current filter context | Not applicable | Not applicable | Rankings are not additive. State the ranking KPI, sort order, and tie behavior. Do not rank a ratio calculated from mixed grains. |
| S-13 | Scheduled vs Operated Flight Count | Count of scheduled, operated, and cancelled flight legs | Scheduled, operated, and cancelled counts | Not applicable; count measures | The three counts must reconcile: operated plus cancelled equals scheduled. Use this alongside cancellation and completion rates. |

**Supporting-metric rule:** S-01 through S-13 are report metrics, not substitutes for the 21 required KPIs. A page may use them in addition to the required KPI set, but it must not replace a required KPI with a supporting metric.

### 11.6 Measure Construction Rules

1. Use explicit DAX measures. Do not rely on implicit aggregations for ratios.
2. Use `DIVIDE` with a BLANK result for every ratio. Do not return zero unless the business definition explicitly requires zero.
3. Use `SUMX` over the fact table for ASK and RPK. Do not sum a ratio or an average across rows.
4. Use USD columns for every financial measure. Do not convert currency inside a measure.
5. Do not sum original-currency amounts across currencies. Filter to one currency or use USD.
6. Do not use `RELATED` inside a fact-table measure to pull a dimension value. Use the relationship and the filter context.
7. Do not create a fact-to-fact relationship to make a visual work. Use shared dimensions and separate measures.
8. Do not enable bidirectional filtering or many-to-many relationships. If a requirement appears to need one, escalate it as a model decision.
9. Use the active date relationship for the default date role. Use `USERELATIONSHIP` only for documented inactive roles.
10. Use the role-playing airport dimensions for origin and destination. Do not activate two relationships from the same physical DimAirport to DimRoute; use the approved role copies.
11. Calculate booking-level metrics after summarizing to BookingReference. Do not average coupon rows.
12. Calculate flight-level metrics after filtering to the declared flight population. Do not count booking rows as flights.
13. Use `DISTINCTCOUNT` for customer, booking, flight, and event counts where the grain can repeat. Do not use `COUNTROWS` unless the table is already at the required grain.
14. Preserve negative delays and negative unit contribution. Do not clamp valid negative values to zero.
15. Round only for presentation. Keep full precision in the model and in reconciliation files.
16. Show the denominator or response count in tooltips for every ratio. A percentage without its base is not decision-grade evidence.
17. Reconcile every critical measure to an independent control calculation before a page is accepted.
18. Treat a blank ratio as "not applicable" or "no eligible population", not as a zero performance result.
19. Do not use a visual-level filter to hide invalid records. Invalid records must be handled in the pipeline and disclosed.
20. Record the measure name, definition, date role, denominator, and owner in the KPI dictionary before DAX implementation.
21. What-if scenarios are report-layer calculations. They must disclose baseline, assumptions, formulas, and limitations; they must not write back to facts or be presented as forecasts.

## 12. Controlled Data-Quality Defects

### 12.1 Defect Policy

Controlled defects are synthetic issues deliberately injected into RAW data so that detection, disposition, and reconciliation can be tested. They are not permission to publish bad CURATED data.

- Defects are injected only in RAW.
- STAGING detects and classifies every injected defect.
- CURATED contains only accepted records. High-severity defects must have zero accepted rows.
- RAW values are preserved. Corrections are written to STAGING or CURATED with a disposition record.
- No record is silently deleted. Every rejected or corrected record has a rule ID, reason code, and disposition.
- A defect must not be injected into a control total, a primary key definition, or a reporting-period boundary in a way that makes reconciliation impossible. The exception is a deliberate duplicate or invalid key that STAGING must detect.
- Defect counts, rates, and dispositions must be reported by dataset, rule, and severity.
- The injection rate is a target for test coverage, not an acceptance threshold for CURATED.

### 12.2 Defect Catalogue

| ID | Defect | Example | Detection rule | Severity | Required treatment | CURATED outcome | Max injected rate |
|---|---|---|---|---|---|---|---|
| DQ-01 | Duplicate source record | Same booking coupon appears twice with the same business key | Business-key duplicate count greater than 1 | High | Keep the earliest valid record; log the duplicate and reason; do not sum both | One accepted row; duplicate quarantined | 0.50% |
| DQ-02 | Missing conditionally required attribute | ComplaintCategory blank when FeedbackType is Complaint; ResolutionDateKey blank when ResolutionStatus is Resolved | Conditional null and dependency check | High | Correct from source or quarantine | Conditional fields populated as required | 2.00% |
| DQ-03 | Invalid foreign key | Booking references a flight key that does not exist | Anti-join to the target dimension or fact | High | Quarantine the row or correct it only with a documented source rule | Zero orphan required keys | 0.20% |
| DQ-04 | Inconsistent text casing | `lhr`, `Lhr`, or `LHR` for the same airport code | Uppercase and trim comparison | Low | Standardize to the controlled code | Clean code | 1.00% |
| DQ-05 | Invalid date | Booking date after travel date; resolution before feedback | Date-order and range rules | High | Correct only with a documented rule; otherwise quarantine | Zero invalid required dates | 0.20% |
| DQ-06 | Negative or impossible numeric value | Negative seats, zero distance, fare below zero, delay beyond a plausible bound | Range and cross-field checks | High | Quarantine or correct with a documented rule | Zero impossible required values | 0.20% |
| DQ-07 | Invalid airport code | Code is not three uppercase letters or is absent from DimAirport | Regex plus referential check | High | Standardize or quarantine | Zero unresolved airport codes | 0.20% |
| DQ-08 | Currency inconsistency | Unsupported currency code, missing rate, or USD flag on a non-USD currency | Code-list and rate join | High | Quarantine; never convert with a missing or guessed rate | Zero unresolved currency rows | 0.10% |
| DQ-09 | Invalid flight status | Unknown status or cancellation flag that disagrees with status | Allowed-value and cross-field checks | High | Correct from the authoritative field or quarantine | Status and flags consistent | 0.20% |
| DQ-10 | Missing operational timestamp | Operated flight has no actual departure or arrival | Null check conditioned on status | High | Quarantine or correct from a documented source; do not invent a timestamp | Zero missing timestamps for operated flights | 0.20% |
| DQ-11 | Inconsistent booking identifier | Same ticket appears under different customers or channels | Cross-field and duplicate checks | High | Quarantine the conflicting rows | One consistent ticket-to-customer relationship | 0.10% |
| DQ-12 | Financial reconciliation exception | Coupon passenger, fee (including cancellation and no-show fees), and ancillary allocations do not reconcile to booking and financial control totals | Reconcile allocated coupon components to booking controls and financial totals | Critical | Block publication; resolve allocation or source error | Zero unexplained difference; applicable tolerance remains subject to formal owner approval | 0.05% |
| DQ-13 | Reactionary misclassification | Delay marked reactionary without an upstream event | Evidence check against `ReactionaryEvidenceID` | High | Set `ReactionaryFlag = FALSE`; retain as unclassified unless evidence is found | Evidence-based classification only | 0.10% |
| DQ-14 | Duplicate feedback event | Same customer, flight, type, and submission timestamp appears twice | Composite duplicate check | Medium | Keep one event; log the duplicate | One accepted event | 0.20% |

### 12.3 Severity and Disposition

| Severity | Meaning | CURATED acceptance |
|---|---|---|
| Critical | Breaks financial control, grain, or reporting-period integrity | Zero accepted rows; publication blocked until resolved |
| High | Breaks a required key, required value, or business rule | Zero accepted rows unless an approved exception is documented |
| Medium | Degrades an optional attribute or non-critical classification | Accepted with a documented default or null, and disclosed |
| Low | Cosmetic or standardization issue | Corrected and counted |

**Disposition record fields:** `QualityRuleID`, `Dataset`, `SourceFile`, `SourceRowNumber`, `BusinessKey`, `Severity`, `Disposition` (Accepted, Corrected, Quarantined, Rejected), `ReasonCode`, `OriginalValue`, `CorrectedValue`, `RuleVersion`, `RunID`, `ProcessedAtUTC`.

**Defect evidence:** the QA report must show injected count, detected count, corrected count, quarantined count, false-positive count, false-negative count, and final CURATED count. A defect family with a detected count below the injected count is a test failure.

## 13. Validation and Reconciliation Tests

### 13.1 Test Status and Evidence

Status values are PLANNED, IN PROGRESS, PASS, FAIL, and BLOCKED. No test in this document is claimed as PASS. Data tests are PLANNED until the generator exists. Power BI runtime tests are BLOCKED until a semantic model and report exist.

Every executed test must record: test ID, run timestamp, dataset version, seed, configuration hash, row counts, expected result, actual result, difference, status, evidence path, and reviewer. Evidence is stored under `qa/results/`; manifests are stored under `data/manifests/`; audit summaries are stored under `reports/audit/`.

### 13.2 Structural and Referential Tests

| ID | Test | Method | Expected result | Evidence | Status |
|---|---|---|---|---|---|
| T-01 | Exactly 10 approved airlines | Count active rows in DimAirline and distinct AirlineId, AirlineIATACode, and AirlineICAOCode values within the selected ReferenceVersion | 10 rows, 10 AirlineId values, 10 IATA codes, and 10 ICAO codes | `qa/results/structural_airlines.csv` | PLANNED |
| T-02 | Reporting-period coverage | Check DimDate for every date from 2025-10-01 through 2026-09-30; count `IsReportingPeriod` rows | 365 dates; no gaps; no duplicates | `qa/results/calendar_coverage.csv` | PLANNED |
| T-03 | Flight volume target | Count FactFlightOperations rows | Between 150,000 and 250,000, or an approved exception | `qa/results/flight_volume.csv` | PLANNED |
| T-04 | Unique primary keys | Duplicate check on every primary key | Zero duplicates in every table | `qa/results/primary_key_uniqueness.csv` | PLANNED |
| T-05 | Unique business keys | Duplicate check on every business key in Section 7.3 | Zero duplicates | `qa/results/business_key_uniqueness.csv` | PLANNED |
| T-06 | Required columns and types | Schema contract check against Section 6 | All required columns present; types match; no unexpected nulls | `qa/results/schema_contract.csv` | PLANNED |
| T-07 | Fact grain uniqueness | Duplicate check on each fact's grain key | Zero duplicate grain rows | `qa/results/fact_grain.csv` | PLANNED |
| T-08 | Dimension member counts | Count dimension rows against reference lists | Exact match to approved reference version | `qa/results/dimension_counts.csv` | PLANNED |
| T-09 | Required foreign keys resolve | Anti-join every required FK to its target | Zero unresolved required FKs | `qa/results/fk_required.csv` | PLANNED |
| T-10 | Route airports valid | Check origin and destination exist and differ | Zero invalid or same-airport routes | `qa/results/route_airports.csv` | PLANNED |
| T-11 | Aircraft ownership and type | Check aircraft airline and type against DimAirline and DimAircraftType | Zero invalid aircraft references | `qa/results/aircraft_refs.csv` | PLANNED |
| T-12 | Fact foreign keys resolve | Anti-join booking, cost, disruption, and feedback FKs | Zero unresolved required FKs | `qa/results/fk_facts.csv` | PLANNED |
| T-13 | No orphan records | Consolidated orphan report by fact and key | Zero orphans in CURATED | `qa/results/orphans.csv` | PLANNED |
| T-14 | No duplicate revenue rows | Check coupon business key and allocated revenue once per coupon | Zero duplicate coupons; allocation totals reconcile | `qa/results/revenue_duplicates.csv` | PLANNED |

### 13.3 Business and Financial Tests

| ID | Test | Method | Expected result | Evidence | Status |
|---|---|---|---|---|---|
| T-15 | Distance positive and consistent | Range check plus comparison to DimRoute.DistanceKM | Positive; within 0.5% of route distance | `qa/results/distance_checks.csv` | PLANNED |
| T-16 | Seats and passengers valid | Non-negative checks; revenue plus non-revenue carried versus booked; capacity check | No negative values; carried counts not greater than booked; capacity exceptions documented | `qa/results/passenger_checks.csv` | PLANNED |
| T-17 | Cancellation and completion flags | Cross-field check of FlightStatus, CancellationFlag, and CompletionFlag | Flags consistent; rates sum to 1 | `qa/results/status_flags.csv` | PLANNED |
| T-18 | Delay and block minutes valid | Recalculate from UTC timestamps; compare stored values | Exact match; nulls only for cancelled flights | `qa/results/delay_minutes.csv` | PLANNED |
| T-19 | Revenue identities | Recalculate net passenger, fee, and ancillary revenue | Exact match at two decimals | `qa/results/revenue_identities.csv` | PLANNED |
| T-20 | Refund sign convention | Range check and identity check | Refunds are non-negative; subtracted once | `qa/results/refund_signs.csv` | PLANNED |
| T-21 | Currency codes and rates | Check DimCurrency, exact-date rate, and USD conversion | Every financial row has a valid rate; conversion matches | `qa/results/currency_checks.csv` | PLANNED |
| T-22 | Booking lead time | Recalculate from FullDate values for TravelDate and BookingDate | Non-negative; matches stored value | `qa/results/lead_time.csv` | PLANNED |
| T-23 | Delay attribution partitions flight delay | Sum event delay minutes per flight and compare to arrival delay | Proposed one-minute engineering validation threshold for positive arrival delay, not owner-approved; otherwise record explicit Unattributed event; zero event minutes for non-delayed flights | `qa/results/delay_attribution.csv` | PLANNED |
| T-24 | Reactionary evidence | Check ReactionaryFlag against type eligibility and evidence ID | No reactionary event without evidence | `qa/results/reactionary.csv` | PLANNED |
| T-25 | Feedback resolution dates | Check ResolutionDateKey against FeedbackDateKey and status | Present when resolved; not before feedback | `qa/results/feedback_dates.csv` | PLANNED |
| T-26 | Cost reconciliation | Sum cost ledger by airline and month to control | Difference 0.00 USD or within the proposed 0.01 USD engineering validation threshold; not owner-approved | `qa/results/cost_reconciliation.csv` | PLANNED |
| T-27 | Tax and fee separation | Recalculate revenue identities with tax excluded and fee included once | Tax never in revenue; fee included once | `qa/results/tax_fee_checks.csv` | PLANNED |
| T-63 | Disruption event identity and sequence uniqueness | Check global DisruptionID uniqueness and independently check FlightOperationKey plus EventSequence uniqueness and contiguous sequence starting at 1 within each flight | Zero duplicate business IDs; zero duplicate flight-sequence pairs; sequences start at 1 and contain no gaps | `qa/results/disruption_event_identity.csv` | PLANNED |
| T-64 | Disruption-to-flight airline and route consistency | Resolve every FlightOperationKey to FactFlightOperations and compare RouteKey with the referenced flight. Compare AirlineKey with the operating airline as defined by OD-16. | Zero unresolved flight references, route mismatches, or operating-airline mismatches. | `qa/results/disruption_flight_consistency.csv` | PLANNED |
| T-65 | Revenue component identity and classification integrity | Recalculate the existing passenger, fee, and ancillary revenue identities from their documented fact columns; verify the component inclusion and exclusion rules without introducing a separate revenue classification reference | Every component identity reconciles exactly under the documented formula; no tax double count, duplicate component, or unsupported revenue classification | `qa/results/revenue_component_classification.csv` | PLANNED |
| T-66 | Cost classification reference integrity | Match every FactOperatingCosts CostCategory and CostSubcategory pair to the selected active `ref_cost_classification.csv` version | Exactly one active match per cost row; zero missing, duplicate, inactive, or ambiguous mappings | `qa/results/cost_classification_integrity.csv` | PLANNED |
| T-67 | Disruption classification reference integrity | Match every disruption type used by FactDisruptions to exactly one active `ref_disruption_types.csv` row in the selected version; reconcile the curated dimension attributes | Exactly one active reference match per used type; category and behavior flags reconcile; invalid mappings are quarantined | `qa/results/disruption_classification_integrity.csv` | PLANNED |
| T-68 | Source-to-standard mapping uniqueness | Inspect active source-to-standard mapping records for duplicate source keys, overlapping rules, and multiple target classifications within the same mapping scope and version | Every accepted source value resolves to exactly one standard classification; ambiguous mappings are rejected or quarantined | `qa/results/classification_mapping_uniqueness.csv` | PLANNED |
| T-69 | Classification reference-version and manifest integrity | Compare cost and disruption reference versions used by generated data with the exact versions recorded in dataset manifests and the selected refresh configuration | Every dataset and refresh uses the declared version; no unrecorded or mixed-version classification is accepted | `qa/results/classification_reference_versions.csv` | PLANNED |
| T-70 | Unmapped classification quarantine and reason completeness | Inject or inspect unmapped, inactive, invalid, and ambiguous source classifications; reconcile source records to accepted and quarantined dispositions | Every invalid mapping is quarantined with the required reason and lineage metadata; no silent fallback or loss of source records | `qa/results/classification_quarantine.csv` | PLANNED |
| T-71 | Cross-airline classification taxonomy consistency | Compare the selected cost and disruption taxonomy codes and definitions across all ten synthetic airline simulations | All ten airlines use the same approved taxonomy version and definitions; any approved exception is explicit and separately evidenced | `qa/results/airline_taxonomy_consistency.csv` | PLANNED |
| T-72 | Approved airline identity roster reconciliation | Compare DimAirline and ref_airlines.csv with the Section 2.1 roster on AirlineId, AirlineName, AirlineIATACode, AirlineICAOCode, HomeCountry, and HomeCountryCode for the selected ReferenceVersion | Exactly ten intended identities; zero missing, extra, duplicated, or mismatched identities; IATA/ICAO/name uniqueness is version-qualified | `qa/results/airline_identity_roster.csv` | PLANNED |
| T-73 | IATA code format and version-qualified uniqueness | Validate AirlineIATACode against `^[A-Z0-9]{2}$`; check uniqueness within ReferenceVersion in ref_airlines.csv and DimAirline; confirm it is not a key | Every IATA code is two uppercase alphanumeric characters and unique within the selected version; no fact join uses it | `qa/results/airline_iata_codes.csv` | PLANNED |
| T-74 | ICAO code format and version-qualified uniqueness | Validate AirlineICAOCode against `^[A-Z]{3}$`; check uniqueness within ReferenceVersion in ref_airlines.csv and DimAirline; confirm it is not a key | Every ICAO code is three uppercase letters and unique within the selected version; no fact join uses it | `qa/results/airline_icao_codes.csv` | PLANNED |
| T-75 | Airline identity source provenance completeness | For every populated identity attribute, resolve exactly one authoritative selected-version ref_airline_sources.csv record on AirlineId + AttributeName + AttributeValue with a real SourceOrganization, SourceURL, SourceType, SourceRetrievedDate, SourceVerifiedDate, VerificationMethod, and VERIFIED status; require EvidenceHash or SourceArchiveRef | Every required attribute has complete attribute-level provenance; every populated optional attribute has a VERIFIED record; optional attributes with no VERIFIED record are null; no fabricated or undated source record is accepted; OperatingRegion and BusinessModelClass are excluded | `qa/results/airline_identity_provenance.csv` | PLANNED |
| T-76 | Unsupported and conflicting identity attribute handling | Inspect source records marked CONFLICTING, UNVERIFIED, SUPERSEDED, or QUARANTINED; test unresolved required and optional attributes; verify no inference from home country, brand, or ownership | Conflicting or unsupported values are quarantined with reason and lineage; required conflicts block approval; optional attributes remain null; no silent selection, inference, OperatingRegion, or BusinessModelClass identity claim | `qa/results/airline_identity_conflicts.csv` | PLANNED |
| T-77 | Airline identity reference-to-dimension reconciliation | Compare the selected ref_airlines.csv version to DimAirline on AirlineId, AirlineKey mapping, every identity attribute, active-member count, and ReferenceVersion | Exact row-for-row reconciliation; same AirlineId resolves to the same AirlineKey; zero unexplained differences; no orphan or extra dimension member | `qa/results/airline_identity_reconciliation.csv` | PLANNED |
| T-78 | Airline identity reference-version, manifest, refresh, and key integrity | Verify T-78-01 to T-78-10: one distinct version in ref_airlines.csv and ref_airline_sources.csv; manifest version; DimAirline.ReferenceVersion; Power BI SelectedReferenceVersion; manifest status APPROVED; ten active AirlineId and ten unique AirlineKey values; one authoritative VERIFIED record per populated attribute; no key reassignment; reconciliation note for every identity change; no mixed-version facts | All ten sub-checks pass; a mismatch, unapproved version, missing key map, reassigned key, orphan fact key, or mixed version blocks generation and refresh | `qa/results/airline_identity_versions.csv` | PLANNED |
| T-79 | Synthetic disclosure exact-string and rendered-output integrity | Verify the Unicode code points of the exact canonical string, persistent page footer/header, tooltip while a page is visible, export template, and a rendered screenshot; test report extract metadata | Exact string `Synthetic Simulation — Not Actual Airline Performance` is present unconditionally on every page, tooltip while visible, export, and screenshot; no hyphen variant or “where practical” exception; failure blocks report release | `qa/results/disclosure_integrity.csv` | BLOCKED |

**Airline identity requirement trace:** T-72 and T-75 support REQ-023; T-73 and T-74 support REQ-024; T-75 and T-76 support REQ-025; T-76 supports REQ-026; T-77 supports REQ-027; T-78 supports REQ-028; T-79 supports BR-01 and REQ-001 disclosure evidence.

### 13.4 KPI and Reconciliation Tests

| ID | Test | Method | Expected result | Evidence | Status |
|---|---|---|---|---|---|
| T-28 | ASK independent calculation | Recalculate from seats and distance in a separate query | Equal to K-01 within 0.1% | `qa/results/kpi_ask.csv` | PLANNED |
| T-29 | RPK independent calculation | Recalculate from revenue passengers and distance | Equal to K-02 within 0.1% | `qa/results/kpi_rpk.csv` | PLANNED |
| T-30 | Load factor reconciliation | Recalculate RPK divided by ASK, including cancelled capacity | Equal to K-03 within 0.01 percentage point | `qa/results/kpi_load_factor.csv` | PLANNED |
| T-31 | Passenger revenue reconciliation | Compare coupon net passenger revenue to booking and financial controls | Equal within the proposed 0.01 USD per booking engineering validation threshold; not owner-approved | `qa/results/kpi_passenger_revenue.csv` | PLANNED |
| T-32 | Total revenue reconciliation | Compare passenger, fee, and ancillary revenue to total | Equal within the proposed 0.01 USD per airline-month engineering validation threshold; not owner-approved | `qa/results/kpi_total_revenue.csv` | PLANNED |
| T-33 | CASK and contribution reconciliation | Recalculate operating cost, CASK, total RASK, and unit contribution | Proposed engineering validation thresholds: 0.01 USD per ASK and 0.01 USD for monetary amounts; neither is owner-approved | `qa/results/kpi_cask.csv` | PLANNED |
| T-34 | OTP, cancellation, completion | Recalculate counts and ratios from status flags | Equal within 0.01 percentage point | `qa/results/kpi_operations.csv` | PLANNED |
| T-35 | Average delay and utilization | Recalculate delays and block hours; compare to availability reference | Proposed engineering validation thresholds: 1 minute for delay and 0.1% for utilization; neither is an owner-approved acceptance threshold | `qa/results/kpi_delay_utilization.csv` | PLANNED |
| T-36 | Customer KPIs | Recalculate satisfaction, complaints, refunds, repeat bookings, and recovery | Equal to definitions; denominators match | `qa/results/kpi_customer.csv` | PLANNED |
| T-37 | Zero-denominator behavior | Test zero or missing denominators for ASK, RPK, operated flights with valid departure or arrival delay, scheduled flights, available aircraft hours, eligible coupons, valid satisfaction responses, eligible customers, prior-period revenue and cost, operated flights, route revenue, and eligible service cases | Every applicable ratio returns BLANK, not zero or infinity; DAX runtime behavior is verified when the semantic model is available | `qa/results/kpi_zero_denominator.csv` | BLOCKED |
| T-38 | No duplicate revenue through joins | Compare headline revenue with and without each dimension join | No change; no fan-out | `qa/results/revenue_fanout.csv` | PLANNED |
| T-39 | Airline, route, month, and total reconciliation | Roll up revenue, cost, ASK, and RPK across each hierarchy | Components sum to total; differences within tolerance | `qa/results/kpi_rollups.csv` | PLANNED |

### 13.5 Reproducibility, Semantic-Model, and Runtime Tests

| ID | Test | Method | Expected result | Evidence | Status |
|---|---|---|---|---|---|
| T-40 | Deterministic rerun | Run the same seed, configuration, and code version twice | Same row counts, key sets, control totals, and hashes of logical output | `qa/results/reproducibility.csv` | PLANNED |
| T-41 | Manifest integrity | Compare file hashes and row counts to manifests | Every file matches its manifest | `qa/results/manifest_integrity.csv` | PLANNED |
| T-42 | Relationship cardinality | Inspect every model relationship | All 1:* single-direction; no unintended inactive or missing relationship | `qa/results/model_relationships.csv` | BLOCKED |
| T-43 | Role-playing dimensions | Test origin, destination, departure, arrival, booking, travel, feedback resolution, and disruption event-location roles, including EventLocationAirportKey | Each role filters only its intended dimension or fact population; inactive date roles are activated only by intended measures; event-location filtering does not propagate through DimRoute | `qa/results/model_roles.csv` | BLOCKED |
| T-44 | No fact-to-fact or many-to-many | Model review and relationship inventory | Zero prohibited relationships | `qa/results/model_prohibited.csv` | BLOCKED |
| T-45 | Power BI refresh | Refresh the model in Power BI Desktop | Refresh succeeds; row counts match CURATED | `qa/results/pbi_refresh.csv` | BLOCKED |
| T-46 | Report KPI reconciliation | Compare page visuals to control calculations | Every critical visual matches within tolerance | `qa/results/pbi_kpi_reconciliation.csv` | BLOCKED |
| T-47 | Booking lead-time bounds and date coverage | Recalculate lead time from FullDate values; check BookingDateKey against DimDate; apply a maximum only if OD-22 is formally approved | Lead time is non-negative and booking date is covered; no 365-day maximum is enforced while OD-22 remains open | `qa/results/lead_time_bounds.csv` | PLANNED |
| T-48 | Cancellation-fee and no-show-fee separation | Check TransactionStatus against CancellationFeeUSD and NoShowFeeUSD for every coupon | Cancelled coupons may carry cancellation fees only; NoShow coupons may carry no-show fees only; all other statuses carry neither; both fee fields are never positive on the same coupon | `qa/results/cancellation_no_show_fees.csv` | PLANNED |
| T-49 | K-18 period complaint-rate calculation | Independently count complaint events by FeedbackDateKey and revenue passengers by ScheduledDepartureDateKey for the same reporting period; calculate per 1,000 passengers | Formula matches `(ComplaintEvents / RevenuePassengers) * 1000`; zero passengers returns BLANK; date populations match the K-18 definition | `qa/results/kpi_complaint_rate.csv` | PLANNED |
| T-50 | DimDate coverage and date-key integrity | Check continuous DimDate coverage from 2024-10-01 through 2026-10-31; validate reporting-period flags and all fact date keys | No calendar gaps or duplicate dates; reporting period is exactly 2025-10-01 through 2026-09-30; required date keys resolve; travel dates are within the reporting period | `qa/results/date_coverage_integrity.csv` | PLANNED |
| T-51 | Time-zone and daylight-saving transitions | Validate IANA zone resolution, UTC-to-local conversion, daylight-saving transitions, cross-time-zone flights, overnight arrivals, and cancelled-flight date/timestamp behavior | Local dates and timestamps match the recorded time-zone database; ambiguous and nonexistent local times are handled deterministically; cancelled flights retain scheduled date keys and null actual timestamps | `qa/results/timezone_dst.csv` | PLANNED |
| T-52 | Cancellation and disruption-event consistency | Compare cancelled flight status and flags with disruption-event records; check cancelled-flight delay treatment | Cancelled flights remain in FactFlightOperations; status and flags agree; cancellation is not converted into an invented operational delay; event treatment follows the documented rules | `qa/results/cancellation_disruption.csv` | PLANNED |
| T-53 | Coupon-to-flight passenger reconciliation | Sum Flown coupon PassengerCount where IsRevenuePassenger is TRUE by FlightOperationKey and compare with FactFlightOperations.RevenuePassengers; separately inspect cancelled coupons | Differences are reported by flight; cancelled coupons reconcile to zero carried passengers; no tolerance is assumed until OD-20 is formally approved | `qa/results/coupon_flight_passenger_reconciliation.csv` | PLANNED |
| T-54 | Injected-defect detection and disposition | Compare injected defect inventory with detected defects and recorded dispositions by dataset, rule, and severity | Every injected defect is detected; injected and detected counts reconcile; corrected, quarantined, false-positive, and false-negative outcomes are recorded | `qa/results/defect_injection_detection.csv` | PLANNED |
| T-55 | Booking allocation residual attribution | Recalculate booking-level allocations and rounding residuals; inspect eligible coupons, residual assignment, tie-break, and one-time allocation | Allocations reconcile to booking controls after rounding; residual goes to the largest eligible coupon, ties to the lowest BookingTransactionKey, and is assigned once; execution remains blocked pending OD-14 formal approval | `qa/results/booking_allocation_residual.csv` | BLOCKED |
| T-56 | Aircraft availability composite-key uniqueness | Check uniqueness of the combination AircraftKey, CalendarDateKey, and ReferenceVersion; separately verify no duplicate AircraftKey and CalendarDateKey combinations within the selected reference version | Zero duplicate composite keys and zero duplicate aircraft-date combinations within the selected version | `qa/results/aircraft_availability_keys.csv` | PLANNED |
| T-57 | Aircraft and date reference integrity | Anti-join AircraftKey to DimAircraft and CalendarDateKey to DimDate; validate required values and YYYYMMDD date-key format | Zero unresolved required references, null keys, or invalid date keys | `qa/results/aircraft_availability_references.csv` | PLANNED |
| T-58 | Availability status and hours validation | Check AvailableHours range and validate every AvailabilityStatus against the documented status/hour combinations | Available requires hours greater than 0.00 and no greater than 24.00; Maintenance, Stored, Retired, and No Planned Availability require 0.00; invalid values are rejected or quarantined with a reason | `qa/results/aircraft_availability_status.csv` | PLANNED |
| T-59 | Aircraft availability reference-version integrity and reproducibility | Compare dataset ReferenceVersion with generation manifests; verify one explicitly selected version per semantic-model refresh; rerun historical version checks | Every dataset matches its manifest; exactly one version is selected per refresh; previously published versions remain reproducible; historical corrections have a new version and reconciliation note | `qa/results/aircraft_availability_versions.csv` | PLANNED |
| T-60 | K-13 available-aircraft-hour denominator eligibility | Independently calculate available aircraft hours using only Available records for active aircraft-days and the selected ReferenceVersion; compare operating block hours from FactFlightOperations and recalculate K-13 | Only Available records contribute to the denominator; excluded statuses contribute zero; operating block hours are not duplicated; K-13 matches the independent calculation; zero denominator returns BLANK | `qa/results/kpi_aircraft_utilization.csv` | PLANNED |
| T-61 | Disruption event-location airport integrity | Resolve EventLocationAirportKey to DimAirport and resolve the referenced flight route; compare the event airport with route origin and destination using the proposed baseline selection rule | Zero unresolved airport keys; origin is used by default; destination is used only when explicitly identified by the source; intermediate and en-route events are quarantined with reason codes | `qa/results/disruption_event_location_integrity.csv` | PLANNED |
| T-62 | Disruption event local-date derivation | Recalculate EventDateKey by converting EventStartTimestampUTC using EventLocationAirportKey's TimeZoneIANA and the time-zone database version recorded in the manifest; validate IANA zones and DimDate lookup | Every EventDateKey matches the independently derived local date; invalid zones, missing dates, and timezone-version mismatches are reported and quarantined; EventEndTimestampUTC does not determine the date key | `qa/results/disruption_event_local_date.csv` | PLANNED |

### 13.6 Tolerances and Pass Rules

| Item | Tolerance |
|---|---|
| Row counts and key counts | Exact match |
| Required foreign-key resolution | Zero unresolved required keys |
| Financial amounts | Proposed engineering validation threshold: 0.01 USD per transaction, booking, airline-month, and total. This is not an owner-approved acceptance threshold; applicable financial tolerances remain subject to the relevant formal owner decisions, including OD-20. |
| ASK and RPK | 0.1% of the independent control value |
| Ratios and percentages | 0.01 percentage point |
| Delay minutes | Proposed engineering validation threshold: 1 minute per flight; not an owner-approved acceptance threshold |
| Injected-defect detection | 100% of injected defects detected |
| False positives | Less than 1% of clean records |
| Reproducibility | Identical logical output for the same seed and configuration |

**Pass rule:** a test is PASS only when it has been executed, the evidence file exists, the expected and actual results are recorded, and a reviewer has accepted the result. A static document check is not a substitute for a data test or a Power BI runtime test. A test that cannot run is BLOCKED, not PASS.

**Gate rule:** G3 - Data contracts and model design - is not PASS until all critical open decisions are approved, this document is reviewed, and the data dictionary is aligned. G4 - Data generation - is not authorized until G3 passes.

## 14. Decisions Requiring Approval

The decision register distinguishes proposed design baselines from owner-approved business decisions. A baseline or proposal describes the current architectural recommendation; it is not evidence of owner approval. A decision is formally closed only when the project owner records the selected option, rejected alternatives, rationale, impact on tables and KPIs, affected requirements, approver, and approval date. Until that record exists, the decision remains open and affected implementation must be treated as provisional.

| ID | Decision | Baseline or proposal | Why it matters | Status |
|---|---|---|---|---|
| OD-01 | Real airline identity population and identity/reference model (parent) | Split into OD-01A (population) and OD-01B (identity, key, provenance, lifecycle, reference version, and Power BI constraints). | Defines the airline dimension, comparisons, and all airline-level KPIs | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING; SPLIT INTO OD-01A/OD-01B |
| OD-01A | Ten-airline population and inclusion/exclusion boundary | Fixed roster in Section 2.1; real identities; synthetic operations; fixed reporting period; OD-01A records the population decision and evidence requirements. | Defines which airlines are in scope and the real-identity/synthetic-data boundary | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING |
| OD-01B | Airline identity, key, provenance, lifecycle, and reference-version model | `AirlineId` durable identity; permanent `AirlineKey`; IATA/ICAO/name version-qualified attributes; `LegalName` reference-only; `IsActive` + `StatusEffectiveDate`; Type 1 with immutable snapshots; manifest-authoritative reference versions; T-78 and G3-RV-01. | Defines identity joins, provenance, reproducibility, historical semantics, and Power BI relationship constraints | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING |
| OD-02 | Airport and network population | Populated from ref datasets; controlled lists for airports, route regions, and IANA time zones. | Drives flight volume, route coverage, distance, and network analysis | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-03 | Fleet composition | Populated from ref datasets; controlled aircraft types, capacities, and status. | Drives capacity, aircraft utilization, and type-level analysis | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-04 | Synthetic exchange-rate policy | USD per one unit of currency; exact-date rate; six decimals; synthetic source. Currency set: USD, EUR, GBP, JPY, CAD. | Every non-USD financial fact depends on it | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-05 | Cancelled-flight capacity treatment | Scheduled ASK includes cancelled flights. Alternative: operated ASK excludes cancelled flights. | Changes load factor, passenger RASK, total RASK, CASK, and unit contribution | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-06 | Passenger revenue definition | Net base fare: base fare minus discount minus passenger refund. Excludes taxes, fees, ancillary revenue, non-revenue tickets, Booked, cancelled, and no-show coupons. | Defines passenger yield, passenger RASK, average passenger revenue, and total revenue | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-07 | Tax and fee treatment | Taxes are pass-through and excluded from revenue. Carrier-retained fees are included in total operating revenue but not passenger revenue. | Changes total RASK, fee revenue, and revenue reconciliation | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-08 | Refund, cancellation-fee, no-show, and chargeback treatment | Refunds are positive magnitudes and reduce revenue. Cancellation fees and no-show fees are separate fee revenue fields. Chargebacks are not modeled. | Changes net revenue, refund rate, and financial control totals | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-09 | OTP threshold and basis | Departure OTP uses a 15-minute threshold; early departures are on time. Arrival OTP is a supporting variant. | Changes OTP, delay analysis, and operational rankings | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-10 | Aircraft-utilization availability assumption | 14.00 available hours per active aircraft-day, with maintenance and stored days excluded. | Changes aircraft utilization and capacity commentary | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-11 | Satisfaction score scale | Integer 1 through 5. | Changes satisfaction averages and complaint analysis | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-12 | Complaint-rate denominator | Complaints per 1,000 revenue passengers, period-level, not cohort-matched. | Changes complaint rate and customer-service comparisons | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-13 | Revenue, cost, and delay-cause category mappings | Revenue component treatment follows the existing booking-fact fields and identities; no separate revenue classification reference is proposed. Cost classifications use the proposed versioned `ref_cost_classification.csv` mapped to existing `FactOperatingCosts.CostCategory` and `CostSubcategory` fields. Disruption types use the proposed versioned `ref_disruption_types.csv` reconciled to `DimDisruptionType`. Source mappings must resolve uniquely; invalid or ambiguous mappings are quarantined with reason and lineage metadata. Exact codes, subcategories, and source mappings remain unapproved. | Changes revenue classification integrity, CASK, cost analysis, disruption analysis, and page filters | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-14 | Booking transaction grain and allocation | One row per passenger ticket coupon per flight segment. Booking-level amounts allocated exactly once, pro-rata to base fare, residual to largest eligible coupon, ties by lowest BookingTransactionKey. | Defines revenue grain, refund rate, lead time, and repeat-booking measures | OWNER DIRECTION STATED - FORMAL APPROVAL RECORD INCOMPLETE |
| OD-15 | Separate FactRevenue versus revenue in FactBookingTransactions | No separate FactRevenue. Revenue is held in FactBookingTransactions. The master prompt lists FactRevenue as a candidate. | A second revenue fact would create duplication and fact-to-fact risk | OWNER DIRECTION STATED - FORMAL APPROVAL RECORD INCOMPLETE |
| OD-16 | Codeshare and marketing-carrier treatment | One row per operating flight leg; marketing codeshares are not duplicated. | Prevents duplicate capacity and revenue | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-17 | Service-recovery definition | Eligible case is a complaint with `ServiceRecoveryFlag = TRUE`; recovered means `ResolutionStatus = Resolved`. | Changes service recovery rate and customer-service conclusions | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-18 | Repeat-booking and lead-time eligibility | Exclude cancelled and fully refunded bookings from the baseline eligible population. | Changes repeat booking rate and booking lead time | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-19 | Diversion and reaccommodation accounting | Not modeled in the baseline. `FlightStatus` is Operated or Cancelled. | A diversion policy would change completion, delay, RPK, and revenue treatment | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-20 | Passenger-count reconciliation tolerance | Coupon revenue passengers must reconcile to flight revenue passengers by flight. Zero at booking grain for carried-passenger counts; 0.01 USD at coupon level for amounts. | A loose tolerance hides booking-to-flight errors; a zero tolerance may be unrealistic | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-21 | Targets and target variance | No targets defined in the baseline. Report actuals only; target variance is marked unavailable in the semantic model. | Target variance, management alerts, and performance rankings depend on approved targets | PROPOSED - OWNER APPROVAL REQUIRED |
| OD-22 | Maximum booking lead time | Proposal: maximum booking lead time of 365 calendar days. Until approved, no 365-day maximum is normative or may be enforced by K-16. | Affects booking-date coverage, lead-time eligibility, K-16, and date-dimension requirements | OPEN - OWNER APPROVAL REQUIRED |
| OP-01 | Cohort complaint rate | Proposed supporting metric: complaint events attributed to a travel cohort divided by revenue passengers in that same travel cohort, expressed per 1,000 passengers. This is distinct from period-level K-18 and requires owner approval before implementation. | Changes cohort-based customer-service comparisons and date-role logic | OPEN - OWNER APPROVAL REQUIRED |

**Critical decisions for G3:** OD-01A, OD-01B, OD-02, OD-03, OD-04, OD-05, OD-06, OD-07, OD-08, OD-12, OD-13, OD-14, OD-15, OD-16, OD-19, OD-20, and OD-21 require formal owner approval records before they can be treated as closed for G3. OD-01A, OD-01B, OD-02, and OD-03 define the controlled airline, airport, and fleet populations and identity/reference rules required by the reference datasets and generation design. Owner direction has previously been stated for OD-14 and OD-15, but their formal approval records are incomplete. The remaining listed decisions are proposals requiring owner approval. G3 cannot pass while critical decisions remain open. The ten-airline roster is the owner-confirmed intended population, but OD-01A and OD-01B remain open until their formal signatures and approval dates are recorded. Reference-version approval is gate artifact `G3-RV-01`, not an OD-series decision; OD-23 is rejected and is not created.

**Decision-record rule:** an approval must state the chosen option, the rejected alternatives, the impact on tables and KPIs, the affected requirements, the approver, and the date. A verbal approval is not sufficient.

### 14.1 Individual Decision Approval Records

This register tracks the formal approval state of every owner decision and open proposal. The named project owner is the designated approver identity for the pending template only. Recording this identity does not constitute approval of any decision.

| Decision ID | Project owner / approver | Approval date | Status |
|---|---|---|---|
| OD-01 | KH Mohammad Farhan |  | PENDING - SPLIT; SEE OD-01A/OD-01B |
| OD-01A | KH Mohammad Farhan |  | PENDING |
| OD-01B | KH Mohammad Farhan |  | PENDING |
| OD-02 | KH Mohammad Farhan |  | PENDING |
| OD-03 | KH Mohammad Farhan |  | PENDING |
| OD-04 | KH Mohammad Farhan |  | PENDING |
| OD-05 | KH Mohammad Farhan |  | PENDING |
| OD-06 | KH Mohammad Farhan |  | PENDING |
| OD-07 | KH Mohammad Farhan |  | PENDING |
| OD-08 | KH Mohammad Farhan |  | PENDING |
| OD-09 | KH Mohammad Farhan |  | PENDING |
| OD-10 | KH Mohammad Farhan |  | PENDING |
| OD-11 | KH Mohammad Farhan |  | PENDING |
| OD-12 | KH Mohammad Farhan |  | PENDING |
| OD-13 | KH Mohammad Farhan |  | PENDING |
| OD-14 | KH Mohammad Farhan |  | PENDING |
| OD-15 | KH Mohammad Farhan |  | PENDING |
| OD-16 | KH Mohammad Farhan |  | PENDING |
| OD-17 | KH Mohammad Farhan |  | PENDING |
| OD-18 | KH Mohammad Farhan |  | PENDING |
| OD-19 | KH Mohammad Farhan |  | PENDING |
| OD-20 | KH Mohammad Farhan |  | PENDING |
| OD-21 | KH Mohammad Farhan |  | PENDING |
| OD-22 | KH Mohammad Farhan |  | PENDING |
| OP-01 | KH Mohammad Farhan |  | PENDING |

**Status rule:** Every record remains PENDING until the selected option, rejected alternatives, rationale, table and KPI impacts, affected requirements, approver confirmation, approval date, and supporting evidence are completed and verified. No verbal direction or template entry alone closes a decision. For OD-01A, the owner-confirmed roster and inclusion boundary are inputs to the decision record, not a completed formal approval. For OD-01B, the owner-confirmed design is an input, not a completed formal approval. OD-01A and OD-01B are separate signatures. Reference-version approval remains `G3-RV-01`, not an OD-series decision.

#### Detailed decision approval record template

Use one completed record for each decision before changing its status.

| Field | Required record |
|---|---|
| Decision ID and title |  |
| Selected option |  |
| Rejected alternatives |  |
| Rationale |  |
| Impact on facts, dimensions and reference datasets |  |
| Impact on KPIs, calculations and reporting |  |
| Affected requirements and validation test IDs |  |
| Supporting evidence / reference |  |
| Project owner / approver | KH Mohammad Farhan |
| Approval date |  |
| Decision status | PENDING |

**Approval control:** Do not change a decision to APPROVED until the project owner has explicitly confirmed the complete record. Keep the document-level approval status in Section 16.4 separate from individual decision approvals. This section does not authorize schema freeze, data generation, implementation, or a G3 PASS.

## 15. Acceptance Criteria

### 15.1 Document Acceptance

| ID | Criterion | Evidence | Status |
|---|---|---|---|
| AC-01 | All 16 required sections are present and correctly numbered | Section heading check | DOCUMENTED |
| AC-02 | Exactly 10 real airline identities are stated as a fixed constraint, with source verification required before reference approval | Sections 2, 2.1, 4.3, and 7.3 | DOCUMENTED |
| AC-03 | Reporting dates 2025-10-01 through 2026-09-30 are stated correctly | Sections 2, 9.4, and 9.5 | DOCUMENTED |
| AC-04 | All required dimensions and candidate facts have a business purpose, grain, primary key, and foreign keys | Sections 4 and 5 | DOCUMENTED |
| AC-05 | Required columns, data types, nullability, and business definitions are documented | Section 6 | DOCUMENTED |
| AC-06 | Relationship cardinality, filter direction, role-playing dimensions, and semantic-model constraints are documented | Section 8 | DOCUMENTED |
| AC-07 | Date, timestamp, time-zone, and fiscal-calendar rules are documented | Section 9 | DOCUMENTED |
| AC-08 | Currency conversion and financial-recognition rules are documented | Section 10 | DOCUMENTED |
| AC-09 | All 21 required KPIs have business meaning, formula, numerator, denominator, and exclusions | Section 11.2 through 11.4 | DOCUMENTED |
| AC-10 | Controlled data-quality defects and dispositions are documented | Section 12 | DOCUMENTED |
| AC-11 | Validation and reconciliation tests, tolerances, and evidence rules are documented | Section 13 | DOCUMENTED |
| AC-12 | Open decisions, including OD-01A and OD-01B, are identified and not presented as approved | Section 14 | DOCUMENTED |
| AC-13 | The document is consistent with the project scope and business requirements, with any differences disclosed | This section and `OD01_REMEDIATION_CHANGE_RECORD.md` | DOCUMENTED |
| AC-14 | The file is valid UTF-8 Markdown with no escaped headings, malformed tables, duplicated sections, or accidental instructions | Repair verification report | EXTERNAL EVIDENCE |
| AC-15 | The document does not authorize data generation, model implementation, or a release claim | Sections 1 and 16 | DOCUMENTED |

### 15.2 Data-Generation Gate

| ID | Criterion | Evidence | Status |
|---|---|---|---|
| AC-16 | Critical open decisions are approved and recorded | Signed decision records | OPEN |
| AC-17 | Schema version is frozen and aligned with the data dictionary | Approved schema and `04_DATA_DICTIONARY.md` | PLANNED |
| AC-18 | Reference data versions are approved through `G3-RV-01`, with the manifest as the authoritative approval record | Approved reference manifest and `G3-RV-01` record | PLANNED |
| AC-19 | Validation tests are implemented and dry-run successfully | Test code and dry-run evidence | PLANNED |
| AC-20 | G3 data contracts and model design gate is APPROVED | Gate review record | NOT STARTED |
| AC-21 | G4 data generation is authorized | Written authorization after G3 | BLOCKED |
| AC-22 | No datasets, semantic model, DAX measures, or report pages have been created by this document | Repository inspection | DOCUMENTED |
| AC-23 | OD-01A and OD-01B design records exist, carry the required status, and are not represented as formally approved | `OD01A_AIRLINE_POPULATION_DECISION.md`, `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | DOCUMENTED - PENDING FORMAL APPROVAL |
| AC-24 | T-78 and `G3-RV-01` are defined; neither is executed or approved by this document | Sections 3.4, 13, and 14 | PLANNED |

**Acceptance rule:** document acceptance does not equal data acceptance. The document can be accepted with open decisions, but data generation cannot begin until the critical decisions are closed and G3 passes.

## 16. Document Status and Next Step

### 16.1 Current Status

**Status:** DRAFT - CONTROLLED OD-01 REMEDIATION COMPLETE; PENDING REVIEW AND FORMAL APPROVAL.

**Version:** 1.5.

**What is complete in this document:**

- Escaped Markdown was replaced with valid headings, lists, and tables.
- The document was reorganized into the 16 required sections.
- Dimension and fact grains, keys, required columns, data types, and business rules were made explicit.
- Relationship and semantic-model rules were documented, including role-playing dates and airports.
- Date, time-zone, fiscal-calendar, currency, and financial policies were documented.
- All 21 required KPIs were given a business meaning, formula, numerator, denominator, and exclusions.
- Supporting metrics required by the five pages were added.
- Controlled defects, validation tests, tolerances, and evidence rules were documented.
- Open decisions were recorded and are not presented as approved.
- The airline identity model now separates durable `AirlineId` business identity from permanent `AirlineKey` warehouse identity; IATA and ICAO are mutable, version-qualified attributes.
- The reference schema, attribute-level provenance, source hierarchy, conflict/quarantine rules, evidence durability, staleness policy, reference manifest, `G3-RV-01`, Type 1 historical limitation, key-map controls, and Power BI reference-version constraints are documented.
- Tests T-72 to T-78 were reconciled to the identity/reference model, and T-79 was added for the exact synthetic-data disclosure.
- OD-01A and OD-01B design records exist and are referenced; both remain subject to formal signature and approval.

**What is not complete:**

- OD-01A and OD-01B do not have formal signatures or approval dates. Owner confirmation of the design is not formal approval.
- No other decision in Section 14 has a complete formal approval record. Owner direction was stated for OD-14 and OD-15, but the required approver, date, and complete decision-record details are not captured in this document.
- The reference manifest has not been created or approved; `G3-RV-01` has not been executed.
- No reference CSV, data dictionary, dataset, semantic model, DAX measure, or Power BI page has been created.
- No data-quality or reconciliation test has been executed; T-79 is BLOCKED because no rendered report exists.
- No Power BI Desktop runtime validation has been performed.
- No gate has been marked APPROVED or PASS by this document; G3 gate execution NOT STARTED; G3 design documentation PREPARED — DRAFT (documentation state, not approval); G3 formal approval NOT FORMALLY APPROVED; G4 remains BLOCKED.
- `01_PROJECT_SCOPE.md` was not in the authorized edit set. Its high-level present-tense “source-verified” and “region/business-model” wording is a disclosed residual, not a silent change to this contract.

### 16.2 Next Step

1. Review this document against `01_PROJECT_SCOPE.md`, `02_BUSINESS_REQUIREMENTS.md`, `OD01A_AIRLINE_POPULATION_DECISION.md`, `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`, and the master prompt.
2. Obtain the project owner's formal signatures and approval dates for OD-01A and OD-01B. Do not treat the owner-confirmed design status as approval.
3. Approve or revise the remaining critical decisions in Section 14, starting with OD-02, OD-03, OD-04, OD-05, OD-06, OD-07, OD-08, OD-12, OD-13, OD-14, OD-15, OD-16, OD-19, OD-20, and OD-21.
4. Execute `G3-RV-01` only after the reference version, manifest, source evidence, T-75/T-76 results, and T-78 plan are complete.
5. Freeze the schema version and align it with the planned data dictionary.
6. Create `04_DATA_DICTIONARY.md` only when authorized. Do not create it as part of this remediation.
7. Record the G3 decision in the progress ledger and traceability matrix.
8. Authorize G4 data generation only after G3 is APPROVED.

**Next document:** `04_DATA_DICTIONARY.md` - not created by this task.

**Do not proceed to data generation, Power BI model construction, DAX development, or report page construction until the approval conditions in Section 15 are met.**

### 16.3 Change Log

| Version | Date | Change | Author / status |
|---|---|---|---|
| 1.0 | Before repair | Original data-contract draft with escaped Markdown and limited detail | Data design draft |
| 1.1 | 2026-11-01 | Repaired Markdown; added required sections, data types, keys, relationships, KPI detail, defect controls, validation tests, and open decisions | Documentation repair; pending approval |
| 1.2 | 2026-11-01 | Specified proposed versioned cost and disruption classification references, OD-13 mapping controls, tests T-65 to T-71, and foundational G3 population dependencies | Controlled design update; pending owner approval |
| 1.3 | 2026-11-01 | Aligned T-64 with OD-16 operating-airline ownership and corrected the displayed document version | Documentation alignment; pending owner approval |
| 1.4 | 2026-11-01 | Reconciled the airline identity population to ten real, source-verified airlines; replaced the ambiguous standalone airline-code field with separate IATA and ICAO identifiers; documented attribute-level provenance, nullable optional attributes, and tests T-72 to T-77; OD-01 remains pending and no data generation is authorized | Controlled documentation migration; pending owner approval |
| 1.5 | 2026-11-01 | Applied the owner-confirmed OD-01 remediation: split OD-01A/OD-01B; introduced durable `AirlineId` and permanent `AirlineKey`; made IATA/ICAO version-qualified attributes; defined `LegalName` as reference-only; added `StatusEffectiveDate`; removed `OperatingRegion` from identity; retained optional analytical `BusinessModelClass`; added reference manifest, `G3-RV-01`, Type 1 historical limitation, T-78, T-79, and Power BI reference-version/disclosure controls; formal signatures and approval remain PENDING | Controlled documentation remediation; pending review and formal approval |

### 16.4 Approval Record

| Role | Name | Decision | Date |
|---|---|---|---|
| Project owner |  |  |  |
| Data architecture lead |  |  |  |
| Power BI solution architect |  |  |  |
| QA / validation lead |  |  |  |

**Approval status:** PENDING. This document is not approved for data generation.


---

## Portfolio Transition Amendment — A360-PA-001
**Effective direction date:** 2026-11-04  
**Status:** Owner-directed portfolio implementation track

### Amendment precedence

For this synthetic-data portfolio project, this amendment supersedes earlier provisions that prohibit all engineering implementation until formal G3/G4 approval. It permits controlled portfolio engineering without representing historical G3/G4 gates as passed.

This limited permission covers reference-data preparation, synthetic-data generation, Python engineering, data-layer construction, Power Query, semantic modelling, DAX, Power BI reports, testing, and portfolio documentation.

### Controls that remain mandatory

- Real airline identity attributes must be traceable to sources. Unverified attributes remain null or explicitly pending verification.
- Operational, passenger/customer, booking, financial, disruption, and feedback records must be synthetic.
- Real passenger personal information is prohibited.
- Synthetic generation must be reproducible and documented.
- Keys, grains, relationships, units, dates, and business definitions must be documented.
- Data quality must cover completeness, validity, uniqueness, referential integrity, and reconciliation.
- Financial and operational KPIs must be reconciled against independently calculated results.
- RAW, STAGING, CURATED, and REFERENCE layers must remain distinguishable.
- Material schema and business-rule changes must be recorded.
- The required disclosure is **Synthetic Simulation — Not Actual Airline Performance** and must appear on dashboards, relevant tooltips, and exports.

### Historical gate treatment

G3 and G4 are not declared approved by this amendment. Their historical statuses remain unchanged. Portfolio implementation checkpoints are separate and must be evidenced by actual tests, review results, and artifacts.

A draft schema may evolve during engineering. A versioned schema baseline must be established before final model and report release.

No signature, independent reviewer, source verification, test result, or approval may be fabricated.

This amendment changes the implementation permission for the portfolio track only. It does not authorize production deployment or the use of real passenger data.
