# AEROVISION 360 — OD-04 Exchange-Rate Policy Resolution Assessment

**Document type:** Decision package — exchange-rate policy  
**Decision ID:** OD-04  
**Decision title:** Synthetic exchange-rate policy for USD conversion  
**Parent decision:** OD-01 (series)  
**Decision owner / approver:** KH Mohammad Farhan  
**Formal status:** PROPOSED — OWNER APPROVAL REQUIRED (per controlled `03_DATA_CONTRACTS.md`, Section 14)  
**Decision date:** [BLANK — to be completed by the owner at signature]  
**Prepared:** 2026-11-04  
**Governing baseline:** `03_DATA_CONTRACTS.md` version 1.5, Section 10  
**Related fact tables:** FactBookingTransactions, FactOperatingCosts  
**Related reference file:** `data/04_reference/ref_exchange_rates.csv` (does not exist)  
**Blocking status:** BLOCKS FactBookingTransactions and FactOperatingCosts implementation  

---

## STATUS NOTICE — NOT A FORMAL APPROVAL

This document is a decision package for owner review. It does not constitute formal approval of OD-04, does not record a signature or approval date, and does not authorize creation of `ref_exchange_rates.csv`, FactBookingTransactions, or FactOperatingCosts. G3 cannot pass while OD-04 remains open.

---

## 1. Purpose and Authority

OD-04 defines the exchange-rate regime used to convert original-currency financial amounts to USD in FactBookingTransactions and FactOperatingCosts. Without an approved OD-04 and a corresponding `ref_exchange_rates.csv`, no financial fact table can be generated because:

- Every non-USD financial row requires an exact-date exchange rate (`ExchangeRateToUSD`)
- Currency conversion must not be performed in Power BI or DAX — it is performed once in STAGING/CURATED
- Missing rates block rows (defect DQ-08: "Quarantine; never convert with a missing or guessed rate")
- USD conversion is validated at transaction-row level (proposed threshold 0.01 USD per row, not owner-approved)

The authority for this record is the owner confirmation recorded in `OD01_OWNER_DECISION_CONFIRMATION.md`, which records eight choices as OWNER-CONFIRMED but does not record a signature, approval date, or independent review.

---

## 2. Contractual Requirements (from `03_DATA_CONTRACTs.md` Section 10)

### 2.1 Reporting Currency

- USD is the only reporting currency
- All financial KPIs in Section 11 are calculated from USD columns
- Original transaction currency and original amount are preserved for audit and currency-mix analysis
- Amounts in different currencies must never be summed before conversion
- Currency conversion must not be performed in Power BI visuals or DAX measures

### 2.2 Exchange-Rate Contract (`ref_exchange_rates.csv`)

| Column | Data type | Null | Definition |
|--------|-----------|------|------------|
| CurrencyCode | String(3) | No | ISO 4217 code; foreign key to DimCurrency |
| RateDate | Date | No | Effective date of the rate |
| ExchangeRateToUSD | Decimal(18,6) | No | USD per one unit of the currency; positive |
| RateSource | String(50) | No | Synthetic source identifier |
| IsSynthetic | Boolean | No | True for all baseline rates |
| RateVersion | String(20) | No | Reference version |

### 2.3 Conversion Formula

`AmountUSD = Amount * ExchangeRateToUSD`, rounded to two decimals at the final amount level. The rate is not rounded before multiplication.

### 2.4 Rate-Date Rule

- Use the transaction date for bookings and the cost date for costs
- A period-average rate is not allowed unless explicitly approved and labeled
- The rate must exist for the exact date
- The baseline does not use forward-filling
- If forward-filling is approved later, it must have a documented maximum gap and an `IsCarriedForward` flag

### 2.5 Rate Plausibility

- Synthetic rates must be positive
- Stable enough to avoid absurd conversions
- Documented as fictional
- Must not be copied from a live market feed or presented as real exchange rates

### 2.6 OD-04 Status (Current Controlled Document)

**OD-04 | Synthetic exchange-rate policy | USD per one unit of currency; exact-date rate; six decimals; synthetic source. Currency set: USD, EUR, GBP, JPY, CAD. | Every non-USD financial fact depends on it | PROPOSED - OWNER APPROVAL REQUIRED**

**OD-04 | KH Mohammad Farhan | PENDING**

---

## 3. Unresolved Decisions

| # | Decision | Status | Impact |
|---|----------|--------|--------|
| OD-04a | Formal owner approval of OD-04 | PENDING | Blocks all financial fact generation |
| OD-04b | Currency set | CONFLICT | OD-04 lists USD, EUR, GBP, JPY, CAD but DimCurrency has AED, QAR, SGD, INR, GBP, EUR, USD, AUD (8 currencies). Must reconcile. |
| OD-04c | Rate source | UNSPECIFIED | "Synthetic source identifier" is required but no source name, publisher, or methodology is defined |
| OD-04d | RateVersion value | UNSPECIFIED | Required column but no value or versioning scheme defined |
| OD-04e | Forward-filling | EXPLICITLY NOT ALLOWED unless later approved | No maximum gap or `IsCarriedForward` flag defined |
| OD-04f | Weekend/holiday handling | UNSPECIFIED | Rate must exist for exact date; no fallback for non-business days |
| OD-04h | Historical rate immutability | UNSPECIFIED | No statement that rates are immutable after publication |
| OD-04i | Rate volatility bounds | UNSPECIFIED | "Stable enough to avoid absurd conversions" is qualitative, not quantitative |

---

## 4. Dimension Currency Mismatch (Critical)

**OD-04 currency set:** USD, EUR, GBP, JPY, CAD (5 currencies)

**DimCurrency currency set:** AED, QAR, SGD, INR, GBP, EUR, USD, AUD (8 currencies)

**Impact:**
- FactBookingTransactions references `TransactionCurrencyKey` → DimCurrency (8 currencies)
- FactOperatingCosts references `CurrencyKey` → DimCurrency (8 currencies)
- If OD-04's currency set (5 currencies) is enforced, 3 DimCurrency currencies (AED, QAR, SGD, INR, AUD — 5 actually not in OD-04 set) would have no exchange rate, blocking all transactions/costs in those currencies
- Conversely, JPY and CAD (in OD-04 set) are not in DimCurrency, so rates for them would reference a nonexistent dimension key

**Resolution required:** Either align OD-04's currency set with DimCurrency's 8 currencies, or align DimCurrency with OD-04's 5 currencies. This is a blocking discrepancy.

---

## 5. Technically Viable Options

### Option A: USD-per-one-unit, exact-date, no forward-fill (as documented in Section 10.2)

**Description:** One rate row per currency per rate date. Rate must exist for exact transaction/cost date. No forward-filling. USD-per-one-unit at 6 decimals.

**Advantages:**
- Simple, deterministic, auditable
- Matches existing contract Section 10.2 schema
- No rate interpolation or estimation risk
- Synthetic rates clearly disclosed as fictional

**Disadvantages:**
- Requires a rate for every transaction/cost date — high row count if coverage is broad
- Weekend/holiday dates with no rate will block rows unless rates exist for all calendar dates
- No fallback mechanism for missing dates

**Disruption risk:** High if rate coverage has gaps; any missing rate quarantines the financial row (DQ-08, High severity)

### Option B: USD-per-one-unit with forward-filling (maximum gap N days, `IsCarriedForward` flag)

**Description:** Same as Option A but allows carrying forward the last known rate for up to N days when a date is missing.

**Advantages:**
- Reduces row count requirements
- Handles weekends/holidays without explicit rates for every date
- Explicit `IsCarriedForward` flag maintains auditability

**Disadvantages:**
- Requires formal owner approval (currently explicitly not allowed)
- Introduces rate staleness risk
- Adds complexity to conversion logic and validation

**Disruption risk:** Medium; reduces missing-rate blocks but adds staleness risk

### Option C: Period-average rate (weekly/monthly)

**Description:** Use an average rate for a period instead of exact-date rates.

**Advantages:**
- Far fewer rate rows required
- Simpler rate maintenance

**Disadvantages:**
- Explicitly not allowed by Section 10.2 unless explicitly approved and labeled
- Less precise; introduces averaging bias
- Would require contract amendment

**Disruption risk:** Very high; requires contract change and owner approval

---

## 6. Recommended Option: Option A (Exact-Date, No Forward-Fill)

**Rationale:**
- Matches the existing controlled contract Section 10.2 without amendment
- Simplest to implement, test, and audit
- All rates are explicit and disclosed as synthetic
- No rate-staleness or interpolation risk
- Consistent with the deterministic, seed-based generation philosophy used elsewhere in the project

**Preconditions before implementation:**
1. Resolve the OD-04 currency set vs. DimCurrency mismatch (Option: align OD-04 to DimCurrency's 8 currencies, since DimCurrency is already implemented and populated)
2. Define RateSource value (e.g., "AEROVISION-360-SYNTHETIC-FX-V1")
3. Define RateVersion value (e.g., "FX-2026-11-04-001")
4. Define rate coverage period (must cover all booking dates and cost dates in the reporting period: 2024-10-01 through 2026-10-31 per DimDate coverage)
5. Owner formal approval of OD-04
6. Owner formal approval of the rate values (synthetic but must be recorded)

---

## 7. Impact on Blocked Fact Tables

### FactBookingTransactions
- `TransactionCurrencyKey` → DimCurrency (8 currencies)
- `ExchangeRateToUSD` (Decimal 18,6) — from ref_exchange_rates.csv
- USD-converted columns: BaseFareUSD, DiscountUSD, TaxUSD, FeeUSD, AncillaryRevenueUSD, RefundUSD, AncillaryRefundUSD, FeeRefundUSD, CancellationFeeUSD, NoShowFeeUSD, NetPassengerRevenueUSD, NetFeeRevenueUSD, NetAncillaryRevenueUSD
- Rate-date rule: use BookingDateKey (UTC calendar date of booking transaction)
- Blocked until: OD-04 approved + ref_exchange_rates.csv exists + rate coverage includes all booking dates

### FactOperatingCosts
- `CurrencyKey` → DimCurrency (8 currencies)
- `ExchangeRateToUSD` (Decimal 18,6) — from ref_exchange_rates.csv
- `CostAmountUSD` (Decimal 18,2, signed) — from CostAmount * ExchangeRateToUSD
- Rate-date rule: use CostDateKey (accounting date)
- Blocked until: OD-04 approved + ref_exchange_rates.csv exists + rate coverage includes all cost dates

---

## 8. Proposed Reference-Data Schema

File: `data/04_reference/ref_exchange_rates.csv`

| Column | Type | Example |
|--------|------|---------|
| CurrencyCode | String(3) | "EUR" |
| RateDate | Date (YYYY-MM-DD) | "2025-10-01" |
| ExchangeRateToUSD | Decimal(18,6) | 1.050000 |
| RateSource | String(50) | "AEROVISION-360-SYNTHETIC-FX-V1" |
| IsSynthetic | Boolean | TRUE |
| RateVersion | String(20) | "FX-2026-11-04-001" |

**Primary key:** CurrencyCode + RateDate (composite)

**Coverage requirement:** One row per DimCurrency currency code × one row per date in the reporting period (2024-10-01 through 2026-10-31, per DimDate coverage), or at minimum every date that appears as a BookingDateKey or CostDateKey in the financial facts.

---

## 9. Example Synthetic Records (ILLUSTRATIVE ONLY — NOT FOR PRODUCTION)

| CurrencyCode | RateDate | ExchangeRateToUSD | RateSource | IsSynthetic | RateVersion |
|--------------|----------|-------------------|------------|-------------|-------------|
| USD | 2025-10-01 | 1.000000 | AEROVISION-360-SYNTHETIC-FX-V1 | TRUE | FX-2026-11-04-001 |
| EUR | 2025-10-01 | 1.050000 | AEROVISION-360-SYNTHETIC-FX-V1 | TRUE | FX-2026-11-04-001 |
| GBP | 2025-10-01 | 1.220000 | AEROVISION-360-SYNTHETIC-FX-V1 | TRUE | FX-2026-11-04-001 |
| AED | 2025-10-01 | 0.272000 | AEROVISION-360-SYNTHETIC-FX-V1 | TRUE | FX-2026-11-04-001 |
| QAR | 2025-10-01 | 0.274000 | AEROVISION-360-SYNTHETIC-FX-V1 | TRUE | FX-2026-11-04-001 |
| SGD | 2025-10-01 | 0.735000 | AEROVISION-360-SYNTHETIC-FX-V1 | TRUE | FX-2026-11-04-001 |
| INR | 2025-10-01 | 0.012000 | AEROVISION-360-SYNTHETIC-FX-V1 | TRUE | FX-2026-11-04-001 |
| AUD | 2025-10-01 | 0.645000 | AEROVISION-360-SYNTHETIC-FX-V1 | TRUE | FX-2026-11-04-001 |

**These are illustrative examples only.** Actual rate values require owner approval and must be documented as fictional — not copied from any live market feed.

---

## 10. Required Owner Approvals

| Approval | Description | Status |
|----------|-------------|--------|
| OD-04 formal approval | Synthetic exchange-rate policy (exact-date, USD-per-one-unit, 6 decimals, no forward-fill) | PENDING |
| Currency set alignment | Reconcile OD-04's 5 currencies with DimCurrency's 8 currencies | PENDING |
| RateSource value | Approve the synthetic source identifier string | PENDING |
| RateVersion value | Approve the rate version string | PENDING |
| Rate coverage period | Approve the date range for rate generation | PENDING |
| Individual rate values | Approve each synthetic rate (or approve a rate-generation methodology) | PENDING |

---

## 11. Discrepancy Log (Current Controlled Document vs. Backups)

| Item | Controlled `03_DATA_CONTRACTS.md` | Some backup files | Resolution Required |
|------|-----------------------------------|-------------------|---------------------|
| OD-04 status | PROPOSED - OWNER APPROVAL REQUIRED; PENDING | APPROVED - DESIGN CONTRACT | Current controlled document governs. OD-04 is PENDING. |
| Currency set | USD, EUR, GBP, JPY, CAD (OD-04 entry) | USD, EUR, GBP, JPY, CAD | DimCurrency has 8 different currencies; must reconcile |

---

## 12. Next Steps After Owner Approval

1. Create `data/04_reference/ref_exchange_rates.csv` with approved rate values
2. Create `data/manifests/ref_exchange_rates_manifest.json` with SHA-256 hash
3. Implement FactBookingTransactions builder
4. Implement FactOperatingCosts builder
5. Add currency conversion validation tests (DQ-08, T-21)

---

**Do not** mark OD-04 approved. **Do not** create `ref_exchange_rates.csv`. **Do not** implement FactBookingTransactions or FactOperatingCosts until OD-04 is formally approved and the currency mismatch is resolved.
