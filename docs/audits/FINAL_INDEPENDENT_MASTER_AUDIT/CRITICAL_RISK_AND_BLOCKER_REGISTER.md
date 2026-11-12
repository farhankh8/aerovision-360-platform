# CRITICAL RISK AND BLOCKER REGISTER

**Source:** MASTER_PROJECT_BLOCKERS_REGISTER.md (2026-11-06), OD-01A/01B/04, PROGRESS_LEDGER.md, phase audits  
**Status:** All 18 blockers open (0 resolved); some high-priority claims are STALE relative to current DAX/model (corrected in Phase J)  
**Audit mode:** Read-only. No blocker resolved or approved.

---

## 1. Critical blockers (CB-01 to CB-09) — gating, all open

| ID | Blocker | Status | Blocks | Owner decision required? | Acceptance criteria |
|---|---|---|---|---|---|
| CB-01 | OD-01A — airline population formal signature | OWNER-CONFIRMED — signature pending | G3, reference data, all data generation, all pages | Yes — Project Owner | Signed OD-01A with approval date |
| CB-02 | OD-01B — airline identity/reference formal signature | OWNER-CONFIRMED — signature pending | G3-RV-01, key map, reference data | Yes — Project Owner | Signed OD-01B with approval date |
| CB-03 | OD-04 — exchange-rate policy formal approval | PROPOSED — owner approval required | FactBookingTransactions, FactOperatingCosts, Page 03/04 financials | Yes — Owner (7 sub-decisions) | Signed OD-04 covering currency scope, convention, rate source, version, missing-date behavior, methodology |
| CB-04 | Currency set mismatch | OD-04 lists 5 (USD,EUR,GBP,JPY,CAD); DimCurrency has 8 (AED,QAR,SGD,INR,GBP,EUR,USD,AUD) | Referential integrity for financial facts | Yes — Owner (OD-04a) | Documented resolution aligning currency sets (recommend: expand OD-04 to all 8) |
| CB-05 | G3-RV-01 — reference-version approval | NOT EXECUTED | Reference data creation, model refresh, version-pinned generation | Yes — Owner/QA | Approved reference manifest + key map; T-75/T-76/T-78 evidence |
| CB-06 | Schema freeze | NOT AUTHORIZED | Power Query/model build; rework risk | Yes — Project Owner | Written schema-freeze record with contract/schema hash |
| CB-07 | G3 — formal gate approval | NOT FORMALLY APPROVED | G4 data generation authorization | Yes — Gate review | Gate review APPROVED |
| CB-08 | G4 — written data generation authorization | NOT AUTHORIZED | All data generation (reference, synthetic, financial) | Yes — Project Owner | Written G4 authorization recorded |
| CB-09 | Independent reviewer assignment | NOT AVAILABLE | All QA PASS decisions (tests executed but not PASSED) | Yes — Project Owner | Named reviewer for test PASS decisions |

**All 9 critical blockers open. Zero resolved.**

---

## 2. High-priority blockers (HB-01 to HB-10) — corrected for current evidence

| ID | Blocker | Status | Affected | Resolution required | Notes (correction) |
|---|---|---|---|---|---|
| HB-01 | FactBookingTransactions not loaded to model | Blocked by OD-04 | Page 03 financials | Build after OD-04 + exchange rates | Source CSV exists; not model-loaded |
| HB-02 | FactOperatingCosts not loaded to model | Blocked by OD-04 | Page 03 financials | Build after OD-04 + exchange rates | Source CSV exists; not model-loaded |
| HB-03 | ref_exchange_rates.csv does not exist | Blocked by OD-04 | Page 03/04 financials | Create after OD-04 approval | — |
| HB-04 | ref_aircraft_availability.csv does not exist | Not created | Page 02 OP05 | Create after domain OD approval | — |
| HB-05 | Power Query "incomplete (2 of 14)" | STALE — incorrect | — | — | **Corrected:** Power Query defines 16 of 16 tables. Not a current blocker. |
| HB-06 | semantic_model.json "incomplete" | STALE — incorrect | — | — | **Corrected:** 16 tables, 51 measures documented; only OP01/03/OP04 registration gap remains (see C-01). |
| HB-07 | DS03 "counts dimension rows (3 instead of 540)" | STALE — incorrect | Page 06 (doesn't exist) | — | **Corrected:** Current DS03 = COUNTROWS(FILTER(RELATED(dim_disruption_type[ControllableFlag])=TRUE())) — correct pattern; Page 06 does not exist in the 5-page report. |
| HB-08 | FL04 "uses SUM on boolean" | STALE — incorrect | Page 01 FL04 | — | **Corrected:** Current FL04 uses COUNTROWS + DIVIDE with BLANK() guard — correct pattern. |
| HB-09 | Percentage formatting ambiguity (FL04/CF03 ×100) | OPEN | Page 01/04 | Document fraction vs percentage-point | Genuine formatting documentation need |
| HB-10 | OP01/OP03/OP04 missing from model.json | OPEN | Page 02 | Register 3 measures | Genuine registration gap |

**Genuine high-priority items remaining:** HB-01, HB-02, HB-03, HB-04, HB-09, HB-10. HB-05–HB-08 are stale and corrected.

---

## 3. Medium-priority blockers (MB-01 to MB-10)

| ID | Blocker | Status | Rationale |
|---|---|---|---|
| MB-01 | No QA tests executed / 0 PASS | OPEN | 79 tests PLANNED/BLOCKED; no PASS without independent reviewer |
| MB-02 | Controlled data-quality defects not documented | OPEN | No defect register executed |
| MB-03 | Reference data layer incomplete | OPEN | ref_airlines, ref_exchange_rates, manifest missing |
| MB-04 | Flight volume below target (5,000 vs 150K–250K) | OPEN | Validation volume only |
| MB-05 | No dataset manifests for curated tables | OPEN | Contract requires SHA-256, row counts, reconciliation totals |
| MB-06 | No automated data lineage | OPEN | RAW→CURATED→Power BI traceability missing |
| MB-07 | Power BI pages "not built" | STALE — incorrect | **Corrected:** 5 pages / 120 visuals built in main PBIX. |
| MB-08 | Drill-through pages not built | OPEN | DRL-* pages specified, not implemented |
| MB-09 | Mobile layout not built | OPEN | Not implemented |
| MB-10 | Export validation not done | OPEN | T-79 blocked; no export template |

**Genuine medium items:** MB-01, MB-02, MB-03, MB-04, MB-05, MB-06, MB-08, MB-09, MB-10. MB-07 stale (corrected).

---

## 4. Risk of non-resolution

| Blocker | Consequence if not resolved |
|---|---|
| CB-01/CB-02 | No airline population authorization; no reference data; no data generation; project cannot proceed |
| CB-03/CB-04 | Page 03/04 permanently blocked; no financial KPIs; referential integrity failures |
| CB-05 | No approved reference version; mixed-version risk; no reproducible generation |
| CB-06 | Schema drift; conflicting definitions; rework required |
| CB-07 | G4 cannot be authorized; stalled at design phase |
| CB-08 | No data generation; no synthetic datasets; no Power BI data |
| CB-09 | No QA PASS decisions; no gate advancement; no release |
| PROD-01 | No current backup of main PBIX; cannot recover current report |

---

## 5. Blocker dependency chain

```
CB-01 (OD-01A signature) ──┐
CB-02 (OD-01B signature) ──┼──→ CB-05 (G3-RV-01) ──→ CB-06 (schema freeze) ──→ CB-07 (G3 approval) ──→ CB-08 (G4 authorization) ──→ data generation ──→ model load → QA → release
CB-03 (OD-04 approval) ──┘
CB-04 (currency mismatch) ──┘
CB-09 (independent reviewer) ────────────────────────────────────────────→ needed for QA PASS
```

Root of the chain: **CB-01 / CB-02 (OD-01A/OD-01B signatures)**. Nothing downstream can proceed until these are signed.
