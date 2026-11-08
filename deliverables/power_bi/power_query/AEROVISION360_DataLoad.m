// AEROVISION 360 - Power Query M Scripts (import-ready)
// Data source: deliverables/data/*.csv (Parquet counterparts exist but are not imported alongside CSV)
// Power BI Desktop > Get Data > Text/CSV, apply one block per table. No source data modified.
// Synthetic Simulation - Not Actual Airline Performance

// dim_airline
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_airline.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"AirlineKey", Int64.Type}, {"AirlineId", type text}, {"AirlineIATACode", type text}, {"AirlineICAOCode", type text}, {"AirlineName", type text}, {"HomeCountry", type text}, {"HomeCountryCode", type text}, {"IsActive", type logical}, {"ReferenceVersion", type text}})
in
    ChangedType

// dim_airport
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_airport.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"AirportKey", Int64.Type}, {"AirportCode", type text}, {"AirportName", type text}, {"City", type text}, {"Country", type text}, {"CountryCode", type text}, {"Region", type text}, {"Latitude", type number}, {"Longitude", type number}, {"TimeZoneIANA", type text}, {"IsActive", type logical}})
in
    ChangedType

// dim_route
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_route.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"RouteKey", Int64.Type}, {"RouteCode", type text}, {"OriginAirportKey", Int64.Type}, {"DestinationAirportKey", Int64.Type}, {"DistanceKM", type number}, {"DistanceMiles", type number}, {"RouteRegion", type text}, {"IsInternational", type logical}, {"IsActive", type logical}})
in
    ChangedType

// dim_date
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_date.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"DateKey", Int64.Type}, {"FullDate", type date}, {"Year", Int64.Type}, {"Quarter", Int64.Type}, {"MonthNumber", Int64.Type}, {"MonthName", type text}, {"MonthShortName", type text}, {"YearMonth", type text}, {"YearMonthSort", Int64.Type}, {"WeekNumber", Int64.Type}, {"WeekStartDate", type date}, {"DayOfMonth", Int64.Type}, {"DayName", type text}, {"DayOfWeekNumber", Int64.Type}, {"IsWeekend", type logical}, {"IsReportingPeriod", type logical}, {"FiscalYear", Int64.Type}, {"FiscalQuarter", Int64.Type}, {"FiscalMonthNumber", Int64.Type}})
in
    ChangedType

// dim_aircraft
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_aircraft.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"AircraftKey", Int64.Type}, {"AircraftRegistration", type text}, {"AirlineKey", Int64.Type}, {"AircraftTypeKey", Int64.Type}, {"FleetEntryDate", type date}, {"FleetStatus", type text}, {"SeatCapacity", Int64.Type}, {"PlannedDailyAvailableHours", type number}, {"IsActive", type logical}})
in
    ChangedType

// dim_aircraft_type
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_aircraft_type.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"AircraftTypeKey", Int64.Type}, {"Manufacturer", type text}, {"AircraftModel", type text}, {"AircraftCategory", type text}, {"TypicalSeatCapacity", Int64.Type}, {"MaximumSeatCapacity", Int64.Type}, {"RangeKM", type number}, {"BodyType", type text}})
in
    ChangedType

// dim_customer
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_customer.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"CustomerKey", Int64.Type}, {"CustomerID", type text}, {"CustomerSegment", type text}, {"LoyaltyTier", type text}, {"HomeCountry", type text}, {"HomeCountryCode", type text}, {"RegistrationDate", type date}, {"IsActive", type logical}})
in
    ChangedType

// dim_disruption_type
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_disruption_type.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"DisruptionTypeKey", Int64.Type}, {"DisruptionCode", type text}, {"DisruptionName", type text}, {"DisruptionCategory", type text}, {"ControllableFlag", type logical}, {"ReactionaryEligibleFlag", type logical}, {"IsActive", type logical}})
in
    ChangedType

// dim_booking_channel
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_booking_channel.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"BookingChannelKey", Int64.Type}, {"ChannelCode", type text}, {"ChannelName", type text}, {"ChannelCategory", type text}, {"IsDirect", type logical}, {"IsActive", type logical}})
in
    ChangedType

// dim_currency
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_currency.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"CurrencyKey", Int64.Type}, {"CurrencyCode", type text}, {"CurrencyName", type text}, {"CurrencySymbol", type text}, {"DecimalPlaces", Int64.Type}, {"IsReportingCurrency", type logical}})
in
    ChangedType

// dim_fare_class
let
    Source = Csv.Document(File.Contents("deliverables/data/dim_fare_class.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"FareClassKey", Int64.Type}, {"FareClassCode", type text}, {"FareClassName", type text}, {"CabinClass", type text}, {"RefundabilityCategory", type text}, {"IsAncillaryEligible", type logical}, {"DisplayOrder", Int64.Type}})
in
    ChangedType

// fact_flight_operations
let
    Source = Csv.Document(File.Contents("deliverables/data/fact_flight_operations.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"FlightOperationKey", Int64.Type}, {"FlightLegID", type text}, {"FlightNumber", type text}, {"AirlineKey", Int64.Type}, {"RouteKey", Int64.Type}, {"AircraftKey", Int64.Type}, {"ScheduledDepartureTimestampUTC", type datetimezone}, {"ActualDepartureTimestampUTC", type datetimezone}, {"ScheduledArrivalTimestampUTC", type datetimezone}, {"ActualArrivalTimestampUTC", type datetimezone}, {"ScheduledDepartureDateKey", Int64.Type}, {"ScheduledArrivalDateKey", Int64.Type}, {"AvailableSeats", Int64.Type}, {"BookedPassengers", Int64.Type}, {"RevenuePassengers", Int64.Type}, {"NonRevenuePassengers", Int64.Type}, {"FlightDistanceKM", type number}, {"FlightStatus", type text}, {"DepartureDelayMinutes", type number}, {"ArrivalDelayMinutes", type number}, {"BlockMinutes", type number}, {"CancellationFlag", type logical}, {"CompletionFlag", type logical}, {"OnTimeFlag", type logical}, {"OnTimeArrivalFlag", type logical}})
in
    ChangedType

// fact_disruptions
let
    Source = Csv.Document(File.Contents("deliverables/data/fact_disruptions.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"DisruptionKey", Int64.Type}, {"DisruptionID", type text}, {"FlightOperationKey", Int64.Type}, {"AirlineKey", Int64.Type}, {"RouteKey", Int64.Type}, {"EventLocationAirportKey", Int64.Type}, {"DisruptionTypeKey", Int64.Type}, {"EventSequence", Int64.Type}, {"EventDateKey", Int64.Type}, {"EventStartTimestampUTC", type datetimezone}, {"EventEndTimestampUTC", type datetimezone}, {"DelayMinutes", Int64.Type}, {"PrimaryCauseFlag", type logical}, {"ReactionaryFlag", type logical}, {"ReactionaryEvidenceID", type text}, {"RecoveryStatus", type text}})
in
    ChangedType

// fact_customer_feedback
let
    Source = Csv.Document(File.Contents("deliverables/data/fact_customer_feedback.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"FeedbackKey", Int64.Type}, {"FeedbackID", type text}, {"CustomerKey", Int64.Type}, {"AirlineKey", Int64.Type}, {"FlightOperationKey", Int64.Type}, {"RouteKey", Int64.Type}, {"FeedbackDateKey", Int64.Type}, {"FeedbackType", type text}, {"SatisfactionScore", type number}, {"ComplaintCategory", type text}, {"ServiceRecoveryFlag", type logical}, {"ResolutionStatus", type text}, {"ResolutionDateKey", Int64.Type}, {"FeedbackChannel", type text}})
in
    ChangedType

// fact_booking_transactions
let
    Source = Csv.Document(File.Contents("deliverables/data/fact_booking_transactions.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"BookingTransactionKey", Int64.Type}, {"BookingReference", type text}, {"TicketNumber", type text}, {"TicketCouponNumber", Int64.Type}, {"CustomerKey", Int64.Type}, {"AirlineKey", Int64.Type}, {"FlightOperationKey", Int64.Type}, {"RouteKey", Int64.Type}, {"FareClassKey", Int64.Type}, {"BookingChannelKey", Int64.Type}, {"BookingDateKey", Int64.Type}, {"TravelDateKey", Int64.Type}, {"PassengerCount", Int64.Type}, {"IsRevenuePassenger", type logical}, {"BaseFareAmount", type number}, {"DiscountAmount", type number}, {"TaxAmount", type number}, {"FeeAmount", type number}, {"AncillaryRevenueAmount", type number}, {"RefundAmount", type number}, {"AncillaryRefundAmount", type number}, {"FeeRefundAmount", type number}, {"CancellationFeeAmount", type number}, {"NoShowFeeAmount", type number}, {"TransactionCurrencyKey", Int64.Type}, {"ExchangeRateToUSD", type number}, {"RateDateKey", Int64.Type}, {"RateVersion", type text}, {"BaseFareUSD", type number}, {"DiscountUSD", type number}, {"TaxUSD", type number}, {"FeeUSD", type number}, {"AncillaryRevenueUSD", type number}, {"RefundUSD", type number}, {"AncillaryRefundUSD", type number}, {"FeeRefundUSD", type number}, {"CancellationFeeUSD", type number}, {"NoShowFeeUSD", type number}, {"NetPassengerRevenueUSD", type number}, {"NetFeeRevenueUSD", type number}, {"NetAncillaryRevenueUSD", type number}, {"TransactionStatus", type text}, {"IsRefunded", type logical}, {"BookingLeadTimeDays", Int64.Type}, {"SyntheticProvenance", type text}})
in
    ChangedType

// fact_operating_costs
let
    Source = Csv.Document(File.Contents("deliverables/data/fact_operating_costs.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=CsvQuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteAllHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{"OperatingCostKey", Int64.Type}, {"CostLineID", type text}, {"FlightOperationKey", Int64.Type}, {"AirlineKey", Int64.Type}, {"RouteKey", Int64.Type}, {"CostDateKey", Int64.Type}, {"CostCategory", type text}, {"CostSubcategory", type text}, {"CostAmount", type number}, {"CurrencyKey", Int64.Type}, {"ExchangeRateToUSD", type number}, {"RateDateKey", Int64.Type}, {"RateVersion", type text}, {"CostAmountUSD", type number}, {"CostDescription", type text}, {"SourceDocumentNumber", type text}, {"IsAllocated", type logical}, {"SyntheticProvenance", type text}})
in
    ChangedType