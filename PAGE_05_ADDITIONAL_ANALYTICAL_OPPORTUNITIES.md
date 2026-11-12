# AEROVISION 360 — Page 05 Additional Analytical Opportunities

**Analysis Date:** 2026-11-08  
**Principle:** Do not restrict the dashboard to the reference. Investigate all legitimate business questions answerable with available, approved data.  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## Methodology

Each opportunity was evaluated against:
- Available tables and columns (verified from manifests and direct data profiling)
- Existing DAX measures (verified from dax/AEROVISION360_Measures.dax)
- Relationships (verified from semantic_model.json and RELATIONSHIP_VALIDATION.csv)
- Governance restrictions (OD-04 blocked, OD-11 pending, fact-to-fact not allowed)
- Data grain (distinguished feedback events from passengers, bookings, coupons, customers)

---

## Opportunity 1 — Feedback Volume by Channel

| Field | Value |
|-------|-------|
| Business value | Shows how customers choose to provide feedback; identifies channel dominance for service operations |
| Supporting fields | fact_customer_feedback[FeedbackChannel] (Email, Call Center, Social, Web, Mobile, Airport) |
| Data grain | One row = one feedback event |
| Proposed metric | CF01 = COUNTROWS(fact_customer_feedback) |
| Appropriate visual | Bar chart (category: FeedbackChannel, values: CF01) |
| DAX requirements | None — CF01 already exists and is verified |
| Governance constraints | None — CF measures are approved |
| Validation method | CF01 = 2,500 reconciled against source CSV |
| Existing visual? | Yes — Page 05 already has CF01 by FeedbackChannel (report.json visual #10) |

## Opportunity 2 — Feedback Volume by Type

| Field | Value |
|-------|-------|
| Business value | Shows the mix of Surveys, Complaints, Claims, and Compliments; indicates overall sentiment direction |
| Supporting fields | fact_customer_feedback[FeedbackType] (Survey, Complaint, Claim, Compliment) |
| Data grain | One row = one feedback event |
| Proposed metric | CF01 = COUNTROWS(fact_customer_feedback) |
| Appropriate visual | Bar chart (category: FeedbackType, values: CF01) |
| DAX requirements | None — CF01 already exists |
| Governance constraints | None |
| Validation method | CF01 = 2,500; FeedbackType distribution: Survey(641), Complaint(638), Claim(618), Compliment(603) |
| Existing visual? | Yes — Page 05 already has CF01 by FeedbackType (report.json visual #12) |

## Opportunity 3 — Average Satisfaction by Airline

| Field | Value |
|-------|-------|
| Business value | Compares customer satisfaction performance across the 10 airlines |
| Supporting fields | fact_customer_feedback[SatisfactionScore] × dim_airline[AirlineName] |
| Data grain | One row = one feedback event; linked via AirlineKey |
| Proposed metric | CF02 = AVERAGE(fact_customer_feedback[SatisfactionScore]) |
| Appropriate visual | Bar chart (category: AirlineName, values: CF02) |
| DAX requirements | None — CF02 already exists and is verified |
| Governance constraints | None |
| Validation method | CF02 = 2.99 reconciled (mean of 1,897 non-null scores out of 2,500) |
| Existing visual? | Yes — Page 05 already has CF02 by AirlineName (report.json visual #11) |

## Opportunity 4 — Feedback Volume by Resolution Status

| Field | Value |
|-------|-------|
| Business value | Shows how feedback cases are being resolved; identifies backlog or unresolved issues |
| Supporting fields | fact_customer_feedback[ResolutionStatus] (Open, In Progress, Resolved, Closed - No Action) |
| Data grain | One row = one feedback event |
| Proposed metric | CF01 = COUNTROWS(fact_customer_feedback) |
| Appropriate visual | Bar chart (category: ResolutionStatus, values: CF01) |
| DAX requirements | None — CF01 already exists |
| Governance constraints | None |
| Validation method | CF01 = 2,500; ResolutionStatus: Open(639), Closed-No Action(631), In Progress(626), Resolved(604) |
| Existing visual? | Yes — Page 05 already has CF01 by ResolutionStatus (report.json visual #13) |

## Opportunity 5 — Positive vs Negative Feedback Rate

| Field | Value |
|-------|-------|
| Business value | Quantifies the balance of positive (Compliment) vs negative (Complaint + Claim) feedback |
| Supporting fields | fact_customer_feedback[FeedbackType] |
| Data grain | One row = one feedback event |
| Proposed metric | CF09 = DIVIDE(CF06, CF01) (positive rate); CF10 = DIVIDE(CF05 + CF07, CF01) (negative rate) |
| Appropriate visual | Bar chart or card pair |
| DAX requirements | None — CF09 and CF10 already exist |
| Governance constraints | None |
| Validation method | CF09 and CF10 are computed from verified CF01, CF05, CF06, CF07 |
| Existing visual? | No — not in current Page 05 visuals |

## Opportunity 6 — Service Recovery Rate

| Field | Value |
|-------|-------|
| Business value | Shows percentage of complaints that received service recovery; indicates complaint handling effectiveness |
| Supporting fields | fact_customer_feedback[ServiceRecoveryFlag] × fact_customer_feedback[FeedbackType]="Complaint" |
| Data grain | One row = one feedback event |
| Proposed metric | CF11 = DIVIDE(COUNTROWS(ServiceRecoveryFlag=TRUE), COUNTROWS(FeedbackType="Complaint")) |
| Appropriate visual | KPI card |
| DAX requirements | None — CF11 already exists |
| Governance constraints | None |
| Validation method | CF11 computed from verified counts; ServiceRecoveryFlag True=381, Complaints=638 |
| Existing visual? | Yes — Page 05 already has CF11 card (visual #7) |

## Opportunity 7 — Resolution Rate

| Field | Value |
|-------|-------|
| Business value | Shows percentage of feedback cases marked as Resolved; indicates case closure effectiveness |
| Supporting fields | fact_customer_feedback[ResolutionStatus] |
| Data grain | One row = one feedback event |
| Proposed metric | CF12 = DIVIDE(COUNTROWS(ResolutionStatus="Resolved"), COUNTROWS(NOT ISBLANK(ResolutionStatus))) |
| Appropriate visual | KPI card |
| DAX requirements | None — CF12 already exists |
| Governance constraints | None |
| Validation method | CF12 computed from verified counts; Resolved=604, non-blank ResolutionStatus=2,500 |
| Existing visual? | Yes — Page 05 already has CF12 card (visual #8) |

## Opportunity 8 — Complaint Satisfaction vs Compliment Satisfaction

| Field | Value |
|-------|-------|
| Business value | Compares average satisfaction of complaints vs compliments; highlights satisfaction gap |
| Supporting fields | fact_customer_feedback[SatisfactionScore] × fact_customer_feedback[FeedbackType] |
| Data grain | One row = one feedback event |
| Proposed metric | CF13 = CALCULATE(CF02, FeedbackType="Complaint"); CF14 = CALCULATE(CF02, FeedbackType="Compliment") |
| Appropriate visual | Bar chart or card pair |
| DAX requirements | None — CF13 and CF14 already exist |
| Governance constraints | None |
| Validation method | CF13/CF14 computed from verified CF02 with FeedbackType filters |
| Existing visual? | No — not in current Page 05 visuals |

## Opportunity 9 — Active Customers

| Field | Value |
|-------|-------|
| Business value | Shows the size of the active customer base; indicator of customer retention health |
| Supporting fields | dim_customer[IsActive] |
| Data grain | One row = one customer |
| Proposed metric | CF04 = COUNTROWS(FILTER(dim_customer, IsActive=TRUE)) |
| Appropriate visual | KPI card |
| DAX requirements | None — CF04 already exists |
| Governance constraints | None |
| Validation method | CF04 = 4,808 (4808 active, 192 inactive out of 5,000) |
| Existing visual? | Yes — Page 05 already has CF04 card (visual #4) |

## Opportunity 10 — Customer Segment Distribution

| Field | Value |
|-------|-------|
| Business value | Shows customer base composition by segment (Leisure, Business, Corporate, Group); supports segmentation strategy |
| Supporting fields | dim_customer[CustomerSegment] |
| Data grain | One row = one customer |
| Proposed metric | COUNTROWS(dim_customer) |
| Appropriate visual | Donut or bar chart |
| DAX requirements | New measure: `COUNTROWS(dim_customer)` or reuse CF04 pattern |
| Governance constraints | None |
| Validation method | Segment distribution: Leisure(3,107), Business(1,118), Corporate(496), Group(279) |
| Existing visual? | No — not in current Page 05 visuals |

## Opportunity 11 — Loyalty Tier Distribution

| Field | Value |
|-------|-------|
| Business value | Shows loyalty program penetration; supports CRM and retention analysis |
| Supporting fields | dim_customer[LoyaltyTier] |
| Data grain | One row = one customer |
| Proposed metric | COUNTROWS(dim_customer) |
| Appropriate visual | Donut or bar chart |
| DAX requirements | New measure |
| Governance constraints | None |
| Validation method | Tier distribution: Silver(1,980), Gold(1,514), Platinum(820), None(686) |
| Existing visual? | No — not in current Page 05 visuals |

## Opportunity 12 — Complaint Category Breakdown (complaints only)

| Field | Value |
|-------|-------|
| Business value | Identifies the most common complaint types; guides service improvement priorities |
| Supporting fields | fact_customer_feedback[ComplaintCategory] (populated only for complaints) |
| Data grain | One row = one complaint feedback event |
| Proposed metric | CF05 (complaint count) filtered by ComplaintCategory |
| Appropriate visual | Bar chart (category: ComplaintCategory, values: CF05) |
| DAX requirements | None — CF01/CF05 already exist; filter by FeedbackType="Complaint" |
| Governance constraints | None |
| Validation method | ComplaintCategory null for non-complaints (1,862 nulls); populated for 638 complaints: Other(89), Delay(85), Seat(82), Customer Service(81), Baggage(79), In-Flight Experience(75), Cancellation(75), Boarding(72) |
| Existing visual? | No — not in current Page 05 visuals |

## Opportunities NOT Recommended

| Opportunity | Reason Not Recommended |
|-------------|------------------------|
| Passenger count by class | dim_fare_class unused (no FK); OD-04 blocked |
| Satisfaction by class | No common grain between satisfaction and class; fact-to-fact not allowed |
| Travel Type analysis | TravelType field does not exist |
| Gender analysis | Gender field does not exist |
| Six service ratings | Only one SatisfactionScore column exists |
| Satisfied/Dissatisfied passenger counts | No approved threshold (OD-11); satisfaction not at passenger grain |
| Behaviour decomposition (Gender → Type → Travel → Satisfaction) | Gender and Travel Type absent; fact-to-fact not allowed |

---

## Recommended Additional Visuals (beyond reference)

These are legitimate, data-supported opportunities not in the reference but valuable for customer intelligence:

| ID | Visual | Metric | Justification |
|----|--------|--------|---------------|
| V14 | Positive vs Negative Feedback Rate | CF09, CF10 | Sentiment balance not covered by reference |
| V15 | Complaint Satisfaction vs Compliment Satisfaction | CF13, CF14 | Satisfaction gap analysis |
| V16 | Customer Segment Distribution | COUNTROWS(dim_customer) | Customer base composition |
| V17 | Loyalty Tier Distribution | COUNTROWS(dim_customer) | Loyalty program health |
| V18 | Complaint Category Breakdown | CF05 by ComplaintCategory | Service improvement priorities |
