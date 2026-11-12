# AEROVISION 360 — Page 05 Project Discovery

**Project:** AEROVISION 360 — Airline Intelligence Platform  
**Target Page:** Page 05 — Customer & Service Intelligence (subtitle: Passenger Satisfaction Review)  
**Discovery Date:** 2026-11-08  
**Status:** READ-ONLY DISCOVERY — NO MODIFICATIONS MADE  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Project Structure Inventory

Inspected the complete `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360\` project directory.

### Key folders

| Folder | Purpose |
|--------|---------|
| `data/03_curated/` | Curated source datasets (CSV + Parquet) — 14 datasets |
| `data/04_reference/` | Reference files (airline workbook, exchange rates, route keymap) |
| `data/manifests/` | JSON manifests for every dataset (schemas, row counts, validation) |
| `deliverables/power_bi/` | Power BI project files (report, semantic model, DAX, Power Query, theme) |
| `deliverables/power_bi/report/report.json` | Report page definitions including Page 05 |
| `deliverables/power_bi/semantic_model/semantic_model.json` | Table/column/relationship metadata |
| `deliverables/power_bi/semantic_model/model.json` | Measure expressions (partial, contains errors per audit) |
| `deliverables/power_bi/dax/AEROVISION360_Measures.dax` | Authoritative DAX measure definitions |
| `deliverables/power_bi/power_query/AEROVISION360_DataLoad.m` | Power Query M (incomplete — defines only 2 of 14 tables) |
| `deliverables/power_bi/audit/` | Audit reports (data quality, DAX audit, relationship validation, governance) |
| `contracts/bi_consumption_model_m311.json` | BI consumption model contract |
| `m311_governed_measures.py` | Governed measure definitions (Python) |

### Power BI file status

| File | Status |
|------|--------|
| `deliverables/power_bi/AEROVISION_360.pbix` | Exists (1,003,650 bytes) but report internally has one blank page only; custom JSON specs not loaded |
| `deliverables/power_bi/AEROVISION_360.pbip` | Import-ready project file |
| `deliverables/power_bi/report/report.json` | Contains 5 pages including Page 05 "Customer & Service Intelligence" with 13 visuals |

No modifications were made to any project file during this discovery.

---

## 2. Dataset Inventory

All datasets inspected from `data/03_curated/` (curated layer) and their manifests.

### Dimensions (11)

| # | Dataset | Rows | Columns | PK | Business Purpose | Suitable for Page 05? |
|---|---------|------|---------|----|------------------|----------------------|
| 1 | dim_customer | 5,000 | 8 | CustomerKey | Customer master data | YES — partial (CustomerSegment, LoyaltyTier, HomeCountry; NO Gender) |
| 2 | dim_airline | 10 | 12 | AirlineKey | Airline master data | YES — AirlineName for slicers/legends |
| 3 | dim_airport | 72 | 11 | AirportKey | Airport master data | NO — not customer-facing |
| 4 | dim_route | 320 | 9 | RouteKey | Route master data | YES — RouteCode for slicers |
| 5 | dim_date | 761 | 19 | DateKey | Calendar date dimension | YES — date filtering (feedback dates need USERELATIONSHIP) |
| 6 | dim_aircraft | 440 | 9 | AircraftKey | Aircraft master data | NO — not customer-facing |
| 7 | dim_aircraft_type | 12 | 8 | AircraftTypeKey | Aircraft type classification | NO — not customer-facing |
| 8 | dim_disruption_type | 9 | 7 | DisruptionTypeKey | Disruption classification | NO — not customer-facing |
| 9 | dim_fare_class | 8 | 7 | FareClassKey | Fare/cabin class taxonomy | PARTIAL — CabinClass exists but NO FK to any fact (unused dimension) |
| 10 | dim_booking_channel | 7 | 6 | BookingChannelKey | Booking channel taxonomy | UNUSED — NO FK to any fact |
| 11 | dim_currency | 8 | 6 | CurrencyKey | Currency master data | BLOCKED / UNUSED — OD-04, NO FK to any fact |

### Facts (3)

| # | Dataset | Rows | Grain | PK | Business Purpose | Suitable for Page 05? |
|---|---------|------|-------|----|------------------|----------------------|
| 1 | fact_booking_transactions | 9,956 | One row per passenger ticket coupon | BookingTransactionKey | Booking/coupon transactions | BLOCKED — OD-04 exchange-rate policy (unresolved) |
| 2 | fact_customer_feedback | 2,500 | One row per feedback event | FeedbackKey | Customer feedback events | YES — primary source for Page 05 |
| 3 | fact_flight_operations | 5,000 | One row per flight operation leg | FlightOperationKey | Flight operations | PARTIAL — RevenuePassengers (FL02) but flight-level, not booking-level |

### Other facts (not customer-relevant)

| Dataset | Rows | Grain | Page 05 Relevant? |
|---------|------|-------|-------------------|
| fact_disruptions | 1,754 | One row per disruption event | NO |
| fact_operating_costs | — | One row per cost ledger line | NO (OD-04 blocked) |

### Data quality summary (from DATA_QUALITY_AUDIT.csv)

| Dataset | Row Count | Null Columns | Duplicate Rows | PK Unique? | Status |
|---------|-----------|-------------|---------------|------------|--------|
| dim_customer | 5,000 | 0 | 0 | Yes | PASS |
| fact_customer_feedback | 2,500 | SatisfactionScore=603, ComplaintCategory=1,862, ResolutionDateKey=1,896 | 0 | Yes | PASS |
| fact_booking_transactions | 9,956 | 0 (PassengerCount) | 0 | Yes | PASS |
| dim_fare_class | 8 | 0 | 0 | Yes | PASS |
| dim_date | 761 | 0 | 0 | Yes | PASS |
| dim_airline | 10 | 3 entirely null columns | 0 | Yes | PASS |

---

## 3. Column-Level Investigation

### dim_customer (5,000 rows, PK CustomerKey, no nulls)

| Column | Type | Business Meaning | Example Values | Distinct | Null | Key | Filter? | Aggregate? | Analytical Dimension? |
|--------|------|-----------------|----------------|----------|------|-----|---------|------------|----------------------|
| CustomerKey | int32 | Surrogate PK | 1–5000 | 5,000 | 0 | PK | Yes | No | No |
| CustomerID | string | Synthetic business key | CUST-... | 5,000 | 0 | BK | Yes | No | No |
| CustomerSegment | string | Customer segment | Leisure, Business, Corporate, Group | 4 | 0 | No | Yes | No | YES |
| LoyaltyTier | string | Loyalty tier | Silver, Gold, Platinum, None | 4 | 0* | No | Yes | No | YES |
| HomeCountry | string | Customer home country | 8 countries | 8 | 0 | No | Yes | No | YES |
| HomeCountryCode | string | Country code | IN, AE, GB, SG, US, QA, DE, AU | 8 | 0 | No | Yes | No | YES |
| RegistrationDate | date | Customer registration date | 2024-10-01 to 2025-09-30 | 366 | 0 | No | Yes | No | YES |
| IsActive | boolean | Is customer active | True, False | 2 | 0 | No | Yes | No | YES |
| **Gender** | — | **DOES NOT EXIST** | — | — | — | — | — | — | — |

*Direct data profile shows 0 nulls; DQ audit CSV lists LoyaltyTier=686 nulls but value "None"=686 exists. Treated as 0 nulls per manifest `"no_null_values": true`.

**Gender availability:** `dim_customer[Gender]` does NOT exist anywhere in the project. Confirmed via manifest, direct data profile, model.json, semantic_model.json, DAX file, Power Query, and full-project grep (zero matches).

### fact_customer_feedback (2,500 rows, PK FeedbackKey, grain = one feedback event)

| Column | Type | Business Meaning | Example Values | Distinct | Null | Key | Filter? | Aggregate? | Analytical Dimension? |
|--------|------|-----------------|----------------|----------|------|-----|---------|------------|----------------------|
| FeedbackKey | int64 | Surrogate PK | — | 2,500 | 0 | PK | Yes | No | No |
| FeedbackID | string | Business key | — | 2,500 | 0 | BK | Yes | No | No |
| CustomerKey | int32 | FK → dim_customer | — | 2,500 | 0 | FK | Yes | No | Yes (join) |
| AirlineKey | int32 | FK → dim_airline | 10 airlines | 10 | 0 | FK | Yes | No | Yes (join) |
| FlightOperationKey | int64 | FK → fact_flight_operations (degenerate ref, no relationship) | — | — | 0 | FK | No | No | No |
| RouteKey | int32 | FK → dim_route | — | — | 0 | FK | Yes | No | Yes (join) |
| FeedbackDateKey | int32 | FK → dim_date (INACTIVE relationship) | — | — | 0 | FK | Yes* | No | Yes (join) |
| FeedbackType | string | Type of feedback | Survey, Complaint, Claim, Compliment | 4 | 0 | No | Yes | No | YES |
| SatisfactionScore | int8 | Satisfaction score 1–5 | 1, 2, 3, 4, 5 | 5 | 603 | No | Yes (AVG) | No | YES |
| ComplaintCategory | string | Complaint category (complaints only) | Other, Delay, Seat, Customer Service, Baggage, In-Flight Experience, Cancellation, Boarding | 8 | 1,862 | No | Yes | No | YES |
| ServiceRecoveryFlag | boolean | Service recovery applied | True, False | 2 | 0 | No | Yes | No | YES |
| ResolutionStatus | string | Resolution status | Open, Closed - No Action, In Progress, Resolved | 4 | 0 | No | Yes | No | YES |
| ResolutionDateKey | int32 | FK → dim_date (INACTIVE) | — | — | 1,896 | FK | No | No | No |
| FeedbackChannel | string | Feedback channel | Email, Call Center, Social, Web, Mobile, Airport | 6 | 0 | No | Yes | No | YES |

*FeedbackDateKey relationship is inactive — requires USERELATIONSHIP in DAX to filter by date.

**Six service-rating columns:** Do NOT exist. Only one `SatisfactionScore` (1–5) column exists. No per-category ratings (Arrival Time Convenience, Cleanliness, Ease of Online Booking, Baggage Handling, In-flight Service, Food and Drink) are present.

### fact_booking_transactions (9,956 rows, PK BookingTransactionKey, grain = one passenger ticket coupon) — OD-04 BLOCKED

| Column | Type | Business Meaning | Example Values | Distinct | Null | Key | Filter? | Aggregate? | Analytical Dimension? |
|--------|------|-----------------|----------------|----------|------|-----|---------|------------|----------------------|
| BookingTransactionKey | int64 | Surrogate PK | — | 9,956 | 0 | PK | Yes | No | No |
| BookingReference | string | Business key | — | 9,956 | 0 | BK | Yes | No | No |
| CustomerKey | int32 | FK → dim_customer | 4,204 distinct customers | 4,204 | 0 | FK | Yes | No | Yes (join) |
| AirlineKey | int32 | FK → dim_airline | — | — | 0 | FK | Yes | No | Yes (join) |
| FlightOperationKey | int64 | FK → fact_flight_operations (degenerate ref) | — | — | 0 | FK | No | No | No |
| RouteKey | int32 | FK → dim_route | — | — | 0 | FK | Yes | No | Yes (join) |
| FareClassKey | int32 | FK → dim_fare_class | 1–8 | 8 | 0 | FK | Yes | No | Yes (join) |
| BookingChannelKey | int32 | FK → dim_booking_channel | — | — | 0 | FK | Yes | No | Yes (join) |
| BookingDateKey | int32 | FK → dim_date (INACTIVE) | — | — | 0 | FK | Yes* | No | Yes (join) |
| TravelDateKey | int32 | FK → dim_date (ACTIVE) | — | — | 0 | FK | Yes | No | Yes (join) |
| PassengerCount | int8 | Passengers per coupon | **Always 1** | 1 | 0 | No | Yes (SUM) | No | NO |
| IsRevenuePassenger | boolean | Revenue vs non-revenue | True (8,922), False (1,034) | 2 | 0 | No | Yes | No | YES |
| IsRefunded | boolean | Is refunded | False (9,457), True (499) | 2 | 0 | No | Yes | No | YES |
| TransactionStatus | string | Transaction status | Flown, Ticketed, Booked, Cancelled, Refunded, NoShow | 6 | 0 | No | Yes | No | YES |
| NetPassengerRevenueUSD | decimal | Net passenger revenue USD | — | — | 0 | No | Yes (SUM) | No | NO |
| **TravelType** | — | **DOES NOT EXIST** | — | — | — | — | — | — | — |
| **Gender** | — | **DOES NOT EXIST** | — | — | — | — | — | — | — |

**OD-04 status:** FactBookingTransactions is blocked per exchange-rate policy (unresolved). Passenger-count measures (RV_*) exist in DAX but are under governance question.

### dim_fare_class (8 rows, PK FareClassKey, NO FK to any fact — UNUSED)

| Column | Type | Values |
|--------|------|--------|
| FareClassKey | int32 | 1–8 |
| FareClassCode | string | Y, M, B, W, E, J, C, F |
| FareClassName | string | Economy Flexible, Economy Standard, Economy Basic, Premium Economy Flexible, Premium Economy Standard, Business Flexible, Business Standard, First Flexible |
| CabinClass | string | Economy (3), Premium Economy (2), Business (2), First (1) |
| RefundabilityCategory | string | Refundable, Partially Refundable, Non-Refundable |
| IsAncillaryEligible | boolean | True (all) |
| DisplayOrder | int | 1, 2 |

**CabinClass values:** Economy, Premium Economy, Business, First. **"Economy Plus" does NOT exist.** Closest is Premium Economy.

**Critical limitation:** dim_fare_class has NO foreign key relationship to any fact table. It cannot slice fact_booking_transactions or fact_customer_feedback without a model change (out of scope for this discovery).

### dim_airline (10 rows), dim_date (761 rows), dim_route (320 rows)

| Dataset | Key Columns | Page 05 Use |
|---------|-------------|-------------|
| dim_airline | AirlineKey, AirlineName (10 airlines) | Airline slicer/legend |
| dim_date | DateKey, FullDate (2024-10-01 to 2026-10-31), IsReportingPeriod | Date slicer; reporting period 2025-10-01 to 2026-09-30 |
| dim_route | RouteKey, RouteCode, RouteRegion, IsInternational | Route slicer |

---

## 4. Data Lineage

### CF measures lineage (VERIFIED)

```
Source: data/03_curated/fact_customer_feedback.csv/.parquet
  → Power Query: AEROVISION360_DataLoad.m (incomplete — only 2 of 14 tables defined)
  → Semantic model: fact_customer_feedback table
  → DAX measures: CF01–CF14 (in dax/AEROVISION360_Measures.dax)
  → Power BI visual: Page 05 cards and bar charts (in report.json)
```

### RV measures lineage (OD-04 BLOCKED)

```
Source: data/03_curated/fact_booking_transactions.csv/.parquet
  → Semantic model: fact_booking_transactions table
  → DAX measures: RV_BookingCount, RV_DistinctBookings, RV_RevenuePassengers, etc.
  → Governance: OD-04 blocked (exchange-rate policy unresolved)
  → Page 05: NOT recommended until OD-04 resolved
```

### Critical lineage gaps

1. **No lineage between fact_booking_transactions and fact_customer_feedback** — fact-to-fact joins not allowed. They share dimension tables (dim_customer, dim_airline, dim_route) but at different grains.
2. **dim_fare_class has no FK to any fact** — CabinClass cannot slice booking or feedback data.
3. **fact_customer_feedback date relationships inactive** — FeedbackDateKey and ResolutionDateKey both inactive; date filtering requires USERELATIONSHIP.
4. **No Gender or TravelType columns exist anywhere** — cannot trace to any source.

---

## 5. Semantic Model Investigation

### Relationships (from semantic_model.json and RELATIONSHIP_VALIDATION.csv)

#### Active relationships relevant to Page 05

| From Table | From Column | To Table | To Column | Cardinality | Direction | Active | Validation |
|------------|-------------|----------|-----------|-------------|-----------|--------|------------|
| fact_customer_feedback | CustomerKey | dim_customer | CustomerKey | 1:* | Single | Yes | 0 orphans in 2,500 rows |
| fact_customer_feedback | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Yes | 0 orphans |
| fact_customer_feedback | RouteKey | dim_route | RouteKey | 1:* | Single | Yes | 0 orphans |
| fact_booking_transactions | CustomerKey | dim_customer | CustomerKey | 1:* | Single | Yes | 0 orphans |
| fact_booking_transactions | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Yes | 0 orphans |
| fact_booking_transactions | RouteKey | dim_route | RouteKey | 1:* | Single | Yes | 0 orphans |
| fact_booking_transactions | FareClassKey | dim_fare_class | FareClassKey | 1:* | Single | Yes (model.json) | Listed as UNUSED in validation |
| fact_booking_transactions | TravelDateKey | dim_date | DateKey | 1:* | Single | Yes | Active travel date |

#### Inactive relationships (do not filter by default)

| From Table | From Column | To Table | To Column | Role |
|------------|-------------|----------|-----------|------|
| fact_customer_feedback | FeedbackDateKey | dim_date | DateKey | INACTIVE |
| fact_customer_feedback | ResolutionDateKey | dim_date | DateKey | INACTIVE |
| fact_booking_transactions | BookingDateKey | dim_date | DateKey | INACTIVE |

#### Relationships NOT allowed

| From | To | Reason |
|------|-----|--------|
| fact_customer_feedback | fact_booking_transactions | FlightOperationKey — fact-to-fact join not allowed |
| fact_booking_transactions | fact_customer_feedback | FlightOperationKey — fact-to-fact join not allowed |

#### Unused dimensions (no FK to any fact)

| Dimension | Reason |
|-----------|--------|
| dim_fare_class | No FK column in any fact |
| dim_booking_channel | No FK column in any fact |
| dim_currency | No FK column in any fact; OD-04 blocked |

### Critical relationship findings for Page 05

1. **fact_customer_feedback has NO active date relationship.** A date slicer on dim_date[FullDate] will NOT filter feedback visuals unless measures use `USERELATIONSHIP(dim_date[DateKey], fact_customer_feedback[FeedbackDateKey])`.

2. **Fact-to-fact relationships are NOT allowed.** Booking data and feedback data cannot be directly joined. "Satisfied Passengers" (combining passenger counts with satisfaction) cannot be computed at the passenger level.

3. **dim_fare_class, dim_booking_channel, dim_currency are unused** — class dimension cannot slice facts without model change.

4. **Only one active relationship allowed between dim_date and any fact table.** Role-playing dates must be inactive.

---

## 6. Existing Report Page 05 Configuration

From `deliverables/power_bi/report/report.json`, Page "Customer & Service Intelligence" contains 13 visuals:

| # | Visual Type | Measure | Purpose |
|---|-------------|---------|---------|
| 1 | Card | CF01 | Total feedback events |
| 2 | Card | CF02 | Average satisfaction score |
| 3 | Card | CF03 | Complaint percentage |
| 4 | Card | CF04 | Active customers |
| 5 | Card | CF05 | Complaint count |
| 6 | Card | CF06 | Compliment count |
| 7 | Card | CF11 | Service recovery rate |
| 8 | Card | CF12 | Resolution rate |
| 9 | Bar Chart | CF01 by AirlineName | Feedback volume by airline |
| 10 | Bar Chart | CF01 by FeedbackChannel | Feedback volume by channel |
| 11 | Bar Chart | CF02 by AirlineName | Avg satisfaction by airline |
| 12 | Bar Chart | CF01 by FeedbackType | Feedback volume by type |
| 13 | Bar Chart | CF01 by ResolutionStatus | Feedback volume by resolution status |

**Note:** None of these visuals have explicit title properties set in report.json. Titles must be configured in Power BI Desktop.

---

## Summary of Discovery

- **Primary data source for Page 05:** `fact_customer_feedback` (2,500 feedback events) — fully supported
- **Customer dimension:** `dim_customer` (5,000 customers) — supported for segmentation, NO Gender
- **Booking data:** `fact_booking_transactions` (9,956 coupons) — OD-04 BLOCKED
- **Class dimension:** `dim_fare_class` (8 fare classes, 4 cabin classes) — UNUSED (no FK to facts)
- **No Gender field** anywhere in the project
- **No TravelType field** anywhere in the project
- **No six service-rating columns** — only one `SatisfactionScore` (1–5)
- **"Economy Plus" does NOT exist** — actual values: Economy, Premium Economy, Business, First
- **Page 05 already exists** with 13 CF-based visuals — Visual 1 (CF01) validated as PASS