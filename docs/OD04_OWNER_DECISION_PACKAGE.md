# AEROVISION 360 — OD-04 Owner Decision Package

**Document type:** Owner decision package — exchange-rate policy  
**Decision ID:** OD-04  
**Decision title:** Synthetic exchange-rate policy for USD conversion  
**Decision owner / approver:** KH Mohammad Farhan  
**Formal status:** PROPOSED — OWNER APPROVAL REQUIRED  
**Prepared:** 2026-11-04  
**Governing baseline:** `03_DATA_CONTRACTS.md` version 1.5, Section 10  
**Source documents reviewed:**  
- `docs/03_DATA_CONTRACTS.md` (Sections 10.1–10.2, 10.4, 10.5, 10.8, 11.1, Section 14 OD register)  
- `docs/OWNER_DECISIONS_2026-11-04.md`  
- `docs/OD01A_AIRLINE_POPULATION_DECISION.md`  
- `data/03_curated/dim_currency.parquet` (8 currencies, USD reporting)  
- `data/03_curated/dim_currency_manifest.json`  

---

## STATUS NOTICE — NOT A FORMAL APPROVAL

This document is an owner decision package. It presents decision questions and options for explicit owner selection. It does not constitute formal approval of OD-04, does not record a signature or approval date, and does not authorize creation of `ref_exchange_rates.csv` or implementation of FactBookingTransactions or FactOperatingCosts.

---

## 1. Decision Questions for Owner Selection

### Decision 1: Currency scope

**Current controlled status:** PROPOSED — PENDING  
**OD-04 currency set (documented):** USD, EUR, GBP, JPY, CAD (5 currencies)  
**Existing DimCurrency currency set:** AED, QAR, SGD, INR, GBP, EUR, USD, AUD (8 currencies)  
**Impact:** FactBookingTransactions and FactOperatingCosts reference `CurrencyKey` → DimCurrency. Every non-USD financial row requires an exchange rate. A mismatch between the OD-04 currency set and DimCurrency means some currencies would have no rate (blocking rows) or rates would reference nonexistent dimension members (blocking referential integrity).

**Option 1 — Expand OD-04 to cover all eight existing DimCurrency currencies**

| Dimension | Detail |
|-----------|--------|
| Currency set | AED, QAR, SGD, INR, GBP, EUR, USD, AUD (8 currencies) |
| Rationale | Matches the already-implemented DimCurrency dimension. No dimension member is orphaned or removed. |
| Data-model implication | `ref_exchange_rates.csv` requires 8 currencies × N dates. No dimension changes needed. |
| Risk | Larger rate table; more owner-approved rate values required. |

**Option 2 — Restrict analytical scope to the five OD-04 currencies**

| Dimension | Detail |
|-----------|--------|
| Currency set | USD, EUR, GBP, JPY, CAD (5 currencies) |
| Rationale | Matches the OD-04 documented proposal as written. |
| Data-model implication | DimCurrency retains 8 members, but 3 (AED, QAR, SGD, INR, AUD — actually 5 not in OD-04 set: AED, QAR, SGD, INR, AUD) would have no exchange rate. Any financial transaction or cost in those currencies cannot be converted and must be quarantined (DQ-08, High severity). JPY and CAD are in OD-04 but not in DimCurrency, so rates for them would reference nonexistent dimension keys unless DimCurrency is also amended. |
| Risk | Data loss / quarantine risk for non-covered currencies; referential integrity gaps for JPY/CAD unless DimCurrency is amended. |

**Option 3 — Define a different approved currency scope with documented rationale**

| Dimension | Detail |
|-----------|--------|
| Currency set | Owner-specified set (to be documented) |
| Rationale | Owner determines the analytical currency scope based on business requirements. |
| Data-model implication | Requires either amending DimCurrency or accepting quarantined rows. Must be documented in the controlled contract via a controlled change. |
| Risk | Highest — requires contract amendment and may invalidate existing dimension reference data. |

**Owner decision required:** Select Option 1, 2, or 3.

**Recommended:** Option 1 — expand OD-04 to cover all eight existing DimCurrency currencies, subject to owner confirmation that all eight currencies are genuinely in analytical scope.

---

### Decision 2: Exchange-rate convention

**Current controlled status:** PROPOSED — PENDING  
**Proposed convention:** USD per one unit of transaction currency  
**Proposed precision:** Six decimal places  
**Lookup rule:** Exact-date rate (transaction date for bookings, cost date for costs)  
**Forward-filling:** Not permitted under current proposal  
**Rounding:** Round `AmountUSD` to two decimals at the final amount level; do not round the rate before multiplication  

**Owner decision required:** Confirm or revise the exchange-rate convention, precision, lookup rule, and rounding behavior.

---

### Decision 3: Rate source

**Current controlled status:** UNSPECIFIED  
**Required field:** `RateSource` (String(50), not null)  
**Synthetic simulation disclosure required:** All rates must be documented as fictional; must not be copied from a live market feed or presented as real exchange rates.

**Options:**

| Option | RateSource value | Rationale |
|--------|-----------------|-----------|
| 3a | `"AEROVISION-360-SYNTHETIC-FX-V1"` | Project-branded, versioned, clearly synthetic. |
| 3b | `"SIMULATED-FX-V1"` | Generic, clearly synthetic. |
| 3c | Owner-specified value | Owner-defined source identifier. |

**Owner decision required:** Select a RateSource value and confirm that all rates are synthetic simulation data, not actual market rates.

---

### Decision 4: RateVersion

**Current controlled status:** UNSPECIFIED  
**Required field:** `RateVersion` (String(20), not null)  
**Purpose:** Preserve historical reproducibility; allow rate table versioning if rates are ever revised.

**Options:**

| Option | RateVersion value | Rationale |
|--------|------------------|-----------|
| 4a | `"FX-2026-11-04-001"` | Date-based version, deterministic, reproducible. |
| 4b | `"FX-V1"` | Simple version label. |
| 4c | Owner-specified value | Owner-defined version convention. |

**Owner decision required:** Select a RateVersion value and confirm the versioning convention supports historical reproducibility.

---

### Decision 5: Rate coverage and missing-date behaviour

**Current controlled status:** PROPOSED — PENDING  
**Coverage requirement:** One rate row per currency per effective date. Rate must exist for every booking date (FactBookingTransactions) and cost date (FactOperatingCosts).  
**Reporting period:** 2025-10-01 through 2026-09-30 (DimDate reporting period)  
**DimDate full coverage:** 2024-10-01 through 2026-10-31  

**Missing-date behaviour (current contract):**
- Forward-filling is NOT allowed unless explicitly approved and labeled
- If forward-filling is approved later, it must have a documented maximum gap and an `IsCarriedForward` flag
- Missing rate → quarantine the financial row (DQ-08, High severity: "never convert with a missing or guessed rate")

**Options:**

| Option | Missing-date behaviour | Rationale |
|--------|----------------------|-----------|
| 5a | No forward-fill; exact-date only; missing rate quarantines row | Matches current contract. Simplest, most auditable. |
| 5b | Forward-fill with maximum gap N days + `IsCarriedForward` flag | Requires contract amendment and owner approval. Reduces row count but introduces staleness risk. |
| 5c | Period-average rate | Explicitly not allowed by current contract; requires contract amendment. |

**Owner decision required:** Select missing-date behaviour. If Option 5b is desired, specify maximum gap and approve contract amendment.

---

### Decision 6: Rate-generation methodology

**Current controlled status:** UNSPECIFIED  
**Contract requirement:** Synthetic rates must be positive, stable enough to avoid absurd conversions, and documented as fictional.

**Options:**

| Option | Methodology | Rationale |
|--------|-------------|-----------|
| 6a | Owner-provided static rate table | Owner defines every rate value. Maximum control, maximum owner effort. |
| 6b | Deterministic algorithmic generation (seed-based) | Rates generated from a documented seed and formula. Reproducible. Requires owner approval of the algorithm and parameters. |
| 6c | Hybrid: algorithmic base + owner-adjusted rates | Algorithmic generation with owner overrides for specific currency-date pairs. |

**Owner decision required:** Select rate-generation methodology and approve the specific rate values or algorithm parameters.

**All example rates in this document are illustrative only — not approved exchange rates.**

---

### Decision 7: Downstream implications

**FactBookingTransactions:**
- `TransactionCurrencyKey` → DimCurrency
- `ExchangeRateToUSD` from `ref_exchange_rates.csv`
- USD-converted columns: BaseFareUSD, DiscountUSD, TaxUSD, FeeUSD, AncillaryRevenueUSD, RefundUSD, AncillaryRefundUSD, FeeRefundUSD, CancellationFeeUSD, NoShowFeeUSD, NetPassengerRevenueUSD, NetFeeRevenueUSD, NetAncillaryRevenueUSD
- Rate-date rule: use BookingDateKey (UTC calendar date of booking transaction)
- Blocked until: OD-04 approved + `ref_exchange_rates.csv` exists + rate coverage includes all booking dates

**FactOperatingCosts:**
- `CurrencyKey` → DimCurrency
- `ExchangeRateToUSD` from `ref_exchange_rates.csv`
- `CostAmountUSD` (Decimal 18,2, signed)
- Rate-date rule: use CostDateKey (accounting date)
- Blocked until: OD-04 approved + `ref_exchange_rates.csv` exists + rate coverage includes all cost dates

**DimCurrency:** Already implemented with 8 currencies, USD as sole reporting currency. No changes required if Option 1 (Decision 1) is selected.

**Financial reconciliation and auditability:** Section 10.8 requires USD conversion reconciliation at transaction-row level (proposed 0.01 USD per row, not owner-approved). All conversions must be traceable to a rate row in `ref_exchange_rates.csv`.

---

## 2. Owner Decision Record Table

| Decision ID | Question | Current status | Owner decision required | Options | Owner selection |
|-------------|----------|----------------|------------------------|---------|-----------------|
| OD-04a | Currency scope | Owner-confirmed (2026-11-07) | Confirmed — Option 1 selected | Option 1 (8 currencies), Option 2 (5 currencies), Option 3 (custom) | Option 1 — AED, QAR, SGD, INR, GBP, EUR, USD, AUD |
| OD-04b | Exchange-rate convention | Owner-confirmed (2026-11-07) | Confirmed | USD per unit, 6 decimals, exact-date, no forward-fill | USD per unit; exact-date lookup; 6 decimal places; round final amount to 2 decimals; no forward-fill |
| OD-04c | Rate source | Owner-confirmed (2026-11-07) | Confirmed | 3a, 3b, or 3c | `AEROVISION-360-SYNTHETIC-FX-V1` |
| OD-04d | Rate version | Owner-confirmed (2026-11-07) | Confirmed | 4a, 4b, or 4c | `FX-YYYY-MM-DD-NNN` (current value: `FX-2026-11-04-001`) |
| OD-04e | Missing-date behaviour | Owner-confirmed (2026-11-07) | Confirmed | 5a (no forward-fill), 5b (forward-fill + gap), 5c (period-average) | 5a — No forward-fill; exact-date only; missing rate quarantines row |
| OD-04f | Rate-generation methodology | Owner-confirmed (2026-11-07) | Confirmed | 6a (static), 6b (algorithmic), 6c (hybrid) | Owner-provided static rate table |

---

## 3. Boundaries — What This Document Does NOT Do

- Does **not** mark OD-04 as approved
- Does **not** modify `03_DATA_CONTRACTS.md` or any controlled contract
- Does **not** modify `OWNER_DECISIONS_2026-11-04.md` or any decision register
- Does **not** create `ref_exchange_rates.csv`
- Does **not** modify any existing dataset, dimension, fact, or builder
- Does **not** implement FactBookingTransactions or FactOperatingCosts
- Does **not** perform Git operations
- Does **not** present any rate value as an approved exchange rate (all examples are illustrative)

---

## 3. Next Steps After Owner Approval

Once the owner records selections for all seven decision questions:

1. Record the owner's decisions in the controlled governance documentation
2. Update `03_DATA_CONTRACTS.md` through a controlled change (if currency set or other contract elements change)
3. Create `data/04_reference/ref_exchange_rates.csv` with owner-approved rate values
4. Create `data/manifests/ref_exchange_rates_manifest.json` with SHA-256 hash
5. Implement FactBookingTransactions builder
6. Implement FactOperatingCosts builder
7. Add currency conversion validation tests (DQ-08, T-21)

---

**The three verified fact tables (FactFlightOperations, FactDisruptions, FactCustomerFeedback) remain frozen and unaffected by this decision package.**
