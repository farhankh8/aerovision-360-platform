# AEROVISION 360 — OD-04 Exchange Rate Policy Decision Brief

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Decision ID:** OD-04  
**Decision Title:** Exchange-Rate Policy  
**Decision Date:** 2026-11-08 (prepared)  
**Status:** UNRESOLVED — OWNER DECISION REQUIRED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Decision Summary

OD-04 governs exchange-rate policy for converting non-USD monetary amounts to USD in AEROVISION 360 financial facts. The decision is currently UNRESOLVED and blocks FactBookingTransactions and FactOperatingCosts.

**Current Controlled Status:** PROPOSED — PENDING  
**Required Decision:** Owner decision required on all seven sub-decisions (OD-04a through OD-04g)

---

## 2. Decision Areas

### OD-04a — Currency Scope

**Current Status:** PROPOSED — PENDING

| Option | Currency Set | Rationale |
|--------|--------------|-----------|
| Option 1 | AED, QAR, SGD, INR, GBP, EUR, USD, AUD (8 currencies) | Matches existing DimCurrency dimension; no dimension mismatches |
| Option 2 | USD, EUR, GBP, JPY, CAD (5 currencies) | Matches original OD-04 proposal but creates mismatch with DimCurrency (AED, QAR, SGD, INR missing) |
| Option 3 | Owner-specified custom set | Requires contract amendment and DimCurrency changes |

**Impact of mismatch:** If OD-04 currency set (5 currencies) differs from DimCurrency (8 currencies), fact rows in currencies without exchange rates must be quarantined (DQ-08). JPY and CAD are in OD-04 but NOT in DimCurrency, so their rates would reference nonexistent dimension keys.

**Recommendation:** Option 1 — expand OD-04 to cover all 8 existing DimCurrency currencies.

---

### OD-04b — Exchange-Rate Convention

**Current Status:** PROPOSED — PENDING

| Element | Proposed Convention |
|---------|-------------------|
| Rate Direction | USD per one unit of transaction currency |
| Precision | 6 decimal places |
| Lookup Rule | Exact-date rate (transaction date for bookings, cost date for costs) |
| Forward-Fill | NOT permitted |
| Rounding | Round final converted amount to 2 decimals at final amount level; do not reconvert USD amounts |

**Owner Decision Required:** Yes — confirm or revise convention, precision, lookup rule, forward-fill prohibition, rounding behavior.

---

### OD-04c — Rate Source

**Current Status:** UNSPECIFIED

| Option | Rate Source Value | Rationale |
|--------|------------------|-----------|
| 3a | "AEROVISION-360-SYNTHETIC-FX-V1" | Project-branded, versioned, clearly synthetic |
| 3b | "SIMULATED-FX-V1" | Generic, clearly synthetic |
| 3c | Owner-specified value | Owner-defined rate source identifier |

**Required Decision:** Select RateSource value and confirm all rates are synthetic simulation data, not actual market rates.

---

### OD-04d — Rate Version

**Current Status:** UNSPECIFIED

| Option | RateVersion Value | Rationale |
|--------|-------------------|-----------|
| 4a | "FX-2026-11-04-001" | Date-based version, deterministic, reproducible |
| 4b | "FX-V1" | Simple version label |
| 4c | Owner-specified value | Owner-defined version convention |

**Owner decision required:** Select RateVersion value and confirm versioning convention supports historical reproducibility.

---

### OD-04e — Missing-Date Behaviour

**Current Status:** PROPOSED — PENDING

| Option | Missing-Date Behaviour | Rationale |
|--------|----------------------|-----------|
| 5a | No forward-fill; exact-date lookup; missing exact-date rate quarantines row | Matches current contract. Simplest, most auditable. |
| 5b | Forward-fill with maximum gap N days + IsCarriedForward flag | Requires contract amendment and owner approval. Reduces row count but introduces staleness risk. |
| 5c | Period-average rate | Explicitly not allowed by current contract; requires contract amendment. |

**Owner decision required:** Select missing-date behaviour. If Option 5b is desired, specify maximum gap and approve contract amendment.

---

### OD-04f — Rate Generation Methodology

**Current Status:** UNSPECIFIED

| Option | Methodology | Rationale |
|--------|-------------|-----------|
| 6a | Owner-provided static rate table | Owner defines exact rate values. Maximum control, maximum owner effort. |
| 6b | Deterministic algorithmic generation (seed-based) | Rates generated from documented seed and formula. Reproducible. Requires owner approval of algorithm and parameters. |
| 6c | Hybrid: algorithmic base + owner-adjusted rates | Algorithmic generation with owner overrides for specific currency-date pairs. |

**Owner decision required:** Select rate-generation methodology and approve specific rate values or algorithm parameters.

**All example rates in this document are illustrative only — not approved exchange rates.**

---

## 3. Impact Assessment

### Affected Facts

| Fact Table | Currency Key Column | USD-Converted Columns | Rows Affected | Status |
|------------|-------------------|----------------------|---------------|--------|
| fact_booking_transactions | TransactionCurrencyKey | BaseFareUSD, DiscountUSD, TaxUSD, FeeUSD, AncillaryRevenueUSD, RefundUSD, AncillaryRefundUSD, FeeRefundUSD, CancellationFeeUSD, NoShowFeeUSD, NetPassengerRevenueUSD, NetFeeRevenueUSD, NetAncillaryRevenueUSD | ~9,956 rows | BLOCKED |
| fact_operating_costs | CurrencyKey | CostAmountUSD | ~7,480 rows | BLOCKED |

### Impact on Page 03 (Revenue & Finance)
- **18 visuals** depend on RV_* and CX_* measures
- **All blocked** by OD-04
- No revenue/cost data can be displayed until OD-04 is resolved

---

## 10. Downstream Dependencies

| Component | Depends on OD-04? | Status |
|-----------|-------------------|--------|
| FactBookingTransactions | YES | BLOCKED |
| FactOperatingCosts | YES | BLOCKED |
| Page 03 Revenue & Finance | YES | BLOCKED (18 visuals) |
| Page 04 Cost & Financial Intelligence | YES | Potentially blocked (CX_* measures) |
| Page 05 Customer & Service Intelligence | NO | Uses CF measures only |

---

## 13. Decision Summary Table

| Decision ID | Question | Options | Current Status | Owner Decision Required? |
|-------------|----------|---------|------------------|--------------------------|
| OD-04a | Currency scope | Option 1 (8 currencies), Option 2 (5 currencies), Option 3 (custom) | YES — PROPOSED — PENDING |
| OD-04b | Exchange-rate convention | USD per one unit, 6 decimals, exact-date, no forward-fill | YES — PROPOSED — PENDING |
| OD-04c | Rate source | Option 3a, 3b, 3c | YES — OWNER DECISION REQUIRED |
| OD-04d | Rate version | Option 4a, 4b, 4c | YES — OWNER DECISION REQUIRED |
| OD-04e | Missing-date behaviour | Option 5a (no forward-fill), 5b (forward-fill + gap), 5c (period-average) | YES — PROPOSED — PENDING |
| OD-04f | Rate-generation methodology | Option 6a (static), 6b (algorithmic), 6c (hybrid) | YES — OWNER DECISION REQUIRED |

**All 6 OD-04 sub-decisions require owner decision.** None have been resolved.

---

## 7. Evidence Trail

| Source Document | Location | Relevance |
|-----------------|----------|-----------|
| OD-04 Owner Decision Brief | `docs/OD04_OWNER_DECISION_BRIEF.md` | Primary decision document |
| OD-04 Owner Decision Record | `docs/OD04_OWNER_DECISION_RECORD.md` | Approval record |
| Data Contracts v1.5 | `docs/03_DATA_CONTRACTS.md` Sections 10.1–10.2 | Contractual basis |
| DimCurrency Manifest | `data/03_curated/dim_currency_manifest.json` | 8 existing currencies |
| FactBookingTransactions | `data/03_curated/fact_booking_transactions.csv` | 9,956 rows blocked |
| FactOperatingCosts | `data/03_curated/fact_operating_costs.csv` | 7,480 rows blocked |

---

**END OF DOCUMENT — OD-04 EXCHANGE RATE POLICY DECISION BRIEF**
