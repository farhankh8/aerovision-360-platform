# EXISTING AUDIT CONTRADICTION RECONCILIATION

**Purpose:** Reconcile known contradictions between prior audit/investigation reports and the actual repository evidence.  
**Method:** Each contradiction lists the original claim, evidence inspected in this audit, the corrected conclusion, confidence, and whether resolved.  
**Rule:** No new inconsistencies created while reconciling old ones. Missing evidence is not treated as a confirmed defect.

---

## Contradiction 1 — PBIX reported as blank vs. five populated pages

| Element | Detail |
|---|---|
| Original claim | Prior `MASTER_PROJECT_AUDIT_AEROVISION_360.md` (2026-11-06): PBIX "effectively blank"; Page 03–06 not built; `PROGRESS_LEDGER.md`: Power BI "NOT CREATED", `power_bi/` remains empty |
| Evidence inspected | `deliverables/power_bi/AEROVISION_360.pbix` = 9,422,203 bytes; extracted 5 pages (01 Executive Overview, 02 Operations, Revenue & Finance, COST & FINANCIAL INTELLIGENCE, 05 Customer & Service Intelligence) with 120 visuals |
| Corrected conclusion | **Claim is FALSE for the main PBIX.** The prior audit assessed the 1 MB backup (`AEROVISION_360_VERIFIED_BACKUP.pbix`), which IS a single stub page ("Page 1", 0 visuals). The main 9.4 MB PBIX (modified 08-11-2026) is fully populated with 5 pages / 120 visuals. The prior audit and ledger are STALE — they predate the current main PBIX. |
| Confidence | High |
| Resolved | Yes |

---

## Contradiction 2 — Main PBIX vs. backup PBIX

| Element | Detail |
|---|---|
| Original claim | Backups (`VERIFIED_BACKUP`, `PRE_IMPLEMENTATION_BACKUP`) assumed to be current copies of the report |
| Evidence inspected | SHA-256 hashes: main `4E02560D…` (9.4 MB, 5 pages, 120 visuals); verified `64136DE1…` (1 MB, 1 stub page, 0 visuals); pre-impl `4AC59DF8…` (1 MB, 1 stub page, 0 visuals). All three differ. |
| Corrected conclusion | Backups are NOT current copies and NOT consistent with the main PBIX. They are stale single-page stubs and cannot serve as recovery sources. Main PBIX is authoritative. |
| Confidence | High |
| Resolved | Yes |

---

## Contradiction 3 — Five-page / 120-visual report vs. differing visual counts

| Element | Detail |
|---|---|
| Original claim | Prior audit: report "blank"; extracted `report.json`: 44 visuals with different page names ("Network & Capacity Intelligence", "Operations & Disruption") |
| Evidence inspected | Binary PBIX pages: 01 Executive Overview (24), 02 Operations (23), Revenue & Finance (23), COST & FINANCIAL INTELLIGENCE (23), 05 Customer & Service Intelligence (27) = 120 total |
| Corrected conclusion | Authoritative PBIX = 120 visuals across 5 pages with the owner's actual page names. Extracted `report.json` (44 visuals, different names) is a simplified/placeholder layout, not the current Desktop state. |
| Confidence | High |
| Resolved | Yes |

---

## Contradiction 4 — Page 05: 13 / 16 / 27 visual reports

| Element | Detail |
|---|---|
| Original claim | Conflicting reports: Page 05 = 13 visuals, 16 visuals, or 27 visuals |
| Evidence inspected | Binary PBIX page `18bdd7f468e4853e0a00` ("05 - Customer & Service Intelligence") = 27 visual directories |
| Corrected conclusion | **27 is correct** for the authoritative PBIX. The "16 investigated visuals" (owner context) is a validation-coverage subset that passed data validation, not the total visual count. The "13" figure is unsupported by the binary. |
| Confidence | High |
| Resolved | Yes |

---

## Contradiction 5 — 54 DAX measures vs 51 model registrations

| Element | Detail |
|---|---|
| Original claim | 54 measures in DAX file vs 51 in model.json; OP01, OP03, OP04 missing from model.json |
| Evidence inspected | DAX file = 54 measures (FL×4, DS×3, CF×14, OP×3, RV×17, CX×10, NC×3). model.json = 51 registered; fact_flight_operations registers only FL01–FL04. OP01, OP03, OP04 present in DAX (lines 31–33) but absent from model.json. |
| Corrected conclusion | **Confirmed genuine:** 54 DAX vs 51 registered; gap = OP01, OP03, OP04 (3 measures). These are defined in DAX but not registered in the semantic model and not bound to visuals. |
| Confidence | High |
| Resolved | Yes (gap identified; closure = register the 3 measures) |

---

## Contradiction 6 — 22 OD-04-blocked measures vs. prefix totals

| Element | Detail |
|---|---|
| Original claim | 22 measures reportedly dependent on OD-04; "32 measures reportedly available" |
| Evidence inspected | OD-04 blocks FactBookingTransactions and FactOperatingCosts. Financial measures by prefix: RV = 17, CX = 10, NC = 3 → 30 financial measures. Of these, the ones strictly requiring USD-converted financial fact data = RV_/CX_/NC_ families that aggregate amount columns. |
| Corrected conclusion | The "22" and "32" figures could not be independently verified as exact counts because OD-04 dependency is at the *fact-table data* level (all financial measures are blocked from producing USD values), not a per-measure count of 22. The correct statement: **all RV_/CX_/NC_ financial measures (30) depend on OD-04-approved exchange rates and loaded financial facts; none can render correct USD values until OD-04 is resolved.** Operational measures (FL/DS/CF = 21) are not OD-04-blocked. |
| Confidence | Medium (exact "22"/"32" counts not verifiable; the functional conclusion — financial measures blocked by OD-04 — is verified) |
| Resolved | Partially (exact count not verifiable; functional impact confirmed) |

---

## Contradiction 7 — Power Query 2/14 vs 2/16 tables

| Element | Detail |
|---|---|
| Original claim | Prior audit / blockers register: Power Query "defines only 2 of 14 tables"; conflicting "2 of 16" |
| Evidence inspected | `power_query/AEROVISION360_DataLoad.m` = 16 query blocks covering all 16 model tables (11 dims + 5 facts) |
| Corrected conclusion | **Claim is FALSE.** Power Query defines 16 of 16 tables. The "2 of 14/16" figures are stale/incorrect. |
| Confidence | High |
| Resolved | Yes |

---

## Contradiction 8 — Page 05 pending vs implemented visuals

| Element | Detail |
|---|---|
| Original claim | Page 05 reported as "pending" visuals in some reports |
| Evidence inspected | Binary PBIX Page 05 = 27 visuals implemented (cards, charts, slicers, decomposition tree, page navigator); 16 reportedly validated |
| Corrected conclusion | Page 05 visuals are IMPLEMENTED (27). The "pending" characterization reflects incomplete *validation coverage* (16 of 27 validated per owner context), not missing visual development. |
| Confidence | High |
| Resolved | Yes |

---

## Contradiction 9 — Governance: owner-confirmed vs formally approved

| Element | Detail |
|---|---|
| Original claim | Various records describe OD-01A/OD-01B as approved |
| Evidence inspected | `OD01A_AIRLINE_POPULATION_DECISION.md` and `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`: both "OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING"; no signature, no approval date, no independent review |
| Corrected conclusion | OD-01A and OD-01B are **owner-confirmed but NOT formally approved/signed.** Owner-confirmed ≠ formally approved. This is a genuine blocker (CB-01/CB-02). |
| Confidence | High |
| Resolved | Yes (status clarified) |

---

## Contradiction 10 — G3-RV-01 not executed; OD-04 unresolved

| Element | Detail |
|---|---|
| Original claim | Multiple reports list G3-RV-01 not executed and OD-04 unresolved as open items |
| Evidence inspected | OD-04 = PROPOSED — OWNER APPROVAL REQUIRED (currency mismatch 5 vs 8 unresolved); G3-RV-01 = NOT EXECUTED; reference manifest and ref_* CSVs not created |
| Corrected conclusion | **Confirmed genuine and open.** G3-RV-01 not executed; OD-04 unresolved. Both are active blockers in the dependency chain. |
| Confidence | High |
| Resolved | No — these remain open action items |

---

## Contradiction 11 — FactBookingTransactions / FactOperatingCosts "do not exist"

| Element | Detail |
|---|---|
| Original claim | Prior audit: "FactBookingTransactions and FactOperatingCosts do not exist anywhere in the project" |
| Evidence inspected | `data/03_curated/fact_booking_transactions.csv` (9,956 rows, 50 cols) and `fact_operating_costs.csv` (7,480 rows, 18 cols) both exist; plus Parquet counterparts |
| Corrected conclusion | **Claim is FALSE as to source files.** Both financial fact tables exist as curated CSVs. They are NOT loaded into the Power BI model (absent from `data_sources.json`) and are blocked by OD-04. They exist as source but are not model-loaded. |
| Confidence | High |
| Resolved | Yes |

---

## Contradiction 12 — Reference data / data/03_curated "not created" or "empty"

| Element | Detail |
|---|---|
| Original claim | `PROGRESS_LEDGER.md`: `data/03_curated/` datasets not created; `data/04_reference/` empty; prior audit: reference layer "NEARLY EMPTY" |
| Evidence inspected | `data/03_curated/` = 16 populated tables (CSV + Parquet); `data/04_reference/` = reference workbook, crosswalk, keymap, manifest; `data/manifests/` = 16 manifest JSONs |
| Corrected conclusion | **Partially stale.** Curated data IS populated (16 tables). Reference CSVs required for governance (`ref_airlines.csv`, `ref_exchange_rates.csv`, reference manifest) are NOT created. The ledger's claim that curated data doesn't exist is wrong; its claim that governance reference CSVs don't exist is correct. |
| Confidence | High |
| Resolved | Yes (distinguished curated data vs governance reference CSVs) |

---

## Reconciliation summary

| Contradiction | Status | Resolved? |
|---|---|---|
| 1. PBIX blank vs 5 pages | Resolved — main PBIX populated | Yes |
| 2. Main vs backup PBIX | Resolved — backups are stubs | Yes |
| 3. 120 visuals vs differing counts | Resolved — 120 is authoritative | Yes |
| 4. Page 05 visual count | Resolved — 27 | Yes |
| 5. 54 vs 51 DAX | Resolved — OP01/03/OP04 gap | Yes |
| 6. 22/32 OD-04 measures | Partially — functional impact confirmed | Partially |
| 7. Power Query 2/14 vs 2/16 | Resolved — 16 of 16 | Yes |
| 8. Page 05 pending vs implemented | Resolved — implemented | Yes |
| 9. Owner-confirmed vs approved | Resolved — not formally approved | Yes |
| 10. G3-RV-01 / OD-04 open | Confirmed open | No (action item) |
| 11. Financial facts "don't exist" | Resolved — exist as CSV, not model-loaded | Yes |
| 12. Curated/reference "empty" | Resolved — curated populated; ref CSVs missing | Yes |

No new inconsistencies were created. Contradictions 6 and 10 remain as tracked open items (functional impact confirmed; exact measure count in #6 not verifiable; #10 is a genuine open governance action).
