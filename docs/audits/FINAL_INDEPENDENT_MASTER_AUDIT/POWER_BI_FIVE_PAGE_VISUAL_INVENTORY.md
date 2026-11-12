# POWER BI FIVE PAGE VISUAL INVENTORY

**Source of truth:** Authoritative main PBIX `deliverables/power_bi/AEROVISION_360.pbix` (9,422,203 bytes; extracted page.json + per-page visual.json)  
**NOTE:** This inventory differs from the extracted `deliverables/power_bi/report/report.json` (which lists only 44 visuals with different page names). The binary PBIX is authoritative: **5 pages, 120 visuals.**  
**Visual categories counted:** All visual containers including cards, charts, slicers, tables, maps, decomposition trees, page navigators, textboxes, images, shapes, action buttons, images.

---

## Summary by page

| Page | PBIX display name | Visual count |
|---|---|---|
| Page 01 | `01 - Executive Overview` | 24 |
| Page 02 | `02 - Operations` | 23 |
| Page 03 | `Revenue & Finance.` | 23 |
| Page 04 | `COST & FINANCIAL INTELLIGENCE` | 23 |
| Page 05 | `05 - Customer & Service Intelligence` | 27 |
| **Total** | | **120** |

These match the owner's page names exactly. Page 05 = 27 visuals (reconciling the conflicting prior reports of 13/16/27).

---

## Page 01 — Executive Overview (24 visuals)

| # | Visual name (GUID) | Type | Title | Bindings |
|---|---|---|---|---|
| 1 | `134b37e8…` | cardVisual | 'Average Departure Delay (min).' | Data: measure |
| 2 | `26bc4c3b…` | textbox | — | — |
| 3 | `27ee2f1c…` | textbox | — | — |
| 4 | `359e1852…` | clusteredBarChart | 'Disruptions by Category.' | Category: dim_disruption_type; Y: measure |
| 5 | `3aad321b…` | image | — | — |
| 6 | `42655472…` | cardVisual | 'Flights Operated' | Data: measure (FL01) |
| 7 | `6b946b56…` | textbox | — | — |
| 8 | `6c06925f…` | cardVisual | 'Revenue Passengers' | Data: measure (FL02) |
| 9 | `728ff79c…` | shape | — | — |
| 10 | `7a356602…` | donutChart | 'Disruptions Overview' | Category: dim_disruption_type; Y: measure |
| 11 | `8a80ae66…` | slicer | 'FLIGHT DATE RANGE' | Values: dim_date |
| 12 | `8c1f0b07…` | cardVisual | 'Average Disruption Delay.' | Data: measure (DS02) |
| 13 | `966ff6cb…` | lineClusteredColumnComboChart | — | Category: dim_date; Y: measure; Y2: measure |
| 14 | `9bb0512e…` | clusteredBarChart | 'Disruptions by Airline.' | Category: dim_airline; Y: measure |
| 15 | `a221b157…` | slicer | 'AIRLINE' | Values: dim_airline |
| 16 | `a6cde62b…` | textbox | — | — |
| 17 | `b66e39b0…` | textbox | — | — |
| 18 | `c6e915e4…` | lineChart | 'Customer Satisfaction Trend' | Category: dim_date; Y: measure |
| 19 | `cc010976…` | pageNavigator | — | — |
| 20 | `ea6243d0…` | cardVisual | 'Controllable Disruptions.' | Data: measure (DS03) |
| 21 | `ead26b7e…` | cardVisual | 'Cancellation Rate' | Data: measure (FL04) |
| 22 | `eb893d36…` | image | — | — |
| 23 | `f1148b2c…` | textbox | — | — |
| 24 | `f1442aa3…` | cardVisual | 'Total Disruptions' | Data: measure (DS01) |

**Observations:** KPI cards for FL01 (Flights Operated), FL02 (Revenue Passengers), FL04 (Cancellation Rate), DS01 (Total Disruptions), DS02 (Average Disruption Delay), DS03 (Controllable Disruptions). Charts for disruptions by category/airline, satisfaction trend. Slicers for date range and airline. Page navigator present.

---

## Page 02 — Operations (23 visuals)

| # | Visual name (GUID) | Type | Title | Bindings |
|---|---|---|---|---|
| 1 | `04879e1f…` | slicer | 'AIRLINE' | Values: dim_airline |
| 2 | `07780bf6…` | columnChart | 'Flight Status Distribution by Month' | Category: dim_date; Series: fact_flight_operations |
| 3 | `09958aa0…` | cardVisual | 'On-Time Performance' | Data: measure |
| 4 | `15e090b5…` | shape | — | — |
| 5 | `241afe3c…` | image | — | — |
| 6 | `2c1e09b7…` | cardVisual | 'Total Block Minutes' | Data: (blank) |
| 7 | `30c1bae2…` | tableEx | 'Operational KPIs by Route (Top 5)' | Values: dim_route + 3 measures |
| 8 | `4db0f6e0…` | cardVisual | 'Scheduled Flights' | Data: measure |
| 9 | `660ea8a3…` | textbox | — | — |
| 10 | `6771c916…` | lineChart | 'On-Time Performance Trend' | Category: dim_date; Y: measure |
| 11 | `81f645b4…` | image | — | — |
| 12 | `866653e2…` | textbox | — | — |
| 13 | `8e493c57…` | cardVisual | 'Average Arrival Delay' | Data: measure |
| 14 | `9e6a8900…` | slicer | 'FLIGHT DATE RANGE' | Values: dim_date |
| 15 | `a80e6461…` | donutChart | 'Flights by Status' | Category: fact_flight_operations |
| 16 | `c3a78435…` | cardVisual | 'Average Departure Delay' | Data: measure |
| 17 | `c4432dbf…` | textbox | — | — |
| 18 | `ceeafb28…` | cardVisual | 'Flight Completion Rate' | Data: measure |
| 19 | `dc35de89…` | pageNavigator | — | — |
| 20 | `eca43af7…` | columnChart | 'Block Minutes by Airline/Month' | Category: dim_date; Series: dim_airline |
| 21 | `ecd72442…` | clusteredBarChart | 'Flight Operations by Airline' | Category: dim_airline; Y: measure |
| 22 | `ed2f588c…` | shape | — | — |
| 23 | `fb91348f…` | image | — | — |

**Observations:** Operations KPIs (On-Time Performance, Total Block Minutes, Scheduled Flights, Average Arrival/Departure Delay, Flight Completion Rate). Charts for flight status, on-time trend, block minutes, operations by airline. Route KPI table. Slicers for airline and date range.

**Finding P02-01 (MEDIUM):** Page 02 visuals reference FL/DS measures (FL04 Cancellation Rate etc. appear on Page 01). The OP01/OP03/OP04 measures defined in DAX (On-Time Departure Rate, Average Arrival Delay, Flight Completion Rate) are **not registered in `model.json`** and **not bound to any Page 02 visual** — the Operations page does not use the dedicated OP measures.

---

## Page 03 — Revenue & Finance (23 visuals)

| # | Visual name (GUID) | Type | Title | Bindings |
|---|---|---|---|---|
| 1 | `03b43b62…` | cardVisual | 'NET ANCILLARY REVENUE (USD)' | Data: measure |
| 2 | `0970055f…` | clusteredBarChart | 'REVENUE BY BOOKING CHANNEL (USD)' | Category: dim_booking_channel; Y: measure |
| 3 | `11a152b8…` | slicer | 'AIRLINE' | Values: dim_airline |
| 4 | `1f5a97cd…` | clusteredBarChart | 'TOTAL REVENUE BY AIRLINE (USD)' | Category: dim_airline; Y: measure |
| 5 | `2be529e2…` | pageNavigator | — | — |
| 6 | `2c152b70…` | donutChart | 'REVENUE COMPOSITION BY STREAM (USD)' | Y: measure x3 |
| 7 | `3ae90a40…` | image | — | — |
| 8 | `4549d5e9…` | image | — | — |
| 9 | `4de4f261…` | shape | — | — |
| 10 | `61452380…` | textbox | — | — |
| 11 | `6e96f18a…` | clusteredBarChart | 'TOTAL REVENUE BY ROUTE (USD)' | Category: dim_route; Y: measure |
| 12 | `71cedc65…` | treemap | 'REVENUE CONTRIBUTION BY FARE CLASS (USD)' | Group: dim_fare_class; Values: measure |
| 13 | `90df39e4…` | textbox | — | — |
| 14 | `9f8985b6…` | slicer | 'BOOKING CHANNEL' | Values: dim_booking_channel |
| 15 | `a6a2480d…` | cardVisual | 'NET FEE REVENUE (USD)' | Data: measure |
| 16 | `ab115f53…` | cardVisual | 'REVENUE PASSENGERS' | Data: measure |
| 17 | `dbc4dd20…` | cardVisual | 'DISTINCT BOOKINGS' | Data: measure |
| 18 | `e2efeb01…` | slicer | 'FLIGHT DATE RANGE' | Values: dim_date |
| 19 | `e86300a0…` | pivotTable | 'MONTHLY REVENUE PERFORMANCE BY AIRLINE' | Rows: dim_airline; Values: measures |
| 20 | `ed034910…` | cardVisual | 'NET PASSENGER REVENUE (USD)' | Data: measure |
| 21 | `ed6a755a…` | cardVisual | 'AVERAGE REV PER REV PASSENGER (USD)' | Data: measure |
| 22 | `f1abe76a…` | cardVisual | 'TOTAL OPERATING REVENUE (USD)' | Data: measure |
| 23 | `fee309e1…` | lineChart | 'MONTHLY REVENUE TREND (USD)' | Category: dim_date; Y: measure |

**Observations:** Revenue KPI cards (TOTAL OPERATING REVENUE, NET PASSENGER/FEE/ANCILLARY REVENUE, REVENUE PASSENGERS, DISTINCT BOOKINGS, AVERAGE REV PER REV PASSENGER). Charts by channel/airline/route/fare class, revenue composition, monthly trend. Pivot table by airline. Slicers for airline, channel, date.

**Finding P03-01 (HIGH):** Page 03 financial KPI cards depend on RV_/CX_/NC_ measures that require USD-converted financial fact data (FactBookingTransactions, FactOperatingCosts). These facts are **blocked by OD-04** (exchange-rate approval pending) and are **not loaded into the model** — financial values cannot render until OD-04 is approved and exchange rates exist.

---

## Page 04 — COST & FINANCIAL INTELLIGENCE (23 visuals)

| # | Visual name (GUID) | Type | Title | Bindings |
|---|---|---|---|---|
| 1 | `0152f658…` | pageNavigator | — | — |
| 2 | `0b71ff27…` | lineChart | 'Monthly Operating Cost Trend' | Category: dim_date; Y: measure |
| 3 | `1f851d45…` | cardVisual | 'POSITIVE OPERATING COSTS (USD)' | Data: measure |
| 4 | `289a2ead…` | textbox | — | — |
| 5 | `29bd8135…` | slicer | 'FLIGHT DATE RANGE' | Values: dim_date |
| 6 | `4b6fb96a…` | cardVisual | 'TOTAL OPERATING COSTS (USD)' | Data: measure |
| 7 | `64297b11…` | scatterChart | 'Airline Cost Efficiency vs Operating Contribution' | Category: dim_airline; Size/X/Y: measures |
| 8 | `66814fb4…` | actionButton | — | — |
| 9 | `6b916740…` | cardVisual | 'REVENUE-TO-COST RATIO (%)' | Data: measure |
| 10 | `7b9fc3c1…` | map | 'Operating Cost Geographic Distribution' | X: fact_route_costs_map; Y: fact_route_costs_map |
| 11 | `7bf21b8e…` | clusteredBarChart | 'Costs by Category' | Category: fact_operating_costs; Y: measure |
| 12 | `810d8c79…` | cardVisual | 'COST PER FLIGHT OPERATION (USD)' | Data: measure |
| 13 | `8aa781f5…` | slicer | 'AIRLINE' | Values: dim_airline |
| 14 | `973b26c3…` | treemap | 'Route Cost Composition' | Group: dim_route; Values: measure |
| 15 | `ab6b336f…` | cardVisual | 'COST REVERSALS (USD)' | Data: measure |
| 16 | `b4c92752…` | cardVisual | 'NET OPERATING CONTRIBUTION (USD)' | Data: measure |
| 17 | `bae30e58…` | cardVisual | 'NET OPERATING COSTS (USD)' | Data: measure |
| 18 | `c6dbbfe2…` | image | — | — |
| 19 | `d0798840…` | clusteredBarChart | 'Costs by Airline ' | Category: dim_airline; Y: measure |
| 20 | `d4df1502…` | textbox | — | — |
| 21 | `dc221590…` | shape | — | — |
| 22 | `dc7352fe…` | image | — | — |
| 23 | `f8eb8352…` | cardVisual | 'COST PER REVENUE PASSENGER (USD)' | Data: measure |

**Observations:** Cost KPI cards (TOTAL/POSITIVE/NET OPERATING COSTS, COST REVERSALS, COST PER FLIGHT OPERATION, COST PER REVENUE PASSENGER, REVENUE-TO-COST RATIO, NET OPERATING CONTRIBUTION). Cost trend, costs by category/airline, route cost composition (treemap), airline cost efficiency scatter. Map for geographic distribution. Slicers for date and airline.

**Finding P04-01 (HIGH):** Map visual `Operating Cost Geographic Distribution` binds X/Y to `fact_route_costs_map`, a table **not present** in the 16-table `semantic_model/model.json`. This is a potential broken/orphaned visual reference requiring investigation (table may exist only in the in-PBIX binary model, which could not be deserialized — limitation L-2).

**Finding P04-02 (HIGH):** All cost/revenue/contribution KPI cards on Page 04 depend on financial measures blocked by OD-04 (same as Page 03).

---

## Page 05 — Customer & Service Intelligence (27 visuals)

| # | Visual name (GUID) | Type | Title | Bindings |
|---|---|---|---|---|
| 1 | `0fe9bb8f…` | clusteredColumnChart | 'Feedback by Type' | Category: fact_customer_feedback; Y: measure |
| 2 | `14037c71…` | cardVisual | 'Compliment Count' | Data: measure |
| 3 | `1d231063…` | textbox | — | — |
| 4 | `20e756e0…` | cardVisual | 'Claim Count' | Data: measure |
| 5 | `25aacad6…` | cardVisual | 'Active Customers' | Data: measure |
| 6 | `36d2c32e…` | pageNavigator | — | — |
| 7 | `439d392e…` | cardVisual | 'Complaint Count' | Data: measure |
| 8 | `5e92bed6…` | cardVisual | 'Negative Feedback Rate' | Data: measure |
| 9 | `6c568761…` | cardVisual | 'Positive Feedback Rate' | Data: measure |
| 10 | `6c60e5c7…` | cardVisual | 'Overall Satisfaction Rating' | Data: measure |
| 11 | `6e262dd4…` | cardVisual | 'Total Passengers' | Data: measure |
| 12 | `7257f772…` | donutChart | 'Complaint Category Breakdown.' | Series: fact_customer_feedback; Y: measure |
| 13 | `88e52850…` | decompositionTreeVisual | 'Complaint Analysis — Decomposition Tree' | Analyze: measure; ExplainBy: fact_customer_feedback x3, dim_airline, fact_customer_feedback |
| 14 | `8b77e78a…` | cardVisual | 'Survey Count' | Data: measure |
| 15 | `8c24742a…` | shape | — | — |
| 16 | `8df15d8a…` | image | — | — |
| 17 | `9d681854…` | actionButton | — | — |
| 18 | `9db1942d…` | pieChart | 'Customer Segment Distribution.' | Category: dim_customer; Y: measure |
| 19 | `a3673ba6…` | lineChart | 'Average Satisfaction by Airline.' | Category: dim_airline; Y: measure |
| 20 | `b70a5127…` | textbox | — | — |
| 21 | `cc316451…` | image | — | — |
| 22 | `d7c9f82a…` | cardVisual | 'Complaint Rate' | Data: measure |
| 23 | `e282b23a…` | textbox | — | — |
| 24 | `e350f80c…` | slicer | 'Feedback Channel' | Values: fact_customer_feedback |
| 25 | `ebf42944…` | clusteredBarChart | 'Feedback by Channel' | Category: fact_customer_feedback; Y: measure |
| 26 | `f8a8219a…` | slicer | 'Customer Segment' | Values: dim_customer |
| 27 | `fc61d603…` | cardVisual | 'Average Satisfaction Score' | Data: measure |

**Observations:** Customer KPI cards (CF01 Total Feedback/Total Passengers, CF02 Overall Satisfaction/Average Satisfaction Score, CF03 Complaint Rate, CF04 Active Customers, CF05 Complaint Count, CF06 Compliment Count, CF07 Claim Count, CF08 Survey Count, CF09 Positive Feedback Rate, CF10 Negative Feedback Rate, CF11 Service Recovery). Charts for feedback by type/channel, complaint category, customer segment, satisfaction by airline, decomposition tree. Slicers for channel and segment.

**Note on owner context:** The owner reported Page 05 had 16 investigated visuals all passing validation. The authoritative PBIX contains 27 visuals on Page 05. The 16 investigated visuals are a subset that passed validation; the remaining 11 visuals exist in the PBIX but their individual validation evidence should be confirmed. This is reconciled in Phase J (Page 05 pending vs implemented visuals).

---

## Cross-page coherence

- Navigation: page navigators present on Pages 01, 04, 05 (cross-page navigation exists).
- Slicers: date range and airline slicers recur on Pages 01, 02, 03, 04 (shared filter context).
- Measures: FL/DS measures on Pages 01/02; RV/CX/NC financial measures on Pages 03/04 (blocked by OD-04); CF measures on Page 05.
- The five pages collectively form a coherent airline intelligence dashboard (executive → operations → revenue → cost → customer), with Page 03 and 04 both covering financials (revenue vs cost), consistent with the owner's 5-page structure.
