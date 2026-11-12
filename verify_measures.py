from m311_governed_measures import (
    calculate_flights_operated, calculate_total_revenue_passengers,
    calculate_average_delay_minutes, calculate_cancellation_rate,
    calculate_disruptions_total, calculate_average_delay_disruption,
    calculate_controllable_disruptions, calculate_feedback_total,
    calculate_average_satisfaction, calculate_complaint_percentage,
    check_governance_status, GovernanceStatus
)
from m311_bi_contract import validate_contract_against_schemas
from pathlib import Path
import pandas as pd

# Load actual data
fact_flight = pd.read_parquet('data/03_curated/fact_flight_operations.parquet')
fact_disrupt = pd.read_parquet('data/03_curated/fact_disruptions.parquet')
fact_feedback = pd.read_parquet('data/03_curated/fact_customer_feedback.parquet')
dim_disrupt = pd.read_parquet('data/03_curated/dim_disruption_type.parquet')

# Verify all 10 measures
results = {
    'FL01': calculate_flights_operated(fact_flight),
    'FL02': calculate_total_revenue_passengers(fact_flight),
    'FL03': calculate_average_delay_minutes(fact_flight),
    'FL04': calculate_cancellation_rate(fact_flight),
    'DS01': calculate_disruptions_total(fact_disrupt),
    'DS02': calculate_average_delay_disruption(fact_disrupt),
    'DS03': calculate_controllable_disruptions(fact_disrupt, dim_disrupt),
    'CF01': calculate_feedback_total(fact_feedback),
    'CF02': calculate_average_satisfaction(fact_feedback),
    'CF03': calculate_complaint_percentage(fact_feedback),
}

print('=== Measure Verification ===')
for mid, val in results.items():
    print(f'  {mid}: {val}')

# Governance status
print('\n=== Governance Status ===')
for mid in ['FL01','FL02','FL03','FL04','DS01','DS02','DS03','CF01','CF02','CF03']:
    print(f'  {mid}: {check_governance_status(mid)}')

# Contract validation
contract_path = Path('contracts/bi_consumption_model_m311.json')
if contract_path.exists():
    vr = validate_contract_against_schemas(contract_path)
    print(f'\n=== Contract Validation: {"VALID" if vr["valid"] else "INVALID"} ===')
    if vr['errors']:
        for e in vr['errors']:
            print(f'  ERROR: {e}')
    if vr['warnings']:
        for w in vr['warnings']:
            print(f'  WARNING: {w}')