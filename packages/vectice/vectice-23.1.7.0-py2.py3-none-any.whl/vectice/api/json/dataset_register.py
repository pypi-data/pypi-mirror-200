from __future__ import annotations

from vectice.models.resource.metadata import FilesMetadata, MetadataDB
from vectice.utils.deprecation import deprecate


class DatasetRegisterOutput(dict):
    @property
    def version(self) -> str:
        return str(self["version"])

    @property
    def use_existing_version(self) -> bool:
        return bool(self["useExistingVersion"])

    @property
    def use_existing_dataset(self) -> bool:
        return bool(self["useExistingDataset"])

    # TODO: complete the jobrun property
    @property
    def job_run(self) -> str:
        return str(self["jobRun"])


class DatasetRegisterInput(dict):
    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def data_sources(self) -> list[dict]:
        return list(self["datasetSources"])

    @property
    @deprecate(
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'inputs' property is renamed 'derived_from'. "
        "Using 'inputs' will raise an error in v{fail_at}. "
        "The property will be removed in v{remove_at}.",
    )
    def inputs(self) -> list[int]:
        return self.derived_from

    @property
    def derived_from(self) -> list[int]:
        return list(self["inputs"])


class DatasetSourceInput(dict):
    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def usage(self) -> str:
        return str(self["usage"])

    @property
    def origin(self) -> str:
        return str(self["origin"])

    @property
    def size(self) -> int:
        return int(self["size"])

    @property
    def dbs(self) -> list[MetadataDB]:
        return [MetadataDB(**item) for item in self["dbs"]]

    @property
    def files(self) -> FilesMetadata:
        return FilesMetadata(**self["files"])
