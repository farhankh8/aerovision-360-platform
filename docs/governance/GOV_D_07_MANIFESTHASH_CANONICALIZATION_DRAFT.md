# GOV-D-07 — ManifestHash Canonicalization Decision

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** GOV-D-07-2026-11-06-001  
**Document Type:** Owner Decision Draft — ManifestHash Canonicalization Approval  
**Status:** REVISED DRAFT — OWNER REVIEW REQUIRED  
**Prepared:** 2026-11-06  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Revision Basis:** Owner Option B — Approve with technical revisions  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Decision Purpose

This decision record establishes a canonical JSON serialization and SHA-256 hashing procedure for reference manifest files. The manifest hash field (`ManifestHash`) defined in `data/manifests/reference_versions.csv` must be reproducible: given the same manifest content, any compliant implementation must produce the same hash value. Without a canonicalization rule, different serializations of the same logical manifest could produce different hash values, breaking reproducibility and auditability.

The manifest hash is used by QA test `T-78` (Classification reference-version and manifest integrity) to verify that the reference manifest used to generate a fact table matches the manifest used by Power BI at refresh time. Without a canonical serialization, hash values cannot be independently reproduced, and `G3-RV-01` (reference-version approval) cannot record a defensible manifest hash.

This decision record is a **documentation and technical-analysis artifact only**. It does not create reference data, does not modify any source file, and does not authorize any implementation.

---

## 2. Problem Statement

Contract v1.5 (`docs/03_DATA_CONTRACTS.md`), Section 9.4 (line 264), names `ManifestHash` as a field of the reference manifest register (`data/manifests/reference_versions.csv`) but does **not** define how the hash is computed. Specifically:

- No canonical JSON serialization method is specified.
- No field inclusion/exclusion rules are defined.
- No encoding, line-ending, whitespace, or key-ordering rules are defined.
- No SHA-256 hash casing or output format is defined.
- No test vector is provided for independent verification.

Finding A-04 / GOV-D-07 is classified as **HIGH severity, P0** (must resolve before OD-01A/OD-01B signature) in both `CC01_REMEDIATION_REGISTER_V2.md` and `CC01_REMEDIATION_PRIORITY_MATRIX.md`. Its acceptance criteria require: method recorded, reproducible test vector matches, and T-78 can recompute.

---

## 3. Existing Evidence (Phase 1 Inspection)

### 3.1 Governance Documents Inspected

| File | Location | Relevance to GOV-D-07 | Status |
|---|---|---|---|
| CC-01 Remediation Register — Revised | `docs/governance/CC01_REMEDIATION_REGISTER_V2.md` | Lists A-04 / GOV-D-07 as HIGH, P0; acceptance criteria: method recorded, test vector matches, T-78 recompute | Exists |
| CC-01 Remediation Priority Matrix | `docs/governance/CC01_REMEDIATION_PRIORITY_MATRIX.md` | Lists A-04 / GOV-D-07: ManifestHash canonicalization undefined | Exists |
| CC-01 Findings Remediation Plan | `docs/governance/CC01_FINDINGS_REMEDIATION_PLAN.md` | Line 35: A-04 / GOV-D-07, dependency G3-RV-01; T-78; authorization GOV-D-07 | Exists |
| CC-01 Remediation Plan Reconciliation | `docs/governance/CC01_REMEDIATION_PLAN_RECONCILIATION.md` | Corrects P0 count from 9 to 11 (includes A-04 / GOV-D-07) | Exists |
| CC-01 Owner Self-Review | `docs/governance/CC01_OWNER_SELF_REVIEW.md` | GOV-D-07 listed as pending owner decision | Exists |
| CC-01 Owner Self-Review Findings | `docs/governance/CC01_OWNER_SELF_REVIEW_FINDINGS.md` | GOV-D-07 HIGH severity | Exists |
| OD-01 Pre-Signature Readiness Audit | `docs/governance/OD_01_PRESIGNATURE_READINESS_AUDIT.md` | OD-01A/OD-01B not ready; GOV-D-07 pending | Exists |
| AEROVISION 360 Governance Investigation Report | `docs/AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md` | §7.4: GOV-D-07 PENDING OWNER APPROVAL; details exact question, source, dependencies | Exists |
| OD-01 Owner-Confirmation Addendum Acceptance | `docs/governance/OD01_OWNER_CONFIRMATION_ADDENDUM_ACCEPTANCE.md` | Addendum accepted by owner 2026-11-06; does not cover GOV-D-07 | Exists |
| GOV-D-06 Staleness Threshold Decision Draft | `docs/governance/GOV_D_06_STALENESS_THRESHOLD_DECISION_DRAFT.md` | Separate decision (365/180 days); not part of GOV-D-07 | Exists |

**NOT FOUND:** `docs/governance/GOV_D_06_OWNER_ACCEPTANCE.md` — no formal acceptance record for GOV-D-06 exists yet.

### 3.2 Contract Evidence Inspected

| File | Line(s) | Content |
|---|---|---|
| `docs/03_DATA_CONTRACTs.md` (v1.5 DRAFT) | 259-260 | SHA-256 `EvidenceHash` required for VERIFIED records; staleness thresholds are proposed policy, not owner-approved |
| `docs/03_DATA_CONTRACTs.md` (v1.5 DRAFT) | 264 | Reference manifest register `data/manifests/reference_versions.csv` records `ManifestHash` among fields; `ApprovedBy` and `ApprovalDate` blank until real approval |
| `docs/03_DATA_CONTRACTs.md` (v1.5 DRAFT) | 265 | Reference-version approval uses gate artifact `G3-RV-01`, not an OD-series decision |
| `docs/03_DATA_CONTRACTs.md` (v1.5 DRAFT) | 266 | Airline key mapping: immutable after approval; never derived from CSV row order |

**NOT MODIFIED:** `docs/03_DATA_CONTRACTs.md` was read only and not modified.

### 3.3 Manifest Files Inspected

| File | Location | Notes |
|---|---|---|
| Per-dataset manifests (15 files) | `data/manifests/*.json` | dim_airline_manifest.json, dim_aircraft_manifest.json, fact_flight_operations_manifest.json, etc. Each contains SHA-256 hashes for source and output files |
| Reference version register | `data/manifests/reference_versions.csv` | **DOES NOT EXIST** — confirmed by investigation report line 1060 |
| Airline identifier crosswalk manifest | `data/manifests/airline_id_crosswalk_manifest.json` | Exists; contains `audit_report_sha256`, `airline_reference_workbook_sha256`, `crosswalk_csv_sha256` |

### 3.4 Hashing Utilities Inspected

| File | Location | Content | Compatibility with RFC 8785 |
|---|---|---|---|
| SHA-256 utility module | `src/utilities/hashing.py` | `sha256_bytes()`, `sha256_stream()`, `sha256_file()` — SHA-256 over bytes/streams/files | Compatible: JCS produces deterministic bytes that can be passed to `sha256_bytes()` |
| SHA-256 unit tests | `tests/unit/test_hashing.py` | Tests `sha256_bytes(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"` | Compatible: tests SHA-256 primitive, not JCS |
| Quality manifest module | `src/quality/manifest.py` | `QualityManifest` class; persists quality run manifests; `verify_checksums()` checks `source_sha256` | Compatible: stores and verifies SHA-256 digests |

### 3.5 QA Test Evidence

| Test ID | File Reference | Status | Relevance |
|---|---|---|---|
| T-78 | `docs/03_DATA_CONTRACTs.md` line 1670 | PLANNED/BLOCKED | Classification reference-version and manifest integrity; compares versions with manifests |
| T-79 | `docs/03_DATA_CONTRACTs.md` line 1680 | BLOCKED | Synthetic disclosure integrity |

**NOT FOUND:** No existing RFC 8785 implementation, no existing manifest-hash computation script, no existing test vector for manifest hash reproducibility.

---

## 4. Proposed Canonicalization Standard (RFC 8785 JCS)

### 4.1 Standard Selection

The proposed canonicalization standard is **RFC 8785 — JSON Canonicalization Scheme (JCS)**. JCS is an IETF-standardized deterministic JSON serialization scheme designed specifically for applications requiring stable hashes across independent implementations. It replaces the previous custom serialization rules with a single, externally specified standard.

### 4.2 RFC 8785 Requirements Documented

| Requirement | RFC 8785 Rule |
|---|---|
| Character encoding | UTF-8 |
| Byte-order mark | None (no BOM) |
| Object-property ordering | Deterministic: lexicographic comparison of UTF-16 code units (RFC 8785 Section 3.2.3) |
| Number serialization | Deterministic per I-JSON (RFC 7493) / IEEE 754 binary64; integers without leading zeros or trailing zeros after decimal; exponents use lowercase `e`; no unnecessary leading/trailing zeros; values exceeding binary64 precision must be represented as strings or rejected |
| String escaping | Deterministic per RFC 8259 with specific escaping rules for control characters and non-ASCII |
| Array order | Preserved as written in source; arrays are ordered collections |
| Duplicate JSON object keys | Rejected: input with duplicate keys is non-canonical and must be rejected |
| Non-I-JSON input | Rejected: input not conforming to RFC 7493 (I-JSON) must be rejected |
| Additional whitespace | None in canonical output: no insignificant whitespace |
| Top-level value | Must be a JSON object (for manifest use) |

### 4.3 Unicode Normalization

RFC 8785 **does not** perform Unicode Normalization Form C (NFC) or any other Unicode normalization. String values are serialized as-is after I-JSON string escaping. Whether Unicode normalization is required as a separate input-validation step is an **open owner decision**:

- **Option 1 (preserve exact):** No Unicode normalization. String values are preserved exactly as provided, subject only to RFC 8785 escaping. Risk: different byte sequences for canonically equivalent Unicode strings (e.g., precomposed vs. decomposed accented characters) produce different hashes.
- **Option 2 (normalize on input):** Apply NFC normalization to all string values before RFC 8785 serialization. Risk: alters original string values; must be documented as input validation.

**Recommendation:** Option 1 (preserve exact string values, no NFC normalization) unless evidence demonstrates a requirement for normalization. This avoids silently modifying source data and follows RFC 8785 as specified.

### 4.4 What RFC 8785 Does Not Cover (Separate Owner Decisions)

| Area | RFC 8785 Coverage | Owner Decision Required |
|---|---|---|
| Unicode normalization | Not covered | Yes — see Section 4.3 |
| Field inclusion/exclusion | Not covered | Yes — see Section 5.3 |
| `ManifestHash` self-exclusion | Not covered | Yes — see Section 5 |
| Timestamp format | Not covered (strings only) | Yes — JCS preserves strings exactly as supplied; it does not auto-convert timestamp strings or timezone offsets to UTC. UTC ISO 8601 (`YYYY-MM-DDThh:mm:ssZ`) must be enforced through separate input validation before canonicalization. |
| Hash algorithm | Not covered | Yes — SHA-256 recommended |
| Hash output casing | Not covered | Yes — lowercase hexadecimal recommended |

---

## 5. ManifestHash Self-Exclusion

### 5.1 Recommended Rule

The `ManifestHash` property must not participate in its own hash calculation. The recommended procedure is:

1. **Parse** the manifest as JSON.
2. **Validate** its structure (reject duplicate keys; reject non-I-JSON input).
3. **Remove** the `ManifestHash` property entirely from the hash input object. If `ManifestHash` is present, it is stripped before canonicalization.
4. **Canonicalize** the remaining JSON object using RFC 8785 JCS.
5. **Encode** the canonical JSON as UTF-8 bytes.
6. **Calculate** SHA-256 over the resulting UTF-8 byte sequence.
7. **Store** the digest as a 64-character lowercase hexadecimal string in the `ManifestHash` field.

```
ManifestHash = SHA-256( UTF-8( RFC8785( manifest_object_without_ManifestHash ) ) )
```

**Pipeline distinction:** These are three separate and sequential steps:
1. **JSON canonicalization** — RFC 8785 JCS serializes the manifest object (minus `ManifestHash`) into a canonical character sequence with deterministic property ordering, number serialization, and string escaping.
2. **UTF-8 encoding** — The canonical character sequence is encoded as UTF-8 bytes (no BOM).
3. **SHA-256 hashing** — SHA-256 is computed over the exact UTF-8 byte sequence, producing a 64-character lowercase hexadecimal digest.

RFC 8785 governs step 1 only. UTF-8 encoding (step 2) and SHA-256 hashing (step 3) are applied to the output of step 1.

### 5.2 Behavior for ManifestHash Edge Cases

| ManifestHash State | Handling | Result |
|---|---|---|
| Absent (property not present) | Nothing to remove; canonicalize all remaining properties | Hash computed over all properties |
| Explicit `null` | Property removed before canonicalization; `null` does not contribute to hash | Hash computed over remaining properties |
| Empty string `""` | Property removed before canonicalization; empty string does not contribute | Hash computed over remaining properties |
| Malformed value | Property removed before canonicalization; value does not contribute | Hash computed over remaining properties |
| Present with valid hash | Property removed before canonicalization; existing hash value does not contribute | Hash recomputed over remaining properties; may differ from stored value |

**Key principle:** Whatever value `ManifestHash` holds (absent, null, empty, or a previous hash), it is removed from the hash input before canonicalization. The stored hash is always computed over the manifest minus the `ManifestHash` property itself.

---

## 6. Retroactive Application (Migration Policy)

### 6.1 Recommended Policy

- **Do not silently rewrite existing manifests.** Historical source files and evidence are preserved as-is.
- **Introduce an explicitly versioned canonicalization standard.** This document (GOV-D-07) defines version `1.0` of the ManifestHash canonicalization specification based on RFC 8785 JCS.
- **Apply the approved standard to newly generated or formally regenerated manifests.** All new `reference_versions.csv` entries and new per-dataset manifests use the approved standard.
- **Regenerate existing manifests only after explicit authorization and documented impact assessment.** Existing manifests in `data/manifests/` retain their current hash values unless explicitly regenerated under the new standard.
- **Record the canonicalization specification version alongside the resulting hash.** Each manifest entry includes a reference to the canonicalization specification version used to compute its `ManifestHash`.

### 6.2 Distinction: Historical vs. Newly Approved

| Category | Manifests | Hash Standard | Status |
|---|---|---|---|
| Historical | Existing `data/manifests/*.json` files | Various/unspecified (not RFC 8785) | Preserved; not recomputed |
| Newly generated | New `reference_versions.csv` entries and new per-dataset manifests | RFC 8785 JCS v1.0 (this specification) | Generated under approved standard |
| Regenerated | Existing manifests explicitly regenerated | RFC 8785 JCS v1.0 | Requires explicit authorization + impact assessment |

---

## 7. Contract Embedding Strategy

### 7.1 Recommendation

Keep the full technical canonicalization specification in this separately versioned governance document (`GOV_D_07_MANIFESTHASH_CANONICALIZATION_DRAFT.md` and its successor versions). The data contract (`03_DATA_CONTRACTs.md`) should **reference** the approved specification and its version number, but the detailed rules should not be embedded in the contract body.

### 7.2 Contract Reference

Contract v1.5 line 264 names `ManifestHash` as a manifest field. After GOV-D-07 approval, the contract (or a controlled contract amendment) should add a reference such as:

> "`ManifestHash` is computed per the canonicalization method specified in governance document `GOV-D-07` (version X.Y), based on RFC 8785 JSON Canonicalization Scheme."

**This task does not modify `03_DATA_CONTRACTs.md`.** The contract reference is a recommendation for a future controlled document change.

---

## 8. Test Requirements

### 8.1 Validation Scenarios

The twelve validation scenarios from the previous draft are retained and strengthened. Each scenario is classified by maturity:

| Maturity Label | Meaning |
|---|---|
| Test specified | Scenario described in this document; no code exists |
| Test implemented | Test code written in repository; not yet run |
| Test executed | Test run at least once; result observed |
| Test passed | Test executed successfully with evidence |

| # | Test Case | Expected Result | Maturity |
|---|---|---|---|
| V-01 | RFC 8785 canonicalization consistency — same manifest, two independent implementations | Identical SHA-256 digest | Specified |
| V-02 | Different JSON property ordering produces same hash | Reordered keys yield identical hash | Specified |
| V-03 | Whitespace differences do not change hash | Pretty-printed vs. minified yield identical hash | Specified |
| V-04 | Unicode strings handled per RFC 8785 | Same string value yields identical hash | Specified |
| V-05 | Number serialization per RFC 8785 | `1.50` serializes as `1.5`; `1e2` serializes as `100` | Specified |
| V-06 | Duplicate JSON object keys rejected | Validation error; no hash produced | Specified |
| V-07 | Missing vs. null value produce different hashes | `"field": null` ≠ missing `field` | Specified |
| V-08 | Array ordering preserved | Reordered array → different hash | Specified |
| V-09 | ManifestHash removal | Hash identical whether `ManifestHash` is absent, `null`, `""`, or a previous hash | Specified |
| V-10 | SHA-256 verification procedure | Recomputed hash matches stored `ManifestHash` | Specified |
| V-11 | Modified manifest detection | Any field change → different hash; verification fails | Specified |
| V-12 | Canonicalization specification version | Version identifier recorded alongside hash | Specified |

### 8.2 Implementation Status

- **Tests specified:** All 12 (V-01 through V-12) are specified in this document.
- **Tests implemented:** 0. No RFC 8785 test code exists in the repository.
- **Tests executed:** 0. No tests have been run.
- **Tests passed:** 0. No test results exist.

**Existing SHA-256 tests** (`tests/unit/test_hashing.py`) test the SHA-256 primitive only (`sha256_bytes(b"abc")` against the known RFC 4634 test vector). They do **not** test RFC 8785 canonicalization or ManifestHash computation. These existing tests are compatible with the proposed approach but do not validate it.

---

## 9. Owner Decision Options

| Option | Description | Owner Action |
|---|---|---|
| **OPTION A — Approve the revised RFC 8785-based standard as proposed** | Accept all recommendations in Sections 4–8: RFC 8785 JCS, ManifestHash removal before canonicalization, no Unicode normalization (Option 1), separate versioned governance document, 12 specified tests | Mark APPROVED; record date and signature |
| **OPTION B — Approve with further owner-directed changes** | Accept with modifications to specific rules (e.g., require Unicode NFC normalization, different timestamp format, different hash output casing, embedded contract specification) | Mark RETURNED FOR REVISION with specified changes |
| **OPTION C — Reject and return for redesign** | Reject the proposed method; require a fundamentally different approach | Mark REJECTED; document alternative requirements |

### 9.1 Technical Recommendations Still Requiring Owner Approval

| Item | Recommended Value | Owner Decision |
|---|---|---|
| Canonicalization standard | RFC 8785 JCS | [BLANK] |
| Unicode normalization | Option 1: preserve exact, no NFC | [BLANK] |
| ManifestHash self-exclusion | Remove property before canonicalization | [BLANK] |
| Hash algorithm | SHA-256 | [BLANK] |
| Hash output format | Lowercase hexadecimal (64 chars) | [BLANK] |
| Timestamp format | ISO 8601 `YYYY-MM-DDThh:mm:ssZ` (UTC) | [BLANK] |
| Retroactive application | Do not silently rewrite; versioned standard | [BLANK] |
| Contract embedding | Separate versioned governance doc; contract references it | [BLANK] |
| Canonicalization specification version | 1.0 (this document) | [BLANK] |

---

## 10. Explicit Approval Status

| Field | Entry |
|---|---|
| Decision | [ ] OPTION A — APPROVED   [ ] OPTION B — RETURNED FOR REVISION   [ ] OPTION C — REJECTED |
| Approval scope | GOV-D-07 — ManifestHash Canonicalization (RFC 8785 JCS) |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Approval conditions | [BLANK — to be completed at signature] |
| Signed-copy path | [BLANK — no docs/approvals/ structure] |
| Signed-copy SHA-256 | [BLANK — no signed copy exists] |
| Retention confirmed | [ ] Yes   [X] No — GOV-D-08 PENDING |
| Verification date/result | [BLANK — PENDING] |

**Formal signature:** ______________________________  
**Approval date:** ______________________________  

**Approval status:** PENDING. ManifestHash canonicalization is proposed (revised draft), not approved. No owner decision has been made on GOV-D-07.

---

## 11. Implementation Restrictions

The following are strictly prohibited by this decision record:

- Do not modify OD-01A or OD-01B.
- Do not modify contract v1.5 (`03_DATA_CONTRACTs.md`).
- Do not modify existing owner decisions.
- Do not modify production manifests or reference CSV files in `data/manifests/`.
- Do not modify hashing implementation (`src/utilities/hashing.py`).
- Do not modify Power Query or DAX.
- Do not modify the PBIX.
- Do not generate reference data.
- Do not create `data/manifests/reference_versions.csv`.
- Do not execute `G3-RV-01`.
- Do not freeze the schema.
- Do not authorize `G3` or `G4`.
- Do not claim independent review.
- Do not mark GOV-D-07 formally approved.
- Do not fabricate test results, signatures, approvals or reviewers.

Only this GOV-D-07 draft revision and its revision record may be created. No implementation activity is authorized.

---

## 12. End of Decision Record

This document records the revised ManifestHash canonicalization method based on RFC 8785 JCS. No source files, data, DAX, Power Query, semantic model, Power BI, or other project artifacts were modified during its creation. No signature, approval date, reviewer identity, or approval evidence has been created. GOV-D-07 remains pending formal owner approval.

**Verdict: READY FOR OWNER REVIEW** — The revised draft replaces custom serialization rules with RFC 8785 JCS, resolves the ManifestHash self-exclusion ambiguity, defines a retroactive migration policy, specifies 12 test scenarios with clear maturity labels, and presents three owner decision options. Owner decision is required before any downstream activity (G3-RV-01, T-78, reference manifest creation) can proceed.