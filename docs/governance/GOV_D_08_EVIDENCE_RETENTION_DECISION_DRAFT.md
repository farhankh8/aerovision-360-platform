# GOV-D-08 — Evidence Retention Policy Decision

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** GOV-D-08-2026-11-06-001  
**Document Type:** Owner Decision Draft — Evidence Retention Policy Approval  
**Status:** REVISED DRAFT — OWNER REVIEW REQUIRED  
**Prepared:** 2026-11-06  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Decision Purpose

This decision record establishes the evidence-retention structure and procedure required before OD-01A and OD-01B can be signed. It defines where signed decision records, approval evidence, verification records, and hash registers will be stored; how integrity is maintained; who is responsible; and how long records are retained.

This decision record is a **documentation and technical-analysis artifact only**. It does not create the `docs/approvals/` directory, does not create signed documents, does not enter signatures, and does not authorize any implementation.

---

## 2. Existing Problem

| Attribute | Detail |
|---|---|
| Finding ID | A-05 / GOV-D-08 |
| Severity | HIGH (P0 — must resolve before OD-01A/OD-01B signature) |
| Source | `CC01_REMEDIATION_REGISTER_V2.md`, `CC01_REMEDIATION_PRIORITY_MATRIX.md`; `AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md` §7.5 |
| Problem | `docs/approvals/` does not exist. No signed-copy retention structure, no hash register, no verification log, no retention period, no named records custodian. Without this structure, OD-01A and OD-01B approval blocks cannot complete their signed-copy path, hash, or retention fields. |

**Why it blocks:** A signed copy can be altered or lost, and the approval may not be reconstructable. The approval blocks' signed-copy path, SHA-256, and retention fields cannot be completed until GOV-D-08 is approved and the structure exists.

---

## 3. Evidence Inspected

### 3.1 Governance Documents Inspected

| File | Location | Relevance |
|---|---|---|
| OD-01 Remediation Action Register | `docs/governance/OD_01_REMEDIATION_ACTION_REGISTER.md` | Line 32: A-05 / GOV-D-08, HIGH, P0; acceptance criteria: structure exists read-only; signed-copy path/hash recorded; verification log works |
| CC-01 Remediation Register — Revised | `docs/governance/CC01_REMEDIATION_REGISTER_V2.md` | Line 43: A-05 / GOV-D-08, HIGH, P0; same acceptance criteria |
| CC-01 Remediation Priority Matrix | `docs/governance/CC01_REMEDIATION_PRIORITY_MATRIX.md` | Line 35: A-05 / GOV-D-08, HIGH, P0; same acceptance criteria |
| CC-01 Owner Self-Review | `docs/governance/CC01_OWNER_SELF_REVIEW.md` | Line 157-161: `docs/approvals/` does not exist; approve retention structure; create read-only structure; dependency GOV-D-08 |
| CC-01 Owner Self-Review Findings | `docs/governance/CC01_OWNER_SELF_REVIEW_FINDINGS.md` | Lines 93-97: same finding; dependency GOV-D-08 |
| CC-01 Remediation Plan Reconciliation | `docs/governance/CC01_REMEDIATION_PLAN_RECONCILIATION.md` | Lines 90-95: corrected circular dependency — GOV-D-08 approval must come BEFORE OD-01A/B signatures |
| GOV-D-07 Owner Acceptance Record | `docs/governance/GOV_D_07_OWNER_ACCEPTANCE.md` | GOV-D-07 accepted (Option A); does not resolve GOV-D-08 |
| GOV-D-07 ManifestHash Canonicalization Draft | `docs/governance/GOV_D_07_MANIFESTHASH_CANONICALIZATION_DRAFT.md` | RFC 8785 JCS v1.0 accepted for manifest canonicalization; not yet implemented; distinct from ordinary evidence file hashing |
| OD-01 Owner-Confirmation Addendum Acceptance | `docs/governance/OD01_OWNER_CONFIRMATION_ADDENDUM_ACCEPTANCE.md` | Addendum accepted 2026-11-06; does not resolve GOV-D-08 |
| AEROVISION 360 Governance Investigation Report | `docs/AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md` | §7.5: GOV-D-08 PENDING OWNER APPROVAL; `docs/approvals/` does not exist; defines exact question, source, dependencies |
| AEROVISION 360 Owner Decision Worksheet | `docs/AEROVISION_360_OWNER_DECISION_WORKSHEET.md` | §7: GOV-D-08 detailed options, proposed structure, procedure, consequences |
| OD-01A Decision Record | `docs/OD01A_AIRLINE_POPULATION_DECISION.md` | Lines 251-253: signed-copy path and hash blank; retention confirmed No — D-08 PENDING |
| OD-01B Decision Record | `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | Lines 415-417: same blank fields |

### 3.2 Existing Approved Requirements

None for GOV-D-08. The decision is pending owner approval.

### 3.3 Previously Owner-Directed Choices

None specific to GOV-D-08 have been formally owner-directed. The compensating-control proposal §9 defines a proposed structure and read-only procedure but explicitly states it is `PROPOSED — NOT IMPLEMENTED`.

### 3.4 New Recommendations Requiring Owner Approval

All structural and procedural details below are **new recommendations** requiring owner decision:

| Decision Element | Recommended Value | Owner Decision |
|---|---|---|
| Evidence-retention structure path | `docs/approvals/` | [BLANK] |
| Subfolder structure | `docs/approvals/OD01A/`, `docs/approvals/OD01B/`, `docs/approvals/evidence/`, `docs/approvals/hash_register/` | [BLANK] |
| Read-only control for signed copies | Procedural controls plus restricted filesystem permissions; enforced at signature time | [BLANK] |
| Hash algorithm | SHA-256 | [BLANK] |
| Hash register file | `docs/approvals/hash_register/decision_hash_register.csv` | [BLANK] |
| Verification log | Append-only | [BLANK] |
| Records custodian | Project owner initially; documented delegation permitted | [BLANK] |
| Retention period | Proposed: seven years after supersession or withdrawal, subject to applicable legal, contractual and organizational requirements. **This seven-year period is a proposed operational policy, not a verified statutory requirement.** | [BLANK] |
| Git exclusion for signed copies | Signed copies remain outside Git unless separately authorized | [BLANK] |
| Correction procedure | Preserve originals; never overwrite; new version requires new signed copy | [BLANK] |

---

## 4. Proposed Folder Structure

```
docs/approvals/
├── README.md
├── OD01A/
│   ├── approval_record.md
│   ├── signed_copy.md
│   ├── evidence_index.md
│   └── sha256.txt
├── OD01B/
│   ├── approval_record.md
│   ├── signed_copy.md
│   ├── evidence_index.md
│   └── sha256.txt
├── evidence/
│   ├── scope/
│   ├── audit/
│   ├── reaudit/
│   ├── reviewer/
│   └── source-verification/
└── hash_register/
    ├── decision_hash_register.csv
    └── verification_log.csv
```

### Folder Definitions

| Folder | Purpose | Permitted Contents | Modification Restrictions |
|---|---|---|---|
| `docs/approvals/` | Root evidence-retention structure | README.md only at root level | Read-only after owner approval |
| `docs/approvals/OD01A/` | OD-01A signed decision package | `approval_record.md`, `signed_copy.md`, `evidence_index.md`, `sha256.txt` | Read-only after signature deposited |
| `docs/approvals/OD01B/` | OD-01B signed decision package | `approval_record.md`, `signed_copy.md`, `evidence_index.md`, `sha256.txt` | Read-only after signature deposited |
| `docs/approvals/evidence/` | Supporting evidence for decisions | Governance subfolders: scope, audit, reaudit, reviewer, source-verification | Append-only; no silent overwriting |
| `docs/approvals/hash_register/` | Integrity registers | `decision_hash_register.csv`, `verification_log.csv` | Append-only records; corrections add new rows |

### README.md Contents

The root README.md must record:
- Structure version
- Approved retention period
- Named records custodian
- Hash algorithm used (SHA-256)
- Date of owner approval
- Reference to GOV-D-08 decision document

---

## 5. Evidence-Integrity Requirements

### 5.1 Evidence Identifier Attributes

| Attribute | Purpose |
|---|---|
| Evidence identifier | Unique ID for each stored artifact |
| Original filename | Document identity at time of capture |
| Document version | Version of the stored document |
| SHA-256 digest | Integrity hash of the exact stored artifact |
| Hash calculation method | SHA-256 over exact file bytes (ordinary file hashing, not RFC 8785 JCS) |
| Capture or acceptance timestamp | When the artifact was captured or accepted |
| Decision or finding reference | GOV-D-xx or A-xx/B-xx/C-xx/D-xx/E-xx reference |
| Evidence status | ACCEPTED, PENDING, SUPERSEDED, QUARANTINED |
| Verification result | PASS or FAIL with date and operator |
| Supersession history | Chain of superseding versions |
| Access controls | Custodian and write permissions |

### 5.2 Hashing vs. Canonicalization Distinction

| Operation | Applies To | Method | Status |
|---|---|---|---|
| Ordinary evidence file hashing | Signed copies, approval records, evidence documents | SHA-256 over exact file bytes | Specified in GOV-D-08; not yet implemented |
| Canonical JSON manifest hashing | Reference manifest `ManifestHash` field | RFC 8785 JCS v1.0 per GOV-D-07 | Accepted per GOV-D-07; implementation NOT STARTED |
| Evidence verification | Recompute stored artifact hash; compare to register | Recompute SHA-256; compare with register value | Specified in GOV-D-08; not yet implemented |

**Important:** GOV-D-07 (RFC 8785 JCS) is accepted for manifest canonicalization but its implementation is NOT STARTED. GOV-D-08 uses ordinary SHA-256 file hashing for signed copies and evidence documents. These are distinct operations and must not be conflated.

### 5.3 Hash Verification Procedure

1. Recompute SHA-256 over the exact stored artifact bytes.
2. Compare to the value recorded in `decision_hash_register.csv` and in the approval block.
3. Record verification date, operator, path, expected hash, actual hash, and result in `verification_log.csv`.
4. A mismatch stops use of the artifact; quarantine it and investigate before any further approval action.
5. Verification is an integrity check, not independent assurance.

---

## 6. Read-Only Controls

### 6.1 Original Evidence Preservation

- Original evidence files are never silently overwritten or replaced.
- When a document is corrected, a new version is created and the prior version is retained.
- Each version is independently hashed and recorded in the hash register.

### 6.2 Append-Only Verification History

- `verification_log.csv` is append-only. Each verification attempt adds a new row.
- Failed verifications are recorded with result `FAIL` and trigger quarantine.

### 6.3 Superseded Evidence Handling

- Superseded versions retain their original hash and remain accessible.
- New versions receive new evidence identifiers and new hashes.
- Supersession history is recorded in the hash register.

### 6.4 Correction Procedures

- Corrections after signature require a new version and a new signed copy.
- Never overwrite a prior signed copy.
- Both versions remain accessible with their respective hashes.

### 6.5 Duplicate Evidence

- Duplicate evidence is not silently merged. Each instance receives its own evidence identifier and hash entry.

### 6.6 Failed Hash Verification

- A hash mismatch stops use of the artifact.
- The artifact is quarantined with status `QUARANTINED`.
- Investigation must complete before any further approval action uses the artifact.

### 6.7 Backup and Recovery

- Backup procedure and recovery point are owner-defined.
- Backup copies are independently hashed to verify integrity.

### 6.8 Access Permissions

- Write access is restricted to the owner or designated records custodian.
- Read access is available to governance participants.
- Filesystem read-only permissions are recommended but **do not by themselves** provide immutable storage; procedural controls are required.

---

## 7. Retention and Supersession Policy

| Policy Element | Recommended Value | Owner Decision |
|---|---|---|
| Retention period | Proposed: seven years after supersession or withdrawal, subject to applicable legal, contractual and organizational requirements. **This seven-year period is a proposed operational policy, not a verified statutory requirement.** | [BLANK] |
| Records custodian | Project owner initially; documented delegation permitted | [BLANK] |
| Version history | All versions retained for retention period | [BLANK] |
| Superseded evidence | Retained, not deleted | [BLANK] |
| Final disposition | Owner-defined after retention period | [BLANK] |

---

## 8. Access Responsibilities

| Responsibility | Assigned To | Notes |
|---|---|---|
| Records custodian | Project owner initially; documented delegation permitted | Responsible for structure integrity, hash register, verification log |
| Owner | KH Mohammad Farhan | Project Owner; approves decisions and signs records |
| Independent reviewer | Not assigned | `OD01B-B-08` independent reviewer is separate and NOT resolved by GOV-D-08 |
| Governance participants | Read access to evidence | No write access without custodian authorization |

---

## 9. Dependency Resolution (Circular Dependency)

### 9.1 The Circular Dependency

The remediation plan originally listed A-05 / GOV-D-08 with dependency "OD-01A/B signatures", while OD-01A/B cannot be signed until GOV-D-08 is approved. This creates a circular dependency: OD-01A/OD-01B signature requires GOV-D-08, but GOV-D-08 depends on OD-01A/OD-01B signature.

### 9.2 Corrected Dependency Sequence

The `CC01_REMEDIATION_PLAN_RECONCILIATION.md` corrected the dependency: GOV-D-08 approval must come **before** OD-01A/B signatures.

**Corrected sequence:**

1. **Owner approves GOV-D-08** — retention structure, custodian, retention period, hash register, verification log defined.
2. **Owner authorizes creation of `docs/approvals/`** — separate authorization after GOV-D-08 approval.
3. **`docs/approvals/` structure is created** — hash register and verification log initialized.
4. **Owner signs OD-01A** — signed copy deposited in `docs/approvals/OD01A/`; hash recorded; retention confirmed.
5. **Owner signs OD-01B** — signed copy deposited in `docs/approvals/OD01B/`; hash recorded; retention confirmed.
6. **G3-RV-01 execution** — can proceed after OD-01A/OD-01B signatures and retention structure.

**GOV-D-08 does not resolve the independent reviewer item (`OD01B-B-08`).** That is a separate evidence item requiring a named human reviewer or a signed owner acceptance of the D-02 no-reviewer limitation.

### 9.3 GOV-D-08 Impact on Downstream Gates

| Gate | Impact of GOV-D-08 |
|---|---|
| OD-01A signature | Enables completion of signed-copy path, hash, retention fields |
| OD-01B signature | Same; does not resolve reviewer item |
| G3-RV-01 | Not directly blocked by GOV-D-08; retention structure supports clean approval reconstruction |
| G3 | Not directly blocked by GOV-D-08; G3 requires OD-01A/OD-01B signatures |
| G4 | Blocked by G3; not affected by GOV-D-08 |

---

## 10. Owner Decision Options

| Option | Description | Owner Action |
|---|---|---|
| **OPTION A — Approve the proposed controlled evidence-retention structure** | Accept `docs/approvals/` structure with subfolders, SHA-256 integrity, append-only verification log, read-only signed copies, hash register, named custodian, owner-defined retention period | Mark APPROVED; record custodian, retention period, and date |
| **OPTION B — Approve with recommended refinements** | Approve with the following refinements: SHA-256 hash algorithm; append-only verification log; preserve originals and never overwrite signed evidence; procedural controls plus restricted filesystem permissions; project owner as initial custodian with documented delegation permitted; proposed seven-year retention period after supersession or withdrawal (subject to applicable legal, contractual and organizational requirements — not a verified statutory requirement); signed copies remain outside Git unless separately authorized | Mark APPROVED; record custodian, retention period, and date |
| **OPTION C — Reject and return for redesign** | Reject the proposed method; require a fundamentally different approach | Mark REJECTED; document alternative requirements |

---

## 11. Implementation Acceptance Criteria

| Criterion | Source | Status |
|---|---|---|
| Approved folder structure created | GOV-D-08 Section 4 | NOT STARTED |
| README.md documenting retention procedures | GOV-D-08 Section 4 | NOT STARTED |
| Initialized evidence register (`decision_hash_register.csv`) | GOV-D-08 Section 5 | NOT STARTED |
| Initialized verification log (`verification_log.csv`) | GOV-D-08 Section 5 | NOT STARTED |
| SHA-256 verification procedure defined | GOV-D-08 Section 5 | SPECIFIED |
| Records custodian assigned | GOV-D-08 Section 8 | NOT NAMED |
| Retention and supersession policy defined | GOV-D-08 Section 7 | NOT DEFINED |
| Backup and recovery procedure defined | GOV-D-08 Section 6 | SPECIFIED (owner to define backup details) |
| Access-control procedure defined | GOV-D-08 Section 6 | SPECIFIED |
| Signed copies kept outside Git unless separately authorized | GOV-D-08 Section 3.4 | SPECIFIED |

---

## 12. Remaining Risks

| Risk | Description | Mitigation |
|---|---|---|
| R-01 | No records custodian named | Project owner initially; documented delegation permitted at approval |
| R-02 | Seven-year retention period is proposed operational policy, not verified statutory requirement | Owner must explicitly approve or revise; confirm against applicable legal and contractual requirements |
| R-03 | Filesystem read-only insufficient | Procedural controls required in addition |
| R-04 | Hash register not yet implemented | Implementation requires separate authorization after owner approval |
| R-05 | Circular dependency misunderstanding | Corrected: GOV-D-08 before OD-01A/B signatures |

---

## 13. Explicit Approval Status

| Field | Entry |
|---|---|
| Decision | [ ] OPTION A — APPROVED   [ ] OPTION B — APPROVE WITH REFINEMENTS   [ ] OPTION C — REJECTED |
| Approval scope | GOV-D-08 — Evidence Retention Policy |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Approval conditions | [BLANK — to be completed at signature] |
| Records custodian | [BLANK — project owner initially; documented delegation permitted] |
| Retention period | [BLANK — proposed seven years after supersession or withdrawal, subject to applicable legal, contractual and organizational requirements] |
| Signed-copy path | [BLANK — no docs/approvals/ structure] |
| Signed-copy SHA-256 | [BLANK — no signed copy exists] |
| Retention confirmed | [ ] Yes   [X] No — GOV-D-08 PENDING |
| Verification date/result | [BLANK — PENDING] |

**Formal signature:** ______________________________  
**Approval date:** ______________________________  

**Approval status:** PENDING. Evidence retention policy is proposed (revised draft), not approved. No owner decision has been made on GOV-D-08. No `docs/approvals/` directory exists. No implementation is authorized.

---

## 14. End of Decision Record

This document records the revised Evidence Retention Policy. No source files, data, DAX, Power Query, semantic model, Power BI, or other project artifacts were modified during its creation. No `docs/approvals/` directory was created. No signature, approval date, custodian name, retention period, or approval evidence has been created. GOV-D-08 remains pending formal owner approval.

**Verdict: REVISED DRAFT — OWNER REVIEW REQUIRED** — The draft defines the complete retention structure, integrity controls, dependency resolution, and acceptance criteria, incorporating the recommended refinements (SHA-256, append-only verification log, preserve-originals, procedural controls plus restricted filesystem permissions, project owner as initial custodian, proposed seven-year retention period, Git exclusion). Owner decision is required before `docs/approvals/` can be created and before OD-01A/OD-01B signature blocks can be completed.