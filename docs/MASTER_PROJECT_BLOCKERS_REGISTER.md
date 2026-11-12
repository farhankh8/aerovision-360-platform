# MASTER PROJECT BLOCKERS REGISTER — AEROVISION 360

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform
**Audit Reference:** docs/MASTER_PROJECT_AUDIT_AEROVISION_360.md
**Prepared:** 2026-11-06
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance

---

## 1. Blocker Summary

| Total Blockers | Critical | High | Medium | Resolved | Open |
|---|---|---|---|---|---|
| 18 | 9 | 6 | 3 | 0 | 18 |

**No blockers have been resolved. All 18 are open.**

---

## 2. Critical Blockers (Gating — Must Resolve Before Any Implementation)

| ID | Blocker | Current Status | Impact | Owner Decision Required | Acceptance Criteria |
|---|---|---|---|---|---|
| CB-01 | OD-01A — Airline population formal signature | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE PENDING | Blocks G3, reference data, all data generation, all pages | Yes — Project Owner | Signed OD-01A decision record with approval date |
| CB-02 | OD-01B — Airline identity/reference formal signature | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE PENDING | Blocks G3-RV-01, reference data, key map approval | Yes — Project Owner | Signed OD-01B decision record with approval date |
| CB-03 | OD-04 — Exchange-rate policy formal approval | PROPOSED — OWNER APPROVAL REQUIRED | Blocks FactBookingTransactions, FactOperatingCosts, Page 03 (all 18 financial visuals) | Yes — Project Owner (7 sub-decisions) | Signed OD-04 decision record covering currency scope, convention, rate source, rate version, missing-date behavior, rate-generation methodology, downstream implications |
| CB-04 | Currency set mismatch | OD-04 lists 5 currencies (USD, EUR, GBP, JPY, CAD); DimCurrency has 8 (AED, QAR, SGD, INR, GBP, EUR, USD, AUD) | Blocks referential integrity for financial facts; currencies without rates would be quarantined | Yes — Project Owner (OD-04a) | Documented resolution aligning currency sets (recommended: expand OD-04 to all 8 DimCurrency currencies) |
| CB-05 | G3-RV-01 — Reference version approval | NOT EXECUTED | Blocks reference data creation, model refresh, version-pinned generation | Yes — Project Owner / QA | Approved reference manifest and key map; T-75/T-76/T-78 evidence |
| CB-06 | Schema freeze | NOT AUTHORIZED | Blocks Power Query/model build; risks rework and conflicting definitions | Yes — Project Owner | Written schema freeze record with contract/schema hash |
| CB-07 | G3 — Formal gate approval | NOT FORMALLY APPROVED | Blocks G4 data generation authorization | Yes — Gate review | Gate review APPROVED |
| CB-08 | G4 — Written data generation authorization | NOT AUTHORIZED | Blocks all data generation (reference data, synthetic data, financial facts) | Yes — Project Owner | Written G4 authorization recorded |
| CB-09 | Independent reviewer assignment | NOT AVAILABLE | Blocks all QA PASS decisions (tests remain EXECUTED, not PASSED) | Yes — Project Owner | Named reviewer assigned for test PASS decisions |

**All 9 critical blockers are open. Zero are resolved.**

---

## 3. High-Priority Blockers (Block Specific Pages or KPIs)

| ID | Blocker | Current Status | Affected Page(s) | Affected KPIs / Visuals | Resolution Required |
|---|---|---|---|---|---|
| HB-01 | FactBookingTransactions does not exist | DOES NOT EXIST — blocked by OD-04 | Page 03 — Revenue & Finance | Total Revenue, Passenger Revenue, Yield, RASK, CASK, Unit Contribution, Refund Rate, Booking Lead Time, Repeat Booking Rate, Fare Class Mix, Channel Mix, Ancillary Revenue per Passenger | Build FactBookingTransactions after OD-04 approval and exchange rates exist |
| HB-02 | FactOperatingCosts does not exist | DOES NOT EXIST — blocked by OD-04 | Page 03 — Revenue & Finance | Operating Cost, CASK, Unit Contribution | Build FactOperatingCosts after OD-04 approval and exchange rates exist |
| HB-03 | ref_exchange_rates.csv does not exist | DOES NOT EXIST — blocked by OD-04 | Page 03 — Revenue & Finance | All financial KPIs requiring USD conversion | Create exchange rate reference after OD-04 approval |
| HB-04 | ref_aircraft_availability.csv does not exist | DOES NOT EXIST — not created | Page 02 — Operations Performance | OP05 — Aircraft Utilization (K-13) | Create reference after OD-10 approval |
| HB-05 | Aircraft rotation/sequence data missing | DOES NOT EXIST | Page 02 — Operations Performance | V3 — Turnaround Time | Replaced with Block Minutes by Airline/Month (specification complete — no further action needed) |
| HB-06 | Power Query M incomplete | Defines only 2 of 14 tables | All pages | All data refresh and model loading | Define all 14 tables in AEROVISION360_DataLoad.m |
| HB-07 | semantic_model.json incomplete | Missing dimensions; incomplete relationship list | All pages | All model relationships and measure expressions | Add missing dimensions (dim_aircraft, dim_airport, dim_customer, dim_disruption_type, dim_date for disruptions/feedback); complete relationship list; add measure expressions |
| HB-08 | DS03 DAX expression bug | Counts dimension rows instead of fact events | Page 06 — Disruption & Risk Analytics | DS03 — Controllable Disruptions (shows 3 instead of 540) | Fix DAX to count fact events where related disruption type is controllable |
| HB-09 | FL04 boolean SUM risk | Uses SUM on boolean column | Page 01 — Executive Overview | FL04 — Cancellation Rate | Replace SUM(CancellationFlag) with COUNTROWS(FILTER(CancellationFlag=TRUE)) |
| HB-10 | Percentage formatting ambiguity | FL04 and CF03 multiply by 100; may display incorrectly with Percent format | Page 01 — Executive Overview; Page 04 — Customer Intelligence | FL04, CF03 | Document whether values are fractions (format as Percent) or percentage points (format as Number with % suffix) |

**All 10 high-priority blockers are open. Zero are resolved.**

---

## 4. Medium-Priority Blockers (Quality and Completeness)

| ID | Blocker | Current Status | Affected Area | Rationale |
|---|---|---|---|---|
| MB-01 | No QA tests executed | 79 tests all PLANNED or BLOCKED; 0 PASSED | QA / Governance | No PASS decisions possible without execution and independent reviewer evidence |
| MB-02 | Controlled data-quality defects not documented | Design documents exist; no defect register executed | Data Engineering | Contract requires intentional defects to be documented and testable |
| MB-03 | Reference data layer nearly empty | Only airline reference workbook exists; all ref_* CSVs missing | Data Engineering | All reference datasets (airlines, sources, airports, aircraft types, currencies, etc.) missing |
| MB-04 | Flight volume below target | 5,000 rows (validation volume); target is 150K–250K | Data Engineering | Current volume is for validation only; full portfolio volume requires confirmation |
| MB-05 | No dataset manifests | Manifests missing for curated tables | Data Engineering | Contract requires manifests with SHA-256 hashes, row counts, reconciliation totals |
| MB-06 | No automated data lineage | No lineage tracking exists | Data Engineering | Contract requires traceability from RAW to CURATED to Power BI |
| MB-07 | Power BI report pages not built | PBIX exists but effectively blank (one blank page) | Reporting | Pages 01, 02, 04, 05, 06 designed but not built; Page 03 blocked |
| MB-08 | Drill-through pages not built | DRL-Airline, DRL-Route, DRL-Flight, DRL-Feedback not designed/built | Reporting | Drill-through pages specified but not implemented |
| MB-09 | Mobile layout not built | No mobile layout designed | Reporting | Mobile layout specified in design system but not implemented |
| MB-10 | Export validation not done | Export disabled until T-79 passes | Reporting | No export template with disclosure; no Excel/PDF/ PowerPoint export validation |

**All 10 medium-priority blockers are open. Zero are resolved.**

---

## 5. Blocker Dependency Chain

```
CB-01 (OD-01A signature) ──┐
CB-02 (OD-01B signature) ──┼──→ CB-05 (G3-RV-01) ──→ CB-06 (Schema freeze) ──→ CB-07 (G3 approval) ──→ CB-08 (G4 authorization) ──→ Data generation ──→ Semantic model → DAX → Reports → QA → Release
CB-03 (OD-04 approval) ──┘                                                        │
CB-04 (Currency mismatch) ──┘                                                      │
CB-09 (Independent reviewer) ──────────────────────────────────────────────────────┘ (needed for QA PASS)

HB-01/HB-02/HB-03 (Financial facts) ──┐
HB-04 (Aircraft availability) ────────┼──→ Dependent on CB-08 (G4 authorization) and domain-specific OD approvals
HB-06/HB-07 (Power Query/Model) ─────┘
HB-08/HB-09/HB-10 (DAX fixes) ────────┴──→ Can be fixed immediately (no gate dependency)
```

---

## 6. Blocker-to-Work-Item Mapping

| Blocker ID | Resolves Work Item(s) |
|---|---|
| CB-01 | All data generation; reference data; G3 |
| CB-02 | G3-RV-01; key map approval; reference data |
| CB-03 | FactBookingTransactions; FactOperatingCosts; Page 03; all financial KPIs |
| CB-04 | Referential integrity for financial facts in all 8 DimCurrency currencies |
| CB-05 | Reference data creation; model refresh version pinning |
| CB-06 | Power Query/model build without rework risk |
| CB-07 | G4 data generation authorization |
| CB-08 | All data generation (reference, synthetic, financial) |
| CB-09 | All QA test PASS decisions |
| HB-01 | Page 03 revenue KPIs and visuals |
| HB-02 | Page 03 cost KPIs and visuals |
| HB-03 | Page 03 currency conversion; all financial KPIs |
| HB-04 | Page 02 OP05 Aircraft Utilization |
| HB-05 | Resolved — V3 replaced with Block Minutes (no further action) |
| HB-06 | All data refresh; model loading |
| HB-07 | All model relationships; measure expressions |
| HB-08 | Page 06 DS03 measure accuracy |
| HB-09 | Page 01 FL04 measure accuracy |
| HB-10 | Page 01 and Page 04 percentage display correctness |

---

## 7. Estimated Effort to Resolve Blockers

| Category | Items | Est. Active Hours | Est. Elapsed Time |
|---|---|---|---|
| Governance approvals (CB-01 to CB-09) | 9 items | 16–24 hours (active) | 4–8 weeks (approval/waiting) |
| High-priority fixes (HB-01 to HB-10) | 10 items | 64–96 hours (after gates) | 2–3 weeks |
| Medium-priority improvements (MB-01 to MB-10) | 10 items | 200–300 hours | 5–8 weeks |
| **Total** | **29 items** | **280–420 hours** | **11–19 weeks (plus 4–8 weeks approval/waiting)** |

---

## 8. Risk of Not Resolving

| Blocker | Consequence of Non-Resolution |
|---|---|
| CB-01 / CB-02 | No airline population authorization; no reference data; no data generation; project cannot proceed |
| CB-03 | Page 03 cannot be built; no financial KPIs; no revenue/cost analysis |
| CB-04 | Referential integrity failures; currencies without rates quarantined; financial data incomplete |
| CB-05 | No approved reference version; mixed-version risk; no reproducible generation |
| CB-06 | Schema drift; conflicting definitions; rework required |
| CB-07 | G4 cannot be authorized; project stalled at design phase |
| CB-08 | No data generation; no synthetic datasets; no Power BI data |
| CB-09 | No QA PASS decisions; no gate advancement; no release |
| HB-01 to HB-03 | Page 03 permanently blocked; no revenue/finance analysis |
| HB-04 | Page 02 missing OP05 KPI card |
| HB-08 | Page 06 DS03 reports incorrect values (3 instead of 540) |
| HB-09 | Page 01 FL04 may display incorrectly |
| HB-10 | Page 01 and Page 04 percentages may display as 448% instead of 4.48% |

---

## End of Blockers Register

This document is blocker-register evidence only. No source files, data, DAX, PBIX, or report pages were modified during its creation. No blocker is resolved; all 18 remain open.
