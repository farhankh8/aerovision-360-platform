# AEROVISION 360 — Implementation QA Blueprint

**Status:** ENGINEERING PREPARATION — TEST PLAN DESIGNED, NO TEST EXECUTED
**Version:** 0.1
**Prepared:** 2026-11-02
**Governing contract:** `docs/03_DATA_CONTRACTS.md` version 1.5
**Traceability authority:** `docs/REQUIREMENTS_TRACEABILITY.md`
**Companion documents:** `POWER_BI_SEMANTIC_MODEL_BLUEPRINT.md`, `POWER_BI_DASHBOARD_SPECIFICATION.md`, `DAX_KPI_CATALOGUE.md`
**Project root:** `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`

> **Status notice.** This is a QA plan, not evidence of execution. `qa/results/` is empty. No test has been run, no report has been rendered, and no test is claimed PASS. T-37, T-42–T-46, T-55, and T-79 remain `BLOCKED`; T-72–T-78 remain `PLANNED`; G3 is `NOT STARTED`; G4 is `BLOCKED`.

**Canonical disclosure:** `Synthetic Simulation — Not Actual Airline Performance`

## 1. Purpose and quality principles

The QA layer must prove that the synthetic data, CURATED model, semantic model, DAX measures, report pages, and disclosure meet the contract and business requirements. It must not merely show that files exist.

**Principles:**

- Test the business rule and the control total, not only the schema.
- Use independent recalculation, not the same transformation code that produced the data.
- Preserve expected and actual values, row counts, tolerances, and evidence paths.
- Fail closed: a critical/high defect blocks publication; a missing test is not a pass.
- Distinguish `PLANNED`, `IMPLEMENTED`, `EXECUTED`, `PASSED`, `FAILED`, and `BLOCKED` from the contract's canonical status vocabulary.
- A document review is not a data test. A schema parse is not a reconciliation.
- No reviewer identity, execution date, or approval is invented. A test cannot be `PASSED` without a reviewer and evidence.
- Disclosure failure is critical, not cosmetic.

## 2. Test-state model

The master prompt requires six execution states; the contract uses a five-value canonical status vocabulary. The QA layer uses both explicitly:

| Blueprint state | Contract status | Meaning | Can release? |
|---|---|---|---|
| `PLANNED` | `PLANNED` | Test designed; code/data/report not available | No |
| `IMPLEMENTED` | `IN PROGRESS` | Test code or manual procedure exists; not executed | No |
| `EXECUTED` | `IN PROGRESS` | Test was run; evidence not reviewed/accepted | No |
| `PASSED` | `PASS` | Executed with evidence; reviewer accepted | Yes, if all other gates pass |
| `FAILED` | `FAIL` | Executed; expected result not met | No |
| `BLOCKED` | `BLOCKED` | Cannot execute because a prerequisite is absent | No |

**Current state:** all contract tests are `PLANNED` or `BLOCKED`; no test is `IMPLEMENTED`, `EXECUTED`, `PASSED`, or `FAILED`. The document-level checks in Section 12 are separate from the T-01–T-79 data/report tests.

## 3. Test scope

| Layer | What is tested | Primary evidence |
|---|---|---|
| A. Reference and identity | Ten airlines, provenance, `AirlineId`/`AirlineKey`, version, manifest | T-72–T-78; `qa/results/airline_*` |
| B. Structural and referential | Grain, keys, types, relationships, orphan keys | T-01–T-14; `qa/results/schema_*`, `keys_*` |
| C. Business and financial | Capacity, passengers, revenue, costs, refunds, allocation, delay, feedback | T-15–T-36, T-47–T-55, T-61–T-71 |
| D. KPI and reconciliation | 21 KPIs, zero denominators, rollups, independent controls | T-28–T-39, T-46, T-60 |
| E. Reproducibility and runtime | Seeded rerun, Power BI refresh, roles, report, disclosure, export | T-40–T-46, T-79 |
| F. Release | Packaging, documentation, privacy, authorization, no prohibited artifacts | Release checklist; not a substitute for T-tests |

## 4. Test environment and prerequisites

| Prerequisite | Current state | Required before execution |
|---|---|---|
| Approved OD-01A/OD-01B | Pending signature | Signed decision records and dates |
| Critical OD decisions | Partially open | Formal owner decisions; no silent defaults |
| `G3-RV-01` approved reference version | `NOT EXECUTED` | Approved manifest and reference version |
| Reference data | Not created | Approved `ref_*` files and provenance |
| Schema freeze | Not authorized | Written freeze |
| G4 data authorization | `BLOCKED` | Written authorization |
| Python environment | Python 3.13.2 detected; packages not pinned | Locked environment and manifest |
| Power BI Desktop | Detected earlier; version unverified | Version record and test workbook |
| Rendered report | Absent | Authorized report build |
| Independent reviewer | Not assigned | Named reviewer for PASS decisions |

**No test may use production airline data, real passenger data, or external claims.** All operating data is synthetic.

## 5. Test coverage by test family

### 5.1 Reference and airline identity

| Test | Name / focus | Current status | Method and evidence |
|---|---|---|---|
| T-72 | Approved roster reconciliation | `PLANNED` | Compare DimAirline to `ref_airlines.csv` on the six identity attributes for the selected version; 10 exact identities; `qa/results/airline_identity_roster.csv` |
| T-73 | IATA format and version-qualified uniqueness | `PLANNED` | Regex `^[A-Z0-9]{2}$`; uniqueness within version; not a key; `airline_iata_codes.csv` |
| T-74 | ICAO format and version-qualified uniqueness | `PLANNED` | Regex `^[A-Z]{3}$`; uniqueness within version; not a key; `airline_icao_codes.csv` |
| T-75 | Attribute-level provenance completeness | `PLANNED` | One VERIFIED source per populated attribute; real source organization/URL/type/date/method; evidence hash/archive; `BusinessModelClass` and `OperatingRegion` excluded; `airline_identity_provenance.csv` |
| T-76 | Unsupported/conflicting identity handling | `PLANNED` | Inspect CONFLICTING/UNVERIFIED/SUPERSEDED/QUARANTINED; required conflicts block; optional null; no inference; `airline_identity_conflicts.csv` |
| T-77 | Reference-to-dimension reconciliation | `PLANNED` | Row-for-row on identity and key map; no orphan/extra; `airline_identity_reconciliation.csv` |
| T-78 | Version, manifest, refresh, key integrity | `PLANNED` | T-78-01–T-78-10; one version, approved manifest, stable key map, no mixed facts, no key reassignment; `airline_identity_versions.csv` |
| T-79 | Exact disclosure and rendered output | `BLOCKED` | Unicode code points, footer/header, visible tooltip, export, screenshot, metadata; exact string; `disclosure_integrity.csv` |

### 5.2 Structural, key, and referential

| Test group | IDs | Current status | What must be proven |
|---|---|---|---|
| Scope/date | T-01–T-02 | `PLANNED` | Fixed scope; 2025-10-01–2026-09-30 inclusive; no outside reporting rows |
| Flight structural | T-03–T-14 | `PLANNED` | 150,000–250,000 legs; grain; keys; capacity; flags; date keys; referential integrity |
| Booking structural | T-19–T-22, T-27 | `PLANNED` | Coupon grain; one passenger per coupon; FKs; currencies; revenue identities; lead-time mechanics |
| Cost structural | T-26 | `PLANNED` | Ledger grain; classification; allocation; control totals |
| Disruption structural | T-23–T-24 | `PLANNED` | Event sequence; delay attribution; reactionary evidence |
| Feedback structural | T-25 | `PLANNED` | Event grain; valid customer/flight; score/category rules |
| Date/quality | T-47–T-54 | `PLANNED` | Date roles; DST; period boundaries; controlled defects; quarantine |
| Availability | T-56–T-59 | `PLANNED` | Composite key; references; status/hours; version reproducibility |

**Structural acceptance:** zero duplicate primary/business keys; zero duplicate fact grain; zero unresolved required foreign keys; zero invalid date keys; zero mixed reference versions; exact schema parity.

### 5.3 Business and financial

| Test group | IDs | Current status | What must be proven |
|---|---|---|---|
| Capacity | T-15 | `PLANNED` | Scheduled capacity positive; cancelled capacity retained; no overbooking; available seats = aircraft configuration |
| Passengers | T-16–T-17 | `PLANNED` | Revenue + non-revenue ≤ booked ≤ capacity; cancelled flights carry zero; no negative counts |
| Delay/cancellation | T-18, T-23–T-24 | `PLANNED` | UTC delay arithmetic; arrival delay partition; cancellation flags; reactionary evidence |
| Revenue | T-19, T-31–T-32, T-38–T-39 | `PLANNED` | Passenger/fee/ancillary identities; tax excluded; refunds once; booking controls; rollups |
| Refunds/no-show | T-20 | `PLANNED` | Refund rate denominator; cancellation/no-show fees; no double refund |
| Ancillary/fees | T-21 | `PLANNED` | Fee and ancillary revenue identities; separation from passenger revenue |
| Lead time/repeat | T-22, T-47 | `PLANNED` | Non-negative lead time; booking-level dedupe; eligibility rules; no 365-day assumption |
| Costs | T-26, T-33 | `PLANNED` | Ledger control; category classification; allocation sum; CASK reconciliation |
| Feedback | T-25, T-36, T-49 | `PLANNED` | Feedback grain; complaint denominator; satisfaction scale; resolution date; service recovery |
| Classification | T-63–T-71 | `PLANNED` | Approved cost/disruption taxonomy; exact matching; quarantine; cross-airline consistency |
| Allocation | T-55 | `BLOCKED` | OD-14 formal approval absent; residual and tie-break cannot be accepted |

### 5.4 KPI and reconciliation

| Test | Focus | Current status | Independence requirement |
|---|---|---|---|
| T-28 | ASK | `PLANNED` | Independent SQL/Python recomputation from flight rows within 0.1% |
| T-29 | RPK | `PLANNED` | Independent recalculation; revenue passengers only; cancelled zero |
| T-30 | Load factor | `PLANNED` | Independent RPK/ASK; within 0.01 percentage point |
| T-31 | Passenger yield/revenue control | `PLANNED` | Revenue identity plus RPK; tax/fee/ancillary excluded |
| T-32 | Total RASK / ancillary | `PLANNED` | Total operating revenue identity; tax excluded |
| T-33 | CASK / cost | `PLANNED` | Cost control; non-operating exclusions |
| T-34 | OTP/cancellation/completion | `PLANNED` | Denominator = scheduled/valid operated; cancelled included where required |
| T-35 | Average delay/utilization | `PLANNED` | Valid arrival denominator; availability denominator; no double count |
| T-36 | Average revenue/ancillary/refund/lead/satisfaction/repeat/recovery | `PLANNED` | Grain-correct denominators; booking-level dedupe; response counts |
| T-37 | Zero-denominator behavior | `BLOCKED` | Runtime DAX test; no semantic model |
| T-38 | Revenue rollups | `PLANNED` | Coupon → booking → flight → airline → route → month → total |
| T-39 | Cost/contribution rollups | `PLANNED` | Ledger → airline → route → month → total; no double allocation |
| T-46 | Report KPI reconciliation | `BLOCKED` | Render each page and compare to control calculations |
| T-60 | K-13 utilization | `PLANNED` | Independent numerator/denominator; selected version; airline filter transfer |

**Independent evidence:** use a separate DuckDB/Python script or Excel control workbook, not the production transformation function. Record expected/actual/difference/tolerance. A formula copied from the production code is not independent evidence.

### 5.5 Power BI semantic model and report

| Test | Focus | Current status | Evidence |
|---|---|---|---|
| T-37 | Zero-denominator runtime | `BLOCKED` | Measure test matrix with zero/blank filters |
| T-42 | Relationship cardinality | `BLOCKED` | Relationship inventory; all 1:* single direction |
| T-43 | Role-playing dimensions | `BLOCKED` | Origin/destination/departure/arrival/booking/travel/feedback/event-location tests |
| T-44 | No fact-to-fact/M2M | `BLOCKED` | Model review and prohibited-relationship query |
| T-45 | Refresh | `BLOCKED` | Refresh log; row counts match CURATED |
| T-46 | Report KPI reconciliation | `BLOCKED` | Visual-by-visual control comparison |
| T-79 | Disclosure | `BLOCKED` | Rendered screenshot, tooltip, export, metadata |

**Date-role test:** with `DimDate` filtered to a period, confirm K-16/K-17/K-20 use `BookingDateKey` through `USERELATIONSHIP`, while K-04/K-05/K-14/K-15 use `TravelDateKey`, K-09 uses scheduled departure, and K-18 uses feedback date for complaints plus departure date for passengers. Change only one date-role filter and verify that the affected measures change while unrelated measures do not. Record the expected and actual values; this is part of T-43.

**Report checks beyond the contract tests:** page inventory, custom tooltips, export template, mobile layout, accessibility, interaction review, no unsupported severity/sentiment/service-category fields. These are specified in `POWER_BI_DASHBOARD_SPECIFICATION.md`; they do not replace T-42–T-46 or T-79.

### 5.6 Reproducibility and release

| Test | Focus | Current status | Evidence |
|---|---|---|---|
| T-40 | Seed/config reproducibility | `PLANNED` | Two runs with same seed/config/reference; logical rows, keys, controls, hashes |
| T-41 | Clean rebuild reproducibility | `PLANNED` | Clean environment rebuild; key map and manifest |
| Release | Packaging, privacy, documentation, authorization | `PLANNED` | Release checklist; no PII/secrets; no unauthorized artifacts |

## 6. Test design details

### 6.1 Boundary and negative tests

- Reporting period start `2025-10-01` and end `2026-09-30`; flights departing before/after are excluded or explicitly out of scope.
- Overnight flight: departure and arrival local dates differ; arrival date is later.
- Cross-time-zone flight: scheduled and actual dates derived independently.
- DST transition: at least one affected region; no duplicate/missing hour errors.
- Cancelled flight: scheduled timestamps and date keys present; actual timestamps/delays null; carried passengers zero.
- Zero/blank denominator: every ratio returns BLANK; no infinity.
- Duplicate business key: rejected/quarantined; no silent dedupe.
- Orphan required FK: rejected; no `-1` fallback.
- Mixed reference versions: blocks refresh/generation.
- Reassigned `AirlineKey`: critical failure.
- Refund greater than paid: rejected.
- Allocation residual: assigned once; ties by lowest key (OD-14).
- Satisfaction score outside 1–5: rejected.
- Resolution date before feedback: rejected.
- Missing reference provenance: required attribute blocks; optional remains null.

### 6.2 Test data management

- Test data is generated, never real airline data.
- Use a small deterministic fixture for unit tests and the full planned volume for performance/reconciliation.
- Do not use production data to “make a test pass.”
- Do not alter expected results to match observed results. A changed expectation requires a documented rule change, not a test edit.
- Preserve failed-run evidence; do not overwrite it with a passing rerun.

### 6.3 Evidence schema

Each test evidence file under `qa/results/<run_id>/` should include:

| Column | Meaning |
|---|---|
| `test_id` | Contract ID, e.g. `T-28` |
| `run_id` | Immutable run identifier |
| `dataset` | Table/file under test |
| `rule_id` | DQ or business rule identifier |
| `expected` | Expected value/range |
| `actual` | Observed value |
| `difference` | Numeric difference, where applicable |
| `tolerance` | Approved/proposed tolerance |
| `status` | `PLANNED`, `IMPLEMENTED`, `EXECUTED`, `PASSED`, `FAILED`, `BLOCKED` |
| `executed_at_utc` | Actual execution timestamp; blank if not executed |
| `executor` | Person/system that executed; no invented identity |
| `reviewer` | Named reviewer; blank until review |
| `evidence_path` | File/screenshot/log path |
| `notes` | Limitation, exception, or decision link |

Evidence files are hashed into the run manifest. Screenshots include the disclosure and are not cropped.

## 7. Defect severity and disposition

| Severity | Examples | Release impact |
|---|---|---|
| Critical | Mixed reference versions; reassigned `AirlineKey`; fabricated approval/provenance; disclosure missing; real PII; fact-to-fact model | Blocks release; stop |
| High | Duplicate grain/key; unresolved required FK; revenue/cost identity failure; cancelled flight carrying passengers; wrong KPI denominator; missing T-79 | Blocks release |
| Medium | Optional provenance gap; non-critical formatting; documented low-base instability; incomplete non-critical interaction | May release only with owner-approved disposition and disclosure |
| Low | Cosmetic label, sort, or spacing | May release with a recorded fix plan |

A defect is closed only with a fix, a retest, and evidence. Do not close by changing the test expectation unless the rule itself changed through the correct decision process.

## 8. Pass/fail and exit criteria

A test is `PASSED` only when:

1. The test was executed against the intended run/version.
2. Expected and actual values are recorded.
3. The tolerance/decision is recorded.
4. Evidence exists and is hashed.
5. A named reviewer accepted it.
6. The test is not dependent on an unapproved rule.

**The G5 data-quality gate, G9 runtime QA gate, and G10 portfolio release gate are not reached until:**

- All applicable T-01–T-79 tests are `PASSED` or explicitly dispositioned with owner approval.
- No critical or high defect remains open.
- T-79 passes on the rendered report, tooltip, export, and screenshot.
- T-42–T-46 pass on the actual semantic model/report.
- T-72–T-78 pass on the approved reference version and key map.
- No unresolved decision changes a KPI definition, population, reference version, or model relationship.
- No PII, secret, unsupported field, or unauthorized artifact is present.
- G4 and schema freeze were completed before implementation.

**Current result:** none of these conditions is met; release is not authorized.

## 9. Requirements traceability coverage

| Requirement group | Test/evidence |
|---|---|
| REQ-001, REQ-023–REQ-028 | T-72–T-79; reference manifest; key map; provenance |
| REQ-002 | T-02, T-50, T-51; date coverage |
| REQ-003 | Schema registry; T-03–T-14; data dictionary |
| REQ-004 | T-40, T-41, T-72–T-78; key-map hash |
| REQ-005 | DQ-01–DQ-14; T-54; quarantine evidence |
| REQ-006 | T-42–T-44; relationship inventory |
| REQ-007 | T-28–T-36; KPI dictionary and reconciliation |
| REQ-008 | T-45, T-46; five-page review |
| REQ-009 | T-42–T-46; interaction and drill-through review |
| REQ-010 | T-37, T-45, T-46; runtime evidence |
| REQ-011 | Release checklist; reproducibility; setup documentation |
| REQ-012–REQ-016 | T-56–T-60; T-37; availability reference |
| REQ-017–REQ-022 | T-63–T-71; cost/disruption taxonomy; no FactRevenue |
| REQ-023–REQ-028 | T-72–T-79; identity, key, version, disclosure |

All requirements remain `NOT STARTED` in the traceability matrix. This blueprint does not change that status.

## 10. Power BI report-specific QA

| Check | Method | Current status |
|---|---|---|
| Five visible pages and exact names | Page inventory | `BLOCKED` — no report |
| No extra visible pages | Page inventory | `BLOCKED` |
| KPI cards match catalogue | Visual review + T-46 | `BLOCKED` |
| Date roles labelled | Visual review | `BLOCKED` |
| No unit-revenue slicing by fare/channel | Interaction review | `BLOCKED` |
| Custom tooltips contain disclosure | T-79 tooltip screenshot | `BLOCKED` |
| Default tooltips disabled | Visual settings review | `BLOCKED` |
| Export template contains disclosure | T-79 export test | `BLOCKED` |
| Mobile layout preserves disclosure | Mobile screenshot | `BLOCKED` |
| Accessibility alt text/tab order | Manual review | `BLOCKED` |
| No severity/sentiment/service-category fields | Model/report review | `BLOCKED` |
| No fact-to-fact cross-filtering | T-44 + interaction review | `BLOCKED` |

## 11. Test execution sequence

1. Freeze the approved reference and schema; record hashes.
2. Build and validate dimensions/flights.
3. Build bookings; run T-19–T-22, T-31, T-53.
4. Build costs; run T-26, T-33, T-39.
5. Build disruptions; run T-18, T-23, T-24, T-61, T-62.
6. Build feedback; run T-25, T-36, T-49.
7. Run structural/referential T-01–T-14, T-47–T-54.
8. Run KPI controls T-28–T-36, T-60.
9. Run reproducibility T-40–T-41.
10. Build the semantic model; run T-37, T-42–T-44.
11. Build the report; run T-45–T-46.
12. Run T-79 on pages, tooltips, exports, screenshots.
13. Review evidence; close defects; record the G5 data-quality and G9 runtime QA results.
14. Do not release until G4, G5, G6–G10, and all gates are satisfied.

## 12. Final preparation review checklist

This checklist is about the preparation sprint, not the airline data tests. It is completed in the final preparation report.

| # | Check | Method | Status |
|---:|---|---|---|
| 1 | All ten authoritative documents read | Read log and source review | `TO VERIFY` |
| 2 | Contract v1.5 is the controlling source | Cross-reference check | `TO VERIFY` |
| 3 | Scope residual corrected and only scope modified | Hash/diff review | `TO VERIFY` |
| 4 | Scope backup exists and original hash recorded | Backup/hash inspection | `TO VERIFY` |
| 5 | Exactly nine engineering documents created | File inventory | `TO VERIFY` |
| 6 | No pre-existing output overwritten | Pre-write inventory | `TO VERIFY` |
| 7 | UTF-8 without BOM and LF | Byte/encoding check | `TO VERIFY` |
| 8 | Exact 21 KPI list preserved | KPI inventory against contract | `TO VERIFY` |
| 9 | Five fact grains and dimension rules preserved | Model cross-check | `TO VERIFY` |
| 10 | AirlineId/AirlineKey stability preserved | Key-rule cross-check | `TO VERIFY` |
| 11 | Reference-version authority preserved | Cross-check against contract/OD-01B | `TO VERIFY` |
| 12 | No invented KPI, airline, fact, or dimension | Cross-check | `TO VERIFY` |
| 13 | Unsupported severity/sentiment/service category not added | Field inventory | `TO VERIFY` |
| 14 | Exact disclosure string preserved | Unicode/string check | `TO VERIFY` |
| 15 | No reference/synthetic data created | Directory inspection | `TO VERIFY` |
| 16 | No Python/Power Query/PBIX/PBIP/DAX artifact created | File inventory | `TO VERIFY` |
| 17 | No approval/date/reviewer/signature invented | Document review | `TO VERIFY` |
| 18 | No Git operation performed | Git status/read-only check | `TO VERIFY` |
| 19 | G3/G4 status unchanged | Ledger cross-check | `TO VERIFY` |
| 20 | QA status separate from document status | Report review | `TO VERIFY` |
| 21 | Cross-document consistency | Keyword/ID review | `TO VERIFY` |
| 22 | Hashes recorded for created/modified files | SHA-256 inventory | `TO VERIFY` |
| 23 | Open decisions marked `OWNER DECISION REQUIRED` where applicable | Marker review | `TO VERIFY` |
| 24 | Work stops before implementation | Final report review | `TO VERIFY` |

## 13. Open decisions and limitations

- Formal OD-01A/OD-01B signatures and dates do not exist.
- `G3-RV-01` is `NOT EXECUTED`; G3 is `NOT STARTED`; G4 is `BLOCKED`.
- Reference data, synthetic data, schema freeze, semantic model, DAX, and report do not exist.
- T-37, T-42–T-46, T-55, and T-79 are blocked by missing runtime/report/OD-14 prerequisites.
- T-72–T-78 are planned, not passed; no reference manifest exists.
- No independent reviewer is assigned.
- Exact tolerances (0.01 USD, 0.1%, one minute) are proposed engineering checks and remain subject to owner approval.
- The report has no severity, sentiment, or service-category field; those views require a contract change.
- No target variance is testable until OD-21 defines targets.
- No Git operation is authorized; version evidence is hash-based until Git is approved.

## 14. Verification checklist for this blueprint

| Check | Status |
|---|---|
| Test states and canonical mapping defined | DOCUMENTED |
| T-01–T-79 coverage mapped | DOCUMENTED |
| Evidence schema and independence rules defined | DOCUMENTED |
| Power BI runtime/disclosure tests separated | DOCUMENTED |
| Release exit criteria defined | DOCUMENTED |
| No test claimed PASS/EXECUTED | VERIFIED |
| No runtime/report evidence exists | VERIFIED BY ABSENCE |
| G9/G10 release authorization | NOT GRANTED |

**End of blueprint.** This document is a QA plan only. It does not execute a test, create evidence, approve a release, or advance a gate.
