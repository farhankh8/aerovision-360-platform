# M3.8 Implementation Plan — End-to-End Vertical Slice

## Scope
**Selected vertical slice**: `airline_reference_workbook` → STAGING → QUALITY → ORCHESTRATION → `dim_airline`

**Justification**: This is the most complete and tested path in the system:
- RAW source `airline_reference_workbook.xlsx` exists in `data/01_raw/`
- STAGING plan defined in `STAGING_PLANS` for `airline_reference_workbook` → `DimAirline`
- Quality gate references `airline_reference_workbook` as one of 4 required STAGING sources
- Default registry includes `dim_airline`
- Existing curated dimension `dim_airline` in `data/03_curated/`

**Data flow**: `airline_reference_workbook.xlsx` → `build_staging_layer.py` → `run_quality_checks.py` → `PipelineOrchestrator` → isolated `dim_airline` output

**Components reused** (no new implementation):
- `scripts/build_staging_layer.py` — actual STAGING transformation
- `scripts/run_quality_checks.py` — actual quality validation
- `src/orchestration/pipeline.py` — actual pipeline orchestrator with quality gate
- `src/orchestration/default_registry.py` — default component registry
- `src/quality/engine.py` — data quality engine
- `src/quality/manifest.py` — quality manifest persistence
- `src/quality/rules.py` — registered quality rules (RULE-001 through RULE-201)

**Integration test scenarios** (16 required):
1. Valid source completes the full vertical slice
2. RAW ingestion preserves source integrity
3. STAGING accepts valid records
4. Invalid records are rejected/quarantined per contract
5. Quality checks execute and persist a manifest
6. Valid quality evidence permits downstream execution
7. Missing quality manifest blocks downstream execution
8. FAIL quality outcome blocks curated generation
9. Incorrect lineage blocks/rejects execution as appropriate
10. Missing source blocks execution
10. Repeated execution behaves deterministically
11. Existing production outputs remain unchanged
12. Component dependency order is respected
13. A failed component prevents dependent components from running
13. Execution manifest accurately records the run
15. Final curated output conforms to its existing schema

**Governance restrictions preserved**:
- OD-04: FactBookingTransactions and FactOperatingCosts remain blocked
- No production datasets modified
- No Git operations

**Test infrastructure**:
- All existing 237 tests must continue passing
- New integration tests use temporary directories
- No test deletions or weakenings