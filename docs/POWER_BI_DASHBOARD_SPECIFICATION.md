# AEROVISION 360 — Power BI Dashboard Specification

**Status:** ENGINEERING PREPARATION — DESIGNED, NOT IMPLEMENTED; NO REPORT OR DASHBOARD
**Version:** 0.1
**Prepared:** 2026-11-02
**Governing contract:** `docs/03_DATA_CONTRACTS.md` version 1.5
**KPI authority:** `docs/DAX_KPI_CATALOGUE.md`
**Companion documents:** `POWER_BI_SEMANTIC_MODEL_BLUEPRINT.md`, `IMPLEMENTATION_QA_BLUEPRINT.md`
**Project root:** `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`

> **Status notice.** This is a report specification, not a built report. No Power BI page, visual, PBIX, PBIP, screenshot, export, or dashboard exists. `power_bi/` is empty. G3 is `NOT STARTED`; G4 is `BLOCKED`; report implementation and publication are `NOT AUTHORIZED`.

## 1. Purpose and experience principles

AEROVISION 360 must read as a serious multi-airline intelligence product, not a chart collection. The five pages answer a defined chain of questions:

1. **Executive Overview** — Is the network creating value, and where are the exceptions?
2. **Network & Capacity Intelligence** — Where is capacity deployed, and how efficiently is it used?
3. **Revenue & Yield Intelligence** — What drives revenue, yield, and unit economics?
4. **Operations & Disruption** — Where is reliability failing, and why?
5. **Customer & Service Intelligence** — What is the customer experience and recovery picture?

**Principles:**

- Every visual answers a named business question.
- KPI cards are large, stable, and not accidentally cross-filtered by unrelated visuals.
- Detail is available through drill-through, not by crowding the first screen.
- The exact synthetic disclosure is always visible and is never conditional.
- No unsupported fields are added to satisfy a visual idea. A missing field becomes `OWNER DECISION REQUIRED`, not a silent invention.
- The report uses the contract's 21 KPIs; supporting metrics may add context but must not replace them.
- Accessibility and mobile layout are designed, not retrofitted.

## 2. Design system

### 2.1 Canvas and grid

| Element | Specification |
|---|---|
| Canvas | 16:9, 1366 × 768 px |
| Safe margin | 16 px |
| Grid | 12 columns, 16 px gutter |
| Header | 64 px high; page title, context, last-refresh label |
| Navigation rail | 88 px wide, left side; five page buttons |
| Filter bar | 44 px high below header; airline, period, route region, page-specific filters |
| Content area | Remaining height; 8 px vertical rhythm |
| Footer disclosure | 30 px high, persistent on every page and drill-through page |
| Card | White surface, 1 px border, 8 px radius, 12 px padding |
| Visual gap | 12–16 px |

### 2.2 Colour system

| Token | Hex | Use |
|---|---|---|
| Ink | `#102A43` | Primary text and titles |
| Secondary ink | `#486581` | Labels and secondary text |
| Background | `#F4F6F8` | Page background |
| Surface | `#FFFFFF` | Cards and tables |
| Border | `#D9E2EC` | Card and table borders |
| Brand teal | `#0B7285` | Primary series, selected state |
| Informational blue | `#1C7ED6` | Secondary series |
| Attention amber | `#E67700` | Warning/exception, not failure |
| Negative red | `#C92A2A` | Negative contribution, cancellations, critical exception |
| Positive green | `#2B8A3E` | Positive contribution, completion, resolved recovery |
| Neutral grey | `#829AB1` | Benchmark, unavailable, prior period |

**Rules:** no red/green as the only encoding; pair colour with a label, icon, or sign; max five data colours per visual; use grey for non-selected context; do not use 3D, gradients for data, pies, or decorative images.

### 2.3 Typography

| Role | Font | Size | Weight |
|---|---|---|---|
| Page title | Segoe UI Semibold | 22 px | 600 |
| KPI value | Segoe UI Semibold | 30 px | 600 |
| KPI label | Segoe UI | 11 px | 400 |
| Visual title | Segoe UI Semibold | 14 px | 600 |
| Axis/label | Segoe UI | 10–11 px | 400 |
| Body/note | Segoe UI | 11 px | 400 |
| Disclosure | Segoe UI Semibold | 11 px | 600 |

Minimum report text is 10 px for axis ticks and 11 px for labels/notes. Do not rely on tiny text for definitions; use a definitions bookmark or side panel.

### 2.4 Page chrome

- **Header:** page name, one-sentence question, period label, `Synthetic Simulation` badge.
- **Navigation rail:** Executive, Network, Revenue, Operations, Customer; icon + short label; selected page has teal bar and white surface.
- **Filter bar:** airline multi-select, period (default = reporting period), route region; page-specific filters only where needed.
- **Footer:** exact disclosure, data-refresh timestamp, selected reference version (display only, not a filter), and a `Definitions` button.
- **Exceptions:** a small amber dot on a nav item indicates a page with an exception; do not use animation.

### 2.5 KPI card specification

| Element | Rule |
|---|---|
| Title | Business name and KPI ID in the tooltip, not in the card title |
| Value | Formatted per DAX catalogue; `BLANK` displays as an em dash, not zero |
| Context | Comparison label only when a valid comparison exists; no invented target |
| Subtext | Denominator/response count for ratios; unit for volumes |
| Sparkline | Optional only if it uses the same measure and a valid time axis |
| Interaction | KPI cards do not cross-filter by other visuals; they respond only to page slicers |
| Tooltip | Custom tooltip with definition, numerator, denominator, date role, disclosure |

### 2.6 Tables and matrices

- Use tables for exceptions and detail, matrices for route/airline hierarchies.
- Sort by the most decision-relevant measure; state the sort in the visual title.
- Top N with an explicit `Top 10` label; do not hide the remainder without a note.
- Numeric alignment right; text left; no merged cells; no blank rows.
- Conditional formatting uses colour plus sign/label. Negative unit contribution is red with a minus sign.
- Row height ≥ 28 px; header 32 px; freeze/scroll where supported.

### 2.7 Tooltips and disclosure

Every custom tooltip page includes the exact string:

`Synthetic Simulation — Not Actual Airline Performance`

Default tooltips are disabled because they cannot guarantee the disclosure. If a visual cannot use a custom tooltip, disable the tooltip and expose values in a side panel. This is a T-79 requirement, not a preference.

## 3. Page map and navigation

| Page | Type | Purpose | Primary KPIs |
|---|---|---|---|
| Executive Overview | Visible | Network value and exceptions | K-01, K-02, K-03, K-06, K-07, K-08, K-09, K-10 |
| Network & Capacity Intelligence | Visible | Capacity, routes, airports, utilization | K-01, K-02, K-03, K-13 |
| Revenue & Yield Intelligence | Visible | Revenue, yield, mix, booking, refunds | K-04, K-05, K-06, K-07, K-08, K-14, K-15, K-16, K-17 |
| Operations & Disruption | Visible | OTP, cancellations, delay, causes, recovery | K-09, K-10, K-11, K-12, K-13 |
| Customer & Service Intelligence | Visible | Satisfaction, complaints, refunds, repeat, recovery | K-17, K-18, K-19, K-20, K-21 |
| DRL-Airline | Hidden drill-through | Airline detail | Context-dependent |
| DRL-Route | Hidden drill-through | Route detail | Context-dependent |
| DRL-Flight | Hidden drill-through | Flight detail | Context-dependent |
| DRL-Feedback | Hidden drill-through | Feedback detail | Context-dependent |

**Navigation behavior:** page buttons use bookmarks or page navigation; selected state is visible; `Reset filters` returns to the reporting period, all airlines, all regions. Do not hide the disclosure behind navigation.

## 4. Global filters and interactions

| Filter | Type | Default | Pages | Notes |
|---|---|---|---|---|
| Period | Date range / relative date | 2025-10-01 to 2026-09-30 | All | Use `DimDate[IsReportingPeriod] = TRUE`; prior-period comparisons may use the full date range |
| Airline | Multi-select | All 10 | All | Use `DimAirline[AirlineName]`; never `AirlineId` or code as the filter key |
| Route region | Multi-select | All | All | Controlled `DimRoute[RouteRegion]` |
| Origin airport | Multi-select | All | Network, Operations | `DimAirport - Origin[AirportCode]` |
| Destination airport | Multi-select | All | Network, Operations | `DimAirport - Destination[AirportCode]` |
| Fare class | Multi-select | All | Revenue | Do not slice yield/RASK by fare class; use mix/average-fare visuals |
| Channel | Multi-select | All | Revenue, Customer | Do not slice unit revenue by channel without a compatible denominator |
| Feedback type | Multi-select | All | Customer | Survey/Complaint/Compliment/Claim |
| Disruption type | Multi-select | All | Operations | Controlled taxonomy; includes Unattributed |
| Aircraft type | Multi-select | All | Network, Operations | `DimAircraftType` |

**Interaction rules:**

- KPI cards respond to page slicers only; unrelated visuals do not cross-filter them.
- Clicking an airline in a ranking filters the page's supporting visuals; it does not change the page's KPI cards unless the user uses the slicer.
- Clicking a route in the map/table opens or filters route context; use a clear selection state.
- Cross-highlighting is allowed only where the target has a shared dimension; never cross-filter a fact with a fact.
- `Edit interactions` must be reviewed page by page; no accidental filtering of disclosure or navigation.
- Sync slicers: airline, period, route region. Do not sync fare class/channel across pages where they do not apply.
- Bookmarks: `Reset filters`, `Definitions`, `Scenario assumptions`, `Data notes`; each bookmark preserves the disclosure.
- No automatic page refresh; no live data; no external map dependency without a fallback.

### 4.1 Date-role guardrail

The model has multiple active date roles: scheduled departure, scheduled arrival, actual departure, actual arrival, booking, travel, feedback, and disruption event. A page-level date slicer filters each fact through its active relationship, which is not necessarily the same business date for every visual.

Rules:

- Label the date role on every trend, table, and tooltip; never use a generic `Date` label when the underlying role differs.
- Do not use a travel-date filter to imply a booking-date cohort for K-16, K-17, or K-20. Use the dedicated booking-date filter or a clearly labelled bookmark.
- Do not compare sub-periods across facts with different date roles unless the measure uses `USERELATIONSHIP` or a role-aware calculation and the visual states it.
- K-18 intentionally combines feedback-date complaints and departure-date passengers within the same period; label it `Period Complaint Rate`, not a cohort rate.
- K-08 combines revenue by travel date, cost by cost date, and ASK by departure date. At page-period level this is the intended mixed-fact KPI; sub-period comparisons require a documented role-aware measure.
- A visual that cannot state its date role is not ready for review.

## 5. Page 1 — Executive Overview

**Business question:** Is the network creating operating value, and which airlines or routes require attention?

**Layout (top to bottom):**

1. Header and global filter bar.
2. KPI row A: Total Operating Revenue, Operating Cost, Unit Contribution, Load Factor.
3. KPI row B: Total RASK, CASK, OTP, Cancellation Rate.
4. Middle-left: monthly revenue vs cost line chart.
5. Middle-right: unit contribution by airline horizontal bar, sorted descending.
6. Lower-left: OTP vs cancellation scatter by airline; bubble size = revenue passengers.
7. Lower-right: exception table by airline.
8. Footer disclosure.

| ID | Visual | Type | Field wells | Purpose | Interaction |
|---|---|---|---|---|---|
| EX-01 | Total Operating Revenue | KPI card | `[Total Operating Revenue USD]` | Scale | Page slicers only |
| EX-02 | Operating Cost | KPI card | `[Operating Cost USD]` | Cost base | Page slicers only |
| EX-03 | Unit Contribution | KPI card | `[Unit Contribution]` | Value per ASK | Page slicers only |
| EX-04 | Load Factor | KPI card | `[Load Factor]` | Capacity use | Page slicers only |
| EX-05 | Total RASK | KPI card | `[Total RASK]` | Unit revenue | Page slicers only |
| EX-06 | CASK | KPI card | `[CASK]` | Unit cost | Page slicers only |
| EX-07 | OTP | KPI card | `[On Time Performance]` | Reliability | Page slicers only |
| EX-08 | Cancellation Rate | KPI card | `[Cancellation Rate]` | Reliability risk | Page slicers only |
| EX-09 | Monthly revenue vs cost | Line chart | Axis: `DimDate[YearMonth]`; Values: `[Total Operating Revenue USD]`, `[Operating Cost USD]` | Trend and gap | Cross-filter airline/route context |
| EX-10 | Unit contribution by airline | Horizontal bar | Axis: `DimAirline[AirlineName]`; Value: `[Unit Contribution]`; colour: sign | Ranking and negative outliers | Filters airline context |
| EX-11 | OTP vs cancellation | Scatter | X: `[On Time Performance]`; Y: `[Cancellation Rate]`; Size: `[Revenue Passengers]`; Detail: `DimAirline[AirlineName]` | Reliability trade-off | Select airline |
| EX-12 | Airline exception table | Table | Airline, Total RASK, CASK, Unit Contribution, OTP, Cancellation Rate, Period Complaint Rate, Satisfaction | Decision table | Select airline; drill-through to DRL-Airline |

**Notes and callouts:** `Unit Contribution` is not net profit; it excludes non-operating items. No target line appears until OD-21 defines targets. The table must show an em dash for BLANK ratios, not zero.

**Filters:** period, airline, route region. Do not put fare class/channel on this page.

**Drill-through:** `DRL-Airline` on airline rows.

**Tooltip:** airline performance tooltip with revenue, unit contribution, OTP, cancellation rate, and disclosure. KPI tooltips show definition, numerator, denominator, date role, and disclosure.

**Mobile:** four KPI cards, revenue/cost chart, unit-contribution bar, top-five exception table, disclosure.

## 6. Page 2 — Network & Capacity Intelligence

**Business question:** Where is capacity deployed, how efficiently is it used, and which routes/airports drive the network?

**Layout:** KPI row; map/route visual; route region capacity; route efficiency table; seasonality; airport/route detail.

| ID | Visual | Type | Field wells | Purpose | Interaction |
|---|---|---|---|---|---|
| NW-01 | ASK | KPI card | `[ASK]` | Offered capacity | Page slicers only |
| NW-02 | RPK | KPI card | `[RPK]` | Traffic | Page slicers only |
| NW-03 | Load Factor | KPI card | `[Load Factor]` | Capacity efficiency | Page slicers only |
| NW-04 | Revenue Passengers | KPI card | `[Revenue Passengers]` | Traffic scale | Page slicers only |
| NW-05 | Aircraft Utilization | KPI card | `[Aircraft Utilization]` | Fleet productivity | Page slicers only |
| NW-06 | Scheduled Flights | KPI card | `[Scheduled Flights]` | Schedule scale | Page slicers only |
| NW-07 | Route map | Map / flow map | Origin: `DimAirport - Origin[Latitude]`, `Longitude`; Destination: `DimAirport - Destination[Latitude]`, `Longitude`; Size: `[ASK]`; Colour: `[Load Factor]`; Tooltip: route, airline, RPK, revenue | Network pattern | Select route; filter table |
| NW-08 | Capacity by route region | Stacked bar | Axis: `DimRoute[RouteRegion]`; Values: `[ASK]` by airline; Legend: `DimAirline[AirlineName]` | Regional concentration | Cross-filter route table |
| NW-09 | Route efficiency table | Table | RouteCode, Origin, Destination, Airline, ASK, RPK, Load Factor, Total RASK, CASK, Unit Contribution | Route decisions | Sort by contribution; drill-through DRL-Route |
| NW-10 | Monthly ASK/RPK | Line chart | Axis: `DimDate[YearMonth]`; Values: `[ASK]`, `[RPK]` | Seasonality | Filter by route/airline |
| NW-11 | Top/bottom load factor routes | Bar | Axis: route; Value: `[Load Factor]`; Top/Bottom N with label | Diagnose imbalance | Select route |
| NW-12 | Airport role filter panel | Slicers | Origin airport, destination airport, aircraft type | Network focus | Page-wide |

**Map rule:** use the built-in map only if the tenant permits it and the visual renders reliably. If not, replace it with a route origin/destination matrix and a bar chart; do not leave a broken map. The fallback must preserve the same questions, fields, and disclosure.

**Route table rule:** show at least 15 rows; provide top/bottom toggles; do not hide negative contribution. Unit contribution uses total operating revenue minus operating cost per ASK; it is not route profitability after overhead allocation unless the allocation is visible.

**Filters:** period, airline, route region, origin, destination, aircraft type.

**Drill-through:** `DRL-Route`.

**Tooltip:** route tooltip with ASK, RPK, load factor, total RASK, CASK, unit contribution, top airline, and disclosure.

**Mobile:** KPI row, route table top 10, route region bar, map replaced by route list if maps are unreliable.

## 7. Page 3 — Revenue & Yield Intelligence

**Business question:** What drives revenue, yield, and unit economics, and how are fare, channel, booking, and refund behaviors changing?

**Layout:** KPI row; revenue trend; yield/RASK/CASK; mix; booking behavior; refund; scenario panel.

| ID | Visual | Type | Field wells | Purpose | Interaction |
|---|---|---|---|---|---|
| RV-01 | Total Operating Revenue | KPI card | `[Total Operating Revenue USD]` | Scale | Page slicers only |
| RV-02 | Passenger Revenue | KPI card | `[Net Passenger Revenue USD]` | Core revenue | Page slicers only |
| RV-03 | Ancillary Revenue | KPI card | `[Net Ancillary Revenue USD]` | Ancillary contribution | Page slicers only |
| RV-04 | Passenger Yield | KPI card | `[Passenger Yield]` | Revenue per RPK | Page slicers only |
| RV-05 | Passenger RASK | KPI card | `[Passenger RASK]` | Revenue per ASK | Page slicers only |
| RV-06 | Total RASK | KPI card | `[Total RASK]` | Total unit revenue | Page slicers only |
| RV-07 | CASK | KPI card | `[CASK]` | Unit cost | Page slicers only |
| RV-08 | Unit Contribution | KPI card | `[Unit Contribution]` | Margin per ASK | Page slicers only |
| RV-09 | Revenue trend by stream | Stacked column/line | Axis: `DimDate[YearMonth]`; Values: `[Net Passenger Revenue USD]`, `[Net Fee Revenue USD]`, `[Net Ancillary Revenue USD]` | Mix over time | Filter airline/route |
| RV-10 | Yield and RASK trend | Line chart | Axis: `DimDate[YearMonth]`; Values: `[Passenger Yield]`, `[Passenger RASK]`, `[Total RASK]` | Unit revenue trend | Filter context |
| RV-11 | RASK vs CASK | Line/column | Axis: `DimDate[YearMonth]`; Values: `[Total RASK]`, `[CASK]` | Contribution spread | Filter context |
| RV-12 | Fare class mix | Horizontal bar | Axis: `DimFareClass[FareClassName]`; Value: `[Net Passenger Revenue USD]`; Share label | Fare contribution | Filter airline/route |
| RV-13 | Channel mix | Horizontal bar | Axis: `DimBookingChannel[ChannelName]`; Value: `[Net Passenger Revenue USD]` | Distribution contribution | Filter airline/route |
| RV-14 | Average passenger revenue | Bar | Axis: `DimAirline[AirlineName]`; Value: `[Average Passenger Revenue]` | Passenger value | Select airline |
| RV-15 | Ancillary per passenger | Bar | Axis: `DimAirline[AirlineName]`; Value: `[Ancillary Revenue per Passenger]` | Ancillary performance | Select airline |
| RV-16 | Booking lead time | Histogram/column | Axis: lead-time bin; Value: count of eligible bookings; line: `[Booking Lead Time]` | Booking behavior | Dedicated booking-date filter; owner-decision note |
| RV-17 | Refund rate | Line/column | Axis: `DimDate[YearMonth]` (booking-date role via measure); Value: `[Refund Rate]` | Refund trend | Filter airline |
| RV-18 | Scenario panel | Cards/inputs | `FareChangePct`, `FuelCostChangePct`, `CapacityChangePct`; outputs `[Fare Scenario Revenue]`, `[Fuel Scenario Cost]`, `[Capacity Scenario ASK]` | Transparent what-if | No writeback; assumptions visible |

**Critical grain rules:**

- K-04, K-05, K-06, K-07, K-08, K-14, and K-15 use flight capacity/traffic denominators. Do not slice these measures by fare class, channel, or customer and present the result as a valid unit revenue. Use revenue mix, average fare, or a separately defined fare-class measure instead.
- K-16 uses booking-date eligibility and booking-level deduplication. The page's travel-date filter is not a booking-date cohort. Use a dedicated `DimDate` slicer labelled `Booking date`; the measure activates the inactive `BookingDateKey` relationship with `USERELATIONSHIP`. Do not use the travel-date slicer for K-16.
- K-17 uses booking-date eligibility and the same `USERELATIONSHIP` role switch. Do not present it as a travel-date refund rate without changing the date role and label.
- K-20 uses booking-date eligibility and the same role switch. Label it `Repeat Booking Rate — booking date`.
- Scenario outputs are report-layer calculations, not facts, not forecasts, and not official KPIs. Show baseline, formula, assumptions, and limitations.

**Filters:** period (travel date), airline, route region, fare class, channel. Add a `Booking date`-labelled `DimDate` slicer to K-16/K-17/K-20 visuals; their measures switch to the inactive booking relationship with `USERELATIONSHIP`.

**Drill-through:** `DRL-Airline`, `DRL-Route`.

**Tooltip:** revenue definition, numerator/denominator, date role, exclusions, and disclosure.

**Mobile:** top four KPI cards, revenue trend, mix bars, lead-time note, refund trend, disclosure.

## 8. Page 4 — Operations & Disruption

**Business question:** Where is reliability failing, what causes it, and how does disruption affect the network?

**Layout:** KPI row; OTP trend; delay distribution; cause mix; airport hotspots; utilization; flight detail.

| ID | Visual | Type | Field wells | Purpose | Interaction |
|---|---|---|---|---|---|
| OP-01 | OTP | KPI card | `[On Time Performance]` | Departure reliability | Page slicers only |
| OP-02 | On-Time Arrival % | KPI card | `[S-03 On-Time Arrival %]` | Arrival reliability | Page slicers only |
| OP-03 | Cancellation Rate | KPI card | `[Cancellation Rate]` | Cancellation risk | Page slicers only |
| OP-04 | Completion Rate | KPI card | `[Completion Rate]` | Schedule completion | Page slicers only |
| OP-05 | Average Arrival Delay | KPI card | `[Average Arrival Delay]` | Delay severity | Page slicers only |
| OP-06 | Aircraft Utilization | KPI card | `[Aircraft Utilization]` | Fleet productivity | Page slicers only |
| OP-07 | Disruption Rate | KPI card | `[S-05 Disruption Rate]` | Event exposure | Page slicers only |
| OP-08 | Reactionary Delay Share | KPI card | `[S-06 Reactionary Delay Share]` | Network propagation | Page slicers only |
| OP-09 | OTP trend | Line chart | Axis: `DimDate[YearMonth]`; Value: `[On Time Performance]` | Trend | Filter airline/route |
| OP-10 | Delay distribution | Column chart | Axis: arrival-delay bin; Value: count of operated flights; label `n` | Delay shape | Filter airline/airport |
| OP-11 | Delay minutes by cause | Horizontal bar | Axis: `DimDisruptionType[DisruptionName]`; Value: sum of `DelayMinutes`; colour: category | Cause concentration | Select cause |
| OP-12 | Disruption events by airport | Table/bar | Axis: `DimAirport - Event Location[AirportCode]`; Value: event count, delay minutes, affected flights | Hotspots | Select airport |
| OP-13 | Utilization by airline/type | Bar | Axis: `DimAirline[AirlineName]` or `DimAircraftType[AircraftModel]`; Value: `[Aircraft Utilization]` | Productivity | Filter context |
| OP-14 | Flight detail table | Table | FlightLegID, airline, route, status, scheduled/actual, arrival delay, passengers, primary cause | Investigation | Drill-through DRL-Flight |

**Delay distribution rule:** use a documented report-layer binning approach; do not create a new fact column without approval. Label bins as minutes and state the bin edges. Do not use a log scale without a label.

**Cause rule:** `PrimaryCauseFlag` identifies the primary cause for attribution; event-level delay can include multiple causes. Do not sum `PrimaryCauseFlag` and `DelayMinutes` in a way that double-counts. The visual must state whether it shows event-level delay or primary-cause delay.

**Disruption type:** the contract has no severity column. Do not add severity. Use delay minutes, type/category, and recovery status. If a severity view is required, it is `OWNER DECISION REQUIRED` and requires a contract change.

**Filters:** period, airline, route region, origin, destination, disruption type, aircraft type.

**Drill-through:** `DRL-Flight`.

**Tooltip:** flight tooltip with status, delay, event sequence, primary cause, reactionary evidence, and disclosure.

**Mobile:** KPI row, OTP trend, cause bar, airport hotspot list, flight table top 10.

## 9. Page 5 — Customer & Service Intelligence

**Business question:** How satisfied are customers, where are complaints and refunds concentrated, and how well are service cases recovered?

**Layout:** KPI row; satisfaction trend; complaint rate; complaint category; channel; refund trend; repeat rate; recovery; feedback table.

| ID | Visual | Type | Field wells | Purpose | Interaction |
|---|---|---|---|---|---|
| CS-01 | Satisfaction | KPI card | `[Satisfaction]` | Average score | Page slicers only |
| CS-02 | Period Complaint Rate | KPI card | `[Period Complaint Rate]` | Complaints per 1,000 passengers | Page slicers only |
| CS-03 | Refund Rate | KPI card | `[Refund Rate]` | Refund exposure | Page slicers only |
| CS-04 | Repeat Booking Rate | KPI card | `[Repeat Booking Rate]` | Customer retention proxy | Page slicers only |
| CS-05 | Service Recovery Rate | KPI card | `[Service Recovery Rate]` | Resolution performance | Page slicers only |
| CS-06 | Feedback Volume | KPI card | `[Feedback Volume]` | Evidence base | Page slicers only |
| CS-07 | Satisfaction trend | Line chart | Axis: `DimDate[YearMonth]`; Value: `[Satisfaction]`; secondary label: response count | Experience trend | Filter airline/region |
| CS-08 | Complaint rate by airline | Horizontal bar | Axis: `DimAirline[AirlineName]`; Value: `[Period Complaint Rate]` | Outlier detection | Select airline |
| CS-09 | Complaint category mix | Horizontal bar | Axis: `FactCustomerFeedback[ComplaintCategory]`; Value: `[Complaint Events]` | Root-cause themes | Filter context |
| CS-10 | Feedback channel mix | Horizontal bar | Axis: `FactCustomerFeedback[FeedbackChannel]`; Value: `[Complaint Events]` | Channel concentration | Filter context |
| CS-11 | Refund rate trend | Line chart | Axis: `DimDate[YearMonth]` (booking-date role via measure); Value: `[Refund Rate]` | Refund trend | Filter airline |
| CS-12 | Repeat booking rate by airline | Bar | Axis: `DimAirline[AirlineName]`; Value: `[Repeat Booking Rate]` | Loyalty proxy | Select airline; owner-decision note |
| CS-13 | Service recovery by airline | Bar | Axis: `DimAirline[AirlineName]`; Value: `[Service Recovery Rate]` | Recovery performance | Select airline |
| CS-14 | Feedback detail table | Table | FeedbackID, airline, route, type, score, category, recovery, resolution status/date | Investigation | Drill-through DRL-Feedback |

**No sentiment visual.** The contract has no sentiment column and no service-category column. Do not build a sentiment gauge, sentiment trend, or word cloud. Sentiment is an `OWNER DECISION REQUIRED` extension requiring a contract change. Use satisfaction, complaint category, and resolution status as supported evidence.

**Small-base rule:** show response/event counts next to every average or rate. If the count is below a documented threshold, label the value as low-base rather than hiding the data. The threshold is a report rule, not a contract KPI.

**Complaint-rate date rule:** numerator uses `FeedbackDateKey`; denominator uses `ScheduledDepartureDateKey`. The page date filter applies to both active relationships. Do not label this a cohort-matched complaint rate; cohort matching is OP-01 and remains open.

**Filters:** period (role-aware: feedback for satisfaction/complaints, booking for refund/repeat), airline, route region, feedback type, channel. Label the period control `Period`, not `Feedback date`, when K-17 or K-20 is on the page.

**Drill-through:** `DRL-Feedback`.

**Tooltip:** feedback summary with type, score, category, recovery, resolution, and disclosure; no PII.

**Mobile:** KPI row, satisfaction trend, complaint category, recovery bar, feedback table top 10.

## 10. Drill-through and tooltip pages

### 10.1 DRL-Airline

- Source: airline ranking, exception table, airline bar.
- Passed filter: `DimAirline[AirlineKey]`.
- Content: airline name, active status, total operating revenue, operating cost, unit contribution, load factor, OTP, cancellation rate, complaint rate, satisfaction; route table; monthly trend; disclosure.
- No customer PII.

### 10.2 DRL-Route

- Source: route table/map.
- Passed filter: `DimRoute[RouteKey]`.
- Content: route code, origin/destination, distance, ASK, RPK, load factor, total RASK, CASK, unit contribution, OTP, cancellation rate; airline comparison; monthly trend; disclosure.
- Show allocation caveat if route cost includes allocated overhead.

### 10.3 DRL-Flight

- Source: flight table.
- Passed filter: `FactFlightOperations[FlightOperationKey]`.
- Content: FlightLegID, flight number, airline, route, aircraft, scheduled/actual timestamps, status, delays, booked/revenue/non-revenue passengers, block minutes, disruption events, primary cause, reactionary evidence; disclosure.
- Do not expose personal customer data.

### 10.4 DRL-Feedback

- Source: feedback table.
- Passed filter: `FactCustomerFeedback[FeedbackKey]`.
- Content: FeedbackID, airline, route, flight, type, satisfaction score, complaint category, service recovery, resolution status/date, channel; disclosure.
- No free text or PII.

### 10.5 Tooltip pages

Create report-page tooltips for: airline performance, route performance, flight disruption, and feedback summary. Each includes the exact disclosure in a persistent footer. Default tooltips are disabled.

## 11. Export, print, and screenshot behavior

- Export is disabled until the export template includes the exact disclosure and T-79 passes.
- PDF/print: footer disclosure on every page; page numbers; selected filters and period; no clipped disclosure.
- PowerPoint export: disclosure on every exported slide/page; do not rely on the report footer being cropped.
- Excel export: add a disclosure header/footer row to every exported table; if the export path cannot guarantee that, disable Excel export.
- Screenshots for the case study must show the disclosure; do not crop the footer.
- The export filename must include `synthetic` and the run ID; do not use an airline name that implies actual performance.

## 12. Accessibility and mobile specification

| Requirement | Implementation |
|---|---|
| Contrast | Text/background contrast at least 4.5:1 for body text; 3:1 for large text |
| Colour independence | Every colour-coded value has a label, sign, or icon |
| Alt text | Every visual has purpose-based alt text; decorative images omitted |
| Tab order | Header → filters → KPI cards → primary chart → secondary charts → table → footer |
| Keyboard | All slicers, buttons, and drill-through actions reachable by keyboard |
| Focus | Visible focus indicator; no focus trap |
| Text size | Minimum 11 px for labels/notes; 10 px only for axis ticks |
| Motion | No auto-play or flashing; no parallax |
| Mobile | 9:16 portrait; KPI cards stacked; one chart per row; filters collapsed; disclosure visible |
| Screen reader | Table titles and measure definitions available in a definitions panel |

## 13. Page acceptance criteria

| ID | Criterion | Evidence |
|---|---|---|
| DB-01 | Exactly five visible pages with the specified names | Page inventory |
| DB-02 | Every page carries the exact disclosure | T-79 screenshot |
| DB-03 | Every custom tooltip carries the disclosure | T-79 tooltip screenshot |
| DB-04 | KPI cards use the authoritative measures and formats | T-46 review |
| DB-05 | No unsupported severity/sentiment/service-category field | Model/report review |
| DB-06 | No fact-to-fact visual cross-filtering | Interaction review |
| DB-07 | Unit-revenue measures are not sliced by incompatible dimensions | Report review |
| DB-08 | Date roles are labelled (departure, arrival, travel, booking, feedback) | Visual review |
| DB-09 | Mobile layout preserves disclosure and key KPIs | Mobile screenshot |
| DB-10 | Export is disabled until T-79 passes | Export settings |
| DB-11 | No PBIX/PBIP or report claimed before creation | Repository inspection |

## 14. Open decisions and risks

- Formal OD-01A/OD-01B signatures and `G3-RV-01`.
- OD-02/OD-03 airport and fleet populations; OD-04 exchange rates; OD-05 capacity; OD-06 passenger revenue; OD-07 tax/fee; OD-08 refunds; OD-09 OTP; OD-10 availability; OD-11 satisfaction; OD-12 complaint rate; OD-13 classification; OD-14 allocation; OD-15 no separate revenue fact; OD-16 codeshare; OD-17 service recovery; OD-18 eligibility; OD-19 diversion; OD-20 tolerance; OD-21 targets; OD-22 lead time; OP-01 cohort complaint rate.
- No target lines or target variance until OD-21. Do not invent targets.
- Map visual availability/tenant policy is unverified; the fallback is required.
- Volume/performance at ~16M coupons is unproven; test before building all visuals.
- K-16/K-20 booking-level eligibility and “fully refunded” logic need an owner decision and possibly a helper table/measure.
- The report cannot claim T-79, T-37, T-42–T-46, or T-55 before a rendered report and runtime tests exist.
- No Git operation is authorized; report version evidence must use file hashes until Git is approved.

## 15. Verification checklist for this specification

| Check | Status |
|---|---|
| Five pages with business questions | DOCUMENTED |
| Layout, KPI cards, visuals, field wells | DOCUMENTED |
| Filters, interactions, drill-through | DOCUMENTED |
| Design system, colour, type, accessibility | DOCUMENTED |
| Mobile and export behavior | DOCUMENTED |
| Disclosure on pages/tooltips/exports | DOCUMENTED — T-79 BLOCKED |
| Unsupported fields excluded | DOCUMENTED |
| No report or dashboard created | VERIFIED BY ABSENCE |
| Report implementation authorization | NOT GRANTED |

**End of specification.** This document is design evidence only. It does not create a report, visual, dashboard, export, or gate advance.
