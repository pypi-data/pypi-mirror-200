from __future__ import annotations

from vectice.models.resource.metadata.base import (
    DatasetSourceType,
    DatasetSourceUsage,
    Metadata,
)


class FilesMetadata(Metadata):
    """The metadata of a set of files."""

    def __init__(
        self,
        files: list[File],
        size: int,
        usage: DatasetSourceUsage | None = None,
        origin: str | None = None,
    ):
        """Initialize a FilesMetadata instance.

        Parameters:
            files: The list of files of the dataset.
            size: The size of the set of files.
            usage: The usage of the dataset.
            origin: Where the dataset files come from.
        """
        super().__init__(size=size, type=DatasetSourceType.FILES, origin=origin, usage=usage)
        self.files = files

    def asdict(self) -> dict:
        return {
            "files": [file.asdict() for file in self.files],
            "size": self.size,
            "type": self.type.value,
            "usage": self.usage.value if self.usage else None,
            "origin": self.origin,
        }


class File:
    """Describe a dataset file."""

    def __init__(
        self,
        name: str,
        size: int,
        fingerprint: str,
        created_date: str | None = None,
        updated_date: str | None = None,
        uri: str | None = None,
    ):
        """Initialize a file.

        Parameters:
            name: The name of the file.
            size: The size of the file.
            fingerprint: The hash of the file.
            created_date: The date of creation of the file.
            updated_date: The date of last update of the file.
            uri: The uri of the file.
        """
        self.name = name
        self.size = size
        self.fingerprint = fingerprint
        self.created_date = created_date
        self.updated_date = updated_date
        self.uri = uri

    def asdict(self) -> dict:
        return {
            "name": self.name,
            "size": self.size,
            "fingerprint": self.fingerprint,
            "createdDate": self.created_date,
            "updatedDate": self.updated_date,
            "uri": self.uri,
        }
