import json, pandas as pd, os
D='deliverables/data/'
base='deliverables/power_bi/semantic_model/semantic_model.json'
data=json.load(open(base))
tables=data['config']['tables']
# rebuild columns from CSV
for f in os.listdir(D):
    if not f.endswith('.csv'): continue
    name=f.replace('.csv','')
    df=pd.read_csv(D+f)
    if name not in tables:
        tables[name]={'columns':list(df.columns),'measures':[],'relationships':[]}
    else:
        tables[name]['columns']=list(df.columns)
# measures
measures={
 'fact_flight_operations':['FL01','FL02','FL03','FL04'],
 'fact_disruptions':['DS01','DS02','DS03'],
 'fact_customer_feedback':['CF01','CF02','CF03'],
}
for t,ms in measures.items():
    tables[t]['measures']=ms
# relationships per validation (active/inactive)
rels={
 'fact_flight_operations':[
  {'fromColumn':'AirlineKey','toTable':'dim_airline','toColumn':'AirlineKey','role':'active'},
  {'fromColumn':'RouteKey','toTable':'dim_route','toColumn':'RouteKey','role':'active'},
  {'fromColumn':'AircraftKey','toTable':'dim_aircraft','toColumn':'AircraftKey','role':'active'},
  {'fromColumn':'ScheduledDepartureDateKey','toTable':'dim_date','toColumn':'DateKey','role':'active'},
  {'fromColumn':'ScheduledArrivalDateKey','toTable':'dim_date','toColumn':'DateKey','role':'inactive'},
 ],
 'fact_disruptions':[
  {'fromColumn':'AirlineKey','toTable':'dim_airline','toColumn':'AirlineKey','role':'active'},
  {'fromColumn':'RouteKey','toTable':'dim_route','toColumn':'RouteKey','role':'active'},
  {'fromColumn':'DisruptionTypeKey','toTable':'dim_disruption_type','toColumn':'DisruptionTypeKey','role':'active'},
  {'fromColumn':'EventLocationAirportKey','toTable':'dim_airport','toColumn':'AirportKey','role':'active'},
  {'fromColumn':'EventDateKey','toTable':'dim_date','toColumn':'DateKey','role':'inactive'},
 ],
 'fact_customer_feedback':[
  {'fromColumn':'CustomerKey','toTable':'dim_customer','toColumn':'CustomerKey','role':'active'},
  {'fromColumn':'AirlineKey','toTable':'dim_airline','toColumn':'AirlineKey','role':'active'},
  {'fromColumn':'RouteKey','toTable':'dim_route','toColumn':'RouteKey','role':'active'},
  {'fromColumn':'FeedbackDateKey','toTable':'dim_date','toColumn':'DateKey','role':'inactive'},
  {'fromColumn':'ResolutionDateKey','toTable':'dim_date','toColumn':'DateKey','role':'inactive'},
 ],
 'dim_aircraft':[
  {'fromColumn':'AirlineKey','toTable':'dim_airline','toColumn':'AirlineKey','role':'active'},
  {'fromColumn':'AircraftTypeKey','toTable':'dim_aircraft_type','toColumn':'AircraftTypeKey','role':'active'},
 ],
 'dim_route':[
  {'fromColumn':'OriginAirportKey','toTable':'dim_airport','toColumn':'AirportKey','role':'active'},
  {'fromColumn':'DestinationAirportKey','toTable':'dim_airport','toColumn':'AirportKey','role':'inactive'},
 ],
}
for t,rs in rels.items():
    tables[t]['relationships']=rs
# ensure unused dims have empty relationships
for t in tables:
    if 'relationships' not in tables[t]:
        tables[t]['relationships']=[]
    if 'measures' not in tables[t]:
        tables[t]['measures']=[]
data['config']['tables']=tables
# update disclosure
data['config']['disclosure']="Synthetic Simulation - Not Actual Airline Performance"
with open(base,'w',encoding='utf-8') as f:
    json.dump(data,f,indent=2)
print('written')
