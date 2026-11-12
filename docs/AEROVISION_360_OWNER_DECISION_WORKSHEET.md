# AEROVISION 360 — Owner Decision Worksheet

**Document ID:** AEROVISION-360-ODW-2026-11-03  
**Document type:** Owner decision-support worksheet — not an approval, signature, waiver, gate decision, or implementation authorization  
**Status:** `PREPARED — OWNER RESPONSE REQUIRED`  
**Prepared:** 2026-11-03 — worksheet date only; this is not an approval date or signature date  
**Prepared by:** AI coding agent — non-independent preparer  
**Project owner / approver:** KH Mohammad Farhan  
**Governing contract:** `docs/03_DATA_CONTRACTS.md` version 1.5 — `DRAFT — PENDING REVIEW AND FORMAL APPROVAL`  
**Governing scope:** `docs/01_PROJECT_SCOPE.md` version 1.1  
**Primary investigation:** `docs/AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md`  
**Fresh re-audit:** `docs/OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md`  
**Decisions covered:** `GOV-D-04` through `GOV-D-08` — the governance-packet decisions `D-04` through `D-08`  
**Read-only status:** this worksheet is the only file created by this task. No existing project document was modified. No decision was approved, signed, or dated.

> **Do not sign OD-01A or OD-01B on the basis of this worksheet.**
>
> This worksheet is decision support. It does not approve any option, record any owner choice, create reference data, authorize schema freeze, execute `G3-RV-01`, start G3, or unblock G4. Every recommendation below is analytical and remains subject to the owner’s explicit written decision.

---

## 1. Executive summary

### 1.1 Bottom line

- **FACT.** Five governance decisions remain unresolved: `GOV-D-04` through `GOV-D-08`. The decision packet marks all five `PENDING`, and the revision 0.2 change record confirms that none is approved.
- **FACT.** No owner-confirmation addendum exists. `OD01_OWNER_DECISION_CONFIRMATION.md` still states contract v1.4 and says OD-01A/OD-01B are “not prepared,” while the current contract is v1.5 and both decision records are revision 0.2.
- **FACT.** `BusinessModelClass` has no populated baseline and no approved analytical mapping. The column is optional and nullable in the design, but `GOV-D-05` remains pending while OD-01B Section 4 sits inside the proposed approval scope.
- **FACT.** The 365-day and 180-day source-staleness thresholds and the 90-day exception are proposals only. Contract v1.5 expressly says they are not owner-approved.
- **FACT.** The `ManifestHash` canonical-JSON method is a proposal only. No manifest exists, and the method is not yet in the contract as an approved rule.
- **FACT.** No evidence-retention structure exists. `docs/approvals/` is absent, no signed copy exists, and no hash register exists.
- **FACT.** OD-01A and OD-01B are both `NOT READY FOR SIGNATURE`; G3 gate execution is `NOT STARTED`; G3 formal approval is `NOT FORMALLY APPROVED`; schema freeze is `NOT AUTHORIZED`; `G3-RV-01` is `NOT EXECUTED`; G4 is `BLOCKED`.
- **RECOMMENDATION.** Resolve the five decisions in one owner-response round, then authorize one controlled documentation-correction package. Execute the owner self-review, re-audit the corrected package, sign OD-01A first and OD-01B second with real dates and evidence, then decide `GOV-D-06` and `GOV-D-07` before preparing `G3-RV-01`.
- **RECOMMENDATION.** Do not populate `BusinessModelClass`, create reference CSVs, start G3/G4, or claim independent assurance while these decisions and evidence gaps remain open.

### 1.2 Decision summary

| ID | Topic | Current status | Worksheet recommendation | Signature impact | G3 / G4 impact |
|---|---|---|---|---|---|
| `GOV-D-04` | Historical owner-confirmation addendum | `PENDING OWNER APPROVAL` | **APPROVE a separate controlled addendum**, preserving the original, with corrected v0.2 text and current hashes | Removes a contradictory evidence-chain statement; supports a clean signature record | No direct G3-RV-01 block; does not start G3 or G4 |
| `GOV-D-05` | `BusinessModelClass` baseline | `PENDING OWNER APPROVAL` | **Option A — keep all values null**; optional nullable analytical column; no population | Allows OD-01B to be signed with an explicit no-population condition | No G3-RV-01 block; a populated column without a rubric would block schema freeze |
| `GOV-D-06` | Source-staleness thresholds and exceptions | `PENDING OWNER APPROVAL` | **APPROVE the 365/180-day policy with an explicit attribute matrix and 90-day exception rules** | Not a direct signature blocker, but the policy must be settled before reference approval | Blocks `G3-RV-01`; indirectly blocks G3; G4 remains blocked |
| `GOV-D-07` | `ManifestHash` canonicalization | `PENDING OWNER APPROVAL` | **APPROVE a fully specified canonical-JSON method** with exact serialization, a method version, and a test vector | Not a direct signature blocker, but needed for reproducible reference approval | Blocks `G3-RV-01`; indirectly blocks G3; G4 remains blocked |
| `GOV-D-08` | Evidence-retention policy | `PENDING OWNER APPROVAL` | **APPROVE the proposed structure and read-only procedure**, with a named custodian and explicit retention period | Completes the signed-copy retention condition; does not itself sign anything | No direct G3-RV-01 block; does not start G3 or G4 |

### 1.3 What the owner is being asked to do

1. **RECOMMENDATION.** Read this worksheet, the investigation report, and the fresh re-audit.
2. **RECOMMENDATION.** Record an explicit choice for each of `GOV-D-04` through `GOV-D-08` using the response template in Section 17.
3. **RECOMMENDATION.** Decide the separate key-map approval route described in Section 10. This is not one of `GOV-D-04`–`GOV-D-08`, but it blocks a clean OD-01B signature.
4. **RECOMMENDATION.** Authorize one controlled documentation-correction package only after the choices are recorded.
5. **RECOMMENDATION.** Execute and record the owner self-review under `CC-01`, sign the no-reviewer limitation under `CC-09`, and accept or reject residual risks.
6. **RECOMMENDATION.** Re-audit the corrected package, then sign OD-01A first and OD-01B second using actual dates and evidence.

### 1.4 What this worksheet does not do

- **FACT.** It does not sign OD-01A or OD-01B.
- **FACT.** It does not mark any decision approved.
- **FACT.** It does not invent an approval date, reviewer identity, hash, or evidence.
- **FACT.** It does not create reference CSVs, a manifest, synthetic data, code, Power Query, DAX, Power BI, or a schema freeze.
- **FACT.** It does not execute `G3-RV-01`, start G3, or unblock G4.
- **FACT.** It does not modify any existing project document.

---

## 2. How to read this worksheet

### 2.1 Statement labels

Every substantive statement is labelled so that verified facts are not confused with design, proposals, or advice.

| Label | Meaning |
|---|---|
| **FACT** | Verified against a current project document or a current repository check. The source is cited. |
| **EXISTING DESIGN** | Already written in a current governing, decision, or design document. “Existing” does not mean “approved.” |
| **PROPOSAL** | An option, draft rule, or draft text under consideration. It is not approved. |
| **RECOMMENDATION** | Analytical advice from this worksheet. It is not an owner decision and creates no approval. |

### 2.2 Status vocabulary

| Status | Meaning in this worksheet |
|---|---|
| `VERIFIED` | Confirmed against the current file, hash, or repository state. |
| `DOCUMENTED BUT NOT VERIFIED` | Written in a document, but not independently or operationally verified. |
| `PARTIALLY VERIFIED` | Some required elements are present and verified; others remain missing or ambiguous. |
| `NOT FOUND` | No current artifact or evidence was found. |
| `PENDING OWNER APPROVAL` | The owner has not recorded an explicit decision. |
| `BLOCKED` | A required precondition is unmet; work must not proceed. |

### 2.3 Identifier rule for this worksheet

Bare `D-04` through `D-08` in this worksheet mean the **governance-packet decisions**, not the contract’s `OD-04` through `OD-08` and not the remediation design specification’s local `D-04` through `D-08`. Bare `B-05` and `B-08` mean the **governance blockers** unless the text explicitly says `OD01B-B-05` or `OD01B-B-08`.

| Qualified ID | Meaning | Original source |
|---|---|---|
| `GOV-D-04`–`GOV-D-08` | Owner decisions in the governance packet | `docs/OD01_OWNER_DECISION_PACKET.md`, Part B |
| `GOV-B-03`–`GOV-B-08` | Governance evidence/blocker items | `docs/OD01_GOVERNANCE_CLOSURE_PROPOSAL.md` and `docs/OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` |
| `OD01B-B-01`–`OD01B-B-08` | OD-01B-specific evidence items | `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` Section 10 |
| `CON-OD-01`–`CON-OD-22` | Contract technical decisions | `docs/03_DATA_CONTRACTS.md` Section 14 |
| `DES-D-01`–`DES-D-18` | Local design decisions in the remediation specification | `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` Section 3 |
| `RA-C-01`–`RA-C-10` | Contradictions in the fresh re-audit | `docs/OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md` Section 5 |

**FACT.** The current project documents use bare identifiers in several places. This worksheet does not rewrite those documents. The proposed namespace convention is analysed in Section 11 and can be adopted by a future controlled change.

### 2.4 Current authority chain

| Layer | Document | Current status | What it can and cannot do |
|---|---|---|---|
| Scope | `01_PROJECT_SCOPE.md` v1.1 | Current | Defines the project boundary; does not approve OD-01A/OD-01B |
| Contract | `03_DATA_CONTRACTS.md` v1.5 | `DRAFT — PENDING REVIEW AND FORMAL APPROVAL` | Defines technical rules; not a formal approval or schema freeze |
| Owner confirmation | `OD01_OWNER_DECISION_CONFIRMATION.md` | Historical; unsigned | Records eight owner-confirmed choices; contains stale v1.4/“not prepared” statements |
| Decision records | `OD01A` v0.2; `OD01B` v0.2 | `OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING` | Define the proposed decisions; not signed |
| Revision authorization | `OD01_REVISION_0.2_CHANGE_RECORD.md` | Implemented at document level | Records D-03/D-09/D-10 authorization; not a signature |
| Re-audit | `OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md` | Non-independent document re-audit | Assesses readiness; not independent assurance |
| Investigation | `AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md` | Completed report | Evidence and analysis; not approval |
| This worksheet | `AEROVISION_360_OWNER_DECISION_WORKSHEET.md` | `PREPARED — OWNER RESPONSE REQUIRED` | Decision support; not approval |

---

## 3. `GOV-D-04` — Historical owner-confirmation addendum

### 3.1 Original decision definition

> **FACT.** The packet asks: “Do you approve a separate controlled addendum to the original owner confirmation stating that the eight choices remain valid, contract v1.5 is current, OD-01A/OD-01B are prepared, historical status statements are superseded, and no approval is implied?”
>
> Source: `docs/OD01_OWNER_DECISION_PACKET.md` lines 84–97.

**EXISTING DESIGN.** The packet’s recommended choice is to approve the addendum and preserve the original record unchanged. Its alternatives are a dated reliance note, deferral, or rejection.

### 3.2 Why the decision exists

- **FACT.** `OD01_OWNER_DECISION_CONFIRMATION.md` states that the governing contract is version 1.4 — unchanged — at lines 20 and 82, and states that OD-01A and OD-01B are “not prepared or signed” at lines 357–358.
- **FACT.** The current contract is version 1.5, SHA-256 `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9`, 211,846 bytes.
- **FACT.** OD-01A and OD-01B are now revision 0.2, prepared 2026-11-01 and revised 2026-11-02. Their current hashes are `2140081A100DFAA0BB87ACC7B9DC429A49D99CE638C09905BBD5A221C12146D9` and `15AE19A42C537F56EFDD1E55CEF15EC73D6472AE520B1AC41EB815118852D7EB`.
- **FACT.** The revision 0.2 change record records D-03/D-09/D-10 authorization but does not itself state contract v1.5. The prior remediation change record documents the v1.4→v1.5 change.
- **FACT.** The proposed Annex A in `OD01_GOVERNANCE_CLOSURE_PROPOSAL.md` is stale: it cites OD-01A and OD-01B as version 0.1 records prepared 2026-11-01 (lines 393–394), not the current v0.2 records. It also does not carry the current decision-record hashes.
- **FACT.** No addendum exists. The original confirmation is preserved at SHA-256 `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`.

**EXISTING DESIGN.** The governance closure proposal’s `GOV-B-05` is the owner-confirmation addendum. It is not the same as `OD01B-B-05`, which is the reference manifest.

### 3.3 Current status

| Field | Status |
|---|---|
| Owner decision | `PENDING OWNER APPROVAL` |
| Addendum artifact | `NOT FOUND` |
| Original confirmation | Preserved; stale statements remain on its face |
| Current contract | v1.5, draft, pending formal approval |
| Current decision records | OD-01A v0.2; OD-01B v0.2; unsigned |
| Governance blocker | `GOV-B-05` remains `OPEN — D-04 PENDING` |
| Signature effect | Contradictory evidence chain remains until resolved |

### 3.4 Available options

| Option | Description | Advantages | Disadvantages | Consequence |
|---|---|---|---|---|
| **A — Controlled addendum** | **PROPOSAL.** Create a separate, dated addendum that preserves the original and states the current contract version, current decision-record versions, superseded historical statements, and no implied approval. | Preserves history; reconciles the evidence chain; makes the current facts explicit; does not alter the original hash. | Requires a new controlled artifact and careful wording; must not imply approval. | **RECOMMENDATION:** adopt this option, with corrected v0.2 text. |
| **B — Dated reliance note** | **PROPOSAL.** Add a shorter note stating that later evidence should be relied on instead of the historical statements. | Lighter than a full addendum; preserves the original. | Less structured; easier to overlook; may not state all eight choices remain valid; weaker evidence chain. | Acceptable fallback, but weaker than A. |
| **C — Defer** | **PROPOSAL.** Leave the contradiction in place until signature. | No new document now. | The signature package remains internally contradictory; a reader cannot tell which contract version governs. | Does not resolve the blocker; increases signature risk. |
| **D — Reject** | **PROPOSAL.** Decline an addendum and leave the original as the only record. | No new artifact. | The evidence chain remains contradictory; the owner confirmation still says v1.4 and “not prepared.” | Not recommended. |
| **E — Rewrite the original** | **PROPOSAL.** Edit `OD01_OWNER_DECISION_CONFIRMATION.md` directly. | Would remove the stale text. | Destroys the historical record and its hash; violates preservation; creates a false impression that the original said something it did not. | **Not permitted.** |

### 3.5 Technical and governance consequences

- **FACT.** `GOV-D-04` is a documentation-control decision, not a design change. It does not alter the eight owner-confirmed choices, the airline population, the identity model, the contract schema, or any test.
- **FACT.** The addendum would not approve OD-01A or OD-01B. It would only reconcile the historical confirmation with later dated evidence.
- **RECOMMENDATION.** The addendum should state that the eight choices remain valid, that contract v1.5 is the current governing baseline, that OD-01A and OD-01B are revision 0.2 records, that the historical v1.4/“not prepared” statements are superseded, and that no approval is implied.
- **RECOMMENDATION.** The addendum should include the current hashes of the contract and both decision records, and should preserve the original confirmation’s hash. It should not use the stale v0.1 text in Annex A without correction.

### 3.6 Impact on OD-01A and OD-01B

| Record | Impact |
|---|---|
| OD-01A | Precondition 8 currently says “B-05 is resolved by D-04, and B-08 is resolved by D-08.” In the governance namespace this is correct for `GOV-B-05`/`GOV-B-08`, but the bare identifiers are ambiguous. The addendum removes the contract-version contradiction and gives the signature a clean evidence reference. |
| OD-01B | Same precondition and evidence-chain issue. The addendum does not resolve `OD01B-B-05` (reference manifest) or `OD01B-B-08` (independent reviewer). |
| Both | The residual-concerns rows still list `B-03`, `B-04`, `B-05`, and `B-08` as open without current statuses; the addendum should be accompanied by corrected residual rows. |

### 3.7 Impact on G3 and G4

- **FACT.** The decision packet says `GOV-D-04` does not directly block `G3-RV-01` and does not directly block G3. It weakens the decision evidence chain.
- **FACT.** G4 remains blocked independently by the absence of G3 approval and written G4 authorization.
- **RECOMMENDATION.** Resolve `GOV-D-04` before signing OD-01A/OD-01B so the signature package does not rely on a confirmation that still says v1.4.

### 3.8 Required documentation changes

1. **Create** a separate controlled addendum, provisionally `docs/OD01_OWNER_DECISION_CONFIRMATION_ADDENDUM.md`, after owner approval and separate authorization.
2. **Do not edit** `OD01_OWNER_DECISION_CONFIRMATION.md`; preserve its current hash.
3. **Correct** the addendum text to cite OD-01A v0.2 and OD-01B v0.2, not v0.1.
4. **Include** the current contract hash, the two decision-record hashes, the original confirmation hash, and a clear “no approval implied” statement.
5. **Update** OD-01A §7.1 precondition 8 and OD-01B §11.1 precondition 8 to use qualified identifiers: `GOV-B-05` resolved by `GOV-D-04`; `GOV-B-08` resolved by `GOV-D-08`.
6. **Update** the residual-concerns rows in both decision records to reflect current statuses.
7. **Record** the addendum in the evidence register and the revision/change record after it is created.
8. **Do not** treat the addendum as an OD-01A/OD-01B signature or as approval of the contract.

### 3.9 Dependencies and required evidence

| Dependency / evidence | Status |
|---|---|
| Owner approval of `GOV-D-04` | `PENDING` |
| Original confirmation hash | `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD` |
| Contract v1.5 hash | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` |
| OD-01A v0.2 hash | `2140081A100DFAA0BB87ACC7B9DC429A49D99CE638C09905BBD5A221C12146D9` |
| OD-01B v0.2 hash | `15AE19A42C537F56EFDD1E55CEF15EC73D6472AE520B1AC41EB815118852D7EB` |
| Revision 0.2 change record | `1B91069C8043A7E5877F3EEB540ACC57766A677DA17BD902A7C49527FA344ECB` |
| Owner signature/date on addendum | `NOT RECORDED` — must be actual if signed |

### 3.10 Recommendation and justification

**RECOMMENDATION.** Approve **Option A**, a separate controlled addendum, and direct that the stale Annex A text be corrected to v0.2 before use.

**Justification.** The original confirmation is a genuine historical record. Rewriting it would destroy evidence; leaving it unqualified would make the signature package rely on a document that says contract v1.4 and “not prepared.” A separate addendum is the least destructive and most auditable reconciliation. It preserves the original hash, states the current facts, and does not imply approval.

**What this recommendation is not.** It is not an owner approval, not a signature, and not a finding that the addendum text already exists in acceptable form.

### 3.11 Exact owner approval required

The owner must record one of the following, with initials and an actual date:

```text
GOV-D-04 — Historical owner-confirmation addendum

[ ] APPROVE Option A — separate controlled addendum
[ ] APPROVE Option B — dated reliance note instead of an addendum
[ ] DEFER
[ ] REJECT

Addendum version/hash approved for preparation: ______________________
Conditions / required corrections: __________________________________
____________________________________________________________________

Owner initials: __________   Actual date: __________________
```

**FACT.** No field above is completed in this worksheet.

---

## 4. `GOV-D-05` — `BusinessModelClass` baseline

### 4.1 Original decision definition

> **FACT.** The packet asks: “Should all `BusinessModelClass` values remain null for the baseline, or should a documented analytical mapping/rubric be approved?”
>
> Source: `docs/OD01_OWNER_DECISION_PACKET.md` lines 99–112.

**EXISTING DESIGN.** The packet’s recommended choice is Option A — all values null. The alternatives are Option B — approve a documented rubric and mapping — or remove the column entirely, which would reopen the owner-confirmed choice.

### 4.2 Why the decision exists

- **FACT.** `BusinessModelClass` is defined as an optional, nullable analytical classification. It is not source-verified identity and has no identity provenance. See OD-01B lines 79–83 and 176, and contract lines 247, 252, 365, and 766.
- **FACT.** OD-01B states `D-05` remains `PENDING` and that the revision does not authorize a populated baseline or a mapping/rubric (lines 82–83 and 185–188).
- **FACT.** The remediation design specification contains a proposed analytical rubric in §6.4, but it expressly says no airline-specific value is assigned and the owner may omit the attribute entirely. The rubric is a proposal, not an approved mapping.
- **FACT.** No mapping owner, allowed-value governance, examples, versioning rule, or populated value exists.
- **FACT.** OD-01B Section 4 is inside the proposed approval scope (Sections 2, 4, 5, 6, and 8), so the signature would approve the nullable column design while the population decision remains pending. The approval block does not yet state that no values are approved.

### 4.3 Current status

| Field | Status |
|---|---|
| Owner decision | `PENDING OWNER APPROVAL` |
| Column design | Optional nullable analytical classification; existing design |
| Populated values | `NONE` |
| Approved rubric/mapping | `NOT FOUND` |
| OD-01B Section 4 | Inside proposed approval scope |
| Approval condition stating “no values approved” | `NOT FOUND` |
| Governance blocker | `GOV-B-06` remains `PENDING — D-05` |

### 4.4 Available options

| Option | Description | Advantages | Disadvantages | Consequence |
|---|---|---|---|---|
| **A — Null baseline** | **PROPOSAL.** Keep all `BusinessModelClass` values null; keep the column optional and nullable; do not populate from `ref_airlines.csv`; label it analytical in reports. | Avoids unsupported classification and false precision; does not block identity work; preserves the owner-confirmed column design; simplest path. | Reports cannot use business-model segmentation in the baseline; a future mapping will require a controlled change. | **RECOMMENDATION:** adopt Option A. |
| **B — Documented mapping** | **PROPOSAL.** Approve a written rubric, allowed values, mapping owner, versioning, examples, classification method, notes, analyst, date, and reference version; populate the column from that mapping. | Enables analytical segmentation; makes the method explicit. | Requires genuine analytical judgment; risks inconsistent labels; needs a mapping owner and review; may delay schema freeze; cannot be presented as source-verified identity. | Acceptable only with a complete, owner-approved rubric and no identity-provenance claim. |
| **C — Remove the column** | **PROPOSAL.** Drop `BusinessModelClass` from `DimAirline` entirely. | Simplifies the model; removes an unused analytical attribute. | Reopens the owner-confirmed design; changes the dimension schema; may remove a desired analytical capability. | Not recommended unless the owner intentionally reopens the design. |
| **D — Defer** | **PROPOSAL.** Leave the decision open and sign OD-01B with a condition. | Avoids a premature choice. | The approval scope still contains Section 4; the condition must be explicit; the decision remains a known open item. | Possible, but weaker than A because it leaves an avoidable ambiguity. |

### 4.5 Technical and governance consequences

- **FACT.** A null baseline does not block `G3-RV-01`. `G3-RV-01` concerns airline identity and reference provenance, not this analytical classification.
- **FACT.** A populated column without an approved rubric and mapping would block schema freeze, because the column would contain unsupported analytical values.
- **FACT.** `BusinessModelClass` is excluded from `ref_airlines.csv` and from identity provenance. Any mapping must therefore be a separate analytical artifact, not a source-identity claim.
- **RECOMMENDATION.** If Option A is chosen, add an explicit approval condition: “No `BusinessModelClass` baseline values are approved; the column remains optional and nullable; any future population requires a separately approved rubric and mapping.”
- **RECOMMENDATION.** If Option B is chosen, require the rubric, allowed values, mapping owner, examples, versioning, classification method, and review cadence before any value is populated. Do not populate values during this task.

### 4.6 Impact on OD-01A and OD-01B

| Record | Impact |
|---|---|
| OD-01A | No substantive impact. The population record does not define `BusinessModelClass`. |
| OD-01B | Direct impact. Section 4 defines the column and is inside the proposed approval scope. The approval block must state the no-population condition if Option A is chosen. Precondition 9 already says D-05 remains pending and no value is populated; that condition should be repeated in the approval conditions and scope. |
| Both | The residual-concerns rows and evidence index should reflect the final D-05 status. |

### 4.7 Impact on G3 and G4

- **FACT.** The decision packet says `GOV-D-05` does not block `G3-RV-01`.
- **FACT.** A null baseline does not block schema freeze. A populated column without a rubric would block schema freeze.
- **FACT.** G4 remains blocked by G3 and written authorization, independent of D-05.
- **RECOMMENDATION.** Do not treat the nullable column design as approval to populate the column.

### 4.8 Required documentation changes

**If Option A — null baseline (recommended):**

1. **Update** OD-01B §11.1 precondition 9 and §11.4 approval conditions to state: no `BusinessModelClass` values are approved; the column remains optional and nullable; future population requires a controlled change.
2. **Update** OD-01B §2.6 and §4 to state the decision is recorded as Option A, not merely pending.
3. **Keep** contract §3.4, §4.3, and §6.2.2 aligned: optional analytical classification; no identity provenance; no source-verified claim.
4. **Record** `GOV-D-05` in the decision register and evidence register.
5. **Do not** add a rubric or populate values.

**If Option B — mapping:**

1. **Create** a separate controlled analytical mapping/rubric document with allowed values, definitions, decision rules, examples, mapping owner, review cadence, versioning, and classification metadata.
2. **Update** OD-01B and the contract to reference the approved mapping and to state that it is analytical, not source-verified identity.
3. **Do not** populate `ref_airlines.csv`; keep the mapping separate from identity provenance.
4. **Require** schema-freeze review of the populated column.
5. **Record** the owner approval and evidence.

### 4.9 Dependencies and required evidence

| Dependency / evidence | Status |
|---|---|
| Owner choice A or B | `PENDING` |
| Current OD-01B text defining the optional column | Present |
| Proposed rubric in design specification §6.4 | `PROPOSAL` only; not approved |
| Mapping owner, examples, versioning (if B) | `NOT FOUND` |
| Populated values | `NONE` |
| Approval condition in OD-01B | `NOT FOUND` |

### 4.10 Recommendation and justification

**RECOMMENDATION.** Choose **Option A — all values null**.

**Justification.** The project has no approved analytical rubric, no mapping owner, and no examples. Populating the column now would create unsupported labels and could imply source-verified business-model identity, which the contract expressly rejects. A null baseline preserves the owner-confirmed column design, avoids false precision, and does not block identity work or `G3-RV-01`. A future mapping can be added through a controlled change when the project is ready to own and review it.

**What this recommendation is not.** It is not an approval of the column, not a finding that the column is required, and not authorization to populate it.

### 4.11 Exact owner approval required

```text
GOV-D-05 — BusinessModelClass baseline

[ ] Option A — NULL baseline; column remains optional and nullable; no values populated
[ ] Option B — MAPPING; approve a documented analytical rubric and mapping
[ ] DEFER

If Option B:
  Rubric/mapping document: ______________________________________
  Mapping owner: _______________________________________________
  Allowed values/version: ______________________________________
  Review cadence: ______________________________________________

Conditions: ____________________________________________________
________________________________________________________________

Owner initials: __________   Actual date: __________________
```

**FACT.** No field above is completed in this worksheet.

---

## 5. `GOV-D-06` — Source-staleness thresholds and exceptions

### 5.1 Original decision definition

> **FACT.** The packet asks: “Do you approve the proposed 365-day maximum for airline name, legal name, group, and home country; 180-day maximum for IATA/ICAO codes; and a maximum 90-day written exception, with stale sources quarantined and not loadable?”
>
> Source: `docs/OD01_OWNER_DECISION_PACKET.md` lines 114–127.

**EXISTING DESIGN.** The packet recommends approving the proposed thresholds and exception policy. Alternatives are stricter thresholds, no exceptions, different anchor dates, or deferral.

### 5.2 Why the decision exists

- **FACT.** Contract v1.5 §3.4 says the proposed maximum age is 365 days for names, legal names, and group, and 180 days for IATA and ICAO codes, measured from `SourceVerifiedDate` to the reference-version approval date (or the current date if earlier). It expressly says these are proposed policy, not owner-approved values (line 260).
- **FACT.** The design specification §7.6 repeats the 365/180-day proposal and says the thresholds are proposed policy (line 531).
- **FACT.** The compensating-control proposal §8.1 adds a 90-day written exception, attribute-specific conditions, and a stale-action table. It states the thresholds are measurable but not owner-approved (lines 548–565).
- **FACT.** The owner packet includes `HomeCountry` in the 365-day group, while contract §3.4 line 260 names “names, legal names and group” and does not explicitly name `HomeCountry` or `HomeCountryCode`. This is an alignment defect that the decision should resolve.
- **FACT.** `G3-RV-01` cannot determine source eligibility without an approved staleness rule. No reference version exists, so no staleness decision has been applied.

### 5.3 Current status

| Field | Status |
|---|---|
| Owner decision | `PENDING OWNER APPROVAL` |
| 365-day rule | Proposed only; expressly not owner-approved |
| 180-day rule | Proposed only; expressly not owner-approved |
| 90-day exception | Proposed only; not owner-approved |
| Attribute coverage | Ambiguous between packet and contract for `HomeCountry`/`HomeCountryCode` |
| `IsActive` lifecycle | No age threshold stated |
| Governance blocker | `GOV-B-07` remains `PENDING — D-06 and D-07` |
| `G3-RV-01` | `NOT EXECUTED`; cannot determine staleness |

### 5.4 Available options

| Option | Description | Advantages | Disadvantages | Consequence |
|---|---|---|---|---|
| **A — Approve proposed policy with clarifications** | **PROPOSAL.** 365 days for `AirlineName`, `LegalName`, `AirlineGroup`, `HomeCountry`, and `HomeCountryCode`; 180 days for IATA/ICAO; 90-day written exception; stale quarantine; no stale load. | Measurable; matches the existing design; gives `G3-RV-01` a workable rule; aligns packet and contract after clarification. | Requires an explicit attribute matrix; some sources may be older than the threshold and require re-verification. | **RECOMMENDATION:** adopt Option A with the matrix in §5.5. |
| **B — Stricter thresholds** | **PROPOSAL.** Shorten the maximum ages, e.g., 180 days for names/group/home country and 90 days for codes. | Stronger freshness; reduces stale-source risk. | More re-verification work; may make legitimate stable attributes harder to approve; no evidence that stricter values are needed. | Acceptable if the owner values freshness over effort. |
| **C — No exceptions** | **PROPOSAL.** Keep the age limits but forbid the 90-day written exception. | Simplest and strictest; no exception judgment. | A required attribute with a temporarily unavailable source could block the reference version entirely. | Acceptable for a strict baseline; may delay `G3-RV-01`. |
| **D — Different anchor date** | **PROPOSAL.** Measure from `SourceRetrievedDate`, reference-version start date, or another anchor instead of `SourceVerifiedDate` to approval date. | Could align with capture date or reporting period. | `SourceRetrievedDate` records capture, not verification; a different anchor may weaken the link between verification and approval. | Not recommended without a specific reason. |
| **E — Defer** | **PROPOSAL.** Leave the thresholds unapproved. | No decision now. | `G3-RV-01` cannot determine source eligibility; reference approval remains blocked. | Does not resolve the blocker. |

### 5.5 Proposed attribute matrix (for owner decision)

**PROPOSAL.** The following matrix resolves the packet/contract ambiguity. It is not approved until the owner records it.

| Attribute group | Maximum age | Anchor | Stale action |
|---|---:|---|---|
| `AirlineName`, `LegalName`, `AirlineGroup`, `HomeCountry`, `HomeCountryCode` | 365 days | `SourceVerifiedDate` to reference-approval date, or current date if earlier | Re-verify; if not re-verified, null an optional value or reject a required value; quarantine the stale source |
| `AirlineIATACode`, `AirlineICAOCode` | 180 days | Same | Re-verify; no stale code may remain authoritative; a code change requires a new reference version |
| `IsActive` / `StatusEffectiveDate` | Event-driven; no fixed age threshold | Verify at each reference version and on any lifecycle event | If status cannot be verified, quarantine the status claim; do not infer activity from age |
| Any source with an unavailable URL | Checked at retrieval and re-verification | `SourceRetrievedDate` / verification date | Use an archived copy with a matching content hash; otherwise quarantine and do not load |

**PROPOSAL — exception rules:**

- The exception must be written, attribute-specific, and time-bound to a maximum of 90 days.
- It must state the reason, evidence inspected, residual risk, and compensating evidence.
- It must be recorded in the manifest and the `G3-RV-01` record and disclosed as a residual risk.
- It is not permitted for a `CONFLICTING` or `UNVERIFIED` source, or for an attribute with no durable evidence.
- A stale required attribute with no approved exception cannot support an approved reference version.
- `SourceRetrievedDate` must not be later than `SourceVerifiedDate`; neither may be later than the approval date.

### 5.6 Technical and governance consequences

- **FACT.** Staleness determines whether a source can support a populated identity attribute in an approved reference version.
- **FACT.** A stale record is quarantined with `STALE` and cannot support a new approved version until re-verified (contract line 260).
- **FACT.** The 90-day exception is a governance exception, not a source-verification shortcut. It must be visible in the manifest and `G3-RV-01`.
- **RECOMMENDATION.** Align the contract, OD-01B, the design specification, and `G3-RV-01` criteria to the same attribute matrix. Do not leave `HomeCountry`/`HomeCountryCode` ambiguous.
- **RECOMMENDATION.** Do not treat `IsActive` as a simple age-based attribute; it is event-driven and must be verified at each reference version.

### 5.7 Impact on OD-01A and OD-01B

| Record | Impact |
|---|---|
| OD-01A | No direct signature block. The population record requires source verification before reference approval; the staleness policy determines when a source is still eligible. |
| OD-01B | Direct impact on the reference/provenance model in Sections 5 and 7. The decision should be reflected in the reference-version approval criteria and `G3-RV-01`. |
| Both | The decision does not itself approve any source or reference version. It only sets the eligibility rule. |

### 5.8 Impact on G3 and G4

- **FACT.** `GOV-D-06` blocks `G3-RV-01`.
- **FACT.** It does not necessarily block the OD-01A/OD-01B signatures, but the signature package should not imply that reference approval is ready.
- **FACT.** G3 remains `NOT STARTED`; G4 remains `BLOCKED` until G3 approval and written G4 authorization.

### 5.9 Required documentation changes

1. **Update** contract §3.4 staleness paragraph to include the approved attribute matrix, including `HomeCountry` and `HomeCountryCode`.
2. **Update** OD-01B Section 7 and the reference-version approval criteria to cite the approved thresholds and exception policy.
3. **Update** the design specification §7.6 to remove “proposed policy” language after approval and to align the attribute matrix.
4. **Update** `G3-RV-01` criteria to require the staleness check and exception disclosure.
5. **Update** T-75/T-76 evidence expectations if needed; do not execute them.
6. **Record** the owner decision, exact thresholds, and any modifications in the decision register and evidence register.

### 5.10 Dependencies and required evidence

| Dependency / evidence | Status |
|---|---|
| Owner approval of thresholds and exception policy | `PENDING` |
| Explicit attribute matrix | Proposed in §5.5; not approved |
| Source verification records with real dates and evidence hashes/archive refs | `NOT CREATED` |
| `G3-RV-01` criteria | `NOT EXECUTED` |
| T-75/T-76 source-provenance tests | `PLANNED` |
| Reference manifest | `NOT CREATED` |

### 5.11 Recommendation and justification

**RECOMMENDATION.** Approve **Option A**, with the attribute matrix in §5.5 and the exception rules stated explicitly.

**Justification.** The proposed 365/180-day policy is measurable and already reflected in the contract and design, but the current documents do not consistently name `HomeCountry`/`HomeCountryCode`, and the 90-day exception needs precise conditions. Approving the clarified matrix gives `G3-RV-01` a deterministic eligibility rule without inventing stricter requirements that the project has not justified. The exception remains bounded and visible.

**What this recommendation is not.** It is not an approval of any source, reference version, or manifest. It does not create source evidence.

### 5.12 Exact owner approval required

```text
GOV-D-06 — Source-staleness thresholds and exceptions

[ ] APPROVE the proposed 365/180-day policy with the attribute matrix in §5.5
[ ] APPROVE modified thresholds: ________________________________
[ ] APPROVE no exceptions
[ ] DEFER
[ ] REJECT

Attribute groups and ages approved: _____________________________
Exception maximum (days): ______________________________________
Anchor date approved: __________________________________________
Conditions: ____________________________________________________
________________________________________________________________

Owner initials: __________   Actual date: __________________
```

**FACT.** No field above is completed in this worksheet.

---

## 6. `GOV-D-07` — `ManifestHash` canonicalization

### 6.1 Original decision definition

> **FACT.** The packet asks: “Do you approve the deterministic canonical-JSON method for `ManifestHash`, covering `reference_version` and fixed-order `ref_airlines.csv` / `ref_airline_sources.csv` name, byte size, and SHA-256, excluding approval metadata and the hash itself?”
>
> Source: `docs/OD01_OWNER_DECISION_PACKET.md` lines 129–142.

**EXISTING DESIGN.** The packet recommends approving the canonical-JSON method. Alternatives are hashing a concatenation of raw CSV bytes, per-file hashes only, or deferral.

### 6.2 Why the decision exists

- **FACT.** The reference manifest is the authoritative approval record, and `ManifestHash` is intended to make the reference version reproducible.
- **FACT.** The compensating-control proposal §8.2 defines a proposed method: uppercase SHA-256 of a canonical UTF-8 JSON object containing `reference_version` and a fixed-order `files` array with `name`, `bytes`, and `sha256`; approval metadata and the hash itself are excluded (lines 571–591).
- **FACT.** The method is proposed, not implemented. No manifest exists. It is not yet an approved contract rule.
- **FACT.** T-78 requires recomputation and comparison; a mismatch fails closed. Without a deterministic method, an independent reviewer cannot reproduce the hash.
- **FACT.** The current proposal does not fully specify JSON string escaping, trailing-newline behavior, method versioning, or a test vector. Those details matter for byte-for-byte reproducibility.

### 6.3 Current status

| Field | Status |
|---|---|
| Owner decision | `PENDING OWNER APPROVAL` |
| Canonical-JSON method | Proposed only |
| Manifest | `NOT CREATED` |
| `ManifestHash` value | `NOT FOUND` |
| T-78 | `PLANNED` |
| `G3-RV-01` | `NOT EXECUTED` |
| Governance blocker | `GOV-B-07` remains `PENDING — D-06 and D-07` |

### 6.4 Available options

| Option | Description | Advantages | Disadvantages | Consequence |
|---|---|---|---|---|
| **A — Canonical JSON, fully specified** | **PROPOSAL.** Hash a canonical UTF-8 JSON object with `reference_version` and the fixed-order file array; specify key order, separators, escaping, no trailing newline, uppercase hex, method version, and a test vector. | Deterministic; independently recomputable; supports T-78 and `G3-RV-01`; excludes circular approval metadata. | Requires precise specification and a test vector; any change to the method requires a new method version. | **RECOMMENDATION:** adopt Option A with the clarifications in §6.5. |
| **B — Concatenate raw CSV bytes** | **PROPOSAL.** Hash a fixed concatenation of the raw CSV bytes, possibly with a separator. | Simple; directly ties the hash to file content. | Ambiguous unless file order, separator, and metadata are fixed; does not naturally include `reference_version`; harder to extend. | Acceptable only with an exact byte-layout specification. |
| **C — Per-file hashes only** | **PROPOSAL.** Record each file’s SHA-256 but no combined manifest hash. | Simple; transparent. | Does not provide one reproducible version-level digest; easier to mix files from different versions; weaker manifest authority. | Not recommended as the only control. |
| **D — Defer** | **PROPOSAL.** Leave the method unapproved. | No decision now. | T-78 reproducibility and `G3-RV-01` remain blocked. | Does not resolve the blocker. |

### 6.5 Proposed method specification (for owner decision)

**PROPOSAL — method identifier `MH-1`.** This identifier is worksheet-local and is not an existing project ID. It is a proposal for versioning the hash method.

**Input object.** The canonical JSON object contains exactly:

```json
{
  "files": [
    {
      "bytes": 0,
      "name": "ref_airlines.csv",
      "sha256": "<64 UPPERCASE HEX CHARACTERS>"
    },
    {
      "bytes": 0,
      "name": "ref_airline_sources.csv",
      "sha256": "<64 UPPERCASE HEX CHARACTERS>"
    }
  ],
  "reference_version": "AIR-YYYY-MM-DD-NNN"
}
```

The placeholders above are illustrative only. They are not real hashes, byte sizes, or reference data.

**Canonicalization rules (proposed):**

1. Encode as UTF-8 without a byte-order mark.
2. Use LF line endings only; do not include a trailing newline.
3. Sort JSON object keys lexicographically by Unicode code point.
4. Use `,` and `:` as separators with no insignificant whitespace.
5. Keep the `files` array in the fixed order `ref_airlines.csv`, then `ref_airline_sources.csv`.
6. Within each file object, use the sorted key order `bytes`, `name`, `sha256`.
7. Emit strings with deterministic JSON escaping; use literal UTF-8 for non-ASCII characters and standard JSON escapes for control characters.
8. Emit `bytes` as a base-10 integer with no leading zeros.
9. Emit `sha256` as uppercase hexadecimal.
10. Hash the raw CSV file bytes exactly as stored; do not normalize line endings or content for the per-file hash.
11. Define `ManifestHash = SHA-256(canonical JSON bytes)`, emitted as uppercase hexadecimal.
12. Exclude the manifest row itself, `ManifestHash`, `Status`, `ApprovedBy`, `ApprovalDate`, `IsCurrent`, `SupersedesReferenceVersion`, and notes.
13. A renamed file, additional file, or changed canonicalization rule requires a new reference version and a new method version.
14. Publish a fixed test vector with two tiny input files and the expected canonical JSON and hash before implementation. The test vector is a method test, not reference data.

**T-78 rule.** T-78 must recompute the hash from the stored files and compare it with the manifest. A mismatch fails closed and blocks generation and refresh. `G3-RV-01` must record the method identifier and the resulting hash.

### 6.6 Technical and governance consequences

- **FACT.** A deterministic hash is required for T-78 and `G3-RV-01` reproducibility.
- **FACT.** An ambiguous method cannot be independently recomputed; two implementations could produce different hashes from the same files.
- **RECOMMENDATION.** Version the method (`MH-1`) and publish a test vector before any manifest is created. Do not let the method change silently.
- **RECOMMENDATION.** Keep approval metadata out of the hash to avoid circularity and unstable hashes.
- **RECOMMENDATION.** Do not create a real manifest or reference CSV while deciding this method.

### 6.7 Impact on OD-01A and OD-01B

| Record | Impact |
|---|---|
| OD-01A | No direct signature block. The population record depends on reference approval, which depends on the manifest hash method. |
| OD-01B | Direct impact on Section 7 and the reference-version/manifest rules. The decision record already treats the manifest as authoritative; the hash method makes that authority reproducible. |
| Both | The decision does not itself approve any reference version or manifest. |

### 6.8 Impact on G3 and G4

- **FACT.** `GOV-D-07` blocks `G3-RV-01`.
- **FACT.** It does not necessarily block the OD-01A/OD-01B signatures, but reference approval cannot be completed without it.
- **FACT.** G3 remains `NOT STARTED`; G4 remains `BLOCKED`.

### 6.9 Required documentation changes

1. **Update** contract §3.4 reference-manifest paragraph and the `ManifestHash` definition with the approved method.
2. **Update** OD-01B Section 7 to reference the method and method version.
3. **Update** the design specification §8.2 or equivalent manifest section to remove “proposed” language and include the exact canonicalization rules.
4. **Update** T-78 to require the method identifier, test vector, and recomputation.
5. **Update** `G3-RV-01` criteria to record the method and resulting hash.
6. **Publish** the test vector before implementation.
7. **Record** the owner decision and method version in the decision register and evidence register.

### 6.10 Dependencies and required evidence

| Dependency / evidence | Status |
|---|---|
| Owner approval of method | `PENDING` |
| Exact canonicalization specification | Proposed in §6.5; not approved |
| Method version `MH-1` | `PROPOSAL` only |
| Test vector | `NOT CREATED` |
| Reference manifest | `NOT CREATED` |
| T-78 execution | `PLANNED` |
| `G3-RV-01` | `NOT EXECUTED` |

### 6.11 Recommendation and justification

**RECOMMENDATION.** Approve **Option A**, a fully specified canonical-JSON method with method identifier `MH-1` and a published test vector.

**Justification.** The canonical-JSON approach is the only option that naturally includes the `reference_version` and both file identities in one reproducible digest while excluding circular approval metadata. The current proposal is directionally correct but under-specified. Adding exact key order, separators, escaping, newline behavior, method versioning, and a test vector makes independent recomputation possible. Hashing raw CSV concatenation or per-file hashes alone would be simpler but weaker for version-level authority.

**What this recommendation is not.** It is not an approval of any manifest, reference version, or hash value. No real hash is created here.

### 6.12 Exact owner approval required

```text
GOV-D-07 — ManifestHash canonicalization

[ ] APPROVE Option A — canonical JSON method MH-1 as specified in §6.5
[ ] APPROVE an alternative method: ________________________________
[ ] DEFER
[ ] REJECT

Method identifier approved: _____________________________________
Test vector required before implementation: [ ] YES [ ] NO
Conditions: ____________________________________________________
________________________________________________________________

Owner initials: __________   Actual date: __________________
```

**FACT.** No field above is completed in this worksheet.

---

## 7. `GOV-D-08` — Evidence-retention policy

### 7.1 Original decision definition

> **FACT.** The packet asks: “Do you approve the proposed read-only evidence structure under `docs/approvals/`, `docs/approvals/evidence/`, and `docs/approvals/hash_register/`, including signed-copy hash verification and retention?”
>
> Source: `docs/OD01_OWNER_DECISION_PACKET.md` lines 144–157.

**EXISTING DESIGN.** The packet recommends approving the structure and read-only procedure. Alternatives are a single-folder retention model, an external records repository, or deferral until signature.

### 7.2 Why the decision exists

- **FACT.** No `docs/approvals/` structure exists. No signed copy exists. No hash register or verification log exists.
- **FACT.** The compensating-control proposal §9 proposes the directory structure, read-only retention procedure, and hash-verification procedure (lines 599–646).
- **FACT.** The proposal leaves the retention period to be “defined by the owner” and does not name a records custodian. Those are genuine owner choices, not documentation details.
- **FACT.** Without a retention rule, a signed copy could be altered or lost, and the approval could not be reconstructed.
- **FACT.** The OD-01A and OD-01B approval blocks currently say `Retention confirmed: No — D-08 PENDING` and leave the signed-copy path and hash blank.

### 7.3 Current status

| Field | Status |
|---|---|
| Owner decision | `PENDING OWNER APPROVAL` |
| `docs/approvals/` | `NOT FOUND` |
| Signed copy | `NOT FOUND` |
| Hash register | `NOT FOUND` |
| Verification log | `NOT FOUND` |
| Retention period | `NOT DEFINED` |
| Records custodian | `NOT NAMED` |
| Governance blocker | `GOV-B-08` remains `PENDING — D-08` |

### 7.4 Available options

| Option | Description | Advantages | Disadvantages | Consequence |
|---|---|---|---|---|
| **A — Proposed read-only structure** | **PROPOSAL.** Use `docs/approvals/OD01A/`, `OD01B/`, `evidence/`, and `hash_register/`; store signed copies read-only; record hashes; verify before and after signature; use a hash register and verification log. | Structured; auditable; separates decision records, evidence, and hashes; supports reconstruction. | Requires a new directory structure and disciplined operation; requires a named custodian and retention period. | **RECOMMENDATION:** adopt Option A with an explicit retention period and custodian. |
| **B — Single-folder retention** | **PROPOSAL.** Put signed copies and hashes in one folder. | Simpler; fewer directories. | Weaker separation; easier to mix evidence and signed records; less scalable. | Acceptable only for a very small project; not recommended. |
| **C — External records repository** | **PROPOSAL.** Store signed copies in an external controlled repository. | Strong separation and access control; may be better for long-term retention. | Adds an external dependency; may be unavailable; needs a reference and hash record in the project. | Acceptable if the owner has a real repository and records the path/hash. |
| **D — Defer until signature** | **PROPOSAL.** Decide retention after signing. | Defers a non-design decision. | The approval block cannot complete its signed-copy path, hash, or retention fields; the signed copy may be created without a retention rule. | Not recommended. |

### 7.5 Proposed structure and procedure (for owner decision)

**PROPOSAL — structure:**

```text
docs/approvals/
  OD01A/
    approval_record.md
    signed_copy.pdf
    evidence_index.md
    sha256.txt
  OD01B/
    approval_record.md
    signed_copy.pdf
    evidence_index.md
    sha256.txt
  evidence/
    scope/
    audit/
    reaudit/
    reviewer/
    source-verification/
  hash_register/
    decision_hash_register.csv
    verification_log.csv
```

**PROPOSAL — read-only procedure:**

1. Sign the decision record once; do not edit the signed copy.
2. Produce a read-only copy in the appropriate `docs/approvals/OD01A` or `OD01B` folder.
3. Record the path, byte size, SHA-256, record version, signer, and signature date in `decision_hash_register.csv`.
4. Restrict write access to the owner or designated records custodian; set the signed copy read-only.
5. Corrections after signature require a new version and a new signed copy; never overwrite the prior signed copy.
6. Retain the signed copy, evidence index, and hash register for the owner-defined retention period.
7. Do not use Git for the signed copy until explicitly authorized.

**PROPOSAL — hash verification:**

- Recompute each stored artifact with `Get-FileHash -Algorithm SHA256`.
- Compare to the register and the value recorded in the approval block.
- Record the verification date, operator, path, expected hash, actual hash, and result in `verification_log.csv`.
- A mismatch stops use of the artifact; quarantine it and investigate before any further approval action.
- Verification is an integrity check, not independent assurance.

### 7.6 Technical and governance consequences

- **FACT.** D-08 is a signature-retention condition, not a design decision. It does not reopen the eight owner-confirmed choices.
- **FACT.** The decision does not assign an independent reviewer. `OD01B-B-08` (independent reviewer) is a separate evidence item and is not resolved by `GOV-D-08`.
- **RECOMMENDATION.** Name a records custodian and set an explicit retention period. “Defined by the owner” is not a completed policy.
- **RECOMMENDATION.** Use a durable signed-copy format and hash the exact signed artifact. If a PDF is used, record the PDF hash; if a signed Markdown file is used, record that file’s hash. Do not hash a reconstructed copy.
- **RECOMMENDATION.** Keep the signed copy out of Git until the owner separately authorizes it.

### 7.7 Impact on OD-01A and OD-01B

| Record | Impact |
|---|---|
| OD-01A | The approval block’s signed-copy path, signed-copy SHA-256, retention confirmation, and verification fields cannot be completed until D-08 is decided and the structure exists. |
| OD-01B | Same fields; same dependency. D-08 does not resolve the reviewer item `OD01B-B-08`. |
| Both | The decision enables a clean signed-copy retention process after signature; it does not itself sign either record. |

### 7.8 Impact on G3 and G4

- **FACT.** `GOV-D-08` does not directly block `G3-RV-01` and does not directly block G3.
- **FACT.** It is a signature-retention condition. Without it, the approval record cannot be reconstructed cleanly.
- **FACT.** G4 remains blocked by G3 and written G4 authorization.

### 7.9 Required documentation changes

1. **Create** the `docs/approvals/` structure only after owner approval and separate authorization.
2. **Update** OD-01A and OD-01B approval blocks to reference the approved structure, custodian, and retention period.
3. **Create** `decision_hash_register.csv` and `verification_log.csv` when the structure is authorized.
4. **Record** the signed-copy path and actual hash only after a signed copy exists.
5. **Record** the retention period and custodian in the decision register and evidence register.
6. **Do not** create a signed copy or hash before signature.

### 7.10 Dependencies and required evidence

| Dependency / evidence | Status |
|---|---|
| Owner approval of structure and procedure | `PENDING` |
| Named records custodian | `NOT NAMED` |
| Explicit retention period | `NOT DEFINED` |
| `docs/approvals/` structure | `NOT FOUND` |
| Signed copies | `NOT FOUND` |
| Hash register and verification log | `NOT FOUND` |
| Actual signed-copy hashes | `NOT FOUND` — cannot exist before signature |

### 7.11 Recommendation and justification

**RECOMMENDATION.** Approve **Option A**, the proposed read-only structure and procedure, with two required additions: a named records custodian and an explicit retention period.

**Justification.** The proposed structure separates decision records, evidence, and hashes, which makes the approval reconstructable. The main weakness is not the directory layout; it is the undefined retention period and custodian. Adding those makes the policy operational. A single-folder model is weaker; an external repository is acceptable only if the owner actually has one and records its path and hash.

**What this recommendation is not.** It is not an approval of a signed copy, a reviewer, or a gate. It does not create the directory structure.

### 7.12 Exact owner approval required

```text
GOV-D-08 — Evidence-retention policy

[ ] APPROVE Option A — proposed read-only structure and procedure
[ ] APPROVE Option A with modifications: ______________________
[ ] APPROVE Option B — single-folder retention
[ ] APPROVE Option C — external records repository
[ ] DEFER
[ ] REJECT

Records custodian: _____________________________________________
Retention period: _____________________________________________
Signed-copy format: ___________________________________________
Conditions: ____________________________________________________
________________________________________________________________

Owner initials: __________   Actual date: __________________
```

**FACT.** No field above is completed in this worksheet.

---

## 8. Consolidated recommendation table

| Item | Recommendation | Label | Why | Owner action | Blocks |
|---|---|---|---|---|---|
| `GOV-D-04` | Approve a separate controlled addendum, preserving the original, with corrected v0.2 text and current hashes | **RECOMMENDATION** | Reconciles the v1.4/“not prepared” contradiction without rewriting history | Approve Option A; sign addendum with actual date | Clean signature evidence chain |
| `GOV-D-05` | Keep all `BusinessModelClass` values null; optional nullable analytical column; no population | **RECOMMENDATION** | No approved rubric or mapping exists; null avoids false precision | Approve Option A; require condition in OD-01B | Populated column / schema freeze only if populated |
| `GOV-D-06` | Approve 365/180-day policy with explicit attribute matrix and 90-day exception rules | **RECOMMENDATION** | Gives `G3-RV-01` a deterministic eligibility rule and resolves `HomeCountry` ambiguity | Approve Option A as clarified | `G3-RV-01`; indirectly G3 |
| `GOV-D-07` | Approve canonical-JSON method `MH-1` with exact serialization and test vector | **RECOMMENDATION** | Makes T-78 and `G3-RV-01` independently reproducible | Approve Option A as clarified | `G3-RV-01`; indirectly G3 |
| `GOV-D-08` | Approve read-only evidence structure with named custodian and explicit retention period | **RECOMMENDATION** | Makes signed-copy retention and approval reconstruction possible | Approve Option A with custodian/retention | Signed-copy retention |
| Key-map route (`KM-01`, worksheet-local) | Approve the key-map **rule** in OD-01B; approve the specific allocation with the first reference manifest through `G3-RV-01` | **RECOMMENDATION** | Resolves the contract §7.1 vs OD-01B §3/§11.3 circularity without freezing an administrative map prematurely | Decide route in Section 10 | OD-01B signature scope |
| Namespace convention (`NS-01`, worksheet-local) | Adopt `GOV-D-xx`, `GOV-B-xx`, `OD01B-B-xx`, `CON-OD-xx`, `DES-D-xx`, `RA-C-xx` in new/current documents; do not rewrite history | **RECOMMENDATION** | Removes ambiguous bare identifiers and the B-05/B-08 precondition defect | Approve namespace adoption | M-07/B-04 clean closure |
| `CC-01` owner self-review | Execute a dated checklist with owner initials, questions, and dispositions | **RECOMMENDATION** | Required compensating-control evidence; owner self-review is not independent review | Execute and attach | M-07; signature readiness |
| `CC-09` no-reviewer limitation | Sign the owner acceptance of the no-independent-review limitation | **RECOMMENDATION** | Makes the D-02 route explicit; avoids implying independent assurance | Sign and date | M-07/B-04; signature readiness |
| H-05 correction | Propagate the six-status G3 vocabulary, consolidate gate criteria, correct the ledger test summary | **RECOMMENDATION** | Removes contradictory G3 reporting and overstatement | Authorize documentation correction | H-05 closure |
| M-12 correction | Align approval scope, resolve key-map trigger, exclude/approve OD-01A Section 3 allocation, state D-05 condition | **RECOMMENDATION** | Makes the signature scope unambiguous | Authorize correction and decide key-map route | M-12 closure; OD-01B signature |

**FACT.** Every row labelled **RECOMMENDATION** is advice, not an approval. No row is completed.

---

## 9. Dependency map

### 9.1 Critical path

```text
Owner reviews worksheet + re-audit
        |
        v
Owner records GOV-D-04, GOV-D-05, GOV-D-08
(and may record GOV-D-06/GOV-D-07 now)
        |
        v
Owner authorizes ONE controlled documentation-correction package
        |
        +--> namespace correction (GOV/OD01B/CON/DES/RA)
        +--> H-05 propagation, ledger test counts, consolidated G3 criteria
        +--> M-12 scope wording and key-map route
        +--> B-04 compensating-control fields and evidence references
        +--> stale residual rows
        +--> D-05 conditional statement
        |
        v
Execute CC-01 owner self-review + CC-09 limitation acceptance
+ residual-risk acceptance
        |
        v
Fresh re-audit of corrected package
        |
        v
Sign OD-01A (actual date and evidence)
        |
        v
Sign OD-01B (actual date and evidence)
        |
        v
Retain signed copies read-only with hashes (after D-08 implementation)
        |
        v
Decide GOV-D-06 and GOV-D-07 (if not already decided)
        |
        v
Prepare G3-RV-01 and reference evidence (separate authorization)
        |
        v
G3 gate review
        |
        v
G4 written authorization
```

### 9.2 Dependency table

| Prerequisite | Enables | Evidence needed | Current status |
|---|---|---|---|
| Owner accepts worksheet/re-audit | Authorization of correction package | Owner response with actual date | `PENDING` |
| `GOV-D-04` | Clean owner-confirmation evidence chain | Addendum with current hashes; original preserved | `PENDING` |
| `GOV-D-05` | OD-01B signature condition; no population | Owner choice; approval condition | `PENDING` |
| `GOV-D-08` | Signed-copy retention structure | Custodian, retention period, directory, hash register | `PENDING` |
| Namespace correction | Clean B-05/B-08/D-04/D-08 mapping | Qualified IDs in preconditions and evidence | `PENDING` |
| Key-map route | Unambiguous OD-01B approval scope | Contract/OD-01B alignment; owner decision | `PENDING` |
| `CC-01` self-review | Signature readiness | Dated checklist, initials, questions/dispositions | `NOT EXECUTED` |
| `CC-09` limitation acceptance | Signature readiness | Signed owner limitation | `NOT EXECUTED` |
| Residual-risk acceptance | Signature readiness | Owner acceptance/rejection | `PENDING` |
| OD-01A signature | OD-01B signature sequence | Actual signature/date/evidence | `NOT SIGNED` |
| OD-01B signature | Reference work preparation | Actual signature/date/evidence | `NOT SIGNED` |
| `GOV-D-06` | `G3-RV-01` source eligibility | Approved thresholds/exception policy | `PENDING` |
| `GOV-D-07` | `G3-RV-01` manifest reproducibility | Approved method/test vector | `PENDING` |
| Reference data + manifest + T-75/T-76/T-78 | `G3-RV-01` | Actual source evidence, CSV, manifest, test results | `NOT CREATED` / `PLANNED` |
| `G3-RV-01` | G3 gate review | Approved reference version | `NOT EXECUTED` |
| G3 APPROVED + written G4 authorization | G4 data generation | Gate record + written authorization | `NOT STARTED` / `BLOCKED` |

### 9.3 What can run in parallel

- **RECOMMENDATION.** The owner can decide `GOV-D-06` and `GOV-D-07` in the same response round as `GOV-D-04`, `GOV-D-05`, and `GOV-D-08`; this shortens the later path to `G3-RV-01`.
- **RECOMMENDATION.** Once authorized, the namespace/H-05/M-12/B-04 documentation corrections can be drafted together as one package.
- **RECOMMENDATION.** Source-verification planning can be prepared, but source retrieval and reference-data creation must wait for explicit authorization and the applicable decisions.
- **FACT.** G3/G4 work cannot run in parallel with the governance corrections because the gates are blocked.

### 9.4 What must not be parallelized

- **FACT.** Do not sign OD-01B before OD-01A; the documented sequence is OD-01A first, then OD-01B.
- **FACT.** Do not execute `G3-RV-01` before `GOV-D-06` and `GOV-D-07` are decided and the reference evidence exists.
- **FACT.** Do not start G3 before the corrected package is re-audited and the critical decisions are approved.
- **FACT.** Do not start G4 before G3 is approved and written G4 authorization exists.

---

## 10. Additional investigation A — The airline `AirlineKey` mapping approval gap

### 10.1 What the documents say

- **FACT.** Contract §7.1 says: “The airline key map is immutable after OD-01B approval, is stored with or hashed into the approved reference manifest, and is loaded by every clean rebuild. A missing or inconsistent map blocks generation and refresh.” See `docs/03_DATA_CONTRACTS.md` line 1046.
- **FACT.** Contract §3.4 says the map is loaded from a controlled, immutable key map stored with or hashed into the approved reference manifest (line 266).
- **FACT.** OD-01B §3 calls the allocation a “Proposed administrative allocation (this revision does not approve the mapping; it is a design baseline, not a source-verified identity fact)” at lines 135–136.
- **FACT.** OD-01B §2 item 10 says the key map is “controlled and immutable after approval” but does not identify which approval (lines 93–96).
- **FACT.** OD-01B §11.3 says Sections 3 and 7 are acknowledged design baselines, not a schema freeze, and that “The key map in Section 3 remains a proposed administrative allocation, not a source-verified identity fact” (lines 381–390).
- **FACT.** OD-01A §3 includes a “Proposed `AirlineId` (OD-01B allocation)” column (lines 88–99) and says the allocation “is not approved by OD-01A” (lines 108–110).
- **FACT.** OD-01A §7.3 says the approval covers Sections 2, 3, and 4 only (lines 223–226), while Section 3 says the allocation is not approved by OD-01A. The scope therefore includes the section but not the allocation, without an explicit exclusion sentence.
- **FACT.** OD-01B evidence `OD01B-B-04` is the proposed key map, status `RECORDED DESIGN — PENDING FORMAL APPROVAL` (line 333).

### 10.2 The circularity

**FACT.** The contract says the map becomes immutable after OD-01B approval. OD-01B says the map is proposed and excludes Section 3 from approval. A signature cannot both exclude the map and make it immutable. There is no unambiguous approval event for the specific `AirlineId`/`AirlineKey` allocation.

**FACT.** OD-01A also contains the proposed `AirlineId` allocation inside its approval scope, but its Section 3 says the allocation is not approved by OD-01A. That creates a second ambiguity: a reader cannot tell whether the OD-01A signature approves the population only or also the identifier allocation.

### 10.3 Options

| Option | Description | Advantages | Disadvantages | Consequence |
|---|---|---|---|---|
| **1 — Include the map in OD-01B approval** | **PROPOSAL.** Make OD-01B Section 3 part of the approved scope; remove the exclusion; state that the specific allocation is approved on signature and becomes immutable. | Immediate certainty; aligns with contract §7.1 as written; one approval event. | Freezes an administrative map before the reference manifest and source verification; conflicts with the current “proposed” label; may require a new version if the roster or allocation changes. | Acceptable if the owner wants the map fixed now. |
| **2 — Approve the rule in OD-01B; approve the allocation with the first manifest** | **PROPOSAL.** OD-01B approves the key-map **rule** (permanent, controlled, no row-order assignment, loaded by every rebuild). The specific allocation is approved with the first reference manifest through `G3-RV-01`, and the contract’s immutability trigger moves from “after OD-01B approval” to “when the first approved reference manifest containing it is approved.” | Aligns with manifest authority; avoids freezing the map before reference evidence; separates the design rule from the administrative allocation; matches contract §3.4’s “stored with or hashed into the approved reference manifest.” | Requires a contract wording change and careful OD-01B scope language; `G3-RV-01` must explicitly include the map. | **RECOMMENDATION:** adopt this route. |
| **3 — Approve the map in OD-01A** | **PROPOSAL.** Put the allocation in the population approval. | One signature covers the roster and identifiers. | Wrong scope: OD-01A is the population decision; OD-01B is the identity/key model; OD-01A Section 3 already says the allocation is not approved by OD-01A. | Not recommended. |
| **4 — Defer** | **PROPOSAL.** Leave the gap open. | No decision now. | OD-01B cannot be signed cleanly; M-12 remains open; contract and decision record remain contradictory. | Does not resolve the blocker. |

### 10.4 Recommended resolution

**RECOMMENDATION.** Adopt **Option 2**.

**Proposed exact changes (not applied):**

1. **Contract §7.1.** Replace “immutable after OD-01B approval” with: “The key map is immutable when the first approved reference manifest containing it is approved through `G3-RV-01`. OD-01B approves the key-map rule, not the specific administrative allocation.”
2. **Contract §3.4.** Keep the requirement that the map is stored with or hashed into the approved reference manifest; add that the specific allocation is part of the `G3-RV-01` evidence.
3. **OD-01B §2 item 10.** State the trigger explicitly: “The key-map rule is approved by OD-01B; the specific allocation becomes immutable when the first reference manifest containing it is approved through `G3-RV-01`.”
4. **OD-01B §3.** Relabel the allocation as “Proposed administrative allocation — specific values approved with the first reference manifest through `G3-RV-01`; not a source-verified identity fact.”
5. **OD-01B §11.3.** State: “Section 3 is an acknowledged design baseline. This approval approves the key-map rule, not the specific allocation. The specific allocation is approved with the first reference manifest through `G3-RV-01`.”
6. **OD-01A §3.** Add: “The proposed `AirlineId` allocation is an OD-01B design baseline. It is not approved by OD-01A and is not part of the population decision.”
7. **OD-01A §7.3.** Add an explicit exclusion: “The proposed `AirlineId` allocation in Section 3 is excluded from this approval; only the population and population-boundary rules are approved.”
8. **OD-01B evidence `OD01B-B-04`.** After signature, change the status to “Key-map rule approved; specific allocation pending `G3-RV-01`.”
9. **`G3-RV-01` criteria.** Require the exact key map, its hash, and the `AirlineId`/`AirlineKey` pairs as part of the approved reference version.
10. **T-78.** Confirm the map is loaded, no key is reassigned, and the map hash matches the manifest.

### 10.5 Why this is better than including the map in OD-01B

**RECOMMENDATION.** The specific allocation is administrative, not source-verified identity. Approving it with the reference manifest keeps it tied to the exact reference version and file hashes, and it avoids freezing a map before the source evidence exists. The design rule — permanent keys, no row-order assignment, no reuse, no re-keying — can be approved in OD-01B now. The specific numbers can be approved with the manifest.

**FACT.** This route requires an owner decision because it changes the approval scope and the contract’s immutability trigger. It is not a documentation-only correction.

### 10.6 Exact owner decision required

```text
Key-map approval route (worksheet item A; worksheet-local ID KM-01)

[ ] Option 1 — Include the specific map in OD-01B approval
[ ] Option 2 — Approve the key-map rule in OD-01B; approve the specific
               allocation with the first reference manifest via G3-RV-01
[ ] Option 3 — Approve the specific map in OD-01A
[ ] DEFER

Conditions: ____________________________________________________
________________________________________________________________

Owner initials: __________   Actual date: __________________
```

**FACT.** No field above is completed in this worksheet.

---

## 11. Additional investigation B — A consistent identifier namespace without rewriting history

### 11.1 The collisions

#### 11.1.1 `D-xx`

**FACT.** The governance packet uses `D-01`–`D-10` for owner decisions. The remediation design specification uses `D-01`–`D-18` for local technical design decisions. The contract uses `OD-01`–`OD-22`, but those are often shortened to `OD-04`, not bare `D-04`. The collision is real when bare `D-04` is used without a document context.

| Bare ID | Governance packet (`GOV-D-xx`) | Contract decision (`CON-OD-xx`) | Design specification (`DES-D-xx`) |
|---|---|---|---|
| `D-01` | Compensating-control approach | OD-01 — real airline population and identity/reference model (parent) | Separate durable identity, warehouse key, and mutable codes |
| `D-02` | No-independent-review limitation | OD-02 — airport and network population | Type 1 `DimAirline`; immutable snapshots; Type 2 deferred |
| `D-03` | Revision 0.2 authorization | OD-03 — fleet composition | `AirlineName` = commercial brand; optional `LegalName` |
| `D-04` | Historical owner-confirmation addendum | OD-04 — synthetic exchange-rate policy | Home-country semantics |
| `D-05` | `BusinessModelClass` baseline | OD-05 — cancelled-flight capacity treatment | Airline-group boundary |
| `D-06` | Source-staleness thresholds | OD-06 — passenger-revenue definition | Operating-region treatment |
| `D-07` | `ManifestHash` canonicalization | OD-07 — tax and fee treatment | Business-model classification |
| `D-08` | Evidence-retention policy | OD-08 — refund, cancellation-fee, no-show, and chargeback treatment | Lifecycle model |
| `D-09` | H-04 risk-register entries | OD-09 — OTP threshold and basis | Provenance architecture |
| `D-10` | H-05 G3 status wording | OD-10 — aircraft-utilization availability | Evidence durability |
| `D-11` | Future signature action (not open) | OD-11 — satisfaction score scale | Reference-version format |
| `D-12` | Future `G3-RV-01`/reference work authorization (not open) | OD-12 — complaint-rate denominator | T-78 reference-version integrity test |
| `D-13`–`D-18` | No governance entries | OD-13–OD-18 | Design decisions D-13–D-18 |

**FACT.** The design specification itself says its `D-01`–`D-18` identifiers are used only in that document and are not OD-series owner decisions (line 121). The governance packet does not carry a similar namespace warning.

#### 11.1.2 `B-xx`

| Bare ID | OD-01B evidence item (`OD01B-B-xx`) | Governance blocker (`GOV-B-xx`) |
|---|---|---|
| `B-03` | Independent audit findings H-01–H-07 and related actions | Stale scope evidence |
| `B-04` | Proposed key map | Approval-record structure |
| `B-05` | Reference manifest — `NOT CREATED` | Historical owner-confirmation addendum — `OPEN — D-04 PENDING` |
| `B-06` | T-78 plan and results — `NOT EXECUTED` | `BusinessModelClass` population mechanism — `PENDING — D-05` |
| `B-07` | `G3-RV-01` reference-version approval — `NOT EXECUTED` | Source staleness and `ManifestHash` — `PENDING — D-06 and D-07` |
| `B-08` | Independent reviewer — `NOT ASSIGNED` | Evidence-retention policy — `OPEN — D-08 PENDING` |

**FACT.** OD-01A line 197 and OD-01B line 352 say “B-05 is resolved by D-04, and B-08 is resolved by D-08.” In the governance namespace, this means `GOV-B-05` is resolved by `GOV-D-04` and `GOV-B-08` by `GOV-D-08`. In OD-01B’s own namespace, `OD01B-B-05` is the reference manifest and `OD01B-B-08` is the independent reviewer. The statement is therefore false under OD-01B’s own namespace.

#### 11.1.3 `C-xx`

**FACT.** Contract §2 uses `C-01`–`C-14` for fixed project constraints. The fresh re-audit uses `C-01`–`C-10` for contradictions. A bare `C-04` can mean “reporting end 2026-09-30” or “historical decision packet versus current authorization.”

### 11.2 Proposed namespace convention

| Namespace | Meaning | Example | Source |
|---|---|---|---|
| `GOV-D-xx` | Governance owner decisions | `GOV-D-04` | Owner decision packet |
| `GOV-B-xx` | Governance evidence/blocker items | `GOV-B-05` | Closure and compensating-control proposals |
| `OD01B-B-xx` | OD-01B-specific evidence items | `OD01B-B-05` | OD-01B Section 10 |
| `CON-OD-xx` | Contract technical decisions | `CON-OD-04` | Contract Section 14 |
| `DES-D-xx` | Local design decisions in the remediation specification | `DES-D-04` | Remediation design specification Section 3 |
| `RA-C-xx` | Fresh re-audit contradictions | `RA-C-01` | Fresh re-audit Section 5 |
| `AUD-H-xx` | Original audit HIGH findings | `AUD-H-04` | Independent governance audit report |
| `AUD-M-xx` | Original audit MEDIUM findings | `AUD-M-07` | Independent governance audit report |
| `CC-xx` | Compensating controls | `CC-01` | Compensating-control proposal |
| `R-xx` | Project risks | `R-09` | Project risk register |
| `T-xx` | Validation tests | `T-78` | Contract Section 13 |

### 11.3 Rules for adoption

1. **FACT.** Preserve all historical records unchanged. Do not rewrite dated audit reports, proposals, change records, or the original owner confirmation merely to add prefixes.
2. **RECOMMENDATION.** Use qualified identifiers on first mention and in every table, precondition, approval block, evidence register, and re-audit finding.
3. **RECOMMENDATION.** Do not use bare `B-05`, `B-08`, `D-04`, or `D-08` in approval or precondition text. Write `GOV-B-05`, `OD01B-B-05`, `GOV-D-04`, etc.
4. **RECOMMENDATION.** Add a namespace legend to OD-01A and OD-01B, or to a single controlled namespace register referenced by both.
5. **RECOMMENDATION.** Keep an alias table: `GOV-D-04 = packet D-04`; `GOV-B-05 = closure proposal B-05`; `OD01B-B-05 = OD-01B evidence B-05`.
6. **RECOMMENDATION.** When citing a document, include both the document and the local ID, e.g., `docs/OD01B... §10 OD01B-B-05`.
7. **RECOMMENDATION.** If a new identifier family is introduced, define it in the namespace register before use.
8. **RECOMMENDATION.** Do not silently rename an existing ID; add an alias and a migration note.

### 11.4 Proposed corrections to the precondition-8 defect

**PROPOSED TEXT (not applied):**

> 8. `GOV-B-05` (historical owner-confirmation addendum) is resolved by `GOV-D-04`; `GOV-B-08` (evidence-retention policy) is resolved by `GOV-D-08`. `OD01B-B-05` (reference manifest) and `OD01B-B-08` (independent reviewer) are separate evidence items and are not resolved by `GOV-D-04` or `GOV-D-08`.

**FACT.** This text resolves the ambiguity without changing the underlying decisions. It should be applied to both OD-01A and OD-01B under a controlled change.

### 11.5 Recommendation

**RECOMMENDATION.** Adopt the qualified namespace convention in new and current documents, preserve historical records, and add a namespace register. Use `GOV-D-xx`, `GOV-B-xx`, `OD01B-B-xx`, `CON-OD-xx`, `DES-D-xx`, and `RA-C-xx` as the standard forms.

**Justification.** The current bare identifiers are readable only with document context. The collision affects precondition 8, the residual-concerns rows, the change record, and any future approval citation. Qualified IDs remove the ambiguity without rewriting history. The convention is also extensible.

---

## 12. Additional investigation C — Owner self-review versus independent review

### 12.1 Definitions

| Dimension | Owner self-review (`CC-01`) | Independent review (`CC-02`) | AI-assisted review |
|---|---|---|---|
| Who performs it | Project owner | Named human reviewer who did not prepare the records | AI coding agent / preparer |
| Independence | Not independent; the owner is the approver and requested the preparation | Independent of preparation, with a recorded independence statement | Not independent |
| What it examines | Decision scope, evidence, conditions, residual limitations, approval readiness | Assumptions, evidence, closure claims, approval scope, from a separate perspective | Document integrity, hashes, cross-document consistency, test-row counts |
| Evidence produced | Dated checklist, owner initials, questions, unresolved items and dispositions | Reviewer name, role, organization, independence statement, checklist, findings, `CONCUR` / `CONCUR WITH RESERVATIONS` / `DISSENT`, signature/date | Hash table, consistency matrix, test counts, limitations |
| Assurance provided | No independent assurance; it is a self-review control | Independent assurance, if genuinely independent | No independent assurance; integrity evidence only |
| Current status | `NOT EXECUTED` | `NOT EXECUTED`; no reviewer assigned | `EXECUTED — document-level` / `PARTIALLY EXECUTED` |

### 12.2 What the documents currently say

- **FACT.** The owner accepted the compensating-control route under `GOV-D-01` and the no-independent-review limitation under `GOV-D-02` (decision packet Part A).
- **FACT.** `CC-01` owner self-review is `NOT EXECUTED`; there is no dated checklist, no owner initials, and no record of unresolved questions or dispositions (fresh re-audit lines 261–266).
- **FACT.** `CC-02` independent challenge is `NOT EXECUTED`; no named reviewer exists (fresh re-audit line 262).
- **FACT.** `CC-09` reviewer limitation is drafted but not owner-accepted (fresh re-audit line 266).
- **FACT.** OD-01A and OD-01B say owner self-review is not independent review and that no independent assurance is claimed (OD-01A lines 203–219; OD-01B lines 359–375).
- **FACT.** The approval blocks still leave reviewer identity, reviewer signature/date, and compensating-control acceptance incomplete (OD-01A lines 240–254; OD-01B lines 404–418).

### 12.3 What each review can and cannot close

- **FACT.** Owner self-review cannot close M-07 by itself. It is one required control in the compensating-control route.
- **FACT.** AI-assisted re-audit cannot be described as independent review. It is document-integrity and consistency evidence.
- **FACT.** Independent review can provide independent assurance, but it is not currently assigned.
- **RECOMMENDATION.** The signature package should include: (a) a completed `CC-01` checklist with owner initials and actual date; (b) a signed `CC-09` limitation acceptance; (c) an explicit residual-risk acceptance or rejection; (d) a reference to the compensating-control evidence in the approval block; and (e) either a named independent reviewer under `CC-02` or a signed statement that no independent reviewer was used.
- **RECOMMENDATION.** Do not label owner self-review or AI-assisted review as independent assurance in any document, dashboard, or conversation.

### 12.4 Evidence needed to close the review controls

| Evidence | Purpose | Current status |
|---|---|---|
| Dated `CC-01` checklist | Prove owner reviewed scope, evidence, conditions, and limitations | `NOT FOUND` |
| Owner initials on each checked item | Prove the review was performed by the owner | `NOT FOUND` |
| Record of questions and dispositions | Show unresolved items were addressed or conditioned | `NOT FOUND` |
| Signed `CC-09` limitation acceptance | Record that no independent reviewer was used | `NOT FOUND` |
| Residual-risk acceptance/rejection | Record the owner’s decision on remaining risk | `NOT FOUND` |
| Named reviewer package (if `CC-02`) | Provide independent assurance | `NOT FOUND` |
| Approval-block reference to the above | Tie the signature to the controls | `NOT FOUND` |

### 12.5 Recommendation

**RECOMMENDATION.** Execute `CC-01` and sign `CC-09` before signing OD-01A/OD-01B. Treat independent review as a recommended future improvement unless the owner chooses to assign a reviewer. Do not claim independent assurance either way.

**Justification.** The owner has already accepted the compensating-control route. The missing element is evidence that the route was actually executed. A signed limitation without a self-review is weak; a self-review without a signed limitation leaves the independence question ambiguous. Both are needed for a clean signature package.

---

## 13. Additional investigation D — What must be corrected in H-05 and M-12

### 13.1 H-05 — G3 status contradiction

#### 13.1.1 Current status

**FACT.** H-05 is `PARTIALLY CLOSED`. The progress ledger now distinguishes gate execution, design documentation, formal approval, schema freeze, `G3-RV-01`, and G4 (ledger lines 12–17). The split vocabulary is not fully propagated, and the ledger’s test-status summary is wrong.

#### 13.1.2 Defects and corrections

| Defect | Current evidence | Required correction | Type |
|---|---|---|---|
| Split vocabulary not propagated | Contract §16.1 line 1907 says “G3 remains NOT STARTED”; AC-20 line 1867 uses a single G3 status; OD-01A/OD-01B status notices use “G3 remains NOT STARTED”; owner confirmation uses the old label | Use the six-status vocabulary in contract, decision records, owner confirmation/addendum, and ledger | Documentation |
| Ledger test summary wrong | Ledger line 13 says “T-01 to T-78 are PLANNED”; contract has eight `BLOCKED` tests: T-37, T-42–T-46, T-55, T-79; 71 `PLANNED`; 0 `PASS` | Correct the summary to 71 `PLANNED`, 8 `BLOCKED`, 0 `PASS`; list the blocked IDs | Documentation |
| Gate criteria not consolidated | Contract AC-16–AC-24 and ledger blocker list are separate | Create one explicit G3 gate-criteria record/table covering entry, evidence, exit, and blockers | Documentation |
| Residual rows stale | OD-01A lines 217–219 and OD-01B lines 373–375 list H-04/H-05/M-07/M-12/B-03/B-04/B-05/B-08 as open without current statuses | Update to the re-audit statuses, with qualified IDs | Documentation |
| Packet D-10 still says `PENDING` | Owner packet Part C line 204; revision change record says D-10 authorized | Mark the packet entry superseded by the change record, or add a dated addendum; do not rewrite the historical packet | Documentation |
| G3 gate execution vs design | Ledger correctly says `NOT STARTED` / `PREPARED — DRAFT`; other documents may still conflate | State explicitly: design documentation is not gate execution, approval, or schema freeze | Documentation |

#### 13.1.3 Acceptance criteria for H-05 closure

- **RECOMMENDATION.** Every current document uses the same six statuses: gate execution `NOT STARTED`; design documentation `PREPARED — DRAFT`; formal approval `NOT FORMALLY APPROVED`; schema freeze `NOT AUTHORIZED`; `G3-RV-01` `NOT EXECUTED`; G4 `BLOCKED`.
- **FACT.** The ledger test summary must match the contract: 71 `PLANNED`, 8 `BLOCKED`, 0 `PASS`.
- **RECOMMENDATION.** One consolidated G3 criteria record exists and is referenced by the contract and ledger.
- **RECOMMENDATION.** Residual rows reflect the current finding statuses.
- **FACT.** H-05 remains `PARTIALLY CLOSED` until these corrections are re-audited.

#### 13.1.4 Owner action vs documentation

**FACT.** The G3 wording was already authorized under `GOV-D-10`; the remaining work is documentation correction and re-audit, not a new business decision. The owner must accept the corrected wording and the re-audit result.

### 13.2 M-12 — Approval scope versus schema freeze

#### 13.2.1 Current status

**FACT.** M-12 is `PARTIALLY CLOSED`. OD-01B now names Sections 2, 4, 5, 6, and 8 as the approval scope and explicitly excludes schema freeze and implementation. The approving sentence still claims reference-version, manifest, and immutable-mapping rules that sit principally in Section 7, which is excluded. The key-map trigger remains circular.

#### 13.2.2 Defects and corrections

| Defect | Current evidence | Required correction | Type |
|---|---|---|---|
| Approval sentence claims Section 7 mechanics | OD-01B §11.3 lines 379–384 claims reference-version, manifest, and immutable-mapping rules; Section 7 is excluded as an acknowledged baseline | Either include Section 7 in the approved scope or remove the claimed mechanics from the approval sentence; state exactly what is approved vs acknowledged | Documentation / owner scope decision |
| Key-map trigger conflict | Contract §7.1 line 1046 says immutable after OD-01B approval; OD-01B §3 lines 135–136 and §11.3 lines 389–390 exclude the map | Adopt the key-map route in Section 10; align contract and OD-01B | Owner decision + documentation |
| OD-01A Section 3 allocation ambiguity | OD-01A §7.3 includes Section 3; §3 lines 108–110 say the allocation is not approved by OD-01A | Add an explicit exclusion for the `AirlineId` allocation, or approve it; recommend exclusion | Documentation / owner scope decision |
| D-05 pending while Section 4 in scope | OD-01B §11.1 precondition 9 and §4; approval block lacks a no-population condition | State in the approval block: no `BusinessModelClass` values approved; nullable design only | Documentation |
| Contract v1.5 draft may be read as approved | Contract status line 1879 is draft; OD-01B cites it as governing baseline | State that OD-01B does not approve the contract; it uses it as a baseline | Documentation |
| Sections 3 and 7 unclear | OD-01B §11.3 calls them acknowledged design baselines, but the approving sentence claims some of their mechanics | State “acknowledged, not approved, not frozen” consistently | Documentation |
| Residual rows stale | Same as H-05 | Update residual statuses with qualified IDs | Documentation |

#### 13.2.3 Acceptance criteria for M-12 closure

- **RECOMMENDATION.** A reader can tell exactly which sections are approved, which are acknowledged, and which are excluded.
- **RECOMMENDATION.** The key map has one unambiguous approval trigger.
- **RECOMMENDATION.** OD-01A’s approval scope does not imply approval of the proposed `AirlineId` allocation.
- **RECOMMENDATION.** OD-01B’s approval block states the D-05 no-population condition.
- **RECOMMENDATION.** The contract’s draft status is explicitly distinguished from the decision-record approval.
- **FACT.** M-12 remains `PARTIALLY CLOSED` until these corrections are re-audited.

#### 13.2.4 Owner action vs documentation

- **FACT.** The key-map route and the OD-01A Section 3 scope choice are genuine owner decisions because they change what the signature approves.
- **FACT.** The wording, cross-references, residual rows, and D-05 condition are documentation corrections once the owner decides the scope.
- **RECOMMENDATION.** Do not sign OD-01B until the scope sentence and key-map trigger are aligned.

---

## 14. Additional investigation E — Evidence needed to close B-04 and B-08

### 14.1 Namespace clarification

**FACT.** “B-04” and “B-08” each have two meanings. This section covers both so that closure is not claimed under the wrong namespace.

| Item | Meaning | What closes it |
|---|---|---|
| `GOV-B-04` | Governance approval-record structure | Completed approval blocks, owner initials/date, evidence references, corrected mappings, re-audit record |
| `OD01B-B-04` | Proposed key map | Key-map approval route, exact allocation/hash, manifest/`G3-RV-01` evidence |
| `GOV-B-08` | Governance evidence-retention policy | D-08 approval, structure, signed copies, hash register, verification log, custodian/retention |
| `OD01B-B-08` | Independent reviewer | Named reviewer package or signed no-reviewer limitation; not D-08 |

### 14.2 `GOV-B-04` — Approval-record structure

| Evidence required | Required content | Current status | Type |
|---|---|---|---|
| Owner initials/date for compensating-control acceptance | The approval block must record the owner’s acceptance of D-01/D-02 and the date | `NOT FOUND` | Owner action |
| `CC-01` self-review evidence | Dated checklist, initials, questions, dispositions | `NOT FOUND` | Owner action |
| `CC-09` limitation acceptance | Signed owner statement that no independent reviewer was used | `NOT FOUND` | Owner action |
| Residual-risk acceptance | Owner acceptance/rejection of remaining risks | `NOT FOUND` | Owner action |
| Corrected precondition 8 | Qualified `GOV-B-05`/`GOV-B-08` mapping; separate `OD01B-B-05`/`OD01B-B-08` | `NOT FOUND` | Documentation |
| Updated residual-concerns row | Current per-finding statuses with qualified IDs | `NOT FOUND` | Documentation |
| Re-audit record field | Reference to the final re-audit after corrections | `BLANK — PENDING` | Documentation + re-audit |
| Signed-copy path/hash | Actual path and hash after signature | `BLANK — D-08 PENDING` | Owner action + external artifact |
| Decision, signature, date, conditions | Actual owner decision and date | `BLANK` | Owner action |
| Compensating-control evidence reference | Explicit reference to `CC-01`, `CC-09`, and residual-risk acceptance | `NOT FOUND` | Documentation |

**Closure criterion.** `GOV-B-04` is closed only when the approval block is complete, the evidence references are real, the mappings are qualified, and the re-audit confirms it. A blank field is not a pass.

### 14.3 `OD01B-B-04` — Proposed key map

| Evidence required | Required content | Current status | Type |
|---|---|---|---|
| Owner-approved key-map route | Section 10 decision | `PENDING` | Owner action |
| Exact `AirlineId`/`AirlineKey` allocation | The ten pairs, with no duplicates or reuse | Proposed in OD-01B §3; not approved | Design + owner approval |
| Map storage/hash | Stored with or hashed into the approved manifest | `NOT CREATED` | External artifact |
| `G3-RV-01` inclusion | Map is part of the reference-version approval | `NOT EXECUTED` | External evidence |
| T-78 key checks | No key reassignment; ten unique keys; map loaded | `PLANNED` | External evidence |
| Evidence status update | `OD01B-B-04` status reflects the chosen route | `RECORDED DESIGN — PENDING FORMAL APPROVAL` | Documentation |

**Closure criterion.** `OD01B-B-04` is closed only when the specific allocation is approved through the chosen route and the map is part of the approved reference manifest. `GOV-D-04` does not close it.

### 14.4 `GOV-B-08` — Evidence-retention policy

| Evidence required | Required content | Current status | Type |
|---|---|---|---|
| D-08 owner approval | Structure, custodian, retention period | `PENDING` | Owner action |
| `docs/approvals/` structure | OD01A/OD01B/evidence/hash_register directories | `NOT FOUND` | Documentation/implementation |
| Signed copies | Read-only signed OD-01A/OD-01B copies | `NOT FOUND` | External artifact |
| `decision_hash_register.csv` | Path, bytes, SHA-256, version, signer, signature date | `NOT FOUND` | External artifact |
| `verification_log.csv` | Date, operator, path, expected/actual hash, result | `NOT FOUND` | External artifact |
| Custodian and retention period | Named custodian; explicit period | `NOT DEFINED` | Owner action |
| Read-only controls | Write access restricted; copy set read-only | `NOT FOUND` | Implementation |
| Verification before/after signature | Hash matches; mismatch blocks approval | `NOT FOUND` | External evidence |

**Closure criterion.** `GOV-B-08` is closed only when the policy is approved, the structure exists, the signed copies and hashes exist, and the verification log records a match. D-08 alone does not create the artifacts.

### 14.5 `OD01B-B-08` — Independent reviewer

| Evidence required | Required content | Current status | Type |
|---|---|---|---|
| Named reviewer | Name, role, organization | `NOT FOUND` | External |
| Independence statement | Independent / not independent; basis | `NOT FOUND` | External |
| Challenge checklist | Scope, challenges, responses, unresolved items | `NOT FOUND` | External |
| Reviewer result | `CONCUR`, `CONCUR WITH RESERVATIONS`, or `DISSENT` | `NOT FOUND` | External |
| Reviewer signature/date | Actual signature and date | `NOT FOUND` | External |
| Alternative: signed no-reviewer limitation | Owner acceptance of D-02 and CC-09 | `NOT FOUND` | Owner action |
| Approval-block reviewer fields | Route, limitation, name/role, independence, result, signature | Partially present; blank | Documentation + owner action |

**Closure criterion.** `OD01B-B-08` is closed either by a genuine independent reviewer package or by a signed owner acceptance of the no-reviewer limitation. `GOV-D-08` (retention) does not close it. No reviewer identity may be invented.

### 14.6 Consolidated evidence matrix

| Evidence | Closes | Owner action? | Documentation? | External? | Current status |
|---|---|---|---|---|---|
| D-04 addendum with current hashes | `GOV-B-05` | Yes | Yes | No | `NOT FOUND` |
| D-05 null baseline condition | `GOV-B-06` | Yes | Yes | No | `NOT FOUND` |
| D-06 approved thresholds | `GOV-B-07` (staleness) | Yes | Yes | No | `NOT FOUND` |
| D-07 approved hash method + test vector | `GOV-B-07` (hash) | Yes | Yes | Test vector | `NOT FOUND` |
| D-08 retention structure | `GOV-B-08` | Yes | Yes | Signed copies/hashes | `NOT FOUND` |
| CC-01 checklist | M-07 / `GOV-B-04` | Yes | Yes | No | `NOT FOUND` |
| CC-09 limitation acceptance | M-07 / `GOV-B-04` | Yes | Yes | No | `NOT FOUND` |
| Residual-risk acceptance | M-07 / `GOV-B-04` | Yes | Yes | No | `NOT FOUND` |
| Key-map route + allocation | `OD01B-B-04` | Yes | Yes | Map hash | `PENDING` |
| Independent reviewer or signed limitation | `OD01B-B-08` | Yes | Yes | Reviewer | `NOT FOUND` |
| Reference CSV + manifest | `OD01B-B-05` | No | No | Yes | `NOT CREATED` |
| T-78 results | `OD01B-B-06` | No | No | Yes | `PLANNED` |
| `G3-RV-01` | `OD01B-B-07` | Yes | No | Yes | `NOT EXECUTED` |

---

## 15. Additional investigation F — Documentation vs owner action vs external evidence

### 15.1 Can be corrected by controlled documentation (after authorization)

- **RECOMMENDATION.** Namespace legend and qualified IDs; precondition-8 correction; residual-row updates.
- **RECOMMENDATION.** H-05 status propagation; ledger test-count correction; consolidated G3 criteria.
- **RECOMMENDATION.** M-12 scope wording; D-05 conditional statement; explicit contract-draft disclaimer.
- **RECOMMENDATION.** B-04 fields and compensating-control evidence references, once the underlying evidence exists.
- **RECOMMENDATION.** Drafting the D-04 addendum, the D-05 condition, the D-06/D-07 contract text, and the D-08 retention policy text after the owner decides.
- **FACT.** Documentation corrections cannot substitute for an owner signature, actual evidence, or a test result.

### 15.2 Requires genuine owner action

**FACT.** The following items cannot be completed by documentation alone and require genuine owner action:

- Choosing `GOV-D-04` through `GOV-D-08`.
- Choosing the key-map approval route.
- Executing `CC-01` owner self-review with initials and date.
- Signing `CC-09` no-reviewer limitation acceptance.
- Accepting or rejecting residual risks.
- Signing OD-01A and OD-01B with actual dates and evidence.
- Naming the records custodian and retention period.
- Authorizing the controlled documentation-correction package.
- Authorizing creation of `docs/approvals/` after D-08.
- Accepting, rejecting, or returning the re-audit and this worksheet.

### 15.3 Requires external evidence or execution

**FACT.** The following items require external evidence or execution:

- Real source-verification records: URLs, retrieval dates, verification dates, evidence hashes or archive references.
- Reference CSVs and the reference manifest.
- T-75/T-76/T-78 execution results.
- `G3-RV-01` artifact.
- Independent reviewer package, if the owner chooses that route.
- Signed copies and hash register.
- G3 gate review record.
- Written G4 authorization.

### 15.4 Cannot be resolved by editing text

**FACT.** The following cannot be resolved by editing text:

- An actual owner signature and date.
- An actual independent review.
- An actual source verification.
- An actual test pass.
- An actual reference manifest hash.
- An actual G3 approval or G4 authorization.

### 15.5 What remains blocked

| Item | Why it remains blocked |
|---|---|
| OD-01A signature | D-04/D-05/D-08 decisions, H-05/M-12/B-04 corrections, CC-01/CC-09 evidence, re-audit, key-map scope |
| OD-01B signature | Same as OD-01A plus key-map trigger, Section 7 scope, D-05 condition, `OD01B-B-05`/`OD01B-B-08` evidence |
| `G3-RV-01` | D-06/D-07, reference data, manifest, T-75/T-76/T-78, owner approval |
| G3 | `G3-RV-01`, critical decisions, schema freeze, gate review |
| G4 | G3 approval plus written G4 authorization |

---

## 16. Recommended sequence and stop conditions

### 16.1 Recommended sequence

1. **Owner review.** Read this worksheet, the investigation report, and the fresh re-audit. Record `ACCEPT FOR DECISION`, `RETURN FOR REVISION`, or `REJECT`.
2. **Owner decisions.** Record `GOV-D-04`, `GOV-D-05`, and `GOV-D-08`; record `GOV-D-06` and `GOV-D-07` now if possible.
3. **Key-map route.** Choose Option 1 or Option 2 in Section 10.
4. **Namespace adoption.** Approve the qualified identifier convention in Section 11.
5. **Correction authorization.** Authorize one controlled documentation-correction package covering namespaces, H-05, M-12, B-04 fields, residual rows, and the D-05 condition.
6. **Owner self-review.** Execute `CC-01` with a dated checklist and initials; sign `CC-09`; accept or reject residual risks.
7. **Re-audit.** Re-audit the corrected package and record final finding statuses.
8. **Sign OD-01A.** Use an actual date and actual evidence references.
9. **Sign OD-01B.** Use an actual date and actual evidence references; state the D-05 condition and key-map scope.
10. **Retain signed copies.** After D-08 implementation, store read-only copies with hashes and verification log entries.
11. **Prepare `G3-RV-01`.** After D-06/D-07 and the reference evidence, prepare the reference version, manifest, T-75/T-76/T-78, and owner approval.
12. **G3 gate.** Hold the gate review only when the criteria are met.
13. **G4.** Authorize data generation only after G3 approval and written G4 authorization.

### 16.2 Stop conditions

- **FACT.** Do not sign OD-01A or OD-01B until the corrections, self-review, and re-audit are complete.
- **FACT.** Do not create reference CSVs, synthetic data, code, Power Query, DAX, or Power BI while the gates are blocked.
- **FACT.** Do not execute `G3-RV-01` before D-06/D-07 and the reference evidence.
- **FACT.** Do not mark G3 `APPROVED` or G4 `AUTHORIZED` without the required records.
- **FACT.** Do not invent a signature, date, hash, reviewer, source, or test result.
- **FACT.** Do not claim independent assurance from AI-assisted or owner self-review.
- **FACT.** Do not freeze the schema or perform a Git write without separate authorization.

### 16.3 Boundary recommendation

**RECOMMENDATION.** Keep the governance correction to one controlled package and one re-audit. After that, the owner should either sign or return the package. Do not let governance work expand indefinitely; the project needs a firm boundary before reference data and implementation. If a new material defect is found during the correction, record it explicitly and decide whether it blocks signature or can be handled as a residual risk.

**Justification.** The investigation already identified the material blockers. A second open-ended governance cycle would delay the project without adding proportional assurance. One package, one re-audit, and a clear sign/return decision is the safest way to move from governance to implementation.

---

## 17. Owner response template

**INSTRUCTIONS.** Complete this template only after reading the worksheet. Use actual dates. Do not sign OD-01A or OD-01B in this template; those are separate decision records with their own signature blocks. Return the completed template to the project record.

```text
AEROVISION 360 — OWNER RESPONSE TO DECISION WORKSHEET

Owner: KH Mohammad Farhan
Response date: ______________________  (actual date; do not prefill)
Worksheet reviewed (path/hash): __________________________________
Re-audit reviewed (path/hash): ___________________________________

Overall response:
[ ] ACCEPT FOR DECISION
[ ] RETURN FOR REVISION
[ ] REJECT

GOV-D-04 — Historical owner-confirmation addendum
[ ] APPROVE Option A — separate controlled addendum
[ ] APPROVE Option B — dated reliance note
[ ] DEFER
[ ] REJECT
Addendum version/hash: __________________________________________
Conditions: _____________________________________________________
________________________________________________________________

GOV-D-05 — BusinessModelClass baseline
[ ] Option A — NULL baseline; optional nullable column; no values populated
[ ] Option B — MAPPING; documented analytical rubric and mapping
[ ] DEFER
If B: rubric/mapping document: ___________________________________
       mapping owner: ____________________________________________
       allowed values/version: ___________________________________
       review cadence: ___________________________________________
Conditions: _____________________________________________________
________________________________________________________________

GOV-D-06 — Source-staleness thresholds and exceptions
[ ] APPROVE proposed 365/180-day policy with the §5.5 attribute matrix
[ ] APPROVE modified thresholds: _________________________________
[ ] APPROVE no exceptions
[ ] DEFER
[ ] REJECT
Attribute groups/ages: __________________________________________
Exception maximum (days): _______________________________________
Anchor date: ____________________________________________________
Conditions: _____________________________________________________
________________________________________________________________

GOV-D-07 — ManifestHash canonicalization
[ ] APPROVE Option A — canonical JSON method MH-1 as specified in §6.5
[ ] APPROVE alternative method: __________________________________
[ ] DEFER
[ ] REJECT
Method identifier: _____________________________________________
Test vector required before implementation: [ ] YES [ ] NO
Conditions: _____________________________________________________
________________________________________________________________

GOV-D-08 — Evidence-retention policy
[ ] APPROVE Option A — proposed read-only structure and procedure
[ ] APPROVE Option A with modifications: _________________________
[ ] APPROVE Option B — single-folder retention
[ ] APPROVE Option C — external records repository
[ ] DEFER
[ ] REJECT
Records custodian: ______________________________________________
Retention period: ______________________________________________
Signed-copy format: ____________________________________________
Conditions: _____________________________________________________
________________________________________________________________

Additional item A — Key-map approval route (KM-01, worksheet-local)
[ ] Option 1 — Include the specific map in OD-01B approval
[ ] Option 2 — Approve the key-map rule in OD-01B; specific allocation
               approved with the first reference manifest via G3-RV-01
[ ] Option 3 — Approve the specific map in OD-01A
[ ] DEFER
Conditions: _____________________________________________________
________________________________________________________________

Additional item B — Namespace convention (NS-01, worksheet-local)
[ ] ADOPT qualified identifiers: GOV-D-xx, GOV-B-xx, OD01B-B-xx,
    CON-OD-xx, DES-D-xx, RA-C-xx
[ ] REJECT
[ ] DEFER

Compensating controls:
CC-01 owner self-review:
[ ] WILL EXECUTE
[ ] COMPLETED — checklist attached
[ ] DEFER
CC-09 no-reviewer limitation:
[ ] ACCEPT
[ ] REJECT
Residual risks:
[ ] ACCEPT
[ ] REJECT
[ ] ACCEPT WITH CONDITIONS: ______________________________________

Authorizations:
[ ] AUTHORIZE preparation of one controlled documentation-correction package
[ ] DO NOT AUTHORIZE
[ ] AUTHORIZE creation of docs/approvals/ structure after D-08
[ ] DO NOT AUTHORIZE

Owner signature: _______________________________________________
Actual date: ___________________________________________________
Notes / conditions / reservations: _______________________________
________________________________________________________________
________________________________________________________________
```

**FACT.** No field above is completed in this worksheet.

---

## 18. Appendices

### Appendix A — Source and hash register

**FACT.** Hashes below were recomputed on 2026-11-03 with PowerShell `Get-FileHash -Algorithm SHA256`. They identify the current files used for this worksheet.

| Document | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `docs/AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md` | 95,042 | `E7522AC81069129DE14D6B0B42F759DC978D5C00DA452BFEE293EBCFD99B9D8F` | Primary investigation report |
| `docs/OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md` | 48,669 | `9706080798D7AA39940DB8696B40968F7C3E8B4682FC11F272DB498335D4BE28` | Latest non-independent re-audit |
| `docs/OD01_OWNER_DECISION_PACKET.md` | 13,673 | `16B09AB99235401B5848EE537EFD7CFE9381E3903B169E176207A840FCCF71B1` | Original D-01–D-10 definitions |
| `docs/OD01_GOVERNANCE_CLOSURE_PROPOSAL.md` | 22,470 | `F71ED26AD698E83C8F63977E55AAEA1B5600433D7F7D19654138AC214B987741` | Governance B-03/B-04/B-05 and Annex A |
| `docs/OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` | 57,809 | `C07C412C69ADB6DCDF72DA8517A142DC6E4FD12C26CB83960EF0FAA8E586BA98` | Governance B-03–B-08 and CC-01–CC-10 |
| `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` | 119,064 | `CC3BCE621142C31B4BB7A46F4CBCB320E640466228184AE2E94E196796F3F8A4` | Local DES-D-01–D-18 and design detail |
| `docs/OD01A_AIRLINE_POPULATION_DECISION.md` | 17,311 | `2140081A100DFAA0BB87ACC7B9DC429A49D99CE638C09905BBD5A221C12146D9` | OD-01A v0.2 |
| `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | 27,795 | `15AE19A42C537F56EFDD1E55CEF15EC73D6472AE520B1AC41EB815118852D7EB` | OD-01B v0.2 |
| `docs/03_DATA_CONTRACTS.md` | 211,846 | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` | Contract v1.5 |
| `docs/OD01_OWNER_DECISION_CONFIRMATION.md` | 28,055 | `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD` | Historical owner confirmation |
| `docs/OD01_REVISION_0.2_CHANGE_RECORD.md` | 11,868 | `1B91069C8043A7E5877F3EEB540ACC57766A677DA17BD902A7C49527FA344ECB` | D-03/D-09/D-10 authorization |
| `docs/PROGRESS_LEDGER.md` | 5,230 | `980080FD30F3D45E09EA473CB42EAE0CCA610EF40E77860AFF3FEEE766380BB4` | G3/G4 status ledger |

### Appendix B — Namespace alias register

| Qualified ID | Alias in historical documents | Meaning |
|---|---|---|
| `GOV-D-01` | `D-01` in owner packet | Compensating-control approach |
| `GOV-D-02` | `D-02` in owner packet | No-independent-review limitation |
| `GOV-D-03` | `D-03` in owner packet | Revision 0.2 authorization |
| `GOV-D-04` | `D-04` in owner packet | Historical owner-confirmation addendum |
| `GOV-D-05` | `D-05` in owner packet | `BusinessModelClass` baseline |
| `GOV-D-06` | `D-06` in owner packet | Source-staleness thresholds |
| `GOV-D-07` | `D-07` in owner packet | `ManifestHash` canonicalization |
| `GOV-D-08` | `D-08` in owner packet | Evidence-retention policy |
| `GOV-D-09` | `D-09` in owner packet | H-04 risk-register entries |
| `GOV-D-10` | `D-10` in owner packet | H-05 G3 status wording |
| `GOV-B-03` | `B-03` in governance proposal | Stale scope evidence |
| `GOV-B-04` | `B-04` in governance proposal | Approval-record structure |
| `GOV-B-05` | `B-05` in governance proposal | Historical owner-confirmation addendum |
| `GOV-B-06` | `B-06` in compensating proposal | `BusinessModelClass` population mechanism |
| `GOV-B-07` | `B-07` in compensating proposal | Source staleness and `ManifestHash` |
| `GOV-B-08` | `B-08` in compensating proposal | Evidence-retention policy |
| `OD01B-B-03` | `B-03` in OD-01B | Audit findings H-01–H-07 |
| `OD01B-B-04` | `B-04` in OD-01B | Proposed key map |
| `OD01B-B-05` | `B-05` in OD-01B | Reference manifest |
| `OD01B-B-06` | `B-06` in OD-01B | T-78 plan and results |
| `OD01B-B-07` | `B-07` in OD-01B | `G3-RV-01` reference-version approval |
| `OD01B-B-08` | `B-08` in OD-01B | Independent reviewer |
| `CON-OD-04`–`CON-OD-08` | `OD-04`–`OD-08` in contract | Contract technical decisions; not governance D-04–D-08 |
| `DES-D-04`–`DES-D-08` | `D-04`–`D-08` in design specification | Local design decisions; not governance D-04–D-08 |
| `RA-C-01`–`RA-C-10` | `C-01`–`C-10` in fresh re-audit | Re-audit contradictions; not contract constraints C-01–C-14 |

### Appendix C — Decision-to-source traceability

| Decision | Original definition | Supporting proposal/design | Current record references | Re-audit reference |
|---|---|---|---|---|
| `GOV-D-04` | Packet lines 84–97 | Closure proposal §4 and Annex A; compensating proposal §6 | OD-01A §7.1; OD-01B §11.1; owner confirmation lines 20, 82, 299, 357–358 | Re-audit §4.3, §8 |
| `GOV-D-05` | Packet lines 99–112 | Compensating proposal §7; design specification §6.4 | OD-01B §2.6, §4, §11.1; contract §3.4, §4.3, §6.2.2 | Re-audit §4.4, §8 |
| `GOV-D-06` | Packet lines 114–127 | Compensating proposal §8.1; design specification §7.6 | Contract §3.4; OD-01B §7; `G3-RV-01` criteria | Re-audit §8 |
| `GOV-D-07` | Packet lines 129–142 | Compensating proposal §8.2 | Contract §3.4; OD-01B §7; T-78 | Re-audit §8 |
| `GOV-D-08` | Packet lines 144–157 | Compensating proposal §9; design specification §10.5 | OD-01A §7.4; OD-01B §11.4; `docs/approvals/` absent | Re-audit §4.3, §8 |

### Appendix D — Checks not possible in this task

- **FACT.** No reference CSV, manifest, or source-verification record exists, so no source staleness, manifest hash, T-75, T-76, or T-78 check could be executed.
- **FACT.** No signed copy exists, so no signed-copy hash or retention verification could be performed.
- **FACT.** No independent reviewer is assigned, so no independent assurance could be obtained.
- **FACT.** No G3 gate review or G4 authorization exists, so no gate status could be advanced.
- **FACT.** No Power BI model, report, or runtime exists, so no runtime or report validation could be performed.
- **FACT.** No Git commit exists; the repository has no committed baseline. This worksheet did not perform a Git write.
- **FACT.** This worksheet is non-independent AI-assisted work. It is decision support, not assurance.

### Appendix E — Worksheet control

| Field | Entry |
|---|---|
| Document ID | `AEROVISION-360-ODW-2026-11-03` |
| Version | 0.1 |
| Status | `PREPARED — OWNER RESPONSE REQUIRED` |
| Prepared | 2026-11-03 |
| Prepared by | AI coding agent — non-independent preparer |
| Owner / approver | KH Mohammad Farhan |
| Approval | `NOT APPROVED — NO SIGNATURE` |
| Revision history | 0.1 — initial worksheet; no prior version |
| Files modified | None; this worksheet is the only new file |
| Next action | Owner reviews and completes the response template in Section 17 |

---

**End of worksheet.** No decision is approved. No signature is recorded. No date in this worksheet is an approval date.

