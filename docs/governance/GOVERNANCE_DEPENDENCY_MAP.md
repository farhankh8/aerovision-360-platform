# GOVERNANCE DEPENDENCY MAP — AEROVISION 360

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** GD-DM-2026-11-06-001  
**Document Type:** Governance Dependency Map  
**Status:** COMPLETE — READY FOR OWNER REVIEW  
**Prepared:** 2026-11-06  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Dependency Map Overview

This document maps all governance dependencies, decision sequences, and downstream impacts. It shows which decisions must be resolved before others can proceed, and what work is blocked by each unresolved decision.

---

## 2. Critical Dependency Chain (Primary Path)

```
OD-01A signature ──────────────────┐
OD-01B signature ──────────────────┼──→ G3-RV-01 ───────────────┐
OD-04 approval (7 sub-decisions) ──┼──→ Schema freeze ───────────┤
Currency mismatch resolution ──────┤                              │
G3-RV-01 execution ────────────────┤                              ▼
Schema freeze written record ──────┴──────────────────────→ G3 formal approval ──→ G4 written authorization ──→ Data generation ──→ Semantic model build ──→ DAX measures ──→ Report pages ──→ QA tests ──→ Release
Independent reviewer assignment ──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Decision Dependency Matrix

| Decision ID | Decision Name | Depends On | Blocks | Downstream Work Blocked |
|---|---|---|---|---|
| OD-01A | Airline population | None | OD-01B; G3; G4; G3-RV-01; Reference data; All generation | Reference data creation; synthetic data; all pages |
| OD-01B | Airline identity/reference | OD-01A (recommended) | G3-RV-01; Schema freeze; G3; G4; Key map approval | Reference data creation; semantic model relationships |
| OD-04 | Exchange-rate policy | OD-01A/OD-01B (recommended) | FactBookingTransactions; FactOperatingCosts; Page 03 | All financial KPIs; Page 03 visuals |
| OD-04a | Currency scope | OD-04 | Referential integrity for financial facts | Currency conversion; financial fact generation |
| OD-04b | Exchange-rate convention | OD-04 | USD conversion definition | Financial measure accuracy |
| OD-04c | Rate source | OD-04 | ref_exchange_rates.csv creation | Financial fact generation |
| OD-04d | Rate version | OD-04 | Rate versioning/reproducibility | Reference version integrity |
| OD-04e | Missing-date behaviour | OD-04 | Missing-date handling rule | Currency conversion logic |
| OD-04f | Rate-generation methodology | OD-04 | Rate value determination | ref_exchange_rates.csv values |
| G3-RV-01 | Reference version approval | OD-01A; OD-01B; OD-04 | Reference data creation; model refresh | All data generation; Power BI refresh |
| Schema freeze | Schema authorization | OD-01A; OD-01B; critical OD decisions | Power Query/model build | Semantic model stability |
| G3 | Data design formal approval | OD-01A; OD-01B; G3-RV-01; Schema freeze | G4 authorization | All Power BI development |
| G4 | Data generation authorization | G3 APPROVED | All data generation | All dataset creation; all Power BI content |
| Independent reviewer | Reviewer assignment | None | All QA PASS decisions | Gate advancement; release |

---

## 4. Blocked Work by Decision

### 4.1 Work Blocked by OD-01A/OD-01B (Unsigned)

| Work Item | Dependency | Current Status |
|---|---|---|
| Reference data creation (ref_airlines.csv, ref_airline_sources.csv) | OD-01A/OD-01B signed; G3-RV-01 executed | NOT CREATED |
| Reference manifest (data/manifests/reference_versions.csv) | OD-01A/OD-01B signed; G3-RV-01 executed | NOT CREATED |
| Key map (AirlineId → AirlineKey) | OD-01B approved | PROPOSED (not approved) |
| Synthetic data generation | OD-01A/OD-01B; G3; G4 authorized | NOT AUTHORIZED |
| Python pipeline execution | G4 authorized | NOT IMPLEMENTED |
| Power Query M execution | G4 authorized | NOT EXECUTED (2 of 14 tables defined only) |
| Semantic model build | G4 authorized | NOT CREATED (JSON specs exist only) |
| DAX measure implementation | G4 authorized; semantic model built | SPECIFIED (not in live model) |
| Report page build | Semantic model built; DAX measures implemented | NOT BUILT (PBIX blank) |

### 4.2 Work Blocked by OD-04 (Unapproved)

| Work Item | Dependency | Current Status |
|---|---|---|
| FactBookingTransactions builder | OD-04 approved; ref_exchange_rates.csv exists | NOT IMPLEMENTED |
| FactOperatingCosts builder | OD-04 approved; ref_exchange_rates.csv exists | NOT IMPLEMENTED |
| ref_exchange_rates.csv | OD-04 approved; currency mismatch resolved | NOT CREATED |
| Financial DAX measures (RASK, CASK, Yield, Unit Contribution, etc.) | Financial facts exist; semantic model updated | NOT IMPLEMENTED |
| Page 03 visuals (RV-01 through RV-18) | Financial DAX measures implemented | NOT BUILT |

### 4.3 Work Blocked by Missing Independent Reviewer

| Work Item | Dependency | Current Status |
|---|---|---|
| All QA test PASS decisions | Independent reviewer assigned or compensating control executed | 0 of 79 tests PASSED |
| Gate advancement (G3→G4→G10) | Independent reviewer or compensating control documented | BLOCKED |
| Release approval (G10) | All QA tests PASSED with reviewer evidence | NOT STARTED |

---

## 5. Upstream/Downstream Impact by Area

### 5.1 Data Engineering Area

| Upstream Decision | Downstream Work Items | Current Status |
|---|---|---|
| OD-01A/OD-01B signatures | Reference data creation; key map; synthetic data generation | BLOCKED |
| OD-04 approval | FactBookingTransactions; FactOperatingCosts; ref_exchange_rates.csv | BLOCKED |
| G4 authorization | All data generation | BLOCKED |
| Currency mismatch resolution | Referential integrity; financial fact generation | BLOCKED |

### 5.2 Semantic Model Area

| Upstream Decision | Downstream Work Items | Current Status |
|---|---|---|
| OD-01B approval | Key map; DimAirline.ReferenceVersion lineage | BLOCKED |
| OD-04 approval | Financial fact relationships; currency dimensions | BLOCKED |
| Schema freeze authorization | Power Query/model build without rework risk | BLOCKED |
| G4 authorization | Semantic model build in Power BI | BLOCKED |

### 5.3 Power BI/Reporting Area

| Upstream Decision | Downstream Work Items | Current Status |
|---|---|---|
| G3 formal approval | Report page build | BLOCKED |
| G4 authorization | Power BI model load; visual creation | BLOCKED |
| OD-04 approval | Page 03 visuals (financial) | BLOCKED |
| OP05 (ref_aircraft_availability.csv) | Page 02 OP05 KPI card | BLOCKED (separate from OD-04) |
| Turnaround Time (aircraft sequence data) | Page 02 V3 Turnaround Time | BLOCKED (replaced with Block Minutes) |

### 5.4 QA/Testing Area

| Upstream Decision | Downstream Work Items | Current Status |
|---|---|---|
| Independent reviewer assignment | All QA test PASS decisions | BLOCKED |
| G3 formal approval | T-01 through T-79 execution | BLOCKED |
| G4 authorization | Power BI runtime validation (T-37, T-46, T-79) | BLOCKED |
| Report pages built | T-45/T-46 report KPI reconciliation | BLOCKED |

---

## 6. Parallel Work Streams (No Governance Blocker)

The following work can proceed without waiting for governance decisions because it uses existing verified data and does not require schema changes, data generation, or financial facts:

| Work Item | Current Status | Governance Dependency |
|---|---|---|
| Page 02 visual build (OP01–OP04 KPI cards; V1–V6) | SPECIFICATION COMPLETE | None (uses existing fact_flight_operations data) |
| Page 04 visual build (CF01–CF03 cards) | SPECIFICATION COMPLETE | None (uses existing fact_customer_feedback data) |
| Page 05 visual build (ASK, RPK, Load Factor visuals) | SPECIFICATION COMPLETE | None (uses existing fact_flight_operations data) |
| Page 06 visual build (DS01–DS03 visuals) | SPECIFICATION COMPLETE | None (uses existing fact_disruptions data) |
| DAX measure fixes (DS03 bug; FL04 boolean SUM; percentage formatting) | SPECIFIED in AEROVISION360_Measures.dax | None (can be implemented in live model once opened) |
| Power Query M completion (all 14 tables) | SPECIFIED in AEROVISION360_DataLoad.m | None (can be implemented once PBIX opened) |

---

## 7. Critical Path Duration Estimate

| Phase | Activities | Active Hours | Elapsed Time |
|---|---|---|---|
| Phase A — Governance Closure | OD-01A/OD-01B signatures; OD-04 approval; G3-RV-01; schema freeze; G3 approval; G4 authorization; reviewer assignment | 16–24 | 4–8 weeks (approval/waiting) |
| Phase B — Non-Blocked Page Build | Page 02, 04, 05, 06 visual build; DAX fixes; Power Query completion | 64–96 | 2–3 weeks (can proceed after G4) |
| Phase C — Data Engineering | ref_aircraft_availability.csv; ref_exchange_rates.csv; FactBookingTransactions; FactOperatingCosts; manifests | 64–96 | 2–3 weeks (after G4) |
| Phase D — Page 03 Build | Financial DAX measures; Page 03 visuals | 40–56 | 1–2 weeks (after Phase C) |
| Phase E — QA and Testing | All 79 tests with independent reviewer | 56–80 | 1–2 weeks |
| Phase F — Deployment | Release packaging; case study; G10 approval | 24–40 | 1 week |

**Total estimated elapsed time:** 11–19 weeks (plus 4–8 weeks approval/waiting in Phase A)

---

## 8. Risk of Non-Approval by Decision

| Decision | Risk if Not Approved | Impact Level |
|---|---|---|
| OD-01A | No airline population; no reference data; project stalled | CRITICAL |
| OD-01B | No key map; no reference version integrity; no reproducible generation | CRITICAL |
| OD-04 | Page 03 cannot be built; no financial analysis | HIGH |
| OD-04a | Currencies without exchange rates quarantined; referential integrity failures | HIGH |
| G3-RV-01 | No approved reference version; mixed-version risk | HIGH |
| Schema freeze | Schema drift; conflicting definitions; rework required | MEDIUM |
| G3 | Project stalled at design phase; no G4 authorization | CRITICAL |
| G4 | No data generation; no Power BI data | CRITICAL |
| Independent reviewer | No QA PASS decisions; no gate advancement | CRITICAL |

---

## 9. End of Dependency Map

This document is dependency-map evidence only. No source files, data, DAX, PBIX, or report pages were modified during its creation. All dependencies reflect the current project state as documented in the master audit deliverables.
