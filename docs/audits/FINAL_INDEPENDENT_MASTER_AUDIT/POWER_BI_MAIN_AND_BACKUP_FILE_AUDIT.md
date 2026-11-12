# POWER BI MAIN AND BACKUP FILE AUDIT

**Project root:** `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`  
**Audit mode:** Read-only. PBIX files extracted as ZIP for structural inspection only; not opened in Power BI Desktop; not modified, resaved, or republished.

---

## 1. PBIX version inventory

| # | File | Full path | Size | Last modified | SHA-256 | Pages | Visuals | Readable? | Authoritative? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `AEROVISION_360.pbix` (main) | `deliverables/power_bi/AEROVISION_360.pbix` | 9,422,203 bytes (~9 MB) | 08-11-2026 14:41 | `4E02560D1496E715526CCE779729F99B94E2F64FA7695FE141A0A9B863F96440` | 5 | 120 | Yes (structure extracted) | **YES** |
| 2 | `AEROVISION_360_VERIFIED_BACKUP.pbix` | `deliverables/power_bi/AEROVISION_360_VERIFIED_BACKUP.pbix` | 1,003,650 bytes (~1 MB) | 05-11-2026 18:11 | `64136DE1142B6A0D643A45AD2AC90A9797294145178D03DF2977F2EC609E40CE` | 1 (stub "Page 1") | 0 | Yes (structure extracted) | No — stale stub |
| 3 | `AEROVISION_360_PRE_IMPLEMENTATION_BACKUP.pbix` | `deliverables/power_bi/AEROVISION_360_PRE_IMPLEMENTATION_BACKUP.pbix` | 1,003,650 bytes (~1 MB) | 05-11-2026 18:16 | `4AC59DF8D34DFB51D6403F0BE5E68EDE3EE1465DA83FDCF51FB9F20B758E18C9` | 1 (stub "Page 1") | 0 | Yes (structure extracted) | No — stale stub |

Also present: `deliverables/power_bi/AEROVISION_360.pbip` (195 bytes), `.platform` (182 bytes) — the Fabric/git project definition alongside the PBIX.

---

## 2. Authoritative version determination

**The main PBIX (`AEROVISION_360.pbix`) is the authoritative version.**

Evidence:
- **Size:** 9.4 MB vs 1 MB backups — the main file contains the full report model and visuals; backups are minimal stubs.
- **Modification date:** main PBIX modified 08-11-2026 (today), backups 05-11-2026 — the main PBIX is the most recently authored.
- **Content:** main PBIX has 5 pages and 120 visuals; each backup has 1 stub page ("Page 1") and 0 visuals.
- **Hash:** all three files have distinct SHA-256 hashes; neither backup equals the main.

**Do not assume the largest file is automatically correct** — in this case the largest file IS correct and current. **Do not assume an older PBIX is the latest** — the older backups are stubs. **Do not assume `report.json` represents the complete current Desktop state** — the extracted `report.json`/`layout` describes 5 pages but only 44 visuals with different page names ("Network & Capacity Intelligence", "Operations & Disruption"); the binary PBIX contains 120 visuals with the owner's actual page names (01 Executive Overview … 05 Customer & Service Intelligence). The binary PBIX is authoritative over the extracted layout.

---

## 3. Backup consistency

**Backups are NOT consistent with the main PBIX.**

| Aspect | Main PBIX | Verified backup | Pre-impl backup | Consistent? |
|---|---|---|---|---|
| File size | 9,422,203 | 1,003,650 | 1,003,650 | No |
| Pages | 5 | 1 | 1 | No |
| Page name(s) | 01 Executive Overview … 05 Customer & Service Intelligence | "Page 1" | "Page 1" | No |
| Visuals | 120 | 0 | 0 | No |
| SHA-256 | `4E02560D…` | `64136DE1…` | `4AC59DF8…` | No (all differ) |

Both backups are effectively empty report shells (single generic page, no visuals). They **cannot** be used as recovery or rollback sources for the current 5-page report. The names "VERIFIED_BACKUP" and "PRE_IMPLEMENTATION_BACKUP" are misleading — neither is a verified or complete backup of the current report.

**Finding PBX-01 (HIGH):** Backup PBIX files are inconsistent with the authoritative main PBIX and must not be relied upon for recovery. Recommendation: once governance gates permit, create a current, complete backup of the main PBIX.

---

## 4. PBIX internal structure (main file)

Extracted from `AEROVISION_360.pbix`:

- `Report/definition/report.json` — schema `item/report/definition/report/3.3.0`; theme Fluent2-CY26SU08; 5 registered resource images + `Customer_&_Service_Intelligenc…png`
- `Report/definition/pages/` — 5 page folders:
  - `85169b8764991979ada4` → `01 - Executive Overview` (24 visuals)
  - `3ba663f9b94b183d8484` → `02 - Operations` (23 visuals)
  - `3c0e9656b72579cb4105` → `Revenue & Finance.` (23 visuals) [Page 03]
  - `ad43d4cc257c455c5a9b` → `COST & FINANCIAL INTELLIGENCE` (23 visuals) [Page 04]
  - `18bdd7f468e4853e0a00` → `05 - Customer & Service Intelligence` (27 visuals)
- `Report/definition/pages/*/visuals/*/visual.json` — per-visual type, title, position, query bindings
- `DataModel` — 2.5 MB serialized binary model stream (could not be deserialized in this read-only environment — limitation L-2)
- `Settings` — Version 4; RelationshipImportEnabled=true; TypeDetectionEnabled=true
- `Version` — 1.32

**Finding PBX-02 (HIGH):** The extracted project layout (`report.json`/`pbip`) and the binary PBIX disagree on page names and visual counts. The binary PBIX (120 visuals, owner's page names) is authoritative; the extracted layout appears to be a simplified/placeholder export. Do not use the extracted layout as the source of truth for the report.

---

## 5. Related Power BI project files (extracted layout)

| File | Path | Size | Role |
|---|---|---|---|
| Project definition | `deliverables/power_bi/AEROVISION_360.pbip` | 195 bytes | Fabric project manifest (name "AEROVISION 360", modelId `aerovision-360-fixed`) |
| Platform marker | `deliverables/power_bi/.platform` | 182 bytes | Logical ID `aerovision360` |
| Report layout | `deliverables/power_bi/report/report.json` | ~ | 5 pages, 44 visuals (simplified; differs from binary) |
| Semantic model | `deliverables/power_bi/semantic_model/model.json` | ~ | 16 tables, 51 registered measures |
| Semantic model detail | `deliverables/power_bi/semantic_model/semantic_model.json` | ~ | Columns, measures, relationships, disclosure |
| DAX measures | `deliverables/power_bi/dax/AEROVISION360_Measures.dax` | ~ | 54 measures (see Phase C audit) |
| Power Query | `deliverables/power_bi/power_query/AEROVISION360_DataLoad.m` | ~ | 16 query blocks |
| Data sources | `deliverables/power_bi/data_sources/data_sources.json` | ~ | 14 CSV sources (omits fact_booking_transactions, fact_operating_costs) |
| Theme | `deliverables/power_bi/theme/theme.json` | ~ | Report theme |
| PBIX audit folder | `deliverables/power_bi/audit/` | — | PBIX-level audit reports (DAX, relationships, data quality, governance) |

---

## 6. PBIX audit findings register

| ID | Finding | Severity | Evidence | Recommended action |
|---|---|---|---|---|
| PBX-01 | Backup PBIX files are 1-page stubs, inconsistent with the 5-page/120-visual main PBIX; cannot serve as recovery source | HIGH | PBIX version inventory; hashes differ | Create current complete backup of main PBIX after gates permit |
| PBX-02 | Extracted `report.json`/layout disagrees with binary PBIX (44 visuals, different page names vs 120 visuals, owner page names) | HIGH | Binary page.json vs extracted report.json | Treat binary PBIX as authoritative; do not rely on extracted layout |
| PBX-03 | In-PBIX `DataModel` (2.5 MB binary) not deserializable; in-PBIX relationships not independently verified vs `model.json` | MEDIUM | Limitation L-2 | Verify model in Power BI Desktop once accessible |
| PBX-04 | Main PBIX is the most recently modified (08-11-2026) and largest (9.4 MB) — authoritative | INFORMATIONAL | File metadata | Confirmed main PBIX is authoritative |

---

## 7. Conclusion

The main PBIX is a genuine, populated 5-page report with 120 visuals and is the authoritative Power BI deliverable. The two backup PBIX files are stale stubs and are not consistent with the main file. The report itself is built; what remains blocked is data loading/refresh (governance-gated), not report development.
