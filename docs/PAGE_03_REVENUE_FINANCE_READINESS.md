# AEROVISION 360 — Page 03 Revenue & Finance Implementation Readiness Report

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** PAGE_03-READINESS-2026-11-07-001  
**Document Type:** Implementation Readiness Report — NOT IMPLEMENTATION AUTHORIZATION  
**Prepared:** 2026-11-07  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Executive Readiness Verdict

**Page 03 Revenue & Finance is NOT IMPLEMENTABLE with existing data.**

All 18 revenue/finance visuals are blocked by the absence of two financial fact tables (`FactBookingTransactions` and `FactOperatingCosts`) and one reference file (`ref_exchange_rates.csv`), all of which are blocked by **OD-04 (Exchange-Rate Policy)**, which is **PROPOSED — OWNER APPROVAL REQUIRED**.

No monetary data exists anywhere in the project. Passenger volume (FL02 = 218,413 RevenuePassengers) is explicitly **not** revenue and must never be presented as such on Page 03.

**Recommendation:** Do not build Page 03 visuals. Do not create financial DAX measures. Do not attempt Power BI financial visuals. Return to Page 03 only after OD-04 is formally approved and the financial fact tables exist in the curated layer.

---

## 2. Existing Verified Tables and Columns

The following curated tables exist in `data/03_curated/` and are loaded via `src/utilities/hashing.py`-compatible CSV files:

| Dataset | Path | Rows | Columns | Financial Relevance |
|---|---|---|---|---|
| dim_airline | `data/03_curated/dim_airline.csv` | 10 | 12 | Dimension only; no financial attributes |
| dim_airport | `data/03_curated/dim_airport.csv` | 72 | 11 | Dimension only; no financial attributes |
| dim_route | `data/03_curated/dim_route.csv` | 320 | 9 | Dimension only; no financial attributes |
| dim_date | `data/03_curated/dim_date.csv` | 761 | 19 | Dimension only; date dimension for time-series |
| dim_aircraft | `data/03_curated/dim_aircraft.csv` | 440 | 9 | Dimension only; no financial attributes |
| dim_aircraft_type | `data/03_curated/dim_aircraft_type.csv` | 12 | 8 | Dimension only; no financial attributes |
| dim_customer | `data/03_curated/dim_customer.csv` | 785 | 8 | Dimension only; no financial attributes |
| dim_disruption_type | `data/03_curated/dim_disruption_type.csv` | 9 | 7 | Dimension only; no financial attributes |
| dim_booking_channel | `data/03_curated/dim_booking_channel.csv` | 7 | 6 | Dimension only; unused (no FKs); no financial attributes |
| dim_currency | `data/03_curated/dim_currency.csv` | 8 | 6 | Dimension only; unused (no FKs); USD is reporting currency |
| dim_fare_class | `data/03_curated/dim_fare_class.csv` | 8 | 8 | Dimension only; unused (no FKs); no monetary attributes |
| fact_flight_operations | `data/03_curated/fact_flight_operations.csv` | 5,000 | 25 | Fact; no monetary columns; contains RevenuePassengers (count, not revenue) |
| fact_disruptions | `data/03_curated/fact_disruptions.csv` | 1,754 | 16 | Fact; delay minutes only; no monetary attributes |
| fact_customer_feedback | `data/03_curated/fact_customer_feedback.csv` | 2,500 | 16 | Fact; satisfaction scores only; no monetary attributes |

**Evidence:** `docs/PAGE_03_REVENUE_FINANCE_DATA_AUDIT.md`, Section 2.1; `data/manifests/` per-dataset manifest JSON files; `src/utilities/hashing.py` (SHA-256 utilities); `tests/unit/test_hashing.py` (SHA-256 primitive tests).

---

## 3. Missing Data Sources (Critical Blockers)

| Missing Asset | Expected Location | Referenced By | Status | Blocker |
|---|---|---|---|---|
| FactBookingTransactions | `data/03_curated/fact_flight_operations.csv` (absent) | Contract Section 5.3; OD-04; Page 03 visuals RV-01 through RV-18 | **DOES NOT EXIST** | OD-04 not approved; ref_exchange_rates.csv missing |
| FactOperatingCosts | `data/03_curated/fact_operating_costs.csv` (absent) | Contract Section 5.4; OD-04; Page 03 visuals RV-07 through RV-08 | **DOES NOT EXIST** | OD-04 not approved; ref_exchange_rates.csv missing |
| ref_exchange_rates.csv | `data/04_reference/ref_exchange_rates.csv` (absent) | OD-04 Section 2.2; OD04_OWNER_DECISION_PACKAGE.md; OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md | **DOES NOT EXIST** | OD-04 not approved; no rate values approved |

**No raw source files exist** for booking transactions, operating costs, or exchange rates. Confirmed via glob searches for `*booking*`, `*cost*`, `*revenue*`, `*fare*` — zero matches for financial fact files anywhere in the project.

**Evidence:** `docs/PAGE_03_REVENUE_FINANCE_DATA_AUDIT.md` Sections 2.2–2.3; `data/03_curated/` directory listing (only 14 non-financial files present); `data/manifests/` directory listing (14 per-dataset manifests, no reference manifests for financial data).

---

## 4. Required Data Contracts

| Contract Reference | Section | Content | Status |
|---|---|---|---|
| `docs/03_DATA_CONTRACTs.md` | Section 5.3 | FactBookingTransactions schema (TransactionCurrencyKey, ExchangeRateToUSD, USD-converted columns) | Documented; table does not exist |
| `docs/03_DATA_CONTRACTs.md` | Section 5.4 | FactOperatingCosts schema (CurrencyKey, ExchangeRateToUSD, CostAmountUSD) | Documented; table does not exist |
| `docs/03_DATA_CONTRACTs.md` | Section 10.2 | Reference manifest `ref_manifests.csv` (includes ManifestHash field; no canonicalization method defined) | Design only; not created |
| `docs/03_DATA_CONTRACTs.md` | Section 10 | Currency rules: USD reporting currency; no summing mixed currencies before conversion; no conversion in Power BI/DAX | Documented; not implemented |
| `docs/OD04_OWNER_DECISION_PACKAGE.md` | All | OD-04 decision questions OD-04a through OD-04f | DRAFT — owner decision required |
| `docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md` | All | OD-04 resolution assessment with 6 unresolved sub-decisions | PROPOSED — OWNER APPROVAL REQUIRED |

---

## 5. Currency and OD-04 Blockers

### 5.1 Currency Set Mismatch (Critical)

| Currency Set | Currencies | Count | Source |
|---|---|---|---|
| OD-04 proposed set | USD, EUR, GBP, JPY, CAD | 5 | OD-04 Owner Decision Package, Decision 1 |
| DimCurrency (implemented) | AED, QAR, SGD, INR, GBP, EUR, USD, AUD | 8 | `data/03_curated/dim_currency.csv` |

**Impact:**
- `FactBookingTransactions.TransactionCurrencyKey` → DimCurrency (8 currencies)
- `FactOperatingCosts.CurrencyKey` → DimCurrency (8 currencies)
- If OD-04's 5-currency set is enforced: 3 DimCurrency currencies (AED, QAR, SGD, INR, AUD) would have no exchange rate, blocking all transactions/costs in those currencies
- Conversely, JPY and CAD (in OD-04 set) are not in DimCurrency, so rates for them would reference nonexistent dimension keys
- **Resolution required:** Either align OD-04's currency set with DimCurrency's 8 currencies (Option 1 recommended), or align DimCurrency with OD-04's 5 currencies, or define a custom owner-approved set (Option 3)

### 5.2 OD-04 Sub-Decisions (All Pending)

| Decision ID | Question | Status | Options |
|---|---|---|---|
| OD-04a | Currency scope | PROPOSED — PENDING | Option 1 (8 currencies), Option 2 (5 currencies), Option 3 (custom) |
| OD-04b | Exchange-rate convention | PROPOSED — PENDING | USD per unit, 6 decimals, exact-date, no forward-fill |
| OD-04c | Rate source | UNSPECIFIED | 3a (AEROVISION-360-SYNTHETIC-FX-V1), 3b (SIMULATED-FX-V1), 3c (owner-specified) |
| OD-04d | Rate version | UNSPECIFIED | 4a (FX-2026-11-04-001), 4b (FX-V1), 4c (owner-specified) |
| OD-04e | Missing-date behaviour | PROPOSED — PENDING | 5a (no forward-fill), 5b (forward-fill + gap), 5c (period-average — explicitly not allowed) |
| OD-04f | Rate-generation methodology | UNSPECIFIED | 6a (static), 6b (algorithmic), 6c (hybrid) |
| OD-04g | Formal owner approval | PROPOSED — PENDING | Approve or reject OD-04 package |

**All 7 sub-decisions are pending owner approval.** None can be resolved by implementation activity.

**Evidence:** `docs/OD04_OWNER_DECISION_PACKAGE.md` (all sections); `docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md` (Sections 2–12); `docs/03_DATA_CONTRACTs.md` Section 10.

---

## 6. Financial KPI Definitions and Dependencies

### 6.1 Monetary KPIs (All NOT AVAILABLE)

| KPI | Required Data | Source Status | Classification | Reason |
|---|---|---|---|---|
| Total Operating Revenue | NetPassengerRevenueUSD + NetFeeRevenueUSD + NetAncillaryRevenueUSD | FactBookingTransactions does not exist | NOT AVAILABLE | OD-04 blocked; ref_exchange_rates.csv missing |
| Net Passenger Revenue | NetPassengerRevenueUSD | FactBookingTransactions does not exist | NOT AVAILABLE | FactBookingTransactions blocked by OD-04 |
| Net Ancillary Revenue | NetAncillaryRevenueUSD | FactBookingTransactions does not exist | NOT AVAILABLE | FactBookingTransactions blocked by OD-04 |
| Net Fee Revenue | NetFeeRevenueUSD | FactBookingTransactions does not exist | NOT AVAILABLE | FactBookingTransactions blocked by OD-04 |
| Operating Cost USD | CostAmountUSD | FactOperatingCosts does not exist | NOT AVAILABLE | FactOperatingCosts blocked by OD-04 |
| Total RASK | Revenue / ASK | Revenue unavailable; ASK derivable | NOT AVAILABLE | Revenue numerator missing |
| Passenger RASK | Passenger Revenue / ASK | Revenue unavailable; ASK derivable | NOT AVAILABLE | Revenue numerator missing |
| CASK | Operating Cost / ASK | Cost unavailable; ASK derivable | NOT AVAILABLE | Cost numerator missing |
| Unit Contribution | (Revenue − Cost) / ASK | Both unavailable | NOT AVAILABLE | Both numerators missing |
| Passenger Yield | Passenger Revenue / RPK | Revenue unavailable; RPK derivable | NOT AVAILABLE | Revenue numerator missing |
| Ancillary Revenue per Passenger | Ancillary Revenue / Revenue Passengers | Revenue unavailable | NOT AVAILABLE | Revenue numerator missing |
| Average Passenger Revenue | Passenger Revenue / Revenue Passengers | Revenue unavailable | NOT AVAILABLE | Revenue numerator missing |
| Refund Rate | Refunded coupons / Eligible coupons | FactBookingTransactions missing | NOT AVAILABLE | Fact table missing |
| Booking Lead Time | BookingDate, TravelDate per booking | FactBookingTransactions missing | NOT AVAILABLE | Fact table missing |
| Repeat Booking Rate | Customer bookings over time | FactBookingTransactions missing | NOT AVAILABLE | Fact table missing |

### 6.2 Non-Monetary Operational Metrics That ARE Available

| Measure | Source | Status | Usable for Page 03? |
|---|---|---|---|
| Revenue Passengers | fact_flight_operations[RevenuePassengers] | AVAILABLE (FL02 = 218,413) | **No** — passenger count, not revenue; must never be labeled as revenue |
| Available Seats | fact_flight_operations[AvailableSeats] | AVAILABLE | Yes — capacity measure |
| Load Factor | RPK / ASK | DERIVABLE | Yes — capacity measure |
| ASK | AvailableSeats × FlightDistanceKM | DERIVABLE | Yes — capacity measure |
| RPK | RevenuePassengers × FlightDistanceKM | DERIVABLE | Yes — traffic measure |

**Important:** FL02 = SUM(fact_flight_operations[RevenuePassengers]) = 218,413 passengers. This is **passenger volume**, not revenue. It must never be formatted as currency, labeled as "Revenue," or used in any financial calculation.

### 6.3 Dependencies

| Dependency | Status | Owner Decision Required? |
|---|---|---|
| OD-04 formal approval (all 7 sub-decisions) | PENDING | Yes |
| Currency set reconciliation (OD-04 5 vs DimCurrency 8) | PENDING | Yes |
| RateSource value selection | PENDING | Yes |
| RateVersion value selection | PENDING | Yes |
| Rate coverage period approval | PENDING | Yes |
| Individual rate value approval (or algorithm approval) | PENDING | Yes |
| ref_exchange_rates.csv creation | BLOCKED by OD-04 | N/A (owner data decision) |
| FactBookingTransactions implementation | BLOCKED by OD-04 | N/A (implementation after OD-04) |
| FactOperatingCosts implementation | BLOCKED by OD-04 | N/A (implementation after OD-04) |
| Semantic model relationships for financial facts | NOT CREATED | N/A (after fact tables exist) |
| Financial DAX measures | NOT CREATED | N/A (after fact tables exist) |
| Power Query M queries for financial facts | NOT CREATED | N/A (after OD-04 approval) |

---

## 7. Proposed Dashboard Layout (Not Implementable Today)

The following visual specifications exist in `docs/PAGE_03_REVENUE_FINANCE_DATA_AUDIT.md` Section 6 but **none are implementable** with existing data:

| Visual ID | Visual | Required Data | Classification | Feasible? |
|---|---|---|---|---|
| RV-01 | Total Operating Revenue KPI | Net Passenger + Fee + Ancillary Revenue USD | NOT AVAILABLE | ❌ |
| RV-02 | Passenger Revenue KPI | NetPassengerRevenueUSD | NOT AVAILABLE | ❌ |
| RV-03 | Ancillary Revenue KPI | NetAncillaryRevenueUSD | NOT AVAILABLE | ❌ |
| RV-04 | Passenger Yield KPI | Passenger Revenue / RPK | NOT AVAILABLE | ❌ |
| RV-05 | Passenger RASK KPI | Passenger Revenue / ASK | NOT AVAILABLE | ❌ |
| RV-06 | Total RASK KPI | Total Revenue / ASK | NOT AVAILABLE | ❌ |
| RV-07 | CASK KPI | Operating Cost / ASK | NOT AVAILABLE | ❌ |
| RV-08 | Unit Contribution KPI | (Revenue − Cost) / ASK | NOT AVAILABLE | ❌ |
| RV-09 | Revenue trend by stream | Net Passenger/Fee/Ancillary Revenue by month | NOT AVAILABLE | ❌ |
| RV-10 | Yield and RASK trend | Yield/RASK by month | NOT AVAILABLE | ❌ |
| RV-11 | RASK vs CASK | RASK and CASK by month | NOT AVAILABLE | ❌ |
| RV-12 | Fare class mix | Revenue by FareClass | PARTIALLY AVAILABLE | ⚠️ Dimension exists; no fact data |
| RV-13 | Channel mix | Revenue by BookingChannel | PARTIALLY AVAILABLE | ⚠️ Dimension exists; no fact data |
| RV-14 | Average passenger revenue | Revenue / Revenue Passengers | NOT AVAILABLE | ❌ |
| RV-15 | Ancillary per passenger | Ancillary Revenue / Revenue Passengers | NOT AVAILABLE | ❌ |
| RV-16 | Booking lead time | BookingDate vs TravelDate per booking | NOT AVAILABLE | ❌ |
| RV-17 | Refund rate trend | Refunded coupons by month | NOT AVAILABLE | ❌ |
| RV-18 | Scenario panel | Fare/fuel/capacity change inputs | NOT AVAILABLE | ❌ |

**Result: 0 of 18 visuals are feasible.**

The existing `report.json` already contains Page 03 as "Revenue & Yield Intelligence — OD-04 BLOCKED" with a single textbox explaining the block — this is the correct state and should not be changed until OD-04 is approved.

---

## 8. Power Query Implementation Requirements (Post-Go Only)

Once OD-04 is approved, the following Power Query queries would need to be added to `deliverables/power_bi/power_query/AEROVISION360_DataLoad.m`:

| Query | Source | Purpose |
|---|---|---|
| ref_exchange_rates | `data/04_reference/ref_exchange_rates.csv` | Currency conversion rates (CurrencyCode, RateDate, ExchangeRateToUSD, RateSource, IsSynthetic, RateVersion) |
| FactBookingTransactions | `data/03_curated/fact_flight_operations.csv` (new) | Flight booking transactions with monetary amounts |
| FactOperatingCosts | `data/03_curated/fact_operating_costs.csv` (new) | Operating cost transactions with currency and cost category |

None of these files exist. All three require OD-04 approval before creation.

---

## 9. DAX Implementation Requirements (Post-Go Only)

Once the financial fact tables exist, the following DAX measures would be required:

| Measure | Proposed DAX | Dependencies |
|---|---|---|
| Net Passenger Revenue | SUM(FactBookingTransactions[NetPassengerRevenueUSD]) | FactBookingTransactions |
| Net Ancillary Revenue | SUM(FactBookingTransactions[NetAncillaryRevenueUSD]) | FactBookingTransactions |
| Net Fee Revenue | SUM(FactBookingTransactions[NetFeeRevenueUSD]) | FactBookingTransactions |
| Total Operating Revenue | SUM(FactBookingTransactions[NetPassengerRevenueUSD]) + SUM(FactBookingTransactions[NetFeeRevenueUSD]) + SUM(FactBookingTransactions[NetAncillaryRevenueUSD]) | FactBookingTransactions |
| Operating Cost USD | SUM(FactOperatingCosts[CostAmountUSD]) | FactOperatingCosts |
| Operating Profit | Total Operating Revenue − Operating Cost USD | Both fact tables |
| Operating Margin | Operating Profit / Total Operating Revenue | Both fact tables |
| Passenger Yield | Net Passenger Revenue / RPK | FactBookingTransactions + fact_flight_operations |
| RASK | Total Operating Revenue / ASK | FactBookingTransactions + fact_flight_operations |
| CASK | Operating Cost USD / ASK | FactOperatingCosts + fact_flight_operations |

None of these DAX measures exist in `AEROVISION360_Measures.dax` (which contains only 14 non-financial measures: FL01–CF03, OP01–OP04).

---

## 10. Data Validation and Reconciliation Tests (Post-Go Only)

The following QA tests would be required after implementation:

| Test ID | Test | Status |
|---|---|---|
| T-78 | Classification reference-version and manifest integrity | PLANNED/BLOCKED |
| T-79 | Synthetic disclosure exact-string and rendered-output integrity | BLOCKED |
| T-21 (proposed) | Currency conversion integrity (0.01 USD per row tolerance) | NOT CREATED |
| DQ-08 (proposed) | Missing exchange rate quarantine | NOT CREATED |
| Manifest hash validation | SHA-256 of ref_exchange_rates.csv matches manifest | NOT CREATED |

None of these tests exist or have been executed.

---

## 11. Dependency-Ordered Implementation Plan

| Order | Task | Dependency | Owner Action Required? |
|---|---|---|---|
| 1 | Owner approves OD-04 (all 7 sub-decisions: currency scope, exchange-rate convention, rate source, rate version, missing-date behaviour, rate-generation methodology, formal approval) | None | Yes — owner decision |
| 2 | Owner approves currency set reconciliation (align OD-04's 5 currencies with DimCurrency's 8 currencies) | OD-04 approval | Yes — owner decision |
| 3 | Owner approves RateSource value | OD-04 approval | Yes — owner decision |
| 4 | Owner approves RateVersion value | OD-04 approval | Yes — owner decision |
| 5 | Owner approves rate coverage period | OD-04 approval | Yes — owner decision |
| 6 | Owner approves individual rate values or rate-generation algorithm | OD-04 approval | Yes — owner decision |
| 7 | Create `data/04_reference/ref_exchange_rates.csv` with approved rate values | OD-04 approval + all sub-decisions | Implementation (after owner approval) |
| 8. Create `data/manifests/ref_exchange_rates_manifest.json` with SHA-256 hash | Step 7 | Implementation (after step 7) |
| 9. Implement FactBookingTransactions builder | OD-04 approval + step 7 | Implementation (after step 8) |
| 10. Implement FactOperatingCosts builder | OD-04 approval + step 7 | Implementation (after step 8) |
| 11. Add currency conversion validation tests (DQ-08, T-21) | Steps 7–10 | Implementation (after step 10) |
| 12. Add financial fact tables to semantic model | Steps 9–10 | Implementation (after step 10) |
| 13. Add financial DAX measures | Step 12 | Implementation (after step 12) |
| 14. Build Page 03 visuals | Step 13 | Implementation (after step 13) |
| 15. Execute T-78 and T-79 validation tests | Step 14 | Implementation (after step 14) |

---

## 12. Exact First Implementation Task

**The single next actionable task is:**

> **Owner formally approves OD-04 (all 7 sub-decisions), starting with the currency scope decision (Option 1: expand to all 8 existing DimCurrency currencies: AED, QAR, SGD, INR, GBP, EUR, USD, AUD).**

Until this owner decision is recorded, nothing else can proceed:
- `ref_exchange_rates.csv` cannot be created
- FactBookingTransactions cannot be built
- FactOperatingCosts cannot be built
- No financial DAX measures can be written
- No Page 03 financial visuals can be built
- Page 03 remains correctly blocked with its existing "OD-04 BLOCKED" textbox

**No implementation activity on Page 03 financials can begin until OD-04 is formally approved.**

---

## 13. Restrictions Honored

| Restriction | Status |
|---|---|
| No synthetic financial amounts generated | ✅ Verified — no financial data created |
| No exchange rates invented | ✅ Verified — no rate values created |
| OD-04 not modified | ✅ Verified — read only |
| Source data not modified | ✅ Verified — read only |
| Power Query not modified | ✅ Verified — read only |
| DAX not modified | ✅ Verified — read only |
| PBIX not modified | ✅ Verified — read only |
| G3 not approved | ✅ Verified — not attempted |
| G4 not authorized | ✅ Verified — not attempted |
| G3-RV-01 not executed | ✅ Verified |
| Schema freeze not authorized | ✅ Verified |
| Pages 01/02 not modified | ✅ Verified — read only |
| CC-01 not executed | ✅ Verified — not attempted |

---

## 14. Conclusion

**Page 03 Revenue & Finance cannot be implemented with existing project data.**

All 18 revenue/finance visuals are blocked by the absence of FactBookingTransactions and FactOperatingCosts, which are themselves blocked by unapproved OD-04 and missing ref_exchange_rates.csv. No monetary data exists anywhere in the project. Passenger volume (FL02 = 218,413 RevenuePassengers) is explicitly not revenue and must not be presented as such.

**The project should defer Page 03 until OD-04 is formally approved, exchange rates are established, and the two financial fact tables are built and loaded.**
