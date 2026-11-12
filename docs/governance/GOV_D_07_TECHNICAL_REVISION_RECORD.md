# GOV-D-07 — Technical Revision Record

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** GOV-D-07-TRR-2026-11-06-001  
**Document Type:** Technical Revision Record  
**Status:** COMPLETE — READY FOR OWNER REVIEW  
**Prepared:** 2026-11-06  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Original Unresolved Issues

The previous GOV-D-07 draft (first version) had the following unresolved issues identified under Owner Option B — Approve with technical revisions:

| Issue ID | Issue | Location in Previous Draft |
|---|---|---|
| TR-01 | Custom JSON serialization rules combined multiple standards (RFC 8259 escaping, lexicographic key sorting, minified whitespace) without referencing a single canonicalization standard | Section 4.3 and Section 5.1 |
| TR-02 | Unicode NFC normalization claimed as part of canonicalization, but RFC 8785 does not perform Unicode normalization; no separate input-validation rule documented | Section 4.1 (rule 7) and Section 4.4 |
| TR-03 | ManifestHash self-exclusion ambiguous: unclear whether to set to `""`, remove the field, or leave as-is before hashing | Section 5.3 (ManifestHash = NO) and Section 5.2 |
| TR-04 | No retroactive application/migration policy for existing manifests | Not addressed |
| TR-05 | Contract embedding strategy undecided: whether to embed full specification in `03_DATA_CONTRACTs.md` or reference a separate governed document | Not addressed |
| TR-06 | Test maturity not distinguished: no clarity on which tests are specified vs. implemented vs. executed vs. passed | Section 6 (acceptance criteria only) |
| TR-07 | No explicit owner decision options mapped to the revised technical standard | Section 9 (generic options only) |

---

## 2. Changes Made

### 2.1 Canonicalization Standard (TR-01 resolved)

| Aspect | Previous Draft | Revised Draft |
|---|---|---|
| Standard | Custom serialization rules (RFC 8259 escaping, code-point key sort, minified whitespace, integer/decimal rules) | RFC 8785 — JSON Canonicalization Scheme (JCS) |
| Key ordering | Lexicographic by Unicode code point | Deterministic per RFC 8785 Section 3.2.3: lexicographic comparison of UTF-16 code units (not UTF-8 byte ordering) |
| Number serialization | Custom: no trailing zeros, no unnecessary exponent | Deterministic per I-JSON (RFC 7493) / IEEE 754 binary64; integers without leading zeros or trailing zeros after decimal; exponents use lowercase `e`; no unnecessary leading/trailing zeros; values exceeding binary64 precision must be represented as strings or rejected |
| String escaping | RFC 8259 standard | RFC 8785 (RFC 8259-based with specific control character/non-ASCII rules) |
| Duplicate keys | Not permitted | Rejected: input with duplicate keys is non-canonical |
| Non-I-JSON input | Not addressed | Rejected |
| Additional whitespace | None (minified) | None (canonical output has no insignificant whitespace) |
| Unicode normalization | NFC claimed | Not claimed; RFC 8785 does not normalize; separate input-validation decision documented (Option 1: preserve exact) |

### 2.2 ManifestHash Self-Exclusion (TR-02 resolved)

| Aspect | Previous Draft | Revised Draft |
|---|---|---|
| Procedure | `ManifestHash` field excluded (marked NO in matrix) | Explicit 7-step procedure: parse → validate → remove property → canonicalize → encode → SHA-256 → store |
| Absent `ManifestHash` | Not addressed | Hash computed over all remaining properties |
| Null `ManifestHash` | Not addressed | Property removed; null does not contribute |
| Empty string `ManifestHash` | Not addressed | Property removed; empty string does not contribute |
| Malformed `ManifestHash` | Not addressed | Property removed; value does not contribute |
| Previous valid hash | Not addressed | Removed before canonicalization; hash recomputed |

### 2.3 Retroactive Application (TR-03 resolved)

New Section 6 added defining:
- Do not silently rewrite existing manifests
- Versioned canonicalization standard (v1.0)
- Apply to newly generated or formally regenerated manifests only
- Regeneration requires explicit authorization + impact assessment
- Record canonicalization specification version alongside hash
- Distinction table: Historical vs. Newly generated vs. Regenerated manifests

### 2.4 Contract Embedding (TR-04 resolved)

New Section 7 added:
- Keep full specification in separately versioned governance document
- Data contract references the approved specification and version
- Example contract reference language provided
- Explicit statement: `03_DATA_CONTRACTs.md` NOT modified in this task

### 2.5 Test Requirements (TR-05 resolved)

| Aspect | Previous Draft | Revised Draft |
|---|---|---|
| Test count | 12 scenarios | 12 scenarios (V-01 through V-12) |
| Test maturity labels | None | Specified / Implemented / Executed / Passed |
| RFC 8785-specific tests | Not present | V-01 (canonicalization consistency), V-05 (number serialization) |
| ManifestHash removal test | V-09 | V-09 (explicit: absent/null/empty/previous hash all produce same result) |
| Existing test compatibility | Not addressed | Noted: `tests/unit/test_hashing.py` tests SHA-256 primitive only, compatible but does not validate RFC 8785 |
| Tests executed | Claimed none | Explicitly stated: 0 specified, 0 implemented, 0 executed, 0 passed |

### 2.6 Owner Decision Options (TR-06 resolved)

| Aspect | Previous Draft | Revised Draft |
|---|---|---|
| Options | A (approve), B (reject/revise), C (reject) | A (approve RFC 8785 as proposed), B (approve with changes), C (reject and redesign) |
| Technical recommendations requiring approval | Listed in table | 9 items in explicit table with [BLANK] owner decisions |
| Approval block | Generic | Updated to reference OPTION A/B/C |

---

## 3. Technical Justification

| Change | Justification |
|---|---|
| RFC 8785 JCS | Provides a single, externally standardized, IETF-ratified deterministic JSON serialization scheme. Two independent implementations following RFC 8785 produce identical character sequences for the same logical JSON, using lexicographic comparison of UTF-16 code units for property ordering (Section 3.2.3) and I-JSON / IEEE 754 binary64 for number serialization. The canonical character sequence is then UTF-8 encoded and SHA-256 hashed as separate sequential steps. |
| No Unicode NFC claim | RFC 8785 does not perform Unicode normalization. Claiming NFC would misrepresent the standard and create interoperability risk. Unicode normalization is documented as a separate input-validation decision (Option 1: preserve exact values). |
| ManifestHash removal before canonicalization | Resolves the self-referential paradox: a hash cannot include its own value. Removing the property entirely (rather than setting to empty string) ensures the stored hash value never influences the computed hash, regardless of its current content. |
| Versioned standard | Enables traceability: each manifest hash is tied to a specific canonicalization specification version, supporting future migration and audit. |
| Separate governance document | Keeps the data contract focused on business rules while the technical canonicalization detail lives in a versioned, independently reviewable document. |

---

## 4. Decisions Still Requiring Owner Approval

| # | Decision | Recommended Value | Owner Decision |
|---|---|---|---|
| 1 | Approve GOV-D-07 revised draft | OPTION A / B / C | [BLANK] |
| 2 | Canonicalization standard | RFC 8785 JCS | [BLANK] |
| 3 | Unicode normalization | Option 1: preserve exact, no NFC | [BLANK] |
| 4 | ManifestHash self-exclusion | Remove property before canonicalization | [BLANK] |
| 5 | Hash algorithm | SHA-256 | [BLANK] |
| 6 | Hash output format | Lowercase hexadecimal (64 chars) | [BLANK] |
| 7 | Timestamp format | ISO 8601 `YYYY-MM-DDThh:mm:ssZ` (UTC) | [BLANK] |
| 8 | Retroactive application | Do not silently rewrite; versioned standard | [BLANK] |
| 9 | Contract embedding | Separate versioned doc; contract references it | [BLANK] |
| 10 | Canonicalization specification version | 1.0 (this document) | [BLANK] |

---

## 5. Files Inspected

| File | Location | Purpose |
|---|---|---|
| GOV-D-07 draft (previous) | `docs/governance/GOV_D_07_MANIFESTHASH_CANONICALIZATION_DRAFT.md` | Baseline document being revised |
| CC01_REMEDIATION_REGISTER_V2.md | `docs/governance/` | A-04 / GOV-D-07 acceptance criteria |
| CC01_REMEDIATION_PRIORITY_MATRIX.md | `docs/governance/` | P0 classification and acceptance criteria |
| CC01_FINDINGS_REMEDIATION_PLAN.md | `docs/governance/` | Dependency on G3-RV-01 and T-78 |
| CC01_REMEDIATION_PLAN_RECONCILIATION.md | `docs/governance/` | P0 count correction |
| CC01_OWNER_SELF_REVIEW.md | `docs/governance/` | GOV-D-07 pending owner decision |
| CC01_OWNER_SELF_REVIEW_FINDINGS.md | `docs/governance/` | GOV-D-07 HIGH severity |
| OD_01_PRESIGNATURE_READINESS_AUDIT.md | `docs/governance/` | OD-01A/OD-01B not ready |
| AEROVISION_360_GOVERNANCE_INVESTIGATION_REPORT.md | `docs/` | §7.4: GOV-D-07 exact question, source, dependencies |
| OD01_OWNER_CONFIRMATION_ADDENDUM_ACCEPTANCE.md | `docs/governance/` | Addendum accepted; does not cover GOV-D-07 |
| GOV_D_06_STALENESS_THRESHOLD_DECISION_DRAFT.md | `docs/governance/` | Separate decision (365/180 days) |
| 03_DATA_CONTRACTs.md (v1.5 DRAFT) | `docs/` | Lines 259–266: ManifestHash field, reference manifest |
| src/utilities/hashing.py | `src/utilities/` | SHA-256 primitive (compatible with JCS byte output) |
| tests/unit/test_hashing.py | `tests/unit/` | SHA-256 primitive tests (compatible, not RFC 8785) |
| src/quality/manifest.py | `src/quality/` | QualityManifest checksum verification (compatible) |
| data/manifests/dim_airline_manifest.json | `data/manifests/` | Example per-dataset manifest structure |
| data/manifests/fact_flight_operations_manifest.json | `data/manifests/` | Example per-dataset manifest structure |
| data/manifests/reference_versions.csv | `data/manifests/` | Does not exist (confirmed) |

**NOT FOUND:** `docs/governance/GOV_D_06_OWNER_ACCEPTANCE.md` — no formal acceptance record for GOV-D-06.

---

## 6. Files Modified and Created

| File | Action | Reason |
|---|---|---|
| `docs/governance/GOV_D_07_MANIFESTHASH_CANONICALIZATION_DRAFT.md` | Rewritten (replaces previous draft) | RFC 8785 JCS standard, resolved ManifestHash exclusion, migration policy, contract strategy, updated tests, updated decision options |
| `docs/governance/GOV_D_07_TECHNICAL_REVISION_RECORD.md` | Created | This revision record |

**NOT MODIFIED:**
- `docs/03_DATA_CONTRACTs.md` (contract v1.5)
- OD-01A or OD-01B decision records
- Any existing owner decisions
- Production manifests in `data/manifests/`
- Reference CSV files
- `src/utilities/hashing.py`
- `tests/unit/test_hashing.py`
- `src/quality/manifest.py`
- Power Query, DAX, semantic model files, or PBIX

---

## 7. Implementation Restrictions

The following remain strictly prohibited:

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

---

## 8. Final Readiness Assessment

| Criterion | Status |
|---|---|
| Canonicalization standard clearly specified | Complete (RFC 8785 JCS) |
| ManifestHash self-exclusion resolved | Complete (7-step removal procedure) |
| Unicode normalization decision documented | Complete (Option 1: preserve exact; owner decision required) |
| Retroactive migration policy defined | Complete (Section 6) |
| Contract embedding strategy defined | Complete (Section 7; contract not modified) |
| Test scenarios specified | Complete (V-01 through V-12) |
| Test maturity labels distinguished | Complete (specified/implemented/executed/passed) |
| Owner decision options defined | Complete (OPTION A/B/C) |
| Approval status block present | Complete (all fields blank, pending owner) |
| Implementation restrictions documented | Complete (Section 11 of draft) |
| Tests actually executed | None (0 executed, 0 passed) |
| Formal owner approval obtained | None (pending) |

**Verdict: READY FOR OWNER REVIEW**

The revised GOV-D-07 draft and this technical revision record are complete. The document replaces custom serialization rules with RFC 8785 JCS, resolves all previously ambiguous technical decisions, clearly distinguishes specified tests from executed tests, and presents three explicit owner decision options. No implementation is authorized. No signatures, approvals, or test results have been fabricated.

Owner decision is required on OPTION A/B/C and on the 9 technical recommendations in Section 4 of the revision record before any downstream activity (G3-RV-01, T-78, reference manifest creation) can proceed.