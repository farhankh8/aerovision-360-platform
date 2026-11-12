# AEROVISION 360 — ISSUE AND RISK REGISTER

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY AUDIT — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Issue Register

| ID | Severity | Component | Issue | Impact | Recommended Action |
|----|----------|-----------|-------|--------|-------------------|
| ISS-001 | CRITICAL | PBIX report | Report has only one blank page ("Page 1"); all 5 report pages exist only in report.json | No report visuals in Power BI Desktop; report unusable | Rebuild all 5 pages in Power BI Desktop from report.json |
| ISS-002 | CRITICAL | OD-04 | Exchange-rate policy unresolved; FactBookingTransactions and FactOperatingCosts blocked | Page 03 (18 visuals) cannot be implemented; 22 measures blocked | Resolve OD-04 or accept Page 03 limitation |
| ISS-003 | CRITICAL | G3 data design gate | Not approved; OD-01A/01B unsigned; schema freeze not authorized | No data generation; no reference version; no schema freeze | Obtain OD-01A/01B signatures; approve G3-RV-01 |
| ISS-004 | HIGH | dim_airline | 3 entirely null columns (AirlineGroup, BusinessModelClass, StatusEffectiveDate) | Airline enrichment data missing | Do not fabricate values; document limitation |
| ISS-005 | HIGH | dim_fare_class, dim_booking_channel, dim_currency | Unused dimensions; no FK to any fact table | 3 dimensions cannot be used in reports | Add FKs or hide/remove from report scope |
| ISS-006 | HIGH | Power Query M | Only 2 of 14 tables defined; dim_airline column count wrong (14 vs 12) | 12 tables cannot be loaded via Power Query | Rewrite Power Query M for all 14 tables |
| ISS-007 | MEDIUM | model.json | Wrong FL01, FL02, CF03 expressions | Model metadata incorrect; may cause confusion | Correct model.json to match DAX file |
| SM-08 | MEDIUM | semantic_model.json | No measure expressions; incomplete relationship list | Cannot validate logic from JSON alone | Add measure expressions; complete relationships |
| DAX-01 | MEDIUM | DS03 | Counts dimension rows (3) instead of fact events (540) | Incorrect disruption count | Fix to count fact_disruptions where RELATED(dim_disruption_type[ControllableFlag]) = TRUE() |
| DAX-02 | MEDIUM | FL04 | Uses SUM over boolean column (CancellationFlag) | May fail depending on storage type | Replace with COUNTROWS(FILTER(...CancellationFlag = TRUE())) |
| DAX-03 | MEDIUM | FL04, CF03 | Percentage scaling ambiguity (multiply by 100) | May display as 448% / 2552% if formatted as Percent | Document convention: return fraction with Percent format, or keep number with number format |
| DAX-04 | MEDIUM | OP01, OP03, OP04 | Not in DAX file; defined only in specification | Measures not available in model | Add OP01, OP03, OP04 to DAX file |
| CF-01 | MEDIUM | CF11 | Numerator counts ALL ServiceRecoveryFlag=True (381), denominator counts complaints (638) | Measure comment says "(of complaints)" but DAX doesn't filter by FeedbackType | Review with owner; decide whether to fix numerator or update comment |
| CF-02 | MEDIUM | CF14 | All 603 Compliment events have NULL SatisfactionScore; CF14 returns BLANK | Correct behavior but may confuse users | Document clearly; display as em dash (—) not zero |
| DS-01 | LOW | dim_date inactive date relationships | FeedbackDateKey, ResolutionDateKey, BookingDateKey all inactive | Date slicer won't filter feedback without USERELATIONSHIP | Add USERELATIONSHIP in measures; document limitation |

---

## 2. Risk Register

| Risk ID | Risk Title | Inherent Rating | Current Status | Mitigation |
|---------|------------|-----------------|----------------|------------|
| R-09 | Airline suspension, cessation, merger, or lifecycle change | HIGH | OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED | IsActive flag, StatusEffectiveDate, controlled ReferenceVersion, T-78 lifecycle checks |
| R-10 | Reference-version change after data refresh or generation | HIGH | OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED | One approved ReferenceVersion per generation; manifest; T-78-01 to T-78-10; fail closed on mismatch |
| R-11 | Historical reproducibility and reference-snapshot consistency | HIGH | OPEN — MITIGATION NOT IMPLEMENTED / NOT VERIFIED | Permanent AirlineKey; immutable reference snapshots; no re-keying; T-78-09/10 |

---

## 10. Issue Severity Distribution

| Severity | Count | Issues |
|----------|-------|--------|
| CRITICAL | 3 | M-001, M-002, M-003 |
| HIGH | 5 | M-004, M-005, M-006, DAX-01, CF-01 |
| MEDIUM | 6 | DAX-02, DAX-03, DAX-04, CF-02, SM-07, SM-08 |
| LOW | 1 | M-010 |

---

## 11. Issue Distribution by Component

| Component | Count | Issues |
|-----------|-------|--------|
| Power BI report | 1 | M-001 |
| OD-04 governance | 1 | M-002 |
| G3 governance | 1 | M-003 |
| dim_airline | 1 | M-004 |
| dim_fare_class, dim_booking_channel, dim_currency | 1 | M-005 |
| Power Query M | 1 | M-006 |
| model.json | 1 | M-007 |
| semantic_model.json | 1 | SM-08 |
| DS03 measure | 1 | DAX-01 |
| FL04 measure | 1 | DAX-02 |
| FL04, CF03 measures | 1 | DAX-03 |
| OP01, OP03, OP04 measures | 1 | DAX-04 |
| CF11 measure | 1 | CF-01 |
| CF14 measure | 1 | CF-02 |
| dim_date relationships | 1 | SM-06 |

---

## 10. Conclusion

The issue register identifies **13 issues** across the project:

- **3 CRITICAL:** PBIX blank page, OD-04 blocked, G3 not approved
- **5 HIGH:** dim_airline null columns, unused dimensions, Power Query incomplete, model.json wrong expressions, CF11 semantic issue
- **6 MEDIUM:** DAX formatting, DS03 count error, OP measures missing, CF14 BLANK, semantic_model.json incomplete, dim_date inactive relationships
- **1 LOW:** dim_date inactive relationships

All issues are documented with recommended actions. The project cannot proceed to implementation until G3 is approved and OD-04 is resolved.
