# DAX Measure Audit — AEROVISION 360

## Scope
- `deliverables/power_bi/dax/AEROVISION360_Measures.dax`
- `deliverables/power_bi/semantic_model/model.json`
- `deliverables/power_bi/semantic_model/semantic_model.json`
- `contracts/bi_consumption_model_m311.json`

## Reconciliation against source data (`deliverables/data`)

| Measure | Expected | Recomputed from CSV | Match |
|---|---:|---:|---|
| FL01 Flights Operated | 4,776 | 4,776 | Yes |
| FL02 Total Revenue Passengers | 218,413 | 218,413 | Yes |
| FL03 Average Delay Minutes | 43.42 | 43.4209 | Yes (rounded) |
| FL04 Cancellation Rate | 4.48% | 4.48% | Yes |
| DS01 Total Disruptions | 1,754 | 1,754 | Yes |
| DS02 Average Delay (Disruption) | 120.62 | 120.6152 | Yes (rounded) |
| DS03 Controllable Disruptions | 540 | 540 (fact events whose disruption type is controllable) | Yes only if expression joins to fact |
| CF01 Total Feedback Events | 2,500 | 2,500 | Yes |
| CF02 Average Satisfaction Score | 2.99 | 2.9910 | Yes (rounded) |
| CF03 Complaint Percentage | 25.52% | 25.52% | Yes |

## Findings

### DAX-01 (P1) — DS03 expression counts dimension rows, not fact events
- File: `deliverables/power_bi/dax/AEROVISION360_Measures.dax`
- Current: `DS03 = COUNTROWS ( FILTER ( dim_disruption_type, dim_disruption_type[ControllableFlag] = TRUE() ) )`
- Issue: counts rows in `dim_disruption_type` (3 controllable types), not disruption events. Expected DS03 = 540 events.
- Fix: count `fact_disruptions` where related disruption type is controllable, e.g.
  `COUNTROWS ( FILTER ( fact_disruptions, RELATED ( dim_disruption_type[ControllableFlag] ) = TRUE() ) )`
  (requires active relationship `dim_disruption_type[DisruptionTypeKey] -> fact_disruptions[DisruptionTypeKey]`).

### DAX-02 (P2) — FL04 uses SUM over a boolean column
- File: `deliverables/power_bi/dax/AEROVISION360_Measures.dax`
- Current: `VAR _cancelled = SUM ( fact_flight_operations[CancellationFlag] )`
- Issue: `CancellationFlag` is boolean; DAX `SUM` may not accept boolean depending on storage type. Safer:
  `COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CancellationFlag] = TRUE() ) )`.

### DAX-03 (P2) — Percentage scaling / format ambiguity
- FL04 and CF03 multiply by 100 and therefore return percentage points (4.48, 25.52).
- If these are formatted with Power BI "Percent", they will display 448.00% / 2552.00%.
- Decide either: return fraction and use Percent format, or keep number and use a number format with a literal `%`. Document the chosen convention.

### DAX-04 (P1) — semantic_model/model.json contains wrong measure expressions
- File: `deliverables/power_bi/semantic_model/model.json`
- FL01 expression is `COUNTROWS(fact_flight_operations)` (all rows) instead of operated flights.
- FL02 expression is `SUM(fact_flight_operations[BookedPassengers])` instead of `RevenuePassengers`.
- CF03 expression filters `ComplaintCategory` values instead of `FeedbackType = "Complaint"`.
- DS03 expression counts dimension rows.
- This JSON is a custom specification, not a guaranteed PBIX definition; it must be corrected before use.

### DAX-05 (P2) — model.json omits all dimension tables
- Only 3 fact tables are defined; no dimensions, relationships, or most measures metadata.
- Treat as incomplete custom spec.

### DAX-06 (P2) — semantic_model/semantic_model.json has no expressions
- Lists measure names only; cannot validate logic. Relationship list is incomplete (missing dim_aircraft, dim_airport, dim_customer, dim_disruption_type, dim_date for disruptions/feedback, etc.).

### DAX-07 (P3) — FL02 naming must remain passenger volume
- FL02 must be labeled "Total Revenue Passengers" and never presented as monetary revenue. Report pages must include disclosure "Synthetic Simulation — Not Actual Airline Performance" and OD-04 blocked status.

### DAX-08 (P3) — CF02/CSS scale definition pending (OD-11)
- SatisfactionScore is 1–5; no thresholds should be invented. Document pending owner decision.

## Correct approved expressions (reference)
```
FL01 = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[FlightStatus] = "Operated" ) )
FL02 = SUM ( fact_flight_operations[RevenuePassengers] )
FL03 = AVERAGE ( fact_flight_operations[DepartureDelayMinutes] )
FL04 = VAR _total = COUNTROWS ( fact_flight_operations )
       VAR _cancelled = COUNTROWS ( FILTER ( fact_flight_operations, fact_flight_operations[CancellationFlag] = TRUE() ) )
       RETURN IF ( _total = 0, BLANK(), DIVIDE ( _cancelled, _total ) * 100 )
DS01 = COUNTROWS ( fact_disruptions )
DS02 = AVERAGE ( fact_disruptions[DelayMinutes] )
DS03 = COUNTROWS ( FILTER ( fact_disruptions, RELATED ( dim_disruption_type[ControllableFlag] ) = TRUE() ) )
CF01 = COUNTROWS ( fact_customer_feedback )
CF02 = AVERAGE ( fact_customer_feedback[SatisfactionScore] )
CF03 = VAR _total = COUNTROWS ( fact_customer_feedback )
       VAR _complaints = COUNTROWS ( FILTER ( fact_customer_feedback, fact_customer_feedback[FeedbackType] = "Complaint" ) )
       RETURN IF ( _total = 0, BLANK(), DIVIDE ( _complaints, _total ) * 100 )
```
