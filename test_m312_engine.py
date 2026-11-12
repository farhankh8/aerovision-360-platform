from m312_consumption_engine import (
    execute_measure, verify_measure_access, verify_dataset_access,
    list_approved_measures, build_response,
    get_measure_info
)
from m311_governed_measures import GovernanceStatus
import pandas as pd

fact_flight = pd.read_parquet('data/03_curated/fact_flight_operations.parquet')
fact_disrupt = pd.read_parquet('data/03_curated/fact_disruptions.parquet')
fact_feedback = pd.read_parquet('data/03_curated/fact_customer_feedback.parquet')

print('=== M3.12.2 Engine Verification ===')
print()

# 1. List approved measures
print('1. Approved Measures:')
for mid, info in list_approved_measures().items():
    if mid != '_blocked':
        print(f'   {mid}: {info}')

print()
print('2. Execute Measures (no filters):')
measure_ids = ['FL01', 'FL02', 'FL03', 'FL04', 'DS01', 'DS02', 'DS03', 'CF01', 'CF02', 'CF03']
for mid in measure_ids:
    df = fact_flight if mid in ['FL01', 'FL02', 'FL03', 'FL04'] else (fact_disrupt if mid in ['DS01', 'DS02', 'DS03'] else fact_feedback)
    result = execute_measure(mid, df)
    print(f'   {mid}: value={result["value"]}, status={result["execution_status"]}, governance={result["governance_status"]}')

print()
print('3. Build Response:')
result = execute_measure('FL01', fact_flight)
response = build_response('FL01', result)
print(f'   Response has {len(response)} keys')
print(f'   Disclaimer: {response["disclaimer"]}')
print(f'   Measure: {response["measure_id"]} = {response["value"]} {response["unit"]}')

print()
print('4. Governance Rejection Tests:')
for mid in ['UNDEF-01', 'UNDEF-02', 'UNKNOWN_MEASURE']:
    result = verify_measure_access(mid)
    print(f'   {mid}: allowed={result["allowed"]}, status={result["governance_status"]}, block={result["block_code"]}')

print()
print('5. Dataset Blocking Tests:')
for ds in ['FactBookingTransactions', 'FactOperatingCosts', 'unknown_dataset']:
    result = verify_dataset_access(ds)
    print(f'   {ds}: accessible={result["accessible"]}, block={result["block_code"]}')

print()
print('6. Measure Info:')
for mid in ['FL01', 'FL02', 'FL03', 'FL04']:
    info = get_measure_info(mid)
    print(f'   {mid}: {info["name"]}, status={info["governance_status"]}, unit={info["unit"]}')

print()
print('7. Unit Check:')
for mid in ['FL01', 'FL02', 'FL03', 'FL04', 'DS01', 'DS02', 'DS03', 'CF01', 'CF02', 'CF03']:
    from m312_consumption_engine import _get_measure_unit
    unit = _get_measure_unit(mid)
    print(f'   {mid}: unit={unit}')

print()
print('=== Engine Verification Complete ===')