# MASTER PROJECT REMAINING ROADMAP — AEROVISION 360

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Audit Reference:** docs/MASTER_PROJECT_AUDIT_AEROVISION_360.md
**Prepared:** 2026-11-06
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Executive Summary

This roadmap identifies the remaining work to take AEROVISION 360 from its current state (15% complete, design and preparation phase) to a production-ready portfolio release.

**Critical finding: The project cannot proceed to data generation or report building until governance gates are cleared.** G2 (Scope) is the only passed gate. G3 (Data Design) is not formally approved. G4 (Data Generation) is blocked. No synthetic data has been generated beyond the 5,000-flight validation volume. No Power BI report pages have been built.

The roadmap is organized into:
1. Critical blockers (must resolve before anything else)
2. High-priority issues (block specific pages/KPIs)
3. Medium-priority improvements (quality and completeness)
4. Remaining dashboard pages (Pages 03–06)
5. Required data engineering
6. Required governance approvals
7. Final testing and QA
8. Deployment and publication

Each task specifies dependencies and acceptance criteria.

---

## 2. Critical Blockers (Must Resolve Before Any Implementation)

These blockers prevent ALL downstream work. No data generation, no semantic model, no report building, no DAX implementation can proceed until these are resolved.

| ID | Blocker | Current Status | Dependency | Acceptance Criteria |
|---|---|---|---|---|
| B-01 | OD-01A formal signature | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE PENDING | None (owner decision) | Signed OD-01A decision record with approval date |
| B-02 | OD-01B formal signature | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE PENDING | None (owner decision) | Signed OD-01B decision record with approval date |
| B-03 | OD-04 formal approval | PROPOSED — OWNER APPROVAL REQUIRED | OD-01A/OD-01B | Signed OD-04 decision record covering all 7 sub-decisions |
| B-04 | Currency set mismatch | OD-04 lists 5 currencies; DimCurrency has 8 | OD-04 approval | Documented resolution aligning currency sets |
| B-05 | G3-RV-01 reference version | NOT EXECUTED | OD-01A/OD-01B approval | Approved reference manifest and key map |
| B-06 | Schema freeze | NOT AUTHORIZED | Critical OD decisions | Written schema freeze record with hash |
| B-07 | G3 formal approval | NOT FORMALLY APPROVED | B-01 through B-06 | Gate review APPROVED |
| B-08 | G4 written authorization | NOT AUTHORIZED | G3 APPROVED | Written G4 authorization recorded |
| B-09 | Independent reviewer | NOT AVAILABLE | None (project owner decision) | Named reviewer assigned for QA PASS decisions |

**All 9 critical blockers must be resolved before Phase 1 (reference data) can begin.**

---

## 3. High-Priority Issues (Block Specific Pages or KPIs)

| ID | Issue | Affected Page(s) | Affected KPIs/Visuals | Resolution |
|---|---|---|---|---|
| H-01 | FactBookingTransactions does not exist | Page 03 — Revenue & Finance | Total Revenue, Passenger Revenue, Yield, RASK, CASK, Unit Contribution, Refund Rate, Booking Lead Time, Repeat Booking Rate, Fare Mix, Channel Mix | Build FactBookingTransactions after OD-04 approval and exchange rates exist |
| H-02 | FactOperatingCosts does not exist | Page 03 — Revenue & Finance | Operating Cost, CASK, Unit Contribution | Build FactOperatingCosts after OD-04 approval and exchange rates exist |
| H-03 | ref_exchange_rates.csv does not exist | Page 03 — Revenue & Finance | All financial KPIs requiring USD conversion | Create exchange rate reference after OD-04 approval |
| H-04 | ref_aircraft_availability.csv does not exist | Page 02 — Operations Performance | OP05 — Aircraft Utilization | Create reference after OD-10 approval |
| H-05 | Aircraft rotation/sequence data missing | Page 02 — Operations Performance | V3 — Turnaround Time | Replaced with Block Minutes by Airline/Month (specification complete) |
| H-06 | Power Query M incomplete | All pages | All data refresh | Define all 14 tables in AEROVISION360_DataLoad.m (currently only 2) |
| H-07 | semantic_model.json incomplete | All pages | All model relationships | Add missing dimensions and relationships |
| H-08 | DS03 DAX expression bug | Page 06 — Disruption & Risk | DS03 — Controllable Disruptions | Fix to count fact events, not dimension rows |
| H-09 | FL04 boolean SUM risk | Page 01 — Executive Overview | FL04 — Cancellation Rate | Replace SUM with COUNTROWS on boolean |
| H-10 | Percentage formatting ambiguity | Page 01 — Executive Overview | FL04, CF03 | Document whether values are fractions or percentage points |

---

## 4. Medium-Priority Improvements

| ID | Improvement | Affected Area | Rationale |
|---|---|---|---|
| M-01 | Complete test execution (T-01 to T-79) | QA / Governance | 0 of 79 tests executed; no PASS decisions possible |
| M-02 | Add data-quality defect documentation | Data Engineering | Controlled defects should be documented per contract |
| M-03 | Complete reference data layer | Data Engineering | All ref_* CSVs missing except airline workbook |
| M-04 | Increase flight volume to target range | Data Engineering | Current 5,000 rows is validation volume; target is 150K–250K |
| M-05 | Add dataset manifests for all curated tables | Data Engineering | Manifests with SHA-256 hashes and reconciliation totals |
| M-06 | Document data lineage | Data Engineering | No automated lineage tracking exists |
| M-07 | Complete Power BI report pages | Reporting | Pages 01, 02, 04, 05, 06 designed but not built; Page 03 blocked |
| M-08 | Build drill-through pages | Reporting | DRL-Airline, DRL-Route, DRL-Flight, DRL-Feedback not built |
| M-09 | Add mobile layout | Reporting | Mobile layout not designed or built |
| M-10 | Add export validation | Reporting | Export disabled until T-79 passes |

---

## 5. Remaining Dashboard Pages

### Page 03 — Revenue & Finance (BLOCKED)

**Readiness: 5%** — Specification exists; no data; no measures; no visuals.

| Remaining Work | Dependencies | Acceptance Criteria |
|---|---|---|
| Approve OD-04 (all 7 sub-decisions) | OD-01A/OD-01B | Signed decision record |
| Resolve currency set mismatch (5 vs 8) | OD-04 approval | Documented resolution |
| Create ref_exchange_rates.csv | OD-04 approval; currency resolution | Owner-approved synthetic rates; manifest hash |
| Build FactBookingTransactions | OD-04 approval; exchange rates; G4 authorization | Loaded to curated layer; manifest; reconciliation |
| Build FactOperatingCosts | OD-04 approval; exchange rates; G4 authorization | Loaded to curated layer; manifest; reconciliation |
| Add financial fact relationships to semantic model | Financial facts loaded | Relationships complete; no fact-to-fact paths |
| Implement financial DAX measures | Semantic model complete | RASK, CASK, Yield, Unit Contribution, etc. verified |
| Build Page 03 visuals (RV-01 through RV-18) | DAX measures implemented | All 18 visuals rendered; disclosure visible |
| Execute Page 03 QA tests | Report built; independent reviewer | All applicable tests PASSED |

### Page 04 — Customer Intelligence (READY TO BUILD)

**Readiness: 15%** — Design specified; DAX measures CF01–CF03 available; source data exists.

| Remaining Work | Dependencies | Acceptance Criteria |
|---|---|---|
| Build Page 04 visuals in Power BI Desktop | Semantic model; DAX measures | CS-01 through CS-14 rendered; disclosure visible |
| Execute Page 04 QA tests | Report built; independent reviewer | All applicable tests PASSED |

### Page 05 — Route & Network Intelligence (READY TO BUILD)

**Readiness: 15%** — Design specified; DAX measures (ASK, RPK, Load Factor) derivable; source data exists.

| Remaining Work | Dependencies | Acceptance Criteria |
|---|---|---|
| Build Page 05 visuals in Power BI Desktop | Semantic model; DAX measures | NW-01 through NW-12 rendered; map fallback if unavailable |
| Execute Page 05 QA tests | Report built; independent reviewer | All applicable tests PASSED |

### Page 06 — Disruption & Risk Analytics (READY TO BUILD)

**Readiness: 15%** — Design specified; DAX measures DS01–DS03 available; source data exists.

| Remaining Work | Dependencies | Acceptance Criteria |
|---|---|---|
| Build Page 06 visuals in Power BI Desktop | Semantic model; DAX measures | OP-09 through OP-14 rendered; disclosure visible |
| Execute Page 06 QA tests | Report built; independent reviewer | All applicable tests PASSED |

### Page 01 — Executive Overview (PARTIALLY BUILT)

**Readiness: 20%** — Design specified; DAX measures FL01–FL04 available; some issues to fix.

| Remaining Work | Dependencies | Acceptance Criteria |
|---|---|---|
| Fix DS03 DAX expression | None | Counts fact events, not dimension rows |
| Fix FL04 boolean SUM | None | Uses COUNTROWS on boolean |
| Clarify percentage formatting | None | Documented convention |
| Build Page 01 visuals in Power BI Desktop | Semantic model; DAX measures | EX-01 through EX-12 rendered; disclosure visible |
| Execute Page 01 QA tests | Report built; independent reviewer | All applicable tests PASSED |

### Page 02 — Operations Performance (PARTIALLY BUILT)

**Readiness: 25%** — Design specified; DAX measures OP01–OP04 verified; V3 replaced with Block Minutes.

| Remaining Work | Dependencies | Acceptance Criteria |
|---|---|---|
| Build Page 02 visuals in Power BI Desktop | Semantic model; DAX measures | KPI cards + V1–V6 rendered; disclosure visible |
| Execute Page 02 QA tests | Report built; independent reviewer | All 27 tests PASSED |

---

## 6. Required Data Engineering

| ID | Task | Dependencies | Acceptance Criteria |
|---|---|---|---|
| DE-01 | Create ref_aircraft_availability.csv | OD-10 approval | One row per aircraft per date per version; validated statuses/hours |
| DE-02 | Create ref_exchange_rates.csv | OD-04 approval; currency resolution | One row per currency per date; owner-approved rates |
| DE-03 | Build FactBookingTransactions | OD-04 approval; exchange rates; G4 authorization | Loaded to curated; row count reconciled; manifest created |
| DE-04 | Build FactOperatingCosts | OD-04 approval; exchange rates; G4 authorization | Loaded to curated; row count reconciled; manifest created |
| DE-05 | Complete Power Query M for all 14 tables | Curated data available | All 14 tables defined; error handling; duplicate prevention |
| DE-06 | Complete semantic_model.json relationships | Financial facts loaded | All dimensions and facts related correctly; no fact-to-fact paths |
| DE-07 | Increase flight volume to target range | G4 authorization; generator foundation | 150K–250K flight legs (or documented justification for different volume) |
| DE-08 | Add dataset manifests for all curated tables | Curated data available | SHA-256 hashes; row counts; reconciliation totals |
| DE-09 | Document data lineage | All data layers | Lineage traceable from RAW to CURATED to Power BI |

---

## 7. Required Governance Approvals

| ID | Approval | Owner | Dependencies | Acceptance Criteria |
|---|---|---|---|---|
| GA-01 | OD-01A signature | Project Owner | None | Signed decision record with date |
| GA-02 | OD-01B signature | Project Owner | None | Signed decision record with date |
| GA-03 | OD-04 formal approval | Project Owner | OD-01A/OD-01B | Signed decision covering all 7 sub-decisions |
| GA-04 | OD-05 through OD-22 decisions | Project Owner | OD-01A/OD-01B | Recorded decisions with rationale |
| GA-05 | G3-RV-01 execution | Project Owner / QA | OD-01A/OD-01B; critical decisions | Approved manifest; key map; T-75/T-76/T-78 evidence |
| GA-06 | Schema freeze | Project Owner | Critical OD decisions | Written freeze record with hash |
| GA-07 | G3 formal approval | Gate review | GA-01 through GA-06 | Gate review APPROVED |
| GA-08 | G4 written authorization | Project Owner | G3 APPROVED | Written authorization recorded |
| GA-09 | Independent reviewer assignment | Project Owner | None | Named reviewer for QA PASS decisions |

---

## 8. Final Testing and QA

| ID | Test | Dependencies | Acceptance Criteria |
|---|---|---|---|
| QT-01 | T-01 to T-14 (Structural/referential) | Semantic model; curated data | All PASSED with reviewer evidence |
| QT-02 | T-15 to T-36 (Business/financial) | Financial facts; DAX measures | All PASSED with reviewer evidence |
| QT-03 | T-37 (Zero-denominator) | Power BI model; rendered report | PASSED with reviewer evidence |
| QT-04 | T-38 to T-39 (Rollups) | Semantic model; DAX measures | All PASSED with reviewer evidence |
| QT-05 | T-40 to T-46 (Reproducibility/report) | Rendered report; PBIX | All PASSED with reviewer evidence |
| QT-06 | T-47 to T-55 (Business/financial) | Financial facts; DAX measures | All PASSED with reviewer evidence |
| QT-07 | T-56 to T-71 (Reference/quality) | Reference data; curated data | All PASSED with reviewer evidence |
| QT-08 | T-72 to T-78 (Airline identity) | Reference data; DimAirline | All PASSED with reviewer evidence |
| QT-09 | T-79 (Disclosure) | Rendered report; tooltips; exports | PASSED — disclosure visible on all pages, tooltips, exports |
| QT-10 | Performance and accessibility testing | Rendered report | Acceptable refresh time; WCAG compliance |

---

## 9. Deployment and Publication

| ID | Task | Dependencies | Acceptance Criteria |
|---|---|---|---|
| DP-01 | Package release artifacts | All gates passed; all tests PASSED | Setup documentation; release checklist; reproducibility instructions |
| DP-02 | Privacy review (no PII/secrets) | All data layers | Repository review confirms no real passenger PII |
| DP-03 | Portfolio case study | All report pages built; QA complete | Case study with disclosure on every page |
| DP-04 | Final gate review (G10) | All previous gates; all tests PASSED | G10 APPROVED |
| DP-05 | Publication | G10 APPROVED | Report published; disclosure present on all artifacts |

---

## 10. Implementation Sequence (Prioritized)

### Phase A: Governance Closure (Weeks 1–4, elapsed)
1. GA-01: OD-01A signature
2. GA-02: OD-01B signature
3. GA-03: OD-04 formal approval (all 7 sub-decisions)
4. GA-04: OD-05 through OD-22 decisions
5. GA-05: G3-RV-01 execution
6. GA-06: Schema freeze
7. GA-07: G3 formal approval
8. GA-08: G4 written authorization
9. GA-09: Independent reviewer assignment

### Phase B: Non-Blocked Page Build (Can proceed in parallel with reference data preparation)
10. Build Page 02 visuals (OP01–OP04 KPI cards, V1, V2, V3 Block Minutes, V4, V5, V6)
11. Build Page 04 visuals (CS-01 through CS-14)
12. Build Page 05 visuals (NW-01 through NW-12; map fallback if unavailable)
13. Build Page 06 visuals (OP-09 through OP-14)
14. Fix DS03 DAX expression (counts fact events)
15. Fix FL04 boolean SUM (uses COUNTROWS)
16. Clarify percentage formatting convention

### Phase C: Data Engineering (After G4 authorization)
17. DE-01: Create ref_aircraft_availability.csv
18. DE-02: Create ref_exchange_rates.csv
19. DE-03: Build FactBookingTransactions
20. DE-04: Build FactOperatingCosts
21. DE-05: Complete Power Query M for all 14 tables
22. DE-06: Complete semantic_model.json relationships
23. DE-07: Increase flight volume to target range
24. DE-08: Add dataset manifests
25. DE-09: Document data lineage

### Phase D: Page 03 Build (After financial facts exist)
27. Implement financial DAX measures (RASK, CASK, Yield, Unit Contribution, etc.)
28. Build Page 03 visuals (RV-01 through RV-18)
29. Add OP05 Aircraft Utilization (after ref_aircraft_availability.csv)

### Phase E: QA and Testing (After all pages built)
30. QT-01 through QT-10 execution with independent reviewer
31. Defect closure and re-test

### Phase F: Deployment (After all tests PASSED)
32. DP-01 through DP-05 execution
33. G10 final gate review

---

## 11. Dependencies Summary

```
OD-01A/B signatures ──→ G3-RV-01 ──→ Schema freeze ──→ G3 approval ──→ G4 authorization
                                                      ↓                                         ↓
                                          Reference data creation ────→ Data generation
                                                      ↓                                         ↓
                                          Semantic model completion ────→ Power BI model build
                                                      ↓                                         ↓
                                          DAX measure implementation ────→ Report page build
                                                      ↓                                         ↓
                                          QA test execution ────────────→ Defect closure
                                                      ↓                                         ↓
                                          Release packaging ─────────────→ G10 approval
                                                      ↓                                         ↓
                                          Publication ─────────────────────→ Project complete
```

**Critical path: OD-01A/OD-01B → OD-04 → G3-RV-01 → Schema freeze → G3 → G4 → Data generation → Model → DAX → Reports → QA → Release**

**Parallel path: Page 02, 04, 05, 06 design and visual build can proceed once semantic model has the 3 existing facts and 10 measures.**

---

## End of Roadmap

This document is roadmap evidence only. No source files, data, DAX, PBIX, or report pages were modified during its creation. No implementation is authorized until the critical blockers in Section 2 are resolved.
