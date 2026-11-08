# AEROVISION 360 — OD-01 Remediation Change Record

**Document type:** Controlled change record  
**Change ID:** OD-01-REM-001  
**Change title:** OD-01 contract remediation to version 1.5  
**Record version:** 1.0  
**Status:** CONTROLLED CHANGE RECORD — PENDING REVIEW  
**Prepared:** 2026-11-01  
**Project owner / approver:** KH Mohammad Farhan  
**Governing contract:** `03_DATA_CONTRACTS.md` version 1.5  
**Related decisions:** `OD01A_AIRLINE_POPULATION_DECISION.md`, `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`

> **STATUS NOTICE**
>
> This change record documents a controlled documentation remediation. It is not
> a formal approval, signature, schema freeze, gate review, data authorization,
> or release claim. OD-01A and OD-01B remain
> `OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING`. G3 remains
> `NOT STARTED`; G4 remains `BLOCKED`. No reference CSV, synthetic dataset,
> Python pipeline, Power Query query, semantic model, DAX measure, Power BI
> report, dashboard, or Git operation was created by this change set.

## 1. Authority and scope

The owner authorized a controlled remediation of the OD-01 decision package:

**Existing documents authorized for modification:**

1. `docs/03_DATA_CONTRACTS.md`
2. `docs/02_BUSINESS_REQUIREMENTS.md`
3. `docs/REQUIREMENTS_TRACEABILITY.md`
4. `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt`
5. `docs/PROGRESS_LEDGER.md`

**New documents authorized for creation:**

1. `docs/OD01A_AIRLINE_POPULATION_DECISION.md`
2. `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`
3. `docs/OD01_REMEDIATION_CHANGE_RECORD.md`

The following documents were not modified:

- `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md`
- `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md`
- `docs/OD01_OWNER_DECISION_RESOLUTION.md`
- `docs/OD01_OWNER_DECISION_CONFIRMATION.md`
- `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md`
- `docs/01_PROJECT_SCOPE.md`

`01_PROJECT_SCOPE.md` was outside the authorized edit set. Its high-level
present-tense “source-verified” and “region/business-model” wording is a
disclosed residual, not a silent change. No claim of complete scope alignment is
made.

## 2. Mandatory source hashes verified before editing

All values were verified with SHA-256 before any authorized file was modified.

| Source | SHA-256 | Result |
|---|---|---|
| `docs/OD01_OWNER_DECISION_RESOLUTION.md` | `BE62CBDC017073F6D9135D7DEEF3993F64D74D881102A5C867134C889E20A220` | MATCH |
| `docs/OD01_OWNER_DECISION_CONFIRMATION.md` | `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD` | MATCH |
| `docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md` | `CC3BCE621142C31B4BB7A46F4CBCB320E640466228184AE2E94E196796F3F8A4` | MATCH |
| `docs/OD01_FORMAL_DECISION_RECORD_DRAFT.md` | `C594DFCD8FE1B6809E28CBE1B3EE6D24FAA0772D35DD1FE57767FECCD3CA2A60` | MATCH |
| `docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md` | `FD94BD369D3DDDC1AF84C040C27014F112E74B4B0F938CE95B617C7B142BECE6` | MATCH |
| `docs/03_DATA_CONTRACTS.md` | `EB1DE0E1B80E9E30B4905740BDD66AB96657073119D63C49AA48445CB06446E2` | MATCH |
| `docs/PROGRESS_LEDGER.md` | `42A00E3A41A9ABBC6B9F930BFE39DD369E6B9681B9F56194921E7145E6F8A7A3` | MATCH |

**Baseline hashes verified before editing:**

| Source | SHA-256 |
|---|---|
| `docs/01_PROJECT_SCOPE.md` | `3238D7199F10F5E4E8BF7193D27825A2EE13FD571CCDE9B44DC3CE123FBD72B9` |
| `docs/02_BUSINESS_REQUIREMENTS.md` | `E2FCC8132981C96720E572F01EF353C255CA6BE91F27854950D93FF0DFC1DB6E` |
| `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt` | `17BD2C6FCADB9E2A917D047B2B2D9716E21CB1709B5A46ABF01AB2833C56D429` |
| `docs/REQUIREMENTS_TRACEABILITY.md` | `1AD225D00EA6D5808B6E0050DBFCE10F84CBAEF2B66DE70C4362370BBA9CC751` |

## 3. Backup

**Backup directory:** `docs/od01_remediation_backup_20261101_221748`

| File | Original SHA-256 | Preserved |
|---|---|---|
| `03_DATA_CONTRACTS.md` | `EB1DE0E1B80E9E30B4905740BDD66AB96657073119D63C49AA48445CB06446E2` | Yes |
| `02_BUSINESS_REQUIREMENTS.md` | `E2FCC8132981C96720E572F01EF353C255CA6BE91F27854950D93FF0DFC1DB6E` | Yes |
| `REQUIREMENTS_TRACEABILITY.md` | `1AD225D00EA6D5808B6E0050DBFCE10F84CBAEF2B66DE70C4362370BBA9CC751` | Yes |
| `AEROVISION_360_MASTER_BUILD_PROMPT.txt` | `17BD2C6FCADB9E2A917D047B2B2D9716E21CB1709B5A46ABF01AB2833C56D429` | Yes |
| `PROGRESS_LEDGER.md` | `42A00E3A41A9ABBC6B9F930BFE39DD369E6B9681B9F56194921E7145E6F8A7A3` | Yes |

The backup contains the pre-write versions only. The three new destinations were
confirmed absent before creation; no existing destination was overwritten.

## 4. Files changed and created

| File | Change | Original SHA-256 | New SHA-256 | New bytes |
|---|---|---|---|---|
| `docs/03_DATA_CONTRACTS.md` | Contract v1.4 to v1.5; substantive identity, reference, provenance, lifecycle, Power BI, test, decision and status changes | `EB1DE0E1B80E9E30B4905740BDD66AB96657073119D63C49AA48445CB06446E2` | `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9` | 211,846 |
| `docs/02_BUSINESS_REQUIREMENTS.md` | Version 1.1; BR-01, BR-09, BR-10 and BR-15 aligned; exact disclosure and reference-version evidence added | `E2FCC8132981C96720E572F01EF353C255CA6BE91F27854950D93FF0DFC1DB6E` | `F5B3140A91C868692A37609F904129BD166861045A9D00C9840815B0CCC4E709` | 5,921 |
| `docs/REQUIREMENTS_TRACEABILITY.md` | REQ-001, REQ-004, REQ-006, REQ-023 to REQ-027 reconciled; REQ-028 added; all statuses remain NOT STARTED | `1AD225D00EA6D5808B6E0050DBFCE10F84CBAEF2B66DE70C4362370BBA9CC751` | `4EE19E921BDC3067D17E172422D85D76B2660EF478EF4AB385D816BA4C314DEB` | 5,742 |
| `docs/AEROVISION_360_MASTER_BUILD_PROMPT.txt` | Version 1.1; identity, key, reference-version, relationship, gate and disclosure rules aligned | `17BD2C6FCADB9E2A917D047B2B2D9716E21CB1709B5A46ABF01AB2833C56D429` | `000E9613C56039A8A95F667AF571C63D4841FF69EE04B8ACDCDD6B8FE8429122` | 20,426 |
| `docs/PROGRESS_LEDGER.md` | Contract v1.5 and OD-01A/OD-01B statuses recorded; G3 remains NOT STARTED; G4 remains BLOCKED; implementation artifacts recorded as not created | `42A00E3A41A9ABBC6B9F930BFE39DD369E6B9681B9F56194921E7145E6F8A7A3` | `C6297622D8CFE5BD90402BBB034B1091C70BAA2895BF0438F4E94C003E343C1F` | 4,076 |
| `docs/OD01A_AIRLINE_POPULATION_DECISION.md` | New population decision record; owner-confirmed design; formal signature and approval pending | Absent | `399241AD2AE21F4A1FB3D7E589950117F9CDADB8303F78CC161F484CD7255A06` | 11,487 |
| `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | New identity/reference decision record; owner-confirmed design; formal signature and approval pending | Absent | `CDD48B9F0B68CE401D827E5F910076104CCCE73FFBF7BA0A6BC21D75D07C3C05` | 20,782 |
| `docs/OD01_REMEDIATION_CHANGE_RECORD.md` | This change record | Absent | Computed after creation; reported in the final response to avoid a self-referential hash | — |

**Line-ending and encoding normalization:** the five modified legacy files were
written as UTF-8 without BOM and LF line endings. Some original files used
BOM/CRLF or mixed line endings; the master prompt was already LF without BOM.
The backup preserves the original bytes. The two new decision records and this
change record use UTF-8 without BOM and LF.

## 5. Contract v1.5 substantive changes

The contract was not version-bumped only. The following content was reconciled:

1. **Identity separation.** `AirlineId` is the durable business identity;
   `AirlineKey` is the permanent positive `Int32` warehouse surrogate. IATA,
   ICAO and name are mutable, version-qualified attributes, not keys.
2. **Reference schema.** `ref_airlines.csv` uses `AirlineId` plus
   `ReferenceVersion` as its primary key. `ref_airline_sources.csv` records
   attribute-level provenance joined on `AirlineId`.
3. **Attribute semantics.** `AirlineName` is the commercial brand; `LegalName`
   is optional and reference-only; `HomeCountry` is headquarters/domicile;
   `AirlineGroup` is the optional ultimate parent or group brand.
4. **Analytical classification.** `BusinessModelClass` is optional, nullable and
   analytical. `OperatingRegion` is removed from airline identity; analytical
   region is derived from route and airport geography.
5. **Lifecycle.** `IsActive` and `StatusEffectiveDate` are the minimal lifecycle.
   `LifecycleStatus` and `MergedIntoAirlineId` are deferred.
6. **Historical semantics.** `DimAirline` is Type 1 with immutable reference
   snapshots. Build reproducibility is preserved; as-was historical identity
   labels are not. Type 2 is deferred.
7. **Reference authority.** The reference manifest is the authoritative approval
   record. `DimAirline.ReferenceVersion` is hidden technical lineage only. Every
   generation and refresh pins exactly one approved version.
8. **Key integrity.** The airline key map is controlled and immutable after
   approval. The same `AirlineId` always resolves to the same `AirlineKey`; no
   row order, hash order, random selection, database identity or rebuild
   sequence may assign it. Facts are never re-keyed.
9. **Gate artifact.** Reference-version approval uses `G3-RV-01`, not an
   OD-series decision. OD-23 is rejected and is not created. REQ-028 and T-78 are
   retained.
10. **Provenance controls.** The source hierarchy, controlled values, conflict
    and quarantine rules, evidence durability, staleness policy and supersession
    are documented.
11. **Power BI controls.** `DimAirline` joins facts on `AirlineKey`; there is no
    second active `DimAirline` path through `DimAircraft`; `SelectedReferenceVersion`
    is validated; `AirlineKey` and `ReferenceVersion` are hidden.
12. **Disclosure.** Every report page, tooltip while visible and exported result
    must carry the exact unconditional string
    `Synthetic Simulation — Not Actual Airline Performance`. T-79 verifies it.
13. **Decisions.** OD-01 is split into OD-01A and OD-01B. Both are
    owner-confirmed designs with formal signature and approval pending. The
    remaining critical decisions are still open.
14. **Acceptance and status.** AC-23 and AC-24 were added. The document remains
    pending review and formal approval; G3 is NOT STARTED and G4 is BLOCKED.

## 6. OD-01A and OD-01B summary

**OD-01A — Airline population:**

- Fixes the ten-airline intended population.
- Defines inclusion and exclusion criteria.
- Separates real identity attributes from synthetic operational and financial
  data.
- Records evidence requirements and the shared evidence index.
- Leaves the formal owner signature and approval date blank.

**OD-01B — Airline identity and reference model:**

- Defines the `AirlineId`/`AirlineKey` hierarchy and proposed 1:1 allocation.
- Defines the `DimAirline` attribute dictionary and reference datasets.
- Defines source provenance, conflict/quarantine handling, lifecycle and Type 1
  historical semantics.
- Defines the reference manifest, key-map controls, T-78 sub-checks and
  `G3-RV-01`.
- Defines Power BI relationship and disclosure rules.
- Leaves the formal owner signature, reviewer assignment and approval date blank.

Both records carry the exact status
`OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING`.

## 7. Requirements and tests impact

| Item | Change | Status |
|---|---|---|
| REQ-001 | Clarified real identity plus source verification before reference approval; added reference-version and disclosure evidence | NOT STARTED |
| REQ-004 | Added stable `AirlineId`/`AirlineKey` mapping and one selected `ReferenceVersion` | NOT STARTED |
| REQ-006 | Added `AirlineKey` relationship, hidden lineage and no ambiguous airline filter path | NOT STARTED |
| REQ-023 | Reconciled to `AirlineId`; OD-01A remains pending | NOT STARTED |
| REQ-024 | Reconciled to durable `AirlineId`, permanent `AirlineKey`, version-qualified IATA/ICAO | NOT STARTED |
| REQ-025 | Added evidence durability and provenance controls | NOT STARTED |
| REQ-026 | Clarified nullable optional attributes and analytical `BusinessModelClass` | NOT STARTED |
| REQ-027 | Added `AirlineKey` and `ReferenceVersion` to reconciliation | NOT STARTED |
| REQ-028 | Added reference-version, manifest, refresh and key integrity; `G3-RV-01`, not OD-23 | NOT STARTED |
| T-72 to T-77 | Reconciled to `AirlineId`, version-qualified attributes and key mapping | PLANNED |
| T-78 | Added ten reference-version, manifest, refresh and key-integrity sub-checks | PLANNED |
| T-79 | Added exact disclosure and rendered-output integrity test | BLOCKED |

**ID integrity:** 28 unique requirement IDs and 79 unique test IDs were found.
No requirement or test ID was removed, renumbered or duplicated. No test was
executed; no test result was invented. T-79 is BLOCKED because no rendered
Power BI report exists.

## 8. Cross-document consistency results

| Check | Result | Evidence |
|---|---|---|
| Ten airline names, IATA, ICAO, home countries and country codes match across the contract, master prompt, OD-01A and OD-01B | PASS | Roster comparison |
| Authorized documents use `AirlineId`, permanent `AirlineKey`, version-qualified IATA/ICAO and no standalone code key | PASS | Contract, BR, traceability, master prompt, OD-01A/OD-01B |
| `LegalName` is reference-only; `OperatingRegion` is not an identity field; `BusinessModelClass` is optional analytical | PASS | Contract Sections 2, 3.4, 4.3 and 6.2.2; OD-01B |
| Type 1, immutable snapshots, Type 2 deferral, `IsActive` and `StatusEffectiveDate` are consistently stated | PASS | Contract Sections 3.4, 4.3 and 6.2.2; OD-01B |
| Reference manifest authority, one selected version, hidden lineage and `G3-RV-01` are consistently stated | PASS | Contract Sections 3.4, 7, 8.4 and 13; OD-01B; master prompt |
| OD-23 is rejected and not created; REQ-028 and T-78 are retained | PASS | Contract Section 14; traceability; OD-01B; master prompt |
| Exact disclosure is present in every disclosure-bearing normative document | PASS | Unicode codepoint check; zero ASCII-hyphen variants |
| `01_PROJECT_SCOPE.md` remains unchanged and its high-level wording residual is disclosed | PASS WITH DISCLOSED RESIDUAL | Scope hash unchanged; Section 1 of this record |
| Audit, specification, resolution, confirmation and original draft remain unchanged | PASS | SHA-256 comparison |
| No reference CSV, synthetic dataset, Python, Power Query, Power BI, DAX or dashboard artifact was created | PASS | Directory inspection |

## 9. QA checks 1 to 24

These are document-level checks. Execution-dependent checks are separately
reported as BLOCKED in Section 10; a document check does not substitute for a
data or runtime test.

| # | Check | Result |
|---:|---|---|
| 1 | Mandatory source hashes verified before editing | PASS |
| 2 | Only the five authorized existing files were modified | PASS |
| 3 | The three new destinations were absent before creation | PASS |
| 4 | Timestamped backup exists with original hashes | PASS |
| 5 | Contract version 1.5 contains substantive changes, not a version-only bump | PASS |
| 6 | `AirlineId` and `AirlineKey` responsibilities are separated | PASS |
| 7 | IATA and ICAO are version-qualified attributes, not keys | PASS |
| 8 | `LegalName` is reference-only and absent from `DimAirline` | PASS |
| 9 | `HomeCountry` and `AirlineGroup` semantics are defined | PASS |
| 10 | `BusinessModelClass` is optional analytical; `OperatingRegion` is removed from identity | PASS |
| 11 | `IsActive` and `StatusEffectiveDate` are defined; deferred lifecycle fields are excluded | PASS |
| 12 | Type 1 and immutable snapshot limitations are explicit; Type 2 is deferred | PASS |
| 13 | Manifest authority, one selected version and technical lineage are defined | PASS |
| 14 | Key mapping is stable and independent of row order and database identity | PASS |
| 15 | `G3-RV-01` is used and OD-23 is rejected | PASS |
| 16 | Provenance, source hierarchy, conflict, quarantine and evidence durability are documented | PASS |
| 17 | REQ-028, T-78 and T-79 are present with unique IDs | PASS |
| 18 | OD-01A and OD-01B carry the exact owner-confirmed/pending status and blank signatures | PASS |
| 19 | All ten airline identities match across authorized documents | PASS |
| 20 | The exact canonical disclosure is present in all disclosure-bearing normative documents | PASS |
| 21 | No reference data, synthetic data, Python, Power Query, Power BI, DAX or dashboard was created | PASS |
| 22 | G3 remains NOT STARTED; G4 remains BLOCKED; schema freeze remains unauthorized | PASS |
| 23 | No signature, approval date, reviewer identity or external verification was invented | PASS |
| 24 | UTF-8 without BOM, LF line endings, valid tables and no duplicate IDs | PASS |

**QA result:** 24 of 24 document-level checks PASS. No document-level FAIL was
found. Execution-dependent checks are BLOCKED, not PASS.

## 10. Execution and gate results

| Check | Result | Reason |
|---|---|---|
| T-72 to T-78 execution | BLOCKED | No reference CSV, source records, manifest, generated dataset or model exists |
| T-79 execution | BLOCKED | No rendered Power BI report or export exists |
| `G3-RV-01` | BLOCKED | Reference version, manifest, source evidence and test results do not exist |
| G3 gate | NOT STARTED | Formal OD-01A/OD-01B approvals, remaining critical decisions, schema freeze, validation implementation and gate review are outstanding |
| G4 gate | BLOCKED | G3 has not passed and no written G4 authorization exists |
| Formal OD-01A approval | PENDING | Signature and approval date are blank |
| Formal OD-01B approval | PENDING | Signature, reviewer assignment and approval date are blank |
| Independent review | BLOCKED | No reviewer is assigned; no independent assurance exists |

## 11. Remaining approvals and authorizations

| Item | Current state | Required next action |
|---|---|---|
| OD-01A population decision | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING | Owner signature and approval date |
| OD-01B identity/reference decision | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING | Owner signature, reviewer control and approval date |
| OD-02 to OD-22 and OP-01 | PENDING or PROPOSED as recorded in contract Section 14 | Complete formal decision records |
| `G3-RV-01` | NOT EXECUTED | Approve exact reference version, manifest, source evidence, T-75/T-76 results, T-78 plan and refresh configuration |
| Schema freeze | NOT AUTHORIZED | Review and freeze after decisions and reference-version approval |
| Reference-data creation | NOT AUTHORIZED | Explicit authorization after OD-01A/OD-01B, `G3-RV-01` and schema freeze |
| Synthetic-data generation | NOT AUTHORIZED | G3 APPROVED and written G4 authorization |
| Power BI implementation | NOT AUTHORIZED | G4 and explicit Power BI authorization |
| Independent reviewer | NOT ASSIGNED | Assign a reviewer or document an owner-accepted compensating control; do not claim independence |

## 12. Work not performed

- No reference CSV or reference manifest was created.
- No source URL, source organization, verification date or evidence hash was
  invented.
- No synthetic dataset, generator, seed run or validation result was created.
- No Python code, Power Query query, semantic model, DAX measure, Power BI
  report, dashboard or screenshot was created.
- No schema freeze, data dictionary, G3 review or G4 authorization was
  performed.
- No signature, approval date, reviewer identity or external verification was
  recorded.
- No Git operation was performed.
- No file outside the authorized set was modified.
- No claim of actual airline performance, source verification completion,
  independent assurance or release readiness is made.

## 13. Current gate status and next step

**G3:** `NOT STARTED`  
**G4:** `BLOCKED`  
**OD-01A:** `OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING`  
**OD-01B:** `OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING`  
**Schema freeze:** `NOT AUTHORIZED`  
**Reference data:** `NOT AUTHORIZED`  
**Synthetic data:** `NOT AUTHORIZED`  
**Power BI:** `NOT AUTHORIZED`

**Next gate:** obtain the owner's formal signatures and approval dates for
OD-01A and OD-01B, complete the remaining critical decisions, then execute
`G3-RV-01` and the remaining G3 entry criteria. Stop after this remediation; do
not start reference-data generation, synthetic-data generation, schema freeze,
G3, or G4 automatically.

## 14. Change record approval

| Role | Name | Decision | Signature | Date |
|---|---|---|---|---|
| Project owner / approver | KH Mohammad Farhan |  |  |  |
| Independent reviewer | Not assigned |  |  |  |
| Data architecture reviewer |  |  |  |  |

**Approval status:** PENDING REVIEW. This change record is not a formal approval
of OD-01, OD-01A, OD-01B, the contract, the schema, any reference version, or any
gate. It records the change set and the work that remains.
