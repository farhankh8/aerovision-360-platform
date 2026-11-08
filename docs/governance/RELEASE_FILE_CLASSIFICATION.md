# AEROVISION 360 — Release File Classification

**Classification ID:** RELEASE-FILES-2026-11-08  
**Prepared:** 2026-11-08  
**Prepared by:** Autonomous engineering agent (OpenCode)  
**Status:** CLASSIFICATION PREPARED — NO files staged, committed, or pushed

---

## 1. Git State Summary

| Property | Value |
|---|---|
| Branch | `main` |
| Commits | Zero (no commits exist) |
| Staged files | 93 (initial project import, pre-dates this session) |
| Unstaged modified files | 7 |
| Untracked files | ~170+ |
| Force-push | Not performed (prohibited) |
| Commit/push | Not performed (requires owner authorization) |

---

## 2. File Classification

### 2.1 Required Project Source (Include in Release)

| File | Reason |
|---|---|
| `src/` | Python source code — core pipeline, quality, orchestration, staging, transformations, utilities, validation |
| `tests/` | Test suite — 595 unit tests, fact-builder tests |
| `scripts/build_*.py` | Build scripts for curated layer and fact tables |
| `scripts/run_pipeline.py` | Pipeline execution script |
| `scripts/run_quality_checks.py` | Quality check execution script |
| `config/` | Configuration files |
| `contracts/` | Contract definitions |

### 2.2 Required Documentation (Include in Release)

| File | Reason |
|---|---|
| `README.md` | Project overview and status |
| `docs/01_PROJECT_SCOPE.md` | Project scope v1.1 (authoritative per D-1) |
| `docs/02_BUSINESS_REQUIREMENTS.md` | Business requirements BR-01 through BR-15 |
| `docs/03_DATA_CONTRACTS.md` | Data contracts v1.5 (DRAFT — pending formal approval) |
| `docs/PROGRESS_LEDGER.md` | Execution ledger (authoritative status record) |
| `docs/PROJECT_RISK_REGISTER.md` | Project risk register (R-09 to R-11) |
| `docs/REQUIREMENTS_TRACEABILITY.md` | Requirement-to-evidence tracking |
| `docs/OD01A_AIRLINE_POPULATION_DECISION.md` | OD-01A decision record (signature pending) |
| `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | OD-01B decision record (signature pending) |
| `docs/governance/OD04_OWNER_DECISION_RECORD.md` | OD-04g approval record (signature pending) |
| `docs/governance/OD01_OWNER_CONFIRMATION_ADDENDUM_DRAFT.md` | GOV-D-04 addendum (signature pending) |
| `docs/governance/GOV_D_06_OWNER_ACCEPTANCE.md` | GOV-D-06 acceptance (signature pending) |
| `docs/governance/GOV_D_07_OWNER_ACCEPTANCE.md` | GOV-D-07 acceptance (authorization pending) |
| `docs/governance/GOV_D_08_OWNER_ACCEPTANCE.md` | GOV-D-08 acceptance (authorization pending) |
| `docs/governance/CC01_OWNER_SELF_REVIEW.md` | CC-01 self-review (owner execution pending) |
| `docs/governance/OWNER_APPROVAL_SESSION.md` | Consolidated owner approval session (this session) |
| `docs/governance/G3-RV-01_GATE_ARTIFACT_TEMPLATE.md` | G3-RV-01 template (blocked pending signatures) |
| `docs/governance/SCHEMA_FREEZE_EVIDENCE_PACKAGE.md` | Schema freeze evidence (blocked pending authorization) |
| `docs/DAX_KPI_CATALOGUE.md` | DAX measure catalogue |
| `docs/POWER_BI_DASHBOARD_SPECIFICATION.md` | Power BI dashboard specification |
| `docs/POWER_BI_SEMANTIC_MODEL_BLUEPRINT.md` | Semantic model blueprint |
| `docs/POWER_QUERY_IMPLEMENTATION_BLUEPRINT.md` | Power Query implementation blueprint |

### 2.3 Required Deliverables (Include in Release)

| File | Reason |
|---|---|
| `deliverables/power_bi/AEROVISION_360.pbix` | Authoritative PBIX — 5 pages, 120 visuals, 16 tables, 54 measures |
| `deliverables/power_bi/AEROVISION_360.pbip` | Power BI project file |
| `deliverables/power_bi/dax/AEROVISION360_Measures.dax` | DAX measure source — 54 measures |
| `deliverables/power_bi/power_query/AEROVISION360_DataLoad.m` | Power Query M — 16 queries |
| `deliverables/power_bi/semantic_model/model.json` | Semantic model — 54 measures registered |
| `deliverables/power_bi/semantic_model/semantic_model.json` | Semantic model config — 16 tables |
| `deliverables/power_bi/data_sources/data_sources.json` | Data sources — 14 sources (3 financial missing) |
| `deliverables/power_bi/data_sources_integration_patch.json` | Integration patch (prepared, not executed) |
| `deliverables/excel/AEROVISION_360_AIRLINE_ANALYTICS.xlsx` | Excel workbook — 12 sheets, 266,725 bytes |

### 2.4 Data Assets (Include in Release — Development Status)

| File | Reason | Status |
|---|---|---|
| `data/03_curated/fact_booking_transactions.csv` | 9,956 rows — synthetic development output | PROVISIONAL — not production-authorized |
| `data/03_curated/fact_operating_costs.csv` | 7,480 rows — synthetic development output | PROVISIONAL — not production-authorized |
| `data/03_curated/dim_currency.csv` | 8 currencies | PROVISIONAL — not production-authorized |
| `data/03_curated/*.csv` (all other curated) | Curated dimension and fact tables | PROVISIONAL — not production-authorized |
| `data/04_reference/ref_exchange_rates.csv` | 2,920 exchange rates | PROVISIONAL — not production-authorized |
| `data/04_reference/AIRLINE_ID_CROSSWALK.csv` | Airline ID crosswalk | Reference file |
| `data/04_reference/DIM_ROUTE_KEYMAP_V1.csv` | Route key map v1 | Reference file |
| `data/manifests/*.json` | 18 manifest files with SHA-256 hashes | All hashes verified (34/34 file entries) |
| `data/01_raw/` | Raw layer source index and runs | Preserved — not modified |
| `data/02_staging/` | Staging layer runs and quarantine | Preserved — not modified |

### 2.5 Tests and Validation (Include in Release)

| File | Reason |
|---|---|
| `tests/unit/` | 26 test files — 595 tests passed |
| `pytest_exec.txt` | Test execution evidence (this session) |
| `pytest_fact.txt` | Fact-builder test evidence |

### 2.6 Generated Evidence (Include in Release)

| File | Reason |
|---|---|
| `docs/governance/G3-RV-01_GATE_ARTIFACT_TEMPLATE.md` | Gate artifact template (prepared, not executed) |
| `docs/governance/SCHEMA_FREEZE_EVIDENCE_PACKAGE.md` | Schema freeze evidence (prepared, not authorized) |
| `docs/governance/RELEASE_FILE_CLASSIFICATION.md` | This classification document |

### 2.7 Temporary Files (EXCLUDE from Release)

| File | Reason for Exclusion |
|---|---|
| `.pytest_basetemp/` through `.pytest_final/` | Pytest cache directories |
| `pytest_current.txt`, `pytest_exec.txt`, `pytest_fact.txt`, `pytest_fin.txt` | Temporary test output |
| `_final_complete.py`, `_final_reconcile*.py`, `_inspect_*.py` | Temporary inspection scripts |
| `add_cdr.py`, `add_original_tests.py`, `add_propose.py` | Temporary/duplicate scripts |
| `analyze.py`, `apply_fix.py`, `audit2.py`, `audit3.py` | Temporary analysis scripts |
| `build_deliverables.py`, `build_excel.py`, `create_excel.py` | Temporary build scripts |
| `check_*.py`, `comprehensive_fix.py`, `debug_test.py` | Temporary debug scripts |
| `find_execute*.py`, `find_fallback.py`, `find_milestones.py` | Temporary search scripts |
| `fix_*.py` (all) | Temporary fix scripts |
| `inspect_*.py`, `investigate.py`, `page05_audit_data.py` | Temporary inspection scripts |
| `restore_*.py` | Temporary restore scripts |
| `trace_flow.py`, `validate_pbi.py`, `verify_*.py` | Temporary validation scripts |
| `test.txt`, `test_output.txt`, `test_results.txt`, `test_run.txt` | Temporary test output |
| `all_files.txt` | Temporary file listing |
| `AEROVISION_360_COMPLETE_FORENSIC_AUDIT.md` | Superseded audit report |
| `M31*.md`, `M37*.txt`, `M38*.md`, `M39*.md` | Superseded milestone reports |
| `PAGE_04_*.md`, `PAGE_05_*.md` | Superseded page reports |
| `STAGE_*.md` | Superseded stage reports |
| `docs/audits/` | Superseded audit directory |
| `docs/MASTER_*.md` | Superseded master reports |
| `docs/M310_*.md`, `docs/M311_*.md` | Superseded milestone docs |
| `docs/OD01_OWNER_DECISION_PACKET.pre-approval-backup.md` | Superseded backup |
| `docs/OWNER_DECISIONS_2026-11-04.md` | Superseded decision doc |
| `remediation_data/` | Temporary remediation data |
| `incident_data/` | Temporary incident data |
| `governance_decisions/` | Temporary governance decisions |

### 2.8 Build Artifacts (EXCLUDE from Release)

| File | Reason for Exclusion |
|---|---|
| `.venv/` | Python virtual environment |
| `__pycache__/` directories | Python cache |
| `.ruff_cache/` | Ruff cache |
| `.gitignore` | Already staged |
| `.agents/` | Agent skill data (staged) |
| `.freebuff/` | Unknown — investigate before release |

### 2.9 Sensitive or Potentially Sensitive Files (REVIEW Before Release)

| File | Concern | Action |
|---|---|---|
| `config/` | May contain connection strings or credentials | Review before release |
| `contracts/` | May contain sensitive contract terms | Review before release |
| `.freebuff/` | Unknown origin and contents | Investigate before release |
| Any file containing passwords, tokens, API keys | Must not be committed | Secret scan required before commit |

### 2.10 Unclassified — Requires Investigation

| File/Directory | Reason |
|---|---|
| `.freebuff/` | Unknown purpose and contents |
| `docs/governance/` (additional files not listed above) | Need review for release relevance |
| `reports/` subdirectories | Some may contain relevant evidence, some superseded |

---

## 3. Proposed Release Inclusion/Exclusion List

### Include (Release-Critical):
- All files in sections 2.1, 2.2, 2.3, 2.4 (data assets), 2.5, 2.6

### Exclude (Do Not Release):
- All files in sections 2.7, 2.8
- All files in section 2.9 until secret scan completed

### Review Required (Do Not Release Until Cleared):
- All files in sections 2.9, 2.10

---

## 4. Safe Git Release Checklist

- [ ] Secret scan completed (no credentials in staged/committed files)
- [ ] Owner authorization for commit and push obtained
- [ ] Release commit message prepared
- [ ] Version identifier assigned (e.g., v1.0.0-governance-pending)
- [ ] Release notes prepared
- [ ] File classification reviewed (this document)
- [ ] No force-push planned
- [ ] No unrelated files included in commit
- [ ] Pre-existing staged and unstaged changes preserved

---

**End of Release File Classification.**  
No files have been staged, committed, or pushed. All classifications are recommendations pending owner review and authorization.
