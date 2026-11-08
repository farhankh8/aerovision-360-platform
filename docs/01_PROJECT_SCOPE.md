# AEROVISION 360 — Project Scope

**Version:** 1.1  
**Status:** Baseline for implementation — OD-01 wording aligned; formal OD-01A/OD-01B approval pending  
**Last updated:** 2026-11-02  
**Project type:** Synthetic operational and financial data business intelligence portfolio  
**Reporting period:** 2025-10-01 through 2026-09-30, inclusive

## 1. Purpose

AEROVISION 360 is a multi-airline intelligence platform for analyzing
financial performance, revenue efficiency, network capacity, operational
reliability, customer experience, and management scenarios.

The deliverable is an evidence-based Power BI project, not merely a
collection of charts. Requirements must trace to implementation, tests,
and recorded evidence.

## 2. Fixed scope

- Ten real airline identities with documented identity attributes and
  attribute-level source provenance required before reference approval,
  plus synthetic operating profiles.
- One inclusive 12-month reporting period.
- Synthetic airports, routes, aircraft, bookings, passengers, revenue,
  costs, operations, disruptions, and customer-feedback data.
- Python-based reproducible data generation and validation.
- Power Query M transformations.
- A documented dimensional semantic model.
- Explicit DAX measures with independent reconciliation.
- Five executive report pages and supporting interactions.
- Data-quality controls, documentation, QA evidence, and a portfolio case study.

The initial planning target is 150,000–250,000 flight-leg records. This
is a target, not a guaranteed output. Confirm the grain, model needs,
storage, and refresh performance before finalizing the generator.

### 2.1 Fixed airline identity roster

The project population is fixed to these ten real airline identities. The
roster is the owner-confirmed intended project population; formal OD-01A
and OD-01B signatures and approval remain pending.

| Airline | IATA | ICAO | Home country | Country code |
|---|---|---|---|---|
| Emirates | EK | UAE | United Arab Emirates | AE |
| Qatar Airways | QR | QTR | Qatar | QA |
| Singapore Airlines | SQ | SIA | Singapore | SG |
| Air India | AI | AIC | India | IN |
| IndiGo | 6E | IGO | India | IN |
| British Airways | BA | BAW | United Kingdom | GB |
| Lufthansa | LH | DLH | Germany | DE |
| Delta Air Lines | DL | DAL | United States | US |
| Southwest Airlines | WN | SWA | United States | US |
| Qantas | QF | QFA | Australia | AU |

Identity attributes are real; each populated attribute must be
source-verified and recorded at attribute level before a reference version
is approved. Operational, customer, booking, revenue, cost, disruption,
feedback, and financial records for these airlines are synthetic
simulations. The roster does not authorize reference-data creation, data
generation, a schema freeze, or a G3 PASS.

## 3. Executive report pages

1. Executive Overview.
2. Network & Capacity Intelligence.
3. Revenue & Yield Intelligence.
4. Operations & Disruption.
5. Customer & Service Intelligence.

Supporting experiences include appropriate drill-through, tooltips,
navigation, bookmarks, dynamic titles, and transparent what-if analysis.

## 4. Core technologies

- Power BI Desktop.
- Power Query M.
- DAX.
- Python.
- Git.
- CSV, Parquet, or Excel where justified by compatibility and use.

Databases, live APIs, cloud deployment, orchestration, and machine
learning are optional extensions. They must not delay a correct core BI
solution.

## 5. Data and governance boundaries

Airline identity attributes — official airline name, IATA code, ICAO
code, home country, country code, and only source-supported group and
legal-name values (legal name is reference/provenance only) — are real
and require attribute-level source verification before reference
approval. Business model is an optional analytical classification, not a
source-verified identity attribute. Operating region is not an airline
identity attribute; derive analytical region from route and airport
geography when needed. All operational, customer, booking, revenue,
cost, disruption, feedback, and financial data are synthetic simulations.
No real passenger personal information may be used.

No generated result may be presented as the actual performance of
Emirates, Qatar Airways, Singapore Airlines, Air India, IndiGo,
British Airways, Lufthansa, Delta Air Lines, Southwest Airlines,
Qantas, or any other named airline. Every dashboard and exported result
must disclose: "Synthetic Simulation — Not Actual Airline Performance".

Raw data must remain distinguishable from staged and curated data.
Intentional data-quality issues must be documented and testable.
Financial definitions, time zones, units, keys, and denominators must
be consistent and explicit.

## 6. Required deliverables

- Reproducible generator and configuration.
- Raw, staging, curated, and reference data as appropriate.
- Schemas, data dictionary, and source manifests.
- Data-quality rules, test results, and reconciliation evidence.
- Documented dimensional model and relationships.
- KPI dictionary and DAX measures.
- Power Query documentation.
- Five executive pages and supporting interactions.
- Power BI Desktop refresh and runtime-validation evidence.
- Test results, performance measurements, and known limitations.
- README, setup instructions, Git history, and portfolio case study.

## 7. Out of scope for the initial release

- Live connections to real airline operational systems.
- Claims that synthetic forecasts predict actual airline outcomes.
- Claims that synthetic operational or financial results are the actual
  performance of any named airline.
- Production airline deployment or certification.
- Mandatory machine-learning models or cloud infrastructure.

These may be considered later through explicit scope change control.

## 8. Acceptance principles

A requirement is complete only when its implementation and evidence
are recorded. Critical calculations must reconcile independently.
Static checks do not replace runtime validation in Power BI Desktop.

No gate may be marked PASS without evidence. Failed or blocked gates
must remain visible until resolved or formally accepted with rationale.

## 9. Change control

Record material scope changes, their rationale, affected requirements,
trade-offs, tests, and approval. Do not silently remove requirements
to make a phase appear complete.

---

## Portfolio Transition Amendment — A360-PA-001
**Effective direction date:** 2026-11-04  
**Status:** Owner-directed portfolio implementation track

The project will proceed as a synthetic-data BI portfolio simulation. The six-dashboard target is:

1. Executive Overview
2. Flight Operations
3. Revenue & Finance
4. Customer Intelligence
5. Route & Network Intelligence
6. Disruption & Risk Analytics

This six-dashboard specification supersedes the earlier five-page planning target for portfolio implementation.

The synthetic-data boundary, ten-airline identity scope, source provenance, and mandatory disclosure remain in force:

**Synthetic Simulation — Not Actual Airline Performance**

This amendment supplements the original scope. Historical scope records are preserved.
