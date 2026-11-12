# GOV-D-06 — Staleness Threshold Decision

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** GOV-D-06-2026-11-07-001  
**Document Type:** Owner Decision Draft — Staleness Threshold Approval  
**Status:** OWNER ACCEPTED — FORMAL GOVERNANCE APPROVAL PENDING  
**Prepared:** 2026-11-07  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Decision Purpose

This decision record establishes the staleness thresholds for reference-data verification in AEROVISION 360. Staleness thresholds define how long a verified source record may remain in force before it must be re-verified, and when a stale record must be escalated to quarantine status. Without approved thresholds, `G3-RV-01` (reference-version approval) cannot determine whether a source is eligible to support an approved reference version, and OD-01A/OD-01B cannot be signed.

This decision record records the project owner's previously communicated threshold values for formal documentation. It does **not** constitute formal governance approval.

---

## 2. Owner-Confirmed Decision

| Attribute | Value |
|---|---|
| Decision ID | GOV-D-06 |
| Decision Title | Staleness Threshold Approval |
| Owner | KH Mohammad Farhan — Project Owner |
| Status | OWNER ACCEPTED — FORMAL GOVERNANCE APPROVAL PENDING |
| Decision Date | 2026-11-06 |
| Confirmation Source | ChatGPT conversation, 2026-11-06 |

### 2.1 Owner-Confirmed Staleness Thresholds

| Attribute Category | Threshold | Applies To |
|---|---|---|
| Stale Threshold | 365 days | Airline name, legal name, airline group attributes |
| Critical Threshold | 180 days | Airline IATA code, Airline ICAO code attributes |

### 2.2 Decision Rationale

Reference-data freshness thresholds ensure that airline identity attributes remain current and verifiable. A stale threshold defines how long a verified source record may remain in force before it must be re-verified. A critical threshold defines when a stale record must be escalated to quarantine status.

The 365-day threshold applies to name, legal name, and group attributes — attributes that change infrequently. The 180-day threshold applies to IATA and ICAO codes — attributes that change more frequently and require more frequent re-verification.

### 2.3 Scope of Application

The staleness thresholds apply to:

- `ref_airlines.csv` — Airline name, legal name, group attributes
- `ref_airline_sources.csv` — Airline IATA code, Airline ICAO code attributes

Staleness is measured from `SourceVerifiedDate` to the reference-version approval date (or the current date if earlier). A stale record is quarantined with `QuarantineReason = STALE` and cannot support a populated attribute in an approved version until re-verified.

---

## 3. Contract Context

Contract v1.5 (`docs/03_DATA_CONTRACTs.md`), Section 9.4 (line 260), states:

> "Staleness: the proposed maximum age is 365 days for names, legal names and group, and 180 days for IATA and ICAO codes, measured from `SourceVerifiedDate` to the reference-version approval date (or the current date if earlier). A stale record is `QUARANTINED` with `STALE` and cannot support a new approved version until re-verified. These thresholds are proposed policy, not owner-approved values."

The contract establishes the staleness concept but leaves the specific numerical thresholds as proposed policy. This decision record records the owner-confirmed threshold values (365 days general, 180 days for codes) that were previously communicated by the project owner on 2026-11-06.

---

## 4. Technical Implications

### 4.1 Staleness Measurement

Staleness age is measured as:

```
Staleness Age = Reference Version Approval Date (or Current Date if earlier) − SourceVerifiedDate
```

If `Staleness Age > Staleness Threshold`, the record is considered stale and must be quarantined with `QuarantineReason = STALE`.

### 4.2 Threshold Application

| Attribute Category | Threshold | Re-verification Required When |
|---|---|---|
| Airline Name | 365 days | `SourceVerifiedDate` is more than 365 days before reference-version approval date |
| Legal Name | 365 days | `SourceVerifiedDate` is more than 365 days before reference-version approval date |
| Airline Group | 365 days | `SourceVerifiedDate` is more than 365 days before reference-version approval date |
| Airline IATA Code | 180 days | `SourceVerifiedDate` is more than 180 days before reference-version approval date |
| Airline ICAO Code | 180 days | `SourceVerifiedDate` is more than 180 days before reference-version approval date |

### 4.3 Quarantine Behavior

When a record becomes stale:

1. `VerificationStatus` changes from `VERIFIED` to `QUARANTINED`
2. `QuarantineReason` is set to `STALE`
3. The record cannot support a populated attribute in an approved version until re-verified
4. The airline record becomes incomplete if the stale record supported a required identity attribute
5. The optional attribute remains null if no other `VERIFIED` record exists

### 4.4 Re-verification Process

When a stale record is re-verified:

1. Source content is re-captured
2. `SourceRetrievedDate` is updated to the re-capture date
3. `SourceVerifiedDate` is updated to the re-verification date
4. `EvidenceHash` is recalculated against the new capture
5. `VerificationStatus` returns to `VERIFIED` if the value still matches
6. `IsAuthoritative` remains `TRUE` if it was the authoritative record

---

## 5. Approval Requirements

This decision record records owner-confirmed thresholds that require **formal governance approval**. The following elements are recorded:

| Decision Element | Accepted Value | Formal Approval Status |
|---|---|---|
| Stale Threshold (Name/Legal Name/Group) | 365 days | PENDING — Formal governance approval required |
| Critical Threshold (IATA/ICAO Code) | 180 days | PENDING — Formal governance approval required |
| Anchor Date | SourceVerifiedDate to reference-version approval date | PENDING — Formal governance approval required |
| Stale Action | QUARANTINE with QuarantineReason = STALE | PENDING — Formal governance approval required |
| Exception Policy | 90-day exception policy to be defined | PENDING — Owner decision required |

---

## 6. Approval Requirements Block

| Field | Entry |
|---|---|
| Decision | [ ] OWNER ACCEPTED   [ ] FORMALLY APPROVED   [ ] RETURNED FOR REVISION |
| Approval scope | GOV-D-06 — Staleness Threshold Approval (365/180 days) |
| Owner name | KH Mohammad Farhan |
| Owner decision | OWNER ACCEPTED — thresholds confirmed |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no formal approval date recorded] |
| Approval conditions | [BLANK — to be completed at formal approval] |
| Signed-copy path | [BLANK — no docs/approvals/ structure] |
| Signed-copy SHA-256 | [BLANK — no signed copy exists] |
| Retention confirmed | [ ] Yes   [X] No — GOV-D-08 PENDING |
| Verification date/result | [BLANK — PENDING] |

**Formal signature:** ______________________________  
**Formal approval date:** ______________________________  

**Approval status:** OWNER ACCEPTED — formal governance approval pending. Thresholds are confirmed by the owner but not yet formally approved through governance channels.

---

## 7. End of Decision Record

This document records the owner-confirmed staleness thresholds for reference-data verification. No source files, data, DAX, Power Query, semantic model, Power BI, or other project artifacts were modified during its creation. No signature, formal approval date, reviewer identity, or formal governance approval evidence has been created. GOV-D-06 remains pending formal governance approval.
