# AEROVISION 360 — Post-Publication Smoke Test Plan

**Plan ID:** SMOKE-TEST-2026-11-08  
**Prepared:** 2026-11-08  
**Prepared by:** Autonomous engineering agent (OpenCode)  
**Status:** PLAN PREPARED — BLOCKED pending production deployment

---

## 1. Test Overview

These smoke tests verify that the published AEROVISION 360 solution functions correctly in the production Power BI environment. All tests must pass before the release is considered valid.

**Execution environment:** Power BI Service (published workspace)  
**Required access:** Owner-provided workspace credentials  
**Prerequisite:** Production deployment complete (PROD-DEPLOY-2026-11-08)

---

## 2. Smoke Test Cases

| ID | Test | Description | Expected Result | Pass/Fail | Evidence |
|---|---|---|---|---|---|
| SMT-01 | Report opening | Open published AEROVISION_360 report in Power BI service | Report loads within 30 seconds; no error messages | NOT EXECUTED | Screenshot or service log |
| SMT-02 | Data refresh | Trigger manual or scheduled refresh of the semantic model | Refresh completes successfully; no refresh errors | NOT EXECUTED | Refresh history log |
| SMT-03 | Page navigation | Navigate all 5 pages: Executive Overview, Operations, Revenue & Finance, Cost & Financial Intelligence, Customer & Service Intelligence | All 5 pages render correctly; no missing visuals | NOT EXECUTED | Navigation log |
| SMT-04 | KPI verification | Verify key KPIs against source data: FL01=4,776; FL02=218,413; RV_TotalOperatingRevenueUSD; CX_TotalOperatingCostsUSD | KPI values match curated source data within rounding tolerance | NOT EXECUTED | Query results vs source CSV |
| SMT-05 | Permission checks | Verify RLS restricts data by user role | Users see only data authorized for their role | NOT EXECUTED | RLS test results |
| SMT-06 | Excel deliverable | Verify Excel workbook accessible and calculates correctly | Excel opens; formulas compute; no #ERROR values | NOT EXECUTED | File open verification |
| SMT-07 | Release artifact integrity | Verify published artifacts match local source files | SHA-256 hashes match pre-publication values | NOT EXECUTED | Hash comparison |
| SMT-08 | Synthetic disclosure | Verify "Synthetic Simulation — Not Actual Airline Performance" appears on all pages | Disclosure visible on every page, tooltip, and export | NOT EXECUTED | Visual inspection |

---

## 3. Test Execution Procedure

1. Obtain owner-provided Power BI workspace credentials
2. Navigate to the published AEROVISION_360 workspace
3. Execute tests SMT-01 through SMT-08 in order
4. Record pass/fail and evidence for each test
5. If any test fails, investigate root cause and remediate before release validation
6. Only after all 8 tests pass, report release as validated

---

## 4. Entry Criteria

- [ ] Production deployment complete (PROD-DEPLOY-2026-11-08)
- [ ] Owner-provided workspace access confirmed
- [ ] All 5 report pages published
- [ ] Semantic model published and refreshed
- [ ] Excel workbook accessible

---

## 5. Exit Criteria

- [ ] All 8 smoke tests passed
- [ ] Evidence recorded for each test
- [ ] No critical defects remaining
- [ ] Owner sign-off on smoke test results

---

## 6. What OpenCode Can Do vs. What Owner Must Do

**OpenCode can (prepared):**
- This smoke test plan (this document)
- Expected results and evidence requirements
- Entry/exit criteria definition

**OpenCode cannot (requires owner/external):**
- Execute smoke tests against live Power BI service
- Provide workspace credentials
- Verify published report rendering
- Confirm refresh completion
- Sign off on test results

---

**End of Post-Publication Smoke Test Plan.**  
No smoke tests have been executed. All tests are blocked pending production deployment and owner-provided access.
