# OD-01A / OD-01B OWNER ACTION CHECKLIST

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** OD01A-OD01B-OWNER-ACTION-CHECKLIST-2026-11-08  
**Document type:** Owner action checklist — personal actions required from the project owner  
**Based on:** `OD01A_OD01B_FINAL_APPROVAL_READINESS_REPORT.md` (audit baseline: `FINAL_INDEPENDENT_MASTER_AUDIT/`)  
**Prepared:** 2026-11-08  
**Project owner / approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  
**Status:** READY FOR OWNER EXECUTION — NO FIELD PRE-FILLED BY OPENSECODE  

---

## How to use this checklist

This checklist lists **only the actions that you, the project owner (KH Mohammad Farhan), must personally perform**. Each action states what to review, what to decide or sign, and the evidence you must produce. No field is pre-filled; no signature, date, or reviewer identity is invented here. Complete the items in order — OD-01A must be signed before OD-01B because OD-01B depends on OD-01A's population decision.

**Rules you must honor:**
- Do not backdate any signature or approval date.
- Do not let anyone (including OpenCode) insert a signature or approval date on your behalf.
- Do not claim independent review where no independent reviewer exists.
- Do not execute G3-RV-01 or G4 until OD-01A and OD-01B are formally signed.
- Do not modify PBIX, DAX, Power Query, or source dataset files.

---

## Phase 0 — Owner personal decisions (no signature yet, decisions only)

| # | Action | What you must do | Evidence to produce | Done? |
|---|---|---|---|---|
| P-1 | Accept H-05 split G3 vocabulary | Review `docs/governance/H05_OWNER_DECISION_BRIEF.md` and confirm: G3 gate execution = NOT STARTED; G3 design documentation = PREPARED — DRAFT; G3 formal approval = NOT FORMALLY APPROVED; G4 = BLOCKED; G3-RV-01 = NOT EXECUTED; test inventory = 71 PLANNED + 8 BLOCKED = 79, 0 PASS | Owner confirmation recorded (your decision, dated) | [ ] |
| P-2 | Resolve H-04 residual risk | Review `docs/governance/H04_RESIDUAL_RISK_ACCEPTANCE_CLARIFICATION_DRAFT.md`. Choose: OPTION A (acknowledge open risks, defer acceptance), OPTION B (provisional acceptance), or OPTION C (defer all). No residual risk is accepted unless you explicitly select it. | Owner decision recorded, dated, with option selected | [ ] |
| P-3 | Accept compensating-control route | Confirm acceptance of the D-02 no-independent-reviewer limitation: no independent reviewer available; independent assurance NOT CLAIMED; compensating controls documented but not executed. | `C-06_OD01B-B-08_OWNER_ACCEPTANCE.md` OPTION B already recorded 2026-11-07; re-confirm | [ ] |
| P-4 | Confirm GOV-D-04 addendum | Review `docs/governance/OD01_OWNER_CONFIRMATION_ADDENDUM_DRAFT.md` (clarifies eight owner-confirmed choices vs contract v1.5). Decide whether to execute it as a signed controlled artifact. | Signed addendum (if executed) — real date, not backdated | [ ] |
| P-5 | Confirm GOV-D-08 evidence retention | Review `docs/governance/GOV_D_08_OWNER_ACCEPTANCE.md` (Option B accepted 2026-11-06). Decide to implement the `docs/approvals/` structure, SHA-256 hash register, and append-only verification log. | Implementation decision recorded | [ ] |

---

## Phase 1 — CC-01 Owner Self-Review (you must execute personally)

**Prerequisite:** Items P-1 to P-5 should be resolved first. CC-01 cannot be executed by OpenCode — you are the preparer of OD-01A/OD-01B and therefore cannot be the independent reviewer.

| # | Action | What you must do | Evidence to produce | Done? |
|---|---|---|---|---|
| C-1 | Execute CC-01 checklist | Complete `docs/governance/CC01_OWNER_SELF_REVIEW.md` checklist with a **dated checklist and your initials**. Record each unresolved question and its disposition. Record your acceptance of executed controls and residual limitation. | Dated CC-01 checklist with owner initials; unresolved-question record; dispositions | [ ] |
| C-2 | Confirm self-review is NOT independent review | Explicitly record that CC-01 is owner self-review, NOT independent audit, and that no independent assurance is claimed. | Statement in CC-01 record | [ ] |

**CC-01 acceptance criteria (all must be true):**
- [ ] Dated checklist completed by you (project owner)
- [ ] Owner initials present
- [ ] Each unresolved question recorded with a disposition
- [ ] Owner acceptance of executed controls and residual limitation recorded
- [ ] Explicitly labeled "owner self-review — not independent review"

**Current status:** NOT EXECUTED (14 PASS / 14 FAIL / 4 PARTIAL; overall NOT COMPLETE). Nine blocking conditions for OD-01A and nine for OD-01B remain.

---

## Phase 2 — Compensating-control challenge (document, do not claim independence)

| # | Action | What you must do | Evidence to produce | Done? |
|---|---|---|---|---|
| CC-1 | Document compensating-control challenge | Record in writing the compensating-control challenge accepted under D-01/D-02: no independent reviewer assigned; AI-assisted review is NOT independent assurance; self-review and automated hash/schema checks are the compensating controls. | Signed compensating-control documentation | [ ] |
| CC-2 | Sign D-02 no-reviewer limitation | Since no independent reviewer is available, sign your acknowledgment of the D-02 limitation. | Signed limitation acknowledgment | [ ] |
| CC-3 | Complete B-04 in approval blocks | Add compensating-control initials, date, and evidence reference to both OD-01A §7.4 and OD-01B §11.4 approval blocks. | Initials/date/evidence reference in both approval blocks | [ ] |

**Compensating-control acceptance criteria:**
- [ ] Challenge documented in writing
- [ ] Reviewer-limitation statement recorded (no independent reviewer; AI review not independent)
- [ ] Signed owner acknowledgment of D-02 limitation (if no reviewer)
- [ ] Compensating-control execution marked complete/closed (not partial)

**Current status:** PARTIAL — NOT CLOSED (CC-09 accepted under D-02; CC-01 not executed; CC-02 not executed).

---

## Phase 3 — GOV-B-05 / GOV-B-08 (owner-confirmation addendum + evidence retention)

| # | Action | What you must do | Evidence to produce | Done? |
|---|---|---|---|---|
| GV-1 | Execute GOV-D-04 addendum | Sign `docs/governance/OD01_OWNER_CONFIRMATION_ADDENDUM_DRAFT.md` as a controlled artifact, citing contract v1.5 and OD-01A/B v0.2, superseding historical statements, with no approval implied. Real date, not backdated. | Signed GOV-D-04 addendum with real date | [ ] |
| GV-2 | Implement GOV-D-08 structure | Create read-only `docs/approvals/` with subfolders `OD01A/`, `OD01B/`, `evidence/`, `hash_register/`; establish SHA-256 hash register; establish append-only verification log; record records custodian (you, initially); confirm seven-year retention policy; confirm Git exclusion for signed copies. | `docs/approvals/` structure; hash register; verification log; retention confirmed | [ ] |
| GV-3 | Record GOV-B-05 / GOV-B-08 resolution | Record that GOV-B-05 is resolved by GOV-D-04 and GOV-B-08 is resolved by GOV-D-08 (or explicitly withhold signature if not resolved). | Resolution recorded in both OD-01A and OD-01B approval blocks | [ ] |

**GOV-D-04 acceptance criteria:**
- [ ] Addendum executed with your signature (real date)
- [ ] Cites contract v1.5 and OD-01A/B v0.2
- [ ] Supersedes historical statements; no approval implied

**GOV-D-08 acceptance criteria:**
- [ ] Read-only `docs/approvals/` exists with the four subfolders
- [ ] SHA-256 hash register initialized
- [ ] Append-only verification log initialized
- [ ] Signed-copy retention path recorded
- [ ] Retention confirmed ([ ] Yes)
- [ ] Signed copies excluded from Git

**Current status:** GOV-D-04 accepted in principle but NOT SIGNED; GOV-D-08 accepted in principle but `docs/approvals/` NOT CREATED, registers NOT INITIALIZED.

---

## Phase 4 — Fresh re-audit (precondition 9)

| # | Action | What you must do | Evidence to produce | Done? |
|---|---|---|---|---|
| RA-1 | Complete fresh re-audit | Perform (or commission under the compensating-control route) a fresh governance re-audit of OD-01A/OD-01B against the corrected artifacts (risk register, progress ledger, OD-01A/B §7.3/§11.3, closure proposal). Record the final finding status for H-04, H-05, M-07, M-12 and confirm no signature blocker remains. | Fresh re-audit record with final finding status | [ ] |

**Re-audit acceptance criteria:**
- [ ] Re-audit record exists
- [ ] References corrected artifacts
- [ ] Final finding status recorded for each finding (open / partially verified / closed at documentation level only)
- [ ] Confirms no signature blocker remains (or lists remaining blockers explicitly)
- [ ] Independent assurance NOT claimed

**Current status:** PENDING (no fresh re-audit completed).

---

## Phase 5 — Formal OD-01A signature (sign FIRST)

**Prerequisites:** Phases 0–4 complete. OD-01B must NOT be signed before OD-01A.

| # | Field | What you enter | Source location |
|---|---|---|---|
| S-1 | Decision | [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION | OD-01A §7.4 |
| S-2 | Approval scope | OD-01A Sections 2, 3, and 4 only | OD-01A §7.3 |
| S-3 | Exclusions | OD-01B; reference CSVs; schema freeze; synthetic data; production ETL; Power Query; Power BI; G3; G4 | OD-01A §7.3 |
| S-4 | Owner name | KH Mohammad Farhan | OD-01A §7.4 |
| S-5 | Owner decision | Your decision text | OD-01A §7.4 |
| S-6 | **Owner signature** | **Your real signature — not pre-filled, not backdated** | OD-01A §7.4 |
| S-7 | **Actual approval date** | **Your real approval date — not pre-filled, not backdated** | OD-01A §7.4 |
| S-8 | Approval conditions | Your conditions (if any) | OD-01A §7.4 |
| S-9 | Reviewer route | [ ] Compensating control   [ ] Independent reviewer   [ ] N/A | OD-01A §7.2 |
| S-10 | Compensating-control acceptance | Your acceptance text | OD-01A §7.2 |
| S-11 | Reviewer limitation statement | "No independent reviewer; AI review is not independent assurance" | OD-01A §7.2 |
| S-12 | Reviewer name / role / org | Your entry (or blank if none) | OD-01A §11 |
| S-13 | Reviewer independence | [ ] Independent   [ ] Not independent   [ ] N/A — no reviewer | OD-01A §11 |
| S-14 | Reviewer result | [ ] CONCUR   [ ] CONCUR WITH RESERVATIONS   [ ] DISSENT   [ ] N/A | OD-01A §11 |
| S-15 | Reviewer signature / date | Your entry (or blank) | OD-01A §11 |
| S-16 | Residual concerns | H-04, H-05, M-07, M-12 open pending re-audit; B-03–B-08 open | OD-01A §7.4 |
| S-17 | Re-audit record | Your fresh re-audit reference | OD-01A §7.1(9) |
| S-18 | Scope v1.1 SHA-256 | `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` | OD-01A §6 E-07 |
| S-19 | Contract v1.5 SHA-256 | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` | OD-01A §7.4 |
| S-20 | Signed-copy path | Path under `docs/approvals/OD01A/` (once GOV-D-08 structure exists) | OD-01A §7.4 |
| S-21 | Signed-copy SHA-256 | SHA-256 of the signed copy | OD-01A §7.4 |
| S-22 | Retention confirmed | [ ] Yes   [ ] No | OD-01A §7.4 |
| S-23 | Verification date / result | Your verification date and result | OD-01A §7.4 |

**OD-01A acceptance criteria (all must be true before signing OD-01B):**
- [ ] Revision 0.2 hashes verified and recorded (Item 1)
- [ ] H-04, H-05, M-07, M-12 re-audited (Item 2)
- [ ] CC-01 owner self-review executed with initials (Item 3)
- [ ] Compensating-control challenge documented and closed (Item 4)
- [ ] GOV-B-05 resolved by GOV-D-04; GOV-B-08 resolved by GOV-D-08 (Item 5)
- [ ] Fresh re-audit records final finding status; no signature blocker remains (precondition 9)
- [ ] All signature-block fields S-1 to S-23 completed by you
- [ ] Real signature + real approval date (not backdated)

**Current status:** BLOCKED — all signature fields BLANK.

---

## Phase 6 — Formal OD-01B signature (sign AFTER OD-01A)

**Prerequisite:** OD-01A formally signed first.

| # | Field | What you enter | Source location |
|---|---|---|---|
| B-1 | Decision | [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION | OD-01B §11.4 |
| B-2 | Approval scope | OD-01B Sections 2, 4, 5, 6, and 8 only | OD-01B §11.3 |
| B-3 | Exclusions | Schema freeze; reference CSVs; synthetic data; production ETL; Power Query; semantic model; DAX; Power BI; G3; G4; G3-RV-01; Git | OD-01B §11.3 |
| B-4 | Owner name | KH Mohammad Farhan | OD-01B §11.4 |
| B-5 | Owner decision | Your decision text | OD-01B §11.4 |
| B-6 | **Owner signature** | **Your real signature — not pre-filled, not backdated** | OD-01B §11.4 |
| B-7 | **Actual approval date** | **Your real approval date — not pre-filled, not backdated** | OD-01B §11.4 |
| B-8 | Approval conditions | Your conditions (if any) | OD-01B §11.4 |
| B-9 | Reviewer route | [ ] Compensating control   [ ] Independent reviewer   [ ] N/A | OD-01B §11.2 |
| B-10 | Compensating-control acceptance | Your acceptance text | OD-01B §11.2 |
| B-11 | Reviewer limitation statement | "No independent reviewer; AI review is not independent assurance" | OD-01B §11.2 |
| B-12 | Reviewer name / role / org | Your entry (or blank if none) | OD-01B §11 |
| B-13 | Reviewer independence | [ ] Independent   [ ] Not independent   [ ] N/A — no reviewer | OD-01B §11 |
| B-14 | Reviewer result | [ ] CONCUR   [ ] CONCUR WITH RESERVATIONS   [ ] DISSENT   [ ] N/A | OD-01B §11 |
| B-15 | Reviewer signature / date | Your entry (or blank) | OD-01B §11 |
| B-16 | Residual concerns | H-04, H-05, M-07, M-12 open pending re-audit; B-03–B-08 open | OD-01B §11.4 |
| B-17 | Re-audit record | Your fresh re-audit reference | OD-01B §11.1(9) |
| B-18 | D-05 PENDING noted | "D-05 remains PENDING; no BusinessModelClass value populated" | OD-01B §11.1(9) |
| B-19 | Scope v1.1 SHA-256 | `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` | OD-01B §10 |
| B-20 | Contract v1.5 SHA-256 | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` | OD-01B §11.4 |
| B-21 | Signed-copy path | Path under `docs/approvals/OD01B/` | OD-01B §11.4 |
| B-22 | Signed-copy SHA-256 | SHA-256 of the signed copy | OD-01B §11.4 |
| B-23 | Retention confirmed | [ ] Yes   [ ] No | OD-01B §11.4 |
| B-24 | Verification date / result | Your verification date and result | OD-01B §11.4 |

**OD-01B acceptance criteria (all must be true):**
- [ ] OD-01A formally signed first (B-0 depends on OD-01A population)
- [ ] All Items 1–7 preconditions met (same as OD-01A)
- [ ] D-05 PENDING noted; no BusinessModelClass value populated
- [ ] All signature-block fields B-1 to B-24 completed by you
- [ ] Real signature + real approval date (not backdated)

**Current status:** BLOCKED — all signature fields BLANK; OD-01A not yet signed.

---

## Phase 7 — Post-signature retention (per GOV-D-08)

| # | Action | What you must do | Evidence to produce | Done? |
|---|---|---|---|---|
| RT-1 | Deposit signed copies | Place the signed OD-01A and OD-01B copies in `docs/approvals/OD01A/` and `docs/approvals/OD01B/` respectively. | Signed copies deposited | [ ] |
| RT-2 | Record signed-copy hashes | Compute and record SHA-256 of each signed copy in the hash register. | Hash register entries | [ ] |
| RT-3 | Log verification | Append a verification entry (date, result, file, hash) to the verification log. | Verification log entry | [ ] |
| RT-4 | Confirm Git exclusion | Confirm signed copies remain outside Git unless separately authorized. | Git status check | [ ] |

**Retention acceptance criteria:**
- [ ] Signed copies retained read-only under `docs/approvals/`
- [ ] SHA-256 hashes recorded in hash register
- [ ] Verification log append-only entry made
- [ ] Signed copies excluded from Git

---

## Summary: owner's personal signature package

You must personally produce, in order:

1. **H-05 decision** (accept split G3 vocabulary)
2. **H-04 decision** (residual risk option A/B/C)
3. **CC-01 owner self-review** (dated checklist + initials + dispositions)
4. **Compensating-control documentation** (D-02 limitation signed; B-04 initials/date/evidence in both approval blocks)
5. **GOV-D-04 addendum** (signed, real date)
6. **GOV-D-08 structure** (`docs/approvals/` + hash register + verification log)
7. **Fresh re-audit** (final finding status; no blocker remains)
8. **OD-01A signature** (real signature + real approval date, all S-fields)
9. **OD-01B signature** (real signature + real approval date, all B-fields; D-05 noted)
10. **Signed-copy retention** (deposit + hash + verification log + Git exclusion)

**Only after all 10 items are complete** are OD-01A and OD-01B formally signed and approved, unblocking G3-RV-01 and the downstream roadmap (reference data, G3 approval, G4 authorization, financial data generation, QA, production deployment).

---

## Restrictions honored (do not deviate)

- No independent review claimed (no reviewer assigned; independent assurance NOT CLAIMED).
- No signature, approval date, or reviewer identity fabricated or pre-filled by OpenCode.
- No approved decision wording changed.
- G3-RV-01 and G4 NOT executed (remain blocked until OD-01A/OD-01B signed).
- No PBIX, DAX, Power Query, or source dataset modified.
- No `docs/approvals/` structure, signed copy, hash register, or verification log created by OpenCode (implementation actions reserved to you under GOV-D-08).

**STOP — Complete this checklist personally, then confirm to proceed to G3-RV-01.**
