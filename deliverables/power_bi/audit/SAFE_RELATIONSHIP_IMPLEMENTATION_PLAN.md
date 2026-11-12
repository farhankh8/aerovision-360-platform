# Safe Relationship Implementation Plan — AEROVISION 360

## Scope and method
- Read-only architecture task. No PBIX, source data or specifications were modified.
- Evidence source: `RELATIONSHIP_VALIDATION.csv`, actual 14 CSV schemas, key uniqueness, null checks and referential integrity checks.
- All 14 datasets inspected; all proposed FK paths have 0 orphan rows.

## Ambiguous paths detected and resolutions

### 1. Airline to Flight Operations (ambiguous)
- Paths:
  - `dim_airline.AirlineKey -> fact_flight_operations.AirlineKey` (direct)
  - `dim_airline.AirlineKey -> dim_aircraft.AirlineKey -> fact_flight_operations.AircraftKey` (indirect)
- Evidence: in all 5,000 flight rows, `fact_flight_operations.AirlineKey` equals the related `dim_aircraft.AirlineKey`. The indirect path is therefore lossless.
- Resolution: keep the snowflake path active (`dim_airline -> dim_aircraft -> fact_flight_operations`) and make the direct `dim_airline -> fact_flight_operations` relationship **inactive**. This preserves airline filtering of flights while avoiding two active paths.
- Risk: if future data allows a flight's operating airline to differ from aircraft owner, the inactive direct relationship can be activated and the snowflake path deactivated.

### 2. Airport to Disruptions (ambiguous)
- Paths:
  - `dim_airport.AirportKey -> fact_disruptions.EventLocationAirportKey` (direct)
  - `dim_airport.AirportKey -> dim_route.OriginAirportKey -> fact_disruptions.RouteKey` (indirect)
- Evidence: in all 1,754 disruption rows, `EventLocationAirportKey` equals the related route's `OriginAirportKey`.
- Resolution: keep `dim_airport -> dim_route` and `dim_route -> fact_disruptions` active; make direct `dim_airport -> fact_disruptions` **inactive**.

### 3. Origin vs Destination Airport
- `dim_airport` connects to `dim_route` twice (OriginAirportKey, DestinationAirportKey).
- Only one can be active. Keep Origin active; Destination inactive.
- Evidence: both columns have 0 orphans against `dim_airport.AirportKey`.

### 4. Role-playing Date
- `dim_date` connects to multiple facts/columns. Within each table pair only one relationship can be active.
- Keep the primary operational date active in each fact:
  - `fact_flight_operations.ScheduledDepartureDateKey` active; `ScheduledArrivalDateKey` inactive.
  - `fact_disruptions.EventDateKey` active.
  - `fact_customer_feedback.FeedbackDateKey` active; `ResolutionDateKey` inactive.
- Secondary date roles require inactive relationships and `USERELATIONSHIP` in measures, unless separate date tables are created.

## Recommended active relationships (14)
1. dim_airline.AirlineKey -> dim_aircraft.AirlineKey
2. dim_aircraft_type.AircraftTypeKey -> dim_aircraft.AircraftTypeKey
3. dim_airport.AirportKey -> dim_route.OriginAirportKey
4. dim_aircraft.AircraftKey -> fact_flight_operations.AircraftKey
5. dim_route.RouteKey -> fact_flight_operations.RouteKey
6. dim_date.DateKey -> fact_flight_operations.ScheduledDepartureDateKey
7. dim_airline.AirlineKey -> fact_disruptions.AirlineKey
8. dim_route.RouteKey -> fact_disruptions.RouteKey
9. dim_disruption_type.DisruptionTypeKey -> fact_disruptions.DisruptionTypeKey
10. dim_date.DateKey -> fact_disruptions.EventDateKey
11. dim_customer.CustomerKey -> fact_customer_feedback.CustomerKey
12. dim_airline.AirlineKey -> fact_customer_feedback.AirlineKey
13. dim_route.RouteKey -> fact_customer_feedback.RouteKey
14. dim_date.DateKey -> fact_customer_feedback.FeedbackDateKey

## Recommended inactive relationships (5)
1. dim_airport.AirportKey -> dim_route.DestinationAirportKey
2. dim_airline.AirlineKey -> fact_flight_operations.AirlineKey
3. dim_date.DateKey -> fact_flight_operations.ScheduledArrivalDateKey
4. dim_airport.AirportKey -> fact_disruptions.EventLocationAirportKey
5. dim_date.DateKey -> fact_customer_feedback.ResolutionDateKey

## Relationships that must not be created
1. fact_disruptions.FlightOperationKey -> fact_flight_operations.FlightOperationKey (fact-to-fact).
2. fact_customer_feedback.FlightOperationKey -> fact_flight_operations.FlightOperationKey (fact-to-fact).
3. dim_fare_class, dim_booking_channel, dim_currency: no FK exists in current facts; do not invent relationships.
4. No additional active path between dim_airline and fact_flight_operations beyond the snowflake path.
5. No additional active path between dim_airport and fact_disruptions beyond the route path.

## Role-playing dimension recommendations
- Date: a single `dim_date` table is recommended, with inactive relationships for secondary date roles. Create separate date tables only if independent slicing by arrival/event/feedback/resolution date is required in reports.
- Airport: a single `dim_airport` table is recommended, with origin active and destination inactive. Create a separate destination airport dimension only if independent destination filtering is required.
- Airline and Aircraft: keep as separate dimensions with the snowflake relationship active.

## Evidence summary
- All 14 datasets: 0 duplicate rows; all candidate PKs unique and non-null.
- Referential integrity: 0 orphans for all validated FK paths.
- Airline flight-vs-aircraft key equality: 5,000/5,000.
- Disruption event-vs-route-origin equality: 1,754/1,754.
- Date key ranges and FK nulls validated; ResolutionDateKey has 1,896 nulls (inactive nullable relationship).

## Final relationship count
- Total relationships to create: **19**
- Active: **14**
- Inactive: **5**
- Fact-to-fact relationships: **0**

## Implementation status
This configuration has **not** been implemented in Power BI Desktop. It is a verified read-only architecture recommendation.