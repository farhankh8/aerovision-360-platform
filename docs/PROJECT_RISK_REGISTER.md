# AEROVISION 360 — Project Risk Register

**Document ID:** A360-RISK-REGISTER-2026-11-02  
**Document type:** Controlled project risk register  
**Status:** ACTIVE REGISTER — R-09 TO R-11 RECORDED; MITIGATIONS NOT YET IMPLEMENTED  
**Created:** 2026-11-02  
**Owner / approver:** KH Mohammad Farhan, project owner  
**Authorization:** D-09 — owner-approved creation of a dedicated project risk register containing R-09, R-10, and R-11  
**Related decisions:** OD-01A; OD-01B; contract v1.5 Sections 3.4 and 13  
**Related change record:** `OD01_REVISION_0.2_CHANGE_RECORD.md`  
**Scope:** Airline reference identity, lifecycle, versioning, and historical reproducibility  
**Data authorization:** None. This register does not authorize reference CSVs, synthetic data, production ETL, Power Query, Power BI, schema freeze, G3, G4, or `G3-RV-01`.

> **Status notice**
>
> D-09 authorizes the register entries, not the underlying controls. No
> mitigation is recorded as implemented or verified unless an evidence item
> exists. No reference data, synthetic dataset, or production implementation has
> been created. The controls remain design commitments until their evidence is
> produced and accepted.

## 1. Purpose and use

This register records the airline identity and reference-version risks that were
identified during the OD-01 governance review. It is the dedicated register
required by H-04 and supports the decision records without replacing them.

The register does not:

- approve OD-01A or OD-01B;
- approve a reference version;
- freeze the schema;
- authorize data generation or implementation;
- claim that a mitigation has been executed; or
- claim independent assurance.

## 2. Rating method

| Dimension | Values used |
|---|---|
| Likelihood | `LOW`, `MEDIUM`, `HIGH` |
| Impact | `LOW`, `MEDIUM`, `HIGH` |
| Inherent rating | Combined likelihood and impact before the proposed controls; `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` |
| Residual rating | Expected rating after the proposed controls are implemented and evidenced; current rating is provisional until evidence exists |

The ratings are governance assessments, not measured operational probabilities.
They must be reviewed when the reference version, population, or control design
changes.

## 3. Register summary

| Risk ID | Risk title | Inherent rating | Current status |
|---|---|---|---|
| `R-09` | Airline suspension, cessation, merger, or lifecycle change | `HIGH` | `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED` |
| `R-10` | Reference-version change after data refresh or generation | `HIGH` | `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED` |
| `R-11` | Historical reproducibility and reference-snapshot consistency | `HIGH` | `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED` |

## 4. Risk entries

### R-09 — Airline suspension, cessation, merger, or lifecycle change

| Field | Register entry |
|---|---|
| Risk ID | `R-09` |
| Risk title | Airline suspension, cessation, merger, or lifecycle change |
| Description | An airline in the fixed reference population may be suspended, cease operations, merge, rebrand, or otherwise change operating status during the reporting period or a later reference version. |
| Root cause | Route suspension, regulatory action, insolvency, merger, operator decision, or a successor-entity event. |
| Potential consequence | The airline dimension may include a non-operating carrier without a status rule; reports may show active airline capacity, revenue, or other performance for an inactive carrier; historical facts may be misread; a merger or successor may be represented under the wrong durable identity. |
| Likelihood | `LOW` for the 12-month baseline because the ten airlines are initially active; `MEDIUM` for a future reference version or lifecycle event. |
| Impact | `HIGH` — incorrect airline status can distort all airline-level reporting and historical interpretation. |
| Inherent risk rating | `HIGH` |
| Mitigation controls | `IsActive` Boolean and `StatusEffectiveDate`; controlled new `ReferenceVersion` for a status change; Tier 3 change control for a new airline, successor, merger, or rebrand; immutable reference snapshots; T-78 lifecycle and version checks; reconciliation note; no silent rewrite of historical facts. |
| Monitoring method | Review `IsActive` and `StatusEffectiveDate` at each reference-version approval; execute T-78-01 to T-78-10 at generation and refresh; verify that a status change has a new version and source evidence; review lifecycle exceptions in the owner-approved change note. |
| Risk owner role | Project Owner — accountable; Data Architecture/QA — control owner and evidence custodian |
| Residual risk | `MEDIUM` until the lifecycle rule is applied to an approved reference version and T-78 evidence exists; target `LOW` after verification and owner acceptance. |
| Current status | `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED` |
| Evidence required for closure | Approved reference version containing the lifecycle attributes; source records supporting the status; T-78-01 to T-78-10 results; reconciliation note for any status change; owner acceptance of the residual risk. |

### R-10 — Reference-version change after data refresh or generation

| Field | Register entry |
|---|---|
| Risk ID | `R-10` |
| Risk title | Reference-version change after data refresh or generation |
| Root cause | Uncontrolled reference update, refresh parameter drift, manifest mismatch, missing version pinning, or a changed reference snapshot being selected after facts were generated. |
| Description | A reference dataset may change after data refresh or generation, or a refresh may select a different airline reference version from the one used to generate the facts. |
| Potential consequence | Silent version drift; facts and dimension attributes drawn from different snapshots; inconsistent airline identity; non-reproducible airline-level results; failed reconciliation; misleading historical trends. |
| Likelihood | `MEDIUM` — reference data can be updated independently unless the refresh is pinned and validated. |
| Impact | `HIGH` — mixed versions can invalidate airline facts and reports across the model. |
| Inherent risk rating | `HIGH` |
| Mitigation controls | One approved `ReferenceVersion` per generation and refresh; authoritative reference manifest; `SelectedReferenceVersion` in the Power BI model; T-78-01 to T-78-10; fail closed on mismatch; immutable reference snapshots; controlled refresh procedure; no mixed-version facts. |
| Monitoring method | Compare the manifest version, `ref_airlines.csv` version, `ref_airline_sources.csv` version, `DimAirline.ReferenceVersion`, and `SelectedReferenceVersion`; execute T-78 before refresh; record the manifest hash and refresh configuration; review every mismatch as a blocking exception. |
| Risk owner role | Project Owner — accountable; Data Architecture/QA — control owner and T-78 evidence custodian |
| Residual risk | `MEDIUM` until the manifest, version pinning, and T-78 are implemented and evidenced; target `LOW` after successful verification. |
| Current status | `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED` |
| Evidence required for closure | Approved manifest; pinned reference version; T-78-01 to T-78-10 results; refresh configuration; successful mismatch/fail-closed test; owner acceptance of the residual risk. |

### R-11 — Historical reproducibility and reference-snapshot consistency

| Field | Register entry |
|---|---|
| Risk ID | `R-11` |
| Risk title | Historical reproducibility and reference-snapshot consistency |
| Description | Historical synthetic facts may become inconsistent with a changed airline identity, or a correction may re-key facts, overwrite a prior reference version, or lose the snapshot needed to reproduce an earlier result. |
| Root cause | Reassigned `AirlineKey`, rebuilt dimension, mutable reference snapshot, missing reconciliation note, or unrecorded identity correction. |
| Potential consequence | Broken trends; facts linked to the wrong airline; an earlier report cannot be reproduced; historical comparisons become unreliable; audit and portfolio-release evidence fail. |
| Likelihood | `MEDIUM` — identity and reference corrections are expected to occur across versions. |
| Impact | `HIGH` — lost reproducibility undermines the airline model, reporting, and governance evidence. |
| Inherent risk rating | `HIGH` |
| Mitigation controls | Permanent `AirlineKey`; stable `AirlineId`; controlled immutable key map; immutable reference snapshots; no re-keying of historical facts; T-78-09 and T-78-10; reconciliation note for every identity change; seeded reproducibility evidence; version-pinned refresh. |
| Monitoring method | Verify key-map stability and absence of reassignment at each reference approval; compare historical fact keys to the approved key map; execute T-78-09/10; reproduce a sample build from the recorded snapshot and seed; require a reconciliation note for every identity change. |
| Risk owner role | Project Owner — accountable; Data Architecture/QA — control owner and reconciliation evidence custodian |
| Residual risk | `MEDIUM` until T-78 and reproducibility tests are executed; target `LOW` after verified evidence. |
| Current status | `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED` |
| Evidence required for closure | Approved key map; immutable snapshot record; T-78-09/10 results; reproducibility test result from the recorded snapshot and seed; reconciliation notes; owner acceptance of the residual risk. |

## 5. Register controls

- The register is reviewed when a reference version is proposed, when the airline population changes, and before `G3-RV-01` approval.
- A risk may be marked `CLOSED` only when the evidence required for closure exists and has been reviewed.
- D-09 authorizes the register and entries; it does not close R-09 to R-11 or accept residual risk as verified.
- Owner acceptance of residual risk is a separate signature/decision; no acceptance is recorded in this register.
- No named individual other than the project owner is recorded as a risk owner. Control ownership remains role-based.
- This register does not modify OD-01A, OD-01B, contract v1.5, or the progress ledger.

## 6. Revision history

| Version | Date | Change | Status |
|---|---|---|---|
| 0.1 | 2026-11-02 | Created dedicated project risk register and recorded R-09, R-10, and R-11 under D-09. | Active register; mitigations open and unverified. |

No risk closure or residual-risk acceptance is recorded.
