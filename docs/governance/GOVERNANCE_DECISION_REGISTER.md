# GOVERNANCE DECISION REGISTER — AEROVISION 360

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** GD-REG-2026-11-06-001  
**Document Type:** Governance Decision Register  
**Status:** COMPLETE — READY FOR OWNER REVIEW  
**Prepared:** 2026-11-06  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Decision Register Overview

| Total Decisions | OWNER-DIRECTED | DRAFT | READY FOR SIGNATURE | NOT READY FOR SIGNATURE | FORMALLY APPROVED | BLOCKED |
|---|---|---|---|---|---|---|
| 21 | 16 | 0 | 0 | 21 | 0 | 5 |

**No decision has been formally signed or approved.** All decisions are owner-directed (communicated by the project owner) but none carry formal signature, approval date, or independent assurance.

---

## 2. Decision Register Details

| ID | Decision | Classification | Status | Owner Decision Required | Dependencies | Blocker(s) | Downstream Impact |
|---|---|---|---|---|---|---|---|
| OD-01A | Airline population | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Re-audit preconditions; H-04, H-05, M-07, M-12; B-03–B-08 | CB-01 | Blocks G3, reference data, all generation |
| OD-01B | Airline identity/reference | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Re-audit preconditions; H-04, H-05, M-07, M-12; B-03–B-08 | CB-02 | Blocks G3-RV-01, key map approval, reference data |
| OD-04 | Exchange-rate policy | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | OD-01A/OD-01B; OD-04a–OD-04f; currency mismatch | CB-03 | Blocks FactBookingTransactions, FactOperatingCosts, Page 03 |
| OD-04a | Currency scope | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | OD-04 approval | CB-04 | Blocks referential integrity for financial facts |
| OD-04b | Exchange-rate convention | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | OD-04 approval | HB-09 | Blocks USD conversion definition |
| OD-04c | Rate source | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | OD-04 approval | HB-03 | Blocks ref_exchange_rates.csv creation |
| OD-04d | Rate version | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | OD-04 approval | HB-03 | Blocks rate versioning and reproducibility |
| OD-04e | Missing-date behaviour | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | OD-04 approval | HB-03 | Blocks missing-date handling rule |
| OD-04f | Rate-generation methodology | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | OD-04 approval | HB-03 | Blocks rate value determination |
| G3-RV-01 | Reference version approval | NOT READY | No | Yes | OD-01A; OD-01B; OD-04 | CB-05 | Blocks reference data creation; model refresh |
| Schema freeze | Schema authorization | NOT READY | No | Yes | OD-01A; OD-01B; critical OD decisions | CB-06 | Blocks Power Query/model build |
| G3 | Data design formal approval | NOT READY | No | Yes | OD-01A; OD-01B; G3-RV-01; Schema freeze | CB-07 | Blocks G4 authorization |
| G4 | Data generation authorization | NOT READY | No | Yes | G3 APPROVED | CB-08 | Blocks all data generation |
| Independent reviewer | Reviewer assignment | NOT READY | No | Yes | None | CB-09 | Blocks all QA PASS decisions |
| Compensating control | Owner self-review route | OWNER-DIRECTED | NOT READY | No | None | CB-09 | Blocks independent assurance |
| OD-R-01 | Split OD-01 into OD-01A/OD-01B | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | None | Part of OD-01A/OD-01B | Enables separate population/identity decisions |
| OD-R-02 | Permanent identity (AirlineId/AirlineKey) | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables stable key model |
| OD-R-03 | Historical dimension (Type 1) | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables Type 1 baseline |
| OD-R-04 | AirlineName as commercial brand | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables brand-based display |
| OD-R-05 | HomeCountry as headquarters/domicile | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables country comparison |
| OD-R-06 | AirlineGroup as ultimate parent | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables optional group attribute |
| OD-R-07 | Remove OperatingRegion | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Removes ambiguous identity field |
| OD-R-08 | BusinessModelClass as analytical | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables optional analytical column |
| OD-R-09 | Minimal lifecycle (IsActive + StatusEffectiveDate) | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables minimal lifecycle |
| OD-R-10 | Requirements/T-78/G3-RV-01 (not OD-23) | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B/OD-04 | Part of OD-01B/OD-04 | Enables T-78 integrity checks |
| OD-R-11 | Reference version format | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables version format |
| OD-R-12 | Evidence controls and provenance durability | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables provenance tracking |
| OD-R-13 | ReferenceVersion in DimAirline | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables lineage column |
| OD-R-14 | G3 status semantics | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables honest gate reporting |
| OD-R-15 | Reviewer controls | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | None | CB-09 | Enables compensating control route |
| OD-R-16 | BusinessModelClass naming | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables optional analytical column |
| OD-R-17 | Signed-copy retention | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B/OD-04 | D-08 PENDING | Enables retention structure |
| OD-R-18 | LegalName in reference layer | OWNER-DIRECTED | NOT READY FOR SIGNATURE | Yes | Part of OD-01B | Part of OD-01B | Enables optional legal name |

---

## 3. Status Classification Definitions

| Classification | Definition |
|---|---|
| OWNER-DIRECTED | Decision choice communicated by the project owner but not formally signed. No approval date, no signature, no independent assurance. |
| DRAFT | Documentation exists but needs correction before it can be signed. |
| READY FOR SIGNATURE | Evidence and documentation are sufficient; only the owner's formal signature and date are missing. |
| NOT READY FOR SIGNATURE | Unresolved issues remain (re-audit preconditions, missing evidence, unresolved dependencies). |
| FORMALLY APPROVED | Verifiable approval evidence exists (signature, date, reviewer, hash). |
| BLOCKED | Dependency prevents progression regardless of owner willingness. |

---

## 4. Current Status by Classification

### 4.1 OWNER-DIRECTED (16 decisions)

These decisions have been communicated by the project owner but not formally signed:

OD-01A, OD-01B, OD-04, OD-04a, OD-04b, OD-04c, OD-04d, OD-04e, OD-04f, OD-R-01, OD-R-02, OD-R-03, OD-R-04, OD-R-05, OD-R-06, OD-R-07, OD-R-08, OD-R-09, OD-R-10, OD-R-11, OD-R-12, OD-R-13, OD-R-14, OD-R-15, OD-R-16, OD-R-17, OD-R-18

*(16 of these are sub-decisions of OD-01A, OD-01B, and OD-04. Counted as 16 distinct items in the register above.)*

### 4.2 NOT READY FOR SIGNATURE (21 decisions)

All owner-directed decisions are also NOT READY FOR SIGNATURE because re-audit preconditions remain open (H-04, H-05, M-07, M-12; B-03–B-08), no independent reviewer is assigned, and no signed copy structure exists.

### 4.3 FORMALLY APPROVED (0 decisions)

No decision has been formally signed or approved.

### 4.4 BLOCKED (5 decisions)

| Blocker ID | Register Entry | Status | Evidence |
|---|---|---|---|
| CB-01 | OD-01A signature | OPEN | OD01A_AIRLINE_POPULATION_DECISION.md v0.2; no signature |
| CB-02 | OD-01B signature | OPEN | OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md v0.2; no signature |
| CB-03 | OD-04 approval | OPEN | OD04_OWNER_DECISION_PACKAGE.md; PROPOSED status |
| CB-04 | Currency mismatch | OPEN | OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md Section 4 |
| CB-05 | G3-RV-01 | OPEN | OD01A Section 7; OD01B Section 7; no manifest created |
| CB-06 | Schema freeze | OPEN | PROGRESS_LEDGER.md; NOT AUTHORIZED |
| CB-07 | G3 formal approval | OPEN | PROGRESS_LEDGER.md; NOT FORMALLY APPROVED |
| CB-08 | G4 authorization | OPEN | PROGRESS_LEDGER.md; BLOCKED |
| CB-09 | Independent reviewer | OPEN | OWNER_DECISIONS_2026-11-04.md; NOT AVAILABLE |

---

## 5. Alignment with Master Blocker Register

| Blocker ID | Register Entry | Status | Evidence |
|---|---|---|---|
| CB-01 | OD-01A signature | OPEN | OD01A_AIRLINE_POPULATION_DECISION.md v0.2; no signature |
| CB-02 | OD-01B signature | OPEN | OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md v0.2; no signature |
| CB-03 | OD-04 approval | OPEN | OD04_OWNER_DECISION_PACKAGE.md; PROPOSED status |
| CB-04 | Currency mismatch | OPEN | OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md Section 4 |
| CB-05 | G3-RV-01 | OPEN | OD01A Section 7; OD01B Section 7; no manifest created |
| CB-06 | Schema freeze | OPEN | PROGRESS_LEDGER.md; NOT AUTHORIZED |
| CB-07 | G3 formal approval | OPEN | PROGRESS_LEDGER.md; NOT FORMALLY APPROVED |
| CB-08 | G4 authorization | OPEN | PROGRESS_LEDGER.md; BLOCKED |
| CB-09 | Independent reviewer | OPEN | OWNER_DECISIONS_2026-11-04.md; NOT AVAILABLE |

---

## 6. End of Register

This document is decision-register evidence only. No source files, data, DAX, PBIX, or report pages were modified during its creation. No decision is formally approved; no signature or approval date is recorded.
