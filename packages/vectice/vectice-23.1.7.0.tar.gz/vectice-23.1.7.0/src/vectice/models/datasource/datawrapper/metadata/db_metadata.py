from __future__ import annotations

from typing import Any

from vectice.models.resource.metadata.base import (
    DatasetSourceOrigin,
    DatasetSourceType,
    DatasetSourceUsage,
    Metadata,
)
from vectice.models.resource.metadata.db_metadata import (
    Column,
    DBMetadata,
    MetadataDB,
)
from vectice.utils.deprecation import deprecate


def __getattr__(name: str) -> Any:
    attrs = {
        "DatasetSourceOrigin": DatasetSourceOrigin,
        "DatasetSourceType": DatasetSourceType,
        "DatasetSourceUsage": DatasetSourceUsage,
        "Metadata": Metadata,
        "DBMetadata": DBMetadata,
        "Column": Column,
        "MetadataDB": MetadataDB,
    }

    if name in attrs:
        return attrs[name]

    raise AttributeError(f"'{__name__}' module has no attribute '{name}'")


@deprecate(
    warn_at="23.1",
    fail_at="23.3",
    remove_at="23.4",
    reason="The `vectice.models.datasource.datawrapper.metadata.db_metadata` module "
    "is deprecated in favor the `vectice.models.resource.metadata.db_metadata` module. "
    "Importing from the deprecated module will fail in v{fail_at}, "
    "and the module will be removed in v{remove_at}.",
)
def _warn() -> None:
    pass


_warn()
