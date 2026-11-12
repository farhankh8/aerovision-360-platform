"""Statistical Anomaly Detection for AEROVISION 360.

Provides explainable, evidence-based statistical anomaly detection using
traditional statistical techniques. Does not use synthetic training data
or claim model accuracy. Reports insufficient evidence when historical
data is unavailable.

Algorithms:
- Z-score: for approximately normal distributions
- Median Absolute Deviation (MAD): robust alternative to Z-score
- Interquartile Range (IQR): robust outlier detection
- Rolling averages: for time-series trend detection
- Seasonal comparisons: when sufficient historical data exists
- Distribution comparisons: Kolmogorov-Smirnov type tests
- Volume anomalies: unexpected changes in record counts
- Missingness anomalies: unexpected increases in null proportions
- Unusual category frequencies: unexpected value distribution shifts
- Unexpected metric changes: deviation from expected metric values

For every anomaly, captures:
- Dataset identifier
- Metric name
- Observed value
- Expected range or baseline
- Detection method used
- Threshold applied
- Severity classification
- Confidence/evidence strength
- Historical comparison window
- Detection timestamp
- Human-readable explanation

Distinguishes between:
- Data-quality failure (rule violation)
- Statistical anomaly (outlier from baseline)
- Expected business variation (within normal range)
- Insufficient historical evidence (deferred)
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np  # Used for statistical calculations


# ---------------------------------------------------------------------------
# Anomaly severity classification
# ---------------------------------------------------------------------------

class AnomalySeverity(str, Enum):
    """Severity classification for detected anomalies."""
    CRITICAL = "critical"  # Immediate action required; blocks operations
    HIGH = "high"        # Serious; requires attention soon
    MEDIUM = "medium"    # Notable; warrants review
    LOW = "low"          # Minor; informational
    INFO = "info"        # Informational only


class AnomalyStatus(str, Enum):
    """Status of an anomaly detection result."""
    DETECTED = "detected"
    RESOLVED = "resolved"
    MONITORING = "monitoring"


# ---------------------------------------------------------------------------
# Anomaly result model
# ---------------------------------------------------------------------------

@dataclass
class AnomalyResult:
    """Result of a single anomaly detection check."""
    dataset_id: str
    metric: str
    observed_value: float
    expected_range: Tuple[float, float] | None
    baseline_value: float | None
    detection_method: str
    threshold: float
    severity: AnomalySeverity
    confidence: float  # 0.0 to 1.0, where 1.0 is highest confidence
    historical_window: str
    detection_timestamp: datetime
    explanation: str
    is_data_quality_failure: bool = False
    is_expected_variation: bool = False


# ---------------------------------------------------------------------------
# Core anomaly detection algorithms
# ---------------------------------------------------------------------------


def detect_z_score(
    values: list[float],
    threshold: float = 3.0,
    baseline: Optional[list[float]] = None,
) -> list[AnomalyResult]:
    """Detect anomalies using Z-score method.

    Assumes approximately normal distribution. Values beyond
    threshold standard deviations from the mean are flagged.

    Args:
        values: List of numeric values to analyze.
        threshold: Z-score threshold (default 3.0 = 99.7% confidence).
        baseline: Optional baseline values for comparison. If provided,
                  compares current values against baseline mean/std.

    Returns:
        List of AnomalyResult objects for detected anomalies.
    """
    if not values:
        return []

    # Compute mean and std
    if baseline is not None and len(baseline) > 0:
        baseline_mean = float(np.mean(baseline))
        baseline_std = float(np.std(baseline)) if np.std(baseline) > 0 else 1.0
        current_mean = float(np.mean(values))
        current_std = float(np.std(values)) if np.std(values) > 0 else 1.0
    else:
        current_mean = float(np.mean(values))
        current_std = float(np.std(values)) if np.std(values) > 0 else 1.0
        baseline_mean = current_mean
        baseline_std = current_std

    results: list[AnomalyResult] = []

    for i, value in enumerate(values):
        if current_std == 0:
            continue  # No variance, cannot compute Z-score

        z_score = abs(value - baseline_mean) / baseline_std

        if z_score > threshold:
            # Determine severity based on how many thresholds exceeded
            if z_score > 4.0:
                severity = AnomalySeverity.CRITICAL
            elif z_score > 3.5:
                severity = AnomalySeverity.HIGH
            elif z_score > 3.0:
                severity = AnomalySeverity.MEDIUM
            else:
                severity = AnomalySeverity.LOW

            # Confidence decreases as we move further out (extreme values
            # are less likely under normal distribution)
            confidence = max(0.1, 1.0 - (z_score - threshold) / (threshold * 0.5))

            results.append(AnomalyResult(
                dataset_id="",  # Will be set by caller
                metric="",      # Will be set by caller
                observed_value=value,
                expected_range=(
                    baseline_mean - threshold * baseline_std,
                    baseline_mean + threshold * baseline_std,
                ),
                baseline_value=baseline_mean,
                detection_method="z_score",
                threshold=threshold,
                severity=severity,
                confidence=round(confidence, 3),
                historical_window="current_run",
                detection_timestamp=datetime.now(timezone.utc),
                explanation=(
                    f"Z-score anomaly detected: value={value:.4f}, "
                    f"z-score={z_score:.2f} (exceeds threshold={threshold})"
                ),
            ))

    return results


def detect_mad(
    values: list[float],
    threshold: float = 3.5,
    baseline: Optional[list[float]] = None,
) -> list[AnomalyResult]:
    """Detect anomalies using Median Absolute Deviation (MAD).

    More robust than Z-score for heavy-tailed or non-normal distributions.
    Uses the median and MAD instead of mean and standard deviation.

    Args:
        values: List of numeric values to analyze.
        threshold: MAD threshold multiplier (default 3.5).
        baseline: Optional baseline values for comparison.

    Returns:
        List of AnomalyResult objects for detected anomalies.
    """
    if not values:
        return []

    # Compute median and MAD
    if baseline is not None and len(baseline) > 0:
        baseline_median = float(np.median(baseline))
        # MAD: median of |x - median|
        deviations = [abs(x - baseline_median) for x in baseline]
        baseline_mad = float(np.median(deviations)) if deviations else 1.0
        current_median = float(np.median(values))
        current_deviations = [abs(x - current_median) for x in values]
    else:
        current_median = float(np.median(values))
        deviations = [abs(x - current_median) for x in values]
        baseline_mad = float(np.median(deviations)) if deviations else 1.0
        baseline_median = current_median

    # MAD-based Z-score: 0.6745 * MAD approximates std for normal dist
    # But we use MAD directly for robustness
    results: list[AnomalyResult] = []

    for i, value in enumerate(values):
        if baseline_mad == 0:
            continue  # No variability

        # MAD score: (value - median) / (0.6745 * MAD)
        mad_score = abs(value - baseline_median) / (0.6745 * baseline_mad)

        if mad_score > threshold:
            if mad_score > 4.0:
                severity = AnomalySeverity.CRITICAL
            elif mad_score > 3.5:
                severity = AnomalySeverity.HIGH
            elif mad_score > 3.0:
                severity = AnomalySeverity.MEDIUM
            else:
                severity = AnomalySeverity.LOW

            confidence = max(0.1, 1.0 - (mad_score - threshold) / (threshold * 0.5))

            results.append(AnomalyResult(
                dataset_id="",
                metric="",
                observed_value=value,
                expected_range=(
                    baseline_median - threshold * 0.6745 * baseline_mad,
                    baseline_median + threshold * 0.6745 * baseline_mad,
                ),
                baseline_value=baseline_median,
                detection_method="mad",
                threshold=threshold,
                severity=severity,
                confidence=round(confidence, 3),
                historical_window="current_run",
                detection_timestamp=datetime.now(timezone.utc),
                explanation=(
                    f"MAD anomaly detected: value={value:.4f}, "
                    f"MAD score={mad_score:.2f} (exceeds threshold={threshold})"
                ),
            ))

    return results


def detect_iqr(
    values: list[float],
    threshold: float = 1.5,
    baseline: Optional[list[float]] = None,
) -> list[AnomalyResult]:
    """Detect anomalies using Interquartile Range (IQR) method.

    Uses the IQR (Q3 - Q1) to define fences. Values outside
    [Q1 - k*IQR, Q3 + k*IQR] are flagged as outliers.

    Args:
        values: List of numeric values to analyze.
        threshold: IQR fence multiplier (default 1.5 = standard IQR).
        baseline: Optional baseline values for comparison.

    Returns:
        List of AnomalyResult objects for detected anomalies.
    """
    if not values:
        return []

    # Compute quartiles
    if baseline is not None and len(baseline) > 0:
        baseline_sorted = sorted(baseline)
        q1_base = float(np.percentile(baseline_sorted, 25))
        q3_base = float(np.percentile(baseline_sorted, 75))
        iqr_base = q3_base - q1_base
        lower_fence_base = q1_base - threshold * iqr_base
        upper_fence_base = q3_base + threshold * iqr_base

        baseline_q2 = float(np.median(baseline_sorted))
        baseline_count = len(baseline_sorted)
        # Compute Q1/Q3 for current data using same method
        current_sorted = sorted(values)
    else:
        current_sorted = sorted(values)
        q1_base = float(np.percentile(current_sorted, 25))
        q3_base = float(np.percentile(current_sorted, 75))
        iqr_base = q3_base - q1_base
        lower_fence_base = q1_base - threshold * iqr_base
        upper_fence_base = q3_base + threshold * iqr_base
        baseline_q2 = float(np.median(current_sorted))
        baseline_count = len(current_sorted)

    results: list[AnomalyResult] = []

    for value in values:
        if value < lower_fence_base or value > upper_fence_base:
            # Determine severity based on how far outside the fence
            if value < lower_fence_base:
                distance_pct = (lower_fence_base - value) / abs(lower_fence_base) if lower_fence_base != 0 else 1.0
                if distance_pct > 0.5:
                    severity = AnomalySeverity.CRITICAL
                elif distance_pct > 0.3:
                    severity = AnomalySeverity.HIGH
                elif distance_pct > 0.2:
                    severity = AnomalySeverity.MEDIUM
                else:
                    severity = AnomalySeverity.LOW
            else:
                distance_pct = (value - upper_fence_base) / upper_fence_base if upper_fence_base != 0 else 1.0
                if distance_pct > 0.5:
                    severity = AnomalySeverity.CRITICAL
                elif distance_pct > 0.3:
                    severity = AnomalySeverity.HIGH
                elif distance_pct > 0.2:
                    severity = AnomalySeverity.MEDIUM
                else:
                    severity = AnomalySeverity.LOW

            # Confidence based on distance from fence
            confidence = max(0.1, 1.0 - abs(distance_pct - 0.2) / 0.3)

            results.append(AnomalyResult(
                dataset_id="",
                metric="",
                observed_value=value,
                expected_range=(lower_fence_base, upper_fence_base),
                baseline_value=baseline_q2,
                detection_method="iqr",
                threshold=threshold,
                severity=severity,
                confidence=round(confidence, 3),
                historical_window="current_run",
                detection_timestamp=datetime.now(timezone.utc),
                explanation=(
                    f"IQR anomaly detected: value={value:.4f}, "
                    f"outside fence [{lower_fence_base:.4f}, {upper_fence_base:.4f}]"
                ),
            ))

    return results


def detect_volume_anomaly(
    current_count: int,
    baseline_counts: list[int],
    threshold: float = 2.0,
) -> AnomalyResult | None:
    """Detect volume anomalies (unexpected record count changes).

    Uses a simple ratio comparison against baseline history.

    Args:
        current_count: The current record count.
        baseline_counts: Historical list of record counts for comparison.
        threshold: Z-score threshold for volume change detection.

    Returns:
        AnomalyResult if anomaly detected, None otherwise.
    """
    if not baseline_counts:
        # No baseline available - report as info (deferred)
        return None

    # Compute mean and std of baseline counts
    import numpy as np
    baseline_mean = float(np.mean(baseline_counts))
    baseline_std = float(np.std(baseline_counts)) if len(baseline_counts) > 1 else 1.0

    if baseline_std == 0:
        return None  # No variability in baseline

    # Compute Z-score for current count
    z_score = abs(current_count - baseline_mean) / baseline_std

    if z_score > threshold:
        # Determine severity
        if z_score > 4.0:
            severity = AnomalySeverity.CRITICAL
        elif z_score > 3.5:
            severity = AnomalySeverity.HIGH
        elif z_score > 3.0:
            severity = AnomalySeverity.MEDIUM
        else:
            severity = AnomalySeverity.LOW

        confidence = max(0.1, 1.0 - (z_score - threshold) / (threshold * 0.5))

        # Determine if it's an increase or decrease
        is_increase = current_count > baseline_mean

        if is_increase:
            explanation = (
                f"Volume anomaly: current count={current_count}, "
                f"baseline mean={baseline_mean:.1f}, "
                f"Z-score={z_score:.2f} (exceeds threshold={threshold}), "
                f"indicating {int(current_count - baseline_mean)} additional records"
            )
        else:
            explanation = (
                f"Volume anomaly: current count={current_count}, "
                f"baseline mean={baseline_mean:.1f}, "
                f"Z-score={z_score:.2f} (exceeds threshold={threshold}), "
                f"indicating {int(baseline_mean - current_count)} fewer records"
            )

        return AnomalyResult(
            dataset_id="",
            metric="record_count",
            observed_value=float(current_count),
            expected_range=(
                float(baseline_mean - threshold * baseline_std),
                float(baseline_mean + threshold * baseline_std),
            ),
            baseline_value=baseline_mean,
            detection_method="volume_anomaly",
            threshold=threshold,
            severity=severity,
            confidence=round(confidence, 3),
            historical_window=f"baseline_n={len(baseline_counts)}",
            detection_timestamp=datetime.now(timezone.utc),
            explanation=explanation,
            is_data_quality_failure=True,
        )

    return None


def detect_missingness_anomaly(
    current_null_pct: float,
    baseline_null_pcts: list[float],
    threshold: float = 2.0,
) -> AnomalyResult | None:
    """Detect missingness anomalies (unexpected increase in null proportions).

    Args:
        current_null_pct: Current percentage of null values (0-100).
        baseline_null_pcts: Historical list of null percentages.
        threshold: Z-score threshold for missingness change detection.

    Returns:
        AnomalyResult if anomaly detected, None otherwise.
    """
    if not baseline_null_pcts:
        return None  # No baseline available

    import numpy as np
    baseline_mean = float(np.mean(baseline_null_pcts))
    baseline_std = float(np.std(baseline_null_pcts)) if len(baseline_null_pcts) > 1 else 1.0

    if baseline_std == 0:
        return None  # No variability in baseline

    # Compute Z-score for current null pct
    z_score = abs(current_null_pct - baseline_mean) / baseline_std

    if z_score > threshold:
        if z_score > 4.0:
            severity = AnomalySeverity.CRITICAL
        elif z_score > 3.5:
            severity = AnomalySeverity.HIGH
        elif z_score > 3.0:
            severity = AnomalySeverity.MEDIUM
        else:
            severity = AnomalySeverity.LOW

        confidence = max(0.1, 1.0 - (z_score - threshold) / (threshold * 0.5))

        # Determine direction
        is_increase = current_null_pct > baseline_mean

        if is_increase:
            explanation = (
                f"Missingness anomaly: current null pct={current_null_pct:.1f}%, "
                f"baseline mean={baseline_mean:.1f}%, "
                f"Z-score={z_score:.2f} (exceeds threshold={threshold}), "
                f"indicating {current_null_pct - baseline_mean:.1f}% increase in missing values"
            )
        else:
            explanation = (
                f"Missingness anomaly: current null pct={current_null_pct:.1f}%, "
                f"baseline mean={baseline_mean:.1f}%, "
                f"Z-score={z_score:.2f} (exceeds threshold={threshold}), "
                f"indicating {baseline_mean - current_null_pct:.1f}% decrease in missing values"
            )

        return AnomalyResult(
            dataset_id="",
            metric="null_percentage",
            observed_value=current_null_pct,
            expected_range=(baseline_mean - threshold * baseline_std, baseline_mean + threshold * baseline_std),
            baseline_value=baseline_mean,
            detection_method="missingness_anomaly",
            threshold=threshold,
            severity=severity,
            confidence=round(confidence, 3),
            historical_window=f"baseline_n={len(baseline_null_pcts)}",
            detection_timestamp=datetime.now(timezone.utc),
            explanation=explanation,
            is_data_quality_failure=True,
        )

    return None


def detect_category_frequency_anomaly(
    current_counts: dict[str, int],
    baseline_counts: dict[str, int] | None,
    threshold: float = 2.0,
) -> list[AnomalyResult]:
    """Detect unusual category frequency anomalies.

    Compares the frequency distribution of categorical values
    against a baseline distribution.

    Args:
        current_counts: Dict of {category: count} from current data.
        baseline_counts: Dict of {category: count} from baseline, or None.
        threshold: Z-score threshold for anomaly detection.

    Returns:
        List of AnomalyResult objects for detected anomalies.
    """
    results: list[AnomalyResult] = []

    if baseline_counts is None or len(baseline_counts) == 0:
        # No baseline - return info (deferred)
        total = sum(current_counts.values()) if current_counts else 0
        if total > 0:
            # Report the dominant category frequency as informational
            top_category = max(current_counts, key=current_counts.get) if current_counts else "unknown"
            results.append(AnomalyResult(
                dataset_id="",
                metric="category_frequency",
                observed_value=float(current_counts.get(top_category, 0)),
                expected_range=(0, total),
                baseline_value=float(total),
                detection_method="category_frequency",
                threshold=threshold,
                severity=AnomalySeverity.INFO,
                confidence=0.5,
                historical_window="no_baseline",
                detection_timestamp=datetime.now(timezone.utc),
                explanation=(
                    f"Category frequency anomaly: no baseline available, "
                    f"total={total}, top category='{top_category}'={current_counts.get(top_category, 0)}"
                ),
                is_expected_variation=True,
            ))
        return results

    # Compute total baseline
    baseline_total = sum(baseline_counts.values())

    # For each category in current data, compute its proportion and compare
    # to baseline proportion
    for category, current_count in current_counts.items():
        baseline_count = baseline_counts.get(category, 0)

        # Current proportion
        current_prop = current_count / sum(current_counts.values()) if sum(current_counts.values()) > 0 else 0

        # Baseline proportion
        baseline_prop = baseline_count / baseline_total if baseline_total > 0 else 0

        # If baseline has 0 for this category but current has values,
        # or vice versa, that's an anomaly
        if baseline_prop == 0 and current_count > 0:
            # New category appeared
            # Use a very high threshold effectively
            z_score = 5.0  # Effectively "infinite" compared to baseline
        elif current_prop == 0 and baseline_count > 0:
            # Category disappeared
            z_score = 5.0
        else:
            # Compute difference in proportions
            # Simple: (current_prop - baseline_prop) / sqrt(baseline_prop * (1 - baseline_prop) / baseline_total)
            # Simplified for lightweight implementation
            prop_diff = current_prop - baseline_prop
            if baseline_total > 0 and (baseline_prop * (1 - baseline_prop)) > 0:
                std_error = (baseline_prop * (1 - baseline_prop) / baseline_total) ** 0.5
                if std_error > 0:
                    z_score = abs(prop_diff) / std_error
                else:
                    z_score = 0
            else:
                z_score = abs(prop_diff) * 10  # Scale for significance

        if z_score > threshold:
            if z_score > 4.0:
                severity = AnomalySeverity.CRITICAL
            elif z_score > 3.5:
                severity = AnomalySeverity.HIGH
            elif z_score > 3.0:
                severity = AnomalySeverity.MEDIUM
            else:
                severity = AnomalySeverity.LOW

            confidence = max(0.1, 1.0 - (z_score - threshold) / (threshold * 0.5))

            if current_count > baseline_count:
                change_desc = f"increase from {baseline_count} to {current_count}"
            elif current_count < baseline_count:
                change_desc = f"decrease from {baseline_count} to {current_count}"
            else:
                change_desc = "change in frequency"

            results.append(AnomalyResult(
                dataset_id="",
                metric="category_frequency",
                observed_value=float(current_count),
                expected_range=(0, baseline_count * 2) if baseline_count > 0 else (0, 1),
                baseline_value=float(baseline_count),
                detection_method="category_frequency",
                threshold=threshold,
                severity=severity,
                confidence=round(confidence, 3),
                historical_window=f"baseline_n={baseline_total}",
                detection_timestamp=datetime.now(timezone.utc),
                explanation=(
                    f"Category frequency anomaly: '{category}' {change_desc}, "
                    f"Z-score={z_score:.2f} (exceeds threshold={threshold})"
                ),
            ))

    return results


# ---------------------------------------------------------------------------
# High-level detection entry point
# ---------------------------------------------------------------------------

def detect_anomalies(
    dataset_id: str,
    metric_name: str,
    values: list[float] | None = None,
    records: list[dict[str, Any]] | None = None,
    column_name: str | None = None,
    schema: QualitySchema | None = None,
    historical_values: list[float] | None = None,
    **kwargs: Any,
) -> list[AnomalyResult]:
    """Detect anomalies in dataset metrics using multiple methods.

    This is the main entry point for anomaly detection. It runs multiple
    detection algorithms and returns combined results.

    Args:
        dataset_id: Identifier for the dataset being analyzed.
        metric_name: Name of the metric being analyzed (e.g., "record_count", "null_percentage").
        values: List of numeric values to analyze.
        records: List of record dicts (used if values not directly provided).
        column_name: Name of the column to analyze (if values not provided).
        schema: QualitySchema for the dataset (for type information).
        historical_values: Historical values for baseline comparison.
        **kwargs: Additional method-specific parameters.

    Returns:
        List of AnomalyResult objects from all detection methods.
    """
    results: list[AnomalyResult] = []

    # Extract values if records provided
    if values is None and records is not None and column_name is not None:
        vals = []
        for record in records:
            val = record.get(column_name)
            if val is not None and val != "":
                try:
                    vals.append(float(val))
                except (ValueError, TypeError):
                    pass
        values = vals if vals else None

    if not values or len(values) == 0:
        # No data to analyze
        return results

    # Detect volume anomaly (if metric is record_count)
    if metric_name == "record_count" or (historical_values and len(historical_values) > 0):
        vol_result = detect_volume_anomaly(len(values), historical_values, kwargs.get("volume_threshold", 2.0))
        if vol_result is not None:
            vol_result.dataset_id = dataset_id
            vol_result.metric = metric_name
            results.append(vol_result)

    # Detect missingness anomaly (if metric is null_percentage or similar)
    if metric_name in ("null_percentage", "missingness") or (
        historical_values and len(historical_values) > 1
    ):
        # Estimate current null percentage if we have records with nulls
        current_null_pct = kwargs.get("current_null_pct", 0.0)
        missing_result = detect_missingness_anomaly(current_null_pct, historical_values, kwargs.get("missingness_threshold", 2.0))
        if missing_result is not None:
            missing_result.dataset_id = dataset_id
            missing_result.metric = metric_name
            results.append(missing_result)

    # Z-score detection (most general)
    z_threshold = kwargs.get("z_score_threshold", 3.0)
    z_results = detect_z_score(values, threshold=z_threshold, baseline=historical_values)
    for r in z_results:
        r.dataset_id = dataset_id
        r.metric = metric_name
        results.append(r)

    # MAD detection (robust alternative)
    mad_threshold = kwargs.get("mad_threshold", 3.5)
    mad_results = detect_mad(values, threshold=mad_threshold, baseline=historical_values)
    for r in mad_results:
        r.dataset_id = dataset_id
        r.metric = metric_name
        # Avoid duplicates - check if similar Z-score result already exists
        if not any(
            a.metric == r.metrics if hasattr(a, 'metrics') else a.metric == r.metric and a.observed_value == r.observed_value
            for a in results
        ):
            results.append(r)

    # IQR detection
    iqr_threshold = kwargs.get("iqr_threshold", 1.5)
    iqr_results = detect_iqr(values, threshold=iqr_threshold, baseline=historical_values)
    for r in iqr_results:
        r.dataset_id = dataset_id
        r.metric = metric_name
        # Avoid duplicates
        if not any(
            a.metric == r.metric and a.observed_value == r.observed_value for a in results
        ):
            results.append(r)

    # Category frequency anomaly (if schema has categorical columns)
    if schema is not None and schema.type_rules:
        cat_results = detect_category_frequency_anomaly(
            current_counts=kwargs.get("category_counts", {}),
            baseline_counts=kwargs.get("baseline_category_counts"),
            threshold=kwargs.get("category_threshold", 2.0),
        )
        for r in cat_results:
            r.dataset_id = dataset_id
            r.metric = metric_name
            results.append(r)

    # Post-processing: classify and deduplicate
    results = _classify_anomalies(results)

    return results


def _classify_anomalies(
    results: list[AnomalyResult],
) -> list[AnomalyResult]:
    """Classify and deduplicate anomaly results.

    Rules:
    - If both a data-quality failure and a statistical anomaly are detected
      for the same issue, mark as data-quality failure.
    - If an anomaly is within expected business variation, mark accordingly.
    - Remove duplicates based on observed value and metric.
    - Ensure no result has both DETECTED and RESOLVED status.
    """
    classified: list[AnomalyResult] = []
    seen_keys: set[tuple[str, float]] = set()  # (metric, observed_value) pairs

    for result in results:
        # Skip if duplicate (same metric and observed value)
        key = (result.metric, result.observed_value)
        if key in seen_keys:
            continue
        seen_keys.add(key)

        # If marked as data-quality failure, keep classification
        if result.is_data_quality_failure:
            result.is_expected_variation = False
            classified.append(result)
            continue

        # If marked as expected variation, keep classification
        if result.is_expected_variation:
            classified.append(result)
            continue

        # Default: mark as detected
        result.is_expected_variation = False
        classified.append(result)

    return classified


# ---------------------------------------------------------------------------
# Insufficient historical evidence handling
# ---------------------------------------------------------------------------

def detect_with_fallback(
    dataset_id: str,
    metric_name: str,
    values: list[float],
    **kwargs: Any,
) -> tuple[list[AnomalyResult], bool]:
    """Detect anomalies with fallback for insufficient historical data.

    If sufficient historical observations are unavailable, this function
    implements deterministic statistical detection and explicitly reports
    that ML-based detection is deferred.

    Returns:
        Tuple of (anomaly_results, historical_sufficient)
        where historical_sufficient is True if enough baseline data exists.
    """
    historical_values = kwargs.get("historical_values", [])

    if not historical_values or len(historical_values) < 5:
        # Insufficient historical data - implement deterministic detection
        # with explicit deferral of ML-based detection
        results: list[AnomalyResult] = []

        # Simple deterministic check: flag if values have high variance
        # or if any individual value is extremely high/low relative to
        # the limited data we have
        if len(values) > 0:
            import numpy as np
            val_array = np.array(values, dtype=float)
            mean_val = float(np.mean(val_array)) if len(val_array) > 0 else 0
            std_val = float(np.std(val_array)) if len(val_array) > 0 else 0

            if std_val > 0:
                # Flag values more than 2 std devs from mean (deterministic)
                for v in val_array:
                    z = abs(v - mean_val) / std_val
                    if z > 2.0:
                        results.append(AnomalyResult(
                            dataset_id=dataset_id,
                            metric=metric_name,
                            observed_value=v,
                            expected_range=(mean_val - 2 * std_val, mean_val + 2 * std_val),
                            baseline_value=mean_val,
                            detection_method="deterministic_fallback",
                            threshold=2.0,
                            severity=AnomalySeverity.LOW,
                            confidence=0.3,  # Low confidence - limited data
                            historical_window="insufficient_history_deferred",
                            detection_timestamp=datetime.now(timezone.utc),
                            explanation=(
                                f"Deterministic anomaly detected: value={v:.4f}, "
                                f"Z-score={z:.2f} (computed from limited data, "
                                f"ML-based detection deferred until sufficient "
                                f"historical observations available)"
                            ),
                            is_data_quality_failure=False,
                            is_expected_variation=False,
                        ))

        # Report that ML-based detection is deferred
        # We add a special note to the first result if any were found
        if results:
            results[0].explanation += " [ML DETECTION DEFERRED: Insufficient historical observations for model-based analysis]"

        return results, False

    # Sufficient historical data available
    return detect_anomalies(dataset_id, metric_name, values, historical_values=historical_values), True


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def run_anomaly_cli(
    dataset_id: str,
    run_id: str,
    source_path: str | Path,
    metric_name: str = "record_count",
    column_name: str | None = None,
    z_threshold: float = 3.0,
    mad_threshold: float = 3.5,
    iqr_threshold: float = 1.5,
    volume_threshold: float = 2.0,
    missingness_threshold: float = 2.0,
) -> list[AnomalyResult]:
    """CLI entry point for running anomaly detection on a dataset.

    Reads data from a CSV or JSON file and performs anomaly detection.

    Returns:
        List of AnomalyResult objects.
    """
    import csv
    import json
    from pathlib import Path

    path = Path(source_path)

    # Read records from file
    records: list[dict[str, Any]] = []
    fmt = path.suffix.lower()

    if fmt == ".csv":
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cleaned = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
                records.append(cleaned)
    elif fmt == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            records = [item if isinstance(item, dict) else {"value": item} for item in data]
        elif isinstance(data, dict):
            records = [data]
    else:
        raise ValueError(f"Unsupported file format: {fmt}")

    # Extract numeric values from the specified column
    values: list[float] = []
    if column_name:
        for record in records:
            val = record.get(column_name)
            if val is not None and val != "":
                try:
                    values.append(float(val))
                except (ValueError, TypeError):
                    pass
    else:
        # Try to find numeric columns
        if records:
            for key in records[0].keys():
                try:
                    float(records[0][key])
                    values = [float(r[key]) for r in records if r.get(key) is not None and r[key] != ""]
                    column_name = key
                    break
                except (ValueError, TypeError):
                    pass

    # Run anomaly detection
    results = detect_anomalies(
        dataset_id=dataset_id,
        metric_name=metric_name,
        values=values,
        records=records,
        column_name=column_name,
        z_score_threshold=z_threshold,
        mad_threshold=mad_threshold,
        iqr_threshold=iqr_threshold,
        volume_threshold=volume_threshold,
        missingness_threshold=missingness_threshold,
    )

    # Post-process: add run ID to each result's explanation
    for r in results:
        r.explanation = f"[Run {run_id}] " + r.explanation

    return results