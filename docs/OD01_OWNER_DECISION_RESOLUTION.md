# AEROVISION 360 — OD-01 Owner Decision Resolution

**Technical review and proposed owner decision record for the 18 architecture decisions in the OD-01 remediation specification**

| Document control | Value |
|---|---|
| Document | `docs/OD01_OWNER_DECISION_RESOLUTION.md` |
| Document type | Owner decision resolution — preparation for owner confirmation |
| Status | **PENDING OWNER CONFIRMATION — NOT AN APPROVAL** |
| Prepared | 2026-11-01 |
| Prepared by | Terminal AI agent, technical review facilitator, for KH Mohammad Farhan |
| Project owner / final authority | KH Mohammad Farhan |
| Governing specification | `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` |
| Specification SHA256 | `CC3BCE621142C31B4BB7A46F4CBCB320E640466228184AE2E94E196796F3F8A4` |
| Governing contract | `docs/03_DATA_CONTRACTS.md` version 1.4 |
| OD-01 status | **PENDING** |
| G3 status | **NOT STARTED** |
| G4 status | **BLOCKED** |
| Effect on existing documents | None — no existing document was modified |
| Effect on implementation | None — no schema, reference data, dataset, Power BI file or Git state was changed |

> **Decision-preparation notice.** This document records recommendations for owner confirmation. It does not approve any decision, sign any record, enter a decision date, freeze a schema, approve a reference version, authorise data generation, or change OD-01, G3 or G4. No decision in this document may be cited as approved until the owner completes a separate, signed decision record.

> **No source verification is claimed.** No airline name, code, country, group, region, business model or legal name has been verified against an external source in this task. The roster remains the intended population. All operational and financial data remain synthetic.

---

## 1. Executive decision summary

### 1.1 Result of the technical review

All 18 proposed decisions were reviewed against the remediation specification, the audit findings, the data contract, the Power BI star-schema requirement and the portfolio scope. The proposed direction is largely sound, but four areas need correction before contract editing:

1. **Do not create a separate airline master-data registry.** `AirlineId` should be a stable attribute in the approved reference snapshot and `DimAirline`; `AirlineKey` should be the permanent warehouse key. A separate registry table adds a join and a lifecycle without analytical value.
2. **Do not add the full lifecycle model to a fixed 12-month simulation.** Keep `IsActive` and add one `StatusEffectiveDate` field for effective dating. Defer `LifecycleStatus` and `MergedIntoAirlineId`; a merger or cessation is a Tier 3 scope change, not an unused baseline column set.
3. **Do not create OD-23.** A recurring reference-version approval is an operational gate artifact, not a new OD-series decision. Use `G3-RV-01` with defined criteria. Keep REQ-028 and T-78.
4. **Keep `LegalName` out of the star schema unless a report needs it.** Resolve H-01 by defining `AirlineName` as the commercial brand and keeping an optional, verified `LegalName` in the reference/provenance layer. This narrows `DimAirline` and avoids an unused column.

The most important architectural challenge is **historical semantics**. Type 1 plus immutable reference snapshots preserves build reproducibility, but it does not preserve “as-was” identity labels in historical reports. That is acceptable only because the roster and reporting period are fixed and no identity change is planned. The limitation must be explicit; Type 2 remains the trigger if as-was reporting is later required.

### 1.2 Decision status summary

| Status | Count | Decisions |
|---|---:|---|
| `RECOMMENDED — PENDING OWNER CONFIRMATION` | 14 | OD-R-02, 03, 04, 05, 06, 07, 08, 11, 12, 13, 14, 16, 17, 18 |
| `NEEDS OWNER CLARIFICATION` | 3 | OD-R-01, 09, 15 |
| `NOT RECOMMENDED` | 1 | OD-R-10 as proposed (OD-23); a modified option is recommended |
| `DEFERRED` | 2 sub-options | Type 2 SCD; full lifecycle fields |

No decision is `APPROVED`. The 18 decisions are recorded in Section 5; detailed selected options and rationale are in Section 6.

### 1.3 Key technical challenges

| # | Challenge | Finding |
|---:|---|---|
| 1 | Does `AirlineId` need a separate persistent registry? | No. The approved reference snapshot is the registry; a separate table is unnecessary complexity. |
| 2 | Can `AirlineKey` remain stable across reference snapshots? | Yes. Assign it once per `AirlineId`; never reuse or re-key facts. |
| 3 | Does `ReferenceVersion` belong in `DimAirline`? | Yes, as a hidden technical lineage column. Manifest-only lineage is weaker for T-78. |
| 4 | Does Type 1 plus immutable snapshots preserve history? | It preserves build reproducibility, not as-was semantic identity. Accept the limitation for a fixed roster; use Type 2 only if as-was reporting is required. |
| 5 | Are full lifecycle fields necessary? | No. `IsActive` plus `StatusEffectiveDate` is enough for H-04; defer `LifecycleStatus` and `MergedIntoAirlineId`. |
| 6 | Do OD-01A and OD-01B create unnecessary governance overhead? | They add one record, but they separate a defensible population decision from contested rules. Use one shared evidence index to limit overhead. |
| 7 | Does OD-23 duplicate the existing approval register? | Yes. Use `G3-RV-01` as a recurring reference-version approval artifact, not a new OD ID. |
| 8 | Is evidence archiving necessary? | Not mandatory for every source. A SHA-256 hash, URL, retrieval date and verification date are sufficient for the portfolio; archive is optional. |
| 9 | Is a one-person reviewer control defensible? | Only if it is transparent. Use a named reviewer where possible; otherwise record the self-review limitation and use automated checks plus a peer/mentor second pass. |
| 10 | Is `BusinessModel` an identity attribute? | No. Keep it as an optional analytical classification, or remove it; never source-verify it as identity. |

### 1.4 What the owner is being asked to do

The owner is asked to confirm, reject or defer the 18 selected options in Section 5, and specifically to resolve the eight choices in Section 13. This resolution does **not** authorise contract editing. A separate controlled change task is required after owner confirmation.

---

## 2. Project architecture context

### 2.1 Project boundary

AEROVISION 360 is a portfolio-grade Power BI project: ten real airline identities, a fixed 12-month reporting period from 2025-10-01 to 2026-09-30, and synthetic operational, customer, booking, revenue, cost, disruption, feedback and financial data. The architecture must support a clean star schema, reproducible generation, credible airline comparison and transparent disclosure. It is not an airline master-data management platform.

### 2.2 Three different identities

| Concept | Purpose | Mutability | Used by |
|---|---|---|---|
| `AirlineId` | Durable business identity and provenance link | Immutable; never reused | Reference files, provenance, cross-version lineage |
| `AirlineKey` | Permanent warehouse surrogate | Immutable; never reused | `DimAirline` primary key and every fact foreign key |
| `AirlineIATACode` / `AirlineICAOCode` | Operational attributes | Mutable by new reference version | Display, validation, operational reference |

Conflating these three is the root cause of H-07. IATA is not a key. `AirlineKey` is not a business identity. `AirlineId` is not a fact-table join.

### 2.3 Identity versus analytical classification

| Class | Examples | Source-verified? | In identity reconciliation? |
|---|---|---|---|
| Identity | `AirlineId`, `AirlineName`, IATA, ICAO, `HomeCountry`, `HomeCountryCode`, `AirlineGroup`, `IsActive`, `StatusEffectiveDate` | Yes for airline facts; `AirlineId` is an administrative assignment; `IsActive` baseline is the approved population scope, and a status change requires evidence; `StatusEffectiveDate` requires evidence when populated | Yes; `AirlineId` is the provenance join |
| Analytical | `BusinessModelClass`, derived operating region | No; method and analyst recorded | No |
| Technical | `AirlineKey`, `ReferenceVersion` | Not applicable | Lineage only; hidden in reports |

### 2.4 What this resolution does not authorise

- No contract version change.
- No OD-01 draft edit.
- No audit report edit.
- No requirements or test-register edit.
- No G3 or G4 status change.
- No reference CSV creation or population.
- No synthetic data generation.
- No script, dataset or Power BI file creation.
- No Git operation.
- No signature or approval date.

---

## 3. Verified baseline

### 3.1 Hash verification

| Artifact | SHA256 | Result |
|---|---|---|
| Remediation specification | `CC3BCE621142C31B4BB7A46F4CBCB320E640466228184AE2E94E196796F3F8A4` | MATCH — required gate passed |
| OD-01 draft | `C594DFCD8FE1B6809E28CBE1B3EE6D24FAA0772D35DD1FE57767FECCD3CA2A60` | MATCH |
| Audit report | `FD94BD369D3DDDC1AF84C040C27014F112E74B4B0F938CE95B617C7B142BECE6` | MATCH |
| Data contract v1.4 | `EB1DE0E1B80E9E30B4905740BDD66AB96657073119D63C49AA48445CB06446E2` | MATCH |
| Progress ledger | `42A00E3A41A9ABBC6B9F930BFE39DD369E6B9681B9F56194921E7145E6F8A7A3` | MATCH |
| Project scope | `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` | MATCH |
| Business requirements | `E2FCC8132981C96720E572F01EF353C255CA6BE91F27854950D93FF0DFC1DB6E` | MATCH |
| Master build prompt | `17BD2C6FCADB9E2A917D047B2B2D9716E21CB1709B5A46ABF01AB2833C56D429` | MATCH |
| Requirements traceability | `1AD225D00EA6D5808B6E0050DBFCE10F84CBAEF2B66DE70C4362370BBA9CC751` | MATCH |
| Migration report | `EFA6060BD0D73B48341A238DE460EA0497B3AF2304709489F1B2DF6B15408CA7` | MATCH |
| Backup manifest | `87D1A446521E661FE64EE41B9FA6F027DAEA22DA2C5EE66203892B2539AB6785` | MATCH |

The destination `docs/OD01_OWNER_DECISION_RESOLUTION.md` did not exist before creation. The specification hash was verified before any review or writing.

### 3.2 Authoritative inputs reviewed

| Input | Use in this resolution |
|---|---|
| `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` | 18 decisions, architecture, T-78, approval controls |
| `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md` | Current approval scope and draft contradictions |
| `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` | 33 findings and 18 corrective actions |
| `docs/03_DATA_CONTRACTS.md` v1.4 | Current keys, `DimAirline`, provenance, T-72 to T-77, decision register |
| `docs/01_PROJECT_SCOPE.md` | Fixed roster, synthetic boundary, reporting period |
| `docs/02_BUSINESS_REQUIREMENTS.md` | BR-01 multi-airline comparison |
| `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt` | Fixed roster, identity rules, gate vocabulary |
| `docs/REQUIREMENTS_TRACEABILITY.md` | REQ-001 and REQ-023 to REQ-027 |
| `docs/PROGRESS_LEDGER.md` | G3 `NOT STARTED`; G4 `BLOCKED` |

### 3.3 Current governance state

| Item | State |
|---|---|
| OD-01 | PENDING; draft `PENDING OWNER SIGNATURE` |
| Audit outcome | NOT READY — MATERIAL CORRECTIONS REQUIRED; 61/100 |
| G3 | NOT STARTED |
| G4 | BLOCKED |
| Schema freeze | Not authorised |
| Reference version approval | Not defined; not approved |
| Reference CSV files | 0 |
| Datasets or scripts | 0 |
| Power BI files | 0 |
| Git commits | None recorded |
| Signatures or decision dates | None entered |

### 3.4 Evidence classification

The audit is a structured adversarial self-audit, not independent third-party assurance. The migration report’s 99 checks are document-integrity evidence reported by the migration script; they were not independently re-executed. Neither class proves that the future reference data is verified. This resolution must not upgrade either evidence class.

---

## 4. Technical challenge results

### 4.1 Airline identity and key design

**Verdict: sound, with one simplification.** `AirlineId` and `AirlineKey` are both needed, but they serve different layers. `AirlineId` is the stable business identity used by reference files and provenance. `AirlineKey` is the permanent warehouse surrogate used by facts and Power BI relationships. IATA and ICAO are mutable attributes. No separate airline registry table is needed: the approved `ref_airlines.csv` snapshot is the registry, and `DimAirline` is its curated projection.

**Challenge:** a separate persistent registry would add a second source of airline membership, a join, and a lifecycle that the project does not need. It would also create a new failure mode where the registry and the reference snapshot disagree. Reject it.

**Consequence:** `AirlineId` must be assigned once and never reused. `AirlineKey` must be assigned once and never reused. A rebuild must reproduce the same key for the same `AirlineId`. Facts never join on IATA, ICAO, name or `AirlineId`.

### 4.2 Reference versioning and immutable snapshots

**Verdict: sound.** The version format `AIR-YYYY-MM-DD-NNN`, one approved version per generation/refresh, and immutable snapshots are appropriate. The manifest is the control record; the reference files are the snapshot; `DimAirline.ReferenceVersion` is the lineage link. T-78 is the right control and should not be folded into T-77.

**Challenge:** a version identifier is not an approval. The manifest must carry `Status`, `ApprovedBy`, `ApprovalDate` and `ManifestHash`, and the refresh must pin one approved version. A free-text version or a version that changes after approval would defeat reproducibility. The date in the identifier is the effective date, not the approval date.

**Consequence:** exactly one version per generation and refresh; no mixed versions; no overwrite of a published version; a correction creates a new version and a reconciliation note.

### 4.3 Power BI star-schema compatibility

**Verdict: compatible, with discipline.** A ten-row `DimAirline` is a normal dimension. `AirlineKey` is the relationship key; `AirlineId`, `ReferenceVersion`, `StatusEffectiveDate` and `AirlineKey` should be hidden from report consumers. `AirlineGroup` and `BusinessModelClass` are degenerate attributes, not separate dimensions. `OperatingRegion` should not be stored in `DimAirline`; if needed, derive it from `DimRoute`/`DimAirport` geography.

**Challenge:** the known `DimAirline`–`DimAircraft` filter path must not be activated as a second path. `DimAircraft.AirlineKey` is for lineage/validation, not an active relationship. Fleet-by-airline analysis uses a role-playing `DimAirline - Fleet` dimension or a documented `TREATAS` measure, tested under T-42/T-43.

**Consequence:** one clean star schema; no snowflake airline group/region tables; no active ambiguous path; report filters use `AirlineKey` relationships.

### 4.4 Fact-to-dimension relationships

**Verdict: sound.** Every fact carries `AirlineKey`; it resolves to exactly one `DimAirline` row. No fact carries IATA, ICAO, name or `AirlineId` as a physical relationship key. Orphans block refresh; they are not mapped to a default airline.

**Challenge:** historical facts must not be re-keyed when identity attributes change. Type 1 reports current identity attributes. If a reference version changes a name or code, the fact stays linked to the same `AirlineKey`, but the report label is the current one. That is a semantic limitation, not a key-integrity failure.

**Consequence:** stable keys, no re-keying, no code joins, no silent orphan handling.

### 4.5 Historical reproducibility

**Verdict: build reproducibility yes; as-was semantic history no.** Type 1 plus immutable reference snapshots preserves the exact reference values and provenance used for each build. It does not preserve the identity label that was current when a historical fact occurred. For a fixed 12-month period with a fixed roster and no planned identity change, this is acceptable.

**Challenge:** if an airline is renamed mid-period, Type 1 will show the new name against all historical facts. That may be acceptable for a portfolio, but it must be disclosed. If as-was reporting is required, Type 2 with `AirlineVersionKey` or a bridge is the trigger. Do not pretend Type 1 provides as-was history.

**Consequence:** document the limitation; add a Type 2 trigger; keep `AirlineKey` stable; use T-78 for version/key integrity.

### 4.6 Provenance and source verification

**Verdict: directionally sound, but too heavy if applied indiscriminately.** Every populated source-verified identity attribute needs an authoritative `VERIFIED` record; baseline `IsActive = TRUE` is population scope, and a status change requires evidence. Optional identity attributes remain null without one. Analytical attributes are excluded. `SourceRecordID`, one-row-per-assertion, `IsAuthoritative`, canonicalisation, retrieval date, verification date, evidence hash and supersession links are justified by M-05/M-06.

**Challenge:** mandatory archival of every source is overkill for a portfolio. A SHA-256 hash plus URL, retrieval date and verification date is sufficient; archive is optional for high-risk sources. Staleness rules should be simple and configurable, not a document-management system. `LegalName` and `AirlineGroup` are optional; they do not need to be populated to approve the population.

**Consequence:** T-75/T-76 enforce evidence; no fabrication; optional null is valid; analytical attributes are not forced through identity provenance.

### 4.7 Data quality and reconciliation

**Verdict: sound, with version-qualified uniqueness.** T-72 to T-77 need updating for `AirlineId`, `AirlineKey`, version-qualified IATA/ICAO uniqueness, every-populated-attribute provenance and analytical exclusions. T-78 adds the missing version/manifest/refresh check. T-79 covers disclosure at report release.

**Challenge:** T-73/T-74 currently test uniqueness without a version qualifier. In a multi-version reference file, the same code can appear in two versions. The tests must scope uniqueness to the selected `ReferenceVersion`. T-77 must not compare analytical attributes as identity.

**Consequence:** deterministic tests; no false duplicate failures; no mixed-version refresh.

### 4.8 Implementation complexity

**Verdict: reduce before building.** The full lifecycle model, OD-23, mandatory evidence archive, and `LegalName` in `DimAirline` are unnecessary for this portfolio. Keep the stable key model, reference snapshots, T-78, provenance and disclosure. Use one `StatusEffectiveDate` field instead of three lifecycle fields. Use `G3-RV-01` instead of OD-23. Keep `LegalName` in the reference layer. This preserves auditability while reducing schema and governance overhead.

### 4.9 Portfolio scope and maintainability

**Verdict: appropriate if kept lean.** Ten airlines, one 12-month period, one star schema, reproducible Python generation and a documented Power BI model. The project should demonstrate BI engineering discipline, not enterprise MDM. Every additional field or approval artifact must earn its place in the portfolio narrative.

---

## 5. All 18 owner decisions

| ID | Decision | Status | Selected option | Findings / actions |
|---|---|---|---|---|
| OD-R-01 | Split OD-01 | `NEEDS OWNER CLARIFICATION` | Split into OD-01A population and OD-01B identity/reference rules; one shared evidence index | M-12, O-02 / A-09, A-18 |
| OD-R-02 | Permanent identity | `RECOMMENDED — PENDING OWNER CONFIRMATION` | `AirlineId` durable identity; `AirlineKey` permanent warehouse key; IATA/ICAO mutable attributes; no separate registry | H-07, H-03 / A-03, A-04 |
| OD-R-03 | Historical dimension | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Type 1 baseline + immutable snapshots; Type 2 `DEFERRED` | H-03 / A-04 |
| OD-R-04 | AirlineName | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Commercial brand; optional `LegalName` in reference/provenance, not required in `DimAirline` | H-01 / A-01 |
| OD-R-05 | HomeCountry | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Principal headquarters/domicile; no incorporation/AOC fields in baseline | M-01 / A-10 |
| OD-R-06 | AirlineGroup | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Ultimate parent/group brand; optional/nullable; no group dimension | M-02 / A-10 |
| OD-R-07 | OperatingRegion | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Remove from identity; derive analytical region from route/airport geography | M-03 / A-10 |
| OD-R-08 | BusinessModel | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Optional analytical `BusinessModelClass`; no identity provenance; null allowed | M-04 / A-10 |
| OD-R-09 | Lifecycle management | `NEEDS OWNER CLARIFICATION` | Keep `IsActive`; add `StatusEffectiveDate`; defer `LifecycleStatus` and `MergedIntoAirlineId` | H-04 / A-05 |
| OD-R-10 | Requirements and tests | `NOT RECOMMENDED` as proposed | Add REQ-028 and T-78; do **not** add OD-23; use `G3-RV-01` | H-06, M-07 / A-07, A-08 |
| OD-R-11 | Reference version | `RECOMMENDED — PENDING OWNER CONFIRMATION` | `AIR-YYYY-MM-DD-NNN`; immutable; one approved version per refresh | H-06, L-08 / A-07, A-17 |
| OD-R-12 | Evidence controls | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Retrieval/verification dates, SHA256 hash, optional archive, staleness, supersession | M-05, M-06 / A-11 |
| OD-R-13 | ReferenceVersion in DimAirline | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Keep as hidden technical lineage column; T-78 enforces it | H-06 / A-07 |
| OD-R-14 | G3 status | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Change to `IN PROGRESS` only after owner records the decision; no change now | H-05 / A-06 |
| OD-R-15 | Reviewer controls | `NEEDS OWNER CLARIFICATION` | Named reviewer if available; otherwise transparent compensating control | M-07, M-13 / A-08, A-16 |
| OD-R-16 | BusinessModelClass | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Use `BusinessModelClass` if retained; otherwise remove entirely | M-04 / A-10 |
| OD-R-17 | Signed-copy retention | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Read-only signed copy, SHA256, revision history; Git only after authorisation | M-13, O-04 / A-16, A-18 |
| OD-R-18 | LegalName | `RECOMMENDED — PENDING OWNER CONFIRMATION` | Optional in reference/provenance; not required for population; omit from `DimAirline` | H-01 / A-01 |

**Status note:** `NOT RECOMMENDED` for OD-R-10 applies only to the proposed **OD-23** element. The modified option — REQ-028, T-78 and `G3-RV-01` — is recommended. `DEFERRED` applies to Type 2 and the full lifecycle field set, not to the baseline decision.

---

## 6. Recommended selected option for each decision

### OD-R-01 — Split OD-01 into population and identity/reference decisions

**Status:** `NEEDS OWNER CLARIFICATION`

**Selected option:** Split into **OD-01A — Approved airline population** and **OD-01B — Airline identity and reference-data rules**. Use one shared evidence index and one one-page decision brief to avoid duplicated governance overhead. OD-01A may be signed first; OD-01B depends on the corrected contract and re-audit.

**Technical correctness:** The split separates two different approval objects: the ten-identity population and the rules that govern keys, provenance, history and reference versions. It does not change the schema by itself.

**Business justification:** The population is defensible; the rules are the source of all seven HIGH findings. A single signature over both would force the owner to approve unresolved rules or delay the population unnecessarily.

**Power BI:** No direct impact. The semantic model depends on OD-01B, not on the split.

**Python:** No direct impact. The reference builder depends on OD-01B rules.

**History:** No direct impact. Type 1 and versioning are OD-01B decisions.

**Complexity:** One additional decision record. Shared evidence and a common brief keep the overhead low. A single record with two explicit approval blocks is an acceptable alternative if the owner prefers fewer files.

**Risks / alternatives rejected:** Keeping one broad record preserves M-12 ambiguity and review fatigue. Splitting into more than two records is unnecessary.

**Final recommendation:** Split, with shared evidence. If the owner rejects the split, narrow the single record to population plus identity rules and state that reference-schema details are proposed, not frozen.

**Findings / actions:** M-12 / A-09; O-02 / A-18.

### OD-R-02 — Permanent airline identity and warehouse key

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** `AirlineId` (`String(20)`, format `AIR-0001`) is the permanent business identity and provenance link. `AirlineKey` (`Int32`) is the permanent warehouse surrogate and the only fact-table join. `AirlineIATACode` and `AirlineICAOCode` are mutable attributes, unique within a `ReferenceVersion`. Do **not** create a separate airline registry table; the approved `ref_airlines.csv` snapshot is the registry.

**Technical correctness:** This resolves H-07. A mutable code cannot be a key, a provenance join and a uniqueness test at the same time. Separating `AirlineId` from `AirlineKey` keeps reference lineage readable and the star schema efficient.

**Business justification:** The airline identity remains stable across corrections, code changes and reference versions. Provenance and audit records remain attached to the airline, not to a code that may be reassigned.

**Power BI:** Facts join `AirlineKey`; `DimAirline` has one row per airline. `AirlineId` and `AirlineKey` are hidden from report consumers. No IATA/ICAO/name joins.

**Python:** Build a deterministic `AirlineId` → `AirlineKey` map once. Never derive `AirlineKey` from row order after the initial assignment. Never re-key facts.

**History:** `AirlineId` and `AirlineKey` survive reference versions, Type 1 updates and rebuilds. They are never reused after cessation or merger.

**Complexity:** Low. Two identifiers, one mapping table in the generator, no new dimension.

**Risks / alternatives rejected:** A separate registry adds a second membership source and a join; reject. Using IATA as the key recreates H-07; reject. Using only `AirlineKey` is technically possible but loses a readable, stable reference/provenance identifier; not recommended.

**Final recommendation:** Adopt the two-key model. Record the administrative `AirlineId`/`AirlineKey` allocation in OD-01B; it is a project assignment, not an airline fact.

**Findings / actions:** H-07 / A-03; H-03 / A-04.

### OD-R-03 — Type 1 baseline with immutable reference snapshots

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`; Type 2 `DEFERRED`

**Selected option:** `DimAirline` is Type 1: one row per airline, permanent `AirlineKey`, stable `AirlineId`, and a hidden `ReferenceVersion` lineage column. Reference versions are immutable snapshots. Type 2 is deferred until as-was identity reporting is explicitly required.

**Technical correctness:** Type 1 is sufficient for a fixed ten-airline roster and a fixed 12-month period. It avoids `AirlineVersionKey`, bridge tables and effective-dated facts. Immutable snapshots plus the generation manifest preserve build reproducibility.

**Business justification:** The project compares current airline identities; it does not need to reconstruct which brand or code was displayed on a historical flight. The simpler model is easier to explain and defend in a portfolio.

**Power BI:** Simple star schema; one airline dimension; no bridge; no role-playing version dimension. `ReferenceVersion` is hidden.

**Python:** Generate against one approved snapshot; record the version in the manifest; validate key stability; do not mix versions.

**History:** Build reproducibility is preserved. As-was semantic identity is **not** preserved. If an airline is renamed mid-period, Type 1 shows the current name against all facts. This limitation must be documented; Type 2 is the trigger if as-was reporting becomes necessary.

**Complexity:** Low. Type 2 would add a row key, effective dates, fact-key changes and an as-of test.

**Risks / alternatives rejected:** Type 2 now is over-engineering for a fixed roster. Type 1 without immutable snapshots would destroy reproducibility; reject. Type 1 with a claim of as-was history would be inaccurate; reject.

**Final recommendation:** Adopt Type 1 with snapshots and an explicit as-was limitation. Defer Type 2 and record the trigger.

**Findings / actions:** H-03 / A-04; H-04 / A-05.

### OD-R-04 — AirlineName is the commercial brand

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** `AirlineName` is the approved commercial brand used in the roster and reports. `LegalName` is optional, verified and stored in `ref_airlines.csv` and provenance; it is **not required in `DimAirline`**. Display names use the brand. T-72 compares the canonical brand, not a legal name.

**Technical correctness:** This resolves H-01. It gives one deterministic display attribute and avoids false `CONFLICTING` records when a source returns a legal entity name. Legal names remain available for audit without widening the star schema.

**Business justification:** The portfolio and reports are brand-oriented. Legal entity names are not used for airline comparison and would add noise.

**Power BI:** Airline labels, slicers and report titles use `AirlineName`. No legal-name column is needed in the dimension.

**Python:** Canonicalise the brand (NFKC, trim, collapse whitespace, preserve case/punctuation). Verify `LegalName` only if populated; otherwise leave it null.

**History:** A brand change creates a new reference version with the same `AirlineId`/`AirlineKey`; the old version retains the old brand.

**Complexity:** Low; removes an unnecessary dimension column while keeping optional reference evidence.

**Risks / alternatives rejected:** Using a legal name as the display name recreates H-01. Removing `LegalName` entirely is acceptable but less flexible; it is not recommended if the owner wants legal-entity evidence.

**Final recommendation:** Brand in the dimension; optional legal name in the reference/provenance layer only.

**Findings / actions:** H-01 / A-01.

### OD-R-05 — HomeCountry is principal headquarters or domicile

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** `HomeCountry` is the country of the airline's principal headquarters or domicile. `HomeCountryCode` is the ISO 3166-1 alpha-2 code. Do **not** add incorporation country or AOC state fields in the baseline; record them as out of scope unless a later requirement appears.

**Technical correctness:** “Home country” is otherwise ambiguous. A single definition makes T-72/T-75 deterministic and avoids source conflicts caused by mixing incorporation, AOC and ownership.

**Business justification:** Country comparison and geographic analysis need one consistent basis. Headquarters/domicile is the most useful and source-verifiable basis for this portfolio.

**Power BI:** `HomeCountry`/`HomeCountryCode` support country filters and maps; no extra geography dimension is required.

**Python:** Validate the country name against ISO 3166-1 and the code against alpha-2. Record the source note when headquarters and incorporation differ.

**History:** A country change creates a new reference version with the same keys.

**Complexity:** Low. No new fields beyond the existing country pair.

**Risks / alternatives rejected:** Country of incorporation or AOC state would answer a different question and create conflicts. Adding all three fields is unnecessary for this project.

**Final recommendation:** Adopt headquarters/domicile; document incorporation/AOC as out of scope.

**Findings / actions:** M-01 / A-10.

### OD-R-06 — AirlineGroup is the ultimate parent or group brand

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** `AirlineGroup` is the ultimate parent company or group brand that consolidates the airline. It is optional and nullable. Use the parent group's official source, a government registry, then the airline's corporate source only where it explicitly states the ultimate parent. No separate group dimension.

**Technical correctness:** The boundary is explicit and avoids mixing brand, immediate holding company and ultimate parent. Null is valid when the relationship is independent or unverified.

**Business justification:** Group-level comparison is useful for a multi-airline portfolio, but the project must not infer ownership. A nullable degenerate attribute is sufficient.

**Power BI:** `AirlineGroup` is a slicer attribute on `DimAirline`; null is displayed as “Independent / not verified” or left blank by report design. No snowflake group table.

**Python:** Populate only from a `VERIFIED` source; otherwise null. Do not infer from home country or brand similarity.

**History:** A group change creates a new reference version with the same keys.

**Complexity:** Low; one optional column, no new dimension.

**Risks / alternatives rejected:** Immediate parent is a different concept; reject. A group dimension adds a join and a hierarchy without analytical necessity. Inferring group from ownership assumptions violates the no-fabrication rule.

**Final recommendation:** Keep optional, nullable, source-verified; no group dimension.

**Findings / actions:** M-02 / A-10; H-02 / A-02.

### OD-R-07 — Remove OperatingRegion from identity attributes

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** Remove `OperatingRegion` from `ref_airlines.csv`, `DimAirline` identity reconciliation and T-75. If region analysis is needed, derive an analytical region from `DimRoute`/`DimAirport` geography at the curated/report layer. Do not store a source-verified region in the airline identity.

**Technical correctness:** Region is not a single source-verifiable identity fact for a global airline. Storing it invites arbitrary labels and conflicts. Deriving it from route/airport geography is deterministic and auditable.

**Business justification:** Network and geographic analysis can still be delivered without adding an ambiguous identity field. The airline dimension stays focused on identity.

**Power BI:** Use airport/route geography or a derived region column in `DimRoute`/`DimAirport`; do not add a region slicer sourced from `DimAirline`.

**Python:** Do not generate an identity region. If an analytical region is required, document the mapping and version it with the build configuration.

**History:** No identity versioning is needed for a removed field. Route/airport geography follows its own reference rules.

**Complexity:** Removes a field and a provenance obligation. Low.

**Risks / alternatives rejected:** A controlled six-region vocabulary is possible, but it still needs a declared basis (headquarters vs network). Keeping the current ambiguous field is rejected. A separate region dimension is unnecessary.

**Final recommendation:** Remove it. If the owner insists on a region, define a separate analytical mapping with an explicit basis and keep it out of identity tests.

**Findings / actions:** M-03 / A-10.

### OD-R-08 — BusinessModel is an analytical classification

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** Keep an optional `BusinessModelClass` as an **analytical** attribute, not a source-verified identity attribute. Populate it only from a documented rubric and a versioned analytical mapping; record method, analyst and date. Null is valid. Exclude it from `ref_airlines.csv` identity fields, T-72 and T-75. If the owner does not need the comparison, remove the attribute entirely.

**Technical correctness:** Business model is an analyst taxonomy, not a civil-aviation registry fact. Treating it as identity invites false precision and unsupported provenance. A labelled analytical column avoids that.

**Business justification:** A full-service/low-cost comparison is useful in a portfolio, but it must not be presented as a verified airline identity fact.

**Power BI:** Use `BusinessModelClass` as a slicer with a clear “analytical classification” label; null is allowed. Do not use it in identity reconciliation.

**Python:** Populate from a versioned mapping or generator configuration, not from a source-verification workflow. Record the method and analyst in the build documentation.

**History:** An analytical classification change is a build/report change, not an identity change. Record it in the build manifest; it does not require a new identity reference version unless the owner wants it versioned with the reference snapshot.

**Complexity:** Low if retained; lower if removed.

**Risks / alternatives rejected:** Source-verifying it as identity is rejected (M-04). Keeping the ambiguous name `BusinessModel` is rejected; use `BusinessModelClass` if retained. A separate classification reference file is unnecessary for ten airlines.

**Final recommendation:** Retain as optional analytical `BusinessModelClass` if the portfolio needs the comparison; otherwise remove it.

**Findings / actions:** M-04 / A-10; H-02 / A-02.

### OD-R-09 — Minimal lifecycle management

**Status:** `NEEDS OWNER CLARIFICATION`

**Selected option:** Keep the existing `IsActive` Boolean. Add **one** `StatusEffectiveDate` Date column, nullable, required when `IsActive = FALSE`. All ten baseline airlines are `IsActive = TRUE` with null `StatusEffectiveDate`. Do **not** add `LifecycleStatus` or `MergedIntoAirlineId` in the baseline. A suspension or cessation is a Tier 3 scope change with a new reference version; a merger creating a successor entity is a new scenario and a new `AirlineId`.

**Technical correctness:** H-04 requires an `IsActive` lifecycle and effective dating. One date field provides effective dating without building an unused lifecycle state machine. `LifecycleStatus` duplicates `IsActive` for the baseline, and `MergedIntoAirlineId` implies merger-history machinery the fixed roster does not need.

**Business justification:** The project is a fixed 12-month simulation with ten active airlines. The owner needs a controlled way to record a status change, not a master-data lifecycle platform.

**Power BI:** Hide `StatusEffectiveDate` from report consumers. The baseline has no lifecycle slicer; all ten airlines are active. If a status change occurs, the report can disclose it without changing the star schema.

**Python:** Validate that `IsActive = FALSE` requires a real `StatusEffectiveDate` and an evidence record. Do not generate merger mappings or successor logic in the baseline.

**History:** A status change creates a new reference version; facts retain `AirlineKey`. Previous status/date pairs are preserved in the immutable reference snapshots; the Type 1 dimension carries only the current status and date. The reason for a status change is recorded in the change-control note, not as an extra dimension column. Type 2 as-was identity remains deferred.

**Complexity:** Low: one column and one validation rule. The full lifecycle proposal adds three fields, a state model and merger logic.

**Risks / alternatives rejected:** `IsActive` only fails H-04's effective-dating requirement. The full lifecycle field set is deferred because it is unnecessary for the baseline. If the owner wants mid-period lifecycle events, adopt the full fields and Type 2 in a separate decision.

**Final recommendation:** Adopt the minimal model. If the owner requires full lifecycle/merger tracking, mark this decision `DEFERRED` and keep the fixed-roster assumption.

**Findings / actions:** H-04 / A-05; H-03 / A-04.

### OD-R-10 — Requirements, T-78 and reference-version approval

**Status:** `NOT RECOMMENDED` as proposed (OD-23); modified option recommended

**Selected option:** Add **REQ-028** for airline identity reference-version and manifest integrity. Add **T-78** with the ten sub-checks in the remediation specification. Do **not** create OD-23. Use **`G3-RV-01` — Airline identity reference-version approval** as a recurring gate artifact with the owner, criteria, exact version, file hashes, source evidence, T-75/T-76 results, T-78 plan/results and refresh configuration.

**Technical correctness:** T-78 is necessary because T-77 compares reference to dimension, not reference/manifest/refresh. REQ-028 links the test to a requirement. OD-23 is not technically necessary; it duplicates a recurring operational approval in the OD-series register.

**Business justification:** A recurring reference-version approval is a gate control, not a one-time architecture decision. A gate artifact keeps the decision register focused and still gives the owner accountability.

**Power BI:** The refresh exposes a `SelectedReferenceVersion` parameter; T-78 compares it to the manifest and `DimAirline.ReferenceVersion`. A mismatch blocks refresh.

**Python:** The generator records the version and file hashes in the manifest; T-78 reads the manifest, reference files, dimension and refresh configuration.

**History:** One approved version per generation/refresh; no mixed versions; reconciliation note for identity changes.

**Complexity:** T-78 is moderate but necessary. OD-23 is avoidable overhead. `G3-RV-01` must be defined in the G3 gate package.

**Risks / alternatives rejected:** Extending T-77 only is rejected because it would mix two different integrity questions. OD-23 is rejected as a duplicate decision ID. If the owner insists on an OD ID, use OD-23 but document the duplication and the recurring nature.

**Final recommendation:** REQ-028 + T-78 + `G3-RV-01`. Do not create OD-23.

**Findings / actions:** H-06 / A-07; M-07 / A-08.

### OD-R-11 — Reference version format and immutability

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** `ReferenceVersion` format `AIR-YYYY-MM-DD-NNN`, regex `^AIR-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$`. The date is the effective date; `NNN` is a same-day sequence. A version is immutable after approval. Exactly one approved version is used per generation and refresh. Status lifecycle: `DRAFT`, `READY FOR REVIEW`, `APPROVED`, `RETIRED`, `REJECTED`.

**Technical correctness:** A deterministic format makes the manifest, dimension, refresh parameter and T-78 comparable. The sequence handles multiple versions on one date. Immutability preserves reproducibility.

**Business justification:** A clear version identifier makes the reference data auditable and prevents silent drift between generation and refresh.

**Power BI:** The `SelectedReferenceVersion` parameter must equal the approved manifest version; the column is hidden in `DimAirline`.

**Python:** Write the version to every manifest; hash the reference files; never mutate an approved version.

**History:** Versions are immutable snapshots; a correction creates a new version and a reconciliation note.

**Complexity:** Low. The format is readable; no UUID or database sequence is needed.

**Risks / alternatives rejected:** Free-text versions are not testable. Date-only versions collide. UUIDs are unreadable in a portfolio. The chosen format is appropriate.

**Final recommendation:** Adopt the format and one-version rule.

**Findings / actions:** H-06 / A-07; L-08 / A-17.

### OD-R-12 — Evidence controls and provenance durability

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** Keep `SourceRecordID` (`SRC-000001`, globally unique, never reused), one row per source-attribute assertion, `AirlineId` as the join, controlled `AttributeName`, `IsAuthoritative`, `SourceRetrievedDate`, `SourceVerifiedDate`, SHA-256 `EvidenceHash` required for `VERIFIED`, optional `SourceArchiveRef`, URL/domain hygiene, staleness and re-verification, and reciprocal supersession links.

**Technical correctness:** This resolves M-05/M-06. It makes T-75/T-76 deterministic and prevents an unverified optional value from entering the reference. A hash plus URL and dates is sufficient evidence for a portfolio; mandatory archive is not required.

**Business justification:** The project’s design requires source-verified identities; that claim is not yet earned. The evidence must be reproducible and must not be fabricated. Optional attributes can remain null.

**Power BI:** No direct model impact. Evidence lives in the reference/QA layer, not in the star schema.

**Python:** Validate the schema, URL, dates, hash, authority flag and supersession links. Quarantine stale or conflicting records. Do not load non-`VERIFIED` values.

**History:** Evidence is version-scoped; a new version creates new source records with supersession links; published evidence is immutable.

**Complexity:** Moderate. The schema is detailed but necessary for the provenance claim. Keep the staleness thresholds configurable; do not build a document-management system.

**Risks / alternatives rejected:** URL + verification date only is rejected (M-06). Mandatory archive of every page is overkill. A single row per source document is rejected because it cannot represent per-attribute authority.

**Final recommendation:** Adopt the evidence controls with optional archive and simple staleness thresholds (365 days general; 180 days for codes).

**Findings / actions:** M-05, M-06 / A-11; H-02 / A-02.

### OD-R-13 — Keep ReferenceVersion in DimAirline

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** Keep `ReferenceVersion` (`String(30)`) as a hidden technical lineage column in `DimAirline`. It is populated from the approved manifest and compared by T-78. It is not a business attribute, not a slicer and not a relationship key.

**Technical correctness:** A manifest alone proves which version was approved, but not which version built the dimension. The column is the cheapest way to make T-78 enforceable across reference files, manifest, dimension and refresh. Ten rows make the storage cost negligible.

**Business justification:** The lineage column makes refresh mismatches visible and supports a defensible audit trail.

**Power BI:** Hide the column from report view. Do not use it as a slicer or filter. It is for refresh validation only.

**Python:** Populate it from the selected manifest; reject a build if the value differs across rows.

**History:** It identifies the snapshot that produced the current Type 1 row. It does not provide as-was history.

**Complexity:** Low. No new table or relationship.

**Risks / alternatives rejected:** Manifest-only lineage is weaker because it cannot prove the dimension build. A separate `DimReferenceVersion` table is overkill for a single selected version. Do not expose the column to report consumers.

**Final recommendation:** Keep the technical column.

**Findings / actions:** H-06 / A-07; H-03 / A-04.

### OD-R-14 — G3 status semantics

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** Define gate statuses as `NOT STARTED`, `IN PROGRESS`, `READY FOR REVIEW`, `APPROVED`, `BLOCKED`, separate from test status (`PLANNED`, `IN PROGRESS`, `PASS`, `FAIL`, `BLOCKED`) and decision status (`PENDING`, `APPROVED`, `REJECTED`, `DEFERRED`). After the owner formally records the decision, change G3 to `IN PROGRESS` with the existing contract, OD-01 draft and audit as evidence, and list approvals, schema freeze, reference-version approval, validation implementation and gate review as blockers. Do not change the status in this task.

**Technical correctness:** The current `NOT STARTED` contradicts the 195 KB contract and T-01 to T-77 in the same ledger row. `IN PROGRESS` accurately describes design work without claiming approval.

**Business justification:** Honest gate reporting prevents a stakeholder from believing either that no design exists or that the design is approved.

**Power BI:** No direct impact.

**Python:** No direct impact.

**History:** No direct impact.

**Complexity:** Low; a vocabulary and a controlled ledger update.

**Risks / alternatives rejected:** Keeping `NOT STARTED` preserves H-05. Marking `APPROVED` would be false. If the owner prefers, use `NOT FORMALLY APPROVED` instead of `IN PROGRESS`, but the status must stop implying that no work exists.

**Final recommendation:** Change to `IN PROGRESS` only after the owner records the decision; keep G4 `BLOCKED`.

**Findings / actions:** H-05 / A-06.

### OD-R-15 — Reviewer controls and compensating independence

**Status:** `NEEDS OWNER CLARIFICATION`

**Selected option:** Name a reviewer/verifier who is not the preparer. If no separate person is available, use a transparent compensating control: self-review checklist, automated hash/schema checks, a second-pass review by a peer or mentor where available, a reviewer-challenge and residual-concerns section, and an explicit statement that the review is not independent third-party assurance.

**Technical correctness:** A one-person project cannot manufacture independence. A documented compensating control is more defensible than an unnamed “verified” claim.

**Business justification:** The owner needs evidence review before signature, but the record must not overstate the independence of that review.

**Power BI:** Automated checks can validate model relationships, hidden columns and filter paths. They do not replace a human review.

**Python:** Automated checks can validate hashes, schema, provenance completeness and key stability.

**History:** The reviewer result and residual concerns are retained with the signed record.

**Complexity:** Low to moderate, depending on whether a peer/mentor is available.

**Risks / alternatives rejected:** Owner-only approval without a checklist is rejected (M-07). Pretending the preparer is independent is rejected. An external audit is not required for the portfolio, but its absence must be stated.

**Final recommendation:** Name a reviewer if possible; otherwise adopt the compensating control and record the limitation.

**Findings / actions:** M-07 / A-08; M-13 / A-16.

### OD-R-16 — Use BusinessModelClass if the attribute remains

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** If the business-model attribute is retained, name it `BusinessModelClass` and treat it as an optional analytical classification. It is not source-verified identity, has no provenance requirement, allows null and is excluded from T-72/T-75. If the owner does not need the comparison, remove it entirely.

**Technical correctness:** The name signals that the value is an analyst classification, not a registry fact. It prevents the attribute from being swept into identity reconciliation.

**Business justification:** A labelled analytical slicer is useful; an unlabelled “identity” attribute invites false precision.

**Power BI:** Label the slicer “Business model (analytical)” and allow blank. Do not use it in identity tests.

**Python:** Populate from a versioned analytical mapping or configuration, not from a source-verification workflow.

**History:** Analytical classification changes are build/report changes, not identity changes.

**Complexity:** Low.

**Risks / alternatives rejected:** Keeping the ambiguous `BusinessModel` name is rejected. Removing the attribute is acceptable if the portfolio does not need the comparison.

**Final recommendation:** Rename if retained; otherwise remove.

**Findings / actions:** M-04 / A-10; H-02 / A-02.

### OD-R-17 — Signed-copy retention and revision control

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** Store the signed copy read-only in `docs/approvals/` (not created by this task). Record its SHA-256 in the decision register and evidence register. Keep a revision-history table with version, date, author, change summary and reviewer. A signed copy is never edited; corrections create a new version. Git commit/tag only after explicit authorisation.

**Technical correctness:** A hash and a read-only copy make the signed artifact tamper-evident. Revision history preserves the audit trail.

**Business justification:** A decision record that can be edited after signature is not a reliable approval record.

**Power BI:** No direct impact.

**Python:** No direct impact.

**History:** The signed copy is the retained evidence; the working copy is not.

**Complexity:** Low; one folder and a hash register.

**Risks / alternatives rejected:** Keeping only a working-folder copy is rejected. Editing a signed copy is rejected. Git tagging is useful but must not be performed without authorisation.

**Final recommendation:** Adopt read-only retention and hashes; defer Git tag until after approval and authorisation.

**Findings / actions:** M-13 / A-16; O-04 / A-18.

### OD-R-18 — Optional LegalName

**Status:** `RECOMMENDED — PENDING OWNER CONFIRMATION`

**Selected option:** `LegalName` is optional in `ref_airlines.csv` and `ref_airline_sources.csv`. It is not required for the ten-airline population and is **not added to `DimAirline`** unless a report requirement later appears. If added later, it must be nullable and source-verified.

**Technical correctness:** This resolves H-01 without widening the star schema. The brand remains the display name; the legal name remains available for audit.

**Business justification:** Legal entity names are useful evidence but are not used in airline comparison. Keeping them in the reference layer avoids an unused dimension column.

**Power BI:** Reports use `AirlineName` only. No legal-name slicer is required.

**Python:** Verify `LegalName` only if populated; otherwise leave it null. Do not infer a legal name from a brand.

**History:** A legal-name change is a reference change; it creates a new version with the same keys.

**Complexity:** Low; one optional reference field.

**Risks / alternatives rejected:** Adding `LegalName` to `DimAirline` now is unnecessary. Removing legal names entirely is acceptable but less flexible; it is not recommended if the owner wants legal-entity evidence.

**Final recommendation:** Optional in the reference/provenance layer; not required in the dimension.

**Findings / actions:** H-01 / A-01.

---

## 7. Consolidated rationale and rejected alternatives

| Theme | Selected direction | Rejected alternative | Why rejected |
|---|---|---|---|
| Identity keys | `AirlineId` + permanent `AirlineKey`; IATA/ICAO attributes | IATA as business key | Mutable, reassignable, ambiguous across versions (H-07) |
| Registry | Approved reference snapshot is the registry | Separate airline registry table | Duplicate membership source, extra join, no analytical value |
| History | Type 1 + immutable snapshots; Type 2 deferred | Type 2 from day one | Bridge/fact-key complexity not needed for fixed roster |
| Lifecycle | `IsActive` + `StatusEffectiveDate` | Full `LifecycleStatus` + `MergedIntoAirlineId` | Unused state machine for a fixed 12-month simulation |
| Name | Brand in dimension; legal name optional in reference | Legal name as display name | H-01 ambiguity; wrong report labels |
| Region | Derived analytical geography | Stored identity region | No single source-verifiable definition (M-03) |
| Business model | Optional analytical `BusinessModelClass` | Source-verified identity attribute | Analyst taxonomy, not registry fact (M-04) |
| Version approval | `G3-RV-01` recurring gate artifact | OD-23 decision ID | Duplicates the approval register; recurring operational control |
| Evidence | Hash + URL + dates; archive optional | Mandatory archive of every source | Overkill for a portfolio; no document-management system |
| Review | Named reviewer or transparent compensating control | Unnamed “verified” claim | Overstates independence (M-07) |

---

## 8. Data model implications

### 8.1 Proposed `DimAirline` shape

| Column | Type | Null | Role | Decision note |
|---|---|---|---|---|
| `AirlineKey` | Int32 | No | Primary key; fact foreign key | Permanent; hidden in reports |
| `AirlineId` | String(20) | No | Stable business identity; unique | `AIR-0001`; hidden or audit-only |
| `AirlineIATACode` | String(2) | No | Mutable attribute; unique within version | Not a key |
| `AirlineICAOCode` | String(3) | No | Mutable alternate attribute; unique within version | Not a key |
| `AirlineName` | String(100) | No | Commercial brand; display label | T-72 compares brand |
| `HomeCountry` | String(100) | No | Principal headquarters/domicile | Not incorporation/AOC |
| `HomeCountryCode` | String(2) | No | ISO 3166-1 alpha-2 | Paired with `HomeCountry` |
| `AirlineGroup` | String(100) | Yes | Ultimate parent/group brand | Optional; no group dimension |
| `IsActive` | Boolean | No | Operating status | All ten true in baseline |
| `StatusEffectiveDate` | Date | Yes | Effective date of a non-active status | Required only when `IsActive = FALSE` |
| `BusinessModelClass` | String(50) | Yes | Analytical classification | Not identity; no provenance; label in reports |
| `ReferenceVersion` | String(30) | No | Technical lineage | Hidden; T-78 compares |

**Not in `DimAirline`:** `OperatingRegion` (derived analytically), `LegalName` (reference/provenance only), `LifecycleStatus` and `MergedIntoAirlineId` (deferred full lifecycle), `AirlineVersionKey` (Type 2 only).

### 8.2 Proposed `ref_airlines.csv` shape

| Column | Type | Null | Role |
|---|---|---|---|
| `AirlineId` | String(20) | No | Primary key with `ReferenceVersion` |
| `ReferenceVersion` | String(30) | No | Primary key with `AirlineId` |
| `AirlineIATACode` | String(2) | No | Mutable attribute; unique within version |
| `AirlineICAOCode` | String(3) | No | Mutable alternate attribute; unique within version |
| `AirlineName` | String(100) | No | Commercial brand; unique within version |
| `HomeCountry` | String(100) | No | Identity attribute |
| `HomeCountryCode` | String(2) | No | Identity attribute |
| `AirlineGroup` | String(100) | Yes | Optional identity attribute |
| `LegalName` | String(200) | Yes | Optional legal name; not in dimension |
| `IsActive` | Boolean | No | Operating status |
| `StatusEffectiveDate` | Date | Yes | Required when inactive |

`BusinessModelClass` and any derived region are analytical, not part of this identity reference.

### 8.3 Proposed `ref_airline_sources.csv` shape

| Column | Type | Null | Role |
|---|---|---|---|
| `SourceRecordID` | String(30) | No | Primary key; `SRC-000001`; globally unique |
| `AirlineId` | String(20) | No | Stable provenance join |
| `AttributeName` | String(30) | No | Controlled identity attribute name |
| `AttributeValue` | String(200) | No | Canonical loaded value |
| `SourceOrganization` | String(150) | No | Real organisation |
| `SourceURL` | String(500) | No for `VERIFIED` | HTTPS; no secrets/tracking |
| `SourceType` | String(30) | No | Controlled source type |
| `SourceRetrievedDate` | Date | No | Capture date |
| `SourceVerifiedDate` | Date | No | Actual verification date |
| `VerificationStatus` | String(20) | No | `VERIFIED`, `CONFLICTING`, `UNVERIFIED`, `SUPERSEDED`, `QUARANTINED` |
| `VerificationMethod` | String(50) | No for `VERIFIED` | Controlled method |
| `IsAuthoritative` | Boolean | No | Exactly one true per populated identity attribute/version |
| `EvidenceHash` | String(64) | No for `VERIFIED` | SHA-256; required for `VERIFIED`; archive is optional |
| `SourceArchiveRef` | String(200) | Yes | Optional read-only archive |
| `SupersedesSourceRecordID` | String(30) | Yes | Prior record replaced |
| `SupersededBySourceRecordID` | String(30) | Yes | Required when `SUPERSEDED`; reciprocal |
| `QuarantineReason` | String(50) | Yes | Required when `QUARANTINED` |
| `Notes` | String(500) | Yes | No secrets or personal data |
| `ReferenceVersion` | String(30) | No | Must match reference and manifest |
| `CreatedBy` / `CreatedDate` | String / Date | No | Preparation audit |
| `ReviewedBy` / `ReviewedDate` | String / Date | Yes | Required for `VERIFIED` |

Controlled `AttributeName` values: `AirlineName`, `LegalName`, `AirlineIATACode`, `AirlineICAOCode`, `HomeCountry`, `HomeCountryCode`, `AirlineGroup`, `IsActive`. `StatusEffectiveDate` is evidence metadata for an `IsActive` change, not a separately verified identity value. `BusinessModelClass` and any derived region are excluded. `IsActive = TRUE` for the ten baseline airlines is an OD-01A population-scope decision, not a source-verified identity fact; it does not require a provenance row. A change to `FALSE` requires an `IsActive` evidence row and a `StatusEffectiveDate`.

### 8.4 Key and relationship rules

- `ref_airlines.csv` primary key: `AirlineId` + `ReferenceVersion`.
- `DimAirline` primary key: `AirlineKey`; unique `AirlineId`; IATA/ICAO/name unique within `ReferenceVersion`.
- `ref_airline_sources.csv` primary key: `SourceRecordID`; one authoritative `VERIFIED` record per populated source-verified identity attribute (`AirlineId` + `AttributeName` + `ReferenceVersion`). A baseline `IsActive = TRUE` is population scope, not a source-verified attribute; a status change requires separate evidence.
- Facts join `DimAirline` on `AirlineKey`; no IATA/ICAO/name joins.
- `DimAircraft.AirlineKey` remains lineage/validation; no active second filter path.
- `ReferenceVersion` is a technical column, not a relationship.
- No Type 2 `AirlineVersionKey` in the baseline.

### 8.5 What the model intentionally does not contain

- No separate airline registry table.
- No airline group dimension.
- No operating-region identity column.
- No legal-name column in the star schema.
- No lifecycle state machine or merger mapping.
- No Type 2 version rows, bridge table or effective-dated facts.
- No code-based fact relationships.

---

## 9. Power BI implications

1. **Star schema:** `DimAirline` is a ten-row dimension; facts relate on `AirlineKey`. No snowflake for group, region or legal name.
2. **Hidden technical columns:** `AirlineKey`, `AirlineId`, `ReferenceVersion` and `StatusEffectiveDate` are hidden from report view. `AirlineKey` is the relationship key, not a report field.
3. **Report labels:** `AirlineName` is the commercial brand. `AirlineGroup` is an optional slicer. `BusinessModelClass` is an optional analytical slicer, clearly labelled.
4. **No operating-region identity field:** If a region view is required, derive it from `DimRoute`/`DimAirport` geography at the model/report layer.
5. **Filter path:** Do not activate `DimAirline`–`DimAircraft` as a second path. Use a role-playing `DimAirline - Fleet` dimension or a documented `TREATAS` measure; validate with T-42/T-43.
6. **Refresh control:** Expose `SelectedReferenceVersion`; compare it to the approved manifest and `DimAirline.ReferenceVersion`. T-78 blocks a mismatch.
7. **Disclosure:** Every page, tooltip, export and screenshot carries `Synthetic Simulation — Not Actual Airline Performance` (em dash U+2014). T-79 is the report-release test.
8. **Performance:** A ten-row dimension and no bridge/Type 2 rows keep the model simple and fast.
9. **Security and claims:** No real passenger data; no airline affiliation, sponsorship or endorsement claim; all operational/financial results are synthetic.

---

## 10. Python pipeline implications

1. **Reference builder:** Read the approved reference snapshot; validate the schema; assign `AirlineKey` from a deterministic `AirlineId` map; never derive keys from row order after initial assignment.
2. **Stable keys:** `AirlineId` and `AirlineKey` are assigned once and never reused. A rebuild must reproduce the same mapping.
3. **Version manifest:** Record `ReferenceVersion`, file hashes, source evidence hashes, approved status and reconciliation note. Do not mutate a published version.
4. **Provenance validation:** Enforce one row per assertion, controlled `AttributeName`, one authoritative `VERIFIED` record per populated identity attribute, real URL/date/hash, staleness and reciprocal supersession.
5. **Lifecycle validation:** `IsActive = FALSE` requires a real `StatusEffectiveDate` and evidence. Baseline all active/null. Do not generate merger mappings.
6. **Analytical classification:** `BusinessModelClass` comes from a versioned analytical mapping, not source verification; null allowed; record method/analyst.
7. **Derived region:** Do not generate an identity region. If needed, derive it from airport/route geography in the curated/report layer.
8. **Dimension build:** One row per airline; Type 1; `ReferenceVersion` populated; no Type 2 rows.
9. **Tests:** Produce evidence for T-72 to T-78; T-79 at report release; T-42/T-43 for model relationships.
10. **No generation:** This resolution does not authorise running the generator, creating CSV files or producing datasets.

---

## 11. Requirements and test implications

### 11.1 Requirements

| Requirement | Proposed change | Decision |
|---|---|---|
| REQ-001 | Keep ten real, to-be-source-verified airline identities and synthetic simulations | No change to intent; tense correction later |
| REQ-023 | Reconcile on `AirlineId` and the commercial brand, supported by provenance | Update wording |
| REQ-024 | Separate IATA/ICAO identifiers, unique within a reference version | Update wording |
| REQ-025 | Attribute-level provenance with source hierarchy, status and conflicts | Update wording; add evidence fields |
| REQ-026 | Nullable unsupported attributes and quarantine; no fabrication | Update wording for lifecycle and analytical exclusions |
| REQ-027 | Exact reference-to-dimension reconciliation | Update to include `AirlineId`/`AirlineKey`; exclude analytical attributes |
| **REQ-028** | **Airline identity reference-version, manifest and refresh integrity** | **New — recommended** |

### 11.2 Tests

| Test | Proposed change | Decision |
|---|---|---|
| T-72 | Roster reconciliation on `AirlineId`, brand, codes and countries; exactly ten identities | Update |
| T-73 | IATA format and uniqueness **within `ReferenceVersion`** | Update |
| T-74 | ICAO format and uniqueness **within `ReferenceVersion`** | Update |
| T-75 | Every populated source-verified identity attribute has one authoritative `VERIFIED` record; optional null; baseline `IsActive` is scope, not a source fact | Update; exclude analytical |
| T-76 | Conflicts/quarantine; status-change evidence; no silent selection | Update |
| T-77 | Reference-to-dimension reconciliation on `AirlineId`/`AirlineKey`; exclude analytical | Update |
| **T-78** | **Reference version, manifest, dimension and refresh integrity; ten sub-checks** | **New — recommended** |
| T-79 | Disclosure exact-string and rendered-output integrity | New at report release; not identity |
| T-42/T-43 | Relationship cardinality and role-playing dimensions; no active `DimAirline`–`DimAircraft` path | Existing; apply to model |

### 11.3 Findings and actions trace

All 33 findings and 18 actions remain mapped. The complete finding set is **H-01, H-02, H-03, H-04, H-05, H-06, H-07; M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08, M-09, M-10, M-11, M-12, M-13; L-01, L-02, L-03, L-04, L-05, L-06, L-07, L-08; O-01, O-02, O-03, O-04, O-05**. The complete action set is **A-01, A-02, A-03, A-04, A-05, A-06, A-07, A-08, A-09, A-10, A-11, A-12, A-13, A-14, A-15, A-16, A-17, A-18**. No finding or action is omitted, merged or silently downgraded. The decisions in this resolution change the selected implementation for H-01, H-03, H-04, H-06, H-07 and M-07/M-12; they do not close any finding until the contract, draft and tests are updated and re-audited.

| Finding group | Actions | Resolution effect |
|---|---|---|
| H-01 / A-01 | Brand plus optional reference-only `LegalName` | Narrower dimension; same audit closure |
| H-02 / A-02 | Every populated source-verified identity attribute `VERIFIED`; baseline `IsActive` scope; analytical excluded | Preserved |
| H-03 / A-04 | Type 1, stable keys, `ReferenceVersion` | Preserved |
| H-04 / A-05 | Minimal `IsActive` + `StatusEffectiveDate` | Leaner than full lifecycle; owner must accept scope assumption |
| H-05 / A-06 | Gate vocabulary; `IN PROGRESS` after approval | Preserved; no status change now |
| H-06 / A-07 | T-78; no OD-23; `G3-RV-01` | Simpler approval artifact |
| H-07 / A-03 | `AirlineId`/`AirlineKey`; IATA/ICAO attributes | Preserved |
| M-01 to M-04 / A-10 | Home country, group, region, business model | Region removed; business model analytical |
| M-05/M-06 / A-11 | Provenance schema, evidence, staleness | Preserved; archive optional |
| M-07 / A-08 | Reviewer and reference-version approval | `G3-RV-01` replaces OD-23 |
| M-08 / A-12 | Change-control tiers | Preserved |
| M-09 / A-13 | Filter-path constraint | Preserved |
| M-10 / A-14 | Evidence classification | Preserved |
| M-11 / A-15 | Disclosure | Preserved; T-79 later |
| M-12 / A-09 | Approval scope | OD-01A/OD-01B split |
| M-13 / A-16 | Retention and metadata | Preserved |
| L-01 to L-08 / A-17 | Text, schema, supersession, version format | Preserved |
| O-01 to O-05 / A-18 | Brief, split, ADR, Git, reviewer challenge | Preserved |

---

## 12. Risks and residual concerns

| ID | Risk or residual concern | Impact | Mitigation | Residual after mitigation |
|---|---|---|---|---|
| R-01 | No airline identity value has been source-verified in this task | The population is intended, not verified; OD-01A cannot claim verification yet | Execute the provenance workflow and T-75/T-76 before signature | Source verification remains outstanding |
| R-02 | The audit is a structured self-audit, not independent assurance | The 61/100 score is not third-party assurance | Name a reviewer or record the compensating control; re-audit after corrections | Independence limitation remains |
| R-03 | Type 1 does not preserve as-was identity labels | A mid-period rename would show the current brand against historical facts | Disclose the limitation; keep immutable snapshots; trigger Type 2 if as-was reporting is required | Semantic history limitation remains |
| R-04 | The minimal lifecycle model may be challenged by an auditor expecting full lifecycle fields | H-04 closure could be disputed | Document the fixed-roster scope assumption and Tier 3 change control; owner explicitly accepts the minimal model | Possible re-audit challenge |
| R-05 | Splitting OD-01 adds a second decision record | Extra governance overhead | Use one shared evidence index and one brief; sign OD-01A first | Modest overhead remains |
| R-06 | OD-23 is not used | The reference-version approval needs a home | Define `G3-RV-01` in the G3 gate package with criteria and evidence | Gate artifact must still be created |
| R-07 | `BusinessModelClass` is an analyst judgement | The classification could be read as an airline fact | Label it analytical; record method/analyst; allow null; exclude identity tests | Subjectivity remains |
| R-08 | `AirlineGroup` and `LegalName` may be null | Some group/legal analysis is unavailable | Do not infer; keep optional; add later only with evidence | Coverage may be incomplete |
| R-09 | `ReferenceVersion` adds a technical column | Slight dimension width; possible misuse as a slicer | Hide it; use only for T-78 lineage | Low |
| R-10 | Evidence capture and hashing take effort | The provenance register may slow delivery | Keep archive optional; use a simple hash/URL/date workflow; one row per assertion | Moderate effort remains |
| R-11 | Reference-version approval is not yet defined | T-78 cannot be fully enforced without an approved manifest | Define `G3-RV-01` before G3 review | Approval process outstanding |
| R-12 | No data, schema freeze, Power BI file or Git commit exists | The project cannot yet demonstrate the design | Do not claim implementation; proceed only after owner confirmation and controlled change | Implementation remains blocked |
| R-13 | The fixed-roster assumption may not hold | A merger/cessation would invalidate the baseline | Treat it as a Tier 3 scope change; new scenario/new `AirlineId` for a successor; full lifecycle only if required | Scope risk remains |
| R-14 | One-person review can be challenged as insufficiently independent | Governance score may remain capped | Transparent compensating control; peer/mentor second pass where possible; no independence claim | Independence risk remains |

**Residual conclusion:** The design is materially simpler and more defensible than the full remediation proposal, but it is not implementation-ready. It is ready for owner decision. Source verification, contract editing, tests, re-audit, signature and gate review remain outstanding.

---

## 13. Decisions requiring explicit owner confirmation

All 18 decisions require owner confirmation. The following choices need a specific answer beyond “accept” because they change scope or governance:

| # | Decision | Question for the owner | Recommended answer | Consequence if rejected |
|---:|---|---|---|---|
| 1 | OD-R-01 | Split OD-01 into OD-01A/OD-01B, or keep one record with two approval blocks? | Split, with one shared evidence index | One broad record remains; M-12 risk persists |
| 2 | OD-R-03 | Accept Type 1 with build reproducibility but no as-was identity history? | Accept for the fixed 12-month roster; defer Type 2 | Type 2 adds a version key, bridge and as-of tests |
| 3 | OD-R-09 | Use minimal `IsActive` + `StatusEffectiveDate`, or the full `LifecycleStatus` + `MergedIntoAirlineId` model? | Minimal model; defer full lifecycle | Full model adds unused fields and merger logic |
| 4 | OD-R-10 | Replace OD-23 with `G3-RV-01`, or keep OD-23? | `G3-RV-01`; no OD-23 | OD-23 duplicates the decision register |
| 5 | OD-R-15 | Name a reviewer, or accept the documented compensating control? | Name a reviewer if available; otherwise accept the control | Self-review limitation remains unresolved |
| 6 | OD-R-18 | Keep `LegalName` in the reference layer only, or add it to `DimAirline`? | Reference-only; add later only if a report needs it | A wider dimension and an extra provenance obligation |
| 7 | OD-R-08 | Keep `BusinessModelClass` as an optional analytical attribute, or remove it? | Keep only if the portfolio needs the comparison; otherwise remove | An unlabelled or unused attribute remains |
| 8 | OD-R-07 | Remove `OperatingRegion` from identity, or keep a documented analytical region? | Remove; derive region from route/airport geography | An ambiguous identity field remains |

**Owner instruction:** For each row, record `ACCEPT`, `REJECT`, `DEFER` or an explicit alternative. Do not mark any row `APPROVED` in this document. The signed decision record is a separate artifact.

---

## 14. Proposed owner approval block

> **Template only — no signature, no date, no approval.** This block is not completed. It must not be cited as evidence of owner approval.

| Field | Value |
|---|---|
| Resolution ID | `OD-01-OWNER-RESOLUTION-2026-11-01` |
| Project owner / approver | KH Mohammad Farhan |
| Resolution status | **PENDING OWNER CONFIRMATION** |
| Decision date | [BLANK — owner to enter at signature] |
| Owner signature | [BLANK — owner to sign] |
| Approval evidence reference | [BLANK — owner to enter] |
| Selected options | As recorded in Section 5; choices in Section 13 |
| OD-01 status after this resolution | **PENDING** (unchanged) |
| G3 status after this resolution | **NOT STARTED** (unchanged) |
| G4 status after this resolution | **BLOCKED** (unchanged) |

**Owner attestation (proposed wording, not yet signed):**

- I have reviewed the 18 decisions and the technical challenges in this resolution.
- I confirm the selected options recorded in Section 5, subject to any explicit changes I record in Section 13.
- I understand that this resolution does not approve OD-01, freeze the schema, approve a reference version, authorise data generation or change G3/G4.
- I understand that Type 1 preserves build reproducibility but not as-was identity history.
- I understand that no airline identity value has been source-verified in this task.
- I understand that the review is not independent third-party assurance.
- I will sign OD-01A/OD-01B only after the contract, draft and tests are corrected and re-audited.

**No decision in this document is `APPROVED`.** The owner’s signature on a separate decision record is required before any status changes.

---

## 15. Implementation authorization boundaries

### 15.1 What is authorised now

Only the creation and review of this resolution. No implementation, contract, schema, reference data, Power BI or Git action is authorised.

### 15.2 What remains prohibited until the owner confirms and a separate task is authorised

- Editing `docs/03_DATA_CONTRACTS.md`, the OD-01 draft, the audit report, the scope, the business requirements, the master prompt, the traceability matrix or the progress ledger.
- Changing contract version 1.4.
- Creating or populating `ref_airlines.csv`, `ref_airline_sources.csv` or any other reference CSV.
- Creating synthetic data, datasets, scripts, JSON, Power BI files or model artifacts.
- Changing G3 to `IN PROGRESS` or any other status.
- Changing G4 from `BLOCKED`.
- Inserting signatures, approval dates or approval evidence.
- Any Git commit, tag, branch or worktree operation.
- Claiming that OD-01 is approved or that the schema is frozen.

### 15.3 Controlled sequence after owner confirmation

1. Record the owner’s selected options in a separate signed resolution or decision record.
2. Apply the approved decisions to `docs/03_DATA_CONTRACTS.md` as version 1.5, with a pre-write backup and hash.
3. Align `docs/REQUIREMENTS_TRACEABILITY.md`, the data-dictionary outline and the test register; add REQ-028, T-78 and `G3-RV-01` if approved.
4. Rewrite or split the OD-01 draft into OD-01A/OD-01B, with no false approval language.
5. Align scope, business requirements, master prompt and progress ledger only where the approved decisions require it.
6. Obtain reviewer evidence or document the compensating control; re-audit and close the HIGH findings and M-07/M-12.
7. Owner signs OD-01A/OD-01B with a real date and real evidence references.
8. Proceed to G3 review, schema freeze and reference-version approval; G4 only with separate written authorisation.

### 15.4 Stop conditions

Stop and return to the owner if any of the following occurs:

- The remediation specification hash differs from `CC3BCE621142C31B4BB7A46F4CBCB320E640466228184AE2E94E196796F3F8A4`.
- Any existing baseline hash changes unexpectedly.
- A required decision remains unresolved.
- A request asks for invented sources, dates, signatures, airline values or verification claims.
- A request asks to mark OD-01 approved, freeze the schema or change G3/G4 without the required evidence.
- A request asks to create reference data, scripts or Power BI artifacts before authorisation.

---

**End of resolution. Status: PENDING OWNER CONFIRMATION. No decision approved. No existing document modified. No implementation performed.**






