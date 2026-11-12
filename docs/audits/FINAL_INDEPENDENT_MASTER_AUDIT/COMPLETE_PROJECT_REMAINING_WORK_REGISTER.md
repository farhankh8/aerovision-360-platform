# COMPLETE PROJECT REMAINING WORK REGISTER

**Source:** All phase audits (A–I), blockers register, contradiction reconciliation  
**Register status:** Open items only; completed work is NOT listed here as pending  
**Audit mode:** Read-only

---

## A. Governance approvals (GATING — root dependency chain)

| ID | Remaining work | Dependency | Owner decision required? | Status |
|---|---|---|---|---|
| A-01 | Formal signature + approval date on OD-01A (airline population) | None (root) | Yes — Project Owner | OPEN |
| A-02 | Formal signature + approval date on OD-01B (airline identity/reference) | A-01 | Yes — Project Owner | OPEN |
| A-03 | Formal approval of OD-04 (exchange-rate policy; 7 sub-decisions) | A-01/A-02 | Yes — Project Owner | OPEN |
| A-04 | Resolve OD-04 currency-set mismatch (5 vs 8 currencies) | A-03 | Yes — Project Owner | OPEN |
| A-05 | Execute G3-RV-01 (reference-version approval; manifest + key map + T-75/T-76/T-78) | A-01/A-02/A-03 + schema freeze | Yes — Owner/QA | OPEN |
| A-06 | Schema freeze authorization | A-01/A-02/A-03/A-05 | Yes — Project Owner | OPEN |
| A-07 | G3 formal gate approval | A-01…A-06 | Yes — Gate review | OPEN |
| A-08 | Written G4 data generation authorization | A-07 | Yes — Project Owner | OPEN |
| A-09 | Assign independent reviewer; close compensating control; enable QA PASS decisions | A-01…A-08 | Yes — Project Owner | OPEN |

---

## B. Reference data & data generation (gated by A-01…A-08)

| ID | Remaining work | Dependency | Status |
|---|---|---|---|
| B-01 | Create `ref_airlines.csv`, `ref_airline_sources.csv` | A-05 (G3-RV-01) | BLOCKED |
| B-02 | Create `ref_exchange_rates.csv` (approved rates, all 8 DimCurrency currencies) | A-03/A-04 (OD-04) | BLOCKED |
| B-03 | Create reference manifest `data/manifests/reference_versions.csv` | A-05 | BLOCKED |
| B-04 | Generate synthetic data / curated financial facts (FactBookingTransactions, FactOperatingCosts) | A-08 (G4) + B-02 | BLOCKED |
| B-04b | Load financial facts into Power BI model (add to data_sources.json) | B-04 | BLOCKED |
| B-05 | Create `ref_aircraft_availability.csv` (Page 02 OP05) | Domain OD approval | BLOCKED |

---

## C. Semantic model & DAX closures (NO OD/G4 dependency — can proceed)

| ID | Remaining work | Dependency | Status |
|---|---|---|---|
| C-01 | Register OP01, OP03, OP04 in `semantic_model/model.json` | None | OPEN (can do now) |
| C-02 | Bind OP01/OP03/OP04 to Page 02 visuals | C-01 | OPEN |
| C-03 | Investigate/resolve `fact_route_costs_map` binding on Page 04 map | None (verify in Power BI Desktop) | OPEN |
| C-04 | dim_airline `BusinessModelClass` — do NOT populate until OD-01B D-05 approved | OD-01B D-05 | ON HOLD (by design) |

---

## D. Dashboard / visual (development complete — no build remaining)

| ID | Remaining work | Status |
|---|---|---|
| D-01 | None — all 5 pages / 120 visuals built | COMPLETE (built) |
| D-02 | Confirm validation coverage for full 27 Page 05 visuals (16 validated per owner) | OPEN (validation evidence) |
| D-03 | Rendered-page visual/data-value verification (requires Power BI Desktop) | OPEN (environment) |

---

## E. Testing & QA

| ID | Remaining work | Dependency | Status |
|---|---|---|---|
| E-01 | Execute test suite; obtain independent QA PASS decisions | A-09 (independent reviewer) | BLOCKED |
| E-02 | Execute T-79 disclosure rendering validation | Rendered report + Power BI Desktop | BLOCKED |
| E-03 | Confirm "335 passed" claim independently | Test environment | OPEN (verification) |

---

## F. Documentation & records

| ID | Remaining work | Status |
|---|---|---|
| F-01 | Populate empty governance documents (6 files at 0 bytes) | OPEN |
| F-02 | Record OD-01A/01B revision 0.2 before/after hashes | OPEN |
| F-03 | Update PROGRESS_LEDGER to reflect current built state (it is stale) | OPEN |

---

## G. Production readiness

| ID | Remaining work | Dependency | Status |
|---|---|---|---|
| G-01 | Create current complete backup of main PBIX | None | OPEN (can do now) |
| G-02 | Production refresh path / gateway / credentials | A-08 (G4) | BLOCKED |
| G-03 | RLS / access control design | — | OPEN |
| G-04 | Automated lineage (RAW→CURATED→Power BI) | — | OPEN |
| G-05 | Monitoring, alerting, operational runbook | — | OPEN |
| G-06 | Production-scale data volume (5,000 → 150K–250K flights) | A-08 (G4) | BLOCKED |

---

## Items deliberately NOT included (already complete — do not repeat)
- Five Power BI dashboard pages (built; 120 visuals)
- DAX measure development (54 measures written)
- Power Query query development (16 queries)
- Semantic model design (16 tables, 51 measures registered)
- Source data curation (16 tables populated)
- Architecture/specifications (complete)
