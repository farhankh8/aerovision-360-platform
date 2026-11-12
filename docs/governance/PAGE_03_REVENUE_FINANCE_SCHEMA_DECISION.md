# GOV-D-04 Schema Decision — FactBookingTransactions and FactOperatingCosts

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** PAGE_03-SCHEMA-2026-11-07-001  
**Document Type:** Owner Decision Draft — Fact Table Schema Design  
**Status:** PROPOSED — OWNER DECISION REQUIRED — NOT APPROVED  
**Prepared:** 2026-11-07  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Decision Identification

| Field | Value |
|---|---|
| Decision ID | OD-04-SCHEMA-2026-11-07-001 |
| Decision Title | FactBookingTransactions and FactOperatingCosts Schema Design |
| Decision Status | PROPOSED — OWNER DECISION REQUIRED — NOT APPROVED |
| Prepared Date | 2026-11-07 |
| Prepared By | Enterprise Data Governance Architect (non-independent) |
| Related Decisions | OD-04a through OD-04f (owner-confirmed); GOV-D-07 (ManifestHash Canonicalization, separate decision) |

---

## 2. Existing Evidence Inspected

| File | Location | Relevance |
|---|---|---|
| `docs/governance/OD04_OWNER_DECISION_RECORD.md` | `docs/governance/` | OD-04a through OD-04f owner-confirmed; OD-04g formal approval pending |
| `docs/governance/OD04_OWNER_DECISION_BRIEF.md` | `docs/governance/` | OD-04 decision brief |
| `docs/OD04_OWNER_DECISION_PACKAGE.md` | `docs/` | OD-04 decision package with decision questions |
| `docs/03_DATA_CONTRACTs.md` | `docs/` | Sections 10 (currency), 14 (decisions); Section 2.1 (airline roster) |
| `docs/PAGE_03_REVENUE_FINANCE_READINESS.md` | `docs/` | Page 03 blocked by OD-04; no financial fact tables exist |
| `data/03_curated/dim_currency.csv` | `data/03_curated/` | 8 currencies; USD is reporting currency |
| `data/03_curated/dim_airline.csv` | `data/03_curated/` | 10 airlines with AirlineKey, AirlineIATACode, AirlineICAOCode |
| `data/03_curated/dim_route.csv` | `data/03_curated/` | Route definitions |
| `data/03_curated/dim_date.csv` | `data/03_curated/` | Date dimension with DateKey as Int64 YYYYMMDD |

---

## 4. Owner Confirmed Decisions (OD-04a through OD-04f)

| Decision ID | Decision | Accepted Value |
|---|---|---|
| OD-04a | Currency scope | All 8 existing DimCurrency currencies: AED, QAR, SGD, INR, GBP, EUR, USD, AUD |
| OD-04b | Exchange-rate convention | USD per one unit; exact-date lookup; 6 decimal places; no forward-fill; round final converted amount to 2 decimals |
| OD-04c | Rate source | `AEROVISION-360-SYNTHETIC-FX-V1` |
| OD-04d | Rate version | `FX-YYYY-MM-DD-NNN` date-based versioning |
| OD-04e | Missing-date behaviour | No forward-fill; missing exact-date rate quarantines the affected row |
| OD-04f | Rate-generation methodology | Deterministic algorithmic generation; fixed seed; documented parameters |

---

## 4. Owner-Approved FactBookingTransactions Schema

### 4.1 Business Purpose

Record one row per scheduled flight booking transaction. Each row represents a single booking transaction for a flight leg with monetary amounts in the original transaction currency converted to USD using the approved canonicalization method (OD-04b through OD-04f).

### 4.2 Schema

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
| FlightStatus | String(20) | No | From FactFlightOperations |
| DepartureDelayMinutes | Int64 | No | From FactFlightOperations |
| ArrivalDelayMinutes | Int64 | No | From FactFlightOperations |
| BlockMinutes | Int64 | No | From FactFlightOperations |
| CancellationFlag | Boolean | No | Duplicates FactFlightOperations flag |
| CompletionFlag | Boolean | No | Duplicates FactFlightOperations flag |
| OnTimeFlag | Boolean | No | Duplicates FactFlightOperations flag |
| OnTimeArrivalFlag | Boolean | No | Duplicates FactFlightOperations flag |
| OriginalCurrencyKey | Int64 | No | Foreign key → DimCurrency.CurrencyKey |
| OriginalAmount | Decimal(18,2) | No | Original booking amount in original currency |
| ExchangeRateToUSD | Decimal(18,6) | No | Exchange rate from SourceCurrency to USD |
| RateDateKey | Int64 | No | Foreign key → dim_date.DateKey (rate date) |
| RateVersion | String(20) | No | Reference version identifier |
| NetPassengerRevenueUSD | Decimal(18,2) | No | OriginalAmount × ExchangeRateToUSD, rounded to 2 decimals |

### 4.4 Business Rules

| Rule ID | Rule Statement |
|---|---|
| FBK-01 | BookingTransactionKey is unique per manifest version |
| FBK-02 | BookingID is unique per manifest version |
| FBK-03 | RevenuePassengers + NonRevenuePassengers = BookedPassengers |
| FBK-04 | BookedPassengers ≤ AvailableSeats |
| FBK-05 | FlightStatus ∈ {Scheduled, Departed, Arrived, Cancelled, Delayed} |
| FBK-06 | CancellationFlag implies CompletionFlag = FALSE |
| FBK-07 | DepartureDelayMinutes, ArrivalDelayMinutes, BlockMinutes come from FactFlightOperations |
| FBK-08 | OnTimeFlag, OnTimeArrivalFlag come from FactFlightOperations |

---

## 5. FactOperatingCosts Schema Proposal

### 5.1 Business Purpose

Record one row per scheduled flight operating cost transaction. Each row represents a single operating cost entry per flight leg with monetary amounts in the original transaction currency converted to USD using the approved canonicalization method.

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
| IsSynthetic | Boolean | No | Always TRUE for synthetic reference data |
| RateVersion | String(20) | No | Reference version identifier |
| CancellationFlag | Boolean | No | Duplicates FactFlightOperations flag |
| CompletionFlag | Boolean | No | Duplicates FactFlightOperations flag |

### 5.3 Business Rules

| Rule ID | Rule Statement |
|---|---|
| FOC-01 | OperatingCostKey is unique per manifest version |
| FOC-02 | OperatingCostID is unique per manifest version |
| FOC-03 | CostAmountUSD = Round(CostAmountOriginal × ExchangeRateToUSD, 2) |
| FOC-04 | CurrencyKey resolves to DimCurrency.CurrencyKey |
| FOC-05 | ExchangeRateToUSD comes from ref_exchange_rates.csv for CostDateKey |
| FOC-06 | CancellationFlag duplicates FactFlightOperations flag |
| FOC-08 | CompletionFlag duplicates FactFlightOperations flag |

---

## 6. Restrictions

| Restriction | Status |
|---|---|
| Modify OD-01A/OD-01B | NOT MODIFIED |
| Modify contract v1.5 | NOT MODIFIED |
| Modify Power Query files | NOT MODIFIED |
| Modify DAX measures | NOT MODIFIED |
| Modify semantic model | NOT MODIFIED |
| Modify Power BI/PBIX | NOT MODIFIED |
| Generate financial data | NOT CREATED |
| Create Power Query queries | NOT CREATED |
| Generate reference data | NOT CREATED |
| Authorize G3 or G4 | NOT AUTHORIZED |
| Execute G3-RV-01 | NOT EXECUTED |
| Execute T-78 | NOT EXECUTED |
| Freeze schema | NOT AUTHORIZED |

---

## 7. End of Decision Record

This document records the proposed schema design for FactBookingTransactions and FactOperatingCosts. No source files, data, DAX, Power Query, semantic model, Power BI, or other project artifacts were modified during its creation. No signature, approval date, reviewer identity, or approval evidence has been created. The schema is pending owner decision.