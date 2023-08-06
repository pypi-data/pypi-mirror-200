from __future__ import annotations

import datetime
import glob
import hashlib
import logging
import os

from vectice.models.resource.base import Resource
from vectice.models.resource.metadata.base import DatasetSourceOrigin
from vectice.models.resource.metadata.files_metadata import File, FilesMetadata

_logger = logging.getLogger(__name__)


class FileResource(Resource):
    """Wrap columnar data and its metadata in a local file.

    Vectice stores metadata -- data about your dataset -- communicated
    with a resource.  Your actual dataset is not stored by Vectice.

    This resource wraps data that you have stored in a local file.

    ```python
    from vectice import FileResource, connect

    my_project = connect(...)  # (1)
    my_phase = my_project.phase(...)  # (2)
    my_iter = my_phase.iteration()  # (3)

    my_iter.step_my_data = FileResource(path="my/file/path")
    ```

    1. See [connection][vectice.Connection.connect].
    1. See [phases][vectice.models.Phase].
    1. See [iterations][vectice.models.Iteration].

    Note that these three concepts are distinct, even if easily conflated:

    * Where the data is stored
    * The format at rest (in storage)
    * The format when loaded in a running Python program

    Notably, the statistics collectors provided by Vectice operate
    only on this last and only in the event that the data is loaded as
    a pandas dataframe.
    """

    _origin = DatasetSourceOrigin.LOCAL.value

    def __init__(self, path: str):
        """Initialize a file resource.

        Parameters:
            path: The path of the file to wrap.

        Examples:
            The following example shows how to wrap a CSV file
            called `iris.csv` in the current directory:

            ```python
            from vectice import FileResource
            iris_trainset = FileResource(path="iris.csv")
            ```
        """
        super().__init__()
        self.path = path
        _logger.info(f"File: {path} wrapped successfully.")

    def _fetch_data(self) -> dict[str, bytes]:
        datas = {}
        for file in self.metadata.files:
            with open(file.name, "rb") as opened_file:
                datas[file.name] = opened_file.read()
        return datas

    def _build_metadata(self, path: str | None = None) -> FilesMetadata:
        if self.path is None:
            raise ValueError("Path can not be None.")
        files, total_size = self._file_visitor_list_builder(self.path, [])
        metadata = FilesMetadata(size=total_size, origin=self._origin, files=files)
        return metadata

    def _file_visitor_list_builder(self, path: str, files: list[File]) -> tuple[list[File], int]:
        total_size = 0
        if not os.path.exists(path):
            raise FileNotFoundError
        if os.path.isfile(path):
            file: File = self._build_file_from_path(path)
            total_size += file.size
            files.append(file)
        else:
            for entry_path in glob.glob(f"{path}/**", recursive=True):
                if os.path.isfile(entry_path):
                    glob_file: File = self._build_file_from_path(entry_path)
                    total_size += glob_file.size
                    files.append(glob_file)
        return files, total_size

    def _build_file_from_path(self, path: str) -> File:
        entry_stats: os.stat_result = os.stat(path)
        name = path.split("\\")[-1]
        return File(
            name=name,
            size=entry_stats.st_size,
            fingerprint=self._compute_digest_for_path(path),
            updated_date=self._convert_date_to_iso(entry_stats.st_mtime),
            created_date=self._convert_date_to_iso(self._get_created_date(entry_stats)),
            uri=f"file://{os.path.abspath(path)}",
        )

    @staticmethod
    def _get_created_date(entry_stats: os.stat_result) -> float:
        try:
            return float(entry_stats.st_birthtime)  # type: ignore[attr-defined]
        except AttributeError:
            return entry_stats.st_ctime

    @staticmethod
    def _compute_digest_for_path(path: str) -> str:
        sha = hashlib.sha256()
        bytes_array = bytearray(128 * 1024)
        mv = memoryview(bytes_array)
        with open(path, "rb", buffering=0) as file:
            n = file.readinto(mv)
            while n:
                sha.update(mv[:n])
                n = file.readinto(mv)
        return sha.hexdigest()

    @staticmethod
    def _convert_date_to_iso(timestamp: float) -> str:
        return datetime.datetime.fromtimestamp(timestamp).isoformat()
