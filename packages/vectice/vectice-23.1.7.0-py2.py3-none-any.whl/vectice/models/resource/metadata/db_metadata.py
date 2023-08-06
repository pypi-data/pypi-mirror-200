from __future__ import annotations

from vectice.models.resource.metadata.base import (
    DatasetSourceType,
    DatasetSourceUsage,
    Metadata,
)


class DBMetadata(Metadata):
    """Class that describes metadata of dataset that comes from a database."""

    def __init__(
        self,
        dbs: list[MetadataDB],
        size: int,
        usage: DatasetSourceUsage | None = None,
        origin: str | None = None,
    ):
        """Initialize a DBMetadata instance.

        Parameters:
            dbs: The list of databases.
            size: The size of the metadata.
            usage: The usage of the metadata.
            origin: The origin of the metadata.
        """
        super().__init__(size=size, type=DatasetSourceType.DB, usage=usage, origin=origin)
        self.dbs = dbs

    def asdict(self) -> dict:
        return {
            "dbs": [db.asdict() for db in self.dbs],
            "size": self.size,
            "filesCount": None,
            "files": [],
            "type": self.type.value,
            "usage": self.usage.value if self.usage else None,
            "origin": self.origin,
        }


class Column:
    """Model a column of a dataset, like a database column."""

    def __init__(
        self,
        name: str,
        data_type: str,
        is_unique: bool | None = None,
        nullable: bool | None = None,
        is_private_key: bool | None = None,
        is_foreign_key: bool | None = None,
    ):
        """Initialize a column.

        Parameters:
            name: The name of the column.
            data_type: The type of the data contained in the column.
            is_unique: If the column uniquely defines a record.
            nullable: If the column can contain null value.
            is_private_key: If the column uniquely defines a record,
                individually or with other columns (can be null).
            is_foreign_key: If the column refers to another one,
                individually or with other columns (cannot be null).
        """
        self.name = name
        self.data_type = data_type
        self.is_unique = is_unique
        self.nullable = nullable
        self.is_private_key = is_private_key
        self.is_foreign_key = is_foreign_key

    def asdict(self) -> dict:
        return {
            "name": self.name,
            "dataType": self.data_type,
            "isUnique": self.is_unique,
            "nullable": self.nullable,
            "isPK": self.is_private_key,
            "isFK": self.is_foreign_key,
        }


class MetadataDB:
    def __init__(self, name: str, columns: list[Column], rows_number: int, size: int | None = None):
        """Initialize a MetadataDB instance.

        Parameters:
            name: The name of the table.
            columns: The columns that compose the table.
            rows_number: The number of row of the table.
            size: The size of the table.
        """
        self.name = name
        self.size = size
        self.rows_number = rows_number
        self.columns = columns

    def asdict(self) -> dict:
        return {
            "name": self.name,
            "size": self.size,
            "rowsNumber": self.rows_number,
            "columns": [column.asdict() for column in self.columns],
        }
