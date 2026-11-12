# AEROVISION 360 — Page 05 Real Data Source Audit

**Project:** AEROVISION 360 — Airline Intelligence Platform  
**Target Page:** Page 05 — Customer & Service Intelligence (Passenger Satisfaction Review)  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY INVESTIGATION COMPLETE — NO DATASETS, DAX, POWER QUERY, RELATIONSHIPS, PBIX, OR REPORT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Complete Source Inventory

All source datasets were inspected from two locations (identical content):

| Location | Path | Contents |
|----------|------|----------|
| Primary curated layer | `data/03_curated/` | 28 files (14 CSV + 14 Parquet) |
| Deliverables data layer | `deliverables/data/` | Same 14 datasets + `customer_feedback/` subdirectory |

### Dataset Inventory (14 total)

| # | Dataset | File (Parquet) | File (CSV) | Rows | Columns | Primary Key | Grain |
|---|---------|---------------|------------|------|---------|-------------|-------|
| 1 | dim_customer | `data/03_curated/dim_customer.parquet` | `data/03_curated/dim_customer.csv` | 5,000 | 8 | CustomerKey | One row per customer |
| 2 | fact_customer_feedback | `data/03_curated/fact_customer_feedback.parquet` | `data/03_curated/fact_customer_feedback.csv` | 2,500 | 14 | FeedbackKey | One row per feedback event |
| 3 | fact_booking_transactions | `data/03_curated/fact_booking_transactions.parquet` | `data/03_curated/fact_booking_transactions.csv` | 9,956 | 45 | BookingTransactionKey | One row per ticket coupon |
| 4 | dim_fare_class | `data/03_curated/dim_fare_class.parquet` | `data/03_curated/dim_fare_class.csv` | 8 | 7 | FareClassKey | One row per fare class |
| 5 | dim_airline | `data/03_curated/dim_airline.parquet` | `data/03_curated/dim_airline.csv` | 10 | 12 | AirlineKey | One row per airline |
| 6 | dim_date | `data/03_curated/dim_date.parquet` | `data/03_curated/dim_date.csv` | 761 | 19 | DateKey | One row per calendar date |
| 7 | dim_route | `data/03_curated/dim_route.parquet` | `data/03_curated/dim_route.csv` | 320 | 9 | RouteKey | One row per directional route |
| 8 | dim_booking_channel | `data/03_curated/dim_booking_channel.parquet` | `data/03_curated/dim_booking_channel.csv` | 7 | 6 | BookingChannelKey | One row per booking channel |
| 9 | dim_currency | `data/03_curated/dim_currency.parquet` | `data/03_curated/dim_currency.csv` | 8 | 6 | CurrencyKey | One row per currency |
| 10 | dim_airport | `data/03_curated/dim_airport.parquet` | `data/03_curated/dim_airport.csv` | 72 | 11 | AirportKey | One row per airport |
| 11 | dim_aircraft | `data/03_curated/dim_aircraft.parquet` | `data/03_curated/dim_aircraft.csv` | 440 | 9 | AircraftKey | One row per aircraft |
| 12 | dim_aircraft_type | `data/03_curated/dim_aircraft_type.parquet` | `data/03_curated/dim_aircraft_type.csv` | 12 | 8 | AircraftTypeKey | One row per aircraft type |
| 13 | dim_disruption_type | `data/03_curated/dim_disruption_type.parquet` | `data/03_curated/dim_disruption_type.csv` | 9 | 7 | DisruptionTypeKey | One row per disruption type |
| 14 | fact_flight_operations | `data/03_curated/fact_flight_operations.parquet` | `data/03_curated/fact_flight_operations.csv` | 5,000 | 25 | FlightOperationKey | One row per flight leg |
| 15 | fact_disruptions | `data/03_curated/fact_disruptions.parquet` | `data/03_curated/fact_disruptions.csv` | 1,754 | 16 | DisruptionKey | One row per disruption event |
| 16 | fact_operating_costs | `data/03_curated/fact_operating_costs.parquet` | `data/03_curated/fact_operating_costs.csv` | 7,480 | 18 | OperatingCostKey | One row per cost ledger line |

**Note:** 16 datasets total (not 14 as previously stated — fact_disruptions and fact_operating_costs are additional). All have matching CSV and Parquet files with identical content.

---

## 2. Actual Schemas and Profiling Results

### 2.1 dim_customer (5,000 rows, 8 columns, PK: CustomerKey)

**File:** `data/03_curated/dim_customer.parquet` (also `.csv`)

| Column | Type | Nulls | Distinct | Sample Values | Notes |
|--------|------|-------|----------|---------------|-------|
| CustomerKey | int32 | 0 | 5,000 | 1–5,000 | Primary key, unique |
| CustomerID | string | 0 | 5,000 | CUST-... | Synthetic business key |
| CustomerSegment | string | 0 | 4 | Leisure(3,107), Business(1,118), Corporate(496), Group(279) | Closest proxy for "customer type" |
| LoyaltyTier | string | 0 | 4 | Silver(1,980), Gold(1,514), Platinum(820), None(686) | "None" is a valid tier value |
| HomeCountry | string | 0 | 8 | 8 countries | Geography dimension |
| HomeCountryCode | string | 0 | 8 | IN, AE, GB, SG, US, QA, DE, AU | Country code |
| RegistrationDate | object (date) | 0 | 366 | 2024-10-01 to 2025-09-30 | Customer registration date |
| IsActive | bool | 0 | 2 | True(4,808), False(192) | Active flag |

**Gender column:** DOES NOT EXIST. Confirmed absent from schema, data, and build script (`scripts/build_dim_customer.py` contains no gender references).

---

### 2.2 fact_customer_feedback (2,500 rows, 14 columns, PK: FeedbackKey)

**File:** `data/03_curated/fact_customer_feedback.parquet` (also `.csv`, also in `deliverables/data/customer_feedback/`)

| Column | Type | Nulls | Distinct | Sample Values | Notes |
|--------|------|-------|----------|---------------|-------|
| FeedbackKey | int64 | 0 | 2,500 | — | Primary key, unique |
| FeedbackID | string | 0 | 2,500 | — | Business key, unique |
| CustomerKey | int32 | 0 | 1,938 | — | FK → dim_customer; 562 customers have multiple feedback events |
| AirlineKey | int32 | 0 | 10 | — | FK → dim_airline |
| FlightOperationKey | int64 | 0 | 2,500 | — | Degenerate reference to fact_flight_operations (no relationship) |
| RouteKey | int32 | 0 | 320 | — | FK → dim_route |
| FeedbackDateKey | int32 | 0 | — | — | FK → dim_date (INACTIVE relationship) |
| FeedbackType | string | 0 | 4 | Survey(641), Complaint(638), Claim(618), Compliment(603) | Type of feedback |
| SatisfactionScore | Int8 | 603 (24.1%) | 5 | 1(377), 2(387), 3(378), 4(386), 5(369) | Scale 1–5; mean 2.991 |
| ComplaintCategory | string | 1,862 (74.5%) | 8 | Other(89), Delay(85), Seat(82), Customer Service(81), Baggage(79), In-Flight Experience(75), Cancellation(75), Boarding(72) | Populated only for complaints |
| ServiceRecoveryFlag | bool | 0 | 2 | True(381), False(2,119) | Service recovery applied |
| ResolutionStatus | string | 0 | 4 | Open(639), Closed - No Action(631), In Progress(626), Resolved(604) | Case resolution status |
| ResolutionDateKey | Int32 | 1,896 (75.8%) | — | — | FK → dim_date (INACTIVE); null when not resolved |
| FeedbackChannel | string | 0 | 6 | Email(428), Call Center(422), Social(420), Web(418), Mobile(407), Airport(405) | Feedback channel |

**Duplicate rows:** 0  
**Duplicate FeedbackKey:** 0  
**Duplicate FeedbackID:** 0

**Service rating columns:** Only ONE satisfaction column exists (`SatisfactionScore`, 1–5). No separate columns for Arrival Time Convenience, Cleanliness, Ease of Online Booking, Baggage Handling, In-flight Service, or Food and Drink. The value "In-Flight Experience" appears only as a ComplaintCategory value (75 rows), not as a rating column.

---

### 2.3 fact_booking_transactions (9,956 rows, 45 columns, PK: BookingTransactionKey) — OD-04 BLOCKED

**File:** `data/03_curated/fact_booking_transactions.parquet` (also `.csv`)

**OD-04 Status:** Blocked per exchange-rate policy (unresolved). Revenue/passenger measures from this table are under governance restriction.

| Column | Type | Nulls | Distinct | Sample Values | Notes |
|--------|------|-------|----------|---------------|-------|
| BookingTransactionKey | int64 | 0 | 9,956 | — | Primary key, unique |
| BookingReference | string | 0 | 9,956 | — | Business key, unique |
| TicketNumber | string | 0 | — | — | Ticket number |
| TicketCouponNumber | int8 | 0 | — | — | Coupon number within ticket |
| CustomerKey | int32 | 0 | 4,204 | — | FK → dim_customer; 4,204 unique customers with bookings |
| AirlineKey | int32 | 0 | 10 | — | FK → dim_airline |
| FlightOperationKey | int64 | 0 | 5,000 | — | Degenerate reference (no relationship) |
| RouteKey | int32 | 0 | 320 | — | FK → dim_route |
| FareClassKey | int32 | 0 | 8 | 1–8 | FK → dim_fare_class (dimension unused, no FK from facts) |
| BookingChannelKey | int32 | 0 | 7 | — | FK → dim_booking_channel (dimension unused) |
| BookingDateKey | int32 | 0 | — | — | FK → dim_date (INACTIVE) |
| TravelDateKey | int32 | 0 | — | — | FK → dim_date (ACTIVE) |
| PassengerCount | int8 | 0 | 1 | **Always 1** | Every coupon = 1 passenger |
| IsRevenuePassenger | bool | 0 | 2 | True(8,922), False(1,034) | Revenue vs non-revenue |
| IsRefunded | bool | 0 | 2 | False(9,457), True(499) | Refund status |
| TransactionStatus | string | 0 | 6 | Flown(5,909), Ticketed(1,547), Booked(1,010), Cancelled(774), Refunded(499), NoShow(217) | Transaction status |
| BaseFareAmount … NetAncillaryRevenueUSD | float64 | 0 | — | — | Monetary amounts (USD-converted) |
| TransactionCurrencyKey | int32 | 0 | — | — | FK → dim_currency |
| ExchangeRateToUSD | float64 | 0 | — | — | Exchange rate |
| RateDateKey | int32 | 0 | — | — | FX rate date |
| RateVersion | string | 0 | — | — | FX rate version |
| BookingLeadTimeDays | int16 | 0 | — | — | Days between booking and travel |
| SyntheticProvenance | string | 0 | — | — | Data provenance flag |

**TravelType column:** DOES NOT EXIST.  
**Gender column:** DOES NOT EXIST.

**Key metrics (verified):**
- SUM(PassengerCount) = 9,956 (equals row count, since always 1)
- SUM(PassengerCount where IsRevenuePassenger=TRUE) = 8,922
- DISTINCTCOUNT(CustomerKey) = 4,204

---

### 2.4 dim_fare_class (8 rows, 7 columns, PK: FareClassKey) — UNUSED DIMENSION

**File:** `data/03_curated/dim_fare_class.parquet` (also `.csv`)

**Critical:** No foreign key relationship to any fact table. Cannot slice booking or feedback data.

| Column | Type | Values |
|--------|------|--------|
| FareClassKey | int32 | 1–8 |
| FareClassCode | string | Y, M, B, W, E, J, C, F |
| FareClassName | string | Economy Flexible, Economy Standard, Economy Basic, Premium Economy Flexible, Premium Economy Standard, Business Flexible, Business Standard, First Flexible |
| CabinClass | string | Economy(3), Premium Economy(2), Business(2), First(1) |
| RefundabilityCategory | string | Refundable, Partially Refundable, Non-Refundable |
| IsAncillaryEligible | bool | True (all 8) |
| DisplayOrder | int16 | 1, 2 |

**CabinClass values:** Economy, Premium Economy, Business, First. **"Economy Plus" does NOT exist.** Closest equivalent is Premium Economy.

---

### 2.5 dim_airline (10 rows, 12 columns, PK: AirlineKey)

**File:** `data/03_curated/dim_airline.parquet` (also `.csv`)

| Column | Type | Nulls | Notes |
|--------|------|-------|-------|
| AirlineKey | int32 | 0 | Primary key |
| AirlineId | string | 0 | AIR_0001 through AIR_0010 |
| AirlineIATACode | string | 0 | IATA code |
| AirlineICAOCode | string | 0 | ICAO code |
| AirlineName | string | 0 | Airline name |
| AirlineGroup | string | 10 (100%) | **Entirely null** |
| HomeCountry | string | 0 | Home country |
| HomeCountryCode | string | 0 | Country code |
| BusinessModelClass | string | 10 (100%) | **Entirely null** |
| IsActive | bool | 0 | All True |
| StatusEffectiveDate | object | 10 (100%) | **Entirely null** |
| ReferenceVersion | string | 0 | Draft value |

**3 entirely null columns:** AirlineGroup, BusinessModelClass, StatusEffectiveDate.

---

### 2.6 dim_date (761 rows, 19 columns, PK: DateKey)

**File:** `data/03_curated/dim_date.parquet` (also `.csv`)

| Column | Type | Notes |
|--------|------|-------|
| DateKey | int32 | Primary key (YYYYMMDD format) |
| FullDate | object (date) | Full date |
| Year | int16 | Year |
| Quarter | int8 | Quarter |
| MonthNumber | int8 | Month number |
| MonthName | string | Month name |
| MonthShortName | string | Short month name |
| YearMonth | string | Year-Month |
| YearMonthSort | int32 | Sort key |
| WeekNumber | int8 | ISO week number |
| WeekStartDate | object (date) | Week start (Monday) |
| DayOfMonth | int8 | Day of month |
| DayName | string | Day name |
| DayOfWeekNumber | int8 | Day of week number |
| IsWeekend | bool | Weekend flag |
| IsReportingPeriod | bool | Reporting period flag |
| FiscalYear | int16 | Fiscal year |
| FiscalQuarter | int8 | Fiscal quarter |
| FiscalMonthNumber | int8 | Fiscal month number |

**Date range:** 2024-10-01 to 2026-10-31 (761 continuous dates, no gaps)  
**Reporting period:** 2025-10-01 to 2026-09-30 (365 days)

---

### 2.7 Other Datasets (not customer-relevant)

| Dataset | Rows | Columns | PK | Page 05 Relevant? |
|---------|------|---------|-----|-------------------|
| dim_route | 320 | 9 | RouteKey | YES — RouteCode for slicers |
| dim_booking_channel | 7 | 6 | BookingChannelKey | NO — unused (no FK to facts) |
| dim_currency | 8 | 6 | CurrencyKey | NO — unused + OD-04 blocked |
| dim_airport | 72 | 11 | AirportKey | NO — not customer-facing |
| dim_aircraft | 440 | 9 | AircraftKey | NO — not customer-facing |
| dim_aircraft_type | 12 | 8 | AircraftTypeKey | NO — not customer-facing |
| dim_disruption_type | 9 | 7 | DisruptionTypeKey | NO — not customer-facing |
| fact_flight_operations | 5,000 | 25 | FlightOperationKey | PARTIAL — RevenuePassengers (flight-level, different population) |
| fact_disruptions | 1,754 | 16 | DisruptionKey | NO — not customer-facing |
| fact_operating_costs | 7,480 | 18 | OperatingCostKey | NO — OD-04 blocked |

---

## 3. Search for Missing Reference Fields

A project-wide search was performed across all `.py`, `.json`, `.md`, `.csv`, `.dax`, `.m`, `.txt` files (excluding `.git`, `__pycache__`, `.venv`, `.pytest_cache`, `.ruff_cache`).

### Gender
| Search Scope | Result |
|-------------|--------|
| dim_customer schema | NOT FOUND (8 columns, no Gender) |
| fact_customer_feedback schema | NOT FOUND (14 columns, no Gender) |
| fact_booking_transactions schema | NOT FOUND (45 columns, no Gender) |
| All source CSV/Parquet files | NOT FOUND |
| build_dim_customer.py | NOT FOUND |
| All DAX measures | NOT FOUND |
| All project documentation | NOT FOUND (only in docs I created earlier) |
| **Conclusion** | **Gender does not exist anywhere in the project** |

### Travel Type / Type of Travel
| Search Scope | Result |
|-------------|--------|
| fact_booking_transactions schema | NOT FOUND (45 columns, no TravelType) |
| fact_customer_feedback schema | NOT FOUND |
| dim_customer schema | NOT FOUND |
| All source files | NOT FOUND |
| All DAX measures | NOT FOUND |
| **Conclusion** | **Travel Type does not exist anywhere in the project** |

### Individual Service Ratings (6 categories)
| Reference Category | Found in Project? | Where |
|-------------------|-------------------|-------|
| Arrival Time Convenience | NO | Not a column anywhere |
| Cleanliness | NO | Not a column anywhere |
| Ease of Online Booking | NO | Not a column anywhere |
| Baggage Handling | PARTIAL | Value "Baggage" exists in ComplaintCategory (79 rows, complaints only) |
| In-flight Service | PARTIAL | Value "In-Flight Experience" exists in ComplaintCategory (75 rows, complaints only) |
| Food and Drink | NO | Not a column anywhere |
| Overall Satisfaction | YES | SatisfactionScore (1–5) column in fact_customer_feedback |

**Conclusion:** Only one satisfaction score column exists. No per-category service rating columns.

### Passenger Class / Cabin Class
| Field | Found? | Values |
|-------|--------|--------|
| CabinClass | YES (dim_fare_class) | Economy, Premium Economy, Business, First |
| "Economy Plus" | NO | Does not exist; closest is Premium Economy |
| FareClassCode | YES (dim_fare_class) | Y, M, B, W, E, J, C, F |

### Customer Behaviour Attributes
| Field | Found? | Source |
|-------|--------|--------|
| CustomerSegment | YES | dim_customer (Leisure, Business, Corporate, Group) |
| LoyaltyTier | YES | dim_customer (Silver, Gold, Platinum, None) |
| HomeCountry | YES | dim_customer |
| IsActive | YES | dim_customer |

---

## 4. Evidence-Backed Available Fields for Page 05

### From fact_customer_feedback (PRIMARY SOURCE — fully supported)

| Field | Type | Values | Nulls | Use Case |
|-------|------|--------|-------|----------|
| FeedbackKey | int64 | 2,500 unique | 0 | Count of feedback events (CF01) |
| FeedbackType | string | Survey, Complaint, Claim, Compliment | 0 | Feedback type breakdown |
| SatisfactionScore | Int8 | 1–5 | 603 (24.1%) | Average satisfaction (CF02) |
| ComplaintCategory | string | 8 categories | 1,862 (74.5%) | Complaint breakdown (complaints only) |
| ServiceRecoveryFlag | bool | True/False | 0 | Service recovery rate (CF11) |
| ResolutionStatus | string | Open, Closed - No Action, In Progress, Resolved | 0 | Resolution rate (CF12) |
| FeedbackChannel | string | Email, Call Center, Social, Web, Mobile, Airport | 0 | Feedback channel breakdown |
| CustomerKey | int32 | FK → dim_customer | 0 | Customer segmentation |
| AirlineKey | int32 | FK → dim_airline | 0 | Airline breakdown |
| RouteKey | int32 | FK → dim_route | 0 | Route breakdown |
| FeedbackDateKey | int32 | FK → dim_date | 0 | Date filtering (INACTIVE relationship) |

### From dim_customer (SECONDARY SOURCE — supported)

| Field | Type | Values | Nulls | Use Case |
|-------|------|--------|-------|----------|
| CustomerKey | int32 | 5,000 unique | 0 | Customer join key |
| CustomerSegment | string | Leisure, Business, Corporate, Group | 0 | Customer segment analysis |
| LoyaltyTier | string | Silver, Gold, Platinum, None | 0 | Loyalty tier analysis |
| HomeCountry | string | 8 countries | 0 | Geographic analysis |
| HomeCountryCode | string | 8 codes | 0 | Geographic analysis |
| IsActive | bool | True/False | 0 | Active customer count (CF04) |

### From dim_airline (SUPPORTED)

| Field | Type | Values | Use Case |
|-------|------|--------|----------|
| AirlineKey | int32 | 10 unique | Airline join key |
| AirlineName | string | 10 airlines | Airline slicer/legend |

### From dim_date (SUPPORTED with limitation)

| Field | Type | Use Case | Limitation |
|-------|------|----------|------------|
| FullDate | date | Date slicer | FeedbackDateKey relationship is INACTIVE; requires USERELATIONSHIP |

### From dim_fare_class (NOT USABLE — no FK to facts)

| Field | Type | Values | Limitation |
|-------|------|--------|------------|
| CabinClass | string | Economy, Premium Economy, Business, First | dim_fare_class has NO FK to any fact table |

---

## 5. Missing Fields and Datasets

| Reference Component | Missing Field | Status | Source Required | Classification |
|-------------------|--------------|--------|-----------------|----------------|
| Male Passengers | dim_customer[Gender] | NOT FOUND | Would need customer demographic data with gender | C — Not yet located |
| Female Passengers | dim_customer[Gender] | NOT FOUND | Would need customer demographic data with gender | C — Not yet located |
| Travel Type | fact_booking_transactions[TravelType] | NOT FOUND | Would need booking data with travel type (Business/Personal) | C — Not yet located |
| Satisfied Passengers | Satisfaction threshold definition | NOT APPROVED | OD-11 owner decision pending | B — Governance decision required |
| Neutral/Dissatisfied | Satisfaction threshold definition | NOT APPROVED | OD-11 owner decision pending | B — Governance decision required |
| Service Rating: Arrival Time Convenience | Separate rating column | NOT FOUND | Would need per-category rating survey data | C — Not yet located |
| Service Rating: Cleanliness | Separate rating column | NOT FOUND | Would need per-category rating survey data | C — Not yet located |
| Service Rating: Ease of Online Booking | Separate rating column | NOT FOUND | Would need per-category rating survey data | C — Not yet located |
| Service Rating: Food and Drink | Separate rating column | NOT FOUND | Would need per-category rating survey data | C — Not yet located |
| Economy Plus class | CabinClass value | NOT FOUND | Would need fare class data with "Economy Plus" | C — Not yet located (Premium Economy exists instead) |
| Passenger-level identifiers | PassengerID (distinct from booking/coupon) | NOT FOUND | Would need passenger manifest data | C — Not yet located |
| Fact-to-fact join (bookings + feedback) | Relationship | NOT ALLOWED | Governance prohibits fact-to-fact joins | A — Policy restriction (not data missing) |

### Classification Key:
- **A:** Available elsewhere in existing project (but blocked by policy/grain)
- **B:** Available from legitimate source needing governance approval
- **C:** Not yet located, requires further investigation

---

## 6. Existing Data Relationships and Grain

### Active Relationships (relevant to Page 05)

| From | From Column | To | To Column | Cardinality | Direction | Active | Orphans |
|------|-------------|----|-----------|-------------|-----------|--------|---------|
| fact_customer_feedback | CustomerKey | dim_customer | CustomerKey | 1:* | Single | Yes | 0 |
| fact_customer_feedback | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Yes | 0 |
| fact_customer_feedback | RouteKey | dim_route | RouteKey | 1:* | Single | Yes | 0 |
| fact_booking_transactions | CustomerKey | dim_customer | CustomerKey | 1:* | Single | Yes | 0 |
| fact_booking_transactions | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Yes | 0 |
| fact_booking_transactions | RouteKey | dim_route | RouteKey | 1:* | Single | Yes | 0 |
| fact_booking_transactions | FareClassKey | dim_fare_class | FareClassKey | 1:* | Single | Yes (model.json) | Listed as unused in validation |
| fact_booking_transactions | TravelDateKey | dim_date | DateKey | 1:* | Single | Yes | — |

### Inactive Relationships

| From | From Column | To | To Column | Reason |
|------|-------------|----|-----------|--------|
| fact_customer_feedback | FeedbackDateKey | dim_date | DateKey | Role-playing date; only one active relationship per fact-date pair |
| fact_customer_feedback | ResolutionDateKey | dim_date | DateKey | Role-playing date; only one active relationship per fact-date pair |
| fact_booking_transactions | BookingDateKey | dim_date | DateKey | Role-playing date; only one active relationship per fact-date pair |

### Relationships NOT Allowed

| From | To | Reason |
|------|-----|--------|
| fact_customer_feedback | fact_booking_transactions | FlightOperationKey — fact-to-fact join prohibited by governance |
| fact_booking_transactions | fact_customer_feedback | FlightOperationKey — fact-to-fact join prohibited by governance |

### Grain Summary

| Table | Grain | Row Count | Key Implication for Page 05 |
|-------|-------|-----------|------------------------------|
| fact_customer_feedback | One row per feedback event | 2,500 | Satisfaction is at feedback-event grain, NOT passenger grain |
| fact_booking_transactions | One row per ticket coupon | 9,956 | Each coupon = 1 passenger; not distinct passengers |
| dim_customer | One row per customer | 5,000 | CustomerSegment is customer attribute, not travel type |
| fact_flight_operations | One row per flight leg | 5,000 | RevenuePassengers is flight-level, different population |

**Critical grain distinction:** Feedback events (2,500) ≠ Passengers (9,956 coupons / 8,922 revenue) ≠ Customers (5,000 total / 4,204 with bookings). These cannot be treated as interchangeable.

---

## 7. Governance Restrictions

| Restriction | ID | Status | Impact on Page 05 |
|-------------|-----|--------|-------------------|
| FactBookingTransactions blocked | OD-04 | Unresolved | RV_* measures (revenue, passenger counts from bookings) cannot be used |
| Satisfaction scale threshold | OD-11 | Owner approval pending | No "satisfied/dissatisfied" count can be computed |
| Fact-to-fact joins | Governance | Prohibited | Cannot join bookings + feedback at passenger level |
| dim_fare_class unused | Validation | No FK to facts | CabinClass cannot slice any fact table |
| dim_booking_channel unused | Validation | No FK to facts | Channel dimension cannot slice facts |
| dim_currency unused + blocked | Validation + OD-04 | No FK to facts | Currency dimension cannot slice facts |

---

## 8. Exact Additional Source-Data Requirements

To reproduce the reference dashboard fully, the following source data would be required:

### A. Gender Data (for Male/Female KPIs)
- **Required:** A gender column in dim_customer or a customer demographic source
- **Status:** Not located in project (Classification C)
- **Action:** Do not infer from names or IDs. Would require new source data with gender attribute.

### B. Travel Type Data (for Travel Type slicer/charts)
- **Required:** A travel type column (Business/Personal) in fact_booking_transactions or dim_customer
- **Status:** Not located in project (Classification C)
- **Action:** Would require new source data with travel type attribute.

### C. Six Service Rating Columns (for service ratings visual)
- **Required:** Separate rating columns for Arrival Time Convenience, Cleanliness, Ease of Online Booking, Baggage Handling, In-flight Service, Food and Drink
- **Status:** Not located in project (Classification C)
- **Action:** Would require survey data with per-category ratings (1–5 scale each).

### D. Satisfaction Threshold Definition (for Satisfied/Dissatisfied counts)
- **Required:** Approved definition of what score constitutes "satisfied" (e.g., 4–5) vs "neutral/dissatisfied" (1–3)
- **Status:** OD-11 owner decision pending (Classification B)
- **Action:** Requires governance approval before implementation.

### E. Economy Plus Cabin Class (for class donut)
- **Required:** "Economy Plus" as a CabinClass value
- **Status:** Not in dim_fare_class (actual values: Economy, Premium Economy, Business, First)
- **Action:** Would require fare class taxonomy update OR use Premium Economy as substitute.

### F. Fact-to-Fact Join Capability (for behaviour decomposition)
- **Required:** Ability to join fact_booking_transactions with fact_customer_feedback
- **Status:** Prohibited by governance
- **Action:** Would require governance policy change OR a bridge table at common grain.

---

## 9. File Paths and Evidence Summary

| Evidence Item | File Path | Line/Section |
|--------------|-----------|--------------|
| dim_customer schema (8 cols, no Gender) | `data/03_curated/dim_customer.parquet` | Full schema profiled |
| fact_customer_feedback schema (14 cols, 1 SatisfactionScore) | `data/03_curated/fact_customer_feedback.parquet` | Full schema profiled |
| fact_booking_transactions schema (45 cols, no TravelType/Gender) | `data/03_curated/fact_customer_booking.parquet` | Full schema profiled |
| dim_fare_class schema (CabinClass: Economy/Premium Economy/Business/First) | `data/03_curated/dim_fare_class.parquet` | Full schema profiled |
| CF01 DAX | `deliverables/power_bi/dax/AEROVISION360_Measures.dax` | Line 16 |
| CF02 DAX | `deliverables/power_bi/dax/AEROVISION360_Measures.dax` | Line 17 |
| CF03–CF14 DAX | `deliverables/power_bi/dax/AEROVISION360_Measures.dax` | Lines 18–29 |
| Page 05 report definition | `deliverables/power_bi/report/report.json` | Lines 835–1091 |
| Semantic model relationships | `deliverables/power_bi/semantic_model/semantic_model.json` | Lines 132–197 (feedback), 392–512 (bookings) |
| Data quality audit | `deliverables/power_bi/audit/DATA_QUALITY_AUDIT.csv` | All rows |
| Relationship validation | `deliverables/power_bi/audit/RELATIONSHIP_VALIDATION.csv` | All rows |
| DAX measure audit | `deliverables/power_bi/audit/DAX_MEASURE_AUDIT.md` | All measures |
| Governance compliance | `deliverables/power_bi/audit/GOVERNANCE_COMPLIANCE.md` | OD-04, OD-11 sections |
| Remediation plan | `deliverables/power_bi/audit/POWER_BI_REMEDIATION_PLAN.md` | P0–P4 items |
| Build script (no gender) | `scripts/build_dim_customer.py` | No gender references |
| Build script (1 SatisfactionScore only) | `scripts/build_fact_customer_feedback.py` | Lines 62, 116, 119, 121 |

---

## 10. Conclusion

**What exists:** 16 datasets with verified schemas. Primary customer intelligence source is `fact_customer_feedback` (2,500 events) with `SatisfactionScore` (1–5), `FeedbackType`, `ComplaintCategory`, `ServiceRecoveryFlag`, `ResolutionStatus`, `FeedbackChannel`. Customer dimension has `CustomerSegment`, `LoyaltyTier`, `HomeCountry`, `IsActive` — but NO Gender.

**What is missing:** Gender, Travel Type, six service-rating columns, Economy Plus cabin class, passenger-level identifiers, satisfaction threshold definition (OD-11 pending), fact-to-fact join capability (prohibited).

**What is blocked:** fact_booking_transactions (OD-04), dim_fare_class (no FK to facts), inactive date relationships on feedback.

**Recommendation:** Page 05 can be built using only CF measures (CF01–CF14) from fact_customer_feedback plus dim_customer segmentation. All reference components requiring Gender, Travel Type, six service ratings, or passenger-class cross-tabs cannot be built without new source data or governance decisions.

---

**Audit complete. Read-only. No datasets, DAX, Power Query, relationships, PBIX, or report files were modified.**
