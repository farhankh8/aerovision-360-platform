# AEROVISION 360 — G3-RV-01 Reference Version Execution Readiness

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY INVESTIGATION — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Gate Status

| Gate | Status | Evidence |
|------|--------|----------|
| G3-RV-01 — Airline Reference Version Approval | NOT EXECUTED | Gate artifact not created; reference CSV and manifest do not exist |
| OD-01A | Owner-confirmed design, formal signature pending | `docs/OD01A_AIRLINE_POPULATION_DECISION.md` |
| OD-01B | Owner-confirmed design, formal signature pending | `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` |

**G3-RV-01 is NOT EXECUTED.** It cannot be executed until OD-01A and OD-01B receive formal owner signatures.

---

## 2. G3-RV-01 Prerequisites

| Prerequisite | Status | Evidence | Blocks G3-RV-01? |
|--------------|--------|----------|------------------|
| OD-01A Airline Population Decision | Owner-confirmed design, formal signature pending | `docs/OD01A_AIRLINE_POPULATION_DECISION.md` | Yes |
| OD-01B Airline Identity Reference Decision | Owner-confirmed design, formal signature pending | `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` | Yes |
| Reference CSV files | NOT CREATED | `data/04_reference/` directory exists but contains no `ref_airlines.csv` or `ref_airline_sources.csv` | Yes |
| Reference version manifest | NOT CREATED | `data/manifests/` contains dataset manifests but no reference exchange rate manifest | Yes |
| T-75, T-76, T-78 validation tests | NOT EXECUTED | No test execution evidence | Yes |
| Owner approval date | NOT RECORDED | No approval date in governance records | Yes |

---

## 3. Required Reference Dataset Contents

Once OD-01A and OD-01B are formally approved and G3-RV-01 is executed, the following reference dataset files must be created:

### ref_airlines.csv
| Column | Type | Required | Notes |
|--------|------|----------|-------|
| AirlineId | String(20) | Yes | Durable business identity |
| AirlineIATACode | String(2) | No | Mutable, version-qualified attribute |
| AirlineICAOCode | String(3) | No | Mutable, version-qualified attribute |
| AirlineName | String(100) | No | Commercial brand |
| HomeCountry | String(100) | No | Country of headquarters/domicile |
| HomeCountryCode | String(2) | No | ISO 3166-1 alpha-2 |
| IsActive | boolean | No | Airline operating status |
| StatusEffectiveDate | date | Yes when IsActive=FALSE | Null for baseline active state |
| ReferenceVersion | String(30) | Yes | Version-qualified attribute |

Primary Key: AirlineId + ReferenceVersion

### ref_airline_sources.csv
| Column | Type | Required | Notes |
|--------|------|----------|-------|
| SourceRecordID | String(30) | Yes | Globally unique |
| AirlineId | String(20) | Yes | Resolves to dim_airline.AirlineId |
| AttributeName | String(30) | Yes | Controlled values: AirlineName, LegalName, AirlineIATACode, AirlineICAOCode, HomeCountry, HomeCountryCode, AirlineGroup, IsActive |
| AttributeValue | String(200) | Yes | The attribute value |
| SourceOrganization | String(150) | Yes | Source organization name |
| SourceURL | String(500) | Yes | Source URL (HTTPS only) |
| SourceType | String(30) | Yes | OfficialAirline, GovernmentRegistry, IndustryAuthority, OtherDocumented |
| SourceRetrievedDate | date | Yes | Date source was retrieved |
| SourceVerifiedDate | date | Yes | Date value was verified (>= retrieval date) |
| VerificationStatus | string(20) | yes | VERIFIED, CONFLICTING, UNVERIFIED, SUPERSEDED, QUARANTINED |
| ReferenceVersion | string(30) | yes | References the version |
| CreatedBy | string(100) | yes | Who created the record |
| CreatedDate | date | yes | When created |

Primary Key: SourceRecordID

Primary Key: SourceRecordID

---

## 4. Dependencies

| Dependency | Status | Blocks G3-RV-01? |
|------------|--------|------------------|
| OD-01A formal signature | PENDING | Yes |
| OD-01B formal signature | PENDING | Yes |
| ref_airlines.csv creation | NOT CREATED | Yes |
| ref_airline_sources.csv creation | NOT CREATED | Yes |
| T-75/T-76/T-78 validation | NOT EXECUTED | Yes |

---

## 5. Conclusion

G3-RV-01 cannot be executed until OD-01A and OD-01B receive formal owner signatures and the reference CSV files are created. The gate remains NOT EXECUTED.
