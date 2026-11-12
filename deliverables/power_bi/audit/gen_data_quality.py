import pandas as pd, os
D='deliverables/data/'
expected={'dim_airport':72,'dim_aircraft_type':12,'dim_aircraft':440,'dim_customer':5000,'dim_date':761,'dim_disruption_type':9,'dim_fare_class':8,'dim_booking_channel':7,'dim_currency':8,'dim_route':320,'dim_airline':10,'fact_flight_operations':5000,'fact_disruptions':1754,'fact_customer_feedback':2500}
pk={'dim_airport':'AirportKey','dim_aircraft_type':'AircraftTypeKey','dim_aircraft':'AircraftKey','dim_customer':'CustomerKey','dim_date':'DateKey','dim_disruption_type':'DisruptionTypeKey','dim_fare_class':'FareClassKey','dim_booking_channel':'BookingChannelKey','dim_currency':'CurrencyKey','dim_route':'RouteKey','dim_airline':'AirlineKey','fact_flight_operations':'FlightOperationKey','fact_disruptions':'DisruptionKey','fact_customer_feedback':'FeedbackKey'}
null_summary={
 'dim_airline':'AirlineGroup, BusinessModelClass, StatusEffectiveDate (all 10 null)',
 'dim_customer':'LoyaltyTier (686 null)',
 'fact_customer_feedback':'SatisfactionScore (603), ComplaintCategory (1862), ResolutionDateKey (1896)',
 'fact_disruptions':'EventEndTimestampUTC (322), ReactionaryEvidenceID (1682)',
 'fact_flight_operations':'ActualDeparture/Arrival timestamps and delay/block (224 each, cancelled flights)',
}
rows=[]
for name,exp in expected.items():
    df=pd.read_csv(D+name+'.csv')
    nulls=df.isna().sum()
    null_cols='; '.join([f"{c}={int(v)}" for c,v in nulls.items() if v>0]) if (nulls>0).any() else 'none'
    dups=int(df.duplicated().sum())
    status='PASS' if len(df)==exp else 'FAIL'
    notes=null_summary.get(name,'')
    if name=='dim_airline':
        notes += '; 3 columns entirely null (airline reference gap)'
    if name in ('dim_booking_channel','dim_currency','dim_fare_class'):
        notes += '; no FK references in current facts (unused in 14-table model)'
    if name=='dim_date':
        notes='No nulls; 761 rows 2024-10-01 to 2026-10-31'
    rows.append({
        'Dataset':name+'.csv',
        'ExpectedRows':exp,
        'ActualRows':len(df),
        'RowCountStatus':status,
        'ColumnCount':df.shape[1],
        'NullColumns':null_cols,
        'DuplicateRows':dups,
        'CandidatePrimaryKey':pk[name],
        'PKUniqueNonNull':bool(df[pk[name]].isna().sum()==0 and df[pk[name]].nunique()==len(df)),
        'DataQualityStatus':'PASS' if (len(df)==exp and dups==0) else 'ISSUE',
        'Notes':notes
    })
out=pd.DataFrame(rows)
out.to_csv('deliverables/power_bi/audit/DATA_QUALITY_AUDIT.csv',index=False)
print(out.to_string(index=False))
