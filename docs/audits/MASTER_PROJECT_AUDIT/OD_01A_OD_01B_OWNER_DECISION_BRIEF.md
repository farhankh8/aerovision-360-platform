# AEROVISION 360 — OD-01A / OD-01B Owner Decision Brief

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Decision ID:** OD-01A (Airline Population), OD-01B (Airline Identity Reference)  
**Decision Date:** 2026-11-08 (prepared)  
**Status:** OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Decision Summary

| Decision ID | Title | Current Status | Owner Decision Required? |
|-------------|-------|----------------|--------------------------|
| OD-01A | Airline Population | Owner-confirmed design, formal signature and approval pending | YES — formal signature required |
| OD-01B | Airline Identity Reference | Owner-confirmed design, formal signature and approval pending | Yes — formal signature required |

---

## 2. OD-01A — Airline Population Decision

### Current State (from `docs/OD01A_AIRLINE_POPULATION_DECISION.md`)

The OD-01A decision document records the owner-confirmed intended population of 10 airlines:
1. Emirates (AIR-0001)
2. Qatar Airways (AIR-0002)
3. Singapore Airlines (AIR-0003)
4. Air India (AIR-0004)
5. IndiGo (AIR-0005)
6. British Airways (AIR-0006)
7. Lufthansa (AIR-0007)
8. Delta Air Lines (AIR-0008)
9. Southwest Airlines (AIR-0009)
10. Qantas (AIR-0010)

### OD-01A Decision Content

The decision document records that:
- The airline population is fixed at 10 airlines for the baseline
- The airline identities are real (Emirates, Qatar Airways, Singapore Airlines, Air India, IndiGo, British Airways, Lufthansa, Delta Air Lines, Southwest Airlines, Qantas)
- All operational, customer, and financial data is synthetic
- No real passenger personal information is used

### Status: OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING

The OD-01A decision document confirms the airline population design, but the formal owner signature and approval date have not been recorded. The document states:

> "OD-01A — Airline Population Decision — Owner-confirmed design, formal signature and approval pending"

### Blocking Impact

OD-01A blocks G3-RV-01 (Reference Version Approval), which in turn blocks G4 (Data Generation). Until OD-01A is formally signed by the owner, no source data can be generated and no reference CSV files can be created.

---

## 2. OD-01B — Airline Identity Reference Decision

### Current State (from `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`)

The OD-01B decision document records:
- AirlineId as the durable business identity
- AirlineKey as the permanent warehouse surrogate
- AirlineName as the commercial brand
- AirlineIATACode and AirlineICAOCode as mutable, version-qualified attributes (NOT keys)
- HomeCountry as country of headquarters/domicile
- AirlineGroup as optional ultimate parent/group brand
- BusinessModelClass as optional analytical classification
- OperatingRegion NOT an airline identity attribute (derived from route/airport geography)
- IsActive and StatusEffectiveDate as lifecycle attributes
- dim_airline is Type 1 baseline

### OD-01B Decision Content

The decision document records the dimension design for dim_airline:
- AirlineId is the durable business identity
- AirlineKey is the permanent warehouse surrogate
- AirlineName is the commercial brand
- AirlineIATACode and AirlineICAOCode are mutable, version-qualified attributes
- HomeCountry is country of headquarters/domicile
- AirlineGroup is optional ultimate parent/group brand
- BusinessModelClass is optional analytical classification
- OperatingRegion is NOT an airline identity attribute
- IsActive and StatusEffectiveDate are lifecycle attributes

### Status: OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING

The OD-01B decision document records the customer identity and reference model design, but the formal owner signature and approval date have not been recorded. The document states:

> "OD-01B — Airline Identity Reference Decision — Owner-confirmed design, formal signature and approval pending"

### Status: OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE AND APPROVAL PENDING

### Blocking Impact

OD-01B blocks G3-RV-01 (Reference Version Approval), which in turn blocks G4 (Data Generation). Until OD-01B is formally signed by the owner, no reference CSV files can be created.

---

## 3. Governance Decision Register Impact

| Decision ID | Current Status | Owner Decision Required? | Blocks |
|-------------|----------------|--------------------------|--------|
| OD-01A | Owner-confirmed design, formal signature pending | Yes — formal signature | Data generation (G4) |
| OD-01B | Owner-confirmed design, formal signature pending | Yes — formal signature | Data generation, reference version creation |

---

## 10. Decision Record Requirements

| Required Element | Status |
|------------------|--------|
| Owner signature | NOT RECORDED |
| Approval date | NOT RECORDED |
| Formal approval document | NOT CREATED |
| Evidence of review | NOT PERFORMED |
