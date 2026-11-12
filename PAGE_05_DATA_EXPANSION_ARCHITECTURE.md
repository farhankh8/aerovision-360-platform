# AEROVISION 360 — Page 05 Data Expansion Architecture

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Architecture Date:** 2026-11-08  
**Status:** ARCHITECTURE DESIGN COMPLETE — READ-ONLY DESIGN, NO IMPLEMENTATION  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Architecture Objective

Define how genuine additional datasets could be incorporated into AEROVISION 360 to support Page 05 reference dashboard components that are currently unsupported (Gender, Travel Type, six service ratings, Economy Plus, Satisfied/Dissatisfied counts, passenger behaviour decomposition).

**Core constraint:** Zero fabrication. No merging unrelated passenger records with AEROVISION customers. External data must remain identifiable as a separate source.

---

## 2. Current Architecture State

### 2.1 Existing Model (Validated)

| Layer | Tables | Relationships | Page 05 Usable Tables |
|-------|--------|---------------|----------------------|
| CURATED | 16 tables (11 dims, 5 facts) | Star schema; fact-to-fact prohibited | FactCustomerFeedback, DimCustomer, DimAirline, DimDate, DimRoute, DimFareClass (unused) |
| SEMANTIC MODEL | Same 16 tables | Active/inactive relationships defined | Same |
| POWER BI | Report with 5 pages | Page 05 has 13 CF-based visuals | Page 05 existing |

### 2.2 Architecture Constraints

| Constraint | Source | Impact on Expansion |
|------------|--------|---------------------|
| No fact-to-fact relationships | Data Contracts Section 5.1 | Cannot join FactBookingTransactions with FactCustomerFeedback |
| OD-04 blocked facts | Governance | FactBookingTransactions and FactOperatingCosts blocked |
| OD-11 pending | Governance | Satisfaction scale threshold undefined |
| All data synthetic | C-08 | No real passenger personal information |
| No Gender column | Verified across all 16 datasets | Cannot infer from names/IDs |
| No TravelType column | Verified across all 16 datasets | Cannot fabricate travel type |
| dim_fareClass unused | Relationship validation | No FK to any fact |

---

## 3. Expansion Architecture Options

### Option A — Native Data Only (RECOMMENDED)

Build Page 05 using only existing AEROVISION 360 data.

| Component | Architecture | Data Source | Measures | Visuals |
|-----------|-------------|-------------|----------|---------|
| Total Feedback Events | Existing fact | FactCustomerFeedback | CF01 | Card |
| Average Satisfaction Score | Existing fact | FactCustomerFeedback | CF02 | Card |
| Complaint Rate | Existing fact | FactCustomerFeedback | CF03 | Card |
| Active Customers | Existing dim | DimCustomer | CF04 | Card |
| Feedback by Channel | Existing fact | FactCustomerFeedback | CF01 | Bar chart |
| Feedback by Type | Existing fact | FactCustomerFeedback | CF01 | Bar chart |
| Avg Satisfaction by Airline | Existing fact + dim | FactCustomerFeedback + DimAirline | CF02 | Bar chart |
| Feedback by Resolution | Existing fact | FactCustomerFeedback | CF01 | Bar chart |
| Positive/Negative Feedback Rate | Existing fact | FactCustomerFeedback | CF09, CF10 | Cards |
| Service Recovery Rate | Existing fact | FactCustomerFeedback | CF11 | Card |
| Resolution Rate | Existing fact | FactCustomerFeedback | CF12 | Card |
| Complaint vs Compliment Satisfaction | Existing fact | FactCustomerFeedback | CF13, CF14 | Cards |
| Customer Segment Distribution | Existing dim | DimCustomer | COUNTROWS | Donut |
| Loyalty Tier Distribution | Existing dim | DimCustomer | COUNTROWS | Donut |
| Complaint Category Breakdown | Existing fact | FactCustomerFeedback | CF05 | Bar chart |
| Slicers | Existing dims/facts | DimCustomer, FactCustomerFeedback | N/A | 7 slicers |

**Unsupported reference components:** Gender, Travel Type, six service ratings, Satisfied/Dissatisfied counts, class-based visuals, behaviour decomposition.

**Pros:** Zero fabrication, governance-compliant, fully verifiable, no new data acquisition needed
**Cons:** Does not match full reference dashboard structure

---

### Option B — Native Data + External Survey as Separate Subject Area

Add the Maven/Kaggle Airline Passenger Satisfaction dataset as a completely separate, clearly-labeled subject area within the same Power BI report but with NO relationships to AEROVISION facts.

| Component | Architecture | Data Source | Relationship to AEROVISION? |
|-----------|-------------|-------------|----------------------------|
| Gender KPIs | Separate fact table | Maven/Kaggle dataset | NONE — separate population |
| Travel Type slicer | Separate dimension | Maven/Kaggle dataset | NONE — separate population |
| Six service ratings | Separate fact table | Maven/Kaggle dataset | NONE — separate population |
| Class distribution | Separate fact table | Maven/Kaggle dataset | NONE — separate population |

**Implementation:**
- Create separate fact table `FactExternalPassengerSurvey` in CURATED layer
- No relationships to any AEROVISION fact or dimension
- Visuals clearly labeled "External Passenger Survey — Not AEROVISION Data"
- Separate disclosure text

**Pros:** Provides all missing reference fields
**Cons:** License unverified, access blocked, population mismatch, adds complexity, requires separate model space, two different disclosure standards on one page

**Verdict:** NOT RECOMMENDED — violates principle of analytical coherence; mixing synthetic and real survey data on one dashboard creates confusion about which numbers are AEROVISION's

---

### Option C — Separate Analytical Model

Build Page 05 using AEROVISION 360 native data in the main model, and create a completely separate Power BI file (or report) for the external survey data.

| Component | Architecture | Location | Model |
|-----------|-------------|----------|-------|
| AEROVISION customer intelligence | Native CF measures | Main Power BI report | AEROVISION 360 semantic model |
| External survey data | Maven/Kaggle dataset | Separate Power BI report | Separate semantic model |

**Pros:** Clean separation, no mixing of populations, each model self-consistent
**Cons:** Two reports to maintain, users must switch between reports, external data license still unverified

**Verdict:** VIABLE if external data is needed, but adds operational complexity

---

## 4. Recommended Architecture: Option A (Native Data Only)

### 4.1 Design Rationale

1. **Zero fabrication** — No invented columns, measures, or values
2. **Governance compliant** — OD-04 and OD-11 respected; no blocked measures used
3. **Fully verifiable** — Every number reconciles to source CSV/Parquet
4. **Analytically coherent** — Single population, single grain, single disclosure
5. **Professional** — Dashboard answers genuine business questions with available data

### 4.2 Architecture Diagram (Native Only)

```
┌─────────────────────────────────────────────────────────────────┐
│                    AEROVISION 360 Semantic Model                │
│                                                                 │
│  DIMENSIONS                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ DimDate  │  │DimAirline│  │DimRoute  │  │DimCustomer│       │
│  │ (761)    │  │  (10)    │  │  (320)   │  │  (5,000)  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │              │              │              │             │
│  ┌────┴─────┐  ┌─────┴─────┐  ┌────┴─────┐  ┌────┴─────┐        │
│  │FactCustomerFeedback│              │              │            │
│  │   (2,500)          │              │              │            │
│  └────────────────────┘              │              │            │
│         CF01-CF14 measures          │              │            │
│                                     │              │            │
│  Page 05 Visuals:                   │              │            │
│  • 10 KPI cards                     │              │            │
│  • 6 charts                         │              │            │
│  • 7 slicers                        │              │            │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Data Flow (No Changes to Existing)

```
Source: data/03_curated/fact_customer_feedback.parquet
       → Power BI imports CURATED table
       → Semantic model relationships (active/inactive)
       → DAX measures CF01-CF14
       → Power BI visuals on Page 05
       → Disclosure: "Synthetic Simulation — Not Actual Airline Performance"
```

**No new datasets, no new Power Query, no new relationships, no new DAX measures required.**

---

## 5. Alternative Architecture: External Data as Separate Subject Area (If Required)

If the business requires the full reference dashboard including Gender, Travel Type, and six service ratings, the following architecture would be needed:

### 5.1 External Survey Data Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              External Passenger Survey (Separate Subject Area)  │
│                                                                 │
│  FactExternalPassengerSurvey (~130,000 rows)                    │
│  • Gender, Customer Type, Type of Travel, Class                 │
│  • 12 service rating columns (0-5 scale)                        │
│  • Satisfaction (categorical)                                   │
│  • id (survey response identifier)                              │
│                                                                 │
│  NO RELATIONSHIPS to any AEROVISION fact or dimension           │
│  NO shared keys                                                 │
│  Separate disclosure: "External Survey Data — Not AEROVISION"   │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Prerequisites Before External Data Can Be Added

| Prerequisite | Status | Action Required |
|--------------|--------|-----------------|
| License verification | UNRESOLVED | Clarify Maven "Public Domain" vs Kaggle "Other" |
| Download access | BLOCKED | Both platforms require login |
| Record count verification | UNRESOLVED | 499 vs 120,000+ discrepancy |
| Population segregation | DESIGN REQUIRED | Separate model space with no relationships |
| Governance approval | PENDING | Owner decision on external data use |
| Disclosure standard | DESIGN REQUIRED | Dual disclosure on same page |

---

## 6. Relationship Design Rules (For Any Future Expansion)

If any future expansion adds new tables to the semantic model, the following rules must be followed:

| Rule | Source | Rationale |
|------|--------|-----------|
| No fact-to-fact relationships | Data Contracts Section 5.1 | Prevents double-counting and ambiguous filter paths |
| Shared dimensions only | Data Contracts Section 5.1 | Cross-fact analysis through conformed dimensions |
| One active relationship per fact-date pair | Model design | Prevents ambiguous date filtering |
| Role-playing dates must be inactive | Model design | Only one active date relationship per fact |
| No inferred gender/travel type | Project rules | Zero fabrication principle |
| External data must be segregated | Project rules | Prevents mixing populations |
| Disclosure on every visual | Dashboard spec | T-79 requirement |

---

## 7. DAX Measure Design Rules (For Any Future Measures)

| Rule | Source | Rationale |
|------|--------|-----------|
| Reuse existing CF measures where possible | Project rules | No unnecessary duplication |
| No new measures for unsupported fields | Project rules | Zero fabrication |
| DIVIDE with BLANK() for ratios | DAX Catalogue | Zero denominator handling |
| Date role explicitly stated | DAX Catalogue | Prevents ambiguous filtering |
| USERELATIONSHIP for inactive dates | Dashboard spec | Feedback date relationships inactive |
| No satisfaction thresholds without OD-11 | Governance | Owner approval pending |

---

## 8. Visual Architecture (Native Data Only)

### 8.1 KPI Section (10 Cards)

| Position | Visual | Measure | Data Source |
|----------|--------|---------|-------------|
| Row 1, Card 1 | Total Feedback Events | CF01 | FactCustomerFeedback |
| Row 1, Card 2 | Average Satisfaction Score | CF02 | FactCustomerFeedback |
| Row 1, Card 3 | Complaint Rate | CF03 | FactCustomerFeedback |
| Row 1, Card 4 | Active Customers | CF04 | DimCustomer |
| Row 1, Card 5 | Positive Feedback Rate | CF09 | FactCustomerFeedback |
| Row 2, Card 1 | Negative Feedback Rate | CF10 | FactCustomerFeedback |
| Row 2, Card 2 | Service Recovery Rate | CF11 | FactCustomerFeedback |
| Row 2, Card 3 | Resolution Rate | CF12 | FactCustomerFeedback |
| Row 2, Card 4 | Complaint Satisfaction Avg | CF13 | FactCustomerFeedback |
| Row 2, Card 5 | Compliment Satisfaction Avg | CF14 | FactCustomerFeedback |

### 8.2 Chart Section (6 Charts)

| Position | Visual | Measure | Category | Data Source |
|----------|--------|---------|----------|-------------|
| Row 3, Left | Feedback by Channel | CF01 | FeedbackChannel | FactCustomerFeedback |
| Row 3, Right | Feedback by Type | CF01 | FeedbackType | FactCustomerFeedback |
| Row 4, Left | Avg Satisfaction by Airline | CF02 | AirlineName | FactCustomerFeedback + DimAirline |
| Row 4, Right | Feedback by Resolution Status | CF01 | ResolutionStatus | FactCustomerFeedback |
| Row 5, Left | Complaint Category Breakdown | CF05 | ComplaintCategory | FactCustomerFeedback (filtered to Complaint) |
| Row 5, Right | Customer Segment Distribution | COUNTROWS | CustomerSegment | DimCustomer |

### 8.3 Slicer Section (7 Slicers)

| Slicer | Table | Column | Type |
|--------|-------|--------|------|
| Airline | DimAirline | AirlineName | Multi-select |
| Customer Segment | DimCustomer | CustomerSegment | Multi-select |
| Loyalty Tier | DimCustomer | LoyaltyTier | Multi-select |
| Feedback Type | FactCustomerFeedback | FeedbackType | Multi-select |
| Feedback Channel | FactCustomerFeedback | FeedbackChannel | Multi-select |
| Resolution Status | FactCustomerFeedback | ResolutionStatus | Multi-select |
| Date Range | DimDate | FullDate | Date (requires USERELATIONSHIP) |

---

## 9. Unsupported Reference Components (Architecture Decision)

| Component | Decision | Reason |
|-----------|----------|--------|
| Male/Female Passengers KPIs | EXCLUDED | No Gender field exists; zero fabrication rule |
| Travel Type slicer/charts | EXCLUDED | No TravelType field exists |
| Six service ratings | EXCLUDED | Only SatisfactionScore exists |
| Satisfied/Dissatisfied counts | EXCLUDED | OD-11 threshold pending; not at passenger grain |
| Satisfaction by Class & Type | EXCLUDED | dim_fareClass unused; TravelType absent; fact-to-fact prohibited |
| Passengers by Travel Type & Class | EXCLUDED | TravelType absent; class unused |
| Passengers by Class donut | EXCLUDED | dim_fareClass unused; "Economy Plus" absent |
| Behaviour decomposition | EXCLUDED | Gender & TravelType absent; fact-to-fact prohibited |
| Gender slicer | EXCLUDED | No Gender field exists |

---

## 10. Implementation Readiness

| Item | Status | Notes |
|------|--------|-------|
| Native data available | YES | CF01-CF14 verified against source |
| Semantic model relationships | YES | Active relationships support all CF-based visuals |
| DAX measures | YES | All 14 CF measures defined and verified |
| Power BI report definition | YES | Page 05 already defined with 13 visuals in report.json |
| Visual 1 (CF01) | PASS | Validated at 2,500 |
| Visual 2 (CF02) | PASS | Validated at 2.99 |
| External data integration | NO | Not feasible (see Section 5.1) |
| Governance approval for OD-04 | PENDING | Would be needed for any booking-based passenger measure |
| Governance approval for OD-11 | PENDING | Would be needed for satisfied/dissatisfied counts |

---

## 11. Conclusion

**Recommended architecture: Option A — Native Data Only.** The AEROVISION 360 semantic model fully supports a customer intelligence dashboard using FactCustomerFeedback measures (CF01-CF14). The reference dashboard's unsupported components (Gender, Travel Type, six service ratings, Satisfied/Dissatisfied counts, class-based visuals, behaviour decomposition) cannot be built without new source data that cannot be responsibly integrated due to population mismatch, no common join key, license conflicts, and access restrictions.

Any future consideration of external data would require separate governance approval, license clarification, and a clearly segregated model space with no relationships to AEROVISION facts.
