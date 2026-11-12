# H-04 — Residual Risk Acceptance Clarification Draft

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** H-04-RAC-2026-11-07-001  
**Document Type:** Owner Decision Draft — Residual Risk Acceptance Clarification  
**Status:** DRAFT — OWNER DECISION REQUIRED — NOT APPROVED  
**Prepared:** 2026-11-07  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Finding ID

H-04 — Risk register omitted three scenarios (R-09, R-10, R-11)

---

## 2. Exact Problem

The risk register `docs/PROJECT_RISK_REGISTER.md` records R-09, R-10, and R-11 with inherent ratings of HIGH and current status `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED`. The register specifies:

- **Section 4:** Each risk carries a residual risk rating of `MEDIUM`, with the explicit qualification that this rating applies *until* the proposed controls are implemented and evidenced, and that the target is `LOW` after verification and owner acceptance.
- **Section 5:** "A risk may be marked `CLOSED` only when the evidence required for closure exists and has been reviewed." No risk has been closed.
- **Section 5:** "D-09 authorizes the register and entries; it does not close R-09 to R-11 or accept residual risk as verified. Owner acceptance of residual risk is a separate signature/decision; no acceptance is recorded in this register."

The original H-04 finding noted that the risk register omitted three scenarios. The register now exists (created under D-09) and records R-09, R-10, and R-11. However, the mitigations remain unimplemented and unverified. The question for the owner is: **what exactly is being accepted, if anything, when considering H-04 closure?**

This draft does **not** accept residual risk. It clarifies what acceptance would mean, what evidence is required, and what cannot yet be claimed.

---

## 3. Risk-by-Risk Analysis

### R-09 — Airline suspension, cessation, merger, or lifecycle change

| Field | Register Entry |
|---|---|
| Risk ID | R-09 |
| Risk title | Airline suspension, cessation, merger, or lifecycle change |
| Inherent rating | HIGH |
| Current status | OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED |
| Likelihood | LOW for 12-month baseline (all ten airlines initially active); MEDIUM for future reference version or lifecycle event |
| Impact | HIGH — incorrect airline status can distort all airline-level reporting and historical interpretation |
| Mitigation controls | `IsActive` Boolean and `StatusEffectiveDate`; controlled new `ReferenceVersion` for status change; Tier 3 change control for new airline/successor/merger/rebrand; immutable reference snapshots; T-78 lifecycle and version checks; reconciliation note; no silent rewrite of historical facts |
| Monitoring method | Review `IsActive` and `StatusEffectiveDate` at each reference-version approval; execute T-78-01 to T-78-10 at generation and refresh; verify status change has new version and source evidence; review lifecycle exceptions in owner-approved change note |
| Risk owner role | Project Owner — accountable; Data Architecture/QA — control owner and evidence custodian |
| Residual risk | MEDIUM until lifecycle rule applied to approved reference version and T-78 evidence exists; target LOW after verification and owner acceptance |
| Evidence required for closure | Approved reference version containing lifecycle attributes; source records supporting status; T-78-01 to T-78-10 results; reconciliation note for status change; owner acceptance of residual risk |

### R-10 — Reference-version change after data refresh or generation

| Field | Register Entry |
|---|---|
| Risk ID | R-10 |
| Risk title | Reference-version change after data refresh or generation |
| Inherent rating | HIGH |
| Current status | OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED |
| Likelihood | MEDIUM — reference data can be updated independently unless refresh is pinned and validated |
| Impact | HIGH — mixed versions can invalidate airline facts and reports across the model |
| Mitigation controls | One approved `ReferenceVersion` per generation and refresh; authoritative reference manifest; `SelectedReferenceVersion` in Power BI model; T-78-01 to T-78-10; fail closed on mismatch; immutable reference snapshots; controlled refresh procedure; no mixed-version facts |
| Monitoring method | Compare manifest version, `ref_airlines.csv` version, `ref_airline_sources.csv` version, `DimAirline.ReferenceVersion`, and `SelectedReferenceVersion`; execute T-78 before refresh; record manifest hash and refresh configuration; review every mismatch as blocking exception |
| Risk owner role | Project Owner — accountable; Data Architecture/QA — control owner and T-78 evidence custodian |
| Residual risk | MEDIUM until manifest, version pinning, and T-78 implemented and evidenced; target LOW after successful verification |
| Evidence required for closure | Approved manifest; pinned reference version; T-78-01 to T-78-10 results; refresh configuration; successful mismatch/fail-closed test; owner acceptance of residual risk |

### R-11 — Historical reproducibility and reference-snapshot consistency

| Field | Register Entry |
|---|---|
| Risk ID | R-11 |
| Risk title | Historical reproducibility and reference-snapshot consistency |
| Inherent rating | HIGH |
| Current status | OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED |
| Likelihood | MEDIUM — identity and reference corrections expected across versions |
| Impact | HIGH — lost reproducibility undermines airline model, reporting, and governance evidence |
| Mitigation controls | Permanent `AirlineKey`; stable `AirlineId`; controlled immutable key map; immutable reference snapshots; no re-keying of historical facts; T-78-09 and T-78-10; reconciliation note for every identity change; seeded reproducibility evidence; version-pinned refresh |
| Monitoring method | Verify key-map stability and absence of reassignment at each reference approval; compare historical fact keys to approved key map; execute T-78-09/10; reproduce sample build from recorded snapshot and seed; require reconciliation note for every identity change |
| Risk owner role | Project Owner — accountable; Data Architecture/QA — control owner and reconciliation evidence custodian |
| Residual risk | MEDIUM until T-78 and reproducibility tests executed; target LOW after verified evidence |
| Evidence required for closure | Approved key map; immutable snapshot record; T-78-09/10 results; reproducibility test result from recorded snapshot and seed; reconciliation notes; owner acceptance of residual risk |

---

## 4. Distinction: Temporary Exposure vs. Post-Mitigation Residual Risk

The risk register explicitly states that the `MEDIUM` residual ratings are **provisional**:

> "Residual rating: Expected rating after the proposed controls are implemented and evidenced; current rating is provisional until evidence exists."

This distinction is critical:

| Concept | Meaning | Current Status for R-09/R-10/R-11 |
|---|---|---|
| **Inherent risk** | Risk before any controls are applied | HIGH for all three risks |
| **Temporary exposure** | Risk present now, while controls are unimplemented | HIGH — equivalent to inherent risk because no controls are implemented |
| **Post-mitigation residual risk** | Risk expected to remain after controls are implemented and evidenced | MEDIUM (provisional) — target LOW after verification and owner acceptance |

The register records all three risks as `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED`. This means **none of the proposed controls have been implemented**. The `MEDIUM` residual rating is therefore not yet realized — it is the *projected* residual risk *after* controls are implemented. The actual current exposure is effectively at the inherent HIGH level because no controls are in place.

**Accepting "MEDIUM residual risk" today would conflate the projected post-mitigation residual risk with the current actual exposure.** The controls are unimplemented; the actual exposure is HIGH.

---

## 5. Evidence Required for Risk Closure

### R-09 Closure Evidence
- Approved reference version containing lifecycle attributes (`IsActive`, `StatusEffectiveDate`)
- Source records supporting each airline status
- T-78-01 to T-78-10 test results
- Reconciliation note for any status change
- Owner acceptance of residual risk

### R-10 Closure Evidence
- Approved manifest
- Pinned reference version
- T-78-01 to T-78-10 results
- Refresh configuration
- Successful mismatch/fail-closed test
- Owner acceptance of residual risk

### R-11 Closure Evidence
- Approved key map
- Immutable snapshot record
- T-78-09/10 results
- Reproducibility test result from recorded snapshot and seed
- Reconciliation notes
- Owner acceptance of residual risk

---

## 6. Monitoring, Review Triggers, and Outstanding Control Ownership

| Risk | Monitoring Method | Review Trigger | Control Ownership |
|---|---|---|---|
| R-09 | Review `IsActive` and `StatusEffectiveDate` at each reference-version approval; execute T-78-01 to T-78-10 at generation and refresh; verify status change has new version and source evidence; review lifecycle exceptions in owner-approved change note | Before each reference-version approval; at each generation and refresh | Project Owner — accountable; Data Architecture/QA — control owner and evidence custodian |
| R-10 | Compare manifest version, `ref_airlines.csv` version, `ref_airline_sources.csv` version, `DimAirline.ReferenceVersion`, and `SelectedReferenceVersion`; execute T-78 before refresh; record manifest hash and refresh configuration; review every mismatch as blocking exception | Before each refresh; on every version mismatch | Project Owner — accountable; Data Architecture/QA — control owner and T-78 evidence custodian |
| R-11 | Verify key-map stability and absence of reassignment at each reference approval; compare historical fact keys to approved key map; execute T-78-09/10; reproduce sample build from recorded snapshot and seed; require reconciliation note for every identity change | At each reference-version approval; on every identity change | Project Owner — accountable; Data Architecture/QA — control owner and reconciliation evidence custodian |

---

## 7. What H-04 Closure Would Require

To close H-04 (the finding that the risk register omitted R-09, R-10, R-11), all three risks must be addressed as follows:

1. **Risks remain documented** — `docs/PROJECT_RISK_REGISTER.md` exists and records all three risks. This addresses the original finding that the register omitted them.
2. **Risks remain OPEN** — None of R-09, R-10, R-11 may be marked CLOSED until their respective evidence for closure exists and has been reviewed.
3. **Mitigations unimplemented** — All mitigation controls remain documented but not implemented. No control has been verified as effective.
4. **Residual risk not accepted** — Owner acceptance of residual risk is explicitly a separate decision. No acceptance has been recorded.
5. **H-04 itself cannot be closed** — Because the underlying risks remain open and unmitigated, H-04 cannot be resolved as "closed" in any meaningful sense.

---

## 8. Owner Decision Options

| Option | Description | Owner Action |
|---|---|---|
| **OPTION A — Acknowledge open risks, defer acceptance** | Acknowledge R-09, R-10, R-11 as OPEN with mitigations NOT IMPLEMENTED / NOT VERIFIED. Defer residual risk acceptance until controls are implemented and evidenced. | Mark ACKNOWLEDGED — risks remain open; no residual risk accepted at this time |
| **OPTION B — Accept provisional residual risk** | Accept the MEDIUM residual risk ratings as provisional projections, explicitly understanding they apply only *after* controls are implemented. | Mark PROVISIONAL ACCEPTANCE — residual risk accepted provisionally, pending control implementation |
| **OPTION C — Require implementation before any acceptance** | Defer all risk decisions until R-09, R-10, R-11 mitigations are implemented and evidenced via T-78 testing. | Mark DEFERRED — no risk decision until controls implemented |

---

## 9. Owner Acceptance Section

| Field | Entry |
|---|---|
| Decision | [ ] OPTION A — ACKNOWLEDGED   [ ] OPTION B — PROVISIONAL ACCEPTANCE   [ ] OPTION C — DEFERRED |
| Approval scope | H-04 — Residual Risk Acceptance Clarification (R-09, R-10, R-11) |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Approval conditions | [BLANK — to be completed at signature] |
| Residual risk accepted | [ ] None   [ ] Provisional MEDIUM for R-09   [ ] Provisional MEDIUM for R-10   [ ] Provisional MEDIUM for R-11   [ ] Provisional MEDIUM for all three |
| Formal signature | ______________________________ |
| Approval date | ______________________________ |

**Approval status:** DRAFT — OWNER DECISION REQUIRED — NOT APPROVED. No signature, approval date, or formal approval evidence has been created.

---

## 10. End of Decision Record

This document records the proposed clarification for H-04 residual risk. No source files, data, DAX, Power Query, semantic model, Power BI, or other project artifacts were modified during its creation. `docs/PROJECT_RISK_REGISTER.md` was read only and not modified. `docs/governance/C-06_OD01B-B-08_CC-01_SELF_REVIEW_CHECKLIST.md` was read only and not modified. No reviewer was invented, no signature was fabricated, no independent assurance was claimed, and no risk was marked CLOSED. H-04 remains pending formal owner decision.
