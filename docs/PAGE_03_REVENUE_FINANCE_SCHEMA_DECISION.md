# AEROVISION 360 — FactBookingTransactions and FactOperatingCosts Schema Decision

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** PAGE_03-SCHEMA-2026-11-07-001  
**Document Type:** Owner Decision Draft — Financial Fact Table Schema Design  
**Status:** PROPOSED — OWNER DECISION REQUIRED  
**Prepared:** 2026-11-07  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Decision Identification

| Field | Value |
|---|---|
| Decision ID | OD-04-SCHEMA-2026-11-07-001 |
| Decision Title | FactBookingTransactions and FactOperatingCosts Schema Design |
| Decision Status | PROPOSED — OWNER DECISION REQUIRED — NOT APPROVED |
| Prepared By | Enterprise Data Governance Architect (non-independent) |
| Related Decisions | OD-04a through OD-04f (owner-confirmed); GOV-D-07 (ManifestHash Canonicalization, separate decision) |

---

## 2. Existing Evidence Inspected

| Source Document | Location | Role |
|---|---|---|
| `docs/OD04_OWNER_DECISION_RECORD.md` | `docs/governance/` | OD-04a through OD-04f owner-confirmed; OD-04g formal approval pending |
| `docs/governance/OD04_OWNER_DECISION_BRIEF.md` | `docs/governance/` | OD-04 decision brief with proposed currency scope |
| `docs/OD04_OWNER_DECISION_PACKAGE.md` | `docs/` | OD-04 decision package with contract references |
| `docs/03_DATA_CONTRACTs.md` | `docs/` | Contract v1.5 DRAFT, Sections 10 (currency), Section 14 (decisions), Section 15 (gates) |
| `docs/PAGE_03_REVENUE_FINANCE_READINESS.md` | `docs/` | Page 03 readiness report confirming Page 03 blocked by OD-04 |
| `data/03_curated/dim_currency.csv` | `data/03_curated/` | 8 currencies: AED, QAR, SGD, INR, GBP, EUR, USD, AUD; USD is reporting currency |
| `data/03_curated/dim_airline.csv` | `data/03_curated/` | 10 airlines with AirlineKey, AirlineIATACode, AirlineICAOCode |
| `data/03_curated/dim_route.csv` | `data/03_curated/` | Route dimension with RouteKey, OriginAirportKey, DestinationAirportKey |
| `data/03_curated/dim_date.csv` | `data/03_curated/` | Date dimension with DateKey as Int64 YYYYMMDD |

---

## 3. OD-04g Formal Approval Status

**Important correction:** The owner has explicitly approved OD-04g in conversation on 2026-11-07. However, the existing `OD04_OWNER_DECISION_RECORD.md` still shows OD-04g as "PROPOSED — OWNER APPROVAL NOT YET GRANTED."

**Correction required:** Update `OD04_OWNER_DECISION_RECORD.md` to reflect that OD-04g formal approval was given by the project owner on 2026-11-07. Do not fabricate a signature or formal approval date beyond what the owner has explicitly confirmed.

---

## 4. FactBookingTransactions Schema Proposal

### 4.1 Business Purpose

Record one row per scheduled flight booking transaction. Each row represents a single booked flight leg with monetary attributes denominated in the original transaction currency and converted to USD using the approved canonicalization method.

### 4.2 Proposed Schema

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| BookingTransactionKey | Int64 | No | Primary key, surrogate key |
| BookingID | String(20) | No | Business identifier, unique per booking transaction |
| AirlineKey | Int64 | No | Foreign key → DimAirline.AirlineKey |
| FlightOperationKey | Int64 | No | Foreign key → FactFlightOperations.FlightOperationKey |
| RouteKey | Int64 | No | Foreign key → dim_route.RouteKey |
| BookingDateKey | Int64 | No | Foreign key → dim_date.DateKey |
| TravelDateKey | Int64 | No | Foreign key → dim_date.DateKey |
| AvailableSeats | Int64 | No | Positive integer |
| BookedPassengers | Int64 | No | Positive integer |
| RevenuePassengers | Int64 | No | Positive integer, ≤ BookedPassengers |
| NonRevenuePassengers | Int64 | No | Positive integer, RevenuePassengers + NonRevenuePassengers = BookedPassengers |
| FlightStatus | String(20) | No | Flight status from fact_flight_operations |
| DepartureDelayMinutes | Int64 | No | Duplicate of FactFlightOperations value |
| ArrivalDelayMinutes | Int64 | No | Duplicate of FactFlightOperations value |
| BlockMinutes | Int64 | No | Duplicate of FactFlightOperations value |
| CancellationFlag | Boolean | No | Duplicates FactFlightOperations flag |
| CompletionFlag | Boolean | No | Duplicates FactFlightOperations flag |
| OnTimeFlag | Boolean | No | Duplicates FactFlightOperations flag |
| OnTimeArrivalFlag | Boolean | No | Duplicates FactFlightOperations flag |

### 4.3 Problems with Previous Proposal — Resolved

| Issue | Previous (Incorrect) | Correction |
|---|---|---|
| ManifestHash self-exclusion ambiguity | Ambiguous whether ManifestHash is removed or set to empty | `ManifestHash` property removed entirely before canonicalization (per GOV-D-07) |
| ManifestHash self-exclusion ambiguous | Unclear whether to set to "" or remove field | Property removed entirely before canonicalization |

---

## 4.3 Field-by-Field Specification

| Field | Type | Nullable | Description |
|---|---|---|---|
| BookingTransactionKey | Int64 | No | Primary key |
| BookingID | String(20) | No | Business identifier |
| AirlineKey | Int64 | No | Foreign key → DimAirline.AirlineKey |
| FlightOperationKey | Int64 | No | Foreign key → FactFlightOperations.FlightOperationKey |
| RouteKey | Int64 | No | Foreign key → dim_route.RouteKey |
| BookingDateKey | Int64 | No | Foreign key → dim_date.DateKey |
| TravelDateKey | Int64 | No | Foreign key → dim_date.DateKey |
| AvailableSeats | Int64 | No | Positive integer |
| BookedPassengers | Int64 | No | Positive integer |
| RevenuePassengers | Int64 | No | Positive integer, ≤ BookedPassengers |
| NonRevenuePassengers | Int64 | No | Positive integer, RevenuePassengers + NonRevenuePassengers = BookedPassengers |
| FlightStatus | String(20) | No | From fact_flight_operations |
| DepartureDelayMinutes | Int64 | No | From fact_flight_operations |
| ArrivalDelayMinutes | Int64 | No | From fact_flight_operations |
| BlockMinutes | Int64 | No | From fact_flight_operations |
| CancellationFlag | Boolean | No | From fact_flight_operations |
| CompletionFlag | Boolean | No | From fact_flight_operations |
| OnTimeFlag | Boolean | No | From fact_flight_operations |
| OnTimeArrivalFlag | Boolean | No | From fact_flight_operations |

### 4.4 Business Rules

| Rule | Rule Statement |
|---|---|
| FBK-01 | BookingTransactionKey is unique per manifest version |
| FBK-02 | BookingID is unique per manifest version |
| FBK-03 | RevenuePassengers + NonRevenuePassengers = BookedPassengers |
| FBK-04 | BookedPassengers ≤ AvailableSeats |
| FBK-05 | FlightStatus ∈ {Scheduled, Departed, Arrived, Cancelled, Delayed} |
| FBK-06 | CancellationFlag implies CompletionFlag = FALSE |
| FBK-07 | DepartureDelayMinutes, ArrivalDelayMinutes, BlockMinutes come from FactFlightOperations |
| FBK-08 | OnTimeFlag and OnTimeArrivalFlag come from FactFlightOperations |

---

## 4. Field-by-Field Specification

### 4.4.1 FlightOperationsKey
- **Type:** Int64
- **Nullability:** No
- **Description:** Foreign key to FactFlightOperations.FlightOperationKey. Links the booking to the specific flight leg.

### 4.4.2 AirlineKey
- **Type:** Int64
- **Nullability:** No
- **Description:** Foreign key to DimAirline.AirlineKey. Identifies the operating airline.

### 4.4.3 RouteKey
- **Type:** Int64
- **Nullability:** No
- **Description:** Foreign key to dim_route.RouteKey. Identifies the route of the booking.

### 4.4.4 BookingDateKey
- **Type:** Int64
- **Nullability:** No
- **Description:** Foreign key to dim_date.DateKey. The date the booking was made.

### 4.4.5 TravelDateKey
- **Type:** Int64
- **Nullability:** No
- **Description:** Foreign key to dim_date.DateKey. The date of travel for the booking.

### 4.4.6 AvailableSeats
- **Type:** Int64
- **Nullability:** No
- **Description:** Positive integer. Total seats available on the flight.

### 4.4.7 BookedPassengers
- **Type:** Int64
- **Nullability:** No
- **Description:** Positive integer. Total passengers booked on the flight.

### 4.4.8 RevenuePassengers
- **Type:** Int64
- **Nullability:** No
- **Description:** Positive integer. Revenue-paying passengers on the flight.

### 4.4.9 NonRevenuePassengers
- **Type:** Int64
- **Nullability:** No
- **Description:** Positive integer. Non-revenue passengers on the flight.

### 4.4.10 FlightStatus
- **Type:** String(20)
- **Nullability:** No
- **Description:** From FactFlightOperations. Values: Scheduled, Departed, Arrived, Cancelled, Delayed.

### 4.4.11 DepartureDelayMinutes
- **Type:** Int64
- **Nullability:** No
- **Description:** From FactFlightOperations. Departure delay in minutes.

### 4.4.12 ArrivalDelayMinutes
- **Type:** Int64
- **Nullability:** No
- **Description:** From FactFlightOperations. Arrival delay in minutes.

### 4.4.13 BlockMinutes
- **Type:** Int64
- **Nullability:** No
- **Description:** From FactFlightOperations. Block minutes for the flight.

### 4.4.14 CancellationFlag
- **Type:** Boolean
- **Nullability:** No
- **Description:** From FactFlightOperations. Cancellation flag.

### 4.4.15 CompletionFlag
- **Type:** Boolean
- **Nullability:** No
- **Description:** From FactFlightOperations. Completion flag.

### 4.4.16 OnTimeFlag
- **Type:** Boolean
- **Nullability:** No
- **Description:** From FactFlightOperations. On-time departure flag.

### 4.4.17 OnTimeArrivalFlag
- **Type:** Boolean
- **Nullability:** No
- **Description:** From FactFlightOperations. On-time arrival flag.

---

## 5. FactOperatingCosts Schema Proposal

### 5.1 Business Purpose

Record one row per scheduled flight operating cost transaction. Each row represents a single operating cost entry per flight leg with monetary amounts in the original transaction currency and converted to USD using the approved canonicalization method.

### 5.2 Proposed Schema

| Column | Type | Nullable | Description |
|---|---|---|---|
| OperatingCostKey | Int64 | No | Primary key |
| OperatingCostID | String(20) | No | Business identifier, unique per operating cost entry |
| AirlineKey | Int64 | No | Foreign key → DimAirline.AirlineKey |
| FlightOperationKey | Int64 | No | Foreign key → FactFlightOperations.FlightOperationKey |
| RouteKey | Int64 | No | Foreign key → dim_route.RouteKey |
| CostDateKey | Int64 | No | Foreign key → dim_date.DateKey |
| CostCategory | String(50) | No | Cost category classification |
| CostSubcategory | String(50) | No | Cost subcategory |
| CostAmountOriginal | Decimal(18,2) | No | Original cost amount in original currency |
| OriginalCurrencyKey | Int64 | No | Foreign key → DimCurrency.CurrencyKey |
| ExchangeRateToUSD | Decimal(18,6) | No | Exchange rate from source currency to USD |
| CostAmountUSD | Decimal(18,2) | No | Cost amount in USD |
| RateSource | String(50) | No | Source of exchange rate |
| RateVersion | String(20) | No | Reference version of exchange rate |
| IsSynthetic | Boolean | No | Always TRUE for synthetic reference data |
| CancellationFlag | Boolean | No | Duplicates FactFlightOperations flag |
| CompletionFlag | Boolean | No | Duplicates FactFlightOperations flag |

### 5.3 Business Rules

| Rule | Rule Statement |
|---|---|
| FOC-01 | OperatingCostKey is unique per manifest version |
| FOC-02 | OperatingCostID is unique per manifest version |
| FOC-03 | CostAmountUSD = OriginalCostAmount × ExchangeRateToUSD, rounded to 2 decimals |
| FOC-04 | CurrencyKey resolves to DimCurrency.CurrencyKey |
| FOC-05 | ExchangeRateToUSD comes from ref_exchange_rates.csv for CostDateKey |
| FOC-06 | CancellationFlag implies CompletionFlag = FALSE |
| FOC-07 | CancellationFlag duplicates FactFlightOperations flag |
| FOC-08 | CompletionFlag duplicates FactFlightOperations flag |

### 5.3 Field-by-Field Specification

| Field | Type | Nullable | Description |
|---|---|---|---|
| OperatingCostKey | Int64 | No | Primary key |
| OperatingCostID | String(20) | No | Business identifier |
| AirlineKey | Int64 | No | Foreign key → DimAirline.AirlineKey |
| FlightOperationKey | Int64 | No | Foreign key → FactFlightOperations.FlightOperationKey |
| RouteKey | Int64 | No | Foreign key → dim_route.RouteKey |
| CostDateKey | Int64 | No | Foreign key → dim_date.DateKey |
| CostCategory | String(50) | No | Cost category classification |
| CostSubcategory | String(50) | No | Cost subcategory |
| CostAmountOriginal | Decimal(18,2) | No | Original cost amount in original currency |
| OriginalCurrencyKey | Int64 | No | Foreign key → DimCurrency.CurrencyKey |
| ExchangeRateToUSD | Decimal(18,6) | No | Exchange rate from source currency to USD |
| CostAmountUSD | Decimal(18,2) | No | Cost amount in USD |
| IsSynthetic | Boolean | No | Always TRUE for synthetic reference data |
| RateVersion | String(20) | No | Reference version identifier |
| CancellationFlag | Boolean | No | Duplicates FactFlightOperations flag |
| CompletionFlag | Boolean | No | Duplicates FactFlightOperations flag |

---

## 6. Relationship and Filter Context

| Table | Relationship | Filter Context |
|---|---|---|
| FactBookingOperations | DimAirline.AirlineKey → FactBookingOperations.AirlineKey | Single filter path |
| FactBookingOperations | DimRoute.RouteKey → FactBookingOperations.RouteKey | Single filter path |
| FactBookingOperations | DimDate.DateKey → FactBookingOperations.BookingDateKey | Single filter path |
| FactBookingOperations | DimDate.DateKey → FactBookingOperations.TravelDateKey | Single filter path |
| FactBookingOperations | DimCurrency.CurrencyKey → FactBookingOperations.CurrencyKey | Single filter path |
| FactOperatingCosts | DimAirline.AirlineKey → FactOperatingCosts.AirlineKey | Single filter path |
| FactOperatingCosts | DimRoute.RouteKey → FactOperatingCosts.RouteKey | Single filter path |
| FactOperatingCosts | DimCurrency.CurrencyKey → FactOperatingCosts.CurrencyKey | Single filter path |
| FactOperatingCosts | DimDate.DateKey → FactOperatingCosts.CostDateKey | Single filter path |

---

## 7. Implementation Restrictions

| Restriction | Status |
|---|---|
| Modify OD-01A/OD-01B | Not modified |
| Modify GOV-D-04 through GOV-D-08 | Not modified |
| Modify contract v1.5 | Not modified |
| Modify Power Query files | Not modified |
| Modify semantic model files | Not modified |
| Modify DAX measures | Not modified |
| Modify PBIX | Not modified |
| Generate financial CSV data | Not created |
| Create financial manifests | Not created |
| Authorize financial data generation | Not authorized |
| Freeze schema | Not authorized |
| Execute G3-RV-01 | Not executed |
| Authorize G3/G4 | Not authorized |

---

## 8. End of Decision Record

This document records the proposed schema design for FactBookingTransactions and FactOperatingCosts. No source files, data, DAX, Power Query, semantic model, Power BI, or other project artifacts were modified during its creation. No signature, approval date, or implementation authorization has been created. Owner decision is required before any implementation activity can begin.
