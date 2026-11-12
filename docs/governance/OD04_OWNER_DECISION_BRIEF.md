# OD-04 — Owner Decision Brief: Currency and Exchange-Rate Policy

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** OD04-DB-2026-11-07-001  
**Document Type:** Owner Decision Brief — Exchange-Rate Policy  
**Status:** PREPARED — OWNER DECISION REQUIRED — NOT APPROVED  
**Prepared:** 2026-11-07  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Executive Summary

OD-04 defines the currency and exchange-rate policy for financial reference data in AEROVISION 360. It gates the creation of `FactBookingTransactions` and `FactOperatingCosts`, and therefore blocks all Page 03 Revenue & Finance visuals.

Six technical sub-decisions (OD-04a through OD-04f) require owner decision, plus one formal governance gate (OD-04g). Two additional specification details (OD-04h, OD-04i) are identified as unresolved and require controlled clarification but are not part of the formal approval gate.

| Decision ID | Question | Current Status | Evidence Available? |
|---|---|---|---|
| OD-04a | Currency scope | Owner-confirmed — 8 currencies (AED, QAR, SGD, INR, GBP, EUR, USD, AUD) | Yes — DimCurrency has 8 currencies |
| OD-04b | Exchange-rate convention | Owner-confirmed — USD per unit, exact-date, 6 decimals, no forward-fill | Yes — contract Section 10.2 |
| OD-04c | Rate source | Owner-confirmed — `AEROVISION-360-SYNTHETIC-FX-V1` | Yes — owner-specified synthetic identifier |
| OD-04d | Rate version | Owner-confirmed — `FX-YYYY-MM-DD-NNN` (current: `FX-2026-11-04-001`) | Yes — consistent with airline ReferenceVersion format |
| OD-04e | Missing-date behaviour | Owner-confirmed — No forward-fill; exact-date only; missing rate quarantines row | Yes — contract specifies exact-date only |
| OD-04f | Rate-generation methodology | Owner-confirmed — Deterministic algorithmic generation | Yes — consistent with synthetic-data policy |
| OD-04g | Formal owner approval | PROPOSED — PENDING | N/A — requires owner action |
| OD-04h | Historical rate immutability | UNSPECIFIED — specification gap | No — requires controlled clarification |
| OD-04i | Rate volatility bounds | UNSPECIFIED — specification gap | No — requires controlled clarification |

**Status:** OD-04a through OD-04f are owner-confirmed (2026-11-07). OD-04g (formal owner approval) is pending signature and date. OD-04h and OD-04i are unresolved specification details requiring controlled clarification.

---

## 2. Current Project Position

### 2.1 Page 03 Revenue & Finance Status

Page 03 — Revenue & Finance **cannot be implemented** with existing project data. No monetary data exists anywhere in the project.

| Item | Status | Evidence |
|---|---|---|
| FactBookingTransactions | DOES NOT EXIST | `data/03_curated/` contains only 3 fact tables: fact_flight_operations, fact_disruptions, fact_customer_feedback |
| FactOperatingCosts | DOES NOT EXIST | Same directory |
| ref_exchange_rates.csv | DOES NOT EXIST | `data/04_reference/` does not exist |
| Currency conversion DAX measures | DO NOT EXIST | `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md` contains no monetary measures |
| Power Query for financial facts | DOES NOT EXIST | `AEROVISION360_DataLoad.m` contains 14 tables, none financial |
| T-78 (manifest integrity) | PLANNED/BLOCKED | Requires manifest and reference data |
| Page 03 visuals | BLOCKED | `report.json` contains placeholder text "OD-04 BLOCKED" |

**FL02 is passenger volume, not revenue.** `FL02 = SUM(fact_flight_operations[RevenuePassengers]) = 218,413` passengers. It must never be formatted as currency or labeled as revenue.

**Evidence:** `docs/PAGE_03_REVENUE_FINANCE_DATA_AUDIT.md` Section 9; `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md`; `deliverables/power_bi/dax/AEROVISION360_Measures.dax` line 5.

### 2.2 Existing Dimension Currency (dim_currency)

**File:** `data/03_curated/dim_currency.csv`  
**Status:** Exists in curated layer; 8 rows; versioned manifest at `data/manifests/dim_currency_manifest.json`

| CurrencyKey | CurrencyCode | CurrencyName | CurrencySymbol | DecimalPlaces | IsReportingCurrency |
|---|---|---|---|---|---|
| 1 | AED | UAE Dirham | د.إ | 2 | False |
| 2 | QAR | Qatari Riyal | ر.ق | 2 | False |
| 3 | SGD | Singapore Dollar | S$ | 2 | False |
| 4 | INR | Indian Rupee | ₹ | 2 | False |
| 5 | GBP | Pound Sterling | £ | 2 | False |
| 6 | EUR | Euro | € | 2 | False |
| 7 | USD | US Dollar | $ | 2 | True |
| 8 | AUD | Australian Dollar | A$ | 2 | False |

**Evidence:** `data/03_curated/dim_currency.csv`; `data/manifests/dim_currency_manifest.json`

**Key fact:** USD is the only reporting currency (`IsReportingCurrency = TRUE`). All other currencies are dimensional attributes with no associated fact data and no exchange rates.

### 2.3 OD-04 Proposed Currency Set

**File:** `docs/OD04_OWNER_DECISION_PACKAGE.md` (Decision 1 — Currency scope)  
**Proposed set:** USD, EUR, GBP, JPY, CAD (5 currencies)

**Mismatch with DimCurrency:**
- DimCurrency has 8 currencies; OD-04 proposes 5
- Currencies in DimCurrency but NOT in OD-04: AED, QAR, SGD, INR, AUD (5 currencies would lack exchange rates)
- Currencies in OD-04 but NOT in DimCurrency: JPY, CAD (rates would reference nonexistent dimension keys)

**Impact:** `FactBookingTransactions.TransactionCurrencyKey → DimCurrency`; `FactOperatingCosts.CurrencyKey → DimCurrency`. Any non-USD financial row requires an exchange rate against a DimCurrency currency code. If OD-04's 5-currency set is enforced without updating DimCurrency, 3 DimCurrency currencies have no conversion path.

**Evidence:** `docs/OD04_OWNER_DECISION_PACKAGE.md` Decision 1; `docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md` Section 4; `data/03_curated/dim_currency.csv`

---

## 4. OD-04 Component Analysis

### OD-04a — Currency Scope

**Options:**

| Option | Currency Set | Rationale | Risk |
|---|---|---|---|
| **Option 1 — Expand to all 8 DimCurrency currencies** | AED, QAR, SGD, INR, GBP, EUR, USD, AUD | Matches implemented dimension; no orphaned dimension members | Larger rate table; more owner-approved rate values |
| Option 2 — Restrict to OD-04 5 currencies | USD, EUR, GBP, JPY, CAD | Matches OD-04 text | JPY and CAD not in DimCurrency → orphaned rate rows; 3 DimCurrency currencies (AED, QAR, SGD, INR, AUD — actually 5 not in OD-04 set) would have no exchange rate |
| Option 3 — Owner-specified custom set | Owner-defined set | Owner determines analytical currency scope | Requires DimCurrency amendment or orphaned rows; highest documentation burden |

**Recommendation: Option 1** — Expand OD-04 to cover all 8 existing DimCurrency currencies. This matches the already-implemented dimension and avoids orphaned records. Owner must confirm all 8 currencies are analytically relevant.

**Confidence:** High — contract requirement for exact-dimension matching is clear; expanding OD-04 is the lowest-risk path.

---

### OD-04b — Exchange-Rate Convention

**Options:**

| Attribute | Option A (Recommended) | Option B | Option C |
|---|---|---|---|
| Direction | USD per one unit of transaction currency | One unit of USD per transaction currency | Mixed by currency |
| Precision | 6 decimal places | 4 decimal places | Variable by currency |
| Lookup rule | Exact date (transaction date for bookings, cost date for costs) | Period-average | Last-known rate |
| Rounding | Round final AmountUSD to 2 decimals | Round rate first | Round at each step |
| Forward-fill | Not allowed | Allowed with max gap N days | Not allowed |

**Recommendation: Option A** — USD per one unit, exact-date lookup, 6 decimal places, round final amount only. This matches the existing contract Section 10.2 exactly.

**Confidence:** High — contract already specifies this; deviation requires contract amendment.

---

### OD-04c — Exchange-Rate Source

**Current state:** No rate source has been identified anywhere in the project. No API configuration, source document, or methodology exists.

**Options:**

| Option | Source | Evidence | Viability |
|---|---|---|---|
| 3a | "AEROVISION-360-SYNTHETIC-FX-V1" | Proposed in OD04 document | Viable as synthetic identifier; requires owner approval |
| 3b | "SIMULATED-FX-V1" | Proposed in OD04 document | Viable but generic |
| 3c | Owner-specified | Not specified | Requires owner input |
| — | Live market rates | Not referenced anywhere | REJECTED — violates synthetic simulation policy |

**Recommendation:** Defer until owner confirms source identifier. Do not invent rate source names.

**Confidence:** Low — no evidence exists; owner decision required.

---

### OD-04d — Rate Version

**Current state:** No rate version convention exists. `ref_exchange_rates.csv` does not exist.

**Options:**

| Option | Version Value | Rationale |
|---|---|---|
| 4a | "FX-2026-11-04-001" | Date-based, deterministic, reproducible |
| 4b | "FX-V1" | Simple version label |
| 4c | Owner-specified | Owner-defined |

**Recommendation: Option 4a** — date-based versioning matches project conventions (ReferenceVersion format `AIR-YYYY-MM-DD-NNN` used for airline reference versions).

**Confidence:** Medium — pattern consistent with existing ReferenceVersion scheme, but owner must approve.

---

### OD-04e — Missing-Date Behaviour

**Current state:** Contract explicitly states forward-filling is NOT allowed unless explicitly approved. Missing rate → quarantine the financial row (DQ-08, High severity).

**Options:**

| Option | Behaviour | Rationale | Risk |
|---|---|---|---|
| 5a | No forward-fill; exact-date only; missing rate quarantines row | Matches current contract; simplest; most auditable | Higher row rejection rate on weekends/holidays |
| 5b | Forward-fill with max gap N days + `IsCarriedForward` flag | Reduces row count; handles weekends/holidays | Requires contract amendment; staleness risk |
| 5c | Period-average rate | Fewer rate rows | Explicitly not allowed by contract; requires amendment |

**Recommendation: Option 5a** — No forward-fill; exact-date only. Matches current contract; simplest; most auditable.

**Confidence:** High — contract already specifies this; changing requires amendment.

---

### OD-04f — Rate-Generation Methodology

**Current state:** No rate-generation methodology exists. No rate values exist.

**Options:**

| Option | Methodology | Rationale | Risk |
|---|---|---|---|
| 6a | Owner-provided static rate table | Maximum control; exact values known | Maximum owner effort |
| 6b | Deterministic algorithmic generation (seed-based) | Reproducible; lower owner effort | Requires owner approval of algorithm |
| 6c | Hybrid: algorithmic base + owner overrides | Balanced control | Complexity |

**Recommendation: Option 6b** — deterministic algorithmic generation. Reproducible; lower owner burden; consistent with project's synthetic simulation disclosure.

**Confidence:** Medium — requires owner approval of algorithm and parameters.

---

## 5. Financial Data Dependencies

| Component | Dependency | Status |
|---|---|---|
| FactBookingTransactions | OD-04 approved; `ref_exchange_rates.csv` exists; rate coverage includes all booking dates | BLOCKED |
| FactOperatingCosts | OD-04 approved; `ref_exchange_rates.csv` exists; rate coverage includes all cost dates | BLOCKED |
| Net Passenger Revenue | FactBookingTransactions[NetPassengerRevenueUSD] | NOT AVAILABLE — fact table missing |
| Operating Cost USD | FactOperatingCosts[CostAmountUSD] | NOT AVAILABLE — fact table missing |
| RASK | Revenue / ASK | NOT AVAILABLE — revenue numerator missing |
| CASK | Operating Cost / ASK | NOT AVAILABLE — cost numerator missing |
| Yield | Passenger Revenue / RPK | NOT AVAILABLE — revenue numerator missing |

**Evidence:** `docs/PAGE_03_REVENUE_FINANCE_READINESS.md` Section 5; `docs/PAGE_02_OPERATIONS_DAX_SPECIFICATION.md` Section 4.

---

## 6. Recommended Owner Decisions

| Decision ID | Question | Recommended Decision | Evidence Basis |
|---|---|---|---|
| OD-04a | Currency scope | Option 1 — Expand to 8 currencies matching DimCurrency | Matches existing DimCurrency; avoids orphaned records |
| OD-04b | Exchange-rate convention | USD per one unit; exact-date; 6 decimals; no forward-fill; round final amount only | Matches contract Section 10.2 |
| OD-04c | Rate source | Owner to confirm synthetic source identifier | No existing evidence; owner input required |
| OD-04d | Rate version | "FX-YYYY-MM-DD-NNN" date-based version | Consistent with airline ReferenceVersion format |
| OD-04e | Missing-date behaviour | No forward-fill; exact-date only; missing rate quarantines row | Matches current contract |
| OD-04f | Rate-generation methodology | Deterministic algorithmic generation (owner-approved parameters) | Reproducible; consistent with synthetic simulation |
| OD-04g | Formal owner approval | Owner must approve all above | Required before any financial fact table creation |

**Critical:** None of these decisions can be delegated to implementation. All require explicit owner approval before `ref_exchange_rates.csv` or any financial fact table can be created.

---

## 7. Owner Decision Table

| Decision ID | Question | Option 1 | Option 2 | Option 3 | Owner Selection |
|---|---|---|---|---|---|
| OD-04a | Currency scope | 8 currencies (all DimCurrency) | 5 currencies (USD, EUR, GBP, JPY, CAD) | Owner-specified custom set | [BLANK] |
| OD-04b | Exchange-rate convention | USD per unit, exact-date, 6 decimals, no forward-fill | Other convention | Owner-specified | [BLANK] |
| OD-04c | Rate source | "AEROVISION-360-SYNTHETIC-FX-V1" | "SIMULATED-FX-V1" | Owner-specified | [BLANK] |
| OD-04d | Rate version | "FX-YYYY-MM-DD-NNN" | "FX-V1" | Owner-specified | [BLANK] |
| OD-04e | Missing-date behaviour | No forward-fill; exact-date only | Forward-fill with max gap + flag | Period-average | [BLANK] |
| OD-04f | Rate-generation | Owner-provided static table | Deterministic algorithmic | Hybrid base + owner overrides | [BLANK] |
| OD-04g | Formal OD-04 approval | APPROVE | REJECT | RETURN FOR REVISION | [BLANK] |

**Owner signature:** ______________________________  
**Approval date:** ______________________________

---

## 8. Implementation Readiness Conditions

**Prerequisites for Page 03 financial visuals:**

| Prerequisite | Status | Owner Action Required? |
|---|---|---|
| OD-04 formal approval (all sub-decisions) | PROPOSED — PENDING | Yes |
| Currency set reconciliation (OD-04 5 vs DimCurrency 8) | PENDING | Yes |
| RateSource value selection | UNSPECIFIED | Yes |
| RateVersion value selection | UNSPECIFIED | Yes |
| Rate coverage period approval | UNSPECIFIED | Yes |
| Individual rate values or algorithm approval | UNSPECIFIED | Yes |
| `ref_exchange_rates.csv` creation | BLOCKED by OD-04 | N/A — implementation after approval |
| FactBookingTransactions implementation | BLOCKED by OD-04 | N/A |
| FactOperatingCosts implementation | BLOCKED by OD-04 | N/A |
| Financial DAX measures | NOT CREATED | N/A — after fact tables exist |

**Immediate next action:** Owner approves OD-04 currency scope (Option 1: all 8 DimCurrency currencies).

---

## 9. End of Decision Brief

This document prepares the owner decision for OD-04. No owner decision has been made. No exchange rates have been invented. No financial fact tables have been created. No implementation activity is authorized.

**Approvals required before Page 03 implementation can begin:**

1. OD-04 formal approval (this document)
2. `ref_exchange_rates.csv` creation with owner-approved rates
3. FactBookingTransactions and FactOperatingCosts implementation
4. Financial DAX measures
5. Page 03 visual build

**All prerequisite activities remain blocked until OD-04 is formally approved.**
