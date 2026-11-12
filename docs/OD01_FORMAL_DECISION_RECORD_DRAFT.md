# AEROVISION 360 - OD-01 Formal Decision Record (DRAFT)

**Document type:** Formal decision record - draft for owner review and signature
**Decision ID:** OD-01
**Decision title:** Real airline identity population
**Decision owner / approver:** KH Mohammad Farhan
**Formal status:** PENDING OWNER SIGNATURE
**Decision date:** [BLANK - to be completed by the owner at signature]
**Owner approval evidence:** [BLANK - to be completed at signature]
**Draft version:** 0.1
**Draft prepared:** 2026-11-01
**Governing baseline:** `03_DATA_CONTRACTS.md` version 1.4
**Related migration report:** `OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt`

> **DRAFT NOTICE - NOT AN APPROVAL**
>
> This document is a draft prepared for owner review. It does not close OD-01, does not
> constitute owner approval, and does not authorize data generation, a schema freeze, or a
> G3 PASS. No decision date and no signature have been entered. G3 remains NOT STARTED and
> G4 remains BLOCKED. The six active baseline documents have not been modified by the
> preparation of this draft.

---

## 1. Purpose

This record prepares the formal owner decision required to close OD-01, "Real airline
identity population." The controlled documentation migration of 2026-11-01 reconciled the
project to ten real airline identities and separated the IATA and ICAO identifiers. That
migration updated the documentation baseline but did not complete the formal decision
record.

This draft sets out, in one place, the decision proposed for owner signature: the exact
roster, the approval scope and exclusions, the boundary between real identity attributes
and synthetic performance data, the source-verification rules, the required provenance
reference files, the impacted schemas and tests, and the known risks and limitations.

If signed, this record would become the approval evidence for OD-01. Until then, the
decision remains open and the roster remains approved only as the intended population.

---

## 2. Decision statement proposed for approval

The owner is asked to approve the following statements as a single decision:

| ID | Proposed decision |
|---|---|
| D-1 | The baseline airline population is fixed to exactly the ten real airline identities listed in Section 3. No airline may be added, removed, substituted, or renamed without a new approved decision and reference version. |
| D-2 | `AirlineName`, `AirlineIATACode`, `AirlineICAOCode`, `HomeCountry`, and `HomeCountryCode` are real identity attributes. They must be source-verified and must reconcile exactly across the approved roster, `ref_airlines.csv`, and `DimAirline`. |
| D-3 | `AirlineIATACode` is the primary business key for airline identity. `AirlineICAOCode` is a unique alternate identifier. There is no standalone ambiguous `AirlineCode` field. `AirlineKey` remains the internal surrogate primary key of `DimAirline`. |
| D-4 | `AirlineGroup`, `OperatingRegion`, and `BusinessModel` are optional identity attributes. They may be populated only where reliable, recorded evidence supports the value; otherwise they must be null. They must not be inferred from home country, ownership assumptions, or generic industry labels. |
| D-5 | Airline identity values require attribute-level provenance in `ref_airline_sources.csv`, following the source hierarchy, verification statuses, conflict resolution, quarantine, and versioning rules in Section 6 of this record and Section 3.4 of the data contract. |
| D-6 | All operational, customer, booking, revenue, cost, disruption, feedback, and financial data for these airlines are synthetic simulations. No output may be presented as the actual performance of any named airline. |
| D-7 | This decision approves the population and identity rules only. It does not approve any reference data values beyond the roster, does not create or populate reference CSV files, does not freeze the schema, and does not authorize data generation. |

---

## 3. Approved airline roster

The exact proposed population is:

| # | Airline | IATA | ICAO | Home country | Country code |
|---|---|---|---|---|---|
| 1 | Emirates | EK | UAE | United Arab Emirates | AE |
| 2 | Qatar Airways | QR | QTR | Qatar | QA |
| 3 | Singapore Airlines | SQ | SIA | Singapore | SG |
| 4 | Air India | AI | AIC | India | IN |
| 5 | IndiGo | 6E | IGO | India | IN |
| 6 | British Airways | BA | BAW | United Kingdom | GB |
| 7 | Lufthansa | LH | DLH | Germany | DE |
| 8 | Delta Air Lines | DL | DAL | United States | US |
| 9 | Southwest Airlines | WN | SWA | United States | US |
| 10 | Qantas | QF | QFA | Australia | AU |

### 3.1 Optional identity attributes

No `AirlineGroup`, `OperatingRegion`, or `BusinessModel` value is approved by this record.
These attributes are deliberately left unpopulated at decision level:

| Attribute | Treatment in this record |
|---|---|
| `AirlineGroup` | Not approved. Populate only from a VERIFIED source record for the specific airline and value; otherwise null. Do not infer from brand, home country, or ownership assumptions. |
| `OperatingRegion` | Not approved. Populate only from an explicitly defined, source-supported region label; otherwise null. |
| `BusinessModel` | Not approved. Populate only where reliable evidence supports Full Service, Low Cost, Regional, or Charter; otherwise null. |

### 3.2 Roster rules

- The roster is fixed for the baseline reporting period.
- Airline membership must not change during the reporting period. A merger, rebrand, or
  code change requires a new approved scenario and reference version.
- The roster fixes intended identity values; it does not substitute for the source records
  required before `ref_airlines.csv` may be treated as approved reference data.
- The roster does not authorize data generation, schema freeze, or a G3 PASS.

---

## 4. Approval scope and exclusions

### 4.1 In scope if signed

If the owner signs this record, the approval covers:

1. The ten-airline population in Section 3 as the fixed baseline identity population.
2. The identity attribute set and the separation of IATA and ICAO identifiers in D-2 and D-3.
3. The nullable treatment of unsupported optional attributes in D-4.
4. The attribute-level provenance model and source-verification rules in Section 6.
5. The requirement that `ref_airlines.csv` and `ref_airline_sources.csv` exist as the
   controlled identity reference and provenance register before reference approval.
6. The real-identity versus synthetic-performance boundary and disclosure requirement in
   Section 5.
7. The traceability to BR-01, REQ-001, REQ-023 to REQ-027, and T-72 to T-77 recorded in
   Section 8.

### 4.2 Out of scope and exclusions

This record does not:

- Approve OD-02 to OD-22, OP-01, or any other open decision.
- Approve specific `AirlineGroup`, `OperatingRegion`, or `BusinessModel` values.
- Certify that any source record, URL, organization, or verification date exists. Those
  records must be created and verified separately before they can support loaded values.
- Create, populate, or validate `ref_airlines.csv` or `ref_airline_sources.csv`.
- Freeze the data contract, the semantic model, or the reference schemas.
- Authorize data generation, G4 activity, or a G3 PASS.
- Approve financial definitions, KPI definitions, targets, or reporting tolerances.
- Modify Power BI files, project source code, or any of the six active baseline documents.
- Grant rights to use airline names beyond nominative identification in a synthetic
  portfolio. No affiliation, sponsorship, or endorsement by any airline is claimed or implied.
- Authorize the use of real passenger personal information.

---

## 5. Real identity versus synthetic performance boundary

| Domain | Status | Examples |
|---|---|---|
| Airline identity | Real, source-verified | Official airline name, IATA code, ICAO code, home country, country code, and only source-supported optional attributes |
| Airports and routes | Synthetic | Airport codes and names, cities, coordinates, route networks, distances |
| Fleet and aircraft | Synthetic | Aircraft registrations, types, assignments, availability, utilization |
| Customers and bookings | Synthetic | Customer records, segments, bookings, channels, fares, lead times |
| Operations | Synthetic | Schedules, flights, delays, cancellations, disruptions, recovery |
| Revenue, cost, and financials | Synthetic | Revenue, refunds, fees, ancillary revenue, costs, currency conversion, margins |
| Feedback and service | Synthetic | Satisfaction scores, complaints, resolutions, service recovery |
| Reporting outputs | Synthetic simulation | Dashboards, exports, commentary, and portfolio narrative |

**Disclosure rule.** Every dashboard, page, tooltip where practical, and exported result must
display or carry the disclosure:

> "Synthetic Simulation - Not Actual Airline Performance"

**Presentation rule.** No chart title, commentary, filename, or narrative may imply that a
simulated result is the actual performance of Emirates, Qatar Airways, Singapore Airlines,
Air India, IndiGo, British Airways, Lufthansa, Delta Air Lines, Southwest Airlines, Qantas,
or any other real entity.

**Data rule.** Real passenger personal information must not be used. Customer records are
synthetic.

---

## 6. Airline identity source-verification requirements

These requirements restate the controlled rules in Section 3.4 of `03_DATA_CONTRACTS.md`
and bind the future reference build.

### 6.1 Source hierarchy

Preference order:

1. The airline's official corporate source.
2. An official government or civil-aviation registry.
3. An official ICAO or IATA directory where access is documented.
4. A reputable industry reference.

The hierarchy is a preference order, not permission to invent a source. A lower-priority
source may be used only with a recorded reason. Conflicting sources must be recorded, not
silently discarded.

### 6.2 Source types and verification statuses

| Field | Controlled values |
|---|---|
| `SourceType` | `OfficialAirline`, `GovernmentRegistry`, `IndustryAuthority`, `OtherDocumented` |
| `VerificationStatus` | `VERIFIED`, `CONFLICTING`, `UNVERIFIED`, `SUPERSEDED`, `QUARANTINED` |

Only `VERIFIED` records may support a populated required identity attribute in an approved
reference version. `CONFLICTING` and `QUARANTINED` records must not be loaded into
`ref_airlines.csv`.

`SourceVerifiedDate` is an ISO 8601 calendar date (`YYYY-MM-DD`) recording the date the
source was actually checked. It must not be inferred, back-filled, or planned.

### 6.3 Conflict resolution

| Attribute | Precedence |
|---|---|
| Official name | Airline official corporate source |
| Airline group | Airline official corporate source |
| IATA code | Applicable official IATA code registry |
| ICAO code | Applicable official ICAO code registry |
| Home country and country code | Official government or civil-aviation registry |

If a conflict remains unresolved, a required attribute blocks the airline record from
approval; an optional attribute remains null and the conflict is quarantined.

### 6.4 Missing values and quarantine

- Required identity fields must never be blank. If a required value cannot be verified, the
  airline record is incomplete and must not be treated as approved reference data.
- Optional fields remain null. No placeholder, inferred value, or fabricated source may be
  inserted.
- Duplicate, conflicting, unsupported, stale, or malformed source records must be
  quarantined with `SourceRecordID`, reason, and lineage. Quarantined records must not be
  silently promoted.

### 6.5 Lineage, versioning, and reproducibility

- Every populated identity attribute in `ref_airlines.csv` must resolve to at least one
  source record for the same `AirlineIATACode`, `AttributeName`, and `AttributeValue` in the
  selected reference version.
- A source record that supports no loaded value must be marked `QUARANTINED` or
  `SUPERSEDED` with a reason.
- `ReferenceVersion` identifies the exact reference snapshot. Published versions are
  immutable. Any identity correction requires a new version, a reconciliation note, and a
  new source record where the evidence changed.
- The selected version must be recorded in every generation manifest and semantic-model
  refresh configuration.

### 6.6 Prohibition on fabrication

Source URLs, source organizations, verification dates, and verification statuses must be
real and recorded only after verification. A blank or unavailable source is not evidence.
No value may be sourced from memory, assumption, or an unrecorded conversation.

---

## 7. Required provenance reference files

| File | Grain | Key | Required content |
|---|---|---|---|
| `ref_airlines.csv` | One row per approved airline per `ReferenceVersion` | `AirlineIATACode` as primary business key; `AirlineICAOCode` as unique alternate identifier | `AirlineIATACode`, `AirlineICAOCode`, `AirlineName`, `HomeCountry`, `HomeCountryCode`, `IsActive`, `ReferenceVersion`; optional `AirlineGroup`, `OperatingRegion`, `BusinessModel` |
| `ref_airline_sources.csv` | One row per `SourceRecordID` per `ReferenceVersion` | `SourceRecordID` | `SourceRecordID`, `AirlineIATACode`, `AttributeName`, `AttributeValue`, `SourceOrganization`, `SourceURL`, `SourceType`, `SourceVerifiedDate`, `VerificationStatus`, `Notes`, `ReferenceVersion` |

**Current state:** neither file exists. The reference directory contains zero files. This
record does not create or populate them. Creation and population require separate explicit
authorization, real verified sources, and reference-version approval.

---

## 8. Impacted schemas, requirements, and validation tests

### 8.1 Impacted schemas

| Object | Impact |
|---|---|
| `DimAirline` (Section 4.3; Table 6.2.2) | Exactly 10 active rows; unique IATA code, ICAO code, and name; no standalone airline-code column; nullable optional attributes; identity attributes reconcile to the reference |
| `ref_airlines.csv` | Holds the approved population and identity attributes per reference version |
| `ref_airline_sources.csv` | Holds attribute-level provenance for every populated identity value |
| `FactFlightOperations` | `AirlineKey` membership restricted to the approved ten; no orphan airline |
| `FactBookingTransactions` | `AirlineKey` membership restricted to the approved ten; revenue and demand comparisons inherit the population |
| `FactOperatingCosts` | `AirlineKey` membership restricted to the approved ten; cost and CASK comparisons inherit the population |
| `FactDisruptions` | `AirlineKey` membership restricted to the approved ten; disruption comparisons inherit the population |
| `FactCustomerFeedback` | `AirlineKey` membership restricted to the approved ten; satisfaction and complaint comparisons inherit the population |
| Semantic model and reports | Airline filter and slicer paths resolve to `DimAirline`; every airline-level KPI and comparison uses the approved population |

### 8.2 Affected requirements

| Requirement | Impact |
|---|---|
| BR-01 - Multi-airline comparison | Defines the ten real identities and the synthetic boundary for all cross-airline comparison |
| REQ-001 - Real airline identities with synthetic simulations | Primary requirement governed by this decision; closure still requires reference, generator, and validation evidence |
| REQ-023 - Ten approved identities reconciled to the roster with provenance | Population and reconciliation obligation confirmed |
| REQ-024 - Separate unique IATA and ICAO identifiers | Identifier model confirmed; no ambiguous standalone code |
| REQ-025 - Attribute-level provenance register | Provenance model confirmed |
| REQ-026 - Nullable unsupported attributes and quarantine | Nullability and no-inference rules confirmed |
| REQ-027 - Exact reference-to-dimension reconciliation | Reconciliation obligation confirmed |

All listed requirements remain NOT STARTED until implementation evidence exists.

### 8.3 Validation tests

| Test | What it will verify |
|---|---|
| T-72 | `DimAirline` and `ref_airlines.csv` reconcile to the Section 3 roster on IATA, ICAO, name, home country, and country code; exactly ten identities; zero missing, extra, duplicated, or mismatched |
| T-73 | IATA codes match `^[A-Z0-9]{2}$` and are unique |
| T-74 | ICAO codes match `^[A-Z]{3}$` and are unique |
| T-75 | Every populated identity attribute resolves to a selected-version source record with real organization, URL, type, verified date, and VERIFIED status |
| T-76 | Conflicting, unverified, superseded, or quarantined records are handled correctly; required conflicts block approval; optional attributes remain null |
| T-77 | Selected `ref_airlines.csv` version reconciles row-for-row to `DimAirline` with zero unexplained differences |

All tests remain PLANNED. This record does not implement them.

---

## 9. Risks and limitations

| # | Risk or limitation | Impact | Mitigation or treatment |
|---|---|---|---|
| R-1 | Airline identity attributes can change over time, including codes, names, and ownership | Stale reference data and broken reconciliation | Record `SourceVerifiedDate`; version every change; require a new approved reference version; keep the roster fixed only for the baseline period |
| R-2 | Official sources may be unavailable, ambiguous, or conflicting | Required attributes cannot be verified; airline record blocked | Apply the source hierarchy; record conflicts; quarantine unresolved values; block required attributes rather than infer |
| R-3 | Group, region, and business-model attributes are subjective or commercially sensitive | Misleading comparisons and unsupported claims | Leave null unless a reliable source supports the exact value; no inference from home country |
| R-4 | Real airline names may be read as endorsement or as actual performance | Reputational and legal exposure | Synthetic disclosure on every output; explicit no-affiliation statement; no real data; no claim of endorsement |
| R-5 | Reference files do not yet exist and no source records have been verified | Decision could be mistaken for completed reference approval | This record approves population and rules only; reference approval requires separate evidence and authorization |
| R-6 | IATA and ICAO codes can be reused or reassigned across time | Identity collision or wrong airline mapping | Bind codes to the reference version and verified date; treat changes as a new version; never reuse a code silently |
| R-7 | Scope pressure to generate data before governance closes | Premature G4 activity and rework | G3 remains NOT STARTED; G4 remains BLOCKED; this record does not authorize generation |
| R-8 | Record remains unsigned | OD-01 stays open; G3 cannot pass | Keep status PENDING OWNER SIGNATURE until the owner signs and dates the record |

**Limitations.** This record does not verify any source, does not establish that the roster
values are current as of the signature date, and does not validate any generated data. It
records the approved population and the rules that future reference and validation work must
satisfy.

---

## 10. Alternatives considered and rejected

| Alternative | Reason rejected |
|---|---|
| Retain fictional airline identities | Does not meet the project requirement for real, source-verified identities and traceable provenance; the controlled migration already replaced the fictional population |
| Retain a single standalone `AirlineCode` | Ambiguous between IATA and ICAO, weaker validation, and collision-prone; separate identifiers are required |
| Use a different or larger roster | Breaks baseline stability and comparability; the ten-airline roster is the approved intended population |
| Infer `AirlineGroup`, `OperatingRegion`, or `BusinessModel` from home country or brand | Unsupported inference; would create fabricated identity attributes |
| Populate reference CSVs from general knowledge without sources | Violates the no-fabrication rule and the provenance requirement |
| Treat the migration report as the formal approval | The report records a documentation change, not an owner decision; OD-01 requires an owner-signed record |

---

## 11. Rationale

The project compares airlines, so the airline dimension must be stable, identifiable, and
defensible. Real identity attributes make the portfolio recognizable and allow the
documentation to be checked against public sources. Synthetic performance data protects the
project from misrepresenting any airline and keeps the analytical work reproducible without
using confidential or personal data.

Separating IATA and ICAO codes removes an ambiguity that would otherwise propagate into
keys, validation, and reporting. Attribute-level provenance makes each identity value
auditable instead of relying on undocumented assumptions. Nullable optional attributes
prevent the project from inventing group, region, or business-model values that it cannot
support.

For these reasons, the proposed decision is to approve the ten-airline population and the
identity rules in this record, while explicitly withholding approval of reference values,
schema freeze, and data generation until their own evidence exists.

---

## 12. Formal approval block

To be completed only by the decision owner at signature. No field in this block is filled
in the draft.

| Field | Entry |
|---|---|
| Decision ID | OD-01 |
| Decision title | Real airline identity population |
| Decision owner / approver | KH Mohammad Farhan |
| Selected option | Approve the ten-airline roster and identity rules in Sections 2 to 7 |
| Rejected alternatives | As recorded in Section 10 |
| Rationale | As recorded in Section 11 |
| Impact on facts, dimensions, and reference datasets | As recorded in Section 8.1 |
| Impact on KPIs, calculations, and reporting | All airline-level KPIs, comparisons, filters, and report pages inherit the approved population |
| Affected requirements and validation tests | BR-01, REQ-001, REQ-023 to REQ-027, T-72 to T-77 |
| Supporting evidence | This record; `03_DATA_CONTRACTS.md` v1.4; `OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt`; verified pre-write backup |
| Owner confirmation | [BLANK - owner to confirm] |
| Decision date | [BLANK - owner to enter at signature] |
| Owner signature | ____________________________________________ |
| Approval evidence reference | [BLANK - signed copy location or reference] |
| Formal status after signature | APPROVED (only after all fields above are completed and verified) |

**Owner attestation (to be affirmed at signature):**

- I have reviewed the roster, scope, exclusions, boundary, provenance rules, impacts, and
  risks in this record.
- I approve the ten-airline population and the identity rules as the baseline for OD-01.
- I understand that this approval does not create or populate reference CSV files, does not
  freeze the schema, does not authorize data generation, and does not close G3.
- I understand that all operational and financial results remain synthetic and must be
  disclosed as such.

Signature: ______________________________  Date: ____________________

---

## 13. Status and next steps

**Current formal status: PENDING OWNER SIGNATURE.**

OD-01 remains open. The roster is approved only as the intended population. G3 remains NOT
STARTED. G4 remains BLOCKED. Data generation is not authorized.

If the owner signs this record, the following would still require separate controlled
action and are not performed by this draft:

1. Enter the decision date, owner confirmation, signature, and approval evidence reference.
2. Verify the completed record and change OD-01 to APPROVED in the decision register and
   approval record, under a controlled documentation update.
3. Create and populate `ref_airlines.csv` and `ref_airline_sources.csv` only under separate
   explicit authorization, using real verified sources.
4. Implement and run T-72 to T-77, recording evidence in the QA results directory.
5. Continue the remaining critical G3 decisions, schema freeze, reference-version approval,
   validation implementation, and gate review.

Until signature, no status change is permitted.

---

## 14. Evidence register

| Evidence | Reference | Status |
|---|---|---|
| Data contract baseline | `docs/03_DATA_CONTRACTS.md` version 1.4 | Current; OD-01 pending |
| Migration final report | `docs/OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt` | Complete; 99 checks passed |
| Pre-write backup | `docs/od01_real_airline_migration_apply_backup_20261101_204216/` | Verified against baseline |
| Project scope roster | `docs/01_PROJECT_SCOPE.md` Section 2.1 | Current; formal record pending |
| Business requirements | `docs/02_BUSINESS_REQUIREMENTS.md` BR-01 | Current |
| Master build prompt | `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt` | Current |
| Requirements traceability | `docs/REQUIREMENTS_TRACEABILITY.md` REQ-001, REQ-023 to REQ-027 | All NOT STARTED |
| Progress ledger | `docs/PROGRESS_LEDGER.md` | G3 NOT STARTED; G4 BLOCKED |

**Baseline document hashes at draft preparation (SHA256):**

| Document | SHA256 |
|---|---|
| `01_PROJECT_SCOPE.md` | `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` |
| `02_BUSINESS_REQUIREMENTS.md` | `E2FCC8132981C96720E572F01EF353C255CA6BE91F27854950D93FF0DFC1DB6E` |
| `03_DATA_CONTRACTS.md` | `EB1DE0E1B80E9E30B4905740BDD66AB96657073119D63C49AA48445CB06446E2` |
| `AEROVISION_360_MASTER_BUILD_PROMPT.txt` | `17BD2C6FCADB9E2A917D047B2B2D9716E21CB1709B5A46ABF01AB2833C56D429` |
| `REQUIREMENTS_TRACEABILITY.md` | `1AD225D00EA6D5808B6E0050DBFCE10F84CBAEF2B66DE70C4362370BBA9CC751` |
| `PROGRESS_LEDGER.md` | `42A00E3A41A9ABBC6B9F930BFE39DD369E6B9681B9F56194921E7145E6F8A7A3` |

---

## 15. Draft control

**Prepared for:** KH Mohammad Farhan, project owner
**Preparation basis:** `03_DATA_CONTRACTS.md` v1.4; OD-01 migration final report; the six
active baseline documents
**Document status:** DRAFT - NOT SIGNED - NOT AN APPROVAL
**Effect on OD-01:** none; decision remains PENDING
**Effect on G3:** none; remains NOT STARTED
**Effect on G4:** none; remains BLOCKED

This draft must not be cited as approval evidence. Only a completed, signed, and dated copy
may close OD-01.
