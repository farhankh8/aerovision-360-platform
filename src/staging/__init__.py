"""STAGING data layer package for AEROVISION 360.

Provides controlled transformation of RAW source snapshots into typed,
validated staging records with rejection and lineage handling.
"""

from src.staging.staging_processor import (
    DEFAULT_SCHEMA_VERSION,
    DEFAULT_TRANSFORMATION_VERSION,
    Disposition,
    QualityStatus,
    SourceStagingPlan,
    StagingError,
    StagingFormatError,
    StagingIntegrityError,
    StagingProcessor,
    StagingSourceContext,
    StagingStatus,
    StagedRecord,
    StagingResult,
    get_staging_plan,
    read_source_records,
)

__all__ = [
    "DEFAULT_SCHEMA_VERSION",
    "DEFAULT_TRANSFORMATION_VERSION",
    "Disposition",
    "QualityStatus",
    "SourceStagingPlan",
    "StagingError",
    "StagingFormatError",
    "StagingIntegrityError",
    "StagingProcessor",
    "StagingSourceContext",
    "StagingStatus",
    "StagedRecord",
    "StagingResult",
    "get_staging_plan",
    "read_source_records",
]
