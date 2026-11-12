# AEROVISION 360 — Page 05 Data Feasibility Matrix

**Statuses:** FULLY SUPPORTED | PARTIALLY SUPPORTED | UNSUPPORTED | GOVERNANCE BLOCKED | REQUIRES FURTHER INVESTIGATION  
**Analysis Date:** 2026-11-08  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## Complete Feasibility Matrix

| Component | Business Question | Required Data | Actual Availability | Data Grain | DAX | Relationships | Governance | Validation | Status | Recommendation |
|-----------|------------------|---------------|---------------------|------------|-----|---------------|------------|------------|--------|----------------|
| Total Passengers | How many total passengers? | fact_booking_transactions[PassengerCount] or fact_flight_operations[RevenuePassengers] | SUM(PassengerCount)=9,956 (coupons); RV_RevenuePassengers=8,922 (OD-04 blocked); FL02=218,413 (flight-level) | Coupon = 1 passenger; flight leg = N passengers | RV_RevenuePassengers = CALCULATE(SUM(PassengerCount), IsRevenuePassenger=TRUE) | fact_booking_transactions → dim_date (TravelDateKey active) | OD-04 BLOCKED | Reconciled: SUM=9,956, SUM(IsRev=TRUE)=8,922 | PARTIALLY SUPPORTED | Defer until OD-04 resolved; use CF01 as volume proxy |
| Male Passengers | How many male passengers? | dim_customer[Gender] | **DOES NOT EXIST** | N/A | N/A | N/A | N/A | N/A | UNSUPPORTED | Reject — do not build; no gender field |
| Female Passengers | How many female passengers? | dim_customer[Gender] | **DOES NOT EXIST** | N/A | N/A | N/A | N/A | N/A | UNSUPPORTED | Reject — do not build; no gender field |
| Satisfied Passengers | How many satisfied passengers? | fact_customer_feedback[SatisfactionScore] with threshold | SatisfactionScore (1–5), 603 NULLs; no approved threshold (OD-11 pending) | Feedback event (2,500 events), not passenger | CF02 = AVERAGE(SatisfactionScore); no count measure exists | fact_customer_feedback → dim_date (INACTIVE) | OD-11 threshold pending | CF02 = 2.99 reconciled | PARTIALLY SUPPORTED | Use CF02 avg score; do not build count without OD-11 |
| Neutral/Dissatisfied Passengers | How many neutral/dissatisfied passengers? | fact_customer_feedback[SatisfactionScore] with threshold | Same as above | Same as above | No measure exists | Same as above | OD-11 pending | Same as above | PARTIALLY SUPPORTED | Use CF03 complaint rate as proxy; do not build count |
| Satisfaction by Class & Type | Satisfaction by class × travel type | SatisfactionScore × CabinClass × TravelType | SatisfactionScore exists; dim_fare_class unused (no FK); TravelType absent | Feedback event | None possible | No common grain between satisfaction and class | N/A | N/A | PARTIALLY SUPPORTED | Use Satisfaction by Airline (existing) or FeedbackType breakdown |
| Passengers by Travel Type & Class | Passengers by travel type × class | PassengerCount × TravelType × CabinClass | TravelType absent; dim_fare_class unused; booking fact blocked | Coupon | None possible | dim_fare_class no FK to facts | OD-04 blocked | N/A | UNSUPPORTED | Reject — no TravelType; class dim unused |
| Service Ratings (six categories) | Six service-quality ratings | Six rating columns | Only one SatisfactionScore + ComplaintCategory | Feedback event | CF02 for overall | N/A | N/A | CF02 = 2.99 reconciled | UNSUPPORTED | Use overall SatisfactionScore + ComplaintCategory top-8 |
| Passengers by Class (donut) | Passenger distribution by class | PassengerCount × CabinClass | CabinClass exists (4 values) but dim_fare_class unused (no FK) | Coupon | None possible | dim_fare_class no FK to any fact | N/A | N/A | PARTIALLY SUPPORTED | Defer until dim_fare_class FK added; replace "Economy Plus" with Premium Economy |
| Behaviour Analysis (decomposition) | Total → Gender → Customer Type → Travel Type → Satisfaction | Gender, CustomerSegment, TravelType, SatisfactionScore | Gender absent; TravelType absent; CustomerSegment exists; Satisfaction at feedback grain | Mixed grains | None possible | Fact-to-fact join not allowed | N/A | N/A | UNSUPPORTED | Alternative: CF01 → FeedbackType → ComplaintCategory → ResolutionStatus |

---

## Slicer Feasibility

| Slicer | Table | Column | Active Relationship? | Status | Notes |
|--------|-------|--------|---------------------|--------|-------|
| Airline | dim_airline | AirlineName | Yes (via fact keys) | FULLY SUPPORTED | 10 airlines |
| Customer Segment | dim_customer | CustomerSegment | Yes (via fact_customer_feedback.CustomerKey) | FULLY SUPPORTED | Business/Corporate/Group/Leisure — proxy for customer type |
| Loyalty Tier | dim_customer | LoyaltyTier | Yes | FULLY SUPPORTED | Silver/Gold/Platinum/None |
| Home Country | dim_customer | HomeCountry / HomeCountryCode | Yes | FULLY SUPPORTED | 8 countries |
| Feedback Type | fact_customer_feedback | FeedbackType | Direct column | FULLY SUPPORTED | Survey/Complaint/Compliment/Claim |
| Feedback Channel | fact_customer_feedback | FeedbackChannel | Direct column | FULLY SUPPORTED | Email/Call Center/Social/Web/Mobile/Airport |
| Resolution Status | fact_customer_feedback | ResolutionStatus | Direct column | FULLY SUPPORTED | Open/In Progress/Resolved/Closed-No Action |
| Cabin Class | dim_fare_class | CabinClass | NO — dim_fare_class unused (no FK) | UNSUPPORTED | Cannot slice any fact |
| Travel Type | — | — | Field does not exist | UNSUPPORTED | No TravelType column anywhere |
| Gender | — | — | Field does not exist | UNSUPPORTED | No Gender column anywhere |
| Date Range | dim_date | FullDate | INACTIVE for fact_customer_feedback | REQUIRES USERELATIONSHIP | FeedbackDateKey & ResolutionDateKey both inactive |

---

## Governance Blockers Summary

| Governance Item | Status | Impact on Page 05 |
|----------------|--------|-------------------|
| OD-04 (FactBookingTransactions blocked) | Unresolved | RV_* passenger/revenue measures cannot be used |
| OD-11 (Satisfaction scale threshold) | Owner approval pending | No "satisfied/dissatisfied" count possible |
| Fact-to-fact joins | Not allowed | Cannot join bookings + feedback at passenger level |
| dim_fare_class unused | No FK to facts | Class dimension cannot slice facts |
| Feedback date relationships | Inactive | Date slicer needs USERELATIONSHIP |
