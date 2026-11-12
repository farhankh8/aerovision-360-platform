# AEROVISION 360 — DAX KPI Catalogue

**Status:** ENGINEERING PREPARATION — DESIGNED, NOT EXECUTED; NO DAX MEASURE CREATED
**Version:** 0.1
**Prepared:** 2026-11-02
**Governing contract:** `docs/03_DATA_CONTRACTS.md` version 1.5, Section 11
**Companion documents:** `POWER_BI_SEMANTIC_MODEL_BLUEPRINT.md`, `POWER_QUERY_IMPLEMENTATION_BLUEPRINT.md`
**Project root:** `C:\Users\KHfar\OneDrive\Desktop\AEROVISION_360`

> **Status notice.** This catalogue contains proposed DAX formulas. No measure has been created, executed, or validated in Power BI. No semantic model or report exists. The authoritative 21-KPI list is K-01 through K-21 in contract Section 11; this document does not replace or silently expand that list. OD-01A/OD-01B, `G3-RV-01`, G3, and G4 remain pending or blocked as recorded.

**Canonical disclosure:** `Synthetic Simulation — Not Actual Airline Performance`

## 1. KPI conventions

- All financial measures use USD columns. Never aggregate original currencies or convert currency in DAX.
- Every ratio uses `DIVIDE(numerator, denominator, BLANK())` or equivalent. Zero/missing denominator returns BLANK, not zero or infinity.
- Percentages are stored as decimal fractions; format as percent in the report.
- Ratios are measures, not additive fact columns. Do not sum a ratio across airlines, routes, or months.
- Revenue is held only in `FactBookingTransactions`. There is no separate `FactRevenue`.
- Flight-level capacity and traffic use `FactFlightOperations`; booking-level revenue uses `FactBookingTransactions`. Do not multiply a booking row by flight rows.
- Booking-level metrics (`K-16`, `K-20`) must summarize to one row per `BookingReference` before calculating; do not average coupon rows.
- Each KPI declares its date role. Default roles are in contract Section 9.4.
- The 15-minute OTP threshold, 1–5 satisfaction scale, 14.00 available hours, complaint-rate denominator, allocation, and eligibility rules remain open decisions where noted.
- A KPI with a policy dependency is still design-complete, but it is not approved for implementation until the dependency is formally closed. `K-16` and `K-20` require a booking-eligibility helper design because no persisted “fully refunded” flag exists.

## 2. Base measures

These are proposed internal measures. Names may be adjusted; definitions must not change without change control.

```DAX
Net Passenger Revenue USD =
SUM ( FactBookingTransactions[NetPassengerRevenueUSD] )

Net Fee Revenue USD =
SUM ( FactBookingTransactions[NetFeeRevenueUSD] )

Net Ancillary Revenue USD =
SUM ( FactBookingTransactions[NetAncillaryRevenueUSD] )

Total Operating Revenue USD =
[Net Passenger Revenue USD] + [Net Fee Revenue USD] + [Net Ancillary Revenue USD]

Operating Cost USD =
SUM ( FactOperatingCosts[CostAmountUSD] )

ASK =
SUMX (
    FactFlightOperations,
    FactFlightOperations[AvailableSeats] * FactFlightOperations[FlightDistanceKM]
)

RPK =
SUMX (
    FactFlightOperations,
    FactFlightOperations[RevenuePassengers] * FactFlightOperations[FlightDistanceKM]
)

Revenue Passengers =
SUM ( FactFlightOperations[RevenuePassengers] )

Available Seats =
SUM ( FactFlightOperations[AvailableSeats] )

Scheduled Flights =
COUNTROWS ( FactFlightOperations )

Cancelled Flights =
CALCULATE (
    COUNTROWS ( FactFlightOperations ),
    FactFlightOperations[CancellationFlag] = TRUE
)

Operated Flights =
CALCULATE (
    COUNTROWS ( FactFlightOperations ),
    FactFlightOperations[CompletionFlag] = TRUE
)

On Time Departures =
CALCULATE (
    COUNTROWS ( FactFlightOperations ),
    FactFlightOperations[CompletionFlag] = TRUE,
    FactFlightOperations[OnTimeFlag] = TRUE
)

Operated Flights With Valid Departure =
CALCULATE (
    COUNTROWS ( FactFlightOperations ),
    FactFlightOperations[CompletionFlag] = TRUE,
    NOT ISBLANK ( FactFlightOperations[DepartureDelayMinutes] )
)

On Time Arrivals =
CALCULATE (
    COUNTROWS ( FactFlightOperations ),
    FactFlightOperations[CompletionFlag] = TRUE,
    FactFlightOperations[OnTimeArrivalFlag] = TRUE
)

Operated Flights With Valid Arrival =
CALCULATE (
    COUNTROWS ( FactFlightOperations ),
    FactFlightOperations[CompletionFlag] = TRUE,
    NOT ISBLANK ( FactFlightOperations[ArrivalDelayMinutes] )
)

Operating Block Hours =
SUMX (
    FILTER (
        FactFlightOperations,
        FactFlightOperations[CompletionFlag] = TRUE
    ),
    DIVIDE ( FactFlightOperations[BlockMinutes], 60 )
)

Available Aircraft Hours =
CALCULATE (
    SUM ( RefAircraftAvailability[AvailableHours] ),
    RefAircraftAvailability[AvailabilityStatus] = "Available",
    RefAircraftAvailability[ReferenceVersion] =
        SELECTEDVALUE ( _SelectedReferenceVersion[ReferenceVersion] ),
    TREATAS ( VALUES ( DimAirline[AirlineKey] ), DimAircraft[AirlineKey] )
)

Complaint Events =
CALCULATE (
    COUNTROWS ( FactCustomerFeedback ),
    FactCustomerFeedback[FeedbackType] = "Complaint"
)

Feedback Volume =
COUNTROWS ( FactCustomerFeedback )

Satisfaction Score Sum =
SUM ( FactCustomerFeedback[SatisfactionScore] )

Satisfaction Responses =
COUNT ( FactCustomerFeedback[SatisfactionScore] )
```

**Note on `Available Aircraft Hours`:** `TREATAS` transfers the airline filter to `DimAircraft` without activating a second `DimAirline`→`DimAircraft` path. The measure must be tested with and without an airline filter, and with a date filter. It must not multiply flight rows. If the model uses a different approved fleet-role design, this measure must be revised with evidence.

## 3. The 21 required KPIs

### K-01 — ASK (Available Seat Kilometres)

- **Business purpose:** measure scheduled capacity offered.
- **Exact definition:** sum of available seats multiplied by scheduled flight distance for every scheduled leg.
- **Numerator/components:** `AvailableSeats × FlightDistanceKM` for every scheduled leg.
- **Denominator:** not applicable; volume measure.
- **Source tables/columns:** `FactFlightOperations[AvailableSeats]`, `FlightDistanceKM`.
- **Calculation grain:** flight leg.
- **DAX proposal:** `ASK` in Section 2.
- **Format:** `#,##0`.
- **Aggregation:** additive across flight legs; not a ratio.
- **Filter context:** default flight date role = `ScheduledDepartureDateKey`; includes cancelled flights; excludes duplicate legs, non-scheduled rows, zero-distance rows.
- **Edge cases:** zero rows returns 0 (volume measure); cancelled capacity remains included; operated-only variant must be labeled `Operated ASK`.
- **Validation:** T-28 independent recalculation within 0.1%.
- **Related dashboard:** Executive Overview; Network & Capacity Intelligence.
- **Business interpretation:** how much seat capacity the network offered, regardless of whether it was used.
- **Decision status:** design complete; capacity policy OD-05 affects interpretation of cancelled capacity.

### K-02 — RPK (Revenue Passenger Kilometres)

- **Business purpose:** measure revenue passenger traffic carried.
- **Exact definition:** sum of revenue passengers multiplied by scheduled flight distance.
- **Numerator/components:** `RevenuePassengers × FlightDistanceKM`.
- **Denominator:** not applicable; volume measure.
- **Source tables/columns:** `FactFlightOperations[RevenuePassengers]`, `FlightDistanceKM`.
- **Calculation grain:** flight leg.
- **DAX proposal:** `RPK` in Section 2.
- **Format:** `#,##0`.
- **Aggregation:** additive across operated flight legs; cancelled flights contribute zero.
- **Filter context:** default flight date role; non-revenue passengers excluded; cancelled flights zero.
- **Edge cases:** a revenue passenger on a cancelled leg must not be counted; no negative values.
- **Validation:** T-29 independent recalculation within 0.1%.
- **Related dashboard:** Executive Overview; Network & Capacity Intelligence.
- **Business interpretation:** revenue traffic carried; the numerator of load factor and the denominator of passenger yield.
- **Decision status:** design complete; revenue-passenger reconciliation OD-20 pending.

### K-03 — Load Factor

- **Business purpose:** measure how much scheduled capacity is used by revenue traffic.
- **Exact definition:** `RPK / ASK`.
- **Numerator:** RPK.
- **Denominator:** ASK, including cancelled flights.
- **Source tables/columns:** `FactFlightOperations`.
- **Calculation grain:** flight leg rolled to the selected context.
- **DAX proposal:**
```DAX
Load Factor = DIVIDE ( [RPK], [ASK], BLANK() )
```
- **Format:** `0.0%`.
- **Aggregation:** non-additive ratio; recalculate at the selected context.
- **Filter context:** default flight date role; non-revenue passengers excluded; cancelled capacity included.
- **Edge cases:** zero ASK returns BLANK; do not substitute operated ASK unless explicitly labeled.
- **Validation:** T-30 within 0.01 percentage point of independent RPK/ASK.
- **Related dashboard:** Executive Overview; Network & Capacity Intelligence.
- **Business interpretation:** percentage of offered seat-kilometres used by paying traffic.
- **Decision status:** design complete; OD-05 capacity treatment pending.

### K-04 — Passenger Yield

- **Business purpose:** measure passenger revenue per revenue passenger kilometre.
- **Exact definition:** `NetPassengerRevenueUSD / RPK`.
- **Numerator:** net passenger revenue in USD.
- **Denominator:** RPK.
- **Source tables/columns:** `FactBookingTransactions[NetPassengerRevenueUSD]`; `FactFlightOperations[RevenuePassengers]`, `FlightDistanceKM`.
- **Calculation grain:** shared airline/route/date context; revenue at coupon grain, traffic at flight grain.
- **DAX proposal:**
```DAX
Passenger Yield =
DIVIDE ( [Net Passenger Revenue USD], [RPK], BLANK() )
```
- **Format:** `$0.0000`.
- **Aggregation:** non-additive ratio; recalculate at context.
- **Filter context:** default travel-date revenue role and flight date role; excludes taxes, fees, ancillary, non-revenue passengers, cancelled/no-show passenger revenue; refunds netted.
- **Edge cases:** zero RPK returns BLANK; do not slice by fare class or channel without a compatible RPK denominator, because flight traffic is not split by those dimensions. Use average fare or revenue mix for those slices instead.
- **Validation:** T-31 revenue control plus T-29 RPK; T-39 rollups.
- **Related dashboard:** Revenue & Yield Intelligence.
- **Business interpretation:** average passenger revenue earned per revenue passenger kilometre.
- **Decision status:** design complete; OD-06 passenger revenue and OD-08 refunds pending.

### K-05 — Passenger RASK

- **Business purpose:** measure passenger revenue per available seat kilometre.
- **Exact definition:** `NetPassengerRevenueUSD / ASK`.
- **Numerator:** net passenger revenue in USD.
- **Denominator:** ASK, including cancelled flights.
- **Source tables/columns:** `FactBookingTransactions`, `FactFlightOperations`.
- **Calculation grain:** shared context.
- **DAX proposal:**
```DAX
Passenger RASK =
DIVIDE ( [Net Passenger Revenue USD], [ASK], BLANK() )
```
- **Format:** `$0.0000`.
- **Aggregation:** non-additive ratio.
- **Filter context:** travel-date revenue; flight capacity; excludes tax, fees, ancillary, non-revenue passengers; refunds netted.
- **Edge cases:** zero ASK returns BLANK; cancelled capacity remains in ASK.
- **Validation:** T-31, T-28, T-39.
- **Related dashboard:** Revenue & Yield Intelligence; Executive Overview.
- **Business interpretation:** passenger revenue generated per unit of offered capacity.
- **Decision status:** design complete; OD-05/OD-06/OD-08 pending.

### K-06 — Total RASK

- **Business purpose:** measure total airline-retained operating revenue per available seat kilometre.
- **Exact definition:** `TotalOperatingRevenueUSD / ASK`.
- **Numerator:** net passenger revenue + net fee revenue + net ancillary revenue.
- **Denominator:** ASK, including cancelled flights.
- **Source tables/columns:** `FactBookingTransactions` USD columns; `FactFlightOperations`.
- **Calculation grain:** shared context.
- **DAX proposal:**
```DAX
Total RASK =
DIVIDE ( [Total Operating Revenue USD], [ASK], BLANK() )
```
- **Format:** `$0.0000`.
- **Aggregation:** non-additive ratio.
- **Filter context:** travel-date revenue; excludes taxes, pass-through amounts, non-operating income, FX gains.
- **Edge cases:** zero ASK returns BLANK; do not mix currencies.
- **Validation:** T-32, T-28, T-39.
- **Related dashboard:** Executive Overview; Revenue & Yield Intelligence.
- **Business interpretation:** total operating revenue per unit of capacity, including fees and ancillary.
- **Decision status:** design complete; OD-07/OD-08 pending.

### K-07 — CASK

- **Business purpose:** measure operating cost per available seat kilometre.
- **Exact definition:** `OperatingCostUSD / ASK`.
- **Numerator:** sum of operating-cost ledger lines in USD.
- **Denominator:** ASK, including cancelled flights.
- **Source tables/columns:** `FactOperatingCosts[CostAmountUSD]`; `FactFlightOperations`.
- **Calculation grain:** shared context.
- **DAX proposal:**
```DAX
CASK =
DIVIDE ( [Operating Cost USD], [ASK], BLANK() )
```
- **Format:** `$0.0000`.
- **Aggregation:** non-additive ratio.
- **Filter context:** cost date role; includes Fuel, Crew, Maintenance, Airport Charges, Navigation, Sales and Distribution, Overhead, Other; excludes non-operating costs, interest, tax, impairments, FX.
- **Edge cases:** zero ASK returns BLANK; negative credits remain signed; do not hide negative values.
- **Validation:** T-33, T-26, T-28, T-39.
- **Related dashboard:** Executive Overview; Revenue & Yield Intelligence; Network & Capacity Intelligence.
- **Business interpretation:** operating cost required per unit of offered capacity.
- **Decision status:** design complete; OD-13 classification and cost policy pending.

### K-08 — Unit Contribution

- **Business purpose:** measure operating contribution per available seat kilometre.
- **Exact definition:** `(TotalOperatingRevenueUSD − OperatingCostUSD) / ASK`, equivalent to `Total RASK − CASK`.
- **Numerator:** total operating revenue minus operating cost.
- **Denominator:** ASK, including cancelled flights.
- **Source tables/columns:** `FactBookingTransactions`, `FactOperatingCosts`, `FactFlightOperations`.
- **Calculation grain:** shared context.
- **DAX proposal:**
```DAX
Unit Contribution =
DIVIDE ( [Total Operating Revenue USD] - [Operating Cost USD], [ASK], BLANK() )
```
or `[Total RASK] - [CASK]` with blank-safe handling.
- **Format:** `$0.0000`.
- **Aggregation:** non-additive ratio; negative is valid.
- **Filter context:** same revenue/cost definitions; excludes non-operating items.
- **Edge cases:** zero ASK returns BLANK; do not clamp negative contribution to zero; if both revenue and cost are blank, return BLANK.
- **Validation:** T-33, T-32, T-39.
- **Related dashboard:** Executive Overview; Revenue & Yield Intelligence.
- **Business interpretation:** operating profit contribution per unit of capacity before non-operating items.
- **Decision status:** design complete; OD-06/OD-07/OD-08/OD-13 pending.

### K-09 — On-Time Performance (OTP)

- **Business purpose:** measure the share of operated departures within the on-time threshold.
- **Exact definition:** `OnTimeDepartures / OperatedFlightsWithValidDeparture`.
- **Numerator:** operated flights with `OnTimeFlag = TRUE`.
- **Denominator:** operated flights with a non-null departure delay.
- **Source tables/columns:** `FactFlightOperations[CompletionFlag]`, `[OnTimeFlag]`, `[DepartureDelayMinutes]`.
- **Calculation grain:** flight leg.
- **DAX proposal:**
```DAX
On Time Performance =
DIVIDE ( [On Time Departures], [Operated Flights With Valid Departure], BLANK() )
```
- **Format:** `0.0%`.
- **Aggregation:** non-additive ratio.
- **Filter context:** departure date role; cancelled flights excluded from denominator and reported via cancellation rate; early departures count as on time.
- **Edge cases:** zero valid departures returns BLANK; a missing actual departure is not on time and is excluded from the valid-departure denominator; label departure vs arrival basis.
- **Validation:** T-34, T-37.
- **Related dashboard:** Operations & Disruption; Executive Overview.
- **Business interpretation:** percentage of operated departures that were within 15 minutes of schedule.
- **Decision status:** OD-09 15-minute threshold and departure basis are proposed; formal approval required.

### K-10 — Cancellation Rate

- **Business purpose:** measure the share of scheduled flights cancelled.
- **Exact definition:** `CancelledFlights / ScheduledFlights`.
- **Numerator:** flights with `CancellationFlag = TRUE`.
- **Denominator:** all scheduled flight legs, including cancelled.
- **Source tables/columns:** `FactFlightOperations[CancellationFlag]`.
- **Calculation grain:** flight leg.
- **DAX proposal:**
```DAX
Cancellation Rate =
DIVIDE ( [Cancelled Flights], [Scheduled Flights], BLANK() )
```
- **Format:** `0.0%`.
- **Aggregation:** non-additive ratio.
- **Filter context:** departure date role; do not exclude cancelled flights from the denominator.
- **Edge cases:** zero scheduled flights returns BLANK; duplicate legs must be excluded before counting.
- **Validation:** T-34, T-17.
- **Related dashboard:** Operations & Disruption; Executive Overview.
- **Business interpretation:** percentage of scheduled flights that did not operate.
- **Decision status:** design complete; OD-19 diversion treatment pending.

### K-11 — Completion Rate

- **Business purpose:** measure the share of scheduled flights operated.
- **Exact definition:** `OperatedFlights / ScheduledFlights`.
- **Numerator:** flights with `CompletionFlag = TRUE`.
- **Denominator:** all scheduled flight legs, including cancelled.
- **Source tables/columns:** `FactFlightOperations[CompletionFlag]`.
- **Calculation grain:** flight leg.
- **DAX proposal:**
```DAX
Completion Rate =
DIVIDE ( [Operated Flights], [Scheduled Flights], BLANK() )
```
- **Format:** `0.0%`.
- **Aggregation:** non-additive ratio.
- **Filter context:** departure date role; cancelled flights remain in denominator.
- **Edge cases:** zero scheduled flights returns BLANK; completion + cancellation = 1 in the baseline.
- **Validation:** T-34, T-17.
- **Related dashboard:** Operations & Disruption.
- **Business interpretation:** percentage of scheduled flights completed.
- **Decision status:** design complete; OD-19 pending.

### K-12 — Average Delay

- **Business purpose:** measure average arrival delay per operated flight with a valid arrival delay.
- **Exact definition:** `SUM(ArrivalDelayMinutes) / OperatedFlightsWithValidArrival`.
- **Numerator:** sum of arrival delay minutes for eligible operated flights.
- **Denominator:** count of operated flights with non-null arrival delay.
- **Source tables/columns:** `FactFlightOperations[ArrivalDelayMinutes]`, `[CompletionFlag]`.
- **Calculation grain:** flight leg.
- **DAX proposal:**
```DAX
Average Arrival Delay =
DIVIDE (
    CALCULATE (
        SUM ( FactFlightOperations[ArrivalDelayMinutes] ),
        FactFlightOperations[CompletionFlag] = TRUE
    ),
    [Operated Flights With Valid Arrival],
    BLANK()
)
```
- **Format:** `0.0 min`.
- **Aggregation:** non-additive average; early arrivals produce negative delay and remain.
- **Filter context:** arrival date role via `USERELATIONSHIP` if the page uses arrival date; default departure date otherwise; cancelled flights excluded and reported separately.
- **Edge cases:** zero eligible flights returns BLANK; do not treat missing delay as zero.
- **Validation:** T-35.
- **Related dashboard:** Operations & Disruption.
- **Business interpretation:** typical arrival delay among flights with a valid measurement.
- **Decision status:** design complete; delay attribution OD-09/OD-13 pending.

### K-13 — Aircraft Utilization

- **Business purpose:** measure operating block hours per available aircraft hour.
- **Exact definition:** `OperatingBlockHours / AvailableAircraftHours`.
- **Numerator:** sum of `BlockMinutes / 60` for operated flights.
- **Denominator:** sum of `AvailableHours` from `ref_aircraft_availability.csv` for `AvailabilityStatus = Available`, active aircraft-days, selected `ReferenceVersion`.
- **Source tables/columns:** `FactFlightOperations[BlockMinutes]`; `RefAircraftAvailability[AvailableHours]`, `[AvailabilityStatus]`, `[ReferenceVersion]`; `DimAircraft`, `DimDate`.
- **Calculation grain:** flight/aircraft-day context; denominator at aircraft-day.
- **DAX proposal:**
```DAX
Aircraft Utilization =
DIVIDE ( [Operating Block Hours], [Available Aircraft Hours], BLANK() )
```
- **Format:** `0.00`.
- **Aggregation:** non-additive ratio.
- **Filter context:** only `Available` records contribute; `Maintenance`, `Stored`, `Retired`, and `No Planned Availability` excluded; cancelled flights excluded from block hours; selected version only.
- **Edge cases:** zero available hours returns BLANK; the 14.00-hour baseline is OD-10 proposed; no double counting with scheduled block hours.
- **Validation:** T-35, T-60, T-56–T-59.
- **Related dashboard:** Operations & Disruption; Network & Capacity Intelligence.
- **Business interpretation:** how intensively available aircraft hours were used by operated flying.
- **Decision status:** OD-10 availability assumption is proposed; formal approval required.

### K-14 — Average Passenger Revenue

- **Business purpose:** measure average net passenger revenue per revenue passenger.
- **Exact definition:** `NetPassengerRevenueUSD / RevenuePassengers`.
- **Numerator:** net passenger revenue in USD.
- **Denominator:** revenue passengers carried.
- **Source tables/columns:** `FactBookingTransactions[NetPassengerRevenueUSD]`; `FactFlightOperations[RevenuePassengers]`.
- **Calculation grain:** shared context; flight passenger denominator, coupon revenue numerator.
- **DAX proposal:**
```DAX
Average Passenger Revenue =
DIVIDE ( [Net Passenger Revenue USD], [Revenue Passengers], BLANK() )
```
- **Format:** `$#,##0.00`.
- **Aggregation:** non-additive average.
- **Filter context:** excludes non-revenue passengers, taxes, fees, ancillary, cancelled/no-show passenger revenue; refunds netted.
- **Edge cases:** zero revenue passengers returns BLANK; do not slice by fare class/channel because the flight denominator is not split by those dimensions.
- **Validation:** T-36, T-31, T-39.
- **Related dashboard:** Revenue & Yield Intelligence.
- **Business interpretation:** average passenger revenue per paying passenger carried.
- **Decision status:** design complete; OD-06/OD-08 pending.

### K-15 — Ancillary Revenue per Passenger

- **Business purpose:** measure average net ancillary revenue per revenue passenger.
- **Exact definition:** `NetAncillaryRevenueUSD / RevenuePassengers`.
- **Numerator:** net ancillary revenue in USD.
- **Denominator:** revenue passengers carried.
- **Source tables/columns:** `FactBookingTransactions[NetAncillaryRevenueUSD]`; `FactFlightOperations[RevenuePassengers]`.
- **Calculation grain:** shared context.
- **DAX proposal:**
```DAX
Ancillary Revenue per Passenger =
DIVIDE ( [Net Ancillary Revenue USD], [Revenue Passengers], BLANK() )
```
- **Format:** `$#,##0.00`.
- **Aggregation:** non-additive average.
- **Filter context:** excludes non-revenue passengers, taxes, fees, and passenger fare; ancillary refunds netted.
- **Edge cases:** zero revenue passengers returns BLANK; ancillary refunds reduce, not increase.
- **Validation:** T-36, T-32, T-39.
- **Related dashboard:** Revenue & Yield Intelligence; Customer & Service Intelligence.
- **Business interpretation:** average ancillary revenue earned per paying passenger.
- **Decision status:** design complete; OD-07/OD-08 pending.

### K-16 — Booking Lead Time

- **Business purpose:** measure average days between booking and travel at booking grain.
- **Exact definition:** `SUM(EligibleBookingLeadTimeDays) / EligibleBookings`, one row per eligible `BookingReference`.
- **Numerator:** sum of lead-time days for eligible bookings.
- **Denominator:** count of eligible bookings.
- **Source tables/columns:** `FactBookingTransactions[BookingReference]`, `[BookingLeadTimeDays]`, `[BookingDateKey]`, `[TravelDateKey]`, `[TransactionStatus]`, `[IsRevenuePassenger]`, `[IsRefunded]`.
- **Calculation grain:** booking, not coupon.
- **DAX proposal:**
```DAX
Booking Lead Time =
VAR BookingRows =
    CALCULATETABLE (
        ADDCOLUMNS (
            SUMMARIZE (
                FactBookingTransactions,
                FactBookingTransactions[BookingReference]
            ),
            "@Lead", CALCULATE ( MIN ( FactBookingTransactions[BookingLeadTimeDays] ) ),
            "@Coupons", CALCULATE ( COUNTROWS ( FactBookingTransactions ) ),
            "@EligibleCoupons",
                CALCULATE (
                    COUNTROWS ( FactBookingTransactions ),
                    FactBookingTransactions[TransactionStatus] IN { "Ticketed", "Flown" }
                ),
            "@RefundedCoupons",
                CALCULATE (
                    COUNTROWS ( FactBookingTransactions ),
                    FactBookingTransactions[IsRefunded] = TRUE
                )
        ),
        USERELATIONSHIP ( FactBookingTransactions[BookingDateKey], DimDate[DateKey] )
    )
VAR Eligible =
    FILTER (
        BookingRows,
        [@Lead] >= 0
            && [@EligibleCoupons] > 0
            && [@RefundedCoupons] < [@Coupons]
    )
RETURN
    DIVIDE ( SUMX ( Eligible, [@Lead] ), COUNTROWS ( Eligible ), BLANK() )
```
- **Format:** `0.0 days`.
- **Aggregation:** non-additive average; booking-level denominator.
- **Filter context:** booking-date period via `USERELATIONSHIP` on `FactBookingTransactions[BookingDateKey]`; negative lead times excluded and reported as defects; cancelled and fully refunded bookings excluded under proposed OD-18; booking date must be in period.
- **Edge cases:** zero eligible bookings returns BLANK; no 365-day cap while OD-22 is open; multi-segment bookings count once.
- **Validation:** T-36, T-47, T-22, T-37.
- **Related dashboard:** Revenue & Yield Intelligence; Customer & Service Intelligence.
- **Business interpretation:** how far in advance customers book; a demand-planning and revenue-management indicator.
- **Decision status:** **OWNER DECISION REQUIRED** — OD-18 eligibility and OD-22 lead-time policy are open, and no persisted “fully refunded” flag exists. The DAX above is a proposal, not an approved definition.

### K-17 — Refund Rate

- **Business purpose:** measure the share of eligible ticket coupons that were refunded.
- **Exact definition:** `RefundedEligibleCoupons / EligibleCoupons`.
- **Numerator:** eligible ticketed revenue coupons with `IsRefunded = TRUE`.
- **Denominator:** eligible ticketed revenue coupons issued in the period.
- **Source tables/columns:** `FactBookingTransactions[IsRevenuePassenger]`, `[IsRefunded]`, `[TransactionStatus]`, `[BookingDateKey]`.
- **Calculation grain:** coupon.
- **DAX proposal:**
```DAX
Refund Rate =
VAR Eligible =
    CALCULATETABLE (
        FILTER (
            FactBookingTransactions,
            FactBookingTransactions[IsRevenuePassenger] = TRUE
                && FactBookingTransactions[TransactionStatus] IN { "Ticketed", "Flown", "Refunded" }
        ),
        USERELATIONSHIP ( FactBookingTransactions[BookingDateKey], DimDate[DateKey] )
    )
VAR Refunded =
    FILTER ( Eligible, [IsRefunded] = TRUE )
RETURN
    DIVIDE ( COUNTROWS ( Refunded ), COUNTROWS ( Eligible ), BLANK() )
```
- **Format:** `0.0%`.
- **Aggregation:** non-additive ratio.
- **Filter context:** booking-date period via `USERELATIONSHIP` on `FactBookingTransactions[BookingDateKey]`; excludes non-revenue, duplicate, unticketed, and out-of-period coupons; refunded coupons remain in denominator.
- **Edge cases:** zero eligible coupons returns BLANK; a refunded coupon remains in the denominator; a cancelled unticketed coupon is excluded; do not count the same refund twice.
- **Validation:** T-36, T-20, T-31.
- **Related dashboard:** Customer & Service Intelligence; Revenue & Yield Intelligence.
- **Business interpretation:** how often eligible ticket coupons were refunded.
- **Decision status:** design complete; OD-08 refund treatment and OD-18 eligibility interpretation pending. Confirm whether Cancelled/NoShow coupons belong in the denominator before implementation.

### K-18 — Period Complaint Rate

- **Business purpose:** measure complaints per 1,000 revenue passengers in the same period.
- **Exact definition:** `(ComplaintEvents / RevenuePassengers) × 1000`.
- **Numerator:** feedback events with `FeedbackType = Complaint` by `FeedbackDateKey`.
- **Denominator:** revenue passengers carried by `ScheduledDepartureDateKey` in the same period.
- **Source tables/columns:** `FactCustomerFeedback[FeedbackType]`, `[FeedbackDateKey]`; `FactFlightOperations[RevenuePassengers]`, `[ScheduledDepartureDateKey]`.
- **Calculation grain:** period-level ratio; numerator feedback event, denominator flight passenger.
- **DAX proposal:**
```DAX
Period Complaint Rate =
DIVIDE ( [Complaint Events], [Revenue Passengers], BLANK() ) * 1000
```
- **Format:** `0.00 per 1,000`.
- **Aggregation:** non-additive ratio; period-level, not cohort-matched.
- **Filter context:** complaint date role = feedback; passenger date role = flight departure; both within the same period; excludes compliments, surveys, claims; duplicates removed upstream.
- **Edge cases:** zero passengers returns BLANK; do not mix a feedback-date numerator with a travel-date denominator outside the same period; do not use cohort complaint rate (OP-01) under this name.
- **Validation:** T-49, T-36, T-37.
- **Related dashboard:** Customer & Service Intelligence; Executive Overview.
- **Business interpretation:** complaint volume normalized by passenger traffic in the period.
- **Decision status:** OD-12 denominator is proposed; formal approval required.

### K-19 — Satisfaction

- **Business purpose:** measure average valid customer satisfaction score.
- **Exact definition:** `SUM(ValidSatisfactionScore) / Count(ValidSatisfactionScore)`.
- **Numerator:** sum of valid scores.
- **Denominator:** count of valid scores.
- **Source tables/columns:** `FactCustomerFeedback[SatisfactionScore]`.
- **Calculation grain:** feedback event.
- **DAX proposal:**
```DAX
Satisfaction =
DIVIDE ( [Satisfaction Score Sum], [Satisfaction Responses], BLANK() )
```
- **Format:** `0.00`.
- **Aggregation:** non-additive average; report response count with the average.
- **Filter context:** feedback date; scale 1–5; null/out-of-range/non-score feedback excluded.
- **Edge cases:** zero valid responses returns BLANK; a small base must be visible; do not treat null as zero.
- **Validation:** T-36, T-37.
- **Related dashboard:** Customer & Service Intelligence.
- **Business interpretation:** average satisfaction among customers who provided a valid score.
- **Decision status:** OD-11 1–5 scale is proposed; formal approval required.

### K-20 — Repeat Booking Rate

- **Business purpose:** measure the share of customers with two or more eligible bookings.
- **Exact definition:** `CustomersWithTwoOrMoreBookings / CustomersWithAtLeastOneBooking`.
- **Numerator:** distinct customers with at least two distinct eligible `BookingReference` values in the period.
- **Denominator:** distinct customers with at least one eligible `BookingReference` in the period.
- **Source tables/columns:** `FactBookingTransactions[CustomerKey]`, `[BookingReference]`, `[BookingDateKey]`, `[TransactionStatus]`, `[IsRefunded]`.
- **Calculation grain:** customer-booking.
- **DAX proposal:**
```DAX
Repeat Booking Rate =
VAR BookingRows =
    CALCULATETABLE (
        ADDCOLUMNS (
            SUMMARIZE (
                FactBookingTransactions,
                FactBookingTransactions[BookingReference],
                FactBookingTransactions[CustomerKey]
            ),
            "@Coupons", CALCULATE ( COUNTROWS ( FactBookingTransactions ) ),
            "@EligibleCoupons",
                CALCULATE (
                    COUNTROWS ( FactBookingTransactions ),
                    FactBookingTransactions[TransactionStatus] IN { "Ticketed", "Flown" }
                ),
            "@RefundedCoupons",
                CALCULATE (
                    COUNTROWS ( FactBookingTransactions ),
                    FactBookingTransactions[IsRefunded] = TRUE
                )
        ),
        USERELATIONSHIP ( FactBookingTransactions[BookingDateKey], DimDate[DateKey] )
    )
VAR Eligible =
    FILTER (
        BookingRows,
        [@EligibleCoupons] > 0 && [@RefundedCoupons] < [@Coupons]
    )
VAR CustomerBookings =
    GROUPBY (
        Eligible,
        [CustomerKey],
        "@BookingCount", COUNTX ( CURRENTGROUP (), [BookingReference] )
    )
RETURN
    DIVIDE (
        COUNTROWS ( FILTER ( CustomerBookings, [@BookingCount] >= 2 ) ),
        COUNTROWS ( CustomerBookings ),
        BLANK()
    )
```
- **Format:** `0.0%`.
- **Aggregation:** non-additive ratio; customer-booking grain.
- **Filter context:** booking-date period via `USERELATIONSHIP` on `FactBookingTransactions[BookingDateKey]`; excludes cancelled and fully refunded bookings under proposed OD-18; multiple coupons on one booking count once.
- **Edge cases:** zero eligible customers returns BLANK; no customer PII exposed.
- **Validation:** T-36, T-37, T-47.
- **Related dashboard:** Customer & Service Intelligence.
- **Business interpretation:** share of active customers who booked more than once in the period.
- **Decision status:** **OWNER DECISION REQUIRED** — OD-18 eligibility is open, and no persisted “fully refunded” flag exists. The DAX above is a proposal.

### K-21 — Service Recovery Rate

- **Business purpose:** measure the share of eligible service cases that were resolved.
- **Exact definition:** `RecoveredEligibleCases / EligibleServiceCases`.
- **Numerator:** complaints with `ServiceRecoveryFlag = TRUE` and `ResolutionStatus = Resolved`.
- **Denominator:** complaints with `ServiceRecoveryFlag = TRUE`.
- **Source tables/columns:** `FactCustomerFeedback[FeedbackType]`, `[ServiceRecoveryFlag]`, `[ResolutionStatus]`, `[ResolutionDateKey]`, `[FeedbackDateKey]`.
- **Calculation grain:** feedback event.
- **DAX proposal:**
```DAX
Service Recovery Rate =
DIVIDE (
    CALCULATE (
        COUNTROWS ( FactCustomerFeedback ),
        FactCustomerFeedback[FeedbackType] = "Complaint",
        FactCustomerFeedback[ServiceRecoveryFlag] = TRUE,
        FactCustomerFeedback[ResolutionStatus] = "Resolved",
        NOT ISBLANK ( FactCustomerFeedback[ResolutionDateKey] )
    ),
    CALCULATE (
        COUNTROWS ( FactCustomerFeedback ),
        FactCustomerFeedback[FeedbackType] = "Complaint",
        FactCustomerFeedback[ServiceRecoveryFlag] = TRUE
    ),
    BLANK()
)
```
- **Format:** `0.0%`.
- **Aggregation:** non-additive ratio.
- **Filter context:** feedback date; excludes surveys, compliments, claims; resolution date on/after feedback date.
- **Edge cases:** zero eligible cases returns BLANK; “Closed - No Action” is not resolved; a missing resolution date is not resolved.
- **Validation:** T-36, T-37, T-25.
- **Related dashboard:** Customer & Service Intelligence.
- **Business interpretation:** how often triggered service-recovery cases reached a resolved state.
- **Decision status:** OD-17 definition proposed; formal approval required.

## 4. KPI summary matrix

| ID | KPI | Grain | Primary date role | Format | Dashboard | Decision dependency |
|---|---|---|---|---|---|---|
| K-01 | ASK | Flight | Departure | `#,##0` | Executive, Network | OD-05 |
| K-02 | RPK | Flight | Departure | `#,##0` | Executive, Network | OD-20 |
| K-03 | Load Factor | Flight | Departure | `0.0%` | Executive, Network | OD-05 |
| K-04 | Passenger Yield | Flight + coupon | Travel | `$0.0000` | Revenue | OD-06, OD-08 |
| K-05 | Passenger RASK | Flight + coupon | Travel | `$0.0000` | Revenue, Executive | OD-05, OD-06, OD-08 |
| K-06 | Total RASK | Flight + coupon | Travel | `$0.0000` | Revenue, Executive | OD-07, OD-08 |
| K-07 | CASK | Flight + cost | Cost | `$0.0000` | Executive, Revenue, Network | OD-13 |
| K-08 | Unit Contribution | Flight + coupon + cost | Travel/Cost | `$0.0000` | Executive, Revenue | OD-06/07/08/13 |
| K-09 | OTP | Flight | Departure | `0.0%` | Operations, Executive | OD-09 |
| K-10 | Cancellation Rate | Flight | Departure | `0.0%` | Operations, Executive | OD-19 |
| K-11 | Completion Rate | Flight | Departure | `0.0%` | Operations | OD-19 |
| K-12 | Average Delay | Flight | Arrival/Departure | `0.0 min` | Operations | OD-09/OD-13 |
| K-13 | Aircraft Utilization | Flight + aircraft-day | Departure | `0.00` | Operations, Network | OD-10 |
| K-14 | Average Passenger Revenue | Flight + coupon | Travel | `$#,##0.00` | Revenue | OD-06, OD-08 |
| K-15 | Ancillary Revenue per Passenger | Flight + coupon | Travel | `$#,##0.00` | Revenue, Customer | OD-07, OD-08 |
| K-16 | Booking Lead Time | Booking | Booking | `0.0 days` | Revenue, Customer | **OWNER DECISION REQUIRED** (OD-18/OD-22) |
| K-17 | Refund Rate | Coupon | Booking | `0.0%` | Customer, Revenue | OD-08/OD-18 |
| K-18 | Period Complaint Rate | Feedback + flight | Feedback/Departure | `0.00 per 1,000` | Customer, Executive | OD-12 |
| K-19 | Satisfaction | Feedback | Feedback | `0.00` | Customer | OD-11 |
| K-20 | Repeat Booking Rate | Customer-booking | Booking | `0.0%` | Customer | **OWNER DECISION REQUIRED** (OD-18) |
| K-21 | Service Recovery Rate | Feedback | Feedback | `0.0%` | Customer | OD-17 |

## 5. Supporting metrics (not substitutes for K-01–K-21)

The contract defines S-01 to S-13. They may be used in visuals in addition to the required KPIs, but must not replace them. Proposed formulas are in contract Section 11.5; key rules:

- `S-01 Revenue Growth %` and `S-02 Cost Growth %`: prior comparable period; zero prior returns BLANK.
- `S-03 On-Time Arrival %`: arrival basis; separate from K-09.
- `S-04 Delay Minutes per Operated Flight`: all operated flights; missing delay is a DQ exception, not zero.
- `S-05 Disruption Rate`: distinct disrupted flights / scheduled flights.
- `S-06 Reactionary Delay Share`: attributed delay minutes with evidence / all attributed delay; zero returns BLANK.
- `S-07 Ancillary Revenue Share`: net ancillary / total operating revenue.
- `S-08 Booking Channel Mix` and `S-09 Fare Class Mix`: state the basis; do not mix count and revenue.
- `S-10 Route Contribution`: route revenue − route cost; margin requires zero-revenue guard.
- `S-11 Target Variance`: targets are not defined; report actuals only and label target variance unavailable (OD-21).
- `S-12 Airline and Route Rankings`: RANKX; state KPI, order, tie behavior; not additive.
- `S-13 Scheduled vs Operated Flight Count`: operated + cancelled = scheduled.

## 6. Validation and execution boundary

| Requirement | Status |
|---|---|
| 21 KPI definitions documented | DOCUMENTED |
| DAX formulas proposed | DOCUMENTED — NOT EXECUTED |
| Independent control calculations | PLANNED (T-28–T-36, T-49, T-60) |
| Zero-denominator runtime test | BLOCKED (T-37; no model) |
| Report KPI reconciliation | BLOCKED (T-46; no report) |
| Synthetic disclosure test | BLOCKED (T-79; no rendered report) |
| Target variance | OWNER DECISION REQUIRED (OD-21; no targets) |
| Sentiment KPI | NOT IN CONTRACT — do not build |
| Severity KPI | NOT IN CONTRACT — do not build |

**No DAX is claimed to compile or run.** Formula proposals must be implemented, tested, and reconciled in a future authorized model. A zero-denominator test is not a static review; it requires Power BI runtime execution.

## 7. Open decisions

- OD-01A/OD-01B formal signatures and approval.
- OD-02/OD-03 controlled airport and fleet populations.
- OD-04 exchange rates; OD-05 capacity; OD-06 passenger revenue; OD-07 tax/fee; OD-08 refunds; OD-09 OTP; OD-10 availability; OD-11 satisfaction; OD-12 complaint rate; OD-13 classification; OD-14 allocation; OD-15 no separate revenue fact; OD-16 codeshare; OD-17 service recovery; OD-18 repeat/lead eligibility; OD-19 diversion; OD-20 passenger tolerance; OD-21 targets; OD-22 maximum lead time; OP-01 cohort complaint rate.
- K-16 and K-20 require a booking-eligibility helper or a persisted booking-level indicator; without it, the proposed DAX may misclassify fully refunded bookings. This is a design gap to resolve before implementation.
- The 0.01 USD, one-minute, and 0.1% thresholds are proposed engineering validation thresholds, not owner-approved acceptance criteria.

**End of catalogue.** This document is design evidence only. It does not execute DAX, create a model, build a report, or advance a gate.
