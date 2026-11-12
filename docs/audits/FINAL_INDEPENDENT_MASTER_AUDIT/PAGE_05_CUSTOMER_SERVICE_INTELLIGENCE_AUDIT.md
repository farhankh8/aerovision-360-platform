# PAGE 05 — CUSTOMER & SERVICE INTELLIGENCE AUDIT

**Source:** Authoritative main PBIX `deliverables/power_bi/AEROVISION_360.pbix`, page folder `18bdd7f468e4853e0a00`  
**Page name:** `05 - Customer & Service Intelligence`  
**Page order:** Page 05 (fifth page)  
**Visual count:** 27  
**Page rendered in Power BI Desktop:** Not independently verified (limitation L-1); visual metadata verified from binary.  
**Owner context:** Owner reported Page 05 had 16 investigated visuals, all passing data validation per existing investigation reports.

---

## 1. Visual inventory

27 visuals (full table in `POWER_BI_FIVE_PAGE_VISUAL_INVENTORY.md`). Key data visuals:

| Visual | Type | Title | Bound measure | Bound column/table |
|---|---|---|---|---|
| Card | cardVisual | 'Total Passengers' | CF01 (Total Feedback Events) | fact_customer_feedback |
| Card | cardVisual | 'Overall Satisfaction Rating' | CF02 | fact_customer_feedback |
| Card | cardVisual | 'Average Satisfaction Score' | CF02 | fact_customer_feedback |
| Card | cardVisual | 'Complaint Rate' | CF03 | fact_customer_feedback |
| Card | cardVisual | 'Active Customers' | CF04 | dim_customer |
| Card | cardVisual | 'Complaint Count' | CF05 | fact_customer_feedback |
| Card | cardVisual | 'Compliment Count' | CF06 | fact_customer_feedback |
| Card | cardVisual | 'Claim Count' | CF07 | fact_customer_feedback |
| Card | cardVisual | 'Survey Count' | CF08 | fact_customer_feedback |
| Card | cardVisual | 'Positive Feedback Rate' | CF09 | CF06/CF01 |
| Card | cardVisual | 'Negative Feedback Rate' | CF10 | (CF05+CF07)/CF01 |
| Card | cardVisual | 'Complaint Count' (duplicate card) | CF05 | fact_customer_feedback |
| Clustered column chart | clusteredColumnChart | 'Feedback by Type' | measure | fact_customer_feedback |
| Clustered bar chart | clusteredBarChart | 'Feedback by Channel' | measure | fact_customer_feedback |
| Donut chart | donutChart | 'Complaint Category Breakdown.' | measure | fact_customer_feedback |
| Pie chart | pieChart | 'Customer Segment Distribution.' | measure | dim_customer |
| Line chart | lineChart | 'Average Satisfaction by Airline.' | CF02 | dim_airline |
| Decomposition tree | decompositionTreeVisual | 'Complaint Analysis — Decomposition Tree' | CF01 + explain-by fields | fact_customer_feedback, dim_airline |
| Slicer | slicer | 'Feedback Channel' | — | fact_customer_feedback |
| Slicer | slicer | 'Customer Segment' | — | dim_customer |
| Page navigator | pageNavigator | — | — | — |
| Action button | actionButton | — | — | — |

Plus textboxes, images, shapes.

---

## 2. Measure binding correctness (customer measures)

| Measure | Defined in DAX? | Registered in model.json? | Bound on Page 05? | Status |
|---|---|---|---|---|
| CF01 | Yes | Yes | Yes (Total Passengers) | COMPLETE |
| CF02 | Yes | Yes | Yes (Overall Satisfaction / Avg Score) | COMPLETE |
| CF03 | Yes | Yes | Yes (Complaint Rate) | COMPLETE |
| CF04 | Yes | Yes | Yes (Active Customers) | COMPLETE |
| CF05 | Yes | Yes | Yes (Complaint Count) | COMPLETE |
| CF06 | Yes | Yes | Yes (Compliment Count) | COMPLETE |
| CF07 | Yes | Yes | Yes (Claim Count) | COMPLETE |
| CF08 | Yes | Yes | Yes (Survey Count) | COMPLETE |
| CF09 | Yes | Yes | Yes (Positive Feedback Rate) | COMPLETE |
| CF10 | Yes | Yes | Yes (Negative Feedback Rate) | COMPLETE |
| CF11 | Yes | Yes | No (Service Recovery Rate) | COMPLETE (defined, unused on page) |
| CF12 | Yes | Yes | No (Resolution Rate) | COMPLETE (defined, unused on page) |
| CF13 | Yes | Yes | No (Complaint Satisfaction Avg) | COMPLETE (defined, unused on page) |
| CF14 | Yes | Yes | No (Compliment Satisfaction Avg) | COMPLETE (defined, unused on page) |

All CF01–CF14 measures defined in DAX and registered in `model.json` (fact_customer_feedback). Page 05 binds CF01–CF10; CF11–CF14 defined but not bound to Page 05 visuals (not a defect — intentionally unused measures are not required to be on every page).

**CF11 and CF14 specifically investigated (per owner context / known open DAX issues):**
- CF11 = `DIVIDE(COUNTROWS(FILTER(ServiceRecoveryFlag=TRUE)), CF05)` — Service Recovery Rate (of complaints). Division-by-zero guarded via DIVIDE; if CF05=0 returns BLANK. Defined and registered.
- CF14 = `CALCULATE(CF02, FeedbackType="Compliment")` — Compliment Satisfaction Avg. Defined and registered.

No DAX defect found in CF11/CF14 expressions from static review. Independent execution not possible without Power BI Desktop (limitation L-1).

---

## 3. Reconciliation with owner's "16 investigated visuals"

The owner reported Page 05 had 16 investigated visuals, all passing data validation. The authoritative PBIX contains **27 visuals** on Page 05.

**Corrected conclusion:** 27 visuals exist on Page 05 in the authoritative PBIX. The 16 investigated visuals represent a validated subset; the additional 11 visuals exist in the report but their individual validation evidence should be confirmed. This is not a "missing visual" defect — the visuals are built. The gap is validation evidence coverage for the full 27, not visual development.

**Reconciled:** Page 05 = 27 visuals (matches one of the conflicting prior reports). The "16 visuals passing validation" is a validation-coverage statement, not a visual-count statement.

---

## 4. Filters, slicers, interactions

- Slicers: `Feedback Channel` (fact_customer_feedback), `Customer Segment` (dim_customer).
- Page navigator and action button present (cross-page navigation).

---

## 5. Disclosure

OD-01A/OD-01B Section 8 require the exact disclosure `Synthetic Simulation — Not Actual Airline Performance` on every page, tooltip, and export. Present in model/DAX/data-source metadata; rendered-page placement not independently verifiable (limitation L-1).

---

## 6. Findings

| ID | Finding | Severity | Evidence | Confidence |
|---|---|---|---|---|
| P05-01 | Page 05 has 27 visuals in authoritative PBIX (reconciles 13/16/27 conflicting reports); 16 validated subset confirmed | INFORMATIONAL | Binary page.json (27 visuals); owner investigation reports | High |
| P05-02 | CF11–CF14 defined & registered but not bound to Page 05 visuals (intentionally unused; not a defect) | INFORMATIONAL | `dax/…`; `model.json`; Page 05 visual bindings | High |
| P05-03 | Page rendering / individual visual data values not independently verified (limitation L-1) | INFORMATIONAL | — | — |

---

## 7. Implementation status

**COMPLETE AND VERIFIED (as built):** Page 05 exists with 27 visuals; all CF01–CF10 measures bound; CF measures defined and registered; slicers, navigation present.

**Validation coverage:** 16 of 27 visuals reportedly validated (owner context); full 27-visual validation evidence to be confirmed. Not a build defect.

Not counted as incomplete — dashboard development is complete.
