from m311_governed_measures import calculate_flights_operated, calculate_total_revenue_passengers, calculate_average_delay_minutes, calculate_cancellation_rate, calculate_disruptions_total, calculate_average_delay_disruption, calculate_controllable_disruptions, calculate_feedback_total, calculate_average_satisfaction, calculate_complaint_percentage, check_governance_status, GovernanceStatus
from m311_bi_contract import MEASURE_DEFINITIONS, BLOCKED_MEASURES, DATASET_IDS, MODEL_VERSION, validate_contract_against_schemas, export_contract_json
from pathlib import Path
import pandas as pd

fact_flight = pd.read_parquet('data/03_curated/fact_flight_operations.parquet')
fact_disrupt = pd.read_parquet('data/03_curated/fact_disruptions.parquet')
fact_feedback = pd.read_parquet('data/03_curated/fact_customer_feedback.parquet')
dim_disrupt = pd.read_parquet('data/03_curated/dim_disruption_type.parquet')

print('=== M3.12.2 Foundation Verification ===')
contract_path = Path('contracts/bi_consumption_model_m311.json')
vr = validate_contract_against_schemas(contract_path)
print(f'Contract version: {MODEL_VERSION}')
print(f'Contract valid: {vr["valid"]}')
print(f'Dataset IDs: {list(DATASET_IDS.values())}')
print(f'Approved measures: {list(MEASURE_DEFINITIONS.keys())}')
print(f'Governance - FL01: {check_governance_status("FL01")}')
print(f'Governance - UNDEF-01: {check_governance_status("UNDEF-01")}')

print()
print('Pre-computed measure results:')
print(f'FL01: {calculate_flights_operated(fact_flight)}')
print(f'FL02: {calculate_total_revenue_passengers(fact_flight)}')
print(f'FL03: {calculate_average_delay_minutes(fact_flight)}')
print(f'FL04: {calculate_cancellation_rate(fact_flight)}')
print(f'DS01: {calculate_disruptions_total(fact_disrupt)}')
print(f'DS02: {calculate_average_delay_disruption(fact_disrupt)}')
print(f'DS03: {calculate_controllable_disruptions(fact_disrupt, dim_disrupt)}')
print(f'CF01: {calculate_feedback_total(fact_feedback)}')
print(f'CF02: {calculate_average_satisfaction(fact_feedback)}')
print(f'CF03: {calculate_complaint_percentage(fact_feedback)}')