# OD-04 — Owner Decision Record: Currency and Exchange-Rate Policy

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** OD04-OA-2026-11-07-001  
**Document Type:** Owner Decision Record — Currency and Exchange-Rate Policy  
**Status:** OWNER ACCEPTED — FORMAL OD-04g APPROVAL PENDING OWNER SIGNATURE  
**Prepared:** 2026-11-07  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner:** KH Mohammad Farhan  
**Acceptance Basis:** Explicit project-owner confirmation in conversation, 2026-11-07  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Decision Identification

| Field | Value |
|---|---|
| Decision ID | OD-04 |
| Decision Title | Synthetic Exchange-Rate Policy for USD Conversion |
| Decision Basis | OD04_OWNER_DECISION_PACKAGE.md; OD04_OWNER_DECISION_BRIEF.md; 03_DATA_CONTRACTs.md Section 10; dim_currency.csv |
| Decision Date | 2026-11-07 |
| Acceptance Basis | Explicit project-owner confirmation in conversation, 2026-11-07 |

---

## 2. Accepted Decisions — OD-04a through OD-04f

The project owner has explicitly confirmed the following decisions:

| Decision ID | Question | Accepted Decision | Source Evidence |
|---|---|---|---|
| OD-04a | Currency scope | All 8 existing DimCurrency currencies: AED, QAR, SGD, INR, GBP, EUR, USD, AUD | data/03_curated/dim_currency.csv; data/manifests/dim_currency_manifest.json |
| OD-04b | Exchange-rate convention | USD per one unit of transaction currency; exact-date lookup; 6 decimal places; round final converted amount to 2 decimals; no forward-fill; no rate-period averaging | 03_DATA_CONTRACTs.md Section 10.2 |
| OD-04c | Rate source | AEROVISION-360-SYNTHETIC-FX-V1 | Owner-specified synthetic source identifier |
| OD-04d | Rate version | FX-YYYY-MM-DD-NNN date-based versioning | Consistent with AIR-YYYY-MM-DD-NNN airline reference-version format |
| OD-04e | Missing-date behaviour | No forward-fill; missing exact-date rate quarantines the affected financial row (DQ-08: High severity) | Data contract |
| OD-04f | Rate-generation methodology | Deterministic algorithmic generation; fixed seed; documented algorithm and parameters; reproducible output; explicitly synthetic; immutable versioned outputs | Project synthetic-data policy |
| OD-04h | Historical rate immutability | UNSPECIFIED | Requires future controlled clarification |
| OD-04i | Rate volatility bounds | UNSPECIFIED | Requires future controlled clarification |

OD-04h and OD-04i are deliberately excluded from the formal approval scope of OD-04a through OD-04f.

---

## 3. Approval Scope and Authorization Boundaries

### 3.1 Scope of OD-04g

OD-04g requests formal owner approval of the exchange-rate policy decisions OD-04a through OD-04f.

The approval scope includes:

- The eight-currency reporting scope.
- USD conversion convention.
- Synthetic rate source identifier.
- Date-based rate versioning.
- Missing-date quarantine behaviour.
- Deterministic rate-generation methodology.

### 3.2 Items not authorized by OD-04g alone

Formal approval of OD-04 does not independently authorize:

| Item | Authorization Status |
|---|---|
| G3-RV-01 execution | Requires its own prerequisites and authorization |
| Schema freeze | Requires separate owner authorization |
| G3 formal approval | Requires completion of its governance prerequisites |
| G4 data-generation authorization | Requires separate formal authorization |
| Production data promotion | Not authorized |
| Financial Power BI integration | Requires applicable governance and G4 authorization |

### 3.3 Existing implementation evidence

The project repository contains existing synthetic exchange-rate and financial fact-builder outputs.

Their existence is recorded as technical evidence only. This decision record does not retroactively authorize their creation, certify them as production data, or authorize their promotion or integration into the production Power BI model.

---

## 4. Formal Approval Record — OD-04g

**Decision ID:** OD-04g — Formal owner approval of OD-04  
**Decision title:** Formal approval of OD-04 Synthetic Exchange-Rate Policy  
**Decision owner / approver:** KH Mohammad Farhan  
**Formal status:** PENDING — OWNER SIGNATURE AND ACTUAL APPROVAL DATE REQUIRED

### 4.1 Decision Scope

| Decision ID | Accepted Decision | Status |
|---|---|---|
| OD-04a | Eight currencies: AED, QAR, SGD, INR, GBP, EUR, USD, AUD | Owner-confirmed |
| OD-04b | USD per one unit of transaction currency; exact-date lookup; six decimal places; final amount rounded to two decimals; no forward-fill or rate-period averaging | Owner-confirmed |
| OD-04c | AEROVISION-360-SYNTHETIC-FX-V1 | Owner-confirmed |
| OD-04d | FX-YYYY-MM-DD-NNN | Owner-confirmed |
| OD-04e | Missing exact-date rate quarantines the affected financial row | Owner-confirmed |
| OD-04f | Deterministic algorithmic generation using fixed seeds and reproducible outputs | Owner-confirmed |

### 4.2 Supporting Evidence

| Source Document | Location | Role |
|---|---|---|
| OD04_OWNER_DECISION_PACKAGE.md | Project root | Source decision package |
| OD04_OWNER_DECISION_BRIEF.md | docs/governance/ | Owner decision brief |
| 03_DATA_CONTRACTs.md | docs/ | Section 10: reporting currency and conversion rules |
| dim_currency.csv | data/03_curated/ | Eight-currency reference |
| dim_currency_manifest.json | data/manifests/ | Currency reference manifest |
| PAGE_03_REVENUE_FINANCE_READINESS.md | docs/ | Financial readiness evidence |

### 4.3 Known Limitations

| Decision ID | Detail | Status | Required Action |
|---|---|---|---|
| OD-04h | Historical rate immutability | UNSPECIFIED | Controlled clarification and future approval |
| OD-04i | Rate volatility bounds | UNSPECIFIED | Controlled clarification and future approval |

These limitations remain visible and must not be represented as approved requirements.

### 4.4 Formal Approval Statement

I, KH Mohammad Farhan, as Project Owner and Approver for AEROVISION 360, formally approve OD-04 — Synthetic Exchange-Rate Policy for USD Conversion, comprising decisions OD-04a through OD-04f as recorded in this document.

I acknowledge that OD-04h (historical rate immutability) and OD-04i (rate volatility bounds) remain unspecified and are excluded from this approval. They require future controlled clarification and approval.

This approval is limited to the documented policy decisions. It does not independently authorize G3-RV-01, schema freeze, G3, G4, production data promotion, or financial Power BI integration.

### 4.5 Owner Approval Record — To Be Completed by Project Owner

| Field | Entry |
|---|---|
| Decision | [X] APPROVED [ ] REJECTED [ ] RETURNED FOR REVISION |
| Approval scope | OD-04a through OD-04f only |
| Owner name | KH Mohammad Farhan |
| Owner decision | I formally approve the OD-04 synthetic exchange-rate policy comprising OD-04a through OD-04f, based on the documented technical evidence and synthetic-data requirements. |
| Owner signature | <u>Farhan</u> — Typed signature representation (not handwritten, not cryptographic) |
| Actual approval date | 08 November 2026 |
| Approval conditions | OD-04h and OD-04i remain UNSPECIFIED and require future controlled clarification and approval. This approval does not authorize G3-RV-01, schema freeze, G3, G4, production data promotion, or financial Power BI integration. |
| Signature evidence | Typed signature representation communicated by Project Owner via owner authorization directive on 08 November 2026 |
| Approval date evidence | 08 November 2026 — date communicated by Project Owner via owner authorization directive |

**Formal approval status:** APPROVED — Owner signature and approval date recorded on 08 November 2026.

---

## 5. Implementation Readiness and Authorization

| Prerequisite | Current Status | Notes |
|---|---|---|
| OD-04a currency scope | OWNER-CONFIRMED | Eight currencies |
| OD-04b conversion convention | OWNER-CONFIRMED | Exact-date USD conversion |
| OD-04c synthetic source | OWNER-CONFIRMED | AEROVISION-360-SYNTHETIC-FX-V1 |
| OD-04d rate version | OWNER-CONFIRMED | Date-based versioning |
| OD-04e missing-date behaviour | OWNER-CONFIRMED | Quarantine affected row |
| OD-04f generation methodology | OWNER-CONFIRMED | Deterministic algorithm |
| OD-04g formal approval | PENDING | Owner signature and date required |
| OD-04h historical immutability | UNSPECIFIED | Future controlled clarification |
| OD-04i volatility bounds | UNSPECIFIED | Future controlled clarification |
| G3-RV-01 | NOT AUTHORIZED BY THIS RECORD | Separate governance gate |
| Schema freeze | NOT AUTHORIZED BY THIS RECORD | Separate owner authorization |
| G3 | NOT APPROVED BY THIS RECORD | Separate governance gate |
| G4 | NOT AUTHORIZED BY THIS RECORD | Separate authorization required |
| Production data promotion | NOT AUTHORIZED | Separate approval required |
| Financial Power BI integration | NOT AUTHORIZED BY THIS RECORD | Requires applicable approvals and G4 |

---

## 6. Governance and Change Control

1. This document records the decisions and approval scope described above.
2. OD-04h and OD-04i must remain explicitly unresolved until separately clarified and approved.
3. Any change to the approved currency scope, conversion convention, rate source, versioning, missing-date behaviour, or generation methodology requires controlled change review.
4. Existing synthetic outputs must retain their provenance, manifests and integrity evidence.
5. Formal approval must be supported by an actual owner signature and actual approval date.
6. No independent assurance is claimed by this document.

---

## 7. Existing Evidence Register

| Source Document | Location | Purpose |
|---|---|---|
| OD04_OWNER_DECISION_PACKAGE.md | Project root | Original decision package |
| OD04_OWNER_DECISION_BRIEF.md | docs/governance/ | Decision brief |
| 03_DATA_CONTRACTs.md | docs/ | Currency and conversion contract |
| dim_currency.csv | data/03_curated/ | Currency reference data |
| dim_currency_manifest.json | data/manifests/ | Currency manifest |
| PAGE_03_REVENUE_FINANCE_READINESS.md | docs/ | Financial implementation readiness |
| AEROVISION360_Measures.dax | deliverables/power_bi/dax/ | DAX measure evidence |
| AEROVISION360_DataLoad.m | deliverables/power_bi/power_query/ | Power Query evidence |
| report.json | deliverables/power_bi/report/ | Report definition evidence |
| fact_booking_transactions_manifest.json | data/manifests/ | Financial fact manifest |
| fact_operating_costs_manifest.json | data/manifests/ | Operating-cost fact manifest |
| reference_manifest.json | data/manifests/ | Reference data manifest |

Existing evidence must be interpreted according to its actual status. Its presence does not imply authorization.

---

## 8. Final Decision Status

| Item | Status |
|---|---|
| OD-04a through OD-04f | OWNER-CONFIRMED |
| OD-04h | UNSPECIFIED |
| OD-04i | UNSPECIFIED |
| OD-04g formal approval | PENDING OWNER SIGNATURE AND DATE |
| G3-RV-01 | NOT AUTHORIZED BY THIS RECORD |
| Schema freeze | NOT AUTHORIZED BY THIS RECORD |
| G3 | NOT APPROVED BY THIS RECORD |
| G4 | NOT AUTHORIZED BY THIS RECORD |
| Production promotion | NOT AUTHORIZED BY THIS RECORD |

**Owner decision status:** OD-04a through OD-04f owner-confirmed; OD-04g formal approval pending.

**Implementation authorization:** This record does not independently authorize G3-RV-01, G3, G4 or production implementation.

**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 9. Document Closure

This decision record becomes formally approved only when the Project Owner completes the approval record in Section 4.5 with an actual signature and actual approval date.

No AI agent, automated process, or project assistant may supply or fabricate the owner's signature or approval date.

**End of OD-04 Owner Decision Record.**