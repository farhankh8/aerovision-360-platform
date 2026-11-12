# AEROVISION 360 — Page 05 Reference Dashboard Analysis

**Reference:** PowerBI | Project | Airline Passenger Satisfaction Review (Maven Analytics)  
**Reference URL:** https://images.openai.com/static-rsc-4/... (JPEG image — could not be fetched as text)  
**Reference Page:** novypro.com/project/airline-passenger-satisfaction-review (returns 404)  
**Analysis Date:** 2026-11-08  
**Status:** ANALYSIS BASED ON COMPONENT DESCRIPTIONS FROM USER PROMPTS (reference image not directly inspectable)

---

## 1. Reference Components Identified

From the user's prompt, the reference dashboard contains the following analytical areas:

| # | Reference Component | Reference Visual Type | Intended Business Question |
|---|---------------------|----------------------|---------------------------|
| 1 | Total Passengers | KPI Card | Total passenger volume |
| 2 | Male Passengers | KPI Card | Male passenger count |
| 3 | Female Passengers | KPI Card | Female passenger count |
| 4 | Satisfied Passengers | KPI Card | Count of satisfied passengers |
| 5 | Neutral or Dissatisfied Passengers | KPI Card | Count of neutral/dissatisfied passengers |
| 6 | Passenger Satisfaction by Class & Type | Clustered/stacked horizontal bar | Satisfaction distribution across class × travel type |
| 7 | Number of Passengers by Travel Type and Class | Clustered column | Passenger count by travel type × class |
| 8 | Passenger Service Ratings | Visual (unspecified) | Six service-quality category ratings |
| 9 | Total Passengers by Class | Donut chart | Passenger distribution by cabin class |
| 10 | Passenger Behaviour Analysis | Decomposition tree / Sankey | Total → Gender → Customer Type → Travel Type → Satisfaction |

### Reference filters/slicers described

| # | Slicer | Reference Values |
|---|--------|------------------|
| 1 | Passenger Class | Business, Economy, Economy Plus |
| 2 | Travel Type | Business, Personal |
| 3 | Satisfaction | Satisfied, Neutral or Dissatisfied |
| 4 | Gender | (if available) |
| 5 | Customer Type | (if available) |
| 6 | Airline Name | (if available) |
| 7 | Flight Date Range | (if available) |

### Reference behaviour flow
Total Passengers → Gender → Customer Type → Type of Travel → Satisfaction

---

## 2. Component-by-Component Analysis

### Component 1 — Total Passengers (KPI Card)

| Field | Reference Requirement | AEROVISION 360 Reality |
|-------|----------------------|----------------------|
| Business question | How many total passengers? | How many feedback events / revenue passengers? |
| Required data | fact_booking_transactions[PassengerCount] or fact_flight_operations[RevenuePassengers] | fact_booking_transactions (OD-04 blocked) or fact_flight_operations |
| Data grain | One record = one passenger | One coupon row = 1 passenger (booking); one flight leg = N revenue passengers (operations) |
| DAX | SUM(PassengerCount) or similar | RV_RevenuePassengers = 8,922 (OD-04 blocked); FL02 = 218,413 (flight-level, different population) |
| Relationships | fact_booking_transactions → dim_fare_class | dim_fare_class unused (no FK) |
| Status | PARTIALLY SUPPORTED | Measure exists but blocked by OD-04 |

**Finding:** "Total Passengers" cannot be cleanly computed. SUM(PassengerCount) = 9,956 = coupon count (always 1 per row). RV_RevenuePassengers = 8,922 but OD-04 blocked. FL02 = 218,413 is flight-level revenue passengers, a different population.

### Component 2 — Male Passengers (KPI Card)

| Field | Reference Requirement | AEROVISION 360 Reality |
|-------|----------------------|----------------------|
| Business question | How many male passengers? | Not applicable |
| Required data | dim_customer[Gender] or equivalent | **DOES NOT EXIST** anywhere in project |
| Status | UNSUPPORTED | No gender field; must not infer from names/IDs |

**Finding:** Gender field confirmed absent from dim_customer (8 columns: CustomerKey, CustomerID, CustomerSegment, LoyaltyTier, HomeCountry, HomeCountryCode, RegistrationDate, IsActive). Full-project grep returned zero matches for "Gender", "Male", "Female". **Must not be built.**

### Component 3 — Female Passengers (KPI Card)

| Field | Reference Requirement | AEROVISION 360 Reality |
|-------|----------------------|----------------------|
| Business question | How many female passengers? | Not applicable |
| Required data | dim_customer[Gender] or equivalent | **DOES NOT EXIST** |
| Status | UNSUPPORTED | No gender field |

**Finding:** Same as Component 2. **Must not be built.**

### Component 4 — Satisfied Passengers (KPI Card)

| Field | Reference Requirement | AEROVISION 360 Reality |
|-------|----------------------|----------------------|
| Business question | How many satisfied passengers? | Average satisfaction score available |
| Required data | SatisfactionScore with "satisfied" threshold | SatisfactionScore (1–5) exists; 603 NULLs (24.1%); no approved threshold (OD-11 pending) |
| Data grain | Passenger level | Feedback-event level (2,500 events), not passenger level |
| DAX | Count where SatisfactionScore >= threshold | CF02 = AVERAGE(SatisfactionScore) = 2.99; no count measure exists |
| Status | PARTIALLY SUPPORTED | Average score available; count of "satisfied passengers" not valid at passenger grain |

**Finding:** Only average satisfaction (CF02) is verifiable. "Satisfied Passengers" count cannot be computed because: (a) satisfaction is at feedback-event grain, not passenger grain; (b) fact-to-fact join not allowed; (c) no approved "satisfied" threshold (OD-11 pending).

### Component 5 — Neutral or Dissatisfied Passengers (KPI Card)

| Field | Reference Requirement | AEROVISION 360 Reality |
|-------|----------------------|----------------------|
| Business question | How many neutral/dissatisfied passengers? | Not directly available |
| Required data | SatisfactionScore with threshold | Same limitations as Component 4 |
| Status | PARTIALLY SUPPORTED | Same as Component 4 |

**Finding:** Same limitations as Component 4. Complaint rate (CF03 = 25.52%) is available as a proxy for dissatisfaction but is not a count of neutral/dissatisfied passengers.

### Component 6 — Passenger Satisfaction by Class & Type (bar chart)

| Field | Reference Requirement | AEROVISION 360 Reality |
|-------|----------------------|----------------------|
| Business question | How does satisfaction vary by class and travel type? | Cannot compute cross-tab |
| Required data | SatisfactionScore × CabinClass × TravelType | SatisfactionScore on fact_customer_feedback; CabinClass on dim_fare_class (unused, no FK); TravelType does not exist |
| Data grain | Feedback-event level with class & type dimensions | No common grain between satisfaction and class |
| Status | PARTIALLY SUPPORTED | Satisfaction exists; class dim exists but unused; travel type absent; no common grain |

**Finding:** Cannot build satisfaction × class × travel type. Closest supported alternative: Satisfaction by FeedbackType or by Airline (existing Page 05 visuals CF02 by AirlineName).

### Component 7 — Number of Passengers by Travel Type and Class (clustered column)

| Field | Reference Requirement | AEROVISION 360 Reality |
|-------|----------------------|----------------------|
| Business question | How many passengers by travel type and class? | Cannot compute |
| Required data | PassengerCount × TravelType × CabinClass | TravelType does not exist; dim_fare_class unused (no FK); PassengerCount on fact_booking_transactions (OD-04 blocked) |
| Status | UNSUPPORTED | No TravelType field; class dim unused; booking fact blocked |

**Finding:** CustomerSegment (Business/Corporate/Group/Leisure) exists on dim_customer but is a customer segment, not travel type, and cannot be linked to fare class at a common grain.

### Component 8 — Passenger Service Ratings (six categories)

| Reference Category | Reference Meaning | AEROVISION 360 Equivalent | Status |
|-------------------|------------------|--------------------------|--------|
| Arrival Time Convenience | Rating for arrival convenience | None | UNSUPPORTED |
| Cleanliness | Rating for cleanliness | None | UNSUPPORTED |
| Ease of Online Booking | Rating for booking ease | None | UNSUPPORTED |
| Baggage Handling | Rating for baggage handling | ComplaintCategory="Baggage" (complaints only) | PARTIAL |
| In-flight Service | Rating for in-flight service | ComplaintCategory="In-Flight Experience" (complaints only) | PARTIAL |
| Food and Drink | Rating for food and drink | None | UNSUPPORTED |
| Overall satisfaction | Overall score | SatisfactionScore (1–5), CF02 = 2.99 | SUPPORTED |

**Finding:** Six separate service-rating columns do NOT exist. Only one SatisfactionScore column and ComplaintCategory (populated only for complaints) exist. Cannot reproduce the six-category rating visual.

### Component 9 — Total Passengers by Class (donut chart)

| Field | Reference Requirement | AEROVISION 360 Reality |
|-------|----------------------|----------------------|
| Business question | How are passengers distributed by class? | Cannot compute class distribution |
| Required data | PassengerCount × CabinClass | CabinClass exists (Economy/Premium Economy/Business/First) but dim_fare_class has NO FK to any fact |
| Reference categories | Business, Economy, Economy Plus | Actual: Economy, Premium Economy, Business, First ("Economy Plus" absent) |
| Status | PARTIALLY SUPPORTED | Class values exist but relationship gap prevents use |

**Finding:** dim_fare_class is unused (no FK to fact_booking_transactions). Cannot build class donut without model change. "Economy Plus" must be replaced with "Premium Economy" if built.

### Component 10 — Passenger Behaviour Analysis (decomposition tree / Sankey)

| Reference Flow Step | Reference Dimension | AEROVISION 360 Equivalent | Status |
|--------------------|--------------------|--------------------------|--------|
| Total Passengers | Passenger count | RV_RevenuePassengers (OD-04 blocked) or SUM(PassengerCount) | PARTIAL |
| Gender | Gender | **DOES NOT EXIST** | UNSUPPORTED |
| Customer Type | Customer type | CustomerSegment (Business/Corporate/Group/Leisure) | PARTIAL (proxy) |
| Type of Travel | Travel type | **DOES NOT EXIST** | UNSUPPORTED |
| Satisfaction | Satisfaction | SatisfactionScore (feedback grain only) | PARTIAL (different grain) |
| Connected journey | Fact-to-fact path | Not allowed | UNSUPPORTED |

**Finding:** The decomposition tree flow cannot be built as specified. Gender and Travel Type are absent; fact-to-fact join not allowed; satisfaction at different grain.

---

## 3. Reference Component Feasibility Summary

| # | Component | Classification | Primary Blocker |
|---|-----------|---------------|-----------------|
| 1 | Total Passengers | PARTIALLY SUPPORTED | OD-04 blocked; grain ambiguity (coupons vs passengers) |
| 2 | Male Passengers | UNSUPPORTED | No gender field |
| 3 | Female Passengers | UNSUPPORTED | No gender field |
| 4 | Satisfied Passengers | PARTIALLY SUPPORTED | Satisfaction at feedback grain; no threshold (OD-11); not passenger grain |
| 5 | Neutral/Dissatisfied | PARTIALLY SUPPORTED | Same as #4 |
| 6 | Satisfaction by Class & Type | PARTIALLY SUPPORTED | Class dim unused; travel type absent; no common grain |
| 7 | Passengers by Travel Type & Class | UNSUPPORTED | No TravelType; class dim unused |
| 8 | Service Ratings (six) | UNSUPPORTED | Only one SatisfactionScore; no per-category ratings |
| 9 | Passengers by Class (donut) | PARTIALLY SUPPORTED | dim_fare_class unused (no FK); "Economy Plus" absent |
| 10 | Behaviour Analysis | UNSUPPORTED | Gender & Travel Type absent; fact-to-fact not allowed |

---

## 4. What the Reference Gets Right (Analytical Intent)

Even though specific components are unsupported, the reference's analytical intent is sound:

| Reference Intent | Supported Alternative in AEROVISION 360 |
|-----------------|----------------------------------------|
| Customer volume | Total Feedback Events (CF01 = 2,500) |
| Customer satisfaction | Average Satisfaction Score (CF02 = 2.99) |
| Complaint monitoring | Complaint Rate (CF03 = 25.52%) |
| Customer base health | Active Customers (CF04 = 4,808) |
| Feedback by channel | Feedback by Channel (existing bar chart) |
| Feedback by type | Feedback by Type (existing bar chart) |
| Resolution performance | Resolution Rate (CF12) |
| Service recovery | Service Recovery Rate (CF11) |
| Satisfaction by airline | Avg Satisfaction by Airline (existing bar chart) |
| Customer segmentation | Customer Segment (Business/Corporate/Group/Leisure) |
