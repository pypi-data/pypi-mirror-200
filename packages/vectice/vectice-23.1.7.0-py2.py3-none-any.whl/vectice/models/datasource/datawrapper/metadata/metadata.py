from __future__ import annotations

from typing import Any

from vectice.models.resource.metadata.base import DatasetSourceOrigin, DatasetSourceType, DatasetType
from vectice.utils.deprecation import deprecate


def __getattr__(name: str) -> Any:
    if name == "SourceUsage":
        return _get_deprecated_source_usage()
    if name == "SourceOrigin":
        return _get_deprecated_source_origin()
    if name == "SourceType":
        return _get_deprecated_source_type()

    raise AttributeError(f"'{__name__}' module has no attribute '{name}'")


@deprecate(
    warn_at="23.1",
    fail_at="23.3",
    remove_at="23.4",
    reason="The `SourceUsage` enumeration is renamed `DatasetType`. "
    "Importing and using `SourceUsage` will fail in v{fail_at}. "
    "The enumeration will be removed in v{remove_at}.",
)
def _get_deprecated_source_usage():
    return DatasetType


@deprecate(
    warn_at="23.1",
    fail_at="23.3",
    remove_at="23.4",
    reason="The `SourceOrigin` enumeration is renamed `DatasetSourceOrigin`. "
    "Importing and using `SourceOrigin` will fail in v{fail_at}. "
    "The enumeration will be removed in v{remove_at}.",
)
def _get_deprecated_source_origin():
    return DatasetSourceOrigin


@deprecate(
    warn_at="23.1",
    fail_at="23.3",
    remove_at="23.4",
    reason="The `SourceType` enumeration is renamed `DatasetSourceType`. "
    "Importing and using `SourceType` will fail in v{fail_at}. "
    "The enumeration will be removed in v{remove_at}.",
)
def _get_deprecated_source_type():
    return DatasetSourceType


@deprecate(
    warn_at="23.1",
    fail_at="23.3",
    remove_at="23.4",
    reason="The `vectice.models.datasource.datawrapper.metadata.metadata` module "
    "is deprecated in favor the `vectice.models.resource.metadata.base` module. "
    "Importing from the deprecated module will fail in v{fail_at}, "
    "and the module will be removed in v{remove_at}.",
)
def _warn() -> None:
    pass


_warn()
