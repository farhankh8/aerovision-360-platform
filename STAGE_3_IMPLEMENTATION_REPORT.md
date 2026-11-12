# AEROVISION 360 — Stage 3: Semantic Model Engineering — Implementation Report

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Stage:** Stage 3 — Semantic Model Engineering  
**Date:** 2026-11-07  
**Owner:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Summary

Stage 3 is complete. Both financial fact tables (FactBookingTransactions, FactOperatingCosts) have been integrated into the existing semantic model architecture with proper relationships to DimAirline, DimRoute, DimDate, and DimCurrency. All 47 automated validation tests pass. No PBIX was modified. No source datasets were modified. No DAX measures were added (deferred to Stage 4 per OD-04). No Page 03 visuals were built.

The model grew from 14 to 16 tables. All existing tables, columns, relationships, and measures are unchanged (regression verified).

---

## 2. Files Created or Modified

### 2.1 Files modified

| File | Change |
|---|---|
| `deliverables/power_bi/semantic_model/semantic_model.json` | Added `fact_booking_transactions` and `fact_operating_costs` table definitions with columns, measures (empty), and relationships |
| `deliverables/power_bi/semantic_model/model.json` | Added `fact_booking_transactions` and `fact_operating_costs` table entries with empty measures arrays |

### 2.2 Files created (tests)

| File | Tests | Status |
|---|---|---|
| `tests/unit/test_stage3_semantic_model.py` | 47 | All PASSED |

### 2.3 Implementation report

| File |
|---|
| `STAGE_3_IMPLEMENTATION_REPORT.md` |

---

## 3. Tables Registered

| Table | Rows (source) | Columns | Grain | Primary Key | Measures |
|---|---|---|---|---|---|
| FactBookingTransactions | 9,956 | 45 | One row per passenger ticket coupon | BookingTransactionKey | 0 (deferred to Stage 4) |
| FactOperatingCosts | 7,480 | 18 | One row per operating-cost ledger line | OperatingCostKey | 0 (deferred to Stage 4) |

Total model tables: 16 (14 existing + 2 new).

---

## 4. Relationships Created

### 4.1 FactBookingTransactions → Dimensions (8 relationships)

| From Column | To Table | To Column | Role | Purpose |
|---|---|---|---|---|
| AirlineKey | dim_airline | AirlineKey | active | Operating airline of the coupon |
| RouteKey | dim_route | RouteKey | active | Booked route |
| CustomerKey | dim_customer | CustomerKey | active | Booking customer |
| FareClassKey | dim_fare_class | FareClassKey | active | Fare class |
| BookingChannelKey | dim_booking_channel | BookingChannelKey | active | Booking distribution channel |
| TravelDateKey | dim_date | DateKey | active | Travel date (primary date role for revenue) |
| BookingDateKey | dim_date | DateKey | inactive | Booking date (cohort analysis, USERELATIONSHIP) |
| TransactionCurrencyKey | dim_currency | CurrencyKey | active | Original transaction currency |

**Not a relationship:** FlightOperationKey (fact-to-fact prohibited per contract Section 8.5; logical reference only).

### 4.2 FactOperatingCosts → Dimensions (4 relationships)

| From Column | To Table | To Column | Role | Purpose |
|---|---|---|---|---|
| AirlineKey | dim_airline | AirlineKey | active | Cost-bearing airline |
| RouteKey | dim_route | RouteKey | active | Costed route |
| CostDateKey | dim_date | DateKey | active | Cost accounting date (primary date role) |
| CurrencyKey | dim_currency | CurrencyKey | active | Original cost currency |

**Not a relationship:** FlightOperationKey (fact-to-fact prohibited per contract Section 8.5; logical reference only).

---

## 5. Cardinality and Filter Direction

All relationships follow the established convention:
- **Cardinality:** 1:many (dimension → fact) — every relationship is from a fact surrogate key to a dimension primary key
- **Filter direction:** Single direction only (no bidirectional relationships)
- **Role:** `active` for primary date/primary dimension, `inactive` for secondary date roles

### 5.1 Date-Role Design (DimDate role-playing)

| Fact | Active Date Role | Inactive Date Roles |
|---|---|---|
| FactFlightOperations | ScheduledDepartureDateKey | ScheduledArrivalDateKey |
| FactDisruptions | (none active) | EventDateKey |
| FactCustomerFeedback | (none active) | FeedbackDateKey, ResolutionDateKey |
| FactBookingTransactions | TravelDateKey | BookingDateKey |
| FactOperatingCosts | CostDateKey | (none) |

DimDate has no outgoing relationships (pure dimension). Each fact has at most one active relationship to DimDate — no ambiguous paths.

### 5.2 No Ambiguous Filter Paths

- **No fact-to-fact relationships:** FlightOperationKey is carried as a logical reference only, not a model relationship
- **No circular dependencies:** All relationships flow from facts to dimensions only
- **No ambiguous airline path:** dim_aircraft → dim_airline is active (correct direction: aircraft filters airline), dim_airline does NOT filter dim_aircraft
- **No many-to-many relationships**

---

## 6. Financial Model Integrity

### 6.1 Dimension Key Resolution

All foreign keys resolve to dimension rows:
- FactBookingTransactions: 8 FKs all resolve (CustomerKey, AirlineKey, FlightOperationKey/logical, RouteKey, FareClassKey, BookingChannelKey, BookingDateKey, TravelDateKey, RateDateKey, TransactionCurrencyKey)
- FactOperatingCosts: 6 FKs all resolve (FlightOperationKey/logical, AirlineKey, RouteKey, CostDateKey, RateDateKey, CurrencyKey)

### 6.2 Original and Converted Amounts Preserved

| Table | Original Amount Columns | USD Amount Columns | Currency Key | Rate Date Key | Rate Version |
|---|---|---|---|---|---|
| FactBookingTransactions | BaseFareAmount, DiscountAmount, TaxAmount, FeeAmount, AncillaryRevenueAmount, RefundAmount, AncillaryRefundAmount, FeeRefundAmount, CancellationFeeAmount, NoShowFeeAmount | BaseFareUSD through NetAncillaryRevenueUSD | TransactionCurrencyKey | RateDateKey | RateVersion = FX-2026-11-04-001 |
| FactOperatingCosts | CostAmount (signed) | CostAmountUSD (signed) | CurrencyKey | RateDateKey | RateVersion = FX-2026-11-04-001 |

### 6.3 No Cross-Currency Aggregation

- Original-currency amounts carry a CurrencyKey referencing DimCurrency
- USD-converted amounts are available for aggregation
- ExchangeRateToUSD > 0 for all rows (no missing rates, no forward-fill)
- All rates use exact-date lookup (OD-04b/OD-04e)

### 6.4 Refunds, Reversals, Negative Adjustments

- Refunds stored as positive magnitudes (contract Section 10.4), subtracted in measure identities
- Cost reversals stored as negative CostAmount/CostAmountUSD
- All booking monetary amounts are non-negative (refunds are positive magnitudes)
- IsRefunded flag preserved for refund detection

### 6.5 Synthetic Provenance

- `SyntheticProvenance` column present on both fact tables
- Value: "Synthetic Simulation — Not Actual Airline Performance."
- Model disclosure field preserved

---

## 7. Model Validation Results

**Test execution:** `python -m pytest tests/unit/test_stage3_semantic_model.py` — **47 passed, 0 failed.**

| # | Test Category | Result |
|---|---|---|
| 1 | Table registration (both tables present, 16 total) | PASS |
| 2 | Model JSON / semantic model consistency | PASS |
| 3 | Existing tables unchanged (regression) | PASS |
| 4 | Column names match source datasets | PASS |
| 5 | Column count (45 + 18) | PASS |
| 6 | All required columns present | PASS |
| 7 | No column renaming | PASS |
| 8 | Primary-key uniqueness | PASS |
| 9 | Foreign-key relationships resolve | PASS |
| 10 | FK columns present in source | PASS |
| 11 | Relationship cardinality (1:many) | PASS |
| 12 | No many-to-many | PASS |
| 13 | Single-direction filtering | PASS |
| 14 | No fact-to-fact relationships | PASS |
| 15 | No circular date paths | PASS |
| 16 | DimDate role-playing (no outgoing rels) | PASS |
| 17 | No ambiguous airline paths | PASS |
| 18 | Date-role behavior (active/inactive) | PASS |
| 19 | Currency conversion lineage | PASS |
| 20 | No forward-fill exchange rates | PASS |
| 21 | Original + USD amounts present | PASS |
| 22 | No cross-currency aggregation | PASS |
| 23 | Refunds and reversals represented | PASS |
| 24 | Booking sign convention | PASS |
| 25 | Model schema validity | PASS |
| 26 | All tables have required fields | PASS |
| 27 | All relationships have required fields | PASS |
| 28 | Dimensions have no measures | PASS |
| 29 | Existing table columns unchanged | PASS |
| 30 | Existing relationships unchanged | PASS |
| 31 | Existing measures unchanged | PASS |
| 32-47 | Synthetic provenance, model disclosure, etc. | PASS |

---

## 8. Regression Protection for Existing 14 Tables

All existing tables verified unchanged:
- **Columns:** All original columns present (no removals or renames)
- **Relationships:** All existing relationship counts preserved (fact_flight_operations: 5, fact_disruptions: 5, fact_customer_feedback: 5)
- **Measures:** All existing measures unchanged (FL01-FL04, DS01-DS03, CF01-CF14)
- **DimDate:** No outgoing relationships (role-playing dimension preserved)

---

## 9. Governance Boundaries Observed

- **OD-04 remains owner-approved** — currency conventions applied
- **GOV-D-07 remains unapproved** — no ManifestHash canonicalization introduced
- **G3/G4 approval status unchanged** — not claimed
- **G3-RV-01 not executed** — not required for Stage 3
- **T-78 not executed** — not required for Stage 3
- **No DAX measures added** — deferred to Stage 4 (DAX file explicitly blocks financial measures: "OD-04: FactBookingTransactions / FactOperatingCosts are blocked; no revenue/cost measures defined.")
- **No Page 03 visuals built** — deferred to Stage 5
- **PBIX not modified** — only semantic model JSON files updated
- **Source CSV/Parquet files not modified**
- **Power Query integration not rebuilt** — Stage 2 outputs used as-is

---

## 10. Unresolved Blockers

| Blocker | Impact | Required Action |
|---|---|---|
| **GOV-D-07 ManifestHash canonicalization** is a REVISED DRAFT, not approved | No canonical ManifestHash in model metadata | Owner approval of GOV-D-07 required |
| **`ref_cost_classification.csv` does not exist** | Cost classification reference integrity (T-66) cannot be validated against model | `ref_cost_classification.csv` must be created and approved (OD-13 pending) |
| **`ref_airline_sources.csv` does not exist** | Airline identity provenance (T-75/T-76/T-78) cannot be validated | Airline source verification and reference approval (OD-01B / G3-RV-01) pending |
| **No financial DAX measures** | Revenue/cost KPIs cannot be computed yet | Stage 4 (Financial DAX) — measures must be added after semantic model is approved |

None of these blockers prevent Stage 3 completion.

---

## 11. Restrictions Observed

Per the Stage 3 strict scope:
- PBIX: **Not modified**
- Pages 01, 02, 04: **Not modified**
- Page 03 visuals: **Not built**
- Financial DAX measures: **Not added**
- Source CSV/Parquet files: **Not modified**
- Power Query integration: **Not rebuilt**
- Unrelated dimensions/measures: **Not changed**

---

## 12. Next Stage Readiness

Stage 3 is complete and all 47 tests pass. The semantic model now includes both financial fact tables with correct relationships, date roles, currency lineage, and financial aggregation safety. The model is ready for Stage 4 (Financial DAX measures).

**Request: Owner review of Stage 3 results before authorizing Stage 4.**
