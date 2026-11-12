# Implementation Test Results - AEROVISION 360

| Test | Actual | Expected | Status |
|---|---:|---:|---|
| FL01 | 4776 | 4776 | PASS |
| FL02 | 218413 | 218413 | PASS |
| FL03 | 43.42085427135678 | 43.42 | PASS |
| FL04 | 4.4799999999999995 | 4.48 | PASS |
| DS01 | 1754 | 1754 | PASS |
| DS02 | 120.615165336374 | 120.62 | PASS |
| DS03 | 540 | 540 | PASS |
| CF01 | 2500 | 2500 | PASS |
| CF02 | 2.9910384818133897 | 2.99 | PASS |
| CF03 | 25.52 | 25.52 | PASS |
| PK dim_airline.AirlineKey | 10 | 10 | PASS |
| PK dim_airport.AirportKey | 72 | 72 | PASS |
| PK dim_route.RouteKey | 320 | 320 | PASS |
| PK dim_date.DateKey | 761 | 761 | PASS |
| PK dim_aircraft.AircraftKey | 440 | 440 | PASS |
| PK dim_aircraft_type.AircraftTypeKey | 12 | 12 | PASS |
| PK dim_customer.CustomerKey | 5000 | 5000 | PASS |
| PK dim_disruption_type.DisruptionTypeKey | 9 | 9 | PASS |
| PK dim_booking_channel.BookingChannelKey | 7 | 7 | PASS |
| PK dim_currency.CurrencyKey | 8 | 8 | PASS |
| PK dim_fare_class.FareClassKey | 8 | 8 | PASS |
| PK fact_flight_operations.FlightOperationKey | 5000 | 5000 | PASS |
| PK fact_disruptions.DisruptionKey | 1754 | 1754 | PASS |
| PK fact_customer_feedback.FeedbackKey | 2500 | 2500 | PASS |
| RI FFO Airline | 0 | 0 | PASS |
| RI FFO Route | 0 | 0 | PASS |
| RI FFO Aircraft | 0 | 0 | PASS |
| RI FFO SchedDepDate | 0 | 0 | PASS |
| RI FFO SchedArrDate | 0 | 0 | PASS |
| RI FD Airline | 0 | 0 | PASS |
| RI FD Route | 0 | 0 | PASS |
| RI FD DisruptionType | 0 | 0 | PASS |
| RI FD EventAirport | 0 | 0 | PASS |
| RI FD EventDate | 0 | 0 | PASS |
| RI FCF Customer | 0 | 0 | PASS |
| RI FCF Airline | 0 | 0 | PASS |
| RI FCF Route | 0 | 0 | PASS |
| RI FCF FeedbackDate | 0 | 0 | PASS |
| Blocked financial terms in DAX | 0 | 0 | PASS |
| dim_date rows | 761 | 761 | PASS |

**Total tests:** 40  **Failures:** 0