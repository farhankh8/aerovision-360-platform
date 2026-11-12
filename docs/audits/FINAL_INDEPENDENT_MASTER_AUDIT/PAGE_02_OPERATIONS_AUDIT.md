# PAGE 02 — OPERATIONS AUDIT

**Source:** Authoritative main PBIX `deliverables/power_bi/AEROVISION_360.pbix`, page folder `3ba663f9b94b183d8484`  
**Page name:** `02 - Operations`  
**Page order:** Page 02 (second page)  
**Visual count:** 23  
**Page rendered in Power BI Desktop:** Not independently verified (limitation L-1); visual metadata verified from binary.

---

## 1. Visual inventory

23 visuals (full table in `POWER_BI_FIVE_PAGE_VISUAL_INVENTORY.md`). Key data visuals:

| Visual | Type | Title | Bound measure | Bound column/table |
|---|---|---|---|---|
| Card | cardVisual | 'On-Time Performance' | measure | — |
| Card | cardVisual | 'Total Block Minutes' | measure | — (binding blank) |
| Card | cardVisual | 'Scheduled Flights' | measure | — |
| Card | cardVisual | 'Average Arrival Delay' | measure | — |
| Card | cardVisual | 'Average Departure Delay' | measure | — |
| Card | cardVisual | 'Flight Completion Rate' | measure | — |
| Column chart | columnChart | 'Flight Status Distribution by Month' | Series: fact_flight_operations | dim_date |
| Column chart | columnChart | 'Block Minutes by Airline/Month' | Series: dim_airline | dim_date |
| Line chart | lineChart | 'On-Time Performance Trend' | measure | dim_date |
| Donut chart | donutChart | 'Flights by Status' | — | fact_flight_operations |
| Clustered bar chart | clusteredBarChart | 'Flight Operations by Airline' | measure | dim_airline |
| Table | tableEx | 'Operational KPIs by Route (Top 5)' | 3 measures | dim_route |
| Slicer | slicer | 'AIRLINE' | — | dim_airline |
| Slicer | slicer | 'FLIGHT DATE RANGE' | — | dim_date |

Plus textboxes, images, shapes, page navigator.

---

## 2. Measure binding correctness

| Measure | Defined in DAX? | Registered in model.json? | Bound on Page 02? | Status |
|---|---|---|---|---|
| FL01 | Yes | Yes | Indirect (Scheduled Flights / Flights by Status) | COMPLETE |
| FL03 | Yes | Yes | Average Departure/Arrival Delay | COMPLETE |
| FL04 | Yes | Yes | Flight Completion Rate | COMPLETE |
| DS01–DS03 | Yes | Yes | Not on Page 02 | — |
| OP01 (On-Time Departure Rate) | Yes | **NO** | **NO** | NOT REGISTERED / NOT BOUND |
| OP03 (Average Arrival Delay) | Yes | **NO** | **NO** | NOT REGISTERED / NOT BOUND |
| OP04 (Flight Completion Rate) | Yes | **NO** | **NO** | NOT REGISTERED / NOT BOUND |

**Critical finding:** OP01, OP03, OP04 are defined in the DAX file (`dax/AEROVISION360_Measures.dax` lines 31–33) but are **absent from `semantic_model/model.json`** (which registers only FL01–FL04 for fact_flight_operations) and are **not bound to any Page 02 visual**. Page 02 uses generic FL/DS-bound cards instead of the dedicated OP operations measures.

---

## 3. Filters, slicers, interactions

- Slicers: `AIRLINE` (dim_airline), `FLIGHT DATE RANGE` (dim_date).
- Table visual `Operational KPIs by Route (Top 5)` binds dim_route + 3 measures.

---

## 4. Findings

| ID | Finding | Severity | Evidence | Confidence |
|---|---|---|---|---|
| P02-01 | OP01, OP03, OP04 measures defined in DAX but not registered in model.json and not bound to any Page 02 visual | HIGH | `dax/…` lines 31–33; `model.json` fact_flight_operations measures = [FL01..FL04] only; Page 02 visual bindings | High |
| P02-02 | `Total Block Minutes` card shows blank measure binding in visual.json | MEDIUM | Page 02 visual `2c1e09b7…` Bindings empty | Medium |
| P02-03 | Page rendering not independently verified (limitation L-1) | INFORMATIONAL | — | — |

---

## 5. Implementation status

**IMPLEMENTED — NOT FULLY VERIFIED:** Page 02 exists with 23 visuals; operational cards/charts present and bound; slicers present.

**GAP:** OP01/OP03/OP04 measures (3) defined in DAX but missing from model registration and unbound — a model registration gap, not a dashboard-build gap. Can be resolved by registering the three measures in the semantic model (no OD/G4 dependency).
