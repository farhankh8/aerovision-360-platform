# GOVERNANCE APPROVAL MATRIX — AEROVISION 360

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** GD-AM-2026-11-06-001  
**Document Type:** Governance Approval Matrix  
**Status:** COMPLETE — READY FOR OWNER REVIEW  
**Prepared:** 2026-11-06  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Approval Matrix Overview

| Decision ID | Decision | Classification | Formal Signature | Approval Date | Reviewer Assigned | Evidence Required | Downstream Blocked Until Approved |
|---|---|---|---|---|---|---|---|
| OD-01A | Airline population | OWNER-DIRECTED | No | No | No | Signed decision record; re-audit preconditions; scope/contract hashes; compensating-control evidence | G3, reference data, all generation |
| OD-01B | Airline identity/reference | OWNER-DIRECTED | No | No | No | Signed decision record; re-audit preconditions; scope/contract hashes; compensating-control evidence | G3-RV-01, key map approval |
| OD-04 | Exchange-rate policy | OWNER-DIRECTED | No | No | No | Signed decision record; all 7 sub-decisions; currency mismatch resolution | FactBookingTransactions, FactOperatingCosts, Page 03 |
| OD-04a | Currency scope | OWNER-DIRECTED | No | No | No | Option 1/2/3 selection; currency mismatch resolution | Referential integrity for financial facts |
| OD-04b | Exchange-rate convention | OWNER-DIRECTED | No | No | No | Convention confirmation (USD/unit; 6 decimals; exact-date; no forward-fill) | USD conversion definition |
| OD-04c | Rate source | OWNER-DIRECTED | No | No | No | RateSource value (3a/3b/3c) | ref_exchange_rates.csv creation |
| OD-04d | Rate version | OWNER-DIRECTED | No | No | No | RateVersion value (4a/4b/4c) | Rate versioning/reproducibility |
| OD-04e | Missing-date behaviour | OWNER-DIRECTED | No | No | No | Behaviour selection (5a/5b/5c) | Missing-date handling rule |
| OD-04f | Rate-generation methodology | OWNER-DIRECTED | No | No | No | Methodology selection (6a/6b/6c) | Rate value determination |
| G3-RV-01 | Reference version approval | NOT READY | No | No | No | Approved manifest; key map; T-75/T-76/T-78 results | Reference data creation; model refresh |
| Schema freeze | Schema authorization | NOT READY | No | No | No | Written freeze record; contract/schema hash | Power Query/model build |
| G3 | Data design formal approval | NOT READY | No | No | No | Gate review APPROVED; OD-01A/OD-01B; G3-RV-01; schema freeze | G4 authorization |
| G4 | Data generation authorization | NOT READY | No | No | No | Written G4 authorization; G3 APPROVED | All data generation |
| Independent reviewer | Reviewer assignment | NOT READY | No | No | No | Named reviewer or documented compensating control | All QA PASS decisions |

---

## 2. Approval Evidence Requirements by Decision

### 2.1 OD-01A — Airline Population

| Evidence Element | Required | Current Status | Source Document |
|---|---|---|---|
| Owner signature | Required | Missing | OD01A_AIRLINE_POPULATION_DECISION.md Section 7.4 |
| Approval date | Required | Missing | OD01A_AIRLINE_POPULATION_DECISION.md Section 7.4 |
| Reviewer route | Required | Documented (compensating control) | OD01A Section 7.2 |
| Reviewer limitation statement | Required | Documented | OD01A Section 7.2 |
| Reviewer name/role/organization | Required if assigned | Not assigned | OD01A Section 7.4 |
| Reviewer independence | Required | N/A (no reviewer) | OD01A Section 7.4 |
| Reviewer result | Required if reviewer assigned | N/A (no reviewer) | OD01A Section 7.4 |
| Residual concerns | Required | Documented | OD01A Section 7.4 |
| Re-audit record | Required | PENDING | OD01A Section 7.1 |
| Scope v1.1 SHA-256 | Required | Recorded | 9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C |
| Contract v1.5 SHA-256 | Required | Recorded | D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9 |
| Signed-copy path | Required | Missing | D-08 PENDING |
| Signed-copy SHA-256 | Required | Missing | No signed copy exists |
| Retention confirmed | Required | Not confirmed | D-08 PENDING |
| Verification date/result | Required | PENDING | OD01A Section 7.4 |

### 2.2 OD-01B — Airline Identity and Reference

| Evidence Element | Required | Current Status | Source Document |
|---|---|---|---|
| Owner signature | Required | Missing | OD01B Section 11.4 |
| Approval date | Required | Missing | OD01B Section 11.4 |
| Reviewer route | Required | Documented (compensating control) | OD01B Section 11.2 |
| Reviewer limitation statement | Required | Documented | OD01B Section 11.2 |
| Reviewer name/role/organization | Required if assigned | Not assigned | OD01B Section 11.4 |
| Reviewer independence | Required | N/A (no reviewer) | OD01B Section 11.4 |
| Reviewer result | Required if reviewer assigned | N/A (no reviewer) | OD01B Section 11.4 |
| Residual concerns | Required | Documented | OD01B Section 11.2 |
| Re-audit record | Required | PENDING | OD01B Section 11.1 |
| Scope v1.1 SHA-256 | Required | Recorded | 9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C |
| Contract v1.5 SHA-256 | Required | Recorded | D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9 |
| Signed-copy path | Required | Missing | D-08 PENDING |
| Signed-copy SHA-256 | Required | Missing | No signed copy exists |
| Retention confirmed | Required | Not confirmed | D-08 PENDING |
| Verification date/result | Required | PENDING | OD01B Section 11.4 |

### 2.3 OD-04 — Exchange-Rate Policy

| Evidence Element | Required | Current Status | Source Document |
|---|---|---|---|
| Owner signature | Required | Missing | OD04_OWNER_DECISION_PACKAGE.md Section 2 |
| Approval date | Required | Missing | OD04_OWNER_DECISION_PACKAGE.md Section 2 |
| OD-04a selection | Required | Missing | Option 1/2/3 selection |
| OD-04b selection | Required | Missing | Convention confirmation |
| OD-04c selection | Required | Missing | RateSource value |
| OD-04d selection | Required | Missing | RateVersion value |
| OD-04e selection | Required | Missing | Missing-date behaviour |
| OD-04f selection | Required | Missing | Methodology selection |
| Currency mismatch resolution | Required | Missing | 5 vs 8 currency alignment |
| Rate coverage period | Required | Missing | Date range for rate generation |
| Individual rate values/methodology | Required | Missing | Owner-approved rates or algorithm |
| Signed-copy path | Required | Missing | D-08 PENDING |
| Signed-copy SHA-256 | Required | Missing | No signed copy exists |
| Retention confirmed | Required | Not confirmed | D-08 PENDING |
| Verification date/result | Required | PENDING | OD04 Section 2 |

### 2.4 G3-RV-01 — Reference Version Approval

| Evidence Element | Required | Current Status | Source Document |
|---|---|---|---|
| Owner signature | Required | Missing | OD01A Section 7; OD01B Section 11 |
| Approval date | Required | Missing | OD01A Section 7; OD01B Section 11 |
| ReferenceVersion value | Required | Not assigned | Format AIR-YYYY-MM-DD-NNN |
| ManifestHash | Required | Not computed | SHA-256 of reference/provenance files |
| SupersedesReferenceVersion | Required if applicable | Not applicable (first version) | OD01B Section 7 |
| ReconciliationNote | Required if identity change | Not applicable (first version) | OD01B Section 7 |
| T-75 results | Required | NOT EXECUTED | qa/results/ |
| T-76 results | Required | NOT EXECUTED | qa/results/ |
| T-78 results | Required | NOT EXECUTED | qa/results/airline_identity_versions.csv |
| Refresh configuration | Required | Not documented | OD01B Section 7 |
| Signed-copy path | Required | Missing | D-08 PENDING |
| Retention confirmed | Required | Not confirmed | D-08 PENDING |

### 2.5 Schema Freeze

| Evidence Element | Required | Current Status | Source Document |
|---|---|---|---|
| Owner signature | Required | Missing | PROGRESS_LEDGER.md; OD01A Section 7 |
| Approval date | Required | Missing | PROGRESS_LEDGER.md; OD01B Section 11 |
| Contract version | Required | v1.5 | docs/03_DATA_CONTRACTS.md |
| Schema hash | Required | Not computed | To be computed at freeze |
| Signed-copy path | Required | Missing | D-08 PENDING |
| Retention confirmed | Required | Not confirmed | D-08 PENDING |

### 2.6 G3 — Data Design Formal Approval

| Evidence Element | Required | Current Status | Source Document |
|---|---|---|---|
| Owner signature | Required | Missing | PROGRESS_LEDGER.md |
| Approval date | Required | Missing | PROGRESS_LEDGER.md |
| Gate review evidence | Required | Not held | No G3 gate review conducted |
| OD-01A/OD-01B approval | Required | PENDING | Depend on OD-01A/OD-01B |
| G3-RV-01 approval | Required | NOT EXECUTED | Depend on G3-RV-01 |
| Schema freeze | Required | NOT AUTHORIZED | Depend on schema freeze |
| Validation implementation | Required | NOT STARTED | No validation code executed |
| Signed-copy path | Required | Missing | D-08 PENDING |
| Retention confirmed | Required | Not confirmed | D-08 PENDING |

### 2.7 G4 — Data Generation Authorization

| Evidence Element | Required | Current Status | Source Document |
|---|---|---|---|
| Owner signature | Required | Missing | PROGRESS_LEDGER.md |
| Approval date | Required | Missing | PROGRESS_LEDGER.md |
| G3 APPROVED | Required | NOT FORMALLY APPROVED | Depend on G3 |
| Authorized datasets | Required | Not specified | To be specified at authorization |
| Authorized reference version | Required | Not specified | Depend on G3-RV-01 |
| Signed-copy path | Required | Missing | D-08 PENDING |
| Retention confirmed | Required | Not confirmed | D-08 PENDING |

### 2.8 Independent Reviewer

| Evidence Element | Required | Current Status | Source Document |
|---|---|---|---|
| Reviewer name | Required if independent review | Not assigned | OWNER_DECISIONS_2026-11-04.md |
| Reviewer role/organization | Required if assigned | Not assigned | OWNER_DECISIONS_2026-11-04.md |
| Reviewer independence | Required | N/A (no reviewer) | OWNER_DECISIONS_2026-11-04.md |
| Reviewer result | Required if reviewer assigned | N/A (no reviewer) | OWNER_DECISIONS_2026-11-04.md |
| Compensating-control acceptance | Required if no reviewer | Accepted but not executed | OWNER_DECISIONS_2026-11-04.md |

---

## 3. Approval Evidence Checklist by Decision

Each decision requires the following evidence elements to be marked `FORMALLY APPROVED`:

| Evidence Element | OD-01A | OD-01B | OD-04 | G3-RV-01 | Schema Freeze | G3 | G4 | Independent Reviewer |
|---|---|---|---|---|---|---|---|---|
| Owner signature | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Approval date | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Reviewer route documented | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Reviewer limitation statement | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Reviewer name/role/org | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Reviewer independence | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Reviewer result | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Reviewer signature/date | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Residual concerns recorded | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Re-audit record | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Scope v1.1 SHA-256 | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Contract v1.5 SHA-256 | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Signed-copy path | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Signed-copy SHA-256 | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Retention confirmed | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Verification date/result | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

---

## 3. Approval Dependencies

```
OD-01A signature ──────────────────┐
OD-01B signature ──────────────────┼──→ G3-RV-01 ───────────────┐
OD-04 approval (7 sub-decisions) ──┼──→ Schema freeze ───────────┤
Currency mismatch resolution ──────┤                              │
G3-RV-01 execution ────────────────┤                              ▼
Schema freeze written record ──────┴──────────────────────→ G3 formal approval ──→ G4 written authorization ──→ Data generation ──→ Semantic model build ──→ DAX measures ──→ Report pages ──→ QA tests ──→ Release
Independent reviewer assignment ──────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Critical path:** OD-01A/OD-01B → OD-04 → G3-RV-01 → Schema freeze → G3 → G4 → Data generation

**Parallel considerations:** Page 02, 04, 05, 06 design specifications are complete and measures are verified against source data; these pages can be built in Power BI Desktop once the semantic model has the 3 existing facts and 10 measures (which are already specified).

---

## 3. Alignment with Master Blocker Register

| Matrix Decision | Blocker ID | Blocker Status | Alignment |
|---|---|---|---|
| OD-01A | CB-01 | OPEN | Aligned — signature pending |
| OD-01B | CB-02 | OPEN | Aligned — signature pending |
| OD-04 | CB-03 | OPEN | Aligned — approval pending |
| OD-04a | CB-04 | OPEN | Aligned — currency mismatch unresolved |
| G3-RV-01 | CB-05 | OPEN | Aligned — execution pending |
| Schema freeze | CB-06 | OPEN | Aligned — authorization pending |
| G3 | CB-07 | OPEN | Aligned — formal approval pending |
| G4 | CB-08 | OPEN | Aligned — authorization pending |
| Independent reviewer | CB-09 | OPEN | Aligned — reviewer not assigned |

---

## 4. End of Approval Matrix

This document is approval-matrix evidence only. No source files, data, DAX, PBIX, or report pages were modified during its creation. No decision is formally approved; no signature or approval date is recorded.
