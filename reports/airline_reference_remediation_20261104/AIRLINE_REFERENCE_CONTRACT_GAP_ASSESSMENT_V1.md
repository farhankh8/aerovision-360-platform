# AEROVISION 360
# Airline Reference Contract Gap Assessment

**Document:** AIRLINE_REFERENCE_CONTRACT_GAP_ASSESSMENT_V1  
**Assessment date:** 2026-11-04T14:56:32.468373+05:30  
**Status:** DRAFT ? OWNER REVIEW REQUIRED  
**Scope:** Airline identity and reference-data contract compatibility  
**Governing baseline:** Data Contract v1.5  

> Synthetic Simulation ? Not Actual Airline Performance

---

## 1. Executive Assessment

The existing ten-airline reference workbook and semantic airline
dimension reconcile by commercial airline name.

The semantic dimension contains ten records with permanent warehouse
keys 1 through 10. The existing identifier crosswalk maps the source
workbook identifiers to semantic dimension identifiers and keys.

The current implementation is structurally usable as a starting point,
but the source workbook and provenance register are not yet fully
compatible with the airline identity and reference-data contract.

No production dimension rebuild is recommended.

No reference-version approval, G3 approval, or G4 authorization
is established by this assessment.

## 2. Verified Source Artifacts

| Artifact | SHA256 |
|---|---|
| Airline reference workbook | `6f9d21365e69b540b8a99cdb461cc5280e570853d5d4ebd5a4f03f7945231c25` |
| Airline ID crosswalk | `1c68eb62e30ed0dd87981bdc5e63cf68a8493f7111150ae84b6df13804b6268d` |
| Crosswalk manifest | `5e148bbc00b9b2e05a9782fc3e99e286a21edc9bab9189c07826ed644e9a9f31` |

All three source hashes matched the previously inspected versions
before this report was created.

## 3. Identity and Key Reconciliation

Ten airline source records were compared with ten semantic DimAirline
records.

Results:

- Ten commercial airline names matched.
- Source identifiers use AIR001 through AIR010.
- Semantic identifiers use AIR-0001 through AIR-0010.
- Source workbook keys use A360-AIR-001 through A360-AIR-010.
- Semantic warehouse keys use integers 1 through 10.
- All ten source IsActive values are blank.
- All ten semantic DimAirline IsActive values are TRUE.

### Required disposition

1. Retain the existing semantic AirlineKey values 1 through 10.
2. Do not regenerate or reorder permanent warehouse keys.
3. Preserve the source-to-semantic crosswalk.
4. Obtain formal owner review and OD-01B approval before treating
   the crosswalk as approved.
5. Do not assume that source identifiers and semantic identifiers
   are interchangeable.

## 4. Reference-Version Compatibility

The source Airlines sheet contains:

`A360-REF-0.3-DRAFT`

The semantic DimAirline sheet contains:

`AIR-2026-11-04-001`

The source workbook version is explicitly marked as a draft.
The semantic dimension version does not, by itself, establish
reference-version approval.

The canonical reference-version format is:

`AIR-YYYY-MM-DD-NNN`

An approved version must be selected through the authoritative
reference manifest and G3-RV-01 process.

No version is approved by this report.

## 5. Airline Source-Sheet Gaps

The Airlines sheet has ten records.

### 5.1 Field-name mappings

| Workbook field | Contract field |
|---|---|
| IATA_Code | AirlineIATACode |
| ICAO_Code | AirlineICAOCode |
| CountryName | HomeCountry |
| CountryISO2 | HomeCountryCode |

These are candidate field mappings. They must be applied only
through a controlled reference transformation.

### 5.2 Required status

All ten source IsActive values are blank.

The semantic dimension currently shows all ten records as active.
That difference must be resolved through documented owner approval
and appropriate supporting evidence.

Do not silently copy the semantic dimension's status into an
approved reference dataset.

### 5.3 Optional attributes

LegalName is populated for nine airlines. Southwest Airlines has
no verified LegalName in the inspected workbook.

LegalName is optional. The missing value must remain null unless
adequate verified evidence becomes available.

The three-digit IATA airline code is supplementary source information.
It is distinct from the two-character AirlineIATACode field and
must not be substituted for it.

## 6. Source Register Provenance Gaps

The Source Register contains 59 records across ten airlines.

The inspected records have unique SourceRecordId values and no
duplicate airline-plus-attribute combinations.

However, the workbook does not contain all required contract fields.

### 6.1 Existing field aliases

| Existing field | Contract field |
|---|---|
| SourceRecordId | SourceRecordID |
| SourcePublisher | SourceOrganization |
| AccessedDate | SourceRetrievedDate |

### 6.2 Missing contract fields

- AttributeValue
- SourceType
- SourceVerifiedDate
- VerificationMethod
- IsAuthoritative
- ReferenceVersion
- CreatedBy
- CreatedDate

The absence of AttributeValue means the current provenance register
cannot independently reconcile the exact asserted value to the
loaded airline identity attribute.

The workbook's VERIFIED label alone is insufficient to close this gap.

### 6.3 Attribute coverage

The 59 inspected provenance records comprise:

| Source attribute | Records |
|---|---:|
| IATA_Code | 10 |
| ICAO_Code | 10 |
| CountryName | 10 |
| CountryISO2 | 10 |
| IATA_AirlineCode | 10 |
| LegalName | 9 |
| **Total** | **59** |

No AirlineName provenance assertion was present for the ten airlines.

The current source register's attribute names also require controlled
mapping to the contract's approved AttributeName vocabulary.

The three-digit IATA airline code must remain outside the canonical
airline identity attributes unless a separately approved requirement
is established.

## 7. Required Remediation Sequence

### R1 ? Formal identity decisions

Obtain formal OD-01A and OD-01B approval records, including selected
decisions, rationale, approver identity and approval dates.

### R2 ? Crosswalk approval

Review all ten mappings, confirm the durable identities, preserve
warehouse keys 1 through 10 and record formal approval.

### R3 ? Provenance completion

For every populated identity attribute, capture the exact asserted
AttributeValue, source organization, URL, source type, retrieved
date, verified date, verification method, authority status and
required version lineage.

Do not fabricate source details, dates or evidence.

### R4 ? Airline status

Resolve the blank source IsActive values through the approved
baseline decision and supporting evidence.

### R5 ? Canonical field transformation

Create a documented transformation specification for the workbook
fields and controlled provenance field aliases.

Preserve original source artifacts and their hashes.

### R6 ? Reference version

Establish one selected reference version, permanent airline key map
and authoritative reference manifest.

### R7 ? Validation

Execute the applicable airline identity tests:

- T-72: Airline identity roster reconciliation.
- T-73: IATA code format and uniqueness.
- T-74: ICAO code format and uniqueness.
- T-75: Attribute-level provenance completeness.
- T-76: Conflict and unsupported-value handling.
- T-77: Reference-to-dimension reconciliation.
- T-78: Reference version, manifest and key integrity.

These tests must have actual execution evidence before being marked PASS.

### R8 ? Gate approval

Complete G3-RV-01, schema freeze and the formal G3 gate review.
Obtain written G4 authorization only after G3 approval.

## 8. Explicit Non-Actions

This assessment does not:

- Modify the airline reference workbook.
- Modify the airline identifier crosswalk.
- Change any permanent AirlineKey.
- Create approved reference CSV files.
- Create or approve a reference manifest.
- Execute G3-RV-01.
- Approve OD-01A or OD-01B.
- Freeze the schema.
- Authorize G4.
- Generate FactFlightOperations or any other fact table.
- Modify production dimensions.

## 9. Current Gate Position

| Item | Status |
|---|---|
| Ten-airline name reconciliation | PASS |
| Semantic AirlineKey alignment | PASS |
| Crosswalk implementation | PRESENT ? PROVISIONAL |
| Airline source contract compatibility | REQUIRES REMEDIATION |
| Provenance completeness | INCOMPLETE |
| OD-01A / OD-01B | PENDING FORMAL APPROVAL |
| G3-RV-01 | NOT EXECUTED |
| Schema freeze | NOT AUTHORIZED |
| G3 | NOT APPROVED |
| G4 | BLOCKED |
| Fact generation | NOT STARTED |

---

**Assessment conclusion:**

The existing airline identity work should be preserved. The next
engineering effort should focus on controlled source-to-contract
reconciliation, provenance completion and formal governance approval.

The existing production dimensional model must not be rebuilt merely
to address these reference-data documentation and approval gaps.
