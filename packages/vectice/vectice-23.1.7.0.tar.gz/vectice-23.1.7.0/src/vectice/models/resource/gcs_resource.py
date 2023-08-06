from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.models.resource.base import Resource
from vectice.models.resource.metadata import DatasetSourceOrigin
from vectice.models.resource.metadata.files_metadata import File, FilesMetadata

if TYPE_CHECKING:
    from google.cloud.storage import Blob, Bucket, Client


class GCSResource(Resource):
    """Wrap columnar data and its metadata in GCS.

    Vectice stores metadata -- data about your dataset -- communicated
    with a resource.  Your actual dataset is not stored by Vectice.

    This resource wraps data that you have stored in Google Cloud
    Storage.  You assign it to a step.

    ```python
    from vectice import GCSResource
    from google.cloud.storage import Client

    my_service_account_file = "MY_SERVICE_ACCOUNT_JSON_PATH"  # (1)
    gcs_client = Client.from_service_account_json(json_credentials_path=my_service_account_file)  # (2)
    gcs_resource = GCSResource(
        gcs_client,
        bucket_name="my_bucket",
        resource_paths="my_folder/my_filename",
    )
    ```

    1. See [Service account credentials](https://developers.google.com/workspace/guides/create-credentials#service-account).
    1. See [GCS docs](https://cloud.google.com/python/docs/reference/storage/latest/modules).

    Note that these three concepts are distinct, even if easily conflated:

    * Where the data is stored
    * The format at rest (in storage)
    * The format when loaded in a running Python program

    Notably, the statistics collectors provided by Vectice operate
    only on this last and only in the event that the data is loaded as
    a pandas dataframe.
    """

    _origin = DatasetSourceOrigin.GCS.value

    def __init__(
        self,
        gcs_client: Client,
        bucket_name: str,
        resource_paths: str | list[str],
    ):
        """Initialize a GCS resource.

        Parameters:
            gcs_client: The `google.cloud.storage.Client` used
                to interact with Google Cloud Storage.
            bucket_name: The name of the bucket to get data from.
            resource_paths: The paths of the resources to get.
        """
        super().__init__()
        self.bucket_name = bucket_name
        self.resource_paths = resource_paths if isinstance(resource_paths, list) else [resource_paths]
        self.gcs_client = gcs_client

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
            origin=self._origin,
            files=files,
        )
        return metadata

    def _get_blob(self, path: str) -> Blob:
        from google.cloud import storage

        bucket: Bucket = storage.Bucket(self.gcs_client, name=self.bucket_name)
        blob = bucket.get_blob(blob_name=path)
        if blob is None:
            raise NoSuchGCSResourceError(self.bucket_name, path)
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


class NoSuchGCSResourceError(Exception):
    def __init__(self, bucket: str, resource: str):
        self.message = f"{resource} does not exist in the GCS bucket {bucket}."
        super().__init__(self.message)
