# AEROVISION 360 — Page 05 Complete Implementation Plan

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Plan Date:** 2026-11-08  
**Status:** IMPLEMENTATION PLAN COMPLETE — READ-ONLY DESIGN, NO IMPLEMENTATION  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Plan Objective

Implement Page 05 — Customer & Service Intelligence using only verified AEROVISION 360 native data. The plan follows the controlled one-visual-at-a-time methodology with validation after each visual.

**Architecture decision:** Native data only (Option A from Data Expansion Architecture). External Maven/Kaggle dataset cannot be integrated due to population mismatch, no common join key, license conflict, and access restrictions.

---

## 2. Implementation Scope

### 2.1 Visuals to Implement (16 total)

| Visual ID | Visual Name | Type | Measure | Data Source | Status |
|-----------|-------------|------|---------|-------------|--------|
| V01 | Total Feedback Events | KPI Card | CF01 | fact_customer_feedback | PASS |
| V02 | Average Satisfaction Score | KPI Card | CF02 | fact_customer_feedback | PASS |
| V03 | Complaint Rate | KPI Card | CF03 | fact_customer_feedback | PLANNED |
| V04 | Active Customers | KPI Card | CF04 | dim_customer | PLANNED |
| V05 | Positive Feedback Rate | KPI Card | CF09 | fact_customer_feedback | PLANNED |
| V06 | Negative Feedback Rate | KPI Card | CF10 | fact_customer_feedback | PLANNED |
| V07 | Service Recovery Rate | KPI Card | CF11 | fact_customer_feedback | PLANNED |
| V08 | Resolution Rate | KPI Card | CF12 | fact_customer_feedback | PLANNED |
| V09 | Complaint Satisfaction Avg | KPI Card | CF13 | fact_customer_feedback | PLANNED |
| V10 | Compliment Satisfaction Avg | KPI Card | CF14 | fact_customer_feedback | PLANNED |
| V11 | Feedback by Channel | Bar Chart | CF01 | fact_customer_feedback | PLANNED |
| V12 | Feedback by Type | Bar Chart | CF01 | fact_customer_feedback | PLANNED |
| V13 | Avg Satisfaction by Airline | Bar Chart | CF02 | fact_customer_feedback + dim_airline | PLANNED |
| V14 | Feedback by Resolution Status | Bar Chart | CF01 | fact_customer_feedback | PLANNED |
| V15 | Complaint Category Breakdown | Bar Chart | CF05 | fact_customer_feedback | PLANNED |
| V16 | Customer Segment Distribution | Donut Chart | COUNTROWS(dim_customer) | dim_customer | PLANNED |

### 2.2 Slicers to Implement (7 total)

| Slicer ID | Slicer Name | Table | Column | Status |
|-----------|-------------|-------|--------|--------|
| S01 | Airline | dim_airline | AirlineName | PLANNED |
| S02 | Customer Segment | dim_customer | CustomerSegment | PLANNED |
| S03 | Loyalty Tier | dim_customer | LoyaltyTier | PLANNED |
| S04 | Feedback Type | fact_customer_feedback | FeedbackType | PLANNED |
| S05 | Feedback Channel | fact_customer_feedback | FeedbackChannel | PLANNED |
| S06 | Resolution Status | fact_customer_feedback | ResolutionStatus | PLANNED |
| S07 | Date Range | dim_date | FullDate | PLANNED (requires USERELATIONSHIP) |

### 2.3 Explicitly Excluded (Unsupported)

| Excluded Component | Reason |
|-------------------|--------|
| Male/Female Passengers KPIs | No Gender field exists anywhere in project |
| Travel Type slicer/charts | No TravelType field exists anywhere in project |
| Six service ratings | Only one SatisfactionScore column exists |
| Satisfied/Dissatisfied passenger counts | OD-11 threshold pending; satisfaction not at passenger grain |
| Satisfaction by Class & Type | dim_fareClass unused (no FK); TravelType absent; fact-to-fact prohibited |
| Passengers by Travel Type & Class | TravelType absent; class unused |
| Passengers by Class donut | dim_fareClass unused; "Economy Plus" absent |
| Behaviour decomposition tree | Gender & TravelType absent; fact-to-fact prohibited |
| Gender slicer | No Gender field exists |

---

## 3. Implementation Sequence

The plan follows the controlled one-visual-at-a-time methodology:

**Phase 1: KPI Cards (V01-V10)** — Implement all 10 KPI cards first
**Phase 2: Charts (V11-V16)** — Implement all 6 charts
**Phase 3: Slicers (S01-S07)** — Implement all 7 slicers
**Phase 4: Formatting and Validation** — Apply formatting, tooltips, interactions, final QA

### Phase 1 — KPI Cards

| Order | Visual | Measure | Prerequisite | Validation Method |
|-------|--------|---------|--------------|-------------------|
| 1 | V01 Total Feedback Events | CF01 | None | Reconcile to 2,500 source rows |
| 2 | V02 Average Satisfaction Score | CF02 | V01 PASS | Reconcile to 2.99 (1,897 non-null scores) |
| 3 | V03 Complaint Rate | CF03 | V02 PASS | Reconcile to 25.52% |
| 4 | V04 Active Customers | CF04 | V03 PASS | Reconcile to 4,808 (IsActive=TRUE) |
| 5 | V05 Positive Feedback Rate | CF09 | V04 PASS | Reconcile CF06/CF01 = 603/2,500 |
| 6 | V06 Negative Feedback Rate | CF10 | V05 PASS | Reconcile (CF05+CF07)/CF01 = (638+618)/2,500 |
| 7 | V07 Service Recovery Rate | CF11 | V06 PASS | Reconcile service recovery flags / complaints |
| 8 | V08 Resolution Rate | CF12 | V07 PASS | Reconcile Resolved / non-blank ResolutionStatus |
| 9 | V09 Complaint Satisfaction Avg | CF13 | V08 PASS | Reconcile AVG(SatisfactionScore where FeedbackType=Complaint) |
| 10 | V10 Compliment Satisfaction Avg | CF14 | V09 PASS | Reconcile AVG(SatisfactionScore where FeedbackType=Compliment) |

### Phase 2 — Charts

| Order | Visual | Measure | Category/Field | Prerequisite | Validation Method |
|-------|--------|---------|----------------|--------------|-------------------|
| 11 | V11 Feedback by Channel | CF01 | FeedbackChannel | V10 PASS | Bar counts sum to 2,500 |
| 12 | V12 Feedback by Type | CF01 | FeedbackType | V11 PASS | Bar counts sum to 2,500 |
| 13 | V13 Avg Satisfaction by Airline | CF02 | AirlineName | V12 PASS | Each bar shows avg score for airline's feedback |
| 14 | V14 Feedback by Resolution Status | CF01 | ResolutionStatus | V13 PASS | Bar counts sum to 2,500 |
| 15 | V15 Complaint Category Breakdown | CF05 | ComplaintCategory | V14 PASS | Filtered to FeedbackType=Complaint; counts sum to 638 |
| 16 | V16 Customer Segment Distribution | COUNTROWS | CustomerSegment | V15 PASS | Donut segments sum to 5,000 |

### Phase 3 — Slicers

| Order | Slicer | Table | Column | Prerequisite | Validation Method |
|-------|--------|-------|--------|--------------|-------------------|
| 17 | S01 Airline | dim_airline | AirlineName | V16 PASS | Filtering changes all visual values |
| 18 | S02 Customer Segment | dim_customer | CustomerSegment | S01 PASS | Filtering changes all visual values |
| 19 | S03 Loyalty Tier | dim_customer | LoyaltyTier | S02 PASS | Filtering changes all visual values |
| 20 | S04 Feedback Type | fact_customer_feedback | FeedbackType | S03 PASS | Filtering changes all visual values |
| 21 | S05 Feedback Channel | fact_customer_feedback | FeedbackChannel | S04 PASS | Filtering changes all visual values |
| 22 | S06 Resolution Status | fact_customer_feedback | ResolutionStatus | S05 PASS | Filtering changes all visual values |
| 23 | S07 Date Range | dim_date | FullDate | S06 PASS | Requires USERELATIONSHIP; test filtering |

### Phase 4 — Formatting and Validation

| Task | Description | Prerequisite |
|------|-------------|--------------|
| Apply visual titles | All visuals need explicit titles (none set in report.json) | All visuals implemented |
| Apply number formatting | Cards: integer counts, 2 decimal places for scores, percentages with 2 decimals | All visuals implemented |
| Configure tooltips | Include measure definition, numerator, denominator, date role, disclosure | All visuals implemented |
| Configure interactions | KPI cards respond to slicers only; charts cross-highlight | All visuals + slicers |
| Apply disclosure text | "Synthetic Simulation — Not Actual Airline Performance" on page | All visuals implemented |
| Final QA | Validate all KPIs against source, test filter combinations | All formatting complete |

---

## 4. Visual Implementation Procedure (Per Visual)

For each visual, follow these 12 steps:

| Step | Action | Evidence Required |
|------|--------|-------------------|
| STEP 1 | Explain business purpose | Documented in plan |
| STEP 2 | Identify exact verified source table and fields | Source file path, column names |
| STEP 3 | Identify existing measures that can be reused | Measure name, DAX formula |
| STEP 4 | Create only necessary new DAX measures | Measure name, DAX formula (if needed) |
| STEP 5 | Explain DAX and business logic | Plain English explanation |
| STEP 6 | Build the visual in Power BI | Visual type, field wells |
| STEP 7 | Configure formatting, titles, tooltips | Title text, number format, tooltip content |
| STEP 8 | Configure filters and interactions | Slicer assignments, edit interactions |
| STEP 9 | Validate displayed result against source data | Independent calculation, match/mismatch |
| STEP 10 | Capture implementation evidence | Screenshot, values, validation result |
| STEP 11 | Update implementation tracker | Status: PASS/FAIL/BLOCKED |
| STEP 12 | Report PASS/FAIL and wait for approval | Owner confirmation before next visual |

**Rule:** Do not proceed to the next visual until the current visual has passed validation and the owner has confirmed.

---

## 5. DAX Measure Requirements

### 5.1 Existing Measures to Reuse (No New DAX Needed)

| Measure | DAX Formula | Verified Value | Used In Visuals |
|---------|-------------|----------------|-----------------|
| CF01 | COUNTROWS(fact_customer_feedback) | 2,500 | V01, V11, V12, V14 |
| CF02 | AVERAGE(fact_customer_feedback[SatisfactionScore]) | 2.99 | V02, V13 |
| CF03 | Complaint % | 25.52% | V03 |
| CF04 | COUNTROWS(FILTER(dim_customer, IsActive=TRUE)) | 4,808 | V04 |
| CF05 | COUNTROWS(FILTER(FeedbackType="Complaint")) | 638 | V15 |
| CF06 | COUNTROWS(FILTER(FeedbackType="Compliment")) | 603 | V05 |
| CF07 | COUNTROWS(FILTER(FeedbackType="Claim")) | 618 | V06 |
| CF09 | DIVIDE(CF06, CF01) | ~24.12% | V05 |
| CF10 | DIVIDE(CF05+CF07, CF01) | ~50.24% | V06 |
| CF11 | Service recovery rate | Computed | V07 |
| CF12 | Resolution rate | Computed | V08 |
| CF13 | CALCULATE(CF02, FeedbackType="Complaint") | Computed | V09 |
| CF14 | CALCULATE(CF02, FeedbackType="Compliment") | Computed | V10 |

**No new DAX measures are required.** All measures already exist and are verified.

### 5.2 New DAX Measures Required

| Measure | DAX Formula | Required For | Status |
|---------|-------------|--------------|--------|
| Customer Segment Count | COUNTROWS(dim_customer) | V16 | NEW — simple count |

---

## 6. Validation Methods

### 6.1 KPI Validation (Cards)

| Visual | Measure | Expected Value | Validation Query |
|--------|---------|----------------|------------------|
| V01 | CF01 | 2,500 | COUNT(*) from fact_customer_feedback |
| V02 | CF02 | 2.99 | AVG(SatisfactionScore) where NOT NULL |
| V03 | CF03 | 25.52% | COUNT(FeedbackType="Complaint") / COUNT(*) |
| V04 | CF04 | 4,808 | COUNT(DimCustomer where IsActive=TRUE) |
| V05 | CF09 | ~24.12% | COUNT(FeedbackType="Compliment") / COUNT(*) |
| V06 | CF10 | ~50.24% | (COUNT(Complaint) + COUNT(Claim)) / COUNT(*) |
| V07 | CF11 | Computed | COUNT(ServiceRecoveryFlag=TRUE) / COUNT(FeedbackType="Complaint") |
| V08 | CF12 | Computed | COUNT(ResolutionStatus="Resolved") / COUNT(NOT ISBLANK(ResolutionStatus)) |
| V09 | CF13 | Computed | AVG(SatisfactionScore where FeedbackType="Complaint") |
| V10 | CF14 | Computed | AVG(SatisfactionScore where FeedbackType="Compliment") |

### 6.2 Chart Validation (Bars/Donut)

| Visual | Measure | Validation Method |
|--------|---------|-------------------|
| V11 | CF01 by FeedbackChannel | Sum of all channel bars = 2,500 |
| V12 | CF01 by FeedbackType | Sum of all type bars = 2,500 |
| V13 | CF02 by AirlineName | Each bar = AVG(SatisfactionScore) for that airline's feedback |
| V14 | CF01 by ResolutionStatus | Sum of all status bars = 2,500 |
| V15 | CF05 by ComplaintCategory | Filtered to FeedbackType="Complaint"; sum = 638 |
| V16 | COUNTROWS by CustomerSegment | Sum of all segments = 5,000 |

### 6.3 Slicer Validation

| Slicer | Validation Method |
|--------|-------------------|
| S01 Airline | Select one airline; all visuals filter to that airline's feedback |
| S02 Customer Segment | Select one segment; all visuals filter to customers in that segment |
| S03 Loyalty Tier | Select one tier; all visuals filter to customers in that tier |
| S04 Feedback Type | Select one type; all visuals filter to that feedback type |
| S05 Feedback Channel | Select one channel; all visuals filter to that channel |
| S06 Resolution Status | Select one status; all visuals filter to that status |
| S07 Date Range | Select date range; requires USERELATIONSHIP on FeedbackDateKey |

---

## 7. Formatting Standards

| Element | Standard |
|---------|----------|
| Page size | 1280 × 720 (consistent with existing pages) |
| KPI card count format | Integer with thousands separator (e.g., "2,500" not "3K") |
| KPI card score format | 2 decimal places (e.g., "2.99") |
| KPI card percentage format | 2 decimal places (e.g., "25.52%") |
| Card title | Explicit title on every card (none currently set in report.json) |
| Chart title | Explicit title on every chart |
| Tooltip | Include measure definition, numerator, denominator, date role, disclosure |
| Disclosure | "Synthetic Simulation — Not Actual Airline Performance" visible on page |
| No auto-abbreviation | Cards must show full numbers, not abbreviated |

---

## 8. Dependencies and Blockers

### 7.1 Dependencies

| Dependency | Status | Impact if Not Resolved |
|------------|--------|----------------------|
| Power BI Desktop access | Required | Cannot build visuals or set titles/formatting |
| report.json import | Required | Page 05 visual definitions not in PBIX |
| CF measures registration | Verified | CF01-CF14 already registered in model |
| dim_date active relationship | INACTIVE for feedback | Date slicer (S07) requires USERELATIONSHIP |

### 7.2 Blockers

| Blocker | Severity | Description | Resolution Required |
|---------|----------|-------------|---------------------|
| OD-04 blocked facts | High | FactBookingTransactions blocked; no passenger count measures | Owner decision on OD-04 |
| OD-11 pending | High | Satisfaction scale threshold undefined | Owner decision on OD-11 |
| dim_fareClass unused | Medium | No FK to facts; class-based visuals impossible | Model change approval |
| Feedback date relationships inactive | Medium | Date slicer cannot filter feedback without USERELATIONSHIP | DAX measure design decision |
| report.json not in PBIX | High | Custom report pages not loaded into PBIX | Import report.json into PBIX |

---

## 8. Timeline Estimates (Per Visual)

| Phase | Visual Count | Est. Time per Visual | Total Est. Time |
|-------|-------------|---------------------|-----------------|
| Phase 1: KPI Cards | 10 | 30-45 minutes each | 5-7.5 hours |
| Phase 2: Charts | 6 | 45-60 minutes each | 4.5-6 hours |
| Phase 3: Slicers | 7 | 20-30 minutes each | 2-3.5 hours |
| Phase 4: Formatting & QA | — | — | 2-3 hours |
| **Total** | **23** | — | **13.5-20 hours** |

**Note:** Time estimates assume Power BI Desktop access and one-visual-at-a-time methodology with owner approval between visuals.

---

## 9. Implementation Tracker

The implementation tracker is maintained at `PAGE_05_IMPLEMENTATION_TRACKER.md`. Statuses:

| Status | Definition |
|--------|------------|
| NOT STARTED | Visual not yet begun |
| INVESTIGATING | Source data being verified |
| READY FOR IMPLEMENTATION | Source verified, ready to build |
| IN PROGRESS | Visual being built in Power BI |
| VALIDATING | Result being compared to source data |
| PASS | Visual implemented and validated |
| FAIL | Visual implemented but validation failed |
| BLOCKED | Visual cannot be implemented (governance, data missing) |

**Current status:**
- V01: PASS
- V02: PASS
- V03-V16: NOT STARTED
- S01-S07: NOT STARTED

---

## 10. Go/No-Go Criteria

### Go Criteria (Proceed with Implementation)
- [ ] Power BI Desktop access available
- [ ] report.json can be imported into PBIX
- [ ] Owner approves native-data-only architecture
- [ ] Owner approves one-visual-at-a-time methodology

### No-Go Criteria (Stop and Reassess)
- [ ] External data required but cannot be licensed/accessed
- [ ] OD-04 or OD-11 blocking required KPIs
- [ ] Owner requires unsupported reference components (Gender, Travel Type, etc.)

---

## 11. Post-Implementation QA

After all 23 elements are implemented:

| QA Item | Method | Pass/Fail |
|---------|--------|-----------|
| All KPI values match source | Independent calculation vs Power BI display | — |
| All chart values sum correctly | Bar totals = 2,500 (feedback) or 5,000 (customers) | — |
| All slicers filter correctly | Select each slicer value; verify visual changes | — |
| Date slicer works | Requires USERELATIONSHIP test | — |
| Disclosure visible | "Synthetic Simulation — Not Actual Airline Performance" on page | — |
| No unsupported fields | No Gender, TravelType, service ratings visible | — |
| No fact-to-fact cross-filter | Interaction review confirms no fact-to-fact | — |
| Number formatting correct | No "3K" abbreviation; 2 decimal places for scores | — |
| Mobile layout | 9:16 portrait; disclosure visible | — |

---

## 12. Conclusion

The implementation plan provides a complete, controlled path to build Page 05 using only verified AEROVISION 360 native data. All 10 KPI cards use existing CF measures that are validated against source. All 6 charts and 7 slicers use existing tables and columns. No new DAX measures are required (except a simple count for the donut chart). No external data is needed. No governance restrictions are bypassed.

The plan is ready for execution, beginning with Visual 3 (Complaint Rate, CF03) after owner approval.
