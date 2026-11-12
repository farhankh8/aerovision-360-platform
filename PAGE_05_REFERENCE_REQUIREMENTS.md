# AEROVISION 360 — Page 05 Reference Dashboard Requirements

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Target Page:** Page 05 — Customer & Service Intelligence (Passenger Satisfaction Review)  
**Reference:** Maven Analytics Airline Passenger Satisfaction Review  
**Analysis Date:** 2026-11-08  
**Status:** REQUIREMENTS BREAKDOWN COMPLETE — READ-ONLY  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Reference Component Inventory

The reference dashboard contains 16 component groups across KPIs, charts, slicers, and filters. Each is analyzed below for exact field, grain, calculation, and relationship requirements.

---

## 2. Component-by-Component Requirements

### Component 1 — Total Passengers (KPI Card)

| Attribute | Requirement |
|-----------|-------------|
| Business question | What is the total passenger volume across the network? |
| Intended metric | Count of all passengers |
| Required data grain | One record = one passenger |
| Required source tables | FactBookingTransactions (PassengerCount) or FactFlightOperations (RevenuePassengers) |
| Required columns | PassengerCount, IsRevenuePassenger, or RevenuePassengers |
| Required DAX | SUM(PassengerCount) or CALCULATE(SUM(PassengerCount), IsRevenuePassenger=TRUE) |
| Required relationships | FactBookingTransactions → DimDate (TravelDateKey active) |
| Filters/interactions | Period (travel date), Airline, Route |
| Reference provides calculation? | No — no specific numbers or formula visible |
| **AEROVISION 360 availability** | PARTIALLY SUPPORTED — RV_RevenuePassengers = 8,922 exists but OD-04 BLOCKED; SUM(PassengerCount) = 9,956 coupons; FL02 = 218,413 flight-level (different population) |

---

### Component 2 — Male Passengers (KPI Card)

| Attribute | Requirement |
|-----------|-------------|
| Business question | How many passengers are male? |
| Intended metric | Count of male passengers |
| Required data grain | One record = one passenger with gender attribute |
| Required source tables | DimCustomer or FactBookingTransactions with Gender column |
| Required columns | Gender (Male/Female) |
| Required DAX | CALCULATE([Total Passengers], Gender = "Male") |
| Required relationships | DimCustomer → facts |
| Filters/interactions | Gender slicer |
| Reference provides calculation? | No |
| **AEROVISION 360 availability** | UNSUPPORTED — Gender column does not exist in any table, script, DAX, or documentation. Zero matches in project-wide search. Must not infer from names or IDs. |

---

### Component 3 — Female Passengers (KPI Card)

| Attribute | Requirement |
|-----------|-------------|
| Business question | How many passengers are female? |
| Intended metric | Count of female passengers |
| Required data grain | One record = one passenger with gender attribute |
| Required source tables | DimCustomer or FactBookingTransactions with Gender column |
| Required columns | Gender (Male/Female) |
| Required DAX | CALCULATE([Total Passengers], Gender = "Female") |
| Required relationships | DimCustomer → facts |
| Filters/interactions | Gender slicer |
| Reference provides calculation? | No |
| **AEROVISION 360 availability** | UNSUPPORTED — Same as Component 2. Gender column does not exist anywhere in the project. |

---

### Component 4 — Satisfied Passengers (KPI Card)

| Attribute | Requirement |
|-----------|-------------|
| Business question | How many passengers are satisfied? |
| Intended metric | Count of passengers with satisfaction above threshold |
| Required data grain | One record = one passenger with satisfaction classification |
| Required source tables | FactCustomerFeedback (SatisfactionScore) linked to passenger data |
| Required columns | SatisfactionScore, satisfaction threshold definition |
| Required DAX | CALCULATE([Total Passengers], SatisfactionScore >= threshold) |
| Required relationships | Fact-to-fact join (bookings ↔ feedback) OR satisfaction at passenger grain |
| Filters/interactions | Satisfaction slicer (Satisfied / Neutral or Dissatisfied) |
| Reference provides calculation? | No — no threshold definition visible |
| **AEROVISION 360 availability** | PARTIALLY SUPPORTED — SatisfactionScore exists (1-5, 1,897 non-null of 2,500) but only at feedback-event grain, not passenger grain. Fact-to-fact join prohibited. OD-11 threshold undefined. CF02 = AVERAGE(SatisfactionScore) = 2.99 is available as average, not count. |

---

### Component 5 — Neutral or Dissatisfied Passengers (KPI Card)

| Attribute | Requirement |
|-----------|-------------|
| Business question | How many passengers are neutral or dissatisfied? |
| Intended metric | Count of passengers with satisfaction at or below threshold |
| Required data grain | One record = one passenger with satisfaction classification |
| Required source tables | Same as Component 4 |
| Required columns | SatisfactionScore, threshold definition |
| Required DAX | CALCULATE([Total Passengers], SatisfactionScore < threshold) |
| Required relationships | Same as Component 4 |
| Filters/interactions | Same as Component 4 |
| Reference provides calculation? | No |
| **AEROVISION 360 availability** | PARTIALLY SUPPORTED — Same limitations as Component 4. CF03 = Complaint Rate (25.52%) available as proxy but not a count of neutral/dissatisfied passengers. |

---

### Component 6 — Passenger Class (Slicer)

| Attribute | Requirement |
|-----------|-------------|
| Business question | Filter analysis by passenger cabin class |
| Intended metric | N/A (filter dimension) |
| Required data grain | One record = one fare class definition |
| Required source tables | DimFareClass linked to FactBookingTransactions |
| Required columns | CabinClass (Business, Economy, Economy Plus) |
| Required DAX | N/A (slicer dimension) |
| Required relationships | DimFareClass → FactBookingTransactions (FareClassKey) |
| Filters/interactions | Multi-select slicer on CabinClass |
| Reference provides values? | Yes — Business, Economy, Economy Plus |
| **AEROVISION 360 availability** | PARTIALLY SUPPORTED — DimFareClass exists with CabinClass values (Economy, Premium Economy, Business, First) but has NO FK to any fact table. "Economy Plus" does not exist (closest is Premium Economy). Relationship must be added to use. |

---

### Component 7 — Travel Type (Slicer)

| Attribute | Requirement |
|-----------|-------------|
| Business question | Filter analysis by purpose of travel |
| Intended metric | N/A (filter dimension) |
| Required data grain | One record = one travel type definition |
| Required source tables | FactBookingTransactions or DimCustomer with TravelType column |
| Required columns | TravelType (Business, Personal) |
| Required DAX | N/A (slicer dimension) |
| Required relationships | Fact table → dim with TravelType |
| Filters/interactions | Multi-select slicer on TravelType |
| Reference provides values? | Yes — Business, Personal |
| **AEROVISION 360 availability** | UNSUPPORTED — TravelType column does not exist in any table, script, DAX, or documentation. Zero matches in project-wide search. |

---

### Component 8 — Satisfaction Slicer

| Attribute | Requirement |
|-----------|-------------|
| Business question | Filter analysis by satisfaction category |
| Intended metric | N/A (filter dimension) |
| Required data grain | One record = one satisfaction category |
| Required source tables | FactCustomerFeedback with satisfaction bucket |
| Required columns | SatisfactionScore (bucketed to Satisfied/Neutral/Dissatisfied) |
| Required DAX | Bucketing logic based on OD-11 threshold |
| Required relationships | FactCustomerFeedback → DimDate (FeedbackDateKey) |
| Filters/interactions | Multi-select slicer (Satisfied, Neutral or Dissatisfied) |
| Reference provides values? | Yes — Satisfied, Neutral or Dissatisfied |
| **AEROVISION 360 availability** | PARTIALLY SUPPORTED — SatisfactionScore exists but no approved bucketing threshold (OD-11 pending). Can use raw score values (1-5) as slicer but not categorized buckets. |

---

### Component 9 — Customer Type Slicer

| Attribute | Requirement |
|-----------|-------------|
| Business question | Filter analysis by customer type |
| Intended metric | N/A (filter dimension) |
| Required data grain | One record = one customer type definition |
| Required source tables | DimCustomer with CustomerType column |
| Required columns | CustomerType (Loyal, Disloyal, or similar) |
| Required DAX | N/A (slicer dimension) |
| Required relationships | DimCustomer → facts |
| Filters/interactions | Multi-select slicer on CustomerType |
| Reference provides values? | Yes — Loyal Customer, Disloyal Customer (from reference dataset) |
| **AEROVISION 360 availability** | PARTIALLY SUPPORTED — DimCustomer has CustomerSegment (Leisure, Business, Corporate, Group) which is a proxy but not the same as reference's Loyal/Disloyal Customer Type. Different taxonomy. |

---

### Component 10 — Type of Travel Slicer

| Attribute | Requirement |
|-----------|-------------|
| Business question | Filter analysis by travel purpose |
| Intended metric | N/A (filter dimension) |
| Required data grain | One record = one travel type definition |
| Required source tables | FactBookingTransactions with TypeOfTravel column |
| Required columns | TypeOfTravel (Business Travel, Personal Travel) |
| Required DAX | N/A (slicer dimension) |
| Required relationships | Fact table → dim with TypeOfTravel |
| Filters/interactions | Multi-select slicer on TypeOfTravel |
| Reference provides values? | Yes — Business Travel, Personal Travel |
| **AEROVISION 360 availability** | UNSUPPORTED — TypeOfTravel/TravelType column does not exist anywhere in the project. |

---

### Component 11 — Passenger Satisfaction by Class & Type (Clustered/Stacked Horizontal Bar)

| Attribute | Requirement |
|-----------|-------------|
| Business question | How does satisfaction vary by cabin class and travel type? |
| Intended metric | Passenger count or average satisfaction by class × travel type |
| Required data grain | One record = one passenger with class, travel type, and satisfaction |
| Required source tables | FactBookingTransactions (class, travel type, passengers) + FactCustomerFeedback (satisfaction) linked at passenger level |
| Required columns | CabinClass, TravelType, SatisfactionScore, PassengerCount |
| Required DAX | Cross-tab of satisfaction by class × travel type with passenger counts |
| Required relationships | Fact-to-fact join OR common grain between bookings and feedback |
| Filters/interactions | Class slicer, Travel Type slicer, Satisfaction slicer, Period |
| Reference provides calculation? | No — no specific numbers visible |
| **AEROVISION 360 availability** | UNSUPPORTED AS SPECIFIED — Class (dim_fare_class) unused, TravelType absent, satisfaction at feedback-event grain, fact-to-fact join prohibited. Cannot compute cross-tab. |

---

### Component 12 — Number of Passengers by Travel Type and Class (Clustered Column)

| Attribute | Requirement |
|-----------|-------------|
| Business question | How many passengers travel by type and class? |
| Intended metric | Passenger count by TravelType × CabinClass |
| Required data grain | One record = one passenger with travel type and class |
| Required source tables | FactBookingTransactions with TravelType and FareClassKey linked to DimFareClass |
| Required columns | TravelType, CabinClass, PassengerCount |
| Required DAX | SUM(PassengerCount) grouped by TravelType and CabinClass |
| Required relationships | FactBookingTransactions → DimFareClass (FareClassKey), TravelType column in fact |
| Filters/interactions | Period, Airline, Route |
| Reference provides calculation? | No |
| **AEROVISION 360 availability** | UNSUPPORTED — TravelType absent; dim_fare_class unused (no FK); fact grain is coupon (PassengerCount always 1). |

---

### Component 13 — Passenger Service Ratings (Six Categories)

| Attribute | Requirement |
|-----------|-------------|
| Business question | How do passengers rate individual service quality factors? |
| Intended metric | Average rating per service category |
| Required data grain | One record = one passenger with per-category ratings |
| Required source tables | Feedback/survey data with per-category rating columns |
| Required columns | Arrival Time Convenience, Cleanliness, Ease of Online Booking, Baggage Handling, In-flight Service, Food and Drink (each 0-5 or 1-5 scale) |
| Required DAX | AVERAGE of each rating column |
| Required relationships | Feedback table → DimDate, DimAirline |
| Filters/interactions | Period, Airline, Route, Class |
| Reference provides categories? | Yes — six named categories |
| **AEROVISION 360 availability** | UNSUPPORTED — Only one SatisfactionScore column (1-5) exists. ComplaintCategory exists but only populated for complaints (638 of 2,500 events) and is not a rating scale. Six named categories do not exist in any table. |

---

### Component 14 — Total Passengers by Class (Donut Chart)

| Attribute | Requirement |
|-----------|-------------|
| Business question | How are passengers distributed across cabin classes? |
| Intended metric | Passenger count and percentage by CabinClass |
| Required data grain | One record = one passenger with class |
| Required source tables | FactBookingTransactions (PassengerCount) + DimFareClass (CabinClass) |
| Required columns | CabinClass, PassengerCount |
| Required DAX | SUM(PassengerCount) grouped by CabinClass; percentage of total |
| Required relationships | FactBookingTransactions → DimFareClass (FareClassKey) |
| Filters/interactions | Period, Airline, Route |
| Reference provides values? | Yes — Business, Economy, Economy Plus |
| **AEROVISION 360 availability** | PARTIALLY SUPPORTED — CabinClass values exist (Economy, Premium Economy, Business, First) but dim_fare_class has NO FK to any fact. "Economy Plus" absent. Relationship must be added. |

---

### Component 15 — Passenger Behaviour Analysis (Decomposition Tree / Sankey)

| Attribute | Requirement |
|-----------|-------------|
| Business question | How do customer attributes flow through to satisfaction outcomes? |
| Intended metric | Hierarchical breakdown: Total → Gender → Customer Type → Type of Travel → Satisfaction |
| Required data grain | One record = one passenger with all attributes |
| Required source tables | Unified passenger dataset with Gender, CustomerType, TypeOfTravel, Satisfaction |
| Required columns | Gender, CustomerType, TypeOfTravel, Satisfaction, PassengerCount |
| Required DAX | Decomposition tree measure hierarchy |
| Required relationships | All dimensions connected to common passenger grain |
| Filters/interactions | All slicers apply |
| Reference provides flow? | Yes — Gender → Customer Type → Type of Travel → Satisfaction |
| **AEROVISION 360 availability** | UNSUPPORTED AS SPECIFIED — Gender and TravelType absent; satisfaction at feedback-event grain not passenger grain; fact-to-fact join prohibited. |

---

### Component 16 — Gender Slicer

| Attribute | Requirement |
|-----------|-------------|
| Business question | Filter all visuals by passenger gender |
| Intended metric | N/A (filter dimension) |
| Required data grain | One record = one gender value |
| Required source tables | DimCustomer with Gender column |
| Required columns | Gender (Male, Female) |
| Required DAX | N/A |
| Required relationships | DimCustomer → facts |
| Filters/interactions | Multi-select slicer applied to all Page 05 visuals |
| Reference provides values? | Yes — Male, Female |
| **AEROVISION 360 availability** | UNSUPPORTED — Gender column does not exist anywhere in the project. |

---

## 3. Reference Filter Requirements

| Slicer | Reference Values | AEROVISION 360 Equivalent | Status |
|--------|----------------|---------------------------|--------|
| Passenger Class | Business, Economy, Economy Plus | CabinClass: Economy, Premium Economy, Business, First | PARTIAL — "Economy Plus" absent; dim_fare_class unused |
| Travel Type | Business, Personal | None exists | UNSUPPORTED |
| Satisfaction | Satisfied, Neutral or Dissatisfied | SatisfactionScore 1-5 (no approved threshold) | PARTIAL — OD-11 pending |
| Gender | Male, Female | None exists | UNSUPPORTED |
| Customer Type | Loyal Customer, Disloyal Customer | CustomerSegment: Leisure, Business, Corporate, Group | PARTIAL — different taxonomy |
| Airline Name | 10 real airlines | AirlineName: 10 synthetic airline names | SUPPORTED |
| Flight Date Range | Date range | DimDate FullDate (2024-10-01 to 2026-10-31) | SUPPORTED (inactive relationship to feedback) |

---

## 4. Reference Analytical Flow Requirements

### Reference Decomposition Tree Flow

```
Total Passengers
    → Gender (Male / Female)
        → Customer Type (Loyal / Disloyal)
            → Type of Travel (Business / Personal)
                → Satisfaction (Satisfied / Neutral or Dissatisfied)
```

### AEROVISION 360 Equivalent Flow (Maximum Possible)

```
Total Feedback Events (CF01 = 2,500)
    → FeedbackType (Survey / Complaint / Claim / Compliment)
        → ResolutionStatus (Open / In Progress / Resolved / Closed - No Action)
            → SatisfactionScore (1-5, 1,897 valid)
```

**Gap:** The reference flow starts with passenger-level attributes (Gender, Customer Type, Travel Type) that do not exist in AEROVISION 360. The closest AEROVISION 360 equivalent starts with feedback-event attributes that all exist.

---

## 5. Requirements Summary Matrix

| # | Component | Classification | Primary Blocker | Can Be Built With Native Data? |
|---|-----------|---------------|-----------------|-------------------------------|
| 1 | Total Passengers | PARTIALLY SUPPORTED | OD-04 blocked; grain ambiguity | Partial (CF01 as proxy) |
| 2 | Male Passengers | UNSUPPORTED | No Gender field | No |
| 3 | Female Passengers | UNSUPPORTED | No Gender field | No |
| 4 | Satisfied Passengers | PARTIALLY SUPPORTED | Satisfaction not at passenger grain; OD-11 threshold absent | No (count); Yes (avg via CF02) |
| 5 | Neutral/Dissatisfied | PARTIALLY SUPPORTED | Same as #4 | No (count); Yes (CF03 as proxy) |
| 6 | Passenger Class slicer | PARTIALLY SUPPORTED | dim_fare_class unused; "Economy Plus" absent | No (needs model change) |
| 7 | Travel Type slicer | UNSUPPORTED | No TravelType field | No |
| 8 | Satisfaction slicer | PARTIALLY SUPPORTED | No approved threshold (OD-11) | Partial (raw score 1-5) |
| 9 | Customer Type slicer | PARTIALLY SUPPORTED | Different taxonomy (CustomerSegment) | Yes (proxy) |
| 10 | Type of Travel slicer | UNSUPPORTED | No TypeOfTravel field | No |
| 11 | Satisfaction by Class & Type | UNSUPPORTED | Class unused; TravelType absent; fact-to-fact prohibited | No |
| 12 | Passengers by Travel Type & Class | UNSUPPORTED | TravelType absent; class unused | No |
| 13 | Six Service Ratings | UNSUPPORTED | Only one SatisfactionScore column | No |
| 14 | Passengers by Class donut | PARTIALLY SUPPORTED | dim_fare_class unused; "Economy Plus" absent | No (needs model change) |
| 15 | Behaviour Analysis | UNSUPPORTED | Gender & TravelType absent; fact-to-fact prohibited | No |
| 16 | Gender slicer | UNSUPPORTED | No Gender field | No |

**Summary:** 5 UNSUPPORTED, 7 PARTIALLY SUPPORTED, 4 components have partial native-data equivalents. None of the reference components can be built exactly as specified using only native AEROVISION 360 data.

---

## 6. Fields Required but Missing from AEROVISION 360

| Field | Required For | Classification | Source Needed |
|-------|-------------|----------------|---------------|
| Gender | Components 2, 3, 16 | C — Not located | Customer demographic source |
| TravelType / TypeOfTravel | Components 7, 10, 11, 12 | C — Not located | Booking data with travel purpose |
| Service rating columns (6+) | Component 13 | C — Not located | Per-category satisfaction survey data |
| Satisfaction threshold definition | Components 4, 5, 8 | B — OD-11 pending | Owner decision |
| Economy Plus cabin class | Components 6, 14 | C — Not located | Fare class taxonomy update |
| Passenger-level identifier | Components 11, 12, 15 | C — Not located | Unified passenger grain |
| Fact-to-fact join capability | Components 11, 15 | A — Prohibited | Governance policy change |

---

## 7. Conclusion

The reference dashboard requires 11 fields/dimensions that do not exist in AEROVISION 360, plus 2 governance decisions (OD-04, OD-11) that are unresolved. The only components that can be built with native data are those based on FactCustomerFeedback measures (CF01-CF14) and DimCustomer segmentation. All passenger-level, gender, travel-type, and service-rating components require either new source data or governance decisions before implementation.
