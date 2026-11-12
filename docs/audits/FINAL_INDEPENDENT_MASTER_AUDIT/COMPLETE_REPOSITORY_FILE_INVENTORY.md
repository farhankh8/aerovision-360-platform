# COMPLETE REPOSITORY FILE INVENTORY

**Project root:** `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`  
**Audit type:** Read-only, evidence-based  
**Inventory basis:** Full recursive file walk excluding `.git/`, `__pycache__/`, `.pytest_*/`, `.ruff_cache/` (dependency caches and bytecode — classified as non-source, not inspected for content)  
**Total inventoried files:** 8,056 (full itemized listing exported to `$env:TEMP\opencode\file_inventory.csv` with columns: FullName, Length, LastWriteTime)  
**Directories inventoried:** all project directories listed below  
**Inspection method:** directory listing + file metadata (size, last modified); content inspection for source/config/documentation files; binary PBIX files extracted as ZIP for structural inspection only (not modified)

---

## A. Top-level project root files

The root contains build/inspection/fix scripts and root documentation. Root `.py` files (not in `src/` or `tests/`) are investigative/one-off scripts and are classified as generated/inspection artifacts, not production source:

| File | Size | Type | Classification | Production-relevant? |
|---|---|---|---|---|
| `README.md` | ~ | Markdown | Documentation | Yes |
| `all_files.txt` | ~ | Text | Generated artifact | No |
| `add_cdr.py`, `add_original_tests.py`, `add_propose.py`, `analyze.py`, `apply_fix.py`, `audit2.py`, `audit3.py`, `audit_page02.py`, `build_deliverables.py`, `build_excel.py`, `check_bytes.py`, `check_markers.py`, `check_method.py`, `check_state.py`, `comprehensive_fix.py`, `create_excel.py`, `create_excel_workbook.py`, `debug_test.py`, `find_execute*.py` (6), `find_fallback.py`, `find_milestones.py`, `fix_*.py` (many), `inspect_dim_airline.py`, `inspect_tests.py`, `investigate.py`, `m311_bi_contract.py`, `m312_*.py`, `page05_audit_data.py`, `read_method.py`, `restore_original*.py`, `trace_flow.py`, `validate_pbi.py`, `verify_*.py` (6) | various | Python | Investigation / fix / inspection scripts | Mostly No (one-off) |
| `_final_*.py` (9), `_inspect_*.py` (14), `_inspect_single*.py` | various | Python | Inspection scripts (this audit cycle) | No |
| `test.txt`, `test_output.txt`, `test_results.txt`, `test_run.txt` | various | Text | Test output artifacts | No |
| `M31*_*.md`, `STAGE_*_*.md`, `PAGE_04_*.md`, `PAGE_05_*.md`, `AEROVISION_360_COMPLETE_FORENSIC_AUDIT.md` | various | Markdown | Implementation/audit reports | Partial (historical) |

> Note: many root `.py` files are named `fix_*`, `find_*`, `inspect_*`, `_final_*` — these are one-off investigation/remediation scripts, not production pipeline code. Production Python lives in `src/`.

---

## B. Directory-by-directory inventory

### `docs/` — project documentation & governance

| Subdirectory | Purpose | File count (approx.) | Notes |
|---|---|---|---|
| `docs/` (root docs) | Scope, requirements, contracts, blueprints, roadmaps, risk register, decision records, completion history | ~60 `.md`/`.txt` | Core governance and spec documents |
| `docs/governance/` | Governance decision records, self-review, acceptance, evidence matrices | ~35 `.md` | Several files are **0 bytes** (empty): `GOVERNANCE_APPROVAL_MATRIX.md`, `GOVERNANCE_DECISION_PACK.md`, `OD_01_REMEDIATION_ACTION_REGISTER.md`, `KEY_MAP_IMMUTABILITY_TRIGGER_OWNER_ACCEPTANCE.md`, `C-06_OD01B-B-08_INDEPENDENT_REVIEWER_DECISION_DRAFT.md`, `GOV_D_06_STALENESS_THRESHOLD_DECISION_DRAFT.md` |
| `docs/audits/` | Existing audit reports | multiple subfolders | Includes `MASTER_PROJECT_AUDIT/` |
| `docs/audits/MASTER_PROJECT_AUDIT/` | Prior master audit (2026-11-06) — **STALE relative to current PBIX** | — | See contradiction reconciliation |
| `docs/backups/` | OD-01 revision, portfolio transition backups (4 timestamped folders) | — | Historical backups |
| `docs/g3_approval_backup_20261101/`, `docs/od01_*_backup_*/` | Governance backup folders | — | Historical |

Key governance documents inspected (full text read): `OD01A_AIRLINE_POPULATION_DECISION.md`, `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`, `OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md`, `OD04_OWNER_DECISION_PACKAGE.md`, `PROGRESS_LEDGER.md`, `MASTER_PROJECT_BLOCKERS_REGISTER.md`, `MASTER_PROJECT_AUDIT_AEROVISION_360.md`, `03_DATA_CONTRACTS.md`, `POWER_BI_DASHBOARD_SPECIFICATION.md`, `POWER_BI_SEMANTIC_MODEL_BLUEPRINT.md`, `POWER_QUERY_IMPLEMENTATION_BLUEPRINT.md`, `PYTHON_ETL_IMPLEMENTATION_BLUEPRINT.md`, `DAX_KPI_CATALOGUE.md`, `ENGINEERING_DATA_MODEL_BLUEPRINT.md`.

### `deliverables/` — built outputs

| Subdirectory | Contents | Production-relevant? |
|---|---|---|
| `deliverables/power_bi/` | **Main Power BI project**: `AEROVISION_360.pbix` (9,422,203 bytes, **authoritative**), `AEROVISION_360_VERIFIED_BACKUP.pbix` (1 MB, **stub**), `AEROVISION_360_PRE_IMPLEMENTATION_BACKUP.pbix` (1 MB, **stub**), `AEROVISION_360.pbip`, `.platform`, `report/report.json`, `semantic_model/model.json`, `semantic_model/semantic_model.json`, `dax/AEROVISION360_Measures.dax`, `power_query/AEROVISION360_DataLoad.m`, `data_sources/data_sources.json`, `theme/theme.json`, `audit/` (PBIX-level audit reports) | **Yes — core deliverable** |
| `deliverables/power_bi_backup_20261105/` | Extracted PBIX layout backup (`.platform`, `pbip`, `data_sources`, `dax`, `power_query`, `report`, `semantic_model`, `theme`) | Partial (historical extracted layout) |
| `deliverables/data/` | Exported data: `customer_feedback/`, `dimensions/`, `disruptions/`, `flight_operations/`, plus root-level `fact_booking_transactions.csv`, `fact_operating_costs.csv`, `fact_*.csv`, `dim_*.csv` + `.parquet` counterparts | Yes (data exports) |
| `deliverables/excel/` | `AEROVISION_360_AIRLINE_ANALYTICS.xlsx` (12 sheets, openpyxl-verified) | Yes |
| `deliverables/exports/`, `deliverables/screenshots/` | Exports and screenshots | Partial |

### `data/` — source & curated data layers

| Subdirectory | Contents | Production-relevant? |
|---|---|---|
| `data/03_curated/` | **16 tables**, CSV + Parquet each (11 dimensions + 5 facts), plus `recovery/` folder with dated recovery copies | **Yes — source data** |
| `data/04_reference/` | `AEROVISION_360_AIRLINE_REFERENCE_WORKBOOK.xlsx`, `AIRLINE_ID_CROSSWALK.csv`, `DIM_ROUTE_KEYMAP_V1.csv`, `DIM_ROUTE_KEYMAP_V1_MANIFEST.json` | Yes (reference data — partial; `ref_airlines.csv`, `ref_exchange_rates.csv` NOT created) |
| `data/manifests/` | 13 manifest JSONs (dims + facts + reference) | Yes |
| `data/execution/` | Many timestamped run directories (generated execution artifacts) | No (generated/cache) |
| `data/01_raw/`, `data/02_staging/` | Referenced by contract but not found populated at time of audit | Not found / not created |

> Contradiction note: `PROGRESS_LEDGER.md` and the prior master audit state `data/03_curated/` is "not created" and `data/04_reference/` is empty. **Actual inspection shows both are populated.** These documents are stale (see Phase J reconciliation).

### `scripts/` — Python build scripts

| Folder | Contents |
|---|---|
| `scripts/` | Build scripts for dimensions (`build_dim_*.py`), facts (`build_fact_*.py`), raw/staging/curated layers (`build_raw_layer.py`, `build_staging_layer.py`, `build_curated.py`), pipeline (`run_pipeline.py`), quality (`run_quality_checks.py`), validation (`validate_airline_reference.py`), audit (`audit_dimensions*.py`) |
| `scripts/backups/` | 8 dated backup folders with prior script versions |

### `src/` — Python source (production pipeline)

`src/ingestion/`, `src/staging/`, `src/transformations/`, `src/quality/`, `src/orchestration/`, `src/utilities/`, `src/validation/`, `src/generators/` — each with `.py` source and `__pycache__` bytecode (not inspected as source)

### `tests/` — test suites

| Folder | Contents |
|---|---|
| `tests/unit/` | 25 test files: `test_dim_airline_curated.py`, `test_fact_booking_transactions.py`, `test_fact_customer_feedback.py`, `test_fact_disruptions.py`, `test_fact_flight_operations.py`, `test_fact_operating_costs.py`, `test_hashing.py`, `test_io.py`, `test_logging.py`, `test_m310_quality_governance.py`, `test_m311_analytical_validation.py`, `test_m311_integration.py`, `test_m38_integration.py`, `test_m39_observability.py`, `test_paths.py`, `test_pipeline_cli.py`, `test_pipeline.py`, `test_raw_ingestion.py`, `test_settings.py`, `test_stage2_power_query_integration.py`, `test_stage3_semantic_model.py`, `test_stage4_financial_dax.py`, `test_stage5_page03_dashboard.py`, `test_staging_layer.py`, `test_staging_processor.py` |
| `tests/data_quality/`, `tests/reconciliation/` | Directories present (contents limited) |

### `reports/`, `qa/`, `config/`, `contracts/`, `incident_data/`, `remediation_data/`, `power_bi/` (root)

- `reports/` — audit reports, final case study, network expansion deployment packages, production expansion audit
- `qa/results/`, `qa/screenshots/` — QA evidence
- `config/`, `contracts/` — configuration and contracts
- `incident_data/`, `remediation_data/` — incident and remediation data
- `power_bi/` (root) — separate Power BI folder (distinct from `deliverables/power_bi/`)

### Excluded from content inspection (inventoried by metadata only)
`.git/`, `__pycache__/`, `.pytest_*/`, `.ruff_cache/`, `.venv/`, `data/execution/*` run directories — dependency caches, bytecode, and generated execution runs. Classified as non-source / not production-relevant.

---

## C. Power BI files (PBIX) — version inventory (Phase B detail)

| File | Path | Size | Modified | Pages | Visuals | Authoritative? |
|---|---|---|---|---|---|---|
| Main PBIX | `deliverables/power_bi/AEROVISION_360.pbix` | 9,422,203 bytes | 08-11-2026 14:41 | 5 | 120 | **YES — authoritative** |
| Verified backup | `deliverables/power_bi/AEROVISION_360_VERIFIED_BACKUP.pbix` | 1,003,650 bytes | 05-11-2026 18:11 | 1 (stub: "Page 1") | 0 | No — stale stub |
| Pre-implementation backup | `deliverables/power_bi/AEROVISION_360_PRE_IMPLEMENTATION_BACKUP.pbix` | 1,003,650 bytes | 05-11-2026 18:16 | 1 (stub: "Page 1") | 0 | No — stale stub |

- All three PBIX files have **different SHA-256 hashes** (main: `4E02560D...`; verified: `64136DE1...`; pre-impl: `4AC59DF8...`).
- The two 1 MB backups are **not consistent with** and **not current versions of** the main 9.4 MB PBIX.
- In-PBIX binary model (`DataModel`, 2.5 MB) is serialized binary and could not be deserialized in this read-only environment — limitation disclosed.

---

## D. Duplicate / obsolete / orphaned findings

1. **Duplicate data files:** `deliverables/data/` contains the same CSVs/Parquet at root level AND under `dimensions/`, `disruptions/`, `flight_operations/`, `customer_feedback/` subfolders (e.g., `dim_airline.csv` appears in both `deliverables/data/` and `deliverables/data/dimensions/`).
2. **Duplicate PBIX backups:** two 1 MB backups with identical size but different hashes; neither matches the main PBIX.
3. **Missing expected artifacts:** `ref_airlines.csv`, `ref_exchange_rates.csv`, `ref_aircraft_availability.csv`, `data/manifests/reference_versions.csv` not created; `data/01_raw/`, `data/02_staging/` not populated.
4. **Empty governance files:** 6 files in `docs/governance/` are 0 bytes (listed above).
5. **Stale documentation:** `PROGRESS_LEDGER.md` (2026-11-02) and `MASTER_PROJECT_AUDIT_AEROVISION_360.md` (2026-11-06) describe a pre-built-PBIX state (report "blank", Power BI "not created", DAX "10 measures", Power Query "2 of 14") that does not match the current repository.

---

## E. Inspection coverage statement

Every directory listed above was walked. Source, configuration, and documentation files were opened and read where text-based. PBIX binaries were extracted and structurally inspected (pages, visuals, report.json) but not opened in Power BI Desktop and not modified. The binary `DataModel` inside the PBIX could not be deserialized (limitation). Large generated caches (`data/execution/*`, bytecode) were inventoried by metadata only.

Full itemized file listing: `$env:TEMP\opencode\file_inventory.csv` (8,056 rows).
