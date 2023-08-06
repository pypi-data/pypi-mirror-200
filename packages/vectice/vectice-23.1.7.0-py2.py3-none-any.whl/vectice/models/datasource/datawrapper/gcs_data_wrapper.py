from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.models.datasource.datawrapper.data_wrapper import DataWrapper
from vectice.models.resource.metadata import (
    DatasetSourceOrigin,
    DatasetSourceUsage,
    DatasetType,
    File,
    FilesMetadata,
)
from vectice.utils.deprecation import deprecate

if TYPE_CHECKING:
    from google.cloud.storage import Blob, Bucket, Client


class GcsDataWrapper(DataWrapper):
    """Deprecated. Wrap columnar data and its metadata in GCS.

    WARNING: **Wrappers are deprecated.**
    Instead, use [`Dataset`][vectice.models.dataset.Dataset]
    and [`GCSResource`][vectice.models.resource.gcs_resource.GCSResource].

    Vectice stores metadata -- data about your dataset -- communicated
    with a DataWrapper.  Your actual dataset is not stored by Vectice.

    This DataWrapper wraps data that you have stored in Google Cloud
    Storage.  You assign it to a step.

    ```python
    from vectice import DatasetType, GcsDataWrapper, connect
    from google.cloud.storage import Client

    my_service_account_file = "MY_SERVICE_ACCOUNT_JSON_PATH" # (1)
    gcs_client = Client.from_service_account_json(json_credentials_path=my_service_account_file)  # (2)

    my_project = connect(...)  # (3)
    my_phase = my_project.phase(...)  # (4)
    my_iter = my_phase.iteration()  # (5)

    my_iter.step_my_data = GcsDataWrapper(
        gcs_client,
        bucket_name="my_bucket",
        resource_paths="my_folder/my_filename",
        name="My origin dataset name",
        type=DatasetType.ORIGIN,
    )
    ```

    1. See [Service account credentials](https://developers.google.com/workspace/guides/create-credentials#service-account).
    1. See [GCS docs](https://cloud.google.com/python/docs/reference/storage/latest/modules).
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

    @deprecate(
        parameter="inputs",
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'inputs' parameter is renamed 'derived_from'. "
        "Using 'inputs' will raise an error in v{fail_at}. "
        "The parameter will be removed in v{remove_at}.",
    )
    def __init__(
        self,
        gcs_client: Client,
        bucket_name: str,
        resource_paths: str | list[str],
        name: str,
        usage: DatasetSourceUsage | None = None,
        derived_from: list[int] | None = None,
        inputs: list[int] | None = None,
        type: DatasetType | None = None,
    ):
        """Initialize a GCS data wrapper.

        Parameters:
            gcs_client: The `google.cloud.storage.Client` used
                to interact with Google Cloud Storage.
            bucket_name: The name of the bucket to get data from.
            resource_paths: The paths of the resources to get.
            name: The name of the DataWrapper (local to Vectice).
            usage: The usage of the dataset.
            derived_from: The list of dataset ids to create a new dataset from.
            inputs: Deprecated. Use `derived_from` instead.
            type: The type of the dataset.
        """
        if not derived_from and inputs:
            derived_from = inputs

        self.bucket_name = bucket_name
        self.resource_paths = resource_paths if isinstance(resource_paths, list) else [resource_paths]
        self.gcs_client = gcs_client
        super().__init__(name=name, type=type, usage=usage, derived_from=derived_from)

    def _fetch_data(self) -> dict[str, bytes]:
        datas = {}
        for path in self.resource_paths:
            blob = self._get_blob(path)
            datas[f"{self.bucket_name}/{path}"] = blob.download_as_bytes()
        return datas

    def _build_metadata(self) -> FilesMetadata:
        files = []
        size = 0
        for path in self.resource_paths:
            blob = self._get_blob(path)
            blob_file = self._build_file_from_blob(blob)
            files.append(blob_file)
            size += blob_file.size
        metadata = FilesMetadata(
            size=size,
            origin=DatasetSourceOrigin.GCS.value,
            files=files,
            usage=self.usage,
        )
        return metadata

    def _get_blob(self, path: str) -> Blob:
        from google.cloud import storage

        bucket: Bucket = storage.Bucket(self.gcs_client, name=self.bucket_name)
        blob = bucket.get_blob(blob_name=path)
        if blob is None:
            raise NoSuchGcsResourceError(self.bucket_name, path)
        blob.reload()
        return blob

    def _build_file_from_blob(self, blob: Blob) -> File:
        return File(
            name=blob.name,
            size=blob.size,
            fingerprint=blob.md5_hash,
            created_date=blob.time_created.isoformat(),
            updated_date=blob.updated.isoformat(),
            uri=f"gs://{self.bucket_name}/{blob.name}",
        )


class NoSuchGcsResourceError(Exception):
    def __init__(self, bucket: str, resource: str):
        self.message = f"{resource} does not exist in the GCS bucket {bucket}."
        super().__init__(self.message)

    def __str__(self):
        return self.message
