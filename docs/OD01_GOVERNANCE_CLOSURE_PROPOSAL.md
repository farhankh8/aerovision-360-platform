# AEROVISION 360 — OD-01 Governance Closure Proposal

**Document ID:** OD01-GCP-2026-11-02  
**Document type:** Controlled remediation proposal — not an approval, signature, waiver, gate decision, or implementation authorization  
**Status:** PROPOSED — OWNER DECISIONS D-03 THROUGH D-10 PENDING  
**Prepared:** 2026-11-02  
**Prepared by:** Build AI agent — non-independent preparer  
**Project owner / approver:** KH Mohammad Farhan  
**Governing contract:** `03_DATA_CONTRACTS.md` version 1.5  
**Governing scope:** `01_PROJECT_SCOPE.md` version 1.1  
**Decision records:** OD-01A version 0.1; OD-01B version 0.1  
**Related decision packet:** `OD01_OWNER_DECISION_PACKET.md`  
**G3:** `NOT STARTED`  
**G4:** `BLOCKED`  
**`G3-RV-01`:** `NOT EXECUTED`

> **Status notice**
>
> The owner has accepted the compensating-control approach and the
> no-independent-review limitation, as recorded in the decision packet. That
> acceptance does not approve OD-01A, OD-01B, or decisions D-03 through D-10.
> No formal signature, approval date, reviewer identity, completed review
> activity, or independent assurance is recorded here.
>
> This proposal is documentation only. It does not create reference CSVs,
> synthetic data, production Python, Power Query, DAX, Power BI, a schema
> freeze, a G3/G4 change, or a Git operation. No existing controlling document
> has been modified.

---

## 1. Controlling sources and current status

### 1.1 Sources inspected

- `docs/OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md`
- `docs/OD01A_AIRLINE_POPULATION_DECISION.md`
- `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`
- `docs/OD01_OWNER_DECISION_CONFIRMATION.md`
- `docs/OD01_OWNER_DECISION_RESOLUTION.md`
- `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md`
- `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md`
- `docs/OD01_REMEDIATION_CHANGE_RECORD.md`
- `docs/01_PROJECT_SCOPE.md`
- `docs/02_BUSINESS_REQUIREMENTS.md`
- `docs/03_DATA_CONTRACTS.md`
- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/PROGRESS_LEDGER.md`

### 1.2 Current hashes

Recomputed with PowerShell `Get-FileHash -Algorithm SHA256` on 2026-11-02. All listed files were UTF-8 without BOM and LF-only at verification time.

| File | SHA-256 |
|---|---|
| `OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` | `C07C412C69ADB6DCDF72DA8517A142DC6E4FD12C26CB83960EF0FAA8E586BA98` |
| `OD01A_AIRLINE_POPULATION_DECISION.md` | `399241AD2AE21F4A1FB3D7E589950117F9CDADB8303F78CC161F484CD7255A06` |
| `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | `CDD48B9F0B68CE401D827E5F910076104CCCE73FFBF7BA0A6BC21D75D07C3C05` |
| `OD01_OWNER_DECISION_CONFIRMATION.md` | `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD` |
| `OD01_OWNER_DECISION_RESOLUTION.md` | `BE62CBDC017073F6D9135D7DEEF3993F64D74D881102A5C867134C889E20A220` |
| `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` | `FD94BD369D3DDDC1AF84C040C27014F112E74B4B0F938CE95B617C7B142BECE6` |
| `OD01_REMEDIATION_DESIGN_SPECIFICATION.md` | `CC3BCE621142C31B4BB7A46F4CBCB320E640466228184AE2E94E196796F3F8A4` |
| `OD01_REMEDIATION_CHANGE_RECORD.md` | `B74329743E5FD5343FA8EB0F1A103436C54A63D949526437E902EA03D6869A22` |
| `01_PROJECT_SCOPE.md` | `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` |
| `02_BUSINESS_REQUIREMENTS.md` | `F5B3140A91C868692A37609F904129BD166861045A9D00C9840815B0CCC4E709` |
| `03_DATA_CONTRACTS.md` | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` |
| `REQUIREMENTS_TRACEABILITY.md` | `4EE19E921BDC3067D17E172422D85D76B2660EF478EF4AB385D816BA4C314DEB` |
| `PROGRESS_LEDGER.md` | `C6297622D8CFE5BD90402BBB034B1091C70BAA2895BF0438F4E94C003E343C1F` |

### 1.3 Recorded owner instruction

The decision packet records D-01 and D-02 as accepted owner instructions, with the explicit limitations that no independent reviewer performed the review, AI-assisted re-audit is not independent assurance, owner self-review is self-review, residual risks remain transparent, and future independent review is recommended.

D-03 through D-10 remain PENDING. The D-01/D-02 acceptance does not imply approval of any technical decision, decision-record revision, addendum, risk-register entry, gate-label change, threshold, hash method, or retention policy.

---

## 2. B-03 — Stale scope evidence

### 2.1 Complete stale-hash assessment

| Document / location | Old value | Classification | Proposed treatment |
|---|---|---|---|
| OD-01A §6, E-07 | `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` | **Stale current-decision citation** | Correct to current scope v1.1 in OD-01A revision 0.2. |
| OD-01B §10, shared evidence E-01–E-12 | Inherits OD-01A E-07 | **Stale through shared index** | Correct the shared evidence reference in OD-01B revision 0.2. |
| `OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` | Old hash appears as historical evidence | Intentional historical reference | Do not change; it explains the defect. |
| `OD01_REMEDIATION_CHANGE_RECORD.md` line 73 | Old hash recorded before the later scope correction | Historical controlled-change evidence | Preserve; do not rewrite history. |
| `OD01_OWNER_DECISION_RESOLUTION.md` line 123 | Old hash in the pre-confirmation resolution | Historical evidence | Preserve; not a current approval citation. |
| `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` line 98 | Old hash in the audit snapshot | Historical evidence | Preserve; audit is a dated record. |
| `OD01_FORMAL_DECISION_RECORD_DRAFT.md` line 426 | Old hash in the superseded draft | Historical draft evidence | Preserve; do not use as current authority. |
| `scope_alignment_backup_20261102_202419/01_PROJECT_SCOPE.md` | Old hash | Preserved backup | Preserve; do not edit. |

### 2.2 Current values

| Evidence | SHA-256 | Bytes |
|---|---|---:|
| Current `01_PROJECT_SCOPE.md` v1.1 | `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` | 6,384 |
| Pre-correction backup | `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` | 5,790 |

The old hash is genuine but obsolete. The correction is evidence hygiene, not a change to the population decision.

### 2.3 Proposed exact correction

Replace OD-01A E-07 with:

> **E-07 — Project scope.** `docs/01_PROJECT_SCOPE.md`, version 1.1, current at review on 2026-11-02; SHA-256 `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C`; 6,384 bytes. The scope was subsequently corrected under a separate controlled change after the remediation change record; this evidence item records the current governing scope, not the pre-correction backup.

Update OD-01B §10 to reference the corrected shared evidence item. Add revision-history entries to both records. Recompute both file hashes after editing. No edit is authorized now.

---

## 3. B-04 — Approval record structure

### 3.1 Design principles

The approval block must make the following unambiguous:

- What exactly is approved.
- What is excluded.
- Who decided and when.
- Whether a reviewer or compensating-control route was used.
- Whether independence is claimed.
- What conditions and residual concerns remain.
- Where the signed copy is retained and what its hash is.

### 3.2 Required fields

| Field | Required content |
|---|---|
| Decision | `APPROVED`, `REJECTED`, or `RETURNED FOR REVISION`. |
| Approval scope | Explicit section/decision scope. |
| Exclusions | Reference data, schema freeze, data generation, production ETL, Power Query, Power BI, G3, G4. |
| Owner name | Confirm the designated approver. |
| Owner decision | Blank until signed. |
| Approval conditions | Explicit conditions; no implied conditions. |
| Reviewer route | Independent reviewer / compensating controls accepted / N/A. |
| Compensating-control acceptance | Owner initials/date if no reviewer. |
| Reviewer limitation | No independent assurance statement. |
| Reviewer name/role/organization | Blank unless a reviewer is actually assigned. |
| Reviewer independence | Independent / not independent / N/A. |
| Reviewer result | `CONCUR`, `CONCUR WITH RESERVATIONS`, `DISSENT`, or `N/A`. |
| Residual concerns | Blank field for recorded residual issues. |
| Signature and date | Owner signature and actual signature date; blank until signed. |
| Evidence references | Re-audit, scope v1.1 hash, contract v1.5 hash, reviewer/control evidence. |
| Signed-copy path | Future `docs/approvals/...` path. |
| Signed-copy SHA-256 | Actual hash only after the signed copy exists. |
| Retention and verification | Read-only retention and verification confirmation. |

### 3.3 OD-01A approval scope

> This approval covers the fixed ten-airline population and population-boundary rules in OD-01A Sections 2, 3, and 4 only. It does not approve OD-01B, reference values or CSV creation, schema freeze, synthetic data generation, production ETL, Power Query, Power BI, G3, or G4.

### 3.4 OD-01B approval scope

> This approval covers the governing airline identity, key, provenance, lifecycle, reference-version, manifest, immutable-mapping, and Power BI identity/disclosure rules in OD-01B Sections 2, 4, 5, 6, and 8. Sections 3 and 7 are acknowledged design baselines, not a schema freeze. This approval does not create or populate reference CSVs, approve a schema freeze, authorize data generation, production ETL, Power Query, Power BI, G3, or G4.

### 3.5 Proposed blank block

```text
Decision: [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION

Approval scope: ______________________________________________
Exclusions: __________________________________________________
Owner name: __________________________________________________
Owner decision: ______________________________________________
Owner signature: _____________________________________________
Actual approval date: ________________________________________
Approval conditions: _________________________________________
______________________________________________________________

Reviewer route:
[ ] Independent reviewer   [ ] Compensating controls accepted   [ ] N/A
Compensating-control acceptance: _____________________________
Reviewer limitation statement: ________________________________
Reviewer name/role/organization: ______________________________
Reviewer independence: [ ] Independent [ ] Not independent [ ] N/A
Reviewer result: [ ] CONCUR [ ] CONCUR WITH RESERVATIONS [ ] DISSENT [ ] N/A
Reviewer signature/date: _____________________________________
Residual concerns: ___________________________________________

Evidence references:
- Re-audit record: ____________________________________________
- Scope v1.1 SHA-256: _________________________________________
- Contract v1.5 SHA-256: ______________________________________
- Signed-copy path: ___________________________________________
- Signed-copy SHA-256: ________________________________________
- Retention confirmed: [ ] Yes [ ] No
- Verification date/result: ___________________________________
```

No field has been completed.

---

## 4. B-05 — Historical owner-confirmation addendum

The original `OD01_OWNER_DECISION_CONFIRMATION.md` remains unchanged at `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`.

The proposed addendum is in Annex A. It is **not** a separate executed record and not an approval. It becomes a controlled addendum only after D-04 is approved.

---

## 5. H-04 — Proposed risk-register entries

These entries are proposed, not incorporated. They are designed for a future controlled risk-register update or addendum.

### R-09 — Airline lifecycle and cessation

| Field | Proposed entry |
|---|---|
| Risk ID | `R-09` |
| Risk description | An airline in the reference population is suspended, ceases operations, or changes operating status during the reporting period or a later reference version. |
| Cause | Route suspension, regulatory action, insolvency, merger, or operator decision. |
| Consequence | The roster may include a non-operating airline without a status rule; reports may show active airline capacity or revenue for an inactive carrier; historical facts may be misread. |
| Likelihood | Low for the 12-month baseline (all ten are initially active); Medium for a future reference version. |
| Impact | High. |
| Mitigation | `IsActive` Boolean and `StatusEffectiveDate`; Tier 3 scope change; new `ReferenceVersion`; prior status retained in immutable snapshots; T-78 lifecycle/version checks; owner-approved change note. |
| Owner | Project Owner accountable; Data Architecture/QA responsible for evidence. |
| Residual risk | Medium until the lifecycle rule is applied to a real reference version and T-78 is executed; Low after verified evidence. |
| Status | `PROPOSED — NOT APPROVED` |

### R-10 — Reference-version change after refresh

| Field | Proposed entry |
|---|---|
| Risk ID | `R-10` |
| Risk description | A reference dataset is updated after a model refresh, or a refresh selects a different airline reference version from the one used for generation. |
| Cause | Uncontrolled reference update, refresh parameter drift, manifest mismatch, or missing version pinning. |
| Consequence | Silent version drift; airline facts and dimension attributes from different snapshots; non-reproducible airline-level results. |
| Likelihood | Medium. |
| Impact | High. |
| Mitigation | One approved `ReferenceVersion`; manifest authority; `SelectedReferenceVersion`; T-78-01 to T-78-10; fail closed on mismatch; immutable reference snapshots. |
| Owner | Project Owner accountable; Data Architecture/QA responsible for T-78 evidence. |
| Residual risk | Medium until manifest and T-78 are implemented; Low after successful evidence. |
| Status | `PROPOSED — NOT APPROVED` |

### R-11 — Historical reproducibility and consistency

| Field | Proposed entry |
|---|---|
| Risk ID | `R-11` |
| Risk description | Historical synthetic facts become inconsistent with a changed airline identity, or a correction re-keys facts or overwrites a prior reference version. |
| Cause | Reassigned `AirlineKey`, rebuilt dimension, mutable reference snapshot, or missing reconciliation note. |
| Consequence | Broken trends; facts linked to the wrong airline; unreproducible historical reports; audit failure. |
| Likelihood | Medium. |
| Impact | High. |
| Mitigation | Permanent `AirlineKey`; stable `AirlineId`; immutable snapshots; no re-keying; T-78-09/10; reconciliation note for corrections; seeded reproducibility evidence. |
| Owner | Project Owner accountable; Data Architecture/QA responsible for reconciliation evidence. |
| Residual risk | Medium until T-78 and reproducibility tests are executed; Low after verified evidence. |
| Status | `PROPOSED — NOT APPROVED` |

No risk has been accepted. No risk register file has been modified or created.

---

## 6. H-05 — Proposed precise G3 wording

### 6.1 Problem

The ledger currently uses one label, `NOT STARTED`, while also presenting design evidence. That makes it unclear whether design work exists, whether decisions are approved, whether the gate has run, or whether the schema is frozen.

### 6.2 Proposed separate dimensions

| Dimension | Proposed wording | Meaning |
|---|---|---|
| Design documentation | `PREPARED — DRAFT` | Contract v1.5, OD-01A/B v0.1, and design blueprints exist; this is not a gate status or approval. |
| Decision status | `NOT FORMALLY APPROVED` | OD-01A/B and other critical decisions remain unsigned/pending. |
| G3 gate execution | `NOT STARTED` / `NOT EXECUTED` | No G3 gate review has been held; blueprints do not start the gate. |
| Schema freeze | `NOT AUTHORIZED` | No schema is frozen. |
| G4 | `BLOCKED` | G4 remains blocked until G3 passes and written authorization exists. |

### 6.3 Proposed ledger wording

```text
G3 — Data design gate: NOT STARTED — gate review not executed.
G3 design documentation: PREPARED — DRAFT; contract v1.5 and OD-01A/B v0.1 exist, but this is not approval.
G3 decision status: NOT FORMALLY APPROVED — OD-01A/B signatures and other critical decisions pending.
Schema freeze: NOT AUTHORIZED.
G4 — Data generation: BLOCKED.
```

This wording does not mark G3 started merely because blueprints exist, and does not mark it complete.

### 6.4 Status

`PROPOSED — D-10 PENDING`. The ledger remains unchanged.

---

## 7. M-07 and M-12 — Proposed workflow and narrow scope

### 7.1 Proposed approval workflow

1. Prepare the decision record and evidence index.
2. Owner performs structured self-review (`CC-01`); record it as owner self-review.
3. Challenge the package with an independent reviewer (`CC-02`) or the documented compensating controls (`CC-06`/`CC-09`); never call AI review independent.
4. Re-audit and close the required findings; record `CLOSED`, `PARTIALLY CLOSED`, or `OPEN`.
5. Owner records the decision, scope, conditions, and residual concerns.
6. Owner signs and dates the record; evidence references are completed.
7. Signed copy is retained read-only; SHA-256 is recorded; retention is confirmed.
8. Future independent review is scheduled as a separate improvement.
9. `G3-RV-01` is prepared and approved only after formal OD-01A/OD-01B decisions and reference evidence.

### 7.2 Reviewer result vocabulary

- `CONCUR`
- `CONCUR WITH RESERVATIONS`
- `DISSENT`
- `N/A — compensating control accepted`

No reviewer identity is assigned or invented.

### 7.3 M-12 scope statement

The approval must state that it is a decision-rule approval, not a schema freeze, and not authorization for reference data, synthetic data, ETL, Power Query, or Power BI. The B-04 scope statements in Section 3 satisfy M-12 when incorporated into the signature blocks.

### 7.4 Status

`PROPOSED — D-03 and D-10 PENDING`.

---

## 8. Proposed controlled changes and affected files

| Change | Affected file(s) | Proposed change | Authorization |
|---|---|---|---|
| `CH-01` | `OD01A_AIRLINE_POPULATION_DECISION.md` | v0.2: correct E-07; add reviewer/control statement; add approval-block fields; add re-audit precondition; add revision history; update hash. | `D-03` pending |
| `CH-02` | `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | v0.2: correct shared E-07; add explicit scope/exclusions; add approval-block fields; add re-audit precondition; add `BusinessModelClass` null-baseline note if D-05 approved; add revision history; update hash. | `D-03`, `D-05` pending |
| `CH-03` | Future addendum, original confirmation unchanged | Create the B-05 addendum as a separate controlled record. | `D-04` pending |
| `CH-04` | Risk register / controlled addendum | Add R-09 to R-11. | `D-09` pending |
| `CH-05` | `PROGRESS_LEDGER.md` | Replace the contradictory G3 wording with the split status block. | `D-10` pending |
| `CH-06` | Future `docs/approvals/` | Create retention structure, hash register, and verification log at signature. | `D-08` pending |
| `CH-07` | Future contract/design change | Adopt staleness thresholds and `ManifestHash` method. | `D-06`, `D-07` pending |
| `CH-08` | OD-01A / OD-01B | Execute formal signatures after all conditions close. | `D-11` pending |
| `CH-09` | Future gate/reference artifacts | Prepare and execute `G3-RV-01`; create reference data only after separate authorization. | `D-12` pending |

No existing document has been modified. No new controlling record has been executed.

---

## 9. Verification

### 9.1 Method

- `Get-FileHash -LiteralPath <path> -Algorithm SHA256`.
- Byte inspection for UTF-8 BOM.
- CRLF count by byte inspection.
- `Select-String` for stale scope hashes, R-09 to R-11, reviewer fields, G3 status, and pending decisions.
- Directory and file-count checks for implementation artifacts.

### 9.2 Results for existing files

- All current controlling files listed in Section 1.2 were UTF-8 without BOM and LF-only.
- Current scope hash: `9A9EEA...512C`; old backup hash: `3238D7...72B9`.
- OD-01A still contains the stale E-07 hash; OD-01B inherits it through the shared index.
- No current project risk register contains the required H-04 scenarios; proposed R-09 to R-11 are in this proposal.
- The ledger still says G3 `NOT STARTED` with design evidence; H-05 wording is proposed only.
- No reviewer identity, reviewer signature, owner signature, or approval date is present.
- `docs/approvals/` is absent; `data/04_reference/`, `data/manifests/`, `qa/results/`, `qa/screenshots/`, and `power_bi/` contain no files.
- No Git operation was performed.

### 9.3 New-file verification

The new proposal and decision packet are verified after creation by PowerShell for existence, SHA-256, byte length, UTF-8 without BOM, and LF-only line endings. Their exact hashes are reported in the final response. The verification is document integrity, not independent assurance.

---

## 10. Status and stop condition

- OD-01A: `NOT READY` for formal signature.
- OD-01B: `NOT READY` for formal signature.
- D-01/D-02: recorded as owner instructions; no formal approval.
- D-03 to D-10: `PENDING`.
- H-04, H-05, M-07, M-12: partially closed; signature blockers remain.
- G3: `NOT STARTED`.
- G4: `BLOCKED`.
- `G3-RV-01`: `NOT EXECUTED`.

**Stop condition:** No signatures, approvals, reference CSVs, synthetic datasets, production Python, Power Query, DAX, Power BI, schema freeze, G3/G4 advancement, or Git operations. The owner must review the decision packet and explicitly approve the next controlled changes.

---

## Annex A — Proposed owner-confirmation addendum

**Status:** PROPOSED — NOT SIGNED — NOT AN APPROVAL. This text is not a separate controlling record until D-04 is approved.

> **Controlled addendum to OD-01 Owner Decision Confirmation**
>
> **Original record:** `OD01_OWNER_DECISION_CONFIRMATION.md`, SHA-256 `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`.
>
> 1. The eight owner-confirmed choices in the original record remain valid.
> 2. The current governing contract is `03_DATA_CONTRACTS.md` version 1.5, SHA-256 `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9`.
> 3. OD-01A and OD-01B have been prepared as version 0.1 records, prepared 2026-11-01.
> 4. Historical statements in the original confirmation’s document-control table, section 7.1, and section 9.1 are superseded by later dated evidence.
> 5. No signature, formal approval, schema freeze, reference-data authorization, synthetic-data authorization, G3 change, or G4 change is implied.
>
> Owner acceptance: [BLANK — D-04 PENDING]
>
> Recorded by: ______________________________
> Date: ____________________________________
