# AEROVISION 360 - OD-01 Independent Governance Audit Report

**Audit type:** Read-only enterprise governance audit
**Audit date:** 2026-11-01
**Subject:** `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md`
**Subject SHA256:** `C594DFCD8FE1B6809E28CBE1B3EE6D24FAA0772D35DD1FE57767FECCD3CA2A60`
**Governing baseline:** `docs/03_DATA_CONTRACTS.md` version 1.4
**Report status:** Final audit report
**Approval readiness:** NOT READY - MATERIAL CORRECTIONS REQUIRED
**Overall score:** 61/100

> **Independence limitation.** This audit was performed by the same assistant that
> prepared the draft in the preceding step. It is a structured adversarial self-audit,
> not independent third-party assurance. A separate human reviewer should validate the
> findings before signature. This limitation is itself recorded as a governance finding
> (M-07).

---

## 1. Executive summary

The OD-01 draft is a substantial and largely well-structured decision record. The
ten-airline roster is internally exact across the scope, data contract, master prompt,
and draft. The identifier separation, the real-versus-synthetic boundary, and most of
the provenance rules are sound. The draft is also honest about what it does not approve:
no reference values, no schema freeze, no data generation, and no gate advancement.

It is not ready for owner signature as written.

Seven HIGH findings affect the substance of what the owner would be approving:

1. `AirlineName` is undefined as legal registered name versus commercial brand name.
2. The verification rule requires `VERIFIED` only for required attributes, while T-75
   requires it for every populated attribute; optional attributes are therefore
   under-controlled and the rule contradicts its own test.
3. There is no slowly changing dimension, effective-dating, or `AirlineKey` stability
   model for identity changes across reference versions.
4. The risk register omits airline suspension or cessation, reference updates after a
   model refresh, and historical data inconsistency after an identity change.
5. G3 is recorded as NOT STARTED while the data contract already contains the design
   evidence the draft relies on; the status label is not credible as written.
6. There is no airline identity reference-version and manifest integrity test comparable
   to T-59 and T-69.
7. The mutable IATA code is used as the business key and as the provenance join key,
   with no stable airline identifier and no version-qualified uniqueness rule.

Thirteen MEDIUM findings, eight LOW findings, and five observations add definitional,
provenance, approval-control, and documentation gaps. None of them invalidates the
roster itself. Several would become CRITICAL if the record were used to build reference
data without correction.

**Bottom line:** the core population decision is defensible, but the record as a whole
is not signature-ready. Correct the HIGH findings and the approval-scope wording, or
split OD-01 into a narrow population decision and a separate identity/reference-rules
decision.

---

## 2. Audit scope and exclusions

### 2.1 Scope

The audit examined:

- The complete 446-line draft (447 newline-delimited lines including the trailing newline).
- All six active baseline documents.
- The OD-01 migration final report.
- The original migration backup and the pre-write apply backup.
- The draft's roster, identifier model, provenance rules, approval block, and
  cross-document references.

The audit checked internal consistency, decision completeness, identity integrity,
architecture, provenance design, synthetic-data governance, approval controls,
traceability, risk coverage, and auditability.

### 2.2 Exclusions and limitations

- No external source was consulted. The audit did not verify airline names, codes,
  countries, group ownership, regions, or business models against public sources.
- No reference CSV, dataset, semantic model, DAX measure, or report exists to test.
- No legal, trademark, privacy, or security review was performed.
- No Git operation was executed. The repository's version-control state was not changed.
- The auditor prepared the draft, so this is not independent third-party assurance.
- The audit assesses the document, not the future implementation.

### 2.3 Read-only confirmation

The only file created by this audit is this report. No baseline document, draft,
reference file, Power BI file, source file, or Git state was modified.

---

## 3. Evidence inspected

| Evidence | Path | SHA256 | Size |
|---|---|---|---|
| Decision draft | `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md` | `C594DFCD8FE1B6809E28CBE1B3EE6D24FAA0772D35DD1FE57767FECCD3CA2A60` | 26,179 |
| Project scope | `docs/01_PROJECT_SCOPE.md` | `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` | 5,790 |
| Business requirements | `docs/02_BUSINESS_REQUIREMENTS.md` | `E2FCC8132981C96720E572F01EF353C255CA6BE91F27854950D93FF0DFC1DB6E` | 4,513 |
| Data contract | `docs/03_DATA_CONTRACTS.md` | `EB1DE0E1B80E9E30B4905740BDD66AB96657073119D63C49AA48445CB06446E2` | 195,181 |
| Master build prompt | `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt` | `17BD2C6FCADB9E2A917D047B2B2D9716E21CB1709B5A46ABF01AB2833C56D429` | 16,801 |
| Requirements traceability | `docs/REQUIREMENTS_TRACEABILITY.md` | `1AD225D00EA6D5808B6E0050DBFCE10F84CBAEF2B66DE70C4362370BBA9CC751` | 4,456 |
| Progress ledger | `docs/PROGRESS_LEDGER.md` | `42A00E3A41A9ABBC6B9F930BFE39DD369E6B9681B9F56194921E7145E6F8A7A3` | 1,842 |
| Migration final report | `docs/OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt` | `EFA6060BD0D73B48341A238DE460EA0497B3AF2304709489F1B2DF6B15408CA7` | 9,891 |

Backups inspected:

- `docs/od01_real_airline_migration_backup_20261101_185328/` - six baseline files.
- `docs/od01_real_airline_migration_apply_backup_20261101_204216/` - six baseline files
  plus `BACKUP_MANIFEST.txt` (`87D1A446521E661FE64EE41B9FA6F027DAEA22DA2C5EE66203892B2539AB6785`).

Both backup sets contain the pre-migration hashes recorded in the migration report:
`F9F06819...`, `C5D98649...`, `363FBB99...`, `3CB41CD1...`, `F80F3CA0...`, and
`3B959982...`.

---

## 4. Integrity verification

| Check | Result |
|---|---|
| Report path free before creation | PASS - `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` did not exist |
| Draft hash matches the hash recorded in the preceding turn | PASS |
| Six baseline hashes match the draft's evidence register | PASS |
| Six baseline hashes unchanged during the audit | PASS |
| Migration report hash unchanged | PASS |
| Original backup hashes match the migration report BEFORE hashes | PASS |
| Apply backup hashes match the original backup | PASS |
| Reference CSV files present | 0 |
| Reference directory files | 0 |
| Power BI files | 0 |
| Git command executed by this audit | None |

No protected file changed unexpectedly. The draft's baseline hash table is accurate.

---

## 5. Domain scorecard

Scores use the required 0 to 5 scale.

| # | Domain | Score | Weight | Weighted points | Rationale |
|---|---|---:|---:|---:|---|
| 1 | Decision completeness | 4 | 15% | 12.0 | All 21 required elements are present; approval and change-control gaps remain |
| 2 | Airline identity integrity | 3 | 15% | 9.0 | Roster is exact; name, country, group, region, and model semantics are underdefined |
| 3 | Data architecture | 2 | 15% | 6.0 | Identifier separation is sound; key stability, versioning, and SCD are material gaps |
| 4 | Source provenance | 3 | 15% | 9.0 | Rules are detailed; optional verification, cardinality, durability, and normalization gaps |
| 5 | Synthetic-data governance | 4 | 10% | 8.0 | Strong boundary; disclosure has a qualifier and an exact-string mismatch |
| 6 | Formal approval controls | 3 | 10% | 6.0 | Fields and status are correct; self-approval and no verifier or evidence standard |
| 7 | Cross-document traceability | 3 | 10% | 6.0 | IDs and versions align; G3 status and change-control contradictions |
| 8 | Risk and exception management | 2 | 5% | 2.0 | Eight risks, but three required scenarios are absent and several are only partial |
| 9 | Auditability and reproducibility | 3 | 5% | 3.0 | Hashes and backups are good; 99 checks are self-reported and the draft lacks revision metadata |

---

## 6. Weighted overall score

| Domain | Score / 5 | Weight | Points |
|---|---:|---:|---:|
| Decision completeness | 4 | 15% | 12.0 |
| Airline identity integrity | 3 | 15% | 9.0 |
| Data architecture | 2 | 15% | 6.0 |
| Source provenance | 3 | 15% | 9.0 |
| Synthetic-data governance | 4 | 10% | 8.0 |
| Formal approval controls | 3 | 10% | 6.0 |
| Cross-document traceability | 3 | 10% | 6.0 |
| Risk and exception management | 2 | 5% | 2.0 |
| Auditability and reproducibility | 3 | 5% | 3.0 |
| **Total** | | **100%** | **61.0 / 100** |

**Overall score: 61/100.** This is a material-corrections outcome, not an approval
recommendation.

---

## 7. Critical findings

**None.**

No finding met the CRITICAL threshold at the time of audit. The draft does not approve
reference values, does not create data, and explicitly excludes schema freeze and data
generation, so the HIGH findings have not yet produced invalid identity data or
misleading reporting.

This is not reassurance. H-01, H-02, H-03, and H-07 would become CRITICAL if the record
were used to populate `ref_airlines.csv` or `ref_airline_sources.csv` without correction,
because they could produce invalid names, unverified optional attributes, broken
historical identity links, or duplicate keys.

## 8. High findings

### H-01 - `AirlineName` is undefined as legal name versus commercial brand

| Field | Detail |
|---|---|
| Severity | HIGH |
| Document and section | Draft Section 3 (L65-74), D-2 (L50), Section 6.3 (L198); contract Table 6.2.2 (L722) |
| Evidence | The roster uses brand names such as `IndiGo`, `Emirates`, `Qantas`, and `Air India`. The contract requires a "Unique official source-verified airline name" but never defines whether "official" means the registered legal entity or the commercial brand. T-72 (draft L285) requires exact reconciliation to the roster. |
| Why it matters | Illustrative examples, not source-verified in this audit, include `InterGlobe Aviation Limited` versus `IndiGo`, `Emirates Airline` versus `Emirates`, `Qantas Airways Limited` versus `Qantas`, and `Air India Limited` versus `Air India`. A source-verification exercise can legitimately return a legal or a brand form. The record gives no rule for choosing one. |
| Risk or consequence | Source records may be marked `CONFLICTING` when they are not; T-72 may fail on exact match; `DimAirline` may show legal names while the roster and reports show brands; the owner may approve an identity definition that is not implementable as written. |
| Recommended corrective action | Define `AirlineName` as the approved commercial brand name used by the project. Add an optional `LegalName` attribute if the legal entity is needed, or state explicitly that legal names are out of scope. Add a canonicalization rule and update T-72 to compare against the defined attribute. |
| Owner approval required | Yes - this changes the approved identity attribute definition. |

### H-02 - Optional identity attributes are not consistently required to be `VERIFIED`

| Field | Detail |
|---|---|
| Severity | HIGH |
| Document and section | Draft Section 3.1 (L83-85), Section 6.2 (L187-189), Section 6.5 (L219-221), T-75 (L288); contract Section 3.4 (L241, L246), T-75 (L1628) |
| Evidence | Section 3.1 requires `AirlineGroup` to come from a `VERIFIED` record but says only "source-supported" for `OperatingRegion` and "reliable evidence" for `BusinessModel`. Section 6.2 limits the `VERIFIED` requirement to "a populated required identity attribute." T-75 requires "every populated identity attribute" to resolve to a `VERIFIED` record. The rule and the test contradict each other. |
| Why it matters | A literal reading of Section 6.2 permits an optional attribute to be populated from an `UNVERIFIED` or `CONFLICTING` source. T-75 would then fail, or the implementer would weaken the test to match the rule. Either outcome undermines the no-fabrication control. |
| Risk or consequence | Unsupported group, region, or business-model values could enter `ref_airlines.csv` and airline-level reporting. The record would approve a provenance model that cannot enforce its own optional-attribute rule. |
| Recommended corrective action | Require `VERIFIED` status for every populated identity attribute, required or optional. Align Section 3.1, Section 6.2, Section 6.5, and T-75. State that an optional attribute with no `VERIFIED` source remains null. |
| Owner approval required | Yes - this tightens the approved provenance rule. |

### H-03 - No SCD, effective-dating, or `AirlineKey` stability model

| Field | Detail |
|---|---|
| Severity | HIGH |
| Document and section | Draft Section 3.2 (L89-91), Section 6.5 (L224-228), Section 8.1 (L257); contract Section 4.3 (L349), Section 3.4 (L250), Section 8.1 (L1120) |
| Evidence | The draft says membership must not change during the reporting period and that a merger, rebrand, or code change requires a new scenario and reference version. It also says published reference versions are immutable and corrections require a new version. It never states whether `AirlineKey` is permanent across versions, whether `DimAirline` is Type 1 or Type 2, or how historical facts map to a changed identity. |
| Why it matters | A new reference version can change a name, code, group, or active status. If `AirlineKey` is reassigned or `DimAirline` is rebuilt, historical facts and Power BI relationships point at the wrong member. T-77 reconciles only the selected reference version to the current dimension; it does not test historical consistency. |
| Risk or consequence | Orphaned or duplicated airline members; broken trend analysis; inconsistent airline-level KPIs across refreshes; a reference correction that silently changes history. |
| Recommended corrective action | Define `AirlineKey` as a permanent surrogate assigned once per airline and stable across reference versions. Define `DimAirline` as Type 1 for the baseline, with versioned reference snapshots, or Type 2 if historical identity tracking is required. Add an effective-dating and historical reconciliation rule and a test that compares facts generated under one version to the dimension built from another. |
| Owner approval required | Yes - this is an architecture and history-retention decision. |

### H-04 - Risk register omits three required scenarios and their controls

| Field | Detail |
|---|---|
| Severity | HIGH |
| Document and section | Draft Section 9 (L300-307); contract Section 4.3 (L349) |
| Evidence | The register contains R-1 to R-8. It does not address an airline being suspended or ceasing operations, a reference dataset being updated after a model refresh, or historical synthetic data becoming inconsistent with a changed identity reference. The contract addresses only merger or rebrand, not suspension or cessation. |
| Why it matters | These are not edge cases for a 12-month airline simulation. An airline can suspend routes or cease operations; a reference version can change between generation and refresh; historical facts can outlive the identity version that produced them. Each scenario needs an explicit control, not an implied one. |
| Risk or consequence | The roster may include a non-operating airline without a status rule; a refresh may mix airline reference versions; historical results may not reconcile after an identity correction. |
| Recommended corrective action | Add risks and controls for suspension/cessation (`IsActive` lifecycle and effective dating), reference-version pinning and refresh manifest checks, and historical re-mapping/reconciliation. Add corresponding tests, including the airline reference-version test in H-06. |
| Owner approval required | Yes - these are policy and test-register changes. |

### H-05 - G3 status contradicts the design evidence in the same ledger row

| Field | Detail |
|---|---|
| Severity | HIGH |
| Document and section | `docs/PROGRESS_LEDGER.md` L9; draft L19 and L390; contract version 1.4 |
| Evidence | The ledger marks G3 as `NOT STARTED` while the same row states that data contract version 1.4 documents schemas, grains, keys, units, date roles, reference datasets, K13, and validation tests T-01 to T-77. The draft relies on that design as its governing baseline and repeats `G3 remains NOT STARTED`. |
| Why it matters | A reader cannot tell whether G3 has not begun, whether design work is in progress but not approved, or whether `NOT STARTED` is being used as a synonym for `NOT FORMALLY APPROVED`. Those are different governance states with different evidence requirements. |
| Risk or consequence | Gate reporting is unreliable; a stakeholder may believe no design exists when a 195 KB contract does; a future gate review may be based on a false status; audit findings may be dismissed as premature. |
| Recommended corrective action | Define the gate status vocabulary. Either mark G3 `IN PROGRESS` with design drafted and approvals pending, or rename the current state to `NOT FORMALLY APPROVED` and keep the design evidence visible. Add explicit G3 entry and exit criteria. |
| Owner approval required | Yes - this changes governance reporting. |

### H-06 - No airline identity reference-version or manifest integrity test

| Field | Detail |
|---|---|
| Severity | HIGH |
| Document and section | Draft Section 8.3 (L285-290); contract T-69 (L1622), T-59 (L1674), T-72 to T-77 (L1625-1630) |
| Evidence | The contract has version-integrity tests for cost/disruption classifications (T-69) and aircraft availability (T-59). The airline identity tests T-72 to T-77 cover roster reconciliation, code formats, provenance completeness, conflict handling, and reference-to-dimension reconciliation. None verifies that the selected `ref_airlines.csv` and `ref_airline_sources.csv` version matches the generation manifest and the Power BI refresh configuration. |
| Why it matters | T-77 compares the reference to `DimAirline`, not to the manifest or refresh. A model could refresh against a different airline reference version than the one used to generate the facts, and every existing test could still pass. |
| Risk or consequence | Silent version drift; airline-level facts and dimension attributes from different snapshots; a reconciliation that looks correct at the current version but is not reproducible. |
| Recommended corrective action | Add T-78, or extend T-77, to verify that the airline identity reference version in the generation manifest, the curated dimension, and the selected refresh configuration is identical, and that exactly one version is used per refresh. Record evidence in `qa/results/airline_identity_versions.csv`. |
| Owner approval required | Yes - this adds a validation obligation. |

### H-07 - Mutable IATA code is the business key and provenance link, with no stable airline identifier

| Field | Detail |
|---|---|
| Severity | HIGH |
| Document and section | Draft D-3 (L51), Section 7 (L242-243), R-6 (L305); contract Section 3.4 (L239, L242); T-73 and T-74 (L1626-1627) |
| Evidence | `AirlineIATACode` is declared the primary business key. `ref_airline_sources.csv` links provenance to the airline through `AirlineIATACode`. The grain is one row per airline per `ReferenceVersion`, but uniqueness tests T-73 and T-74 check the code in the reference file without a version qualifier. No stable `AirlineId` or reference-level `AirlineKey` is defined. |
| Why it matters | IATA codes are mutable and can be reassigned; the draft's own R-6 acknowledges this. If a code changes, the same airline gets a new business key and its old source records no longer resolve. If multiple reference versions coexist, the same IATA code appears more than once, so it is not unique in the file. |
| Risk or consequence | Duplicate-key failures or ambiguous keys; orphaned provenance after a code change; historical facts mapped to the wrong airline; T-73/T-74 passing or failing depending on how the file is partitioned. |
| Recommended corrective action | Introduce a stable `AirlineId` (or use the permanent `AirlineKey`) as the persistent identity and provenance link. Define the reference business key as `AirlineId` or as `AirlineIATACode` plus `ReferenceVersion`, and the alternate key as `AirlineICAOCode` plus `ReferenceVersion`. Keep IATA and ICAO as attributes. Update `ref_airline_sources.csv`, T-73, T-74, T-75, and T-77. |
| Owner approval required | Yes - this changes the identity and provenance schema. |

## 9. Medium findings

### M-01 - `HomeCountry` is not defined

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 3 (L65-74), Section 6.3 (L202); contract Table 6.2.2 (L724) |
| Evidence | The roster lists a home country and country code, but the draft never defines whether home country means country of incorporation, principal headquarters, principal place of business, or the state issuing the air operator certificate. |
| Why it matters | For a group airline, these can differ. The source hierarchy points to a government or civil-aviation registry, which may certify a different country from the commercial headquarters. |
| Risk or consequence | A valid source may be marked conflicting; the wrong country code could enter `DimAirline`; T-72 may fail on a definition the roster never states. |
| Recommended corrective action | Define `HomeCountry` as the country of the airline's principal headquarters or domicile, and state that legal registration and AOC state are separate concepts. Add the definition to Section 3 and the contract. |
| Owner approval required | Yes - this defines an approved identity attribute. |

### M-02 - `AirlineGroup` boundary and source hierarchy are ambiguous

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 3.1 (L83), Section 6.3 (L199); contract Table 6.2.2 (L723) |
| Evidence | The contract calls `AirlineGroup` a "source-verified group or parent brand." The draft gives the airline's official corporate source precedence for airline group. A subsidiary airline's own site may not state its ultimate parent, and "group" versus "parent brand" is undefined. |
| Why it matters | Group ownership changes are common, and the group label drives comparisons. Without a boundary rule, the same airline can be assigned to a brand, an operating group, or an ultimate parent. |
| Risk or consequence | Inconsistent group values; false group-level comparisons; optional attribute left null unnecessarily or populated with a brand rather than a group. |
| Recommended corrective action | Define the group boundary as the ultimate parent or group brand, specify the parent company or regulator source as authoritative, and add a group hierarchy or a documented null rule. |
| Owner approval required | Yes - this defines an optional identity attribute. |

### M-03 - `OperatingRegion` has no controlled vocabulary

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 3.1 (L84); contract Table 6.2.2 (L726) |
| Evidence | The contract permits a "controlled region label only where explicitly defined and supported" but provides no list of regions and no rule for whether region means headquarters region, primary operating network, or regulatory region. |
| Why it matters | "Region" is not a single source-verifiable fact for a global airline. Without a vocabulary, values will vary by author and source. |
| Risk or consequence | Inconsistent labels; invalid region-level comparisons; optional attribute populated with arbitrary geography. |
| Recommended corrective action | Define a controlled region list and a decision rule, or remove `OperatingRegion` from the identity attributes and treat it as a derived analytical label. Until then, require null. |
| Owner approval required | Yes - this defines an optional identity attribute. |

### M-04 - `BusinessModel` is a classification, not a source-verifiable identity fact

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 3.1 (L85); contract Table 6.2.2 (L727) |
| Evidence | The allowed values are Full Service, Low Cost, Regional, and Charter. No rubric, decision tree, or authoritative source standard is provided. Airlines can operate hybrid models or multiple brands. |
| Why it matters | Business model is an analyst taxonomy, not an identity attribute published by a civil-aviation registry. Treating it as source-verifiable invites false precision and disputes. |
| Risk or consequence | Inconsistent classification; unsupported labels; optional attribute either null for every airline or populated by opinion. |
| Recommended corrective action | Either define a documented classification rubric with examples and a named source standard, or remove `BusinessModel` from the identity attributes and treat it as a derived analytical label with an explicit method. |
| Owner approval required | Yes - this changes the identity attribute set. |

### M-05 - Provenance record design leaves cardinality, vocabulary, and authority unresolved

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 7 (L243), Section 6.5 (L219-221); contract Section 3.4 (L242), T-75 (L1628) |
| Evidence | `SourceRecordID` has no format or uniqueness scope. The grain is one row per `SourceRecordID`, but it is not stated whether one source supporting four attributes requires one record or four. Multiple sources supporting one attribute are allowed, but there is no `IsAuthoritative` or `SelectedForLoad` flag. `AttributeName` has no controlled vocabulary, and there is no normalization rule for values such as country names or legal suffixes. |
| Why it matters | T-75 can only resolve provenance if the record identity and attribute naming are deterministic. Without an authority flag, two `VERIFIED` sources can disagree and both remain eligible. |
| Risk or consequence | Duplicate or ambiguous provenance; a source that supports multiple attributes is recorded inconsistently; the same attribute has several `VERIFIED` values and no selected one; T-75 results depend on implementation choices. |
| Recommended corrective action | Define the `SourceRecordID` format and uniqueness scope; state the one-row-per-source-attribute-assertion rule; add a controlled `AttributeName` list; add an authoritative or selected-for-load flag; define canonicalization and comparison rules. |
| Owner approval required | No for clarification; yes if new schema fields are added. |

### M-06 - Source evidence is not durable, and "stale" is undefined

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 6.2 (L191), Section 6.4 (L213), Section 6.6 (L232), R-2 (L301); contract Section 3.4 (L246, L252) |
| Evidence | The provenance record stores a URL, organization, type, and verification date. It does not require an archived copy, content hash, retrieval timestamp, URL/domain validation, or re-verification interval. Section 6.4 requires "stale" records to be quarantined but never defines stale. |
| Why it matters | A URL is not durable evidence. Pages move, content changes, and sites disappear. Without a captured artifact or hash, the project cannot prove what was verified on the recorded date. |
| Risk or consequence | A `VERIFIED` record remains trusted after its source changes or disappears; an auditor cannot reproduce the verification; stale evidence silently supports current reference data. |
| Recommended corrective action | Add `SourceRetrievedDate` and a content hash or archived-copy reference. Define URL/domain validation and a staleness threshold with a re-verification trigger. State what happens when a previously verified URL becomes unavailable. |
| Owner approval required | Yes - this changes the provenance policy and schema. |

### M-07 - Approval workflow lacks independent verification and reference-version approval criteria

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 12 (L351-370), Section 13 (L397); contract Section 14.1 (L1733), Section 16.4 (L1872-1881) |
| Evidence | The owner is the sole approver and also the person for whom the draft was prepared. There is no named verifier, no review checklist, and no definition of what "verified" means in "only after all fields above are completed and verified." The contract's approval record lists project owner, data architecture lead, Power BI solution architect, and QA/validation lead, but the draft addresses only the owner. No decision ID, owner, or criteria exist for reference-version approval. |
| Why it matters | Self-approval without a challenge step is a control weakness, even in a one-person project. Reference-version approval is a separate gate that the draft requires but does not define. |
| Risk or consequence | A record can be signed without evidence review; reference data can be treated as approved without an accountable approver; the approval cannot be defended to a third party. |
| Recommended corrective action | Add a named reviewer/verifier and a completeness checklist. Define what evidence must be inspected before status changes. Define a reference-version approval decision with an owner and criteria, or document a compensating control if one person holds all roles. |
| Owner approval required | Yes - this changes the approval process. |

### M-08 - Change control uses three different paths for identity changes

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft D-1 (L49), Section 3.2 (L90-91), Section 6.5 (L224-226); contract Section 4.3 (L349), Section 3.4 (L250) |
| Evidence | D-1 says a rename requires a new approved decision and reference version. Section 3.2 says a merger, rebrand, or code change requires a new approved scenario and reference version. Section 6.5 says any identity correction requires a new reference version, a reconciliation note, and a new source record. The contract says a merger or rebrand requires a new approved scenario. |
| Why it matters | A name change, code change, rebrand, merger, and roster change are different events, but the draft assigns overlapping controls. The owner cannot tell which path applies. |
| Risk or consequence | Inconsistent handling; either unnecessary decisions for minor corrections or silent changes under the label of a new version. |
| Recommended corrective action | Define change tiers: attribute correction or code change -> new reference version; merger, rebrand, or operating-model change -> new scenario; airline added or removed -> new decision. Align D-1, Section 3.2, Section 6.5, and the contract. |
| Owner approval required | Yes - this changes change-control policy. |

### M-09 - Semantic-model impact omits the known airline filter-path constraint

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 8.1 (L265); contract Section 8.2 (L1110), Section 8.3 (L1174) |
| Evidence | The draft says airline filter and slicer paths resolve to `DimAirline`. It does not mention the contract's rule that `DimAirline` must not have an active relationship to `DimAircraft`, because that would create a second filter path to `FactFlightOperations`. The contract requires a role-playing `DimAirline - Fleet` dimension or a `TREATAS` measure if fleet-by-airline analysis is needed. |
| Why it matters | This is a known semantic-model risk, not a future unknown. Omitting it from the decision record makes the impact assessment incomplete and invites an ambiguous model. |
| Risk or consequence | Ambiguous filter paths; incorrect fleet-by-airline counts; a model that passes relationship checks but produces inconsistent results. |
| Recommended corrective action | Add the `DimAirline`/`DimAircraft` constraint and the role-playing or `TREATAS` option to Section 8.1, with a cross-reference to contract Section 8.3. |
| Owner approval required | No - this is a documentation correction. |

### M-10 - The evidence register presents the migration's 99 checks as independent assurance

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 14 (L414); migration report L91 |
| Evidence | The register says the migration report is "Complete; 99 checks passed." Those 99 checks were executed by the migration script and validate document consistency, replacement counts, hashes, encodings, and status strings. They are not an independent governance review and do not test the draft. |
| Why it matters | A reader may treat 99 passing checks as evidence that the decision record is sound. The migration report itself says a successful migration proves consistency, not governance quality. |
| Risk or consequence | Overstated assurance; the owner may skip the review the draft still needs; audit evidence is confused with implementation evidence. |
| Recommended corrective action | Label the result as "reported by the migration script; not independently re-executed." Add the migration report hash and a reference to this audit. Keep the 99 checks as document-integrity evidence, not decision-quality evidence. |
| Owner approval required | No - this is a documentation correction. |

### M-11 - Disclosure is conditional and the exact string is inconsistent

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 5 (L147-150); scope L97; contract L73; master prompt L57 |
| Evidence | The draft requires the disclosure on every dashboard, page, "tooltip where practical," and exported result. The qualifier makes tooltip disclosure optional. The draft uses a hyphen (`U+002D`) in "Synthetic Simulation - Not Actual Airline Performance"; the scope, contract, and master prompt use an em dash (`U+2014`). No export template, screenshot, or automated exact-string test is defined. |
| Why it matters | A disclosure control is only effective if it is unconditional and exact. "Where practical" creates an exception path, and two different strings can render differently or fail a check. |
| Risk or consequence | A viewer may see simulated results without the disclosure; an automated check may fail on the character mismatch; exports and screenshots may lose the footer. |
| Recommended corrective action | Remove "where practical" or define approved exceptions with owner sign-off. Adopt one canonical string, preferably the baseline em dash form. Add an export template/footer and an exact-string validation test. |
| Owner approval required | No for the string; yes if exceptions are permitted. |

### M-12 - The approval block approves Sections 2 to 7 while excluding a schema freeze

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft Section 12 (L359), Section 4.2 (L124), Section 7 (L242-243) |
| Evidence | The selected option says "Approve the ten-airline roster and identity rules in Sections 2 to 7." Section 7 defines the reference file grain, key, and required content. Section 4.2 says the record does not freeze "the data contract, the semantic model, or the reference schemas." |
| Why it matters | The owner could be recorded as approving the reference schema in Section 7 while the exclusions say no schema is frozen. The scope of signature is ambiguous. |
| Risk or consequence | A later reader cannot tell whether the schema was approved; the approval may be challenged; the owner may inadvertently authorize design details that still need review. |
| Recommended corrective action | Narrow the selected option to the population and identity rules in Sections 2, 4, 5, and 6, and state that Section 7 is proposed design acknowledged but not frozen. Alternatively, split the decision into population approval and reference-schema approval. |
| Owner approval required | Yes - this changes the approval scope. |

### M-13 - Audit metadata and record-retention controls are incomplete

| Field | Detail |
|---|---|
| Severity | MEDIUM |
| Document and section | Draft L10, Section 12 (L349-382), Section 14 (L411-431), Section 15 (L437) |
| Evidence | The draft has a version number and a "Prepared for" line but no preparer identity, no revision history, no reviewer sign-off, and no retention or immutability rule for the signed copy. The evidence register omits the migration report hash, backup manifest hash, and draft hash. |
| Why it matters | A formal decision record must show who prepared it, what changed between versions, who reviewed it, and where the signed evidence is retained. Hashes without a retention rule can be regenerated from altered files. |
| Risk or consequence | The audit trail cannot be reconstructed; a signed record can be edited after signature; the evidence register cannot be tied to the exact artifacts reviewed. |
| Recommended corrective action | Add prepared-by and reviewed-by fields, a revision table, the missing hashes, and a retention rule that stores the signed copy read-only with its hash in the decision register. |
| Owner approval required | No for documentation; yes for the retention policy. |

## 10. Low findings and observations

### 10.1 Low findings

| ID | Location | Finding | Why it matters | Recommended action | Owner approval |
|---|---|---|---|---|---|
| L-01 | Draft L59 | The heading "Approved airline roster" can imply the roster is formally approved. The body says "exact proposed population" and the status is PENDING. | A reader who scans headings may misread the approval state. | Rename to "Proposed airline roster" or add "(approved as intended population; formal OD-01 pending)" to the heading. | No |
| L-02 | Draft L242-243 | The required-files table omits data types, lengths, and nullability, although the contract defines them. | Implementers must cross-reference two documents; drift is possible. | Add a column or a direct cross-reference to contract Section 3.4 and Table 6.2.2. | No |
| L-03 | Draft L411-431 | The evidence register omits the migration report hash, backup manifest hash, and draft hash. | The exact artifacts reviewed cannot be tied to the record without external lookup. | Add the three hashes and a note that the report hash is recorded in the audit response. | No |
| L-04 | Draft L437 | "Prepared for" is present, but no preparer identity or role is recorded. | The audit trail does not show who prepared the draft. | Add "Prepared by" with name/role and date. | No |
| L-05 | Draft L10 | The draft has version 0.1 but no revision history table. | Future changes cannot be traced to a version. | Add a revision table with version, date, author, and change summary. | No |
| L-06 | Draft L222-223 | A `SUPERSEDED` source record must have a reason, but there is no `SupersededBy` link to the replacement record. | Lineage stops at the superseded record. | Add `SupersededBySourceRecordID` or require the replacement ID in `Notes`. | No |
| L-07 | Scope L20, contract L73, master L19/L57 | The baseline documents use "real, source-verified" in the present tense while no source verification exists and OD-01 is pending. | A reader may believe verification is complete rather than a future obligation. | Change to "real, to be source-verified" or add "verification pending" in each location. | No |
| L-08 | Draft L242; contract L240, L250 | `ReferenceVersion` is `String(30)` with no format or example. | Inconsistent version labels weaken manifest and refresh matching. | Define a format and a validation rule, for example `AIR-YYYY-MM-DD-NNN`. | No |

### 10.2 Observations

| ID | Observation | Recommendation |
|---|---|---|
| O-01 | The draft is 26 KB and 446 content lines for a population decision. Its length is disproportionate to the decision and increases review fatigue. | Add a one-page decision brief at the top and keep the detailed rules as appendices. |
| O-02 | The draft combines a population decision with identity, provenance, and reference-file rules. The HIGH findings are concentrated in the rules, not the roster. | Consider splitting OD-01 into OD-01A (population, signable after narrow corrections) and OD-01B (identity and reference rules, after H-01 to H-07). |
| O-03 | The record is closer to a governance specification than an Architecture Decision Record (ADR). | Use a short ADR template for future decisions and reserve long records for enterprise-grade reference designs. |
| O-04 | The signed record has no version-control binding, and source URLs may carry tracking parameters or credentials. | Commit and tag the signed record after approval, and add a source-URL hygiene rule that excludes tokens, query secrets, and personal data. |
| O-05 | The approval block has no place for reviewer dissent or residual concerns. | Add a short "reviewer challenge and residual concerns" section before the signature block. |

---

## 11. Airline roster validation

### 11.1 Roster as audited

| # | Airline | IATA | ICAO | Home country | Country code | Internal consistency |
|---|---|---|---|---|---|---|
| 1 | Emirates | EK | UAE | United Arab Emirates | AE | Match |
| 2 | Qatar Airways | QR | QTR | Qatar | QA | Match |
| 3 | Singapore Airlines | SQ | SIA | Singapore | SG | Match |
| 4 | Air India | AI | AIC | India | IN | Match |
| 5 | IndiGo | 6E | IGO | India | IN | Match |
| 6 | British Airways | BA | BAW | United Kingdom | GB | Match |
| 7 | Lufthansa | LH | DLH | Germany | DE | Match |
| 8 | Delta Air Lines | DL | DAL | United States | US | Match |
| 9 | Southwest Airlines | WN | SWA | United States | US | Match |
| 10 | Qantas | QF | QFA | Australia | AU | Match |

### 11.2 Validation results

| Check | Result |
|---|---|
| Roster rows in scope Section 2.1 | 10 |
| Roster rows in contract Section 2.1 | 10 |
| Roster rows in master prompt Section 4 | 10 |
| Roster rows in draft Section 3 | 10 |
| Scope vs contract roster | Exact match, 10 of 10 |
| Scope vs master roster | Exact match, 10 of 10 |
| Scope vs draft roster | Exact match, 10 of 10 |
| Duplicate airline names | 0 |
| Duplicate IATA codes | 0 |
| Duplicate ICAO codes | 0 |
| IATA length errors (must be 2) | 0 |
| ICAO length errors (must be 3) | 0 |
| IATA `6E` accepted by `^[A-Z0-9]{2}$` | Yes |
| Country-code duplicates | India/IN twice and United States/US twice; expected, not a defect |
| Fictional airline references in the six active documents | 0 |
| Standalone `AirlineCode` in the six active documents | 0 |
| `AirlineCode` in the draft | 2, both as a rejected concept (D-3 and alternatives); not a schema field |
| `fictional airline` in the draft | 1, as a rejected alternative; not a current identity |

### 11.3 Roster conclusion

The roster is internally consistent, complete, and free of duplicate or malformed
identifiers. BR-01, REQ-001, the traceability matrix, and the progress ledger reference
the ten-airline population without restating a conflicting roster. The audit did not
verify the codes or names against external sources; that remains the future T-75
obligation. The `AirlineName` semantic ambiguity in H-01 is the main identity risk.

## 12. Identity architecture review

### 12.1 What is sound

- The separation of `AirlineKey` (surrogate), `AirlineIATACode` (business identifier),
  `AirlineICAOCode` (alternate identifier), and `AirlineName` is the correct shape.
- The contract states that business keys are unique but are not used as physical
  relationship keys in Power BI (L1006). That protects the semantic model from
  business-key churn.
- `DimAirline` is defined as one row per real airline with exactly ten active members
  and unique IATA, ICAO, and name (contract L335-349).
- Optional attributes are nullable and may not be inferred from home country
  (contract L347; draft D-4).
- Fact tables that carry `AirlineKey` inherit the population, and the draft explicitly
  restricts membership to the approved ten (draft L260-264).

### 12.2 What is not resolved

| Design element | Assessment | Finding |
|---|---|---|
| Stable airline identity | No permanent `AirlineId`; IATA is the business key and provenance link | H-07 |
| Version-qualified uniqueness | Grain is per `ReferenceVersion`, but IATA alone is declared the key | H-07 |
| Surrogate-key stability | `AirlineKey` permanence across versions is not stated | H-03 |
| Slowly changing dimension | No Type 1/Type 2 decision or effective-dating model | H-03 |
| Name changes | Treated as a new decision, scenario, or version depending on section | H-01, M-08 |
| Code changes and reassignment | Acknowledged as a risk, but no key or lineage control | H-07, M-08 |
| Mergers and acquisitions | New scenario required, but no mapping of combined or retired identities | H-03, H-04 |
| Suspension or cessation | No status beyond `IsActive` boolean | H-04 |
| Retired identifiers | No rule for retaining or quarantining retired IATA/ICAO codes | H-07 |
| Power BI filter paths | Known `DimAirline`/`DimAircraft` constraint is omitted from the draft impact | M-09 |
| Referential integrity | Facts restricted to the ten; no orphan quarantine rule in the draft | Observation |

### 12.3 Semantic-model implications

The contract's Section 8.3 is explicit: `DimAirline` must not have an active
relationship to `DimAircraft`, because `DimAirline` already filters
`FactFlightOperations` directly. Activating both paths would create an ambiguous filter
path. Fleet-by-airline analysis requires a role-playing `DimAirline - Fleet` dimension
or a documented `TREATAS` measure (contract L1110, L1174).

The draft's Section 8.1 says only that airline filter paths resolve to `DimAirline`. It
does not carry this constraint forward. That is a documentation gap, not a schema change,
but it matters because the decision record is the artifact a future model builder is
most likely to read.

### 12.4 Architecture conclusion

The identifier separation is correct, but the model is not yet stable under change. A
mutable code cannot simultaneously be the business key, the provenance join key, and the
uniqueness test without a version qualifier or a permanent identifier. Resolve H-07 and
H-03 before the schema is frozen; otherwise the semantic model will inherit an identity
that cannot survive a code change or a reference correction.

---

## 13. Provenance review

### 13.1 What is sound

The draft reproduces the contract's provenance model with reasonable fidelity:

- Attribute-level lineage is required for every populated identity value (draft L219-221).
- The source hierarchy is explicit and prefers official airline, government, and
  ICAO/IATA sources (draft L169-178).
- Source types and verification statuses are controlled (draft L182-189).
- `SourceVerifiedDate` is an actual check date in ISO 8601, not an inferred date
  (draft L191-192).
- Conflict resolution is attribute-specific (draft L196-205).
- Missing required values block approval; optional values remain null (draft L209-215).
- Quarantine, versioning, immutability, and no-fabrication rules are stated
  (draft L213-234).
- The draft explicitly says it does not verify any source and does not create the
  reference files (draft L245-247, L309-312).

### 13.2 What is not resolved

| Provenance requirement | Draft coverage | Assessment |
|---|---|---|
| Every populated attribute is `VERIFIED` | Required attributes only in Section 6.2; T-75 says every attribute | Contradiction - H-02 |
| Stable airline link | `AirlineIATACode` only | Mutable link - H-07 |
| `SourceRecordID` identity | Field named, no format or uniqueness scope | Ambiguous - M-05 |
| One source, many attributes | Not defined | Ambiguous - M-05 |
| Many sources, one attribute | Allowed, but no authoritative/selected flag | Ambiguous - M-05 |
| Controlled `AttributeName` | No vocabulary | Ambiguous - M-05 |
| Value normalization | No canonicalization rule | Gap - M-05 |
| Source durability | URL and date only; no archive or hash | Gap - M-06 |
| Staleness | Term used, never defined | Gap - M-06 |
| URL/domain validation | Not defined | Gap - M-06 |
| Superseded lineage | Reason required, no successor link | Gap - L-06 |
| Record-level audit metadata | No created/modified by/date | Gap - M-13 |
| Reference-version approval | Required, but no owner or criteria | Gap - M-07 |

### 13.3 Provenance conclusion

The provenance design is stronger than most portfolio projects and is close to
enterprise-grade in intent. It is not yet executable without interpretation. The
combination of a mutable airline key, an undefined source-record cardinality, and an
optional-attribute verification contradiction means two competent implementers could
build different registers and both claim compliance.

## 14. Synthetic-data governance review

### 14.1 What is sound

- The draft separates real identity attributes from synthetic operational, customer,
  booking, revenue, cost, disruption, feedback, and financial data (draft L136-145).
- The disclosure is required on dashboards, pages, and exports (draft L147-150).
- The presentation rule prohibits titles, commentary, filenames, and narrative that
  imply actual airline performance (draft L152-155).
- Real passenger personal information is prohibited (draft L157-158).
- The exclusions prohibit claims of airline affiliation, sponsorship, or endorsement
  (draft L128-129).
- The scope, contract, and master prompt carry the same boundary (scope L55-58 and
  L90-97; contract L73; master L57).

### 14.2 What is not resolved

| Control | Assessment | Finding |
|---|---|---|
| Disclosure is unconditional | "Tooltip where practical" creates an exception | M-11 |
| Disclosure string is exact | Draft uses hyphen; baseline uses em dash | M-11 |
| Exports and screenshots retain disclosure | No export template or image control | M-11 |
| Disclosure is tested | No exact-string or rendered-output test | M-11 |
| Airline names do not imply endorsement | Explicit no-affiliation statement; legal review not performed | Observation |
| Synthetic data cannot be mistaken for actual performance | Strong wording; residual risk remains | R-4, M-11 |

### 14.3 Synthetic-governance conclusion

This is the strongest domain in the draft. The boundary is clear, repeated, and
consistent in substance. The remaining weakness is operational: a disclosure that is
optional on tooltips and spelled two ways is not a controlled disclosure. Fix M-11 and
add a rendered-output check before the first report page is released.

---

## 15. Formal approval review

### 15.1 Current state

| Field | Draft value | Assessment |
|---|---|---|
| Decision ID | OD-01 | Correct |
| Decision title | Real airline identity population | Correct |
| Decision owner / approver | KH Mohammad Farhan | Correct and consistent with contract L1737 |
| Decision date | `[BLANK]` | Correct - not invented |
| Owner signature | Blank line | Correct - not invented |
| Owner approval evidence | `[BLANK]` | Correct - not invented |
| Formal status | `PENDING OWNER SIGNATURE` | Correct |
| G3 | `NOT STARTED` | Consistent with ledger, but contradicted by design evidence (H-05) |
| G4 | `BLOCKED` | Consistent with ledger |
| OD-01 in contract | `PENDING - ROSTER APPROVED AS INTENDED POPULATION; FORMAL DECISION RECORD INCOMPLETE` | Consistent |

No section states that OD-01 is already approved. The draft distinguishes the roster
approved as the intended population from formal approval of the decision record. That
distinction is clear in the purpose, the status block, the approval block, and Section 13.

### 15.2 Fields required before OD-01 can become APPROVED

1. Owner confirmation that the record has been reviewed.
2. Decision date, entered at signature.
3. Owner signature.
4. Approval evidence reference, including the signed copy location.
5. Verification that all fields are complete, by a named verifier or documented
   compensating control.
6. Confirmation of the approval scope, including whether Section 7 is acknowledged
   design or approved schema (M-12).
7. Update of the OD-01 row in contract Section 14 and the Section 14.1 register.
8. Retention of the signed copy with a hash in the evidence register (M-13).

### 15.3 Approval-control weaknesses

- The owner is also the preparer and the only approver; there is no independent
  reviewer (M-07).
- "Verified" is not defined and no checklist exists (M-07).
- The selected option covers Sections 2 to 7 while the exclusions disclaim a schema
  freeze (M-12).
- No reference-version approval owner or criteria exist (M-07).
- No retention or immutability rule protects the signed record (M-13).

### 15.4 Approval conclusion

The approval block is structurally complete and honest about the pending state. It is
not control-complete. The draft is not ready for signature until the HIGH findings and
M-07/M-12 are resolved.

---

## 16. Cross-document traceability

### 16.1 Reference consistency

| Item | Draft | Baseline | Result |
|---|---|---|---|
| OD-01 status | PENDING | Contract L1703 and L1737 PENDING | Match |
| Roster | 10 rows, Section 3 | Scope L42-53, contract L79-90, master L44-55 | Exact match |
| IATA/ICAO identifiers | Separate fields, D-3 | Contract L239, L720-721 | Match |
| Reference datasets | `ref_airlines.csv`, `ref_airline_sources.csv` | Contract L214-215, L238 | Match |
| Synthetic boundary | Section 5 | Scope L55-58, contract L73, master L57 | Match in substance |
| BR-01 | Section 8.2 | BR-01 L6-17 | Match |
| REQ-001 | Section 8.2 | Traceability L7 | Match |
| REQ-023 to REQ-027 | Section 8.2 | Traceability L29-33; contract L1632 | Match |
| T-72 to T-77 | Section 8.3 | Contract L1625-1630 | Match |
| Contract version | 1.4 | Contract L1870; ledger L9 | Match |
| G3 | NOT STARTED | Ledger L9 | Text match; substantive contradiction (H-05) |
| G4 | BLOCKED | Ledger L10 | Match |
| Approval register | Owner KH Mohammad Farhan | Contract L1737 | Match |

### 16.2 Contradictions and inconsistencies

| ID | Issue | Evidence | Severity |
|---|---|---|---|
| X-01 | G3 is NOT STARTED while design evidence is recorded in the same ledger row | Ledger L9; contract v1.4 | HIGH - H-05 |
| X-02 | D-1 requires a new decision for a rename; the contract requires a new scenario for a merger or rebrand; Section 6.5 requires a new version for an identity correction | Draft L49, L90-91, L224-226; contract L349, L250 | MEDIUM - M-08 |
| X-03 | Disclosure string uses a hyphen in the draft and an em dash in the baseline | Draft L150; scope L97; contract L73; master L57 | MEDIUM - M-11 |
| X-04 | Baseline says "real, source-verified" in the present tense; the draft says "must be source-verified" and no verification exists | Scope L20; contract L73; master L19/L57; draft L50 | LOW - L-07 |
| X-05 | Approval block approves Sections 2 to 7; exclusions disclaim a reference-schema freeze | Draft L359, L124, L242-243 | MEDIUM - M-12 |

### 16.3 Missing cross-references

- The draft's Section 8.1 does not cite contract Section 8.3 on the
  `DimAirline`/`DimAircraft` filter path (M-09).
- The evidence register does not include the migration report hash, backup manifest
  hash, or draft hash (L-03).
- The draft does not cite the original migration backup, only the pre-write apply
  backup (L-03).

### 16.4 Test and requirement traceability

- No incorrect test IDs were found. T-72 to T-77 exist in the contract and are
  described consistently in the draft.
- No untraceable requirement was found. REQ-001 and REQ-023 to REQ-027 exist in the
  traceability matrix and map to the draft's impact table.
- All requirements remain NOT STARTED. The draft does not claim otherwise.
- The missing airline reference-version test is a control gap, not an incorrect ID
  (H-06).

### 16.5 Traceability conclusion

Identifier-level traceability is strong. Status-level and change-control traceability
are not. A reader can find every referenced requirement and test, but cannot reconcile
the G3 status, the three change-control paths, or the approval scope without
interpretation.

## 17. Risk scenario assessment

| # | Scenario | Coverage | Evidence | Finding |
|---:|---|---|---|---|
| 1 | Airline changes its official name | Partial | R-1 and D-1 require a new version/decision; name semantics undefined | H-01, M-08 |
| 2 | IATA code changes | Partial | R-1 and R-6 acknowledge the risk; no stable key or code-history mapping | H-07, M-08 |
| 3 | ICAO code changes | Partial | Same as IATA; alternate identifier has no history rule | H-07, M-08 |
| 4 | Airline merger or acquisition | Partial | Section 3.2 requires a new scenario; no combined/retired identity mapping | H-03, M-02 |
| 5 | Two sources disagree on an attribute | Covered in principle | Section 6.3 precedence and Section 6.4 quarantine; no same-tier tie-breaker or authority flag | M-05 |
| 6 | Source website becomes unavailable | Partial | R-2 says sources may be unavailable; no archive, hash, or re-verification trigger | M-06 |
| 7 | Historical source evidence changes | Partial | Section 6.5 requires a new version and reconciliation note; no re-verification trigger | M-06, H-03 |
| 8 | Airline group ownership changes | Partial | R-1 and R-3 acknowledge change; group boundary and source are undefined | M-02 |
| 9 | Business-model classification is disputed | Partial | R-3 allows null; no rubric or authoritative standard | M-04 |
| 10 | Airline operating region is undefined | Partial | R-3 allows null; no controlled vocabulary | M-03 |
| 11 | Airline is suspended or ceases operations | **Gap** | No risk, status, or effective-dating control; `IsActive` is a boolean only | H-04 |
| 12 | Reference dataset is updated after a model refresh | Partial | Section 6.5 and contract L290 require one selected version; no airline version/manifest test | H-06, H-04 |
| 13 | Historical synthetic data becomes inconsistent with a changed identity reference | **Gap** | No historical mapping, SCD rule, or re-reconciliation test | H-03, H-04 |
| 14 | Dashboard user mistakes simulated performance for actual | Partial | R-4 and Section 5 disclosure; qualifier, string mismatch, and export control weaken it | M-11 |

**Risk coverage summary:** 1 covered in principle, 11 partial, 2 gaps. The two gaps are
material because they affect the identity population and historical reporting, not just
documentation.

---

## 18. Approval readiness decision

**NOT READY - MATERIAL CORRECTIONS REQUIRED.**

The core roster is correct and the draft is honest about its pending status. The
decision is defensible in principle. But the owner would be signing a record that:

- does not define what `AirlineName` means;
- contradicts itself on whether optional attributes must be `VERIFIED`;
- has no stable airline identifier or version-qualified key;
- has no SCD or historical identity model;
- omits three required risk scenarios;
- reports G3 as NOT STARTED despite the design evidence it relies on;
- has no airline reference-version integrity test;
- approves Sections 2 to 7 while disclaiming a schema freeze.

Those are material, not cosmetic. The record is not ready for signature as written.

### 18.1 What would change the decision

1. Close H-01 to H-07.
2. Close M-07 (approval workflow) and M-12 (approval scope).
3. Add an independent reviewer or a documented compensating control.
4. Re-run this audit against the corrected draft and confirm the HIGH findings are
   closed.

If the owner wants to sign only the population decision, split OD-01 into a narrow
population record and a separate identity/reference-rules record. The population record
would still need H-01, H-02, and H-07 resolved or explicitly excluded, and M-12 narrowed.

**No approval is granted by this audit.**

---

## 19. Required corrective action register

| ID | Priority | Action | Findings | Owner approval | Blocks signature |
|---|---|---|---|---|---|
| A-01 | P1 | Define `AirlineName` as commercial brand; add optional `LegalName` or exclude legal names; update T-72 | H-01 | Yes | Yes |
| A-02 | P1 | Require `VERIFIED` for every populated attribute; align Section 3.1, 6.2, 6.5, and T-75 | H-02 | Yes | Yes |
| A-03 | P1 | Add stable `AirlineId`/permanent `AirlineKey`; define version-qualified business and alternate keys; update provenance and tests | H-07 | Yes | Yes |
| A-04 | P1 | Define SCD/effective dating, `AirlineKey` stability, and historical mapping; add historical reconciliation test | H-03 | Yes | Yes |
| A-05 | P1 | Add suspension/cessation, post-refresh reference change, and historical inconsistency risks, controls, and tests | H-04 | Yes | Yes |
| A-06 | P1 | Define G3 status semantics; mark IN PROGRESS or rename NOT FORMALLY APPROVED; add gate criteria | H-05 | Yes | Yes |
| A-07 | P1 | Add airline reference-version/manifest integrity test T-78 or extend T-77 | H-06 | Yes | Yes |
| A-08 | P1 | Add verifier/reviewer role, completeness checklist, and reference-version approval owner/criteria | M-07 | Yes | Yes |
| A-09 | P1 | Narrow approval scope to Sections 2, 4, 5, and 6; acknowledge Section 7 as proposed design, not frozen | M-12 | Yes | Yes |
| A-10 | P2 | Define `HomeCountry`, `AirlineGroup`, `OperatingRegion`, and `BusinessModel` semantics, vocabularies, and rubrics | M-01 to M-04 | Yes | Before reference build |
| A-11 | P2 | Define `SourceRecordID` cardinality, `AttributeName` vocabulary, authority flag, normalization, archival, staleness, and URL validation | M-05, M-06 | Yes if schema changes | Before reference build |
| A-12 | P2 | Reconcile the three change-control paths into explicit tiers | M-08 | Yes | Before schema freeze |
| A-13 | P2 | Add the `DimAirline`/`DimAircraft` filter-path constraint to Section 8.1 | M-09 | No | Before model build |
| A-14 | P2 | Label the 99 checks as reported, not independent; add the migration report hash and draft hash | M-10, L-03 | No | No |
| A-15 | P2 | Fix disclosure qualifier, canonical string, export template, and exact-string test | M-11 | No for wording; yes for exceptions | Before report release |
| A-16 | P2 | Add preparer/reviewer fields, revision history, retention/immutability rule, and signed-copy hash | M-13, L-04, L-05 | No for documentation; yes for retention | Before signature |
| A-17 | P3 | Fix heading, table data types, `SupersededBy`, present-tense "source-verified", and `ReferenceVersion` format | L-01, L-02, L-06, L-07, L-08 | No | No |
| A-18 | P3 | Adopt the one-page brief, consider splitting OD-01, use ADR format, commit/tag the signed record, add reviewer challenge | O-01 to O-05 | Yes for split | No |

---

## 20. Final governance status

| Item | Status |
|---|---|
| OD-01 | **PENDING** - formal decision record incomplete |
| Decision record | Draft, `PENDING OWNER SIGNATURE` |
| Approval readiness | **NOT READY - MATERIAL CORRECTIONS REQUIRED** |
| Overall audit score | **61/100** |
| Critical findings | 0 |
| High findings | 7 |
| Medium findings | 13 |
| Low findings | 8 |
| Observations | 5 |
| G3 - Data design | **NOT STARTED** (status semantics disputed - H-05) |
| G4 - Data generation | **BLOCKED** |
| Reference CSV population | Not authorized; no files exist |
| Schema freeze | Not authorized |
| Dataset generation | Not authorized |
| Power BI files | None created or modified |
| Git operations | None performed |
| Baseline integrity | All six hashes unchanged |
| Draft integrity | Hash unchanged: `C594DFCD8FE1B6809E28CBE1B3EE6D24FAA0772D35DD1FE57767FECCD3CA2A60` |

**Final statement.** This audit does not approve OD-01, does not sign the draft, does not
change G3 or G4, and does not authorize reference data or generation. The draft is a
strong foundation with material governance corrections outstanding. The owner should not
sign it until the P1 actions are closed and the corrected draft is re-audited.

The SHA256 of this report is calculated after creation and reported in the audit
response. It is not embedded here to avoid a self-referential hash.

