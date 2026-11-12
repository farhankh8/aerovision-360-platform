# AEROVISION 360 — Governance Investigation Report

**Document ID:** A360-GOV-INV-2026-11-02  
**Document type:** Read-only governance investigation report — not an approval, signature, waiver, gate decision, or implementation authorization  
**Status:** FINAL INVESTIGATION REPORT — EVIDENCE RECORDED; OD-01A AND OD-01B NOT READY FOR SIGNATURE  
**Prepared:** 2026-11-02  
**Prepared by:** Build AI agent — non-independent investigator  
**Project owner / approver:** KH Mohammad Farhan  
**Governing scope:** `01_PROJECT_SCOPE.md` version 1.1  
**Governing contract:** `03_DATA_CONTRACTS.md` version 1.5 — draft, pending review and formal approval  
**Decision records:** `OD01A_AIRLINE_POPULATION_DECISION.md` revision 0.2; `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` revision 0.2  
**Latest governance re-audit:** `OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md`  
**G3 gate execution:** `NOT STARTED`  
**G3 design documentation:** `PREPARED — DRAFT`  
**G3 formal approval:** `NOT FORMALLY APPROVED`  
**Schema freeze:** `NOT AUTHORIZED`  
**`G3-RV-01`:** `NOT EXECUTED`  
**G4:** `BLOCKED`

> **Status notice**
>
> This is a non-independent, AI-assisted governance investigation. It is not
> independent assurance, external verification, certification, a signature, or
> an approval. The investigator is not a named human reviewer.
>
> This report records what exists, what is missing, and what the evidence
> supports. It does not approve OD-01A, OD-01B, contract v1.5, any owner
> decision, any risk acceptance, any schema, any reference version, or any gate.
>
> No existing controlling document was modified. No signature, approval date,
> reviewer identity, source-verification result, reference CSV, manifest,
> synthetic dataset, production code, Power Query query, semantic model, DAX
> measure, Power BI file, schema freeze, `G3-RV-01` execution, G3/G4
> advancement, or Git write operation was performed.
>
> The only file created by this investigation is this report.

---

## 1. Executive summary

### 1.1 Bottom line

The governance package has improved materially since the original governance
audit report. That original report is itself a structured self-audit, not
independent assurance. The stale scope hash is corrected, the risk register now
contains the three H-04 scenarios, the progress ledger separates G3 gate
execution from design documentation, and the OD-01A/OD-01B approval blocks are
substantially more complete and honest about the absence of independent review.

Those improvements are not sufficient to sign either decision record.

The package still has:

- five unresolved owner decisions, `D-04` through `D-08`;
- two unresolved identifier collisions, one for `B-xx` and one for `D-xx`;
- an unresolved key-map approval gap between contract §7.1 and OD-01B §11.3;
- a G3 status vocabulary that is correct only in the progress ledger;
- an incorrect ledger test-status summary;
- no executed owner self-review, no named independent reviewer, and no signed
  no-reviewer limitation;
- no `G3-RV-01`, reference manifest, reference CSV, or signed-copy retention
  structure;
- no formal approval of contract v1.5, which both decision records cite as the
  governing baseline.

### 1.2 Status summary

| Area | Status | Basis |
|---|---|---|
| Repository inspection | `VERIFIED — READ-ONLY` | 31 pre-existing current documents plus root files hashed; no implementation artifacts; Git has no commits |
| `H-04` — Risk register omissions | `PARTIALLY VERIFIED — CLOSED AT DOCUMENTATION LEVEL` | R-09–R-11 exist; mitigations remain open and unexecuted |
| `H-05` — G3 status contradiction | `PARTIALLY VERIFIED` | Ledger split exists; contract and decision records still use a single G3 label; ledger test summary is wrong |
| `M-07` — Approval workflow and reference-version criteria | `PARTIALLY VERIFIED` | Compensating-control route documented; owner self-review and reviewer limitation are not executed |
| `M-12` — Approval scope versus schema freeze | `PARTIALLY VERIFIED` | Scope narrowed; key-map approval gap and Section 3 `AirlineId` ambiguity remain |
| `B-03` — Stale scope evidence (governance namespace) | `VERIFIED — CLOSED AT DOCUMENT LEVEL` | Current scope hash present; obsolete hash absent from current OD-01A/OD-01B |
| `B-04` — Approval-record structure (governance namespace) | `PARTIALLY VERIFIED` | Fields exist; owner initials/date and compensating-control evidence reference missing |
| `B-05` — Owner-confirmation addendum (governance namespace) | `PENDING OWNER APPROVAL` | Addendum not created; original confirmation still says contract v1.4 and OD-01A/B not prepared |
| `B-08` — Evidence retention (governance namespace) | `PENDING OWNER APPROVAL` | `docs/approvals/` does not exist |
| `D-04` — Historical owner-confirmation addendum | `PENDING OWNER APPROVAL` | No addendum; proposed Annex A is stale at OD-01A/B v0.1 |
| `D-05` — `BusinessModelClass` baseline | `PENDING OWNER APPROVAL` | Null/optional design exists; no population authorized |
| `D-06` — Source-staleness thresholds | `PENDING OWNER APPROVAL` | Proposed 365/180-day thresholds expressly not owner-approved |
| `D-07` — `ManifestHash` canonicalization | `PENDING OWNER APPROVAL` | Method proposed only; not in contract |
| `D-08` — Evidence-retention policy | `PENDING OWNER APPROVAL` | Retention structure absent |
| OD-01A | `BLOCKED — NOT READY FOR SIGNATURE` | Preconditions unmet; residual rows stale; Section 3 scope ambiguity |
| OD-01B | `BLOCKED — NOT READY FOR SIGNATURE` | Preconditions unmet; key-map gap; B/D namespace ambiguity; D-05 pending |
| G3 gate execution | `NOT STARTED` | No gate review held |
| G3 formal approval | `NOT FORMALLY APPROVED` | OD-01A/OD-01B unsigned; decisions pending |
| G4 | `BLOCKED` | G3 not approved; no written G4 authorization |
| Unauthorized modifications | `NONE DETECTED` | Only this report was created; existing file hashes unchanged |

### 1.3 What is genuinely stronger

The following are verified document-level improvements:

1. **Scope evidence is corrected.** `01_PROJECT_SCOPE.md` is version 1.1 at
   6,384 bytes with SHA-256
   `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C`.
   OD-01A E-07 and OD-01B shared evidence cite that value. The obsolete hash
   `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9`
   is absent from both current decision records.

2. **The H-04 risk scenarios exist.** `PROJECT_RISK_REGISTER.md` contains
   R-09, R-10, and R-11 with causes, consequences, ratings, controls,
   monitoring, ownership, residual risk, and closure evidence. All three are
   explicitly `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED`.

3. **The G3 split exists in the ledger.** `PROGRESS_LEDGER.md` now separates
   gate execution, design documentation, formal approval, schema freeze,
   `G3-RV-01`, and G4.

4. **Approval blocks are structurally honest.** OD-01A and OD-01B contain
   decision, scope, exclusion, signature, date, reviewer, limitation,
   residual-concern, signed-copy, and retention fields. Blanks are clearly
   marked as blanks. No signature, date, or reviewer identity was invented.

5. **The backup is intact.** The revision 0.2 backup manifest and the three
   preserved files match their recorded SHA-256 values.

### 1.4 What still prevents signature

The signature blockers are not primarily defects in the ten-airline roster.
They are governance, record-structure, and approval-scope defects:

1. `D-04` is pending, so the owner-confirmation chain still says contract v1.4
   and “OD-01A/B not prepared.”
2. `D-05` is pending while OD-01B Section 4 is inside the approval scope.
3. `D-06` and `D-07` are pending, so `G3-RV-01` cannot be executed.
4. `D-08` is pending, so no signed-copy retention or hash register exists.
5. The `B-xx` tokens mean different things in OD-01B’s evidence table and in
   the governance proposals. Precondition 8 is correct only in the governance
   namespace.
6. The contract makes the airline key map immutable after OD-01B approval;
   OD-01B excludes the key map from approval.
7. OD-01A Section 3 contains a proposed `AirlineId` allocation while Section 3
   is inside OD-01A’s approval scope.
8. H-05 is only partially closed; the six-status G3 vocabulary is not
   propagated, G3 criteria are not consolidated, and the ledger’s test summary
   is wrong.
9. M-07 is only partially closed; owner self-review, acceptance of the executed
   controls, residual-risk acceptance, and the signed no-reviewer limitation
   are missing.
10. B-04 is only partially closed; the compensating-control owner initials/date
    and evidence reference are missing.
11. The residual-concern rows in both decision records are stale after the
    fresh re-audit.
12. Contract v1.5 is still a draft pending review and formal approval.

---

## 2. Scope, authority, and read-only constraints

### 2.1 Scope

This investigation examined the current AEROVISION 360 repository at:

`C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`

It focused on:

- decision blockers `D-04` through `D-08`;
- findings `H-04`, `H-05`, `M-07`, and `M-12`;
- evidence items `B-03`, `B-04`, `B-05`, and `B-08`;
- the current OD-01A and OD-01B revision 0.2 records;
- the current contract v1.5, progress ledger, risk register, owner decision
  packet, owner confirmation, change records, proposals, and fresh re-audit;
- repository state, artifact presence, document hashes, encoding, line endings,
  local links, headings, and test-status counts.

### 2.2 Authority and limits of this report

This report was prepared under the user’s investigation instruction. It is not
a controlled change record, an owner decision, a signature, an approval, a
waiver, or a gate record.

The governing documents remain:

- `01_PROJECT_SCOPE.md` version 1.1;
- `03_DATA_CONTRACTS.md` version 1.5, draft;
- `OD01A_AIRLINE_POPULATION_DECISION.md` revision 0.2;
- `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` revision 0.2;
- `PROGRESS_LEDGER.md`;
- `PROJECT_RISK_REGISTER.md`;
- the owner decision packet and recorded change records.

Where this report and a governing document differ, the governing document
controls, and the difference must be returned to the owner. This report does
not amend any governing document.

### 2.3 Read-only constraints observed

The investigation did not:

- edit, delete, rename, or overwrite any existing document;
- create a reference CSV, manifest, synthetic dataset, data dictionary, schema
  freeze, Python pipeline, Power Query query, semantic model, DAX measure, or
  Power BI artifact;
- populate `BusinessModelClass`;
- create `docs/approvals/` or any retention artifact;
- execute `G3-RV-01`, G3, or G4;
- record a signature, approval date, reviewer identity, or independent-review
  claim;
- perform a Git write operation.

The only file created is this report.

### 2.4 What this investigation cannot establish

This is a document-level investigation. It cannot establish:

- that the airline identity attributes are factually correct;
- that any source URL, source organization, or verification date is real;
- that the risk controls work in operation;
- that the contract is technically implementable without runtime testing;
- that the decision records express the owner’s current intent beyond what the
  documents say;
- that an independent reviewer has reviewed anything;
- that a signed copy exists or is retained;
- that G3 or G4 has passed.

---

## 3. Method, evidence standard, and limitations

### 3.1 Methods used

- SHA-256 recomputation with PowerShell `Get-FileHash -Algorithm SHA256`.
- Byte-length and last-write-time capture.
- UTF-8 BOM inspection.
- CRLF byte-pair counting.
- Markdown local-link resolution.
- Duplicate-heading detection within each current Markdown document.
- Test-row counting and status counting in contract v1.5.
- Global searches for stale hashes, signatures, approval dates, reviewer
  identities, `G3-RV-01`, `BusinessModelClass`, `ManifestHash`, and G3/G4
  status strings.
- Cross-document comparison of OD-01A, OD-01B, the contract, ledger, risk
  register, owner packet, owner confirmation, proposals, change records, and
  fresh re-audit.
- Directory and artifact inspection across `data/`, `qa/`, `reports/`,
  `scripts/`, `src/`, `tests/`, `config/`, `power_bi/`, `docs/approvals/`,
  and the repository root.
- Git state inspection without writes.

### 3.2 Evidence status vocabulary

| Status | Meaning in this report |
|---|---|
| `VERIFIED` | Directly observed in the current repository, or recomputed from the current file, and consistent with the cited record |
| `DOCUMENTED BUT NOT VERIFIED` | Stated in a document, but no execution, source, signature, or runtime evidence exists |
| `PARTIALLY VERIFIED` | Some required elements are present and observed; at least one required element is missing or contradictory |
| `NOT FOUND` | The required file, field, artifact, or evidence does not exist |
| `PENDING OWNER APPROVAL` | A decision or authorization is required from the project owner and has not been recorded |
| `BLOCKED` | The item cannot proceed until a named dependency is resolved |

These statuses are analytical. They are not approvals, waivers, or gate
decisions.

### 3.3 Limitations

- The investigator is an AI agent and is not independent.
- No named human reviewer was assigned or consulted.
- AI-assisted review is not independent assurance.
- Owner self-review is not independent review and is not recorded as executed.
- No source verification was performed.
- No runtime, data, semantic-model, DAX, or Power BI validation was possible.
- No signed copy, hash register, reference manifest, or `G3-RV-01` artifact
  exists to inspect.
- File integrity does not prove governance quality, data correctness, or
  implementation correctness.
- The fresh re-audit is itself a non-independent AI-assisted document; it is
  not independent assurance.

---

## 4. Repository and document inventory

### 4.1 Repository structure

| Path | State | Relevance |
|---|---|---|
| `docs/` | 55 files directly: 31 pre-existing current documents, this report, and 23 dated backups; plus 4 files in `docs/backups/` | Governing and supporting documentation |
| `data/` | 5 directories, 0 files | No reference, raw, staging, or curated data |
| `qa/` | 2 directories, 0 files | No test results or screenshots |
| `reports/` | 2 directories, 0 files | No rendered reports |
| `scripts/` | 0 files | No scripts |
| `src/` | 4 directories, 0 files | No source code |
| `tests/` | 3 directories, 0 files | No tests |
| `config/` | 0 files | No configuration |
| `power_bi/` | 0 files | No Power BI artifacts |
| `.agents/` | 1 file: `skills/data-contract-rewrite.md` (1,570 bytes) | Tooling metadata; not a governing project record |
| `.freebuff/` | 1 file: `project-id` (37 bytes) | Tooling metadata; not a governing project record |
| `.git/` | Initialized; branch `main`; 0 commits; all project paths untracked | No committed history |
| `README.md` | 907 bytes | Project status and data policy |
| `.gitignore` | 480 bytes | Ignore rules; generated data and `*.bak` excluded |

### 4.2 Current governing and decision documents

The table lists the 31 pre-existing documents. This report is the sole new file
and is not self-listed, because a file cannot contain its own stable hash.

All hashes below are SHA-256, recomputed on 2026-11-02. “Inspection” is the
depth actually used: `FULL` means the entire file was read; `TARGETED` means all
cited sections plus global identifier searches were inspected; `METADATA/HASH`
means the file was hashed and checked for cross-references without a full read.

| Path | Bytes | Modified | SHA-256 | Relevance | Inspection |
|---|---:|---|---|---|---|
| `docs/01_PROJECT_SCOPE.md` | 6,384 | 2026-11-02 20:37:37 | `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` | Governing scope v1.1; roster, period, disclosure | FULL |
| `docs/02_BUSINESS_REQUIREMENTS.md` | 5,921 | 2026-11-01 22:34:18 | `F5B3140A91C868692A37609F904129BD166861045A9D00C9840815B0CCC4E709` | BR-01 disclosure and business requirements | FULL |
| `docs/03_DATA_CONTRACTS.md` | 211,846 | 2026-11-01 22:34:18 | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` | Governing contract v1.5; key rules, tests, status | TARGETED |
| `docs/OD01A_AIRLINE_POPULATION_DECISION.md` | 17,311 | 2026-11-02 21:36:10 | `2140081A100DFAA0BB87ACC7B9DC429A49D99CE638C09905BBD5A221C12146D9` | OD-01A population decision v0.2 | FULL |
| `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | 27,795 | 2026-11-02 21:36:18 | `15AE19A42C537F56EFDD1E55CEF15EC73D6472AE520B1AC41EB815118852D7EB` | OD-01B identity/reference decision v0.2 | FULL |
| `docs/PROGRESS_LEDGER.md` | 5,230 | 2026-11-02 21:34:19 | `980080FD30F3D45E09EA473CB42EAE0CCA610EF40E77860AFF3FEEE766380BB4` | G3/G4 status ledger | FULL |
| `docs/PROJECT_RISK_REGISTER.md` | 10,615 | 2026-11-02 21:33:27 | `23964C2D75E46FDC1715463C018E4F723ED23615F503D7AA9A301A28D47B4993` | R-09–R-11 risk register | FULL |
| `docs/REQUIREMENTS_TRACEABILITY.md` | 5,742 | 2026-11-01 22:34:18 | `4EE19E921BDC3067D17E172422D85D76B2660EF478EF4AB385D816BA4C314DEB` | REQ-028 and T-78 traceability | FULL |
| `docs/OD01_OWNER_DECISION_PACKET.md` | 13,673 | 2026-11-02 21:25:27 | `16B09AB99235401B5848EE537EFD7CFE9381E3903B169E176207A840FCCF71B1` | Original `D-01`–`D-10` definitions | FULL |
| `docs/OD01_OWNER_DECISION_CONFIRMATION.md` | 28,055 | 2026-11-01 22:13:05 | `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD` | Eight owner-confirmed choices; stale v1.4 statements | TARGETED |
| `docs/OD01_OWNER_DECISION_RESOLUTION.md` | 78,760 | 2026-11-01 22:03:47 | `BE62CBDC017073F6D9135D7DEEF3993F64D74D881102A5C867134C889E20A220` | Pre-confirmation decision basis | TARGETED |
| `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` | 63,965 | 2026-11-01 21:17:34 | `FD94BD369D3DDDC1AF84C040C27014F112E74B4B0F938CE95B617C7B142BECE6` | Original H-01–H-07 and M-07/M-12 findings | TARGETED |
| `docs/OD01_GOVERNANCE_CLOSURE_PROPOSAL.md` | 22,470 | 2026-11-02 21:25:01 | `F71ED26AD698E83C8F63977E55AAEA1B5600433D7F7D19654138AC214B987741` | Governance B-03/B-04/B-05 and Annex A | TARGETED |
| `docs/OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` | 57,809 | 2026-11-02 21:18:32 | `C07C412C69ADB6DCDF72DA8517A142DC6E4FD12C26CB83960EF0FAA8E586BA98` | Governance B-03–B-08 and CC-01–CC-10 | TARGETED |
| `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` | 119,064 | 2026-11-01 21:41:04 | `CC3BCE621142C31B4BB7A46F4CBCB320E640466228184AE2E94E196796F3F8A4` | Local technical design `D-01`–`D-18` | TARGETED |
| `docs/OD01_REMEDIATION_CHANGE_RECORD.md` | 20,796 | 2026-11-01 22:38:46 | `B74329743E5FD5343FA8EB0F1A103436C54A63D949526437E902EA03D6869A22` | Contract v1.4 → v1.5 change evidence | TARGETED |
| `docs/OD01_REVISION_0.2_CHANGE_RECORD.md` | 11,868 | 2026-11-02 21:36:47 | `1B91069C8043A7E5877F3EEB540ACC57766A677DA17BD902A7C49527FA344ECB` | D-03/D-09/D-10 revision 0.2 authorization | FULL |
| `docs/OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md` | 48,669 | 2026-11-02 22:21:36 | `9706080798D7AA39940DB8696B40968F7C3E8B4682FC11F272DB498335D4BE28` | Latest non-independent re-audit | FULL |
| `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md` | 26,179 | 2026-11-01 20:53:33 | `C594DFCD8FE1B6809E28CBE1B3EE6D24FAA0772D35DD1FE57767FECCD3CA2A60` | Superseded v1.4 draft; historical evidence | METADATA/HASH |
| `docs/OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt` | 9,891 | 2026-11-01 20:42:16 | `EFA6060BD0D73B48341A238DE460EA0497B3AF2304709489F1B2DF6B15408CA7` | Historical migration evidence; stale hash | METADATA/HASH |
| `docs/OD01_MIGRATION_PREPARATION_REPORT.txt` | 1,979 | 2026-11-01 19:59:48 | `51615AF5366A279925F403A92C2613CE8EC0F5E07953210715ADE6C38365D634` | Historical migration preparation | METADATA/HASH |

### 4.3 Current design and supporting documents

| Path | Bytes | Modified | SHA-256 | Relevance | Inspection |
|---|---:|---|---|---|---|
| `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt` | 20,426 | 2026-11-01 22:34:18 | `000E9613C56039A8A95F667AF571C63D4841FF69EE04B8ACDCDD6B8FE8429122` | Original build prompt and acceptance context | METADATA/HASH |
| `docs/DAX_KPI_CATALOGUE.md` | 40,677 | 2026-11-02 20:43:51 | `89C64584ACD86EF5926053D4157865BB32D995780092F5A66BB8049ECCE33891` | KPI/DAX design; not implemented | METADATA/HASH |
| `docs/ENGINEERING_DATA_MODEL_BLUEPRINT.md` | 43,500 | 2026-11-02 20:48:40 | `8F4745FC7DA63D8E50C505237A93D2DDE0C3296822F13EB7CDE36BF0EE457D93` | Dimensional model design; not approved | METADATA/HASH |
| `docs/IMPLEMENTATION_QA_BLUEPRINT.md` | 24,108 | 2026-11-02 20:45:28 | `37A9A21E2C7254FF8374AE676629F637DD245FE0AE84CD1B5B5A2FB678F3677F` | QA design; not executed | METADATA/HASH |
| `docs/IMPLEMENTATION_ROADMAP.md` | 19,790 | 2026-11-02 20:39:54 | `3C3ECA890E3B75E74B8A844E6B0129951129AAFF1456D7AB812BEEA8C04A6733` | Phase plan; not authorization | METADATA/HASH |
| `docs/POWER_BI_DASHBOARD_SPECIFICATION.md` | 34,263 | 2026-11-02 20:48:40 | `CB4000017B9991DDB40A2C23EF7C80B4D1AA10CA0D6438DBD3D0473F4AA10B12` | Report design; not built | METADATA/HASH |
| `docs/POWER_BI_SEMANTIC_MODEL_BLUEPRINT.md` | 23,627 | 2026-11-02 20:48:40 | `EC1A01DFB872A243E878C9966BEADE548F030240C5505055513325F11385038A` | Semantic model design; not built | METADATA/HASH |
| `docs/POWER_QUERY_IMPLEMENTATION_BLUEPRINT.md` | 19,215 | 2026-11-02 20:48:40 | `D93EBA3EEEDD252B20B05FE13BC6BE791F7F8F8D8D8FCD62950884BD98123793` | Power Query design; not built | METADATA/HASH |
| `docs/PYTHON_ETL_IMPLEMENTATION_BLUEPRINT.md` | 24,046 | 2026-11-02 20:37:31 | `A3C33A9B6207644118862A9B5B95C0EECF0194B308AAD78066DD2556D4B57032` | Python ETL design; not built | METADATA/HASH |
| `docs/SYNTHETIC_DATA_GENERATION_BLUEPRINT.md` | 31,774 | 2026-11-02 20:39:54 | `24C4B3A6111E07491A9DC76F7082CD2C92B76531F9A06774A9585A886A233E9E` | Synthetic-data design; not authorized | METADATA/HASH |

### 4.4 Root files

| Path | Bytes | Modified | SHA-256 | Relevance | Inspection |
|---|---:|---|---|---|---|
| `README.md` | 907 | 2026-10-29 16:55:19 | `465BB2C79E8489702F33A2E4F271A5E891D8EBB7FB4D7A76132EBAC9A4BE33CE` | Project status and data policy | FULL |
| `.gitignore` | 480 | 2026-10-29 16:55:19 | `5D6A49024996F74087BF9010A3ECC211455D091FC0534C5C5F33E692907E5341` | Ignore rules | FULL |

### 4.5 Backup inventory summary

The main inventory above excludes dated backups. Backups are summarized
separately because they are historical evidence, not current governing
documents.

| Backup group | Files | Bytes | Status |
|---|---:|---:|---|
| `docs/03_DATA_CONTRACTS.*.pre_*` and `.bak` | 18 | 3,010,485 | Historical pre-change copies; not current authority |
| `docs/PROGRESS_LEDGER.md.pre_*` | 2 | 2,659 | Historical pre-change copies |
| `docs/REQUIREMENTS_TRACEABILITY.md.pre_*` | 3 | 4,684 | Historical pre-change copies |
| `docs/backups/OD01_revision_0.2_20261102_213045/` | 4 | 37,409 | Revision 0.2 backup plus manifest; hashes verified |

Revision 0.2 backup verification:

| File | SHA-256 | Bytes | Result |
|---|---|---:|---|
| `OD01A_AIRLINE_POPULATION_DECISION.md` | `399241AD2AE21F4A1FB3D7E589950117F9CDADB8303F78CC161F484CD7255A06` | 11,487 | Matches manifest and backup copy |
| `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | `CDD48B9F0B68CE401D827E5F910076104CCCE73FFBF7BA0A6BC21D75D07C3C05` | 20,782 | Matches manifest and backup copy |
| `PROGRESS_LEDGER.md` | `C6297622D8CFE5BD90402BBB034B1091C70BAA2895BF0438F4E94C003E343C1F` | 4,076 | Matches manifest and backup copy |
| `_BACKUP_MANIFEST.txt` | `44C0E2616B3AA5362C4EE86513A50DF307834397A81B41694E4C096511B1CE9C` | 1,064 | Present; hash verified |

The revision 0.2 manifest states that no original file was modified before the
backup was verified. The available backup copies match their recorded hashes.
This is document-level evidence; it does not prove that no earlier backup was
ever overwritten outside the available record.

### 4.6 Artifact and directory check

| Location / artifact | Result |
|---|---|
| `data/04_reference/` | Exists; zero files |
| `data/manifests/` | Exists; zero files |
| `qa/results/` | Exists; zero files |
| `qa/screenshots/` | Exists; zero files |
| `power_bi/` | Exists; zero files |
| `docs/approvals/` | Does not exist |
| Reference CSV | None created |
| Reference manifest | None created |
| Synthetic dataset | None created |
| `.py`, `.pbix`, `.pbip`, `.csv`, `.parquet` production artifacts outside backups | None found |
| Git commit history | Zero commits; branch `main`; all project paths untracked |
| Git write operation by this investigation | None |

### 4.7 Key hash cross-check against the fresh re-audit

| File | Current SHA-256 | Fresh re-audit value | Match |
|---|---|---|---|
| `03_DATA_CONTRACTS.md` | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` | Same | Yes |
| `OD01A_AIRLINE_POPULATION_DECISION.md` | `2140081A100DFAA0BB87ACC7B9DC429A49D99CE638C09905BBD5A221C12146D9` | Same | Yes |
| `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | `15AE19A42C537F56EFDD1E55CEF15EC73D6472AE520B1AC41EB815118852D7EB` | Same | Yes |
| `PROGRESS_LEDGER.md` | `980080FD30F3D45E09EA473CB42EAE0CCA610EF40E77860AFF3FEEE766380BB4` | Same | Yes |
| `PROJECT_RISK_REGISTER.md` | `23964C2D75E46FDC1715463C018E4F723ED23615F503D7AA9A301A28D47B4993` | Same | Yes |
| `OD01_REVISION_0.2_CHANGE_RECORD.md` | `1B91069C8043A7E5877F3EEB540ACC57766A677DA17BD902A7C49527FA344ECB` | Same | Yes |
| `OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md` | `9706080798D7AA39940DB8696B40968F7C3E8B4682FC11F272DB498335D4BE28` | Same | Yes |
| `01_PROJECT_SCOPE.md` | `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C` | Same | Yes |

---

## 5. Governance baseline and decision hierarchy

### 5.1 Current authority chain

| Layer | Document | Current status | What it can and cannot do |
|---|---|---|---|
| Scope | `01_PROJECT_SCOPE.md` v1.1 | Baseline for implementation; formal OD-01A/OD-01B approval pending | Defines project scope, roster, period, disclosure; does not approve decision records or data |
| Requirements | `02_BUSINESS_REQUIREMENTS.md` v1.1 | Baseline for data-contract design; formal approval pending | Defines BR-01–BR-15; not implementation evidence |
| Contract | `03_DATA_CONTRACTS.md` v1.5 | `DRAFT — CONTROLLED OD-01 REMEDIATION COMPLETE; PENDING REVIEW AND FORMAL APPROVAL` | Defines schema and rules; not a schema freeze or formal approval |
| Population decision | `OD01A` v0.2 | `OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING` | Converts owner-confirmed population choice into a decision record; not signed |
| Identity decision | `OD01B` v0.2 | `OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING` | Converts identity/reference choices into a decision record; not signed |
| Status ledger | `PROGRESS_LEDGER.md` | G3 split; G4 blocked | Reports status; does not approve |
| Risk register | `PROJECT_RISK_REGISTER.md` | Active; R-09–R-11 open and unverified | Records risks; does not accept residual risk |
| Owner packet | `OD01_OWNER_DECISION_PACKET.md` | D-01/D-02 recorded; D-03–D-10 pending on its face | Defines decisions; packet is historical and partly superseded by change records |
| Owner confirmation | `OD01_OWNER_DECISION_CONFIRMATION.md` | Eight choices confirmed; not a signature | Records owner-confirmed design choices; contains stale v1.4 statements |
| Revision 0.2 change record | `OD01_REVISION_0.2_CHANGE_RECORD.md` | Implemented; document-level verification; re-audit pending | Records D-03/D-09/D-10 changes; not a signature |

### 5.2 What is formally approved

No OD-01A or OD-01B signature exists. No approval date exists. No reviewer
identity exists. No schema freeze exists. No G3 gate approval exists. No G4
authorization exists. No reference version is approved.

The only recorded owner instructions are:

- `D-01` — compensating-control approach accepted, with limitations;
- `D-02` — no-independent-review limitation accepted, with limitations;
- `D-03`, `D-09`, `D-10` — recorded as owner-authorized in the revision 0.2
  change record, not as signatures.

`D-01` and `D-02` are recorded in the owner decision packet. `D-03`, `D-09`,
and `D-10` are recorded as applied in the revision 0.2 change record. The
owner packet still lists `D-03`, `D-09`, and `D-10` as `PENDING`; the change
record states those entries are superseded. This is a historical-record
inconsistency, not an approval of `D-04`–`D-08`.

### 5.3 What the owner confirmation does and does not do

`OD01_OWNER_DECISION_CONFIRMATION.md` records eight owner-confirmed design
choices. It is not a signature, not a formal approval, not a schema freeze, not
a G3 approval, and not a G4 authorization.

It still states:

- the governing contract is version 1.4 — lines 20, 82, and 299;
- version 1.5 does not exist yet — line 327;
- OD-01A and OD-01B are “not prepared or signed” — lines 357–358;
- G3 remains `NOT STARTED` — line 360.

Those statements are historically true for the confirmation’s date but false as
current statements. `D-04` is intended to resolve this through a separate
controlled addendum. It remains pending.

The revision 0.2 change record does not itself state contract v1.5. The
contract-version link relies on the prior remediation change record and on the
decision records’ own “Governing baseline” lines. This is part of the
authorization-chain defect recorded as C-04.

### 5.4 Contract v1.5 status

Contract v1.5 is the governing technical baseline cited by OD-01A and OD-01B,
but it is not formally approved. Its own status is:

`DRAFT — CONTROLLED OD-01 REMEDIATION COMPLETE; PENDING REVIEW AND FORMAL APPROVAL`

This is a dependency, not a contradiction, provided the decision records do not
claim the contract is approved. They do not. The owner should still not read an
OD-01A/OD-01B signature as contract approval.

---

## 6. Identifier namespaces and provenance of codes

### 6.1 Why this section exists

The same short codes are used for different things in different documents. A
report that silently chooses one meaning would create a false evidence chain.
This section records the collisions and defines the analytical notation used in
this report.

**This report does not rename anything in the source documents.** The prefixed
forms below are analytical labels only.

### 6.2 `D-xx` namespace collision

There are three distinct `D-xx` namespaces:

| Code | Governance packet (`GOV-D-xx`) | Contract open decision (`CON-OD-xx`) | Remediation design specification (`DES-D-xx`) |
|---|---|---|---|
| `D-04` | Historical owner-confirmation addendum | Synthetic exchange-rate policy | Home-country semantics |
| `D-05` | `BusinessModelClass` baseline | Cancelled-flight capacity treatment | Airline-group boundary |
| `D-06` | Source-staleness thresholds and exceptions | Passenger-revenue definition | Operating-region treatment |
| `D-07` | `ManifestHash` canonicalization | Tax and fee treatment | Business-model classification |
| `D-08` | Evidence-retention policy | Refund, cancellation-fee, no-show, and chargeback treatment | Lifecycle model |

Sources:

- Governance packet: `OD01_OWNER_DECISION_PACKET.md` lines 84–157.
- Contract open decisions: `03_DATA_CONTRACTS.md` lines 1758–1762.
- Remediation design local decisions: `OD01_REMEDIATION_DESIGN_SPECIFICATION.md`
  lines 128–132; that document states its identifiers are local to it.

**Notation used in this report:**

- `GOV-D-04` through `GOV-D-08` mean the governance-packet decisions requested
  in this investigation. When this report says `D-04` without a prefix in the
  context of owner decisions, it means `GOV-D-04`.
- `CON-OD-04` through `CON-OD-08` mean the contract’s technical open decisions.
- `DES-D-04` through `DES-D-08` mean the remediation design specification’s
  local technical decisions.

The `D-03`, `D-09`, and `D-10` authorizations in the revision 0.2 change record
are governance-packet decisions, not contract `OD-03`, `OD-09`, or `OD-10`.

### 6.3 `B-xx` namespace collision

There are two distinct `B-xx` namespaces:

| Code | OD-01B evidence item (`OD01B-B-xx`) | Governance blocker (`GOV-B-xx`) |
|---|---|---|
| `B-03` | Independent audit findings H-01–H-07 and related actions | Stale scope evidence |
| `B-04` | Proposed key map | Approval-record structure |
| `B-05` | Reference manifest — `NOT CREATED` | Historical owner-confirmation addendum — `OPEN — D-04 PENDING` |
| `B-06` | T-78 plan and results — `NOT EXECUTED` | `BusinessModelClass` population mechanism — `PENDING — D-05` |
| `B-07` | `G3-RV-01` reference-version approval — `NOT EXECUTED` | Source staleness and `ManifestHash` — `PENDING — D-06 and D-07` |
| `B-08` | Independent reviewer — `NOT ASSIGNED` | Evidence-retention policy — `OPEN — D-08 PENDING` |

Sources:

- OD-01B evidence table: `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` lines
  328–337.
- Governance blockers: `OD01_GOVERNANCE_CLOSURE_PROPOSAL.md` §§2–4;
  `OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` §§4–9;
  `OD01_REVISION_0.2_CHANGE_RECORD.md` lines 201–210.

### 6.4 The precondition-8 defect

OD-01A line 197 and OD-01B line 352 both say:

> “B-05 is resolved by D-04, and B-08 is resolved by D-08, or the signature is
> explicitly withheld.”

In the governance namespace this is correct:

- `GOV-B-05` (owner-confirmation addendum) is resolved by `GOV-D-04`;
- `GOV-B-08` (evidence retention) is resolved by `GOV-D-08`.

In OD-01B’s own evidence namespace it is wrong:

- `OD01B-B-05` is the reference manifest, which is not resolved by `GOV-D-04`;
- `OD01B-B-08` is the independent reviewer, which is not resolved by
  `GOV-D-08`.

The decision records do not distinguish the namespaces. A reader cannot tell
which `B-05` and `B-08` the precondition means. This is a material defect in the
signature conditions, not a cosmetic naming issue.

### 6.5 Code provenance table

| Code | Original definition | Original source | Current use in this report |
|---|---|---|---|
| `H-04` | Risk register omits three required scenarios and their controls | `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` §8 lines 228–238 | Finding assessment |
| `H-05` | G3 status contradicts design evidence in the same ledger row | Same report §8 lines 240–250 | Finding assessment |
| `M-07` | Approval workflow lacks independent verification and reference-version approval criteria | Same report §9 lines 350–360 | Finding assessment |
| `M-12` | Approval block approves Sections 2–7 while excluding a schema freeze | Same report §9 lines 410–420 | Finding assessment |
| `GOV-B-03` | Stale scope evidence | `OD01_GOVERNANCE_CLOSURE_PROPOSAL.md` §2 line 78 | Evidence assessment |
| `GOV-B-04` | Approval-record structure | Same proposal §3 line 112 | Evidence assessment |
| `GOV-B-05` | Historical owner-confirmation addendum | Same proposal §4 line 195 | Evidence assessment |
| `GOV-B-08` | Evidence-retention policy | `OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` §9 line 597 | Evidence assessment |
| `OD01B-B-03` | Independent audit findings H-01–H-07 | `OD01B` §10 line 332 | Dual-namespace assessment |
| `OD01B-B-04` | Proposed key map | `OD01B` §10 line 333 | Dual-namespace assessment |
| `OD01B-B-05` | Reference manifest | `OD01B` §10 line 334 | Dual-namespace assessment |
| `OD01B-B-08` | Independent reviewer | `OD01B` §10 line 337 | Dual-namespace assessment |

---

## 7. Decision blockers D-04 to D-08

All five decisions are governance-packet decisions. All five are `PENDING`.
None is approved. None is implied by the revision 0.2 change record, the owner
confirmation, the fresh re-audit, or this report.

### 7.1 `GOV-D-04` — Historical owner-confirmation addendum

| Field | Finding |
|---|---|
| Exact question | Approve a separate controlled addendum to the original owner confirmation stating that the eight choices remain valid, contract v1.5 is current, OD-01A/OD-01B are prepared, historical status statements are superseded, and no approval is implied. |
| Source | `OD01_OWNER_DECISION_PACKET.md` lines 84–97 |
| Current evidence | No addendum file exists. The original confirmation is unchanged at SHA-256 `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`. It still says contract v1.4 and “OD-01A/B not prepared” at lines 20, 82, 299, 327, and 357–358. |
| Proposed text | `OD01_GOVERNANCE_CLOSURE_PROPOSAL.md` Annex A lines 383–393. It cites OD-01A/OD-01B as version 0.1 records, prepared 2026-11-01. Those records are now version 0.2, revised 2026-11-02. The proposed text is therefore stale. |
| Status | `PENDING OWNER APPROVAL` |
| Why it blocks | It blocks a clean signature evidence chain. Without it, the confirmation and the decision records cite different contract versions and different preparation states. |
| What would close it | A separate controlled addendum, preserving the original, citing contract v1.5 and OD-01A/OD-01B revision 0.2, explicitly superseding the historical v1.4/“not prepared” statements, and stating that no approval is implied. The addendum must carry an actual owner decision and date. |
| Dependencies | `GOV-B-05`; `C-04`; contract v1.5 status |

### 7.2 `GOV-D-05` — `BusinessModelClass` baseline

| Field | Finding |
|---|---|
| Exact question | Should all `BusinessModelClass` values remain null for the baseline, or should a documented analytical mapping/rubric be approved? |
| Source | `OD01_OWNER_DECISION_PACKET.md` lines 99–112 |
| Current evidence | OD-01B defines `BusinessModelClass` as an optional nullable analytical classification, not source-verified identity. It says D-05 is pending and no value may be populated — lines 79–83 and 185–188. Contract v1.5 also treats it as optional analytical data and excludes it from identity provenance — lines 247, 252, and 766. No data exists. |
| Status | `PENDING OWNER APPROVAL` |
| Why it blocks | OD-01B Section 4 is inside the approval scope. The owner would approve the nullable column design while the treatment decision remains open. That is acceptable only if the approval conditions explicitly state that no baseline values are approved. The current approval block does not contain that condition. |
| What would close it | An owner decision selecting the null baseline or an approved mapping/rubric. If null is selected, the approval block must state that no values are approved and that the column remains analytical and nullable. If a mapping is selected, the rubric, allowed values, owner, versioning, and examples must exist before population. |
| Dependencies | OD-01B signature; schema freeze if values are populated |

### 7.3 `GOV-D-06` — Source-staleness thresholds and exceptions

| Field | Finding |
|---|---|
| Exact question | Approve the proposed 365-day maximum for airline name, legal name, group, and home country; 180-day maximum for IATA/ICAO codes; and a maximum 90-day written exception, with stale sources quarantined and not loadable. |
| Source | `OD01_OWNER_DECISION_PACKET.md` lines 114–127 |
| Current evidence | Contract v1.5 line 260 states the proposed 365/180-day thresholds and says: “These thresholds are proposed policy, not owner-approved values.” The compensating-control proposal §8.1 repeats the proposal and says it blocks `G3-RV-01`. |
| Status | `PENDING OWNER APPROVAL` |
| Why it blocks | Without approved thresholds, `G3-RV-01` cannot determine whether a source is eligible to support an approved reference version. |
| What would close it | An owner-approved threshold and exception policy recorded in a controlled contract/design change, with the anchor date, stale action, exception duration, evidence requirements, and quarantine rule. |
| Dependencies | `G3-RV-01`; reference approval; contract/design change |

### 7.4 `GOV-D-07` — `ManifestHash` canonicalization

| Field | Finding |
|---|---|
| Exact question | Approve the deterministic canonical-JSON method for `ManifestHash`, covering `reference_version` and fixed-order `ref_airlines.csv` / `ref_airline_sources.csv` name, byte size, and SHA-256, excluding approval metadata and the hash itself. |
| Source | `OD01_OWNER_DECISION_PACKET.md` lines 129–142 |
| Current evidence | Contract v1.5 line 264 names `ManifestHash` as a manifest field but does not define a canonicalization method. The compensating-control proposal §8.2 defines a proposed method and says it is proposed, not implemented. No manifest exists. |
| Status | `PENDING OWNER APPROVAL` |
| Why it blocks | Without a deterministic method, T-78 reproducibility cannot be independently recomputed, and `G3-RV-01` cannot record a defensible manifest hash. |
| What would close it | An owner-approved canonicalization method recorded in the contract/design, with exact JSON field order, encoding, line endings, hash casing, inclusion/exclusion rules, and at least one reproducible test vector. |
| Dependencies | `G3-RV-01`; T-78; reference manifest |

### 7.5 `GOV-D-08` — Evidence-retention policy

| Field | Finding |
|---|---|
| Exact question | Approve the proposed read-only evidence structure under `docs/approvals/`, `docs/approvals/evidence/`, and `docs/approvals/hash_register/`, including signed-copy hash verification and retention. |
| Source | `OD01_OWNER_DECISION_PACKET.md` lines 144–157 |
| Current evidence | `docs/approvals/` does not exist. The compensating-control proposal §9 defines a proposed structure and read-only procedure, but says it is `PROPOSED — NOT IMPLEMENTED`. No hash register, verification log, signed-copy path, or signed-copy hash exists. |
| Status | `PENDING OWNER APPROVAL` |
| Why it blocks | A signed copy can be altered or lost, and the approval may not be reconstructable. The approval blocks’ signed-copy path, hash, and retention fields cannot be completed. |
| What would close it | An owner-approved retention structure and procedure, implemented only at signature time: read-only copy, path, byte size, SHA-256, record version, signer, signature date, hash register, verification log, and retention period. |
| Dependencies | OD-01A/OD-01B signatures; `GOV-B-08` |

### 7.6 Decision summary

| Decision | Topic | Status | Blocks signature? | Blocks `G3-RV-01`? |
|---|---|---|---|---|
| `GOV-D-04` | Owner-confirmation addendum | `PENDING OWNER APPROVAL` | Yes, clean evidence chain | No |
| `GOV-D-05` | `BusinessModelClass` baseline | `PENDING OWNER APPROVAL` | Yes, as an explicit condition | No |
| `GOV-D-06` | Staleness thresholds | `PENDING OWNER APPROVAL` | No | Yes |
| `GOV-D-07` | `ManifestHash` canonicalization | `PENDING OWNER APPROVAL` | No | Yes |
| `GOV-D-08` | Evidence retention | `PENDING OWNER APPROVAL` | Yes, retention condition | No |

---

## 8. Finding H-04 — Risk register omissions

### 8.1 Original finding

The original audit found that the risk register contained R-1 to R-8 but did
not address:

- an airline being suspended or ceasing operations;
- a reference dataset being updated after a model refresh;
- historical synthetic data becoming inconsistent with a changed identity
  reference.

Source: `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` §8 lines 228–238.

### 8.2 Current evidence

`PROJECT_RISK_REGISTER.md` now contains:

| Risk | Scope | Current status |
|---|---|---|
| `R-09` | Airline suspension, cessation, merger, or lifecycle change | `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED` |
| `R-10` | Reference-version change after data refresh or generation | `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED` |
| `R-11` | Historical reproducibility and reference-snapshot consistency | `OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED` |

Each entry contains description, root cause, consequence, likelihood, impact,
inherent rating, mitigation controls, monitoring method, risk-owner role,
residual risk, current status, and evidence required for closure.

The register explicitly states:

- D-09 authorizes the entries, not the controls — lines 16–20;
- no mitigation is recorded as implemented or verified — lines 16–20;
- the register does not approve OD-01A, OD-01B, a reference version, a schema
  freeze, data generation, or implementation — lines 28–35;
- R-09–R-11 remain open and no residual risk is accepted — lines 117–124.

### 8.3 Assessment

**Status: `PARTIALLY VERIFIED — CLOSED AT DOCUMENTATION LEVEL`.**

H-04 was a risk-register omission finding. The required scenarios and controls
now exist, are owned, monitored, and tied to closure evidence. That closes the
documentation omission.

It does not close R-09, R-10, or R-11. No control has been implemented. No
T-78 evidence exists. No owner acceptance of residual risk exists. No reference
version exists. The finding closure must not be read as risk closure.

### 8.4 Residual issues

- R-09–R-11 remain open and unverified.
- The progress ledger does not reference the risk register. This is a minor
  traceability gap.
- OD-01A and OD-01B residual-concern rows still list H-04 as open pending
  re-audit — OD-01A lines 217–219; OD-01B lines 373–375. Those rows are stale
  after the fresh re-audit.
- No owner acceptance of residual risk is recorded.

### 8.5 What would maintain closure

- Keep R-09–R-11 open until the approved reference version, T-78 results,
  applicable reconciliation notes, and owner residual-risk acceptance exist.
- Update the decision-record residual rows to reflect the current H-04 status.
- Do not claim risk closure.

---

## 9. Finding H-05 — G3 status contradiction

### 9.1 Original finding

The original audit found that `PROGRESS_LEDGER.md` marked G3 as `NOT STARTED`
while the same row stated that contract v1.4 documented schemas, grains, keys,
reference datasets, K13, and validation tests. A reader could not tell whether
G3 had not begun, whether design work was in progress but not approved, or
whether `NOT STARTED` was being used as a synonym for `NOT FORMALLY APPROVED`.

Source: `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` §8 lines 240–250.

### 9.2 Current evidence

`PROGRESS_LEDGER.md` now has distinct rows:

| Control | Ledger status | Line |
|---|---|---|
| G3 gate execution | `NOT STARTED` | 12 |
| G3 design documentation | `PREPARED — DRAFT` | 13 |
| G3 formal approval | `NOT FORMALLY APPROVED` | 14 |
| Schema freeze | `NOT AUTHORIZED` | 15 |
| `G3-RV-01` | `NOT EXECUTED` | 16 |
| G4 | `BLOCKED` | 17 |

The ledger also defines the status vocabulary and states that
`PREPARED — DRAFT` is a documentation state, not a gate status or approval —
line 4.

### 9.3 Assessment

**Status: `PARTIALLY VERIFIED`.**

The original same-row contradiction is resolved in the ledger. The correction
is not fully propagated:

- Contract v1.5 still says “G3 remains `NOT STARTED`” in §16.1 line 1907 and
  uses a single G3 status in AC-20 line 1867.
- OD-01A line 26 and OD-01B line 26 still say “G3 remains NOT STARTED” without
  the split label.
- The owner confirmation still says “G3 remains NOT STARTED” at line 360 and
  treats the old ledger as authoritative.
- The ledger’s G3 documentation row says “T-01 to T-78 are PLANNED” — line 13.
  Contract v1.5 has eight `BLOCKED` tests: T-37, T-42–T-46, T-55, and T-79.
  The other 71 are `PLANNED`. The ledger summary is wrong.
- G3 entry and exit criteria are distributed across contract §15.2
  (AC-16–AC-24) and the ledger blocker list. They are not consolidated into one
  explicit gate-criteria record.
- The owner packet still lists governance D-10 as `PENDING`; the change record
  says that entry is superseded.

### 9.4 Test-status evidence

| Status | Count | IDs |
|---|---:|---|
| `PLANNED` | 71 | All test rows except the eight blocked |
| `BLOCKED` | 8 | T-37, T-42, T-43, T-44, T-45, T-46, T-55, T-79 |
| `PASS` | 0 | None |
| Total test rows | 79 | T-01 through T-79 |

The ledger says T-01 to T-78 are `PLANNED` and T-79 is `BLOCKED`. That omits
seven blocked tests: T-37, T-42–T-46, and T-55.

### 9.5 What would close H-05

- Propagate the six-status vocabulary to the contract’s G3 rows, both decision
  record status notices, and the owner confirmation or its addendum.
- Consolidate G3 entry and exit criteria into one explicit gate-criteria record.
- Correct the ledger’s test summary to 71 `PLANNED`, 8 `BLOCKED`, 0 `PASS`.
- Update the residual-status rows in OD-01A and OD-01B.

---

## 10. Finding M-07 — Approval workflow and reference-version criteria

### 10.1 Original finding

The original audit found:

- the owner is the sole approver and the person for whom the draft was prepared;
- no named verifier, review checklist, or definition of “verified” existed;
- the contract’s approval record listed roles the draft did not address;
- no decision ID, owner, or criteria existed for reference-version approval.

Source: `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` §9 lines 350–360.

### 10.2 Current evidence

The package now documents a compensating-control route:

- OD-01A and OD-01B state that no independent reviewer is assigned — OD-01A
  lines 205–219; OD-01B lines 361–375.
- They distinguish AI-assisted review from owner self-review and state that
  owner self-review is not independent review.
- They include reviewer-route, reviewer-limitation, reviewer-result,
  residual-concern, and re-audit-precondition fields.
- `OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` defines CC-01 owner
  self-review, CC-02 independent challenge, CC-06 finding closure, CC-09
  reviewer limitation, and CC-10 future review.
- OD-01B §7 and contract §3.4 define `G3-RV-01` as the reference-version
  approval artifact, with owner, exact version, file hashes, source evidence,
  T-75/T-76 results, T-78 plan/results, and refresh configuration.

### 10.3 Assessment

**Status: `PARTIALLY VERIFIED`.**

The control package is documented, not executed:

- CC-01 owner self-review is `NOT EXECUTED`; no dated checklist, owner initials,
  unresolved-question record, or disposition exists.
- CC-02 independent challenge is `NOT EXECUTED`; no named reviewer exists.
- CC-06 is only `PARTIALLY EXECUTED` as a non-independent document re-audit.
- CC-07 residual-risk register is `PREPARED — OWNER ACCEPTANCE PENDING`.
- CC-08 evidence preservation is `DESIGNED — NOT EXECUTED`;
  `docs/approvals/` does not exist.
- CC-09 reviewer limitation is drafted but not owner-accepted.
- No `G3-RV-01` artifact exists; no reference data or manifest exists.
- The approval blocks still have blank owner decision, signature, date,
  conditions, reviewer identity, reviewer signature, signed-copy path,
  signed-copy hash, and verification result.

### 10.4 The substantive identifier error

OD-01A line 197 and OD-01B line 352 use `B-05` and `B-08` as if they were the
governance blockers. In OD-01B’s own evidence table, `B-05` is the reference
manifest and `B-08` is the independent reviewer. The precondition mappings are
correct only in the governance namespace.

This is not a cosmetic issue. It makes the signature conditions ambiguous and
prevents a clean M-07/B-04 closure.

### 10.5 What would close M-07

- Execute CC-01 owner self-review with a dated checklist and owner initials.
- Record unresolved questions and dispositions.
- Record owner acceptance of the executed controls and residual limitation.
- Record residual-risk acceptance.
- Record a named human reviewer, or a signed owner acknowledgment of the
  no-reviewer limitation under D-02.
- Correct the `B-05`/`B-08` and `D-04`/`D-08` mapping.
- Define and eventually execute `G3-RV-01`.

---

## 11. Finding M-12 — Approval scope versus schema freeze

### 11.1 Original finding

The original audit found that the selected option approved “the ten-airline
roster and identity rules in Sections 2 to 7,” while the record said it did not
freeze the data contract, semantic model, or reference schemas. The signature
scope was ambiguous.

Source: `OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` §9 lines 410–420.

### 11.2 Current evidence

OD-01B §11.3 now says the approval covers Sections 2, 4, 5, 6, and 8 only;
Sections 3 and 7 are acknowledged design baselines, not a schema freeze. It
explicitly excludes schema freeze, reference-data creation, synthetic data,
production ETL, Power Query, semantic model, DAX, Power BI, G3, G4,
`G3-RV-01`, and Git — lines 379–390.

OD-01A §7.3 has a comparable narrow scope for Sections 2, 3, and 4 — lines
223–226.

### 11.3 Assessment

**Status: `PARTIALLY VERIFIED`.**

The scope is narrower and the exclusions are explicit. Four defects remain:

1. **The approving sentence claims rules that sit in the excluded section.**
   OD-01B §11.3 says the approval covers “the governing airline identity, key,
   provenance, lifecycle, reference-version, manifest, immutable-mapping, and
   Power BI identity/disclosure rules in OD-01B Sections 2, 4, 5, 6, and 8.”
   The reference-version, manifest, and immutable-mapping mechanics are
   principally in Section 7, which the same sentence excludes.

2. **The key-map approval gap.** Contract §7.1 line 1046 says the airline key
   map is immutable after OD-01B approval. OD-01B §3 lines 135–136 calls the
   map a proposed administrative allocation and says this revision does not
   approve it. OD-01B §2 item 10 says the map is immutable after approval but
   does not identify which approval. OD-01B §11.3 excludes Section 3. An
   OD-01B signature cannot both exclude the map and make it immutable.

3. **OD-01A Section 3 includes the proposed `AirlineId` allocation.**
   OD-01A §7.3 approves Sections 2, 3, and 4. Section 3 lines 108–110 says the
   `AirlineId` column is proposed and not approved by OD-01A. The population
   approval and the proposed identifier allocation are not cleanly separated.

4. **`GOV-D-05` is pending while OD-01B Section 4 is in scope.** OD-01B lines
   185–188 say no `BusinessModelClass` value may be populated. That is a
   reasonable boundary, but the approval block does not state that no baseline
   values are approved.

### 11.4 What would close M-12

- Make the approving sentence match the section list exactly.
- State whether Sections 3 and 7 are approved, acknowledged, or excluded.
- Resolve the key-map trigger: OD-01B approval or `G3-RV-01`.
- Clarify OD-01A Section 3’s proposed `AirlineId` allocation.
- State the `GOV-D-05` condition in the OD-01B approval block.

---

## 12. Evidence items B-03, B-04, B-05, B-08

### 12.1 Dual-namespace assessment

| Code | OD-01B evidence status | Governance status | Assessment |
|---|---|---|---|
| `B-03` | `RECORDED` — audit findings H-01–H-07 (document title says “independent”; the report itself records a self-audit limitation) | `VERIFIED — CLOSED AT DOCUMENT LEVEL` — stale scope evidence corrected | The OD-01B item is present. The governance blocker is closed at document level, but residual rows still list it open. |
| `B-04` | `RECORDED DESIGN — PENDING FORMAL APPROVAL` — proposed key map | `PARTIALLY VERIFIED` — approval-record structure | The key map remains proposed. The approval-record structure exists but lacks owner initials/date and a compensating-control evidence reference. |
| `B-05` | `NOT CREATED` — reference manifest | `PENDING OWNER APPROVAL` — owner-confirmation addendum | The reference manifest does not exist. The addendum does not exist. `GOV-D-04` does not resolve the manifest. |
| `B-08` | `NOT ASSIGNED` — independent reviewer | `PENDING OWNER APPROVAL` — evidence retention | No reviewer is assigned. `docs/approvals/` does not exist. `GOV-D-08` does not resolve the reviewer. |

### 12.2 `GOV-B-03` — Stale scope evidence

**Status: `VERIFIED — CLOSED AT DOCUMENT LEVEL`.**

Verified:

- `01_PROJECT_SCOPE.md` is version 1.1, 6,384 bytes, SHA-256
  `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C`.
- OD-01A E-07 cites that version, hash, and byte count — line 177.
- OD-01B shared evidence cites the same version, hash, and byte count — lines
  318–324.
- The obsolete hash
  `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9`
  occurs zero times in current OD-01A and OD-01B.
- It remains in dated historical, audit, proposal, and change-record evidence
  that documents the pre-correction value: the original governance audit
  (a self-audit, not independent assurance), owner
  resolution, prior remediation change record, migration final report,
  governance closure proposal, compensating-control proposal, prior formal
  decision draft, and fresh re-audit. That is appropriate historical evidence,
  not a current approval citation.

Residual issue: OD-01A and OD-01B residual-concern rows still list B-03 as open.
Those rows are stale.

### 12.3 `GOV-B-04` — Approval-record structure

**Status: `PARTIALLY VERIFIED`.**

Present in both decision records:

- decision options;
- approval scope and exclusions;
- owner name;
- owner decision field;
- owner signature and actual approval date fields;
- approval conditions field;
- reviewer route;
- compensating-control acceptance statement;
- reviewer limitation statement;
- reviewer name/role/organization;
- reviewer independence;
- reviewer result;
- reviewer signature/date;
- residual concerns;
- re-audit record;
- scope v1.1 hash;
- contract v1.5 hash;
- signed-copy path;
- signed-copy hash;
- retention confirmation;
- verification date/result.

Missing or ambiguous:

- The required owner initials/date for compensating-control acceptance is
  missing. The block says “D-01/D-02 accepted; execution not complete,” but
  records no initials or date.
- There is no explicit reference to the compensating-control evidence: CC-01
  checklist, CC-09 limitation acceptance, or residual-risk acceptance.
- The `B-05`/`B-08` precondition rows conflate the governance blockers with
  OD-01B’s local evidence.
- The re-audit record is blank, which is expected before this report is
  accepted, but it means the block is not complete.
- The residual-concerns row is stale: it lists H-04, H-05, M-07, M-12, B-03,
  B-04, B-05, and B-08 as open without current per-finding statuses.
- The signed-copy path and hash cannot be completed until `GOV-D-08` is decided
  and a signed copy exists.

### 12.4 `GOV-B-05` — Owner-confirmation addendum

**Status: `PENDING OWNER APPROVAL — GOV-D-04 PENDING`.**

No addendum exists. The original confirmation remains unchanged at
`AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`.

Current stale statements:

- “Governing contract: `docs/03_DATA_CONTRACTS.md` version 1.4 — unchanged” —
  line 20.
- “Contract: version 1.4, unchanged” — line 82.
- “`docs/03_DATA_CONTRACTS.md` remains version 1.4” — line 299.
- “Version 1.5 does not exist yet” — line 327.
- “OD-01A not prepared or signed” — line 357.
- “OD-01B not prepared or signed” — line 358.

The proposed Annex A in `OD01_GOVERNANCE_CLOSURE_PROPOSAL.md` lines 383–393
cites OD-01A/OD-01B version 0.1, prepared 2026-11-01. The current records are
version 0.2, revised 2026-11-02. The proposed text must be refreshed before it
can be used.

### 12.5 `GOV-B-08` — Evidence retention

**Status: `PENDING OWNER APPROVAL — GOV-D-08 PENDING`.**

- `docs/approvals/` does not exist.
- No `decision_hash_register.csv`, `verification_log.csv`, signed-copy path, or
  signed-copy hash exists.
- The approval blocks correctly mark signed-copy fields as blank and retention
  as “No — D-08 PENDING.”
- The compensating-control proposal §9 defines a proposed structure and
  read-only procedure, but explicitly says it is `PROPOSED — NOT IMPLEMENTED`.

### 12.6 `OD01B-B-05` — Reference manifest

**Status: `NOT FOUND`.**

OD-01B line 334 classifies the reference manifest as `NOT CREATED`.
`data/manifests/` exists with zero files. No `reference_versions.csv` exists.
No reference version is approved.

This item is not resolved by `GOV-D-04`. It requires OD-01A/OD-01B signatures,
`GOV-D-06`, `GOV-D-07`, reference data, and `G3-RV-01`.

### 12.7 `OD01B-B-08` — Independent reviewer

**Status: `NOT FOUND`.**

OD-01B line 337 classifies the independent reviewer as `NOT ASSIGNED`.
No reviewer name, role, organization, signature, or independence statement
exists. No signed owner acknowledgment of the no-reviewer limitation exists.

This item is not resolved by `GOV-D-08`. It requires a named human reviewer or a
signed D-02 limitation acceptance.

### 12.8 Consolidated evidence matrix

| Code | Original meaning | Current evidence | Status | What would close it |
|---|---|---|---|---|
| `GOV-D-04` | Owner-confirmation addendum | No addendum; original still says v1.4 and “not prepared” | `PENDING OWNER APPROVAL` | Controlled addendum citing v1.5 and v0.2, preserving original |
| `GOV-D-05` | `BusinessModelClass` baseline | Null/optional design; no values; no condition in approval block | `PENDING OWNER APPROVAL` | Owner selects null or mapping; approval condition recorded |
| `GOV-D-06` | Staleness thresholds | Proposed 365/180 days; expressly not approved | `PENDING OWNER APPROVAL` | Approved thresholds and exception policy |
| `GOV-D-07` | `ManifestHash` canonicalization | Method proposed only; not in contract | `PENDING OWNER APPROVAL` | Approved canonical method and test vector |
| `GOV-D-08` | Evidence retention | `docs/approvals/` absent | `PENDING OWNER APPROVAL` | Approved and implemented retention structure |
| `H-04` | Risk-register omissions | R-09–R-11 exist; all open | `PARTIALLY VERIFIED` | Maintain closure; update residual rows; do not claim risk closure |
| `H-05` | G3 status contradiction | Ledger split exists; not propagated; ledger test summary wrong | `PARTIALLY VERIFIED` | Propagate vocabulary; consolidate criteria; correct test summary |
| `M-07` | Approval workflow and reference-version criteria | Compensating route documented; not executed; no reviewer | `PARTIALLY VERIFIED` | Execute self-review; record acceptance/limitation; define `G3-RV-01` |
| `M-12` | Approval scope versus schema freeze | Narrow scope; key-map gap; Section 3 ambiguity | `PARTIALLY VERIFIED` | Align scope; resolve key-map trigger; state D-05 condition |
| `GOV-B-03` | Stale scope evidence | Current hash present; stale hash absent from current records | `VERIFIED` | Update stale residual rows |
| `GOV-B-04` | Approval-record structure | Fields present; initials/date and evidence reference missing | `PARTIALLY VERIFIED` | Complete fields at signature; reference CC evidence |
| `GOV-B-05` | Owner-confirmation addendum | No addendum | `PENDING OWNER APPROVAL` | `GOV-D-04` |
| `GOV-B-08` | Evidence retention | No structure | `PENDING OWNER APPROVAL` | `GOV-D-08` |
| `OD01B-B-03` | Audit findings evidence | Present | `VERIFIED` | No action beyond current use |
| `OD01B-B-04` | Proposed key map | Proposed; not approved | `PARTIALLY VERIFIED` | Resolve key-map approval gap |
| `OD01B-B-05` | Reference manifest | `NOT CREATED` | `NOT FOUND` | Signatures; D-06/D-07; reference data; `G3-RV-01` |
| `OD01B-B-08` | Independent reviewer | `NOT ASSIGNED` | `NOT FOUND` | Named reviewer or signed D-02 limitation |

---

## 13. Cross-document contradictions and consistency checks

### 13.1 Material contradictions

The fresh re-audit records ten contradictions, C-01 through C-10. This
investigation independently confirms them at document level.

| ID | Issue | Evidence | Impact | Status |
|---|---|---|---|---|
| `C-01` | `B-xx` identifiers mean different things | OD-01B evidence table lines 328–337; governance proposals; change record lines 201–210; precondition 8 in both decision records | Precondition 8 is correct only in the governance namespace; M-07/B-04 cannot close cleanly | `OPEN` |
| `C-02` | Key-map approval gap | Contract §7.1 line 1046; OD-01B §3 lines 135–136; OD-01B §11.3 lines 379–390 | An OD-01B signature cannot both exclude the map and make it immutable | `OPEN` |
| `C-03` | `D-xx` identifier collision | Design specification lines 128–132; owner packet lines 84–157 | Authorization trail is readable only with document context | `OPEN` |
| `C-04` | Historical packet versus current authorization | Owner packet Part C lines 193–204; change record lines 34–50; owner confirmation lines 20, 82, 299, 327, 357–358; prior remediation change record | Authorization chain is documented but not clean; D-04 pending | `OPEN` |
| `C-05` | H-05 split vocabulary not propagated | Ledger lines 12–16; contract line 1907; OD-01A line 26; OD-01B line 26 | Reader can still conflate gate execution, documentation, and approval | `OPEN` |
| `C-06` | OD-01A Section 3 includes proposed `AirlineId` allocation | OD-01A lines 108–110 and 223–226 | Signature could be read as approving the identifier allocation | `OPEN` |
| `C-07` | D-05 pending while OD-01B Section 4 is in scope | OD-01B lines 185–188 and 397 | Signature may approve the nullable column design while D-05 is undecided | `OPEN` |
| `C-08` | Residual status rows are stale | OD-01A lines 217–219; OD-01B lines 373–375 | Approval block would contradict the latest re-audit if signed unchanged | `OPEN` |
| `C-09` | Contract v1.5 is not formally approved but is the governing baseline | Contract line 9; OD-01A line 15; OD-01B line 15 | Dependency the owner should not overlook | `OPEN` |
| `C-10` | Ledger test-status summary contradicts the contract | Ledger line 13; contract test rows | G3 documentation evidence overstates readiness | `OPEN` |

### 13.2 Checks that passed

| Check | Result | Evidence |
|---|---|---|
| Roster consistency | PASS — same ten airlines and IATA/ICAO codes across scope, contract, OD-01A, OD-01B | `01_PROJECT_SCOPE.md` lines 44–55; `03_DATA_CONTRACTS.md` §2.1; OD-01A §3; OD-01B §2.1 |
| Reporting period | PASS — 2025-10-01 through 2026-09-30 inclusive in scope, business requirements, contract, OD-01A, OD-01B | Scope line 7; BR-01; contract line 11; OD-01A line 71; OD-01B lines 109–110 |
| Disclosure string | PASS — em dash form used consistently; no current hyphen variant found | Scope line 105; BR-01 line 16; contract lines 78/1227/1680; OD-01A line 74; OD-01B lines 100/118/297 |
| Scope hash | PASS — current scope v1.1 hash present in OD-01A and OD-01B; obsolete hash absent from both | OD-01A line 177; OD-01B lines 318–324 |
| Local Markdown links | PASS — zero broken local links across current Markdown documents | Automated link resolution |
| Duplicate headings | PASS — zero duplicate headings within each current Markdown document | Automated heading check |
| Encoding | PASS — 28 current Markdown files: zero UTF-8 BOM | Byte inspection |
| Line endings | PASS — 28 current Markdown files: zero CRLF pairs | Byte inspection |

**Line-ending note:** two historical `.txt` migration reports
(`OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt` and
`OD01_MIGRATION_PREPARATION_REPORT.txt`) use CRLF. They are historical
evidence, not current Markdown governing documents. All 28 current Markdown
files are LF-only.
| Backup manifest | PASS — revision 0.2 backup hashes match manifest | Manifest and file hashes |
| No unauthorized artifacts | PASS — no reference CSV, manifest, synthetic data, Python, Power Query, DAX, Power BI, or QA output outside backups | Directory inspection |
| No approvals | PASS — `docs/approvals/` absent; no signed copy; no approval date; no reviewer identity | Directory and text inspection |
| Git | PASS — zero commits; all project paths untracked; no Git write by this investigation | `git status`, `git rev-list --count --all` |

### 13.3 Checks that failed or remain open

- C-01 through C-10 remain open.
- H-05, M-07, M-12, and B-04 remain partially verified.
- The ledger’s test summary is wrong.
- The decision-record residual rows are stale.
- The key-map approval trigger is unresolved.
- The B/D namespace collision is unresolved.
- `GOV-D-04` through `GOV-D-08` remain pending.

---

## 14. OD-01A signature readiness

### 14.1 Status

**`BLOCKED — NOT READY FOR SIGNATURE`.**

The population decision itself is coherent:

- exactly ten real airline identities;
- fixed reporting period 2025-10-01 through 2026-09-30;
- synthetic operations, customer, booking, revenue, cost, disruption,
  feedback, and financial data;
- exact unconditional disclosure;
- clear exclusion boundary;
- attribute-level source verification required before reference approval.

The blockers are governance and record-structure issues, not a defect in the
ten-airline roster.

### 14.2 Blocking conditions

| # | Blocker | Evidence | Consequence |
|---:|---|---|---|
| 1 | H-05 partially closed | OD-01A line 26; ledger lines 12–16; contract line 1907 | G3 vocabulary and criteria remain ambiguous |
| 2 | M-07 partially closed | OD-01A lines 205–219 | Owner self-review and executed-control acceptance are missing |
| 3 | B-04 partially closed | OD-01A lines 240–254 | Compensating-control initials/date and evidence reference are missing |
| 4 | `GOV-B-05`/`GOV-D-04` open | Owner confirmation lines 20, 82, 299, 327, 357–358 | Confirmation still says contract v1.4 and OD-01A not prepared |
| 5 | `GOV-B-08`/`GOV-D-08` open | OD-01A lines 251–253 | No signed-copy retention or hash register |
| 6 | Section 3 scope ambiguity | OD-01A lines 108–110 and 223–226 | Proposed `AirlineId` allocation may be read as approved |
| 7 | Residual row stale | OD-01A lines 217–219 | Approval block contradicts the latest re-audit |
| 8 | Re-audit precondition unmet | OD-01A lines 188–201 | “No signature blocker remains” is not satisfied |
| 9 | No signed copy or owner self-review | OD-01A lines 236–258 | Signature evidence chain incomplete |

### 14.3 What would unblock OD-01A

1. Resolve C-01, C-03, C-04, C-06, C-08, and C-10.
2. Decide `GOV-D-04`, `GOV-D-05`, and `GOV-D-08`.
3. Execute and record CC-01 owner self-review.
4. Complete the B-04 compensating-control initials/date and evidence reference.
5. Re-audit the corrected record and update the residual row.
6. Sign with an actual date and actual evidence references.
7. Retain the signed copy read-only after `GOV-D-08` is implemented.

No signature should be entered now.

---

## 15. OD-01B signature readiness

### 15.1 Status

**`BLOCKED — NOT READY FOR SIGNATURE`.**

OD-01B contains the strongest technical content in the package: durable
`AirlineId`, permanent `AirlineKey`, version-qualified IATA/ICAO, provenance,
lifecycle, manifest authority, T-78, and Power BI constraints. It also has the
most serious approval-scope ambiguity.

### 15.2 Blocking conditions

| # | Blocker | Evidence | Consequence |
|---:|---|---|---|
| 1 | H-05, M-07, B-04, `GOV-B-05`/`GOV-D-04`, `GOV-B-08`/`GOV-D-08`, stale residual rows | Same as OD-01A; OD-01B lines 26, 361–375, 404–418 | Signature package incomplete |
| 2 | M-12 partially closed | OD-01B lines 379–390; contract line 1046 | Approving sentence claims Section 7 rules while excluding Section 7 |
| 3 | Key-map approval gap | OD-01B lines 135–136, 389–390; contract line 1046 | Signature cannot both exclude and immobilize the map |
| 4 | `GOV-D-05` pending while Section 4 is in scope | OD-01B lines 185–188, 397 | No condition stating that no `BusinessModelClass` values are approved |
| 5 | `OD01B-B-05` reference manifest absent | OD-01B line 334; `data/manifests/` empty | No approved reference version |
| 6 | `OD01B-B-08` reviewer absent | OD-01B line 337 | No independent review or signed limitation |
| 7 | `G3-RV-01` not executed | OD-01B line 336; ledger line 16 | Reference-version approval missing |
| 8 | Contract v1.5 not formally approved | Contract line 9 | OD-01B must not be read as contract approval |
| 9 | No signed copy or owner self-review | OD-01B lines 400–418 | Signature evidence chain incomplete |

### 15.3 What would unblock OD-01B

1. Resolve C-01, C-02, C-03, C-04, C-05, C-07, C-08, C-09, and C-10.
2. Decide `GOV-D-04`, `GOV-D-05`, and `GOV-D-08`.
3. Resolve the key-map approval trigger.
4. State the D-05 condition in the approval block.
5. Execute and record CC-01 owner self-review.
6. Complete the B-04 compensating-control initials/date and evidence reference.
7. Re-audit the corrected record and update the residual row.
8. Sign OD-01A first, then OD-01B, with actual dates and evidence references.
9. Retain the signed copies read-only after `GOV-D-08` is implemented.
10. Decide `GOV-D-06` and `GOV-D-07`, then prepare `G3-RV-01`.

No signature should be entered now.

---

## 16. G3, G4, and implementation authorization

### 16.1 G3 and G4 status

| Control | Status | Evidence | Meaning |
|---|---|---|---|
| G3 gate execution | `NOT STARTED` | Ledger line 12; contract line 1907 | No gate review held |
| G3 design documentation | `PREPARED — DRAFT` | Ledger line 13; contract v1.5; OD-01A/B v0.2 | Design documents exist; not gate execution |
| G3 formal approval | `NOT FORMALLY APPROVED` | Ledger line 14; unsigned OD-01A/B | No formal approval |
| Schema freeze | `NOT AUTHORIZED` | Ledger line 15; contract line 9 | No freeze decision |
| `G3-RV-01` | `NOT EXECUTED` | Ledger line 16; OD-01B line 336 | No reference version approved |
| G4 data generation | `BLOCKED` | Ledger line 17; contract AC-21 line 1868 | G3 not approved; no written G4 authorization |

### 16.2 Test status

| Status | Count | IDs |
|---|---:|---|
| `PLANNED` | 71 | All test rows except the eight blocked |
| `BLOCKED` | 8 | T-37, T-42, T-43, T-44, T-45, T-46, T-55, T-79 |
| `PASS` | 0 | None |
| Total | 79 | T-01 through T-79 |

The ledger’s “T-01 to T-78 are PLANNED” summary is inaccurate. Seven blocked
tests are omitted from the ledger’s blocker statement.

### 16.3 Artifact state

- `data/04_reference/` — empty.
- `data/manifests/` — empty.
- `qa/results/` — empty.
- `qa/screenshots/` — empty.
- `power_bi/` — empty.
- `docs/approvals/` — absent.
- No `.py`, `.pbix`, `.pbip`, `.csv`, or `.parquet` production artifact outside
  backups.
- No schema freeze, reference CSV, synthetic data, Power Query, DAX, Power BI,
  or Git write operation.

### 16.4 What G3 and G4 require

G3 requires:

- formal OD-01A and OD-01B signatures with actual dates and evidence;
- resolution of the critical decisions listed in contract §14;
- consolidated G3 entry and exit criteria;
- corrected test-status reporting;
- `G3-RV-01` for the reference version;
- a gate review record.

G4 requires:

- G3 `APPROVED`;
- written G4 authorization;
- reference data and manifest approved through `G3-RV-01`;
- schema freeze;
- validation implementation and dry-run evidence.

No G3 or G4 advancement is authorized by this report.

---

## 17. Remediation and closure requirements

### 17.1 How to read this section

The tables below split remediation into five categories:

- **A — Owner decisions:** `GOV-D-04` through `GOV-D-08`.
- **B — Findings:** H-04, H-05, M-07, M-12.
- **C — Evidence and namespace:** `GOV-B-03`, `GOV-B-04`, `GOV-B-05`,
  `GOV-B-08`, `OD01B-B-05`, `OD01B-B-08`, C-01, C-02.
- **D — Document consistency:** C-03 through C-10 and related stale rows.
- **E — Gate and signature:** OD-01A, OD-01B, G3, G4, `G3-RV-01`.

Severity is an analytical priority, not an approval. “Owner” means the project
owner authorizes; a preparer may execute document edits only after explicit
authorization.

### 17.2 Category A — Owner decisions

| ID | Severity | Root cause | Evidence location | Required correction | Owner | Dependency | Authorization | Acceptance criteria | Verification method |
|---|---|---|---|---|---|---|---|---|---|
| `A-01` / `GOV-D-04` | HIGH | Historical confirmation not superseded | Owner confirmation lines 20, 82, 299, 327, 357–358; packet lines 84–97 | Create separate controlled addendum preserving original; cite contract v1.5 and OD-01A/B v0.2; supersede historical statements; no approval implied | Project Owner | C-04; contract status | `GOV-D-04` | Addendum exists, signed/dated, original unchanged, stale statements explicitly superseded | Hash original; text check; owner decision/date |
| `A-02` / `GOV-D-05` | MEDIUM | `BusinessModelClass` treatment undefined | OD-01B lines 79–83, 185–188; contract lines 247, 252, 766 | Owner selects null baseline or approved mapping/rubric; record condition in OD-01B approval block | Project Owner | OD-01B signature | `GOV-D-05` | Decision recorded; no values populated unless mapping approved; approval condition explicit | Search for populated values; inspect approval block |
| `A-03` / `GOV-D-06` | HIGH | Thresholds proposed, not approved | Contract line 260; compensating proposal §8.1 | Approve or revise 365/180-day thresholds and 90-day exception policy; record in controlled change | Project Owner | `G3-RV-01` | `GOV-D-06` | Approved thresholds, anchor, stale action, exception rules recorded | Cross-check contract/design; re-audit |
| `A-04` / `GOV-D-07` | HIGH | `ManifestHash` canonicalization undefined | Contract line 264; compensating proposal §8.2 | Approve deterministic canonical-JSON method; record exact field order, encoding, casing, exclusions, test vector | Project Owner | `G3-RV-01`; T-78 | `GOV-D-07` | Method recorded; reproducible test vector matches; T-78 can recompute | Independent recomputation; manifest test |
| `A-05` / `GOV-D-08` | HIGH | Retention structure absent | `docs/approvals/` absent; compensating proposal §9 | Approve read-only structure, hash register, verification log, signed-copy procedure, retention period | Project Owner | OD-01A/B signatures | `GOV-D-08` | Structure exists read-only; signed-copy path/hash recorded; verification log works | Directory check; hash verification; ACL check |

### 17.3 Category B — Findings

| ID | Severity | Root cause | Evidence location | Required correction | Owner | Dependency | Authorization | Acceptance criteria | Verification method |
|---|---|---|---|---|---|---|---|---|---|
| `B-01` / `H-04` | HIGH | Risk register omitted three scenarios | Risk register R-09–R-11; original audit lines 228–238 | Maintain R-09–R-11 as open; update residual rows; do not claim risk closure | Project Owner | None for doc closure | D-09 recorded; new doc change for residual rows | R-09–R-11 remain open with owners, controls, monitoring, closure evidence; H-04 status current | Register inspection; re-audit |
| `B-02` / `H-05` | HIGH | Single G3 label; criteria not consolidated; ledger test summary wrong | Ledger lines 12–16; contract line 1907; OD-01A line 26; OD-01B line 26; ledger line 13 | Propagate six-status vocabulary; consolidate G3 criteria; correct test summary to 71/8/0 | Project Owner | Controlled doc change | New authorization | All current docs use split status; criteria consolidated; ledger matches contract | Text search; test count; re-audit |
| `B-03` / `M-07` | MEDIUM | No independent reviewer; controls not executed | OD-01A/B §7.2/§11.2; CC-01–CC-10; no `G3-RV-01` | Execute CC-01 self-review; record acceptance, residual risk, signed limitation; define `G3-RV-01` | Project Owner | `GOV-D-08`; B namespace | Owner execution/acceptance | Dated checklist, initials, unresolved questions, acceptance, limitation, `G3-RV-01` definition exist | Artifact inspection; signature check |
| `B-04` / `M-12` | MEDIUM | Scope sentence vs section list; key-map gap; Section 3 ambiguity; D-05 condition | OD-01B lines 379–390; contract line 1046; OD-01A lines 108–110, 223–226 | Align scope; resolve key-map trigger; clarify Section 3; state D-05 condition | Project Owner | `GOV-D-05`; C-02 | New authorization | Signature block unambiguously lists approved/acknowledged/excluded; one key-map trigger; D-05 condition stated | Cross-document review; re-audit |

### 17.4 Category C — Evidence and namespace

| ID | Severity | Root cause | Evidence location | Required correction | Owner | Dependency | Authorization | Acceptance criteria | Verification method |
|---|---|---|---|---|---|---|---|---|---|
| `C-01` / `GOV-B-03` | HIGH | Stale scope hash | OD-01A E-07; OD-01B shared evidence; current scope hash | Update stale residual row; preserve historical evidence | Project Owner | None | D-03 recorded | Stale hash absent from current records; residual row current | Global search; hash check |
| `C-02` / `GOV-B-04` | MEDIUM | Approval record incomplete | OD-01A lines 240–254; OD-01B lines 404–418 | Add owner initials/date for CC acceptance; add CC evidence reference | Project Owner | M-07 | Signature-time completion | Fields completed with actual initials/date and evidence path | Approval-block inspection |
| `C-03` / `GOV-B-05` | MEDIUM | Addendum not created | Owner confirmation stale statements | Execute `GOV-D-04` | Project Owner | `GOV-D-04` | `GOV-D-04` | Addendum exists and supersedes stale statements | Text and hash check |
| `C-04` / `GOV-B-08` | MEDIUM | Retention structure absent | `docs/approvals/` absent | Execute `GOV-D-08` | Project Owner | `GOV-D-08` | `GOV-D-08` | Read-only structure, hash register, verification log exist | Directory and hash check |
| `C-05` / `OD01B-B-05` | HIGH | Reference manifest absent | OD-01B line 334; `data/manifests/` empty | Create only after signatures, D-06/D-07, reference data, `G3-RV-01` | Project Owner | OD-01A/B signatures; D-06/D-07 | Separate reference authorization | Manifest exists with approved version and hash | File check; T-78 |
| `C-06` / `OD01B-B-08` | HIGH | No independent reviewer | OD-01B line 337 | Assign named human reviewer or record signed D-02 limitation | Project Owner | M-07 | Owner decision | Reviewer identity/signature or signed limitation exists | Approval-block inspection |
| `C-07` / `C-01` | HIGH | Duplicate `B-xx` labels | OD-01B lines 328–337; governance proposals; precondition 8 | Adopt prefixed notation in future controlled documents; correct precondition 8 | Project Owner | Controlled doc change | New authorization | No ambiguous B token in signature/preconditions | Global search; cross-doc review |
| `C-08` / `C-02` | HIGH | Contract immutability trigger conflicts with OD-01B exclusion | Contract line 1046; OD-01B lines 135–136, 379–390 | Choose one key-map approval trigger and align contract/decision record | Project Owner | M-12 | New authorization | One documented trigger; no circularity | Cross-document review |

### 17.5 Category D — Document consistency

| ID | Severity | Root cause | Evidence location | Required correction | Owner | Dependency | Authorization | Acceptance criteria | Verification method |
|---|---|---|---|---|---|---|---|---|---|
| `D-01` / `C-03` | MEDIUM | Duplicate `D-xx` labels | Design spec lines 128–132; owner packet lines 84–157 | Add namespace note or prefixed labels in future controlled documents | Project Owner | Controlled doc change | New authorization | Every cited D code unambiguous | Global search; cross-doc review |
| `D-02` / `C-04` | HIGH | Confirmation v1.4 vs contract v1.5 | Owner confirmation lines 20, 82, 299, 327, 357–358; change records | Execute `GOV-D-04`; state contract v1.5 and OD-01A/B v0.2 | Project Owner | `GOV-D-04` | `GOV-D-04` | Evidence chain current and internally consistent | Text and hash check |
| `D-03` / `C-05` | MEDIUM | G3 vocabulary not propagated | Contract line 1907; OD-01A line 26; OD-01B line 26 | Propagate six-status vocabulary | Project Owner | H-05 | New authorization | All current docs use split status | Text search |
| `D-04` / `C-06` | MEDIUM | OD-01A Section 3 includes proposed `AirlineId` | OD-01A lines 108–110, 223–226 | Exclude or explicitly approve the allocation | Project Owner | M-12 | New authorization | Scope statement unambiguous | Cross-document review |
| `D-05` / `C-07` | MEDIUM | D-05 pending while Section 4 in scope | OD-01B lines 185–188, 397 | Add explicit no-values approval condition | Project Owner | `GOV-D-05` | `GOV-D-05` | Condition in approval block | Approval-block inspection |
| `D-06` / `C-08` | MEDIUM | Residual rows stale | OD-01A lines 217–219; OD-01B lines 373–375 | Update statuses to current per-finding results | Project Owner | Re-audit acceptance | New authorization | Rows match current statuses | Text comparison |
| `D-07` / `C-09` | MEDIUM | Contract draft used as governing baseline | Contract line 9; OD-01A/B line 15 | State contract is not approved; complete contract review | Project Owner | Contract review | Formal contract review | Decision records disclaim contract approval; contract status current | Cross-document review |
| `D-08` / `C-10` | MEDIUM | Ledger test summary wrong | Ledger line 13; contract test rows | Correct to 71 `PLANNED`, 8 `BLOCKED`, 0 `PASS` | Project Owner | H-05 | New authorization | Ledger matches contract | Test count |

### 17.6 Category E — Gate and signature

| ID | Severity | Root cause | Evidence location | Required correction | Owner | Dependency | Authorization | Acceptance criteria | Verification method |
|---|---|---|---|---|---|---|---|---|---|
| `E-01` / OD-01A | BLOCKER | Preconditions unmet | OD-01A §7 | Complete all preconditions; sign with actual date/evidence | Project Owner | A/B/C/D items | Owner signature | Signed record with actual date and evidence; residual row current | Signed copy and hash |
| `E-02` / OD-01B | BLOCKER | Preconditions unmet | OD-01B §11 | Complete all preconditions; sign after OD-01A | Project Owner | A/B/C/D items; OD-01A | Owner signature | Signed record with actual date and evidence; key-map trigger resolved | Signed copy and hash |
| `E-03` / G3 | GATE | Gate not executed | Ledger line 12; contract §15.2 | Hold gate review after signatures and criteria consolidation | Project Owner | OD-01A/B; G3 criteria | G3 gate decision | Gate record with entry/exit evidence | Gate review |
| `E-04` / G4 | GATE | G3 not approved | Ledger line 17; contract AC-21 | Keep blocked; require written G4 authorization | Project Owner | G3 approval | Written G4 authorization | Written authorization exists after G3 | Gate record |
| `E-05` / `G3-RV-01` | GATE | No reference version or manifest | Ledger line 16; OD-01B §7 | Execute after D-06/D-07 and reference data | Project Owner | D-06/D-07; signatures | Separate `G3-RV-01` authorization | Artifact with owner, version, hashes, source evidence, T-75/T-76/T-78, refresh config | Artifact and hash verification |

### 17.7 Required sequence

1. Owner reviews this report and the fresh re-audit; records accept, reject, or
   return for revision.
2. Owner authorizes one controlled documentation-correction package covering
   C-01 through C-10.
3. Owner decides `GOV-D-04`, `GOV-D-05`, and `GOV-D-08`.
4. Owner executes and records CC-01 self-review, acceptance of executed
   controls, and residual-risk acceptance.
5. Preparer applies the authorized corrections; re-audit the corrected package.
6. Sign OD-01A first, then OD-01B, using actual dates and evidence references.
7. Retain both signed copies read-only with hashes after `GOV-D-08` is
   implemented.
8. Decide `GOV-D-06` and `GOV-D-07`; prepare and execute `G3-RV-01`; create
   reference data only under separate authorization.
9. Hold the G3 gate review; only after G3 `APPROVED` may written G4
   authorization be considered.

### 17.8 Stop conditions

No signature, approval date, reviewer identity, reference CSV, manifest,
synthetic data, production code, Power Query, semantic model, DAX, Power BI
artifact, schema freeze, `G3-RV-01` execution, G3/G4 advancement, or Git write
operation is authorized by this report.

---

## 18. Final status, blockers, exact next action, files, and checks not possible

### 18.1 Required status summary

```text
PROJECT: AEROVISION 360 — governance investigation complete; no approval granted
Repository inspection: READ-ONLY — 31 pre-existing current documents plus root files hashed; no implementation artifacts; Git has 0 commits; only this report created
OD-01A: BLOCKED — NOT READY FOR SIGNATURE
OD-01B: BLOCKED — NOT READY FOR SIGNATURE
D-04: PENDING OWNER APPROVAL — owner-confirmation addendum not created; original still says contract v1.4 and OD-01A/B not prepared
D-05: PENDING OWNER APPROVAL — BusinessModelClass remains null/optional; no population authorized; approval condition missing
D-06: PENDING OWNER APPROVAL — proposed 365/180-day thresholds expressly not owner-approved
D-07: PENDING OWNER APPROVAL — ManifestHash canonicalization proposed only; not in contract
D-08: PENDING OWNER APPROVAL — evidence-retention structure absent; docs/approvals/ does not exist
G3: NOT STARTED — gate execution not held; design documentation PREPARED — DRAFT; formal approval NOT FORMALLY APPROVED; schema freeze NOT AUTHORIZED; G3-RV-01 NOT EXECUTED
G4: BLOCKED — G3 not approved; no written G4 authorization
Unauthorized modifications: NONE DETECTED — no existing file modified; no data/reference/Power BI/Git artifact created
```

### 18.2 Consolidated blockers

1. `GOV-D-04` pending; owner confirmation still cites contract v1.4 and says
   OD-01A/B are not prepared.
2. `GOV-D-05` pending; OD-01B Section 4 is in scope without a no-values
   approval condition.
3. `GOV-D-06` pending; source eligibility for `G3-RV-01` is undefined.
4. `GOV-D-07` pending; manifest hash reproducibility is undefined.
5. `GOV-D-08` pending; no signed-copy retention or hash register.
6. `B-xx` namespace collision unresolved; precondition 8 is ambiguous.
7. `D-xx` namespace collision unresolved; authorization citations are
   context-dependent.
8. Key-map approval gap between contract §7.1 and OD-01B §11.3.
9. OD-01A Section 3 proposed `AirlineId` allocation is inside the approval
   scope.
10. H-05 partially closed; G3 vocabulary not propagated, criteria not
    consolidated, ledger test summary wrong.
11. M-07 partially closed; owner self-review, control acceptance, residual-risk
    acceptance, and signed limitation missing.
12. B-04 partially closed; compensating-control initials/date and evidence
    reference missing.
13. Residual-concern rows in OD-01A and OD-01B are stale.
14. Contract v1.5 is not formally approved.
15. OD-01A and OD-01B are unsigned.
16. G3 is not started; G4 is blocked.

### 18.3 Exact next action

**Owner action:** review this report and
`OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md`, then record one of:

- `ACCEPT` the findings as the current evidence baseline;
- `REJECT` the findings with reasons;
- `RETURN FOR REVISION` with specific corrections.

Do not sign OD-01A or OD-01B.

If the report is accepted, the next controlled action is to authorize one
documentation-correction package covering C-01 through C-10 and `GOV-D-04`
through `GOV-D-08`. No data, reference, G3, or G4 work is authorized by that
acceptance.

### 18.4 Files created and modified

| Action | Path | Status |
|---|---|---|
| Created | `docs/AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md` | This report; sole new file |
| Modified | None | No existing file changed |
| Deleted | None | No file deleted |
| Renamed | None | No file renamed |
| Git write | None | No add, commit, branch, or tag |
| Data/reference artifact | None | No CSV, manifest, dataset, code, Power Query, DAX, or Power BI file |
| Approval artifact | None | No `docs/approvals/`, signed copy, or hash register |

### 18.5 Checks not possible

| Check | Why it was not possible | Consequence |
|---|---|---|
| Independent review | No named human reviewer exists; investigator is AI | No independent assurance |
| Source verification | No source records, archive, or external verification | Airline identity attributes remain unverified |
| Data/runtime validation | No reference data, synthetic data, code, model, or report | No test can be executed |
| Signed-copy verification | No signed copy or `docs/approvals/` | No signature or retention evidence |
| Hash-register verification | No hash register or verification log | Approval reconstruction not possible |
| `G3-RV-01` verification | No reference version, manifest, or gate artifact | Reference approval not possible |
| Power BI runtime validation | No semantic model or report | No refresh, relationship, DAX, or disclosure runtime evidence |
| Git history verification | Zero commits | No committed change history to audit |
| Contract formal approval | Contract v1.5 is a draft | Governing baseline is not formally approved |
| Owner intent beyond documents | Only documents were inspected | Cannot confirm undocumented intent |
| Line-by-line implementation walkthrough | No implementation exists | No code-level assurance |

### 18.6 Report verification

| Check | Result |
|---|---|
| File exists at the required path | `docs/AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md` |
| Encoding | UTF-8 without BOM |
| Line endings | LF-only |
| Signature / approval date / reviewer identity | None entered |
| Existing controlling document modified | None |
| Additional approval record created | None |
| Reference / synthetic / production / Power BI artifact created | None |
| Git write performed | None |
| Hash | Recorded in the final response because a file cannot contain its own hash self-reference |

No independent assurance, external verification, certification, or runtime
validation is claimed.

---

## Appendix A — Source map

| Topic | Primary source |
|---|---|
| Scope, roster, period, disclosure | `docs/01_PROJECT_SCOPE.md` |
| Business requirements | `docs/02_BUSINESS_REQUIREMENTS.md` |
| Contract rules, tests, decisions | `docs/03_DATA_CONTRACTS.md` |
| OD-01A population decision | `docs/OD01A_AIRLINE_POPULATION_DECISION.md` |
| OD-01B identity/reference decision | `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` |
| G3/G4 status | `docs/PROGRESS_LEDGER.md` |
| H-04 risk register | `docs/PROJECT_RISK_REGISTER.md` |
| D-01–D-10 definitions | `docs/OD01_OWNER_DECISION_PACKET.md` |
| Original H/M findings | `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` |
| B-03/B-04/B-05 governance definitions | `docs/OD01_GOVERNANCE_CLOSURE_PROPOSAL.md` |
| B-03–B-08 and CC controls | `docs/OD01_COMPENSATING_CONTROL_AND_REMEDIATION_PROPOSAL.md` |
| D-03/D-09/D-10 authorization | `docs/OD01_REVISION_0.2_CHANGE_RECORD.md` |
| Latest re-audit and C-01–C-10 | `docs/OD01_REVISION_0.2_FRESH_GOVERNANCE_REAUDIT.md` |
| Local D-01–D-18 definitions | `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` |
| Contract v1.4 → v1.5 evidence | `docs/OD01_REMEDIATION_CHANGE_RECORD.md` |
| Owner-confirmed choices and stale statements | `docs/OD01_OWNER_DECISION_CONFIRMATION.md` |
| Pre-confirmation decision basis | `docs/OD01_OWNER_DECISION_RESOLUTION.md` |
| Historical migration evidence | `docs/OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt` |
| Superseded draft | `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md` |

---

**End of report.**
