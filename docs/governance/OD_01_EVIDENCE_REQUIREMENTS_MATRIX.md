# OD-01 Evidence Requirements Matrix

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** OD-01-ERM-2026-11-06-001  
**Document Type:** Evidence Requirements Matrix  
**Status:** COMPLETE — READY FOR OWNER REVIEW  
**Prepared:** 2026-11-06  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Evidence Requirements Matrix Purpose

This matrix specifies every evidence element required for each governance decision (OD-01A, OD-01B, OD-04, G3-RV-01, Schema Freeze, G3, G4, Independent Reviewer) before it can reach `FORMALLY APPROVED` status. Evidence elements are categorized as:

- **Signature elements** — Owner signature, approval date
- **Reviewer elements** — Reviewer name, role, organization, independence, result, signature/date
- **Evidence references** — Scope hash, contract hash, re-audit record, compensating-control evidence
- **Retention elements** — Signed-copy path, signed-copy hash, retention confirmation
- **Verification elements** — Verification date/result

No evidence element has been completed for any decision. All signature fields are blank.

---

## 2. OD-01A — Airline Population Evidence Requirements

| Evidence Element | Required | Current Status | Source Document | Owner Decision |
|---|---|---|---|---|
| Owner signature | Yes | Missing | OD01A Section 7.4 | KH Mohammad Farhan |
| Approval date | Required | Missing | OD01A Section 7.4 | KH Mohammad Farhan |
| Reviewer route documented | Required | Documented (compensating control) | OD01A Section 7.2 | Project Owner |
| Reviewer limitation statement | Required | Documented | OD01A Section 7.2 | Project Owner |
| Reviewer name/role/organization | Required if assigned | Not assigned | OD01A Section 7.4 | Project Owner |
| Reviewer independence | Required | N/A (no reviewer) | OD01A Section 7.4 | Project Owner |
| Reviewer result | Required if reviewer assigned | N/A (no reviewer) | OD01A Section 7.4 | Project Owner |
| Reviewer signature/date | Required if reviewer assigned | N/A (no reviewer) | OD01A Section 7.4 | Project Owner |
| Residual concerns recorded | Required | Documented | OD01A Section 7.4 | Project Owner |
| Re-audit record | Required | PENDING | OD01A Section 7.1 | Project Owner |
| Scope v1.1 SHA-256 | Required | Recorded | OD01A Section 7.4 | Project Owner |
| Contract v1.5 SHA-256 | Required | Recorded | OD01A Section 7.4 | Project Owner |
| Signed-copy path | Required | Missing | D-08 PENDING | Project Owner |
| Signed-copy SHA-256 | Required | Missing | No signed copy exists | Project Owner |
| Retention confirmed | Required | Not confirmed | D-08 PENDING | Project Owner |
| Verification date/result | Required | PENDING | OD01A Section 7.4 | Project Owner |

---

## 3. OD-01B — Airline Identity and Reference Evidence Requirements

| Evidence Element | Required | Current Status | Source Document | Owner Decision |
|---|---|---|---|---|
| Owner signature | Required | Missing | OD01B Section 11.4 | KH Mohammad Farhan |
| Approval date | Required | Missing | OD01B Section 11.4 | KH Mohammad Farhan |
| Reviewer route documented | Required | Documented (compensating control) | OD01B Section 11.2 | Project Owner |
| Reviewer limitation statement | Required | Documented | OD01B Section 11.2 | Project Owner |
| Reviewer name/role/organization | Required if assigned | Not assigned | OD01B Section 11.4 | Project Owner |
| Reviewer independence | Required | N/A (no reviewer) | OD01B Section 11.4 | Project Owner |
| Reviewer result | Required if reviewer assigned | N/A (no reviewer) | OD01B Section 7.4 | Project Owner |
| Reviewer signature/date | Required if reviewer assigned | N/A (no reviewer) | OD01B Section 7.4 | Project Owner |
| Residual concerns recorded | Required | Documented | OD01B Section 11.4 | Project Owner |
| Re-audit record | Required | PENDING | OD01B Section 11.1 | Project Owner |
| Scope v1.1 SHA-256 | Required | Recorded | OD01B Section 7.4 | Project Owner |
| Contract v1.5 SHA-256 | Required | Recorded | OD01B Section 7.4 | Project Owner |
| Signed-copy path | Required | Missing | D-08 PENDING | Project Owner |
| Signed-copy SHA-256 | Required | Missing | No signed copy exists | Project Owner |
| Retention confirmed | Required | Not confirmed | D-08 PENDING | Project Owner |
| Verification date/result | Required | PENDING | OD01B Section 7.4 | Project Owner |

---

## 4. OD-04 — Exchange-Rate Policy Evidence Requirements

| Evidence Element | Required | Current Status | Source Document | Owner Decision |
|---|---|---|---|---|
| Owner signature | Required | Missing | OD04_OWNER_DECISION_PACKAGE.md Section 2 | KH Mohammad Farhan |
| Approval date | Required | Missing | OD04_OWNER_DECISION_PACKAGE.md Section 2 | KH Mohammad Farhan |
| OD-04a selection | Required | Missing | Option 1/2/3 selection | Project Owner |
| OD-04b selection | Required | Missing | Convention confirmation | Project Owner |
| OD-04c selection | Required | Missing | RateSource value | Project Owner |
| OD-04d selection | Required | Missing | RateVersion value | Project Owner |
| OD-04e selection | Required | Missing | Missing-date behaviour | Project Owner |
| OD-04f selection | Required | Missing | Methodology selection | Project Owner |
| Currency mismatch resolution | Required | Missing | 5 vs 8 currency alignment | Project Owner |
| Rate coverage period | Required | Missing | Date range for rate generation | Project Owner |
| Individual rate values/methodology | Required | Missing | Owner-approved rates or algorithm | Project Owner |
| Signed-copy path | Required | Missing | D-08 PENDING | Project Owner |
| Signed-copy SHA-256 | Required | Missing | No signed copy exists | Project Owner |
| Retention confirmed | Required | Not confirmed | D-08 PENDING | Project Owner |
| Verification date/result | Required | PENDING | OD04 Section 2 | Project Owner |

---

## 5. G3-RV-01 — Reference Version Approval Evidence Requirements

| Evidence Element | Required | Current Status | Source Document | Owner Decision |
|---|---|---|---|---|
| Owner signature | Required | Missing | OD01A Section 7; OD01B Section 11 | KH Mohammad Farhan |
| Approval date | Required | Missing | OD01A Section 7; OD01B Section 11 | KH Mohammad Farhan |
| ReferenceVersion value | Required | Not assigned | Format AIR-YYYY-MM-DD-NNN | Project Owner |
| ManifestHash | Required | Not computed | SHA-256 of reference/provenance files | Project Owner |
| SupersedesReferenceVersion | Required if applicable | Not applicable (first version) | OD01B Section 7 | Project Owner |
| ReconciliationNote | Required if identity change | Not applicable (first version) | OD01B Section 7 | Project Owner |
| T-75 results | Required | NOT EXECUTED | qa/results/ | Project Owner |
| T-76 results | Required | NOT EXECUTED | qa/results/ | Project Owner |
| T-78 results | Required | NOT EXECUTED | qa/results/airline_identity_versions.csv | Project Owner |
| Refresh configuration | Required | Not documented | OD01B Section 7 | Project Owner |
| Signed-copy path | Required | Missing | D-08 PENDING | Project Owner |
| Retention confirmed | Required | Not confirmed | D-08 PENDING | Project Owner |

---

## 6. Schema Freeze — Evidence Requirements

| Evidence Element | Required | Current Status | Source Document | Owner Decision |
|---|---|---|---|---|
| Owner signature | Required | Missing | PROGRESS_LEDGER.md; OD01A Section 7 | KH Mohammad Farhan |
| Approval date | Required | Missing | PROGRESS_LEDGER.md; OD01B Section 11 | KH Mohammad Farhan |
| Contract version | Required | v1.5 | docs/03_DATA_CONTRACTS.md | Project Owner |
| Schema hash | Required | Not computed | To be computed at freeze | Project Owner |
| Signed-copy path | Required | Missing | D-08 PENDING | Project Owner |
| Retention confirmed | Required | Not confirmed | D-08 PENDING | Project Owner |

---

## 7. G3 — Data Design Formal Approval Evidence Requirements

| Evidence Element | Required | Current Status | Source Document | Owner Decision |
|---|---|---|---|---|
| Owner signature | Required | Missing | PROGRESS_LEDGER.md | KH Mohammad Farhan |
| Approval date | Required | Missing | PROGRESS_LEDGER.md | KH Mohammad Farhan |
| Gate review evidence | Required | Not held | No G3 gate review conducted | Project Owner |
| OD-01A/OD-01B approval | Required | PENDING | Depend on OD-01A/OD-01B | Project Owner |
| G3-RV-01 approval | Required | NOT EXECUTED | Depend on G3-RV-01 | Project Owner |
| Schema freeze | Required | NOT AUTHORIZED | Depend on schema freeze | Project Owner |
| Validation implementation | Required | NOT STARTED | No validation code executed | Project Owner |
| Signed-copy path | Required | Missing | D-08 PENDING | Project Owner |
| Retention confirmed | Required | Not confirmed | D-08 PENDING | Project Owner |

---

## 8. G4 — Data Generation Authorization Evidence Requirements

| Evidence Element | Required | Current Status | Source Document | Owner Decision |
|---|---|---|---|---|
| Owner signature | Required | Missing | PROGRESS_LEDGER.md | KH Mohammad Farhan |
| Approval date | Required | Missing | PROGRESS_LEDGER.md | KH Mohammad Farhan |
| G3 APPROVED | Required | NOT FORMALLY APPROVED | Depend on G3 | Project Owner |
| Authorized datasets | Required | Not specified | To be specified at authorization | Project Owner |
| Authorized reference version | Required | Not specified | Depend on G3-RV-01 | Project Owner |
| Signed-copy path | Required | Missing | D-08 PENDING | Project Owner |
| Retention confirmed | Required | Not confirmed | D-08 PENDING | Project Owner |

---

## 9. Independent Reviewer — Evidence Requirements

| Evidence Element | Required | Current Status | Source Document | Owner Decision |
|---|---|---|---|---|
| Reviewer name | Required if independent review | Not assigned | OWNER_DECISIONS_2026-11-04.md | Project Owner |
| Reviewer role/organization | Required if assigned | Not assigned | OWNER_DECISIONS_2026-11-04.md | Project Owner |
| Reviewer independence | Required | N/A (no reviewer) | OWNER_DECISIONS_2026-11-04.md | Project Owner |
| Reviewer result | Required if reviewer assigned | N/A (no reviewer) | OWNER_DECISIONS_2026-11-04.md | Project Owner |
| Compensating-control acceptance | Required if no reviewer | Accepted but not executed | OWNER_DECISIONS_2026-11-04.md | Project Owner |

---

## 10. Evidence Readiness Summary

| Decision ID | Evidence Elements Required | Evidence Elements Present | Evidence Elements Missing | Readiness |
|---|---|---|---|---|
| OD-01A | 17 | 2 (scope hash, contract hash) | 15 | NOT READY |
| OD-01B | 17 | 2 (scope hash, contract hash) | 15 | NOT READY |
| OD-04 | 17 | 0 | 17 | NOT READY |
| G3-RV-01 | 10 | 0 | 10 | NOT READY |
| Schema Freeze | 6 | 1 (contract version) | 5 | NOT READY |
| G3 | 9 | 0 | 9 | NOT READY |
| G4 | 7 | 0 | 7 | NOT READY |
| Independent Reviewer | 5 | 0 | 5 | NOT READY |
| **Total** | **88** | **4** | **84** | **NOT READY** |

---

## 11. Evidence Gaps by Category

### Signature Elements (Missing for all decisions)
- Owner signature — blank on all decision records
- Approval date — blank on all decision records

### Reviewer Elements (Missing for all decisions)
- Reviewer name/role/organization — not assigned
- Reviewer independence — N/A (no reviewer)
- Reviewer result — N/A (no reviewer)
- Reviewer signature/date — blank

### Evidence References (Partially complete)
- Scope v1.1 SHA-256 — present on OD-01A and OD-01B
- Contract v1.5 SHA-256 — present on OD-01A and OD-01B
- Re-audit record — PENDING on all decisions

### Retention Elements (Missing for all decisions)
- Signed-copy path — missing on all decision records
- Signed-copy SHA-256 — missing on all decision records
- Retention confirmed — not confirmed on all decision records

### Verification Elements (Missing for all decisions)
- Verification date/result — PENDING on all decision records

---

## 12. End of Evidence Requirements Matrix

This document is evidence-requirements evidence only. No source files, data, DAX, PBIX, or report pages were modified during its creation. No evidence element has been completed; all 88 required evidence elements across 8 decisions remain missing or incomplete.
