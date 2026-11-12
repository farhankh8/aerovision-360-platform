# AEROVISION 360 — OD-01A / OD-01B Owner Approval Record

**Record ID:** OD01A-OD01B-APPROVAL-2026-11-08  
**Record type:** Owner approval recording — NOT a signature, NOT formal gate approval  
**Approval date:** 2026-11-08  
**Project owner / approver:** KH Mohammad Farhan  
**Prepared:** 2026-11-08  
**Status:** OWNER CONFIRMED — FORMAL SIGNATURE AND RE-AUDIT PRECONDITIONS PENDING  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

> **STATUS NOTICE — NOT A FORMAL SIGNATURE OR GATE APPROVAL**
>
> This record documents the owner's explicit confirmation of OD-01A and OD-01B on
> 2026-11-08. It records the confirmed decisions and remaining formalities. It does
> NOT constitute a formal signature, does not complete the re-audit preconditions in
> Section 7.1/11.1 of the decision records, does not authorize reference-data
> creation, synthetic-data generation, schema freeze, Power BI implementation, G3,
> or G4. No signature line is executed by this record. No independent assurance is
> claimed.

---

## 1. Approval Summary

| Decision ID | Decision Title | Original Status | Current Status | Approval Date |
|-------------|---------------|-----------------|----------------|---------------|
| OD-01A | Airline Population | Owner-confirmed design, formal signature pending | **OWNER CONFIRMED — 2026-11-08** | 2026-11-08 |
| OD-01B | Airline Identity Reference | Owner-confirmed design, formal signature pending | **OWNER CONFIRMED — 2026-11-08** | 2026-11-08 |

---

## 2. OD-01A — Airline Population: Exact Approved Decision

**Source document:** `docs/OD01A_AIRLINE_POPULATION_DECISION.md`, revision 0.2  
**Authority:** Owner confirmation recorded in `docs/OD01_OWNER_DECISION_CONFIRMATION.md` (SHA-256 `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`)

### Approved content — OD-01A Sections 2, 3, and 4 only

Per Section 7.3 of OD-01A, this approval covers:

1. **Fixed baseline population:** Exactly ten real airline identities (Section 3):
   | # | Airline | IATA | ICAO | Home Country | Country Code | Proposed AirlineId |
   |---|---------|------|------|--------------|--------------|-------------------|
   | 1 | Emirates | EK | UAE | United Arab Emirates | AE | AIR-0001 |
   | 2 | Qatar Airways | QR | QTR | Qatar | QA | AIR-0002 |
   | 3 | Singapore Airlines | SQ | SIA | Singapore | SG | AIR-0003 |
   | 4 | Air India | AI | AIC | India | IN | AIR-0004 |
   | 5 | IndiGo | 6E | IGO | India | IN | AIR-0005 |
   | 6 | British Airways | BA | BAW | United Kingdom | GB | AIR-0006 |
   | 7 | Lufthansa | LH | DLH | Germany | DE | AIR-0007 |
   | 8 | Delta Air Lines | DL | DAL | United States | US | AIR-0008 |
   | 9 | Southwest Airlines | WN | SWA | United States | US | AIR-0009 |
   | 10 | Qantas | QF | QFA | Australia | AU | AIR-0010 |

2. **Population-boundary rules** (Sections 2–4):
   - The identities are real; every populated identity attribute must be source-verified and recorded at attribute level before a reference version is approved.
   - Operational, customer, booking, revenue, cost, disruption, feedback, and financial records for the ten airlines are synthetic simulations.
   - The reporting period is 2025-10-01 through 2026-09-30, inclusive.
   - Every report page, tooltip while a page is visible, and exported result must carry the exact unconditional disclosure `Synthetic Simulation — Not Actual Airline Performance`.
   - No additional airline may be added, and no listed airline may be removed or substituted, without controlled change and formal approval.
   - The population is fixed for the baseline. A merger, rebrand, successor entity, or code change is handled under the identity and change-control rules in OD-01B and contract Section 3.4.
   - This record does not authorize reference-data creation, synthetic-data generation, schema freeze, Power BI implementation, or a G3/G4 advance.

### Approval scope exclusions (per OD-01A Section 7.3)

OD-01B; reference CSVs (`ref_airlines.csv`, `ref_airline_sources.csv`); schema freeze; synthetic data generation; production ETL; Power Query; Power BI; G3; G4.

---

## 3. OD-01B — Airline Identity Reference: Exact Approved Decision

**Source document:** `docs/OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md`, revision 0.2  
**Authority:** Owner confirmation recorded in `docs/OD01_OWNER_DECISION_CONFIRMATION.md` (SHA-256 `AC6A95B461A3447F56B972D8518DDDE15C82CFE3924FD718600776D220119FBD`)

### Approved content — OD-01B Sections 2, 4, 5, 6, and 8 only

Per Section 11.3 of OD-01B, this approval covers:

1. **Identity and key model** (Section 2):
   - `AirlineId` is the durable business identity. `AirlineKey` is the permanent warehouse surrogate used by facts and Power BI relationships. They are not interchangeable.
   - IATA and ICAO codes are mutable attributes, unique within a reference version. They are not primary keys, foreign keys, or provenance joins.
   - `AirlineName` is the commercial brand. `LegalName` is optional and remains in the reference/provenance layer only; it is not a `DimAirline` column.
   - `HomeCountry` is the country of the airline's principal headquarters or domicile. `AirlineGroup` is the optional ultimate parent company or group brand and is not inferred.
   - `BusinessModelClass` is an optional analytical classification, not a source-verified identity attribute. `OperatingRegion` is removed from the airline identity model; analytical region is derived from route and airport geography.
   - The minimal lifecycle uses `IsActive` and `StatusEffectiveDate`. `LifecycleStatus` and `MergedIntoAirlineId` are deferred and are not columns.
   - `DimAirline` is Type 1.
   - The reference manifest is the authoritative approval record. `DimAirline.ReferenceVersion` is technical lineage only.
   - The airline key map is controlled and immutable after approval. The same `AirlineId` always resolves to the same `AirlineKey`, independent of row order, rebuild, or database identity sequence. Historical facts are never re-keyed.
   - Reference-version approval uses `G3-RV-01`, not an OD-series decision.

2. **Reporting boundary** (Section 2.1):
   - Population is exactly the ten real airline identities listed in OD-01A Section 3.
   - Fixed reporting period: 2025-10-01 through 2026-09-30.
   - Inclusion/exclusion criteria from OD-01A Section 4 apply.
   - Identity attributes are real and must be source-verified before reference approval; all operational data is synthetic.

3. **Attribute dictionary** (Section 4):
   - `AirlineKey`, `AirlineId`, `AirlineIATACode`, `AirlineICAOCode`, `AirlineName`, `HomeCountry`, `HomeCountryCode`, `BusinessModelClass`, `IsActive`, `StatusEffectiveDate`, `ReferenceVersion` as defined.
   - Excluded columns: `OperatingRegion`, `LegalName`, `LifecycleStatus`, `MergedIntoAirlineId`.

4. **Reference datasets and provenance** (Section 5):
   - `ref_airlines.csv` and `ref_airline_sources.csv` design as defined.
   - One row per `AirlineId` per `ReferenceVersion`; primary key `AirlineId` + `ReferenceVersion`.
   - Every populated identity attribute requires exactly one authoritative `VERIFIED` record per version.

5. **Lifecycle and historical semantics** (Section 6): Type 1 baseline, `IsActive`/`StatusEffectiveDate` minimal lifecycle.

6. **Power BI relationship and disclosure rules** (Section 8).

### Acknowledged design baselines — NOT schema freeze (per OD-01B Section 11.3)

- **Section 3 (Key hierarchy and proposed allocation):** Proposed administrative allocation only; not source-verified identity fact; becomes immutable only after G3-RV-01 reference-version approval.
- **Section 7 (Reference version, manifest, key map, and gate evidence):** Design baseline; `G3-RV-01` gate artifact not executed.

### Approval scope exclusions (per OD-01B Section 11.3)

Schema freeze; reference-data creation or population; synthetic-data generation; production ETL; Power Query; semantic model; DAX; Power BI reports/dashboards; G3 or G4 advancement; `G3-RV-01` execution; Git operations.

---

## 4. Owner Approval Details

| Field | Entry |
|-------|-------|
| Decision owner / approver | KH Mohammad Farhan |
| Role | Project owner |
| Approval date | 2026-11-08 |
| Approval source | Owner explicit confirmation (chat, 2026-11-08) |
| Decisions confirmed | OD-01A (Sections 2, 3, 4 only); OD-01B (Sections 2, 4, 5, 6, 8 only) |
| Formal signature | **NOT RECORDED** — no signature line executed |
| Formal approval date fields in source records | **STILL BLANK** in `OD01A_AIRLINE_POPULATION_DECISION.md` Section 7.4 and `OD01B_AIRLINE_IDENTITY_REFERENCE_DECISION.md` Section 11.4 — not backfilled by this record |
| Owner signature block in source records | **STILL BLANK** — not forged or simulated |
| Reviewer route | Compensating-control route accepted under D-01/D-02; independent reviewer not assigned |
| Independent assurance | NOT CLAIMED |

---

## 5. Outstanding Formalities

The following items remain unresolved before formal signature can be recorded. These are **not** completed by this record:

| Formality | Status | Location |
|-----------|--------|----------|
| Re-audit precondition 1: Revision 0.2 verified, before/after hashes recorded | PENDING | OD-01A §7.1(1); OD-01B §11.1(1) |
| Re-audit precondition 2: E-07 cites current scope v1.1 hash | PENDING | OD-01A §7.1(2); OD-01B §11.1(2) |
| Re-audit precondition 3: H-04 re-audited | PENDING | OD-01A §7.1(3); OD-01B §11.1(3) |
| Re-audit precondition 4: H-05 re-audited | PENDING | OD-01A §7.1(4); OD-01B §11.1(4) |
| Re-audit precondition 5: M-07 and M-12 re-audited | PENDING | OD-01A §7.1(5); OD-01B §11.1(5) |
| Re-audit precondition 6: Owner self-review executed and recorded | NOT EXECUTED | OD-01A §7.1(6); OD-01B §11.1(6) |
| Re-audit precondition 7: Compensating-control challenge documented | PARTIAL — NOT CLOSED | OD-01A §7.1(7); OD-01B §11.1(7) |
| Re-audit precondition 8: GOV-B-05 resolved by GOV-D-04; GOV-B-08 resolved by GOV-D-08 | PENDING | OD-01A §7.1(8); OD-01B §11.1(8) |
| Re-audit precondition 9: Fresh re-audit records final finding status | PENDING | OD-01A §7.1(9); OD-01B §11.1(9) |
| Formal signature line | BLANK — not executed | OD-01A §7.4; OD-01B §11.4 |
| Formal approval date | BLANK — not entered | OD-01A §7.4; OD-01B §11.4 |
| Independent reviewer assignment | NOT ASSIGNED | OD-01A §7.2; OD-01B §11.2 |
| Residual concerns: H-04, H-05, M-07, M-12, B-03, B-04, GOV-B-05, GOV-B-08 | OPEN | OD-01A §7.2; OD-01B §11.2 |

**Current re-audit status:** PENDING (both OD-01A and OD-01B). No precondition is represented as complete merely because this approval record was written.

---

## 6. Updated Blocker Statuses

| Blocker ID | Blocker | Previous Status | Updated Status | Still Blocks |
|------------|---------|-----------------|----------------|--------------|
| OD-01A | Airline Population | Owner-confirmed design, formal signature pending | **OWNER CONFIRMED — formal signature and re-audit preconditions pending** | G3-RV-01 (until formal signature completed) |
| OD-01B | Airline Identity Reference | Owner-confirmed design, formal signature pending | **OWNER CONFIRMED — formal signature and re-audit preconditions pending** | G3-RV-01 (until formal signature completed) |
| G3-RV-01 | Reference Version Approval | NOT EXECUTED | NOT EXECUTED (unchanged) | G4 Data Generation |
| OD-04 | Exchange-Rate Policy | UNRESOLVED | UNRESOLVED (unchanged) | FactBookingTransactions, FactOperatingCosts |
| G4 | Data Generation | BLOCKED | BLOCKED (unchanged) | All fact table generation, model population, report implementation |

---

## 7. G3-RV-01 Prerequisite Assessment

**Question:** Are G3-RV-01 prerequisites satisfied after this owner confirmation?

**Answer: NO.** G3-RV-01 cannot be executed because:

1. OD-01A formal signature is not yet complete — re-audit preconditions are PENDING.
2. OD-01B formal signature is not yet complete — re-audit preconditions are PENDING.
3. Reference CSV files (`ref_airlines.csv`, `ref_airline_sources.csv`) do not exist.
4. Reference manifest (`data/manifests/reference_versions.csv`) does not exist.
5. T-75, T-76, T-78 validation tests are NOT EXECUTED.
6. No independent reviewer is assigned; independent assurance is NOT CLAIMED.
7. Compensating-control execution is PARTIAL — NOT CLOSED; owner self-review is NOT EXECUTED.

**G3-RV-01 status:** NOT EXECUTED — all prerequisites remain unmet.

---

## 8. What This Record Does Not Authorize

- It does not create or populate `ref_airlines.csv`, `ref_airline_sources.csv`, or any reference manifest.
- It does not create synthetic data, Python code, Power Query queries, a semantic model, DAX measures, Power BI reports, or dashboards.
- It does not freeze the schema or approve a data dictionary.
- It does not advance G3 or G4.
- It does not claim that source verification, independent review, or external assurance has occurred.
- It does not execute G3-RV-01.
- It does not authorize a Git operation.
- It does not fill the formal signature, approval date, or approval evidence fields in the source decision records.

---

## 9. Recommended Next Steps for the Owner

1. Complete the re-audit preconditions in OD-01A Section 7.1 and OD-01B Section 11.1.
2. Execute owner self-review and record it as owner self-review (not independent review).
3. Document the compensating-control challenge; do not describe AI-assisted review as independent assurance.
4. Resolve GOV-B-05 via GOV-D-04 and GOV-B-08 via GOV-D-08, or explicitly withhold signature.
5. Obtain a fresh re-audit recording final finding status.
6. Sign OD-01A and OD-01B with a real signature and real approval date in separate controlled artifacts.
7. After formal signatures, proceed to G3 review and reference-version approval via G3-RV-01.
8. G4 requires separate written authorization after G3 passes.

---

**End of record. OD-01A and OD-01B owner confirmation recorded 2026-11-08. Formal signature, re-audit preconditions, G3-RV-01, OD-04, and G4 remain unresolved. No implementation or data generation authorized.**
