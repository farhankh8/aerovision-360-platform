"""RAW data ingestion package for AEROVISION 360.

Provides controlled ingestion of source files into the RAW layer.
Original files are never modified. Each ingestion run produces
immutable snapshots with SHA-256 checksums and full provenance metadata.
"""

from src.ingestion.raw_ingestion import (
    IngestionRun,
    IngestionResult,
    IngestionStatus,
    RawIngestionError,
    RawIngestionManager,
    SourceFormat,
    SourceMeta,
    SourceRecord,
    SnapshotRecord,
    create_default_source_registry,
)

__all__ = [
    "IngestionRun",
    "IngestionResult",
    "IngestionStatus",
    "RawIngestionError",
    "RawIngestionManager",
    "SourceFormat",
    "SourceMeta",
    "SourceRecord",
    "SnapshotRecord",
    "create_default_source_registry",
]
