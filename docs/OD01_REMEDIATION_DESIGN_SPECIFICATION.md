# AEROVISION 360 — OD-01 Remediation Design Specification

**Design specification for correcting the OD-01 decision record and its governing baseline**

| Document control | Value |
|---|---|
| Document | `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` |
| Version | 1.0 |
| Status | **DESIGN COMPLETE — AWAITING OWNER DECISIONS** |
| Prepared | 2026-11-01 |
| Prepared by | Terminal AI agent, design facilitator, for KH Mohammad Farhan |
| Governing baseline | `docs/03_DATA_CONTRACTS.md` version 1.4 |
| Subject | `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md` and `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` |
| Change authority | Project owner only |
| Review status | Structured self-design following a structured self-audit; not independent third-party assurance |
| Effect on OD-01 | None; remains **PENDING** |
| Effect on G3 | None; remains **NOT STARTED** |
| Effect on G4 | None; remains **BLOCKED** |

> **Design-only notice.** This specification does not modify the OD-01 draft, the six active baseline documents, the audit report, reference CSV files, datasets, scripts, Power BI files, or Git state. It does not approve OD-01, does not sign or date anything, and does not advance G3 or G4. It defines the corrections to be authorised and applied in later, separately controlled tasks.

> **No source verification is claimed.** No airline name, code, country, group, operating region, or business model has been verified against an external source in this task. The roster remains the intended population. All operational and financial data remain synthetic.

---

## 1. Executive summary

### 1.1 Why this specification exists

The independent governance audit scored the OD-01 draft **61/100** and found **0 critical, 7 high, 13 medium, 8 low, and 5 observations**. The audit outcome was **NOT READY — MATERIAL CORRECTIONS REQUIRED**. The roster is internally consistent and defensible as the intended population, but the draft is not signature-ready because it does not yet define a stable airline identity, a historical model, a complete provenance design, a reference-version integrity control, or an unambiguous approval scope.

This specification designs the corrections once, before any approved baseline is touched. It maps every finding and every corrective action, proposes the target architecture, defines the exact document changes, and sequences the work so the same decision is not edited inconsistently in different documents.

### 1.2 Core recommendation

The target design is deliberately practical for a single-engineer portfolio project:

1. **Separate three concepts that the draft currently conflates:** `AirlineId` (durable master identity), `AirlineKey` (permanent warehouse surrogate), and `AirlineIATACode` / `AirlineICAOCode` (mutable, versioned attributes). IATA is not a key.
2. **Use Type 1 `DimAirline` for the baseline**, with immutable reference-version snapshots. Type 2 slowly changing dimension is designed but deferred until as-was identity reporting is actually required.
3. **Define `AirlineName` as the commercial brand**, add optional `LegalName`, define `HomeCountry` as principal headquarters/domicile, define `AirlineGroup` as the ultimate parent/group brand, remove `OperatingRegion` from identity attributes, and treat `BusinessModel` as an optional analytical classification with a documented rubric.
4. **Rebuild provenance around `AirlineId`**, one row per source-attribute assertion, one authoritative `VERIFIED` record per populated identity attribute, evidence hashes, retrieval dates, staleness rules, and supersession links.
5. **Add T-78** for airline identity reference-version, manifest, dimension, and Power BI refresh integrity, and define the `ReferenceVersion` format as `AIR-YYYY-MM-DD-NNN`.
6. **Split OD-01 into OD-01A (population) and OD-01B (identity and reference rules)**, or narrow a single record to the population and identity rules while acknowledging the reference schema as proposed design only.
7. **Define the G3 gate vocabulary and criteria.** The recorded status remains `NOT STARTED` in this task; the recommended corrected status is `IN PROGRESS`, because design evidence exists but formal approvals do not.
8. **Re-audit the corrected draft before signature.** No signature, date, approval, schema freeze, reference population, or data generation is authorised by this specification.

### 1.3 Readiness snapshot

| Item | Current state | Target after owner decisions and controlled edits |
|---|---|---|
| Remediation design | **COMPLETE** — this document | Owner review |
| Owner decisions | **PENDING** — 18 proposed decisions in Section 15 | Recorded in a decision brief |
| Contract v1.5 | Not started | Identity, provenance, lifecycle, T-78 and approval controls aligned |
| OD-01 draft | v0.1, PENDING, not signature-ready | v0.2 or OD-01A/OD-01B, corrected and re-audited |
| Independent re-audit | Not started | HIGH findings closed; no new HIGH |
| OD-01 | **PENDING** | Signed only after re-audit |
| G3 | **NOT STARTED** | `IN PROGRESS` after owner-approved status correction; `APPROVED` only at gate review |
| G4 | **BLOCKED** | Remains blocked until G3 is approved and written G4 authorisation exists |

### 1.4 What this specification does not do

- It does not edit the draft, the contract, the scope, the business requirements, the master prompt, the traceability matrix, the progress ledger, or the audit report.
- It does not create or populate `ref_airlines.csv`, `ref_airline_sources.csv`, or any other reference file.
- It does not verify any source, assign any optional airline value, or claim any airline fact.
- It does not freeze the schema, approve a reference version, authorise data generation, or change a gate status.
- It does not perform any Git stage, commit, push, reset, checkout, or tag operation.

---

## 2. Current verified baseline

### 2.1 Authoritative hashes verified at the start of this task

| Artifact | SHA256 | Result |
|---|---|---|
| `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md` | `C594DFCD8FE1B6809E28CBE1B3EE6D24FAA0772D35DD1FE57767FECCD3CA2A60` | MATCH |
| `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` | `FD94BD369D3DDDC1AF84C040C27014F112E74B4B0F938CE95B617C7B142BECE6` | MATCH |
| `docs/03_DATA_CONTRACTS.md` | `EB1DE0E1B80E9E30B4905740BDD66AB96657073119D63C49AA48445CB06446E2` | MATCH |
| `docs/PROGRESS_LEDGER.md` | `42A00E3A41A9ABBC6B9F930BFE39DD369E6B9681B9F56194921E7145E6F8A7A3` | MATCH |

The destination `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` did not exist before creation. Any hash mismatch would have stopped this task before the specification was written.

### 2.2 Inputs read in full

| Input | Role in this specification |
|---|---|
| `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md` | Subject draft; all proposed changes are expressed against its sections |
| `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` | Source of the 33 findings and 18 corrective actions |
| `docs/03_DATA_CONTRACTS.md` v1.4 | Governing contract; identity, provenance, keys, tests, decisions and gates |
| `docs/01_PROJECT_SCOPE.md` | Fixed scope, roster and synthetic boundary |
| `docs/02_BUSINESS_REQUIREMENTS.md` | BR-01 and the multi-airline comparison obligation |
| `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt` | Fixed roster, identity rules, gate vocabulary and synthetic disclosure |
| `docs/REQUIREMENTS_TRACEABILITY.md` | REQ-001 and REQ-023 to REQ-027 |
| `docs/PROGRESS_LEDGER.md` | G3 and G4 status evidence |
| `docs/OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt` | 99-check migration evidence and pre/post hashes |

### 2.3 Current governance state

| Item | Status | Evidence |
|---|---|---|
| OD-01 | **PENDING** | Draft status block; contract Section 14 |
| OD-01 draft | `PENDING OWNER SIGNATURE` | Draft v0.1 |
| Audit readiness | **NOT READY — MATERIAL CORRECTIONS REQUIRED** | Audit Section 18 |
| G3 | **NOT STARTED** | Progress ledger row 9 |
| G4 | **BLOCKED** | Progress ledger row 10 |
| Reference CSV files | **0** | Audit integrity table |
| Power BI files | **0** | Audit integrity table |
| Datasets or scripts | **0** | Audit integrity table |
| Schema freeze | **Not authorised** | Contract Sections 14 and 15 |
| Data generation | **Not authorised** | Contract Section 15 |
| Git commits | **None** | Repository inspection recorded in audit |

### 2.4 Evidence classification

The audit is a **structured adversarial self-audit**, not independent third-party assurance, because the same assistant prepared the draft and performed the audit. The migration report's **99 checks** are document-integrity evidence: they verify replacement counts, hashes, encodings and status strings. They do not independently verify governance quality or the future reference data. The corrected record must label both evidence classes accurately.

---

## 3. Architectural decisions and rationale

The following decisions are **proposed**. None is approved by this specification. Each requires the owner's explicit decision before the contract or draft is edited. The identifiers `D-01` to `D-18` are design-decision references used only in this document; they are not OD-series owner decisions.

| ID | Decision | Recommendation | Why | Main alternative rejected | Owner approval |
|---|---|---|---|---|---|
| D-01 | Separate durable identity, warehouse key and mutable codes | `AirlineId` is durable master identity; `AirlineKey` is permanent warehouse surrogate; IATA/ICAO are versioned attributes | A mutable code cannot safely be a key, a provenance join and a uniqueness test | Keep IATA as business key and add a version qualifier only | Yes |
| D-02 | Historical model | Type 1 `DimAirline` for the baseline; immutable reference-version snapshots; Type 2 deferred | Fixed roster and fixed reporting period do not require as-was dimension rows; avoids bridge and fact-key complexity | Type 2 from day one | Yes |
| D-03 | Airline name semantics | `AirlineName` = commercial brand; optional `LegalName` | Resolves legal-versus-brand ambiguity and makes T-72 deterministic | Legal name as display name; no legal name at all | Yes |
| D-04 | Home country semantics | Country of principal headquarters or domicile; not incorporation, AOC state or ownership | Gives one source-verifiable definition for the roster and tests | Country of incorporation; AOC state | Yes |
| D-05 | Airline group boundary | Ultimate parent company or group brand; optional; null when not verified | Prevents brand, immediate holding company and ultimate parent being mixed | Immediate parent; airline brand | Yes |
| D-06 | Operating region | Remove from identity attributes; derive analytically if needed | Region is not a single source-verifiable identity fact for a global airline | Add a controlled vocabulary without a basis | Yes |
| D-07 | Business model | Optional analytical classification with a documented rubric; not source-verified identity | Business model is an analyst taxonomy, not a registry fact | Treat as a source-verified identity attribute | Yes |
| D-08 | Lifecycle model | Add `LifecycleStatus`, `StatusEffectiveDate`, `MergedIntoAirlineId`; derive `IsActive` | Handles suspension, cessation and merger without deleting history | Boolean `IsActive` only | Yes |
| D-09 | Provenance architecture | One row per source-attribute assertion; stable `AirlineId`; authoritative flag; controlled vocabulary | Makes T-75 deterministic and supports multiple sources | One row per source document; IATA join | Yes |
| D-10 | Evidence durability | Require retrieval date, content hash or archive reference, URL hygiene, staleness and re-verification | A URL alone is not durable evidence | URL plus verification date only | Yes |
| D-11 | Reference version format | `AIR-YYYY-MM-DD-NNN`; one approved version per generation and refresh | Makes manifest and refresh matching unambiguous | Free-text `String(30)` | Yes |
| D-12 | Reference-version integrity test | Add T-78; do not overload T-77 | T-77 is reference-to-dimension; T-78 is version/manifest/refresh integrity | Extend T-77 only | Yes |
| D-13 | G3 gate vocabulary | `NOT STARTED`, `IN PROGRESS`, `READY FOR REVIEW`, `APPROVED`, `BLOCKED` | Separates “not started” from “not formally approved” | Keep `NOT STARTED` and add a note | Yes |
| D-14 | OD-01 scope | Split into OD-01A population and OD-01B identity/reference rules; or narrow a single record | Separates the defensible population decision from the contested rules | Keep Sections 2–7 as one approval | Yes |
| D-15 | Reviewer and reference-version approval | Named reviewer/verifier; compensating controls; proposed OD-23 reference-version approval | Self-approval without challenge is a control weakness | Owner-only approval with no checklist | Yes |
| D-16 | Change-control tiers | Tier 1 evidence/correction; Tier 2 identity attribute; Tier 3 roster/structural; Tier 4 schema | Replaces three overlapping paths with one decision tree | Keep D-1, Section 3.2 and Section 6.5 as separate rules | Yes |
| D-17 | Disclosure control | One exact em-dash string, unconditional on pages, tooltips and exports; test T-79 | Conditional disclosure and two spellings defeat the control | “Where practical” tooltip exception | Yes for exceptions; wording no |
| D-18 | Evidence, revision and retention | Preparer/reviewer fields, revision history, hash register, read-only signed copy | Makes the approval reconstructable and tamper-evident | Unsigned copy in the working folder | Yes for retention |

**Design principles applied**

- Stable identity before mutable attributes.
- One authoritative decision per question; other documents cross-reference it rather than restating it.
- Minimum complexity that still survives identity change.
- No fabricated source, date, URL, airline group, region, business model or verification status.
- Separate identity attributes from analytical classifications.
- Separate design approval from schema freeze, reference-version approval and data generation.
- Evidence over assertion; a blank is not evidence.

---

## 4. Identity model

### 4.1 Key hierarchy and responsibilities

`AirlineId` and `AirlineKey` are **not interchangeable**. `AirlineId` is the governed master-data identity. `AirlineKey` is the warehouse surrogate that facts use. IATA and ICAO are attributes, not keys.

| Identifier | Type | Scope | Assigned by | Mutable? | Reused? | Used for | Not used for |
|---|---|---|---|---|---|---|---|
| `AirlineId` | String(20) | Master data, reference files, provenance | Project governance, once per airline | No | Never | Durable identity, provenance join, cross-version lineage | Fact-table joins, Power BI relationships |
| `AirlineKey` | Int32 | Warehouse / `DimAirline` | Deterministic warehouse assignment, once per airline | No | Never | `DimAirline` primary key; every fact `AirlineKey` foreign key; Power BI relationships | Source identity, provenance, business-key matching |
| `AirlineIATACode` | String(2) | Airline attribute | Verified source | Yes, by new reference version | A code may be reassigned only with explicit retirement and a new version | Display, validation, operational reference | Primary key, provenance join, physical relationship key |
| `AirlineICAOCode` | String(3) | Airline attribute | Verified source | Yes, by new reference version | Same rule as IATA | Display, validation, alternate operational reference | Primary key, provenance join, physical relationship key |
| `AirlineName` | String(100) | Airline attribute | Verified source, canonicalised | Yes, by new reference version | Not applicable | Display, label, roster reconciliation | Key, provenance join |
| `ReferenceVersion` | String(30) | Reference snapshot | Reference-version approval | No after approval | Never | Version pinning, manifest matching, lineage | Airline identity |

**Non-negotiable rule:** no standalone `AirlineCode`. IATA and ICAO remain separate fields. No fact table may join to an airline through IATA, ICAO or name.

### 4.2 Proposed administrative allocation

The following allocation is a **project administration proposal**, not an airline fact and not a source-verified value. It gives the implementer a deterministic, readable key assignment. The owner must approve it before use.

| # | Airline (intended population) | Proposed `AirlineId` | Proposed `AirlineKey` |
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

Assignment rules:

- `AirlineId` format: `^AIR-[0-9]{4}$`; assigned once; never changed or reused.
- `AirlineKey` is a positive `Int32`; assigned once; never changed or reused; not derived from IATA, ICAO or row order after initial assignment.
- A new airline receives the next unused `AirlineId` and `AirlineKey`; a retired airline retains both.
- Rebuilding `DimAirline` must reproduce the same `AirlineKey` for the same `AirlineId`; a rebuild that changes keys is a defect.

### 4.3 Key and uniqueness constraints

| Object | Primary key | Required unique constraints | Rule |
|---|---|---|---|
| `ref_airlines.csv` | `AirlineId` + `ReferenceVersion` | `AirlineIATACode` within version; `AirlineICAOCode` within version; `AirlineName` within version | One row per airline per version; no duplicate codes or names in a version |
| `DimAirline` | `AirlineKey` | `AirlineId`; `AirlineIATACode` + `ReferenceVersion`; `AirlineICAOCode` + `ReferenceVersion`; `AirlineName` + `ReferenceVersion` | Exactly ten active rows in the baseline; no duplicate key or business identifier |
| `ref_airline_sources.csv` | `SourceRecordID` | One authoritative `VERIFIED` record per `AirlineId` + `AttributeName` + `ReferenceVersion` | Provenance joins on `AirlineId`, never on IATA |
| Facts | Their own surrogate key | `AirlineKey` must resolve to exactly one `DimAirline` row | No orphan; no code-based join |

**Version-qualified uniqueness.** IATA and ICAO uniqueness is scoped to a `ReferenceVersion`, not to the whole file. The same code may appear in two different versions because those versions are separate snapshots. Within one approved version, no two airlines may hold the same IATA or ICAO code. A code may be reassigned only when the prior holder is retired in that version and the reassignment is explicitly recorded.

### 4.4 Attribute semantics

**`AirlineName` — commercial brand name.** The approved name used by the airline in the market and on the roster, not the registered legal entity. Legal suffixes such as “Limited”, “PLC” or “Inc.” are not appended unless they are part of the brand. `LegalName` is optional and separately verified. Canonicalisation: Unicode NFKC, trim, collapse internal whitespace, preserve brand case and punctuation. T-72 compares the approved brand roster to the canonical `AirlineName`.

**`LegalName` — optional legal name.** The verified registered legal name of the operating entity, where available. It is not the display name, is not used for T-72 roster reconciliation, and remains null when no `VERIFIED` source exists.

**`HomeCountry` and `HomeCountryCode`.** `HomeCountry` is the country of the airline's **principal headquarters or domicile**. It is not necessarily the country of incorporation, the state that issued the air operator certificate, or the country of ultimate ownership. `HomeCountryCode` is the ISO 3166-1 alpha-2 code for that country. Where headquarters and incorporation differ, the source note records the distinction; the attribute remains the headquarters/domicile country.

**`AirlineGroup`.** The **ultimate parent company or group brand** that consolidates the airline. It is not the airline's own brand and not an intermediate holding company. If the airline is independent, the value is null. If state-owned, the state-owned group/company is used only where one exists and is documented. Source preference: the parent group's official source, a government registry, then the airline's corporate source only where it explicitly states the ultimate parent. No inference from home country, brand similarity or ownership assumptions.

**`OperatingRegion`.** Removed from the identity attribute set. It is not a single source-verifiable fact for a global airline. If region analysis is needed, derive it at the report layer from `DimRoute` / `DimAirport` geography or from a separate analytical mapping approved under a future decision. It is not part of `ref_airlines.csv`, `DimAirline` identity reconciliation or T-75.

**`BusinessModel`.** Optional analytical classification, not a source-verified identity attribute. It is populated only from the rubric in Appendix A, with the classification method, analyst and date recorded. It is excluded from T-72 and T-75. Null is valid. If the owner prefers, rename the column to `BusinessModelClass` to make the distinction explicit.

**`LifecycleStatus` and `IsActive`.** `LifecycleStatus` is one of `Active`, `Suspended`, `Ceased`, `Merged`. `IsActive` is derived: `TRUE` only when `LifecycleStatus = Active`. `StatusEffectiveDate` is required for `Suspended`, `Ceased` and `Merged`; it may be null for the baseline `Active` state. `MergedIntoAirlineId` is required when `LifecycleStatus = Merged` and points to the successor `AirlineId`. `IsActive` is an airline operating state, not the same as `IsCurrent`, which is a reference-version property.

### 4.5 Code lifecycle

| Situation | Required treatment | Key impact |
|---|---|---|
| Code unchanged | Same value in the new version; new source record only if evidence changed | None |
| Code changes for the same airline | New reference version; same `AirlineId` and `AirlineKey`; old code retained in prior versions; new code unique within the new version | None |
| Code retired because airline ceased | Airline retained with `LifecycleStatus = Ceased`; last code may remain in the current version; prior versions retain history | None |
| Code reassigned to another airline | Prior holder must be retired in that version; new holder receives the code in a new version; no two active airlines hold it in one version; reconciliation note required | None; both airlines keep their own IDs/keys |
| Code missing or unverifiable | Approved version is incomplete; required code blocks approval; no placeholder or null in an approved version | Blocked, not inferred |
| Historical code in an old version | Preserved in the immutable old version; not deleted when the current version changes | None |

No code may be silently reused. A code reassignment is a Tier 2 identity change (Section 5.3) and requires a new reference version, a source record for the new holder, and a reconciliation note. If multiple historical code changes become common, add a separate code-history reference at G3; the baseline does not need it.

### 4.6 Identity versus analytical classification

| Class | Attributes | Source verification | Used in T-72 / T-75 | Display |
|---|---|---|---|---|
| Identity | `AirlineId`, `AirlineName`, `LegalName` (if populated), `AirlineIATACode`, `AirlineICAOCode`, `HomeCountry`, `HomeCountryCode`, `AirlineGroup` (if populated), `LifecycleStatus`, `IsActive`, `StatusEffectiveDate`, `MergedIntoAirlineId` | Required for every populated identity attribute, with the lifecycle exception in Section 7.3 | Yes | Yes |
| Analytical | `OperatingRegion` (derived only), `BusinessModel` | Not source-verified; method and analyst recorded | No | Optional, clearly labelled |

### 4.7 Referential integrity and fact mapping

- Every fact carries `AirlineKey`; it must resolve to exactly one `DimAirline` row in the selected reference version.
- No fact carries or joins on `AirlineIATACode`, `AirlineICAOCode`, `AirlineName` or `AirlineId` as a physical relationship key.
- `DimAircraft.AirlineKey` remains a lineage/validation foreign key and must not create an active second filter path. Fleet-by-airline analysis uses a role-playing `DimAirline - Fleet` dimension or a documented `TREATAS` measure.
- A missing `AirlineKey` is a high-severity orphan and must be quarantined, not mapped to a default airline.
- `AirlineKey` and `AirlineId` must never be reassigned, including after a reference correction, merger, cessation or `DimAirline` rebuild.
- Historical facts are not re-keyed when identity attributes change. Type 1 reports current identity attributes; as-was identity reporting is a Type 2 extension (Section 5.4).

---

## 5. Historical model

### 5.1 Type 1 versus Type 2

| Criterion | Type 1 (recommended baseline) | Type 2 (deferred option) |
|---|---|---|
| Rows per airline | One current row | One row per version/effective period |
| Dimension primary key | `AirlineKey` | `AirlineVersionKey` |
| Durable airline key | `AirlineKey` | `AirlineKey` remains durable; `AirlineVersionKey` identifies the row |
| Identity history | Immutable reference-version snapshots | Row-level `EffectiveFrom`, `EffectiveTo`, `IsCurrent` |
| Fact join | `AirlineKey` | `AirlineKey` for the airline; `AirlineVersionKey` or a bridge only if as-was attribution is required |
| As-was reporting | Not supported in the dimension | Supported |
| Complexity | Low | Medium to high |
| Fit for this project | **Yes** — fixed roster, fixed 12-month period, no identity change planned | Only if identity changes must be reported as of the event date |

### 5.2 Recommended baseline: Type 1 with immutable reference versions

`DimAirline` is Type 1:

- One row per airline.
- `AirlineKey` is the permanent warehouse key and primary key.
- `AirlineId` is the permanent master identity and unique alternate key.
- `ReferenceVersion` is a technical lineage column identifying the snapshot that produced the current row.
- No row-level `EffectiveFrom`, `EffectiveTo` or `IsCurrent` columns in the baseline.
- `IsActive` and `LifecycleStatus` describe the airline's current operating state, not version currency.

Version-level effective dating lives in the reference-version manifest (`data/manifests/reference_versions.csv` or an equivalent approved manifest):

| Field | Meaning |
|---|---|
| `ReferenceVersion` | `AIR-YYYY-MM-DD-NNN`; immutable after approval |
| `EffectiveFrom` | Date on which the version becomes effective; normally the date encoded in the version |
| `EffectiveTo` | Day before the next approved version's `EffectiveFrom`; null for the current version |
| `IsCurrent` | `TRUE` for exactly one approved version selected for the current generation/refresh |
| `Status` | `DRAFT`, `READY FOR REVIEW`, `APPROVED`, `RETIRED`, `REJECTED` |
| `ApprovedBy` / `ApprovalDate` | Owner and date; blank until approved |
| `ManifestHash` | SHA-256 of the reference and provenance files for the version |
| `SupersedesReferenceVersion` | Prior version replaced by this one, if any |
| `ReconciliationNote` | Required when an identity value changes |

**`IsCurrent` versus `IsActive`:** `IsCurrent = TRUE` means “this is the selected reference version”; `IsActive = TRUE` means “this airline is operating.” A ceased airline can be in the current reference version with `IsActive = FALSE`. Do not use one field for both meanings.

**ReferenceVersion format:** `^AIR-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$`. Example: `AIR-2026-11-01-001`. The date is the effective date, not the approval date. The three-digit sequence distinguishes multiple versions effective on the same date. The value is not an approval status.

### 5.3 Change scenarios and required treatment

| Scenario | Change tier | Required treatment | Tests |
|---|---|---|---|
| Typo or source-evidence correction that does not change the approved value | Tier 1 | New source record if evidence changed; new reference version if the loaded value changes; reconciliation note | T-75, T-76, T-78 |
| Brand rename (same legal entity) | Tier 2 | Same `AirlineId`/`AirlineKey`; new `AirlineName`; optional `LegalName`; new version and source record | T-72, T-75, T-77, T-78 |
| IATA or ICAO code change | Tier 2 | Same `AirlineId`/`AirlineKey`; new code attribute; version-qualified uniqueness; reconciliation note | T-73, T-74, T-78 |
| Airline group change | Tier 2 | Same keys; new optional `AirlineGroup` value or null; new source record | T-75, T-76, T-78 |
| Merger or acquisition creating a successor entity | Tier 3 | New owner decision/scenario; successor gets a new `AirlineId` and `AirlineKey`; old airline `LifecycleStatus = Merged` and `MergedIntoAirlineId`; old facts retain old key | T-72, T-78 |
| Suspension | Tier 2 | Same keys; `LifecycleStatus = Suspended`; `IsActive = FALSE`; `StatusEffectiveDate`; new version | T-78 |
| Cessation | Tier 2 | Same keys; `LifecycleStatus = Ceased`; `IsActive = FALSE`; `StatusEffectiveDate`; retain row and facts | T-78 |
| Code reassignment | Tier 2 | Prior holder retired in the version; new holder receives the code in a new version; no overlap; reconciliation note | T-73, T-74, T-78 |
| Backdated correction | Tier 2 | New version with an `EffectiveFrom` no later than the correction date; no rewrite of a published version; reconciliation note | T-78 |
| Roster addition, removal or substitution | Tier 3 | New owner decision; new scenario; new reference version; impact assessment | T-72, T-78 |
| Schema, key or SCD change | Tier 4 | New contract version; schema-freeze review; owner approval; G3 impact | All identity tests |

### 5.4 Type 2 trigger and design (deferred)

Type 2 is required only if the project must report identity **as it was at the event date** (for example, historical airline name or code on a flight). The baseline does not require this. If triggered:

- Add `AirlineVersionKey` (`Int32`) as the `DimAirline` primary key.
- Keep `AirlineKey` as the durable airline key and `AirlineId` as the durable master identity.
- Add row-level `EffectiveFrom`, `EffectiveTo` and `IsCurrent`.
- Add `AirlineVersionKey` to facts or use an approved bridge; do not overload `AirlineKey`.
- Add an as-of reconciliation test (proposed T-79, separate from the baseline T-78).
- Obtain owner approval and a schema-freeze decision before implementation.

### 5.5 Historical reconciliation and referential integrity

- `AirlineKey` and `AirlineId` are stable across every reference version and every `DimAirline` rebuild.
- Facts are generated against exactly one approved `ReferenceVersion`; facts from different versions must not be mixed in one refresh.
- T-78 verifies that the reference version, manifest, `DimAirline.ReferenceVersion` and Power BI refresh parameter agree.
- Any identity change requires a reconciliation note stating: old and new values, affected `AirlineId`, source records, version, whether facts are affected, and test evidence.
- Published reference versions are immutable. A correction creates a new version; it does not edit the old one.
- Historical facts remain linked to the same `AirlineKey`. They are not re-keyed, deleted or remapped to a successor airline.
- If a fact references a key absent from the current dimension, the refresh is blocked; the fact is not silently dropped.

### 5.6 What not to do

- Do not introduce Type 2, a bridge table or effective-dated facts for the baseline.
- Do not use `AirlineKey` as a version-row key; if Type 2 is adopted, use `AirlineVersionKey`.
- Do not reuse `AirlineId` or `AirlineKey` after cessation or merger.
- Do not overwrite a published reference version.
- Do not use IATA/ICAO as a fact join or provenance key.

---

## 6. Attribute dictionary

### 6.1 `DimAirline` and `ref_airlines.csv` attributes

| Attribute | Type | Null | Class | Definition and rule | Versioned | Provenance |
|---|---|---|---|---|---|---|
| `AirlineKey` | Int32 | No | Warehouse key | Permanent surrogate primary key of `DimAirline`; assigned once per airline; never reused or changed | No | None |
| `AirlineId` | String(20) | No | Identity key | Durable master identity; `^AIR-[0-9]{4}$`; stable across versions; provenance join | No | None (governed assignment) |
| `AirlineIATACode` | String(2) | No | Identity attribute | Two-character uppercase alphanumeric IATA code; unique within `ReferenceVersion`; mutable by new version | Yes | Required if populated; every approved row is populated |
| `AirlineICAOCode` | String(3) | No | Identity attribute | Three-character uppercase ICAO code; unique within `ReferenceVersion`; mutable by new version | Yes | Required if populated; every approved row is populated |
| `AirlineName` | String(100) | No | Identity attribute | Commercial brand name; unique within version; legal suffix not appended unless part of the brand | Yes | Required |
| `LegalName` | String(200) | Yes | Identity attribute | Verified legal registered name; not used as display name; null if not verified | Yes | Required if populated |
| `HomeCountry` | String(100) | No | Identity attribute | Country of principal headquarters/domicile; not incorporation, AOC state or ownership | Yes | Required |
| `HomeCountryCode` | String(2) | No | Identity attribute | ISO 3166-1 alpha-2 code for `HomeCountry` | Yes | Required |
| `AirlineGroup` | String(100) | Yes | Identity attribute | Ultimate parent company or group brand; null if independent or unverified | Yes | Required if populated |
| `LifecycleStatus` | String(20) | No | Identity/lifecycle | `Active`, `Suspended`, `Ceased`, `Merged` | Yes | Baseline `Active` is an OD-01 roster decision; a change requires a source record |
| `StatusEffectiveDate` | Date | Yes | Identity/lifecycle | Date the current non-Active status took effect; required for Suspended/Ceased/Merged; may be null for Active | Yes | Required when populated |
| `MergedIntoAirlineId` | String(20) | Yes | Identity/lifecycle | Successor `AirlineId` when `LifecycleStatus = Merged`; must exist and must not equal the current airline | Yes | Required when populated |
| `IsActive` | Boolean | No | Derived lifecycle | `TRUE` iff `LifecycleStatus = Active`; not a source-verified attribute | Yes | Derived |
| `ReferenceVersion` | String(30) | No | Technical lineage | Snapshot that produced the row; `^AIR-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$` | No | None |
| `OperatingRegion` | — | — | Analytical only | Removed from identity and from `DimAirline`; derive at report layer if needed | — | Not source-verified |
| `BusinessModel` | String(50) | Yes | Analytical | Optional classification from Appendix A; not source-verified; null allowed; excluded from T-72/T-75 | Yes | Method and analyst, not source provenance |
| `AirlineVersionKey` | Int32 | No (Type 2 only) | Type 2 row key | Only if Type 2 is approved; new key per version; `AirlineKey` remains durable | Yes | None |
| `EffectiveFrom` / `EffectiveTo` | Date | Type 2 only | Type 2 validity | Row-level validity only in Type 2; baseline uses version-level dates | Yes | None |
| `IsCurrent` | Boolean | Type 2 only | Type 2 currency | Row-level current-version flag only in Type 2; baseline uses version-level `IsCurrent` | Yes | None |

### 6.2 Canonicalisation rules

| Attribute | Canonicalisation | Comparison rule |
|---|---|---|
| `AirlineIATACode` | Trim; uppercase; must match `^[A-Z0-9]{2}$` | Exact after canonicalisation |
| `AirlineICAOCode` | Trim; uppercase; must match `^[A-Z]{3}$` | Exact after canonicalisation |
| `AirlineName` | Unicode NFKC; trim; collapse internal whitespace; preserve brand case and punctuation | Exact after canonicalisation; no fuzzy load |
| `LegalName` | Unicode NFKC; trim; collapse whitespace; preserve legal form as published | Exact after canonicalisation |
| `HomeCountry` | Unicode NFKC; trim; use the ISO 3166-1 English short name | Exact after canonicalisation |
| `HomeCountryCode` | Trim; uppercase; ISO 3166-1 alpha-2 | Exact |
| `AirlineGroup` | Unicode NFKC; trim; collapse whitespace; preserve group brand | Exact after canonicalisation |

Fuzzy matching may be used only to detect possible conflicts for manual review. It must never load a value. `SourceAttributeValue` preserves the raw source text; `AttributeValue` is the canonical value that must equal the loaded reference value.

### 6.3 `ref_airlines.csv` required schema

| Field | Type | Null | Key/role |
|---|---|---|---|
| `AirlineId` | String(20) | No | Business identity; part of primary key with `ReferenceVersion` |
| `AirlineIATACode` | String(2) | No | Mutable attribute; unique within version |
| `AirlineICAOCode` | String(3) | No | Mutable alternate attribute; unique within version |
| `AirlineName` | String(100) | No | Commercial brand; unique within version |
| `LegalName` | String(200) | Yes | Optional legal name |
| `HomeCountry` | String(100) | No | Identity attribute |
| `HomeCountryCode` | String(2) | No | Identity attribute |
| `AirlineGroup` | String(100) | Yes | Optional identity attribute |
| `LifecycleStatus` | String(20) | No | Lifecycle status |
| `StatusEffectiveDate` | Date | Yes | Required for non-Active |
| `MergedIntoAirlineId` | String(20) | Yes | Required for Merged |
| `IsActive` | Boolean | No | Derived from lifecycle |
| `ReferenceVersion` | String(30) | No | Part of primary key; version pin |

`BusinessModel` is not part of the identity reference schema. If retained, it belongs in a separate analytical classification table or a clearly labelled analytical column outside the identity reconciliation. `OperatingRegion` is not present.

### 6.4 Analytical classification rubric (`BusinessModel`)

| Class | Definition | Decision rule | Default |
|---|---|---|---|
| Full Service | Scheduled network carrier with multiple cabins and connecting hub operations, including long-haul where applicable | Majority of capacity is scheduled network service with more than one cabin | Null until classified |
| Low Cost | Predominantly point-to-point, low premium density, ancillary-revenue-oriented model | Majority of capacity is point-to-point and single-class or low-premium | Null until classified |
| Regional | Predominantly short-haul feeder or regional operations | Majority of capacity is short-haul regional service | Null until classified |
| Charter | Majority of capacity is contracted or chartered rather than sold as scheduled seats | Charter/contract capacity exceeds scheduled seat capacity | Null until classified |
| Hybrid / Other | Combines models without a clear majority, or fits none of the above | No class reaches the documented majority threshold | Null until classified |
| Unknown | Insufficient evidence | No reliable public evidence | Null |

The rubric is analytical, not a source-verified identity fact. Record `ClassificationMethod`, `ClassificationNotes`, `Analyst`, `ClassifiedDate` and `ReferenceVersion`. Do not assign any airline-specific value in this specification. The owner may choose to omit the attribute entirely; that is simpler and acceptable.

### 6.5 Analytical region fallback (only if the owner rejects removal)

If `OperatingRegion` is retained, it must be a **separate analytical mapping**, not an identity attribute. Use a controlled list: Africa, Asia Pacific, Europe, Latin America and Caribbean, Middle East, North America. Define the basis explicitly as headquarters region or primary network region; do not mix bases. Record method and analyst. It is excluded from T-72 and T-75. The recommended design is removal.

---

## 7. Provenance design

### 7.1 Grain and cardinality

- **Grain:** one row per source-attribute assertion per `ReferenceVersion`.
- A source document that supports four attributes produces **four rows**, sharing an optional `SourceDocumentID` but each with its own globally unique `SourceRecordID`.
- Multiple sources may support one attribute. Exactly **one** authoritative `VERIFIED` record may be selected for a populated attribute in a version.
- A source record that supports no loaded value must be `QUARANTINED` or `SUPERSEDED` with a reason.
- No source record may reference an unknown `AirlineId` or a different `ReferenceVersion`.

### 7.2 Proposed `ref_airline_sources.csv` schema

| Field | Type | Null | Rule |
|---|---|---|---|
| `SourceRecordID` | String(30) | No | `SRC-000001`; globally unique; never reused; primary key |
| `SourceDocumentID` | String(30) | Yes | `DOC-000001`; groups assertions from one source document; not a key |
| `AirlineId` | String(20) | No | Stable provenance join; must exist in `ref_airlines.csv` for the same version |
| `AirlineIATACodeAtVerification` | String(2) | Yes | Context only; must match the version if populated; never used as a join |
| `AttributeName` | String(30) | No | Controlled vocabulary in Section 7.3 |
| `AttributeValue` | String(200) | No | Canonical value that must equal the loaded identity value |
| `SourceAttributeValue` | String(200) | Yes | Raw source text; required when canonicalisation changes the value |
| `SourceOrganization` | String(150) | No | Real organisation name; no invented body |
| `SourceTitle` | String(200) | Yes | Page or document title |
| `SourceURL` | String(500) | No for `VERIFIED` | HTTPS; no credentials, tokens, tracking or personal data |
| `SourceType` | String(30) | No | `OfficialAirline`, `GovernmentRegistry`, `IndustryAuthority`, `OtherDocumented` |
| `SourcePublishedDate` | Date | Yes | Publication date if stated by the source |
| `SourceRetrievedDate` | Date | No | Date the content was captured; ISO 8601 |
| `SourceVerifiedDate` | Date | No | Date the value was actually checked; not inferred; not before retrieval |
| `VerificationStatus` | String(20) | No | `VERIFIED`, `CONFLICTING`, `UNVERIFIED`, `SUPERSEDED`, `QUARANTINED` |
| `VerificationMethod` | String(50) | No for `VERIFIED` | `ManualSourceReview`, `RegistryLookup`, `OfficialDirectory`, `DocumentReview` |
| `IsAuthoritative` | Boolean | No | Exactly one `TRUE` per populated `AirlineId` + `AttributeName` + `ReferenceVersion` |
| `EvidenceHash` | String(64) | Yes | SHA-256 of captured content; required for `VERIFIED` unless `SourceArchiveRef` exists |
| `SourceArchiveRef` | String(200) | Yes | Read-only archived copy reference; at least one of hash/archive required for `VERIFIED` |
| `SupersedesSourceRecordID` | String(30) | Yes | On the new record; points to the record it replaces |
| `SupersededBySourceRecordID` | String(30) | Yes | On the old record; required when status is `SUPERSEDED`; reciprocal with the above |
| `QuarantineReason` | String(50) | Yes | Required when `QUARANTINED`; controlled values in Section 7.3 |
| `Notes` | String(500) | Yes | No secrets or personal data |
| `ReferenceVersion` | String(30) | No | Must match the version in `ref_airlines.csv` and the manifest |
| `CreatedBy` | String(100) | No | Preparer name/role |
| `CreatedDate` | Date | No | Record creation date |
| `ReviewedBy` | String(100) | Yes | Required for `VERIFIED` |
| `ReviewedDate` | Date | Yes | Required for `VERIFIED` |

### 7.3 Controlled vocabularies

**`AttributeName`:** `AirlineName`, `LegalName`, `AirlineIATACode`, `AirlineICAOCode`, `HomeCountry`, `HomeCountryCode`, `AirlineGroup`, `LifecycleStatus` (only when a status changes from the baseline). `OperatingRegion` and `BusinessModel` are excluded because they are analytical, not source-verified identity attributes.

**`SourceType`:** `OfficialAirline`, `GovernmentRegistry`, `IndustryAuthority`, `OtherDocumented`.

**`VerificationStatus`:** `VERIFIED`, `CONFLICTING`, `UNVERIFIED`, `SUPERSEDED`, `QUARANTINED`. A stale record is `QUARANTINED` with `QuarantineReason = STALE`; do not add a sixth status.

**`VerificationMethod`:** `ManualSourceReview`, `RegistryLookup`, `OfficialDirectory`, `DocumentReview`.

**`QuarantineReason`:** `CONFLICT`, `UNVERIFIED`, `STALE`, `MALFORMED`, `DUPLICATE`, `UNSUPPORTED`, `URL_INVALID`, `EVIDENCE_MISSING`, `OTHER`.

### 7.4 Source hierarchy and conflict handling

| Attribute | First preference | Second | Third | Fourth |
|---|---|---|---|---|
| `AirlineName`, `LegalName`, `AirlineGroup` | Parent group or airline official corporate source | Government/civil-aviation registry | Official ICAO/IATA directory | Reputable documented industry source |
| `AirlineIATACode` | Applicable official IATA code registry/directory | Airline official source | Government registry | Other documented source |
| `AirlineICAOCode` | Applicable official ICAO directory | Airline official source | Government registry | Other documented source |
| `HomeCountry`, `HomeCountryCode` | Government/civil-aviation registry | Airline official source | Official ICAO/IATA directory | Other documented source |

Conflict rules:

- If two same-tier sources disagree, mark both `CONFLICTING`; no authoritative record; required attribute blocks approval; optional attribute remains null.
- A higher-tier source may resolve a lower-tier conflict, but the lower-tier record remains recorded as `UNVERIFIED` or `CONFLICTING`; it is never deleted.
- A conflict must not be resolved by memory, inference, brand similarity or home-country assumption.
- The selected record is marked `IsAuthoritative = TRUE`; all others are `FALSE`.
- If a required attribute has no authoritative `VERIFIED` record, the airline record is incomplete and the version cannot be approved.

### 7.5 Verification workflow

1. Identify the airline by `AirlineId` and the attribute by the controlled `AttributeName`.
2. Retrieve the source; record organisation, title, URL, retrieval date and content hash/archive.
3. Extract `SourceAttributeValue`; canonicalise to `AttributeValue`.
4. Record the source row with a provisional status; do not mark `VERIFIED` before review.
5. Review the source and set `VerificationStatus`, `VerificationMethod`, `ReviewedBy` and `ReviewedDate`.
6. Resolve conflicts; select exactly one authoritative record per populated attribute.
7. Confirm every populated identity attribute has evidence; set optional attributes to null if no `VERIFIED` record exists.
8. Approve the reference version; run T-75, T-76 and T-78; retain evidence.

Allowed status transitions:

- `UNVERIFIED` → `VERIFIED` or `QUARANTINED`.
- `VERIFIED` → `SUPERSEDED` (new record exists) or `QUARANTINED` (stale, URL unavailable, conflict or malformed).
- `CONFLICTING` → `VERIFIED` (resolved) or `QUARANTINED`.
- `QUARANTINED` → `VERIFIED` (re-verified) or `SUPERSEDED`.
- A `SUPERSEDED` record is terminal; it is never edited back to `VERIFIED`.

### 7.6 Evidence durability, URL hygiene and staleness

**Retrieval versus verification.** `SourceRetrievedDate` records when the content was captured. `SourceVerifiedDate` records when the value was checked against that capture. Both must be real dates; `SourceVerifiedDate` must be on or after `SourceRetrievedDate`, and neither may be in the future.

**Durability.** Every `VERIFIED` record must have either a SHA-256 `EvidenceHash` of the captured content or a `SourceArchiveRef` to a read-only archived copy. If both exist, they must agree. A URL without a capture is not durable evidence.

**URL hygiene.**

- HTTPS only; no `http://` for new records.
- No credentials, tokens, session identifiers, personal data, or tracking parameters such as `utm_*`.
- No URL shorteners, raw IP addresses, localhost, or link-only redirects.
- The domain must be plausibly associated with `SourceOrganization` or be an official government, ICAO or IATA domain.
- Query parameters are allowed only when required to reach the exact document; they are recorded as part of the URL.
- If a URL becomes unavailable, the record is `QUARANTINED` with `URL_INVALID`; it is not left `VERIFIED`.

**Staleness.** Default maximum age: 365 days for names, legal names and group; 180 days for IATA and ICAO codes. Age is measured from `SourceVerifiedDate` to the reference-version approval date (or the current date if earlier). A stale record is `QUARANTINED` with `STALE` and cannot support a new approved version until re-verified. The thresholds are proposed policy, not approved values.

**Re-verification triggers.** Threshold expiry; URL unavailable; captured content hash changes; source publishes a correction; a new reference version is proposed; a conflicting source appears; the owner requests a review.

### 7.7 Canonicalisation and comparison

Use the rules in Section 6.2. The loaded value must equal the canonical `AttributeValue`. Preserve `SourceAttributeValue` when canonicalisation changes the raw text. Do not use fuzzy matching to load, overwrite or silently resolve a value. Fuzzy matching is only a detection aid for manual review.

### 7.8 Supersession and reference-version relationship

- A changed source or value creates a **new** `SourceRecordID`; the new row sets `SupersedesSourceRecordID` to the old row.
- The old row becomes `SUPERSEDED` and sets `SupersededBySourceRecordID` to the new row. The links must be reciprocal.
- A new reference version is a complete, immutable snapshot. Carry forward still-valid assertions as new source records with new IDs and supersession links; do not mutate the prior version's rows.
- `ReferenceVersion` on every source row must equal the version in `ref_airlines.csv` and the manifest.
- Cross-version joins are allowed only for lineage/supersession reporting; they are not used to satisfy T-75 for the selected version.

### 7.9 No fabrication and T-75 alignment

- No source URL, organisation, verification date or status may be recorded until the source has actually been checked.
- A blank, unavailable or memory-only source is not evidence.
- No placeholder value, inferred group, inferred region or generic business-model label may be loaded.
- T-75 must require, for **every populated identity attribute**, exactly one authoritative `VERIFIED` record with real organisation, URL, type, retrieval date, verified date and evidence hash/archive. An optional attribute with no `VERIFIED` record must be null.
- T-76 must verify that `CONFLICTING`, `UNVERIFIED`, `SUPERSEDED` and `QUARANTINED` records are handled correctly, that required conflicts block approval, and that optional attributes remain null.
- T-75 and T-76 must join on `AirlineId`, not IATA.

---

## 8. Reference-version controls

### 8.1 Version format and lifecycle

`ReferenceVersion` format: `AIR-YYYY-MM-DD-NNN`, regex `^AIR-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$`. The date is the effective date; `NNN` is a same-day sequence. The value is not an approval status and must not contain spaces.

| Status | Meaning | Allowed transitions |
|---|---|---|
| `DRAFT` | Being assembled; not usable for generation or refresh | → `READY FOR REVIEW`, `REJECTED` |
| `READY FOR REVIEW` | Complete; evidence submitted; no approval yet | → `APPROVED`, `REJECTED` |
| `APPROVED` | Owner-approved; immutable; usable for one generation/refresh | → `RETIRED` only |
| `RETIRED` | Superseded by a later approved version; retained for history | Terminal |
| `REJECTED` | Not approved; retained for audit | Terminal |

### 8.2 Version metadata and one-version rule

The authoritative version register is proposed as `data/manifests/reference_versions.csv` (a manifest, not a business reference dataset). It contains one row per version with: `ReferenceVersion`, `EffectiveFrom`, `EffectiveTo`, `IsCurrent`, `Status`, `ApprovedBy`, `ApprovalDate`, `ManifestHash`, `SupersedesReferenceVersion`, `ReconciliationNote`.

- Exactly **one** version may have `IsCurrent = TRUE` for a generation or refresh.
- `EffectiveTo` is the day before the next approved version's `EffectiveFrom`; it is null for the current version.
- The generation manifest records the exact `ReferenceVersion` and the SHA-256 of `ref_airlines.csv` and `ref_airline_sources.csv`.
- The Power BI refresh configuration exposes a `SelectedReferenceVersion` parameter and must use the same value.
- Mixing versions in one refresh, or aggregating two versions, is prohibited.

### 8.3 T-78 — Airline identity reference-version, manifest and refresh integrity

T-78 is a new test. It is separate from T-77 because T-77 checks reference-to-dimension reconciliation, while T-78 checks that the version used by the reference files, the generation manifest, the curated dimension and the Power BI refresh is the same approved version.

| Sub-check | What is verified | Expected result |
|---|---|---|
| T-78-01 | Distinct `ReferenceVersion` values in `ref_airlines.csv` | Exactly one |
| T-78-02 | Distinct `ReferenceVersion` values in `ref_airline_sources.csv` | Exactly one, equal to T-78-01 |
| T-78-03 | Generation manifest `ReferenceVersion` | Equal to T-78-01 |
| T-78-04 | `DimAirline.ReferenceVersion` for all rows | Equal to T-78-01 |
| T-78-05 | Power BI `SelectedReferenceVersion` parameter | Equal to T-78-01 |
| T-78-06 | Version register status and approval | `APPROVED`; not retired or rejected |
| T-78-07 | Population and key set | Exactly ten active `AirlineId` values and ten unique `AirlineKey` values matching the roster |
| T-78-08 | Provenance scope | Every populated identity attribute has exactly one authoritative `VERIFIED` record in the same version; no source row references another version |
| T-78-09 | Key stability | No `AirlineId` or `AirlineKey` reassigned versus the prior version; every fact `AirlineKey` resolves to exactly one dimension row |
| T-78-10 | Historical reconciliation | A reconciliation note exists for every identity change; no mixed-version facts; no silent re-key |

**Evidence:** `qa/results/airline_identity_versions.csv`, with test ID, run timestamp, versions compared, row counts, file hashes, expected result, actual result, status, evidence path and reviewer.

**Failure handling:** a T-78 failure blocks generation and refresh. Do not fall back to an older version, drop rows, or ignore the mismatch. Quarantine the run and record the reason.

### 8.4 Historical reconciliation

- Any identity change requires a reconciliation note before the new version is approved.
- The note states the old and new values, affected `AirlineId`, source records, `ReferenceVersion`, fact impact (normally none because facts use `AirlineKey`) and test evidence.
- T-78-09 and T-78-10 verify key stability and the absence of mixed versions.
- If facts were generated under a different version, block the refresh and reconcile; do not blend the two versions.
- Type 2 as-was reporting is deferred; if adopted, add an as-of test separate from T-78.

### 8.5 Reference-version approval

Reference-version approval is a separate control from OD-01. Proposed decision ID: **OD-23 — Airline identity reference-version approval** (alternative: gate artifact `G3-RV-01` if the owner does not want a new OD ID). The approval must record:

- Exact `ReferenceVersion` and file hashes.
- Source evidence and T-75/T-76 results.
- T-78 results or a documented pre-implementation plan.
- Manifest and refresh configuration.
- Reconciliation note for any identity change.
- Owner, date and signed evidence location.

No reference version may be treated as approved until this record exists. This specification does not create OD-23 or approve any version.

---

## 9. G3 gate model

### 9.1 Gate status vocabulary

Use a gate vocabulary distinct from test status and decision status. The same word must not mean “work started,” “work complete” and “approved.”

| Gate status | Meaning | Evidence required |
|---|---|---|
| `NOT STARTED` | No substantive work or evidence | None |
| `IN PROGRESS` | Work has begun; deliverables incomplete; no approval | Current draft, evidence index, open blockers |
| `READY FOR REVIEW` | Deliverables complete; review not yet signed | Complete package and review checklist |
| `APPROVED` | Gate review signed; evidence accepted; equivalent to PASS | Signed gate record, decision records, hash manifest |
| `BLOCKED` | Cannot proceed because a dependency, decision or defect is unresolved | Named blocker, owner, exit condition |

Test status remains `PLANNED`, `IN PROGRESS`, `PASS`, `FAIL`, `BLOCKED`. Decision status remains `PENDING`, `APPROVED`, `REJECTED`, `DEFERRED`. Do not use `PASS` as a gate status; if the master prompt retains it, define `APPROVED = PASS` explicitly.

### 9.2 Current G3 assessment

The ledger records G3 as `NOT STARTED` while the same row cites a 195 KB data contract with schemas, grains, keys, reference datasets, K-13 and T-01 to T-77. That is not a credible description of “no work started.” The contradiction is a reporting problem, not evidence that the design is approved.

**Recommendation:** after owner approval, change G3 to `IN PROGRESS` with the existing contract, OD-01 draft and audit as evidence, and list the formal approvals, schema freeze, reference-version approval, validation implementation and gate review as blockers. If the owner prefers to reserve `IN PROGRESS` for post-approval work, use the explicit label `NOT FORMALLY APPROVED` instead of `NOT STARTED`. Do not change the status in this task.

### 9.3 G3 entry criteria

- G2 scope gate is PASS.
- Scope, business requirements and master prompt are aligned on the ten-airline population and synthetic boundary.
- A data contract draft exists and covers grains, keys, relationships, reference datasets and validation tests.
- Critical owner decisions are identified and assigned.
- The OD-01 draft has been audited and the findings are recorded.
- Roles for owner, architecture, QA/review and Power BI are named or explicitly covered by compensating controls.

### 9.4 G3 deliverables

1. Data contract v1.5 with the identity model, attribute dictionary, provenance schema, lifecycle model, change-control tiers, T-78 and reference-version controls.
2. `04_DATA_DICTIONARY.md` or an equivalent aligned data dictionary.
3. Signed OD-01A and OD-01B, or a corrected single OD-01.
4. OD-23 reference-version approval, or `G3-RV-01`.
5. Schema-freeze proposal and approval record.
6. Validation plan covering T-72 to T-78, with owners and evidence paths.
7. Reference-version manifest and reconciliation note.
8. Gate review checklist and signed gate record.

### 9.5 G3 exit criteria

- All critical decisions listed in contract Section 14 are formally approved, including OD-01, OD-02, OD-03, OD-04, OD-05, OD-06, OD-07, OD-08, OD-12, OD-13, OD-14, OD-15, OD-16, OD-19, OD-20 and OD-21.
- OD-01 is signed; no HIGH finding remains open; M-07 and M-12 are closed.
- Schema is frozen and aligned with the data dictionary.
- The reference version is approved.
- T-72 to T-78 are defined with owners, methods and evidence paths; execution may remain planned if no data exists.
- Gate review is signed and residual risks are accepted in writing.
- G4 remains blocked until a separate written authorisation exists.

### 9.6 Roles and evidence

| Role | Responsibility | Evidence |
|---|---|---|
| Project owner | Approves scope, population, decisions, reference version and gate | Signed decision and gate records |
| Data architecture lead | Owns contract, identity model, schema freeze | Contract v1.5, data dictionary, schema-freeze record |
| Governance / QA lead | Runs audit, checklist, evidence review and re-audit | Audit report, checklist, re-audit result |
| Power BI solution architect | Owns semantic model, refresh parameter and filter paths | Model specification, T-42/T-43/T-78 evidence |
| Reference data steward | Verifies sources and maintains provenance | Source register, T-75/T-76 evidence |

**One-person compensating controls.** The same person may hold several roles, but the record must say so. Use a self-review checklist, automated hash/schema checks, a second-pass review by a peer or mentor where available, a documented reviewer-challenge section, and an explicit statement that the review is not independent third-party assurance. Do not claim independent assurance that does not exist.

### 9.7 Status-change procedure

A G3 status change requires: owner approval, a controlled ledger edit, an evidence reference, and a note that the change is not a gate approval. Moving to `READY FOR REVIEW` or `APPROVED` requires the gate package and signed review. This specification does not perform any status change.

---

## 10. Approval controls

### 10.1 Split OD-01 into two decisions

| Element | OD-01A — Population | OD-01B — Identity and reference rules |
|---|---|---|
| What is approved | The ten identities as the fixed intended population; commercial-brand definition of `AirlineName`; synthetic boundary | `AirlineId`/`AirlineKey` model; attribute dictionary; provenance; lifecycle; Type 1 baseline; T-78; reference-version controls |
| What is not approved | Reference values, optional attributes, reference schema, schema freeze, data generation | Reference CSV values, schema freeze, data generation, G3 PASS |
| Findings that must be closed first | H-01, M-12, L-01, L-07; M-07 reviewer control | H-02 to H-07; M-05 to M-08; M-11; M-13 |
| Signature readiness | After narrow corrections and reviewer check | After contract v1.5 and re-audit |
| Dependency | Can be signed before OD-01B | Depends on OD-01A and contract v1.5 |

**Single-record alternative.** Keep OD-01 but narrow the selected option to the population and identity rules in Sections 2, 4, 5 and 6; state that Section 7 is proposed design acknowledged but not frozen. Correct all P1 findings first. This is acceptable but produces a longer, harder-to-review record. The split is recommended because the HIGH findings are concentrated in the rules, not the roster.

### 10.2 Proposed approval-scope wording

**OD-01A selected option:**

> Approve the ten airline identities in Section 3 as the fixed baseline population and approve `AirlineName` as the commercial brand name used by the project. This approval does not approve any reference value beyond the intended population, does not approve optional group, region or business-model values, does not approve or freeze the reference schema, does not authorise data generation, and does not close G3.

**OD-01B selected option:**

> Approve the identity and reference rules in Sections 4 to 7: the `AirlineId` and `AirlineKey` model, the identity attribute definitions, the attribute-level provenance rules, the lifecycle model, the Type 1 baseline, T-78 and the reference-version controls. This approval does not create or populate reference CSV files, does not freeze the schema, does not authorise data generation, and does not close G3.

If a single record is retained, combine the two statements and explicitly exclude Section 7 from the frozen scope.

### 10.3 Reviewer and verifier controls

- Name a reviewer/verifier who is not the preparer. If no separate person is available, record the limitation and use compensating controls.
- The reviewer checks completeness, scope, evidence, hashes, cross-document consistency and unresolved findings.
- The reviewer records `CONCUR`, `CONCUR WITH RESERVATIONS` or `DISSENT`, with residual concerns.
- The owner acknowledges the reviewer result before signature.
- No signature or date is filled in this specification.

**Reviewer checklist**

| # | Check | Evidence |
|---:|---|---|
| 1 | Decision scope and exclusions are unambiguous | Approval block |
| 2 | All HIGH findings are closed or explicitly excluded from the scope | Finding matrix |
| 3 | M-07 and M-12 are resolved | Reviewer section, approval scope |
| 4 | All affected documents are aligned | Cross-document matrix |
| 5 | Hashes match the reviewed artifacts | Hash register |
| 6 | Evidence register is complete and correctly classified | Evidence table |
| 7 | No fabricated source, date, URL or airline value | Source register review |
| 8 | Reference version is approved or explicitly out of scope | OD-23 / G3-RV-01 |
| 9 | Tests and evidence paths are defined | T-72 to T-78 |
| 10 | Reviewer dissent and residual concerns are recorded | Challenge section |
| 11 | Signature and date are blank until owner signature | Approval block |
| 12 | Retention and immutability rule is stated | Retention section |

### 10.4 Reference-version approval

Use proposed **OD-23** (preferred) or gate artifact **G3-RV-01**. The owner approves the exact version, file hashes, source evidence, T-75/T-76 results, T-78 plan/results, manifest and refresh configuration. This is not approval of the whole schema and is not a G3 PASS. The approval record is signed, dated, hashed and retained.

### 10.5 Signed-artifact retention and revision control

- Store the signed copy in a read-only `docs/approvals/` folder (not created by this task).
- Record the signed copy SHA-256 in the decision register and evidence register.
- The signed copy is immutable; corrections require a new version, not an edit.
- Add a revision-history table with version, date, author, change summary, reviewer and status.
- Add `Prepared by` and `Reviewed by` fields with role and date.
- Record the migration report hash, backup manifest hash, draft hash and audit report hash in the evidence register.
- Verify the hash before signature and after signature; a mismatch blocks the approval.
- Git commit/tag of the signed record is recommended after approval but requires separate authorisation; do not perform it now.

### 10.6 Approval checklist outcome

The approval block must not be completed until every checklist item is `PASS` or has an owner-approved, documented exception. A blank or `N/A` is not a pass. The reviewer's residual concerns are recorded even if the owner signs.

### 10.7 Disclosure control and exact-string test

**Canonical string:** `Synthetic Simulation — Not Actual Airline Performance` using the em dash (U+2014), not a hyphen.

- Every dashboard page must show the string in a persistent footer or header.
- Every tooltip must carry the string; remove “where practical.” If a tooltip cannot physically contain it, the page-level disclosure must remain visible while the tooltip is open; do not create an exception path.
- Every export (PDF, PPTX, image, CSV report extract) must carry the string in the template or a metadata field. A raw data CSV is not a report, but a report extract is.
- Every screenshot used in the portfolio must include the footer; if cropped, add the exact string in the caption.
- Add **T-79 — Disclosure exact-string and rendered-output integrity**: verify the Unicode code points, page footer, tooltip, export template and a rendered screenshot; evidence in `qa/results/disclosure_integrity.csv`.
- Exceptions require owner sign-off and a documented compensating disclosure; the recommended baseline has no exceptions.

### 10.8 What remains proposed

Type 2 SCD; a code-history reference; a source-archive repository; OD-23; REQ-028; T-78/T-79 implementation; the data dictionary; reference CSV values; schema freeze; data generation; Power BI build; Git tag. None is approved by this specification.

---

## 11. Full 33-finding traceability matrix

Every finding in the audit is mapped below. No finding is merged, omitted or downgraded. “Status” is the design status in this specification, not the implementation status.

### 11.1 HIGH findings

| Finding | Severity | Finding summary | Action(s) | Spec section | Proposed resolution | Verification | Design status |
|---|---|---|---|---|---|---|---|
| H-01 | HIGH | `AirlineName` undefined as legal name versus commercial brand | A-01 | 4.4, 6.1, 6.2 | Define `AirlineName` as commercial brand; add optional `LegalName`; canonicalise and compare brand in T-72 | T-72, T-75; owner approval | RESOLVED BY DESIGN |
| H-02 | HIGH | Optional attributes not consistently required to be `VERIFIED` | A-02, A-10 | 6.1, 7.4, 7.9 | Every populated identity attribute requires an authoritative `VERIFIED` record; optional attributes null without one; analytical attributes excluded | T-75, T-76 | RESOLVED BY DESIGN |
| H-03 | HIGH | No SCD, effective dating or `AirlineKey` stability model | A-04 | 4.1, 4.7, 5.1–5.6 | Type 1 baseline; permanent `AirlineKey`/`AirlineId`; version-level effective dates; Type 2 deferred; T-78 key stability | T-78; reconciliation note | RESOLVED BY DESIGN |
| H-04 | HIGH | Risk register omits suspension/cessation, post-refresh reference change and historical inconsistency | A-05 | 5.3, 5.5, 8.3, 16.1 | Add lifecycle status, version pinning and historical reconciliation controls; add risks R-09 to R-11 | Risk review, T-78 | RESOLVED BY DESIGN |
| H-05 | HIGH | G3 `NOT STARTED` contradicts existing design evidence | A-06 | 9.1–9.7 | Define gate vocabulary; recommend `IN PROGRESS`; do not change status in this task | Ledger review; owner approval | RESOLVED BY DESIGN; STATUS CHANGE PENDING |
| H-06 | HIGH | No airline identity reference-version or manifest integrity test | A-07 | 8.3, 8.4 | Add T-78 with ten sub-checks across reference files, manifest, dimension and refresh | T-78 evidence | RESOLVED BY DESIGN |
| H-07 | HIGH | Mutable IATA code is business and provenance key; no stable airline ID | A-03 | 4.1–4.3, 7.1–7.2 | `AirlineId` durable identity; `AirlineKey` warehouse surrogate; IATA/ICAO versioned attributes; provenance joins on `AirlineId` | T-73, T-74, T-75, T-77, T-78 | RESOLVED BY DESIGN |

### 11.2 MEDIUM findings

| Finding | Severity | Finding summary | Action(s) | Spec section | Proposed resolution | Verification | Design status |
|---|---|---|---|---|---|---|---|
| M-01 | MEDIUM | `HomeCountry` not defined | A-10 | 4.4, 6.1 | Principal headquarters/domicile; separate from incorporation, AOC state and ownership | T-72, T-75 | RESOLVED BY DESIGN |
| M-02 | MEDIUM | `AirlineGroup` boundary and source hierarchy ambiguous | A-10 | 4.4, 6.1, 7.4 | Ultimate parent/group brand; optional; parent/regulator source preference; null if unverified | T-75, T-76 | RESOLVED BY DESIGN |
| M-03 | MEDIUM | `OperatingRegion` has no controlled vocabulary | A-10 | 4.4, 6.1, 6.5 | Remove from identity attributes; derive analytically if needed; fallback controlled list only with a defined basis | Schema check; T-72 excludes it | RESOLVED BY DESIGN; OWNER DECISION |
| M-04 | MEDIUM | `BusinessModel` is a classification, not a source-verifiable identity fact | A-10 | 4.4, 6.4 | Optional analytical rubric; method and analyst recorded; excluded from identity provenance | Rubric review; T-72/T-75 exclusion | RESOLVED BY DESIGN; OWNER DECISION |
| M-05 | MEDIUM | Provenance cardinality, vocabulary and authority unresolved | A-11 | 7.1–7.9 | One row per assertion; `SourceRecordID` format/uniqueness; controlled `AttributeName`; `IsAuthoritative`; canonicalisation | T-75, T-76; schema checks | RESOLVED BY DESIGN |
| M-06 | MEDIUM | Source evidence not durable; “stale” undefined | A-11 | 7.6–7.9 | Retrieval date, evidence hash/archive, URL hygiene, staleness thresholds, re-verification | T-75, T-76; hash checks | RESOLVED BY DESIGN |
| M-07 | MEDIUM | Approval workflow lacks independent verification and reference-version approval criteria | A-08 | 10.3–10.5 | Named reviewer, checklist, compensating controls, OD-23 reference-version approval | Reviewer sign-off; approval checklist | RESOLVED BY DESIGN; OWNER DECISION |
| M-08 | MEDIUM | Three different change-control paths | A-12 | 5.3 | Tier 1 evidence/correction; Tier 2 identity; Tier 3 roster/structural; Tier 4 schema | Cross-document review; T-78 | RESOLVED BY DESIGN |
| M-09 | MEDIUM | Semantic-model impact omits `DimAirline`/`DimAircraft` filter-path constraint | A-13 | 4.7, 10.2 | No active `DimAirline`–`DimAircraft` relationship; role-playing `DimAirline - Fleet` or `TREATAS`; add to OD-01 Section 8.1 | T-42, T-43; model review | RESOLVED BY DESIGN |
| M-10 | MEDIUM | 99 migration checks presented as independent assurance | A-14 | 2.4, 10.5 | Label as reported by the migration script, not independently re-executed; add hashes; cite audit | Evidence register review | RESOLVED BY DESIGN |
| M-11 | MEDIUM | Disclosure conditional and exact string inconsistent | A-15 | 10.7 | Exact em-dash string; unconditional pages, tooltips and exports; T-79 | T-79 rendered-output test | RESOLVED BY DESIGN |
| M-12 | MEDIUM | Approval block approves Sections 2–7 while excluding schema freeze | A-09 | 10.1–10.2 | Split or narrow approval; Section 7 acknowledged design, not frozen | Approval-block review | RESOLVED BY DESIGN; OWNER DECISION |
| M-13 | MEDIUM | Audit metadata and retention incomplete | A-16 | 10.5, 2.4 | Preparer/reviewer fields; revision history; hashes; read-only signed copy | Document review; hash register | RESOLVED BY DESIGN |

### 11.3 LOW findings

| Finding | Severity | Finding summary | Action(s) | Spec section | Proposed resolution | Verification | Design status |
|---|---|---|---|---|---|---|---|
| L-01 | LOW | “Approved airline roster” heading can imply formal approval | A-17 | 10.1, 13 | Rename to “Intended airline population (approved as intended population; formal OD-01 pending)” | Text check | RESOLVED BY DESIGN |
| L-02 | LOW | Required-files table omits types, lengths and nullability | A-17 | 6.1–6.3 | Add type/null/key columns or cross-reference contract Table 6.2.2 and Section 3.4 | Table check | RESOLVED BY DESIGN |
| L-03 | LOW | Evidence register omits migration report, backup manifest and draft hashes | A-14 | 2.1, 10.5 | Add all three hashes and the audit report hash; state source of each | Evidence-register check | RESOLVED BY DESIGN |
| L-04 | LOW | No preparer identity | A-16 | 10.5 | Add `Prepared by` with name/role and date | Document-control check | RESOLVED BY DESIGN |
| L-05 | LOW | No revision history | A-16 | 10.5 | Add version/date/author/change/reviewer table | Document-control check | RESOLVED BY DESIGN |
| L-06 | LOW | `SUPERSEDED` record has no successor link | A-17 | 7.2, 7.8 | Add `SupersededBySourceRecordID`; reciprocal with `SupersedesSourceRecordID` | T-75/T-76 lineage check | RESOLVED BY DESIGN |
| L-07 | LOW | Baseline uses “real, source-verified” in the present tense | A-17 | 13 | Change to “real, to be source-verified” or add “verification pending” in scope, contract and master prompt | Text scan | RESOLVED BY DESIGN |
| L-08 | LOW | `ReferenceVersion` has no format | A-17 | 5.2, 8.1 | `AIR-YYYY-MM-DD-NNN`; regex and validation rule | T-78 format check | RESOLVED BY DESIGN |

### 11.4 Observations

| Finding | Severity | Observation | Action(s) | Spec section | Proposed resolution | Verification | Design status |
|---|---|---|---|---|---|---|---|
| O-01 | OBSERVATION | 26 KB draft is disproportionate to a population decision | A-18 | 10.1 | Add a one-page decision brief at the top; move detail to appendices | Review of brief | RESOLVED BY DESIGN |
| O-02 | OBSERVATION | Draft combines population with identity/provenance/reference rules | A-18 | 10.1 | Split OD-01A and OD-01B | Owner decision | RESOLVED BY DESIGN; OWNER DECISION |
| O-03 | OBSERVATION | Record is closer to a governance specification than an ADR | A-18 | 14 | Use a short ADR template for future decisions; keep this long record as an enterprise reference design | Template review | RESOLVED BY DESIGN |
| O-04 | OBSERVATION | No version-control binding; source URLs may carry tracking/secrets | A-18 | 7.6, 10.5 | URL hygiene; commit/tag signed record after approval, subject to authorisation | URL validation; Git tag later | RESOLVED BY DESIGN; DEFERRED |
| O-05 | OBSERVATION | No reviewer dissent or residual-concerns section | A-18 | 10.3 | Add reviewer challenge and residual concerns before signature | Reviewer template check | RESOLVED BY DESIGN |

### 11.5 Coverage check

| Group | Total | Mapped | Open design gaps |
|---|---:|---:|---:|
| HIGH | 7 | 7 | 0 |
| MEDIUM | 13 | 13 | 0 |
| LOW | 8 | 8 | 0 |
| OBSERVATION | 5 | 5 | 0 |
| **Total** | **33** | **33** | **0** |

All seven HIGH findings have explicit proposed resolutions. H-05 still requires an owner-approved status correction; M-03, M-04, M-07, M-12 and O-02 still require owner decisions. No finding is closed in the implementation sense; closure requires the corrected documents and re-audit.

---

## 12. Full 18-action remediation register

Each action is a proposed correction. None is executed by this specification. “Blocks” states whether the action blocks OD-01 signature, schema freeze or implementation.

### A-01 — Define `AirlineName` as commercial brand; add optional `LegalName`

| Field | Detail |
|---|---|
| Priority / findings | P1 / H-01 |
| Affected documents | Draft Section 3, D-2, Section 6.3, Section 7, T-72; contract Section 3.4, Table 6.2.2, Section 4.3, T-72; scope Section 5; BR-01; master prompt Section 4; traceability REQ-023/REQ-024 |
| Required change | Replace “official source-verified airline name” with a commercial-brand definition; add optional `LegalName`; add canonicalisation; update T-72 to compare the brand, not a legal name |
| Proposed wording | Contract Table 6.2.2: “`AirlineName` is the commercial brand name used by the airline and approved for the project roster. It is unique within the reference version. Legal registered names are recorded separately in `LegalName` when verified; legal suffixes are not appended unless part of the brand.” Add `LegalName` (`String(200)`, nullable): “Verified legal registered name of the operating entity; not used as the display name; null when not verified.” Draft D-2: “`AirlineName` means the commercial brand, not the legal registered name.” |
| Dependencies | D-03; owner approval; contract edit before draft edit |
| Verification | T-72 compares canonical brand names; T-75 proves `LegalName` only when populated; text scan for “official name” ambiguity |
| Owner approval | Yes — changes an approved identity attribute |
| Blocks | Signature: yes. Schema freeze: yes. Implementation: yes |

### A-02 — Require `VERIFIED` for every populated identity attribute

| Field | Detail |
|---|---|
| Priority / findings | P1 / H-02 |
| Affected documents | Draft Section 3.1, Section 6.2, Section 6.5, T-75; contract Section 3.4, T-75; scope Section 5; master prompt Section 4; traceability REQ-025/REQ-026 |
| Required change | Remove the “required attributes only” limit; every populated identity attribute, required or optional, must have an authoritative `VERIFIED` record; optional attributes without one remain null |
| Proposed wording | “Every populated identity attribute in `ref_airlines.csv`, required or optional, must resolve to exactly one authoritative `VERIFIED` record for the same `AirlineId`, `AttributeName`, `AttributeValue` and `ReferenceVersion`. An optional attribute with no `VERIFIED` record must be null. `CONFLICTING`, `UNVERIFIED`, `QUARANTINED` and `SUPERSEDED` records must not support a loaded value.” |
| Dependencies | D-09; A-10 for analytical exclusions; A-11 for authority flag |
| Verification | T-75 requires evidence for every populated identity attribute; T-76 confirms optional nulls and conflicts |
| Owner approval | Yes — tightens the provenance rule |
| Blocks | Signature: yes. Schema freeze: yes. Implementation: yes |

### A-03 — Add stable `AirlineId` and permanent `AirlineKey`; version-qualified business keys

| Field | Detail |
|---|---|
| Priority / findings | P1 / H-07 |
| Affected documents | Draft D-3, Section 7, R-6, T-73/T-74/T-75/T-77; contract Section 3.4, Section 4.3, Table 6.2.2, Sections 7.1–7.3, T-73 to T-77; traceability REQ-024/REQ-027 |
| Required change | Make `AirlineId` the durable business identity and provenance join; make `AirlineKey` the permanent warehouse surrogate; make IATA/ICAO mutable, version-qualified attributes; update tests and facts |
| Proposed wording | “`ref_airlines.csv` has one row per `AirlineId` per `ReferenceVersion`. `AirlineId` is the durable business identity and the only provenance join. `AirlineKey` is the permanent warehouse surrogate, assigned once per `AirlineId`, and is the only fact-table join. `AirlineIATACode` and `AirlineICAOCode` are mutable attributes, unique within a `ReferenceVersion`; they are not business keys.” Draft D-3: “The durable identity is `AirlineId`; `AirlineKey` is the warehouse key; IATA and ICAO are attributes.” |
| Dependencies | D-01; owner approval; contract edit before draft; A-04 for history |
| Verification | T-73/T-74 format and within-version uniqueness; T-75 joins on `AirlineId`; T-77 reconciles `AirlineId` and `AirlineKey`; T-78 version integrity |
| Owner approval | Yes — changes identity and provenance schema |
| Blocks | Signature: yes. Schema freeze: yes. Implementation: yes |

### A-04 — Define Type 1/Type 2, effective dating and `AirlineKey` stability

| Field | Detail |
|---|---|
| Priority / findings | P1 / H-03 |
| Affected documents | Draft Section 3.2, Section 6.5, Section 8.1, Section 9; contract Section 4.3, Section 7, T-77; add T-78; traceability REQ-027/REQ-028; ledger G3 |
| Required change | Declare Type 1 baseline; define permanent keys; define version-level effective dating; define Type 2 trigger; add historical reconciliation and T-78 |
| Proposed wording | “`DimAirline` is Type 1 for the baseline: one row per airline, stable `AirlineKey`, stable `AirlineId`, and a technical `ReferenceVersion` column. Identity history is preserved in immutable reference versions. `AirlineKey` and `AirlineId` are never reused or reassigned. Type 2 is deferred; if adopted, add `AirlineVersionKey` and keep `AirlineKey` durable.” |
| Dependencies | D-02; A-03; A-07 for T-78; owner approval |
| Verification | T-78-09/10 key stability and historical reconciliation; reconciliation note for any identity change |
| Owner approval | Yes — architecture and history-retention decision |
| Blocks | Signature: yes. Schema freeze: yes. Implementation: yes |

### A-05 — Add suspension/cessation, post-refresh version change and historical inconsistency risks

| Field | Detail |
|---|---|
| Priority / findings | P1 / H-04 |
| Affected documents | Draft Section 9; contract Section 4.3; risk register; T-78; scope/BR/master only if they restate risk |
| Required change | Add lifecycle status and effective dating; add version pinning and refresh checks; add historical re-mapping/reconciliation; add risks R-09 to R-11 and controls |
| Proposed wording | Add R-09 “Airline suspended or ceases operations” with `LifecycleStatus`, `IsActive`, `StatusEffectiveDate`; R-10 “Reference dataset updated after refresh” with one approved `ReferenceVersion` and T-78; R-11 “Historical facts inconsistent with changed identity” with permanent `AirlineKey`, no re-keying and T-78-09/10. |
| Dependencies | A-04; A-07; owner approval |
| Verification | Risk-register review; T-78 execution plan; reconciliation note |
| Owner approval | Yes — policy and test-register change |
| Blocks | Signature: yes. Schema freeze: yes. Implementation: yes |

### A-06 — Define G3 status semantics and gate criteria

| Field | Detail |
|---|---|
| Priority / findings | P1 / H-05 |
| Affected documents | Draft line 19 and Section 13; contract Sections 13.1 and 15; `PROGRESS_LEDGER.md` row 9; master prompt Section 15; traceability status vocabulary |
| Required change | Define gate statuses separately from test and decision statuses; replace the contradictory `NOT STARTED` description; add G3 entry/exit criteria |
| Proposed wording | Gate statuses: `NOT STARTED`, `IN PROGRESS`, `READY FOR REVIEW`, `APPROVED`, `BLOCKED`. Ledger row: “G3 — IN PROGRESS. Data contract v1.4 exists; OD-01, schema freeze, reference-version approval, validation implementation and gate review remain outstanding.” Do not change the actual status in this task. |
| Dependencies | D-13; owner approval; A-04/A-07 for exit criteria |
| Verification | Ledger review; gate checklist; no status change without owner approval |
| Owner approval | Yes — changes governance reporting |
| Blocks | Signature: yes (status clarity). Schema freeze: no. Implementation: no |

### A-07 — Add T-78 airline identity reference-version and manifest integrity test

| Field | Detail |
|---|---|
| Priority / findings | P1 / H-06 |
| Affected documents | Draft Section 8.3; contract Section 13.3 and T-77; traceability REQ-028; ledger evidence; Power BI refresh specification |
| Required change | Add T-78 with ten sub-checks across `ref_airlines.csv`, `ref_airline_sources.csv`, generation manifest, `DimAirline.ReferenceVersion` and Power BI `SelectedReferenceVersion`; add evidence file |
| Proposed wording | “T-78 verifies that exactly one approved airline identity `ReferenceVersion` is used by the reference files, the generation manifest, the curated dimension and the selected Power BI refresh configuration, and that `AirlineKey`/`AirlineId` are stable across the prior and current versions. Evidence: `qa/results/airline_identity_versions.csv`.” |
| Dependencies | D-11, D-12; A-03/A-04; contract edit; owner approval |
| Verification | T-78-01 to T-78-10; evidence file with hashes and reviewer |
| Owner approval | Yes — adds a validation obligation |
| Blocks | Signature: yes. Schema freeze: yes. Implementation: yes |

### A-08 — Add verifier/reviewer role, completeness checklist and reference-version approval

| Field | Detail |
|---|---|
| Priority / findings | P1 / M-07 |
| Affected documents | Draft Section 12, Section 13; contract Sections 14.1 and 16.4; approval template; new OD-23 or G3-RV-01 |
| Required change | Add named reviewer/verifier, independence statement, checklist, compensating controls, and a reference-version approval decision with owner and criteria |
| Proposed wording | “A named reviewer/verifier who is not the preparer checks completeness, evidence, hashes, scope and unresolved findings. If no separate person is available, the record states the limitation and applies the compensating controls in Section 10.3. Reference-version approval is a separate decision (proposed OD-23) approving the exact version, file hashes, source evidence, T-75/T-76 and T-78 plan/results.” |
| Dependencies | D-15; owner approval; A-09 for scope; A-07 for T-78 |
| Verification | Reviewer checklist; signed reviewer result; OD-23 record; no blank “verified” |
| Owner approval | Yes — changes approval process |
| Blocks | Signature: yes. Schema freeze: yes (reference approval). Implementation: no |

### A-09 — Narrow the approval scope or split OD-01

| Field | Detail |
|---|---|
| Priority / findings | P1 / M-12 |
| Affected documents | Draft Sections 4.1, 4.2, 12; contract Section 14; scope/BR/master only if they describe approval scope |
| Required change | Stop approving Sections 2–7 while disclaiming a schema freeze; split into OD-01A/OD-01B or narrow to Sections 2, 4, 5 and 6 and acknowledge Section 7 as proposed |
| Proposed wording | OD-01A: “Approve the ten identities as the fixed population and `AirlineName` as the commercial brand; no reference values, optional attributes, reference schema, schema freeze, data generation or G3 closure.” OD-01B: “Approve the identity and reference rules in Sections 4–7; no reference CSV population, schema freeze, data generation or G3 closure.” |
| Dependencies | D-14; owner approval; A-01/A-02/A-03 for scope clarity |
| Verification | Approval-block review; no contradiction with exclusions; reviewer checklist |
| Owner approval | Yes — changes approval scope |
| Blocks | Signature: yes. Schema freeze: no. Implementation: no |

### A-10 — Define `HomeCountry`, `AirlineGroup`, `OperatingRegion` and `BusinessModel`

| Field | Detail |
|---|---|
| Priority / findings | P2 / M-01 to M-04 |
| Affected documents | Draft Section 3.1, Section 6.3; contract Table 6.2.2, Section 3.4, Section 4.3; scope Section 5; BR-01; master prompt Section 4/13; traceability REQ-023/REQ-026; data dictionary |
| Required change | Define home country and group; remove region from identity or define a controlled basis; treat business model as analytical rubric |
| Proposed wording | `HomeCountry`: “country of principal headquarters/domicile, not incorporation, AOC state or ownership.” `AirlineGroup`: “ultimate parent company or group brand; optional; null if independent or unverified.” `OperatingRegion`: “removed from identity; derive at report layer if needed.” `BusinessModel`: “optional analytical classification under the Appendix A rubric; not source-verified identity; null allowed.” |
| Dependencies | D-04 to D-07; owner approval; A-02 for provenance scope |
| Verification | T-72/T-75 for identity attributes; rubric review; schema check that analytical attributes are excluded |
| Owner approval | Yes — changes identity attribute set |
| Blocks | Signature: no if excluded from OD-01A; schema freeze/implementation: yes |

### A-11 — Define provenance cardinality, vocabulary, authority, evidence and staleness

| Field | Detail |
|---|---|
| Priority / findings | P2 / M-05, M-06 |
| Affected documents | Draft Sections 6.2–6.5 and 7; contract Section 3.4; traceability REQ-025/REQ-026; data dictionary; T-75/T-76 |
| Required change | Add `SourceRecordID` format/uniqueness, one-row-per-assertion grain, controlled `AttributeName`, `IsAuthoritative`, canonicalisation, retrieval date, evidence hash/archive, URL hygiene, staleness and re-verification, supersession links |
| Proposed wording | Use the schema and rules in Section 7. Key sentence: “Every populated identity attribute must resolve to exactly one authoritative `VERIFIED` source record for the same `AirlineId`, `AttributeName`, `AttributeValue` and `ReferenceVersion`; all other records are supporting, conflicting, superseded or quarantined.” |
| Dependencies | D-09, D-10; A-02; A-10 for exclusions; owner approval |
| Verification | T-75/T-76; schema checks for `SourceRecordID` uniqueness, `AttributeName` vocabulary, one authoritative flag, hash/archive presence, staleness |
| Owner approval | Yes — changes provenance policy and schema |
| Blocks | Signature: yes. Schema freeze: yes. Implementation: yes |

### A-12 — Reconcile the three change-control paths into tiers

| Field | Detail |
|---|---|
| Priority / findings | P2 / M-08 |
| Affected documents | Draft D-1, Section 3.2, Section 6.5; contract Section 4.3 and Section 3.4; scope Section 9; master prompt; traceability; data dictionary |
| Required change | Replace overlapping rename/rebrand/code/merger rules with four tiers and one decision tree |
| Proposed wording | Tier 1: evidence/correction, new source record/version if value changes. Tier 2: identity attribute change (name, code, country, group, lifecycle), new reference version, same keys. Tier 3: roster/structural change (merger, cessation, add/remove/substitute), new owner decision and scenario. Tier 4: schema/key/SCD change, new contract version and schema-freeze review. |
| Dependencies | D-16; A-04; A-05; owner approval |
| Verification | Cross-document review; scenario table in Section 5.3; T-78 for version changes |
| Owner approval | Yes — changes change-control policy |
| Blocks | Signature: yes. Schema freeze: yes. Implementation: no |

### A-13 — Add the `DimAirline`/`DimAircraft` filter-path constraint

| Field | Detail |
|---|---|
| Priority / findings | P2 / M-09 |
| Affected documents | Draft Section 8.1; contract Section 8.3; model specification; OD-01 impact section |
| Required change | State that `DimAirline` must not have an active relationship to `DimAircraft`; document the role-playing or `TREATAS` option |
| Proposed wording | “`DimAirline` must not have an active relationship to `DimAircraft`, because `DimAirline` already filters `FactFlightOperations` directly. Activating both creates an ambiguous filter path. Fleet-by-airline analysis uses a role-playing `DimAirline - Fleet` dimension related to `DimAircraft`, or a documented `TREATAS` measure. The baseline does not require this role; any addition must pass T-42 and T-43.” |
| Dependencies | None for wording; model design at G3/G4 |
| Verification | Model relationship inventory; T-42/T-43 |
| Owner approval | No — documentation correction |
| Blocks | Signature: no. Schema freeze: no. Implementation: yes (model build) |

### A-14 — Label the 99 checks correctly and add missing hashes

| Field | Detail |
|---|---|
| Priority / findings | P2 / M-10, L-03 |
| Affected documents | Draft Section 14 and evidence register; migration report reference; audit report reference; no edit to the audit report |
| Required change | Label the 99 checks as reported by the migration script and not independently re-executed; add migration report, backup manifest and draft hashes; cite the audit |
| Proposed wording | “Migration report: complete; 99 checks reported by the migration script; not independently re-executed. These checks are document-integrity evidence, not decision-quality assurance. Migration report SHA256: `EFA6060B...`; backup manifest SHA256: `87D1A446...`; draft SHA256: `C594DFCD...`; audit report SHA256: `FD94BD36...`.” |
| Dependencies | A-16 for evidence-register structure |
| Verification | Evidence-register review; hash verification |
| Owner approval | No — documentation correction |
| Blocks | Signature: no. Schema freeze: no. Implementation: no |

### A-15 — Fix disclosure qualifier, canonical string, exports and exact-string test

| Field | Detail |
|---|---|
| Priority / findings | P2 / M-11 |
| Affected documents | Draft Section 5; scope Section 5; contract Section 2/16; master prompt Section 4/13; report theme and export templates; T-79 |
| Required change | Remove “where practical”; use one em-dash string; require page, tooltip, export and screenshot disclosure; add T-79 |
| Proposed wording | “Every dashboard page, tooltip, export and screenshot must carry the exact string `Synthetic Simulation — Not Actual Airline Performance` (em dash U+2014). No exception is permitted without owner sign-off and a documented compensating disclosure. T-79 verifies the exact string in the report definition and rendered output.” |
| Dependencies | D-17; A-16 for evidence; owner decision only if exceptions are requested |
| Verification | T-79 exact code-point check; rendered page/tooltip/export screenshots |
| Owner approval | Wording: no. Exceptions: yes |
| Blocks | Signature: no. Schema freeze: no. Implementation/report release: yes |

### A-16 — Add preparer/reviewer fields, revision history, retention and signed-copy hash

| Field | Detail |
|---|---|
| Priority / findings | P2 / M-13, L-04, L-05 |
| Affected documents | Draft header, Sections 12, 14 and 15; contract Sections 14.1/16.4; approval template; `docs/approvals/` (not created) |
| Required change | Add `Prepared by`, `Reviewed by`, revision history, hash register, read-only signed copy and retention rule |
| Proposed wording | Add a document-control table: prepared by/date, reviewed by/date, revision, change summary, status; evidence register with all hashes; “The signed copy is stored read-only in `docs/approvals/`; its SHA-256 is recorded in the decision register; the signed copy is never edited; corrections create a new version.” |
| Dependencies | A-14; owner approval for retention policy |
| Verification | Document-control review; hash before/after signature; retention-folder check |
| Owner approval | Documentation: no. Retention policy: yes |
| Blocks | Signature: yes. Schema freeze: no. Implementation: no |

### A-17 — Fix low findings L-01, L-02, L-06, L-07 and L-08

| Field | Detail |
|---|---|
| Priority / findings | P3 / L-01, L-02, L-06, L-07, L-08 |
| Affected documents | Draft heading, Section 7 table, Section 6.5, evidence register; scope Section 2.1/5; contract document control, C-02/C-08 and Section 3.4; master prompt Sections 2/4/13; traceability |
| Required change | Rename roster heading; add types/nullability; add `SupersededBySourceRecordID`; change present-tense “source-verified”; define `ReferenceVersion` format |
| Proposed wording | Heading: “Intended airline population (approved as intended population; formal OD-01 pending).” Present tense: “real, to be source-verified” or “real; source verification pending.” Version: “`AIR-YYYY-MM-DD-NNN`; regex `^AIR-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$`.” |
| Dependencies | A-03/A-11 for schema fields; A-16 for evidence register |
| Verification | Text scan; table schema check; T-78 format check; T-75/T-76 supersession check |
| Owner approval | No — documentation correction |
| Blocks | Signature: no. Schema freeze: no. Implementation: no |

### A-18 — Adopt the decision brief, split/ADR/Git/reviewer-challenge recommendations

| Field | Detail |
|---|---|
| Priority / findings | P3 / O-01 to O-05 |
| Affected documents | Draft structure; new decision brief; future ADR template; signed-record Git tag; reviewer section; owner decision on split |
| Required change | Add one-page brief; split OD-01A/B; use ADR for future decisions; commit/tag after approval subject to authorisation; add reviewer challenge |
| Proposed wording | “This record is a formal decision, not a design specification. The one-page brief states the decision, scope, exclusions, evidence, risks and signature. Detailed rules are appendices. Future decisions use a short ADR. The signed record is committed and tagged only after approval and separate authorisation. Reviewer dissent and residual concerns are recorded before signature.” |
| Dependencies | D-14, D-18; owner approval; A-08/A-09/A-16 |
| Verification | Brief review; ADR template; Git tag later; reviewer section present |
| Owner approval | Yes for split and Git/retention; no for structure |
| Blocks | Signature: no. Schema freeze: no. Implementation: no |

### 12.1 Action coverage check

| Group | Total | Mapped | Notes |
|---|---:|---:|---|
| P1 actions | 9 (A-01 to A-09) | 9 | All block signature |
| P2 actions | 7 (A-10 to A-16) | 7 | A-10/A-11/A-12 also block schema freeze or implementation |
| P3 actions | 2 (A-17, A-18) | 2 | Mostly documentation; split/Git require owner approval |
| **Total** | **18** | **18** | No action omitted or merged |

---

## 13. Cross-document impact matrix

### 13.1 Classification legend

| Class | Meaning |
|---|---|
| **A — Mandatory** | Required for consistency with the corrected identity, provenance, reference-version or approval model; must be applied in the controlled change set |
| **B — Optional improvement** | Useful for readability or assurance but not required to close a finding |
| **C — Owner decision** | Cannot be applied until the owner chooses the option in Section 15 |
| **D — Deferred to G3** | Design may reference it, but the artifact or approval belongs to the G3 gate |
| **E — Deferred to G4/implementation** | Requires data generation, model build, runtime testing or Git authorisation |

### 13.2 Impact matrix

| Document | A — Mandatory | B — Optional | C — Owner decision | D — Deferred to G3 | E — Deferred to G4/implementation |
|---|---|---|---|---|---|
| `01_PROJECT_SCOPE.md` | Change present-tense “real, source-verified” to “real, to be source-verified”; rename roster heading; align identity attribute summary and exact disclosure string | Add a one-line reference-version note | Remove `OperatingRegion`; define `BusinessModel` as analytical | — | — |
| `02_BUSINESS_REQUIREMENTS.md` | Change BR-01 present tense; add provenance and reference-version integrity to BR-01 evidence | Add a sentence that identity rules are governed by the contract | — | — | — |
| `03_DATA_CONTRACTS.md` | Doc control/C-02/C-08 tense; Section 3.4 identity/provenance; Section 4.3 DimAirline; Table 6.2.2; Sections 7.1–7.3 keys; Section 13.3 tests; Section 14 OD-01/OD-23; Section 15 acceptance; Section 16 change log | Add data-dictionary cross-reference; add a short identity-model rationale | Type 1 vs Type 2; `OperatingRegion` removal; `BusinessModel` analytical; new fields; OD-23/REQ-028 | Schema freeze; reference-version approval; T-78 implementation plan | Reference CSV population; data generation; model build |
| `AEROVISION_360_MASTER_BUILD_PROMPT.txt` | Change present-tense identity wording; exact disclosure string; gate vocabulary; identity definitions; reference-version integrity | Add a reference-version note | — | G3 entry/exit criteria | Build phases |
| `REQUIREMENTS_TRACEABILITY.md` | Add REQ-028 for airline identity reference-version/manifest integrity; update REQ-023/024/025/027 wording for `AirlineId`/`AirlineKey` and version-qualified keys | Add REQ-029 for disclosure integrity if the owner wants a separate requirement | Approve REQ-028/REQ-029 | Update statuses only after evidence | Link implementation/test evidence |
| `PROGRESS_LEDGER.md` | Replace the contradictory G3 evidence sentence; record the gate vocabulary; keep G4 BLOCKED | Add a reference to the G3 criteria | Change G3 to `IN PROGRESS` | G3 review and approval | G4 authorisation |
| `OD01_FORMAL_DECISION_RECORD_DRAFT.md` | All 33 findings and 18 actions in scope; correct or split; add reviewer, revision, evidence, disclosure, T-78 and approval scope | One-page brief; ADR-style summary; appendices | Split OD-01A/B; add fields; choose Type 1; remove region; business model | Exclude schema freeze and reference values explicitly | — |
| `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` | **No change** — preserve as point-in-time evidence | Optional closure/remediation report, separate file | — | Re-audit against corrected draft | — |
| `04_DATA_DICTIONARY.md` | Required at G3; must align with contract v1.5 | Outline now | Approve new fields and analytical attributes | Create and review at G3 | Use in build |
| `ref_airlines.csv` | Schema design only; do not create | — | Approve values and optional attributes | Reference-version approval | Populate under separate authorisation |
| `ref_airline_sources.csv` | Schema design only; do not create | — | Approve provenance policy and staleness | T-75/T-76 implementation | Populate under separate authorisation |
| `data/manifests/reference_versions.csv` | Design only; not created | — | Approve version register format | Create at G3 | Use in generation/refresh |
| Power BI files | Filter-path constraint; disclosure; `SelectedReferenceVersion` parameter | Theme and export template | Approve model design | Schema freeze | Build, refresh, T-42/T-43/T-78/T-79 |
| Git repository | No operation in this task | Commit/tag after approval | Authorise Git operations | Tag after signature | Commit/tag signed record and release |

### 13.3 Change-control rules

- `03_DATA_CONTRACTS.md` is the canonical rule source. The OD-01 draft and all other documents must cross-reference it rather than restate a different rule.
- The audit report is not edited. It records the state at audit time; closure is proved by a separate re-audit report.
- Scope, business requirements and master prompt should summarise the identity boundary, not duplicate the full schema.
- The progress ledger records status and evidence, not design detail.
- The traceability matrix records requirement-to-evidence links, not a second contract.
- No document may approve a decision, freeze a schema or authorise generation on behalf of the owner.

---

## 14. Dependency-aware implementation sequence

### 14.1 Execution phases

| Phase | Work | Depends on | Outputs | Gate / stop condition |
|---|---|---|---|---|
| 0 | Owner decisions and baseline freeze | Verified hashes | Decision brief covering Section 15 | Stop if any hash differs or a decision is missing |
| 1 | Contract v1.5 architecture | Phase 0 decisions D-01 to D-12 | Identity, attribute, provenance, lifecycle, T-78 and approval rules | Stop if Type 1/2 or key model is undecided |
| 2 | Traceability and data-dictionary alignment | Phase 1 | REQ-028, updated REQ-023/024/025/027, dictionary outline | Stop if T-78 has no requirement link |
| 3 | OD-01 draft rewrite or split | Phase 1 and Phase 2 | OD-01A/OD-01B or corrected OD-01 v0.2 | Stop if approval scope is ambiguous |
| 4 | Cross-document alignment | Phase 3 | Scope, BR, master, ledger and traceability aligned | Stop if any document restates a conflicting rule |
| 5 | Independent review and re-audit | Phase 4 | Reviewer sign-off; re-audit report; HIGH findings closed | Stop if any HIGH remains open or a new HIGH appears |
| 6 | Owner signature | Phase 5 | Signed OD-01A/B; decision date; evidence; hash | Stop if reviewer dissent is unresolved or signature fields incomplete |
| 7 | G3 gate review and schema freeze | Phase 6 | OD-23, schema freeze, data dictionary, gate record | G3 can move to READY FOR REVIEW/APPROVED only with evidence |
| 8 | G4 and build | Phase 7 + written G4 authorisation | Reference files, data, model, tests, reports | G4 remains BLOCKED until authorised |

### 14.2 Dependency graph

```text
D-01/D-02 key and history model
        |
        v
D-03..D-08 attribute and lifecycle semantics
        |
        v
D-09/D-10 provenance and evidence
        |
        v
D-11/D-12 reference-version and T-78
        |
        v
Contract v1.5 ---> Traceability/Data dictionary ---> OD-01 draft/split
                                                        |
                                                        v
                                             Cross-document alignment
                                                        |
                                                        v
                                             Independent review/re-audit
                                                        |
                                                        v
                                                Owner signature
                                                        |
                                                        v
                                             G3 review/schema freeze
                                                        |
                                                        v
                                             G4 (written authorisation)
```

### 14.3 Sequencing rules

- Do not edit the same architectural decision in two documents at different times. Decide once, write it in the contract, then make every other document reference it.
- Do not rewrite the draft before the contract is corrected; otherwise the draft will encode rules that the contract does not support.
- Do not re-audit before all cross-document edits are complete; otherwise the audit will find avoidable inconsistencies.
- Do not sign before the re-audit closes the HIGH findings and M-07/M-12.
- Do not change G3 or G4 as part of a documentation edit; gate changes need their own owner-approved record.
- Do not populate reference CSVs, generate data, build Power BI or tag Git until the relevant gate and written authorisation exist.

### 14.4 Stop conditions

- Any authoritative hash differs from Section 2.1.
- An owner decision in Section 15 is unresolved but the change depends on it.
- A new HIGH finding appears during re-audit.
- A required source cannot be verified and the design tries to infer a value.
- A reference version or schema freeze is requested without the approval record.
- A Git or data-generation action is requested without explicit authorisation.

---

## 15. Outstanding owner decisions

No owner decision is recorded by this specification. The table below is the decision brief the owner must resolve before the contract or draft is edited. “Recommended” is a design recommendation, not an approval.

| ID | Owner decision | Recommended option | Main alternative | Impact if deferred | Blocks |
|---|---|---|---|---|---|
| OD-R-01 | Split OD-01 into population and identity/reference rules? | Split into OD-01A and OD-01B | One corrected record | Review remains long and scope ambiguous | Signature |
| OD-R-02 | Adopt `AirlineId` + permanent `AirlineKey` + mutable IATA/ICAO? | Yes | Keep IATA as business key with version qualifier | H-07 remains open | Signature, schema freeze |
| OD-R-03 | Type 1 baseline with versioned reference snapshots? | Yes; Type 2 deferred | Type 2 now | Complexity and fact-key changes | Signature, schema freeze |
| OD-R-04 | `AirlineName` = commercial brand plus optional `LegalName`? | Yes | Legal name as display name; no legal name | H-01 remains open | Signature |
| OD-R-05 | `HomeCountry` = principal headquarters/domicile? | Yes | Incorporation or AOC state | M-01 remains open | Signature |
| OD-R-06 | `AirlineGroup` = ultimate parent/group brand? | Yes; optional; null if unverified | Immediate parent or airline brand | M-02 remains open | Signature |
| OD-R-07 | Remove `OperatingRegion` from identity? | Yes; derive analytically if needed | Controlled region vocabulary with defined basis | M-03 remains open | Schema freeze |
| OD-R-08 | Treat `BusinessModel` as analytical rubric? | Yes; optional; null allowed | Source-verified identity attribute | M-04 remains open | Schema freeze |
| OD-R-09 | Add `LifecycleStatus`, `StatusEffectiveDate`, `MergedIntoAirlineId`? | Yes | Boolean `IsActive` only | H-04 remains open | Signature, schema freeze |
| OD-R-10 | Add REQ-028, T-78 and OD-23? | Yes | Extend T-77 and reuse existing approval | H-06/M-07 remain open | Signature, schema freeze |
| OD-R-11 | Adopt `AIR-YYYY-MM-DD-NNN` version format? | Yes | Free-text version | T-78 cannot be deterministic | Signature |
| OD-R-12 | Require evidence hash/archive, retrieval date and staleness? | Yes; hash required, archive optional | URL + verification date only | M-06 remains open | Signature, schema freeze |
| OD-R-13 | Add `ReferenceVersion` to `DimAirline`? | Yes; technical column | Derive version only from manifest | T-78 cannot compare the dimension | Schema freeze |
| OD-R-14 | Change G3 to `IN PROGRESS`? | Yes, after owner approval | Keep `NOT STARTED` with a note | H-05 reporting contradiction remains | G3 review |
| OD-R-15 | Add named reviewer/verifier and compensating controls? | Yes; document independence limitation | Owner-only approval | M-07 remains open | Signature |
| OD-R-16 | Rename `BusinessModel` to `BusinessModelClass` and/or remove it? | Rename if retained; removal also acceptable | Keep ambiguous name | M-04 clarity remains | Schema freeze |
| OD-R-17 | Adopt signed-copy retention, hash register and Git tag? | Yes; tag after approval with authorisation | Working-folder copy only | M-13/O-04 remain open | Signature/Git |
| OD-R-18 | Add `LegalName` to `DimAirline`? | Yes, optional | Keep legal names out of the model | H-01 partially unresolved | Schema freeze |

### 15.1 Decision-record rule

Each decision must record the selected option, rejected alternatives, rationale, impact on tables/KPIs/requirements, approver, date and evidence. A verbal direction or a line in this specification is not an owner approval. Until the decision is recorded, the affected design remains proposed.

---

## 16. Risks and deferred work

### 16.1 Residual risks

| ID | Risk | Impact | Mitigation | Owner |
|---|---|---|---|---|
| R-01 | No source verification has been performed | Roster values remain intended, not verified; reference build cannot start | T-75/T-76 with real sources; no fabrication; block approval if evidence missing | Reference steward |
| R-02 | Self-audit and self-design, no independent reviewer | Findings may be missed; approval weaker | Named reviewer; compensating controls; re-audit; state limitation | Owner |
| R-03 | Type 1 cannot report as-was identity | Historical identity changes are not visible in the dimension | Version snapshots; Type 2 trigger; reconciliation note | Architecture lead |
| R-04 | Schema churn from new fields | Rework if owner rejects `AirlineId`, lifecycle or provenance fields | Owner decisions before contract edit; change control | Owner |
| R-05 | Reference-version drift | Facts and dimension use different snapshots | One approved version; T-78; refresh parameter | Power BI architect |
| R-06 | Code reassignment or retirement | Wrong airline mapping | Stable `AirlineId`; version-qualified codes; no overlap; reconciliation note | Reference steward |
| R-07 | Source URL decay or content change | Evidence no longer reproducible | Retrieval date; evidence hash/archive; staleness; quarantine | Reference steward |
| R-08 | Legal/trademark or endorsement concern | Reputational exposure | Synthetic disclosure; no affiliation claim; legal review before release | Owner |
| R-09 | G3 status ambiguity persists | Gate reporting unreliable | Gate vocabulary; owner-approved status correction | Owner |
| R-10 | Owner decision fatigue / review overload | Delays or rubber-stamping | Split OD-01; one-page brief; decision table | Owner |
| R-11 | Pressure to generate data before governance | Premature G4 and rework | G4 remains BLOCKED; stop conditions | Owner |
| R-12 | Ambiguous `DimAirline`/`DimAircraft` filter path | Wrong fleet-by-airline counts | No active relationship; role-playing/TREATAS; T-42/T-43 | Power BI architect |
| R-13 | Disclosure omitted or string mismatch | Misleading simulated performance | Exact em-dash string; unconditional placement; T-79 | Report owner |
| R-14 | One-person control weakness | Self-approval without challenge | Reviewer/compensating controls; checklist; dissent section | Owner |

### 16.2 Deferred work

| Item | Reason deferred | Gate / owner |
|---|---|---|
| Type 2 SCD | Not required for fixed roster/period; adds fact-key complexity | G3, if as-was reporting is required |
| Code-history reference | Baseline has no code changes; version snapshots suffice | G3, if code churn occurs |
| Source-archive repository | Evidence hash may be sufficient for portfolio; archive optional | G3/owner |
| OD-23 reference-version approval | Needs a version to approve | G3 |
| REQ-028 / T-78 | Design defined; implementation not authorised | G3 |
| T-79 disclosure test | Needs report/export artifacts | G4/report release |
| `04_DATA_DICTIONARY.md` | Not created in this task | G3 |
| Reference CSV population | No source verification and no authorisation | G4 |
| Data generation | G4 BLOCKED | G4 |
| Power BI model/report | G6–G8 | G4+ |
| Git commit/tag | Requires explicit authorisation | After signature |
| Independent external review | No separate reviewer engaged | Before signature if possible |

### 16.3 Residual limitations

This specification does not verify any airline identity, does not create reference data, does not implement tests, does not build a semantic model and does not prove that the proposed architecture works in Power BI. It is a design package for owner review. The audit's independence limitation remains: the same assistant prepared the draft and the audit; a separate human reviewer is recommended before signature.

---

## 17. Final readiness assessment

### 17.1 Assessment

| Dimension | Assessment | Evidence |
|---|---|---|
| Finding coverage | **33/33 mapped** | Section 11 |
| Action coverage | **18/18 mapped** | Section 12 |
| HIGH findings | **7/7 have explicit proposed resolutions** | Section 11.1 |
| Identity architecture | Designed; owner decisions pending | Sections 4–5 |
| Provenance architecture | Designed; owner decisions pending | Section 7 |
| Reference-version integrity | Designed; T-78 not implemented | Section 8 |
| G3 model | Designed; status unchanged | Section 9 |
| Approval controls | Designed; reviewer not engaged | Section 10 |
| Cross-document impact | Identified and classified | Section 13 |
| Implementation sequence | Defined | Section 14 |
| Owner decisions | 18 proposed; none recorded | Section 15 |
| Internal consistency | Checked against contract v1.4 and audit findings | This document |
| Signature readiness | **NOT READY** until contract v1.5, draft v0.2/split, owner decisions and re-audit | Sections 14–15 |
| Schema-freeze readiness | **NOT READY** | Sections 14–15 |
| G3 | **NOT STARTED** — recommended `IN PROGRESS` after owner approval | Section 9 |
| G4 | **BLOCKED** | Progress ledger |

### 17.2 What must happen next

1. The owner records decisions OD-R-01 to OD-R-18, or explicitly defers them.
2. A separate authorised task applies the approved decisions to `03_DATA_CONTRACTS.md` as version 1.5.
3. Traceability and the data-dictionary outline are aligned; REQ-028/T-78 are added if approved.
4. The OD-01 draft is rewritten or split into OD-01A/OD-01B.
5. Scope, business requirements, master prompt and progress ledger are aligned.
6. An independent reviewer or documented compensating control reviews the package.
7. The corrected draft is re-audited; all HIGH findings and M-07/M-12 must close.
8. The owner signs OD-01A/OD-01B with a real date and evidence reference.
9. G3 proceeds to `READY FOR REVIEW` and then `APPROVED` only with the gate package.
10. G4 remains blocked until a separate written authorisation exists.

### 17.3 Final statement

This specification is **design-complete for owner review**, not approved, not signed and not implemented. It does not change OD-01, G3 or G4. It does not modify any baseline document, reference CSV, dataset, script, Power BI file or Git state. The recommended path is to decide the 18 owner decisions, correct the contract once, rewrite the draft once, re-audit once, and only then seek signature.

**Current status: OD-01 PENDING · G3 NOT STARTED · G4 BLOCKED · DESIGN COMPLETE — AWAITING OWNER DECISIONS.**

---

## Appendix A — One-page decision brief template

Use this at the top of OD-01A/OD-01B or a corrected OD-01. Keep it to one page.

| Field | Entry |
|---|---|
| Decision ID and title | OD-01A / OD-01B |
| Decision requested | One sentence |
| Population | Ten intended identities; reference to roster |
| What is approved | Population and brand definition, or identity/reference rules |
| What is not approved | Reference values, schema freeze, data generation, G3 closure |
| Key evidence | Contract v1.5, audit, re-audit, source register, T-78 plan |
| Key risks | Source verification absent; Type 1 limitation; one-person review |
| Owner decision | Approve / reject / defer |
| Signature and date | Blank until owner signs |

## Appendix B — Proposed ADR fields for future decisions

`ADR-ID`, `Title`, `Status`, `Context`, `Decision`, `Alternatives`, `Consequences`, `Affected requirements/tests`, `Owner`, `Date`, `Evidence`, `Reviewer`, `Residual concerns`. Use the ADR for one decision; reserve the long record for the enterprise reference design.

## Appendix C — Document hash register (as verified)

| Artifact | SHA256 |
|---|---|
| OD-01 draft | `C594DFCD8FE1B6809E28CBE1B3EE6D24FAA0772D35DD1FE57767FECCD3CA2A60` |
| Audit report | `FD94BD369D3DDDC1AF84C040C27014F112E74B4B0F938CE95B617C7B142BECE6` |
| Data contract v1.4 | `EB1DE0E1B80E9E30B4905740BDD66AB96657073119D63C49AA48445CB06446E2` |
| Progress ledger | `42A00E3A41A9ABBC6B9F930BFE39DD369E6B9681B9F56194921E7145E6F8A7A3` |
| Migration report | `EFA6060BD0D73B48341A238DE460EA0497B3AF2304709489F1B2DF6B15408CA7` |
| Backup manifest | `87D1A446521E661FE64EE41B9FA6F027DAEA22DA2C5EE66203892B2539AB6785` |











