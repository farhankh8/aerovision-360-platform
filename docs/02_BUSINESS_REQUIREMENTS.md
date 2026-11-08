# AEROVISION 360 — Business Requirements

**Version:** 1.1  
**Status:** Baseline for data-contract design — OD-01 remediation applied; formal OD-01A/OD-01B approval pending

## BR-01 — Multi-airline comparison

The platform shall compare ten real airline identities over the defined
reporting period using consistent metric definitions and comparable
filters. The ten identities are the fixed intended population. Each
populated identity attribute must be source-verified and recorded at
attribute level before a reference version is approved. All operational,
customer, and financial results for those airlines shall be synthetic
simulations and must not be presented as actual airline performance.
Every report page, tooltip while a page is visible, and exported result
must carry the exact disclosure `Synthetic Simulation — Not Actual Airline Performance`.

**Evidence:** Airline identity reference and provenance register, reference
manifest and `G3-RV-01` approval, version/key integrity checks T-72 to
T-78, disclosure test T-79, coverage checks, and cross-airline KPI tests.

## BR-02 — Executive performance

Users shall assess revenue, passenger demand, capacity, load factor,
unit revenue, unit cost, operational reliability, and period trends.

**Evidence:** Executive Overview page and independent KPI reconciliation.

## BR-03 — Network and capacity

Users shall compare routes, airports, capacity, traffic, utilization,
seasonality, and route contribution.

**Evidence:** Network & Capacity Intelligence page and route-level tests.

## BR-04 — Revenue and yield

Users shall analyze passenger revenue, ancillary revenue, yield,
RASK, CASK, contribution, fare mix, and booking patterns.

**Evidence:** Revenue & Yield Intelligence page and financial controls.

## BR-05 — Operations and disruption

Users shall investigate punctuality, delay duration, cancellations,
completion, aircraft utilization, disruption causes, and reactionary
delays.

**Evidence:** Operations & Disruption page, event data, and denominator tests.

## BR-06 — Customer and service

Users shall analyze customer segments, loyalty, booking behavior,
satisfaction, complaints, refunds, and service recovery where supported
by generated data.

**Evidence:** Customer & Service Intelligence page and data-grain checks.

## BR-07 — Transparent scenarios

Users shall evaluate fare, capacity, and fuel-cost changes using
explicit assumptions, formulas, baseline values, and limitations.

**Evidence:** Working what-if interactions and scenario test cases.

## BR-08 — Data quality and lineage

The pipeline shall detect and document deliberate anomalies, maintain
raw-data preservation, and report quality outcomes and reconciliation.

**Evidence:** Quality rules, test output, manifests, and disposition log.

## BR-09 — Reproducibility

The data pipeline shall record its seed, configuration, exact
`ReferenceVersion`, and airline key-map hash. Re-running the same version
with the same configuration shall reproduce the same logical output,
including the same `AirlineId` to `AirlineKey` mapping. Immutable reference
snapshots preserve build reproducibility; they do not claim as-was
historical identity labels under the Type 1 model.

**Evidence:** Deterministic rerun comparison, generator metadata, reference
manifest, key-map hash, and T-78 key-consistency results.

## BR-10 — Semantic model integrity

The model shall define table grain, keys, relationship cardinality,
filter direction, date roles, and handling of transaction-level facts.
`DimAirline` shall use `AirlineKey` for physical relationships, preserve
`AirlineId` as durable business identity, hide `ReferenceVersion` as
technical lineage, expose exactly one selected reference version, and
avoid a second active `DimAirline` filter path to `FactFlightOperations`.

**Evidence:** Model specification, relationship review, reference-version
selection check, and test results.

## BR-11 — KPI correctness

Critical measures shall have documented definitions and reconcile
against independent control calculations. Zero denominators, canceled
flights, refunds, taxes, fees, and other material exclusions shall have
explicit treatment.

**Evidence:** KPI dictionary, control calculations, and reconciliation report.

## BR-12 — Report usability

The report shall provide consistent navigation, appropriate filters,
meaningful tooltips and drill-through, readable labels, and a coherent
visual design.

**Evidence:** Page review, interaction tests, and saved QA evidence.

## BR-13 — Performance and runtime validation

The team shall record refresh results, key row counts, KPI checks,
and relevant responsiveness or performance measurements.

**Evidence:** Power BI Desktop runtime-validation log and test results.

## BR-14 — Security and portfolio hygiene

The repository shall not contain secrets or real passenger personal
information. Generated data, temporary artifacts, and configuration
must be handled deliberately.

**Evidence:** Repository review, .gitignore review, and release checklist.

## BR-15 — Documentation and handover

Another analyst shall be able to understand the model, reproduce the
pipeline, interpret KPIs, run tests, and understand known limitations.
The handover shall document the Type 1 historical limitation, the
manifest-authoritative reference-version process, and the exact synthetic
disclosure.

**Evidence:** Complete documentation, setup instructions, traceability
matrix, reference-version and key-map records, and portfolio case study.

## Requirements status

These are design requirements, not evidence that the features have
already been implemented. OD-01A and OD-01B remain owner-confirmed designs
with formal signature and approval pending. Each requirement must be linked
to its implementation artifact, validation test, evidence location, and
status in REQUIREMENTS_TRACEABILITY.md.
