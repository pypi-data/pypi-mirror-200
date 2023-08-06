from __future__ import annotations

from vectice.models.resource.metadata.base import (
    DatasetSourceOrigin,
    DatasetSourceType,
    DatasetSourceUsage,
    DatasetType,
    Metadata,
)
from vectice.models.resource.metadata.db_metadata import Column, DBMetadata, MetadataDB
from vectice.models.resource.metadata.files_metadata import File, FilesMetadata
from vectice.utils.deprecation import deprecate

__all__ = [
    "DBMetadata",
    "Column",
    "MetadataDB",
    "DatasetSourceOrigin",
    "DatasetSourceUsage",
    "DatasetSourceType",
    "DatasetType",
    "File",
    "FilesMetadata",
    "Metadata",
]


@deprecate(
    warn_at="23.1",
    fail_at="23.3",
    remove_at="23.4",
    reason="The `vectice.models.datasource.datawrapper.metadata` module "
    "is deprecated in favor the `vectice.models.resource.metadata` module. "
    "Importing from the deprecated module will fail in v{fail_at}, "
    "and the module will be removed in v{remove_at}.",
)
def _warn() -> None:
    pass


_warn()
