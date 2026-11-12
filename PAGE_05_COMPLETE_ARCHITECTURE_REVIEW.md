# AEROVISION 360 — Page 05 Complete Architecture Review

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Review Date:** 2026-11-08  
**Status:** READ-ONLY ARCHITECTURE REVIEW COMPLETE  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Executive Summary

The AEROVISION 360 architecture is a layered batch ETL system (RAW → STAGING → CURATED → REFERENCE) feeding a Power BI semantic model. Page 05 (Customer & Service Intelligence) is one of five fixed primary report pages. The architecture explicitly prohibits fact-to-fact relationships, blocks FactBookingTransactions under OD-04, and contains no Gender, Travel Type, or service-rating columns. All customer data is synthetic with no real personal information.

---

## 2. Data Architecture

### 2.1 Layered Architecture

| Layer | Folder | Purpose | Write Policy | Consumer |
|-------|--------|---------|--------------|----------|
| RAW | `data/01_raw/` | Preserve generated source records with deliberate defects | Immutable after generation | STAGING, audit |
| STAGING | `data/02_staging/` | Standardize, type, deduplicate, flag, validate | Rebuildable from RAW | CURATED |
| CURATED | `data/03_curated/` | Clean star-schema tables and USD measures | Rebuildable from STAGING | Power BI |
| REFERENCE | `data/04_reference/` | Controlled code lists, calendars, rates, assumptions | Version-controlled | STAGING, CURATED, Power BI |

**Cross-layer rules:**
- RAW is never overwritten or cleaned in place
- Every CURATED row traces to RAW, controlled reference, or documented allocation
- Transformations are deterministic for same seed/config/source/code version
- Invalid records are rejected with reason codes or quarantined — never silently deleted
- No aggregation that duplicates revenue/cost across tables
- No aggregation of different currencies without USD conversion

### 2.2 Star Schema Design

The semantic model uses a star schema with the following dimensions and facts:

**Dimensions (11):**

| Dimension | Grain | PK | FKs | Page 05 Use |
|-----------|-------|-----|-----|-------------|
| DimDate | One row per calendar date | DateKey | None | YES — date filtering |
| DimAirline | One row per airline (Type 1) | AirlineKey | None | YES — airline filtering |
| DimAirport | One row per airport | AirportKey | None | NO — not customer-facing |
| DimRoute | One row per directional O-D pair | RouteKey | OriginAirportKey, DestinationAirportKey | YES — route filtering |
| DimAircraft | One row per aircraft | AircraftKey | AirlineKey, AircraftTypeKey | NO — not customer-facing |
| DimAircraftType | One row per aircraft type | AircraftTypeKey | None | NO — not customer-facing |
| DimCustomer | One row per fictional customer | CustomerKey | None | YES — CustomerSegment, LoyaltyTier, IsActive |
| DimFareClass | One row per fare class | FareClassKey | None | PARTIAL — CabinClass, no FK to facts |
| DimBookingChannel | One row per booking channel | BookingChannelKey | None | NO — no FK to facts |
| DimCurrency | One row per currency | CurrencyKey | None | BLOCKED — OD-04 |
| DimDisruptionType | One row per disruption type | DisruptionTypeKey | None | NO — not customer-facing |

**Facts (5):**

| Fact | Grain | PK | FKs | Page 05 Use |
|------|-------|-----|-----|-------------|
| FactFlightOperations | One row per flight leg | FlightOperationKey | AirlineKey, RouteKey, AircraftKey, ScheduledDepartureDateKey, ScheduledArrivalDateKey | PARTIAL — RevenuePassengers (flight-level) |
| FactBookingTransactions | One row per ticket coupon | BookingTransactionKey | CustomerKey, AirlineKey, FlightOperationKey, RouteKey, FareClassKey, BookingChannelKey, BookingDateKey, TravelDateKey, TransactionCurrencyKey | BLOCKED — OD-04 |
| FactOperatingCosts | One row per cost ledger line | OperatingCostKey | FlightOperationKey, AirlineKey, RouteKey, CostDateKey, CurrencyKey | BLOCKED — OD-04 |
| FactDisruptions | One row per disruption event | DisruptionKey | FlightOperationKey, AirlineKey, RouteKey, EventLocationAirportKey, DisruptionTypeKey, EventDateKey | NO — not customer-facing |
| FactCustomerFeedback | One row per feedback event | FeedbackKey | CustomerKey, AirlineKey, FlightOperationKey, RouteKey, FeedbackDateKey, ResolutionDateKey | YES — PRIMARY Page 05 source |

### 2.3 Relationship Architecture

**Active relationships relevant to Page 05:**

| From | From Column | To | To Column | Cardinality | Active |
|------|-------------|-----|-----------|-------------|--------|
| FactCustomerFeedback | CustomerKey | DimCustomer | CustomerKey | 1:* | Yes |
| FactCustomerFeedback | AirlineKey | DimAirline | AirlineKey | 1:* | Yes |
| FactCustomerFeedback | RouteKey | DimRoute | RouteKey | 1:* | Yes |
| FactBookingTransactions | CustomerKey | DimCustomer | CustomerKey | 1:* | Yes |
| FactBookingTransactions | AirlineKey | DimAirline | AirlineKey | 1:* | Yes |
| FactBookingTransactions | RouteKey | DimRoute | RouteKey | 1:* | Yes |
| FactBookingTransactions | FareClassKey | DimFareClass | FareClassKey | 1:* | Yes (model.json) / UNUSED (validation) |
| FactBookingTransactions | TravelDateKey | DimDate | DateKey | 1:* | Yes |

**Inactive relationships (do not filter by default):**

| From | From Column | To | To Column | Reason |
|------|-------------|-----|-----------|--------|
| FactCustomerFeedback | FeedbackDateKey | DimDate | DateKey | Role-playing date; only one active per fact-date pair |
| FactCustomerFeedback | ResolutionDateKey | DimDate | DateKey | Role-playing date |
| FactBookingTransactions | BookingDateKey | DimDate | DateKey | Role-playing date |

**Fact-to-fact rule (Section 5.1):** "No fact table may have a relationship to another fact table. Shared dimensions provide cross-fact analysis. If a report requires a combination that cannot be expressed through conformed dimensions, the design must be reviewed and approved before implementation."

**Unused dimensions (no FK to any fact):** DimFareClass, DimBookingChannel, DimCurrency — these dimensions exist but cannot slice any fact table without a model change.

---

## 3. Data Provenance Assessment

### 3.1 Data Source Verification

| Dataset | Provenance | Real/Synthetic | Personal Data? | Page 05 Use |
|---------|-----------|---------------|----------------|-------------|
| DimAirline | Real airline identities (10 airlines from roster) | Real identities, synthetic attributes | No | YES |
| DimCustomer | Deterministic synthetic (seed 3602026) | Synthetic | No (C-08) | YES |
| FactCustomerFeedback | Deterministic synthetic (seed 3602026) | Synthetic | No | YES |
| FactBookingTransactions | Deterministic synthetic (seed 3602027) | Synthetic | No | BLOCKED |
| FactFlightOperations | Deterministic synthetic (seed 3602026) | Synthetic | No | PARTIAL |
| All other datasets | Deterministic synthetic | Synthetic | No | N/A |

**C-08 (Data Contracts):** "Real airline identity attributes, to be source-verified before reference approval; all operational, customer, and financial data synthetic; no real passenger personal information"

**Key finding:** All customer and operational data is synthetic. No real passenger personal information exists anywhere in the project. Gender data cannot exist because C-08 prohibits real personal identifiers, and no synthetic gender column was generated.

### 3.2 Build Script Determinism

All build scripts use fixed random seeds:
- `build_dim_customer.py`: SEED = 3602026
- `build_fact_customer_feedback.py`: SEED = 3602026
- `build_fact_booking_transactions.py`: SEED = 3602027

Scripts refuse to overwrite existing outputs (`FileExistsError`), ensuring reproducibility.

---

## 4. Semantic Model Review

### 4.1 Model Tables and Measures

The semantic model (`semantic_model.json`) defines 16 tables with the following measures:

**FactCustomerFeedback measures (CF01-CF14):**
- CF01: Total Feedback Events — `COUNTROWS(fact_customer_feedback)` — VERIFIED (2,500)
- CF02: Average Satisfaction Score — `AVERAGE(SatisfactionScore)` — VERIFIED (2.99)
- CF03: Complaint Percentage — verified (25.52%)
- CF04-CF14: Various feedback counts and rates — all verified

**FactBookingTransactions measures (RV_*, NC_*):** OD-04 BLOCKED — exist in DAX but under governance question

**FactFlightOperations measures (FL01-FL04):** Verified (flights operated, revenue passengers, delay, cancellation rate)

**FactDisruptions measures (DS01-DS03):** Verified (disruptions, delay, controllable disruptions)

**FactOperatingCosts measures (CX_*):** OD-04 BLOCKED

**Flight operations measures (OP01-OP04):** Exist in DAX but not registered in model.json/semantic_model.json

### 4.2 Model Issues Identified

| Issue | Severity | Description | Page 05 Impact |
|-------|----------|-------------|----------------|
| dim_fare_class unused | High | No FK to any fact table | CabinClass cannot slice booking/feedback data |
| dim_booking_channel unused | High | No FK to any fact table | Channel cannot slice facts |
| dim_currency unused + OD-04 blocked | High | No FK to facts + governance blocked | Currency filtering unavailable |
| FactCustomerFeedback date relationships inactive | Medium | FeedbackDateKey and ResolutionDateKey both inactive | Date slicer cannot filter feedback without USERELATIONSHIP |
| FactBookingTransactions OD-04 blocked | Critical | Exchange-rate policy unresolved | Passenger/revenue measures unavailable |
| model.json has incorrect FL01/FL02/CF03 expressions | Medium | Wrong expressions in custom JSON | Model metadata unreliable |
| semantic_model.json incomplete relationships | Medium | Missing aircraft, airport, customer, disruption type relationships | Model metadata incomplete |
| No Gender column anywhere | Critical | Not in any table, script, DAX, or documentation | Male/Female KPIs impossible |
| No TravelType column anywhere | Critical | Not in any table, script, DAX, or documentation | Travel Type analysis impossible |
| No service-rating columns anywhere | Critical | Only SatisfactionScore exists | Six service ratings impossible |

---

## 5. Power BI Architecture Review

### 5.1 Report Definition (`report.json`)

The report defines 5 pages:
1. Executive Overview — 4 visuals (cards + barChart)
2. Network & Capacity Intelligence — 2 visuals (barCharts)
3. Revenue & Finance — 28 visuals (cards, lineCharts, barCharts, pieChart, slicers)
4. Operations & Disruption — 3 visuals (cards FL04, DS03 + barChart DS01)
5. Customer & Service Intelligence — 13 visuals (8 cards CF01-CF12, 5 bar charts)

**Page 05 visuals in report.json:**
1. Card — CF01 (Total Feedback Events)
2. Card — CF02 (Average Satisfaction Score)
3. Card — CF03 (Complaint Percentage)
4. Card — CF04 (Active Customers)
5. Card — CF05 (Complaint Count)
6. Card — CF06 (Compliment Count)
7. Card — CF11 (Service Recovery Rate)
8. Card — CF12 (Resolution Rate)
9. Bar Chart — CF01 by AirlineName
10. Bar Chart — CF01 by FeedbackChannel
11. Bar Chart — CF02 by AirlineName
12. Bar Chart — CF01 by FeedbackType
13. Bar Chart — CF01 by ResolutionStatus

**No visual titles are set in report.json.** No slicers are defined on Page 05.

### 5.2 PBIX File Status

| File | Size | Status |
|------|------|--------|
| `deliverables/power_bi/AEROVISION_360.pbix` | 9,402,888 bytes | Exists, valid ZIP, but internal DataModel is XPress9-compressed (cannot inspect programmatically) |
| `deliverables/power_bi/AEROVISION_360.pbip` | 195 bytes | Import-ready project file |
| `deliverables/power_bi_backup_20261105/` | — | Backup from 2026-11-05 |

**GOV-01:** PBIX report has only one blank page ("Page 1") with no visuals. Custom report.json pages are not loaded into PBIX. Report pages and disclosure are not actually present in PBIX.

---

## 6. Power Query Architecture

### 5.1 Power Query Script (`AEROVISION360_DataLoad.m`)

- Defines only 2 of 14 tables
- dim_airline column count stated as 14; actual is 12
- No error handling or duplicate prevention beyond comments
- Needs full rewrite for all 14 tables

### 5.2 Data Sources (`data_sources.json`)

References 14 CSV datasets from `deliverables/data/` (not `data/03_curated/`). Refresh policy: Power BI Desktop > Refresh; data files are static exports of data/03_curated.

---

## 7. DAX Architecture Review

### 7.1 Measure Categories

| Category | Prefix | Count | Status |
|----------|--------|-------|--------|
| Flight Operations | FL | 4 | Verified |
| Disruptions | DS | 3 | Verified (DS03 has DAX-01 issue) |
| Customer Feedback | CF | 14 | Verified |
| Booking/Revenue | RV | 21 | OD-04 BLOCKED |
| Operating Costs | CX | 11 | OD-04 BLOCKED |
| Financial Performance | NC | 3 | OD-04 BLOCKED (depends on RV/CX) |
| Operations Performance | OP | 3 | Not registered in model |

### 7.2 DAX Issues (from DAX_MEASURE_AUDIT.md)

| Issue | ID | Severity | Description |
|-------|----|----------|-------------|
| DS03 counts dimension rows | DAX-01 | P1 | Counts dim_disruption_type rows (3) instead of fact events (540) |
| FL04 boolean SUM risk | DAX-02 | P2 | SUM on boolean column may fail |
| Percentage scaling ambiguity | DAX-03 | P2 | FL04/CF03 multiply by 100; Power BI Percent format would show 448%/2552% |
| model.json wrong expressions | DAX-04 | P1 | FL01 counts all rows, FL02 uses BookedPassengers, CF03 filters ComplaintCategory |
| model.json omits dimensions | DAX-05 | P2 | Only 3 fact tables defined, no dimensions |
| semantic_model.json no expressions | DAX-06 | P2 | Lists measure names only, no DAX logic |
| FL02 naming ambiguity | DAX-07 | P3 | Must remain "passenger volume", not monetary revenue |
| CF02 scale pending | DAX-08 | P3 | OD-11 satisfaction scale undefined |

---

## 8. Governance Architecture Review

### 8.1 Key Governance Restrictions

| Restriction | ID | Status | Impact on Page 05 |
|-------------|-----|--------|-------------------|
| FactBookingTransactions blocked | OD-04 | Unresolved | RV_* passenger/revenue measures cannot be used |
| Satisfaction scale threshold | OD-11 | Owner approval pending | No "satisfied/dissatisfied" counts |
| Fact-to-fact joins | Governance | Prohibited | Cannot join bookings + feedback at passenger level |
| dim_fare_class unused | Validation | No FK to facts | CabinClass cannot slice facts |
| dim_booking_channel unused | Validation | No FK to facts | Channel cannot slice facts |
| dim_currency unused + blocked | Validation + OD-04 | No FK to facts + blocked | Currency filtering unavailable |
| Feedback date relationships inactive | Model | Both inactive | Date slicer needs USERELATIONSHIP |

### 8.2 OD-04 Exchange Rate Policy

OD-04 blocks FactBookingTransactions and FactOperatingCosts due to unresolved exchange-rate policy. Key sub-decisions:
- OD-04a: Currency scope (AED, QAR, SGD, INR, GBP, EUR, USD, AUD)
- OD-04b: Exchange rate convention (USD per one unit, exact-date lookup, 6 decimals, round to 2 decimals, no forward-fill)
- OD-04c: Rate source (AEROVISION-360-SYNTHETIC-FX-V1)
- OD-04d: Rate version (FX-2026-11-04-001)
- OD-04e: Missing date behavior (no forward-fill; missing exact-date rate quarantines the row)
- OD-04f: Rate generation methodology (deterministic, fixed seed)

---

## 9. Architecture Gaps for Page 05 Reference Requirements

| Reference Requirement | Architecture Gap | Severity | Resolvable Without New Data? |
|----------------------|-----------------|----------|------------------------------|
| Gender (Male/Female KPIs) | No Gender column in any table | Critical | No |
| Travel Type (Business/Personal) | No TravelType column in any table | Critical | No |
| Six service ratings | Only SatisfactionScore exists | Critical | No |
| Satisfied/Dissatisfied counts | No OD-11 threshold defined | High | No (OD-11 pending) |
| Satisfaction by Class | dim_fare_class unused (no FK) | High | No (needs model change) |
| Passengers by Travel Type & Class | No TravelType; dim_fare_class unused | Critical | No |
| Passengers by Class donut | dim_fare_class unused; "Economy Plus" absent | High | No (needs model change) |
| Behaviour decomposition | Gender & TravelType absent; fact-to-fact prohibited | Critical | No |
| Total Passengers KPI | FactBookingTransactions OD-04 blocked | High | No (OD-04 unresolved) |

---

## 10. Conclusion

The AEROVISION 360 architecture is well-documented and follows a clean layered ETL pattern with a star schema semantic model. However, for Page 05 specifically:

1. **The architecture cannot reproduce the reference dashboard as specified** — multiple required fields (Gender, Travel Type, service ratings, Economy Plus) do not exist in any table, script, or configuration.

2. **Fact-to-fact joins are explicitly prohibited** — booking data and feedback data cannot be directly combined at the passenger level.

3. **OD-04 blocks FactBookingTransactions** — passenger-count and revenue measures from bookings are unavailable.

4. **OD-11 leaves satisfaction thresholds undefined** — no "satisfied/dissatisfied" classification is approved.

5. **dim_fare_class is an unused dimension** — CabinClass cannot slice any fact table without a model change.

6. **The existing Page 05 has 13 CF-based visuals** that use verified measures (CF01-CF14) and can serve as the foundation for a customer intelligence page, but they do not match the reference dashboard structure.

**Any expansion of the architecture to support the full reference dashboard would require:**
- New source data with Gender, Travel Type, and service-rating fields
- Governance approval for OD-04 and OD-11
- Either a model change to connect dim_fare_class to facts, or a new fact table
- Clear segregation of any external data as a separate population
