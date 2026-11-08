# AEROVISION 360 — OD-01 Compensating Control and Remediation Proposal

**Document ID:** OD01-CCP-2026-11-02  
**Document type:** Proposal for owner review — not an approval, signature, waiver, gate decision, or implementation authorization  
**Status:** PROPOSED — OWNER REVIEW AND EXPLICIT AUTHORIZATION REQUIRED  
**Prepared:** 2026-11-02  
**Prepared by:** Build AI agent — non-independent preparer  
**Project owner / approver:** KH Mohammad Farhan  
**Governing baselines:** `03_DATA_CONTRACTS.md` version 1.5; `01_PROJECT_SCOPE.md` version 1.1  
**Decision records:** `OD01A_AIRLINE_POPULATION_DECISION.md` version 0.1; `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` version 0.1  
**G3:** `NOT STARTED`  
**G4:** `BLOCKED`  
**`G3-RV-01`:** `NOT EXECUTED`

> **Status notice — not an approval**
>
> The owner has selected the documented compensating-control route because no
> independent reviewer is currently assigned. This proposal prepares the
> controls, the finding re-audit, and the controlled changes needed for a
> defensible approval process. It does not approve OD-01A or OD-01B, does not
> sign either record, does not accept any control on the owner's behalf, and
> does not authorize reference data, schema freeze, data generation, G3, G4,
> Power BI, or Git operations.
>
> No signature, approval date, decision, reviewer identity, or independent
> assurance has been created or inferred. The AI preparer is not an independent
> reviewer. Automated checks in this proposal are document-integrity evidence,
> not independent assurance.

---

## 1. Controlling sources and current state

### 1.1 Sources used

The current versions of the following records were used:

- `docs/OD01A_AIRLINE_POPULATION_DECISION.md`
- `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`
- `docs/OD01_OWNER_DECISION_CONFIRMATION.md`
- `docs/OD01_OWNER_DECISION_RESOLUTION.md`
- `docs/OD01_REMEDIATION_CHANGE_RECORD.md`
- `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md`
- `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md`
- `docs/01_PROJECT_SCOPE.md`
- `docs/02_BUSINESS_REQUIREMENTS.md`
- `docs/03_DATA_CONTRACTS.md`
- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/PROGRESS_LEDGER.md`

### 1.2 Current hashes

All hashes below were recomputed with PowerShell `Get-FileHash -Algorithm SHA256` on 2026-11-02. Every listed file is UTF-8 without a byte-order mark and LF-only at the time of verification. These are integrity results, not content assurance.

| File | SHA-256 | Bytes |
|---|---|---:|
| `OD01A_AIRLINE_POPULATION_DECISION.md` | `399241AD2AE21F4A1FB3D7E589950117F9CDADB8303F78CC161F484CD7255A06` | 11,487 |
| `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | `CDD48B9F0B68CE401D827E5F910076104CCCE73FFBF7BA0A6BC21D75D07C3C05` | 20,782 |
| `OD01_OWNER_DECISION_CONFIRMATION.md` | `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD` | 28,055 |
| `OD01_OWNER_DECISION_RESOLUTION.md` | `BE62CBDC017073F6D9135D7DEEF3993F64D74D881102A5C867134C889E20A220` | 78,760 |
| `OD01_REMEDIATION_CHANGE_RECORD.md` | `B74329743E5FD5343FA8EB0F1A103436C54A63D949526437E902EA03D6869A22` | 20,796 |
| `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` | `FD94BD369D3DDDC1AF84C040C27014F112E74B4B0F938CE95B617C7B142BECE6` | 63,965 |
| `OD01_REMEDIATION_DESIGN_SPECIFICATION.md` | `CC3BCE621142C31B4BB7A46F4CBCB320E640466228184AE2E94E196796F3F8A4` | 119,064 |
| `01_PROJECT_SCOPE.md` | `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` | 6,384 |
| `02_BUSINESS_REQUIREMENTS.md` | `F5B3140A91C868692A37609F904129BD166861045A9D00C9840815B0CCC4E709` | 5,921 |
| `03_DATA_CONTRACTS.md` | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` | 211,846 |
| `REQUIREMENTS_TRACEABILITY.md` | `4EE19E921BDC3067D17E172422D85D76B2660EF478EF4AB385D816BA4C314DEB` | 5,742 |
| `PROGRESS_LEDGER.md` | `C6297622D8CFE5BD90402BBB034B1091C70BAA2895BF0438F4E94C003E343C1F` | 4,076 |

### 1.3 Scope evidence — current versus old

| Evidence | SHA-256 | Status |
|---|---|---|
| Current `01_PROJECT_SCOPE.md` v1.1 | `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` | Current, 6,384 bytes, last updated 2026-11-02 |
| `scope_alignment_backup_20261102_202419/01_PROJECT_SCOPE.md` | `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` | Pre-correction backup, 5,790 bytes |
| OD-01A E-07 cited value | `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` | Stale; matches the backup, not the current scope |

The old hash is not invented: it matches the preserved backup. It is nevertheless obsolete for a current approval record.

### 1.4 Document-control limitation

The owner-confirmation record is historical. It records the eight owner-confirmed choices but also states that contract v1.4 is governing, that contract v1.5 does not exist, and that OD-01A/OD-01B are not prepared. Those statements are superseded by the current contract v1.5 and the prepared decision records. The original record must remain intact; B-05 proposes a controlled addendum.

---

## 2. Compensating-control proposal

### 2.1 Policy statement

The owner has selected documented compensating controls with explicit owner acceptance, while retaining independent review as a future improvement. The controls below are designed to make the review rigorous and transparent. They do not create independent assurance and do not waive any mandatory requirement.

The following rules apply to every control:

- The AI preparer is not independent.
- The project owner is the approver and is not independent of the preparation process.
- Automated checks verify integrity and consistency, not governance quality or implementation correctness.
- No control is treated as accepted until the owner explicitly accepts it in writing.
- A control failure is recorded, not hidden by a later check.
- A finding is not closed merely because a document says it is closed.

### 2.2 Control catalogue

#### CC-01 — Owner-performed structured self-review

| Field | Detail |
|---|---|
| Control ID | `CC-01` |
| Objective | Require the owner to review the decision scope, evidence, conditions, and residual limitations before signing. |
| Procedure | Owner reads OD-01A, OD-01B, this proposal, the current scope, and the re-audit results; completes a structured checklist; records questions and residual concerns; initials each checked item. |
| Evidence required | Dated owner self-review checklist; owner initials; unresolved questions and dispositions. |
| Execution status | `NOT EXECUTED` — owner action pending. |
| Responsible person | Project owner. |
| Limitation | The owner is the approver and requested the preparation; this is not independent review. |
| Acceptance criterion | Checklist completed, all critical questions resolved or recorded as conditions, and owner accepts the residual limitation in writing. |

#### CC-02 — Independent challenge checklist performed separately from the original preparation

| Field | Detail |
|---|---|
| Control ID | `CC-02` |
| Objective | Challenge assumptions, evidence, closure claims, and approval scope from a perspective separate from the original preparation. |
| Procedure | A named human reviewer who did not prepare the records uses a challenge checklist; records challenges, responses, unresolved items, and a `CONCUR` / `CONCUR WITH RESERVATIONS` / `DISSENT` result. |
| Evidence required | Reviewer name, role, organization, independence statement, checklist, findings, and result. |
| Execution status | `NOT EXECUTED` — no independent reviewer is assigned. The document-level adversarial re-audit in Section 3 is not a substitute and must not be labelled independent. |
| Responsible person | Independent reviewer; if unavailable, the owner must accept the documented limitation. |
| Limitation | Without a reviewer, this control cannot provide independent assurance. The future-review recommendation is CC-10. |
| Acceptance criterion | Reviewer result recorded with signature/date; or owner explicitly accepts the absence of independent review and the compensating controls. |

#### CC-03 — Automated document-integrity and hash verification

| Field | Detail |
|---|---|
| Control ID | `CC-03` |
| Objective | Prove that the files inspected are the exact files recorded and detect encoding, BOM, or line-ending drift. |
| Procedure | Compute SHA-256 with PowerShell; compare with recorded hashes; check byte length, UTF-8 BOM, and CRLF count; record the method and actual result. |
| Evidence required | Hash table, command/method record, encoding and line-ending results, exceptions. |
| Execution status | `EXECUTED — document-level` on 2026-11-02. Results are in Section 1.2 and Section 11. |
| Responsible person | Build AI preparer; owner or delegate may independently re-run. |
| Limitation | Integrity only. It does not prove correctness, completeness, or independent approval. |
| Acceptance criterion | All compared hashes match expected values; no unexplained BOM/line-ending differences; any mismatch stops approval. |

#### CC-04 — Cross-document consistency verification

| Field | Detail |
|---|---|
| Control ID | `CC-04` |
| Objective | Verify that the eight owner-confirmed choices and critical terms are consistent across OD-01A, OD-01B, the contract, traceability, and the ledger. |
| Procedure | Targeted section and text comparison for `AirlineId`, `AirlineKey`, `ReferenceVersion`, manifest authority, immutable mapping, `LegalName`, `BusinessModelClass`, `OperatingRegion`, reviewer controls, and disclosure. |
| Evidence required | Consistency matrix; contradictory or ambiguous passages; disposition. |
| Execution status | `EXECUTED — document-level` on 2026-11-02. |
| Responsible person | Build AI preparer. |
| Limitation | Human interpretation remains; not independent. |
| Acceptance criterion | No unresolved contradiction remains; exceptions are disclosed and accepted. |

#### CC-05 — Requirement-to-evidence traceability

| Field | Detail |
|---|---|
| Control ID | `CC-05` |
| Objective | Show that each relevant requirement and test has a planned evidence path and an honest status. |
| Procedure | Trace REQ-001, REQ-004, REQ-028, T-72 to T-79, and `G3-RV-01` to the evidence paths and current status. |
| Evidence required | Traceability table; planned evidence path; current status; blocker. |
| Execution status | `EXECUTED — document-level` on 2026-11-02. All test evidence remains `PLANNED` or `BLOCKED`; no test is reported as `PASS`. |
| Responsible person | Build AI preparer. |
| Limitation | Document-level traceability only; no executed data test. |
| Acceptance criterion | Every relevant requirement has a named evidence path and an accurate status; no manufactured PASS. |

#### CC-06 — Explicit HIGH and MEDIUM finding closure evidence

| Field | Detail |
|---|---|
| Control ID | `CC-06` |
| Objective | Re-audit H-01 to H-07 and M-07/M-12 against the current files and record closure or non-closure with evidence. |
| Procedure | Read the original finding; inspect the current remedies; verify actual text and hashes; classify `CLOSED`, `PARTIALLY CLOSED`, `OPEN`, or `NOT VERIFIABLE`; record residual risk and owner action. |
| Evidence required | Section 3 finding table; exact evidence references; residual risks. |
| Execution status | `PARTIALLY EXECUTED — non-independent document re-audit`. H-04, H-05, M-07, and M-12 remain partially closed. |
| Responsible person | Build AI preparer (non-independent); owner must accept or obtain independent review. |
| Limitation | Static document verification only; no implementation or independent assurance. |
| Acceptance criterion | All findings are `CLOSED` with verified evidence and owner acceptance, or the remaining findings are expressly accepted as conditions. This criterion is **not met** today. |

#### CC-07 — Residual-risk register

| Field | Detail |
|---|---|
| Control ID | `CC-07` |
| Objective | Record the residual risks that remain after the proposed controls and document owner acceptance. |
| Procedure | Maintain the risk register in Section 12; owner initials each residual or rejects it; re-review on any material change. |
| Evidence required | Risk register with risk, impact, control, residual status, owner decision. |
| Execution status | `PREPARED — OWNER ACCEPTANCE PENDING`. |
| Responsible person | Owner accepts; preparer maintains the record. |
| Limitation | Qualitative assessment; no independent validation. |
| Acceptance criterion | Owner acceptance is recorded for each risk or an explicit rejection/condition is recorded. |

#### CC-08 — Evidence preservation

| Field | Detail |
|---|---|
| Control ID | `CC-08` |
| Objective | Preserve signed records and evidence read-only so that the approved artifact can be reconstructed and verified. |
| Procedure | Use the proposed structure in Section 9; store the signed copy read-only; record SHA-256 and byte size; verify before and after signing; restrict edits; corrections require a new version. |
| Evidence required | Retention directory, hash register, verification log, retention statement. |
| Execution status | `DESIGNED — NOT EXECUTED`. No approval directory or evidence file has been created. |
| Responsible person | Owner or designated records custodian. |
| Limitation | Not yet instantiated; read-only controls are untested. |
| Acceptance criterion | Signed copy and evidence are stored read-only; hashes match; retention owner is named. |

#### CC-09 — Reviewer limitation statement

| Field | Detail |
|---|---|
| Control ID | `CC-09` |
| Objective | State plainly that no independent reviewer is assigned and that the approval relies on owner-accepted compensating controls. |
| Procedure | Include the limitation statement in the OD-01A and OD-01B approval records and in the owner acceptance; do not use language implying independent assurance. |
| Evidence required | Signed owner acknowledgment and the limitation text in both records. |
| Execution status | `DRAFTED — OWNER ACCEPTANCE PENDING`. |
| Responsible person | Project owner. |
| Limitation | A statement of limitation cannot cure the absence of independence. |
| Acceptance criterion | Owner signs the limitation statement and no record claims independent assurance. |

#### CC-10 — Future independent review recommendation

| Field | Detail |
|---|---|
| Control ID | `CC-10` |
| Objective | Schedule an independent review when a suitable reviewer becomes available. |
| Procedure | Define a reviewer profile, scope, trigger, evidence package, and target date; perform the review after approval without changing the approved decision retroactively. |
| Evidence required | Future review plan and, when completed, reviewer result. |
| Execution status | `DRAFTED — NOT EXECUTED`. |
| Responsible person | Project owner. |
| Limitation | Future improvement only; no current assurance. |
| Acceptance criterion | Owner approves the plan; future review completed and recorded. |

### 2.3 Control execution summary

| Control | Status | Independent assurance? |
|---|---|---|
| CC-01 Owner self-review | `NOT EXECUTED` | No |
| CC-02 Independent challenge | `NOT EXECUTED` | No — no reviewer |
| CC-03 Hash/integrity verification | `EXECUTED` document-level | No |
| CC-04 Cross-document consistency | `EXECUTED` document-level | No |
| CC-05 Requirement-to-evidence traceability | `EXECUTED` document-level | No |
| CC-06 Finding closure evidence | `PARTIALLY EXECUTED` | No |
| CC-07 Residual-risk register | `PREPARED` | No |
| CC-08 Evidence preservation | `DESIGNED` | No |
| CC-09 Reviewer limitation statement | `DRAFTED` | No |
| CC-10 Future independent review | `DRAFTED` | No — future only |

**No control in this proposal creates independent assurance.**

---

## 3. Re-audit of original findings

### 3.1 Method and limitation

Each original finding was re-read from the audit report, then checked against the current OD-01A, OD-01B, contract, scope, traceability, and ledger. The check was static document verification. No source records, reference CSV, data test, semantic model, or Power BI runtime was available. No finding was marked closed solely because another document claimed closure.

The AI preparer is not independent. The results below are a non-independent adversarial re-audit and must be treated as such.

### 3.2 Status summary

| Finding | Status | Basis |
|---|---|---|
| H-01 `AirlineName` legal versus brand | `CLOSED — document-level` | Current OD-01A/OD-01B/contract define commercial brand and optional reference-only `LegalName`. |
| H-02 Optional identity attributes and `VERIFIED` | `CLOSED — document-level` | Current rule requires `VERIFIED` for every populated identity attribute; optional attributes remain null. |
| H-03 SCD, effective dating, `AirlineKey` stability | `CLOSED — document-level` | Type 1 with immutable snapshots; permanent `AirlineKey`; T-78 historical/version checks defined. |
| H-04 Risk register omissions | `PARTIALLY CLOSED` | Controls exist in design, but no current risk-register entries R-09 to R-11. |
| H-05 G3 status contradiction | `PARTIALLY CLOSED` | Vocabulary and gate criteria exist, but ledger still says `NOT STARTED` beside design evidence. |
| H-06 Reference-version and manifest integrity test | `CLOSED — document-level` | T-78 and manifest authority defined; T-78 not executed. |
| H-07 Mutable IATA code as business key | `CLOSED — document-level` | Stable `AirlineId`/`AirlineKey`; codes version-qualified attributes; provenance links to `AirlineId`. |
| M-07 Approval workflow and reference-version approval criteria | `PARTIALLY CLOSED` | Reviewer/compensating-control requirement and `G3-RV-01` criteria exist; no reviewer, acceptance, or executed checklist. |
| M-12 Approval block scope versus schema freeze | `PARTIALLY CLOSED` | Exclusions exist, but the approval block still lacks an explicit narrow scope statement. |

### 3.3 H-01 — `AirlineName` legal name versus commercial brand

- **Original finding:** The draft did not define whether “official” airline name meant the registered legal entity or the commercial brand. T-72 exact reconciliation could fail or produce false conflicts.
- **Required remediation:** Define `AirlineName` as the approved commercial brand; make `LegalName` optional reference/provenance only or state legal names are out of scope; add canonicalization and update T-72.
- **Evidence currently available:** OD-01A §3 defines `AirlineName` as the commercial brand and says it is not the legal registered name; OD-01B §2.4, §4, and §5 state the same and make `LegalName` optional, reference-only, and omitted when unverified; contract §3.4 and Table 6.2.2 align.
- **New verification performed:** Read the current decision records and contract; searched for `AirlineName` and `LegalName`; confirmed no contradictory current rule remains.
- **Result:** `CLOSED — document-level`.
- **Residual risk:** The ten names and legal names have not been source-verified; T-72 and T-75 are not executed. A future source-verification exercise could reveal a brand/legal mismatch.
- **Evidence reference:** OD-01A §3; OD-01B §2.4, §4, §5; contract §3.4; current hashes in Section 1.2.
- **Owner action:** No new decision is required for the definition. Source verification remains a `G3-RV-01` prerequisite.
- **Independent-review question:** The finding was a definition defect; a document-level correction can address it, but this does not create independent assurance. The overall re-audit condition remains open.

### 3.4 H-02 — Optional identity attributes and `VERIFIED` status

- **Original finding:** The rule required `VERIFIED` only for populated required attributes, while T-75 required every populated identity attribute to resolve to a `VERIFIED` record.
- **Required remediation:** Require `VERIFIED` for every populated identity attribute, required or optional; an optional attribute without a `VERIFIED` source remains null; align the rule and T-75.
- **Evidence currently available:** OD-01B §2.5 and §5 require every populated identity attribute to have a `VERIFIED` source and permit null for optional attributes; contract §3.4 and T-75 align; `LegalName` and `AirlineGroup` are optional and null when unverified.
- **New verification performed:** Read the current attribute rules and provenance section; compared the rule with T-75 wording; no “source-supported” or “reliable evidence” exception remains in the current relevant rule.
- **Result:** `CLOSED — document-level`.
- **Residual risk:** No actual `ref_airline_sources.csv` exists; T-75 has not run; optional values could still be populated incorrectly in implementation.
- **Evidence reference:** OD-01B §2.5, §4, §5; contract §3.4; T-75.
- **Owner action:** No new decision for the rule. Execute T-75 after reference data is authorized.
- **Independent-review question:** Document-level correction is sufficient for the wording defect; no independent review is claimed. Implementation evidence remains absent.

### 3.5 H-03 — SCD, effective dating, and `AirlineKey` stability

- **Original finding:** The draft did not define whether `AirlineKey` is permanent, whether `DimAirline` is Type 1 or Type 2, or how historical facts map after a reference change.
- **Required remediation:** Define a permanent `AirlineKey`, a Type 1 or Type 2 baseline, effective dating, and a historical reconciliation test.
- **Evidence currently available:** OD-01B §2.8 and §6 define Type 1 with immutable reference versions; §3 and §4 define permanent `AirlineKey` values 1–10 and stable `AirlineId`; §7 defines T-78-09/10 for unapproved keys and mixed versions; contract §4.3 and §13 align. Type 2 is deferred.
- **New verification performed:** Read the current lifecycle and key sections; checked the T-78 sub-checks and contract model; confirmed the Type 1 rule and no rekeying.
- **Result:** `CLOSED — document-level`.
- **Residual risk:** T-78 has not run; no `DimAirline` exists; historical as-was identity reporting is a known Type 1 limitation.
- **Evidence reference:** OD-01B §2.8, §3, §4, §6, §7; contract §4.3, §13.
- **Owner action:** No new decision for the design. Execute T-78 after reference data is authorized.
- **Independent-review question:** No independent review is claimed; T-78 execution is required before reference approval.

### 3.6 H-04 — Risk register omissions

- **Original finding:** The risk register omitted airline suspension/cessation, reference data updated after refresh, and historical facts inconsistent with a changed identity. The controls were not explicit.
- **Required remediation:** Add risks and controls for lifecycle status/effective dating, reference-version pinning and refresh checks, and historical re-mapping/reconciliation; add corresponding tests.
- **Evidence currently available:** The controls are designed in OD-01B §6 (lifecycle), §7 (version pinning/T-78), and §8 (dimension/refresh consistency); contract §3.4 and the remediation specification §5.3/§5.5/§8.3 address the scenarios. There is no current project risk register containing the three required scenarios. The remediation specification's internal R-09 to R-11 are unrelated risks (G3 status ambiguity, decision fatigue, and pressure to generate data), not the H-04 suspension/post-refresh/historical-inconsistency entries.
- **New verification performed:** Searched the current documentation for R-09, R-10, R-11, suspension, cessation, post-refresh reference change, and historical inconsistency. The design controls appear in design text; the required project risk-register entries do not.
- **Result:** `PARTIALLY CLOSED`.
- **Residual risk:** A reader of the risk register still cannot see the three required scenarios or their owners and acceptance criteria. The design controls are not yet recorded in the register.
- **Evidence reference:** OD-01B §6, §7, §8; contract §3.4; remediation specification §5.3/§5.5/§8.3; proposed entries in Section 12.2.
- **Owner action:** Authorize a controlled risk-register addendum/update containing R-09 to R-11; accept the residual risk or require a different control; re-audit after the update.
- **Independent-review question:** A documentation update can close the omission, but it does not create independent assurance. H-04 remains a signature blocker until the update is authorized and the re-audit records closure.

### 3.7 H-05 — G3 status contradiction

- **Original finding:** The ledger marked G3 `NOT STARTED` while the same row described a substantial design contract. The meaning of the gate status was ambiguous.
- **Required remediation:** Define the gate status vocabulary and either mark G3 `IN PROGRESS` with approvals pending or rename the state to `NOT FORMALLY APPROVED`; add entry/exit criteria.
- **Evidence currently available:** `PROGRESS_LEDGER.md` line 4 defines gate status vocabulary; contract §13 contains gate rules; the ledger row still says G3 `NOT STARTED` with contract-design evidence. No controlled status correction has been made.
- **New verification performed:** Read the ledger row and the contract gate rule; checked whether any later record changed the G3 status. None has.
- **Result:** `PARTIALLY CLOSED`.
- **Residual risk:** The contradiction remains. A reader can still interpret `NOT STARTED` as meaning no design work exists, which is false.
- **Evidence reference:** `PROGRESS_LEDGER.md` line 12; contract §13; resolution OD-R-14; remediation specification §9.
- **Owner action:** Choose and authorize one controlled correction: `G3 — IN PROGRESS` (design drafted, approvals pending) or `G3 — NOT FORMALLY APPROVED` with design evidence visible; or explicitly amend the finding with a documented rationale. Keeping `NOT STARTED` unchanged leaves H-05 open.
- **Independent-review question:** This is a governance reporting correction, not a data test. It requires owner authorization; no independent reviewer is needed to change a label, but the overall re-audit condition still applies.

### 3.8 H-06 — Reference-version and manifest integrity test

- **Original finding:** No test verified that the airline reference version in the generation manifest, curated dimension, and Power BI refresh configuration was identical.
- **Required remediation:** Add T-78 or extend T-77; verify one version per refresh; record evidence in `qa/results/airline_identity_versions.csv`.
- **Evidence currently available:** OD-01B §2.10 and §7 define `ReferenceVersion`, manifest authority, key-map storage, and T-78-01 to T-78-10; contract §3.4, §7, and §13 align; traceability REQ-028 records T-78.
- **New verification performed:** Read the current T-78 definition and manifest requirements; confirmed the test is defined, not executed.
- **Result:** `CLOSED — document-level`.
- **Residual risk:** T-78 has not run; no manifest exists; the refresh parameter does not exist.
- **Evidence reference:** OD-01B §2.10, §7; contract §3.4, §7, §13; `REQUIREMENTS_TRACEABILITY.md` REQ-028.
- **Owner action:** Approve the design, then execute T-78 in the future `G3-RV-01` process.
- **Independent-review question:** No independent assurance is claimed; T-78 evidence is required before reference approval.

### 3.9 H-07 — Mutable IATA code as the business key

- **Original finding:** `AirlineIATACode` was the primary business key and provenance link, with no stable airline identifier.
- **Required remediation:** Introduce a stable `AirlineId` or permanent `AirlineKey` as identity/provenance link; define reference keys with version; keep IATA/ICAO as attributes; update tests.
- **Evidence currently available:** OD-01B §2.2 and §2.3 define durable `AirlineId` and permanent `AirlineKey`; §3 defines the `AIR-0001` format and 1–10 mapping; §4/§5 make IATA/ICAO version-qualified attributes; contract §3.4 aligns; T-73/T-74/T-75/T-77 are planned.
- **New verification performed:** Read the identity, key, and provenance sections; checked that `ref_airline_sources.csv` joins on `AirlineId`, not IATA; confirmed the code uniqueness rules are version-qualified.
- **Result:** `CLOSED — document-level`.
- **Residual risk:** No source records exist; T-73/T-74/T-75 are not executed; source verification can still reveal code conflicts.
- **Evidence reference:** OD-01B §2.2, §2.3, §3, §4, §5; contract §3.4; T-73 to T-77.
- **Owner action:** No new decision for the identity model; execute source verification and tests later.
- **Independent-review question:** No independent review is claimed; the static design is consistent, but data evidence is absent.

### 3.10 M-07 — Approval workflow and reference-version approval criteria

- **Original finding:** The owner was the sole approver and no named verifier, review checklist, or reference-version approval criteria existed.
- **Required remediation:** Add a named reviewer/verifier and checklist; define evidence inspection; define a reference-version approval decision with owner and criteria, or document a compensating control.
- **Evidence currently available:** OD-01B §11 documents the independent-reviewer-or-compensating-control requirement and the independent-assurance limitation; owner confirmation §11 documents the control set; contract §3.4/§13 and OD-01B §7 define `G3-RV-01`; no reviewer is assigned and no checklist has been executed.
- **New verification performed:** Read the reviewer sections and approval blocks; searched for reviewer names, acceptance, and a completed checklist; `docs/approvals/` is absent.
- **Result:** `PARTIALLY CLOSED`.
- **Residual risk:** Self-approval remains unverified; the owner could sign without a completed challenge step; `G3-RV-01` criteria exist but are not executed.
- **Evidence reference:** OD-01B §11; owner confirmation §11; contract §13; no reviewer artifact exists.
- **Owner action:** Assign a reviewer or explicitly accept CC-01/CC-02/CC-09; execute the checklist; record the result and residual concerns. The formal procedure permits an owner-accepted compensating control, but it does not permit a false independence claim.
- **Independent-review question:** The procedure permits the compensating-control route in principle. It is not satisfied in fact because no owner acceptance or executed review exists.

### 3.11 M-12 — Approval scope versus schema freeze

- **Original finding:** The approval block approved identity rules in Sections 2–7 while the record excluded a schema freeze, leaving the signature scope ambiguous.
- **Required remediation:** Narrow the approval to the population and identity rules, or state that Section 7 is proposed design acknowledged but not frozen; alternatively split the decision.
- **Evidence currently available:** OD-01B §2 sets a broad identity/reference decision; §12 says the record does not create, populate, approve, or freeze the reference schema/dimension; the approval block says the record is not approved for schema freeze. The approval block still lacks an explicit narrow scope sentence.
- **New verification performed:** Read the decision statement, exclusions, and approval block; checked whether the block names the approved sections and excludes a schema freeze explicitly. It does not name a narrow scope.
- **Result:** `PARTIALLY CLOSED`.
- **Residual risk:** A future reader could treat the signature as schema approval, or could treat the identity rules as unapproved design. The ambiguity remains in the signature block.
- **Evidence reference:** OD-01B §2, §12, §11; audit finding M-12.
- **Owner action:** Adopt the B-04 scope statement: approve the governing identity/reference decision rules; expressly state that §5/§7 schemas are design baselines, not a schema freeze; authorize the edit.
- **Independent-review question:** This is an owner-authorized approval-scope clarification. No independent reviewer is required for the wording, but the overall re-audit condition still applies.

### 3.12 Re-audit conclusion

Five HIGH findings are closed at the document level: H-01, H-02, H-03, H-06, and H-07. Two HIGH findings, H-04 and H-05, are only partially closed. M-07 and M-12 are only partially closed.

The audit’s condition that all HIGH findings and M-07/M-12 be closed before signature is **not met**. The compensating-control route can support a defensible review, but it cannot erase the open findings, and it cannot substitute for the missing independent assurance. The owner must authorize the proposed controlled changes and decide the H-04/H-05/M-12 issues before signature.

---

## 4. B-03 — Stale scope evidence

### 4.1 Controlled change proposal

| Field | Detail |
|---|---|
| Evidence item | OD-01A §6, E-07; OD-01B §10 relies on the shared E-01 to E-12 evidence index |
| Old reference | `docs/01_PROJECT_SCOPE.md` — `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` — `RECORDED - NOT MODIFIED BY THIS REMEDIATION` |
| Current reference | `docs/01_PROJECT_SCOPE.md` v1.1 — `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` — 6,384 bytes — last updated 2026-11-02 |
| Reason | The scope was corrected after the remediation change record. The old hash matches the preserved pre-correction backup; it does not represent the current governing scope. |
| Proposed revision | Replace E-07 with the current v1.1 reference and a dated verification statement. Do not describe the scope as unmodified by the remediation; describe it as subsequently corrected under a separate controlled change. |
| Proposed classification | `RECORDED — SCOPE V1.1 CURRENT AT REVIEW 2026-11-02` |
| Hash verification | Both the current file and backup were hashed with SHA-256 on 2026-11-02. Current = `9A9E...512C`; backup = `3238...72B9`. |
| Revision history | OD-01A/OD-01B version 0.1 to 0.2; entry: “Refresh E-07 to scope v1.1; no semantic change to the decision; update record hashes.” |
| Authorization | **NOT AUTHORIZED.** No decision record was edited. |

### 4.2 Why a silent edit is prohibited

OD-01A is a formal decision record. Changing its evidence reference changes what the owner would sign. The change must be controlled, dated, versioned, and rehashed. It must not be made as an undocumented cleanup.

---

## 5. B-04 — Proposed signature-ready structure

### 5.1 Existing block gaps

The current OD-01A §7 and OD-01B §11 blocks contain role, name, decision, signature, date, and approval-evidence fields. They do not contain explicit decision options, approval conditions, reviewer result, residual concerns, or signed-copy retention fields. The owner name is pre-filled. The blocks are not fully signature-ready under the requested field set.

### 5.2 Required fields for both records

| Field | Proposed treatment |
|---|---|
| Owner name | Confirm the existing pre-filled name or leave a controlled blank as the owner directs. |
| Owner signature | Blank until the owner signs; no AI or preparer signature. |
| Actual approval date | Blank until signature; actual date only; no backdating. |
| Decision | Explicit options: `APPROVED`, `REJECTED`, `RETURNED FOR REVISION`. |
| Approval conditions | Blank field; conditions must be recorded, not implied. |
| Reviewer route | `Independent reviewer` / `Compensating controls accepted` / `N/A — no reviewer`. |
| Compensating-control acceptance | Owner initials/date and an explicit statement of accepted controls. |
| Reviewer limitation statement | State no independent assurance where no reviewer is assigned. |
| Reviewer result or N/A | `CONCUR`, `CONCUR WITH RESERVATIONS`, `DISSENT`, or `N/A — compensating control accepted`. |
| Residual concerns | Blank field; record unresolved issues and owner acceptance. |
| Evidence references | Re-audit record, scope v1.1 hash, contract hash, signed-copy path. |
| Signed-copy path | Future `docs/approvals/...` path; do not create now. |
| Signed-copy SHA-256 | Blank until the signed copy exists; then actual hash. |
| Retention confirmation | Read-only retention confirmed by owner/records custodian. |

### 5.3 Proposed OD-01A scope statement

> This approval covers the fixed ten-airline population and population-boundary rules in OD-01A Sections 2, 3, and 4 only. It does not approve OD-01B, reference values or CSV creation, schema freeze, data generation, Power BI implementation, G3, or G4. The reviewer route and any compensating-control acceptance are recorded in this block.

### 5.4 Proposed OD-01B scope statement

> This approval covers the governing airline identity, key, provenance, lifecycle, reference-version, manifest, immutable-mapping, and Power BI identity/disclosure rules in OD-01B Sections 2, 4, 5, 6, and 8. Sections 3 and 7 are acknowledged design baselines, not a schema freeze. This approval does not create or populate reference CSVs, approve a schema freeze, authorize data generation, or change G3 or G4.

### 5.5 Proposed blank approval block

The following is a template only. No name, signature, date, decision, or reviewer identity is entered.

```text
Decision: [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION

Owner name: __________________________________________________
Owner signature: _____________________________________________
Actual approval date: ________________________________________

Approval conditions:
________________________________________________________________
________________________________________________________________

Reviewer route:
[ ] Independent reviewer   [ ] Compensating controls accepted   [ ] N/A

Compensating-control acceptance (if applicable):
I accept the documented controls and residual limitation in
OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md.
Owner initials/date: _________________________________________

Reviewer name/role/organization: ______________________________
Reviewer independence: [ ] Independent  [ ] Not independent — limitation accepted
Reviewer result: [ ] CONCUR [ ] CONCUR WITH RESERVATIONS [ ] DISSENT [ ] N/A
Reviewer signature/date: _____________________________________

Residual concerns:
________________________________________________________________

Evidence references:
- Re-audit record: ____________________________________________
- Scope v1.1 SHA-256: _________________________________________
- Contract v1.5 SHA-256: ______________________________________
- Signed-copy path: ___________________________________________
- Signed-copy SHA-256: ________________________________________
- Retention confirmed: [ ] Yes   [ ] No
```

No decision record has been modified. The owner must authorize the proposed edit.

---

## 6. B-05 — Historical owner confirmation

### 6.1 Proposed controlled addendum

Do not overwrite or rewrite `OD01_OWNER_DECISION_CONFIRMATION.md`. The original remains intact at hash `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`.

Proposed addendum text:

> **Controlled addendum to OD-01 Owner Decision Confirmation**
>
> **Status:** PROPOSED — NOT SIGNED — NOT AN APPROVAL
>
> 1. The eight owner-confirmed choices in the original confirmation remain valid.
> 2. The current governing contract is `03_DATA_CONTRACTS.md` version 1.5, hash `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9`.
> 3. `OD01A_AIRLINE_POPULATION_DECISION.md` and `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` have been prepared as version 0.1 records, prepared 2026-11-01.
> 4. Historical statements in the original confirmation’s document-control table, section 7.1, and section 9.1 are superseded by later dated evidence, including the contract v1.5 and the prepared decision records.
> 5. Nothing in this addendum signs, approves, freezes, or authorizes OD-01A, OD-01B, reference data, schema freeze, data generation, G3, or G4.
>
> Original record preserved: `OD01_OWNER_DECISION_CONFIRMATION.md`, SHA-256 `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`.
>
> Owner acceptance: [BLANK — owner decision required]

### 6.2 Effect

The addendum is a separate controlled artifact. It does not change the original hash and does not imply approval. It prevents the original historical status statements from being mistaken for current facts.

---

## 7. B-06 — `BusinessModelClass` population mechanism

### 7.1 Exact decision required

Choose one:

- **Option A — conservative baseline:** all `BusinessModelClass` values remain null for the baseline; the column remains optional and nullable in `DimAirline`; it is not populated from `ref_airlines.csv`.
- **Option B — documented analytical mapping:** approve a written rubric, allowed values, mapping owner, versioning, and examples; populate the column from that mapping, not from source identity verification.

### 7.2 Assessment

| Field | Detail |
|---|---|
| Recommended option | **Option A — leave all values null.** It avoids unsupported classification, avoids false precision, and does not block the identity decision. |
| Technical consequence | `BusinessModelClass` remains an optional analytical column; reports must not imply source-verified business-model identity. If the column is populated later, a documented mapping and version are required. |
| Existing evidence | OD-01B §2.6/§4/§5 correctly treats it as optional analytical data with no identity provenance and excludes it from identity reference provenance. No mapping/rubric exists. |
| Blocks OD-01A signature? | **No.** |
| Blocks OD-01B signature? | **No**, if the owner accepts the null baseline; the decision record already defines the column as optional. |
| Blocks schema freeze? | **Yes if populated without a rubric.** A null baseline can proceed; a populated column needs an approved mapping before schema freeze. |
| Blocks `G3-RV-01`? | **No.** `G3-RV-01` concerns airline identity/provenance, not this analytical classification. |
| Blocks G4? | **No**, if null and documented. |
| Owner approval status | **PENDING — `OWNER DECISION REQUIRED`.** |

No value has been populated. No mapping has been invented.

---

## 8. B-07 — Source staleness and `ManifestHash` canonicalization

### 8.1 Proposed source-staleness thresholds

No threshold below has owner approval. They are proposals for owner decision.

| Attribute group | Maximum age at reference approval | Anchor | Stale action |
|---|---:|---|---|
| `AirlineName`, `LegalName`, `AirlineGroup`, `HomeCountry` | 365 days | `SourceVerifiedDate` to reference approval date | Re-verify; if not re-verified, null the optional value or reject the required value; quarantine the stale source. |
| `AirlineIATACode`, `AirlineICAOCode` | 180 days | `SourceVerifiedDate` to reference approval date | Re-verify; no stale code may remain authoritative; code changes require a new reference version. |
| Any source with an unavailable URL | Checked at retrieval and re-verification | `SourceRetrievedDate` / verification date | Use an archived copy with a matching content hash; otherwise quarantine and do not load. |

**Exception handling proposal:**

- An exception must be written, attribute-specific, and time-bound (maximum 90 days).
- It must state the reason, the evidence inspected, the residual risk, and the compensating evidence.
- It must be recorded in the manifest and the `G3-RV-01` record and disclosed as a residual risk.
- An exception is not permitted for a `CONFLICTING` or `UNVERIFIED` source, or for an attribute with no durable evidence.
- A stale required attribute with no approved exception cannot support an approved reference version.
- `SourceRetrievedDate` must not be later than `SourceVerifiedDate`; neither may be later than the approval date.

These thresholds are measurable but **not owner-approved**. They block `G3-RV-01` until decided, not OD-01A/B signature.

### 8.2 Proposed deterministic `ManifestHash` method

No manifest exists; this is a specification only.

**Definition:** `ManifestHash` is the uppercase hexadecimal SHA-256 digest of a canonical UTF-8 JSON object containing exactly:

- `reference_version` — the `AIR-YYYY-MM-DD-NNN` identifier;
- `files` — an array in fixed order for `ref_airlines.csv` and `ref_airline_sources.csv`;
- for each file: `name`, `bytes`, and `sha256` of the raw file bytes as stored.

**Canonicalization:**

- UTF-8 without BOM; LF line endings; no trailing whitespace.
- JSON object keys sorted lexicographically; no insignificant whitespace; integer byte sizes; lowercase or uppercase SHA-256 consistently chosen (specify uppercase).
- The raw CSV file bytes are hashed exactly as stored; the build procedure must produce deterministic row and column order.
- Excluded from the hash: the manifest row itself, `ManifestHash`, `Status`, `ApprovedBy`, `ApprovalDate`, `IsCurrent`, `SupersedesReferenceVersion`, and notes. These are approval/workflow metadata and would create circularity or unstable hashes.
- File names are fixed; a renamed or additional file is a new reference version and requires an updated method.

Example shape (placeholders are not real hashes):

```json
{"files":[{"bytes":0,"name":"ref_airlines.csv","sha256":"<64-hex>"},{"bytes":0,"name":"ref_airline_sources.csv","sha256":"<64-hex>"}],"reference_version":"AIR-YYYY-MM-DD-NNN"}
```

`ManifestHash = SHA-256(canonical JSON bytes)`. T-78 must recompute and compare; a mismatch fails closed. `G3-RV-01` records the method and the resulting hash.

This method is proposed, not implemented. It blocks `G3-RV-01` until accepted.

---

## 9. B-08 — Evidence retention proposal

### 9.1 Proposed structure

The following directories are proposed. **They have not been created.**

```text
docs/approvals/
  OD01A/
    approval_record.md
    signed_copy.pdf
    evidence_index.md
    sha256.txt
  OD01B/
    approval_record.md
    signed_copy.pdf
    evidence_index.md
    sha256.txt
  evidence/
    scope/
    audit/
    reaudit/
    reviewer/
    source-verification/
  hash_register/
    decision_hash_register.csv
    verification_log.csv
```

### 9.2 Read-only retention procedure

1. Sign the decision record once; do not edit the signed copy.
2. Produce a read-only copy in the appropriate `docs/approvals/OD01A` or `OD01B` folder.
3. Record the path, byte size, SHA-256, record version, signer, and signature date in `decision_hash_register.csv`.
4. Restrict write access to the owner or designated records custodian; set the signed copy read-only.
5. Corrections after signature require a new version and a new signed copy; never overwrite the prior signed copy.
6. Retain the signed copy, evidence index, and hash register for the project retention period defined by the owner.
7. Do not use Git for the signed copy until explicitly authorized.

### 9.3 Hash-verification procedure

- Recompute each stored artifact with `Get-FileHash -Algorithm SHA256`.
- Compare to the register and the value recorded in the approval block.
- Record the verification date, operator, path, expected hash, actual hash, and result in `verification_log.csv`.
- A mismatch stops use of the artifact; quarantine it and investigate before any further approval action.
- Verification is an integrity check, not independent assurance.

### 9.4 Status

`PROPOSED — NOT IMPLEMENTED`. No approval file, signed copy, or hash register has been created. B-08 is a signature-condition item, not a reason to reopen the eight choices.

---

## 10. Proposed controlled changes and authorization

### 10.1 Change list

| Change ID | Proposed change | Affected record | Authorization status |
|---|---|---|---|
| `CH-01` | OD-01A v0.2: refresh E-07 to scope v1.1; add reviewer/control statement; add signature-ready fields; add re-audit precondition; add revision history; update hash. | OD-01A | **NOT AUTHORIZED** |
| `CH-02` | OD-01B v0.2: refresh shared E-07; add approval-scope statement; add signature-ready fields; add re-audit precondition; add `BusinessModelClass` null-baseline note or deferral; update hash. | OD-01B | **NOT AUTHORIZED** |
| `CH-03` | Create a separate controlled addendum to the owner confirmation using the B-05 text; original remains intact. | New addendum file | **NOT AUTHORIZED** |
| `CH-04` | Add R-09 to R-11 to the risk register or a controlled risk-register addendum; close H-04. | Risk register/addendum | **NOT AUTHORIZED** |
| `CH-05` | Correct G3 status/label per H-05: `IN PROGRESS` or `NOT FORMALLY APPROVED`; do not call it approved. | Progress ledger | **NOT AUTHORIZED** |
| `CH-06` | Create the evidence-retention structure and hash register at signature time. | `docs/approvals/` | **NOT AUTHORIZED** |
| `CH-07` | Adopt the staleness thresholds and `ManifestHash` method in a future controlled contract/design change. | Contract/design record | **NOT AUTHORIZED** |
| `CH-08` | Execute formal OD-01A and OD-01B signatures after all conditions are met. | OD-01A/OD-01B | **NOT AUTHORIZED** |
| `CH-09` | Prepare and execute `G3-RV-01` and reference data after signatures and separate authorization. | Future gate/reference artifacts | **NOT AUTHORIZED** |

### 10.2 Required authorization sequence

1. Owner reviews this proposal and either accepts, rejects, or returns it for revision.
2. Owner explicitly accepts the compensating controls and residual limitations, or assigns a reviewer.
3. Owner authorizes CH-01 through CH-05, CH-07, and CH-08 as applicable.
4. The controlled edits are applied and rehashed; no silent edits.
5. Owner completes CC-01; the re-audit closes H-04, H-05, M-07, and M-12.
6. Owner signs OD-01A first, then OD-01B; actual dates and conditions are recorded.
7. Signed copies are retained under B-08; hashes are verified.
8. A separate controlled update records the decision and G3 status; G3 is not approved.
9. Reference-data preparation and `G3-RV-01` require a separate written authorization.

No step above has been executed beyond the document-level analysis in this proposal.

---

## 11. Verification method and actual results

### 11.1 Method

The following read-only checks were used:

- `Get-FileHash -LiteralPath <path> -Algorithm SHA256` for every controlling document.
- Byte inspection for UTF-8 BOM and CRLF counts.
- `Select-String` searches for `R-09`, `R-10`, `R-11`, `G3`, `reviewer`, `compensating`, `OD-23`, `REQ-028`, and `T-78`.
- Section-level reading of OD-01A, OD-01B, the contract, the scope, traceability, ledger, audit findings, and remediation specification.
- Directory existence and file-count checks for `docs/approvals`, `data/04_reference`, `data/manifests`, `qa/results`, `qa/screenshots`, and `power_bi`.

### 11.2 Actual results

| Check | Method | Actual result |
|---|---|---|
| Current scope hash | `Get-FileHash` | `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` |
| Old scope backup hash | `Get-FileHash` | `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` |
| OD-01A hash | `Get-FileHash` | `399241AD2AE21F4A1FB3D7E589950117F9CDADB8303F78CC161F484CD7255A06` |
| OD-01B hash | `Get-FileHash` | `CDD48B9F0B68CE401D827E5F910076104CCCE73FFBF7BA0A6BC21D75D07C3C05` |
| Contract hash | `Get-FileHash` | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` |
| Encoding/line endings | Byte inspection | All 12 controlling files: UTF-8, no BOM, zero CRLF occurrences. |
| Risk-register entries R-09 to R-11 | `Select-String` | No current project risk-register entries for the three H-04 scenarios. Design controls exist; the specification's internal R-09 to R-11 are unrelated. |
| G3 status | `Select-String`/ledger read | `G3 — Data design` remains `NOT STARTED`; H-05 contradiction remains. |
| Reviewer assignment | `Select-String`/approval-block read | No named independent reviewer; no owner control acceptance; `docs/approvals/` absent. |
| Approval scope | OD-01B read | Broad §2–§8 decision statement; no explicit narrow signature scope; M-12 remains partial. |
| `AirlineId`/`AirlineKey` | OD-01B read | Defined, versioned, stable; no contradiction found. |
| `ReferenceVersion`/manifest | OD-01B/contract read | Defined; T-78 defined but not executed. |
| Reference directory | File count | `data/04_reference/` empty; `data/manifests/` empty. |
| Approval directory | Existence check | `docs/approvals/` absent. |
| QA and Power BI | File count | `qa/results/`, `qa/screenshots/`, and `power_bi/` contain zero files. |
| Git | Not run | No Git command was executed. |

### 11.3 Interpretation

The document-integrity checks passed for the inspected files. That does not mean the governance process passed. The re-audit still has open findings, and the compensating-control route still requires owner acceptance. No `PASS` is claimed for any test, gate, or approval.

---

## 12. Residual-risk register

### 12.1 Register

| ID | Residual risk | Impact | Control / mitigation | Residual status | Owner action |
|---|---|---|---|---|---|
| R-01 | No independent reviewer; self-review limitation | High | CC-01, CC-02, CC-09, CC-10 | Open | Accept limitation or assign reviewer |
| R-02 | H-04 risk-register entries absent | Medium | Proposed R-09 to R-11 | Open | Authorize register update |
| R-03 | H-05 G3 status contradiction | Medium | Proposed status correction | Open | Choose label/status |
| R-04 | M-07 review workflow not executed | Medium | CC-01/CC-02, acceptance | Open | Execute/accept controls |
| R-05 | M-12 approval scope ambiguity | Medium | B-04 scope statement | Open | Authorize record edit |
| R-06 | E-07 stale scope evidence | High | B-03 correction | Open until corrected | Authorize CH-01/CH-02 |
| R-07 | No source verification/reference data | High | `G3-RV-01` future process | Open | Authorize after signature |
| R-08 | `BusinessModelClass` mapping undefined | Low–medium | Null baseline or rubric | Open | Choose Option A/B |
| R-09 | `ManifestHash` method not adopted | Medium | B-07 method | Open | Approve method |
| R-10 | Staleness thresholds not approved | Medium | B-07 thresholds | Open | Approve/replace |
| R-11 | Signed-copy retention not instantiated | Medium | B-08 structure | Open | Authorize at signature |
| R-12 | Owner confirmation historical statements | Low–medium | B-05 addendum | Open | Approve addendum |
| R-13 | T-78/T-79 not executed | High for G3/G4 | Future evidence | Open | Do not claim PASS |
| R-14 | AI preparer is not independent | High | CC-09 limitation | Accepted only if owner says so | Explicit acceptance |

### 12.2 Proposed risk-register entries for H-04

These are proposed entries for a future controlled risk-register update. They are not yet incorporated.

| Risk ID | Scenario | Control | Test / evidence |
|---|---|---|---|
| `R-09` | Airline suspended or ceases operations | `IsActive` and `StatusEffectiveDate`; Tier 3 scope change; new reference version; prior status retained in immutable snapshots | T-78; reference manifest; change-control note |
| `R-10` | Reference dataset updated after model refresh | One approved `ReferenceVersion`; T-78 manifest/dimension/refresh match; fail closed on mismatch | T-78-01 to T-78-10; refresh configuration evidence |
| `R-11` | Historical facts inconsistent with changed identity | Permanent `AirlineKey`; no re-keying; immutable snapshots; reconciliation note | T-78-09/10; historical reconciliation evidence |

No residual risk is accepted until the owner records acceptance.

---

## 13. Remaining owner decisions

| Decision ID | Decision required | Recommendation | Blocks |
|---|---|---|---|
| `D-01` | Accept compensating-control route and the specific controls in Section 2 | Accept with the limitations stated; retain CC-10 as a future independent review | Signature, approval credibility |
| `D-02` | Assign independent reviewer or confirm none is available | If unavailable, explicitly accept CC-09 limitation | Signature |
| `D-03` | Authorize CH-01/CH-02 corrections to OD-01A/OD-01B | Authorize; no silent edits | Signature |
| `D-04` | Approve B-05 addendum or explicit reliance statement | Approve addendum; preserve original | Evidence chain |
| `D-05` | Choose `BusinessModelClass` Option A (null) or Option B (mapping) | Option A — null baseline | Schema freeze if populated |
| `D-06` | Approve/replace staleness thresholds and exception policy | Approve 365/180-day proposal with 90-day exception cap | `G3-RV-01` |
| `D-07` | Approve `ManifestHash` canonicalization | Approve the canonical JSON method | `G3-RV-01` |
| `D-08` | Approve evidence-retention structure and read-only policy | Approve B-08; implement at signature | Signature retention |
| `D-09` | Authorize H-04 risk-register update | Approve R-09 to R-11 | H-04 closure |
| `D-10` | Authorize H-05 G3 status/label correction | Choose `IN PROGRESS` or `NOT FORMALLY APPROVED` | H-05 closure |
| `D-11` | Sign OD-01A, then OD-01B, after conditions close | Sign separately with actual dates/conditions | Formal approval |
| `D-12` | Authorize `G3-RV-01`/reference work after signature | Separate written authorization; no data now | G3/G4 |

All decisions remain **PENDING**. No owner approval has been recorded.

---

## 14. Status and stop condition

- OD-01A: `NOT READY` for formal signature; ready for owner review with the conditions above.
- OD-01B: `NOT READY` for formal signature; ready for owner review with the conditions above.
- H-01, H-02, H-03, H-06, H-07: `CLOSED — document-level`; no independent assurance.
- H-04, H-05, M-07, M-12: `PARTIALLY CLOSED`; signature blockers remain.
- G3: `NOT STARTED`.
- G4: `BLOCKED`.
- `G3-RV-01`: `NOT EXECUTED`.

**Stop condition:** Stop after this proposal. No signatures, approvals, reference CSVs, synthetic datasets, production Python, Power Query, Power BI artifacts, schema freeze, G3/G4 advancement, or Git operations. The owner must review this proposal and explicitly authorize the next controlled change.
