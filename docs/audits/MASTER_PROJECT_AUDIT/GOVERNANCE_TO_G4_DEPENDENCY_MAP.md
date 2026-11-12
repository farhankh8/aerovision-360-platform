# AEROVISION 360 — Governance to G4 Dependency Map

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY INVESTIGATION — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Purpose

This document maps the governance decision dependencies required before G4 (Data Generation) can proceed. G4 is blocked until all upstream governance decisions are resolved.

**Key Finding:** G4 cannot proceed until OD-01A, OD-01B, and OD-04 are resolved AND G3-RV-01 is executed. These four blockers must be cleared before any source data can be generated.

---

## 2. Dependency Chain

```
OD-01A (Airline Population) ──┐
OD-01B (Airline Identity Reference) ──┐
OD-04 (Exchange-Rate Policy)      │
                                  ↓
                          G3-RV-01 (Reference Version Approval)
                                     ↓
                              G4 Data Generation (BLOCKED)
```

---

## 3. Dependency Chain Detail

### Level 1: Owner Decisions (Must be resolved first)

| Decision ID | Status | Blocks |
|-------------|--------|--------|
| OD-01A — Airline Population | Owner-confirmed, formal approval pending | G3-RV-01 |
| OD-01B — Airline Identity Reference | Owner-confirmed, formal approval pending | G3-RV-01 |

### 2. Gate (Requires OD-01A and OD-01B)

| Decision ID | Status | Depends On |
|-------------|--------|------------|
| G3-RV-01 — Reference Version Approval | NOT EXECUTED | OD-01A, OD-01B |

### Level 3: Data Generation (Requires G3-RV-01)

| Decision ID | Status | Depends On |
|-------------|--------|------------|
| G4 — Data Generation | BLOCKED | G3-RV-01 |

---

## 4. Affected Deliverables by Blocker

### OD-01A / OD-01B Block (Airline Population & Identity)

| Affected Item | Location | Impact |
|---------------|----------|--------|
| ref_airlines.csv | `data/04_reference/ref_airlines.csv` | NOT CREATED |
| ref_airline_sources.csv | `data/04_reference/ref_airline_sources.csv` | NOT CREATED |
| FactBookingTransactions | `data/03_curated/fact_booking_transactions.csv` | NOT CREATED |
| FactOperatingCosts | `data/03_curated/fact_operating_costs.csv` | NOT CREATED |
| All 14 curated facts | `data/03_curated/` | NOT GENERATED |

### OD-04 Block (Exchange-Rate Policy)

| Affected Item | Location | Impact |
|---------------|----------|--------|
| ref_exchange_rates.csv | `data/04_reference/ref_exchange_rates.csv` | NOT CREATED |
| FactBookingTransactions (currency conversion) | `data/03_curated/fact_booking_transactions.csv` | Cannot create — no exchange rates |
| FactOperatingCosts (currency conversion) | `data/03_curated/fact_operating_costs.csv` | NOT CREATED |

---

## 5. Decision-to-Implementation Path

```
OD-01A (Airline Population) ──┐
OD-01B (Airline Identity) ────┤
                              ├──→ G3-RV-01 (Reference Version Approval)
OD-04 (Exchange-Rate Policy) ─┘
                                ↓
                           G4 Data Generation
                                ↓
                  Staging → Curated → Power BI Model → Report Pages
```

---

## 6. What Can Proceed Without Blockers

| Item | Status | Can Proceed Without Governance Approval? |
|------|--------|------------------------------------------|
| Documentation (DAX, Power Query M, report.json) | Already created | YES — already exists |
| DAX measure definitions | 54 measures defined | YES — already defined in DAX file |
| Power Query M script | 2 of 14 tables defined | PARTIAL — can document remaining 12 |
| Page 05 visuals (already in PBIX) | 13 of 16 visuals exist | YES — already in PBIX |
| DAX measures (54 total) | 54 defined in file | YES — already written |

---

## 10. Conclusion

Four governance blockers prevent data generation (G4):
1. **OD-01A** — Airline Population (owner signature pending)
2. **OD-01B** — Airline Identity Reference (owner signature pending)
3. **OD-04** — Exchange-Rate Policy (unresolved)
4. **G3-RV-01** — Reference Version Approval (not executed)

Until all four are resolved, no source data can be generated, no Power BI model can be populated, and Page 03 Revenue & Finance and Page 04 Cost & Financial Intelligence cannot be implemented.

Page 05 implementation (6 new visuals + 1 new DAX measure) is independent of these blockers and can proceed once the governance decisions affecting the underlying measures are resolved.
