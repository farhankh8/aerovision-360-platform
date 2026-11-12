# AEROVISION 360 — OD-01 Owner Decision Packet

**Document ID:** OD01-ODP-2026-11-02  
**Document type:** Owner decision packet — D-01/D-02 recorded; D-03 to D-10 pending  
**Status:** PARTIALLY RECORDED — NO FORMAL OD-01A/OD-01B APPROVAL  
**Prepared:** 2026-11-02  
**Prepared by:** Build AI agent — non-independent preparer  
**Project owner / approver:** KH Mohammad Farhan  
**Related proposal:** `OD01_GOVERNANCE_CLOSURE_PROPOSAL.md`  
**G3:** `NOT STARTED`  
**G4:** `BLOCKED`  
**`G3-RV-01`:** `NOT EXECUTED`

> **Status notice**
>
> D-01 and D-02 are recorded from the owner’s explicit instruction. They are
> not a formal signature, not an approval date, and not approval of OD-01A,
> OD-01B, or any technical decision D-03 through D-10.
>
> No independent reviewer has performed the review. AI-assisted re-audit and
> owner self-review are not independent assurance. No external verification,
> certification, signature, reviewer identity, or formal approval is claimed.

---

## Part A — Recorded owner decisions D-01 and D-02

### A.1 D-01 — Compensating-control approach

| Field | Record |
|---|---|
| Decision ID | `D-01` |
| Decision | Accept the documented compensating-control approach, subject to the limitations in this packet. |
| Status | `ACCEPTED — OWNER INSTRUCTION RECORDED` |
| Scope | Governance review and approval preparation only. This is not approval of any technical decision, decision-record revision, or gate. |
| Recorded | 2026-11-02 — recording date only; not an approval date or signature date. |
| Owner identity | KH Mohammad Farhan, project owner. No signature entered. |

### A.2 D-02 — No-independent-review limitation

| Field | Record |
|---|---|
| Decision ID | `D-02` |
| Decision | Accept the no-independent-review limitation for this governance route. Do not describe AI re-audit or owner self-review as independent review. |
| Status | `ACCEPTED — OWNER INSTRUCTION RECORDED` |
| Scope | Applies to the compensating-control route. It does not waive any mandatory finding closure, re-audit, evidence, or approval-scope requirement. |
| Recorded | 2026-11-02 — recording date only; not an approval date or signature date. |
| Owner identity | KH Mohammad Farhan, project owner. No signature entered. |

### A.3 Recorded limitations

The following limitations are part of D-01 and D-02:

1. No independent reviewer has performed the review.
2. AI-assisted re-audit is not independent assurance.
3. Owner self-review must be documented as owner self-review.
4. Residual risks and review limitations must remain transparent.
5. Future independent review remains recommended.
6. No claim of independent assurance, external verification, or certification is permitted.
7. H-04, H-05, M-07, and M-12 remain open or partially closed until the required controlled changes and re-audit are completed.
8. D-01/D-02 do not approve D-03 through D-10.

---

## Part B — Pending owner decisions D-03 to D-10

Each decision below is a separate choice. Recommendation does not equal approval. The owner decision fields are intentionally blank.

### D-03 — Authorize controlled revision 0.2 of OD-01A and OD-01B

| Field | Detail |
|---|---|
| Exact question | Do you authorize OD-01A and OD-01B revision 0.2 to correct stale scope evidence, add the reviewer/compensating-control statement, add signature-ready fields, add the re-audit precondition, and add revision history? |
| Recommended choice | **APPROVE** the controlled revision, limited to the listed changes. |
| Alternative choices | Approve only B-03 and B-04; defer the reviewer/control language; return for revision. |
| Technical consequences | If approved, signature blockers B-03 and B-04 can be corrected and the records can be re-audited. If not approved, the stale evidence and incomplete approval blocks remain and signature is blocked. |
| Documents affected | `OD01A_AIRLINE_POPULATION_DECISION.md`; `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`. |
| Blocks signature? | **Yes.** |
| Blocks `G3-RV-01`? | Yes, indirectly, because the decision records remain unapproved. |
| Blocks G3? | Yes, indirectly. |
| Owner decision | `[ ] APPROVE  [ ] REJECT  [ ] DEFER` |
| Owner initials/date | ______________________________ |

### D-04 — Historical owner-confirmation addendum

| Field | Detail |
|---|---|
| Exact question | Do you approve a separate controlled addendum to the original owner confirmation stating that the eight choices remain valid, contract v1.5 is current, OD-01A/OD-01B are prepared, historical status statements are superseded, and no approval is implied? |
| Recommended choice | **APPROVE** the addendum; preserve the original record unchanged. |
| Alternative choices | Add a dated reliance note instead of an addendum; defer; reject. |
| Technical consequences | The original record currently says contract v1.4 and “OD-01A/B not prepared.” Without an addendum or explicit reliance note, the evidence chain remains contradictory. |
| Documents affected | Future controlled addendum; original `OD01_OWNER_DECISION_CONFIRMATION.md` remains unchanged. |
| Blocks signature? | Blocks a clean signature evidence chain; not a design decision. |
| Blocks `G3-RV-01`? | No. |
| Blocks G3? | No, but it weakens the decision evidence. |
| Owner decision | `[ ] APPROVE  [ ] REJECT  [ ] DEFER` |
| Owner initials/date | ______________________________ |

### D-05 — `BusinessModelClass` baseline

| Field | Detail |
|---|---|
| Exact question | Should all `BusinessModelClass` values remain null for the baseline, or should a documented analytical mapping/rubric be approved? |
| Recommended choice | **Option A — all values null.** Keep the column optional/nullable in `DimAirline`; do not treat it as source-verified identity. |
| Alternative choices | Option B — approve a documented rubric and mapping; remove the column entirely, which would reopen the owner-confirmed choice. |
| Technical consequences | Null avoids unsupported classifications and unblocked schema freeze. A populated column requires a mapping owner, allowed values, examples, and versioning before schema freeze. |
| Documents affected | OD-01B; future data dictionary/schema-freeze material. |
| Blocks signature? | **No**, if Option A is chosen. |
| Blocks `G3-RV-01`? | No. |
| Blocks G3/schema freeze? | Blocks a populated column; null baseline does not. |
| Owner decision | `[ ] Option A — NULL  [ ] Option B — MAPPING  [ ] DEFER` |
| Owner initials/date | ______________________________ |

### D-06 — Source-staleness thresholds and exceptions

| Field | Detail |
|---|---|
| Exact question | Do you approve the proposed 365-day maximum for airline name, legal name, group, and home country; 180-day maximum for IATA/ICAO codes; and a maximum 90-day written exception, with stale sources quarantined and not loadable? |
| Recommended choice | **APPROVE** the proposed thresholds and exception policy. |
| Alternative choices | Stricter thresholds; no exceptions; different anchor dates; defer. |
| Technical consequences | The thresholds determine whether a source can support a populated identity attribute in an approved reference version. Without a decision, `G3-RV-01` cannot determine staleness. |
| Documents affected | Future provenance/contract/design change; `G3-RV-01` criteria. |
| Blocks signature? | **No.** |
| Blocks `G3-RV-01`? | **Yes.** |
| Blocks G3? | Yes, indirectly. |
| Owner decision | `[ ] APPROVE  [ ] REJECT  [ ] DEFER` |
| Owner initials/date | ______________________________ |

### D-07 — `ManifestHash` canonicalization

| Field | Detail |
|---|---|
| Exact question | Do you approve the deterministic canonical-JSON method for `ManifestHash`, covering `reference_version` and fixed-order `ref_airlines.csv` / `ref_airline_sources.csv` name, byte size, and SHA-256, excluding approval metadata and the hash itself? |
| Recommended choice | **APPROVE** the canonical-JSON method. |
| Alternative choices | Hash a concatenation of raw CSV bytes; use per-file hashes only; defer. |
| Technical consequences | A deterministic method is required for T-78 and `G3-RV-01` reproducibility. An ambiguous method cannot be independently recomputed. |
| Documents affected | Future contract/design change; manifest schema; `G3-RV-01`. |
| Blocks signature? | **No.** |
| Blocks `G3-RV-01`? | **Yes.** |
| Blocks G3? | Yes, indirectly. |
| Owner decision | `[ ] APPROVE  [ ] REJECT  [ ] DEFER` |
| Owner initials/date | ______________________________ |

### D-08 — Evidence-retention policy

| Field | Detail |
|---|---|
| Exact question | Do you approve the proposed read-only evidence structure under `docs/approvals/`, `docs/approvals/evidence/`, and `docs/approvals/hash_register/`, including signed-copy hash verification and retention? |
| Recommended choice | **APPROVE** the structure and read-only procedure. |
| Alternative choices | Single-folder retention; external records repository; defer until signature. |
| Technical consequences | Without a retention rule, a signed copy can be altered or lost; the approval may not be reconstructable. |
| Documents affected | Future `docs/approvals/` structure; decision records; hash register. |
| Blocks signature? | Signature retention condition; not the design decision. |
| Blocks `G3-RV-01`? | No. |
| Blocks G3? | No. |
| Owner decision | `[ ] APPROVE  [ ] REJECT  [ ] DEFER` |
| Owner initials/date | ______________________________ |

### D-09 — H-04 risk-register entries R-09 to R-11

| Field | Detail |
|---|---|
| Exact question | Do you approve adding R-09 (airline lifecycle/cessation), R-10 (reference-version change after refresh), and R-11 (historical reproducibility/consistency) to the project risk register with the proposed controls and owners? |
| Recommended choice | **APPROVE** the entries; revise ratings or owners if desired. |
| Alternative choices | Approve with revised likelihood/impact; defer; reject and require a different control. |
| Technical consequences | H-04 remains partially closed without the register entries. The design controls exist, but the risk register does not show the required scenarios. |
| Documents affected | Future risk register or controlled addendum. |
| Blocks signature? | **Yes**, because H-04 is a HIGH finding. |
| Blocks `G3-RV-01`? | Yes, indirectly, because the decision package is not closed. |
| Blocks G3? | Yes, indirectly. |
| Owner decision | `[ ] APPROVE  [ ] REJECT  [ ] DEFER` |
| Owner initials/date | ______________________________ |

### D-10 — H-05 G3 status wording

| Field | Detail |
|---|---|
| Exact question | Do you approve the split status wording: G3 gate `NOT STARTED — gate not executed`; design documentation `PREPARED — DRAFT`; decision status `NOT FORMALLY APPROVED`; schema freeze `NOT AUTHORIZED`; G4 `BLOCKED`? |
| Recommended choice | **APPROVE** the split wording; do not mark G3 started merely because blueprints exist. |
| Alternative choices | `IN PROGRESS` with approvals pending; single `NOT FORMALLY APPROVED` label; keep `NOT STARTED` unchanged. |
| Technical consequences | The split wording distinguishes design documentation from gate execution, formal approval, and schema freeze. Keeping the current single label leaves H-05 unresolved. |
| Documents affected | `PROGRESS_LEDGER.md`; future governance reporting. |
| Blocks signature? | **Yes**, because H-05 is a HIGH finding. |
| Blocks `G3-RV-01`? | Yes, indirectly. |
| Blocks G3? | No gate advancement; it clarifies status only. |
| Owner decision | `[ ] APPROVE  [ ] REJECT  [ ] DEFER` |
| Owner initials/date | ______________________________ |

---

## Part C — Decision summary

| Decision | Topic | Status |
|---|---|---|
| `D-01` | Compensating-control approach | `ACCEPTED — OWNER INSTRUCTION RECORDED` |
| `D-02` | No-independent-review limitation | `ACCEPTED — OWNER INSTRUCTION RECORDED` |
| `D-03` | OD-01A/OD-01B revision 0.2 | `PENDING` |
| `D-04` | Owner-confirmation addendum | `PENDING` |
| `D-05` | `BusinessModelClass` | `PENDING` |
| `D-06` | Source-staleness thresholds | `PENDING` |
| `D-07` | `ManifestHash` | `PENDING` |
| `D-08` | Evidence retention | `PENDING` |
| `D-09` | H-04 risk-register entries | `PENDING` |
| `D-10` | H-05 G3 wording | `PENDING` |

D-11 (sign OD-01A/OD-01B) and D-12 (authorize `G3-RV-01`/reference work) are future actions and are not open in this packet.

---

## Part D — Owner authorization block

This block is blank. It records no signature, approval date, or decision.

```text
I have reviewed the proposal and decision packet.

D-03: [ ] APPROVE [ ] REJECT [ ] DEFER
D-04: [ ] APPROVE [ ] REJECT [ ] DEFER
D-05: [ ] Option A — NULL [ ] Option B — MAPPING [ ] DEFER
D-06: [ ] APPROVE [ ] REJECT [ ] DEFER
D-07: [ ] APPROVE [ ] REJECT [ ] DEFER
D-08: [ ] APPROVE [ ] REJECT [ ] DEFER
D-09: [ ] APPROVE [ ] REJECT [ ] DEFER
D-10: [ ] APPROVE [ ] REJECT [ ] DEFER

Owner name: __________________________________________________
Owner signature: _____________________________________________
Actual authorization date: ___________________________________
Conditions / reservations: ___________________________________
______________________________________________________________
```

No field above has been completed.

---

## Part E — Stop condition

This packet does not authorize any controlled change. The owner must explicitly approve D-03 through D-10 before any decision record, addendum, risk register, ledger, or retention structure is modified. No signature, reference data, synthetic data, production ETL, Power Query, Power BI, schema freeze, G3/G4 change, or `G3-RV-01` execution is authorized.
