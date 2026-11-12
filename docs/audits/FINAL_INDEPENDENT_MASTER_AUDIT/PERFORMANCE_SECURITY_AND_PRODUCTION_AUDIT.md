# PERFORMANCE, SECURITY AND PRODUCTION AUDIT

**Source:** PBIX file metadata, model.json, data_sources.json, repository contents  
**Audit mode:** Read-only. No live service, no credentials store, no deployment target inspected.  
**Production readiness verdict: NOT PRODUCTION-READY.**

---

## 1. Performance

| Aspect | Finding | Severity |
|---|---|---|
| PBIX size | Main PBIX 9.4 MB — reasonable for 120 visuals + embedded model | OK |
| Model size | 16 tables; largest fact 9,956 rows (booking) — small validation volume | OK |
| High-cardinality columns | BookingReference, TicketNumber, FlightLegID, DisruptionID, FeedbackID — identifiers, not used as visual axes typically | OK |
| Calculated columns | None evidenced (measures only) — good | OK |
| Expensive measures | Decomposition tree (Page 05), scatter (Page 04), pivot table (Page 03) — moderate complexity on small data | OK |
| Inefficient transformations | Power Query is flat load (no folding, no filtering) — acceptable for validation volume | OK |
| Refresh reliability | No gateway/credentials configured; data sources are local CSVs | MEDIUM — not production refresh architecture |

**Data volume note:** fact_flight_operations = 5,000 rows is a validation volume, not production volume (target per contract is 150K–250K per MB-04 in blockers register). Production-scale performance not tested.

---

## 2. Security

| Aspect | Finding | Severity |
|---|---|---|
| Credentials/secrets | No credentials, connection strings, or secrets evidenced in repository | OK (none present) — but also no production credential store |
| Access control / RLS | No row-level security evidenced in model.json | MEDIUM — RLS not defined (may not be required for internal demo) |
| Data governance | Disclosure `Synthetic Simulation — Not Actual Airline Performance` present in model, DAX, data sources | OK |
| Auditability | Lineage not automated (MB-06); manifests partial | MEDIUM |
| Synthetic data | Clearly disclosed; original-currency amounts preserved alongside USD | OK |

---

## 3. Production readiness assessment (separate levels)

| Readiness level | Ready? | Basis |
|---|---|---|
| 1. Continued development | **YES** | Code, model, DAX, queries, dashboards all built; development can continue |
| 2. Internal testing | **PARTIAL** | Tests defined; execution & independent PASS pending (CB-09) |
| 3. Stakeholder demonstration | **YES (with caveat)** | 5-page PBIX built; operational & customer KPIs can demo; financial USD values blocked by OD-04 |
| 4. Controlled release | **NO** | G3/G4 not approved; reference data not created; no independent QA PASS |
| 5. Production deployment | **NO** | No G4 authorization, no refresh path, no deployment config, no RLS, backups stale |

---

## 4. Backup and recovery

| Aspect | Finding | Severity |
|---|---|---|
| PBIX backups | Two 1 MB backups are single-page stubs ("Page 1", 0 visuals) — INCONSISTENT with 9.4 MB main PBIX (5 pages, 120 visuals) | HIGH — cannot recover current report from backups |
| Current backup of main PBIX | None | HIGH |
| Recovery procedure | None documented | MEDIUM |

**Finding PROD-01 (HIGH):** No current, complete backup of the authoritative 9.4 MB main PBIX exists. The two labeled backups are stubs.

---

## 5. Monitoring, logging, operational documentation

- No monitoring, alerting, or operational runbook evidenced.
- No deployment configuration (workspace, capacity, environment) evidenced.
- `logs/` not present as a structured artifact.

---

## 6. Production-readiness findings register

| ID | Finding | Severity | Evidence | Confidence |
|---|---|---|---|---|
| PROD-01 | No current complete backup of main PBIX; backups are stubs | HIGH | PBIX version inventory | High |
| PROD-02 | G4 data generation authorization not recorded; no data generation/load executed | HIGH | PROGRESS_LEDGER.md (G4 BLOCKED) | High |
| PROD-03 | No production refresh path / gateway / credentials configured | HIGH | data_sources.json (local CSV paths); no deployment config | High |
| PROD-04 | RLS / access control not defined | MEDIUM | model.json (no RLS) | Medium |
| PROD-05 | No automated lineage (RAW→CURATED→Power BI) | MEDIUM | MB-06 in blockers register | Medium |
| PROD-06 | Validation volume (5,000 flights) below production target (150K–250K) | MEDIUM | MB-04 | Medium |
| PROD-07 | No monitoring, alerting, or operational runbook | LOW | Repository inspection | — |
| PROD-08 | Data volume: fact data is synthetic, disclosed | INFORMATIONAL | disclosure fields | High |

---

## 7. Production readiness verdict

**NOT PRODUCTION-READY.** The report is built (development complete), but it cannot be published/refreshed in production because:
1. Financial fact data not loaded (OD-04 blocked),
2. Reference data not created (G3-RV-01 not executed),
3. G4 not authorized,
4. No independent QA PASS (CB-09),
5. No current backup / refresh path / deployment configuration.

The report is suitable for **stakeholder demonstration** of operational & customer intelligence (with OD-04 financial caveat) and **continued development**, but not for controlled release or production deployment.
