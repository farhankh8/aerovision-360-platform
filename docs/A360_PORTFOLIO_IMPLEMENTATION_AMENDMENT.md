# AEROVISION 360 — Portfolio Implementation Amendment

**Amendment ID:** A360-PA-001
**Date:** 2026-11-04
**Status:** OWNER-DIRECTED PORTFOLIO IMPLEMENTATION BASELINE
**Project:** AEROVISION 360 — Global Multi-Airline Operations & Revenue Intelligence Platform

## 1. Purpose

This amendment proposes a proportionate implementation path for AEROVISION 360 as a synthetic-data Business Intelligence portfolio simulation.

The existing architecture, useful data contracts, source provenance requirements, and quality controls are retained. Governance activities that are disproportionate to a single-developer portfolio project are proposed for simplification.

This amendment does not claim that historical formal gates or approvals have passed.

## 2. Implementation authorization model

Subject to owner approval of this amendment, the project may proceed through a controlled portfolio implementation track.

The portfolio implementation track is distinct from production deployment approval and from the historical G3/G4 gate statuses.

The following work may proceed under the portfolio track:

- Airline and other reference-data preparation.
- Synthetic-data generation.
- Python data engineering and validation.
- RAW, STAGING, and CURATED data preparation.
- Power Query and dimensional modelling.
- DAX measures and KPI reconciliation.
- Power BI report and dashboard development.
- Testing, documentation, and portfolio packaging.

G3 and G4 historical statuses must not be rewritten as APPROVED. Any legacy gate mapping or supersession must be documented transparently.

## 3. Controls retained

The following controls remain mandatory:

1. Real airline identity attributes must have traceable sources or remain null.
2. Operational, booking, customer, financial, disruption, and feedback records must be synthetic.
3. No real passenger personal information may be used.
4. Synthetic data must be reproducible using documented configuration, seeds, and manifests.
5. Data grain, keys, relationships, units, date handling, and business definitions must be documented.
6. Data quality tests must cover uniqueness, completeness, validity, referential integrity, and reconciliation.
7. Financial and operational KPIs must be independently reconciled against source-level calculations.
8. RAW, STAGING, CURATED, and REFERENCE layers must remain distinguishable.
9. Material changes must be recorded.
10. No unsupported production-performance claims may be made.

Required disclosure:

Synthetic Simulation — Not Actual Airline Performance

The disclosure must appear on every dashboard, in relevant tooltips, and in exported report results.

## 4. Airline reference-data policy

Retain the ten-airline scope and the existing OD-01A/OD-01B design decisions.

Real-world identity attributes require source verification. Unverified optional attributes must remain null rather than being invented.

BusinessModelClass remains optional and nullable. OperatingRegion is derived from route and airport geography rather than stored as an airline attribute.

Reference datasets must have a version identifier, source/provenance information, and a reproducibility manifest.

The reference data is for analytical simulation, not a claim of an official airline registry.

## 5. Dashboard scope

The proposed portfolio report scope is six dashboards:

1. Executive Overview
2. Flight Operations
3. Revenue & Finance
4. Customer Intelligence
5. Route & Network Intelligence
6. Disruption & Risk Analytics

This supersedes the earlier five-page planning target only after owner approval and corresponding scope-document updates.

## 6. Proportionate governance

The project will use practical engineering controls instead of production-enterprise approval overhead.

Required evidence will include:

- Owner-approved implementation amendment.
- Versioned schemas and data dictionary.
- Reference-data provenance and manifest.
- Reproducible synthetic-data configuration.
- Automated data-quality tests and results.
- KPI reconciliation evidence.
- Power BI runtime and visual QA evidence.
- Known limitations and synthetic-data disclosure.

An independent reviewer must not be invented. Where no independent reviewer is available, the project must disclose that limitation and use documented self-review and automated checks.

## 7. Historical records

Existing decision records, contract versions, gate records, and audit findings must be preserved as historical evidence.

No historical signature, approval date, reviewer identity, gate PASS, or test PASS may be fabricated.

Any superseded requirement must be identified with its replacement and rationale.

## 8. Implementation sequence

After owner approval:

1. Update the project scope and data contract through controlled revisions.
2. Update the roadmap and progress ledger.
3. Audit the actual Python, Excel, Git, and Power BI environment.
4. Build the airline reference-data workbook and provenance register.
5. Implement the synthetic-data pipeline.
6. Validate RAW, STAGING, and CURATED outputs.
7. Build the Power BI semantic model and DAX measures.
8. Build the six dashboards.
9. Perform reconciliation, runtime, and visual QA.
10. Package the reproducible portfolio deliverable.

## 9. Approval record

**Owner decision:** Direction delegated to the assistant to adopt the recommended portfolio implementation approach, 2026-11-04.

**Approval date:** Not recorded.

**Reviewer:** Not assigned.

**Implementation authorization:** Portfolio implementation direction accepted. Historical G3/G4 approvals are not claimed.

This controlled amendment records the owner's direction to proceed with the recommended portfolio implementation approach. It does not claim a formal signature, independent review, or historical G3/G4 approval.

