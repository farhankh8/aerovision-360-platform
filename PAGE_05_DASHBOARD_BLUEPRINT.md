# AEROVISION 360 — Page 05 Dashboard Blueprint

**Page:** Customer & Service Intelligence — Passenger Satisfaction Review  
**Design Date:** 2026-11-08  
**Status:** DESIGN COMPLETE — AWAITING IMPLEMENTATION APPROVAL  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## Design Principles

1. **Accuracy before appearance** — Every number must be traceable to source data
2. **No fabricated data** — No invented columns, measures, gender, travel types, or service ratings
3. **Governance compliance** — OD-04 blocked facts not used; OD-11 thresholds not invented
4. **Grain integrity** — Feedback events, passengers, bookings, and customers never treated as interchangeable
5. **Reuse existing measures** — CF01–CF14 are verified; no unnecessary DAX duplication
6. **Professional layout** — Clean, executive-ready, consistent with AEROVISION 360 branding

---

## Page Layout (1280 × 720)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  [AEROVISION 360 Header — Navy Blue]                                        │
│  Customer & Service Intelligence                                            │
│  Passenger Satisfaction Review                                              │
│  [Airline Slicer] [Customer Segment Slicer] [Date Range Slicer*]            │
├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┤
│  KPI Card 1  │  KPI Card 2  │  KPI Card 3  │  KPI Card 4  │  KPI Card 5  │
│  Total       │  Average     │  Complaint   │  Active      │  Positive    │
│  Feedback    │  Satisfaction│  Rate        │  Customers   │  Feedback    │
│  Events      │  Score       │              │              │  Rate        │
│  (CF01)      │  (CF02)      │  (CF03)      │  (CF04)      │  (CF09)      │
├──────────────┴──────────────┴──────────────┴──────────────┴──────────────┤
│  KPI Card 6  │  KPI Card 7  │  KPI Card 8  │  KPI Card 9  │  KPI Card 10 │
│  Negative    │  Service     │  Resolution  │  Complaint   │  Compliment  │
│  Feedback    │  Recovery    │  Rate        │  Sat vs      │  Sat vs      │
│  Rate        │  Rate        │              |  Compliment  |  Compliment  │
│  (CF10)      │  (CF11)      │  (CF12)      │  (CF13)      │  (CF14)      │
├─────────────────────────────────────────────────────────────────────────────┤
│  Chart 1: Feedback by Channel        │  Chart 2: Feedback by Type        │
│  (Bar Chart — CF01)                  │  (Bar Chart — CF01)               │
├──────────────────────────────────────┴──────────────────────────────────────┤
│  Chart 3: Avg Satisfaction by Airline    │  Chart 4: Feedback by Resolution│
│  (Bar Chart — CF02)                      │  Status (Bar Chart — CF01)      │
├─────────────────────────────────────────────────────────────────────────────┤
│  Chart 5: Complaint Category Breakdown   │  Chart 6: Customer Segment      │
│  (Bar Chart — CF05 by ComplaintCategory) │  Distribution (Donut)           │
├─────────────────────────────────────────────────────────────────────────────┤
│  [Slicers: Airline | Customer Segment | Loyalty Tier | Feedback Type |      │
│   Feedback Channel | Resolution Status | Date Range*] — right rail           │
│  [*Date slicer requires USERELATIONSHIP on FeedbackDateKey]                 │
│  Disclosure: "Synthetic Simulation — Not Actual Airline Performance"        │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Visual count:** 10 KPI cards + 6 charts + 7 slicers = 23 elements  
**Layout:** 1280 × 720 (consistent with existing pages)

---

## Visual Specifications

### KPI Cards

| ID | Visual | Measure | DAX | Title | Format | Expected Value |
|----|--------|---------|-----|-------|--------|----------------|
| V01 | Card | CF01 | `COUNTROWS(fact_customer_feedback)` | Total Feedback Events | Integer | 2,500 |
| V02 | Card | CF02 | `AVERAGE(fact_customer_feedback[SatisfactionScore])` | Average Satisfaction Score | 2 decimal places | 2.99 |
| V03 | Card | CF03 | Complaint % (FeedbackType="Complaint") | Complaint Rate | Percentage | 25.52% |
| V04 | Card | CF04 | `COUNTROWS(FILTER(dim_customer, IsActive=TRUE))` | Active Customers | Integer | 4,808 |
| V05 | Card | CF09 | `DIVIDE(CF06, CF01)` | Positive Feedback Rate | Percentage | Computed |
| V06 | Card | CF10 | `DIVIDE(CF05 + CF07, CF01)` | Negative Feedback Rate | Percentage | Computed |
| V07 | Card | CF11 | Service recovery rate | Service Recovery Rate | Percentage | Computed |
| V08 | Card | CF12 | Resolution rate | Resolution Rate | Percentage | Computed |
| V09 | Card | CF13 | `CALCULATE(CF02, FeedbackType="Complaint")` | Complaint Satisfaction Avg | 2 decimal places | Computed |
| V10 | Card | CF14 | `CALCULATE(CF02, FeedbackType="Compliment")` | Compliment Satisfaction Avg | 2 decimal places | Computed |

### Charts

| ID | Visual Type | Title | Category/Axis | Values | Legend | Tooltip | Expected Insight |
|----|-------------|-------|---------------|--------|--------|---------|------------------|
| V11 | Bar Chart | Feedback by Channel | FeedbackChannel | CF01 | None | Feedback count + % of total | Which channels customers prefer |
| V12 | Bar Chart | Feedback by Type | FeedbackType | CF01 | None | Feedback count + % of total | Survey vs complaint vs claim vs compliment mix |
| V13 | Bar Chart | Avg Satisfaction by Airline | AirlineName | CF02 | None | Avg score + feedback count | Which airlines have highest/lowest satisfaction |
| V14 | Bar Chart | Feedback by Resolution Status | ResolutionStatus | CF01 | None | Count + % resolved | Case resolution workload |
| V15 | Bar Chart | Complaint Category Breakdown | ComplaintCategory | CF05 (filtered to Complaint) | None | Complaint count | Top complaint drivers |
| V16 | Donut Chart | Customer Segment Distribution | CustomerSegment | COUNTROWS(dim_customer) | None | Customer count + % of total | Customer base composition |

### Slicers

| ID | Table | Column | Type | Default | Notes |
|----|-------|--------|------|---------|-------|
| S01 | dim_airline | AirlineName | Multi-select | All | Filters all feedback visuals via AirlineKey |
| S02 | dim_customer | CustomerSegment | Multi-select | All | Filters via CustomerKey; proxy for customer type |
| S03 | dim_customer | LoyaltyTier | Multi-select | All | Filters via CustomerKey |
| S04 | fact_customer_feedback | FeedbackType | Multi-select | All | Direct column filter |
| S05 | fact_customer_feedback | FeedbackChannel | Multi-select | All | Direct column filter |
| S06 | fact_customer_feedback | ResolutionStatus | Multi-select | All | Direct column filter |
| S07 | dim_date | FullDate | Date range | All | **Requires USERELATIONSHIP** on FeedbackDateKey; inactive by default |

### Interactions

- All slicers cross-filter all KPI cards and charts
- Date slicer (S07) only works on visuals where measures use `USERELATIONSHIP(dim_date[DateKey], fact_customer_feedback[FeedbackDateKey])`
- Charts support cross-highlighting (selecting a bar filters other visuals)
- No drill-through configured (not required for this page)

### Formatting Standards

| Element | Standard |
|---------|----------|
| Page size | 1280 × 720 |
| Font | Consistent with AEROVISION 360 theme (theme.json) |
| KPI card values | Integer for counts; 2 decimal places for scores; percentage with 2 decimals for rates |
| No auto-abbreviation | Cards must show "2,500" not "3K" |
| Colors | Consistent with theme.json; no custom color overrides |
| Disclosure | "Synthetic Simulation — Not Actual Airline Performance" on page |
| Titles | All visuals must have explicit titles (none currently set in report.json) |

---

## DAX Measure Dependencies

All measures already exist in `dax/AEROVISION360_Measures.dax`. No new measures required for the blueprint.

| Measure | Used In Visuals | Verified? |
|---------|----------------|-----------|
| CF01 | V01, V11, V12, V14 | Yes (2,500) |
| CF02 | V02, V13, V09, V14 | Yes (2.99) |
| CF03 | V03 | Yes (25.52%) |
| CF04 | V04 | Yes (4,808) |
| CF05 | V15 | Yes |
| CF06 | V05, V10 | Yes |
| CF07 | V06 | Yes |
| CF09 | V05 | Yes |
| CF10 | V06 | Yes |
| CF11 | V07 | Yes |
| CF12 | V08 | Yes |
| CF13 | V09 | Yes |
| CF14 | V10 | Yes |

**No new DAX measures required.** All 10 CF measures used are verified and reconciled.

---

## Relationship Dependencies

| Visual | Required Relationship | Status | Notes |
|--------|----------------------|--------|-------|
| All CF-based visuals | fact_customer_feedback → dim_customer (CustomerKey) | Active | 0 orphans |
| All CF-based visuals | fact_customer_feedback → dim_airline (AirlineKey) | Active | 0 orphans |
| All CF-based visuals | fact_customer_feedback → dim_route (RouteKey) | Active | 0 orphans |
| Date slicer (S07) | fact_customer_feedback → dim_date (FeedbackDateKey) | INACTIVE | Requires USERELATIONSHIP in measure |
| Customer Segment slicer | fact_customer_feedback → dim_customer (CustomerKey) | Active | Works |
| Loyalty Tier slicer | fact_customer_feedback → dim_customer (CustomerKey) | Active | Works |

---

## Excluded from Blueprint (Unsupported)

| Excluded Element | Reason |
|-----------------|--------|
| Male/Female Passengers KPIs | No gender field exists |
| Travel Type slicer/charts | No TravelType field exists |
| Six service ratings | Only one SatisfactionScore column exists |
| Satisfied/Dissatisfied passenger counts | No OD-11 threshold; satisfaction not at passenger grain |
| Satisfaction by Class | dim_fare_class unused (no FK to facts) |
| Passengers by Class donut | dim_fare_class unused; "Economy Plus" absent |
| Behaviour decomposition tree | Gender & Travel Type absent; fact-to-fact not allowed |
| Total Passengers KPI | OD-04 blocked; grain ambiguity |

---

## Implementation Sequence (Phase 7)

| Order | Visual | Measure | Status |
|-------|--------|---------|--------|
| 1 | Total Feedback Events (card) | CF01 | **PASS** (completed) |
| 2 | Average Satisfaction Score (card) | CF02 | Pending |
| 3 | Complaint Rate (card) | CF03 | Pending |
| 4 | Active Customers (card) | CF04 | Pending |
| 5 | Positive Feedback Rate (card) | CF09 | Pending |
| 6 | Negative Feedback Rate (card) | CF10 | Pending |
| 7 | Service Recovery Rate (card) | CF11 | Pending |
| 8 | Resolution Rate (card) | CF12 | Pending |
| 9 | Complaint Satisfaction Avg (card) | CF13 | Pending |
| 10 | Compliment Satisfaction Avg (card) | CF14 | Pending |
| 11 | Feedback by Channel (bar chart) | CF01 | Pending |
| 12 | Feedback by Type (bar chart) | CF01 | Pending |
| 13 | Avg Satisfaction by Airline (bar chart) | CF02 | Pending |
| 14 | Feedback by Resolution Status (bar chart) | CF01 | Pending |
| 15 | Complaint Category Breakdown (bar chart) | CF05 | Pending |
| 16 | Customer Segment Distribution (donut) | COUNTROWS(dim_customer) | Pending |
| 17 | Slicers (7) | Various | Pending |

**Each visual must be validated against source before proceeding to the next.**
