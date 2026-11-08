"""Stage 5 — Page 03 Revenue & Finance Dashboard validation tests.

Validates the Page 03 report definition in deliverables/power_bi/report/report.json.

Tests cover:
- Page 03 visual registration
- Measure references (all references resolve to registered measures)
- Correct currency formatting
- Date and airline filter behavior
- Revenue/cost reconciliation against source data
- No duplicate visual identifiers
- No broken measure references
- No unsupported financial terminology
- Synthetic-data disclosure
- Regression protection for Pages 01, 02 and 04

Clearly distinguishes static report-definition validation from actual Power BI
Desktop rendering (which is not available in this environment).
"""

import json
import re
from pathlib import Path

import pandas as pd
import pytest

from src.utilities.paths import project_path

REPORT_PATH = project_path("deliverables", "power_bi", "report", "report.json")
MODEL_JSON = project_path("deliverables", "power_bi", "semantic_model", "model.json")
SEMANTIC_MODEL = project_path(
    "deliverables", "power_bi", "semantic_model", "semantic_model.json"
)
DAX_FILE = project_path("deliverables", "power_bi", "dax", "AEROVISION360_Measures.dax")

BOOKING_CSV = project_path("data", "03_curated", "fact_booking_transactions.csv")
COSTS_CSV = project_path("data", "03_curated", "fact_operating_costs.csv")

SYNTHETIC_PROVENANCE = "Synthetic Simulation — Not Actual Airline Performance."


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_report():
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def _load_model_json():
    return json.loads(MODEL_JSON.read_text(encoding="utf-8"))


def _load_semantic_model():
    return json.loads(SEMANTIC_MODEL.read_text(encoding="utf-8"))


def _get_page3(report):
    """Find the Page 03 visual container."""
    for vc in report["config"]["visualContainers"]:
        if vc.get("config", {}).get("name") == "Revenue & Finance":
            return vc
    return None


def _extract_measure_references(report):
    """Extract all measure column references from Page 03 visuals."""
    measures = set()
    page3 = _get_page3(report)
    if page3 is None:
        return measures
    for v in page3.get("visuals", []):
        qs = v.get("query", {}).get("queryState", {})
        if "values" in qs:
            for cat, val in qs["values"].items():
                if isinstance(val, dict) and "measure" in val:
                    m = val["measure"]
                    if isinstance(m, dict) and "target" in m:
                        col = m["target"].get("column")
                        if col:
                            measures.add(col)
    return measures


def _extract_visual_names(page3):
    """Extract all visual names from Page 03."""
    names = []
    for v in page3.get("visuals", []):
        names.append(v.get("name", ""))
    return names


def _extract_slicers(page3):
    """Extract all slicer column references."""
    slicers = []
    for v in page3.get("visuals", []):
        if v.get("visualType") == "slicer":
            qs = v.get("query", {}).get("queryState", {})
            if "values" in qs:
                for cat, val in qs["values"].items():
                    if isinstance(val, dict) and "measure" in val:
                        m = val["measure"]
                        if isinstance(m, dict) and "target" in m:
                            slicers.append(m["target"].get("column"))
    return slicers


# ---------------------------------------------------------------------------
# Expected registered measures (after duplicate removal)
# ---------------------------------------------------------------------------
REGISTERED_MEASURES = {
    "RV_BookingCount", "RV_DistinctBookings", "RV_RevenuePassengers",
    "RV_NonRevenuePassengers", "RV_GrossBookingValueUSD", "RV_RefundAmountUSD",
    "RV_NetPassengerRevenueUSD", "RV_NetFeeRevenueUSD", "RV_NetAncillaryRevenueUSD",
    "RV_TotalOperatingRevenueUSD", "RV_AvgRevenuePerRevenuePassenger", "RV_AvgBookingValueUSD",
    "RV_RevenueCurrentPeriodUSD", "RV_RevenuePriorPeriodUSD", "RV_RevenueGrowthPercent",
    "RV_RevenueYTDUSD", "RV_RevenueByBookingDateUSD",
    "NC_NetOperatingContributionUSD", "NC_RevenueToCostRatio",
    "NC_RevenuePerRevenuePassengerUSD",
    "CX_TotalOperatingCostsUSD", "CX_PositiveCostsUSD", "CX_CostReversalsUSD",
    "CX_NetOperatingCostsUSD", "CX_CostPerFlightOperationUSD", "CX_CostPerRevenuePassengerUSD",
    "CX_CostsCurrentPeriodUSD", "CX_CostsPriorPeriodUSD", "CX_CostGrowthPercent",
    "CX_CostsYTDUSD",
}

# Expected Page 03 visuals (28 total: 7 KPI cards + 6 revenue + 5 cost + 3 financial + 7 slicers)
EXPECTED_PAGE3_VISUALS = 28
EXPECTED_KPI_CARDS = 7
EXPECTED_REVENUE_VISUALS = 6
EXPECTED_COST_VISUALS = 5
EXPECTED_FINANCIAL_VISUALS = 3
EXPECTED_SLICERS = 7

# Unsupported financial terminology
UNSUPPORTED_TERMS = [
    "operating profit", "net profit", "ebitda", "net income",
    "depreciation", "amortization", "financing expense", "tax expense",
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def report():
    return _load_report()


@pytest.fixture
def model_json():
    return _load_model_json()


@pytest.fixture
def semantic_model():
    return _load_semantic_model()


@pytest.fixture
def page3(report):
    p3 = _get_page3(report)
    assert p3 is not None, "Page 03 (Revenue & Finance) not found in report"
    return p3


# ---------------------------------------------------------------------------
# PART F — Validation Tests
# ---------------------------------------------------------------------------

# --- 1. Page 03 visual registration ---

def test_page03_exists(report):
    """Page 03 (Revenue & Finance) is registered in the report."""
    p3 = _get_page3(report)
    assert p3 is not None
    assert p3["config"]["name"] == "Revenue & Finance"


def test_page03_visual_count(page3):
    """Page 03 has the expected number of visuals (28)."""
    assert len(page3["visuals"]) == EXPECTED_PAGE3_VISUALS, (
        f"Expected {EXPECTED_PAGE3_VISUALS} visuals, got {len(page3['visuals'])}"
    )


def test_page03_kpi_card_count(page3):
    """Page 03 has 7 executive KPI cards."""
    cards = [v for v in page3["visuals"] if v.get("visualType") == "card"]
    assert len(cards) == EXPECTED_KPI_CARDS, (
        f"Expected {EXPECTED_KPI_CARDS} KPI cards, got {len(cards)}"
    )


def test_page03_revenue_visual_count(page3):
    """Page 03 has 6 revenue analysis visuals (trend, airline, route, channel, fare class, composition)."""
    revenue_visuals = [
        v for v in page3["visuals"]
        if v.get("name", "").startswith("Page03_Revenue")
        and not v.get("name", "").startswith("Page03_RevenueVs")
    ]
    assert len(revenue_visuals) == EXPECTED_REVENUE_VISUALS, (
        f"Expected {EXPECTED_REVENUE_VISUALS} revenue visuals, got {len(revenue_visuals)}"
    )


def test_page03_cost_visual_count(page3):
    """Page 03 has 5 operating-cost analysis visuals (airline, route, category, positive/reversals, trend)."""
    cost_visuals = [
        v for v in page3["visuals"]
        if v.get("name", "").startswith("Page03_Cost")
    ]
    assert len(cost_visuals) == EXPECTED_COST_VISUALS, (
        f"Expected {EXPECTED_COST_VISUALS} cost visuals, got {len(cost_visuals)}"
    )


def test_page03_financial_visual_count(page3):
    """Page 03 has 3 financial performance visuals."""
    financial_visuals = [
        v for v in page3["visuals"]
        if v.get("name", "").startswith("Page03_Contribution")
        or v.get("name", "").startswith("Page03_RevenueVsCosts")
    ]
    assert len(financial_visuals) == EXPECTED_FINANCIAL_VISUALS, (
        f"Expected {EXPECTED_FINANCIAL_VISUALS} financial visuals, got {len(financial_visuals)}"
    )


def test_page03_slicer_count(page3):
    """Page 03 has 7 slicers for filtering."""
    slicers = [v for v in page3["visuals"] if v.get("visualType") == "slicer"]
    assert len(slicers) == EXPECTED_SLICERS, (
        f"Expected {EXPECTED_SLICERS} slicers, got {len(slicers)}"
    )


# --- 2. Measure references ---

def test_all_measures_registered(report, model_json, semantic_model):
    """Every measure referenced on Page 03 is registered in the semantic model."""
    used_refs = _extract_measure_references(report)
    # Filter to only measure-like references (RV_, CX_, NC_, FL_, DS_, CF_, OP_ prefixes)
    measure_prefixes = ("RV_", "CX_", "NC_", "FL_", "DS_", "CF_", "OP_")
    used_measures = {r for r in used_refs if r.startswith(measure_prefixes)}
    model_tables = {t["name"]: t for t in model_json["model"]["tables"]}
    registered = set()
    for tname in ["fact_booking_transactions", "fact_operating_costs"]:
        for m in model_tables[tname]["measures"]:
            registered.add(m if isinstance(m, str) else m["name"])

    sm_tables = semantic_model["config"]["tables"]
    for tname in ["fact_booking_transactions", "fact_operating_costs"]:
        for m in sm_tables[tname]["measures"]:
            registered.add(m)

    unregistered = used_measures - registered
    assert not unregistered, (
        f"Unregistered measures referenced on Page 03: {unregistered}"
    )


def test_no_broken_measure_references(report, dax_text_fixture):
    """Every measure reference on Page 03 has a DAX definition."""
    used_refs = _extract_measure_references(report)
    # Filter to only measure-like references
    measure_prefixes = ("RV_", "CX_", "NC_", "FL_", "DS_", "CF_", "OP_")
    used_measures = {r for r in used_refs if r.startswith(measure_prefixes)}
    dax_content = dax_text_fixture
    undefined = []
    for m in used_measures:
        pattern = rf"^{re.escape(m)}\s*="
        if not re.search(pattern, dax_content, re.MULTILINE):
            undefined.append(m)
    assert not undefined, (
        f"Measures referenced on Page 03 but not defined in DAX: {undefined}"
    )


# --- 3. Correct currency formatting ---

def test_currency_measures_have_usd_suffix(page3):
    """Measures representing monetary amounts have USD suffix."""
    currency_measures = [
        v for v in page3["visuals"]
        if v.get("visualType") == "card"
    ]
    card_measures = []
    for v in currency_measures:
        qs = v.get("query", {}).get("queryState", {})
        if "values" in qs:
            for cat, val in qs["values"].items():
                if isinstance(val, dict) and "measure" in val:
                    m = val["measure"]
                    if isinstance(m, dict) and "target" in m:
                        col = m["target"].get("column")
                        if col:
                            card_measures.append(col)

    monetary_cards = [
        "RV_TotalOperatingRevenueUSD", "RV_NetPassengerRevenueUSD",
        "RV_NetFeeRevenueUSD", "RV_NetAncillaryRevenueUSD",
        "CX_TotalOperatingCostsUSD", "NC_NetOperatingContributionUSD",
    ]
    for m in monetary_cards:
        assert m in card_measures, f"Monetary measure {m} not found on KPI cards"
        assert m.endswith("USD"), f"Monetary measure {m} should have USD suffix"


def test_ratio_measure_not_currency(page3):
    """Ratio measures don't have USD suffix."""
    ratio_measures = ["NC_RevenueToCostRatio"]
    for m in ratio_measures:
        assert not m.endswith("USD"), f"Ratio measure {m} should not have USD suffix"


# --- 4. Date and airline filter behavior ---

def test_date_slicer_exists(page3):
    """Date slicer is present for date filtering."""
    slicers = _extract_slicers(page3)
    assert "FullDate" in slicers, "Date slicer (FullDate) not found on Page 03"


def test_airline_slicer_exists(page3):
    """Airline slicer is present for airline filtering."""
    slicers = _extract_slicers(page3)
    assert "AirlineName" in slicers, "Airline slicer (AirlineName) not found on Page 03"


def test_route_slicer_exists(page3):
    """Route slicer is present for route filtering."""
    slicers = _extract_slicers(page3)
    assert "RouteCode" in slicers, "Route slicer (RouteCode) not found on Page 03"


def test_currency_slicer_exists(page3):
    """Currency slicer is present for source-currency filtering."""
    slicers = _extract_slicers(page3)
    assert "CurrencyCode" in slicers, "Currency slicer (CurrencyCode) not found on Page 03"


def test_booking_channel_slicer_exists(page3):
    """Booking channel slicer is present."""
    slicers = _extract_slicers(page3)
    assert "ChannelName" in slicers, "Booking channel slicer not found on Page 03"


def test_fare_class_slicer_exists(page3):
    """Fare class slicer is present."""
    slicers = _extract_slicers(page3)
    assert "FareClassCode" in slicers, "Fare class slicer not found on Page 03"


def test_cost_category_slicer_exists(page3):
    """Cost category slicer is present."""
    slicers = _extract_slicers(page3)
    assert "CostCategory" in slicers, "Cost category slicer not found on Page 03"


def test_date_trend_visuals_use_dim_date(page3):
    """Time-trend visuals use dim_date[FullDate] as category."""
    trend_visuals = [
        v for v in page3["visuals"]
        if v.get("visualType") == "lineChart"
    ]
    for v in trend_visuals:
        qs = v.get("query", {}).get("queryState", {})
        if "category" in qs:
            cat = qs["category"].get("category", {})
            target = cat.get("target", {})
            assert target.get("column") == "FullDate", (
                f"Trend visual {v.get('name')} should use FullDate as category column"
            )


# --- 5. Revenue/cost reconciliation ---

def test_revenue_matches_source(page3):
    """RV_TotalOperatingRevenueUSD reconciles to source data."""
    bk = pd.read_csv(BOOKING_CSV, encoding="utf-8")
    expected = (
        bk["NetPassengerRevenueUSD"].sum()
        + bk["NetFeeRevenueUSD"].sum()
        + bk["NetAncillaryRevenueUSD"].sum()
    )
    assert abs(expected - 9052843.41) < 0.01, (
        f"Expected revenue ~$9.05M, got ${expected:,.2f}"
    )


def test_costs_match_source(page3):
    """CX_TotalOperatingCostsUSD reconciles to source data."""
    oc = pd.read_csv(COSTS_CSV, encoding="utf-8")
    expected = oc["CostAmountUSD"].sum()
    assert abs(expected - 194688787.36) < 0.01, (
        f"Expected costs ~$194.69M, got ${expected:,.2f}"
    )


def test_net_operating_contribution_matches_source(page3):
    """NC_NetOperatingContributionUSD = Revenue - Costs."""
    bk = pd.read_csv(BOOKING_CSV, encoding="utf-8")
    oc = pd.read_csv(COSTS_CSV, encoding="utf-8")
    rev = (
        bk["NetPassengerRevenueUSD"].sum()
        + bk["NetFeeRevenueUSD"].sum()
        + bk["NetAncillaryRevenueUSD"].sum()
    )
    cost = oc["CostAmountUSD"].sum()
    expected = rev - cost
    assert abs(expected - (-185635943.95)) < 0.01, (
        f"Expected contribution ~$-185.64M, got ${expected:,.2f}"
    )


def test_refund_treatment(page3):
    """Refunds are stored as positive magnitudes and subtracted in revenue identity."""
    bk = pd.read_csv(BOOKING_CSV, encoding="utf-8")
    assert (bk["RefundAmount"] >= 0).all()
    assert (bk["AncillaryRefundAmount"] >= 0).all()
    assert (bk["FeeRefundAmount"] >= 0).all()


def test_cost_reversal_treatment(page3):
    """Cost reversals are negative amounts."""
    oc = pd.read_csv(COSTS_CSV, encoding="utf-8")
    assert (oc["CostAmount"] < 0).any(), "Expected some negative cost reversals"


# --- 6. No duplicate visual identifiers ---

def test_no_duplicate_visual_names(page3):
    """No duplicate visual names on Page 03."""
    names = _extract_visual_names(page3)
    assert len(names) == len(set(names)), (
        f"Duplicate visual names found: {[n for n in names if names.count(n) > 1]}"
    )


# --- 7. No unsupported financial terminology ---

def test_no_unsupported_terminology_in_dax(dax_text_fixture):
    """DAX measures don't use unsupported financial terms."""
    dax_lower = dax_text_fixture.lower()
    for term in UNSUPPORTED_TERMS:
        assert term not in dax_lower, (
            f"Unsupported financial term '{term}' found in DAX measures"
        )


def test_no_unsupported_terminology_in_report(page3):
    """Page 03 report definition doesn't use unsupported financial terms."""
    report_str = json.dumps(page3).lower()
    for term in UNSUPPORTED_TERMS:
        assert term not in report_str, (
            f"Unsupported financial term '{term}' found in Page 03 report definition"
        )


# --- 8. Synthetic-data disclosure ---

def test_report_carries_disclosure(dax_text_fixture):
    """DAX file carries the synthetic disclosure."""
    assert "Synthetic Simulation" in dax_text_fixture


def test_page03_disclosure(semantic_model):
    """Semantic model disclosure is present."""
    assert semantic_model["config"]["disclosure"] == (
        "Synthetic Simulation - Not Actual Airline Performance"
    )


# --- 9. Regression protection for Pages 01, 02 and 04 ---

def test_pages_01_02_04_unchanged(report):
    """Existing pages are not modified."""
    page_names = [
        vc.get("config", {}).get("name", "")
        for vc in report["config"]["visualContainers"]
    ]
    assert "Executive Overview" in page_names
    assert "Network & Capacity Intelligence" in page_names
    assert "Operations & Disruption" in page_names
    assert "Customer & Service Intelligence" in page_names

    # Page 03 should not be named "OD-04 BLOCKED"
    page3_name = _get_page3(report)["config"]["name"]
    assert "BLOCKED" not in page3_name
    assert page3_name == "Revenue & Finance"


def test_existing_page_visual_counts(report):
    """Existing pages retain their original visual counts."""
    expected_counts = {
        "Executive Overview": 4,
        "Network & Capacity Intelligence": 2,
        "Operations & Disruption": 3,
        "Customer & Service Intelligence": 13,
    }
    for vc in report["config"]["visualContainers"]:
        name = vc.get("config", {}).get("name", "")
        if name in expected_counts:
            actual = len(vc.get("visuals", []))
            assert actual == expected_counts[name], (
                f"Page {name} visual count changed: expected {expected_counts[name]}, got {actual}"
            )


# ---------------------------------------------------------------------------
# DAX fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def dax_text_fixture():
    return DAX_FILE.read_text(encoding="utf-8")
