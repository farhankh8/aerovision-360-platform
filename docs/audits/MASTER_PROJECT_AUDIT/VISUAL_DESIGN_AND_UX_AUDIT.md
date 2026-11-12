# AEROVISION 360 — VISUAL DESIGN AND UX AUDIT

**Project:** AEROVISION 360 — Global Multi-Airline Operations, Revenue & Customer Intelligence Platform  
**Audit ID:** A360-MASTER-AUDIT-2026-11-08-VX  
**Audit Date:** 2026-11-08  
**Status:** READ-ONLY AUDIT — NO PROJECT FILES MODIFIED  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Design System Overview

The Power BI Dashboard Specification (`docs/POWER_BI_DASHBOARD_SPECIFICATION.md`) defines a comprehensive design system for the AEROVISION 360 report.

### 1.1 Canvas and Grid

| Element | Specification |
|---------|---------------|
| Canvas | 16:9, 1366 × 768 px |
| Safe margin | 16 px |
| Grid | 12 columns, 16 px gutter |
| Header | 64 px high |
| Navigation rail | 88 px wide, left side |
| Filter bar | 44 px high below header |
| Content area | Remaining height |
| Footer disclosure | 30 px high |

### 1.2 Color System

| Token | Hex | Use |
|-------|-----|-----|
| Ink | #102A43 | Primary text and titles |
| Secondary ink | #486581 | Labels and secondary text |
| Background | #F4F6F8 | Page background |
| Surface | #FFFFFF | Cards and tables |
| Border | #D9E2EC | Card and table borders |
| Brand teal | #0B7285 | Primary series, selected state |
| Informational blue | #1C7ED6 | Secondary series |
| Attention amber | #E67700 | Warning/exception, not failure |
| Negative red | #C92A2A | Negative contribution, cancellations, critical exception |
| Positive green | #2B8A3E | Positive contribution, completion, resolved recovery |
| Neutral grey | #829AB1 | Benchmark, unavailable, prior period |

**Rules:** No red/green as only encoding; pair with label/icon/sign; max 5 data colors per visual; no 3D, gradients for data, pies, or decorative images.

### 1.3 Typography

| Role | Font | Size | Weight |
|------|------|------|--------|
| Page title | Segoe UI Semibold | 22 px | 600 |
| KPI value | Segoe UI Semibold | 30 px | 600 |
| KPI label | Segoe UI | 11 px | 400 |
| Visual title | Segoe UI Semibold | 14 px | 600 |
| Axis/label | Segoe UI | 10–11 px | 400 |
| Body/note | Segoe UI | 11 px | 400 |
| Disclosure | Segoe UI Semibold | 11 px | 600 |

---

## 2. Page-by-Page Visual Inventory

### Page 01 — Executive Overview

| Visual ID | Visual Type | Measure(s) | Status in report.json | Status in PBIX |
|-----------|-------------|------------|----------------------|----------------|
| EX-01 | Card | FL01 | Defined | NOT BUILT |
| EX-02 | Card | FL02 | Defined | NOT BUILT |
| EX-03 | Card | FL03 | Defined | NOT BUILT |
| EX-04 | Card | FL04 | Defined | NOT IMPLEMENTED |
| EX-05 | Card | RV_TotalOperatingRevenueUSD | Defined | BLOCKED (OD-04) |
| EX-06 | Card | CX_TotalOperatingCostsUSD | Defined | BLOCKED (OD-04) |
| EX-07 | Card | RV_AvgRevenuePerRevenuePassenger | Defined | BLOCKED (OD-04) |
| EX-08 | Card | CX_CostPerRevenuePassengerUSD | Defined | BLOCKED (OD-04) |
| EX-09 | Line Chart | RV_TotalOperatingRevenueUSD, CX_TotalOperatingCostsUSD | Defined | BLOCKED (OD-04) |
| EX-10 | Horizontal Bar | CX_CostPerRevenuePassengerUSD | Defined | BLOCKED (OD-04) |
| EX-11 | Scatter Chart | RV_AvgRevenuePerRevenuePassenger, CX_CostPerRevenuePassengerUSD | Defined | BLOCKED (OD-04) |
| EX-12 | Table | AirlineName, Total RASK, CASK, Unit Contribution, OTP, Cancellation Rate, Complaint Rate, Satisfaction | Defined | BLOCKED (OD-04) |

**Total:** 12 visuals (8 cards, 1 line chart, 1 horizontal bar, 1 scatter chart, 1 table)

---

### Page 02 — Operations & Disruption

| Visual ID | Visual Type | Measure(s) | Category/Axis | Status |
|-----------|-------------|------------|---------------|--------|
| OP-01 | Card | FL04 (Cancellation Rate) | None | NOT IMPLEMENTED |
| OP-02 | Card | DS03 (Controllable Disruptions) | None | NOT IMPLEMENTED |
| OP-03 | Bar Chart | DS01 | Category: DisruptionName | NOT IMPLEMENTED |

**Total:** 3 visuals (2 cards, 1 bar chart)

---

### Page 03 — Revenue & Finance

| Visual ID | Visual Type | Measure(s) | Category/Axis | Status |
|-----------|-------------|------------|---------------|--------|
| RV-01 | Card | RV_TotalOperatingRevenueUSD | None | BLOCKED (OD-04) |
| RV-02 | Card | RV_NetPassengerRevenueUSD | None | BLOCKED (OD-04) |
| RV-03 | Card | RV_NetFeeRevenueUSD | None | BLOCKED (OD-04) |
| RV-04 | Card | RV_NetAncillaryRevenueUSD | None | BLOCKED (OD-04) |
| RV-05 | Card | CX_TotalOperatingCostsUSD | None | BLOCKED (OD-04) |
| RV-06 | Card | CX_NetOperatingContributionUSD | None | BLOCKED (OD-04) |
| RV-07 | Card | NC_RevenueToCostRatio | None | BLOCKED (OD-04) |
| RV-08 | Card | RV_TotalOperatingRevenueUSD | None | BLOCKED (OD-04) |
| RV-09 | Stacked Column/Line | RV_NetPassengerRevenueUSD, RV_NetFeeRevenueUSD, RV_NetAncillaryRevenueUSD | X: YearMonth | BLOCKED (OD-04) |
| RV-10 | Line Chart | RV_TotalOperatingRevenueUSD, CX_TotalOperatingCostsUSD | X: YearMonth | BLOCKED (OD-04) |
| RV-11 | Line Chart | RV_TotalOperatingRevenueUSD, CX_TotalOperatingCostsUSD | X: YearMonth | BLOCKED (OD-04) |
| RV-12 | Horizontal Bar | RV_TotalOperatingRevenueUSD | Category: FareClassName | BLOCKED (OD-04) |
| RV-13 | Horizontal Bar | RV_TotalOperatingRevenueUSD | Category: ChannelName | BLOCKED (OD-04) |
| RV-14 | Bar Chart | RV_AvgRevenuePerRevenuePassenger | Category: AirlineName | BLOCKED (OD-04) |
| RV-15 | Bar Chart | RV_AvgBookingValueUSD | Category: AirlineName | BLOCKED (OD-04) |
| RV-16 | Histogram/Column | Booking Lead Time | X: Lead-time bin | BLOCKED (OD-04) |
| RV-17 | Line/Column | RV_RevenueByBookingDateUSD | X: YearMonth | BLOCKED (OD-04) |
| RV-18 | Cards/Inputs | FareScenarioRevenue, FuelScenarioCost, CapacityScenarioASK | None | BLOCKED (OD-04) |

**Total:** 18 visuals — ALL BLOCKED by OD-04

---

### Page 04 — Operations & Disruption

| Visual ID | Visual Type | Measure(s) | Category/Axis | Status |
|-----------|-------------|------------|---------------|--------|
| OP-01 | Card | FL04 | None | NOT IMPLEMENTED |
| OP-02 | Card | DS03 | None | NOT IMPLEMENTED |
| OP-03 | Bar Chart | DS01 | Category: DisruptionName | NOT IMPLEMENTED |

**Total:** 3 visuals (2 cards, 1 bar chart)

---

### Page 05 — Customer & Service Intelligence

| Visual ID | Visual Type | Measure(s) | Category/Axis | Status |
|-----------|-------------|------------|---------------|--------|
| V01 | Card | CF01 | None | NOT IMPLEMENTED |
| V02 | Card | CF02 | None | NOT IMPLEMENTED |
| V03 | Card | CF03 | None | NOT IMPLEMENTED |
| V04 | Card | CF04 | None | NOT IMPLEMENTED |
| V05 | Card | CF09 | None | NOT IMPLEMENTED |
| V06 | Card | CF10 | None | NOT IMPLEMENTED |
| V07 | Card | CF11 | None | NOT IMPLEMENTED |
| V08 | Card | CF12 | None | NOT IMPLEMENTED |
| V09 | Card | CF13 | None | NOT IMPLEMENTED |
| V10 | Card | CF14 | None | NOT IMPLEMENTED |
| V11 | Bar Chart | CF01 | Category: FeedbackChannel | NOT IMPLEMENTED |
| V12 | Bar Chart | CF01 | Category: FeedbackType | NOT IMPLEMENTED |
| V13 | Bar Chart | CF02 | Category: AirlineName | NOT IMPLEMENTED |
| V14 | Bar Chart | CF01 | Category: ResolutionStatus | NOT IMPLEMENTED |
| V15 | Bar Chart | CF05 | Category: ComplaintCategory | NOT IMPLEMENTED |
| V16 | Bar Chart | COUNTROWS(dim_customer) | Category: CustomerSegment | NOT IMPLEMENTED |

**Total:** 16 visuals (10 cards, 6 bar charts)

---

## 3. Slicers

| Slicer ID | Table | Column | Pages | Status |
|-----------|-------|--------|-------|--------|
| S01 | dim_airline | AirlineName | All | NOT IMPLEMENTED |
| S02 | dim_date | FullDate | All | NOT IMPLEMENTED |
| S03 | dim_route | RouteRegion | All | NOT IMPLEMENTED |
| S04 | dim_airport | AirportCode (Origin/Destination) | Network, Operations | NOT IMPLEMENTED |
| S05 | dim_fare_class | FareClassCode | Revenue | NOT IMPLEMENTED |
| S06 | dim_booking_channel | ChannelName | Revenue, Customer | NOT IMPLEMENTED |
| S07 | fact_customer_feedback | FeedbackType | Customer | NOT IMPLEMENTED |
| S08 | dim_disruption_type | DisruptionName | Operations | NOT IMPLEMENTED |
| S09 | dim_aircraft_type | AircraftType | Network, Operations | NOT IMPLEMENTED |

**Total:** 9 slicers — all NOT IMPLEMENTED

---

## 4. Design Compliance Issues

| Issue ID | Severity | Description | Impact |
|----------|----------|-------------|--------|
| VX-01 | HIGH | No explicit visual titles in report.json | All visuals lack titles |
| VX-02 | HIGH | No explicit number formatting in report.json | All measures use default formatting |
| VX-03 | HIGH | No custom tooltips defined | All visuals use default tooltips (no disclosure) |
| VX-04 | MEDIUM | No slicers defined in report.json | All 9 slicers missing |
| VX-05 | MEDIUM | No drill-through configured | 4 drill-through pages (DRL-Airline, DRL-Route, DRL-Flight, DRL-Feedback) not implemented |
| VX-06 | MEDIUM | No bookmarks defined | Reset filters, Definitions, Scenario assumptions, Data notes bookmarks missing |
| VX-07 | LOW | No mobile layout defined | No 9:16 portrait layout specified |
| VX-08 | LOW | No accessibility features defined | No alt text, keyboard navigation, or screen reader support |

---

## 5. Conclusion

All 16 visuals across 5 pages are **NOT IMPLEMENTED in Power BI Desktop**. The report.json defines all visual configurations, but the PBIX contains only one blank page. Additionally:

1. 18 visuals on Page 03 are blocked by OD-04
2. 6 visuals (V05, V06, V09, V10, V15, V16) do not exist in report.json and need to be created
3. No explicit titles, formatting, tooltips, or slicers defined
4. No drill-through, bookmarks, or mobile layout defined
5. No accessibility features implemented

**Recommendation:** Build all 5 pages in Power BI Desktop from report.json, starting with Page 01 (Executive Overview) which has no OD-04 blocked measures.
