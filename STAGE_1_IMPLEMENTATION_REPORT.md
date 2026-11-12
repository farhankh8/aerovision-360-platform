# AEROVISION 360 — Stage 1 Financial Data Engineering — Implementation Report

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Stage:** Stage 1 — Financial Data Generation (FactBookingTransactions + FactOperatingCosts)  
**Date:** 2026-11-07  
**Owner:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Summary

Stage 1 is complete. Both financial fact tables were generated, validated, and manifest-hashed following existing project conventions. All 113 automated validation tests passed. No source files were modified. No Power BI visuals were started. No governance documentation was created or modified beyond what is required for the implementation artifacts.

---

## 2. Outputs Created

### 2.1 Fact Tables (curated layer)

| File | Rows | Columns | Grain | Primary Key |
|---|---|---|---|---|
| `data/03_curated/fact_booking_transactions.csv` | 9,956 | 45 | One row per passenger ticket coupon | BookingTransactionKey |
| `data/03_curated/fact_booking_transactions.parquet` | 9,956 | 45 | One row per passenger ticket coupon | BookingTransactionKey |
| `data/03_curated/fact_operating_costs.csv` | 7,480 | 18 | One row per operating-cost ledger line | OperatingCostKey |
| `data/03_curated/fact_operating_costs.parquet` | 7,480 | 18 | One row per operating-cost ledger line | OperatingCostKey |

Both files are written as CSV (UTF-8, no BOM) and Parquet (Snappy compression), matching the existing `fact_flight_operations` output convention.

### 2.2 Generator Scripts

| File | Seed | Description |
|---|---|---|
| `scripts/build_fact_booking_transactions.py` | 3602027 | Deterministic NumPy generator for booking coupons |
| `scripts/build_fact_operating_costs.py` | 3602028 | Deterministic NumPy generator for cost ledger lines |

Both scripts:
- Use fixed random seeds with documented generation parameters
- Never overwrite existing outputs (raise `FileExistsError`)
- Never modify source data
- Write CSV, Parquet, quarantine, and manifest outputs
- Include structural and business-rule validation (assertions) inline

### 2.3 Quarantine Files (staging layer)

| File | Rows | Reason |
|---|---|---|
| `data/02_staging/quarantine/fact_booking_transactions_quarantined.csv` | 0 | MISSING_FX_RATE (OD-04e) |
| `data/02_staging/quarantine/fact_operating_costs_quarantined.csv` | 0 | MISSING_FX_RATE (OD-04e) |

Zero rows were quarantined because all transaction/cost dates fall within the FX rate coverage window (2025-10-01 through 2026-09-30) with exact-date rates available for all 8 currencies. The quarantine files exist with headers for audit trail; no forward-filling was applied.

### 2.4 Manifests

| File | SHA-256 (CSV) | SHA-256 (Parquet) | SHA-256 (Quarantine) |
|---|---|---|---|
| `data/manifests/fact_booking_transactions_manifest.json` | `14556fd8002a0a10020a3346d0ad11017facfb1866a059ba5a2c36a2880e84d0` | `372d8d36e12ebc5d85864e1122bd117cfe5eccec59eaae4f9b15d0c955159b78` | `7690a55dd99cf016e8e4b54945a94e903ff73381636b72a6438cce0fbdcec572` |
| `data/manifests/fact_operating_costs_manifest.json` | `1a95131dec314d0ad346f6563b7d0156ba0e8f5453877484c5a9e40878892784` | `90e8eddf2b93d0acf00a14cd5e930f642518b3d03fd509c08eb3af6f345d00bf` | `bfd30c2c9a37ecd19c52277e28d20107b67cd6a09606bd0e290950fa81ca53a6` |

Manifests follow the existing project convention (file-level SHA-256 via `src/utilities/hashing.py`). No `ManifestHash` canonicalization was introduced because GOV-D-07 is a revised draft, not approved. This is documented in each manifest's governance section.

### 2.5 Validation Tests

| File | Tests | Status |
|---|---|---|
| `tests/unit/test_fact_booking_transactions.py` | 57 | All PASSED |
| `tests/unit/test_fact_operating_costs.py` | 56 | All PASSED |
| **Total** | **113** | **All PASSED** |

Test execution: `python -m pytest tests/unit/test_fact_booking_transactions.py tests/unit/test_fact_operating_costs.py` — 113 passed, 0 failed.

---

## 3. Test Coverage

| Category | FactBookingTransactions | FactOperatingCosts |
|---|---|---|
| Schema and data types | Yes | Yes |
| Primary-key uniqueness | Yes | Yes |
| Business-key uniqueness | Yes | Yes |
| Composite grain-key uniqueness | N/A (single-row business key) | Yes |
| Foreign-key integrity | Yes (8 FKs) | Yes (6 FKs) |
| RouteKey/AirlineKey agree with flight leg | Yes | Yes |
| Passenger/seat-capacity constraints | Yes (PassengerCount = 1, lead time ≥ 0) | N/A |
| Travel/cost date within reporting period | Yes | Yes |
| Currency validity | Yes | Yes |
| Exact-date FX lookup | Yes | Yes |
| Missing-rate quarantine | Yes | Yes |
| No forward-fill | Yes | Yes |
| USD conversion accuracy | Yes | Yes |
| Decimal precision and rounding | Yes (2dp money, 6dp rate) | Yes (2dp money, 6dp rate) |
| Null and invalid-value detection | Yes | Yes |
| Duplicate detection | Yes | Yes |
| Deterministic reproducibility | Yes | Yes |
| Synthetic provenance | Yes | Yes |
| Revenue recognition identities | Yes | N/A |
| Cost category/subcategory integrity | N/A | Yes |
| Cost sign convention | N/A | Yes |
| Manifest hash verification | Yes | Yes |
| GOV-D-07 not claimed approved | Yes | Yes |

---

## 4. Data Coverage

### FactBookingTransactions (9,956 rows)

| Attribute | Value |
|---|---|
| BookingDateKey range | 20251001 – 20260927 |
| TravelDateKey range | 20251001 – 20260930 |
| TransactionStatus distribution | Flown: 5,909; Ticketed: 1,547; Booked: 1,010; Cancelled: 774; Refunded: 499; NoShow: 217 |
| Currencies used | All 8 (USD weighted, AED/QAR/SGD/INR/GBP/EUR/AUD also present) |
| IsRefunded = TRUE | 499 rows |
| RateVersion | FX-2026-11-04-001 |
| ExchangeRateToUSD | 6 decimal places, positive, exact-date lookup |

### FactOperatingCosts (7,480 rows)

| Attribute | Value |
|---|---|
| CostDateKey range | 20251001 – 20260930 |
| CostCategory distribution | Fuel: 1,869; Crew: 1,513; Airport Charges: 1,177; Maintenance: 1,103; Navigation: 710; Other: 379; Overhead: 374; Sales and Distribution: 355 |
| CostAmount sign | Positive (expense): 7,133; Negative (credit/reversal): 347 |
| IsAllocated = TRUE | 1,490 rows |
| Currencies used | All 8 |
| RateVersion | FX-2026-11-04-001 |
| ExchangeRateToUSD | 6 decimal places, positive, exact-date lookup |

---

## 5. Schema Notes

Both fact tables follow the data contracts v1.5 (sections 6.3.2 and 6.3.3) as the existing project convention, with `RateDateKey` and `RateVersion` columns added from the schema decision document (GOV-D-04 Section 4 / Section 5) to satisfy the requirement to "preserve exchange-rate date and version."

OD-04 owner-confirmed currency decisions are applied:
- **OD-04a:** All 8 currencies (AED, QAR, SGD, INR, GBP, EUR, USD, AUD)
- **OD-04b:** USD per one unit; exact-date lookup; 6 decimal places for rate; round final converted amount to 2 decimals; no forward-fill
- **OD-04c:** Rate source `AEROVISION-360-SYNTHETIC-FX-V1`
- **OD-04d:** Rate version `FX-2026-11-04-001`
- **OD-04e:** Missing exact-date rate quarantines the row; no forward-fill
- **OD-04f:** Deterministic algorithmic generation; fixed seed; documented parameters

Flight-operation metrics (AvailableSeats, BookedPassengers, delays, etc.) are NOT duplicated in either fact table, per the "do not duplicate flight-operation metrics unnecessarily" requirement. `FlightOperationKey` is carried as a logical fact reference for lineage and reconciliation only, consistent with the contract's fact-reference rule (Section 7.5 / 8.5).

Cancellation, refund, and adjustment scenarios are handled per contract Section 10.6:
- Cancelled/NoShow/Booked coupons: NetPassengerRevenueUSD = 0
- Ticketed/Flown/Refunded coupons: NetPassengerRevenueUSD = BaseFareUSD − DiscountUSD − RefundUSD
- CancellationFee and NoShowFee are mutually exclusive
- IsRefunded = TRUE when any refund amount > 0
- Operating costs support signed amounts (positive = expense, negative = credit/reversal)

---

## 6. Unresolved Blockers

| Blocker | Impact | Required Action |
|---|---|---|
| **GOV-D-07 ManifestHash canonicalization** is a REVISED DRAFT, not approved | No canonical `ManifestHash` field introduced in manifests; file-level SHA-256 hashes follow existing convention | Owner approval of GOV-D-07 (RFC 8785 JCS) required before a canonical manifest hash standard can be adopted |
| **`ref_cost_classification.csv` does not exist** | T-66 (cost classification reference integrity) cannot be executed against a reference version; cost categories are validated inline against the engineering-proposed taxonomy | `ref_cost_classification.csv` must be created and approved (OD-13 pending) before T-66 can run |
| **`ref_airline_sources.csv` does not exist** | T-75/T-76/T-78 (airline identity provenance) cannot be executed | Airline source verification and reference approval (OD-01B / G3-RV-01) pending |

None of these blockers prevent Stage 1 completion. They are documented for Stage 2+ planning.

---

## 7. Restrictions Observed

Per the Stage 1 strict scope:
- Pages 01, 02, 04: **Not modified**
- Existing flight-operation source data: **Not modified**
- PBIX: **Not modified**
- G3-RV-01: **Not executed**
- T-78: **Not executed**
- G3/G4 approval status: **Not changed**
- GOV-D-07/GOV-D-08 approval status: **Not changed**
- Page 03 visuals: **Not started**

---

## 8. Next Stage Readiness

Stage 1 is complete and all 113 tests pass. The two validated fact tables are ready for Stage 2 (Power Query integration). The unresolved blockers listed in Section 6 do not block Stage 1 but should be addressed before Stage 3 (semantic model) if referential integrity against approved reference versions is required.

**Request: Owner review of Stage 1 results before authorizing Stage 2.**
