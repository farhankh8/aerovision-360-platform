# FINAL NEXT STEP AND EXECUTION ROADMAP

**Source:** All phase audits (A–I), remaining work register, blocker register  
**Audit mode:** Read-only. No implementation started.  
**Decision:** The single highest-priority next action, then the complete remaining sequence.

---

## 1. The single best next action

**Obtain the owner's formal signature and approval date on OD-01A (airline population) and OD-01B (airline identity/reference).**

### Why this must happen first

OD-01A/OD-01B signatures are the **root of the entire dependency chain**. Nothing downstream can unblock the project end-to-end until they are signed:

```
OD-01A/OD-01B signatures
    → enables G3-RV-01 (reference-version approval)
    → enables reference-data creation (ref_airlines.csv, manifest, key map)
    → enables schema freeze
    → enables G3 formal gate approval
    → enables written G4 data generation authorization
    → enables all data generation (reference data, synthetic data, financial facts)
    → enables FactBookingTransactions / FactOperatingCosts (requires OD-04 too)
    → enables Power BI model load and refresh
    → enables Page 03/04 financial USD values
    → enables QA test execution + independent PASS
    → enables controlled release and production deployment
```

**Dashboard development is already complete** (5 pages, 120 visuals) and must NOT be repeated. OD-01A/OD-01B are owner-confirmed (design agreed) but not formally signed — only the signature/approval date is missing. This is the smallest action with the largest unblocking effect.

**Why not OD-04 first?** OD-04 also requires owner approval, but OD-01A/01B are the prerequisite for G3-RV-01 and the reference-manifest/key-map foundation that OD-04's exchange rates and financial facts ultimately depend on. The dependency chain puts OD-01A/01B at the root.

**Why not another audit?** Multiple audits already exist; this master audit is complete. Further auditing adds no value until governance decisions are signed.

---

## 2. Complete remaining implementation sequence

### Phase 1 — Governance unlock (owner action)

| Step | Action | Owner/QA | Unblocks |
|---|---|---|---|
| 1.1 | Sign OD-01A + approval date | Owner | Reference data, G3 |
| 1.2 | Sign OD-01B + approval date | Owner | G3-RV-01, key map |
| 1.3 | Approve OD-04 + resolve 5-vs-8 currency mismatch (align to 8 DimCurrency currencies) | Owner | Financial facts |
| 1.4 | Execute G3-RV-01 (manifest, key map, T-75/T-76/T-78) | Owner/QA | Reference data creation |
| 1.5 | Schema freeze authorization | Owner | Model/Power Query build |
| 1.6 | G3 formal gate approval | Gate review | G4 authorization |
| 1.7 | Written G4 data generation authorization | Owner | All data generation |
| 1.8 | Assign independent reviewer; close compensating control | Owner | QA PASS decisions |

### Phase 2 — Data generation (gated by Phase 1)

| Step | Action | Depends on |
|---|---|---|
| 2.1 | Create `ref_airlines.csv`, `ref_airline_sources.csv` | 1.4 |
| 2.2 | Create `ref_exchange_rates.csv` with approved rates (all 8 currencies) | 1.3 |
| 2.3 | Create reference manifest `data/manifests/reference_versions.csv` | 1.4 |
| 2.4 | Generate/sync curated financial facts (FactBookingTransactions, FactOperatingCosts) | 1.7, 2.2 |
| 2.5 | Add financial facts to `data_sources.json` and load to model | 2.4 |

### Phase 3 — Semantic model & DAX closures (no OD/G4 dependency; can overlap with Phase 1)

| Step | Action |
|---|---|
| 3.1 | Register OP01, OP03, OP04 in `semantic_model/model.json` |
| 3.2 | Bind OP01/OP03/OP04 to Page 02 visuals |
| 3.3 | Investigate/resolve `fact_route_costs_map` binding on Page 04 map (verify in Power BI Desktop) |

### Phase 4 — Validation & QA (gated by Phase 1/2)

| Step | Action |
|---|---|
| 4.1 | Execute test suite; obtain independent QA PASS decisions (requires independent reviewer from 1.8) |
| 4.2 | Execute T-79 disclosure rendering validation (requires rendered report / Power BI Desktop) |
| 4.3 | Rendered-page visual/data-value verification (Power BI Desktop) |
| 4.4 | Confirm validation coverage for all 27 Page 05 visuals |

### Phase 5 — Production readiness (gated by Phase 4)

| Step | Action |
|---|---|
| 5.1 | Create current complete backup of main PBIX (9.4 MB) |
| 5.2 | Configure production refresh path / gateway / credentials |
| 5.3 | Design RLS / access control |
| 5.4 | Implement automated lineage (RAW→CURATED→Power BI) |
| 5.5 | Monitoring, alerting, operational runbook |
| 5.6 | Scale data volume to production target (150K–250K flights) |
| 5.7 | Controlled release → production deployment |

---

## 3. What can proceed NOW without waiting for governance

The following have NO OD/G4 dependency and can be done immediately:
- Register OP01/OP03/OP04 in model.json (C-01)
- Create current complete backup of main PBIX (G-01)
- Investigate `fact_route_costs_map` binding (C-03) — requires Power BI Desktop access

Everything else is gated by OD-01A/OD-01B signatures and the chain above.

---

## 4. What must NOT be done

- Do NOT rebuild the dashboard or repeat Page 01–05 development (complete).
- Do NOT treat the 5 pages as unfinished because G4/OD-04 remains blocked.
- Do NOT create reference data or synthetic data before OD-01A/01B signatures and G3-RV-01.
- Do NOT approve any governance decision (audit only).
- Do NOT modify any project implementation file.
