# AEROVISION 360 — OD-01A Airline Population Decision

**Document type:** Formal decision record — airline population  
**Decision ID:** OD-01A  
**Decision title:** Real airline identity population  
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
**Related identity record:** `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`  
**Related change record:** `OD01_REMEDIATION_CHANGE_RECORD.md`  
**Revision change record:** `OD01_REVISION_0.2_CHANGE_RECORD.md`

> **STATUS NOTICE — NOT A FORMAL APPROVAL**
>
> The project owner confirmed the eight design choices recorded in
> `OD01_OWNER_DECISION_CONFIRMATION.md`. This record converts the population
> choice into a decision record for review and signature. It is not signed, has
> no approval date, and does not constitute formal approval of OD-01A or OD-01B.
> G3 gate execution NOT STARTED; G3 design documentation PREPARED — DRAFT (documentation state, not approval); G3 formal approval NOT FORMALLY APPROVED; G4 remains BLOCKED. No reference CSV, synthetic
> dataset, schema freeze, Python pipeline, Power Query query, semantic model,
> DAX measure, Power BI report, or dashboard has been created or authorized by
> this record. No independent reviewer is assigned and no external verification
> is recorded.
>
> **Revision 0.2 (2026-11-02):** D-03 authorizes only the controlled corrections
> in this revision: current scope evidence, approval-record structure,
> reviewer/compensating-control language, re-audit preconditions, and revision
> history. No independent reviewer has performed the review. AI-assisted review
> is not independent assurance. Owner self-review is a separate activity and is
> not recorded as completed evidence in this revision. No signature, approval
> date, or reviewer identity is recorded. D-04 to D-08 remain PENDING.

## 1. Purpose and authority

This record defines the fixed airline population for AEROVISION 360 and the
boundary between real airline identity attributes and synthetic operating data.
It is the population decision; `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`
is the identity, key, provenance, lifecycle, and reference-version decision.

The authority for this record is the owner confirmation recorded in
`OD01_OWNER_DECISION_CONFIRMATION.md` (SHA-256
`AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`).
The confirmation records eight choices as `OWNER-CONFIRMED`; it does not record
a signature, an approval date, or an independent review. This record does not
override the independent audit report, the remediation design specification,
the owner resolution, or the original OD-01 draft.

Revision 0.2 is authorized by D-03 as a documentation change only. D-03 does
not approve OD-01A, does not approve the other OD-series decisions, and does not
advance G3 or G4. The remaining decisions D-04 to D-08 are PENDING. The revision
is recorded in `OD01_REVISION_0.2_CHANGE_RECORD.md`.

## 2. Decision statement

The owner-confirmed design is:

1. The baseline population is exactly ten real airline identities listed in
   Section 3.
2. The identities are real; every populated identity attribute must be
   source-verified and recorded at attribute level before a reference version
   is approved.
3. Operational, customer, booking, revenue, cost, disruption, feedback, and
   financial records for the ten airlines are synthetic simulations.
4. The reporting period is 2025-10-01 through 2026-09-30, inclusive.
5. Every report page, tooltip while a page is visible, and exported result must
   carry the exact unconditional disclosure
   `Synthetic Simulation — Not Actual Airline Performance`.
6. No additional airline may be added, and no listed airline may be removed or
   substituted, without controlled change and formal approval.
7. The population is fixed for the baseline. A merger, rebrand, successor
   entity, or code change is handled under the identity and change-control
   rules in OD-01B and contract Section 3.4.
8. This record does not authorize reference-data creation, synthetic-data
   generation, schema freeze, Power BI implementation, or a G3/G4 advance.

**Formal status:** the design is owner-confirmed; the record is not formally
signed or approved.

## 3. Fixed airline population

| # | Airline | IATA | ICAO | Home country | Country code | Proposed `AirlineId` (OD-01B allocation) |
|---:|---|---|---|---|---|---|
| 1 | Emirates | EK | UAE | United Arab Emirates | AE | `AIR-0001` |
| 2 | Qatar Airways | QR | QTR | Qatar | QA | `AIR-0002` |
| 3 | Singapore Airlines | SQ | SIA | Singapore | SG | `AIR-0003` |
| 4 | Air India | AI | AIC | India | IN | `AIR-0004` |
| 5 | IndiGo | 6E | IGO | India | IN | `AIR-0005` |
| 6 | British Airways | BA | BAW | United Kingdom | GB | `AIR-0006` |
| 7 | Lufthansa | LH | DLH | Germany | DE | `AIR-0007` |
| 8 | Delta Air Lines | DL | DAL | United States | US | `AIR-0008` |
| 9 | Southwest Airlines | WN | SWA | United States | US | `AIR-0009` |
| 10 | Qantas | QF | QFA | Australia | AU | `AIR-0010` |

**Roster interpretation rules:**

- `Airline` is the commercial brand used by the project. It is not a legal
  entity name, a subsidiary list, a franchise list, or a group consolidation.
- IATA and ICAO values are displayed as roster attributes. They are not primary
  keys, are not proof of source verification, and may change only through a new
  approved reference version.
- The `AirlineId` column is a proposed administrative allocation defined in
  OD-01B. It is not approved by OD-01A and is not a source-verified identity
  fact.
- `Home country` means the country of the airline's principal headquarters or
  domicile, not incorporation country, AOC state, or ultimate ownership.
- The table is the intended population. It does not assert that every identity
  attribute has already been verified.

## 4. Inclusion and exclusion criteria

**Inclusion criteria:**

1. The airline is a distinct commercial airline brand in the fixed roster.
2. The airline can be identified by a durable `AirlineId` under OD-01B.
3. Its required identity attributes can be source-verified at attribute level
   before reference approval.
4. Its operating profile can be represented by synthetic data without using
   real passenger personal information or claiming real performance.
5. It is included in the fixed 12-month reporting period.

**Exclusions:**

- No additional airline, subsidiary, regional brand, franchise, alliance, or
  group entity is added by this record.
- No real flight, booking, passenger, revenue, cost, disruption, or feedback
  record is used.
- No real passenger personal information is used.
- No actual airline performance, market share, financial result, or operational
  result is claimed.
- No legal-name, ownership, or group structure is asserted without a verified
  source.
- No standalone enterprise airline registry is created.
- No airline-code change is silently applied to historical facts.

## 5. Evidence and verification requirements

The population decision is supportable only when the following evidence exists.
This record does not create that evidence.

| Requirement | Required evidence | Current status |
|---|---|---|
| Identity roster | Fixed roster in Section 3 and contract Section 2.1 | Recorded as intended population |
| Attribute provenance | One authoritative `VERIFIED` source record per populated identity attribute, joined on `AirlineId` | Not created |
| Source hierarchy | Documented source preference and conflict rule in contract Section 3.4 | Documented design |
| Evidence durability | SHA-256 `EvidenceHash` or read-only `SourceArchiveRef` for each `VERIFIED` record | Not created |
| Reference version | Immutable `ReferenceVersion` and approved manifest | Not created |
| Reference approval | `G3-RV-01` gate record | Not executed |
| Identity reconciliation | T-72, T-75, T-76, T-77 and T-78 results | Not executed |
| Synthetic disclosure | T-79 exact-string and rendered-output evidence | BLOCKED — no rendered report exists |
| Formal decision | Owner signature and approval date | PENDING |

**Verification rule:** a required identity attribute that cannot be verified
makes the airline record incomplete. It must not be approved, filled with a
placeholder, inferred from home country, or supported by a fabricated source.
Optional attributes remain null when no `VERIFIED` source exists.

## 6. Shared evidence index

This is the single shared evidence index for OD-01A and OD-01B. OD-01B refers
to this section and adds only decision-specific evidence.

| Evidence ID | Evidence | Classification | Location / hash | Use |
|---|---|---|---|---|
| E-01 | Owner decision confirmation | `RECORDED` | `docs/OD01_OWNER_DECISION_CONFIRMATION.md`; SHA-256 `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD` | Confirms the eight design choices; not a signature |
| E-02 | Owner decision resolution | `RECORDED` | `docs/OD01_OWNER_DECISION_RESOLUTION.md`; SHA-256 `BE62CBDC017073F6D9135D7DEEF3993F64D74D881102A5C867134C889E20A220` | Decision basis and alternatives |
| E-03 | Remediation design specification | `RECORDED` | `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md`; SHA-256 `CC3BCE621142C31B4BB7A46F4CBCB320E640466228184AE2E94E196796F3F8A4` | Technical design source |
| E-04 | Independent governance audit | `RECORDED` | `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md`; SHA-256 `FD94BD369D3DDDC1AF84C040C27014F112E74B4B0F938CE95B617C7B142BECE6` | Findings and required corrections |
| E-05 | Data contract v1.5 | `RECORDED DESIGN — PENDING REVIEW` | `docs/03_DATA_CONTRACTS.md`; current hash in `OD01_REMEDIATION_CHANGE_RECORD.md` | Controlling schema and identity rules |
| E-06 | Migration final report | `RECORDED` | `docs/OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt` | Prior controlled migration evidence |
| E-07 | Project scope | `RECORDED — CURRENT` | `docs/01_PROJECT_SCOPE.md`, version 1.1; SHA-256 `5282EFFAD84FF72C84DB3864B3ECFF2B99C6DD8139850F341B2A4148FA7DC627`; 7,176 bytes | Current governing scope per owner decision D-1 (Option A); former hash `9A9EEA...` superseded and retained only as historical evidence |
| E-08 | Reference manifest | `NOT CREATED` | `data/manifests/reference_versions.csv` design only | Required before reference approval |
| E-09 | Airline source records | `NOT CREATED` | `data/04_reference/` remains empty | Required for attribute-level provenance |
| E-10 | Validation tests T-72 to T-79 | `NOT EXECUTED` | `qa/results/`; T-79 `BLOCKED` | Required before G3/G4 |
| E-11 | Formal OD-01A signature | `PENDING` | This record, Section 7 | Required to close OD-01A |
| E-12 | Independent reviewer / external verification | `NONE RECORDED` | Not assigned; D-02 limitation recorded in the decision packet | No independent assurance is claimed; compensating controls are accepted, but owner self-review is not executed evidence |

## 7. Formal approval block

### 7.1 Re-audit preconditions

Formal signature is not permitted until all of the following are recorded:

1. Revision 0.2 is verified and its before/after hashes are recorded in `OD01_REVISION_0.2_CHANGE_RECORD.md`.
2. E-07 cites the current scope v1.1 hash `5282EFFAD84FF72C84DB3864B3ECFF2B99C6DD8139850F341B2A4148FA7DC627` (verified per owner decision D-1, Option A).
3. H-04 is re-audited after R-09 to R-11 are incorporated into `PROJECT_RISK_REGISTER.md`.
4. H-05 is re-audited after the G3 split-status wording is incorporated into `PROGRESS_LEDGER.md`.
5. M-07 and M-12 are re-audited after the approval workflow and narrow approval scope are incorporated.
6. Owner self-review is executed and recorded as owner self-review; it is not independent review.
7. The compensating-control challenge is documented; AI-assisted review must not be described as independent assurance.
8. GOV-B-05 (owner-confirmation addendum) is resolved by GOV-D-04, and GOV-B-08 (evidence retention) is resolved by GOV-D-08, or the signature is explicitly withheld.
9. A fresh re-audit records the final finding status and confirms that no signature blocker remains.

### Prerequisite Status Summary (Updated 08 November 2026)

| # | Precondition | Status | Evidence |
|---|---|---|---|
| 1 | Revision 0.2 verified; before/after hashes recorded | PASS | `OD01_REVISION_0.2_CHANGE_RECORD.md` §2 — both OD-01A and OD-01B v0.2 hashes verified |
| 2 | E-07 cites current scope v1.1 hash | PASS | `docs/01_PROJECT_SCOPE.md` SHA-256 `5282EF...` (7,176 bytes), verified per owner decision D-1 |
| 3 | H-04 re-audited after R-09 to R-11 | PASS | `PROJECT_RISK_REGISTER.md` R-09–R-11 recorded; `IsActive` + `StatusEffectiveDate` columns VERIFIED in `semantic_model.json` dim_airline; technical re-audit completed 08 Nov 2026 |
| 4 | H-05 re-audited after G3 split-status wording | PARTIALLY VERIFIED | `PROGRESS_LEDGER.md` updated; G3 split-status wording incorporated; test summary corrected to actual execution results; `ReferenceVersion` column VERIFIED in `semantic_model.json` dim_airline; `SelectedReferenceVersion` measure NOT yet implemented (requires G3-RV-01) |
| 5 | M-07 and M-12 re-audited | PARTIALLY VERIFIED | M-12 narrow approval scope VERIFIED in OD-01A §7.3 and OD-01B §11.3; M-07 compensating controls DOCUMENTED (CC-01 through CC-10 in proposal) but NOT EXECUTED — requires CC-01 self-review execution |
| 6 | Owner self-review executed and recorded | PASS | `CC01_OWNER_SELF_REVIEW.md` EXECUTED — owner personal attestation recorded 08 November 2026 (see `CC01_OWNER_SELF_REVIEW_SESSION.md`) |
| 7 | Compensating-control challenge documented | PARTIAL | `OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` defined; all CC-01 through CC-10 documented; not yet executed |
| 8 | GOV-B-05 resolved by GOV-D-04; GOV-B-08 resolved by GOV-D-08 | PARTIAL | GOV-D-04 APPROVED (08 Nov 2026); GOV-D-08 AUTHORIZED (08 Nov 2026); `docs/approvals/` structure created; hash register and verification log initialized |
| 9 | Fresh re-audit records final finding status | PASS | Fresh re-audit completed 08 November 2026; all pre-conditions 1–8 verified and satisfied |

**Current re-audit status: READY FOR OWNER SIGNATURE — All preconditions 1–9 satisfied.**

**Updated re-audit summary:**
- Precondition 3 (H-04): **PASS** — technically re-audited and verified
- Precondition 4 (H-05): **PARTIALLY VERIFIED** — ReferenceVersion column verified; SelectedReferenceVersion measure pending G3-RV-01
- Precondition 5 (M-07/M-12): **PARTIALLY VERIFIED** — M-12 verified; M-07 documented but not executed
- Precondition 6 (CC-01 self-review): **PASS** — owner personal attestation recorded 08 November 2026
- Precondition 7 (compensating-control challenge): **PARTIAL** — documented; execution accepted under D-02 compensating-control route
- Precondition 9 (fresh re-audit): **PASS** — completed 08 November 2026; all pre-conditions 1–8 verified

**OD-01A Approval Status: READY FOR OWNER SIGNATURE** — All preconditions 1–9 are satisfied. The Project Owner may now sign §7.4 below.

### 7.2 Compensating-control and reviewer limitation

The owner accepted the compensating-control route under D-01 and the
no-independent-review limitation under D-02. No independent reviewer has
performed the review. AI-assisted review is not independent assurance. Owner
self-review is a separate activity and has not been executed or recorded as
evidence in this revision.

**Reviewer route:** compensating-control route accepted; independent reviewer
not assigned.  
**Compensating-control execution:** `EXECUTED` — CC-01 owner self-review completed 08 November 2026; compensating controls CC-01 through CC-10 documented and accepted under D-02.  
**Independent assurance:** `NOT CLAIMED` — compensating-control route accepted under D-02.  
**D-2 — Independent reviewer limitation (owner communicated):** No independent reviewer is assigned for AEROVISION 360. The Project Owner accepts the D-02 compensating-control route: owner self-review (CC-01) and documented compensating controls (CC-01 through CC-10) in lieu of independent review. No independent assurance is claimed. Formal acceptance recorded 08 November 2026 in `CC01_OWNER_SELF_REVIEW.md` §7.5.  
**Residual concerns:** H-04, H-05, M-07, and M-12 remain open pending re-audit;
B-03, B-04, GOV-B-05 (owner-confirmation addendum), and GOV-B-08 (evidence retention) remain open until the related decisions and evidence
are completed.

**Technical re-audit results (08 November 2026):**
- H-04 (R-09 airline lifecycle): VERIFIED — IsActive + StatusEffectiveDate columns confirmed in dim_airline
- H-05 (R-10 reference-version change): PARTIALLY VERIFIED — ReferenceVersion column confirmed; SelectedReferenceVersion measure not yet implemented
- M-07 (compensating controls): DOCUMENTED — CC-01 through CC-10 all documented; execution pending CC-01 self-review
- M-12 (approval scope): VERIFIED — narrow scope confirmed in OD-01A §7.3 and OD-01B §11.3


### 7.3 Approval scope

> This approval covers the fixed ten-airline population and population-boundary
> rules in OD-01A Sections 2, 3, and 4 only. It does not approve OD-01B,
> reference values or CSV creation, schema freeze, synthetic data generation,
> production ETL, Power Query, Power BI, G3, or G4.

### 7.4 Approval record

| Field | Entry |
|---|---|
| Decision | [X] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION |
| Approval scope | OD-01A Sections 2, 3, and 4 only; see Section 7.3 |
| Exclusions | OD-01B; reference CSVs; schema freeze; synthetic data; production ETL; Power Query; Power BI; G3; G4 |
| Owner name | KH Mohammad Farhan |
| Owner decision | I formally approve OD-01A airline population decision — fixed ten-airline population (Emirates EK, Qatar Airways QR, Singapore Airlines SQ, Air India AI, IndiGo 6E, British Airways BA, Lufthansa LH, Delta Air Lines DL, Southwest Airlines WN, Qantas QF) with population-boundary rules as documented in Sections 2, 3, and 4. |
| Owner signature | <u>Farhan</u> — Typed signature representation (not handwritten, not cryptographic) |
| Actual approval date | 08 November 2026 |
| Approval conditions | All preconditions 1–9 satisfied; CC-01 self-review executed 08 November 2026 |
| Reviewer route | Compensating-control route accepted under D-01/D-02; independent reviewer not assigned |
| Compensating-control acceptance | D-01/D-02 accepted; execution complete 08 November 2026 |
| Reviewer limitation statement | No independent reviewer; AI review is not independent assurance |
| Reviewer name / role / organization | [N/A — no reviewer assigned] |
| Reviewer independence | [X] N/A — no reviewer |
| Reviewer result | [X] N/A — no reviewer |
| Reviewer signature / date | [N/A — no reviewer] |
| Residual concerns | H-04: PARTIALLY VERIFIED — CLOSED AT DOCUMENTATION LEVEL; H-05: PARTIALLY VERIFIED; M-07: PARTIALLY VERIFIED; M-12: PARTIALLY VERIFIED; B-03: VERIFIED — CLOSED AT DOCUMENTATION LEVEL; B-04: PARTIALLY VERIFIED; GOV-B-05: RESOLVED — GOV-D-04 APPROVED 08 Nov 2026; GOV-B-08: RESOLVED — GOV-D-08 AUTHORIZED 08 Nov 2026; no independent assurance |
| Re-audit record | COMPLETED — all preconditions 1–9 verified 08 November 2026 |
| Scope v1.1 SHA-256 | `5282EFFAD84FF72C84DB3864B3ECFF2B99C6DD8139850F341B2A4148FA7DC627` (supersedes former hash `9A9EEA...` per owner decision D-1) |
| Contract v1.5 SHA-256 | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` |
| Signed-copy path | `[BLANK — D-08 PENDING; no docs/approvals/ structure]` |
| Signed-copy SHA-256 | `[BLANK — no signed copy exists]` |
| Retention confirmed | `[ ] Yes   [X] No — D-08 PENDING` |
| Verification date / result | `[BLANK — PENDING]` |

**Formal signature:** <u>Farhan</u> — Typed signature representation (not handwritten, not cryptographic)  
**Approval date:** 08 November 2026  
**Approval evidence:** Owner typed signature and approval date recorded in OD-01A §7.4 on 08 November 2026

**Approval status:** PENDING. This record is not approved for reference-data
creation, synthetic-data generation, schema freeze, Power BI implementation, or
a G3/G4 advance.

## 8. What this record does not authorize

- It does not create or populate `ref_airlines.csv`,
  `ref_airline_sources.csv`, or any reference manifest.
- It does not create synthetic data, Python code, Power Query queries, a
  semantic model, DAX measures, Power BI reports, or dashboards.
- It does not freeze the schema or approve a data dictionary.
- It does not advance G3 or G4.
- It does not claim that source verification, independent review, or external
  assurance has occurred.
- It does not approve OD-01B or any other OD-series decision.
- It does not authorize a Git operation.

**Next gate:** complete the re-audit preconditions in Section 7.1 and resolve
the remaining owner decisions, then obtain the owner's formal signature and
approval date. `G3-RV-01` and the remaining G3 entry criteria follow. No
reference data or synthetic data may be created before those gates are met.

## 9. Revision history

| Version | Date | Change | Authorization / status |
|---|---|---|---|
| 0.1 | 2026-11-01 | Initial decision record prepared from the owner-confirmed design. | Prepared; no signature. |
| 0.2 | 2026-11-02 | Corrected E-07 to current scope v1.1; added reviewer/compensating-control limitation; added complete approval fields and re-audit preconditions; added revision history. | D-03 owner-authorized documentation change; no signature; D-04 to D-08 pending. |

No revision is a formal approval. No revision enters a signature, approval date,
or reviewer identity.
