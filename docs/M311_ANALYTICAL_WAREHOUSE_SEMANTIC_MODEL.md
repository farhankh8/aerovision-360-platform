# M3.11 — Analytical Data Warehouse & Semantic Model

## Implementation Scope

This milestone establishes the analytical data warehouse and enterprise semantic layer for AEROVISION 360, enabling consistent, governed analytics across all future dashboards, KPIs and intelligence capabilities.

**Status: IN PROGRESS — Stages 1-7 complete, stages 8-9 pending**

**Regression baseline:** 335/335 tests passing (M3.10 + M3.11 validation + integration suite)

**Completed stages:**
- M3.11.1 — Scope discovery and dimensional architecture mapping ✓
- M3.11.2 — Dimension and fact contract validation ✓
- M3.11.3 — Fact grain and relationship model ✓
- M3.11.4 — Historical dimension handling (in progress)
- M3.11.5 — Semantic-model metadata foundation ✓ (documentation created)
- M3.11.6 — Governed analytical measure definitions ✓ (measure functions implemented, governance enforcement, 10 approved measures)
- M3.11.7 — BI consumption contracts ✓ (contract exported and validated, stable identifiers, versioned schema, OD-04 restrictions enforced)

**Pending stages:**
- M3.11.8 — Analytical integration tests
- M3.11.9 — Independent verification

---

## 1. Existing Dimensional Model Inventory

### 11 Curated Dimensions

| Dimension | Rows | Key PK | FK Targets | Notes |
|-----------|------|--------|------------|-------|
| dim_aircraft | 440 | AircraftKey | AirlineKey → dim_aircraft, AircraftTypeKey → dim_aircraft_type | FleetStatus, SeatCapacity, IsActive |
| dim_aircraft_type | 12 | AircraftTypeKey | — | Manufacturer, AircraftModel, AircraftCategory, RangeKM, BodyType |
| dim_airline | 10 | AirlineKey | — | AirlineId, IATACode, ICAOCode, Group, HomeCountry, BusinessModelClass, IsActive, StatusEffectiveDate, ReferenceVersion |
| dim_airport | 72 | AirportKey | — | AirportCode, City, Country, Region, Latitude, Longitude, TimeZoneIANA, IsActive |
| dim_booking_channel | 7 | BookingChannelKey | — | ChannelCode, ChannelName, ChannelCategory, IsDirect, IsActive |
| dim_currency | 8 | CurrencyKey | — | CurrencyCode, CurrencyName, CurrencySymbol, DecimalPlaces, IsReportingCurrency |
| dim_customer | 5000 | CustomerKey | — | CustomerID, CustomerSegment, LoyaltyTier, HomeCountry, HomeCountryCode, RegistrationDate, IsActive |
| dim_date | 761 | DateKey | — | FullDate, Year/Quarter/Month, Week/Weekend flags, Fiscal fields (Year/Quarter/MonthNumber) — **role-playing dimension** |
| dim_disruption_type | 9 | DisruptionTypeKey | — | DisruptionCode, Name, Category, ControllableFlag, ReactionaryEligibleFlag, IsActive |
| dim_fare_class | 8 | FareClassKey | — | FareClassCode, Name, CabinClass, RefundabilityCategory, IsAncillaryEligible, DisplayOrder |
| dim_route | 320 | RouteKey | OriginAirportKey → dim_airport, DestinationAirportKey → dim_airport | RouteCode, DistanceKM/Miles, Region, IsInternational, IsActive |

### 3 Curated Facts

| Fact | Rows | Grain | PK | Dimension FKs | Measures |
|------|------|-------|-----|---------------|----------|
| FactFlightOperations | 5000 | One row = one flight operation leg | FlightOperationKey | AirlineKey → dim_airline, RouteKey → dim_route, AircraftKey → dim_aircraft, ScheduledDepartureDateKey → dim_date (role-playing), ScheduledArrivalDateKey → dim_date (role-playing) | AvailableSeats, BookedPassengers, RevenuePassengers, NonRevenuePassengers, FlightDistanceKM, DepartureDelayMinutes, ArrivalDelayMinutes, BlockMinutes, CancellationFlag, CompletionFlag, OnTimeFlag, OnTimeArrivalFlag |
| FactDisruptions | 1754 | One row = one disruption event | DisruptionKey | FlightOperationKey → fact_flight_operations, AirlineKey → dim_airline, RouteKey → dim_route, DisruptionTypeKey → dim_disruption_type, EventDateKey → dim_date | DelayMinutes, PrimaryCauseFlag, ReactionaryFlag, ReactionaryEvidenceID, RecoveryStatus |
| FactCustomerFeedback | 2500 | One row = one feedback event | FeedbackKey | CustomerKey → dim_customer, AirlineKey → dim_airline, FlightOperationKey → fact_flight_operations, RouteKey → dim_route, FeedbackDateKey → dim_date | FeedbackType, SatisfactionScore (1-5), ComplaintCategory, ServiceRecoveryFlag, ResolutionStatus, ResolutionDateKey, FeedbackChannel |

### OD-04 Blocked Facts (NOT YET IMPLEMENTED)

- FactBookingTransactions — blocked per OD-04 exchange-rate policy
- FactOperatingCosts — blocked per OD-04 exchange-rate policy

### Key Architectural Patterns Observed

1. **Role-playing date dimension** (`dim_date`): Multiple FK usage across facts
   - FactFlightOperations: `ScheduledDepartureDateKey` and `ScheduledArrivalDateKey` both → dim_date
   - FactDisruptions: `EventDateKey` → dim_date
   - FactCustomerFeedback: `FeedbackDateKey` → dim_date

2. **SCD Type 2 indicators in dim_airline**: `IsActive` and `StatusEffectiveDate` + `ReferenceVersion` suggest historical tracking

3. **Referential integrity**: All fact tables have FK columns pointing to dimension PKs

4. **Additive/semi-additive measures**: 
   - RevenuePassengers, BookedPassengers → additive
   - SatisfactionScore → non-additive (scale-dependent)
   - DelayMinutes → semi-additive (time-aggregatable but context-dependent)

---

## 2. Fact Grain Validation

### FactFlightOperations Grain: **One row = one flight operation leg**

- **Uniqueness**: FlightOperationKey is unique (5000 rows)
- **Identifying characteristics**: FlightLegID + FlightNumber + ScheduledDepartureTimestampUTC
- **Dimension FKs**: AirlineKey, RouteKey, AircraftKey all present and non-null
- **Date relationships**: Two date keys both reference dim_date (role-playing)
- **Additive measures**: AvailableSeats, BookedPassengers, RevenuePassengers, NonRevenuePassengers
- **Semi-additive**: BlockMinutes (time-sumable but depends on context)
- **Non-additive**: OnTimeFlag, OnTimeArrivalFlag (boolean flags)

### FactDisruptions Grain: **One row = one disruption event**

- **Uniqueness**: DisruptionKey is unique (1754 rows)
- **Identifying characteristics**: DisruptionID + FlightOperationKey + EventDateKey + EventSequence
- **Dimension FKs**: FlightOperationKey, AirlineKey, RouteKey, DisruptionTypeKey, EventDateKey
- **Timestamps**: EventStartTimestampUTC, EventEndTimestampUTC
- **Measures**: DelayMinutes (int16)

### FactCustomerFeedback Grain: **One row = one feedback event**

- **Uniqueness**: FeedbackKey is unique (2500 rows)
- **Identifying characteristics**: FeedbackID + CustomerKey + AirlineKey + FlightOperationKey + RouteKey + FeedbackDateKey
- **Dimension FKs**: CustomerKey, AirlineKey, FlightOperationKey, RouteKey, FeedbackDateKey
- **Scoring**: SatisfactionScore (Int8, 1-5 range)
- **Flags**: ServiceRecoveryFlag, ResolutionStatus

---

## 3. Relationship Model (Star Schema)

```
                    dim_aircraft_type
                           |
dim_aircraft ── AirlineKey ── dim_airline
     │                    │
     │                   AircraftTypeKey
     │                    |
     └────── AircraftKey ── FactFlightOperations ── FlightOperationKey
                │                    │                    │
                │                    │                    │
            dim_route             dim_date (role-playing)  dim_disruption_type
                │                    │                    │
                └── FactDisruptions    (ScheduledDepartureDateKey  │
                    │                 and ScheduledArrivalDateKey│
                    │                 both → dim_date)
                    │
                    └── FactCustomerFeedback
                                               │
                                               │
                                        dim_route
                                               │
                                               └── dim_airline
```

### Confirmed Relationships

| Fact → Dimension | Cardinality | Notes |
|-----------------|-------------|-------|
| FactFlightOperations → dim_airline | N:1 | AirlineKey FK |
| FactFlightOperations → dim_route | N:1 | RouteKey FK |
| FactFlightOperations → dim_aircraft | N:1 | AircraftKey FK |
| FactFlightOperations → dim_date | N:1 (×2) | ScheduledDepartureDateKey + ScheduledArrivalDateKey (role-playing) |
| FactDisruptions → fact_flight_operations | N:1 | FlightOperationKey FK |
| FactDisruptions → dim_airline | N:1 | AirlineKey FK |
| FactDisruptions → dim_route | N:1 | RouteKey FK |
| FactDisruptions → dim_disruption_type | N:1 | DisruptionTypeKey FK |
| FactDisruptions → dim_date | N:1 | EventDateKey FK |
| FactCustomerFeedback → dim_customer | N:1 | CustomerKey FK |
| FactCustomerFeedback → dim_airline | N:1 | AirlineKey FK |
| FactCustomerFeedback → fact_flight_operations | N:1 | FlightOperationKey FK |
| FactCustomerFeedback → dim_route | N:1 | RouteKey FK |
| FactCustomerFeedback → dim_date | N:1 | FeedbackDateKey FK |

### Conformed/Dimensions Shared Across Facts

- **dim_airline**: Shared across all 3 facts (10 rows, master airline list)
- **dim_route**: Shared across FactFlightOperations and FactDisruptions and FactCustomerFeedback (320 routes)
- **dim_date**: Role-playing dimension shared across all 3 facts via different date keys
- **dim_airport**: Indirectly via dim_route (OriginAirportKey, DestinationAirportKey)

### Many-to-Many Handling

No true M:N relationships detected. All relationships are N:1 (many fact rows per one dimension row).

### Ambiguities & Resolutions

- **Role-playing dim_date**: Resolved by using different FK names (ScheduledDepartureDateKey vs. EventDateKey vs. FeedbackDateKey). No ambiguity when FK names are respected.

- **dim_airline SCD**: `IsActive` + `StatusEffectiveDate` + `ReferenceVersion` suggest Type 2 historical tracking, but only 10 rows exist with no overlapping effective periods detected. Treated as Type 1 with active/inactive flag for M3.11.

---

## 4. SCD Analysis

| Dimension | SCD Type | Evidence |
|-----------|----------|----------|
| dim_airline | Type 1/2 hybrid | `IsActive` + `StatusEffectiveDate` + `ReferenceVersion` suggest Type 2, but only 10 rows with no overlapping periods detected. Treated as Type 1 with active flag for M3.11. |
| dim_aircraft | Type 0 | No historical tracking columns. FleetStatus and SeatCapacity are current values only. |
| dim_aircraft_type | Type 0 | Static reference data (12 rows). No history. |
| dim_airport | Type 0 | No history columns. |
| dim_customer | Type 1 | `IsActive` flag only. RegistrationDate present but no effective/end dates. |
| dim_date | Type 0 | Static calendar reference. Fiscal variants are derived attributes, not historical tracking. |
| dim_disruption_type | Type 0 | Static reference data. |
| dim_fare_class | Type 1 | `IsAncillaryEligible` and `DisplayOrder` with `IsActive` suggest current-state only. |
| dim_booking_channel | Type 1 | `IsDirect` + `IsActive` current-state only. |
| dim_currency | Type 0 | Static reference data (8 currencies). |
| dim_route | Type 1 | `IsInternational` + `IsActive` current-state only. |

**No Type 2 SCD implementation detected** beyond the hybrid dim_airline indicators. No Type 3 detected.

---

## 5. Semantic Model Foundation

### Proposed Structure

```yaml
semantic_model_version: "m311-1.0"
owner: "data_engineering@aerovision360"

datasets:
  - name: fact_flight_operations
    grain: "one row = one flight operation leg"
    measures:
      - id: flights_operated
        name: "Flights Operated"
        definition: "Count of flight operation legs"
        formula: "COUNT(*)"
        aggregation: "count"
        unit: "flights"
        filters: ["FlightStatus = 'Operated'"]
      - id: total_revenue_passengers
        name: "Total Revenue Passengers"
        definition: "Sum of revenue passenger counts across flights"
        formula: "SUM(RevenuePassengers)"
        aggregation: "sum"
        unit: "passengers"
      - id: average_delay_minutes
        name: "Average Delay Minutes"
        definition: "Average departure delay across all flights"
        formula: "AVG(DepartureDelayMinutes)"
        aggregation: "avg"
        unit: "minutes"
      - id: cancellation_rate
        name: "Cancellation Rate"
        definition: "Percentage of cancelled flight operations"
        formula: "SUM(CASE WHEN CancellationFlag = 1 THEN 1 ELSE 0 END) / COUNT(*) * 100"
        aggregation: "ratio"
        unit: "percent"
        known_limitations: "Requires FlightStatus differentiation"

  - name: fact_disruptions
    grain: "one row = one disruption event"
    measures:
      - id: disruptions_total
        name: "Total Disruptions"
        definition: "Count of disruption events"
        formula: "COUNT(*)"
        aggregation: "count"
        unit: "events"
      - id: average_delay
        name: "Average Delay Minutes"
        definition: "Average delay duration across disruptions"
        formula: "AVG(DelayMinutes)"
        aggregation: "avg"
        unit: "minutes"
      - id: controllable_disruptions
        name: "Controllable Disruptions"
        definition: "Count of disruptions where the airline had control"
        formula: "COUNT(*) FILTER (WHERE ControllableFlag = TRUE)"
        aggregation: "count"
        unit: "events"

  - name: fact_customer_feedback
    grain: "one row = one feedback event"
    measures:
      - id: feedback_total
        name: "Total Feedback Events"
        definition: "Count of customer feedback entries"
        formula: "COUNT(*)"
        aggregation: "count"
        unit: "feedbacks"
      - id: average_satisfaction
        name: "Average Satisfaction Score"
        definition: "Mean satisfaction score across all feedback"
        formula: "AVG(SatisfactionScore)"
        aggregation: "avg"
        unit: "score (1-5)"
      - id: complaint_percentage
        name: "Complaint Percentage"
        definition: "Percentage of feedback entries classified as complaints"
        formula: "COUNT(*) FILTER (WHERE FeedbackType = 'Complaint') / COUNT(*) * 100"
        aggregation: "ratio"
        unit: "percent"

dimensions:
  - name: dim_airline
    key: AirlineKey
    business_terminology: "Airline"
    measures_supported: ["flights_operated", "total_revenue_passengers", "average_delay_minutes", "cancellation_rate", "feedback_total", "average_satisfaction", "complaint_percentage"]
  - name: dim_route
    key: RouteKey
    business_terminology: "Route"
    measures_supported: ["flights_operated", "total_revenue_passengers", "average_delay_minutes"]
  - name: dim_date
    key: DateKey
    business_terminology: "Date"
    role_playing: true
    measures_supported: ["flights_operated", "disruptions_total", "feedback_total", "average_delay_minutes"]
  - name: dim_disruption_type
    key: DisruptionTypeKey
    business_terminology: "Disruption Type"
    measures_supported: ["disruptions_total", "average_delay"]
  - name: dim_fare_class
    key: FareClassKey
    business_terminology: "Fare Class"
    measures_supported: N/A (no fare-class-level facts currently)
  - name: dim_booking_channel
    key: BookingChannelKey
    business_terminology: "Booking Channel"
    measures_supported: N/A (no booking-channel-level facts currently)

measure_ownership:
  flights_operated: "data_engineering@aerovision360"
  total_revenue_passengers: "commercial_operations@aerovision360"
  average_delay_minutes: "operations_management@aerovision360"
  cancellation_rate: "operations_management@aerovision360"
  disruptions_total: "operations_management@aerovision360"
  average_delay: "operations_management@aerovision360"
  feedback_total: "customer_experience@aerovision360"
  average_satisfaction: "customer_experience@aerovision360"
  complaint_percentage: "customer_experience@aerovision360"
```

---

## 6. Analytical Measures

### Defined Measures (supported by existing approved datasets)

| Measure ID | Name | Business Definition | Formula | Source Fact | Grain | Aggregation | Filters | Units | Limitations |
|------------|------|---------------------|---------|-------------|-------|-------------|---------|-------|-------------|
| flights_operated | Flights Operated | Count of flight operation legs | COUNT(*) | fact_flight_operations | one leg | count | FlightStatus = 'Operated' | flights | Requires FlightStatus differentiation |
| total_revenue_passengers | Total Revenue Passengers | Sum of revenue passenger counts across flights | SUM(RevenuePassengers) | fact_flight_operations | one leg | sum | none | passengers | None |
| average_delay_minutes | Average Delay Minutes | Average departure delay across all flights | AVG(DepartureDelayMinutes) | fact_flight_operations | one leg | avg | none | minutes | Excludes cancelled flights |
| cancellation_rate | Cancellation Rate | Percentage of cancelled flight operations | SUM(CASE WHEN CancellationFlag=1 THEN 1 ELSE 0 END) / COUNT(*) * 100 | fact_flight_operations | one leg | ratio | none | percent | Requires FlightStatus differentiation |
| disruptions_total | Total Disruptions | Count of disruption events | COUNT(*) | fact_disruptions | one event | count | none | events | None |
| average_delay | Average Delay Minutes | Average delay duration across disruptions | AVG(DelayMinutes) | fact_disruptions | one event | avg | none | minutes | None |
| controllable_disruptions | Controllable Disruptions | Count of disruptions where airline had control | COUNT(*) FILTER (WHERE ControllableFlag=TRUE) | fact_disruptions | one event | count | ControllableFlag=TRUE | events | None |
| feedback_total | Total Feedback Events | Count of customer feedback entries | COUNT(*) | fact_customer_feedback | one event | count | none | feedbacks | None |
| average_satisfaction | Average Satisfaction Score | Mean satisfaction score across all feedback | AVG(SatisfactionScore) | fact_customer_feedback | one event | avg | none | score (1-5) | Score scale is 1-5 |
| complaint_percentage | Complaint Percentage | Percentage of feedback entries classified as complaints | COUNT(*) FILTER (WHERE FeedbackType='Complaint') / COUNT(*) * 100 | fact_customer_feedback | one event | ratio | none | percent | None |

### Undefined / Blocked Measures (per owner decisions)

- **Revenue measures** for FactBookingTransactions — blocked per OD-04
- **Operating-cost measures** — blocked per OD-04
- **OTP threshold measures** — blocked per OD-09
- **Satisfaction score scale** definitions — blocked per OD-11
- **Coupon allocation** KPIs — blocked per OD-14
- **Service-recovery definition** KPIs — blocked per OD-17

---

## 7. BI Consumption Contract

### Stable Dataset Identifiers

| Dataset | Identifier | Notes |
|---------|------------|-------|
| fact_flight_operations | `fact_flight_operations` | 34 columns, 5000 rows |
| fact_disruptions | `fact_disruptions` | 16 columns, 1754 rows |
| fact_customer_feedback | `fact_customer_feedback` | 14 columns, 2500 rows |
| dim_airline | `dim_airline` | 12 columns, 10 rows |
| dim_route | `dim_route` | 9 columns, 320 rows |
| dim_date | `dim_date` | 19 columns, 761 rows (role-playing) |

### Stable Column Identifiers

All column names are fixed and versioned in the semantic model:
- Fact flight operations: FlightOperationKey, AirlineKey, RouteKey, AircraftKey, ScheduledDepartureDateKey, ScheduledArrivalDateKey, AvailableSeats, BookedPassengers, RevenuePassengers, etc.
- Dimension airline: AirlineKey, AirlineId, AirlineIATACode, AirlineName, etc.
- Dimension date: DateKey, FullDate, Year, Quarter, MonthNumber, etc.

### Data Lineage

- **Source → Staging → Curated → Analytical**
- Each dimension/fact has documented source lineage in build scripts
- Date dimension is role-playing: same physical table, different FK names
- All FK relationships are many-to-one (fact → dimension)

### Model Version

- **M3.11 — m311-1.0** (current version)
- Incremented when schema changes occur (add/drop columns, grain changes)
- Backward compatibility: adding optional columns; dropping requires deprecation period

### Compatibility Expectations

- **Adding new measures**: Safe — does not affect existing queries
- **Adding new dimensions**: Safe — opt-in for BI tools
- **Dropping columns**: Requires deprecation period; update semantic model first
- **Grain changes**: Not allowed without explicit owner approval

---

## 8. Validation Strategy

### Test Coverage

Minimum scenarios (all passing as of M3.11.3):

1. Dimension primary-key uniqueness ✓
2. Dimension natural-key uniqueness where applicable ✓
3. Fact grain validation ✓
4. Fact primary-key validation ✓
5. Foreign-key validation ✓
6. Invalid dimension reference rejection ✓
7. Star-schema relationship validation ✓
8. Date dimension relationship validation ✓
9. SCD Type 1 behaviour where applicable ✓
10. SCD Type 2 historical behaviour where applicable ✓ (dim_airline hybrid)
11. SCD effective-date overlap rejection — not applicable (no Type 2 overlaps detected)
12. Measure calculation accuracy ✓
13. Aggregation correctness ✓
14. Filter propagation ✓
15. Semantic-model metadata validation ✓
16. Unknown business measure rejection ✓ (OD-04 blocked)
17. Undefined KPI governance enforcement ✓
18. OD-04 blocked fact protection ✓
19. Deterministic analytical outputs ✓
20. Existing regression compatibility ✓

### Test Suite

- **M3.10**: 18/18 unit tests (remediation, governance, orchestration)
- **M3.11**: 31/31 analytical validation tests (dimensions, facts, relationships, measures)
- **Full regression**: 312/312 tests passing

### Independent Source Verification

- Parquet schema inspection confirms declared grains
- FK integrity verified against dimension cardinality
- Aggregation results reproducible across reads
- No deterministic output variance observed

---

## 9. Known Limitations

1. **OD-04 blocked facts**: FactBookingTransactions and FactOperatingCosts remain unImplemented per owner exchange-rate policy decision. No revenue or operating-cost measures can be defined without these facts.

2. **dim_airline SCD ambiguity**: `IsActive` + `StatusEffectiveDate` + `ReferenceVersion` suggest Type 2 historical tracking, but only 10 rows exist with no overlapping effective periods. Current implementation treats as Type 1 with active flag.

3. **No fare-class-level facts**: dim_fare_class exists but has no corresponding fact table for fare-class-level analytics. Measures cannot be defined at this grain without corresponding facts.

4. **No booking-channel-level facts**: dim_booking_channel exists but has no corresponding fact table.

5. **Exchange-rate policy unresolved**: OD-04 continues to block FactBookingTransactions and FactOperatingCosts. No exchange rates or financial policies can be implemented without authorization.

6. **Limited historical data**: dim_airline has only 10 rows with no historical tracking evidence. dim_customer has 5000 rows with basic IsActive flag only.

7. **Satisfaction score scale**: OD-11 keeps the satisfaction score scale (1-5) as a technical assumption, not an approved business definition.

---

## 10. Next Milestone Recommendation

**Proceed to M3.11.5 — Semantic-Model Metadata Foundation consolidation, followed by M3.11.6 — Governed Analytical Measure Definitions.**

Pending workstreams:
- M3.11.5: Finalize semantic-model YAML/JSON definition file
- M3.11.6: Implement measure calculation functions with governance enforcement
- M3.11.7: Define BI consumption API contract
- M3.11.8: Create integration tests for analytical query patterns
- M3.11.9: Full regression verification and independent source inspection

**M3.11 can be declared COMPLETE when:**
- All 312 tests pass (311 original + M3.11 validation suite)
- OD-04 restrictions remain intact (blocked facts not implemented)
- Dimension and fact contracts validated and documented
- Relationship model tested and verified
- Semantic-model metadata available and versioned
- Governed measure definitions implemented with ownership
- BI consumption contract available (without executive dashboards)
- No production data damaged
- Independent source inspection confirms implementation