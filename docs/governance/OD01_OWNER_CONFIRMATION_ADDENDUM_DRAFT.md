# AEROVISION 360 — OD-01 Owner-Confirmation Addendum

**Document ID:** OD01-OWNER-CONFIRMATION-ADDENDUM-2026-11-06  
**Document Type:** Controlled addendum — draft for owner review  
**Status:** PROPOSED — OWNER REVIEW REQUIRED  
**Prepared:** 2026-11-06  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Purpose and Scope

This addendum records and clarifies the eight owner-confirmed choices originally documented in `docs/OD01_OWNER_DECISION_CONFIRMATION.md` (version 0.1, dated 2026-11-01). It addresses a version-reference inconsistency identified during the OD-01A/OD-01B pre-signature readiness audit: the original confirmation document references `docs/03_DATA_CONTRACTS.md` version 1.4, while the current contract documentation is version 1.5.

This addendum does **not** create new owner decisions. It does **not** approve contract v1.5. It does **not** authorize schema freeze, data generation, G3, G4, Power BI implementation, or reference-data creation. It is a clarification document only.

---

## 2. Relationship to the Original Confirmation

The original confirmation record (`docs/OD01_OWNER_DECISION_CONFIRMATION.md`, version 0.1, dated 2026-11-01) remains unchanged. This addendum does not modify, replace, or supersede that document. It supplements it with the following clarifications:

1. The eight owner-confirmed choices in Section 4 of this addendum are identical to those in the original confirmation.
2. The original confirmation retains its recorded reference to contract v1.4. Contract v1.5 is the current working draft reviewed for contextual clarification only. This addendum neither replaces the original contract reference nor approves contract v1.5.
3. All other statements, exclusions, and boundaries in the original confirmation remain in effect.

---

## 3. Contract-Version Clarification

| Document | Version | Status |
|---|---|---|
| `docs/03_DATA_CONTRACTS.md` | 1.4 | Referenced in the original confirmation as the governing contract at the time of confirmation. |
| `docs/03_DATA_CONTRACTS.md` | 1.5 | Current working draft. Status: `DRAFT - CONTROLLED OD-01 REMEDIATION COMPLETE; PENDING REVIEW AND FORMAL APPROVAL`. |

This addendum confirms the eight owner choices against the substance of the decision, not against a specific contract version number. Contract v1.5 contains the same governing principles as v1.4 with respect to the eight confirmed choices, plus additional detail added through the OD-01 remediation change record (`OD01_REMEDIATION_CHANGE_RECORD.md`). This addendum does **not** approve contract v1.5. Formal approval of contract v1.5 remains a separate governance decision.

---

## 4. Eight Owner-Confirmed Decisions

The following eight choices were confirmed by the project owner in the ChatGPT conversation on 2026-11-01 and are recorded in `docs/OD01_OWNER_DECISION_CONFIRMATION.md` section 4. Each is reproduced here exactly as confirmed.

### 4.1 OC-01 — Split OD-01 into OD-01A and OD-01B

**Confirmed choice:** Split OD-01 into **OD-01A — Population approval** and **OD-01B — Identity and reference rules**, with one shared evidence index.

**Resolution reference:** OD-R-01  
**Status:** OWNER-CONFIRMED  
**Rationale:** The ten-airline population is independently defensible; the identity, key, provenance, history and reference-version rules are the contested part. A single broad approval would force the owner to sign unresolved rules or delay the population.

### 4.2 OC-02 — Type 1 with Immutable Reference Snapshots

**Confirmed choice:** Use Type 1 `DimAirline` with immutable reference snapshots. Explicitly document that this provides **build reproducibility** but **not as-was historical identity labels**. Defer Type 2.

**Resolution reference:** OD-R-03  
**Status:** OWNER-CONFIRMED  
**Rationale:** The project has a fixed ten-airline roster and a fixed 12-month period. Type 1 avoids `AirlineVersionKey`, bridge tables, effective-dated facts and as-of logic that the portfolio does not need.

### 4.3 OC-03 — Minimal Lifecycle

**Confirmed choice:** Use `IsActive` and `StatusEffectiveDate`. Defer `LifecycleStatus` and `MergedIntoAirlineId`.

**Resolution reference:** OD-R-09  
**Status:** OWNER-CONFIRMED  
**Rationale:** H-04 requires an operating-status flag and effective dating, not a full master-data lifecycle state machine. The fixed roster has ten active airlines for the baseline period.

### 4.4 OC-04 — Reject OD-23; Retain REQ-028 and T-78; Use G3-RV-01

**Confirmed choice:** Reject OD-23 as proposed. Retain **REQ-028** and **T-78**. Use **`G3-RV-01`** as the recurring reference-version approval artifact.

**Resolution reference:** OD-R-10  
**Status:** OWNER-CONFIRMED  
**Rationale:** OD-23 duplicates a recurring operational approval in the OD-series decision register. A reference-version approval is a gate control, not a new architecture decision. T-78 is still required because T-77 checks reference-to-dimension reconciliation, not reference/manifest/dimension/refresh integrity.

### 4.5 OC-05 — Reviewer Controls

**Confirmed choice:** Use a named reviewer where available. Otherwise document the self-review limitation and compensating controls. Never claim independent assurance without independent review.

**Resolution reference:** OD-R-15  
**Status:** OWNER-CONFIRMED  
**Rationale:** A one-person project cannot manufacture independence. A transparent compensating control is more defensible than an unnamed “verified” claim.

### 4.6 OC-06 — Optional LegalName in the Reference Layer

**Confirmed choice:** Keep optional `LegalName` in the reference/provenance layer. Do not add it to `DimAirline`.

**Resolution reference:** OD-R-18  
**Status:** OWNER-CONFIRMED  
**Rationale:** `AirlineName` is the commercial brand used for display and comparison. A legal name is useful evidence but is not an analytical dimension attribute. Keeping it out of `DimAirline` avoids an unused column and an extra provenance obligation in the star schema.

### 4.7 OC-07 — BusinessModelClass as an Analytical Classification

**Confirmed choice:** Retain `BusinessModelClass` as an optional, nullable analytical classification. Do not treat it as a source-verified identity attribute.

**Resolution reference:** OD-R-08  
**Status:** OWNER-CONFIRMED  
**Rationale:** Business model is an analyst taxonomy, not a civil-aviation registry fact. A labelled analytical attribute supports comparison without false precision.

### 4.8 OC-08 — Remove OperatingRegion from Identity

**Confirmed choice:** Remove `OperatingRegion` from `DimAirline` identity attributes. Derive analytical region from route/airport geography where required.

**Resolution reference:** OD-R-07  
**Status:** OWNER-CONFIRMED  
**Rationale:** Region is not a single source-verifiable identity fact for a global airline. Storing it invites arbitrary labels and conflicts. Route and airport geography provide a deterministic analytical alternative.

---

## 5. Explicit Exclusions

This addendum does **not**:

- Approve contract v1.5 or any later contract version.
- Approve OD-01A or OD-01B formal signatures.
- Authorize schema freeze.
- Authorize reference-data creation or population (no `ref_airlines.csv`, `ref_airline_sources.csv`, or reference manifest).
- Authorize synthetic data generation.
- Authorize production ETL, Python pipeline, Power Query, semantic model, DAX measures, Power BI reports, or dashboards.
- Authorize G3 or G4 gate execution.
- Authorize `G3-RV-01` execution.
- Approve any reference version.
- Modify `docs/03_DATA_CONTRACTS.md` or any other controlled document.
- Modify `docs/OD01_OWNER_DECISION_CONFIRMATION.md`.
- Perform any Git operation (commit, tag, branch, worktree).
- Insert a signature, approval date, or approval evidence.
- Claim independent assurance, external verification, or certification.

---

## 6. Approval Requirements

This addendum requires **owner review and confirmation** of the following:

1. Confirmation that the eight owner-confirmed choices in Section 4 accurately reflect the owner’s intent as expressed in the ChatGPT conversation on 2026-11-01.
2. Confirmation that contract v1.5 is **not** formally approved by this addendum and remains a draft pending formal review.
3. Confirmation that no schema freeze, reference-data creation, synthetic-data generation, G3, G4, or Power BI implementation is authorized by this addendum.

---

## 7. Owner Signature and Date — Executed

| Field | Entry |
|---|---|
| Decision owner / approver | KH Mohammad Farhan |
| Role | Project owner |
| Decision scope | The eight owner-confirmed choices in Section 4 |
| Confirmation source | ChatGPT conversation, 2026-11-01 |
| Signature | <u>Farhan</u> — Typed signature representation (not handwritten, not cryptographic) |
| Signature date | 08 November 2026 |
| Formal approval status | EXECUTED |
| Approval evidence reference | Owner authorization directive dated 08 November 2026; typed signature representation: underlined Farhan |
| Signed copy location | `docs/governance/OD01_OWNER_CONFIRMATION_ADDENDUM_DRAFT.md` §7 |

**Executed by Project Owner on 08 November 2026.** Typed signature representation: underlined Farhan. Not a handwritten or cryptographic signature.

---

## 8. Document Version and Traceability

| Field | Value |
|---|---|
| Document ID | `OD01-OWNER-CONFIRMATION-ADDENDUM-2026-11-06` |
| Document type | Owner-confirmation addendum — draft for owner review |
| Document status | **PROPOSED — OWNER REVIEW REQUIRED** |
| Prepared | 2026-11-06 |
| Prepared by | Enterprise Data Governance Architect (non-independent) |
| Project owner | KH Mohammad Farhan |
| Original confirmation | `docs/OD01_OWNER_DECISION_CONFIRMATION.md`, version 0.1, dated 2026-11-01 |
| Original confirmation SHA-256 | `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD` |
| Source resolution SHA-256 | `BE62CBDC017073F6D9135D7DEEF3993F64D74D881102A5C867134C889E20A220` |
| Governing contract (original) | `docs/03_DATA_CONTRACTS.md` version 1.4 |
| Governing contract (current draft) | `docs/03_DATA_CONTRACTS.md` version 1.5 — DRAFT, NOT FORMALLY APPROVED |
| Related decisions | OD-01A, OD-01B |
| Related records | `OD01_REMEDIATION_CHANGE_RECORD.md`, `OD01_OWNER_DECISION_RESOLUTION.md`, `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` |

---

## 9. Remaining Owner Decisions

The following owner decisions remain pending and are **not** approved by this addendum:

| ID | Decision | Status |
|---|---|---|
| GOV-D-04 | Owner-confirmation addendum approval | PENDING — this document is the draft |
| OD-01A | Airline population formal approval | PENDING |
| OD-01B | Airline identity/reference formal approval | PENDING |
| OD-04a | Currency scope | PENDING |
| OD-04b | Exchange-rate convention | PENDING |
| OD-04c | Rate source | PENDING |
| OD-04d | Rate version | PENDING |
| OD-04e | Missing-date behaviour | PENDING |
| OD-04f | Rate-generation methodology | PENDING |
| GOV-D-05 | BusinessModelClass baseline | PENDING |
| GOV-D-06 | Staleness thresholds | PENDING |
| GOV-D-07 | ManifestHash canonicalization | PENDING |
| GOV-D-08 | Evidence retention | PENDING |

---

## 10. End of Addendum

This document is a draft for owner review only. No source files, data, DAX measures, Power Query scripts, semantic model files, PBIX files, or project documentation were modified during its creation. No signature, approval date, reviewer identity, or approval evidence has been created.

**Eight choices are OWNER-CONFIRMED. Formal signature, formal approval, OD-01A/OD-01B approval, schema freeze, G3, and G4 remain unchanged.**

---

**End of addendum.**
