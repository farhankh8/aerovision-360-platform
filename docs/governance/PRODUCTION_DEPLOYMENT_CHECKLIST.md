# AEROVISION 360 — Production Deployment Checklist

**Checklist ID:** PROD-DEPLOY-2026-11-08  
**Prepared:** 2026-11-08  
**Prepared by:** Autonomous engineering agent (OpenCode)  
**Status:** PREPARED — BLOCKED pending external access and owner authorization

---

## 1. Prerequisites (All Must Be Complete Before Deployment)

| # | Prerequisite | Status | Dependency |
|---|---|---|---|
| 1 | OD-04g owner signature and actual approval date | PENDING | Owner action |
| 2 | GOV-D-04 addendum execution | PENDING | Owner action |
| 3 | GOV-D-06 formal approval | PENDING | Owner action |
| 4 | GOV-D-07 implementation authorization | PENDING | Owner action |
| 5 | GOV-D-08 implementation authorization | PENDING | Owner action |
| 6 | D-02 independent reviewer limitation acceptance | PENDING | Owner action |
| 7 | CC-01 owner self-review execution | PENDING | Owner personal execution |
| 8 | OD-01A formal signature and approval date | PENDING | Owner action (after preconditions 1-7) |
| 9 | OD-01B formal signature and approval date | PENDING | Owner action (after OD-01A) |
| 10 | G3-RV-01 executed | BLOCKED | Steps 1-9 |
| 11 | Schema freeze authorized | BLOCKED | Step 10 |
| 12 | G3 approved | BLOCKED | Step 11 |
| 13 | G4 written authorization | BLOCKED | Step 12 |
| 14 | Financial sources integrated into PBIX | BLOCKED | Step 13 + data_sources.json patch |
| 15 | Page 03/04 financial validation | BLOCKED | Step 14 |
| 16 | Excel consistency validation | BLOCKED | Step 14 |
| 17 | Power BI workspace ID | NOT PROVIDED | External access — owner must supply |
| 18 | Power BI credentials | NOT PROVIDED | External access — owner must supply |
| 19 | Gateway configuration | NOT CONFIGURED | External access — owner must supply |
| 20 | Refresh schedule | NOT SET | External access — owner must supply |
| 21 | RLS configuration | NOT CONFIGURED | External access — owner must supply |
| 22 | Monitoring/alerting | NOT CONFIGURED | External access — owner must supply |

**Deployment status:** BLOCKED — 17 of 22 prerequisites incomplete

---

## 2. External Access Requirements (Owner Must Supply)

| Access | Purpose | Status | How to Provide |
|---|---|---|---|
| Power BI workspace ID | Target workspace for PBIX publication | NOT PROVIDED | Secure channel — do not email or commit |
| Power BI credentials | Authentication for publishing | NOT PROVIDED | Secure channel — do not email or commit |
| Gateway configuration | Scheduled data refresh | NOT CONFIGURED | Owner configures in Power BI service |
| Refresh schedule | Automated refresh cadence | NOT SET | Owner sets in Power BI service |
| RLS roles and rules | Row-level security | NOT CONFIGURED | Owner configures in Power BI service |
| Monitoring/alerting | Production observability | NOT CONFIGURED | Owner configures in Power BI service |
| Git remote authorization | Commit and push to `main` | NOT AUTHORIZED | Owner authorizes in Git hosting platform |

**Security Note:** Do not send passwords, tokens, or connection strings in plain text. Use secure channels (password manager, secure file share, or direct entry in Power BI service/Git hosting).

---

## 3. Deployment Steps (To Be Executed After Prerequisites)

1. **Publish PBIX** to Power BI workspace using owner-provided credentials
2. **Configure dataset/semantic model** in workspace
3. **Configure gateway** for scheduled refresh
4. **Set refresh schedule** (daily recommended)
5. **Configure RLS** roles and rules
6. **Configure monitoring and alerting**
7. **Verify publication** — report opens in Power BI service
8. **Execute post-publication smoke tests** (Section 4)

---

## 4. Post-Publication Smoke Tests

| Test | Description | Expected Result | Status |
|---|---|---|---|
| Report-opening smoke test | Open published report in Power BI service | Report loads without errors | NOT EXECUTED |
| Data refresh smoke test | Trigger scheduled refresh | Refresh completes successfully | NOT EXECUTED |
| Page navigation checks | Navigate all 5 pages | All pages render correctly | NOT EXECUTED |
| KPI verification | Verify key KPIs match source data | KPI values match curated data | NOT EXECUTED |
| Permission checks | Verify RLS restricts data appropriately | Users see only authorized data | NOT EXECUTED |
| Excel deliverable verification | Verify Excel file accessible | Excel opens and calculates correctly | NOT EXECUTED |
| Release artifact integrity | Verify published artifacts match source | Hashes match local artifacts | NOT EXECUTED |

---

## 5. What OpenCode Can Do vs. What Owner Must Do

**OpenCode can (prepared, pending authorization):**
- All local technical validation (tests, hashes, file integrity)
- Data_sources.json integration patch (pending OD-04g + G4)
- Financial PBIX integration (pending OD-04g + G4)
- Page 03/04 validation (pending financial integration)
- Excel consistency validation (pending authorized sources)
- Production deployment checklist (this document)
- Smoke test plan (this document)
- Git release manifest and file classification (RELEASE_FILE_CLASSIFICATION.md)

**OpenCode cannot (requires owner/external):**
- Sign OD-04g, GOV-D-04/06/07/08, D-02, OD-01A, OD-01B
- Execute CC-01 self-review
- Authorize G3-RV-01, schema freeze, G3, G4
- Provide Power BI workspace ID, credentials, gateway
- Configure refresh schedule, RLS, monitoring, alerting
- Authorize Git commit and push
- Execute production publication

---

**End of Production Deployment Checklist.**  
No deployment has been attempted. All externally dependent items are blocked pending owner-provided access and authorization.
