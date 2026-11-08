# AEROVISION 360 — OD-01B Airline Identity and Reference Decision

**Document type:** Formal decision record — airline identity and reference model  
**Decision ID:** OD-01B  
**Decision title:** Airline identity, key, provenance, lifecycle, and reference-version model  
**Parent decision:** OD-01 (split into OD-01A and OD-01B)  
**Decision owner / approver:** KH Mohammad Farhan  
**Formal status:** OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING  
**Decision date:** [BLANK — to be completed by the owner at signature]  
**Owner approval evidence:** [BLANK — to be completed at signature]  
**Record version:** 0.2  
**Prepared:** 2026-11-01  
**Revised:** 2026-11-02  
**Revision authorization:** D-03 — owner-authorized controlled revision, recorded in `OD01_REVISION_0.2_CHANGE_RECORD.md`  
**Governing baseline:** `03_DATA_CONTRACTS.md` version 1.5  
**Related population record:** `OD01A_AIRLINE_POPULATION_DECISION.md`  
**Related change record:** `OD01_REMEDIATION_CHANGE_RECORD.md`  
**Revision change record:** `OD01_REVISION_0.2_CHANGE_RECORD.md`

> **STATUS NOTICE — NOT A FORMAL APPROVAL**
>
> The project owner confirmed the eight design choices recorded in
> `OD01_OWNER_DECISION_CONFIRMATION.md`. This record converts the identity,
> reference-version, lifecycle, and Power BI choices into a decision record for
> review and signature. It is not signed, has no approval date, and does not
> constitute formal approval of OD-01A or OD-01B. G3 gate execution NOT STARTED; G3 design documentation PREPARED — DRAFT (documentation state, not approval); G3 formal approval NOT FORMALLY APPROVED; G4
> remains BLOCKED. No reference CSV, reference manifest, synthetic dataset,
> schema freeze, Python pipeline, Power Query query, semantic model, DAX
> measure, Power BI report, or dashboard has been created or authorized by this
> record. No independent reviewer is assigned and no external verification is
> recorded.
>
> **Revision 0.2 (2026-11-02):** D-03 authorizes only the controlled corrections
> in this revision: current scope evidence, narrow approval scope, approval-record
> structure, reviewer/compensating-control language, re-audit preconditions, and
> revision history. D-05 remains PENDING; `BusinessModelClass` must not be
> populated on the basis of this revision. No independent reviewer has performed
> the review. AI-assisted review is not independent assurance. Owner self-review
> is a separate activity and is not recorded as completed evidence. No signature,
> approval date, or reviewer identity is recorded. D-04 and D-06 to D-08 remain
> PENDING.

## 1. Purpose and authority

This record defines how the ten airline identities are keyed, versioned,
sourced, reconciled, and represented in the warehouse and Power BI model. It is
the identity and reference-version decision; OD-01A is the population decision.

The authority for this record is the owner confirmation recorded in
`OD01_OWNER_DECISION_CONFIRMATION.md` (SHA-256
`AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`).
The confirmation records the eight choices as `OWNER-CONFIRMED`; it does not
record a signature, an approval date, or independent assurance. This record
does not modify the audit report, remediation specification, owner resolution,
or original OD-01 draft.

Revision 0.2 is authorized by D-03 as a documentation change only. D-03 does
not approve OD-01B, does not approve the other OD-series decisions, and does not
advance G3 or G4. D-04 and D-06 to D-08 remain PENDING. D-05 remains PENDING and
does not authorize `BusinessModelClass` population. The revision is recorded in
`OD01_REVISION_0.2_CHANGE_RECORD.md`.

## 2. Decision statement

The owner-confirmed design is:

1. OD-01 is split into OD-01A (population) and OD-01B (identity and reference
   model). Each requires a separate formal signature.
2. `AirlineId` is the durable business identity. `AirlineKey` is the permanent
   warehouse surrogate used by facts and Power BI relationships. They are not
   interchangeable.
3. IATA and ICAO codes are mutable attributes, unique within a reference
   version. They are not primary keys, foreign keys, or provenance joins.
4. `AirlineName` is the commercial brand. `LegalName` is optional and remains
   in the reference/provenance layer only; it is not a `DimAirline` column.
5. `HomeCountry` is the country of the airline's principal headquarters or
   domicile. `AirlineGroup` is the optional ultimate parent company or group
   brand and is not inferred.
6. `BusinessModelClass` is an optional analytical classification, not a
   source-verified identity attribute. `OperatingRegion` is removed from the
   airline identity model; analytical region is derived from route and airport
   geography. D-05 remains PENDING; this revision does not authorize a populated
   `BusinessModelClass` baseline or a mapping/rubric.
7. The minimal lifecycle uses `IsActive` and `StatusEffectiveDate`.
   `LifecycleStatus` and `MergedIntoAirlineId` are deferred and are not columns.
8. `DimAirline` is Type 1. Immutable reference snapshots preserve build
   reproducibility, but Type 1 does not preserve as-was historical identity
   labels. Type 2 is deferred until a future requirement demands it.
9. The reference manifest is the authoritative approval record.
   `DimAirline.ReferenceVersion` is technical lineage only. Every generation
   and refresh pins exactly one approved reference version and validates key
   consistency.
10. The airline key map is controlled and immutable after approval. The same
    `AirlineId` always resolves to the same `AirlineKey`, independent of row
    order, rebuild, or database identity sequence. Historical facts are never
    re-keyed.
11. Reference-version approval uses `G3-RV-01`, not an OD-series decision.
    OD-23 is rejected and is not created. REQ-028 and T-78 are retained.
12. The exact unconditional disclosure
    `Synthetic Simulation — Not Actual Airline Performance` is required on
    every report page, tooltip while a page is visible, and exported result.

**Formal status:** the design is owner-confirmed; the record is not formally
signed or approved.

### 2.1 Population and reporting boundary

The population is exactly the ten real airline identities listed in
`OD01A_AIRLINE_POPULATION_DECISION.md`, Section 3. The fixed reporting period is
2025-10-01 through 2026-09-30, inclusive. The inclusion and exclusion criteria
are those in OD-01A Section 4: one row per distinct commercial airline brand in
the fixed roster; no subsidiary, franchise, alliance, group consolidation,
additional airline, real passenger personal information, or actual performance
claim. The identity attributes are real and must be source-verified before
reference approval; all operational, customer, booking, revenue, cost,
disruption, feedback, and financial records are synthetic. Every report page,
tooltip while a page is visible, and exported result must carry the exact
disclosure `Synthetic Simulation — Not Actual Airline Performance`.

OD-01B does not re-approve the population. It defines the identity and
reference model used to represent the population fixed by OD-01A. Both records
require separate formal signatures.

## 3. Key hierarchy and proposed allocation

| Identifier | Type | Scope | Assigned by | Mutable? | Reused? | Used for | Not used for |
|---|---|---|---|---|---|---|---|
| `AirlineId` | String(20) | Master data, reference, provenance | Project governance, once per airline | No | Never | Durable identity, provenance join, cross-version lineage | Fact joins, Power BI relationships |
| `AirlineKey` | Int32 | Warehouse / `DimAirline` | Controlled key map, once per airline | No | Never | `DimAirline` primary key; fact foreign keys; Power BI relationships | Source identity, provenance, business-key matching |
| `AirlineIATACode` | String(2) | Airline attribute | Verified source, per reference version | Yes, by new version | A code may be reassigned only with explicit retirement and a new version | Display, validation, version-qualified uniqueness | Primary key, foreign key, provenance join |
| `AirlineICAOCode` | String(3) | Airline attribute | Verified source, per reference version | Yes, by new version | Same rule as IATA | Display, validation, version-qualified uniqueness | Primary key, foreign key, provenance join |
| `AirlineName` | String(100) | Airline attribute | Verified source, per reference version | Yes, by new version | A brand may change only through a new version | Display, version-qualified uniqueness | Primary key, legal-entity proof, provenance join |
| `LegalName` | String(200) | Reference/provenance only | Verified source, per reference version | Yes, by new version | No | Optional legal-entity context | `DimAirline` column, report slicer, key |

**Proposed administrative allocation (this revision does not approve the
mapping; it is a design baseline, not a source-verified identity fact):**

| # | Airline | `AirlineId` | `AirlineKey` |
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

**Key-map rules:**

- The mapping is stored with or hashed into the approved reference manifest.
  It is not a separate enterprise airline registry table.
- A new airline receives the next unused `AirlineId` and `AirlineKey`. A
  retired airline retains both identifiers. A successor entity receives a new
  pair; old facts retain the old key.
- The map must be loaded by every clean rebuild. A missing, duplicate, or
  inconsistent map blocks generation and refresh.
- No key is assigned from CSV row order, sort order, `row_number`, hash order,
  random selection, database `IDENTITY`, auto-increment, or a newly generated
  sequence.

## 4. `DimAirline` attribute dictionary

| Column | Type | Null | Rule |
|---|---|---|---|
| `AirlineKey` | Int32 | No | Permanent positive surrogate; primary key; unique; hidden from report view. |
| `AirlineId` | String(20) | No | Durable business identity; format `^AIR-[0-9]{4}$`; unique; never reused; not a physical relationship key. |
| `AirlineIATACode` | String(2) | No | Uppercase alphanumeric; unique within `ReferenceVersion`; mutable only through a new version; not a key. |
| `AirlineICAOCode` | String(3) | No | Uppercase letters; unique within `ReferenceVersion`; mutable only through a new version; not a key. |
| `AirlineName` | String(100) | No | Commercial brand; unique within `ReferenceVersion`; not the legal entity name. |
| `AirlineGroup` | String(100) | Yes | Optional ultimate parent company or group brand from a `VERIFIED` source; null when independent or unverified; no inference. |
| `HomeCountry` | String(100) | No | Country of principal headquarters or domicile; not incorporation country, AOC state, or ultimate ownership. |
| `HomeCountryCode` | String(2) | No | ISO 3166-1 alpha-2 code for `HomeCountry`. |
| `BusinessModelClass` | String(50) | Yes | Optional analytical classification: Full Service, Low Cost, Regional, Charter, Hybrid/Other, Unknown. Not source-verified identity; no identity provenance; null allowed; label as analytical. |
| `IsActive` | Boolean | No | Airline operating status. True for the ten baseline airlines. False for a suspended or ceased airline in a later approved version. |
| `StatusEffectiveDate` | Date | Yes | Date the current `IsActive = FALSE` status took effect. Required when `IsActive = FALSE`; null for the baseline active state. |
| `ReferenceVersion` | String(30) | No | Hidden technical lineage field; format `AIR-YYYY-MM-DD-NNN`; not approval. |

**Excluded columns:** `OperatingRegion`, `LegalName`, `LifecycleStatus`,
`MergedIntoAirlineId`. `OperatingRegion` is not an identity attribute;
`LegalName` is reference-only; the other two are deferred.

**D-05 status:** DECIDED — Owner decision GOV-D-05 communicated. `BusinessModelClass` remains an optional, nullable analytical column with no baseline values populated (null baseline). No mapping or rubric is approved at this time. This decision is recorded in the OD-01B §11.4 approval block. Formal signature and actual date pending.

## 5. Reference datasets and provenance

The reference design uses `ref_airlines.csv` and `ref_airline_sources.csv`.
Contract Section 3.4 is the controlling schema.

**`ref_airlines.csv`:**

- Grain: one row per `AirlineId` per `ReferenceVersion`.
- Primary key: `AirlineId` + `ReferenceVersion`.
- Required: `AirlineId`, `AirlineIATACode`, `AirlineICAOCode`, `AirlineName`,
  `HomeCountry`, `HomeCountryCode`, `IsActive`, `ReferenceVersion`.
- Optional: `LegalName`, `AirlineGroup`, `StatusEffectiveDate`.
- Excluded: `OperatingRegion`, `BusinessModelClass`, `LifecycleStatus`,
  `MergedIntoAirlineId`.

**`ref_airline_sources.csv`:**

- Grain: one row per source-attribute assertion per `ReferenceVersion`.
- Primary key: `SourceRecordID`.
- Provenance joins on `AirlineId`, `AttributeName`, and `AttributeValue`, never
  on IATA or ICAO.
- Every populated identity attribute requires exactly one authoritative
  `VERIFIED` record in the selected version.
- Each `VERIFIED` record requires a real source organization, URL, source type,
  retrieval date, verification date, verification method, and either a SHA-256
  evidence hash or a read-only archive reference.
- `CONFLICTING`, `UNVERIFIED`, `SUPERSEDED`, and `QUARANTINED` records remain
  recorded but cannot support a populated attribute in an approved version.
- Unsupported optional attributes remain null. No placeholder, inference, or
  fabricated source is allowed.
- `OperatingRegion` and `BusinessModelClass` are excluded from identity
  provenance because they are not source-verified identity attributes.

The detailed source hierarchy, controlled values, conflict resolution,
quarantine reasons, evidence durability, and staleness rules are in contract
Section 3.4. This record does not create the CSV files.

## 6. Lifecycle and historical semantics

**Minimal lifecycle:** `IsActive` is the operating status. `StatusEffectiveDate`
is required when `IsActive = FALSE` and null for the baseline active state.
`LifecycleStatus` and `MergedIntoAirlineId` are deferred. A future requirement
that needs detailed status transitions or merger lineage must create a new
decision and a new schema version.

**Type 1 baseline:** `DimAirline` holds one row per airline. An identity
attribute change is applied to the current row only after a new reference
version is approved. Historical facts retain `AirlineKey` and are not re-keyed.
This preserves build reproducibility from an immutable snapshot, but it does
not preserve the identity label that was displayed when an old fact occurred.

**Type 2 trigger:** Type 2 is deferred. It becomes necessary only if a future
requirement explicitly demands as-was identity reporting, such as a report that
must show the airline name or code in force on each historical event date. Until
that requirement exists, Type 1 is the approved baseline and the limitation must
be disclosed in documentation.

## 7. Reference version, manifest, key map, and gate evidence

**`ReferenceVersion` format:** `AIR-YYYY-MM-DD-NNN`, regex
`^AIR-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$`. Published versions are immutable.
A correction requires a new version, a reconciliation note, and a new source
record where the evidence changed.

**Authoritative manifest:** `data/manifests/reference_versions.csv` is the
authoritative approval register (design only; not created). It records
`ReferenceVersion`, `EffectiveFrom`, `EffectiveTo`, `IsCurrent`, `Status`,
`ApprovedBy`, `ApprovalDate`, `ManifestHash`, `SupersedesReferenceVersion`, and
`ReconciliationNote`. Exactly one version may be `IsCurrent = TRUE` for a
generation or refresh. `ApprovedBy` and `ApprovalDate` remain blank until a real
approval occurs.

**Lineage versus approval:** `DimAirline.ReferenceVersion` identifies the
snapshot used to build the row. It is not an approval record and must be hidden
from report view. The manifest is the approval record.

**One-version rule:** every generated dataset and semantic-model refresh pins
exactly one approved `ReferenceVersion`. Mixed versions are prohibited. The
Power BI model exposes `SelectedReferenceVersion`, validates it against the
manifest and `DimAirline.ReferenceVersion`, and blocks refresh on mismatch.

**`G3-RV-01`:** the reference-version gate artifact records the owner, criteria,
exact version, file hashes, source evidence, T-75/T-76 results, T-78 plan or
results, and refresh configuration. It is not an OD-series decision. OD-23 is
rejected and is not created.

**T-78 sub-checks:** T-78-01 one distinct version in `ref_airlines.csv`;
T-78-02 one distinct version in `ref_airline_sources.csv`; T-78-03 manifest
version; T-78-04 `DimAirline.ReferenceVersion`; T-78-05 Power BI
`SelectedReferenceVersion`; T-78-06 manifest status `APPROVED`; T-78-07 ten
active `AirlineId` values and ten unique `AirlineKey` values; T-78-08 one
authoritative `VERIFIED` record per populated attribute; T-78-09 no key
reassignment; T-78-10 reconciliation note for every identity change and no
mixed-version facts. A mismatch, unapproved version, missing key map, reassigned
key, orphan fact key, or mixed version blocks generation and refresh.

## 8. Power BI relationship and disclosure rules

- `DimAirline` joins every airline fact on `AirlineKey`. Do not join on
  `AirlineId`, IATA, ICAO, or name.
- Hide `AirlineKey` and `ReferenceVersion` from report view. Keep `AirlineId`
  only as a non-slicer lineage attribute.
- Do not activate a second `DimAirline` path to `FactFlightOperations` through
  `DimAircraft`. Use a role-playing fleet dimension or an approved measure.
- Expose exactly one `SelectedReferenceVersion`; validate it against the
  approved manifest and the `DimAirline` lineage column.
- Every report page must show the exact unconditional disclosure
  `Synthetic Simulation — Not Actual Airline Performance` in a persistent
  footer or header. Every tooltip while a page is visible and every exported
  result must carry it. There is no “where practical” exception.
- T-79 verifies the Unicode code points, persistent placement, tooltip while
  visible, export template, rendered screenshot, and report extract metadata.
  T-79 is `BLOCKED` because no rendered report exists.

## 9. Change control

| Tier | Change | Required control |
|---|---|---|
| 1 | Typo, formatting, or documentation clarification with no semantic effect | Documented correction; no new reference version |
| 2 | IATA, ICAO, brand name, legal name, group, home country, or active status change | New `ReferenceVersion`, new or updated source record, reconciliation note, T-75/T-76/T-78 evidence, `G3-RV-01` update |
| 3 | New airline, successor entity, merger, or rebrand that changes the durable identity | New `AirlineId` and `AirlineKey`; population decision update; new reference version; no reuse or re-keying of old facts |
| 4 | Change to the ten-airline population or the identity/reference decision itself | New formal decision record and owner approval; do not silently edit this record |

A code change never silently rewrites historical facts. A retired airline
retains its identifiers. A successor receives a new pair.

## 10. Evidence index

**Shared evidence:** see `OD01A_AIRLINE_POPULATION_DECISION.md`, Section 6,
evidence IDs E-01 to E-12. That is the single shared evidence index for both
records. Shared E-07 is corrected per owner decision D-1 (Option A) and cites
`docs/01_PROJECT_SCOPE.md` version 1.1, SHA-256
`5282EFFAD84FF72C84DB3864B3ECFF2B99C6DD8139850F341B2A4148FA7DC627`, 7,176
bytes. The former hash `9A9EEA...` is historical backup evidence only, not a current
approval citation.

**OD-01B-specific evidence:**

| Evidence ID | Evidence | Classification | Location / status |
|---|---|---|---|
| B-01 | Contract v1.5 identity and reference rules | `RECORDED DESIGN — PENDING REVIEW` | `docs/03_DATA_CONTRACTS.md` Sections 3.4, 4.3, 6.2.2, 7, 8.4, and 13 |
| B-02 | Remediation specification identity, historical, provenance, and gate design | `RECORDED` | `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` Sections 4 to 8 and 13.2 |
| B-03 | Independent audit findings H-01 to H-07 and related actions | `RECORDED` | `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` |
| B-04 | Proposed key map | `RECORDED DESIGN — PENDING FORMAL APPROVAL` | This record, Section 3 |
| OD01B-B-05 | Reference manifest | `NOT CREATED` | `data/manifests/reference_versions.csv` design only |
| B-06 | T-78 plan and results | `NOT EXECUTED` | Contract Section 13; `qa/results/airline_identity_versions.csv` planned |
| B-07 | `G3-RV-01` reference-version approval | `NOT EXECUTED` | Gate artifact planned; not an OD-series decision |
| OD01B-B-08 | Independent reviewer | `NOT ASSIGNED` | Approval block, Section 11 |

## 11. Formal approval block

### 11.1 Re-audit preconditions

Formal signature is not permitted until all of the following are recorded:

1. Revision 0.2 is verified and its before/after hashes are recorded in `OD01_REVISION_0.2_CHANGE_RECORD.md`.
2. Shared E-07 cites the current scope v1.1 hash `5282EFFAD84FF72C84DB3864B3ECFF2B99C6DD8139850F341B2A4148FA7DC627` (verified per owner decision D-1, Option A).
3. H-04 is re-audited after R-09 to R-11 are incorporated into `PROJECT_RISK_REGISTER.md`.
4. H-05 is re-audited after the G3 split-status wording is incorporated into `PROGRESS_LEDGER.md`.
5. M-07 and M-12 are re-audited after the approval workflow and narrow approval scope are incorporated.
6. Owner self-review is executed and recorded as owner self-review; it is not independent review.
7. The compensating-control challenge is documented; AI-assisted review must not be described as independent assurance.
8. GOV-B-05 (owner-confirmation addendum) is resolved by GOV-D-04, and GOV-B-08 (evidence retention) is resolved by GOV-D-08, or the signature is explicitly withheld.
9. D-05 remains PENDING; no `BusinessModelClass` value is populated on the basis of this approval.
10. A fresh re-audit records the final finding status and confirms that no signature blocker remains.

### Prerequisite Status Summary (Updated 08 November 2026)

| # | Precondition | Status | Evidence |
|---|---|---|---|
| 1 | Revision 0.2 verified; before/after hashes recorded | PASS | `OD01_REVISION_0.2_CHANGE_RECORD.md` §2 |
| 2 | Shared E-07 cites current scope v1.1 hash | PASS | `docs/01_PROJECT_SCOPE.md` SHA-256 `5282EF...` (7,176 bytes), verified per D-1 |
| 3 | H-04 re-audited after R-09 to R-11 | PASS | `PROJECT_RISK_REGISTER.md` R-09–R-11 recorded; `IsActive` + `StatusEffectiveDate` columns VERIFIED in `semantic_model.json` dim_airline; technical re-audit completed 08 Nov 2026 |
| 4 | H-05 re-audited after G3 split-status wording | PARTIALLY VERIFIED | `PROGRESS_LEDGER.md` updated; G3 split-status wording incorporated; test summary corrected; `ReferenceVersion` column VERIFIED in dim_airline; `SelectedReferenceVersion` measure NOT yet implemented |
| 5 | M-07 and M-12 re-audited | PARTIALLY VERIFIED | M-12 narrow approval scope VERIFIED; M-07 compensating controls DOCUMENTED but NOT EXECUTED |
| 6 | Owner self-review executed and recorded | FAIL | `CC01_OWNER_SELF_REVIEW.md` NOT EXECUTED — requires personal owner execution |
| 7 | Compensating-control challenge documented | PARTIAL | Defined but not executed; no reviewer acceptance |
| 8 | GOV-B-05 resolved by GOV-D-04; GOV-B-08 resolved by GOV-D-08 | PARTIAL | GOV-D-04 APPROVED (08 Nov 2026); GOV-D-08 AUTHORIZED (08 Nov 2026) |
| 9 | D-05 remains PENDING; no BusinessModelClass value populated | PASS | GOV-D-05 null-baseline decision recorded in §4 and §11.4 |
| 10 | Fresh re-audit records final finding status | PENDING | No fresh re-audit completed |

**Current re-audit status: PENDING — Preconditions 4 (partial), 5 (partial), 6, 7, and 10 not fully satisfied.**

**OD-01B Approval Status: BLOCKED** — Depends on OD-01A formal approval first. OD-01A prerequisites 4, 5, 6, 7, and 9 are not fully satisfied. OD-01B §11.4 signature cannot be recorded until OD-01A is formally approved and OD-01B prerequisites 4, 5, 6, 7, and 10 are met.

**Technical re-audit results (08 November 2026):**
- H-04 (R-09 airline lifecycle): VERIFIED
- H-05 (R-10 reference-version change): PARTIALLY VERIFIED
- M-07 (compensating controls): DOCUMENTED but NOT EXECUTED
- M-12 (approval scope): VERIFIED

### 11.2 Compensating-control and reviewer limitation

The owner accepted the compensating-control route under D-01 and the
no-independent-review limitation under D-02. No independent reviewer has
performed the review. AI-assisted review is not independent assurance. Owner
self-review is a separate activity and has not been executed or recorded as
evidence in this revision.

**Reviewer route:** compensating-control route accepted; independent reviewer
not assigned.  
**Compensating-control execution:** `PARTIAL — NOT CLOSED`; owner self-review
is `NOT EXECUTED`, and the documented challenge is not a completed independent
review.  
**Independent assurance:** `NOT CLAIMED`.  
**D-2 — Independent reviewer limitation (owner communicated):** No independent reviewer is assigned for AEROVISION 360. The Project Owner accepts the D-02 compensating-control route: owner self-review (CC-01) and documented compensating controls (CC-01 through CC-10) in lieu of independent review. No independent assurance is claimed. Formal acceptance recorded 08 November 2026 in `CC01_OWNER_SELF_REVIEW.md` §7.5.  
**Residual concerns:** H-04, H-05, M-07, and M-12 remain open pending re-audit;
B-03, B-04, OD01B-B-05 (reference manifest), and OD01B-B-08 (independent reviewer) remain open until the related decisions and evidence
are completed.


### 11.3 Approval scope and exclusions

> This approval covers the governing airline identity, key, provenance,
> lifecycle, reference-version, manifest, and Power BI identity/disclosure rules
> in OD-01B Sections 2, 4, 5, 6, and 8. Sections 3 and 7 are acknowledged design
> baselines, not a schema freeze. The proposed airline key map in Section 3
> remains excluded from OD-01B approval; it becomes immutable only after
> G3-RV-01 reference-version approval. This approval does not create or populate
> reference CSVs, approve a schema freeze, authorize synthetic data generation,
> production ETL, Power Query, Power BI, G3, or G4.

**Explicit exclusions:** schema freeze; reference-data creation or population;
synthetic-data generation; production Python/ETL; Power Query; semantic model;
DAX; Power BI reports/dashboards; G3 or G4 advancement; `G3-RV-01` execution;
and any Git operation. The key map in Section 3 remains a proposed administrative
allocation, not a source-verified identity fact.

### 11.4 Approval record

| Field | Entry |
|---|---|
| Decision | `[ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION` |
| Approval scope | OD-01B Sections 2, 4, 5, 6, and 8 only; see Section 11.3 |
| Exclusions | Schema freeze; reference CSVs; synthetic data; production ETL; Power Query; semantic model; DAX; Power BI; G3; G4; `G3-RV-01`; Git |
| Owner name | KH Mohammad Farhan |
| Owner decision | `[BLANK — to be completed by the owner]` |
| Owner signature | `[BLANK — no signature recorded]` |
| Actual approval date | `[BLANK — no approval date recorded]` |
| Approval conditions | GOV-D-05 condition: `BusinessModelClass` remains an optional, nullable analytical column with no baseline values populated (null baseline). No mapping or rubric is approved at this time. `[BLANK — additional conditions to be completed at signature]` |
| Reviewer route | Compensating-control route accepted under D-01/D-02; independent reviewer not assigned |
| Compensating-control acceptance | D-01/D-02 accepted; execution not complete |
| Reviewer limitation statement | No independent reviewer; AI review is not independent assurance |
| Reviewer name / role / organization | `[BLANK — no reviewer assigned]` |
| Reviewer independence | `[ ] Independent   [ ] Not independent   [X] N/A — no reviewer` |
| Reviewer result | `[ ] CONCUR   [ ] CONCUR WITH RESERVATIONS   [ ] DISSENT   [X] N/A — no reviewer` |
| Reviewer signature / date | `[BLANK — no reviewer signature]` |
| Residual concerns | H-04: PARTIALLY VERIFIED — CLOSED AT DOCUMENTATION LEVEL; H-05: PARTIALLY VERIFIED; M-07: PARTIALLY VERIFIED; M-12: PARTIALLY VERIFIED; B-03: VERIFIED — CLOSED AT DOCUMENTATION LEVEL; B-04: PARTIALLY VERIFIED; GOV-B-05: PENDING OWNER APPROVAL — GOV-D-04 RESOLVED; addendum accepted 2026-11-06; GOV-B-08: PENDING OWNER APPROVAL — GOV-D-08 PENDING; no independent assurance |
| Re-audit record | `[BLANK — PENDING]` |
| Scope v1.1 SHA-256 | `5282EFFAD84FF72C84DB3864B3ECFF2B99C6DD8139850F341B2A4148FA7DC627` (supersedes former hash `9A9EEA...` per owner decision D-1) |
| Contract v1.5 SHA-256 | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` |
| Signed-copy path | `[BLANK — D-08 PENDING; no docs/approvals/ structure]` |
| Signed-copy SHA-256 | `[BLANK — no signed copy exists]` |
| Retention confirmed | `[ ] Yes   [X] No — D-08 PENDING` |
| Verification date / result | `[BLANK — PENDING]` |

**Formal signature:** ______________________________  
**Approval date:** ______________________________  
**Approval evidence:** ______________________________

**Approval status:** PENDING. This record is not approved for reference-data
creation, synthetic-data generation, schema freeze, Power BI implementation, or
a G3/G4 advance.

## 12. What this record does not authorize

- It does not create or populate `ref_airlines.csv`,
  `ref_airline_sources.csv`, or any reference manifest.
- It does not create synthetic data, Python code, Power Query queries, a
  semantic model, DAX measures, Power BI reports, or dashboards.
- It does not freeze the schema or approve a data dictionary.
- It does not advance G3 or G4.
- It does not claim that source verification, independent review, or external
  assurance has occurred.
- It does not approve OD-01A or any other OD-series decision.
- It does not authorize a Git operation.

**Next gate:** complete the re-audit preconditions in Section 11.1 and resolve
the remaining owner decisions, then obtain the owner's formal signature and
approval date. `G3-RV-01` and the remaining G3 entry criteria follow. No
reference data or synthetic data may be created before those gates are met.

## 13. Revision history

| Version | Date | Change | Authorization / status |
|---|---|---|---|
| 0.1 | 2026-11-01 | Initial decision record prepared from the owner-confirmed design. | Prepared; no signature. |
| 0.2 | 2026-11-02 | Corrected shared scope evidence; added narrow approval scope/exclusions; added reviewer/compensating-control limitation; added complete approval fields and re-audit preconditions; added D-05 pending note; added revision history. | D-03 owner-authorized documentation change; no signature; D-04 and D-06 to D-08 pending. |

No revision is a formal approval. No revision enters a signature, approval date,
or reviewer identity.
