# OD-01 Remediation Action Register

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** OD-01-RAR-2026-11-06-001  
**Document Type:** Remediation Action Register  
**Status:** COMPLETE — READY FOR OWNER REVIEW  
**Prepared:** 2026-11-06  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Register Purpose

This register lists every corrective action required before OD-01A and OD-01B can be submitted for formal owner signature. Each action is categorized by category (A = Owner decisions, B = Findings, C = Evidence and namespace, D = Document consistency, E = Gate and signature) with severity, root cause, evidence location, required correction, owner, dependency, authorization, acceptance criteria, and verification method.

No action in this register has been completed. All actions are pending owner decision or execution.

---

## 2. Category A — Owner Decisions

Owner decisions require formal project owner action. Severity is an analytical priority, not an approval.

| ID | Severity | Root Cause | Evidence Location | Required Correction | Owner | Dependency | Authorization | Acceptance Criteria | Verification Method |
|---|---|---|---|---|---|---|---|---|---|
| A-01 / GOV-D-04 | HIGH | Historical confirmation not superseded | Owner confirmation lines 20, 82, 299, 357–358; packet lines 84–97 | Create separate controlled addendum preserving original; cite contract v1.5 and OD-01A/B v0.2; supersede historical statements; no approval implied | Project Owner | C-04; contract status | GOV-D-04 | Addendum exists, signed/dated, original unchanged, stale statements explicitly superseded | Hash original; text check; owner decision/date |
| A-02 / GOV-D-05 | MEDIUM | BusinessModelClass treatment undefined | OD-01B lines 79–83, 185–188; contract lines 247, 252, 766 | Owner selects null baseline or approved mapping/rubric; record condition in OD-01B approval block | Project Owner | OD-01B signature | GOV-D-05 | Decision recorded; no values populated unless mapping approved; approval condition explicit | Search for populated values; inspect approval block |
| A-03 / GOV-D-06 | HIGH | Thresholds proposed, not approved | Contract line 260; compensating proposal §8.1 | Approve or revise 365/180-day thresholds and 90-day exception policy; record in controlled change | Project Owner | G3-RV-01 | GOV-D-06 — Owner-accepted | Thresholds confirmed (365/180 days); formal governance approval PENDING; implementation authorization NOT GRANTED | Cross-check contract/design; re-audit |
| A-04 / GOV-D-07 | HIGH | ManifestHash canonicalization undefined | Contract line 264; compensating proposal §8.2 | Approve deterministic canonical-JSON method; record exact field order, encoding, casing, exclusions, test vector | Project Owner | G3-RV-01; T-78 | GOV-D-07 — Owner-accepted | Method recorded (GOV_D_07_OWNER_ACCEPTANCE.md); technical specification DEFINED; implementation NOT STARTED; validation tests NOT EXECUTED; independent review NOT COMPLETED; formal downstream gate approval PENDING | Independent recomputation; manifest test |
| A-05 / GOV-D-08 | HIGH | Retention structure absent | docs/approvals/ absent; compensating proposal §9 | Approve read-only structure, hash register, verification log, signed-copy procedure, retention period | Project Owner | GOV-D-08 | GOV-D-08 — Owner-accepted | Method recorded (GOV_D_08_OWNER_ACCEPTANCE.md); technical specification DEFINED; retention structure implementation NOT STARTED; custodian assignment OWNER ACCEPTED; evidence register NOT INITIALIZED; verification log NOT INITIALIZED; formal OD-01A/OD-01B approval PENDING | Directory check; hash verification; ACL check |

---

## 3. Category B — Findings

Findings require corrective action before signature.

| ID | Severity | Root Cause | Evidence Location | Required Correction | Owner | Dependency | Authorization | Acceptance Criteria | Verification Method |
|---|---|---|---|---|---|---|---|---|---|
| B-01 / H-04 | HIGH | Risk register omitted three scenarios | Risk register R-09–R-11; original audit lines 228–238 | Maintain R-09–R-11 as open; update residual rows; do not claim risk closure | Project Owner | None for documentation closure | D-09 recorded; new doc change for residual rows | R-09–R-11 remain open with owners, controls, monitoring, closure evidence; H-04 status current | Register inspection; re-audit — OWNER ACCEPTED — OPTION A (ACKNOWLEDGED): R-09, R-10, R-11 acknowledged as open risks with HIGH inherent ratings; NO residual risk accepted; mitigations NOT IMPLEMENTED / NOT VERIFIED; all risks remain OPEN |
| B-02 / H-05 | HIGH | Single G3 label; criteria not consolidated; ledger test summary wrong | Ledger lines 12–16; contract line 1907; OD-01A line 26; OD-01B line 26; ledger line 13 | Propagate six-status vocabulary; consolidate G3 criteria; correct test summary to 71 PLANNED, 8 BLOCKED, 0 PASS | Project Owner | Controlled document change | New authorization | All current docs use split status; criteria consolidated; ledger matches contract | Text search; test count; re-audit — PARTIALLY RESOLVED: Six-status vocabulary propagated to all documents (OD-01A line 26, OD-01B line 26, contract line 1907, owner confirmation lines 5/26-28/43-44/80/360-361); test summary corrected to 71 PLANNED, 8 BLOCKED (T-37, T-42–T-46, T-55, T-79), 0 PASS; G3 split into gate execution/NOT STARTED, documentation/PREPARED — DRAFT, formal approval/NOT FORMALLY APPROVED. Consolidated G3 acceptance-criteria record pending owner authorization; G3 gate not APPROVED |
| B-03 / M-07 | MEDIUM | No independent reviewer; controls not executed | OD-01A/B §7.2/§11.2; CC-01–CC-10; no G3-RV-01 | Execute CC-01 self-review; record acceptance, residual risk, signed limitation; define G3-RV-01 | Project Owner | GOV-D-08; B namespace | Owner execution/acceptance | Dated checklist, initials, unresolved questions, acceptance, limitation, G3-RV-01 definition exist | Artifact inspection; signature check |
| B-04 / M-12 | MEDIUM | Scope sentence vs section list; key-map gap; Section 3 ambiguity; D-05 condition | OD-01B lines 379–390; contract line 1046; OD-01A lines 108–110, 223–226 | Align scope; resolve key-map trigger; clarify Section 3; state D-05 condition | Project Owner | GOV-D-05; C-02 | New authorization | Signature block unambiguously lists approved/acknowledged/excluded; one key-map trigger; D-05 condition stated | Cross-document review; re-audit |

---

## 4. Category C — Evidence and Namespace

| ID | Severity | Root Cause | Evidence Location | Required Correction | Owner | Dependency | Authorization | Acceptance Criteria | Verification Method |
|---|---|---|---|---|---|---|---|---|---|
| C-01 / GOV-B-03 | HIGH | Stale scope hash | OD-01A E-07; OD-01B shared evidence; current scope hash | Update stale residual row; preserve historical evidence | Project Owner | None | D-03 recorded | Stale hash absent from current records; residual row current | Global search; hash check — RESOLVED: OD-01A Section 7.4 and OD-01B Section 11.4 updated with current per-finding statuses |
| C-02 / GOV-B-04 | MEDIUM | Approval record incomplete | OD-01A lines 240–254; OD-01B lines 404–418 | Add owner initials/date for CC acceptance; add CC evidence reference | Project Owner | M-07 | Signature-time completion | Fields completed with actual initials/date and evidence path | Approval block inspection |
| C-03 / GOV-B-05 | MEDIUM | Addendum not created | Owner confirmation stale statements | Execute GOV-D-04 | Project Owner | GOV-D-04 | GOV-D-04 | Addendum exists and supersedes stale statements | Text and hash check |
| C-04 / GOV-B-08 | MEDIUM | Retention structure absent | docs/approvals/ absent | Execute GOV-D-08 | Project Owner | GOV-D-08 | GOV-D-08 | Read-only structure, hash register, verification log exist | Directory and hash check |
| C-05 / OD01B-B-05 | HIGH | Reference manifest absent | OD-01B line 334; data/manifests/ empty | Create only after signatures, D-06/D-07, reference data, G3-RV-01 | Project Owner | OD-01A/B signatures; D-06/D-07 | Separate reference authorization | Manifest exists with approved version and hash | File check; T-78 |
| C-06 / OD01B-B-08 | HIGH | No independent reviewer | OD-01B line 337 | Assign named human reviewer or record signed D-02 limitation | Project Owner | M-07 | OWNER ACCEPTED — Option B | Reviewer identity/signature or signed limitation exists — OWNER ACCEPTED: CC-09 reviewer limitation accepted under D-02; CC-01 owner self-review NOT YET EXECUTED; independent assurance NOT CLAIMED | Approval block inspection — PARTIALLY RESOLVED: CC-09 owner acceptance recorded; CC-01 self-review NOT EXECUTED (mandatory prerequisite for OD-01A/OD-01B signature); independent assurance NOT CLAIMED |
| C-07 / C-01 | HIGH | Duplicate B-xx labels | OD-01B lines 328–337; governance proposals; precondition 8 | Adopt prefixed notation in future controlled documents; correct precondition 8 | Project Owner | Controlled document change | New authorization | No ambiguous B token in signature/preconditions | Global search; cross-doc review — RESOLVED: GOV-B-05/GOV-B-08 (governance namespace) and OD01B-B-05/OD01B-B-08 (OD-01B local namespace) distinguished; precondition 8 corrected in both OD-01A Section 7.1 and OD-01B Section 11.1; residual concerns rows updated in both decision records |
| C-08 / C-02 | HIGH | Contract immutability trigger conflicts with OD-01B exclusion | Contract line 1046; OD-01B lines 135–136, 379–390 | Choose one key-map approval trigger and align contract and decision record | Project Owner | M-12 | OWNER ACCEPTED — Option B | One documented trigger; no circularity — G3-RV-01 is the key-map immutability trigger; OD-01B does not approve key map; contract §7.1 and OD-01B §11.3 updated; formal governance approval pending | Cross-document review — RESOLVED: G3-RV-01 approved as key-map immutability trigger; contract §7.1 line 1046 and OD-01B §11.3 lines 379–390 updated; residual risk acceptance PENDING |

---

## 5. Category D — Document Consistency

| ID | Severity | Root Cause | Evidence Location | Required Correction | Owner | Dependency | Authorization | Acceptance Criteria | Verification Method |
|---|---|---|---|---|---|---|---|---|---|
| D-01 / C-03 | MEDIUM | Duplicate D-xx labels | Design spec lines 128–132; owner packet lines 84–157 | Add namespace note or prefixed labels in future controlled documents | Project Owner | Controlled document change | New authorization | Every cited D code unambiguous | Global search; cross-doc review |
| D-02 / C-04 | HIGH | Confirmation v1.4 vs contract v1.5 | Owner confirmation lines 20, 82, 299, 357–358; change records | Execute GOV-D-04; state contract v1.5 and OD-01A/B v0.2 | Project Owner | GOV-D-04 | GOV-D-04 | Evidence chain current and internally consistent | Text and hash check |
| D-03 / C-05 | MEDIUM | G3 vocabulary not propagated | Contract line 1907; OD-01A line 26; OD-01B line 26 | Propagate six-status vocabulary | Project Owner | H-05 | New authorization | All current docs use split status | Text search |
| D-04 / C-06 | MEDIUM | OD-01A Section 3 includes proposed AirlineId | OD-01A lines 108–110, 223–226 | Exclude or explicitly approve the allocation | Project Owner | M-12 | New authorization | Scope statement unambiguous | Cross-document review |
| D-05 / C-07 | MEDIUM | D-05 pending while Section 4 in scope | OD-01B lines 185–188, 397 | Add explicit no-values approval condition | Project Owner | GOV-D-05 | GOV-D-05 | Condition in approval block | Approval block inspection |
| D-06 / C-08 | MEDIUM | Residual rows stale | OD-01A lines 217–219; OD-01B lines 373–375 | Update statuses to current per-finding results | Project Owner | Re-audit acceptance | New authorization | Rows match current statuses | Text comparison |
| D-07 / C-09 | MEDIUM | Contract draft used as governing baseline | Contract line 9; OD-01A/B line 15 | State contract is not approved; complete contract review | Project Owner | Contract review | Formal contract review | Decision records disclaim contract approval; contract status current | Cross-document review |
| D-08 / C-10 | MEDIUM | Ledger test summary wrong | Ledger line 13; contract test rows | Correct to 71 PLANNED, 8 BLOCKED, 0 PASS | Project Owner | H-05 | New authorization | Ledger matches contract | Test count |

---

## 6. Category E — Gate and Signature

| ID | Severity | Root Cause | Evidence Location | Required Correction | Owner | Dependency | Authorization | Acceptance Criteria | Verification Method |
|---|---|---|---|---|---|---|---|---|---|
| E-01 / OD-01A | BLOCKER | Preconditions unmet | OD-01A §7 | Complete all preconditions; sign with actual date/evidence | Project Owner | A/B/C/D items | Owner signature | Signed record with actual date and evidence; residual row current | Signed copy and hash |
| E-02 / OD-01B | BLOCKER | Preconditions unmet | OD-01B §11 | Complete all preconditions; sign after OD-01A | Project Owner | A/B/C/D items; OD-01A | Owner signature | Signed record with actual date and evidence; key-map trigger resolved | Signed copy and hash |
| E-03 / G3 | GATE | Gate not executed | Ledger line 12; contract §15.2 | Hold gate review after signatures and criteria consolidation | Project Owner | OD-01A/B; G3 criteria | G3 gate decision | Gate record with entry/exit evidence | Gate review |
| E-04 / G4 | GATE | G3 not approved | Ledger line 17; contract AC-21 | Keep blocked; require written G4 authorization | Project Owner | G3 approval | Written G4 authorization | Written authorization exists after G3 | Gate record |
| E-05 / G3-RV-01 | GATE | No reference version or manifest | Ledger line 16; OD-01B §7 | Execute after D-06/D-07 and reference data | Project Owner | D-06/D-07; signatures | Separate G3-RV-01 authorization | Artifact with owner, version, hashes, source evidence, T-75/T-76/T-78, refresh config | Artifact and hash verification |

---

## 7. Required Execution Sequence

| Order | Action ID | Action | Dependencies | Authorization Required |
|---|---|---|---|---|
| 1 | A-01 / GOV-D-04 | Create owner-confirmation addendum citing contract v1.5 and OD-01A/B v0.2 | C-04; contract status | GOV-D-04 |
| 2 | D-02 / C-04 | Correct confirmation v1.4 vs contract v1.5 references | GOV-D-04 | GOV-D-04 |
| 3 | C-03 / GOV-B-05 | Create addendum superseding stale confirmation statements | GOV-D-04 | GOV-D-04 |
| 4 | A-02 / GOV-D-05 | Decide BusinessModelClass treatment | OD-01B signature | GOV-D-05 |
| 5 | A-03 / GOV-D-06 | Approve staleness thresholds | G3-RV-01 | GOV-D-06 — Owner-accepted; formal governance approval PENDING |
| 6 | A-04 / GOV-D-07 | Approve ManifestHash canonicalization method | G3-RV-01; T-78 | GOV-D-07 — Owner-accepted; implementation NOT STARTED |
| 7 | A-05 / GOV-D-08 | Approve evidence-retention structure | GOV-D-08 | GOV-D-08 — Owner-accepted; implementation NOT STARTED |
| 8 | C-01 / GOV-B-03 | Update stale residual row | None | D-03 recorded |
| 9 | C-02 / GOV-B-04 | Complete owner initials/date and CC evidence reference | M-07 | Signature-time completion |
| 10 | C-06 / OD01B-B-08 | Assign named reviewer or record signed D-02 limitation | M-07 | Owner decision |
| 11 | D-03 / C-05 | Propagate six-status vocabulary | H-05 | New authorization |
| 12 | D-04 / C-06 | Exclude or explicitly approve AirlineId allocation | M-12 | New authorization |
| 13 | D-05 / C-07 | State no-Values condition in OD-01B approval block | GOV-D-05 | GOV-D-05 |
| 14 | D-06 / C-08 | Update residual rows to current per-finding results | Re-audit acceptance | New authorization |
| 15 | D-07 / C-09 | State contract is not approved; complete contract review | Contract review | New authorization |
| 16 | D-08 / C-10 | Correct ledger test summary to 71/8/0 | H-05 | New authorization |
| 17 | E-01 / OD-01A | Sign OD-01A with actual date and evidence | A/B/C/D items complete | Owner signature |
| 18 | E-02 / OD-01B | Sign OD-01B after OD-01A with actual date and evidence | A/B/C/D items; OD-01A | Owner signature |
| 19 | E-03 / G3 | Hold gate review | OD-01A/B; G3 criteria | G3 gate decision |
| 20 | E-05 / G3-RV-01 | Execute G3-RV-01 | D-06/D-07; signatures | Separate G3-RV-01 authorization |

---

## 8. Authorization Boundaries

| Action | Who Can Authorize | What It Authorizes | What It Does NOT Authorize |
|---|---|---|---|
| Owner decision (A-01 through A-05) | Project Owner only | Decision recorded; scope defined | Data generation, schema freeze, Power BI implementation |
| Document correction (C-01 through C-10) | Project Owner (controlled change) | Text corrected; hashes recomputed | Data generation, Power BI implementation |
| OD-01A/OD-01B signature (E-01, E-02) | Project Owner only | Decision formally approved | Reference-data creation, synthetic data, G3/G4 advancement |
| G3-RV-01 (E-05) | Project Owner | Reference version approved | Data generation, Power BI implementation |
| G4 authorization (E-04) | Project Owner only | Data generation authorized | Schema freeze; reference-version approval |

---

## 9. End of Register

This document is remediation-action register evidence only. No source files, data, DAX, PBIX, or report pages were modified during its creation. No action in this register has been completed; all actions remain pending owner decision or execution.
