# AEROVISION 360 — Page 05 Data Governance and Risk Register

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Register Date:** 2026-11-08  
**Status:** GOVERNANCE REGISTER COMPLETE — READ-ONLY  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Governance Framework

This register documents all governance restrictions, open decisions, risks, and compliance requirements that apply to Page 05 — Customer & Service Intelligence implementation.

---

## 2. Active Governance Restrictions

### 2.1 OD-04 — Exchange Rate Policy (UNRESOLVED)

| Attribute | Value |
|-----------|-------|
| Decision ID | OD-04 |
| Status | UNRESOLVED — owner decision pending |
| Affected tables | FactBookingTransactions, FactOperatingCosts |
| Affected measures | RV_* (revenue/passenger), CX_* (cost), NC_* (financial) |
| Page 05 impact | Total Passengers KPI cannot use booking-based passenger counts; RV_RevenuePassengers (8,922) unavailable |
| Required action | Owner decision on OD-04 before any booking-based measure can be used |
| Workaround | Use CF01 (Total Feedback Events = 2,500) as volume proxy; document limitation |

**OD-04 sub-decisions:**
- OD-04a: Currency scope (AED, QAR, SGD, INR, GBP, EUR, USD, AUD)
- OD-04b: Exchange rate convention (USD per one unit, exact-date lookup, 6 decimals, round to 2 decimals, no forward-fill)
- OD-04c: Rate source (AEROVISION-360-SYNTHETIC-FX-V1)
- OD-04d: Rate version (FX-2026-11-04-001)
- OD-04e: Missing date behaviour (no forward-fill; missing exact-date rate quarantines the row)
- OD-04f: Rate generation methodology (deterministic, fixed seed)

### 2.2 OD-11 — Satisfaction Score Scale Definition (PENDING)

| Attribute | Value |
|-----------|-------|
| Decision ID | OD-11 |
| Status | OWNER APPROVAL PENDING |
| Affected measures | CF02 (Average Satisfaction Score), any "satisfied/dissatisfied" classification |
| Page 05 impact | No approved threshold for classifying satisfaction as "satisfied" (4–5) vs "neutral/dissatisfied" (1–3); cannot build Satisfied/Neutral-Dissatisfied KPI counts |
| Required action | Owner approval of satisfaction score scale thresholds |
| Workaround | Use CF02 average score (2.99) as satisfaction metric; document that 1–5 scale is provisional |

### 2.3 Fact-to-Fact Join Prohibition (ENFORCED)

| Attribute | Value |
|-----------|-------|
| Policy source | Data Contracts Section 5.1; RELATIONSHIP_VALIDATION.csv rows 21-22 |
| Status | ENFORCED — fact-to-fact relationships not allowed |
| Affected analysis | Cannot join FactBookingTransactions with FactCustomerFeedback at passenger level |
| Page 05 impact | Cannot compute "satisfied passengers" by combining booking passenger counts with feedback satisfaction |
| Required action | Governance review and approval before any fact-to-fact relationship |
| Workaround | Analysis limited to shared dimensions (DimCustomer, DimAirline, DimRoute) |

### 2.4 OD-09 — On-Time Performance Threshold (PENDING)

| Attribute | Value |
|-----------|-------|
| Decision ID | OD-09 |
| Status | OWNER APPROVAL PENDING |
| Page 05 impact | Not directly relevant to Page 05 (operations-focused) |
| Required action | Owner decision if OTP metrics needed on Page 05 |

---

## 3. Risk Register

| Risk ID | Risk | Likelihood | Impact | Severity | Mitigation | Owner |
|---------|------|------------|--------|----------|------------|-------|
| R-01 | OD-04 remains unresolved; booking-based passenger measures unavailable | High | High | HIGH | Use CF01 as volume proxy; document limitation; escalate for owner decision | Data Governance |
| R-02 | OD-11 threshold undefined; no satisfied/dissatisfied classification | High | High | HIGH | Use CF02 average score only; document that counts are not possible | Data Governance |
| R-03 | dim_fareClass unused (no FK to facts); class-based visuals impossible | Medium | Medium | MEDIUM | Document as limitation; do not build class donut or satisfaction-by-class | Data Engineering |
| R-04 | FactCustomerFeedback date relationships inactive; date slicer won't filter feedback | Medium | Medium | MEDIUM | Use USERELATIONSHIP in measures; document limitation | DAX Engineer |
| R-05 | No Gender field; Male/Female KPIs cannot be built | High | High | HIGH | Exclude Male/Female KPIs from scope; document as unsupported | Data Governance |
| R-06 | No TravelType field; Travel Type slicer/charts cannot be built | High | High | HIGH | Exclude Travel Type from scope; document as unsupported | Data Governance |
| R-07 | No six service-rating columns; only SatisfactionScore exists | High | High | HIGH | Exclude six service ratings; use CF02 + ComplaintCategory as proxy | Data Governance |
| R-08 | report.json Page 05 not loaded into PBIX (blank report) | High | High | HIGH | Import report.json into PBIX; verify pages load correctly | Power BI Admin |
| R-09 | model.json has incorrect FL01/FL02/CF03 expressions | Medium | Low | LOW | Use DAX file expressions (authoritative); ignore model.json for measure logic | DAX Engineer |
| R-10 | semantic_model.json incomplete relationships | Medium | Low | LOW | Use semantic_model.json for column/relationship reference; verify in PBIX | Data Engineering |
| R-11 | External Maven/Kaggle dataset cannot be integrated (population mismatch, license conflict, access blocked) | High | High | HIGH | Do not integrate external data; build Page 05 with native data only | Data Governance |
| R-12 | Passenger count grain ambiguity (coupons vs passengers vs customers) | Medium | Medium | MEDIUM | Document grain distinctions; use CF01 (feedback events) not passenger counts | Data Engineering |
| R-13 | 603 NULL SatisfactionScore values (24.1% missing) | Medium | Medium | MEDIUM | CF02 computed on 1,897 non-null scores; document NULL exclusion | Data Quality |
| R-14 | 1,862 NULL ComplaintCategory values (74.5% missing) | Medium | Low | LOW | ComplaintCategory only populated for complaints (638 events); use for complaint breakdown only | Data Quality |

---

## 4. Compliance Requirements

### 4.1 Data Contract Compliance (03_DATA_CONTRACTS.md v1.5)

| Contract Section | Requirement | Page 05 Status | Evidence |
|-----------------|-------------|----------------|----------|
| C-08 | All operational, customer, and financial data synthetic; no real passenger personal information | COMPLIANT | All data synthetic; no personal identifiers |
| C-11 | Flight-leg grain: one row per scheduled flight leg | N/A | Not used for Page 05 KPIs |
| Section 5.1 | No fact-to-fact relationships | COMPLIANT | No fact-to-fact joins used |
| Section 5.6 | FactCustomerFeedback grain: one row per feedback event | COMPLIANT | All CF measures respect feedback-event grain |
| Section 6.712 | Required columns never null; optional columns use null | COMPLIANT | SatisfactionScore NULLs documented (603) |
| Section 7.3 | Grain uniqueness tests | COMPLIANT | FeedbackKey unique; BookingTransactionKey unique |
| Section 9 | Date and timestamp rules | PARTIAL | FeedbackDateKey relationship inactive; requires USERELATIONSHIP |
| Section 10 | Currency conversion rules | N/A | No currency measures on Page 05 |
| Section 11 | KPI definitions (K-17 through K-21 for Page 05) | PARTIAL | K-17/K-20 blocked by OD-04; K-18/K-19/K-21 available |

### 4.2 Power BI Dashboard Specification Compliance

| Specification Section | Requirement | Page 05 Status | Evidence |
|----------------------|-------------|----------------|----------|
| Section 2.9 | No unsupported fields added | COMPLIANT | No Gender, TravelType, or service-rating fields |
| Section 2.9 | Missing field becomes OWNER DECISION REQUIRED, not silent invention | COMPLIANT | All missing fields documented as unsupported |
| Section 4 | KPI cards respond to page slicers only | PLANNED | Will be configured in Power BI |
| Section 4 | No fact-to-fact cross-filtering | COMPLIANT | No fact-to-fact relationships |
| Section 4 | Date roles labelled | PLANNED | Will label feedback date role on trends |
| Section 2.7 | Custom tooltips with disclosure | PLANNED | Will include disclosure in tooltips |
| Section 2.7 | Default tooltips disabled | PLANNED | Will disable default tooltips |
| Section 3 | Page 5 = Customer & Service Intelligence | COMPLIANT | Page exists in report.json |
| DB-05 | No unsupported severity/sentiment/service-category field | COMPLIANT | No such fields used |
| DB-06 | No fact-to-fact visual cross-filtering | COMPLIANT | No fact-to-fact relationships |
| DB-08 | Date roles labelled | PLANNED | Will label feedback date role |

### 4.3 Disclosure Requirements

| Requirement | Specification | Page 05 Status |
|-------------|--------------|----------------|
| Page disclosure | "Synthetic Simulation — Not Actual Airline Performance" on every page | PLANNED — will add to Page 05 |
| Tooltip disclosure | Same string in every custom tooltip | PLANNED |
| Export disclosure | Export filename includes "synthetic" and run ID | N/A — export disabled until T-79 passes |
| Mobile disclosure | Visible on mobile layout | PLANNED |

---

## 5. Open Decisions Requiring Owner Approval

| Decision ID | Decision Needed | Impact on Page 05 | Current Status |
|-------------|-----------------|-------------------|----------------|
| OD-04 | Exchange rate policy resolution | Unblocks RV_* passenger/revenue measures | UNRESOLVED |
| OD-11 | Satisfaction score scale threshold (1–5 classification) | Unblocks Satisfied/Dissatisfied counts | OWNER APPROVAL PENDING |
| OD-09 | OTP threshold | Not directly relevant to Page 05 | OWNER APPROVAL PENDING |
| OD-13 | Cost classification | Not relevant to Page 05 | OWNER APPROVAL PENDING |
| OD-17 | Service recovery definition | CF11 already uses ServiceRecoveryFlag; definition pending | OWNER APPROVAL PENDING |
| G3-RV-01 | Reference version approval | Not directly relevant to Page 05 | PENDING |

---

## 6. Data Quality Risk Assessment

### 6.1 FactCustomerFeedback Data Quality

| Quality Dimension | Finding | Impact | Mitigation |
|-------------------|---------|--------|------------|
| Completeness | SatisfactionScore: 603 NULLs (24.1%) | CF02 computed on 1,897 non-null scores | Document NULL exclusion; do not impute |
| Completeness | ComplaintCategory: 1,862 NULLs (74.5%) | Only populated for 638 complaints | Use for complaint breakdown only |
| Completeness | ResolutionDateKey: 1,896 NULLs (75.8%) | Only populated for resolved cases | Use for resolution analysis only |
| Uniqueness | FeedbackKey: 2,500 unique; FeedbackID: 2,500 unique | No duplicates | No impact |
| Referential Integrity | CustomerKey: 0 orphans; AirlineKey: 0 orphans; RouteKey: 0 orphans | All FKs resolve | No impact |
| Consistency | ResolutionDateKey on/after FeedbackDateKey | Verified | No impact |

### 6.2 DimCustomer Data Quality

| Quality Dimension | Finding | Impact | Mitigation |
|-------------------|---------|--------|------------|
| Completeness | No NULLs in any column | No impact | No impact |
| Uniqueness | CustomerKey: 5,000 unique | No impact | No impact |
| Referential Integrity | PK unique and non-null | No impact | No impact |

### 6.3 Grain Distinction Risk

| Risk | Description | Mitigation |
|------|-------------|------------|
| Feedback events vs passengers | 2,500 feedback events ≠ 9,956 coupons ≠ 8,922 revenue passengers ≠ 4,204 customers with bookings | Document grain distinctions; use CF01 as "feedback events" not "passengers" |
| CF02 vs passenger satisfaction | Average satisfaction across feedback events, not passengers | Label as "Average Satisfaction Score" not "Passenger Satisfaction" |

---

## 7. Mitigation Actions Tracker

| Action ID | Action | Priority | Owner | Due | Status |
|-----------|--------|----------|-------|-----|--------|
| A-01 | Escalate OD-04 for owner decision | High | Data Governance | Before Visual 3 | PENDING |
| A-02 | Escalate OD-11 for satisfaction threshold approval | High | Data Governance | Before satisfied/dissatisfied KPIs | PENDING |
| A-03 | Document Gender field absence in Page 05 design | Medium | Data Architect | Before Visual 1 | COMPLETE |
| A-04 | Document TravelType field absence in Page 05 design | Medium | Data Architect | Before Visual 1 | COMPLETE |
| A-05 | Document six service ratings absence in Page 05 design | Medium | Data Architect | Before Visual 1 | COMPLETE |
| A-06 | Import report.json into PBIX | High | Power BI Admin | Before visual implementation | PENDING |
| A-07 | Configure USERELATIONSHIP for FeedbackDateKey | Medium | DAX Engineer | Before Date slicer | PENDING |
| A-08 | Validate all CF measures against source | High | Data Analyst | During Visual 1-10 | IN PROGRESS |

---

## 8. Decision Log

| Decision | Date | Decision | Rationale |
|----------|------|----------|-----------|
| D-01 | 2026-11-08 | Build Page 05 with native data only (Option A) | External Maven/Kaggle dataset cannot be integrated (population mismatch, no common key, license conflict, access blocked) |
| D-02 | 2026-11-08 | Exclude Male/Female KPIs | No Gender field exists; zero fabrication rule |
| D-03 | 2026-11-08 | Exclude Travel Type slicer/charts | No TravelType field exists |
| D-04 | 2026-11-08 | Exclude six service ratings | Only one SatisfactionScore column exists |
| D-05 | 2026-11-08 | Exclude Satisfied/Dissatisfied counts | OD-11 threshold pending; satisfaction not at passenger grain |
| D-06 | 2026-11-08 | Exclude class-based visuals | dim_fareClass unused (no FK); "Economy Plus" absent |
| D-07 | 2026-11-08 | Exclude behaviour decomposition tree | Gender & TravelType absent; fact-to-fact prohibited |
| D-08 | 2026-11-08 | Build V01 (CF01) and V02 (CF02) first | Both measures verified against source; lowest risk |

---

## 9. Escalation Contacts

| Escalation Level | Contact | Responsibility |
|-----------------|---------|----------------|
| Data Governance | Owner decision on OD-04, OD-11, OD-09 | Unblock blocked measures and thresholds |
| Data Engineering | Model changes, relationship configuration | dim_fareClass FK, date relationship activation |
| DAX Engineer | Measure design, USERELATIONSHIP | Feedback date filtering, complex calculations |
| Power BI Admin | PBIX import, report deployment | Getting report.json into PBIX |
| Data Quality | Source data validation, profiling | Reconciliation evidence, NULL handling documentation |

---

## 10. Register Review Cycle

| Review Type | Frequency | Trigger |
|-------------|-----------|---------|
| Governance status check | Weekly | OD-04, OD-11 status changes |
| Risk review | Before each visual | New risks identified during implementation |
| Compliance audit | Before Page 05 release | All DB-01 through DB-11 criteria |
| Data quality revalidation | After any source data refresh | CF measures re-reconciled |

---

## 11. Conclusion

The Page 05 implementation can proceed using only verified AEROVISION 360 native data (CF01-CF14 measures) with the following governance conditions:

1. **OD-04 must remain respected** — No booking-based passenger/revenue measures
2. **OD-11 must remain pending** — No satisfaction thresholds or satisfied/dissatisfied counts
3. **Fact-to-fact joins must remain prohibited** — No booking-feedback passenger-level analysis
4. **No Gender, TravelType, or service-rating fields** — These do not exist; cannot be fabricated
5. **All disclosures must be present** — "Synthetic Simulation — Not Actual Airline Performance" on every visual

The two highest-priority risks (R-01 OD-04 and R-02 OD-11) require owner decisions before certain reference components can be considered. All other risks are manageable within the native-data architecture.
