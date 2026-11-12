# GOVERNANCE DECISION PACK — AEROVISION 360

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Document ID:** GD-2026-11-06-001  
**Document Type:** Governance Decision Pack — Preparation for Formal Approval  
**Status:** COMPLETE — READY FOR OWNER REVIEW  
**Prepared:** 2026-11-06  
**Prepared by:** Enterprise Data Governance Architect (non-independent)  
**Project Owner / Approver:** KH Mohammad Farhan  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance  

---

## 1. Executive Governance Summary

### 1.1 Bottom Line

AEROVISION 360 has complete engineering design documentation across all layers (data contracts, semantic model blueprint, DAX KPI catalogue, dashboard specification, QA blueprint, implementation roadmap) and all curated source data has been validated (14 datasets, 0 duplicates, 0 orphan keys, referential integrity intact). However, **no formal governance decisions have been signed**, and **no gate has been approved**.

The project is **READY WITH BLOCKERS**. All nine outstanding blockers must be resolved through formal owner decisions and signatures before any data generation, schema freeze, Power BI implementation, or report building can proceed.

### 1.2 Current Governance Status

| Area | Status | Evidence Location |
|---|---|---|
| G1 — Environment | IN PROGRESS | Progress Ledger |
| G2 — Scope | PASS | Progress Ledger |
| G3 — Data design gate execution | NOT STARTED | Progress Ledger |
| G3 — Data design documentation | PREPARED — DRAFT | Progress Ledger |
| G3 — Data design formal approval | NOT FORMALLY APPROVED | Progress Ledger |
| Schema freeze | NOT AUTHORIZED | Progress Ledger |
| G3-RV-01 — Reference version approval | NOT EXECUTED | Progress Ledger |
| G4 — Data generation | BLOCKED | Progress Ledger |
| G5–G10 | NOT STARTED | Progress Ledger |
| OD-01A — Airline population | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE PENDING | OD01A_AIRLINE_POPULATION_DECISION.md |
| OD-01B — Airline identity/reference | OWNER-CONFIRMED DESIGN — FORMAL SIGNATURE PENDING | OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md |
| OD-04 — Exchange-rate policy | PROPOSED — OWNER APPROVAL REQUIRED | OD04_OWNER_DECISION_PACKAGE.md |
| Independent reviewer | NOT AVAILABLE | Owner Decisions 2026-11-04 |

### 1.3 What This Pack Contains

| Document | Purpose |
|---|---|
| GOVERNANCE_DECISION_PACK.md | Executive summary and full decision-by-decision treatment |
| GOVERNANCE_DECISION_REGISTER.md | Decision register with status classifications |
| GOVERNANCE_APPROVAL_MATRIX.md | Approval matrix with evidence requirements |
| GOVERNANCE_SIGNATURE_CHECKLIST.md | Signature checklist for formal execution |
| GOVERNANCE_DEPENDENCY_MAP.md | Dependency and sequencing map |

### 1.4 What This Pack Does NOT Do

- It does not sign or approve any decision.
- It does not freeze any schema.
- It does not authorize data generation, reference-data creation, synthetic data, Python pipeline, Power Query, semantic model, DAX, Power BI, G3, or G4.
- It does not fabricate signatures, approval dates, or reviewer identities.
- It does not modify any existing document, dataset, DAX measure, PBIX file, or Power Query script.

---

## 2. Current Governance Status

### 2.1 Gate Status Matrix

| Gate | Name | Status | Next Action | Owner Decision Required |
|---|---|---|---|---|
| G1 | Environment | IN PROGRESS | Complete disk, path, and dependency review | No |
| G2 | Scope | PASS | Maintain traceability | No |
| G3 | Data design | NOT STARTED / NOT FORMALLY APPROVED | OD-01A/OD-01B signatures; critical decisions; G3-RV-01; schema freeze; G3 gate review | Yes |
| G3-RV-01 | Reference version approval | NOT EXECUTED | Approved manifest and reference version | Yes |
| G4 | Data generation | BLOCKED | G3 APPROVED; written G4 authorization | Yes |
| G5–G10 | Data quality through release | NOT STARTED | Depend on G4 | No (downstream) |

### 2.2 Decision Status Summary

| Decision ID | Decision Title | Classification | Formal Signature | Approval Date | Blocker |
|---|---|---|---|---|---|
| OD-01A | Airline population | OWNER-DIRECTED | No | No | Re-audit preconditions; H-04, H-05, M-07, M-12; B-03–B-08 |
| OD-01B | Airline identity/reference | OWNER-DIRECTED | No | No | Re-audit preconditions; H-04, H-05, M-07, M-12; B-03–B-08 |
| OD-04 | Exchange-rate policy | OWNER-DIRECTED | No | No | Currency mismatch; 7 sub-decisions; RateSource; RateVersion |
| OD-04a | Currency scope | OWNER-DIRECTED | No | No | 5 vs 8 currency mismatch |
| OD-04b | Exchange-rate convention | OWNER-DIRECTED | No | No | USD/unit; 6 decimals; exact-date; no forward-fill |
| OD-04c | Rate source | OWNER-DIRECTED | No | No | RateSource value (3a/3b/3c) |
| OD-04d | Rate version | OWNER-DIRECTED | No | No | RateVersion value (4a/4b/4c) |
| OD-04e | Missing-date behaviour | OWNER-DIRECTED | No | No | No forward-fill (5a) |
| OD-04f | Rate-generation methodology | OWNER-DIRECTED | No | No | Static (6a)/algorithmic (6b)/hybrid (6c) |
| G3-RV-01 | Reference version approval | NOT READY | No | No | Depends on OD-01A/OD-01B/OD-04 |
| Schema freeze | Schema authorization | NOT READY | No | No | Depends on OD-01A/OD-01B/critical decisions |
| G3 | Data design formal approval | NOT READY | No | No | Depends on OD-01A/OD-01B/G3-RV-01/schema freeze |
| G4 | Data generation authorization | NOT READY | No | No | Depends on G3 APPROVED |
| Independent reviewer | Reviewer assignment | NOT READY | No | No | Not assigned |
| Compensating control | Owner self-review route | OWNER-DIRECTED | No | No | Compensating control not executed |

---

## 3. Decision Ownership and Accountability

| Decision ID | Decision Owner | Approval Authority | Reviewer Route | Reviewer Assigned | Independent Assurance |
|---|---|---|---|---|---|
| OD-01A | KH Mohammad Farhan | Project Owner | Compensating control (D-01/D-02) | Not assigned | Not claimed |
| OD-01B | KH Mohammad Farhan | Project Owner | Compensating control (D-01/D-02) | Not assigned | Not claimed |
| OD-04 | KH Mohammad Farhan | Project Owner | Compensating control (D-01/D-02) | Not assigned | Not claimed |
| OD-04a–OD-04f | KH Mohammad Farhan | Project Owner | Compensating control (D-01/D-02) | Not assigned | Not claimed |
| G3-RV-01 | KH Mohammad Farhan | Project Owner | Compensating control (D-01/D-02) | Not assigned | Not claimed |
| Schema freeze | KH Mohammad Farhan | Project Owner | Compensating control (D-01/D-02) | Not assigned | Not claimed |
| G3 | Gate review panel | Project Owner | Compensating control (D-01/D-02) | Not assigned | Not claimed |
| G4 | KH Mohammad Farhan | Project Owner | Compensating control (D-01/D-02) | Not assigned | Not claimed |

**Reviewer limitation:** No independent reviewer has been assigned. AI-assisted review is not independent assurance. Owner self-review is a separate activity and has not been executed or recorded as evidence. The compensating-control route is accepted under D-01/D-02 but execution is not complete.

---

## 4. OD-01A Decision — Airline Population

### 4.1 Decision Statement

**Owner-confirmed design (not formally signed):**

1. The baseline population is exactly ten real airline identities listed in Section 3.
2. The identities are real; every populated identity attribute must be source-verified at attribute level before a reference version is approved.
3. Operational, customer, booking, revenue, cost, disruption, feedback, and financial records for the ten airlines are synthetic simulations.
4. The reporting period is 2025-10-01 through 2026-09-30, inclusive.
5. Every report page, tooltip while a page is visible, and exported result must carry the exact unconditional disclosure `Synthetic Simulation — Not Actual Airline Performance`.
6. No additional airline may be added, and no listed airline may be removed or substituted without controlled change and formal approval.
7. The population is fixed for the baseline. A merger, rebrand, successor entity, or code change is handled under OD-01B and contract Section 3.4.
8. This record does not authorize reference-data creation, synthetic-data generation, schema freeze, Power BI implementation, or a G3/G4 advance.

### 4.2 Fixed Airline Population

| # | Airline | IATA | ICAO | Home Country | Country Code | Proposed AirlineId | Proposed AirlineKey |
|---|---|---|---|---|---|---|---|
| 1 | Emirates | EK | UAE | United Arab Emirates | AE | AIR-0001 | 1 |
| 2 | Qatar Airways | QR | QTR | Qatar | QA | AIR-0002 | 2 |
| 3 | Singapore Airlines | SQ | SIA | Singapore | SG | AIR-0003 | 3 |
| 4 | Air India | AI | AIC | India | IN | AIR-0004 | 4 |
| 5 | IndiGo | 6E | IGO | India | IN | AIR-0005 | 5 |
| 6 | British Airways | BA | BAW | United Kingdom | GB | AIR-0006 | 6 |
| 7 | Lufthansa | LH | DLH | Germany | DE | AIR-0007 | 7 |
| 8 | Delta Air Lines | DL | DAL | United States | US | AIR-0008 | 8 |
| 9 | Southwest Airlines | WN | SWA | United States | US | AIR-0009 | 9 |
| 10 | Qantas | QF | QFA | Australia | AU | AIR-0010 | 10 |

**Note:** The AirlineId/AirlineKey allocation is a proposed administrative allocation defined in OD-01B. It is not approved by OD-01A and is not a source-verified identity fact.

### 4.3 Evidence Index

| Evidence ID | Evidence | Classification | Location / Hash | Use |
|---|---|---|---|---|
| E-01 | Owner decision confirmation | RECORDED | docs/OD01_OWNER_DECISION_CONFIRMATION.md; SHA-256 AC6A95B4... | Confirms eight design choices; not a signature |
| E-02 | Owner decision resolution | RECORDED | docs/OD01_OWNER_DECISION_RESOLUTION.md; SHA-256 BE62CBDC01... | Decision basis and alternatives |
| E-03 | Remediation design specification | RECORDED | docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md; SHA-256 CC3BCE62... | Technical design source |
| E-04 | Independent governance audit | RECORDED | docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md; SHA-256 FD94BD36... | Findings and required corrections |
| E-05 | Data contract v1.5 | RECORDED DESIGN — PENDING REVIEW | docs/03_DATA_CONTRACTS.md; SHA-256 D1CE4011... | Controlling schema and identity rules |
| E-06 | Migration final report | RECORDED | docs/OD01_MIGRATION_FINAL_REPORT_20261101_204216.txt | Prior controlled migration evidence |
| E-07 | Project scope | RECORDED — CURRENT | docs/01_PROJECT_SCOPE.md v1.1; SHA-256 9A9EEA41...; 6,384 bytes | Current governing scope |
| E-08 | Reference manifest | NOT CREATED | data/manifests/reference_versions.csv design only | Required before reference approval |
| E-09 | Airline source records | NOT CREATED | data/04_reference/ remains empty | Required for attribute-level provenance |
| E-10 | Validation tests T-72 to T-79 | NOT EXECUTED | qa/results/; T-79 BLOCKED | Required before G3/G4 |
| E-11 | Formal OD-01A signature | PENDING | This record, Section 7 | Required to close OD-01A |
| E-12 | Independent reviewer / external verification | NONE RECORDED | Not assigned; D-02 limitation recorded | No independent assurance claimed |

### 4.4 Formal Approval Block

| Field | Entry |
|---|---|
| Decision | [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION |
| Approval scope | OD-01A Sections 2, 3, and 4 only |
| Exclusions | OD-01B; reference CSVs; schema freeze; synthetic data; production ETL; Power Query; Power BI; G3; G4 |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Approval conditions | [BLANK — to be completed at signature] |
| Reviewer route | Compensating-control route accepted under D-01/D-02; independent reviewer not assigned |
| Compensating-control acceptance | D-01/D-02 accepted; execution not complete |
| Reviewer limitation statement | No independent reviewer; AI review is not independent assurance |
| Reviewer name / role / organization | [BLANK — no reviewer assigned] |
| Reviewer independence | [ ] Independent   [ ] Not independent   [X] N/A — no reviewer |
| Reviewer result | [ ] CONCUR   [ ] CONCUR WITH RESERVATIONS   [ ] DISSENT   [X] N/A — no reviewer |
| Reviewer signature / date | [BLANK — no reviewer signature] |
| Residual concerns | H-04, H-05, M-07, M-12 open pending re-audit; B-03–B-08 open; no independent assurance |
| Re-audit record | [BLANK — PENDING] |
| Scope v1.1 SHA-256 | 9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C |
| Contract v1.5 SHA-256 | D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9 |
| Signed-copy path | [BLANK — D-08 PENDING; no docs/approvals/ structure] |
| Signed-copy SHA-256 | [BLANK — no signed copy exists] |
| Retention confirmed | [ ] Yes   [X] No — D-08 PENDING |
| Verification date / result | [BLANK — PENDING] |

**Formal signature:** ______________________________  
**Approval date:** ______________________________  

**Approval status:** PENDING. Not approved for reference-data creation, synthetic-data generation, schema freeze, Power BI implementation, or G3/G4 advance.

---

## 5. OD-01B Decision — Airline Identity and Reference

### 5.1 Decision Statement

**Owner-confirmed design (not formally signed):**

1. OD-01 is split into OD-01A (population) and OD-01B (identity and reference model). Each requires a separate formal signature.
2. `AirlineId` is the durable business identity. `AirlineKey` is the permanent warehouse surrogate used by facts and Power BI relationships. They are not interchangeable.
3. IATA and ICAO codes are mutable attributes, unique within a reference version. They are not primary keys, foreign keys, or provenance joins.
4. `AirlineName` is the commercial brand. `LegalName` is optional and remains in the reference/provenance layer only; it is not a `DimAirline` column.
5. `HomeCountry` is the country of the airline's principal headquarters or domicile. `AirlineGroup` is the optional ultimate parent company or group brand and is not inferred.
6. `BusinessModelClass` is an optional analytical classification, not a source-verified identity attribute. `OperatingRegion` is removed from the airline identity model; analytical region is derived from route and airport geography. D-05 remains PENDING; this revision does not authorize a populated `BusinessModelClass` baseline or a mapping/rubric.
7. The minimal lifecycle uses `IsActive` and `StatusEffectiveDate`. `LifecycleStatus` and `MergedIntoAirlineId` are deferred and are not columns.
8. `DimAirline` is Type 1. Immutable reference snapshots preserve build reproducibility, but Type 1 does not preserve as-was historical identity labels. Type 2 is deferred until a future requirement demands it.
9. The reference manifest is the authoritative approval record. `DimAirline.ReferenceVersion` is technical lineage only. Every generation and refresh pins exactly one approved reference version and validates key consistency.
10. The airline key map is controlled and immutable after approval. The same `AirlineId` always resolves to the same `AirlineKey`, independent of row order, rebuild, or database identity sequence. Historical facts are never re-keyed.
11. Reference-version approval uses `G3-RV-01`, not an OD-series decision. OD-23 is rejected and is not created. REQ-028 and T-78 are retained.
12. The exact unconditional disclosure `Synthetic Simulation — Not Actual Airline Performance` is required on every report page, tooltip while a page is visible, and exported result.

### 5.2 Key Hierarchy

| Identifier | Type | Scope | Assigned by | Mutable? | Reused? | Used for | Not used for |
|---|---|---|---|---|---|---|---|
| `AirlineId` | String(20) | Master data, reference, provenance | Project governance, once per airline | No | Never | Durable identity, provenance join, cross-version lineage | Fact joins, Power BI relationships |
| `AirlineKey` | Int32 | Warehouse / DimAirline | Controlled key map, once per airline | No | Never | DimAirline primary key; fact foreign keys; Power BI relationships | Source identity, provenance, business-key matching |
| `AirlineIATACode` | String(2) | Airline attribute | Verified source, per reference version | Yes, by new version | A code may be reassigned only with explicit retirement and a new version | Display, validation, version-qualified uniqueness | Primary key, foreign key, provenance join |
| `AirlineICAOCode` | String(3) | Airline attribute | Verified source, per reference version | Yes, by new version | Same rule as IATA | Display, validation, version-qualified uniqueness | Primary key, foreign key, provenance join |
| `AirlineName` | String(100) | Airline attribute | Verified source, per reference version | Yes, by new version | A brand may change only with explicit retirement and a new version | Display, version-qualified uniqueness | Primary key, legal-entity proof, provenance join |
| `LegalName` | String(200) | Reference/provenance only | Verified source, per reference version | Yes, by new version | No | Optional legal-entity context | DimAirline column, report slicer, key |

### 5.3 Evidence Index

| Evidence ID | Evidence | Classification | Location / Status |
|---|---|---|---|
| B-01 | Contract v1.5 identity and reference rules | RECORDED DESIGN — PENDING REVIEW | docs/03_DATA_CONTRACTS.md Sections 3.4, 4.3, 6.2.2, 7, 8.4, 13 |
| B-02 | Remediation specification identity, historical, provenance, and gate design | RECORDED | docs/OD01_REMEDIATION_DESIGN_SPECIFICATION.md Sections 4 to 8 and 13.2 |
| B-03 | Independent audit findings H-01 to H-07 | RECORDED | docs/OD01_INDEPENDENT_GOVERNANCE_AUDIT_REPORT.md |
| B-04 | Proposed key map | RECORDED DESIGN — PENDING FORMAL APPROVAL | This record, Section 5.2 |
| B-05 | Reference manifest | NOT CREATED | data/manifests/reference_versions.csv design only |
| B-06 | T-78 plan and results | NOT EXECUTED | Contract Section 13; qa/results/airline_identity_versions.csv planned |
| B-07 | G3-RV-01 reference-version approval | NOT EXECUTED | Gate artifact planned; not an OD-series decision |
| B-08 | Independent reviewer | NOT ASSIGNED | Approval block, Section 11 |

### 5.4 Formal Approval Block

| Field | Entry |
|---|---|
| Decision | [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION |
| Approval scope | OD-01B Sections 2, 4, 5, 6, and 8 only |
| Exclusions | Schema freeze; reference CSVs; synthetic data; production ETL; Power Query; semantic model; DAX; Power BI; G3; G4; G3-RV-01; Git |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Approval conditions | [BLANK — to be completed at signature] |
| Reviewer route | Compensating-control route accepted under D-01/D-02; independent reviewer not assigned |
| Compensating-control acceptance | D-01/D-02 accepted; execution not complete |
| Reviewer limitation statement | No independent reviewer; AI review is not independent assurance |
| Reviewer name / role / organization | [BLANK — no reviewer assigned] |
| Reviewer independence | [ ] Independent   [ ] Not independent   [X] N/A — no reviewer |
| Reviewer result | [ ] CONCUR   [ ] CONCUR WITH RESERVATIONS   [ ] DISSENT   [X] N/A — no reviewer |
| Reviewer signature / date | [BLANK — no reviewer signature] |
| Residual concerns | H-04, H-05, M-07, M-12 open pending re-audit; B-03–B-08 open; no independent assurance |
| Re-audit record | [BLANK — PENDING] |
| Scope v1.1 SHA-256 | 9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C |
| Contract v1.5 SHA-256 | D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9 |
| Signed-copy path | [BLANK — D-08 PENDING; no docs/approvals/ structure] |
| Signed-copy SHA-256 | [BLANK — no signed copy exists] |
| Retention confirmed | [ ] Yes   [X] No — D-08 PENDING |
| Verification date / result | [BLANK — PENDING] |

**Formal signature:** ______________________________  
**Approval date:** ______________________________  

**Approval status:** PENDING. Not approved for reference-data creation, synthetic-data generation, schema freeze, Power BI implementation, or G3/G4 advance.

---

## 6. OD-04 Decision — Exchange-Rate Policy

### 6.1 Decision Statement

**Owner-directed design (not formally approved):**

OD-04 defines the exchange-rate regime used to convert original-currency financial amounts to USD in FactBookingTransactions and FactOperatingCosts. Without an approved OD-04 and a corresponding `ref_exchange_rates.csv`, no financial fact table can be generated because every non-USD financial row requires an exact-date exchange rate, currency conversion must not be performed in Power BI or DAX, missing rates block rows, and USD conversion is validated at transaction-row level.

### 6.2 Seven Sub-Decisions

| Sub-Decision | Question | Status | Options | Owner Selection |
|---|---|---|---|---|
| OD-04a | Currency scope | PROPOSED — PENDING | Option 1: 8 currencies (expand to match DimCurrency); Option 2: 5 currencies (USD, EUR, GBP, JPY, CAD); Option 3: Owner-specified custom set | [BLANK] |
| OD-04b | Exchange-rate convention | PROPOSED — PENDING | USD per one unit, 6 decimals, exact-date lookup, no forward-fill, round at final amount level | [BLANK] |
| OD-04c | Rate source | UNSPECIFIED | Option 3a: AEROVISION-360-SYNTHETIC-FX-V1; Option 3b: SIMULATED-FX-V1; Option 3c: Owner-specified | [BLANK] |
| OD-04d | Rate version | UNSPECIFIED | Option 4a: FX-2026-11-04-001; Option 4b: FX-V1; Option 4c: Owner-specified | [BLANK] |
| OD-04e | Missing-date behaviour | PROPOSED — PENDING | Option 5a: No forward-fill; exact-date only; missing rate quarantines row; Option 5b: Forward-fill with max gap N days + IsCarriedForward flag; Option 5c: Period-average rate (not allowed by contract) | [BLANK] |
| OD-04f | Rate-generation methodology | UNSPECIFIED | Option 6a: Owner-provided static rate table; Option 6b: Deterministic algorithmic generation (seed-based); Option 6c: Hybrid | [BLANK] |
| OD-04g | Downstream implications | PROPOSED — PENDING | FactBookingTransactions blocked until OD-04 approved + ref_exchange_rates.csv exists + rate coverage includes all booking dates; FactOperatingCosts blocked until OD-04 approved + ref_exchange_rates.csv exists + rate coverage includes all cost dates | [BLANK] |

### 6.3 Currency Mismatch (Critical Blocker)

| Dimension | OD-04 Currency Set | DimCurrency Currency Set | Impact |
|---|---|---|---|
| Currencies | USD, EUR, GBP, JPY, CAD (5) | AED, QAR, SGD, INR, GBP, EUR, USD, AUD (8) | 5 currencies in DimCurrency have no exchange rate if OD-04's set is enforced; JPY and CAD in OD-04 set are not in DimCurrency |

**Resolution required:** Either align OD-04's currency set with DimCurrency's 8 currencies (recommended), or align DimCurrency with OD-04's 5 currencies. This is a blocking discrepancy.

### 6.4 Evidence Index

| Evidence ID | Evidence | Classification | Location / Status |
|---|---|---|---|
| F-01 | OD-04 owner decision package | RECORDED | docs/OD04_OWNER_DECISION_PACKAGE.md |
| F-02 | OD-04 exchange-rate policy assessment | RECORDED | docs/OD04_EXCHANGE_RATE_POLICY_ASSESSMENT.md |
| F-03 | DimCurrency data | RECORDED | data/03_curated/dim_currency.csv; 8 currencies; USD as IsReportingCurrency |
| F-04 | ref_exchange_rates.csv | NOT CREATED | data/04_reference/ref_exchange_rates.csv does not exist |
| F-05 | FactBookingTransactions | NOT CREATED | Blocked by OD-04 |
| F-06 | FactOperatingCosts | NOT CREATED | Blocked by OD-04 |

### 6.5 Formal Approval Block

| Field | Entry |
|---|---|
| Decision | [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION |
| Approval scope | OD-04 policy and all seven sub-decisions (OD-04a through OD-04g) |
| Exclusions | Creation of ref_exchange_rates.csv; implementation of FactBookingTransactions or FactOperatingCosts; financial KPI measures |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Approval conditions | [BLANK — to be completed at signature] |
| Reviewer route | Compensating-control route accepted under D-01/D-02; independent reviewer not assigned |
| Compensating-control acceptance | D-01/D-02 accepted; execution not complete |
| Reviewer limitation statement | No independent reviewer; AI review is not independent assurance |
| Residual concerns | Currency mismatch unresolved; individual rate values not approved; rate coverage period not approved |
| Signed-copy path | [BLANK — no docs/approvals/ structure] |
| Signed-copy SHA-256 | [BLANK — no signed copy exists] |
| Retention confirmed | [ ] Yes   [X] No — D-08 PENDING |
| Verification date / result | [BLANK — PENDING] |

**Formal signature:** ______________________________  
**Approval date:** ______________________________  

**Approval status:** PENDING. Blocks all financial fact generation and Page 03.

---

## 7. G3-RV-01 Decision — Reference Version Approval

### 7.1 Decision Statement

**Not ready for signature.** Depends on OD-01A/OD-01B formal approval and critical OD decisions (including OD-04 currency scope).

**ReferenceVersion format:** `AIR-YYYY-MM-DD-NNN`, regex `^AIR-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$`. Published versions are immutable. A correction requires a new version, a reconciliation note, and a new source record where evidence changed.

### 7.2 Authoritative Manifest Fields

| Field | Requirement |
|---|---|
| ReferenceVersion | AIR-YYYY-MM-DD-NNN; format AIR-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{3}$ |
| EffectiveFrom | First date the version applies |
| EffectiveTo | Last date, or blank while current |
| IsCurrent | Exactly one TRUE for a generation or refresh |
| Status | DRAFT, READY FOR REVIEW, APPROVED, RETIRED, or REJECTED |
| ApprovedBy | Owner identity only after actual approval; blank before signature |
| ApprovalDate | Actual approval date only after signature; blank before approval |
| ManifestHash | SHA-256 of reference and provenance files for the version |
| SupersedesReferenceVersion | Prior version replaced, if any |
| ReconciliationNote | Required for correction or identity change |

**ApprovedBy and ApprovalDate remain blank until a real approval occurs.**

### 7.3 T-78 Sub-Checks

| T-78 ID | Check |
|---|---|
| T-78-01 | One distinct ReferenceVersion in ref_airlines.csv |
| T-78-02 | One distinct ReferenceVersion in ref_airline_sources.csv |
| T-78-03 | Manifest version matches |
| T-78-04 | DimAirline.ReferenceVersion matches |
| T-78-05 | Power BI SelectedReferenceVersion matches |
| T-78-06 | Manifest status = APPROVED |
| T-78-07 | Ten active AirlineId values and ten unique AirlineKey values |
| T-78-08 | One authoritative VERIFIED record per populated attribute |
| T-78-09 | No key reassignment |
| T-78-10 | Reconciliation note for every identity change and no mixed-version facts |

### 7.4 Formal Approval Block

| Field | Entry |
|---|---|
| Decision | [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION |
| Approval scope | One ReferenceVersion per generation/refresh; manifest authority; key map integrity |
| Exclusions | Creation of ref_airlines.csv; ref_airline_sources.csv; any synthetic data |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Dependencies | OD-01A APPROVED; OD-01B APPROVED; OD-04 APPROVED (for currency rates) |
| ReferenceVersion value | [BLANK — to be assigned at approval] |
| Signed-copy path | [BLANK — no docs/approvals/ structure] |
| Retention confirmed | [ ] Yes   [X] No — D-08 PENDING |

**Formal signature:** ______________________________  
**Approval date:** ______________________________  

**Approval status:** PENDING. Blocks reference-data creation and all generation.

---

## 8. Schema Freeze Authorization

### 8.1 Decision Statement

**Not ready for signature.** Depends on OD-01A/OD-01B formal approval and critical OD decisions.

Schema freeze records that the contract v1.5, schema definitions, key relationships, and measure definitions are frozen and will not change without controlled change control.

### 8.2 Formal Approval Block

| Field | Entry |
|---|---|
| Decision | [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION |
| Approval scope | Contract v1.5 schema definitions; key relationships; measure definitions; date roles; relationship cardinality and filter direction |
| Exclusions | Reference-data creation; synthetic-data generation; production ETL; Power Query; Power BI reports/dashboards |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Schema hash | [BLANK — to be computed at freeze] |
| Contract version | v1.5 |
| Signed-copy path | [BLANK — no docs/approvals/ structure] |
| Retention confirmed | [ ] Yes   [X] No — D-08 PENDING |

**Formal signature:** ______________________________  
**Approval date:** ______________________________  

**Approval status:** PENDING. Blocks Power Query/model build without rework risk.

---

## 9. G3 Formal Approval

### 9.1 Decision Statement

**Not ready for signature.** Depends on OD-01A/OD-01B signatures, OD-04 approval, G3-RV-01 execution, schema freeze, and validation implementation.

### 9.2 G3 Gate Entry Criteria

| Criterion | Status |
|---|---|
| OD-01A formal signature | PENDING |
| OD-01B formal signature | PENDING |
| Critical OD decisions (OD-04a through OD-04f) | PENDING |
| G3-RV-01 approved reference version | NOT EXECUTED |
| Schema freeze written record | NOT AUTHORIZED |
| Validation implementation | NOT STARTED |
| Independent reviewer assigned | NOT AVAILABLE |

### 9.3 Formal Approval Block

| Field | Entry |
|---|---|
| Decision | [ ] APPROVED   [ ] REJECTED   [ ] RETURNED FOR REVISION |
| Approval scope | G3 gate execution; design documentation accepted; contract v1.5 approved; schema frozen |
| Exclusions | Data generation; Power BI model build; report page creation |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual approval date | [BLANK — no approval date recorded] |
| Gate review evidence | [BLANK — no gate review held] |
| Signed-copy path | [BLANK — no docs/approvals/ structure] |
| Retention confirmed | [ ] Yes   [X] No — D-08 PENDING |

**Formal signature:** ______________________________  
**Approval date:** ______________________________  

**Approval status:** PENDING. Blocks G4 authorization.

---

## 10. Independent Reviewer Assignment

### 10.1 Decision Statement

**Not ready.** No independent reviewer has been assigned. AI-assisted review is not independent assurance. Owner self-review is a separate activity and has not been executed or recorded as evidence.

### 10.2 Options

| Option | Description | Status |
|---|---|---|
| Option 1 | Name a separate person (peer, mentor, or external) as independent reviewer | Not available |
| Option 2 | Document compensating control: owner self-review + automated hash/schema checks + second-pass review where available | Accepted under D-01/D-02; execution not complete |
| Option 3 | Document no-reviewer limitation and proceed with transparent self-review | Accepted under D-01/D-02; execution not complete |

### 10.3 Formal Approval Block

| Field | Entry |
|---|---|
| Decision | [ ] Independent reviewer assigned   [ ] Compensating control accepted   [ ] N/A — no reviewer |
| Reviewer name | [BLANK — no reviewer assigned] |
| Reviewer role / organization | [BLANK — not assigned] |
| Review date | [BLANK — not completed] |
| Review scope | The eight owner-confirmed choices and the technical clarifications in Sections 5 and 6 |
| Independence status | [ ] Independent   [ ] Not independent   [X] N/A — no reviewer |
| Reviewer result | [ ] CONCUR   [ ] CONCUR WITH RESERVATIONS   [ ] DISSENT   [X] N/A — no reviewer |
| Reviewer signature / date | [BLANK — no reviewer signature] |
| Compensating-control acceptance | D-01/D-02 accepted; execution not complete |
| Residual limitation | No independent third-party assurance is claimed |

**Approval status:** PENDING. Blocks all QA PASS decisions (tests remain EXECUTED, not PASSED).

---

## 11. G4 Data Generation Authorization

### 10.1 Decision Statement

**Not ready for signature.** Depends on G3 APPROVED and written G4 authorization.

### 10.2 Formal Approval Block

| Field | Entry |
|---|---|
| Decision | [ ] AUTHORIZED   [ ] NOT AUTHORIZED   [ ] RETURNED FOR REVISION |
| Approval scope | Reference-data creation; synthetic-data generation; production ETL; Power Query; semantic model; DAX measures; Power BI reports/dashboards |
| Exclusions | Schema freeze; reference-version approval; G3 gate execution |
| Owner name | KH Mohammad Farhan |
| Owner decision | [BLANK — to be completed by the owner] |
| Owner signature | [BLANK — no signature recorded] |
| Actual authorization date | [BLANK — no authorization date recorded] |
| Authorized datasets | [BLANK — to be specified at authorization] |
| Authorized reference version | [BLANK — to be specified at authorization] |
| Signed-copy path | [BLANK — no docs/approvals/ structure] |
| Retention confirmed | [ ] Yes   [X] No — D-08 PENDING |

**Formal signature:** ______________________________  
**Authorization date:** ______________________________  

**Approval status:** PENDING. Blocks all data generation.

---

## 12. Dependencies and Decision Sequence

```
OD-01A signature ──────────────────┐
OD-01B signature ──────────────────┼──→ G3-RV-01 ───────────────┐
OD-04 approval (7 sub-decisions) ──┼──→ Schema freeze ───────────┤
Currency mismatch resolution ──────┤                              │
G3-RV-01 execution ────────────────┤                              ▼
Schema freeze written record ──────┴──────────────────────→ G3 formal approval ──→ G4 written authorization ──→ Data generation ──→ Semantic model build ──→ DAX measures ──→ Report pages ──→ QA tests ──→ Release
Independent reviewer assignment ──────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Critical path:** OD-01A/OD-01B signatures → OD-04 approval → currency mismatch resolution → G3-RV-01 → schema freeze → G3 formal approval → G4 written authorization → data generation.

**Parallel path:** Page 02, 04, 05, 06 design and visual specifications can proceed once the semantic model has the 3 existing facts and 10 measures (these are already specified and measures verified against source data).

---

## 13. Risks and Consequences of Non-Approval

| Blocker | Consequence of Non-Resolution |
|---|---|
| OD-01A/OD-01B unsigned | No airline population authorization; no reference data; no data generation; project cannot proceed |
| OD-04 not approved | Page 03 cannot be built; no financial KPIs; no revenue/cost analysis |
| Currency mismatch | Referential integrity failures; currencies without rates quarantined; financial data incomplete |
| G3-RV-01 not executed | No approved reference version; mixed-version risk; no reproducible generation |
| Schema freeze not authorized | Schema drift; conflicting definitions; rework required |
| G3 not formally approved | G4 cannot be authorized; project stalled at design phase |
| G4 not authorized | No data generation; no synthetic datasets; no Power BI data |
| Independent reviewer not assigned | No QA PASS decisions; no gate advancement; no release |

---

## 14. Required Approval Evidence

For each decision to reach `FORMALLY APPROVED`:

1. Owner signature (wet or digital) on the decision record
2. Actual approval date (not backdated)
3. Named reviewer (if available) or documented compensating-control acceptance
4. Reviewer result (CONCUR / CONCUR WITH RESERVATIONS / DISSENT / N/A)
5. Scope v1.1 SHA-256 hash: `9A9EEA4154B6E6399A88F2A9EE503B8BE233BC69036C76871D7BC1D29DCF512C`
6. Contract v1.5 SHA-256 hash: `D1CE40117E24058643245DA0B7C34E10D7E76E662AB9B9831EDD3D47E5AF21D9`
7. Signed-copy path in `docs/approvals/` (to be created at D-08 approval)
8. Signed-copy SHA-256 hash
9. Retention confirmation (read-only retention log)
10. Verification date and result

---

## 15. Formal Approval and Signature Requirements

| Requirement | Specification |
|---|---|
| Signatory | KH Mohammad Farhan, Project Owner |
| Signature format | Wet or digital signature on the decision record |
| Approval date | Actual calendar date of signature; not backdated |
| Reviewer | Separate person preferred; compensating controls documented if none available |
| Evidence retention | Read-only signed copy in `docs/approvals/`; SHA-256 hash recorded |
| Scope statement | Explicit inclusion and exclusion scope on each decision record |
| Conditions | Explicit conditions recorded; no implied conditions |
| Residual concerns | Recorded openly; not suppressed |
| Re-audit record | Fresh re-audit confirming no signature blocker remains |
| No fabrication | No signature, date, or reviewer identity invented |

---

## 16. Documents in This Pack

| Document | Purpose | Status |
|---|---|---|
| GOVERNANCE_DECISION_PACK.md | Executive summary and full decision-by-decision treatment | This document |
| GOVERNANCE_DECISION_REGISTER.md | Decision register with status classifications | Created |
| GOVERNANCE_APPROVAL_MATRIX.md | Approval matrix with evidence requirements | Created |
| GOVERNANCE_SIGNATURE_CHECKLIST.md | Signature checklist for formal execution | Created |
| GOVERNANCE_DEPENDENCY_MAP.md | Dependency and sequencing map | Created |

---

## 17. Single Most Important Next Action

**The project owner must sign OD-01A and OD-01B.** These are the foundational decisions that unblock G3-RV-01, schema freeze, G3 formal approval, G4 authorization, and all downstream data generation and report building. Without these signatures, the project cannot proceed past the design-and-preparation phase.

---

**End of Governance Decision Pack.** This document is governance preparation evidence only. No source files, data, DAX, PBIX, or report pages were modified during its creation.
