from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.models.datasource.datawrapper.data_wrapper import DataWrapper
from vectice.models.resource.metadata import DatasetSourceOrigin, DatasetSourceUsage, DatasetType, File, FilesMetadata
from vectice.utils.deprecation import deprecate

if TYPE_CHECKING:
    from mypy_boto3_s3 import Client
    from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef, ObjectTypeDef


class S3DataWrapper(DataWrapper):
    """Deprecated. Wrap columnar data and its metadata in AWS S3.

    WARNING: **Wrappers are deprecated.**
    Instead, use [`Dataset`][vectice.models.dataset.Dataset]
    and [`S3Resource`][vectice.models.resource.s3_resource.S3Resource].

    Vectice stores metadata -- data about your dataset -- communicated
    with a DataWrapper.  Your actual dataset is not stored by Vectice.

    This DataWrapper wraps data that you have stored in AWS S3.  You
    assign it to a step.

    ```python
    from vectice import DatasetType, S3DataWrapper, connect
    from boto3.session import Session

    s3_session = Session(  # (1)
        aws_access_key_id="...",
        aws_secret_access_key="...",
        region_name="us-east-1",
    )
    s3_client = s3_session.client(service_name="s3")  # (2)

    my_project = connect(...)  # (3)
    my_phase = my_project.phase(...)  # (4)
    my_iter = my_phase.iteration()  # (5)

    my_iter.step_my_data = S3DataWrapper(
        s3_client,
        bucket_name="my_bucket",
        resource_path="my_resource_path",
        name="My origin dataset name",
        type=DatasetType.ORIGIN,
    )
    ```

    1. See [boto3 sessions][boto3.session.Session].
    1. See [boto3 session client][boto3.session.Session.client].
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
        s3_client: Client,
        bucket_name: str,
        resource_path: str,
        name: str,
        usage: DatasetSourceUsage | None = None,
        derived_from: list[int] | None = None,
        inputs: list[int] | None = None,
        type: DatasetType | None = None,
    ):
        """Initialize an S3 data wrapper.

        Parameters:
            s3_client: The client used to interact with Amazon s3.
            bucket_name: The name of the bucket to get data from.
            resource_path: The paths of the resources to get.
            name: The name of the DataWrapper (local to Vectice).
            usage: The usage of the dataset.
            derived_from: The list of dataset ids to create a new dataset from.
            inputs: Deprecated. Use `derived_from` instead.
            type: The type of the dataset.
        """
        if not derived_from and inputs:
            derived_from = inputs

        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.resource_path = resource_path
        super().__init__(name=name, type=type, usage=usage, derived_from=derived_from)

    def _fetch_data(self) -> dict[str, bytes]:
        s3_objects_list = self._get_s3_objects_list()
        datas = {}
        for s3_object in s3_objects_list["Contents"]:
            object_path = s3_object["Key"]
            data = self._get_aws_data(object_path)
            datas[f"{self.bucket_name}/{object_path}"] = data
        return datas

    def _get_aws_data(self, object_path: str):
        data_response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_path)
        return data_response["Body"].read()

    def _build_metadata(self) -> FilesMetadata:
        s3_objects_list = self._get_s3_objects_list()
        metadata = self._build_metadata_from_objects(s3_objects_list)
        return metadata

    def _get_s3_objects_list(self) -> ListObjectsV2OutputTypeDef:
        return self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.resource_path)

    def _build_metadata_from_objects(self, s3_objects_list: ListObjectsV2OutputTypeDef) -> FilesMetadata:
        if s3_objects_list["KeyCount"] == 0:
            raise NoSuchS3ResourceError(self.bucket_name, self.resource_path)
        s3_objects = s3_objects_list["Contents"]
        files, total_size = self._build_files_list_with_size(s3_objects)
        metadata = FilesMetadata(files=files, origin=DatasetSourceOrigin.S3.value, size=total_size, usage=self.usage)
        return metadata

    def _build_files_list_with_size(self, s3_objects: list[ObjectTypeDef]) -> tuple[list[File], int]:
        files: list[File] = []
        total_size = 0
        for object in s3_objects:
            if not self._is_s3_object_a_folder(object):
                name = object["Key"]
                size = object["Size"]
                file = File(
                    name=name,
                    size=size,
                    fingerprint=self._get_formatted_etag_from_object(object),
                    updated_date=object["LastModified"].isoformat(),
                    created_date=None,
                    uri=f"s3://{self.bucket_name}/{name}",
                )
                total_size += size
                files.append(file)
        return files, total_size

    @staticmethod
    def _get_formatted_etag_from_object(object: ObjectTypeDef) -> str:
        return str(object["ETag"].replace("'", "").replace('"', ""))

    @staticmethod
    def _is_s3_object_a_folder(object: ObjectTypeDef) -> bool:
        return bool(object["Key"].endswith("/"))


class NoSuchS3ResourceError(Exception):
    def __init__(self, bucket: str, resource: str):
        self.message = f"{resource} does not exist in the AWS s3 bucket {bucket}."
        super().__init__(self.message)

    def __str__(self):
        return self.message
