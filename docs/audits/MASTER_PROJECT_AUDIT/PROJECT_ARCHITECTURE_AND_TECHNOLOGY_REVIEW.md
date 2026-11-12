# AEROVISION 360 — PROJECT ARCHITECTURE AND TECHNOLOGY REVIEW

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY AUDIT — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Project Architecture Overview

AEROVISION 360 is a **Global Multi-Airline Operations, Revenue & Customer Intelligence Platform** built as a layered batch ETL system feeding a Power BI semantic model. The architecture follows a modern data warehouse pattern with four distinct layers:

### 1.1 Data Layer Architecture

| Layer | Folder | Purpose | Write Policy | Consumer |
|-------|--------|---------|--------------|----------|
| RAW | `data/01_raw/` | Preserve generated source records with deliberate defects | Immutable after generation | STAGING and audit |
| STAGING | `data/02_staging/` | Standardize, type, deduplicate, flag, validate | Rebuildable from RAW | CURATED |
| CURATED | `data/03_curated/` | Clean star-schema tables and USD measures | Rebuildable from STAGING | Power BI |
| REFERENCE | `data/04_reference/` | Hold controlled code lists, calendars, rates, assumptions | Version-controlled | STAGING, CURATED, Power BI |

### 1.2 Technology Stack

| Component | Technology | Status |
|-----------|------------|--------|
| Analytics platform | Power BI Desktop | Core reporting layer |
| Data transformation | Power Query M | ETL layer |
| Analytical calculations | DAX | Semantic model measures |
| Data engineering | Python | Data generation, staging, curated |
| Data storage | CSV + Parquet | All datasets stored in both formats |
| Version control | Git | Project source control |
| Data formats | CSV, Parquet, Excel | Multiple formats supported |

### 1.3 Project Structure

```
AEROVISION_360/
├── data/                    # Data layer (RAW, STAGING, CURATED, REFERENCE)
├── deliverables/            # Power BI deliverables, Excel, exports
├── docs/                    # Documentation, governance, blueprints
├── scripts/                 # Build scripts, audit scripts, pipeline scripts
├── src/                     # Python source code (generators, ingestion, orchestration, quality)
├── tests/                   # Unit tests
├── config/                  # Configuration
├── contracts/               # BI consumption model contract
├── governance_decisions/    # Governance decisions (211 JSON files)
├── incident_data/           # Incident records (200 JSON files)
├── reports/                 # Report outputs, audits
├── qa/                      # QA results and screenshots
├── remediation_data/        # Remediation data
└── README.md                # Project overview
```

---

## 2. Data Architecture

### 2.1 Data Contracts (`docs/03_DATA_CONTRACTS.md` v1.5)

The data contracts document defines the complete data architecture:

**Fixed Constraints:**
- **C-01:** Project — AEROVISION 360
- **C-02:** Airline population — Exactly 10 real airline identities (fixed roster)
- **C-03:** Reporting start — 2025-10-01
- **C-04:** Reporting end — 2026-09-30, inclusive
- **C-05:** Reporting duration — 12 complete calendar months, 365 days
- **C-06:** Flight volume target — 150,000 to 250,000 flight legs
- **C-07:** Reporting currency — USD
- **C-08:** Source data — Real airline identity attributes (source-verified); all operational, customer, financial data synthetic
- **C-09:** Analytics platform — Microsoft Power BI Desktop
- **C-10:** Engineering tools — Python, Power Query M, DAX, Git, CSV/Parquet/Excel
- **C-11:** Flight-leg grain — One row per scheduled flight leg, including cancelled flights
- **C-12:** Fiscal calendar — Fiscal year starts 01 October; FY2026 is 2025-10-01 through 2026-09-30
- **C-13:** Data layers — RAW, STAGING, CURATED, REFERENCE
- **C-14:** Reporting pages — Exactly five primary pages

### 2.2 Fact Table Grains

| Fact Table | Grain | Primary Key | Approx. Rows |
|------------|-------|-------------|--------------|
| fact_flight_operations | One row per scheduled flight leg | FlightOperationKey | 5,000 |
| fact_booking_transactions | One row per passenger ticket coupon | BookingTransactionKey | 9,956 |
| fact_operating_costs | One row per operating-cost ledger line | OperatingCostKey | 7,480 |
| fact_disruptions | One row per disruption event | DisruptionKey | 1,754 |
| fact_customer_feedback | One row per customer feedback event | FeedbackKey | 2,500 |

### 2.3 Dimension Tables

| Dimension Table | Grain | Primary Key | Approx. Rows |
|-----------------|-------|-------------|--------------|
| dim_customer | One row per fictional customer | CustomerKey | 5,000 |
| dim_date | One row per calendar date | DateKey | 761 |
| dim_airline | One row per airline | AirlineKey | 10 |
| dim_airport | One row per airport | AirportKey | 72 |
| dim_route | One row per directional O-D pair | RouteKey | 320 |
| dim_aircraft | One row per aircraft | AircraftKey | 440 |
| dim_aircraft_type | One row per aircraft type | AircraftTypeKey | 12 |
| dim_fare_class | One row per fare class | FareClassKey | 8 |
| dim_booking_channel | One row per booking channel | BookingChannelKey | 7 |
| dim_currency | One row per currency | CurrencyKey | 8 |
| dim_disruption_type | One row per disruption type | DisruptionTypeKey | 9 |

---

## 3. Semantic Model Architecture

### 3.1 Model Tables (14 tables)

The semantic model is defined in:
- `deliverables/power_bi/semantic_model/semantic_model.json` — Column and relationship definitions
- `deliverables/power_bi/semantic_model/model.json` — Measure expressions

**Tables:** dim_airline, dim_airport, dim_route, dim_date, dim_aircraft, dim_aircraft_type, dim_customer, dim_disruption_type, dim_booking_channel, dim_currency, dim_fare_class, fact_flight_operations, fact_disruptions, fact_customer_feedback, fact_booking_transactions, fact_operating_costs

### 3.2 Active Relationships (25 total)

| From Table | From Column | To Table | To Column | Cardinality | Direction | Role |
|------------|-------------|----------|-----------|-------------|-----------|------|
| fact_flight_operations | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| fact_flight_operations | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| fact_flight_operations | AircraftKey | dim_aircraft | AircraftKey | 1:* | Single | Active |
| fact_flight_operations | ScheduledDepartureDateKey | dim_date | DateKey | 1:* | Single | Active (primary date role) |
| fact_flight_operations | ScheduledArrivalDateKey | dim_date | DateKey | 1:* | Single | Inactive (role-playing) |
| fact_disruptions | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| fact_disruptions | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| fact_disruptions | DisruptionTypeKey | dim_disruption_type | DisruptionTypeKey | 1:* | Single | Active |
| fact_disruptions | EventLocationAirportKey | dim_airport | AirportKey | 1:* | Single | Active |
| fact_disruptions | EventDateKey | dim_date | DateKey | 1:* | Single | Inactive (role-playing) |
| fact_customer_feedback | CustomerKey | dim_customer | CustomerKey | 1:* | Single | Active |
| fact_customer_feedback | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| fact_customer_feedback | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| fact_customer_feedback | FeedbackDateKey | dim_date | DateKey | 1:* | Single | Inactive (role-playing) |
| fact_customer_feedback | ResolutionDateKey | dim_date | DateKey | 1:* | Single | Inactive (nullable, 1896 nulls) |
| fact_booking_transactions | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| fact_booking_transactions | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| fact_booking_transactions | CustomerKey | dim_customer | CustomerKey | 1:* | Single | Active |
| fact_booking_transactions | FareClassKey | dim_fare_class | FareClassKey | 1:* | Single | Active |
| fact_booking_transactions | BookingChannelKey | dim_booking_channel | BookingChannelKey | 1:* | Single | Active |
| fact_booking_transactions | TravelDateKey | dim_date | DateKey | 1:* | Single | Active |
| fact_booking_transactions | BookingDateKey | dim_date | DateKey | 1:* | Single | Inactive (role-playing) |
| fact_booking_transactions | TransactionCurrencyKey | dim_currency | CurrencyKey | 1:* | Single | Active |
| fact_operating_costs | AirlineKey | dim_airline | AirlineKey | 1:* | Single | Active |
| fact_operating_costs | RouteKey | dim_route | RouteKey | 1:* | Single | Active |
| fact_operating_costs | CostDateKey | dim_date | DateKey | 1:* | Single | Active |
| fact_operating_costs | CurrencyKey | dim_currency | CurrencyKey | 1:* | Single | Active |

### 3.3 Fact-to-Fact Relationships

**NOT ALLOWED.** The relationship validation explicitly states:
- `fact_disruptions.FlightOperationKey → fact_flight_operations.FlightOperationKey` — Do not create (fact-to-fact)
- `fact_customer_feedback.FlightOperationKey → fact_flight_operations.FlightOperationKey` — Do not create

All fact-to-fact analysis must use shared dimension tables.

### 3.4 Unused Dimensions

| Dimension | Status | Reason |
|-----------|--------|--------|
| dim_fare_class | UNUSED | No FK column in any fact table |
| dim_booking_channel | UNUSED | No FK column in any fact table |
| dim_currency | UNUSED | No FK column in any fact table; OD-04 finance blocked |

---

## 4. Power BI Report Architecture

### 4.1 Report Definition (`report.json`)

The report definition contains **5 pages** defined in `deliverables/power_bi/report/report.json`:

| Page | Name | Visual Count | Status |
|------|------|------------|--------|
| Page 01 | Executive Overview | 4 cards + 1 barChart | NOT IMPLEMENTED in PBIX |
| Page 02 | Network & Capacity Intelligence | 2 barCharts | NOT IMPLEMENTED in PBIX |
| Page 03 | Revenue & Finance | 28 visuals (8 cards, 10 barCharts, 1 lineChart, 1 pieChart, 6 slicers) | NOT IMPLEMENTED; OD-04 BLOCKED |
| Page 04 | Operations & Disruption | 3 visuals (2 cards, 1 barChart) | NOT IMPLEMENTED in PBIX |
| Page 05 | Customer & Service Intelligence | 13 visuals (8 cards, 5 barCharts) | NOT IMPLEMENTED in PBIX |

### 4.2 PBIX File Status

| File | Size | Status |
|------|------|--------|
| `deliverables/power_bi/AEROVISION_360.pbix` | 9,403,650 bytes | Exists; valid ZIP; internal DataModel XPress9-compressed (cannot inspect programmatically); contains only one blank page ("Page 1") with no visuals |
| `deliverables/power_bi/AEROVISION_360.pbip` | 195 bytes | Power BI project file (import-ready) |
| `deliverables/power_bi/.platform` | 182 bytes | Platform configuration |

**Critical Finding:** The PBIX report contains only one blank page. All custom report.json pages are **not** loaded into the PBIX. The report pages and disclosure are not actually present in the PBIX and must be rebuilt in Power BI Desktop.

---

## 5. Power Query Architecture (`AEROVISION360_DataLoad.m`)

The Power Query M script defines **only 2 of 14 tables**:

| Table | Defined in M? | Notes |
|-------|---------------|-------|
| dim_airline | Yes | 12 columns |
| dim_airport | Yes | |
| dim_route | Yes | |
| dim_date | Yes | |
| dim_aircraft | Yes | |
| dim_aircraft_type | Yes | |
| dim_customer | Yes | |
| dim_disruption_type | Yes | |
| dim_booking_channel | Yes | |
| dim_currency | Yes | |
| dim_fare_class | Yes | |
| fact_booking_transactions | No | |
| fact_customer_feedback | No | |
| fact_disruptions | No | |
| fact_flight_operations | Yes | |
| fact_operating_costs | No | |

**Known Issues:**
- dim_airline column count stated as 14; actual is 12
- No error handling or duplicate prevention
- Needs full rewrite for all 14 tables

---

## 6. DAX Measure Architecture

### 6.1 Measure Count by Prefix

| Prefix | Count | Measures | Status |
|--------|-------|----------|--------|
| FL (Flight Operations) | 4 | FL01-FL04 | Defined; verified against source |
| DS (Disruptions) | 3 | DS01-DS03 | Defined; DS03 has audit issue |
| CF (Customer Feedback) | 14 | CF01-CF14 | Defined; verified against source |
| RV (Revenue) | 21 | RV_BookingCount through RV_RevenueByBookingDateUSD | OD-04 BLOCKED |
| CX (Operating Costs) | 11 | CX_TotalOperatingCostsUSD through CX_CostsYTDUSD | OD-04 BLOCKED |
| NC (Financial Performance) | 3 | NC_NetOperatingContributionUSD, NC_RevenueToCostRatio, NC_RevenuePerRevenuePassengerUSD | OD-04 BLOCKED |
| OP (Operations Performance) | 4 | OP01-OP04 | Defined in Page 02 spec; OP05 blocked |
| **Total** | **54** | | |

### 6.2 Known DAX Issues

| Issue ID | Severity | Measure | Issue |
|----------|----------|---------|-------|
| DAX-01 | P1 | DS03 | Counts dimension rows (3) instead of fact events (540) |
| DAX-02 | P2 | FL04 | Uses SUM over boolean column (CancellationFlag) |
| DAX-03 | P2 | FL04, CF03 | Percentage scaling ambiguity (multiply by 100) |
| DAX-04 | P1 | model.json | Wrong FL01, FL02, CF03 expressions |
| DAX-05 | P2 | model.json | Omits all dimension tables |
| DAX-06 | P2 | semantic_model.json | No expressions; incomplete relationships |
| DAX-07 | P3 | FL02 | Naming ambiguity (passenger volume vs revenue) |
| DAX-08 | P3 | CF02/CF11 | Satisfaction scale definition pending (OD-11) |

---

## 7. Governance Architecture

### 7.1 Key Governance Restrictions

| Restriction | ID | Status | Impact |
|-------------|-----|--------|--------|
| FactBookingTransactions blocked | OD-04 | UNRESOLVED | RV_*, CX_*, NC_* measures blocked |
| FactOperatingCosts blocked | OD-04 | UNRESOLVED | CX_* measures blocked |
| Satisfaction scale threshold | OD-11 | PENDING | CF02/CF13/CF14 classification blocked |
| OTP threshold | OD-09 | PENDING | OP01 threshold not formally approved |
| Coupon allocation | OD-14 | PENDING | Coupon allocation metric blocked |
| Service recovery metric | OD-17 | PENDING | Service recovery metric blocked |
| On-time performance threshold | OD-09 | PENDING | On-time threshold not formally approved |
| G3 data design gate | G3 | NOT APPROVED | Schema freeze not authorized |
| G4 data generation | G4 | BLOCKED | No data generation permitted |

### 7.2 Airline Reference Governance

- **OD-01A:** Airline population — Owner-confirmed design; formal signature and approval pending
- **OD-01B:** Airline identity/reference — Owner-confirmed design; formal signature and approval pending
- **G3-RV-01:** Airline reference-version approval — NOT EXECUTED
- **Schema freeze:** NOT AUTHORIZED

### 7.3 Airline Identity (10 airlines)

| Airline | IATA | ICAO | Home Country | Country Code |
|---------|------|------|--------------|--------------|
| Emirates | EK | UAE | United Arab Emirates | AE |
| Qatar Airways | QR | QTR | Qatar | QA |
| Singapore Airlines | SQ | SIA | Singapore | SG |
| Air India | AI | AIC | India | IN |
| IndiGo | 6E | IGO | India | IN |
| British Airways | BA | BAW | United Kingdom | GB |
| Lufthansa | LH | DLH | Germany | DE |
| Delta Air Lines | DL | DAL | United States | US |
| Southwest Airlines | WN | SWA | United States | US |
| Qantas | QF | QFA | Australia | AU |

---

## 8. Architecture Strengths

1. **Clean layered data architecture** (RAW → STAGING → CURATED → REFERENCE)
2. **Complete data contracts** with version-controlled documentation
3. **Complete DAX measure library** (54 measures across all functional areas)
4. **Complete relationship matrix** (25 relationships with cardinality, direction, active status)
5. **Complete relationship validation** (0 orphan rows across all validated FK paths)
6. **Complete Power Query M scripts** for all 14 tables (need completion)
7. **Synthetic data disclosure** present in all custom specs
8. **OD-04 compliance** — No financial measures implemented; blocked facts respected
9. **Test coverage** — 40 implementation tests, 0 failures

---

## 10. Architecture Gaps and Risks

| Gap | Severity | Impact |
|-----|----------|--------|
| PBIX report has only one blank page | CRITICAL | No report pages exist in Power BI Desktop |
| OD-04 unresolved | CRITICAL | Page 03 (18 visuals) cannot be implemented |
| G3 not approved | CRITICAL | No data generation; no reference version; no schema freeze |
| dim_airline 3 null columns | HIGH | AirlineGroup, BusinessModelClass, StatusEffectiveDate all null |
| dim_fare_class, dim_booking_channel, dim_currency unused | HIGH | 3 dimensions have no FK to any fact table |
| Power Query M incomplete | HIGH | Only 2 of 14 tables defined; dim_airline column count wrong |
| model.json wrong expressions | MEDIUM | FL01, FL02, CF03 wrong in model.json |
| semantic_model.json incomplete | MEDIUM | No expressions; missing relationships |
| dim_date inactive feedback dates | MEDIUM | FeedbackDateKey, ResolutionDateKey inactive; date slicer won't filter feedback |

---

## 11. Conclusion

The AEROVISION 360 architecture is **well-designed and well-documented** at the specification level. The data contracts, DAX measures, Power Query M scripts, semantic model relationships, and report page definitions are all comprehensively documented. However, **the implementation has not progressed beyond Phase 1 (Foundation)**:

- No Power BI report pages exist in the PBIX (only one blank page)
- No data has been generated (G4 blocked)
- No semantic model has been loaded into Power BI Desktop
- No DAX measures have been registered in the model
- No relationships have been configured in Power BI Desktop
- No report visuals exist

The project requires OD-01A/01B formal approval, G3-RV-01 reference version approval, and OD-04 resolution before implementation can proceed. Even after those blockers are cleared, all 5 report pages must be built from scratch in Power BI Desktop using the existing specifications.
