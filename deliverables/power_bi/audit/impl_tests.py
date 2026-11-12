import pandas as pd, json, re, os
D='deliverables/data/'
fo=pd.read_csv(D+'fact_flight_operations.csv')
fd=pd.read_csv(D+'fact_disruptions.csv')
fc=pd.read_csv(D+'fact_customer_feedback.csv')
dt=pd.read_csv(D+'dim_disruption_type.csv')
date=pd.read_csv(D+'dim_date.csv')

results=[]
def test(name, actual, expected, tol=0.005):
    ok = abs(actual-expected) <= tol
    results.append((name, actual, expected, 'PASS' if ok else 'FAIL'))
    return ok

test('FL01',(fo['FlightStatus']=='Operated').sum(),4776)
test('FL02',fo['RevenuePassengers'].sum(),218413)
test('FL03',fo['DepartureDelayMinutes'].mean(),43.42)
test('FL04',fo['CancellationFlag'].sum()/len(fo)*100,4.48)
test('DS01',len(fd),1754)
test('DS02',fd['DelayMinutes'].mean(),120.62)
merged=fd.merge(dt[['DisruptionTypeKey','ControllableFlag']],on='DisruptionTypeKey')
test('DS03',merged['ControllableFlag'].sum(),540)
test('CF01',len(fc),2500)
test('CF02',fc['SatisfactionScore'].mean(),2.99)
test('CF03',(fc['FeedbackType']=='Complaint').sum()/len(fc)*100,25.52)

# relationship cardinality (PK uniqueness)
for t,col in [('dim_airline','AirlineKey'),('dim_airport','AirportKey'),('dim_route','RouteKey'),('dim_date','DateKey'),('dim_aircraft','AircraftKey'),('dim_aircraft_type','AircraftTypeKey'),('dim_customer','CustomerKey'),('dim_disruption_type','DisruptionTypeKey'),('dim_booking_channel','BookingChannelKey'),('dim_currency','CurrencyKey'),('dim_fare_class','FareClassKey'),('fact_flight_operations','FlightOperationKey'),('fact_disruptions','DisruptionKey'),('fact_customer_feedback','FeedbackKey')]:
    df=pd.read_csv(D+t+'.csv')
    ok = df[col].isna().sum()==0 and df[col].nunique()==len(df)
    results.append((f'PK {t}.{col}', int(df[col].nunique()), len(df), 'PASS' if ok else 'FAIL'))

# referential integrity
def ri(name, fact, col, dim, dcol):
    orphans=int((~fact[col].isin(dim[dcol])).sum())
    results.append((f'RI {name}', orphans, 0, 'PASS' if orphans==0 else 'FAIL'))
ri('FFO Airline',fo,'AirlineKey',pd.read_csv(D+'dim_airline.csv'),'AirlineKey')
ri('FFO Route',fo,'RouteKey',pd.read_csv(D+'dim_route.csv'),'RouteKey')
ri('FFO Aircraft',fo,'AircraftKey',pd.read_csv(D+'dim_aircraft.csv'),'AircraftKey')
ri('FFO SchedDepDate',fo,'ScheduledDepartureDateKey',date,'DateKey')
ri('FFO SchedArrDate',fo,'ScheduledArrivalDateKey',date,'DateKey')
ri('FD Airline',fd,'AirlineKey',pd.read_csv(D+'dim_airline.csv'),'AirlineKey')
ri('FD Route',fd,'RouteKey',pd.read_csv(D+'dim_route.csv'),'RouteKey')
ri('FD DisruptionType',fd,'DisruptionTypeKey',dt,'DisruptionTypeKey')
ri('FD EventAirport',fd,'EventLocationAirportKey',pd.read_csv(D+'dim_airport.csv'),'AirportKey')
ri('FD EventDate',fd,'EventDateKey',date,'DateKey')
ri('FCF Customer',fc,'CustomerKey',pd.read_csv(D+'dim_customer.csv'),'CustomerKey')
ri('FCF Airline',fc,'AirlineKey',pd.read_csv(D+'dim_airline.csv'),'AirlineKey')
ri('FCF Route',fc,'RouteKey',pd.read_csv(D+'dim_route.csv'),'RouteKey')
ri('FCF FeedbackDate',fc,'FeedbackDateKey',date,'DateKey')

# blocked financial measures check in DAX file
dax_raw=open('deliverables/power_bi/dax/AEROVISION360_Measures.dax').read()
# strip comments before checking for implemented blocked measures
dax_code='\n'.join(line.split('//')[0] for line in dax_raw.splitlines())
blocked_terms=['Total Revenue =','Operating Cost =','ExchangeRate','FactBookingTransactions =','FactOperatingCosts =']
found=[t for t in blocked_terms if t in dax_code]
results.append(('Blocked financial terms in DAX', len(found), 0, 'PASS' if len(found)==0 else 'FAIL'))

# date filtering sanity (dim_date range)
results.append(('dim_date rows', len(date), 761, 'PASS' if len(date)==761 else 'FAIL'))

# write report
lines=['# Implementation Test Results - AEROVISION 360','','| Test | Actual | Expected | Status |','|---|---:|---:|---|']
for n,a,e,s in results:
    lines.append(f'| {n} | {a} | {e} | {s} |')
fails=[r for r in results if r[3]=='FAIL']
lines.append('')
lines.append(f'**Total tests:** {len(results)}  **Failures:** {len(fails)}')
if fails:
    lines.append('**Failed tests:**')
    for r in fails: lines.append(f'- {r[0]}')
open('deliverables/power_bi/audit/IMPLEMENTATION_TEST_RESULTS.md','w',encoding='utf-8').write('\n'.join(lines))
print('tests',len(results),'failures',len(fails))
