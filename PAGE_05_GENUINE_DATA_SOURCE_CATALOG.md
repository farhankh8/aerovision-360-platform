# AEROVISION 360 — Page 05 Genuine Data Source Catalog

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Catalog Date:** 2026-11-08  
**Status:** SOURCE CATALOG COMPLETE — READ-ONLY INVESTIGATION  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Catalog Purpose

This document catalogs all genuine data sources that could potentially supply the missing fields required for Page 05 (Customer & Service Intelligence). Each source is evaluated for actual accessibility, schema verification, licensing, and compatibility with AEROVISION 360.

**Missing fields to source:** Gender, Travel Type / Type of Travel, six service-rating categories, Economy Plus cabin class, satisfaction threshold definition, passenger-level identifiers.

---

## 2. Internal AEROVISION 360 Sources (Already in Project)

### 2.1 FactCustomerFeedback — Primary Page 05 Source

| Attribute | Value |
|-----------|-------|
| Location | `data/03_curated/fact_customer_feedback.parquet` (also `.csv`) |
| Rows | 2,500 |
| Grain | One row per customer feedback event |
| Fields available | FeedbackKey, FeedbackID, CustomerKey, AirlineKey, FlightOperationKey, RouteKey, FeedbackDateKey, FeedbackType, SatisfactionScore, ComplaintCategory, ServiceRecoveryFlag, ResolutionStatus, ResolutionDateKey, FeedbackChannel |
| Fields missing | Gender, TravelType, service ratings beyond SatisfactionScore |
| License | Internal — synthetic simulation |
| Accessibility | Directly accessible — already in project |
| Verification | Row count, schema, nulls, duplicates all verified |
| Compatibility | Native — already in semantic model |
| Page 05 use | PRIMARY — CF01 through CF14 measures |

### 2.2 DimCustomer — Customer Dimension

| Attribute | Value |
|-----------|-------|
| Location | `data/03_curated/dim_customer.parquet` (also `.csv`) |
| Rows | 5,000 |
| Grain | One row per fictional customer |
| Fields available | CustomerKey, CustomerID, CustomerSegment, LoyaltyTier, HomeCountry, HomeCountryCode, RegistrationDate, IsActive |
| Fields missing | Gender, Customer Type (Loyal/Disloyal), personal identifiers |
| License | Internal — synthetic simulation |
| Accessibility | Directly accessible — already in project |
| Verification | Row count, schema, nulls, duplicates all verified |
| Compatibility | Native — already in semantic model |
| Page 05 use | CustomerSegment as proxy for customer type; LoyaltyTier, HomeCountry for filtering |

### 2.3 DimFareClass — Cabin Class Dimension

| Attribute | Value |
|-----------|-------|
| Location | `data/03_curated/dim_fare_class.parquet` (also `.csv`) |
| Rows | 8 |
| Grain | One row per fare class |
| Fields available | FareClassKey, FareClassCode, FareClassName, CabinClass, RefundabilityCategory, IsAncillaryEligible, DisplayOrder |
| Fields missing | Economy Plus value (actual: Economy, Premium Economy, Business, First) |
| License | Internal — synthetic simulation |
| Accessibility | Directly accessible — already in project |
| Verification | Row count, schema, nulls, duplicates all verified |
| Compatibility | EXISTS but UNUSED — no FK to any fact table |
| Page 05 use | Cannot be used without adding FK relationship to FactBookingTransactions |

### 2.4 FactBookingTransactions — Booking Data (OD-04 Blocked)

| Attribute | Value |
|-----------|-------|
| Location | `data/03_curated/fact_booking_transactions.parquet` (also `.csv`) |
| Rows | 9,956 |
| Grain | One row per ticket coupon |
| Fields available | 45 columns including PassengerCount (always 1), IsRevenuePassenger, FareClassKey, TransactionStatus, IsRefunded |
| Fields missing | TravelType, Gender |
| License | Internal — synthetic simulation but OD-04 BLOCKED |
| Accessibility | File accessible but governance-blocked |
| Verification | Row count, schema, nulls, duplicates all verified |
| Compatibility | Blocked per OD-04 exchange-rate policy |
| Page 05 use | Blocked — cannot use without OD-04 resolution |

### 2.5 FactFlightOperations — Flight-Level Passenger Data

| Attribute | Value |
|-----------|-------|
| Location | `data/03_curated/fact_flight_operations.parquet` (also `.csv`) |
| Rows | 5,000 |
| Grain | One row per flight operation leg |
| Fields available | RevenuePassengers (SUM = 218,413), BookedPassengers, NonRevenuePassengers, AvailableSeats |
| Fields missing | Gender, TravelType, passenger-level identifiers |
| License | Internal — synthetic simulation |
| Accessibility | Directly accessible — already in project |
| Verification | Row count, schema, nulls, duplicates all verified |
| Compatibility | Native — FL02 measure verified |
| Page 05 use | PARTIAL — RevenuePassengers is flight-level, different population from booking-level 8,922 |

---

## 3. External Candidate Sources Evaluated

### 3.1 Maven Analytics Airline Passenger Satisfaction Dataset

| Attribute | Value |
|-----------|-------|
| Source name | Airline Passenger Satisfaction |
| Primary URL | https://mavenanalytics.io/data-playground/airline-passenger-satisfaction |
| Original source | John D (via Kaggle), modified/cleaned by teejmahal20 |
| Kaggle URL | https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction |
| Format | CSV, Single table |
| Stated record count | 499 (Maven structured listing) vs 120,000+ (Maven description) — DISCREPANCY |
| Stated field count | 25 fields |
| License (Maven) | "Public Domain" |
| License (Kaggle) | "Other (specified in description)" — CONFLICT |
| Download access | Requires sign-up/login on both Maven and Kaggle |
| Direct file inspection | NOT POSSIBLE — credentials required |
| Verification status | UNVERIFIED — schema known from public docs but raw file not inspectable |

#### 3.1.1 Schema (from public documentation)

| Column | Type | Values | Nulls |
|--------|------|--------|-------|
| id | int64 | 0 to ~130,000 | No |
| Gender | string | Female, Male | No |
| Customer Type | string | Loyal Customer, disloyal Customer | No |
| Age | int64 | 7 to 85 | No |
| Type of Travel | string | Personal Travel, Business Travel | No |
| Class | string | Business, Eco, Eco Plus | No |
| Flight Distance | int64 | 31 to 4,983 | No |
| Inflight wifi service | int64 | 0 (N/A), 1-5 | No |
| Departure/Arrival time convenient | int64 | 0-5 | No |
| Ease of Online booking | int64 | 0-5 | No |
| Gate location | int64 | 0-5 | No |
| Food and drink | int64 | 0-5 | No |
| Online boarding | int64 | 0-5 | No |
| Seat comfort | int64 | 0-5 | No |
| Inflight entertainment | int64 | 0-5 | No |
| On-board service | int64 | 0-5 | No |
| Leg room service | int64 | 0-5 | No |
| Baggage handling | int64 | 1-5 | No |
| Checkin service | int64 | 0-5 | No |
| Inflight service | int64 | 0-5 | No |
| Cleanliness | int64 | 0-5 | No |
| Departure Delay in Minutes | int64 | 0 to ~1,590 | No |
| Arrival Delay in Minutes | float64 | 0 to ~1,580 | Yes |
| satisfaction | string | satisfied, neutral or dissatisfied | No |

#### 3.1.2 Fields That Match Page 05 Requirements

| Reference Field | Maven/Kaggle Column | Match Quality |
|-----------------|---------------------|---------------|
| Gender | Gender | EXACT — Female/Male |
| Customer Type | Customer Type | EXACT — Loyal Customer/disloyal Customer |
| Type of Travel | Type of Travel | EXACT — Personal Travel/Business Travel |
| Class | Class | PARTIAL — Business/Eco/Eco Plus (vs AEROVISION's Economy/Premium Economy/Business/First) |
| Satisfaction | satisfaction | PARTIAL — categorical (satisfied/neutral or dissatisfied) vs AEROVISION's 1-5 numeric |
| Arrival/Departure Time Convenience | Departure/Arrival time convenient | EXACT — 0-5 scale |
| Cleanliness | Cleanliness | EXACT — 0-5 scale |
| Ease of Online Booking | Ease of Online booking | EXACT — 0-5 scale |
| Baggage Handling | Baggage handling | EXACT — 0-5 scale |
| In-flight Service | Inflight service | EXACT — 0-5 scale |
| Food and Drink | Food and drink | EXACT — 0-5 scale |

#### 3.1.3 Compatibility Assessment

| Compatibility Factor | Assessment |
|---------------------|------------|
| Population match | NO — AEROVISION is synthetic (5,000 customers); Maven is real US airline survey (~130,000 passengers) |
| Common join key | NO — CustomerKey vs id; no shared business key |
| Grain compatibility | NO — feedback events vs survey responses vs booking coupons |
| License clarity | NO — Maven "Public Domain" vs Kaggle "Other" — conflict unresolved |
| Download accessibility | NO — both require login |
| Schema verification | PARTIAL — columns known from docs but raw file not inspectable |
| Record count verification | NO — 499 vs 120,000+ discrepancy |

**Verdict:** Contains all missing fields but CANNOT be integrated with AEROVISION 360 due to population mismatch, no common key, license conflict, and access restrictions.

---

### 3.2 Hugging Face Mirror

| Attribute | Value |
|-----------|-------|
| Source name | airline_satisfaction |
| URL | https://huggingface.co/datasets/thomask1018/airline_satisfaction |
| Format | Parquet/CSV (mirror of Kaggle dataset) |
| Record count | ~130,000 rows |
| Accessibility | Publicly viewable (sample rows), download may be possible |
| License | Inherited from Kaggle — "Other" |
| Verification status | PARTIAL — sample rows visible but full file not independently inspected |

**Verdict:** Same dataset as Maven/Kaggle with same compatibility issues. Public mirror does not resolve license or population mismatch problems.

---

### 3.3 Other Public Airline Datasets Considered

| Source | Status | Reason Not Pursued |
|--------|--------|-------------------|
| US Bureau of Transportation Statistics (BTS) | Not investigated | No passenger satisfaction survey data; focuses on operational statistics |
| IATA passenger surveys | Not investigated | Proprietary, not publicly downloadable |
| Airline Customer Satisfaction Index (ACSI) | Not investigated | Proprietary, requires license |
| Skytrax airline ratings | Not investigated | Aggregated ratings, not passenger-level data |
| Kaggle airline datasets (other) | Not investigated | Would face same license/population compatibility issues |

---

## 4. Source Evaluation Matrix

| Source | Missing Fields Supplied | Downloadable? | Schema Verified? | License Clear? | Population Compatible? | Join Key Compatible? | Overall Verdict |
|--------|------------------------|---------------|------------------|----------------|------------------------|---------------------|-----------------|
| FactCustomerFeedback (internal) | None missing (already has what exists) | Yes | Yes | Internal | N/A (native) | N/A (native) | USE — PRIMARY |
| DimCustomer (internal) | None | Yes | Yes | Internal | N/A | N/A | USE — SECONDARY |
| DimFareClass (internal) | CabinClass values (no Economy Plus) | Yes | Yes | Internal | N/A | N/A | PARTIAL — needs FK |
| FactBookingTransactions (internal) | None (blocked by OD-04) | Yes | Yes | Internal | N/A | N/A | BLOCKED |
| Maven/Kaggle dataset | Gender, TravelType, 6 service ratings, Class, Satisfaction categorical | NO (login required) | PARTIAL (docs only) | NO (conflict) | NO | NO | REJECT — cannot integrate |
| Hugging Face mirror | Same as Maven/Kaggle | PARTIAL | PARTIAL | NO | NO | NO | REJECT — cannot integrate |
| Other public sources | Not investigated | — | — | — | — | — | NOT IN CATALOG |

---

## 5. Genuine Source Recommendations

### 5.1 Sources to USE (Native AEROVISION 360)

| Source | Fields Supplied | Page 05 Components Supported |
|--------|----------------|------------------------------|
| FactCustomerFeedback | SatisfactionScore, FeedbackType, ComplaintCategory, ServiceRecoveryFlag, ResolutionStatus, FeedbackChannel | CF01-CF14, all feedback-based visuals |
| DimCustomer | CustomerSegment, LoyaltyTier, HomeCountry, IsActive | Customer segmentation proxies |
| DimAirline | AirlineName | Airline filtering |
| DimDate | FullDate, IsReportingPeriod | Period filtering (with USERELATIONSHIP for feedback) |
| DimRoute | RouteCode, RouteRegion | Route filtering |
| DimFareClass | CabinClass (Economy/Premium Economy/Business/First) | Class values exist but need FK relationship |

### 5.2 Sources to REJECT

| Source | Reason |
|--------|--------|
| Maven/Kaggle Airline Passenger Satisfaction | Population mismatch, no common key, license conflict, access blocked, record count discrepancy |
| Hugging Face mirror | Same issues as Maven/Kaggle |
| Any external passenger dataset | Would violate rule against merging unrelated passengers with AEROVISION customers |

### 5.3 Sources Requiring Governance Decision Before Use

| Source | Decision Needed | Why |
|--------|----------------|-----|
| FactBookingTransactions | OD-04 resolution | Exchange-rate policy unresolved; passenger/revenue measures blocked |
| Satisfaction threshold (Satisfied/Dissatisfied) | OD-11 approval | No approved definition of what score constitutes "satisfied" |
| dim_fare_class relationship | Model change approval | FK from FactBookingTransactions to DimFareClass must be added |
| FactFlightOperations RevenuePassengers | None (already available) | FL02 = 218,413 but different population from booking-level 8,922 |

---

## 6. Data Gap Summary

| Missing Field | Internal Source Available? | External Source Available? | Integration Feasible? | Required Action |
|---------------|---------------------------|---------------------------|----------------------|-----------------|
| Gender | NO | YES (Maven/Kaggle) | NO (population mismatch, no common key) | Document as unsupported; do not build Male/Female KPIs |
| TravelType | NO | YES (Maven/Kaggle) | NO (same reasons) | Document as unsupported; do not build Travel Type slicer/charts |
| Six service ratings | NO | YES (Maven/Kaggle) | NO (same reasons) | Document as unsupported; use SatisfactionScore + ComplaintCategory instead |
| Economy Plus | NO | YES (Maven/Kaggle "Eco Plus") | NO (different taxonomy) | Use Premium Economy as closest equivalent; document difference |
| Satisfaction threshold | NO | YES (Maven/Kaggle categorical) | NO (different scale) | Wait for OD-11 approval; use CF02 average score |
| Passenger-level ID | NO | NO | N/A | Document grain limitation; distinguish passengers from feedback events |

---

## 7. Conclusion

**No genuine external data source can be responsibly integrated with AEROVISION 360 for Page 05.** The Maven/Kaggle dataset contains all missing fields but cannot be integrated due to:

1. **Population mismatch** — Synthetic AEROVISION customers vs real US airline survey passengers
2. **No common join key** — Impossible to relate records at any grain
3. **License conflict** — Maven "Public Domain" vs Kaggle "Other" — reuse terms unverified
4. **Access restrictions** — Both platforms require login; raw file not inspectable
5. **Record count discrepancy** — 499 vs 120,000+ unresolved

**Recommended approach:** Build Page 05 using only verified AEROVISION 360 native data (CF01-CF14 measures from FactCustomerFeedback, DimCustomer segmentation, DimAirline, DimDate, DimRoute). Document all reference components requiring missing fields as known limitations requiring either new source data acquisition with separate governance approval or explicit scope reduction.
