# AEROVISION 360 — PAGE 05 CUSTOMER & SERVICE INTELLIGENCE

## Complete Data Discovery, Semantic Model Audit & Dashboard Implementation Report

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Report Date:** 2026-11-08  
**Role:** Data & Architecture Research Assistant (Investigation Only)  
**Status:** INVESTIGATION AND DOCUMENTATION ONLY — NO IMPLEMENTATION PERFORMED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## STRICT RULES OBSERVED

- Inspected the actual project only; no assumptions, no fabricated columns, no invented values.
- Did NOT modify the report, semantic model, Power Query, relationships, or DAX measures.
- Did NOT create visuals or new measures.
- Did NOT infer gender from names, IDs, or any indirect attribute.
- Respected fact-table grain; distinguished passenger count from customer count.
- Reused existing validated measures wherever possible; did not duplicate unnecessarily.
- Documented every finding with its source table, column, measure, or file.

---

# EXECUTIVE SUMMARY

Page 05 – Customer & Service Intelligence **already exists** in `deliverables/power_bi/report/report.json` with 13 visuals (8 KPI cards CF01–CF12, 5 bar charts), but it does **NOT** match the reference dashboard structure requested. The reference dashboard (5 KPI cards: Total/Male/Female/Satisfied/Neutral-or-Dissatisfied passengers; satisfaction-by-class; travel-type-by-class; six service ratings; class donut; behaviour decomposition tree) **cannot be reproduced as specified** because multiple required data elements are genuinely absent from the AEROVISION 360 semantic model and source data.

### Headline findings

| # | Finding | Source |
|---|---------|--------|
| 1 | **Gender field does not exist anywhere** in the model, source CSVs/Parquet, Power Query, DAX, or measures. | `dim_customer` manifest (8 columns, no Gender); grep of all project files — zero matches |
| 2 | **Travel Type field does not exist anywhere** (no "TravelType", "Type of Travel"). | `fact_booking_transactions` (45 cols), `fact_customer_feedback` (14 cols), `dim_customer` (8 cols) — grep zero matches |
| 3 | **"Economy Plus" cabin class does not exist**. Actual CabinClass values: Economy, Premium Economy, Business, First. | `dim_fare_class` manifest & data |
| 4 | **Six service-rating categories do not exist**. Only ONE `SatisfactionScore` (1–5) column + `ComplaintCategory`. | `fact_customer_feedback` manifest & data |
| 5 | **fact_booking_transactions is BLOCKED per OD-04** (exchange-rate policy, unresolved). Passenger-count measures (RV_*) exist in DAX but are under governance question. | `m311_governed_measures.py` UNDEF-01/UNDEF-02; `GOVERNANCE_COMPLIANCE.md`; `POWER_BI_REMEDIATION_PLAN.md` |
| 6 | **fact_customer_feedback has NO active date relationship** (FeedbackDateKey & ResolutionDateKey both inactive). | `semantic_model.json` relationships; `RELATIONSHIP_VALIDATION.csv` rows 19–20 |
| 7 | **dim_fare_class, dim_booking_channel, dim_currency have NO FK to any fact** (unused dimensions). | `RELATIONSHIP_VALIDATION.csv` rows 23–25 |
| 8 | **Fact-to-fact relationships are NOT allowed** — booking data and feedback data cannot be directly joined. | `RELATIONSHIP_VALIDATION.csv` rows 21–22 |
| 9 | SatisfactionScore has **603 NULLs out of 2500** (24.1% missing). | `fact_customer_feedback` data profile |
| 10 | PassengerCount is **always 1** (9956 coupons); SUM = 9956, SUM(IsRevenuePassenger=TRUE) = 8922. | `fact_booking_transactions` data profile |

### Bottom line

The reference dashboard's analytical structure **cannot be reproduced faithfully** with verified AEROVISION 360 data. Male/Female KPIs and the full behaviour-decomposition journey (which starts with Gender) are **unsupported** and must be removed or replaced. The six service ratings are **unsupported**; the closest genuine equivalent is the single `SatisfactionScore` (1–5) plus `ComplaintCategory`. Travel Type is **unsupported**; `dim_customer[CustomerSegment]` (Business/Corporate/Group/Leisure) is the closest proxy but is a customer segment, not a travel type.

Recommended path: build Page 05 using **only** the supported elements (feedback counts, average satisfaction, complaint rate, active customers, feedback by channel/type/airline/resolution — i.e., the existing CF measures and the 13 visuals already in report.json), plus a class-based view **only if** the dim_fare_class relationship gap is resolved. Do not build gender, travel-type, or six-rating visuals.

---

# COMPLETE RELEVANT TABLE INVENTORY

All tables in the semantic model (`deliverables/power_bi/semantic_model/semantic_model.json`), with suitability for Page 05.

| # | Table | Rows | Grain | PK | Suitable for Page 05? | Notes |
|---|-------|------|-------|----|----------------------|-------|
| 1 | dim_customer | 5,000 | one row per fictional customer | CustomerKey | **YES — partial** | CustomerSegment = "Customer Type" proxy; LoyaltyTier; HomeCountry. **NO Gender.** |
| 2 | fact_customer_feedback | 2,500 | one row per feedback event | FeedbackKey | **YES** | SatisfactionScore (1–5), FeedbackType, ComplaintCategory, FeedbackChannel, ServiceRecoveryFlag. Single score only. |
| 3 | fact_booking_transactions | 9,956 | one row per passenger ticket coupon | BookingTransactionKey | **PARTIAL / BLOCKED** | PassengerCount, IsRevenuePassenger, FareClassKey. OD-04 blocked. PassengerCount always = 1. |
| 4 | dim_fare_class | 8 | one row per synthetic fare class | FareClassKey | **PARTIAL** | CabinClass (Economy/Premium Economy/Business/First). **NO FK to any fact** (unused dimension). |
| 5 | dim_airline | 10 | one row per airline | AirlineKey | YES | AirlineName slicer/legend. |
| 6 | dim_date | 761 | one row per calendar date | DateKey | YES | FullDate (2024-10-01 to 2026-10-31); reporting period 2025-10-01 to 2026-09-30. |
| 7 | dim_route | 320 | one row per directional O-D pair | RouteKey | YES | RouteCode. |
| 8 | dim_airport | 72 | one row per fictional airport | AirportKey | NO | Not customer-facing. |
| 9 | dim_aircraft | 440 | one row per fictional aircraft | AircraftKey | NO | Not customer-facing. |
| 10 | dim_aircraft_type | 12 | one row per aircraft type | AircraftTypeKey | NO | Not customer-facing. |
| 11 | dim_booking_channel | 7 | one row per booking channel | BookingChannelKey | **UNUSED** | No FK to any fact. ChannelName exists but cannot slice facts. |
| 12 | dim_currency | 8 | one row per currency | CurrencyKey | **UNUSED / BLOCKED** | No FK to any fact; OD-04 finance blocked. |
| 13 | dim_disruption_type | 9 | one row per disruption type | DisruptionTypeKey | NO | Not customer-facing. |
| 14 | fact_flight_operations | 5,000 | one row per flight operation leg | FlightOperationKey | **PARTIAL** | RevenuePassengers (FL02=218,413) — flight-level passenger volume, NOT booking-level. |
| 15 | fact_disruptions | 1,754 | one row per disruption event | DisruptionKey | NO | Not customer-facing. |
| 16 | fact_operating_costs | — | one row per cost ledger line | OperatingCostKey | NO / BLOCKED | OD-04 blocked. Not customer-facing. |

Other tables discovered: `dim_fare_class`, `dim_booking_channel`, `dim_currency` are present in the model but **unused** (no FK relationships to any fact table).

---

# COLUMN-LEVEL DATA DICTIONARY

## dim_customer (5,000 rows, PK CustomerKey, no nulls in any column)

| Column | Type | Distinct values / sample | Page 05 use |
|--------|------|-------------------------|-------------|
| CustomerKey | int32 | 1–5000 (unique) | Join key to facts |
| CustomerID | string | synthetic (e.g., CUST-...) | Business key, not for display |
| CustomerSegment | string | Leisure(3107), Business(1118), Corporate(496), Group(279) | **Closest proxy for "Customer Type"** |
| LoyaltyTier | string | Silver(1980), Gold(1514), Platinum(820), None(686; 686 NULL per DQ audit — see note) | Loyalty slicer |
| HomeCountry | string | 8 countries | Geography slicer |
| HomeCountryCode | string | IN(1288), AE(906), GB(593), SG(509), US(485), QA(474), DE(412), AU(333) | Geography slicer |
| RegistrationDate | date | 2024-10-01 to 2025-09-30 | Not for Page 05 |
| IsActive | boolean | True(4808), False(192) | Active-customer filter |
| **Gender** | — | **DOES NOT EXIST** | — |

Note: DQ audit CSV lists `LoyaltyTier=686` nulls, but direct data profile shows 0 nulls and LoyaltyTier "None" count = 686. The manifest lists `"no_null_values": true`. Treated as no nulls; "None" is a valid tier value.

**Gender availability finding:** `dim_customer[Gender]` does not exist. Confirmed absent from manifest, data, model.json, semantic_model.json, DAX file, Power Query, and all project files (zero grep matches). **Gender cannot be used. Male/Female KPIs must be removed.**

## fact_customer_feedback (2,500 rows, PK FeedbackKey, grain = one feedback event)

| Column | Type | Distinct values / sample | Nulls | Page 05 use |
|--------|------|-------------------------|-------|-------------|
| FeedbackKey | int64 | unique | 0 | Count (CF01) |
| FeedbackID | string | unique | 0 | Business key |
| CustomerKey | int32 | FK → dim_customer | 0 | Join to customer |
| AirlineKey | int32 | FK → dim_airline (10 airlines) | 0 | Airline slicer |
| FlightOperationKey | int64 | FK → fact_flight_operations | 0 | Degenerate fact ref (no relationship) |
| RouteKey | int32 | FK → dim_route | 0 | Route slicer |
| FeedbackDateKey | int32 | FK → dim_date (INACTIVE relationship) | 0 | Date — requires USERELATIONSHIP |
| FeedbackType | string | Survey(641), Complaint(638), Claim(618), Compliment(603) | 0 | Feedback-type breakdown |
| SatisfactionScore | int8 | 1,2,3,4,5 (mean 2.99) | **603** | Satisfaction avg (CF02) |
| ComplaintCategory | string | Other, Delay, Seat, Customer Service, Baggage, In-Flight Experience, Cancellation, Boarding | **1862** (only populated for complaints) | Complaint breakdown |
| ServiceRecoveryFlag | boolean | True(381), False(2119) | 0 | Service recovery (CF11) |
| ResolutionStatus | string | Open, Closed - No Action, In Progress, Resolved | 0 | Resolution breakdown (CF12) |
| ResolutionDateKey | int32 | FK → dim_date (INACTIVE) | 1896 | Not for Page 05 |
| FeedbackChannel | string | Email, Call Center, Social, Web, Mobile, Airport | 0 | Channel breakdown |

**Six service-rating categories (Arrival Time Convenience, Cleanliness, Ease of Online Booking, Baggage Handling, In-flight Service, Food and Drink): DO NOT EXIST.** Only one `SatisfactionScore` column (1–5) and one `ComplaintCategory` column. No per-category rating columns.

## fact_booking_transactions (9,956 rows, PK BookingTransactionKey, grain = one passenger ticket coupon) — OD-04 BLOCKED

| Column | Type | Distinct values / sample | Nulls | Page 05 use |
|--------|------|-------------------------|-------|-------------|
| BookingTransactionKey | int64 | unique | 0 | Count (RV_BookingCount) |
| BookingReference | string | unique | 0 | Distinct bookings (RV_DistinctBookings) |
| CustomerKey | int32 | FK → dim_customer; 4,204 distinct | 0 | Customer join |
| AirlineKey | int32 | FK → dim_airline | 0 | Airline slicer |
| FlightOperationKey | int64 | FK → fact_flight_operations | 0 | Degenerate fact ref |
| RouteKey | int32 | FK → dim_route | 0 | Route slicer |
| FareClassKey | int32 | FK → dim_fare_class; values 1–8 | 0 | Class join — but dim_fare_class unused |
| BookingChannelKey | int32 | FK → dim_booking_channel | 0 | Channel — but unused |
| BookingDateKey | int32 | FK → dim_date (INACTIVE) | 0 | Booking date — inactive |
| TravelDateKey | int32 | FK → dim_date (ACTIVE) | 0 | Travel date — active |
| PassengerCount | int8 | **always 1** | 0 | SUM=9956 (all); SUM(IsRevenuePassenger=TRUE)=8922 |
| IsRevenuePassenger | boolean | True(8922), False(1034) | 0 | Revenue vs non-revenue split |
| IsRefunded | boolean | False(9457), True(499) | 0 | Exclude refunded? |
| NetPassengerRevenueUSD | decimal | — | 0 | Revenue (OD-04 blocked) |
| TransactionStatus | string | Flown, Ticketed, Booked, Cancelled, Refunded, NoShow | 0 | Status filter |
| **TravelType / Type of Travel** | — | **DOES NOT EXIST** | — | — |
| **Gender** | — | **DOES NOT EXIST** | — | — |

OD-04 status: FactBookingTransactions is **blocked** (exchange-rate policy, unresolved). RV_* measures exist in DAX but are under governance question per `GOVERNANCE_COMPLIANCE.md` and `POWER_BI_REMEDIATION_PLAN.md`.

## dim_fare_class (8 rows, PK FareClassKey) — NO FK to any fact (UNUSED)

| Column | Type | Values |
|--------|------|--------|
| FareClassKey | int32 | 1–8 |
| FareClassCode | string | Y, M, B, W, E, J, C, F |
| FareClassName | string | Economy Flexible, Economy Standard, Economy Basic, Premium Economy Flexible, Premium Economy Standard, Business Flexible, Business Standard, First Flexible |
| CabinClass | string | Economy(3), Premium Economy(2), Business(2), First(1) |
| RefundabilityCategory | string | Refundable, Partially Refundable, Non-Refundable |
| IsAncillaryEligible | boolean | True (all) |
| DisplayOrder | int | 1, 2 |

**CabinClass is the class dimension.** Reference wants "Business, Economy, Economy Plus." Actual values: Economy, Premium Economy, Business, First. **"Economy Plus" does not exist** — closest is Premium Economy. Because dim_fare_class has **no FK to any fact**, it cannot slice fact_booking_transactions without a model change (which is out of scope for this investigation).

## dim_airline (10 rows), dim_date (761 rows), dim_route (320 rows)

- dim_airline: AirlineName available for slicer/legend. 3 columns entirely null (AirlineGroup, BusinessModelClass, StatusEffectiveDate).
- dim_date: FullDate, IsReportingPeriod, Year, Quarter, MonthName, etc. Range 2024-10-01 to 2026-10-31. Reporting period 2025-10-01 to 2026-09-30.
- dim_route: RouteCode, RouteRegion, IsInternational, IsActive.

## fact_flight_operations (5,000 rows)

- RevenuePassengers: SUM = 218,413 (FL02 = "Total Revenue Passengers"). Flight-level grain. **Different population from booking-level 8,922.** Must not be mixed with RV_RevenuePassengers.

---

# EXISTING DAX MEASURE INVENTORY

Source: `deliverables/power_bi/dax/AEROVISION360_Measures.dax`, `model.json`, `semantic_model.json`, `contracts/bi_consumption_model_m311.json`. All 54 measures from Page 04 audit plus CF measures.

### Customer-feedback measures (CF) — defined in fact_customer_feedback, expressions present

| Measure | DAX formula | Business definition | Reusable for Page 05? |
|---------|-------------|---------------------|----------------------|
| CF01 | `COUNTROWS(fact_customer_feedback)` | Total feedback events | **YES** (total feedback volume) |
| CF02 | `AVERAGE(fact_customer_feedback[SatisfactionScore])` | Average satisfaction score (1–5) | **YES** (avg satisfaction) |
| CF03 | Complaint % (FeedbackType="Complaint") | Complaint percentage | **YES** (complaint rate) |
| CF04 | Active customers (dim_customer IsActive=TRUE) | Active customer count | **YES** (active customers) |
| CF05 | Complaint count (FeedbackType="Complaint") | Complaint count | YES |
| CF06 | Compliment count (FeedbackType="Compliment") | Compliment count | YES |
| CF07 | Claim count (FeedbackType="Claim") | Claim count | YES |
| CF08 | Survey count (FeedbackType="Survey") | Survey count | YES |
| CF09 | `DIVIDE(CF06, CF01)` | Positive feedback rate | YES |
| CF10 | `DIVIDE(CF05 + CF07, CF01)` | Negative feedback rate | YES |
| CF11 | Service recovery rate (of complaints) | Service recovery % | YES |
| CF12 | Resolution rate | Resolution % | YES |
| CF13 | Avg satisfaction where Complaint | Complaint satisfaction avg | YES |
| CF14 | Avg satisfaction where Compliment | Compliment satisfaction avg | YES |

### Booking/revenue measures (RV) — defined in fact_booking_transactions — OD-04 BLOCKED / governance question

| Measure | DAX formula | Business definition | Reusable? |
|---------|-------------|---------------------|-----------|
| RV_BookingCount | `COUNTROWS(fact_booking_transactions)` | Total booking coupons | Questioned (OD-04) |
| RV_DistinctBookings | `DISTINCTCOUNT(BookingReference)` | Distinct booking references | Questioned |
| RV_RevenuePassengers | `CALCULATE(SUM(PassengerCount), IsRevenuePassenger=TRUE())` | Revenue passengers = **8,922** | Questioned (OD-04) |
| RV_NonRevenuePassengers | `CALCULATE(SUM(PassengerCount), IsRevenuePassenger=FALSE())` | Non-revenue = 1,034 | Questioned |
| RV_NetPassengerRevenueUSD | `SUM(NetPassengerRevenueUSD)` | Net passenger revenue USD | Questioned (OD-04) |
| RV_TotalOperatingRevenueUSD | Sum of 3 revenue components | Total operating revenue | Questioned (OD-04) |
| ... (RV_Avg*, RV_RevenueYTD*, NC_*) | ... | ... | Questioned (OD-04) |

### Flight operations measures (FL) — defined in fact_flight_operations

| Measure | Formula | Value | Reusable? |
|---------|---------|-------|-----------|
| FL01 | Flights operated (FlightStatus="Operated") | 4,776 | NO (not customer) |
| FL02 | `SUM(RevenuePassengers)` | 218,413 | NO (flight-level, different population) |
| FL03 | Average departure delay | 43.42 | NO |
| FL04 | Cancellation rate | 4.48% | NO |

### Measures NOT available (blocked / owner-approval required)

- UNDEF-01 Total Revenue, UNDEF-02 Total Operating Costs — BLOCKED (OD-04)
- UNDEF-04 Satisfaction Score Scale Definition — owner approval pending (OD-11). **No approved thresholds for "satisfied" (e.g., 4–5) exist.**

**No existing measure computes:** Total Passengers (as a KPI distinct from revenue passengers), Male/Female passengers, Satisfied passengers count, Neutral/Dissatisfied passengers count, satisfaction by class, travel type by class, or six service ratings.

---

# RELATIONSHIP ANALYSIS

Source: `semantic_model.json` relationships + `RELATIONSHIP_VALIDATION.csv`.

### Active relationships relevant to Page 05

| From | To | Cardinality | Direction | Active | Notes |
|------|----|-------------|-----------|--------|-------|
| fact_customer_feedback.CustomerKey | dim_customer.CustomerKey | 1:* | Single | Yes | 0 orphans in 2,500 rows |
| fact_customer_feedback.AirlineKey | dim_airline.AirlineKey | 1:* | Single | Yes | 0 orphans |
| fact_customer_feedback.RouteKey | dim_route.RouteKey | 1:* | Single | Yes | 0 orphans |
| fact_booking_transactions.CustomerKey | dim_customer.CustomerKey | 1:* | Single | Yes | 0 orphans |
| fact_booking_transactions.AirlineKey | dim_airline.AirlineKey | 1:* | Single | Yes | 0 orphans |
| fact_booking_transactions.RouteKey | dim_route.RouteKey | 1:* | Single | Yes | 0 orphans |
| fact_booking_transactions.FareClassKey | dim_fare_class.FareClassKey | 1:* | Single | Yes (per model.json) | BUT dim_fare_class listed as unused in RELATIONSHIP_VALIDATION |
| fact_booking_transactions.TravelDateKey | dim_date.DateKey | 1:* | Single | Yes | Active travel date |
| fact_booking_transactions.BookingDateKey | dim_date.DateKey | 1:* | Single | Inactive | Role-playing date |

### Inactive relationships (do not filter by default)

| From | To | Role |
|------|----|------|
| fact_customer_feedback.FeedbackDateKey | dim_date.DateKey | INACTIVE |
| fact_customer_feedback.ResolutionDateKey | dim_date.DateKey | INACTIVE |
| fact_booking_transactions.BookingDateKey | dim_date.DateKey | INACTIVE |

### Critical relationship findings for Page 05

1. **fact_customer_feedback has NO active date relationship.** A date slicer on dim_date[FullDate] will NOT filter feedback unless `USERELATIONSHIP(dim_date[DateKey], fact_customer_feedback[FeedbackDateKey])` is used in the measure.

2. **Fact-to-fact relationships are NOT allowed.** `fact_booking_transactions` (passengers) and `fact_customer_feedback` (satisfaction) cannot be directly joined. They share dimensions (dim_customer, dim_airline, dim_route) but at different grains:
   - fact_booking_transactions: 9,956 coupons, grain = one ticket coupon
   - fact_customer_feedback: 2,500 events, grain = one feedback event
   - Only 4,204 of 5,000 customers have bookings; not every passenger gives feedback.
   
   **Implication:** You cannot compute "Satisfied Passengers" by combining booking passenger counts with feedback satisfaction at the passenger level. Satisfaction exists only at the feedback-event grain (2,500 events), not at the passenger grain (9,956 coupons / 218,413 flight passengers).

3. **dim_fare_class, dim_booking_channel, dim_currency have NO FK to any fact** (RELATIONSHIP_VALIDATION rows 23–25). Although model.json lists them as active relationships from fact_booking_transactions, the relationship validation flags them as unused. The class dimension (dim_fare_class[CabinClass]) cannot slice booking facts without a model change.

4. **Only one active relationship allowed between dim_date and any fact table.** Role-playing dates must be inactive.

### Can feedback be analysed alongside bookings?

**Only through shared dimensions (dim_customer, dim_airline, dim_route), not at row level.** This supports:
- Feedback by airline / route / customer segment (via shared dims)
- It does NOT support: satisfaction by fare class (class is on bookings only, satisfaction is on feedback only, no common grain), or "satisfied passengers" (passenger count ≠ feedback event count).

---

# DATA QUALITY FINDINGS

Source: `DATA_QUALITY_AUDIT.csv`, direct data profiling, manifests.

| Issue | Evidence | Impact on Page 05 |
|-------|----------|-------------------|
| SatisfactionScore 603 NULLs (24.1%) | `fact_customer_feedback` data profile; DQ audit | Average satisfaction (CF02) computed on 1,897 non-null scores. Any "satisfied" classification must handle NULLs. |
| ComplaintCategory 1,862 NULLs | `fact_customer_feedback` data profile | Only populated for complaints (638 rows). Cannot use for all-feedback breakdown. |
| PassengerCount always = 1 | `fact_booking_transactions`: 9,956 rows all = 1 | SUM(PassengerCount) = row count = 9,956 coupons, not distinct passengers. |
| 4,204 distinct customers with bookings (of 5,000) | `fact_booking_transactions` profile | 766 customers have no bookings. DISTINCTCOUNT(CustomerKey) ≠ total passengers. |
| dim_fare_class unused (no FK to facts) | RELATIONSHIP_VALIDATION row 23 | Class dimension cannot slice booking facts. |
| dim_customer LoyaltyTier "None" = 686 | Manifest distributions | Treated as valid tier value, not null. |
| fact_flight_operations has 224 nulls on delay/actual timestamps | DQ audit row 13 | Cancelled flights; not relevant to Page 05. |
| dim_airline 3 entirely null columns | DQ audit / GOVERNANCE | AirlineGroup, BusinessModelClass, StatusEffectiveDate all null. Not relevant. |

### Correct passenger counting logic (verified)

Three candidate calculations are **NOT interchangeable**:

| Calculation | Formula | Result | Meaning |
|-------------|---------|--------|---------|
| SUM(PassengerCount) | all coupons | 9,956 | Total ticket coupons (each = 1 passenger) |
| SUM(PassengerCount where IsRevenuePassenger=TRUE) | RV_RevenuePassengers | 8,922 | Revenue-paying passengers only |
| DISTINCTCOUNT(CustomerKey) | distinct customers w/ bookings | 4,204 | Unique customers who booked (not passenger volume) |
| FL02 = SUM(RevenuePassengers) | fact_flight_operations | 218,413 | Flight-level revenue passengers (different population) |

**Recommendation:** For Page 05 "Total Passengers," use `RV_RevenuePassengers` (8,922) if the OD-04 block is cleared, otherwise `SUM(PassengerCount)` (9,956) with explicit label "ticket coupons." Do NOT use DISTINCTCOUNT(CustomerKey) or FL02 for a passenger KPI — they measure different things.

---

# GENDER AVAILABILITY FINDING

**Gender information does NOT genuinely exist anywhere in the AEROVISION 360 semantic model or source data.**

Search performed across:
- All model tables (`semantic_model.json`, `model.json`) — no Gender column in any table
- `dim_customer` manifest — 8 columns: CustomerKey, CustomerID, CustomerSegment, LoyaltyTier, HomeCountry, HomeCountryCode, RegistrationDate, IsActive. **No Gender.**
- `fact_customer_feedback` manifest — 14 columns, no Gender
- `fact_booking_transactions` manifest — 45 columns, no Gender
- All source data files profiled directly (dim_customer, fact_customer_feedback, fact_booking_transactions) — no Gender column
- DAX measures file (`AEROVISION360_Measures.dax`) — no gender measure
- Power Query (`AEROVISION360_DataLoad.m`) — no gender logic
- All project files (grep for "gender|Gender|Male|Female") — zero matches
- `contracts/bi_consumption_model_m311.json` — no gender field

**Recommendation: Remove the Male Passengers and Female Passengers KPIs and any gender breakdown from the Page 05 implementation.** Do NOT infer gender from names, CustomerID, or any indirect attribute. This is a hard, evidence-based exclusion.

---

# REFERENCE DASHBOARD FEASIBILITY MATRIX

Classifications: SUPPORTED = buildable with verified data; PARTIALLY SUPPORTED = buildable with limitations; UNSUPPORTED = required data unavailable; REQUIRES VALIDATION = more investigation needed.

| Reference component | What we need to establish | Finding | Classification |
|---------------------|---------------------------|---------|----------------|
| Total Passengers | Verified passenger-count calculation | RV_RevenuePassengers = 8,922 (OD-04 blocked) OR SUM(PassengerCount) = 9,956 (coupons). Grain ambiguity. | **PARTIALLY SUPPORTED** |
| Male Passengers | Genuine gender field | **No gender field exists anywhere.** | **UNSUPPORTED** |
| Female Passengers | Genuine gender field | **No gender field exists anywhere.** | **UNSUPPORTED** |
| Satisfied Passengers | Valid satisfaction classification | SatisfactionScore exists (1–5, 603 NULLs) but only at feedback-event grain (2,500 events), not passenger grain. No approved "satisfied" threshold (OD-11 pending). Cannot count "satisfied passengers." | **PARTIALLY SUPPORTED** (avg score only; count not valid) |
| Neutral/Dissatisfied | Valid satisfaction classification | Same as above. No threshold definition for neutral/dissatisfied. | **PARTIALLY SUPPORTED** (avg score only) |
| Satisfaction by Class | Class + satisfaction + passenger count | Class (CabinClass) is on dim_fare_class (unused, no FK to facts); satisfaction is on fact_customer_feedback. No common grain; cannot join. | **PARTIALLY SUPPORTED** (class dim exists but unusable; satisfaction exists but separate grain) |
| Travel Type by Class | Travel type + fare class + passenger count | **No TravelType field exists.** CustomerSegment (Business/Leisure/etc.) is a proxy but not travel type. | **UNSUPPORTED** |
| Service Ratings | Genuine service-rating fields | **No six service-rating columns.** Only SatisfactionScore (1–5) + ComplaintCategory. | **UNSUPPORTED** |
| Passenger Class Donut | Fare class + passenger count | CabinClass exists (Economy/Premium Economy/Business/First) but dim_fare_class unused (no FK). "Economy Plus" doesn't exist. | **PARTIALLY SUPPORTED** (class values exist; relationship gap) |
| Passenger Behaviour | Valid connected analytical dimensions | Reference journey: Total → Gender → Customer Type → Travel Type → Satisfaction. Gender and Travel Type don't exist; fact-to-fact join not allowed. | **UNSUPPORTED** (as specified) |

---

# KPI IMPLEMENTATION BLUEPRINT

The reference KPI cards (Total/Male/Female/Satisfied/Neutral-or-Dissatisfied Passengers) cannot be built as specified. Here is the evidence-based alternative using existing, validated measures.

| KPI | Reference name | Verified alternative | Measure | Source | Expected value | Status |
|-----|---------------|---------------------|---------|--------|----------------|--------|
| 1 | Total Passengers | Total Revenue Passengers | RV_RevenuePassengers | fact_booking_transactions[PassengerCount] where IsRevenuePassenger=TRUE | 8,922 | PARTIAL (OD-04 blocked) |
| 1-alt | Total Passengers (all coupons) | SUM(PassengerCount) | New measure required | fact_booking_transactions[PassengerCount] | 9,956 | REQUIRES NEW MEASURE + OD-04 clearance |
| 2 | Male Passengers | — | — | — | — | UNSUPPORTED (no gender) |
| 3 | Female Passengers | — | — | — | — | UNSUPPORTED (no gender) |
| 4 | Satisfied Passengers | Average Satisfaction Score | CF02 | fact_customer_feedback[SatisfactionScore] | 2.99 (avg) | SUPPORTED (avg only, not count) |
| 5 | Neutral/Dissatisfied | Complaint Percentage | CF03 | fact_customer_feedback[FeedbackType]="Complaint" | 25.52% | SUPPORTED (complaint rate proxy) |
| — | — | Total Feedback Events | CF01 | COUNTROWS(fact_customer_feedback) | 2,500 | SUPPORTED |
| — | — | Active Customers | CF04 | dim_customer IsActive=TRUE | 4,808 | SUPPORTED |

**Validation method:** Reconcile CF01=2,500, CF02=2.99, CF03=25.52% against source CSV (already done in DAX_MEASURE_AUDIT.md — all match). RV_RevenuePassengers=8,922 reconciled against SUM(PassengerCount where IsRevenuePassenger=TRUE).

---

# CHART IMPLEMENTATION BLUEPRINT

### C. Passengers Satisfaction by Class & Type (horizontal bar)

**Reference:** Satisfaction categories × passenger class × passenger counts, with travel-type segmentation.

| Element | Finding | Status |
|---------|---------|--------|
| Satisfaction categories | SatisfactionScore 1–5 only (no pre-bucketed categories) | PARTIAL |
| Passenger class | CabinClass in dim_fare_class (Economy/Premium Economy/Business/First) | PARTIAL (dim unused, no FK) |
| Passenger counts | PassengerCount (always 1) on fact_booking_transactions | PARTIAL (OD-04 blocked) |
| Travel-type segmentation | **No TravelType field exists** | UNSUPPORTED |
| Common grain | Class on bookings; satisfaction on feedback; no join | UNSUPPORTED as cross-tab |

**Verdict:** Cannot build satisfaction × class × travel type as specified. Closest supported alternative: **Average Satisfaction Score (CF02) by FeedbackType** or **by Airline** (existing report.json bar charts already do CF02 by AirlineName). A class-based satisfaction view requires resolving the dim_fare_class FK gap AND a fact-to-fact join (not allowed).

### D. Number of Passengers by Travel Type and Class (clustered column)

| Element | Finding | Status |
|---------|---------|--------|
| Business vs Personal travel | **No TravelType field exists** | UNSUPPORTED |
| Passenger class | CabinClass exists | PARTIAL (dim unused) |
| Passenger counts | PassengerCount on fact_booking_transactions | PARTIAL (OD-04 blocked) |

**Verdict:** UNSUPPORTED as specified. No travel type. CustomerSegment (Business/Corporate/Group/Leisure) is the closest proxy but is not travel type and is on dim_customer, not linked to fare class at a common grain.

### E. Passenger Service Ratings (six categories)

| Reference category | Genuine equivalent | Status |
|--------------------|-------------------|--------|
| Arrival Time Convenience | None | UNSUPPORTED |
| Cleanliness | None | UNSUPPORTED |
| Ease of Online Booking | None | UNSUPPORTED |
| Baggage Handling | ComplaintCategory="Baggage" (complaints only) | PARTIAL (complaint subset) |
| In-flight Service | ComplaintCategory="In-Flight Experience" (complaints only) | PARTIAL (complaint subset) |
| Food and Drink | None | UNSUPPORTED |
| Overall | SatisfactionScore (1–5) | SUPPORTED (single score, CF02) |

**Verdict:** The six service ratings **do not exist.** Closest genuine equivalent: single `SatisfactionScore` (CF02, avg 2.99) and `ComplaintCategory` breakdown for complaints only (8 categories: Other, Delay, Seat, Customer Service, Baggage, In-Flight Experience, Cancellation, Boarding). Do not fabricate the six reference categories.

### F. Total Passengers by Class (donut)

| Element | Finding | Status |
|---------|---------|--------|
| Passenger class dimension | CabinClass (Economy/Premium Economy/Business/First) | PARTIAL |
| Passenger count measure | PassengerCount / RV_RevenuePassengers | PARTIAL (OD-04 blocked) |
| Class categories | 4 values (not Business/Economy/Economy Plus) | PARTIAL ("Economy Plus" absent) |
| Relationship | dim_fare_class has no FK to facts | BLOCKS visual |

**Verdict:** PARTIALLY SUPPORTED. Class values exist but dim_fare_class is unused (no FK to fact_booking_transactions). Cannot build donut without model change. "Economy Plus" must be replaced with "Premium Economy."

### G. Passenger Behaviour Analysis (decomposition tree / Sankey)

Reference journey: Total Passengers → Gender → Customer Type → Type of Travel → Satisfaction.

| Dimension | Exists? | Status |
|-----------|---------|--------|
| Total Passengers | Partial (RV_RevenuePassengers, OD-04 blocked) | PARTIAL |
| Gender | **No** | UNSUPPORTED |
| Customer Type | CustomerSegment (Business/Corporate/Group/Leisure) | PARTIAL (proxy) |
| Type of Travel | **No** | UNSUPPORTED |
| Satisfaction | SatisfactionScore (feedback grain only) | PARTIAL (different grain) |
| Connected journey | Fact-to-fact join not allowed | UNSUPPORTED as specified |

**Verdict:** UNSUPPORTED as specified. Gender and Travel Type are absent; the chain cannot be built. Alternative: a decomposition tree using **Total Feedback (CF01) → FeedbackType → ComplaintCategory → ResolutionStatus** (all within fact_customer_feedback, same grain, supported).

---

# SLICER IMPLEMENTATION BLUEPRINT

| Slicer | Table | Column | Type | Active relationship? | Status |
|--------|-------|--------|------|---------------------|--------|
| Airline | dim_airline | AirlineName | Multi-select | Yes (via fact keys) | SUPPORTED |
| Date range | dim_date | FullDate | Date | **No active relationship to fact_customer_feedback** (FeedbackDateKey inactive) | REQUIRES USERELATIONSHIP |
| Customer Segment | dim_customer | CustomerSegment | Multi-select | Yes (via fact_customer_feedback.CustomerKey) | SUPPORTED (proxy for customer type) |
| Loyalty Tier | dim_customer | LoyaltyTier | Multi-select | Yes | SUPPORTED |
| Feedback Type | fact_customer_feedback | FeedbackType | Multi-select | Direct column | SUPPORTED |
| Feedback Channel | fact_customer_feedback | FeedbackChannel | Multi-select | Direct column | SUPPORTED |
| Resolution Status | fact_customer_feedback | ResolutionStatus | Multi-select | Direct column | SUPPORTED |
| Cabin Class | dim_fare_class | CabinClass | Multi-select | **No FK to any fact** | UNSUPPORTED (dim unused) |
| Travel Type | — | — | — | **Field does not exist** | UNSUPPORTED |

**Date slicer limitation:** fact_customer_feedback's date relationships are inactive. To make a date slicer filter feedback visuals, measures must use `USERELATIONSHIP(dim_date[DateKey], fact_customer_feedback[FeedbackDateKey])`. Alternatively, add a separate active date dimension for feedback (model change, out of scope).

---

# DAX IMPLEMENTATION PLAN

## A. Existing measures to reuse (no new DAX needed)

| Measure | Formula | Use in Page 05 |
|---------|---------|----------------|
| CF01 | `COUNTROWS(fact_customer_feedback)` | Total feedback events card |
| CF02 | `AVERAGE(fact_customer_feedback[SatisfactionScore])` | Average satisfaction card |
| CF03 | Complaint % | Complaint rate card |
| CF04 | Active customers count | Active customers card |
| CF05–CF08 | FeedbackType counts | Feedback-type breakdown |
| CF09, CF10 | Positive/Negative feedback rate | Sentiment breakdown |
| CF11 | Service recovery rate | Recovery card |
| CF12 | Resolution rate | Resolution card |
| CF13, CF14 | Avg satisfaction by Complaint/Compliment | Sentiment-satisfaction cards |

All CF measures are verified against source (DAX_MEASURE_AUDIT.md: CF01=2,500; CF02=2.99; CF03=25.52% — all match).

## B. New measures genuinely required

Only if the project decides to proceed despite OD-04 / relationship gaps:

| Measure | Proposed DAX | Required relationships | Status |
|---------|--------------|----------------------|--------|
| Total Passengers (all) | `SUM(fact_booking_transactions[PassengerCount])` | fact_booking_transactions active | OD-04 BLOCKED |
| Total Revenue Passengers | `RV_RevenuePassengers` (already exists) | fact_booking_transactions active | OD-04 BLOCKED |
| Avg Satisfaction by FeedbackType | `CALCULATE(CF02, VALUES(...))` | none (same table) | SUPPORTED |
| Satisfied % (score ≥ 4) | `DIVIDE(COUNTROWS(FILTER(fact_customer_feedback, [SatisfactionScore]>=4)), COUNTROWS(FILTER(fact_customer_feedback, NOT ISBLANK([SatisfactionScore]))))` | none | Requires OD-11 threshold approval (pending) |

**Note:** No new measure can bridge fact_booking_transactions and fact_customer_feedback (fact-to-fact join not allowed). No measure can produce gender or travel type (fields don't exist).

## C. Unsupported calculations that must NOT be implemented

| Calculation | Reason |
|-------------|--------|
| Male Passengers | No gender field (hard exclusion) |
| Female Passengers | No gender field (hard exclusion) |
| Six service ratings (Arrival Time Convenience, Cleanliness, etc.) | Columns don't exist |
| Travel Type by Class | No TravelType field |
| Satisfied Passengers count (passenger grain) | Satisfaction is at feedback-event grain, not passenger grain; fact-to-fact join not allowed |
| Economy Plus class | Value doesn't exist (use Premium Economy instead) |
| dim_fare_class-based visuals | dim_fare_class has no FK to any fact (unused dimension) |

---

# UNSUPPORTED REFERENCE ELEMENTS

1. **Male Passengers KPI** — UNSUPPORTED. No gender field. Remove.
2. **Female Passengers KPI** — UNSUPPORTED. No gender field. Remove.
3. **Travel Type (Business/Personal) slicer & chart** — UNSUPPORTED. No field exists. CustomerSegment is a proxy, not travel type.
4. **Six service ratings** — UNSUPPORTED. Only SatisfactionScore (1–5) + ComplaintCategory exist. Do not fabricate categories.
5. **Economy Plus class** — UNSUPPORTED as a label. Actual values: Economy, Premium Economy, Business, First.
6. **Passenger behaviour decomposition (Gender → Customer Type → Travel Type → Satisfaction)** — UNSUPPORTED as specified. Gender and Travel Type absent; fact-to-fact join not allowed.
7. **"Satisfied Passengers" / "Neutral or Dissatisfied Passengers" counts** — UNSUPPORTED at passenger grain. Only average satisfaction score (CF02) and complaint rate (CF03) are verifiable.

---

# RECOMMENDED ALTERNATIVES

Replace unsupported reference elements with verified equivalents:

| Reference element | Recommended alternative | Basis |
|-------------------|------------------------|-------|
| Male/Female Passengers | **Remove both KPIs.** Replace with Active Customers (CF04=4,808) or Total Feedback (CF01=2,500) | Gender absent; active customers is a genuine customer metric |
| Satisfied/Neutral-Dissatisfied counts | **Average Satisfaction Score (CF02=2.99)** + **Complaint Rate (CF03=25.52%)** | Only verifiable satisfaction metrics |
| Travel Type by Class | **Customer Segment by Cabin Class** — NOT possible (dim_fare_class unused). Alternative: FeedbackType by Airline (existing charts) | No travel type; class dimension unused |
| Six service ratings | **SatisfactionScore distribution (1–5)** + **ComplaintCategory top-8** | Genuine feedback data |
| Behaviour decomposition tree | **CF01 → FeedbackType → ComplaintCategory → ResolutionStatus** (single-table, same grain) | All within fact_customer_feedback |
| Class donut | **Feedback by Airline** (existing bar chart) or wait for dim_fare_class FK fix | dim_fare_class unused |

---

# IMPLEMENTATION SEQUENCE

1. **Confirm scope decision:** Decide whether to build Page 05 using only supported CF measures (the 13 visuals already in report.json) or attempt to add class-based views (requires dim_fare_class relationship fix, out of scope).
2. **Remove unsupported elements:** Exclude Male/Female KPIs, Travel Type slicers/charts, six service ratings, Economy Plus, and the Gender-led decomposition tree.
3. **Build supported KPI cards:** CF01 (Total Feedback), CF02 (Avg Satisfaction), CF03 (Complaint %), CF04 (Active Customers). Validate: 2,500 / 2.99 / 25.52% / 4,808.
4. **Build supported charts:** Use existing report.json Page 05 visuals — CF01 by AirlineName, CF01 by FeedbackChannel, CF02 by AirlineName, CF01 by FeedbackType, CF01 by ResolutionStatus.
5. **Add slicers:** Airline (dim_airline), Customer Segment (dim_customer), Feedback Type, Feedback Channel, Resolution Status. Note date slicer requires USERELATIONSHIP for feedback.
6. **Apply disclosure:** "Synthetic Simulation — Not Actual Airline Performance" on the page.
7. **Validate:** Reconcile all card values against source CSV (already verified in DAX_MEASURE_AUDIT.md).
8. **Document gaps:** Record OD-04 block on fact_booking_transactions, dim_fare_class unused, inactive feedback date relationship as known limitations.

---

# OUTSTANDING QUESTIONS AND DEPENDENCIES

1. **OD-04 status unresolved:** FactBookingTransactions is blocked. Is RV_RevenuePassengers (8,922) permissible for Page 05? Governance doc says "no financial revenue or operating cost measures defined in DAX" yet RV_* measures exist in the DAX file. This contradiction must be resolved before using any booking-based passenger measure.
2. **dim_fare_class relationship:** dim_fare_class has no FK to any fact. To build class-based visuals, a relationship must be added (model change) — but this is outside the investigation scope and may violate the "do not modify the semantic model" rule.
3. **fact_customer_feedback date relationship:** Both FeedbackDateKey and ResolutionDateKey are inactive. A date slicer won't filter feedback without USERELATIONSHIP or a model change.
4. **OD-11 satisfaction scale:** No approved thresholds for "satisfied" (4–5) vs neutral/dissatisfied. Owner approval pending. Cannot build satisfied/dissatisfied counts without this decision.
5. **Reference dashboard image:** No reference image file exists in the project (searched all image formats — none found). The visual structure described in the prompt could not be compared against an actual image.
6. **Page 05 already exists:** report.json already defines Page 05 "Customer & Service Intelligence" with 13 CF-based visuals. Decision needed: rebuild to match reference (partially impossible) or refine the existing page with supported measures only.

---

# FINAL VERDICT

**RED — IMPLEMENTATION NOT POSSIBLE AS SPECIFIED.**

The reference dashboard requires data elements that are genuinely absent from AEROVISION 360:
- Gender (Male/Female KPIs) — absent
- Travel Type — absent
- Six service-rating categories — absent (only one SatisfactionScore)
- Economy Plus class — absent
- Fact-to-fact join (bookings + feedback) — not allowed
- dim_fare_class relationship to facts — absent (unused dimension)
- OD-04 clearance for fact_booking_transactions — unresolved

**Supported:** CF01–CF14 measures (feedback counts, avg satisfaction 2.99, complaint rate 25.52%, active customers 4,808, resolution/service-recovery rates) and the 13 existing Page 05 visuals in report.json.

**Recommended action:** Build Page 05 using only the supported CF-based visuals and KPIs, remove all gender/travel-type/six-rating/Economy-Plus elements, and document the six unsupported reference components as known gaps requiring either source-data enhancement or governance decisions (OD-04, OD-11) before they can be implemented.

---

**Report generated:** 2026-11-08  
**Evidence sources:** `deliverables/power_bi/semantic_model/semantic_model.json`, `model.json`, `dax/AEROVISION360_Measures.dax`, `report/report.json`, `contracts/bi_consumption_model_m311.json`, `data/manifests/*_manifest.json`, `data/03_curated/*.parquet` (profiled directly), `deliverables/power_bi/audit/*` (DAX audit, data quality, relationship validation, governance compliance, remediation plan, complete audit).  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance. No source data, model, report, or DAX was modified during this investigation.
