# AEROVISION 360 — Consolidated Owner Approval Session

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Session ID:** OWNER-APPROVAL-2026-11-08  
**Prepared:** 2026-11-08  
**Prepared by:** Autonomous engineering agent (OpenCode)  
**Status:** Prepared for owner execution — NO signatures, dates, or approvals have been inserted

---

## Instructions to the Project Owner

Review each item below. For items you approve, enter your signature and actual approval date in the designated fields. Do not sign items you have not reviewed. Items are sequenced by dependency — OD-01A must be signed before OD-01B.

OpenCode will NOT insert signatures, dates, or approval evidence on your behalf. All `[BLANK]` fields require your personal completion.

---

## 1. OD-04g — Formal Approval of Exchange-Rate Policy

**File:** `docs/governance/OD04_OWNER_DECISION_RECORD.md`  
**Section:** §4.5 Owner Approval Record  
**Dependency:** None (standalone decision)  
**Unlocks:** Financial fact production context; prerequisite context for G3-RV-01

| Field | Entry |
|---|---|
| Decision | `[ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION` |
| Approval scope | OD-04a through OD-04f only |
| Owner name | KH Mohammad Farhan |
| Owner decision | `[BLANK — to be completed by the owner]` |
| Owner signature | `[BLANK — no signature recorded]` |
| Actual approval date | `[BLANK — no approval date recorded]` |
| Approval conditions | OD-04h and OD-04i remain UNSPECIFIED and require future controlled clarification and approval. This approval does not authorize G3-RV-01, schema freeze, G3, G4, production data promotion, or financial Power BI integration. |
| Signature evidence | `[BLANK — owner must identify actual signature evidence]` |
| Approval date evidence | `[BLANK — owner must record actual approval date evidence]` |

**Current status:** PENDING — owner signature and actual approval date required

---

## 2. GOV-D-04 — Owner-Confirmation Addendum Execution

**File:** `docs/governance/OD01_OWNER_CONFIRMATION_ADDENDUM_DRAFT.md`  
**Section:** §7 Owner Signature and Date  
**Dependency:** None  
**Unlocks:** GOV-B-05 resolution; OD-01A/OD-01B re-audit precondition 8

| Field | Entry |
|---|---|
| Decision owner / approver | KH Mohammad Farhan |
| Role | Project owner |
| Decision scope | The eight owner-confirmed choices in Section 4 |
| Confirmation source | ChatGPT conversation, 2026-11-01 |
| Signature | `[BLANK — NOT SIGNED]` |
| Signature date | `[BLANK — NOT ENTERED]` |
| Formal approval status | **PENDING** |
| Approval evidence reference | `[BLANK — NOT PROVIDED]` |
| Signed copy location | `[BLANK — NOT CREATED]` |

**Current status:** PROPOSED — owner review required; acceptance recorded 2026-11-06 but formal signature pending

---

## 3. GOV-D-06 — Formal Approval of Staleness Thresholds

**File:** `docs/governance/GOV_D_06_OWNER_ACCEPTANCE.md`  
**Section:** §7 Formal Approval Block  
**Dependency:** None  
**Unlocks:** OD-01A/OD-01B re-audit precondition 8 context; reference-data freshness governance

| Field | Entry |
|---|---|
| Decision | `[ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION` |
| Approval scope | Staleness thresholds: 365 days (Airline Name, Legal Name, Airline Group); 180 days (Airline IATA Code, Airline ICAO Code) |
| Staleness measurement | SourceVerifiedDate to reference-version approval date (or current date if earlier) |
| Stale action | QUARANTINE with QuarantineReason = STALE |
| Owner name | KH Mohammad Farhan |
| Owner decision | `[BLANK — to be completed by the owner]` |
| Owner signature | `[BLANK — no signature recorded]` |
| Actual approval date | `[BLANK — no approval date recorded]` |
| Approval conditions | Implementation of staleness checking in any system or pipeline is NOT authorized by this approval alone; separate implementation authorization is required. |
| Formal approval status | PENDING — owner signature and actual approval date required |

**Current status:** OWNER ACCEPTED — formal governance approval PENDING

---

## 4. GOV-D-07 — Implementation Authorization for ManifestHash Canonicalization

**File:** `docs/governance/GOV_D_07_OWNER_ACCEPTANCE.md`  
**Section:** §7 Implementation Authorization Block  
**Dependency:** GOV-D-06 (recommended sequence)  
**Unlocks:** G3-RV-01 reference manifest creation with ManifestHash field

| Field | Entry |
|---|---|
| Decision | `[ ] AUTHORIZED   [ ] NOT AUTHORIZED   [ ] RETURNED FOR REVISION` |
| Authorization scope | RFC 8785 JCS v1.0 ManifestHash canonicalization; SHA-256; lowercase hexadecimal output (64 characters); UTF-8 without BOM; ManifestHash self-exclusion; exact Unicode preservation; UTC ISO 8601 timestamp handling |
| Validation cases | V-01 through V-12 — none implemented, executed, or passed; to be executed as part of implementation |
| Reference manifest | `data/manifests/reference_versions.csv` with `ManifestHash` field computed per this specification |
| Reviewer/compensating control | Assignment of independent reviewer or documented compensating control required before implementation |
| Downstream gate approval | Formal downstream gate approval (G3-RV-01, T-78) required before implementation |
| Owner name | KH Mohammad Farhan |
| Owner decision | `[BLANK — to be completed by the owner]` |
| Owner authorization | `[BLANK — no authorization recorded]` |
| Actual authorization date | `[BLANK — no authorization date recorded]` |
| Implementation status | NOT STARTED — requires owner authorization above |
| Formal authorization status | PENDING — owner authorization and actual date required |

**Current status:** OWNER ACCEPTED (Option A) — implementation NOT authorized

---

## 5. GOV-D-08 — Implementation Authorization for Evidence Retention

**File:** `docs/governance/GOV_D_08_OWNER_ACCEPTANCE.md`  
**Section:** §7 Implementation Authorization Block  
**Dependency:** None  
**Unlocks:** `docs/approvals/` structure creation; hash register; verification log; signed-copy retention; OD-01A/OD-01B preconditions

| Field | Entry |
|---|---|
| Decision | `[ ] AUTHORIZED   [ ] NOT AUTHORIZED   [ ] RETURNED FOR REVISION` |
| Authorization scope | Creation of evidence-retention structure at `docs/approvals/` with subfolders `OD01A/`, `OD01B/`, `evidence/`, `hash_register/`; SHA-256 hash register (`decision_hash_register.csv`); append-only verification log (`verification_log.csv`); immutable signed-copy retention; procedural controls plus restricted filesystem permissions |
| Records custodian | Project owner initially (KH Mohammad Farhan); documented delegation permitted |
| Retention period | Proposed: seven years after supersession or withdrawal, subject to applicable legal, contractual and organizational requirements |
| Git exclusion | Signed copies remain outside Git unless separately authorized |
| Owner name | KH Mohammad Farhan |
| Owner decision | `[BLANK — to be completed by the owner]` |
| Owner authorization | `[BLANK — no authorization recorded]` |
| Actual authorization date | `[BLANK — no authorization date recorded]` |
| Implementation status | `docs/approvals/` directory NOT CREATED; hash register NOT INITIALIZED; verification log NOT INITIALIZED; signed copies deposited: NONE |
| Formal authorization status | PENDING — owner authorization and actual date required |

**Current status:** OWNER ACCEPTED (Option B) — implementation NOT authorized

---

## 6. D-02 — Owner Acceptance of Independent Reviewer Limitation

**File:** `docs/governance/CC01_OWNER_SELF_REVIEW.md`  
**Section:** §7.5 D-02 Owner Acceptance Block  
**Dependency:** None  
**Unlocks:** OD-01A/OD-01B re-audit preconditions; honest reporting of no independent assurance

**Owner decision wording (to be signed):**

> "No independent reviewer is assigned for AEROVISION 360. I accept the D-02 compensating-control route: owner self-review (CC-01) and documented compensating controls (CC-01 through CC-10) in lieu of independent review. No independent assurance is claimed."

| Field | Entry |
|---|---|
| Decision | `[ ] ACCEPTED   [ ] NOT ACCEPTED   [ ] RETURNED FOR REVISION` |
| Decision scope | D-02 no-independent-reviewer limitation and compensating-control route |
| Owner name | KH Mohammad Farhan |
| Owner decision | `[BLANK — to be completed by the owner]` |
| Owner signature | `[BLANK — no signature recorded]` |
| Actual date | `[BLANK — no date recorded]` |
| Independent reviewer assigned | `[ ] Yes   [X] No — no reviewer assigned` |
| Independent assurance claimed | `[ ] Yes   [X] No — not claimed` |
| Compensating controls accepted | CC-01 through CC-10 (documented but not fully executed) |
| Owner self-review (CC-01) | NOT EXECUTED — requires personal owner execution with dated checklist and initials |
| Formal acceptance status | PENDING — owner signature and actual date required |

**Current status:** D-02 communicated by owner — formal acceptance block prepared, signature pending

---

## 7. CC-01 — Owner Self-Review (Personal Execution Required)

**File:** `docs/governance/CC01_OWNER_SELF_REVIEW.md`  
**Section:** Sections 3, 4, 5, 7  
**Dependency:** D-02 acceptance  
**Unlocks:** OD-01A/OD-01B re-audit precondition 6; signature readiness

**Current recorded status:** 15 PASS / 14 FAIL / 4 PARTIAL of 33 items; NOT COMPLETE

**Owner must personally:**
1. Complete the 33-item checklist with dated checklist and owner initials
2. Record unresolved questions and dispositions
3. Accept executed controls and residual limitation
4. Do NOT convert FAIL or PARTIAL items to PASS without new evidence

**Items requiring owner execution:**
- All FAIL items (14 items): H-04 re-audit, H-05 re-audit, M-07 re-audit, M-12 re-audit, owner self-review execution, fresh re-audit, named reviewer assignment, etc.
- All PARTIAL items (4 items): compensating-control route, compensating-control challenge, B-05/D-04 resolution, B-08/D-08 resolution
- Dated checklist with owner initials and dispositions

**Current status:** NOT COMPLETE — owner personal execution required; agent cannot execute on owner's behalf

---

## 8. OD-01A — Airline Population Formal Approval

**File:** `docs/OD01A_AIRLINE_POPULATION_DECISION.md`  
**Section:** §7.4 Approval Record  
**Dependency:** Re-audit preconditions 1–9 (including D-1 disposition ✅, D-2 acceptance ⬜, CC-01 execution ⬜, GOV-D-04 ⬜, GOV-D-08 ⬜)  
**Unlocks:** OD-01B signature (OD-01B depends on OD-01A)

| Field | Entry |
|---|---|
| Decision | `[ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION` |
| Approval scope | OD-01A Sections 2, 3, and 4 only |
| Exclusions | OD-01B; reference CSVs; schema freeze; synthetic data; production ETL; Power Query; Power BI; G3; G4 |
| Owner name | KH Mohammad Farhan |
| Owner decision | `[BLANK — to be completed by the owner]` |
| Owner signature | `[BLANK — no signature recorded]` |
| Actual approval date | `[BLANK — no approval date recorded]` |
| Approval conditions | `[BLANK — to be completed at signature]` |
| Reviewer route | Compensating-control route accepted under D-01/D-02; independent reviewer not assigned |
| Scope v1.1 SHA-256 | `5282EFFAD84FF72C84DB3864B3ECFF2B99C6DD8139850F341B2A4148FA7DC627` (per D-1) |
| Contract v1.5 SHA-256 | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` |
| Signed-copy path | `[BLANK — D-08 PENDING; no docs/approvals/ structure]` |
| Signed-copy SHA-256 | `[BLANK — no signed copy exists]` |
| Retention confirmed | `[ ] Yes   [X] No — D-08 PENDING` |
| Verification date / result | `[BLANK — PENDING]` |

**Current status:** PENDING — owner signature and actual approval date required; re-audit preconditions 1–9 must be recorded first

---

## 9. OD-01B — Airline Identity/Reference Formal Approval

**File:** `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`  
**Section:** §11.4 Approval Record  
**Dependency:** OD-01A signature FIRST (OD-01B depends on OD-01A's population decision)  
**Unlocks:** G3-RV-01 execution; reference-data creation

| Field | Entry |
|---|---|
| Decision | `[ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION` |
| Approval scope | OD-01B Sections 2, 4, 5, 6, and 8 only |
| Exclusions | Schema freeze; reference CSVs; synthetic data; production ETL; Power Query; semantic model; DAX; Power BI; G3; G4; G3-RV-01; Git |
| Owner name | KH Mohammad Farhan |
| Owner decision | `[BLANK — to be completed by the owner]` |
| Owner signature | `[BLANK — no signature recorded]` |
| Actual approval date | `[BLANK — no approval date recorded]` |
| Approval conditions | GOV-D-05 condition: `BusinessModelClass` remains an optional, nullable analytical column with no baseline values populated (null baseline). No mapping or rubric is approved at this time. `[BLANK — additional conditions to be completed at signature]` |
| Scope v1.1 SHA-256 | `5282EFFAD84FF72C84DB3864B3ECFF2B99C6DD8139850F341B2A4148FA7DC627` (per D-1) |
| Contract v1.5 SHA-256 | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` |
| Signed-copy path | `[BLANK — D-08 PENDING; no docs/approvals/ structure]` |
| Signed-copy SHA-256 | `[BLANK — no signed copy exists]` |
| Retention confirmed | `[ ] Yes   [X] No — D-08 PENDING` |
| Verification date / result | `[BLANK — PENDING]` |

**Current status:** PENDING — owner signature and actual approval date required; MUST follow OD-01A signature

---

## Sequencing Summary

1. OD-04g → GOV-D-04 → GOV-D-06 → GOV-D-07 → GOV-D-08 → D-02 → CC-01 (can proceed in parallel among themselves)
2. OD-01A signature (after preconditions met)
3. OD-01B signature (after OD-01A)
4. G3-RV-01 → Schema freeze → G3 → G4 → Financial integration → Publication → Git release → Evidence archive

---

**End of Owner Approval Session.**  
No signatures, initials, approval dates, or approval evidence have been inserted by this document. All `[BLANK]` fields require Project Owner personal completion.
