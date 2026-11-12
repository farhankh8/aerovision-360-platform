"""Quality manifest — persists validation results for audit and publication gates.

Writes to data/quality/ run manifests using atomic file writes.
Supports per-dataset results and a consolidated run summary.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .engine import QualityResult


class QualityManifest:
    """Persists a quality run manifest for audit and publication-gate purposes.

    Manifest structure under data/quality/:
    {
        "run_id": "20261104_154009_828238",
        "timestamp": "2026-11-04T15:40:09.871275+00:00",
        "source_root": "data/02_staging",
        "datasets": {
            "airline_reference_workbook": {
                "outcome": "passed",
                "failed_critical_rules": 0,
                "warning_rules": 0,
                "info_rules": 0,
                "failed_record_count": 0,
                "warning_record_count": 0,
                "rule_results": { ... }
            },
            ...
        }
    }
    """

    def __init__(
        self,
        run_id: str,
        source_root: str = "data/02_staging",
        manifest_dir: str = "data/quality",
    ) -> None:
        self.run_id = run_id
        self.source_root = Path(source_root)
        self.manifest_dir = Path(manifest_dir)
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.manifest_dir / f"quality_run_{run_id}.json"
        self._dataset_results: Dict[str, QualityResult] = {}

    def add_result(self, dataset_id: str, quality_result: QualityResult) -> None:
        """Add a QualityResult for a dataset and atomically write the manifest.

        Supports multiple dataset-result updates in a single quality run.
        The manifest file is only created on the first write; subsequent
        writes append additional dataset results to the existing manifest.
        Overwrite is only permitted for the manifest owned by this exact
        QualityManifest run ID.
        """
        self._dataset_results[dataset_id] = quality_result
        self._write_manifest()

    def _write_manifest(self) -> None:
        """Atomically write the quality run manifest.

        Supports multiple dataset-result updates in one quality run.
        The manifest is created on the first write.  On subsequent writes
        the entire dataset dictionary is rebuilt from all recorded results
        and written with overwrite=True because the file is known to belong
        to this run ID.
        """
        from src.utilities.io import write_json_atomic

        dataset_summaries: Dict[str, Dict[str, Any]] = {}
        for dataset_id, result in self._dataset_results.items():
            dataset_summaries[dataset_id] = result.to_dict()

        manifest_data: Dict[str, Any] = {
            "run_id": self.run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_root": str(self.source_root),
            "datasets": dataset_summaries,
        }

        # Permit overwrite only for the manifest belonging to this run ID.
        # The manifest filename includes the run_id, so concurrent runs
        # never conflict.  We use overwrite=True here because the file,
        # if it exists, was written by this QualityManifest instance.
        write_json_atomic(self.manifest_path, manifest_data, overwrite=True)

    def get_dataset_outcome(self, dataset_id: str) -> str | None:
        """Return the overall outcome (PASS/WARNING/FAIL) for a dataset, or None."""
        if dataset_id in self._dataset_results:
            return self._dataset_results[dataset_id].outcome
        return None

    def summary(self) -> Dict[str, Any]:
        """Consolidated summary across all datasets in this run."""
        outcomes: Dict[str, int] = {"passed": 0, "warning": 0, "failed": 0}
        total_failed_records = 0
        total_warning_records = 0

        for result in self._dataset_results.values():
            outcomes[result.outcome] += 1
            total_failed_records += result.failed_count
            total_warning_records += result.warning_count

        return {
            "run_id": self.run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_root": str(self.source_root),
            "total_datasets": len(self._dataset_results),
            "outcomes": outcomes,
            "total_failed_records": total_failed_records,
            "total_warning_records": total_warning_records,
        }

    def verify_checksums(self) -> Dict[str, bool]:
        """Verify that source SHA-256 hashes are recorded in results."""
        results: Dict[str, bool] = {}
        for dataset_id, result in self._dataset_results.items():
            results[dataset_id] = result.source_sha256 is not None
        return results