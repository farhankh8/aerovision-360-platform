# C-08 / C-02 — Contract Immutability Trigger Decision

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** C-08-C-02-2026-11-07-001  
**Document Type:** Owner Decision Draft — Contract Immutability Trigger Resolution  
**Status:** DRAFT — OWNER DECISION REQUIRED — NOT APPROVED  
**Prepared:** 2026-11-07  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Finding ID

C-08 / C-02 — Contract immutability trigger conflicts with OD-01B exclusion

---

## 2. Exact Conflict

| Source | Location | Statement |
|---|---|---|
| Contract v1.5 §7.1 | Line 1046 | "The airline key map is immutable after OD-01B approval" |
| OD-01B §3 | Lines 135–136 | "Proposed administrative allocation (this revision does not approve the mapping; it is a design baseline, not a source-verified identity fact)" |
| OD-01B §2 | Item 10 | "Reference-version approval uses G3-RV-01, not an OD-series decision." |
| OD-01B §11.3 | Lines 379–390 | "This approval covers... Sections 2, 4, 5, 6, and 8... Sections 3 and 7 are acknowledged design baselines, not a schema freeze. ... The key map in Section 3 remains a proposed administrative allocation, not a source-verified identity fact." |

**The conflict:** Contract §7.1 says the airline key map is immutable after OD-01B approval. OD-01B explicitly excludes Section 3 (where the key map is defined) from its approval scope and states that the key map in Section 3 is a proposed administrative allocation that is NOT approved by OD-01B. An OD-01B signature cannot both exclude the key map from approval scope and make it immutable through that same approval.

---

## 3. Verified Source References

| Source | Location | Relevance |
|---|---|---|
| Contract v1.5 §7.1 | Line 1046 | Key map immutability after OD-01B approval |
| Contract v1.5 §9.4 | Line 265 | Reference-version approval uses G3-RV-01, not OD-series |
| Contract v1.5 §13 | Line 1895 | Key-map controls and Power BI reference-version constraints documented |
| Contract v1.5 §13 | Line 1934 | v1.5 change record references G3-RV-01 |
| Contract v1.5 §15.2 | AC-18 | Reference data versions approved through G3-RV-01 |
| OD-01B §2 | Item 10 | Reference-version approval uses G3-RV-01 |
| OD-01B §3 | Lines 135–136 | Key map is proposed administrative allocation, not approved |
| OD-01B §7 | Line 271 | G3-RV-01 definition |
| OD-01B §9 | Tier 2 change control | Key map changes require G3-RV-01 update |
| OD-01B §11.3 | Lines 379–390 | Section 3 excluded from OD-01B approval scope |

---

## 4. M-12 Dependency Assessment

**M-12 status: PARTIALLY CLOSED**

Per `AEROVISION_360_OWNER_DECISION_WORKSHEET.md` §13.2:
- OD-01B now names Sections 2, 4, 5, 6, and 8 as the approval scope
- OD-01B explicitly excludes schema freeze and implementation
- The approving sentence still claims reference-version, manifest, and immutable-mapping rules that sit principally in Section 7, which is excluded
- The key-map trigger remains circular until resolved

**Does selecting G3-RV-01 create new circularity?**

No. The corrected sequence is:

1. OD-01B is signed with Sections 2, 4, 5, 6, and 8 in scope; Section 3 (key map) explicitly excluded
2. G3-RV-01 is executed after OD-01A/OD-01B signatures, reference data availability, and manifest creation
3. G3-RV-01 approves the reference version including the manifest containing the key map hash
4. The key map becomes immutable after G3-RV-01 approval

There is no circular dependency: OD-01B does not need to approve the key map to be signed, and G3-RV-01 does not depend on OD-01B approving Section 3.

---

## 5. Option Comparison

| Criteria | Option A: OD-01B triggers immutability | Option B: G3-RV-01 triggers immutability |
|---|---|---|
| Existing approval scope | OD-01B excludes Section 3 (key map) — contradiction | G3-RV-01 covers reference version including manifest with key map |
| Contract consistency | Contradicts OD-01B exclusion of Section 3 | Aligns with contract §7.1 (immutable after approval) and §9.4 (G3-RV-01) |
| Reference-version governance | N/A — OD-01B is not the reference-version gate | G3-RV-01 is the designated gate artifact |
| Immutability and change control | Premature — map not yet approved | Controlled — map becomes immutable after reference-version approval |
| M-12 requirements | Does not resolve circular trigger | Resolves trigger with single unambiguous approval point |
| G3 execution sequence | Breaks sequence — OD-01B signs before manifest exists | Follows sequence — OD-01B signs, then G3-RV-01 executes |
| Circular dependency risk | HIGH — OD-01B can't approve what it excludes | NONE — linear sequence |

**Recommended: Option B — G3-RV-01 approval triggers key-map immutability**

---

## 6. Proposed Replacement Wording

### Contract v1.5 §7.1 (line 1046)

**Current:**
> "The airline key map is immutable after OD-01B approval, is stored with or hashed into the approved reference manifest, and is loaded by every clean rebuild. A missing or inconsistent map blocks generation and refresh."

**Proposed:**
> "The airline key map is immutable after G3-RV-01 approval, is stored with or hashed into the approved reference manifest, and is loaded by every clean rebuild. A missing or inconsistent map blocks generation and refresh."

### OD-01B §11.3 (lines 379–390)

**Current:**
> "This approval covers the governing airline identity, key, provenance, lifecycle, reference-version, manifest, immutable-mapping, and Power BI identity/disclosure rules in OD-01B Sections 2, 4, 5, 6, and 8. Sections 3 and 7 are acknowledged design baselines, not a schema freeze. This approval does not create or populate reference CSVs, approve a schema freeze, authorize synthetic data generation, production ETL, Power Query, Power BI, G3, or G4."

**Proposed:**
> "This approval covers the governing airline identity, key, provenance, lifecycle, reference-version, manifest, and Power BI identity/disclosure rules in OD-01B Sections 2, 4, 5, 6, and 8. Sections 3 and 7 are acknowledged design baselines, not a schema freeze. The key map in Section 3 remains a proposed administrative allocation until G3-RV-01 approval, at which point it becomes immutable as part of the approved reference manifest. This approval does not create or populate reference CSVs, approve a schema freeze, authorize synthetic data generation, production ETL, Power Query, Power BI, G3, or G4."

---

## 7. Consequences of Accepting Option B

- Contract §7.1 and OD-01B §11.3 become consistent: key map immutability triggered by G3-RV-01, not OD-01B
- M-12 circular dependency resolved
- OD-01B can be signed without approving the key map in Section 3
- G3-RV-01 becomes the single unambiguous approval trigger for key-map immutability
- Change control Tier 2 in OD-01B §9 already requires G3-RV-01 update for key-map changes — consistent
- No changes to G3 or G4 authorization required
- No schema freeze triggered

### Consequences of Rejecting Option B

- C-08/C-02 remains open — OD-01B cannot be signed cleanly
- M-12 remains PARTIALLY CLOSED indefinitely
- Contract and OD-01B remain contradictory on key-map immutability
- G3 cannot proceed cleanly without resolved key-map governance

---

## 8. Owner Decision Options

| Option | Description | Owner Action |
|---|---|---|
| **OPTION A — Approve OD-01B as key-map trigger** | Accept that key map becomes immutable after OD-01B approval despite OD-01B excluding Section 3 | Mark APPROVED; requires OD-01B §11.3 revision to include Section 7 mechanics |
| **OPTION B — Approve G3-RV-01 as key-map trigger (RECOMMENDED)** | Accept that key map becomes immutable after G3-RV-01 approval; align contract §7.1 and OD-01B §11.3 accordingly | Mark APPROVED; proceed with documented wording changes |
| **OPTION C — Reject and return for redesign** | Reject both options; require a fundamentally different approach | Mark REJECTED; document alternative requirements |

---

## 9. Owner Acceptance Section

| Field | Entry |
|---|---|
| Decision | [ ] OPTION A — APPROVED   [ ] OPTION B — APPROVED   [ ] OPTION C — REJECTED |
| Approval scope | C-08 / C-02 — Contract Immutability Trigger Resolution |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Approval conditions | [BLANK — to be completed at signature] |
| Contract amendment required | [ ] Yes — §7.1 line 1046 wording change   [ ] No |
| OD-01B amendment required | [ ] Yes — §11.3 lines 379–390 wording change   [ ] No |
| Formal signature | ______________________________ |
| Approval date | ______________________________ |

**Approval status:** DRAFT — OWNER DECISION REQUIRED — NOT APPROVED. No signature, approval date, or formal approval evidence has been created.

---

## 10. End of Decision Record

This document records the proposed resolution for C-08/C-02. No source files, data, DAX, Power Query, semantic model, Power BI, or other project artifacts were modified during its creation. The contract v1.5 was not modified. OD-01A and OD-01B were not modified. No signature, approval date, or formal approval evidence has been created. C-08/C-02 remains pending formal owner decision.
