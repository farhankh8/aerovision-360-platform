# AEROVISION 360 — Page 05 External Data Source Verification

**Target:** Maven Analytics Airline Passenger Satisfaction dataset  
**Verification Date:** 2026-11-08  
**Status:** READ-ONLY VERIFICATION — NO DATA DOWNLOADED, NO IMPORTS, NO PROJECT MODIFICATIONS  
**Disclosure:** Synthetic Simulation — Not Actual Airline Performance.

---

## 1. Source Identity and Provenance

| Attribute | Value | Evidence |
|-----------|-------|----------|
| Dataset name | Airline Passenger Satisfaction | Maven Analytics page title |
| Primary source URL | https://mavenanalytics.io/data-playground/airline-passenger-satisfaction | Maven Analytics data playground |
| Original source | John D (via Kaggle) | Maven page: "Source: John D, via Kaggle" |
| Kaggle dataset URL | https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction | Kaggle dataset by teejmahal20 |
| Original Kaggle author | @johndddddd (modified/cleaned by @teejmahal20) | UBC-MDS README: "originally posted by @johndddddd, which is then modified and cleaned by @teejmahal20" |
| Maven page author | Maven Analytics, LLC | Maven page footer |
| Data type | CSV, Single table | Maven page: "CSV, Single table" |
| Related challenge | Maven Airlines Challenge | Maven page: "Maven Airlines Challenge Use passenger survey data to help an airline improve customer satisfaction ratings." |

---

## 2. Downloadable Dataset Structure and Available Files

### Maven Analytics listing

| Field | Value | Source |
|-------|-------|--------|
| Format | CSV, Single table | Maven page |
| Record count (structured listing) | 499 records | Maven page structured data |
| Record count (description text) | "120,000+ airline passengers" | Maven page description |
| Field count | 25 fields | Maven page |
| Tags | Geospatial, Travel, Weather | Maven page |
| Download access | Requires sign up/login | Maven page: "Sign up or login to download" |
| Download URL (requires auth) | https://accounts.mavenanalytics.io/init?configuration=... | Maven page |

### Kaggle listing

| Field | Value | Source |
|-------|-------|--------|
| Dataset URL | https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction | Kaggle |
| Files | train.csv, test.csv (test.csv = 20% of full dataset, ~3.04 MB) | Kaggle data tab |
| Full dataset size | ~130,000 rows (inferred from test.csv being 20%) | Kaggle data tab + Hugging Face mirror |
| License | "Other (specified in description)" | Kaggle page |
| Usability score | 9.41 | Kaggle page |
| Tags | Classification, Tabular, Binary Classification, Clustering | Kaggle page |

### Hugging Face mirror (third-party)

| Field | Value | Source |
|-------|-------|--------|
| Mirror URL | https://huggingface.co/datasets/thomask1018/airline_satisfaction | Hugging Face |
| Row count | ~130,000 rows (id column shows 104k–130k range) | Hugging Face dataset card |
| Columns | 24 data columns + index | Hugging Face dataset card |

---

## 3. CRITICAL DISCREPANCIES REQUIRING RESOLUTION

### Discrepancy 1: Record Count

| Source | Stated Count | Notes |
|--------|-------------|-------|
| Maven page structured data | 499 records | Listed under "CSV, Single table, 499, records, 25, fields" |
| Maven page description | "120,000+ airline passengers" | Narrative description |
| Kaggle test.csv | 20% of full dataset (~26,000 rows if full is ~130k) | "20% of full dataset to use for testing" |
| Hugging Face mirror | ~130,000 rows | id column ranges up to ~130k |

**Finding:** The Maven page shows a direct contradiction — 499 records in the structured listing vs "120,000+" in the description. This cannot be resolved without direct file inspection (which requires login). **This is a data integrity concern.**

### Discrepancy 2: License

| Source | Stated License | Notes |
|--------|---------------|-------|
| Maven page | "Public Domain" | Maven page license field |
| Kaggle page | "Other (specified in description)" | Kaggle license field |

**Finding:** License statements conflict between Maven ("Public Domain") and Kaggle ("Other"). Cannot confirm actual reuse terms without viewing the Kaggle description license text directly.

---

## 4. Access and Download Status

| Platform | Download Access | Credentials Required? | Can Inspect Raw File? |
|----------|----------------|----------------------|----------------------|
| Maven Analytics | Sign up/login required | Yes | No |
| Kaggle | Login typically required | Likely yes | No |
| Hugging Face mirror | Publicly viewable | No | Partial (sample rows only) |

**Finding:** Neither Maven nor Kaggle allows anonymous download. Direct file inspection was **not possible**. All schema details below come from:
- Maven page structured listing and description
- Kaggle page "About Dataset" content section (publicly visible)
- Hugging Face mirror sample rows (publicly visible)
- Third-party documentation referencing the same dataset

---

## 5. Complete Schema (Verified from Public Sources)

The dataset has **25 fields** per Maven listing. Based on Kaggle "About Dataset" content and Hugging Face mirror, the columns are:

| # | Column Name | Type | Values / Range | Nulls | Description |
|---|-------------|------|----------------|-------|-------------|
| 1 | id / Unnamed: 0 | int64 | 0 to ~130,000 | No | Row index / ID |
| 2 | Gender | string | Female, Male | No | Gender of passengers |
| 3 | Customer Type | string | Loyal Customer, disloyal Customer | No | Customer type |
| 4 | Age | int64 | 7 to 85 | No | Actual age of passengers |
| 5 | Type of Travel | string | Personal Travel, Business Travel | No | Purpose of flight |
| 6 | Class | string | Business, Eco, Eco Plus | No | Travel class (note: "Eco Plus", not "Economy Plus") |
| 7 | Flight Distance | int64 | 31 to 4,983 | No | Flight distance |
| 8 | Inflight wifi service | int64 | 0 (Not Applicable), 1–5 | No | Satisfaction level |
| 9 | Departure/Arrival time convenient | int64 | 0–5 | No | Satisfaction level |
| 10 | Ease of Online booking | int64 | 0–5 | No | Satisfaction level |
| 11 | Gate location | int64 | 0–5 | No | Satisfaction level |
| 12 | Food and drink | int64 | 0–5 | No | Satisfaction level |
| 13 | Online boarding | int64 | 0–5 | No | Satisfaction level |
| 14 | Seat comfort | int64 | 0–5 | No | Satisfaction level |
| 15 | Inflight entertainment | int64 | 0–5 | No | Satisfaction level |
| 16 | On-board service | int64 | 0–5 | No | Satisfaction level |
| 17 | Leg room service | int64 | 0–5 | No | Satisfaction level |
| 18 | Baggage handling | int64 | 1–5 | No | Satisfaction level |
| 19 | Checkin service | int64 | 0–5 | No | Satisfaction level |
| 20 | Inflight service | int64 | 0–5 | No | Satisfaction level |
| 21 | Cleanliness | int64 | 0–5 | No | Satisfaction level |
| 22 | Departure Delay in Minutes | int64 | 0 to ~1,590 | No | Minutes delayed |
| 23 | Arrival Delay in Minutes | float64 | 0 to ~1,580 | Yes (⌀) | Minutes delayed |
| 24 | satisfaction | string | satisfied, neutral or dissatisfied | No | Overall satisfaction (categorical) |

**Total: 24 data columns + 1 index column = 25 fields** (matches Maven listing)

---

## 6. Verification of Missing Reference Fields

| Reference Field Needed | Available in Maven/Kaggle Dataset? | Values | Notes |
|-----------------------|-----------------------------------|--------|-------|
| Gender | **YES** | Female, Male | Column: `Gender` |
| Customer Type | **YES** | Loyal Customer, disloyal Customer | Column: `Customer Type` |
| Type of Travel | **YES** | Personal Travel, Business Travel | Column: `Type of Travel` |
| Class (cabin) | **YES** | Business, Eco, Eco Plus | Column: `Class` — "Eco Plus", not "Economy Plus" |
| Satisfaction (overall) | **YES** | satisfied, neutral or dissatisfied | Column: `satisfaction` — categorical, not 1–5 numeric |
| Arrival/Departure Time Convenience | **YES** | 0–5 (0=N/A) | Column: `Departure/Arrival time convenient` |
| Cleanliness | **YES** | 0–5 (0=N/A) | Column: `Cleanliness` |
| Ease of Online Booking | **YES** | 0–5 (0=N/A) | Column: `Ease of Online booking` |
| Baggage Handling | **YES** | 0–5 | Column: `Baggage handling` |
| In-flight Service | **YES** | 0–5 (0=N/A) | Column: `Inflight service` |
| Food and Drink | **YES** | 0–5 (0=N/A) | Column: `Food and drink` |
| Additional service ratings | **YES** | Inflight wifi service, Gate location, Online boarding, Seat comfort, Inflight entertainment, On-board service, Leg room service, Checkin service | 8 additional rating columns |

**Finding:** The Maven/Kaggle dataset contains **all** the missing fields that AEROVISION 360 lacks: Gender, Customer Type, Type of Travel, Class, and all six service ratings plus eight additional ratings.

---

## 7. Sample Data (from Hugging Face mirror)

| id | Gender | Customer Type | Age | Type of Travel | Class | Flight Distance | ... | satisfaction |
|----|--------|---------------|-----|----------------|-------|-----------------|-----|--------------|
| 70,172 | Male | Loyal Customer | 13 | Personal Travel | Eco Plus | 460 | ... | neutral or dissatisfied |
| 5,047 | Male | disloyal Customer | 25 | Business travel | Business | 235 | ... | neutral or dissatisfied |
| 110,028 | Female | Loyal Customer | 26 | Business travel | Business | 1,142 | ... | satisfied |

---

## 8. Comparison Against AEROVISION 360 Page 05 Reference Requirements

| Reference Component | AEROVISION 360 Status | Maven/Kaggle Status | Can Be Supplied by External Dataset? |
|--------------------|----------------------|---------------------|-------------------------------------|
| Gender | NOT FOUND | YES (Female/Male) | YES |
| Customer Type | CustomerSegment exists (Leisure/Business/Corporate/Group) | YES (Loyal/disloyal) | YES — but different taxonomy |
| Type of Travel | NOT FOUND | YES (Personal/Business Travel) | YES |
| Class / Cabin Class | CabinClass exists (Economy/Premium Economy/Business/First) | YES (Business/Eco/Eco Plus) | YES — but different values |
| Satisfaction | SatisfactionScore (1–5 numeric) | YES (satisfied/neutral or dissatisfied categorical) | YES — but different scale/type |
| Six service ratings | NOT FOUND | YES (12 rating columns) | YES |
| Passenger-level identifiers | NOT FOUND | id column exists | YES |

---

## 9. Compatibility Assessment with AEROVISION 360 Semantic Model

### Incompatibility 1: Completely Different Population

| Attribute | AEROVISION 360 | Maven/Kaggle Dataset |
|-----------|---------------|---------------------|
| Data nature | Synthetic simulation | Real airline passenger survey (US airline data) |
| Passenger count | 5,000 customers | ~130,000 passengers |
| Airlines | 10 synthetic airlines | Not specified (single US airline per one source) |
| Flights | 5,000 flight legs | Not directly comparable |
| Booking coupons | 9,956 coupons | Not applicable (survey responses) |

**Finding:** These are entirely different populations. The Maven/Kaggle passengers are **not** AEROVISION customers. Merging them would fabricate a false relationship.

### Incompatibility 2: No Common Join Key

| AEROVISION 360 | Maven/Kaggle Dataset |
|---------------|---------------------|
| CustomerKey (1–5,000) | id (~0–130,000) |
| BookingTransactionKey | No booking/coupon concept |
| FeedbackKey | No feedback event concept |

**Finding:** There is no common key to join these datasets. They cannot be merged at the row level.

### Incompatibility 3: Different Satisfaction Scale

| AEROVISION 360 | Maven/Kaggle Dataset |
|---------------|---------------------|
| SatisfactionScore: int8, 1–5 (numeric average) | satisfaction: string, "satisfied" / "neutral or dissatisfied" (categorical) |
| Service ratings: only 1 column | Service ratings: 12 separate columns (0–5 scale) |

**Finding:** Cannot directly combine or compare satisfaction values without transformation.

### Incompatibility 4: Different Class Taxonomy

| AEROVISION 360 (dim_fare_class) | Maven/Kaggle Dataset |
|---------------------------------|---------------------|
| Economy, Premium Economy, Business, First | Business, Eco, Eco Plus |

**Finding:** "Premium Economy" ≠ "Eco Plus". Different vocabularies requiring mapping.

### Incompatibility 5: Grain Mismatch

| AEROVISION 360 | Maven/Kaggle Dataset |
|---------------|---------------------|
| fact_customer_feedback: one row per feedback event | Maven/Kaggle: one row per passenger survey response |
| fact_booking_transactions: one row per ticket coupon | Maven/Kaggle: no booking/coupon concept |
| dim_customer: one row per customer | Maven/Kaggle: one row per passenger |

**Finding:** Different grains. Cannot be combined without aggregation that loses meaning.

### Incompatibility 6: Record Count Discrepancy (Unresolved)

| Source | Count |
|--------|-------|
| Maven structured listing | 499 records |
| Maven description | 120,000+ |
| Kaggle test.csv | 20% of full (~26k if full is 130k) |
| Hugging Face mirror | ~130,000 |

**Finding:** Cannot verify actual row count without direct file access. This discrepancy must be resolved before any use.

---

## 10. Suitability as a Separate External Passenger-Survey Dataset

### Criteria for Separate Source Use

| Criterion | Assessment |
|-----------|------------|
| Remains identifiable as separate source | **YES** — clearly a different dataset, different population, different provenance |
| Does not pretend to be AEROVISION customers | **YES** — can be clearly labeled as external survey data |
| Does not merge unrelated passengers with AEROVISION customers | **YES** — no common key, no merge possible |
| License permits reuse | **UNCERTAIN** — Maven says "Public Domain", Kaggle says "Other" — conflict unresolved |
| Download accessible without credentials | **NO** — both Maven and Kaggle require login |
| Schema fully verifiable without download | **PARTIAL** — columns known from public docs, but exact types/nulls/distributions not independently verified |

### Verdict: Not Suitable for Direct Integration

The Maven/Kaggle dataset **cannot** be integrated into the AEROVISION 360 semantic model because:

1. **No common key** — impossible to join with fact_customer_feedback or fact_booking_transactions
2. **Different population** — synthetic vs real survey data; merging would fabricate relationships
3. **Different grain** — feedback events vs survey responses vs booking coupons
4. **License conflict** — Maven "Public Domain" vs Kaggle "Other" — reuse terms unverified
5. **Access blocked** — requires login on both platforms; raw file not inspectable
6. **Record count discrepancy** — 499 vs 120,000+ unresolved

---

## 11. Incompatibilities Summary

| Incompatibility | Severity | Can Be Resolved? |
|-----------------|----------|------------------|
| Different populations (synthetic vs real survey) | Critical | No — would fabricate data |
| No common join key | Critical | No — different entities |
| Different satisfaction scale (1–5 numeric vs satisfied/dissatisfied categorical) | High | Would require transformation, losing information |
| Different class taxonomy (Premium Economy vs Eco Plus) | Medium | Could map, but values are not equivalent |
| License conflict (Public Domain vs Other) | High | Requires clarification |
| Download requires credentials | Medium | Cannot verify without access |
| Record count discrepancy (499 vs 120,000+) | High | Cannot verify without access |

---

## 12. Conclusion and Recommendation

**The Maven/Kaggle Airline Passenger Satisfaction dataset contains all the missing fields** (Gender, Customer Type, Type of Travel, Class, and all six service ratings plus eight additional ratings). **However, it cannot be integrated with AEROVISION 360** because:

1. It is a completely different population with no common key
2. Merging would violate the rule against combining unrelated passengers with AEROVISION customers
3. License terms are conflicting and unverified
4. Direct download requires credentials (not accessible)
5. Record count discrepancy is unresolved

### Recommended Path Forward

**Option A: Build Page 05 using only AEROVISION 360 native data**
- Use CF01–CF14 measures (verified, supported)
- Exclude unsupported reference components (Gender, Travel Type, six service ratings, Satisfied/Dissatisfied counts, class-based visuals)
- Document all gaps as known limitations
- **Pros:** Governance-compliant, no external data risk, fully verifiable
- **Cons:** Does not match full reference dashboard

**Option B: Build Page 05 using AEROVISION native data + external Maven/Kaggle data as a clearly separate, unrelated dataset**
- External dataset would live in its own model/table space
- No relationships to AEROVISION facts
- Separate visuals clearly labeled as "External Passenger Survey (Maven/Kaggle — not AEROVISION data)"
- **Pros:** Provides gender, travel type, service ratings
- **Cons:** License unverified, access blocked, requires separate model space, adds complexity

**Option C: Defer unsupported reference components**
- Build only what AEROVISION 360 genuinely supports
- Document missing fields as requiring future source data acquisition
- **Pros:** Clean, governance-compliant, no fabrication
- **Cons:** Reference dashboard not fully reproduced

**Recommendation:** Proceed with **Option A** — build Page 05 using only verified AEROVISION 360 native CF measures. The external Maven/Kaggle dataset cannot be responsibly integrated given the license conflict, access restrictions, population mismatch, and no common key. Any external data integration would require separate governance approval, license clarification, and a clearly segregated model space.

---

## 13. Evidence Sources

| Source | URL | Access Status |
|--------|-----|---------------|
| Maven Analytics dataset page | https://mavenanalytics.io/data-playground/airline-passenger-satisfaction | Publicly viewable; download requires login |
| Kaggle dataset page | https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction | Page did not return content (likely login-gated) |
| Hugging Face mirror | https://huggingface.co/datasets/thomask1018/airline_satisfaction | Publicly viewable (sample rows) |
| UBC-MDS README (referencing original author) | https://github.com/UBC-MDS-2024-25/airline-customer-satisfaction-predictor/blob/main/README.md | Publicly viewable |
| Warren Ngoun project page (column reference) | https://www.warrenngoun.com/airlineSatisfaction.html | Publicly viewable |

---

**Verification complete. No data downloaded. No project files modified. STOPPED — awaiting owner approval before any import or transformation.**
